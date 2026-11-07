"""Exact M06 adapters and isolated unchanged-importer preview; no old writes."""
import csv,json,io,os,zipfile,importlib.util
from pathlib import Path
from collections import defaultdict
from datetime import timedelta
from contextlib import ExitStack
from .m04_demand import ROOT,load
from .m06_observations import KINDS,BASE,validate as m06_validate
from .m085_provenance import clock,interval,canonical,fingerprint,gate_source,now
from .m085_video_annotation import observation_time
from .m085_survey import uid,CLASSES,RAIL_EVENTS
from .m085_baseline import digest
HEADERS=load(ROOT/'configuration/calibration-m06/template-columns.json')
def event_time(store,c,e):
 return observation_time(store.get(c,e['media_id'],'media'),e.get('video_event_seconds',{}).get('timestamp',e['video_seconds'])) if e.get('media_id') else e.get('timestamp')
def common(s,kind,start,end,source,pid,event):
 a,b=clock(start),clock(end)
 if a>=b:raise ValueError('M06 membutuhkan interval observasi positif; lengkapi akhir pengamatan, jangan menciptakan durasi')
 return {'observation_id':'m085_'+fingerprint([s['id'],kind,start,end,event.get('event_id'),event.get('vehicle_class'),event.get('movement')])[:24],'kind':kind,'source_class':source,'date':a.date().isoformat(),'interval_start':start,'interval_end':end,'timezone':'Asia/Jakarta','location_id':s['location_id'],'approach':event.get('approach') or s['approach'],'direction':event.get('direction') or s['direction'],'vehicle_class':event.get('vehicle_class','all'),'method':event.get('method') or event.get('observation_method') or s['method'],'observer_source':s['observer_id'],'quality':'VERIFIED' if (s.get('review') or {}).get('decision')=='APPROVED' else 'PROVISIONAL','confidence':event.get('confidence','UNKNOWN'),'provenance_id':pid,'uncertainty':event.get('uncertainty'),'notes':None,**{k:None for k in KINDS[kind]}}
def notes(s,events,extra=None):
 ids=[e['event_id'] for e in events]
 return canonical({'survey_id':s['id'],'original_source_class':s['source_class'],'source_event_count':len(ids),'raw_ids_first20':ids[:20],'all_raw_ids_sha256':fingerprint(ids),'lineage_sidecar':'row-lineage.json','raw_sidecar':'raw-events.json','original_annotations':[{k:v for k,v in e.items() if k not in ['event_id','type']} for e in events] if len(events)<=3 else None,'extra':extra,'calibrated_baseline':False})
