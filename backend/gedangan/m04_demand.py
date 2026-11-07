"""Structured synthetic demand, immutable M03 permissions, SUMO-recorded results.

This module never calibrates traffic, changes network permissions, repairs topology,
or computes annual growth. Browser consumes recorded outputs only.
"""
from collections import Counter, defaultdict
import ctypes
from ctypes import wintypes
import hashlib
import json
import math
from pathlib import Path
import random
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
CONF=ROOT/'configuration/demand-m04'
DEMAND=ROOT/'simulation/demand/m04'
RUNS=ROOT/'simulation/runs/m04'
DOC=ROOT/'documentation/m04'
M03=ROOT/'simulation/network/m03'
LABEL='SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC'
sys.path.insert(0,str(ROOT/'configuration'))
from sumo_env_m02 import activate

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,data):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def xml(p,root):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);ET.indent(root);ET.ElementTree(root).write(p,encoding='utf-8',xml_declaration=True)
def relative(p,folder):return str(Path(p).relative_to(folder)).replace('\\','/')

class ProcessMemory(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]

def execute(command,log):
    """Log full process results and sampled per-process resource usage on Windows."""
    command=list(map(str,command));start=time.perf_counter();peak=0;cpu=None;samples=0
    # Files avoid PIPE deadlocks on stress warning logs. These are retained verbatim.
    stdout=Path(log).with_suffix('.stdout.txt');stderr=Path(log).with_suffix('.stderr.txt')
    with stdout.open('w',encoding='utf-8') as out,stderr.open('w',encoding='utf-8') as err:
        proc=subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err)
        kernel=ctypes.WinDLL('kernel32',use_last_error=True);psapi=ctypes.WinDLL('psapi',use_last_error=True)
        kernel.OpenProcess.restype=wintypes.HANDLE
        kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
        kernel.CloseHandle.argtypes=[wintypes.HANDLE]
        psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(ProcessMemory),wintypes.DWORD]
        kernel.GetProcessTimes.argtypes=[wintypes.HANDLE]+[ctypes.POINTER(wintypes.FILETIME)]*4
        handle=kernel.OpenProcess(0x0410,False,proc.pid)
        try:
            while proc.poll() is None:
                if handle:
                    mem=ProcessMemory();mem.cb=ctypes.sizeof(mem)
                    if psapi.GetProcessMemoryInfo(handle,ctypes.byref(mem),mem.cb):peak=max(peak,mem.PeakWorkingSetSize);samples+=1
                if time.perf_counter()-start>180:
                    proc.kill();proc.wait();raise RuntimeError('Process exceeded 180s bounded smoke test; outputs retained')
                time.sleep(.02)
            if handle:
                ft=[wintypes.FILETIME() for _ in range(4)]
                if kernel.GetProcessTimes(handle,*[ctypes.byref(t) for t in ft]):
                    cpu=sum((ft[i].dwHighDateTime<<32)+ft[i].dwLowDateTime for i in [2,3])/1e7
        finally:
            if handle:kernel.CloseHandle(handle)
    elapsed=time.perf_counter()-start;output=stdout.read_text(encoding='utf-8',errors='replace');errors=stderr.read_text(encoding='utf-8',errors='replace')
    result={'command':command,'returncode':proc.returncode,'stdout':output,'stderr':errors,'wall_seconds':elapsed,'cpu_seconds':cpu,'cpu_one_core_percent':cpu/elapsed*100 if cpu is not None else None,'peak_working_set_bytes_sampled':peak or None,'memory_samples':samples,'measurement_note':'Process-specific Windows counters, sampled every ~20ms; peak can be missed for short processes. Not GPU/whole-device benchmark.'}
    save(log,result);return result

