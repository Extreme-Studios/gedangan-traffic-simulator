"""Sequential real SUMO runs; immutable networks; strict route/failure accounting."""
import importlib.util,xml.etree.ElementTree as E,time,statistics,ctypes
from ctypes import wintypes
from collections import Counter,defaultdict
from pathlib import Path
from .m04_demand import ROOT,load,save,sha,xml,execute,activate,registry,types_element,ProcessMemory
from .m07_growth import fingerprint,LABEL
from .m07_projection import baseline,project,requests
from .m07_scenarios import read
from .m051_causality import Trace,analyze_trace
RUNS=ROOT/'simulation/runs/m07';DOC=ROOT/'documentation/m07';VERSION='m07-1'
NETWORKS={'pilot-provisional':ROOT/'simulation/network/m051/provisional/network.net.xml','pilot-strict':ROOT/'simulation/network/m051/strict/network.net.xml','corrected-provisional':ROOT/'simulation/network/m045/provisional/network.net.xml'}
def screens():
 spec=importlib.util.spec_from_file_location('m07_private_access',ROOT/'backend/gedangan/m045_access.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.install_screens();return m
def route(folder,qs,network,mode,home):
 m=screens();inspection=load(ROOT/f'simulation/network/m045/{mode}/inspection.json');edges={e['id']:e for e in inspection['edges']};vs={v['id']:v for v in registry()}
 import sumolib
 net=sumolib.net.readNet(str(network),withInternal=True);root=E.parse(network).getroot();connections=[]
 for c in root.findall('connection'):
  if c.get('from').startswith(':'):continue
  allowed=[v for v in ['motorcycle','passenger','delivery','bus','truck','trailer'] if (c.get('allow') is None or v in c.get('allow').split()) and c.get('disallow')!='all' and v not in c.get('disallow','').split()]
  connections.append({'from':c.get('from'),'to':c.get('to'),'fromLane':int(c.get('fromLane')),'toLane':int(c.get('toLane')),'allowed_vclasses':allowed})
 trips=E.Element('routes');rows=[]
 for q in qs:
  reason=m.type_screen_impl(q,vs[q['vehicle_type_id']],edges,net);rows.append({**q,'reason':reason,'route_status':'NOT_ROUTABLE','edges':[]})
  if reason is None:E.SubElement(trips,'trip',id=q['id'],type=q['vehicle_type_id'],depart=str(q['depart_seconds']),**{'from':q['origin_edge'],'to':q['destination_edge']},departLane='best',departSpeed='0')
 xml(folder/'trips.xml',trips);xml(folder/'types.rou.xml',types_element(registry()))
 log=execute([home/'bin/duarouter.exe','-n',network,'-r',str(folder/'types.rou.xml')+','+str(folder/'trips.xml'),'-o',folder/'routed.rou.xml','--repair','false','--ignore-errors','true','--seed','42','--no-step-log','true'],folder/'routing-process.json')
 if log['returncode']:raise RuntimeError('DUAROUTER process failed; output retained')
 emitted={v.get('id'):v.find('route').get('edges').split() for v in E.parse(folder/'routed.rou.xml').getroot().findall('vehicle') if v.find('route') is not None}
 for row in rows:
  if row['reason']:continue
  ids=emitted.get(row['id']);reason=m.route_screen_impl(ids,row,vs[row['vehicle_type_id']],edges,net,connections) if ids else 'DUAROUTER_NO_ROUTE'
  if reason:row['reason']=reason
  else:row.update(edges=ids,route_status='ROUTABLE',reason='Actual DUAROUTER + inherited M04.5 source/access/width/turn/conditional/trailer screens')
 save(folder/'route-ledger.json',rows);return rows,net
class Resource:
 def __init__(self,pid):
  self.k=ctypes.WinDLL('kernel32',use_last_error=True);self.ps=ctypes.WinDLL('psapi',use_last_error=True);self.k.OpenProcess.restype=wintypes.HANDLE;self.k.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];self.k.CloseHandle.argtypes=[wintypes.HANDLE];self.ps.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(ProcessMemory),wintypes.DWORD];self.k.GetProcessTimes.argtypes=[wintypes.HANDLE]+[ctypes.POINTER(wintypes.FILETIME)]*4;self.h=self.k.OpenProcess(0x0410,False,pid);self.peak=0;self.cpu=None
 def sample(self):
  if not self.h:return
  mem=ProcessMemory();mem.cb=ctypes.sizeof(mem)
  if self.ps.GetProcessMemoryInfo(self.h,ctypes.byref(mem),mem.cb):self.peak=max(self.peak,mem.PeakWorkingSetSize)
  ft=[wintypes.FILETIME() for _ in range(4)]
  if self.k.GetProcessTimes(self.h,*[ctypes.byref(v) for v in ft]):self.cpu=sum((ft[i].dwHighDateTime<<32)+ft[i].dwLowDateTime for i in [2,3])/1e7
 def close(self):
  if self.h:self.k.CloseHandle(self.h)
