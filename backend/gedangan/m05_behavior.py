"""M05 reproducible recorded SUMO experiments, isolated from earlier milestones."""
from pathlib import Path
import json,random,time,sys,xml.etree.ElementTree as ET
from collections import Counter
from .m04_demand import ROOT,load,save,xml,sha,execute,activate,registry
from .m045_access import external_connections
from .m05_railway import source_pilot,CROSSING,audit_source
from .m05_signals import node_patch,programs
from .m05_queues import observe
NET=ROOT/'simulation/network/m05';RUNS=ROOT/'simulation/runs/m05';DOC=ROOT/'documentation/m05'
def baseline():
    drift=[p for p,h in load(DOC/'previous-milestones-sha256.json').items() if sha(ROOT/p)!=h]
    if drift:raise RuntimeError('Prior milestone drift '+str(drift))
def build(home):
    baseline();audit_source()
    for mode in ['strict','provisional']:
        folder=NET/mode;folder.mkdir(parents=True,exist_ok=True)
        original=ROOT/f'simulation/network/m045/{mode}/network.net.xml'; base=ET.parse(original).getroot()
        ns=node_patch();existing={j.get('id') for j in base.findall('junction')}
        for n in list(ns):
            if n.get('id') not in existing:ns.remove(n)
        args=[home/'bin/netconvert.exe','--sumo-net-file',original,'--offset.disable-normalization','true','--no-turnarounds','true','--geometry.remove','false','--junctions.join','false']
        if mode=='provisional':
            rn,re,rc,route=source_pilot(folder,load(ROOT/f'simulation/network/m045/{mode}/inspection.json'))
            ns.extend(list(rn));args+=['--edge-files',folder/'rail.edg.xml','--connection-files',folder/'rail.con.xml']
        xml(folder/'changes.nod.xml',ns);args+=['--node-files',folder/'changes.nod.xml','--output-file',folder/'draft.net.xml']
        result=execute(args,folder/'build-log.json');assert result['returncode']==0,result['stderr']
        draft=ET.parse(folder/'draft.net.xml').getroot();old=external_connections(base);new=external_connections(draft)
        # NETCONVERT can infer movements at rebuilt junctions. Delete every road movement not in immutable baseline.
        dels=ET.Element('connections')
        for key in new:
            if not key[0].startswith('m05_rail_') and key not in old:ET.SubElement(dels,'delete',**dict(zip(['from','to','fromLane','toLane'],key)))
        xml(folder/'remove-inferred.con.xml',dels)
        result=execute([home/'bin/netconvert.exe','--sumo-net-file',folder/'draft.net.xml','--connection-files',folder/'remove-inferred.con.xml','--offset.disable-normalization','true','--no-turnarounds','true','--geometry.remove','false','--output-file',folder/'network.net.xml'],folder/'rebuild-log.json');assert result['returncode']==0,result['stderr']
        final=ET.parse(folder/'network.net.xml').getroot();road={k:v for k,v in external_connections(final).items() if not k[0].startswith('m05_rail_')}
        assert set(road)==set(old),('Road connectivity changed',set(road)-set(old),set(old)-set(road))
        changes=[]
        for e in base.findall('edge'):
            if e.get('function')=='internal':continue
            f=next(x for x in final.findall('edge') if x.get('id')==e.get('id'))
            for a,b in zip(e.findall('lane'),f.findall('lane')):
                for key in ['allow','disallow','shape','width','speed']:
                    if a.get(key)!=b.get(key):changes.append([a.get('id'),key,a.get(key),b.get(key)])
        save(folder/'baseline-audit.json',{'baseline_sha256':sha(original),'road_connection_count':len(old),'new_road_connections':0,'external_lane_differences':changes,'note':'Internal junction geometry is rebuilt for explicit signals/rail topology; Access and original road connection tuples identical. NETCONVERT snaps four adjacent edge shape endpoints to the existing shared crossing node and retrims seven adjacent lane shapes; all changes are enumerated separately. Original M04.5 files remain immutable. Review this localized derivative geometry limitation before field use.'})
        assert all(x[1]=='shape' for x in changes),changes[:5]
        edge_diffs=[{'id':e.get('id'),'before':e.get('shape'),'after':next(x for x in final.findall('edge') if x.get('id')==e.get('id')).get('shape')} for e in base.findall('edge') if e.get('function')!='internal' and next(x for x in final.findall('edge') if x.get('id')==e.get('id')).get('shape')!=e.get('shape')]
        save(folder/'crossing-endpoint-adaptations.json',edge_diffs)
        assert all(d['id'].startswith(('w1240685448_s1_p1_','w1240685448_s1_p2_')) for d in edge_diffs), 'Distant source geometry drift'
        # Explicit rail topology derivative: audit localized endpoint snapping and junction-envelope retrimming.
        assert all(x[0].startswith(('w1240685448_','w160009748_')) for x in changes), 'Unexpected distant geometry change'
        save(folder/'signal-plans.json',programs(final));xml(folder/'network.net.xml',final)
        save(folder/'manifest.json',{'baseline':str(original.relative_to(ROOT)),'baseline_sha256':sha(original),'derived_sha256':sha(folder/'network.net.xml'),'toolchain':'SUMO NETCONVERT 1.28.0','category':'SIMULATION_DERIVATIVE','rail_pilot':mode=='provisional'})
    baseline()