def materialize(store,c,s,for_comparison=False):
 events=store.events(c,s['id']);media=store.get(c,s['media_id'],'media') if s.get('media_id') else None;review=s.get('review') or {};source_error=None
 if review and review.get('content_hash')!=store.content_hash(c,s['id']):review={};source_error='Review snapshot berubah; ulangi review'
 try:source=gate_source(s,review,media)
 except ValueError as exc:
  source_error=str(exc);source='DEMO_SYNTHETIC' if for_comparison else None
 pid='M085_SOURCE_'+s['id'];rows=[];rejected=[];lineage={}
 def rejected_event(e,reason):rejected.append({'event_id':e.get('event_id'),'raw':{k:v for k,v in e.items() if not k.startswith('_')},'reason':reason})
 counts=[];coverage=[];strata=set()
 for e in events:
  try:
   if e['type']=='COUNT':
    e['_wall']=clock(event_time(store,c,e));counts.append(e);strata.add((e['approach'],e['direction'],e['movement'],e['vehicle_class']))
   elif e['type']=='COVERAGE':
    if e.get('media_id'):
     m=store.get(c,e['media_id'],'media');a=observation_time(m,e['review_start_s']);b=observation_time(m,e['review_end_s'])
    else:a,b=e.get('coverage_start') or e['interval_start'],e.get('coverage_end') or e['interval_end']
    if not a or not b:raise ValueError('VIDEO_TIME_ONLY')
    e['_start'],e['_end']=clock(a),clock(b)
    if not clock(s['start'])<=e['_start']<e['_end']<=clock(s['end']):raise ValueError('Coverage di luar sesi')
    coverage.append(e)
    for cls in e['classes']:strata.add((e.get('approach') or s['approach'],e.get('direction') or s['direction'],e.get('movement') or 'straight',cls))
  except Exception as ex:rejected_event(e,'Clock/coverage belum siap: '+str(ex))
 for approach,direction,movement,cls in sorted(strata):
  relevant=[v for v in coverage if cls in v['classes'] and (v.get('approach') or s['approach'])==approach and (v.get('direction') or s['direction'])==direction and (v.get('movement') or 'straight')==movement];group=[e for e in counts if (e['approach'],e['direction'],e['movement'],e['vehicle_class'])==(approach,direction,movement,cls)]
  boundaries={clock(s['start']),clock(s['end'])};cursor=clock(interval(s['start'])[1])
  while cursor<clock(s['end']):boundaries.add(cursor);cursor+=timedelta(minutes=15)
  for cov in relevant:boundaries.update([cov['_start'],cov['_end']])
  ordered=sorted(boundaries)
  for a,b in zip(ordered,ordered[1:]):
   inside=[e for e in group if a<=e['_wall']<b];matches=[v for v in relevant if v['_start']<=a and v['_end']>=b]
   if not inside and not matches:continue
   complete=len(matches)==1 and matches[0]['coverage_status']=='COMPLETE';raw=inside+matches
   # Internal datetime helpers never leak into raw evidence/JSON notes.
   cleaned=[{k:v for k,v in e.items() if not k.startswith('_')} for e in raw]
   try:
    if source is None:raise ValueError(source_error)
    row=common({**s,'review':review},'traffic_count',a.isoformat(),b.isoformat(),source,pid,{'vehicle_class':cls,'movement':movement,'approach':approach,'direction':direction});row['confidence']=min((e.get('confidence','UNKNOWN') for e in raw),key=lambda v:['UNKNOWN','LOW','MEDIUM','HIGH'].index(v)) if raw else 'UNKNOWN';row.update(count=len(inside) if complete else None,turning_movement=movement);row['notes']=notes(s,cleaned,{'partial_count':len(inside),'coverage':'COMPLETE' if complete else 'OVERLAPPING_COVERAGE_REVIEW' if len(matches)>1 else 'UNREVIEWED_OR_PARTIAL','lane_groups':sorted({e.get('lane_group','unknown') for e in inside}),'zero_is_observed':complete and not inside});rows.append(row);lineage[row['observation_id']]=[e['event_id'] for e in raw]
   except Exception as ex:rejected.append({'stratum':[a.isoformat(),b.isoformat(),approach,direction,movement,cls],'raw_event_ids':[e['event_id'] for e in raw],'reason':str(ex)})
 for e in events:
  if e['type'] in ['COUNT','COVERAGE','NOTE','INCIDENT']:continue
  try:
   if source is None:raise ValueError(source_error)
   effective_video_times={}
   if e.get('media_id'):
    source_media=store.get(c,e['media_id'],'media');effective_video_times={key:observation_time(source_media,sec) for key,sec in e.get('video_event_seconds',{}).items()}
   effective={**e,**effective_video_times}
   kind={'QUEUE':'queue','TRAVEL_TIME':'travel_time','SIGNAL':'signal','RAILWAY':'railway','GEOMETRY':'geometry'}[e['type']];start=event_time(store,c,e);end=effective.get('observation_end')
   if e['type']=='TRAVEL_TIME':
    start,end=effective.get('start_timestamp'),effective.get('end_timestamp')
    if e.get('media_id') and e.get('video_start_s') is not None:start,end=observation_time(source_media,e['video_start_s']),observation_time(source_media,e['video_end_s'])
   if e['type']=='SIGNAL':
    times=[effective.get(k) for k in ['green_start','green_end','yellow_start','yellow_end','red_start','red_end'] if effective.get(k)];start=min(times,key=clock) if times else start;end=max(times,key=clock) if len(times)>1 else end
   if e['type']=='RAILWAY':
    times=[effective.get(k) for k in RAIL_EVENTS if effective.get(k)];start=min(times,key=clock) if times else start;end=max(times,key=clock) if len(times)>1 else end
   row=common({**s,'review':review},kind,start,end,source,pid,e)
   if kind=='queue':row.update({k:e.get(k) for k in ['queue_length_m','queue_count','maximum_extent_m','definition','boundary_censored','lane_group']});row.update(length_unit='m',count_unit='vehicles',observation_point=e.get('observation_point') or s['location_id'])
   if kind=='travel_time':row.update({k:e[k] for k in ['travel_time_s','origin','destination','corridor']});row['sample_count']=1
   if kind=='signal':
    for color in ['green','yellow','red']:
     x,y=effective.get(color+'_start'),effective.get(color+'_end');row[color+'_s']=(clock(y)-clock(x)).total_seconds() if x and y else None
    row.update(cycle_s=(clock(end)-clock(start)).total_seconds() if all(effective.get(k) for k in ['green_start','red_end']) else None,offset_s=e.get('offset_s'),intersection_id=e.get('intersection_id') or s['location_id'],signal_head_group=e['signal_group'],phase_id=e['phase'])
   if kind=='railway':
    mapping={'warning_start':'warning_starts','closure':'road_fully_closed','train_approach':'train_approaches','train_pass':'train_passes','train_clearance':'train_clears','barrier_reopen':'barrier_begins_reopening','road_release':'road_traffic_released'};row.update({k:effective.get(v) for k,v in mapping.items()});row.update(train_id=e['train_id'],crossing_site_id=s['location_id'],train_movement=e.get('train_movement'))
   if kind=='geometry':row.update({k:e.get(k) for k in KINDS['geometry']})
   row['notes']=notes(s,[e],{'effective_video_times':effective_video_times,'extra_railway_events':{k:effective.get(k) for k in RAIL_EVENTS} if kind=='railway' else None,'length_status':'LENGTH NOT MEASURED' if kind=='queue' and e.get('queue_length_m') is None else None,'route':e.get('route'),'units':e.get('units'),'instrument':e.get('instrument'),'measurement_method':e.get('measurement_method'),'source':e.get('source')});rows.append(row);lineage[row['observation_id']]=[e['event_id']]
  except Exception as ex:rejected_event(e,str(ex))
 return rows,rejected,lineage
