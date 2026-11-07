"""Evidence derived from actual FCD/routes; no claimed engineering approval."""
import xml.etree.ElementTree as E,statistics
from collections import Counter,defaultdict
from .recovery_common import *
from .recovery_engine import compare
def analyze(key):
 folder=RUNS/key;result=load(folder/'result.json');road=load(folder/'edge-impact.json');vehicles=load(folder/'vehicle-results.json');groups=defaultdict(list)
 for eid,r in road.items():
  name=(r.get('name')or'').lower();role=r['road_function'];region='MAIN_NB_SB'if role=='main_arterial_road'else'FRONTAGE'if role=='frontage_road'else'SUKODONO'if'sukodono'in name else'KETAJEN_RAIL_VICINITY'if'ketajen'in name else'CONCEPT_FLYOVER'if role=='concept_flyover'else'LOCAL_FEEDER_SERVICE'
  groups[region].append((eid,r))
 aggregate={name:{'edges':len(rows),'vehicle_seconds':sum(r['vehicle_seconds']for _,r in rows),'queued_lane_seconds':sum(r['queue_seconds']for _,r in rows),'max_queue_extent_m':max(r['max_queue_extent_m']for _,r in rows),'note':'Per-edge sums can count a vehicle on several road segments; not unique network volume'}for name,rows in groups.items()}
 manifest=load((ROOT/result['network_path']).parent/'manifest.json');fo_samples=0;maxheight=0;fo_ids=set();lane_transitions=Counter();last={};route_errors=[];permitted={(c.get('from'),c.get('to'))for c in E.parse(ROOT/result['network_path']).getroot().findall('connection')if not c.get('from').startswith(':')};vidmap={v['id']:v for v in vehicles}
 for v in vehicles:
  for a,b in zip(v['edges'],v['edges'][1:]):
   if(a,b)not in permitted:route_errors.append({'id':v['id'],'from':a,'to':b})
 for _,step in E.iterparse(folder/'fcd.xml',events=['end']):
  if step.tag!='timestep':continue
  for v in step:
   lane=v.get('lane','')
   if lane.startswith('recovery_fo_'):fo_samples+=1;maxheight=max(maxheight,float(v.get('z','0')));fo_ids.add(v.get('id'))
  step.clear()
 # Proxy fields from engine are candidates. Continuous confirmation is computed
 # separately so gaps between candidate samples never masquerade as duration.
 candidates=load(folder/'spillback-proxy.json');tracked={};episodes=[]
 for c in candidates:
  pair=(c['upstream_lane'],c['downstream_lane']);t=c['elapsed_s'];old=tracked.get(pair)
  if old and t-old['end_s']<=1.01:old['end_s']=t;old['samples']+=1
  else:
   if old and old['end_s']-old['start_s']>=5:episodes.append(old)
   tracked[pair]={'upstream_lane':pair[0],'downstream_lane':pair[1],'start_s':t,'end_s':t,'samples':1}
 episodes.extend(e for e in tracked.values()if e['end_s']-e['start_s']>=5)
 od={}
 for name in sorted({v['od_id']for v in vehicles}):
  vs=[v for v in vehicles if v['od_id']==name];arrived=[v for v in vs if v['arrived']];od[name]={'requested':len(vs),'routed':sum(bool(v['edges'])for v in vs),'failed':sum(not v['edges']for v in vs),'departed':sum(v['departed']for v in vs),'arrived':len(arrived),'running':sum(v['running_at_end']for v in vs),'not_departed':sum(v['not_departed']for v in vs),'arrived_only_mean_duration_s':statistics.mean(v['actual_duration_s']for v in arrived)if arrived else None,'unserved':len(vs)-len(arrived)}
 data={'run_id':key,'status':'PASS'if not route_errors else'FAIL','network_sha256':result['network_sha256'],'network_regions':aggregate,'OD':od,'sedati_jenggolo':'MISSING EXPLICIT NAMED SOURCE CORRIDOR; Ketajen may be local naming alias, not independently verified','station_access':'Recorded through station/rail vicinity is not proof of all station driveway connections','actual_flyover_FCD_samples':fo_samples,'actual_flyover_unique_vehicles':len(fo_ids),'actual_flyover_max_z_m':maxheight,'flyover_engineering_status':manifest['classification'],'route_connection_errors':route_errors,'spillback_span_candidate_samples':len(candidates),'sustained_storage_proxy_episodes':episodes,'spillback_limits':'Conservative consecutive candidate samples for >=5s; engine warm-start candidate delay can undercount. Not field verification or proof every blockage cause was distinguished.','new_bottlenecks':sorted([{'edge':e,**r}for e,r in road.items()],key=lambda x:x['queue_seconds'],reverse=True)[:20],'failed_by_reason':dict(Counter(v.get('reason','UNKNOWN')for v in vehicles if not v['edges']))};save(folder/'analysis.json',data);return data