def demand(folder,mode,n,seed):
    records=load(ROOT/f'simulation/demand/m045/compatibility/{mode}/route-validation.json')['results']
    candidates=[r for r in records if r['route_status']=='ROUTABLE' and r['od_id'] in ['northbound','southbound','station_junction','feeder_to_main','main_to_feeder']]
    rng=random.Random(seed);routes=ET.Element('routes')
    for v in registry():
        if v['id']=='oversize':continue
        ET.SubElement(routes,'vType',id=v['id'],**{k:str(x) for k,x in v['parameters'].items()})
    ET.SubElement(routes,'vType',id='m05_train',**{k:str(v) for k,v in {**load(ROOT/'configuration/railway-m05/pilot.json')['train'],'sigma':0,'minGap':10}.items()})
    specs=[]
    for i in range(n):
        # Exact composition and OD membership are frozen once, reused in every paired run.
        r=rng.choice(candidates);specs.append({'id':f'road_{i}','type':r['vehicle_type_id'],'depart':round(i*240/max(1,n-1),2),'edges':r['edges'],'od_id':r['od_id']})
    # Dedicated station-crossing light vehicles use source-connected route segments already admitted in M04.5.
    if mode=='provisional':
        import sumolib
        net=sumolib.net.readNet(str(NET/mode/'network.net.xml'))
        for i in range(24):
            es=['w1240685448_s1_p0_0_f','w1240685448_s1_p1_0_f','w1240685448_s1_p2_0_f'] if i%2==0 else ['w1240685448_s1_p2_0_r','w1240685448_s1_p1_0_r','w1240685448_s1_p0_0_r']
            assert all(net.getEdge(e).allows('passenger') for e in es)
            specs.append({'id':f'cross_{i}','type':['car','motorcycle','pickup_van'][i%3],'depart':i*8+40,'edges':es,'od_id':'source_connected_crossing_probe'})
    save(folder/'demand.json',{'category':'SYNTHETIC_TEST','seed':seed,'registry_source':'configuration/demand-m04/vehicle-registry.json','OD_source':'simulation/demand/m04/od-matrix.fixture.json','crossing_probes':'Explicit synthetic source-connected station movement; separate from inherited OD counts','vehicles':specs})
    return routes,specs