def provenance(store,c,s):
 review=s.get('review') or {};media=store.get(c,s['media_id'],'media') if s.get('media_id') else None
 if review and review.get('content_hash')!=store.content_hash(c,s['id']):review={}
 source=gate_source(s,review,media);pid='M085_SOURCE_'+s['id']
 return {pid:{'provenance_id':pid,'source_title':'M085 survey '+s['id'],'source_uri':'local-media-sha256:'+media['sha256'] if media else 'local-survey:'+s['id'],'source_class':source,'original_source_class':s['source_class'],'source_year':clock(s['start']).year,'accessed_on':now()[:10],'survey_period':{'start':s['start'],'end':s['end'],'timezone':'Asia/Jakarta'},'method':s['method'],'spatial_scope':s['location_id'],'license_notes':review.get('evidence_reference') or ('Synthetic software fixture, not observed Gedangan' if source=='DEMO_SYNTHETIC' else 'See local reviewed evidence'),'field_evidence_verified':source=='OBSERVED_FIELD' and bool(review.get('field_evidence_verified')),'limitations':['Import does not calibrate empirical baseline','Physical mapping requires independent review'],'human_review':review,'original_video_metadata':{k:v for k,v in (media or {}).items() if k!='local_path'}}}
def csv_bytes(kind,rows):
 out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=HEADERS[kind]);writer.writeheader()
 for r in rows:writer.writerow({k:('' if r[k] is None else canonical(r[k]) if isinstance(r[k],(dict,list)) else str(r[k]).lower() if isinstance(r[k],bool) else r[k]) for k in HEADERS[kind]})
 return out.getvalue().encode('utf-8-sig')