def construction_before_during_after(before,during,after):
 a=load(RUNS/before/'result.json');b=load(RUNS/during/'result.json');c=load(RUNS/after/'result.json')
 if len({r['cohort_sha256']for r in [a,b,c]})!=1:raise ValueError('Construction triplet must share demand cohort')
 av={v['id']:v for v in load(RUNS/before/'vehicle-results.json')};bv={v['id']:v for v in load(RUNS/during/'vehicle-results.json')};cv={v['id']:v for v in load(RUNS/after/'vehicle-results.json')};rows=[];transfer=Counter()
 for vid,x in av.items():
  y,z=bv[vid],cv[vid]
  if x['edges']!=y['edges']or x['edges']!=z['edges']:
   rows.append({'id':vid,'class':x['vehicle_type_id'],'od':x['od_id'],'origin':x['origin_edge'],'destination':x['destination_edge'],'route_before':x['edges'],'route_during':y['edges'],'route_after':z['edges'],'during_status':y['status'],'during_added_distance_m':y['added_distance_m'],'after_added_distance_m':z['added_distance_m'],'during_added_actual_travel_s':y['actual_duration_s']-x['actual_duration_s']if x['arrived']and y['arrived']else None,'after_added_actual_travel_s':z['actual_duration_s']-x['actual_duration_s']if x['arrived']and z['arrived']else None,'censored_during':not(x['arrived']and y['arrived']),'censored_after':not(x['arrived']and z['arrived'])})
   if y['edges']:
    for edge in set(y['edges'])-set(x['edges']):transfer[edge]+=1
 result={'before':before,'during':during,'post_construction_concept':after,'cohort_sha256':a['cohort_sha256'],'rows':rows,'additional_assigned_volume_per_existing_alternative_edge':dict(transfer),'unaccommodated_during':b['failed_routes'],'construction_stage':'Synthetic full-edge closure, not approved traffic management plan','post_operation':'Executable unverified flyover concept, not official opening scenario','frontage_capacity_assumed_unlimited':False};save(DOC/'construction-triplet.json',result);return result
if __name__=='__main__':
 evidence=load(DOC/'acceptance-results.json');jobs={j['name']:j['run_id']for j in evidence['jobs']};rows=[]
 for name,key in jobs.items():
  a=analyze(key);rows.append({'name':name,'run_id':key,'analysis_status':a['status'],'flyover_unique':a['actual_flyover_unique_vehicles'],'flyover_max_z_m':a['actual_flyover_max_z_m'],'sustained_storage_proxy_episodes':len(a['sustained_storage_proxy_episodes'])})
 if all(n in jobs for n in ['morning_base','construction_full','flyover_A']):construction_before_during_after(jobs['morning_base'],jobs['construction_full'],jobs['flyover_A'])
 save(DOC/'network-impact-analysis.json',{'runs':rows,'status':'PASS'if all(r['analysis_status']=='PASS'for r in rows)else'FAIL'});print(json.dumps(rows),flush=True)