def registry():return load(CONF/'vehicle-registry.json')['vehicles']
def validate_inputs(vehicles,config):
    ids=[v['id'] for v in vehicles]
    if len(ids)!=len(set(ids)) or len(ids)!=10:raise ValueError('Exactly ten unique local vehicle definitions required')
    for v in vehicles:
        p=v['parameters']
        if v['sumo_vclass'] not in {'motorcycle','passenger','delivery','bus','truck','trailer'} or p['vClass']!=v['sumo_vclass']:raise ValueError('Invalid or mismatched SUMO class')
        for key in ['length','width','height','maxSpeed','accel','decel','emergencyDecel','minGap','tau','speedFactor']:
            if not isinstance(p[key],(int,float)) or isinstance(p[key],bool) or not math.isfinite(p[key]) or p[key]<=0:raise ValueError('Nonpositive/nonfinite vehicle parameter: '+key)
        if p['length']>30 or p['width']>4 or p['height']>6 or p['maxSpeed']>60 or p['emergencyDecel']<p['decel'] or p['tau']<1:raise ValueError('Vehicle parameter outside conservative technical test envelope')
        if not 0<=p['sigma']<=1 or p['carFollowModel']!='Krauss' or p['laneChangeModel']!='LC2013':raise ValueError('Unsupported behavior foundation')
        if set(p)!=set(v['parameter_provenance']) or any(x['status']!='ASSUMPTION' or not x['provenance_id'] for x in v['parameter_provenance'].values()):raise ValueError('Every vehicle parameter requires assumption provenance')
    if set(config['composition'])!=set(ids) or any(not math.isfinite(x) or x<0 for x in config['composition'].values()) or abs(sum(config['composition'].values())-1)>1e-9:raise ValueError('Invalid vehicle composition')
    if config['baseline_year']!=2026 or config['interval_seconds']!=900 or config['category']!='SYNTHETIC_TEST' or config['year_dimensions']['projection_implemented']:raise ValueError('M04 scope requires synthetic 2026/900-second intervals without projection')
    if not isinstance(config['seed'],int) or isinstance(config['seed'],bool):raise ValueError('Integer seed required')
    for profile in config['profiles'].values():
        if not isinstance(profile['requested_per_interval'],int) or not 0<profile['requested_per_interval']<=500:raise ValueError('Initial staged test capped at 500 requests per interval')

def types_element(vehicles,sublane=False):
    root=ET.Element('routes')
    for v in vehicles:
        p={k:str(value) for k,value in v['parameters'].items()}
        if sublane and v['id']=='motorcycle':p.update(laneChangeModel='SL2015',minGapLat='.2',maxSpeedLat='1',latAlignment='arbitrary')
        ET.SubElement(root,'vType',id=v['id'],**p)
    return root

def inspect(mode):return load(M03/mode/'inspection.json')
def edge_index(mode):return {e['id']:e for e in inspect(mode)['edges']}
def sumonet(mode):
    import sumolib
    return sumolib.net.readNet(str(M03/mode/'network.net.xml'),withInternal=True)

def local_pair(mode):
    data=inspect(mode);edges={e['id']:e for e in data['edges'] if e['road_function']=='local_access_road'}
    pairs=sorted({(c['from'],c['to']) for c in data['connections'] if c['from'] in edges and c['to'] in edges and edges[c['from']]['source_way_id']==edges[c['to']]['source_way_id']})
    if not pairs:return None,None
    # Actual distinct source edges on a local road, never a fabricated connector.
    a,b=pairs[0];return a,b

def make_zones():
    anchors={
        'northbound':('south_gateway','north_gateway'), 'southbound':('north_gateway','south_gateway'),
        'feeder_to_main':('sukodono_west','north_gateway'),'main_to_feeder':('north_gateway','sukodono_west'),
        'frontage_continuity':('frontage_north','frontage_south'),'frontage_exit':('frontage_north','ketajen_east'),
        'gedangan_junction':('gedangan_south','gedangan_north'),'station_junction':('station_west','ketajen_east'),
        'local_trip':('local_origin','local_destination')}
    zones={z:{'id':z,'category':'ASSUMPTION','confidence':'ASSUMPTION','provenance_id':'A-ZONE-01','geographic_zone':None,'assignments':{}} for pair in anchors.values() for z in pair}
    movements=[]
    for mode in ['strict','provisional']:
        edges=edge_index(mode);routes=load(M03/mode/'route-tests/results.json')['results']
        routes.append(dict(test_id='local_trip',starting_edge=local_pair(mode)[0],destination_edge=local_pair(mode)[1]))
        for r in routes:
            for field,zoneid,kind in [('starting_edge',anchors[r['test_id']][0],'origin_candidate_edges'),('destination_edge',anchors[r['test_id']][1],'destination_candidate_edges')]:
                z=zones[zoneid];a=z['assignments'].setdefault(mode,{'origin_candidate_edges':[],'destination_candidate_edges':[],'vehicle_class_eligibility':{},'network_variant':mode,'confidence':'ASSUMPTION','provenance_id':'A-ZONE-01'})
                eid=r[field]
                if eid and eid not in a[kind]:a[kind].append(eid)
                if eid and z['geographic_zone'] is None:
                    pts=edges[eid]['shape'];cx=sum(p[0] for p in pts)/len(pts);cy=sum(p[1] for p in pts)/len(pts)
                    z['geographic_zone']={'crs':'EPSG:32749_LOCAL_M03','origin_utm_m':inspect(mode)['origin_utm_m'],'anchor_xy_m':[cx,cy],'display_envelope_xy_m':[cx-50,cy-50,cx+50,cy+50],'status':'ASSUMPTION','reason':'Display envelope 50m around source-edge centroid; not surveyed travel-zone boundary','source_edge':eid,'source_way_id':edges[eid]['source_way_id']}
    for zone in zones.values():
        for mode,assignment in zone['assignments'].items():
            net=sumonet(mode)
            for v in registry():
                assignment['vehicle_class_eligibility'][v['id']]={kind:[eid for eid in assignment[kind] if any(l.allows(v['sumo_vclass']) for l in net.getEdge(eid).getLanes())] for kind in ['origin_candidate_edges','destination_candidate_edges']}
    for name,(origin,dest) in anchors.items():
        movements.append({'id':name,'origin_zone':origin,'destination_zone':dest,'weight':1,'confidence':'ASSUMPTION','provenance_id':'A-ZONE-01','endpoint_selection':'M03 named route fixture; local uses two adjacent same-way local edges','endpoints':{}})
    for mode in ['strict','provisional']:
        rows=load(M03/mode/'route-tests/results.json')['results']+[dict(test_id='local_trip',starting_edge=local_pair(mode)[0],destination_edge=local_pair(mode)[1])]
        for m in movements:
            r=next(r for r in rows if r['test_id']==m['id']);m['endpoints'][mode]={'origin_edge':r['starting_edge'],'destination_edge':r['destination_edge']}
    save(DEMAND/'od-zones.json',{'category':'ASSUMPTION','zones':list(zones.values())})
    matrix={'schema_version':'m04-1','baseline_year':2026,'category':'SYNTHETIC_TEST','interval_seconds':900,'movements':movements}
    save(DEMAND/'od-matrix.fixture.json',matrix);return matrix