def run(home,name,mode='provisional',n=90,seed=42,signals=True,trains=(),opening_delay=3,network_override=None):
    import traci,sumolib
    netpath=Path(network_override) if network_override else NET/mode/'network.net.xml'
    folder=RUNS/name;folder.mkdir(parents=True,exist_ok=True);routes,specs=demand(folder,mode,n,seed)
    for s in sorted(specs,key=lambda s:s['depart']):
        v=ET.SubElement(routes,'vehicle',id=s['id'],type=s['type'],depart=str(s['depart']),departLane='best',departSpeed='0');ET.SubElement(v,'route',edges=' '.join(s['edges']))
    if trains:
        route=load(NET/mode/'rail-provenance.json')['route']
        # SUMO requires departure ordering globally.
        for i,t in enumerate(trains):
            v=ET.SubElement(routes,'vehicle',id=f'train_{i}',type='m05_train',depart=str(t),departSpeed='0');ET.SubElement(v,'route',edges=' '.join(route))
    types=routes.findall('vType');vehicles=sorted(routes.findall('vehicle'),key=lambda v:float(v.get('depart')));routes[:]=types+vehicles
    xml(folder/'demand.rou.xml',routes)
    add=ET.Element('additional')
    if mode=='provisional':
        tl=ET.SubElement(add,'tlLogic',id=CROSSING,programID='0')
        for k,v in {**load(ROOT/'configuration/railway-m05/pilot.json')['crossing'],'opening-delay':opening_delay}.items():ET.SubElement(tl,'param',key=k,value=str(v))
    detlanes=['w562358500_s16_p0_0_f_0','w512351908_s4_p0_0_f_0']
    import sumolib
    detnet=sumolib.net.readNet(str(netpath))
    for lane in detlanes:
        length=detnet.getLane(lane).getLength()
        ET.SubElement(add,'laneAreaDetector',id='e2_'+lane,lane=lane,pos='0',endPos=str(length-.1),period='1',file=str(folder/'e2.xml'),timeThreshold='1',speedThreshold='0.3',jamThreshold='10')
    xml(folder/'controls.add.xml',add)
    cfg=ET.Element('configuration');inp=ET.SubElement(cfg,'input')
    for k,v in [('net-file',netpath),('route-files',folder/'demand.rou.xml'),('additional-files',folder/'controls.add.xml')]:ET.SubElement(inp,k,value=str(v))
    timing=ET.SubElement(cfg,'time');ET.SubElement(timing,'end',value='900');ET.SubElement(timing,'step-length',value='0.5')
    output=ET.SubElement(cfg,'output')
    for k,v in [('tripinfo-output',folder/'tripinfo.xml'),('summary-output',folder/'summary.xml'),('fcd-output',folder/'fcd.xml')]:ET.SubElement(output,k,value=str(v))
    xml(folder/'run.sumocfg',cfg)
    start=time.perf_counter();traci.start([str(home/'bin/sumo.exe'),'-c',str(folder/'run.sumocfg'),'--seed',str(seed),'--no-step-log','true','--duration-log.disable','true','--error-log',str(folder/'sumo-errors.log')],label=name,stdout=(folder/'sumo-stdout.txt').open('w'))
    c=traci.getConnection(name);net=sumolib.net.readNet(str(netpath),withInternal=True);lengths={l.getID():l.getLength() for e in net.getEdges(withInternal=True) for l in e.getLanes()}
    tls=c.trafficlight.getIDList()
    if not signals:
        for t in tls:
            if t=='m05_gedangan':c.trafficlight.setProgram(t,'off')
    frames=[];events=[];last={};departed=set();arrived=set();loaded=set();moved=set();teleports=[];collisions=[];max_queue=0;red_stops=0;gate_stops=0
    for step in range(1800):
        c.simulationStep();t=c.simulation.getTime();loaded.update(c.simulation.getLoadedIDList());departed.update(c.simulation.getDepartedIDList());arrived.update(c.simulation.getArrivedIDList());teleports.extend(c.simulation.getStartingTeleportIDList());collisions.extend(c.simulation.getCollidingVehiclesIDList())
        for vid in c.simulation.getDepartedIDList():c.vehicle.subscribe(vid,[64,66,81,86,122,80,67,114])
        states={tlsid:c.trafficlight.getRedYellowGreenState(tlsid) for tlsid in tls}
        for tid,state in states.items():
            if last.get(tid)!=state:events.append({'time':t,'controller':tid,'state':state,'previous':last.get(tid)});last[tid]=state
        if step%2:continue
        vs=[]
        for vid,d in c.vehicle.getAllSubscriptionResults().items():
            if not d:continue
            speed=d.get(64,0);x,y=d.get(66,(0,0));lane=d.get(81,'');pos=d.get(86,0);wait=d.get(122,0)
            if speed>.1:moved.add(vid)
            vs.append({'id':vid,'type':c.vehicle.getTypeID(vid),'x':round(x,2),'y':round(y,2),'speed':round(speed,3),'lane':lane,'pos':round(pos,2),'wait':wait,'angle':d.get(67,0),'acceleration':d.get(114,0)})
            if speed<.3:
                for tid,idx,dist,state in c.vehicle.getNextTLS(vid)[:1]:
                    if dist<30 and state in 'rRyY':
                        red_stops+=1
                        if tid==CROSSING:gate_stops+=1
        queues=observe(vs,lengths);max_queue=max(max_queue,sum(q['count'] for q in queues.values()));frames.append({'time':t,'vehicles':vs,'signals':states,'queues':queues})
    remaining=list(c.vehicle.getIDList());pending=c.simulation.getPendingVehicles();c.close()
    trips=ET.parse(folder/'tripinfo.xml').getroot().findall('tripinfo');counts=Counter(s['type'] for s in specs)
    result={'name':name,'category':'SIMULATED_RESULT â€” SYNTHETIC NOT CALIBRATED','mode':mode,'seed':seed,'signals':signals,'train_departures':list(trains),'opening_delay':opening_delay,'warmup_s':0,'measurement_window_s':[0,900],'requested_road':len(specs),'requested_train':len(trains),'loaded':len(loaded),'departed':len(departed),'moved':len(moved),'arrived':len(arrived),'running':remaining,'pending':list(pending),'teleports':teleports,'collisions':collisions,'maximum_stopped_road_queue_count':max_queue,'red_stop_vehicle_seconds':red_stops,'rail_gate_stop_vehicle_seconds':gate_stops,'runtime_wall_seconds':time.perf_counter()-start,'vehicle_composition':dict(counts),'mean_trip_duration_s':sum(float(x.get('duration')) for x in trips)/len(trips) if trips else None,'mean_waiting_s':sum(float(x.get('waitingTime')) for x in trips)/len(trips) if trips else None,'mean_speed_m_s':sum(float(x.get('routeLength'))/float(x.get('duration')) for x in trips)/len(trips) if trips else None,'unserved_accounting':'requested = arrived + running + not departed; pending is SUMO insertion queue only','spillback_status':'NOT_ESTABLISHED: queue reaching boundary alone is insufficient; no validated upstream blocking-duration detector yet','per_type':{typ:{'requested':cnt,'departed':sum(s['id'] in departed for s in specs if s['type']==typ),'moved':sum(s['id'] in moved for s in specs if s['type']==typ),'arrived':sum(s['id'] in arrived for s in specs if s['type']==typ)} for typ,cnt in counts.items()},'demand_sha256':sha(folder/'demand.json'),'network_sha256':sha(netpath),'network_path':str(netpath.relative_to(ROOT))}
    save(folder/'result.json',result);save(folder/'events.json',events);save(folder/'playback.json',{'result':result,'frames':frames,'events':events});print(name,result['departed'],result['arrived'],'gate-stops',gate_stops,flush=True)
    return result

