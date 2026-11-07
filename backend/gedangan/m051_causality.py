"""Read-only priority/storage tracing and conservative causal event classification."""
import importlib.util,sys,math,xml.etree.ElementTree as E
from collections import defaultdict,Counter
from .m04_demand import ROOT,load,save,sha,activate
DOC=ROOT/'documentation/m051';RUNS=ROOT/'simulation/runs/m051';NET=ROOT/'simulation/network/m051'
POLICY=load(ROOT/'configuration/validation-m051/analysis-policy.json')
class Trace:
 def __init__(self,c,network):
  self.c=c;self.frames=[];self.step=0;self.tracked=set();self.meta={};root=E.parse(network).getroot();self.lanes={l.get('id'):l for e in root.findall('edge') for l in e.findall('lane')};self.incoming={c.get('to') for c in root.findall('connection') if not c.get('from','').startswith(':')};self.conns={(c.get('from')+'_'+c.get('fromLane'),c.get('to')+'_'+c.get('toLane')):dict(c.attrib) for c in root.findall('connection') if not c.get('from','').startswith(':')}
 def __getattr__(self,key):return getattr(self.c,key)
 def simulationStep(self,*args):
  result=self.c.simulationStep(*args);self.step+=1;c=self.c
  for vid in c.simulation.getDepartedIDList():c.vehicle.subscribe(vid,[64,66,81,86])
  if self.step%2==0:return result
  time=c.simulation.getTime()
  states=c.vehicle.getAllSubscriptionResults();vs={};by=defaultdict(list)
  # Subscriptions are managed by the unchanged M05 runner. Departing vehicles appear on its next step.
  for vid,d in states.items():
   if not d:continue
   if vid not in self.meta:self.meta[vid]={'length':c.vehicle.getLength(vid),'minGap':c.vehicle.getMinGap(vid),'class':c.vehicle.getVehicleClass(vid),'route':c.vehicle.getRoute(vid)}
   v={'id':vid,'lane':d[81],'pos':d[86],'speed':d[64],'length':self.meta[vid]['length'],'x':d[66][0],'y':d[66][1]};vs[vid]=v;by[v['lane']].append(v)
  observations=[]
  for lane,vehicles in by.items():
   if lane.startswith(':') or lane.startswith('m05_rail_'):continue
   head=max(vehicles,key=lambda v:v['pos']);remaining=float(self.lanes[lane].get('length'))-head['pos']
   if head['speed']<.3 and remaining<10:self.tracked.add(head['id'])
  for vid in self.tracked & vs.keys():
   v=vs[vid];meta=self.meta[vid];lane=v['lane'];links=c.vehicle.getNextLinks(vid);tls=c.vehicle.getNextTLS(vid);rawlink=links[0] if links else None;nextlink=([rawlink[0],rawlink[4],rawlink[1],rawlink[2],rawlink[3],rawlink[5],rawlink[6],rawlink[7]] if rawlink and isinstance(rawlink[1],bool) else rawlink)
   row={**v,'time':time,'route':meta['route'],'class':meta['class'],'minGap':meta['minGap'],'next_tls':tls[0] if tls else None,'next_link':nextlink,'gate_state':c.trafficlight.getRedYellowGreenState('osm_859708050') if 'osm_859708050' in c.trafficlight.getIDList() else None,'leader':c.vehicle.getLeader(vid,100),'is_lane_head':bool(by[lane] and max(by[lane],key=lambda w:w['pos'])['id']==vid),'distance_to_lane_end_m':float(self.lanes[lane].get('length'))-v['pos'],'valid_source_movement':False}
   if nextlink:
    down=nextlink[0];dvs=by.get(down,[]);length=float(self.lanes[down].get('length'));stopped=[w for w in dvs if w['speed']<.3];tail_front=min([w['pos'] for w in stopped],default=None);free=max(0,min([w['pos']-w['length'] for w in dvs],default=length));allow=self.lanes[down].get('allow');deny=self.lanes[down].get('disallow','').split();permitted=(allow is None or meta['class'] in allow.split()) and meta['class'] not in deny and 'all' not in deny
    row.update(downstream_lane=down,downstream_storage_m=length,entry_free_m=free,required_entry_space_m=meta['length']+meta['minGap'],queue_count=len(stopped),queue_tail_front_m=tail_front,queue_tail_rear_m=min([w['pos']-w['length'] for w in stopped],default=None),queue_head_m=max([w['pos'] for w in stopped],default=None),occupancy_raw=c.lane.getLastStepOccupancy(down),valid_source_movement=(lane,down) in self.conns and permitted,network_entry_boundary=lane.rsplit('_',1)[0] not in self.incoming,connector_blockers=[w for w in by.get(nextlink[1],[])],foe_vehicles=c.vehicle.getJunctionFoes(vid,30) if hasattr(c.vehicle,'getJunctionFoes') else [])
   observations.append(row)
  self.frames.append({'time':time,'observations':observations})
  return result