def allocate(total,weights):
    if total<0 or not isinstance(total,int):raise ValueError('Trip total must be nonnegative integer')
    if not weights or any(not math.isfinite(w) or w<0 for w in weights.values()) or sum(weights.values())<=0:raise ValueError('Invalid demand weights')
    exact={k:total*w/sum(weights.values()) for k,w in weights.items()};counts={k:math.floor(v) for k,v in exact.items()}
    for k in sorted(exact,key=lambda k:(-(exact[k]-counts[k]),k))[:total-sum(counts.values())]:counts[k]+=1
    return counts

def generate(mode,profile,config,matrix):
    total=config['profiles'][profile]['requested_per_interval'];rng=random.Random(config['seed'])
    classes=[k for k,n in allocate(total,config['composition']).items() for _ in range(n)]
    ods=[k for k,n in allocate(total,{m['id']:m['weight'] for m in matrix['movements']}).items() for _ in range(n)]
    rng.shuffle(classes);rng.shuffle(ods);lookup={m['id']:m for m in matrix['movements']};requests=[]
    for i,(v,od) in enumerate(zip(classes,ods)):
        row=lookup[od];endpoints=row['endpoints'][mode]
        requests.append({'id':f'm04_{mode}_{profile}_{i:05d}','vehicle_type_id':v,'od_id':od,'origin_zone':row['origin_zone'],'destination_zone':row['destination_zone'],**endpoints,
            'depart_seconds':round((i+rng.random())*config['interval_seconds']/total,3),'interval_start_seconds':0,'interval_end_seconds':900,'baseline_year':2026,'network_variant':mode,'category':'SYNTHETIC_TEST','provenance_id':'S-DEMAND-01','confidence':'ASSUMPTION'})
    return requests

def precheck(request,v,edges,net):
    if v['eligibility']['require_surveyed_geometry_and_legal_clearance']:return 'OVERSIZE_CLEARANCE_UNVERIFIED: no swept-path, height, load or legal permit clearance'
    for key in ['origin_edge','destination_edge']:
        eid=request[key]
        if not eid or eid not in edges:return 'ENDPOINT_EXCLUDED_BY_M03_POLICY: '+key
        if not any(l.allows(v['sumo_vclass']) for l in net.getEdge(eid).getLanes()):return 'M03_LANE_PERMISSION_DENIED: '+v['sumo_vclass']
        if edges[eid]['road_function'] not in v['eligibility']['allowed_road_functions']:return 'HEAVY_ROAD_FUNCTION_SCREEN_FAILED'
        if not any(l.allows(v['sumo_vclass']) and l.getWidth()>=v['eligibility']['minimum_lane_width_m'] for l in net.getEdge(eid).getLanes()):return 'GEOMETRY_WIDTH_SCREEN_FAILED'
    return None

