"""M15.5 real SUMO runner on immutable existing geometry; isolated scenario outputs."""
import time,statistics,xml.etree.ElementTree as E,gzip
from collections import Counter,defaultdict
from .simple_common import *
from .simple_demand import generate,default,integer
from .m155_network import catalog
from .simple_vehicles import registry,types_element
from .m04_demand import activate,xml

def controls(req,folder):
 add=E.Element('additional',{'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance','xsi:noNamespaceSchemaLocation':str(activate()/'data/xsd/additional_file.xsd')});s=req['signal'];tl=E.SubElement(add,'tlLogic',id='m05_gedangan',type='static',programID='m15',offset='0')
 for p in catalog()['signal']['phases']:
  key='green_s'if any(c in p['state']for c in'gG')else'yellow_s'if'y'in p['state']else'all_red_s';duration=float(s[key])
  if not 1<=duration<=180:raise ValueError('Signal duration must be 1..180 seconds')
  E.SubElement(tl,'phase',duration=str(duration),state=p['state'])
 rail=req['rail']
 if rail['direction']!='N_TO_S':raise ValueError('Reverse railway route unavailable in existing baseline')
 tl=E.SubElement(add,'tlLogic',id='osm_859708050',programID='0')
 for k,key in [('time-gap','closing_s'),('opening-delay','reopen_delay_s'),('opening-time','opening_s'),('min-green-time','recovery_s')]:
  value=float(rail[key])
  if not 0<=value<=120:raise ValueError('Rail parameter outside 0..120s')
  E.SubElement(tl,'param',key=k,value=str(value))
 E.SubElement(tl,'param',key='yellow-time',value='3');E.SubElement(tl,'param',key='space-gap',value='-1');xml(folder/'controls.add.xml',add)