def classify(row):
 link=row.get('next_link');tls=row.get('next_tls');signal=link[5] if link else None
 if not link:return 'UNRESOLVED_NO_NEXT_LINK'
 if not row.get('valid_source_movement'):return 'UNRESOLVED_ROUTE_OR_PERMISSION'
 blocked=row.get('queue_count',0)>0 and row.get('entry_free_m',1e9)<row.get('required_entry_space_m',0)
 if blocked and (signal in ['r','R','y','Y','u'] or link[4] or not link[3]):return 'MULTI_CAUSAL_EVENT'
 if signal in ['r','R','y','Y','u']:
  return 'RAILWAY_QUEUE' if row.get('movement_controller')=='osm_859708050' else 'SIGNAL_QUEUE'
 if link[4] or not link[3]:return 'PRIORITY_OR_FOE_QUEUE'
 if not row.get('is_lane_head') or row['distance_to_lane_end_m']>=10:return 'FOLLOWING_OR_APPROACH_QUEUE'
 if row.get('connector_blockers'):return 'BLOCKED_CONNECTOR'
 if row.get('queue_count',0)>0 and row.get('queue_tail_rear_m',1e9)<=POLICY['queue_tail_m'] and row.get('queue_head_to_end_m',1e9)<=POLICY['queue_head_to_end_m'] and row.get('maximum_stopped_body_gap_m',1e9)<=POLICY['maximum_queue_body_gap_m'] and row['entry_free_m']<row['required_entry_space_m']:
  return 'STORAGE_BLOCKAGE_CANDIDATE'
 return 'UNRESOLVED_STOP_INSUFFICIENT_STORAGE_CAUSAL_PROOF'