def validate_route(ids,request,v,edges,net,connections):
    if not ids or ids[0]!=request['origin_edge'] or ids[-1]!=request['destination_edge']:return 'ROUTER_ENDPOINT_MISMATCH'
    for eid in ids:
        e=edges[eid]
        if not any(l.allows(v['sumo_vclass']) and l.getWidth()>=v['eligibility']['minimum_lane_width_m'] for l in net.getEdge(eid).getLanes()):return 'ROUTE_PERMISSION_OR_WIDTH_SCREEN_FAILED'
        if e['road_function'] not in v['eligibility']['allowed_road_functions']:return 'ROUTE_HEAVY_ROAD_FUNCTION_SCREEN_FAILED'
        for tag in ['access','vehicle','motor_vehicle',{'motorcycle':'motorcycle','bus':'bus','truck':'hgv','trailer':'hgv'}.get(v['sumo_vclass'],'motorcar')]:
            if e['tags'].get(tag) in ['no','private','destination','customers','delivery','permit']:return 'SOURCE_ACCESS_RESTRICTED: '+tag
            if tag+':conditional' in e['tags']:return 'SOURCE_CONDITIONAL_ACCESS_UNRESOLVED: '+tag
    for a,b in zip(ids,ids[1:]):
        if not any(c['from']==a and c['to']==b and net.getEdge(a).getLane(int(c['fromLane'])).allows(v['sumo_vclass']) and net.getEdge(b).getLane(int(c['toLane'])).allows(v['sumo_vclass']) for c in connections):return 'EMITTED_LANE_CONNECTION_NOT_ALLOWED'
    return None

def route_batch(folder,mode,requests,home):
    folder.mkdir(parents=True,exist_ok=True);vs={v['id']:v for v in registry()};edges=edge_index(mode);net=sumonet(mode);connections=inspect(mode)['connections']
    trips=ET.Element('routes');results={};eligible=[]
    for q in requests:
        reason=precheck(q,vs[q['vehicle_type_id']],edges,net)
        results[q['id']]={**q,'route_status':'NOT_ROUTABLE','edges':[],'reason':reason,'validation_status':'PROVISIONAL_ASSUMPTIONS' if mode=='provisional' else 'STRICT_DIRECTION_WITH_PARAMETER_ASSUMPTIONS'}
        if not reason:
            ET.SubElement(trips,'trip',id=q['id'],type=q['vehicle_type_id'],depart=str(q['depart_seconds']),**{'from':q['origin_edge'],'to':q['destination_edge']},departLane='best',departSpeed='0');eligible.append(q)
    save(folder/'requested-trips.json',{'category':'SYNTHETIC_TEST','requests':requests});xml(folder/'generated.trips.xml',trips)
    xml(folder/'vehicle-types.rou.xml',types_element(registry()))
    routed=folder/'duarouter.rou.xml'
    # ignore-errors keeps subsequent requests routable; every skipped request is reconciled below.
    log=execute([home/'bin/duarouter.exe','-n',M03/mode/'network.net.xml','-r',str(folder/'vehicle-types.rou.xml')+','+str(folder/'generated.trips.xml'),'-o',routed,'--repair','false','--ignore-errors','true','--seed','20261031','--no-step-log','true'],folder/'routing-log.json')
    if log['returncode']!=0:raise RuntimeError('DUAROUTER failed as a process; see '+str(folder/'routing-log.json'))
    emitted={q.get('id'):q.find('route').get('edges').split() for q in ET.parse(routed).getroot().findall('vehicle') if q.find('route') is not None}
    final=ET.Element('routes')
    for q in requests:
        row=results[q['id']]
        if row['reason']:continue
        ids=emitted.get(q['id'])
        reason=validate_route(ids,q,vs[q['vehicle_type_id']],edges,net,connections) if ids else 'DUAROUTER_NO_ROUTE: see complete routing-log.json'
        if reason:row['reason']=reason;continue
        row.update(route_status='ROUTABLE',edges=ids,reason='Actual DUAROUTER route; immutable M03 emitted connections and class permissions checked')
        ve=ET.SubElement(final,'vehicle',id=q['id'],type=q['vehicle_type_id'],depart=str(q['depart_seconds']),departLane='best',departSpeed='0');ET.SubElement(ve,'route',edges=' '.join(ids))
    xml(folder/'accepted.rou.xml',final)
    rows=list(results.values());save(folder/'route-validation.json',{'category':'SIMULATED_RESULT','network_variant':mode,'requested':len(rows),'routable':sum(r['route_status']=='ROUTABLE' for r in rows),'failed':sum(r['route_status']!='ROUTABLE' for r in rows),'results':rows})
    save(folder/'failed-trips.json',{'category':'SIMULATED_RESULT','failures':[r for r in rows if r['route_status']!='ROUTABLE']})
    counts={}
    for r in rows:
        key=(r['od_id'],r['vehicle_type_id']);cell=counts.setdefault(key,{'year':2026,'network_variant':mode,'od_id':r['od_id'],'vehicle_type_id':r['vehicle_type_id'],'origin_zone':r['origin_zone'],'destination_zone':r['destination_zone'],'interval_start_seconds':0,'interval_end_seconds':900,'requested_trips':0,'routable_trips':0,'failed_routes':0,'unit':'trips_per_15_minute_interval','input_category':'SYNTHETIC_TEST','routing_category':'SIMULATED_RESULT','provenance_id':'S-DEMAND-01'})
        cell['requested_trips']+=1;cell['routable_trips']+=r['route_status']=='ROUTABLE';cell['failed_routes']+=r['route_status']!='ROUTABLE'
    save(folder/'od-interval-counts.json',{'schema_version':'m04-1','coverage_fixture':folder.parent.name=='compatibility','rows':list(counts.values())})
    return rows