def main():
    home=activate();action=sys.argv[1] if len(sys.argv)>1 else 'all'
    if action in ['build','all']:
        build(home)
        from .m05_railway import build_block_control
        build_block_control(home)
    if action in ['run','all']:
        scenarios=[('A_free',False,(),3,90),('B_signal',True,(),3,90),('C_single',False,(70,),3,90),('D_two',False,(70,170),3,90),('D_consecutive',False,(70,85),3,90),('D_long',False,(70,),20,90),('E_combined',True,(70,),3,90),('F_high_free',False,(),3,240),('F_high_signal',True,(),3,240)]
        results=[]
        for seed in [42,43]:
            for name,signals,trains,delay,n in scenarios:results.append(run(home,f'{name}_seed{seed}',n=n,seed=seed,signals=signals,trains=trains,opening_delay=delay))
        results.append(run(home,'strict_signal_seed42',mode='strict',n=60))
        results.append(run(home,'G_e2_instrumented',n=90,signals=True,trains=(70,)))
        results.append(run(home,'I_repro_single_seed42',n=90,signals=False,trains=(70,)))
        results.append(run(home,'H_close_block_control',n=90,signals=False,trains=(70,85),opening_delay=10,network_override=NET/'provisional-block-control/network.net.xml'))
        save(DOC/'scenario-results.json',results)
    baseline()
if __name__=='__main__':main()
