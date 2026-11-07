"""Presentation cache from immutable actual SUMO recordings, never invented motion."""
import json,gzip,math,os,xml.etree.ElementTree as E
from collections import Counter
from .m04_demand import ROOT,load,registry
from .m09_checkpoint import DOC,digest
from .m08_comparison import compare
from .m07_projection import baseline,project
from .m07_scenarios import read as growth
from .m08_scenarios import read as solution
OUT=ROOT/'presentation_demo/m09';CACHE=OUT/'cache'
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);data=json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode();temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(gzip.compress(data,compresslevel=6,mtime=0) if path.suffix=='.gz' else data);os.replace(temp,path)
def points(value):return [[float(v) for v in p.split(',')] for p in value.split()]
def scene(network):
 root=E.parse(network).getroot();lanes=[];edge_role={};inspection=load(ROOT/'simulation/network/m045/provisional/inspection.json')
 for e in inspection['edges']:edge_role[e['id']]=e.get('role') or e.get('road_role') or e.get('road_function','road')
 for e in root.findall('edge'):
  rail=e.get('id','').startswith('m05_rail_')
  for l in e.findall('lane'):
   lanes.append({'id':l.get('id'),'edge':e.get('id'),'internal':e.get('function')=='internal','rail':rail or ('rail' in l.get('allow','').split() and 'passenger' not in l.get('allow','')),'role':edge_role.get(e.get('id'),'rail' if rail else 'connector' if e.get('function')=='internal' else 'road'),'width':float(l.get('width','3.2')),'length':float(l.get('length')),'shape':points(l.get('shape')),'allow':l.get('allow'),'disallow':l.get('disallow')})
 by={l['id']:l for l in lanes};heads=[]
 for c in root.findall('connection'):
  if c.get('tl') and not c.get('from','').startswith(('m05_rail_',':')):
   lane=by.get(c.get('from')+'_'+c.get('fromLane'))
   if lane and len(lane['shape'])>1:heads.append({'controller':c.get('tl'),'link':int(c.get('linkIndex')),'lane':lane['id'],'point':lane['shape'][-1],'previous':lane['shape'][-2],'crossing':c.get('tl')=='osm_859708050'})
 plans=load(ROOT/'documentation/m06/survey-plan.json');presets={}
 for p in plans:
  lane=next((l for l in lanes if l['edge']==p['edge_id']),None)
  if lane:presets[p['location_id']]=lane['shape'][len(lane['shape'])//2][:2]
 location=root.find('location');bounds=[float(x) for x in location.get('convBoundary').split(',')];origin=[(bounds[0]+bounds[2])/2,(bounds[1]+bounds[3])/2]
 return {'version':'m09-1','network_sha256':digest(network),'source_network':str(network.relative_to(ROOT)),'crs':dict(location.attrib),'origin_local':origin,'transform':'worldX=SUMO.x-origin.x; worldZ=-(SUMO.y-origin.y); worldY=sourceZ or zero + render surface offset. Vehicle FCD front bumper -> visual center minus half length along heading.','bounds':bounds,'lanes':lanes,'junctions':[{'id':j.get('id'),'shape':points(j.get('shape'))} for j in root.findall('junction') if j.get('shape') and j.get('type') not in ['internal','rail_signal']],'heads':heads,'presets':presets,'crossing':[-2.43,-56.01],'short_lanes':[{'id':l['id'],'length':l['length']} for l in lanes if l['length']<1],'source_attribution':'© OpenStreetMap contributors · ODbL 1.0 · retained 2026-10-31 snapshot; SUMO-derived lane geometry','geometry_status':'GEOSPATIAL SOURCE / MODEL ASSUMPTION — not field surveyed','buildings':'No building footprints in retained OSM query. Optional off-road massing is STYLIZED CONTEXT, not actual building locations/heights.','refinement':'Render surface thickness, rail sleepers, markings, poles and boom dimensions only. Lane centerlines, junction boundaries and simulation topology unchanged.'}
def export_run(folder,result):
 required=['m08-result.json','m08-input.json','fcd.xml','playback.json','projection.json','lifecycle.json','route-ledger.json','summary.xml'];manifest=load(folder/'m08-output-manifest.json')
 for name in required:
  if name not in manifest or digest(folder/name)!=manifest[name]:raise ValueError('Source hash mismatch: '+str(folder/name))
 network=ROOT/result['network_path']
 if digest(network)!=result['network_sha256']:raise ValueError('Network hash mismatch')
 key=result['run_id'];dest=CACHE/'recordings'/key;dest.mkdir(parents=True,exist_ok=True);scene_key=result['network_sha256'][:20];sp=CACHE/'scenes'/(scene_key+'.json.gz')
 if not sp.exists():write(sp,scene(network))
 recorded=load(folder/'playback.json');reference={f['time']:f for f in recorded['frames']};samples=0;error=0;ids={};types=[];lanes={};vehicles=[];buffer=[];chunks=[];train_visible={};first={};last={};maximum_active=0;step=.5;shift=.5
 def flush():
  if not buffer:return
  name=f'{len(chunks):03d}.json.gz';p=dest/name;write(p,{'frames':buffer});chunks.append({'path':'recordings/'+key+'/'+name,'start':buffer[0]['t'],'end':buffer[-1]['t'],'frames':len(buffer),'sha256':digest(p),'bytes':p.stat().st_size});buffer.clear()
 for _,frame in E.iterparse(folder/'fcd.xml',events=['end']):
  if frame.tag!='timestep':continue
  t=round(float(frame.get('time'))+shift,3);poses=[];snapshot=reference.get(t);ref={v['id']:v for v in snapshot['vehicles']} if snapshot else {}
  for v in frame:
   vid=v.get('id');typ=v.get('type');lane=v.get('lane')
   if vid not in ids:ids[vid]=len(ids);vehicles.append({'id':vid,'type':typ});first[vid]=t
   last[vid]=t
   if lane not in lanes:lanes[lane]=len(lanes)
   x,y,speed,angle=(float(v.get(k)) for k in ['x','y','speed','angle']);poses.append([ids[vid],x,y,angle,speed,lanes[lane]])
   if vid in ref:
    distance=math.hypot(x-ref[vid]['x'],y-ref[vid]['y']);error=max(error,distance);samples+=1
   if typ=='m05_train':train_visible[vid]={'first':first[vid],'last':t}
  maximum_active=max(maximum_active,len(poses));buffer.append({'t':t,'p':poses});frame.clear()
  if len(buffer)>=200:flush()
 flush()
 if not samples or error>.03:raise ValueError('FCD/TraCI clock alignment not demonstrated')
 lifecycle=load(folder/'lifecycle.json');params={v['id']:v['parameters'] for v in registry()};params['m05_train']=load(ROOT/'configuration/railway-m05/pilot.json')['train'];trips=lifecycle['trips'];lifetimes=[]
 for i,v in enumerate(vehicles):
  q=trips.get(v['id'],{});v['first']=first[v['id']];v['last']=last[v['id']];v['length']=params[v['type']]['length'];v['width']=params[v['type']]['width'];v['height']=params[v['type']].get('height',3.5 if v['type']=='m05_train' else 2)
  if v['type']!='m05_train':lifetimes.append({'i':i,'depart':float(q['depart']) if q.get('depart') is not None else None,'arrival':float(q['arrival']) if q.get('arrival') is not None and float(q['arrival'])>=0 else None})
 weighted=lambda metric:sum(v[metric]['mean']*v['departed'] for v in result['od'].values() if v[metric]['mean'] is not None)/result['departed'] if result['departed'] else None
 metrics={k:result[k] for k in ['requested','routable','failed_routes','loaded','departed','arrived','running_at_end','not_departed','unserved_total_at_horizon','max_stopped_count','max_lane_queue_extent_m','verified_in_model_spillback','censored']};metrics.update(waiting_s=weighted('waiting_s_departed_including_unfinished'),elapsed_s=weighted('elapsed_trip_duration_s_departed_including_unfinished'),arrived_only_travel_s=None,throughput_arrivals_per_hour=result['arrived']/result['fixed_horizon_s']*3600)
 index={'id':key,'year':result['year'],'scenario':result['solution_id'],'growth':result['growth_scenario'],'seed':result['seed'],'scene':'scenes/'+scene_key+'.json.gz','scene_sha256':digest(sp),'network_sha256':result['network_sha256'],'cohort_sha256':result['cohort_sha256'],'effective_schedule_sha256':result['effective_schedule_sha256'],'vehicle_registry_sha256':result['m08_input']['vehicle_registry_sha256'],'sumo_version':result['sumo_version'],'demand':{'requested':result['requested'],'projection_hash':result['projection_hash'],'window_s':result['demand_window_s']},'time_window':[.5,2100],'step_s':step,'fcd_to_traci_offset_s':shift,'clock_evidence':{'matching_samples':samples,'maximum_xy_error_m':error,'source':'Retained 5s TraCI snapshots compared to FCD same vehicle at FCD time+0.5s'},'signal_state_resolution_s':1,'signal_note':'Recorded TraCI changes sampled every 1s; no invented transitions between records','source_demand':'SYNTHETIC / CONDITIONAL — not measured Gedangan','validity':'ACTUAL_SUMO_RESULT / NOT EMPIRICALLY CALIBRATED','source_run_folder':str(folder.relative_to(ROOT)),'source_files_sha256':{n:manifest[n] for n in required},'vehicles':vehicles,'lanes':list(lanes),'chunks':chunks,'events':recorded['events'],'lifetimes':lifetimes,'max_active':maximum_active,'train_visible':train_visible,'metrics':metrics,'OD':result['od'],'classes':result['class_lifecycle'],'deferral':result['deferral'],'teleports':result['teleports'],'collisions':result['collisions'],'illegal_permissions':result['illegal_permissions'],'intervention_manifest':result['intervention_manifest']}
 write(dest/'index.json.gz',index);return {k:index[k] for k in ['id','year','scenario','growth','seed','network_sha256','cohort_sha256','validity','metrics','max_active']}|{'index':'recordings/'+key+'/index.json.gz','index_sha256':digest(dest/'index.json.gz')},result
def main():
 OUT.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True);choice=load(ROOT/'documentation/m08/signal-training.json')['selected']['version'];runs=[];raw={}
 for folder in sorted((ROOT/'simulation/runs/m08').iterdir()):
  p=folder/'m08-result.json'
  if not p.exists() or folder.name.startswith('fresh-'):continue
  r=load(p)
  if r['seed']!=42 or r['network_variant']!='pilot-provisional' or r['solution_id']=='S01' and r['solution_version']!=choice:continue
  if r['illegal_permissions'] or r['teleports'] or r['collisions']:raise ValueError('Unsafe recording requires explicit review: '+r['run_id'])
  print('Export actual recording',r['solution_id'],r['year'],r['growth_scenario'],flush=True);run,original=export_run(folder,r);runs.append(run);raw[run['id']]=original
 comparisons=[]
 for r in runs:
  if r['scenario']=='S00':continue
  a=next((a for a in runs if a['year']==r['year'] and a['growth']==r['growth'] and a['scenario']=='S00'),None)
  if a:
   c=compare(raw[a['id']],raw[r['id']]);write(CACHE/'comparisons'/(r['id']+'.json'),c);comparisons.append({'baseline':a['id'],'intervention':r['id'],'comparable':c['parity']['comparable'],'path':'comparisons/'+r['id']+'.json'})
 projections=[];base=baseline()
 for year in range(2026,2041):
  for g in ['LOW','REFERENCE','HIGH']:
   p=project(year,growth(g),base);classes=Counter();ods=Counter()
   for cell in p['cells']:classes[cell['vehicle_class']]+=cell['count'];ods[cell['od_id']]+=cell['count']
   projections.append({'year':year,'growth':g,'requested':p['requested'],'projection_hash':p['projection_hash'],'classes':dict(classes),'OD':dict(ods),'validity':'ILLUSTRATIVE CONDITIONAL DEMAND — NOT A MEASURED FORECAST'})
 catalog=[solution(f'S{i:02d}') for i in range(8)];demo={'version':'m09-1','title':'GEDANGAN TRAFFIC SIMULATOR','developer':'EXTREME STUDIOS','status':'PARTIAL_PENDING_VISUAL_QA','runs':runs,'comparisons':comparisons,'projections':projections,'catalog':catalog,'registry':registry(),'default_run':next(r['id'] for r in runs if r['year']==2026 and r['scenario']=='S00' and r['growth']=='REFERENCE'),'preload_runs':[r['id'] for r in runs if r['growth']=='REFERENCE' and r['scenario']=='S00' or r['growth']=='REFERENCE' and r['year']==2026 and r['scenario']=='S01'],'field_data_status':'NOT YET COLLECTED','empirical_baseline':'BLOCKED — DATA REQUIRED','M10_started':False,'attribution':'© OpenStreetMap contributors / ODbL 1.0. Lane geometry derived by SUMO 1.28.0. Buildings, vegetation and street furniture are stylized context / model assumptions.'};write(CACHE/'catalog.json',demo);write(OUT/'M09_DEMO_MANIFEST.json',demo);print('M09 cache:',len(runs),'actual recordings,',len(comparisons),'paired comparisons',flush=True)
if __name__=='__main__':main()