def analyze_run(folder,rows,config,log,net_hash,run_id):
    trips=ET.parse(folder/'tripinfo.xml').getroot().findall('tripinfo');byid={t.get('id'):t.attrib for t in trips}
    frames=[];history=defaultdict(list)
    for event,el in ET.iterparse(folder/'fcd.xml',events=['end']):
        if el.tag!='timestep':continue
        vehicles=[]
        for v in el.findall('vehicle'):
            d=v.attrib;point={'id':d['id'],'x':float(d['x']),'y':float(d['y']),'speed_m_per_s':float(d['speed']),'lane':d['lane'],'pos_m':float(d['pos']),'type':d['type']}
            if 'posLat' in d:point['pos_lat_m']=float(d['posLat'])
            vehicles.append(point);history[d['id']].append((point['x'],point['y']))
        if vehicles:frames.append({'time_seconds':float(el.get('time')),'vehicles':vehicles})
        el.clear()
    stat=ET.parse(folder/'statistics.xml').getroot();tele=stat.find('teleports');teleports=int(tele.get('total','0')) if tele is not None else None
    vs=stat.find('vehicles');stats=vs.attrib if vs is not None else {}
    states=[]
    for row in rows:
        t=byid.get(row['id']);depart=float(t['depart']) if t else -1;arrival=float(t['arrival']) if t else -1
        pts=history.get(row['id'],[]);moved=any(math.dist(pts[0],p)>1 for p in pts[1:]) if pts else False
        status='NOT_ROUTABLE' if row['route_status']!='ROUTABLE' else 'ARRIVED' if arrival>=0 else 'RUNNING_AT_END' if depart>=0 else 'PENDING_INSERTION'
        states.append({'id':row['id'],'vehicle_type_id':row['vehicle_type_id'],'od_id':row['od_id'],'status':status,'scheduled_depart_seconds':row['depart_seconds'],'actual_depart_seconds':depart if depart>=0 else None,'arrival_seconds':arrival if arrival>=0 else None,'moved_in_recorded_fcd':moved,'recorded_samples':len(pts),'position_extent_m':max((math.dist(pts[0],p) for p in pts),default=0) if pts else 0,'tripinfo':t})
    count=Counter(s['status'] for s in states);routable=sum(r['route_status']=='ROUTABLE' for r in rows)
    metrics={'run_id':run_id,'category':'SIMULATED_RESULT','label':LABEL,'seed':config['seed'],'sumo_version':'1.28.0','network_sha256':net_hash,'requested_trips':len(rows),'routable_trips':routable,'failed_routes':len(rows)-routable,
        'loaded_vehicles':int(stats['loaded']),'departed_vehicles':sum(s['actual_depart_seconds'] is not None for s in states),'arrived_vehicles':count['ARRIVED'],'running_at_end':count['RUNNING_AT_END'],'pending_insertion':count['PENDING_INSERTION'],'moved_vehicles_recorded':sum(s['moved_in_recorded_fcd'] for s in states),'teleported_vehicles':teleports,
        'simulation_start_seconds':0,'simulation_end_seconds':config['simulation_end_seconds'],'simulation_step_seconds':config['step_length_seconds'],'wall_seconds':log['wall_seconds'],'simulated_seconds_per_wall_second':config['simulation_end_seconds']/log['wall_seconds'],'process_cpu_seconds':log['cpu_seconds'],'cpu_one_core_percent':log['cpu_one_core_percent'],'peak_working_set_bytes_sampled':log['peak_working_set_bytes_sampled'],'memory_samples':log['memory_samples'],'measurement_note':log['measurement_note'],'sumo_returncode':log['returncode'],'warnings':[l for l in log['stderr'].splitlines() if l.startswith('Warning:')],'validation_status':'SOFTWARE_SMOKE_ONLY_NOT_CALIBRATED','sumo_vehicle_statistics':stats}
    save(folder/'vehicle-states.json',{'category':'SIMULATED_RESULT','states':states});save(folder/'trajectory.json',{'category':'SIMULATED_RESULT','source':'SUMO FCD output, sampled every 5 seconds. No interpolation/random motion.','run_id':run_id,'frames':frames});save(folder/'metrics.json',metrics)
    return metrics

