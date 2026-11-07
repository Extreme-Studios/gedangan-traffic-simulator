"""Actual SUMO1.28 experiment runner, warm-up, trace, explicit mass balance.
No vClass ignoring, vehicle permission override or disconnected-path teleport.
"""
import copy,time,statistics,xml.etree.ElementTree as E
from datetime import timedelta
from collections import defaultdict,Counter
from .recovery_common import *
from .recovery_data import build_demand
from .recovery_network import build as build_network
from .recovery_routing import route_all,context
from .m04_demand import activate,registry,types_element,xml
def mean(v):return statistics.mean(v)if v else None
def run(request):
 req=copy.deepcopy(request);demand=build_demand(req);spec=req.get('scenario',{'id':'S00'});network,netmanifest=build_network(spec);netfile=network/'network.net.xml';home=activate();import traci
 from . import recovery_common,recovery_data,recovery_network,recovery_routing,recovery_observed
 sources={Path(m.__file__).name:sha(m.__file__)for m in [recovery_common,recovery_data,recovery_network,recovery_routing,recovery_observed]};sources[Path(__file__).name]=sha(__file__)
 inherited=[*sorted((ROOT/'backend/gedangan').glob('m04*.py')),ROOT/'configuration/railway-m05/pilot.json',ROOT/'simulation/network/m045/provisional/inspection.json']
 sources.update({str(p.relative_to(ROOT)):sha(p)for p in inherited})
 signature={'version':'recovery-engine-1','request':req,'cohort_sha256':demand['cohort_sha256'],'network_sha256':sha(netfile),'sources':sources,'registry_sha256':sha(ROOT/'configuration/demand-m04/vehicle-registry.json'),'sumo_sha256':sha(home/'bin/sumo.exe')};key=identity(signature)[:24];folder=RUNS/key;folder.mkdir(parents=True,exist_ok=True)
 if(folder/'result.json').exists():
  stored=load(folder/'input-manifest.json');assert stored==signature
  for name,h in load(folder/'output-manifest.json').items():assert sha(folder/name)==h
  return load(folder/'result.json')
 save(folder/'input-manifest.json',signature);save(folder/'demand.json',demand);save(folder/'progress.json',{'status':'ROUTING','run_id':key,'progress':0})
 try:
  rows=route_all(netfile,demand['requests']);baseline=route_all(PARENT,demand['requests']);bm={r['id']:r for r in baseline};sid=spec.get('id','S00');types={v['id']:v for v in registry()};routes=types_element(registry());delay=float(spec.get('deferral_s',600))if sid=='S04'else 0;heavy={'light_truck','medium_truck','heavy_truck','trailer','oversize'}
  for q in rows:
   q['original_depart_seconds']=q['depart_seconds'];q['deferred_seconds']=delay if q['vehicle_type_id']in heavy else 0;q['depart_seconds']+=q['deferred_seconds'];old=bm[q['id']];q['route_before']=old['edges'];q['route_after']=q['edges'];q['rerouted']=bool(old['edges']and q['edges']and old['edges']!=q['edges']);q['lost_route']=bool(old['edges']and not q['edges']);q['added_distance_m']=q.get('length_m',0)-old.get('length_m',0)if q['edges']and old['edges']else None;q['added_freeflow_s']=q.get('freeflow_s',0)-old.get('freeflow_s',0)if q['edges']and old['edges']else None
   if q['status']=='ROUTABLE':
    v=E.SubElement(routes,'vehicle',id=q['id'],type=q['vehicle_type_id'],depart=str(q['depart_seconds']),departLane='best',departSpeed='0');E.SubElement(v,'route',edges=' '.join(q['edges']))
  trains=req.get('train_times_s',[max(10,demand['warmup_s']-60),demand['warmup_s']+180])
  if not isinstance(trains,list)or len(trains)>20 or any(not isinstance(t,(int,float))or t<0 or t>demand['total_s']for t in trains):raise ValueError('Invalid explicit synthetic railway departure times')
  E.SubElement(routes,'vType',id='recovery_train',**{k:str(v)for k,v in{**load(ROOT/'configuration/railway-m05/pilot.json')['train'],'sigma':0,'minGap':10}.items()})
  trainroute=load(ROOT/'simulation/network/m051/provisional/rail-provenance.json')['route']
  for i,t in enumerate(trains):
   v=E.SubElement(routes,'vehicle',id='recovery_train_'+str(i),type='recovery_train',depart=str(t),departSpeed='0');E.SubElement(v,'route',edges=' '.join(trainroute))
  routes[:]=routes.findall('vType')+sorted(routes.findall('vehicle'),key=lambda e:(float(e.get('depart')),e.get('id')));xml(folder/'demand.rou.xml',routes);save(folder/'route-ledger.json',rows)
  add=E.Element('additional',{'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance','xsi:noNamespaceSchemaLocation':str(home/'data/xsd/additional_file.xsd')});tl=E.SubElement(add,'tlLogic',id='osm_859708050',programID='0')
  for k,v in load(ROOT/'configuration/railway-m05/pilot.json')['crossing'].items():E.SubElement(tl,'param',key=k,value=str(v))
  xml(folder/'controls.add.xml',add);cfg=E.Element('configuration');inp=E.SubElement(cfg,'input')
  for k,v in [('net-file',netfile),('route-files',folder/'demand.rou.xml'),('additional-files',folder/'controls.add.xml')]:E.SubElement(inp,k,value=str(v.resolve()))
  timing=E.SubElement(cfg,'time');E.SubElement(timing,'end',value=str(demand['total_s']));E.SubElement(timing,'step-length',value='.5');process=E.SubElement(cfg,'processing');E.SubElement(process,'time-to-teleport',value='-1');E.SubElement(process,'collision.action',value='warn');out=E.SubElement(cfg,'output')
  for k,v in [('fcd-output',folder/'fcd.xml'),('fcd-output.attributes','id,x,y,z,angle,speed,lane,pos,type'),('device.fcd.period','1'),('tripinfo-output',folder/'tripinfo.xml'),('tripinfo-output.write-unfinished','true'),('tripinfo-output.write-undeparted','true'),('summary-output',folder/'summary.xml'),('statistic-output',folder/'statistics.xml')]:E.SubElement(out,k,value=str(v.resolve())if isinstance(v,Path)else v)
  xml(folder/'run.sumocfg',cfg);save(folder/'progress.json',{'status':'STARTING_SUMO','progress':.02,'run_id':key});label='recovery_'+key;log=(folder/'sumo-stdout.txt').open('w');started=time.monotonic();traci.start([str(home/'bin/sumo.exe'),'-c',str((folder/'run.sumocfg').resolve()),'--seed',str(demand['seed']),'--xml-validation','always','--no-step-log','true','--duration-log.disable','true','--error-log',str((folder/'sumo-errors.log').resolve())],label=label,stdout=log);c=traci.getConnection(label)
  if req.get('signal_off')is True:c.trafficlight.setProgram('m05_gedangan','off')
  net,_,metadata,_=context(str(netfile.resolve()),sha(netfile));road={q['id']for q in rows if q['edges']};rowmap={q['id']:q for q in rows};departed=set();arrived=set();loaded=set(c.simulation.getLoadedIDList())&road;moved=set();teleports=[];collisions=[];illegal=[];closedentry=[];frames=[];events=[];previous={};edge_stats=defaultdict(lambda:{'speed_sum':0,'vehicle_seconds':0,'queue_seconds':0,'max_queue_count':0,'max_queue_extent_m':0,'actual_vehicle_ids':set(),'max_occupancy_count':0});warmstock=None;spillback=[];blocking_since={};travel={};allstates={};tls=c.trafficlight.getIDList();active=set();lastedge={};transitions=[];lanes={l.getID():l for e in net.getEdges(withInternal=True)for l in e.getLanes()};crossvias={q.get('via')for q in E.parse(netfile).getroot().findall('connection')if q.get('tl')=='osm_859708050'and not q.get('from').startswith('m05_rail_')};maxactive=0
  try:
   for step in range(round(demand['total_s']/.5)):
    if time.monotonic()-started>360:raise RuntimeError('Bounded SUMO wall-time360s exceeded; outputs retained with explicit failure')
    c.simulationStep();t=c.simulation.getTime();loaded.update(set(c.simulation.getLoadedIDList())&road);newdepart=set(c.simulation.getDepartedIDList());departed.update(newdepart&road);arrived.update(set(c.simulation.getArrivedIDList())&road);teleports.extend({'time':t,'id':v}for v in c.simulation.getStartingTeleportIDList());collisions.extend({'time':t,'id':v}for v in c.simulation.getCollidingVehiclesIDList())
    for v in newdepart:c.vehicle.subscribe(v,[64,66,67,81,86])
    if step%2:continue
    states=c.vehicle.getAllSubscriptionResults();sig={k:c.trafficlight.getRedYellowGreenState(k)for k in tls}
    for k,s in sig.items():
     if previous.get(k)!=s:events.append({'elapsed_s':t,'controller':k,'state':s});previous[k]=s
    by=defaultdict(list);positions=[];active=set()
    for vid,d in states.items():
     if not d:continue
     lane=d[81];speed=d[64];x,y=d[66];pos=d[86];train=vid not in road;typ='recovery_train'if train else rowmap[vid]['vehicle_type_id'];edge=lanes[lane].getEdge().getID();positions.append({'id':vid,'type':typ,'lane':lane,'edge':edge,'x':round(x,2),'y':round(y,2),'angle':d[67],'speed':round(speed,3),'pos':round(pos,2)})
     if train:continue
     active.add(vid)
     if speed>.1:moved.add(vid)
     cls=types[typ]['sumo_vclass']
     if not lanes[lane].allows(cls):illegal.append({'time':t,'id':vid,'lane':lane,'class':cls})
     if lane in crossvias and set(sig.get('osm_859708050',''))<=set('rR'):closedentry.append({'time':t,'id':vid,'lane':lane})
     if not edge.startswith(':'):
      st=edge_stats[edge];st['actual_vehicle_ids'].add(vid)
      if t>=demand['warmup_s']:st['speed_sum']+=speed;st['vehicle_seconds']+=1
      by[lane].append((vid,pos,speed,types[typ]['parameters']['length']))
      if lastedge.get(vid)not in [None,edge]:transitions.append({'time_s':t,'id':vid,'from':lastedge[vid],'to':edge})
      lastedge[vid]=edge
    maxactive=max(maxactive,len(active))
    if warmstock is None and t>=demand['warmup_s']:warmstock={'elapsed_s':t,'active_road_vehicles':len(active),'ids':sorted(active),'departed_before_measurement':len(departed)}
    queues={}
    for lane,vehicles in by.items():
     eid=lanes[lane].getEdge().getID();st=edge_stats[eid];st['max_occupancy_count']=max(st['max_occupancy_count'],len(vehicles));stopped=[v for v in vehicles if v[2]<.3]
     if not stopped:continue
     tail=min(v[1]-v[3]for v in stopped);front=max(v[1]for v in stopped);extent=front-tail;queues[lane]={'stopped':len(stopped),'extent_m':extent,'tail_m':tail,'boundary_censored':tail<=0}
     if t>=demand['warmup_s']:st['queue_seconds']+=1;st['max_queue_count']=max(st['max_queue_count'],len(stopped));st['max_queue_extent_m']=max(st['max_queue_extent_m'],extent)
     head=max(vehicles,key=lambda v:v[1])
     if head[2]<.3 and lanes[lane].getLength()-head[1]<10:
      links=c.vehicle.getNextLinks(head[0]);ntls=c.vehicle.getNextTLS(head[0]);red=bool(ntls and ntls[0][2]<30 and ntls[0][3]in'rRyY');down=links[0][0]if links else None
      if down and down in lanes and not red:
       dvs=by.get(down,[]);free=min((v[1]-v[3]for v in dvs),default=lanes[down].getLength());need=head[3]+c.vehicle.getMinGap(head[0]);blocked=free<need and any(v[2]<.3 for v in dvs)
       if blocked:
        blocking_since.setdefault(lane,t)
        if t-blocking_since[lane]>=5 and t>=demand['warmup_s']:spillback.append({'elapsed_s':t,'upstream_lane':lane,'downstream_lane':down,'entry_free_m':free,'required_m':need,'upstream_vehicle':head[0],'classification':'IN_MODEL_STORAGE_BLOCKAGE_PROXY_NOT_FIELD_VERIFIED'})
       else:blocking_since.pop(lane,None)
    if(step%4==0):frames.append({'elapsed_s':t,'wib':(datetime.fromisoformat(demand['elapsed_zero_wib'])+timedelta(seconds=t)).isoformat(),'measurement':t>=demand['warmup_s'],'vehicles':positions,'signals':sig,'queues':queues})
    if step%60==0:save(folder/'progress.json',{'status':'RUNNING_SUMO','run_id':key,'elapsed_s':t,'total_s':demand['total_s'],'active':len(active),'progress':.05+.9*t/demand['total_s']})
   running=set(c.vehicle.getIDList())&road;pending=set(c.simulation.getPendingVehicles())&road
  finally:c.close();log.close()
  trips={v.get('id'):dict(v.attrib)for v in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo')if v.get('id')in road};qcount=len(rows);routed=len(road);nfailed=qcount-routed;notdepart=routed-len(departed);notarr=qcount-len(arrived)
  assert qcount==routed+nfailed and routed==len(departed)+notdepart and len(departed)==len(arrived)+len(running)
  trace_ledger=[]
  for q in rows:
   trip=trips.get(q['id']);dur=float(trip['duration'])if trip and float(trip.get('depart','-1'))>=0 else None;got=q['id']in arrived;trace_ledger.append({**q,'loaded':q['id']in loaded,'departed':q['id']in departed,'moved':q['id']in moved,'arrived':got,'running_at_end':q['id']in running,'not_departed':q['id']in road and q['id']not in departed,'actual_duration_s':dur,'duration_censored':not got,'actual_waiting_s':float(trip['waitingTime'])if trip and dur is not None else None,'actual_depart_s':float(trip['depart'])if trip and dur is not None else None,'actual_arrival_s':float(trip['arrival'])if got else None})
  edge_result={}
  for eid,st in edge_stats.items():
   m=metadata.get(eid,{});entry={**{k:v for k,v in st.items()if k not in ['actual_vehicle_ids','speed_sum']},'actual_vehicle_count':len(st['actual_vehicle_ids']),'sampled_mean_speed_m_s':st['speed_sum']/st['vehicle_seconds']if st['vehicle_seconds']else None,'assigned_routes':sum(eid in q['edges']for q in rows),'name':m.get('name'),'road_function':m.get('road_function','concept_flyover'if eid.startswith('recovery_fo_')else'MISSING'),'lane_geometry_source':'SUMO derivative'if eid.startswith('recovery_fo_')else'Inherited OSM/SUMO'};edge_result[eid]=entry
  measurement=[q for q in trace_ledger if not q['warmup']];arrived_measure=[q for q in measurement if q['arrived']];arrivedall=[q for q in trace_ledger if q['arrived']];departure_rows=[q for q in trace_ledger if q['departed']];classcounts={cls:{'requested':sum(q['vehicle_type_id']==cls for q in rows),'routed':sum(q['vehicle_type_id']==cls and bool(q['edges'])for q in rows),'departed':sum(q['vehicle_type_id']==cls and q['departed']for q in trace_ledger),'arrived':sum(q['vehicle_type_id']==cls and q['arrived']for q in trace_ledger)}for cls in types}
  result={'status':'ACTUAL_SUMO_RESULT','run_id':key,'scenario':sid,'request':req,'calendar':demand['calendar'],'cohort_sha256':demand['cohort_sha256'],'network_sha256':sha(netfile),'network_path':str(netfile.relative_to(ROOT)),'classification':demand['status'],'is_observed_target':False,'engineering_status':netmanifest['classification'],'sumo_version':c.getVersion()if False else'1.28.0','total_elapsed_s':demand['total_s'],'horizon_s':demand['horizon_s'],'warmup_s':demand['warmup_s'],'requested':qcount,'routed':routed,'failed_routes':nfailed,'loaded':len(loaded),'departed':len(departed),'arrived':len(arrived),'running_at_end':len(running),'not_departed':notdepart,'not_arrived':notarr,'warmup_state':warmstock,'measurement_cohort':{'requested':len(measurement),'routed':sum(bool(q['edges'])for q in measurement),'arrived':len(arrived_measure),'arrived_only_mean_travel_s':mean([q['actual_duration_s']for q in arrived_measure]),'note':'Requested-at/after selected WIB; excludes warm-up requests from cohort but warm-up vehicles remain in traffic'},'arrived_only_mean_travel_s':mean([q['actual_duration_s']for q in arrivedall]),'departed_including_unfinished_mean_waiting_s':mean([q['actual_waiting_s']for q in departure_rows]),'actual_arrivals_during_measurement':sum(q['arrived']and q['actual_arrival_s']>=demand['warmup_s']for q in trace_ledger),'max_active_road_vehicles':maxactive,'throughput_arrivals_per_hour_measurement':sum(q['arrived']and q['actual_arrival_s']>=demand['warmup_s']for q in trace_ledger)*3600/demand['horizon_s'],'network_sampled_mean_speed_m_s':sum(st['speed_sum']for st in edge_stats.values())/max(1,sum(st['vehicle_seconds']for st in edge_stats.values())),'max_lane_queue_extent_m':max((s['max_queue_extent_m']for s in edge_result.values()),default=0),'spillback_proxy_samples':len(spillback),'spillback_definition':'>=5s upstream stopped head, no immediate red signal and downstream entry storage insufficient at1s samples; model proxy, not field validated or full causal proof','classes':classcounts,'rerouted':sum(q['rerouted']for q in rows),'lost_routes':sum(q['lost_route']for q in rows),'flyover_assigned':sum(any(e.startswith('recovery_fo_')for e in q['edges'])for q in rows),'actual_flyover_vehicles':len(set(v for e,s in edge_stats.items()if e.startswith('recovery_fo_')for v in s['actual_vehicle_ids'])),'teleports':teleports,'collisions':collisions,'illegal_permissions':illegal,'road_in_closed_crossing_samples':closedentry,'railway_schedule_classification':'SYNTHETIC_SCENARIO; no measured timetable/closure for target date','train_times_s':trains,'accounting':'Requested=Routed+Failed; Routed=Departed+Not departed; Departed=Arrived+Running; Not arrived=Requested-Arrived','quality':'REQUIRES_REVIEW'if teleports or collisions or illegal or closedentry else'NO_RECORDED_PERMISSION_COLLISION_TELEPORT_EVENTS','wall_s':time.monotonic()-started,'limitations':['No empirical2026 calibration','Road controller, train schedule and warm-up initial state assumptions explicit','Arrived-only travel time is censored; unfinished and failed trips retained','Network naming/OD coverage gaps remain; no invented diversion route']}
  save(folder/'vehicle-results.json',trace_ledger);save(folder/'edge-impact.json',edge_result);save(folder/'signals.json',events);save(folder/'transitions.json',transitions);save(folder/'spillback-proxy.json',spillback);save(folder/'playback.json',{'network_sha256':sha(netfile),'cohort_sha256':demand['cohort_sha256'],'actual_SUMO':True,'sample_s':2,'frames':frames});save(folder/'result.json',result);save(folder/'progress.json',{'status':'COMPLETE','run_id':key,'progress':1});save(folder/'output-manifest.json',{p.name:sha(p)for p in folder.iterdir()if p.is_file()and p.name!='output-manifest.json'});print(json.dumps({k:result[k]for k in ['run_id','scenario','requested','routed','arrived','running_at_end','failed_routes','flyover_assigned','quality','wall_s']}),flush=True);return result
 except Exception as exc:save(folder/'failure.json',{'error':str(exc),'request':req});save(folder/'progress.json',{'status':'FAILED','run_id':key,'error':str(exc)});raise
def compare(a,b):
 if a['cohort_sha256']!=b['cohort_sha256']or a['warmup_s']!=b['warmup_s']or a['horizon_s']!=b['horizon_s']or a['request'].get('seed',42)!=b['request'].get('seed',42):raise ValueError('INCOMPARABLE: cohort, seed, warm-up and horizon must match')
 if a['train_times_s']!=b['train_times_s']or bool(a['request'].get('signal_off',False))!=bool(b['request'].get('signal_off',False)):raise ValueError('Control sensitivity is not an equivalent intervention comparison: actual train schedule or signal-off state')
 af=RUNS/a['run_id'];bf=RUNS/b['run_id'];ae=load(af/'edge-impact.json');be=load(bf/'edge-impact.json');av={v['id']:v for v in load(af/'vehicle-results.json')};bv=load(bf/'vehicle-results.json');roadrows=[]
 for eid in sorted(set(ae)|set(be)):
  x,y=ae.get(eid,{}),be.get(eid,{});roadrows.append({'edge':eid,'road_function':y.get('road_function',x.get('road_function')),'name':y.get('name',x.get('name')),'baseline_assigned':x.get('assigned_routes',0),'after_assigned':y.get('assigned_routes',0),'assigned_delta':y.get('assigned_routes',0)-x.get('assigned_routes',0),'actual_vehicle_delta':y.get('actual_vehicle_count',0)-x.get('actual_vehicle_count',0),'queue_seconds_delta':y.get('queue_seconds',0)-x.get('queue_seconds',0),'max_queue_extent_delta_m':y.get('max_queue_extent_m',0)-x.get('max_queue_extent_m',0),'speed_delta_m_s':y['sampled_mean_speed_m_s']-x['sampled_mean_speed_m_s']if x.get('sampled_mean_speed_m_s')is not None and y.get('sampled_mean_speed_m_s')is not None else None})
 reroutes=[]
 for y in bv:
  x=av[y['id']]
  if x['edges']!=y['edges']or x['actual_duration_s']!=y['actual_duration_s']:reroutes.append({'id':y['id'],'od_id':y['od_id'],'class':y['vehicle_type_id'],'route_before':x['edges'],'route_after':y['edges'],'rerouted':x['edges']!=y['edges'],'route_lost':bool(x['edges']and not y['edges']),'added_distance_m':y.get('added_distance_m'),'travel_time_delta_s':y['actual_duration_s']-x['actual_duration_s']if x['arrived']and y['arrived']else None,'travel_time_censored':not(x['arrived']and y['arrived'])})
 return {'baseline':a['run_id'],'after':b['run_id'],'cohort_sha256':a['cohort_sha256'],'comparable':True,'arrived_delta':b['arrived']-a['arrived'],'not_arrived_delta':b['not_arrived']-a['not_arrived'],'road_impact':roadrows,'vehicle_route_and_time_changes':reroutes,'decision':'CONDITIONAL TRADEOFF - no automatic best solution or field effectiveness claim','new_bottleneck_candidates':sorted([r for r in roadrows if r['queue_seconds_delta']>0],key=lambda r:r['queue_seconds_delta'],reverse=True)[:20]}
if __name__=='__main__':
 import sys
 req=load(sys.argv[1])if len(sys.argv)>1 else {'date':'2026-08-04','time':'07:00','demand_mode':'REFERENCE_ESTIMATE','acknowledge_estimate':True,'horizon_s':300,'warmup_s':120,'scenario':{'id':'S00'},'seed':42};run(req)
