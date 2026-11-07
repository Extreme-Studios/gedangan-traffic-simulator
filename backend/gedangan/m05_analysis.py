"""Postprocess actual trajectories, control events and conservative spillback evidence."""
import xml.etree.ElementTree as ET
from collections import defaultdict
from .m04_demand import ROOT,load,save,sha
from .m05_railway import CROSSING
RUNS=ROOT/'simulation/runs/m05';DOC=ROOT/'documentation/m05'
def analyze(folder):
    playback=load(folder/'playback.json');r=playback['result'];frames=playback['frames'];mode=r['mode'];net=ET.parse(ROOT/r.get('network_path',f'simulation/network/m05/{mode}/network.net.xml')).getroot()
    lanes={l.get('id'):{'edge':e.get('id'),'length':float(l.get('length'))} for e in net.findall('edge') for l in e.findall('lane')};edges={e.get('id'):e for e in net.findall('edge')};connections={}
    for c in net.findall('connection'):
        if c.get('from','').startswith(':'):continue
        connections[(c.get('from')+'_'+c.get('fromLane'),c.get('to')+'_'+c.get('toLane'))]=c.attrib
    incoming_edges={c.get('to') for c in net.findall('connection') if not c.get('from','').startswith(':') and not c.get('from','').startswith('m05_rail_')}
    specs={v['id']:v for v in load(folder/'demand.json')['vehicles']};dimensions={v['id']:v['parameters'] for v in load(ROOT/'configuration/demand-m04/vehicle-registry.json')['vehicles']}
    signal_red={};signal_release=[];behavior={};previous={};max_extent=0;
    counters=defaultdict(float);spill=[];violations=[];stops={};released=[];rail=[];train_samples=defaultdict(list);timeline=[]
    for f in frames:
        vs=f['vehicles'];bylane=defaultdict(list)
        for v in vs:bylane[v['lane']].append(v)
        for lane,q in f['queues'].items():
            q['lane_start_reached']=q['tail_position']<5
            q['boundary_censored']=q['tail_position']<5 and lanes.get(lane,{}).get('edge') not in incoming_edges
            q['occupancy_percent']=min(100,sum(dimensions.get(w['type'],{'length':80})['length'] for w in bylane[lane])/lanes[lane]['length']*100) if lane in lanes else None
        active=set()
        max_extent=max(max_extent,max([q['extent_m'] for q in f['queues'].values()],default=0))
        for lane,vehicles in bylane.items():
            ordered=sorted(vehicles,key=lambda v:v['pos'])
            for i,v in enumerate(ordered):
                b=behavior.setdefault(v['type'],{'minimum_acceleration_1s':0,'maximum_acceleration_1s':0,'minimum_same_lane_leader_gap_m':None,'samples':0})
                b['samples']+=1
                if v['id'] in previous:
                    pt,ps=previous[v['id']];a=(v['speed']-ps)/(f['time']-pt);b['minimum_acceleration_1s']=min(b['minimum_acceleration_1s'],a);b['maximum_acceleration_1s']=max(b['maximum_acceleration_1s'],a)
                previous[v['id']]=(f['time'],v['speed'])
                if i+1<len(ordered) and lane in lanes and not lane.startswith(':'):
                    lead=ordered[i+1];gap=lead['pos']-dimensions.get(lead['type'],{'length':80})['length']-v['pos']
                    if gap>=0:b['minimum_same_lane_leader_gap_m']=min(b['minimum_same_lane_leader_gap_m'] if b['minimum_same_lane_leader_gap_m'] is not None else gap,gap)
        for (up,down),conn in connections.items():
            if conn.get('tl')!='m05_gedangan':continue
            state=f['signals'].get('m05_gedangan','');signal=state[int(conn['linkIndex'])] if state else ''
            for v in bylane.get(up,[]):
                if lanes[up]['length']-v['pos']>30 or v['id'] not in specs:continue
                route=specs[v['id']]['edges'];edge=lanes[up]['edge'];nextedge=lanes[down]['edge']
                if edge not in route or route.index(edge)+1>=len(route) or route[route.index(edge)+1]!=nextedge:continue
                if signal in 'rR' and v['speed']<.3:signal_red.setdefault(v['id'],{'time':f['time'],'lane':up,'link_index':conn['linkIndex']})
                if signal in 'Gg' and v['speed']>1 and v['id'] in signal_red and not any(x['vehicle']==v['id'] for x in signal_release):signal_release.append({'vehicle':v['id'],'red_stop':signal_red[v['id']],'green_release_time':f['time'],'green_link_index':conn['linkIndex']})
        for (up,down),conn in connections.items():
            q=f['queues'].get(down)
            if not q or q['tail_position']>=5:continue
            for v in bylane.get(up,[]):
                if v['speed']>=.3 or lanes[up]['length']-v['pos']>10 or v['id'] not in specs:continue
                route=specs[v['id']]['edges'];edge=lanes[up]['edge'];nextedge=lanes[down]['edge']
                if edge not in route or route.index(edge)+1>=len(route) or route[route.index(edge)+1]!=nextedge:continue
                state=f['signals'].get(conn.get('tl'),'')
                if conn.get('tl') and (not state or state[int(conn['linkIndex'])] not in 'GgOo'):continue
                key=(up,down,v['id']);active.add(key);counters[key]+=1
                if counters[key]==5:
                    occupancy=min(100,sum(dimensions.get(w['type'],{'length':80})['length'] for w in bylane[down])/lanes[down]['length']*100)
                    spill.append({'time':f['time'],'duration_at_detection_s':5,'upstream_lane':up,'downstream_lane':down,'vehicle':v['id'],'downstream_tail_m':q['tail_position'],'downstream_occupancy_percent':round(occupancy,2),'movement_state':state or 'uncontrolled source connection','category':'SIMULATED_CANDIDATE','limitation':'Queue storage and route intent verified; right-of-way conflicts at uncontrolled junctions can also affect discharge. Not a calibrated Gedangan conclusion.'})
        for key in list(counters):
            if key not in active:counters[key]=0
        gate=f['signals'].get(CROSSING,'')
        for v in vs:
            if v['id'].startswith('train_'):train_samples[v['id']].append((f['time'],v));continue
            if v['speed']<.3 and v['lane'].startswith('w1240685448_s1_p') and 'r' in gate:stops.setdefault(v['id'],f['time'])
            if v['id'] in stops and v['speed']>1 and gate and all(s in 'Gg' for s in gate) and v['id'] not in [x['vehicle'] for x in released]:released.append({'vehicle':v['id'],'stopped_at':stops[v['id']],'released_at':f['time']})
            if v['lane'].startswith(':'+CROSSING+'_') and all(s in 'rR' for s in gate):violations.append({'time':f['time'],'vehicle':v['id'],'lane':v['lane'],'state':gate})
    if train_samples:
        route=load(ROOT/f'simulation/network/m05/{mode}/rail-provenance.json')['route'];chain=[]
        for i,eid in enumerate(route):
            chain.append(eid+'_0')
            if i+1<len(route):
                cc=connections.get((eid+'_0',route[i+1]+'_0'))
                if cc and cc.get('via'):chain.append(cc['via'])
        offsets={};offset=0
        for lane in chain:offsets[lane]=offset;offset+=lanes[lane]['length']
        crosslanes=[l for l in chain if l.startswith(':'+CROSSING+'_')];start=min(offsets[l] for l in crosslanes);end=max(offsets[l]+lanes[l]['length'] for l in crosslanes)
        for tid,samples in train_samples.items():
            distance=[(t,offsets[v['lane']]+v['pos']) for t,v in samples if v['lane'] in offsets]
            first=lambda threshold:next((t for t,d in distance if d>=threshold),None)
            rail.append({'train':tid,'approach_120m':first(start-120),'front_entry':first(start),'rear_exit':first(end+80),'sample_resolution_s':1,'movement_observed':any(v['speed']>.1 for t,v in samples),'category':'SIMULATED_EVENT'})
    summary=ET.parse(folder/'summary.xml').getroot().findall('step');r['loaded']=int(summary[-1].get('loaded')) if summary else r['loaded']
    roadtrips=[v for v in ET.parse(folder/'tripinfo.xml').getroot().findall('tripinfo') if not v.get('id').startswith('train_')]
    r['arrived_road']=len(roadtrips);r['not_departed']=r['requested_road']+r['requested_train']-r['departed'];r['mean_road_trip_duration_s']=sum(float(v.get('duration')) for v in roadtrips)/len(roadtrips) if roadtrips else None
    r['mean_road_waiting_s']=sum(float(v.get('waitingTime')) for v in roadtrips)/len(roadtrips) if roadtrips else None
    r['rail_event_evidence']=rail;r['gate_stopped_then_released']=released;r['road_inside_crossing_while_red_samples']=violations;r['spillback_candidates']=spill;r['spillback_status']='CANDIDATES_REQUIRING_PRIORITY_CAUSALITY_REVIEW' if spill else 'NEGATIVE_IN_THIS_SETUP: no five-second upstream blockage with downstream tail within five metres and available signal movement'
    r['signal_stopped_then_released']=signal_release;r['behavior_measurements']=behavior;r['maximum_queue_extent_m']=max_extent;r['boundary_censored_samples']=sum(q['boundary_censored'] for f in frames for q in f['queues'].values());r['maximum_active_vehicles']=max(len(f['vehicles']) for f in frames);r['simulation_speed_ratio']=900/r['runtime_wall_seconds'];r['maximum_pending_insertion']=max(int(x.get('waiting','0')) for x in summary) if summary else None
    r['train_actual_departures']=[dict(v.attrib) for v in ET.parse(folder/'tripinfo.xml').getroot().findall('tripinfo') if v.get('id').startswith('train_')]
    r['failure_record']={'route_failures':0,'not_departed':r['not_departed'],'still_running':len(r['running']),'teleports':len(r['teleports']),'collisions':len(r['collisions'])}
    counts=[{'time':f['time'],'stopped_count':sum(q['count'] for q in f['queues'].values()),'maximum_front_to_front_extent_m':max([q['extent_m'] for q in f['queues'].values()],default=0),'boundary_censored_lanes':[lane for lane,q in f['queues'].items() if q['boundary_censored']]} for f in frames]
    save(folder/'queue-timeline.json',counts)
    r['stopped_road_vehicle_seconds_1s']=sum(x['stopped_count'] for x in counts)
    trips_by_id={x.get('id'):x for x in ET.parse(folder/'tripinfo.xml').getroot().findall('tripinfo')}
    last_vehicles={v['id']:v for v in frames[-1]['vehicles']}
    life=[]
    for vid in list(specs)+[f'train_{i}' for i in range(r['requested_train'])]:
        trip=trips_by_id.get(vid);state='ARRIVED' if trip is not None else 'RUNNING_AT_HORIZON' if vid in r['running'] else 'NOT_DEPARTED'
        life.append({'id':vid,'type':specs[vid]['type'] if vid in specs else 'm05_train','status':state,'tripinfo':dict(trip.attrib) if trip is not None else None,'last_sample':last_vehicles.get(vid),'right_censored':state!='ARRIVED'})
    save(folder/'vehicle-lifecycle.json',life)
    playback['result']=r;save(folder/'result.json',r);save(folder/'playback.json',playback);save(folder/'crossing-events.json',{'trains':rail,'control_events':[e for e in playback['events'] if e['controller']==CROSSING],'road_stops':stops,'road_releases':released,'red_occupancy_samples':violations,'resolution_s':1});save(folder/'spillback-events.json',spill)
    return r

def main():
    results=[analyze(p.parent) for p in sorted(RUNS.glob('*/result.json')) if (p.parent/'playback.json').exists()]
    save(DOC/'scenario-results.json',results)
    pairs=[]
    for seed in [42,43]:
        for a,b in [('A_free','B_signal'),('A_free','C_single'),('B_signal','E_combined'),('A_free','D_two'),('A_free','D_consecutive'),('C_single','D_long'),('F_high_free','F_high_signal')]:
            names=[f'{x}_seed{seed}' for x in [a,b]];rows=[next((r for r in results if r['name']==n),None) for n in names]
            if all(rows):pairs.append({'runs':names,'identical_demand':rows[0]['demand_sha256']==rows[1]['demand_sha256'],'identical_network':rows[0]['network_sha256']==rows[1]['network_sha256'],'identical_seed':True,'window_s':[0,900],'warmup_s':0,'note':'Finite synthetic pulse, not steady-state estimation; all unserved demand retained in denominator.'})
    save(DOC/'paired-comparisons.json',pairs)
if __name__=='__main__':main()