def simulate(mode,profile,rows,demand_folder,home,config):
    run_id=f'm04-{mode}-{profile}-seed{config["seed"]}';folder=RUNS/run_id;folder.mkdir(parents=True,exist_ok=True)
    c=ET.Element('configuration');inp=ET.SubElement(c,'input');ET.SubElement(inp,'net-file',value=str(M03/mode/'network.net.xml'));ET.SubElement(inp,'route-files',value=str(demand_folder/'vehicle-types.rou.xml')+','+str(demand_folder/'accepted.rou.xml'))
    t=ET.SubElement(c,'time')
    for name,value in [('begin',0),('end',config['simulation_end_seconds']),('step-length',config['step_length_seconds'])]:ET.SubElement(t,name,value=str(value))
    rnd=ET.SubElement(c,'random_number');ET.SubElement(rnd,'seed',value=str(config['seed']))
    processing=ET.SubElement(c,'processing');ET.SubElement(processing,'time-to-teleport',value='300')
    output=ET.SubElement(c,'output')
    for name,value in [('tripinfo-output',folder/'tripinfo.xml'),('tripinfo-output.write-unfinished','true'),('tripinfo-output.write-undeparted','true'),('fcd-output',folder/'fcd.xml'),('device.fcd.period',config['trajectory_period_seconds']),('fcd-output.attributes','id,x,y,speed,lane,pos,type'),('summary-output',folder/'summary.xml'),('statistic-output',folder/'statistics.xml')]:ET.SubElement(output,name,value=str(value))
    report=ET.SubElement(c,'report');ET.SubElement(report,'no-step-log',value='true');xml(folder/'run.sumocfg',c)
    log=execute([home/'bin/sumo.exe','-c',folder/'run.sumocfg','--xml-validation','always'],folder/'simulation-log.json')
    if log['returncode']!=0:raise RuntimeError('SUMO smoke failed: '+str(folder/'simulation-log.json'))
    metrics=analyze_run(folder,rows,config,log,sha(M03/mode/'network.net.xml'),run_id)
    metrics.update(network_variant=mode,profile=profile,demand_sha256=sha(demand_folder/'requested-trips.json'),config_sha256=sha(CONF/'demand-config.json'));save(folder/'metrics.json',metrics)
    save(folder/'run-manifest.json',{'run_id':run_id,'category':'SIMULATED_RESULT','seed':config['seed'],'sumo_version':'1.28.0','network_variant':mode,'network_sha256':metrics['network_sha256'],'demand_sha256':metrics['demand_sha256'],'configuration_sha256':metrics['config_sha256'],'simulation_period_seconds':[0,config['simulation_end_seconds']],'validation_status':metrics['validation_status'],'files':{relative(p,folder):sha(p) for p in folder.iterdir() if p.is_file() and p.name!='run-manifest.json'}})
    return metrics

def compatibility(home,matrix):
    result={}
    for mode in ['strict','provisional']:
        requests=[{'id':f'compat_{mode}_{m["id"]}_{v["id"]}','vehicle_type_id':v['id'],'od_id':m['id'],'origin_zone':m['origin_zone'],'destination_zone':m['destination_zone'],**m['endpoints'][mode],'depart_seconds':i,'network_variant':mode,'category':'SYNTHETIC_TEST','provenance_id':'S-DEMAND-01'} for i,(m,v) in enumerate((m,v) for m in matrix['movements'] for v in registry())]
        result[mode]=route_batch(DEMAND/'compatibility'/mode,mode,requests,home)
        # Independent parser + actual router rejection probe for all vClasses, including denied classes.
        probe=types_element(registry());nb=matrix['movements'][0]['endpoints'][mode]
        for i,v in enumerate(registry()):ET.SubElement(probe,'trip',id='permission_probe_'+v['id'],type=v['id'],depart=str(i),**{'from':nb['origin_edge'],'to':nb['destination_edge']})
        folder=DEMAND/'compatibility'/mode;xml(folder/'permission-probe.trips.xml',probe)
        execute([home/'bin/duarouter.exe','-n',M03/mode/'network.net.xml','-r',folder/'permission-probe.trips.xml','-o',folder/'permission-probe.rou.xml','--ignore-errors','true','--repair','false','--no-step-log','true'],folder/'permission-probe-log.json')
    save(DOC/'compatibility-results.json',result)
    return result