def analyze_trace(folder):
 trace=load(folder/'priority-trace.json');rows=[r for f in trace for r in f['observations']];network=folder/'network.net.xml' if (folder/'network.net.xml').exists() else ROOT/load(folder/'result.json')['network_path'];nr=E.parse(network).getroot();control={(c.get('from')+'_'+c.get('fromLane'),c.get('to')+'_'+c.get('toLane')):c.get('tl') for c in nr.findall('connection') if not c.get('from','').startswith(':')}
 # Join full FCD footprints to priority samples. A lone stopped vehicle near entry is not a storage-filling queue.
 dims={v['id']:v['parameters']['length'] for v in load(ROOT/'configuration/demand-m04/vehicle-registry.json')['vehicles']};dims['m05_train']=80
 rows_at=defaultdict(list)
 for r in rows:rows_at[r['time']].append(r)
 for _,step in E.iterparse(folder/'fcd.xml',events=['end']):
  if step.tag!='timestep':continue
  t=float(step.get('time'))+.5
  if t in rows_at:
   stopped=defaultdict(list);footprints=defaultdict(list)
   for v in step.findall('vehicle'):
    footprints[v.get('lane')].append({'front':float(v.get('pos')),'length':dims.get(v.get('type'),4.5)})
    if float(v.get('speed'))<.3:stopped[v.get('lane')].append({'front':float(v.get('pos')),'length':dims.get(v.get('type'),4.5),'id':v.get('id')})
   for r in rows_at[t]:
    r['sumo_occupancy_raw']=r.get('occupancy_raw',r.get('occupancy_percent'));storage=r.get('downstream_storage_m',0);intervals=sorted((max(0,v['front']-v['length']),min(storage,v['front'])) for v in footprints.get(r.get('downstream_lane'),[]) if min(storage,v['front'])>max(0,v['front']-v['length']));covered=0;end=0
    for lo,hi in intervals:covered+=max(0,hi-max(end,lo));end=max(end,hi)
    r['occupancy_percent']=covered/storage*100 if storage else 0;r['occupancy_method']='DERIVED clipped union of all FCD front-assigned body footprints / lane length; bodies whose front is on another edge are not reconstructed. Raw TraCI occupancy retained separately without assuming percent units.'
    cars=sorted(stopped.get(r.get('downstream_lane'),[]),key=lambda v:v['front']);r['queue_footprints']=cars;r['queue_head_to_end_m']=r.get('downstream_storage_m',0)-max([v['front'] for v in cars],default=-1e9);r['maximum_stopped_body_gap_m']=max([b['front']-b['length']-a['front'] for a,b in zip(cars,cars[1:])],default=0)
  step.clear()
 for r in rows:
  r['movement_controller']=control.get((r['lane'],r.get('downstream_lane')))
  r['downstream_control_context']='RAILWAY_RED' if r.get('next_tls') and r['next_tls'][0]=='osm_859708050' and r['next_tls'][3] in 'rR' else 'SIGNAL_RED_AHEAD' if r.get('next_tls') and r['next_tls'][3] in 'rR' else None
 active={};events=[];samples=Counter()
 for f in trace:
  seen=set()
  for r in sorted(f['observations'],key=lambda r:(r['id'],r['lane'])):
   if r['speed']>=.3:continue
   cause=classify(r);samples[cause]+=1;key=(r['id'],r['lane'],r.get('downstream_lane'),cause);seen.add(key)
   if key not in active:active[key]={'id':len(events)+len(active),'vehicle':r['id'],'upstream_lane':r['lane'],'downstream_lane':r.get('downstream_lane'),'cause':cause,'start':r['time'],'end':r['time'],'evidence':[r]}
   else:active[key]['end']=r['time'];active[key]['evidence'].append(r)
  for key in list(active):
   if key not in seen:events.append(active.pop(key))
 events.extend(active.values());events.sort(key=lambda e:(e['start'],e['vehicle'],e['upstream_lane'],e['cause'],e['end']));output=[]
 for i,e in enumerate(events):
  e['event_id']=folder.name+'_'+str(i);e['duration_s']=e['end']-e['start'];e['confidence']='MEASURED_CONTROL_STATE' if e['cause'] in ['SIGNAL_QUEUE','RAILWAY_QUEUE'] else 'CANDIDATE';e['recovery']=None;e['right_censored']=False
  if e['cause']=='STORAGE_BLOCKAGE_CANDIDATE' and e['duration_s']>=POLICY['continuous_duration_s']:
   future=[r for r in rows if r['id']==e['vehicle'] and r['time']>e['end']];firstfree=next((r for r in future if r['lane']==e['upstream_lane'] and r.get('downstream_lane')==e['downstream_lane'] and r.get('entry_free_m',-1)>=r['length'] and r.get('valid_source_movement') and r.get('next_link') and r['next_link'][3] and not r['next_link'][4]),None)
   if firstfree and any(r['lane']!=e['upstream_lane'] or r.get('downstream_lane')!=e['downstream_lane'] or not r.get('next_link') or not r['next_link'][3] or r['next_link'][4] for r in future if r['time']<=firstfree['time']):firstfree=None
   if firstfree:
    recovered=next((r for r in future if r['time']>=firstfree['time'] and r['time']<=firstfree['time']+POLICY['movement_after_space_window_s'] and r['speed']>1 and r['lane'] in [e['downstream_lane'],firstfree['next_link'][1]]),None)
    if recovered:e['cause']='VERIFIED_SPILLBACK';e['confidence']='SIMULATION_CAUSAL_EVIDENCE';e['recovery']={'space_available_at':firstfree['time'],'queue_dissipation_lag_s':firstfree['time']-e['end'],'moving_at':recovered['time'],'delay_s':recovered['time']-firstfree['time'],'discharge_requirement':'Vehicle front is on the original via connector or original downstream lane; mere creeping on upstream lane is not recovery proof.','space_criterion':'Actual free entry length >= vehicle body length; minimum-gap envelope is used for conservative blockage screening, not a physical clearance certification.','evidence':[firstfree,recovered]}
   else:e['right_censored']=True
  e['contributing_contexts']=sorted({r['downstream_control_context'] for r in e['evidence'] if r.get('downstream_control_context')});e['queue_count_max']=max(r.get('queue_count',0) for r in e['evidence']);e['occupancy_max_percent']=max([r.get('occupancy_percent',0) for r in e['evidence']]);e['queue_extent_max_m']=max([(r.get('queue_head_m') or 0)-(r.get('queue_tail_rear_m') or 0) for r in e['evidence']]);e['upstream_blocked_count']=1;e['downstream_storage_m']=e['evidence'][0].get('downstream_storage_m');e['affected_edges']=[x.rsplit('_',1)[0] for x in [e['upstream_lane'],e['downstream_lane']] if x]
  if e['duration_s']>=1:output.append(e)
 save(folder/'causal-events.json',output);save(folder/'classification-summary.json',{'run':folder.name,'samples_by_class':dict(samples),'events_by_class':dict(Counter(e['cause'] for e in output)),'verified_spillback':sum(e['cause']=='VERIFIED_SPILLBACK' for e in output),'method':'Read-only vehicle-specific nextLinks open/priority/foe + FCD stopped footprints spanning lane (tail<=5m, head<=10m from end, gaps<=10m) + route/permission + continuous5s + storage recovery and movement within5s. Unproven cases remain unresolved.'})
 return output