def isolated_import(path,prov,folder,demo,import_id):
 spec=importlib.util.spec_from_file_location('backend.gedangan.m085_private_m06',ROOT/'backend/gedangan/m06_observations.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.OBS=folder
 # Own the private importer's CSV handle lifetime without modifying legacy source.
 with ExitStack() as handles:
  class ManagedPath(type(Path())):
   def open(self,*args,**kwargs):return handles.enter_context(super().open(*args,**kwargs))
  module.Path=ManagedPath;return module.ingest(path,prov,import_id,demo)
def export_session(store,sid):
 with store.lock,store.connect() as c:
  s=store.get(c,sid,'session');rows,rejected,lineage=materialize(store,c,s)
  try:prov=provenance(store,c,s)
  except Exception:prov={}
  raw=[dict(r) for r in c.execute('SELECT * FROM raw_events WHERE session_id=?',(sid,))];corrections=[dict(r) for r in c.execute('SELECT * FROM corrections WHERE event_id IN (SELECT id FROM raw_events WHERE session_id=?)',(sid,))];recon=[r for r in store.objects(c,'recon') if r['location_id']==s['location_id']];imports=[r for r in store.objects(c,'geometry_import') if r['session_id']==sid];metadata={'session':s,'location':store.get(c,s['location_id'],'location'),'reconnaissance':recon,'geometry_source_documents':imports,'settings':store.get(c,'settings'),'observers':store.objects(c,'observer'),'media':[{k:v for k,v in m.items() if k!='local_path'} for m in store.objects(c,'media')],'raw_immutable':True,'contains_original_video':False,'empirical_baseline':'BLOCKED — DATA REQUIRED'}
  export_id=uid();staging=store.root/'export-staging'/export_id;staging.mkdir(parents=True);accepted=[];m06_rejected=[];flags=[]
  def write(name,value):(staging/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
  related={sid,s.get('media_id'),s['location_id'],'settings'}|{r['id'] for r in recon+imports+store.objects(c,'observer')+store.objects(c,'media')}
  write('rejected-commands.json',[dict(r) for r in c.execute('SELECT * FROM rejected_commands')]);write('adjudications.json',store.objects(c,'adjudication'));write('audit.json',[dict(r) for r in c.execute('SELECT * FROM audit')]);write('registry-versions.json',[dict(r) for r in c.execute('SELECT * FROM versions ORDER BY seq') if r['object_id'] in related]);write('raw-events.json',raw);write('corrections.json',corrections);write('metadata.json',metadata);write('provenance.json',prov);write('row-lineage.json',lineage);write('preimport-rejected.json',rejected)
  for kind in KINDS:
   selected=[r for r in rows if r['kind']==kind];write(kind+'.json',selected);(staging/(kind+'.csv')).write_bytes(csv_bytes(kind,selected))
   for fmt in ['json','csv']:
    a,b=isolated_import(staging/(kind+'.'+fmt),prov,staging/'m06-preview',s['source_class']=='SYNTHETIC_TEST',kind+'_'+fmt);accepted.append({'kind':kind,'format':fmt,'accepted':len(a),'rejected':len(b)});m06_rejected.extend({'kind':kind,'format':fmt,**v} for v in b)
  write('m06-rejected.json',m06_rejected);summary={'id':export_id,'session_id':sid,'rows':len(rows),'preimport_rejected':len(rejected),'import_preview':accepted,'m06_rejected':len(m06_rejected),'source_category':s['source_class'],'observed_baseline_promoted':False,'original_video_copied':False,'raw_event_count':len(raw),'status':'M06_COMPATIBLE_CANDIDATE' if not rejected and not m06_rejected and rows else 'NEEDS_REVIEW_OR_NO_EXPORTABLE_ROWS'};write('summary.json',summary)
  files={str(p.relative_to(staging)).replace('\\','/'):digest(p) for p in staging.rglob('*') if p.is_file()};write('manifest.json',{'version':'m085-1','files':files,'schema_sha256':{k:digest(ROOT/f'configuration/calibration-m06/{k}.schema.json') for k in KINDS},'M06_importer_sha256':digest(ROOT/'backend/gedangan/m06_observations.py'),'session_content_sha256':store.content_hash(c,sid)})
  dest=store.root/'exports'/export_id;dest.parent.mkdir(exist_ok=True);os.replace(staging,dest);archive=dest.with_suffix('.zip')
  with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
   for p in dest.rglob('*'):
    if p.is_file():z.write(p,p.relative_to(dest))
  return {**summary,'package_sha256':digest(archive),'files':list(files),'package_bytes':archive.stat().st_size}