def sublane_test(home):
    """Isolated technical fixture. Never alters or represents Gedangan geometry."""
    folder=RUNS/'isolated-motorcycle-sublane';folder.mkdir(parents=True,exist_ok=True)
    nodes=ET.Element('nodes');ET.SubElement(nodes,'node',id='a',x='0',y='0');ET.SubElement(nodes,'node',id='b',x='500',y='0');xml(folder/'fixture.nod.xml',nodes)
    edges=ET.Element('edges');ET.SubElement(edges,'edge',id='fixture',**{'from':'a','to':'b'},numLanes='1',width='3.2',speed='8.33',allow='motorcycle');xml(folder/'fixture.edg.xml',edges)
    log=execute([home/'bin/netconvert.exe','-n',folder/'fixture.nod.xml','-e',folder/'fixture.edg.xml','-o',folder/'fixture.net.xml'],folder/'netconvert-log.json');assert log['returncode']==0
    results={}
    for model in ['regular','sublane']:
        root=types_element([v for v in registry() if v['id']=='motorcycle'],sublane=model=='sublane')
        for i in range(2):
            v=ET.SubElement(root,'vehicle',id=f'motor_{i}',type='motorcycle',depart='0',departLane='0',departPos='5',departSpeed='0',**({'departPosLat':str(-.9 if i==0 else .9)} if model=='sublane' else {}));ET.SubElement(v,'route',edges='fixture')
        xml(folder/f'{model}.rou.xml',root)
        cmd=[home/'bin/sumo.exe','-n',folder/'fixture.net.xml','-r',folder/f'{model}.rou.xml','--end','90','--step-length','.2','--seed','20261031','--fcd-output',folder/f'{model}.fcd.xml','--fcd-output.attributes','id,x,y,speed,lane,pos,type,posLat','--tripinfo-output',folder/f'{model}.tripinfo.xml','--no-step-log','true','--xml-validation','always']
        if model=='sublane':cmd+=['--lateral-resolution','.4']
        log=execute(cmd,folder/f'{model}-log.json');assert log['returncode']==0,log['stderr']
        proof=[]
        for step in ET.parse(folder/f'{model}.fcd.xml').getroot().findall('timestep'):
            vs=step.findall('vehicle')
            if len(vs)==2 and vs[0].get('lane')==vs[1].get('lane'):
                longitudinal=abs(float(vs[0].get('pos'))-float(vs[1].get('pos')));lateral=abs(float(vs[0].get('y'))-float(vs[1].get('y')))
                if longitudinal<2.1 and lateral>=1.0:proof.append({'time':float(step.get('time')),'longitudinal_gap_m':longitudinal,'lateral_center_gap_m':lateral,'vehicles':[v.attrib for v in vs]})
        results[model]={'returncode':log['returncode'],'arrived':sum(float(v.get('arrival'))>=0 for v in ET.parse(folder/f'{model}.tripinfo.xml').getroot().findall('tripinfo')),'same_lane_lateral_overlap_samples':len(proof),'first_proof':proof[:1],'wall_seconds':log['wall_seconds'],'peak_working_set_bytes_sampled':log['peak_working_set_bytes_sampled'],'warnings':log['stderr'],'category':'SIMULATED_RESULT'}
    results.update(scope='Isolated 500m synthetic single-lane fixture, not Gedangan. Two 0.8m motorcycles, explicit lateral departure positions ±0.9m; not spontaneous Indonesian filtering or calibrated behavior.',enabled_on_gedangan=False)
    save(folder/'results.json',results);return results

def verify_baseline():
    mismatches=[p for p,h in load(DOC/'previous-milestones-sha256.json').items() if sha(ROOT/p)!=h]
    if mismatches:raise RuntimeError('Previous milestone changed: '+str(mismatches))

def finalize_manifests():
    inputs={relative(p,ROOT):sha(p) for p in list(CONF.glob('*.json'))+[DEMAND/'od-zones.json',DEMAND/'od-matrix.fixture.json']}
    code={relative(p,ROOT):sha(p) for p in [Path(__file__),CONF/'build_demand.py',ROOT/'configuration/sumo_env_m02.py']}
    for metric in load(DOC/'run-summary.json'):
        folder=RUNS/metric['run_id'];manifest=load(folder/'run-manifest.json');manifest.update(input_sha256=inputs,code_sha256=code);save(folder/'run-manifest.json',manifest)
        mode=metric['network_variant'];batch=DEMAND/'compatibility'/mode if metric['profile']=='smoke' else DEMAND/mode/metric['profile']
        save(batch/'demand-manifest.json',{'run_id':metric['run_id'],'category':'SYNTHETIC_TEST','network_sha256':sha(M03/mode/'network.net.xml'),'seed':metric['seed'],'sumo_version':'1.28.0','input_sha256':inputs,'code_sha256':code,'validation_status':'FAILURES_RETAINED','files':{relative(p,batch):sha(p) for p in batch.iterdir() if p.is_file() and p.name!='demand-manifest.json'}})
    isolated=RUNS/'isolated-motorcycle-sublane'
    save(isolated/'run-manifest.json',{'category':'SIMULATED_RESULT','scope':'ISOLATED_SYNTHETIC_NOT_GEDANGAN','seed':20261031,'sumo_version':'1.28.0','network_sha256':sha(isolated/'fixture.net.xml'),'simulation_period_seconds':[0,90],'simulation_step_seconds':.2,'validation_status':'TECHNICAL_LATERAL_FIXTURE_ONLY','runs':[{'run_id':'m04-isolated-motorcycle-'+model,'demand_sha256':sha(isolated/f'{model}.rou.xml'),'command_log':f'{model}-log.json'} for model in ['regular','sublane']],'files':{p.name:sha(p) for p in isolated.iterdir() if p.is_file() and p.name!='run-manifest.json'}})