def signature(projection,network,seed,options):
 sources={p.name:sha(p) for p in [ROOT/'backend/gedangan'/name for name in ['m07_growth.py','m07_scenarios.py','m07_projection.py','m07_runner.py','m07_analysis.py']]}
 sources.update({name:sha(ROOT/name) for name in ['backend/gedangan/m045_access.py','backend/gedangan/m04_demand.py','backend/gedangan/m051_causality.py','configuration/demand-m04/vehicle-registry.json','configuration/railway-m05/pilot.json','configuration/validation-m051/analysis-policy.json','toolchain/sumo-win64-1.28.0/bin/sumo.exe','toolchain/sumo-win64-1.28.0/bin/duarouter.exe']})
 return {'version':VERSION,'projection_hash':fingerprint(projection),'network_sha256':sha(network),'seed':seed,'options':options,'source_sha256':sources}
def run(projection,network_variant='pilot-provisional',seed=42,base=None,options=None,force_folder=None):
 home=activate();import traci
 base=base or baseline();options={'trains':[70,970],'signal_off':False,'burst':False,'tau_multiplier':1,**(options or {})};network=NETWORKS[network_variant];mode='strict' if network_variant.endswith('strict') else 'provisional'
 if not isinstance(seed,int) or not 0<=seed<=2147483647 or projection['requested']>2500:raise ValueError('Bounded run envelope exceeded')
 sig=signature(projection,network,seed,options);key=fingerprint(sig)[:20];folder=Path(force_folder) if force_folder else RUNS/key;folder.mkdir(parents=True,exist_ok=True)
 if (folder/'result.json').exists():
  if load(folder/'input-manifest.json')!=sig:raise ValueError('Cache signature mismatch')
  for name,h in load(folder/'output-manifest.json').items():
   if sha(folder/name)!=h:raise ValueError('Cached output hash drift: '+name)
  return load(folder/'result.json')
 save(folder/'input-manifest.json',sig);save(folder/'progress.json',{'status':'ROUTING','run_id':key});save(folder/'projection.json',projection)
 try:
  qs=requests(projection,base,mode,seed,options['burst']);save(folder/'requested-trips.json',qs);rows,net=route(folder,qs,network,mode,home)
  routes=types_element(registry())
  for typ in routes.findall('vType'):typ.set('tau',str(float(typ.get('tau'))*options['tau_multiplier']))
  pilot=network_variant.startswith('pilot') and mode=='provisional';trains=options['trains'] if pilot else []
  if trains:E.SubElement(routes,'vType',id='m05_train',**{k:str(v) for k,v in {**load(ROOT/'configuration/railway-m05/pilot.json')['train'],'sigma':0,'minGap':10}.items()})
  for q in rows:
   if q['route_status']=='ROUTABLE':
    v=E.SubElement(routes,'vehicle',id=q['id'],type=q['vehicle_type_id'],depart=str(q['depart_seconds']),departLane='best',departSpeed='0');E.SubElement(v,'route',edges=' '.join(q['edges']))
  for i,t in enumerate(trains):
   v=E.SubElement(routes,'vehicle',id='m07_train_'+str(i),type='m05_train',depart=str(t),departSpeed='0');E.SubElement(v,'route',edges=' '.join(load(network.parent/'rail-provenance.json')['route']))
  routes[:]=routes.findall('vType')+sorted(routes.findall('vehicle'),key=lambda e:(float(e.get('depart')),e.get('id')));xml(folder/'demand.rou.xml',routes)
  add=E.Element('additional',{'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance','xsi:noNamespaceSchemaLocation':str(home/'data/xsd/additional_file.xsd')})
  if pilot:
   tl=E.SubElement(add,'tlLogic',id='osm_859708050',programID='0')
   for k,v in load(ROOT/'configuration/railway-m05/pilot.json')['crossing'].items():E.SubElement(tl,'param',key=k,value=str(v))
  xml(folder/'controls.add.xml',add);cfg=E.Element('configuration');inp=E.SubElement(cfg,'input')
  for k,v in [('net-file',network),('route-files',folder/'demand.rou.xml'),('additional-files',folder/'controls.add.xml')]:E.SubElement(inp,k,value=str(v.resolve()))
  timing=E.SubElement(cfg,'time');E.SubElement(timing,'end',value='2100');E.SubElement(timing,'step-length',value='.5');proc=E.SubElement(cfg,'processing');E.SubElement(proc,'time-to-teleport',value='-1')
  out=E.SubElement(cfg,'output')
  for k,v in [('tripinfo-output',folder/'tripinfo.xml'),('tripinfo-output.write-unfinished','true'),('tripinfo-output.write-undeparted','true'),('fcd-output',folder/'fcd.xml'),('summary-output',folder/'summary.xml')]:E.SubElement(out,k,value=str(v.resolve()) if isinstance(v,Path) else v)
  xml(folder/'run.sumocfg',cfg);label='m07_'+key;start=time.perf_counter();stdout=(folder/'sumo-stdout.txt').open('w');save(folder/'progress.json',{'status':'RUNNING','run_id':key})
  traci.start([str(home/'bin/sumo.exe'),'-c',str((folder/'run.sumocfg').resolve()),'--seed',str(seed),'--no-step-log','true','--duration-log.disable','true','--error-log',str((folder/'errors.log').resolve()),'--xml-validation','always'],label=label,stdout=stdout)
  connection=traci.getConnection(label);trace=Trace(connection,network);resource=Resource(connection._process.pid);tls=connection.trafficlight.getIDList()
  if options['signal_off'] and 'm05_gedangan' in tls:connection.trafficlight.setProgram('m05_gedangan','off')
  roadids={r['id'] for r in rows if r['route_status']=='ROUTABLE'};loaded=set();departed=set();arrived=set();moved=set();teleports=[];collisions=[];illegal=[];frames=[];events=[];states={};maxq=0;maxextent=0;queue_seconds=defaultdict(float);lane_occupied=defaultdict(list);gate_delay=0;speed_samples=[];dims={v['id']:v['parameters']['length'] for v in registry()};lengths={l.getID():l.getLength() for e in net.getEdges(withInternal=True) for l in e.getLanes()}
  try:
   for step in range(4200):
    if time.perf_counter()-start>180:raise RuntimeError('SUMO driver exceeded180s bounded per-run wall time')
    trace.simulationStep();t=connection.simulation.getTime();loaded.update(set(connection.simulation.getLoadedIDList())&roadids);departed.update(set(connection.simulation.getDepartedIDList())&roadids);arrived.update(set(connection.simulation.getArrivedIDList())&roadids);teleports.extend(connection.simulation.getStartingTeleportIDList());collisions.extend(connection.simulation.getCollidingVehiclesIDList())
    if step%2==0:
     resource.sample();vehicles=[];by=defaultdict(list);sigstates={k:connection.trafficlight.getRedYellowGreenState(k) for k in tls}
     for k,s in sigstates.items():
      if states.get(k)!=s:events.append({'time':t,'controller':k,'state':s});states[k]=s
     for vid,d in connection.vehicle.getAllSubscriptionResults().items():
      if not d:continue
      typ=connection.vehicle.getTypeID(vid);lane=d[81];speed=d[64];x,y=d[66];pos=d[86]
      if vid not in roadids:
       vehicles.append({'id':vid,'type':typ,'lane':lane,'speed':speed,'x':x,'y':y,'pos':pos});continue
      if not net.getLane(lane).allows(connection.vehicle.getVehicleClass(vid)):illegal.append({'id':vid,'lane':lane,'time':t})
      if speed>.1:moved.add(vid)
      speed_samples.append(speed);v={'id':vid,'type':typ,'lane':lane,'speed':speed,'x':round(x,2),'y':round(y,2),'pos':pos};vehicles.append(v)
      if not lane.startswith(':'):by[lane].append(v)
      if speed<.3:
       nexttls=connection.vehicle.getNextTLS(vid)
       if nexttls and nexttls[0][0]=='osm_859708050' and nexttls[0][2]<30 and nexttls[0][3] in 'rRyY':gate_delay+=1
     queues={}
     for lane,vs in by.items():
      stopped=[v for v in vs if v['speed']<.3];storage=lengths[lane];intervals=sorted((max(0,v['pos']-dims[v['type']]),min(storage,v['pos'])) for v in vs);covered=0;end=0
      for lo,hi in intervals:covered+=max(0,hi-max(end,lo));end=max(end,hi)
      lane_occupied[lane].append(min(100,100*covered/storage))
      if stopped:
       tail=min(v['pos']-dims[v['type']] for v in stopped);head=max(v['pos'] for v in stopped);queues[lane]={'count':len(stopped),'extent_m':head-tail,'boundary_censored':tail<=0};queue_seconds[lane]+=1
     maxq=max(maxq,sum(q['count'] for q in queues.values()));maxextent=max(maxextent,max((q['extent_m'] for q in queues.values()),default=0))
     if step%10==0:frames.append({'time':t,'vehicles':vehicles,'signals':sigstates,'queues':queues})
   running=set(connection.vehicle.getIDList())&roadids;pending=set(connection.simulation.getPendingVehicles())&roadids;resource.sample()
  finally:resource.close();connection.close();stdout.close()
  save(folder/'priority-trace.json',trace.frames);save(folder/'result.json',{'network_path':str(network.relative_to(ROOT))})
  causal=analyze_trace(folder);trips={v.get('id'):dict(v.attrib) for v in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo') if v.get('id') in roadids}
  from .m07_analysis import lifecycle_metrics
  stats=lifecycle_metrics(rows,trips,loaded,departed,arrived,running,pending,moved);result={**stats,'run_id':key,'year':projection['year'],'scenario':projection['scenario'],'scenario_hash':projection['scenario_hash'],'projection_hash':projection['projection_hash'],'baseline_hash':projection['baseline_hash'],'seed':seed,'network_variant':network_variant,'network_path':str(network.relative_to(ROOT)),'network_sha256':sha(network),'input_signature':sig,'label':LABEL,'status':'ACTUAL_SUMO_RESULT','fixed_horizon_s':2100,'demand_window_s':[0,1800],'warmup_s':0,'optional_drain_s':0,'teleports':teleports,'collisions':collisions,'illegal_permissions':illegal,'max_stopped_count':maxq,'max_lane_queue_extent_m':maxextent,'queue_duration_lane_seconds':dict(queue_seconds),'lane_occupancy_percent_conditional_on_nonempty':{k:statistics.mean(v) for k,v in lane_occupied.items()},'lane_occupancy_note':'Clipped union of FCD front-assigned body footprints; conditional on lane nonempty at1s samples, not time-average over empty samples; cross-edge body not reconstructed.','sampled_speed_m_s':{'mean':statistics.mean(speed_samples) if speed_samples else None,'min':min(speed_samples) if speed_samples else None,'max':max(speed_samples) if speed_samples else None},'spillback_candidates':sum(e['cause']=='STORAGE_BLOCKAGE_CANDIDATE' for e in causal),'verified_in_model_spillback':sum(e['cause']=='VERIFIED_SPILLBACK' for e in causal),'spillback_not_field_validated':True,'crossing_delay_vehicle_seconds_contextual':gate_delay,'rail_events':events,'train_departures':trains,'wall_seconds':time.perf_counter()-start,'sumo_cpu_seconds':resource.cpu,'sumo_peak_working_set_bytes_sampled':resource.peak,'sumo_version':'1.28.0','options':options}
  if illegal or teleports or collisions:result['safety_status']='REQUIRES_REVIEW'
  else:result['safety_status']='NO_RECORDED_PERMISSION_COLLISION_TELEPORT_EVENTS'
  save(folder/'result.json',result);save(folder/'lifecycle.json',{'trips':trips,'requested_ids':[r['id'] for r in rows],'loaded':sorted(loaded),'departed':sorted(departed),'arrived':sorted(arrived),'running':sorted(running),'pending':sorted(pending),'moved':sorted(moved)})
  save(folder/'playback.json',{'label':LABEL,'sample_period_s':5,'source':'Actual SUMO position samples; no random/interpolated trajectories','frames':frames,'events':events});save(folder/'progress.json',{'status':'COMPLETE','run_id':key});save(folder/'output-manifest.json',{p.name:sha(p) for p in folder.iterdir() if p.is_file() and p.name not in ['output-manifest.json']});print(projection['year'],projection['scenario'],network_variant,stats['requested'],stats['routable'],stats['arrived'],stats['not_departed'],'not departed',flush=True);return result
 except Exception as exc:save(folder/'failure.json',{'error':str(exc),'signature':sig});save(folder/'progress.json',{'status':'FAILED','error':str(exc)});raise
def precompute():
 RUNS.mkdir(parents=True,exist_ok=True);jobs=[]
 for y in [2026,2030,2035,2040]:
  for seed in [42,43]:jobs.append({'year':y,'scenario':'REFERENCE','seed':seed})
 jobs.extend([{'year':2040,'scenario':s,'seed':42} for s in ['LOW','HIGH']]);jobs.append({'year':2026,'scenario':'REFERENCE','seed':42,'network':'pilot-strict'});jobs.append({'year':2026,'scenario':'REFERENCE','seed':42,'network':'corrected-provisional'})
 checkpoint=DOC/'run-queue.json';done=[]
 for i,j in enumerate(jobs):
  save(checkpoint,{'status':'RUNNING','concurrency':1,'completed':done,'next':j,'total':len(jobs)});r=run(project(j['year'],read(j['scenario'])),j.get('network','pilot-provisional'),j['seed']);done.append({'job':j,'run_id':r['run_id']})
 save(checkpoint,{'status':'COMPLETE','concurrency':1,'completed':done,'total':len(jobs)})
if __name__=='__main__':precompute()