def run_all():
 home=activate();import traci
 spec=importlib.util.spec_from_file_location('backend.gedangan.m051_private_m05',ROOT/'backend/gedangan/m05_behavior.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.NET=NET;m.RUNS=RUNS;m.DOC=DOC
 scenarios=[('A_free',False,(),90),('B_signal',True,(),90),('C_single',False,(70,),90),('E_combined',True,(70,),90),('F_high_free',False,(),240),('F_high_signal',True,(),240)]
 for seed in [42,43]:
  for name,signals,trains,n in scenarios:
   label=f'{name}_seed{seed}';folder=RUNS/label;original=traci.getConnection;proxy={}
   def get(label=None):
    c=original(label) if label is not None else original()
    if c not in proxy:proxy[c]=Trace(c,NET/'provisional/network.net.xml')
    return proxy[c]
   traci.getConnection=get
   try:r=m.run(home,label,n=n,seed=seed,signals=signals,trains=trains)
   finally:traci.getConnection=original
   trace=next(iter(proxy.values()));save(folder/'priority-trace.json',trace.frames);ev=analyze_trace(folder)
   save(folder/'run-manifest.json',{'SUMO':'1.28.0','seed':seed,'network_sha256':sha(NET/'provisional/network.net.xml'),'demand_sha256':sha(folder/'demand.json'),'matches_m05_demand':sha(folder/'demand.json')==sha(ROOT/'simulation/runs/m05'/label/'demand.json'),'baseline_run':f'simulation/runs/m05/{label}','no_speed_or_position_override':True,'events':len(ev)})
 if __name__=='__main__':pass
if __name__=='__main__':run_all()