def run(req,on_progress=None):
 protect();start=time.monotonic();demand=generate(req);horizon=demand['execution_horizon_s'];home=activate();names=['simple_common','simple_engine','simple_diagnostics','m156_common','m156_engine','m156_diagnostics','m155_common','m155_demand','m155_engine','m155_network','m14_vehicles','m155_diagnostics','m04_demand','m045_access','recovery_routing','recovery_common','m13_common','m15_demand','m15_network','m15_common'];source_paths=[Path(__file__).parent/(n+'.py')for n in names];snapshot={str(p.relative_to(ROOT)):p.read_text(encoding='utf-8')for p in source_paths};signature={'version':'simple-environment-only-1','request':req,'cohort_sha256':demand['cohort_sha256'],'network_sha256':sha(NETWORK),'sources':{str(p.relative_to(ROOT)):sha(p)for p in source_paths},'sumo_exe_sha256':sha(home/'bin/sumo.exe'),'registry_sha256':sha(ROOT/'configuration/demand-m04/vehicle-registry.json'),'policy_inspection_sha256':sha(ROOT/'simulation/network/m045/provisional/inspection.json')};key=identity(signature)[:24];folder=RUNS/key;folder.mkdir(parents=True,exist_ok=True)
 if(folder/'result.json').exists():return load(folder/'result.json')
 def progress(status,**values):
  value={'status':status,'run_id':key,**values};save(folder/'progress.json',value)
  if on_progress:on_progress(value)
 save(folder/'input-manifest.json',signature);save(folder/'source-snapshot.json',snapshot);save(folder/'demand.json',demand);progress('ROUTED',requested=demand['total'],routed=demand['routed'])
 try:
  home=activate();import traci
  controls(req,folder);routes=types_element();rows=demand['requests'];types={v['id']:v for v in registry()};vehicles=[]
  for r in rows:
   if r['edges']:
    v=E.Element('vehicle',id=r['id'],type=r['vehicle_type_id'],depart=str(r['depart_seconds']),departLane='best',departSpeed='0');E.SubElement(v,'route',edges=' '.join(r['edges']));vehicles.append(v)
  rail=req['rail'];passing=float(rail['passing_s'])
  if not 5<=passing<=60:raise ValueError('Assumed train passing time must be 5..60s')
  speed=80/passing;trainroute=load(ROOT/'simulation/network/m051/provisional/rail-provenance.json')['route'];railroot=E.parse(NETWORK).getroot();cross=next(j for j in railroot.findall('junction')if j.get('id')=='osm_859708050');crossxy=(float(cross.get('x')),float(cross.get('y')));rail_length=0
  # Requested arrival converted to an approximate free-flow departure, actual crossing time retained.
  for eid in trainroute:
   lane=next(e for e in railroot.findall('edge')if e.get('id')==eid).find('lane');points=[[float(x)for x in p.split(',')[:2]]for p in lane.get('shape').split()];rail_length+=float(lane.get('length'))
   if min(((x-crossxy[0])**2+(y-crossxy[1])**2)**.5 for x,y in points)<10:break
  lead=rail_length/speed+speed/1.2;trains=[]
  E.SubElement(routes,'vType',id='m05_train',vClass='rail',length='80',width='2.8',height='3.5',maxSpeed=str(speed),accel='.6',decel='1',sigma='0',minGap='10')
  if len(rail['arrivals_s'])>30:raise ValueError('At most 30 assumed trains per run')
  for i,arrival in enumerate(rail['arrivals_s']):
   target=float(arrival)+float(rail['delay_s'])
   if not 0<=target<=req['duration_s']:raise ValueError('Train arrival must lie within simulation horizon')
   depart=max(0,target-lead);v=E.Element('vehicle',id=f'm15_train_{i}',type='m05_train',depart=str(depart),departSpeed='0');E.SubElement(v,'route',edges=' '.join(trainroute));vehicles.append(v);trains.append({'id':v.get('id'),'requested_arrival_s':target,'depart_s':depart,'note':'Nominal free-flow arrival estimate; actual timing is recorded, not forced'})
  routes.extend(sorted(vehicles,key=lambda e:(float(e.get('depart')),e.get('id'))));xml(folder/'demand.rou.xml',routes);cfg=E.Element('configuration');inp=E.SubElement(cfg,'input')
  for k,p in [('net-file',NETWORK),('route-files',folder/'demand.rou.xml'),('additional-files',folder/'controls.add.xml')]:E.SubElement(inp,k,value=str(p.resolve()))
  timing=E.SubElement(cfg,'time');E.SubElement(timing,'end',value=str(horizon));E.SubElement(timing,'step-length',value='.5');proc=E.SubElement(cfg,'processing');E.SubElement(proc,'time-to-teleport',value='-1');E.SubElement(proc,'collision.action',value='warn');out=E.SubElement(cfg,'output')
  for k,v in [('fcd-output',folder/'fcd.xml'),('fcd-output.attributes','id,x,y,z,angle,speed,lane,pos,type'),('device.fcd.period','.5'),('tripinfo-output',folder/'tripinfo.xml'),('tripinfo-output.write-unfinished','true'),('tripinfo-output.write-undeparted','true'),('summary-output',folder/'summary.xml'),('statistic-output',folder/'statistics.xml')]:E.SubElement(out,k,value=str(v.resolve())if isinstance(v,Path)else v)
  xml(folder/'run.sumocfg',cfg);progress('STARTING_SUMO');log=(folder/'sumo-stdout.txt').open('w');label='m15_'+key;simstart=time.monotonic();traci.start([str(home/'bin/sumo.exe'),'-c',str((folder/'run.sumocfg').resolve()),'--seed',str(req['seed']),'--no-step-log','true','--duration-log.disable','true','--xml-validation','always','--error-log',str((folder/'sumo-errors.log').resolve())],label=label,stdout=log);c=traci.getConnection(label);version=c.getVersion();road={r['id']for r in rows if r['edges']};byid={r['id']:r for r in rows};loaded=set(c.simulation.getLoadedIDList())&road;departed=set();arrived=set();moved=set();illegal=[];collisions=[];teleports=[];events=[];previous={};frame_count=0;laneids=[];laneindex={};vmeta=[{'id':r['id'],'type':r['vehicle_type_id'],**{p:types[r['vehicle_type_id']]['parameters'][p]for p in ['length','width','height']}}for r in rows];vi={v['id']:i for i,v in enumerate(vmeta)}
  for train in trains:vi[train['id']]=len(vmeta);vmeta.append({'id':train['id'],'type':'m05_train','length':80,'width':2.8,'height':3.5})
  from .recovery_routing import context
  net,_,_,_=context(str(NETWORK.resolve()),sha(NETWORK));lane_map={l.getID():l for e in net.getEdges(withInternal=True)for l in e.getLanes()};hour_checkpoint=None;clearance_time=None;maxactive=0;maxqueue=0;maxextent=0;sum_speed=0;samples=0;lastwaiting=0;chunks=[];frames=[];boundary_samples=0
  from .simple_diagnostics import Diagnostics
  diagnostic=Diagnostics(rows,net,req.get('warmup_s',0))
  try:
   for step in range(round(horizon*2)):
    if time.monotonic()-simstart>1800:raise RuntimeError('SUMO wall-time limit 1800s exceeded; evidence retained')
    c.simulationStep();t=c.simulation.getTime();loaded.update(set(c.simulation.getLoadedIDList())&road);new=set(c.simulation.getDepartedIDList());departed.update(new&road);arrived.update(set(c.simulation.getArrivedIDList())&road);teleports.extend({'time':t,'id':v}for v in c.simulation.getStartingTeleportIDList());collisions.extend({'time':t,'id':v}for v in c.simulation.getCollidingVehiclesIDList())
    for vid in new:c.vehicle.subscribe(vid,[64,66,67,81,86])
    for controller in ['m05_gedangan','osm_859708050']:
     state=c.trafficlight.getRedYellowGreenState(controller)
     if previous.get(controller)!=state:events.append({'time':t,'controller':controller,'state':state});previous[controller]=state
    poses=[];diagnostic_states=[];queues=defaultdict(list);active=0;lastwaiting=0
    for vid,s in c.vehicle.getAllSubscriptionResults().items():
     if not s:continue
     lane=s[81];speed=s[64];x,y=s[66]
     if lane not in laneindex:laneindex[lane]=len(laneids);laneids.append(lane)
     diagnostic_states.append({'id':vid,'lane':lane,'speed':speed,'pos':s[86]})
     poses.append([vi[vid],round(x,2),round(y,2),round(s[67],2),round(speed,3),laneindex[lane]])
     if vid not in road:continue
     active+=1;sum_speed+=speed;samples+=1
     if speed>.1:moved.add(vid)
     if not lane_map[lane].allows(types[byid[vid]['vehicle_type_id']]['sumo_vclass']):illegal.append({'time':t,'id':vid,'lane':lane})
     if speed<.3:queues[lane].append((s[86],types[byid[vid]['vehicle_type_id']]['parameters']['length']));lastwaiting+=1
    diagnostic.sample(t,diagnostic_states,departed,arrived,c.simulation.getPendingVehicles()if t%10==0 else None)
    if t==req['duration_s']:hour_checkpoint={'time_s':t,'requested':demand['total'],'routed':len(road),'loaded':len(loaded),'departed':len(departed),'arrived':len(arrived),'active':active,'pending':len(road)-len(departed),'failed_routes':demand['failed_routes']}
    if t>=req['duration_s'] and len(arrived)==len(road) and clearance_time is None:clearance_time=t
    for lane,q in queues.items():
     maxqueue=max(maxqueue,len(q));tail=min(p-l for p,l in q);maxextent=max(maxextent,max(p for p,l in q)-tail)
     if tail<=2:boundary_samples+=1
    maxactive=max(maxactive,active);frames.append({'t':t,'p':poses});frame_count+=1
    if len(frames)>=120 or step==round(horizon*2)-1:
     name=f'frames-{len(chunks):04d}.json.gz'
     with gzip.open(folder/name,'wt',encoding='utf-8',compresslevel=3)as f:f.write(json.dumps(frames,separators=(',',':')))
     chunks.append(name);frames=[]
    if step%60==0:progress('RUNNING_SUMO',elapsed_s=t,total_s=horizon,active=active,departed=len(departed),arrived=len(arrived))
   running=set(c.vehicle.getIDList())&road
  finally:c.close();log.close()
  simwall=time.monotonic()-simstart;progress('COLLECTING_OUTPUT');trips={e.get('id'):dict(e.attrib)for e in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo')};ledger=[]
  for r in rows:
   trip=trips.get(r['id']);ledger.append({**r,'loaded':r['id']in loaded,'departed':r['id']in departed,'moved':r['id']in moved,'arrived':r['id']in arrived,'active':r['id']in running,'tripinfo':trip})
  mean=lambda xs:statistics.mean(xs)if xs else None
  result={'status':'ACTUAL_SUMO_RESULT','run_id':key,'classification':demand['classification'],'request':req,'execution_horizon_s':horizon,'demand_duration_s':req['duration_s'],'hour_checkpoint':hour_checkpoint,'clearance_time_s':clearance_time,'additional_discharge_s':clearance_time-req['duration_s']if clearance_time is not None else None,'network_version':'m155-existing-provisional-1','cohort_sha256':demand['cohort_sha256'],'network_sha256':sha(NETWORK),'sumo_version':version,'requested':demand['total'],'routed':len(road),'failed_routes':demand['failed_routes'],'loaded':len(loaded),'departed':len(departed),'moved':len(moved),'arrived':len(arrived),'active':len(running),'not_departed':len(road)-len(departed),'waiting_at_end':lastwaiting,'max_active':maxactive,'mean_speed_m_s':sum_speed/samples if samples else None,'arrived_only_mean_travel_s':mean([float(trips[v]['duration'])for v in arrived]),'departed_mean_waiting_s':mean([float(trips[v]['waitingTime'])for v in departed]),'throughput_arrivals_per_hour':len(arrived)*3600/req['duration_s'],'max_lane_queue_count':maxqueue,'max_queue_extent_m':maxextent,'spillback_boundary_samples':boundary_samples,'spillback_definition':'Stopped tail at lane start at 0.5s samples: storage-boundary proxy only; no causal spillback claim','teleports':teleports,'collisions':collisions,'illegal_permissions':illegal,'train_schedule':trains,'signal_transitions':len(events),'classes':{k:{state:sum(r['vehicle_type_id']==k and(bool(r['edges'])if state=='routed'else r.get(state,False))for r in ledger)for state in ['routed','loaded','departed','moved','arrived','active']}for k in types},'generation_wall_s':simstart-start,'simulation_wall_s':simwall,'total_wall_s':time.monotonic()-start,'playback_frames':frame_count,'quality':'REQUIRES_REVIEW'if illegal or collisions or teleports else'NO_RECORDED_PERMISSION_COLLISION_TELEPORT_EVENTS','limitations':['Manual/random inputs are not observations or calibrated forecasts','Blocked demand retained; pending and unfinished trips counted separately','No bicycle permission in existing baseline','Only mapped one-way rail direction supported','Train arrival nominal estimate; actual closure states in signals.json','Queue extent is sampled stopped span, not surveyed queue','No field swept-path clearance certificate for trailer; inherited provisional screens only']}
  assert result['requested']==result['routed']+result['failed_routes'];assert result['routed']==result['departed']+result['not_departed'];assert result['departed']==result['arrived']+result['active'];assert sha(NETWORK)==signature['network_sha256']
  diagnostic.finish(ledger,result,folder)
  result['source_demand_window_unchanged']=True
  result['execution_hours']=horizon/3600
  save(folder/'vehicle-results.json',ledger);save(folder/'signals.json',events);save(folder/'playback-index.json',{'id':key,'actual_SUMO':True,'sample_s':.5,'scenario':'S00','year':int(req['date'][:4]),'growth':demand['classification'],'duration_s':horizon,'demand_duration_s':req['duration_s'],'vehicles':vmeta,'lanes':laneids,'chunks':chunks,'events':events,'metrics':result});save(folder/'result.json',result);progress('COMPLETE');save(folder/'output-manifest.json',{p.name:sha(p)for p in folder.iterdir()if p.is_file()and p.name!='output-manifest.json'});return result
 except Exception as exc:progress('FAILED',error=str(exc));save(folder/'failure.json',{'error':str(exc)});raise

if __name__=='__main__':
 import sys
 request=load(sys.argv[1])if len(sys.argv)>1 else default();print(json.dumps(run(request),ensure_ascii=False),flush=True)