def main():
    verify_baseline();home=activate()
    for exe in ['sumo','duarouter','netconvert']:
        log=execute([home/'bin'/f'{exe}.exe','--version'],DOC/f'{exe}-version.json');assert '1.28.0' in log['stdout']
    schema=ET.parse(home/'data/xsd/types/route.xsd').getroot();attributes={e.get('name') for e in schema.iter() if e.tag.endswith('attribute')}
    assert all(k in attributes for v in registry() for k in v['parameters'])
    save(DOC/'attribute-support.json',{'sumo_version':'1.28.0','installed_xsd':str(home/'data/xsd/types/route.xsd'),'xsd_sha256':sha(home/'data/xsd/types/route.xsd'),'all_registry_attributes_present':True,'attributes':sorted(registry()[0]['parameters']),'runtime_parser_validation':'All types included in every --xml-validation always simulation'})
    xml(DEMAND/'vehicle-types.rou.xml',types_element(registry()));shutil.copy2(CONF/'vehicle-registry.json',DEMAND/'vehicle-types.json')
    config=load(CONF/'demand-config.json');validate_inputs(registry(),config);matrix=make_zones();compat=compatibility(home,matrix);summaries=[]
    for mode in ['strict','provisional']:
        metrics=simulate(mode,'smoke',compat[mode],DEMAND/'compatibility'/mode,home,config);summaries.append(metrics)
        print(mode,'dedicated smoke',metrics['departed_vehicles'],'departed',metrics['arrived_vehicles'],'arrived',flush=True)
    # Increasing requested load; each smaller run measured before the next tier starts.
    for profile in ['low','medium','stress']:
        for mode in ['strict','provisional']:
            folder=DEMAND/mode/profile;requests=generate(mode,profile,config,matrix);rows=route_batch(folder,mode,requests,home);metrics=simulate(mode,profile,rows,folder,home,config);summaries.append(metrics)
            print(mode,profile,{k:metrics[k] for k in ['requested_trips','routable_trips','departed_vehicles','arrived_vehicles','pending_insertion','teleported_vehicles','wall_seconds']},flush=True)
    sublane=sublane_test(home);verify_baseline()
    issue={'issues':[{'id':'M03-PERM-01','severity':'blocking_multiclass_smoke','source':'All M03 external lanes allow passenger only','impact':'9 of 10 local types denied; vehicle classes are not relabelled passenger to bypass this. Heavy/motor Gedangan simulation not validated.','resolution':'Requires separately reviewed M03 permission policy update based on source access; no change performed in M04.'},
        {'id':'M03-CONN-02','severity':'route_coverage','impact':'Strict feeder/main and east Ketajen station endpoints remain unroutable; no automatic topology repair.'},
        {'id':'M03-GEOM-03','severity':'oversize_clearance','impact':'No surveyed width, height, swept paths or permits. Oversize always withheld. Lane-width screen for other classes is only an assumption.'},
        {'id':'M03-JUNCTION-04','severity':'unresolved','impact':'Sharp/internal connector geometry and assumed priority controls inherited; simulated delay is not observed Gedangan congestion.'}], 'm03_modified':False}
    save(DOC/'M03-issue-register.json',issue)
    export={'schema_version':'m04-1','label':LABEL,'baseline_year':2026,'sumo_version':'1.28.0','sumo_status':'OFFLINE_RECORDED_RUNS_COMPLETE','field_calibrated':False,'registry':registry(),'zones':load(DEMAND/'od-zones.json')['zones'],'matrix':matrix,'config':config,'runs':summaries,'compatibility':compat,'sublane':sublane,'issues':issue['issues']}
    web=ROOT/'frontend/public/demand/m04';web.mkdir(parents=True,exist_ok=True);save(web/'summary.json',export)
    for m in summaries:
        rid=m['run_id'];source=DEMAND/'compatibility'/m['network_variant'] if m['profile']=='smoke' else DEMAND/m['network_variant']/m['profile'];shutil.copy2(RUNS/rid/'trajectory.json',web/f'{rid}.trajectory.json');shutil.copy2(source/'route-validation.json',web/f'{rid}.routes.json')
    save(DOC/'run-summary.json',summaries)
    save(DOC/'build-manifest.json',{'category':'SIMULATED_RESULT','source_m03_files_sha256':{relative(p,M03):sha(p) for p in M03.rglob('*') if p.is_file()},'configuration_sha256':{p.name:sha(p) for p in CONF.glob('*.json')},'run_ids':[m['run_id'] for m in summaries],'previous_milestones_unchanged':True,'m05_started':False})
    finalize_manifests()

if __name__=='__main__':main()
