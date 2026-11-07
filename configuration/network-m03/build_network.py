"""Deterministic local M02 -> constrained SUMO networks. No traffic simulation."""
from collections import Counter,defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pyproj import Transformer

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from configuration.sumo_env_m02 import activate

OUT=ROOT/'simulation/network/m03'
DOC=ROOT/'documentation/m03'
CONF=ROOT/'configuration/network-m03'

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def xml(p,root):
    ET.indent(root);ET.ElementTree(root).write(p,encoding='utf-8',xml_declaration=True)
def xmlhash(p):return hashlib.sha256(ET.tostring(ET.parse(p).getroot())).hexdigest()
def run(args,log):
    p=subprocess.run([str(x) for x in args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120,creationflags=subprocess.CREATE_NO_WINDOW)
    write(log,{'command':[str(x) for x in args],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    return p
def angle(a,b):
    va=(a['shape'][-1][0]-a['shape'][-2][0],a['shape'][-1][1]-a['shape'][-2][1]);vb=(b['shape'][1][0]-b['shape'][0][0],b['shape'][1][1]-b['shape'][0][1]);norm=math.hypot(*va)*math.hypot(*vb)
    return math.degrees(math.acos(max(-1,min(1,(va[0]*vb[0]+va[1]*vb[1])/norm)))) if norm else 180
def connected_components(edges):
    graph=defaultdict(set)
    for e in edges:graph[e['from']].add(e['to']);graph[e['to']].add(e['from'])
    todo=set(graph);groups=[]
    while todo:
        seed=min(todo);todo.remove(seed);part={seed};stack=[seed]
        while stack:
            for n in graph[stack.pop()]:
                if n not in part:part.add(n);todo.discard(n);stack.append(n)
        groups.append(sorted(part))
    return sorted(groups,key=lambda g:(-len(g),g[0]))

def direction(tags,mode,policy):
    val=tags.get('oneway')
    if val in {'yes','1','true'}:return [1],'VERIFIED','Explicit OSM oneway='+val
    if val=='-1':return [-1],'VERIFIED','Explicit OSM reversed oneway'
    if val in {'no','0','false'}:return [1,-1],'VERIFIED','Explicit OSM bidirectional'
    if val is not None:return [],'MISSING','Unsupported/reversible/conditional oneway requires review'
    if tags.get('junction')=='roundabout' or tags.get('highway')=='motorway':return [1],'INFERRED','Documented OSM implied oneway; not field verification'
    if mode=='provisional' and tags.get('highway') in policy['provisional_bidirectional_highways'] and not any('oneway:' in k or k.endswith(':conditional') for k in tags):
        return [1,-1],'ASSUMPTION','P-DIR-01: temporary bidirectional for whitelisted highway class, not OSM explicit direction'
    return [],'MISSING','Direction unknown; excluded by strict policy or provisional class/conditional guard'

def construct(mode,features,nodes,xy,special,relations,policy):
    edges=[];decisions=[];source_to_edge=defaultdict(list)
    for f in features:
        p=f['properties'];tags=p['tags'];reasons=[]
        for key in ['access','vehicle','motor_vehicle','motorcar']:
            if tags.get(key) in policy['excluded_access_values']:reasons.append(key+'='+tags[key])
        if tags.get('motorcar')=='no' or tags.get('motor_vehicle')=='no':reasons.append('Passenger vehicle explicitly disallowed')
        if any(k.endswith(':conditional') and k.split(':')[0] in {'access','vehicle','motor_vehicle','motorcar','oneway'} for k in tags):reasons.append('Conditional road access/direction not modelled')
        dirs,status,basis=direction(tags,mode,policy)
        if not dirs:reasons.append(basis)
        if reasons:decisions.append({'source_feature_id':f['id'],'source_way_id':p['osm_id'],'action':'EXCLUDED','reasons':reasons});continue
        ids=p['osm_node_ids'];cuts=[0]+[i for i in range(1,len(ids)-1) if ids[i] in special]+[len(ids)-1]
        for piece,(left,right) in enumerate(zip(cuts,cuts[1:])):
            sub=ids[left:right+1]
            if sub[0]==sub[-1]:
                # Preserve genuine roundabout loops by splitting at an existing midpoint node.
                mid=len(sub)//2
                chunks=[sub[:mid+1],sub[mid:]] if len(sub)>2 else []
            else:chunks=[sub]
            for loopindex,chunk in enumerate(chunks):
                if sum(math.dist(xy[a],xy[b]) for a,b in zip(chunk,chunk[1:]))<.01:
                    decisions.append({'source_feature_id':f['id'],'action':'EXCLUDED','reasons':['Zero/sub-centimeter geometry; no artificial replacement']});continue
                for sign in dirs:
                    useids=chunk if sign==1 else list(reversed(chunk));eid=f"w{p['osm_id']}_s{f['id'].split(':')[-1]}_p{piece}_{loopindex}_{'f' if sign==1 else 'r'}"
                    lanes=p['lanes'];lane_status='VERIFIED';lane_basis='OSM lanes on explicit one-way'
                    if len(dirs)>1:
                        key='lanes:forward' if sign==1 else 'lanes:backward';v=tags.get(key)
                        if v and str(v).isdigit():lanes=int(v);lane_basis='OSM '+key
                        else:lanes=max(1,int(lanes)//2) if lanes else policy['temporary_lanes_per_direction'];lane_status='ASSUMPTION';lane_basis='A-LANE-02: temporary per-direction allocation; total lane tag retained separately'
                    elif not lanes:lanes=policy['temporary_lanes_per_direction'];lane_status='ASSUMPTION';lane_basis='A-LANE-01: topology-only placeholder'
                    speed=p['maxspeed_kmh']/3.6 if p['maxspeed_kmh'] is not None else policy['temporary_speed_m_per_s'];speed_status='VERIFIED' if p['maxspeed_kmh'] is not None else 'ASSUMPTION'
                    width=(p['width_m']/max(1,p['lanes'])) if p['width_m'] and p['lanes'] else policy['temporary_lane_width_m'];width_status='ASSUMPTION' if not(p['width_m'] and p['lanes']) else 'INFERRED'
                    edge={'id':eid,'source_feature_id':f['id'],'source_way_id':p['osm_id'],'osm_node_ids':useids,'from':f'osm_{useids[0]}','to':f'osm_{useids[-1]}','sign':sign,'shape':[xy[n] for n in useids],'name':p['name'],'road_function':p['road_function'],'tags':tags,'lanes':lanes,'speed_m_per_s':speed,'lane_width_m':width,'length_m':sum(math.dist(xy[a],xy[b]) for a,b in zip(useids,useids[1:])),'parameter_status':{'direction':status,'lanes':lane_status,'speed':speed_status,'lane_width':width_status,'priority':'ASSUMPTION','junction_control':'ASSUMPTION','capacity':'MISSING'},'parameter_basis':{'direction':basis,'lanes':lane_basis,'speed':'OSM maxspeed km/h converted to m/s' if speed_status=='VERIFIED' else 'A-SPEED-01: 30 km/h topology fixture placeholder','lane_width':'OSM total width / total lanes' if width_status=='INFERRED' else 'A-WIDTH-01: 3.2m engine placeholder'},'direction_source_status':status,'overall_status':'ASSUMPTION','field_verified':False,'source_url':p['osm_url'],'source_version':p['osm_version'],'source_timestamp':p['osm_timestamp'],'capacity_vehicles_per_hour':None,'boundary_source_flag':p['boundary_terminal']}
                    edges.append(edge);source_to_edge[f['id']].append(eid)
        decisions.append({'source_feature_id':f['id'],'source_way_id':p['osm_id'],'action':'INCLUDED','direction_status':status,'direction_basis':basis,'edge_ids':source_to_edge[f['id']]})
    incoming=defaultdict(list);outgoing=defaultdict(list)
    for e in edges:incoming[e['to']].append(e);outgoing[e['from']].append(e)
    connections=[];blocked=[]
    for node in sorted(set(incoming)&set(outgoing)):
        nid=int(node[4:]);tags=nodes[nid].get('tags',{})
        for a in incoming[node]:
            for b in outgoing[node]:
                reason=None;relation_ids=[];deflection=angle(a,b)
                if a['from']==b['to'] or deflection>policy['provisional_max_deflection_degrees']:reason='U-turn / reverse movement conservatively excluded'
                if tags.get('barrier') and tags['barrier']!='cattle_grid':reason='Mapped barrier node quarantined for passenger routing'
                for rel in relations:
                    members=rel['members'];fr={m['ref'] for m in members if m['role']=='from' and m['type']=='way'};to={m['ref'] for m in members if m['role']=='to' and m['type']=='way'};vn={m['ref'] for m in members if m['role']=='via' and m['type']=='node'};vw={m['ref'] for m in members if m['role']=='via' and m['type']=='way'}
                    if a['source_way_id'] not in fr:continue
                    rt=rel['tags'].get('restriction','');conditional=rel['tags'].get('restriction:conditional')
                    if (nid in vn and ((rt.startswith('no_') and b['source_way_id'] in to) or (rt.startswith('only_') and b['source_way_id'] not in to))) or (vw and b['source_way_id'] in vw):
                        reason='OSM restriction / conservative via-way entry quarantine';relation_ids.append(rel['id'])
                    if conditional and ((nid in vn and b['source_way_id'] in to) or b['source_way_id'] in vw):reason='Conditional restriction conservatively active at all times';relation_ids.append(rel['id'])
                continuity=(a['source_way_id']==b['source_way_id'] and a['sign']==b['sign'])
                crosscontinuity=deflection<=policy['strict_cross_way_continuity_max_degrees'] and ((a['road_function']==b['road_function']=='main_arterial_road') or (a['name'] is not None and a['name']==b['name']))
                if mode=='strict' and not(continuity or crosscontinuity):reason=reason or 'Strict: unconfirmed cross-way turning movement excluded'
                if reason:blocked.append({'from':a['id'],'to':b['id'],'node':node,'reason':reason,'restriction_relation_ids':relation_ids});continue
                for lane in range(a['lanes']):
                    connections.append({'from':a['id'],'to':b['id'],'fromLane':lane,'toLane':min(lane,b['lanes']-1),'node':node,'topology_status':'INFERRED','lane_assignment_status':'ASSUMPTION','basis':'Same OSM shared node; source-way continuation' if continuity else 'Same OSM shared node; continuity/turn inference, not field-verified legal movement','deflection_degrees':round(deflection,3)})
    return edges,connections,blocked,decisions

def convert(mode,edges,connections,blocked,nodes,xy,origin,policy,home,relations):
    dest=OUT/mode;dest.mkdir(parents=True,exist_ok=True)
    ns=ET.Element('nodes');used=sorted({n for e in edges for n in e['osm_node_ids']})
    ll=[(nodes[n]['lon'],nodes[n]['lat']) for n in used];local=[xy[n] for n in used]
    ET.SubElement(ns,'location',netOffset=f'{-origin[0]},{-origin[1]}',convBoundary=','.join(map(str,[min(x for x,y in local),min(y for x,y in local),max(x for x,y in local),max(y for x,y in local)])),origBoundary=','.join(map(str,[min(x for x,y in ll),min(y for x,y in ll),max(x for x,y in ll),max(y for x,y in ll)])),projParameter='+proj=utm +zone=49 +south +datum=WGS84 +units=m +no_defs')
    for n in used:ET.SubElement(ns,'node',id=f'osm_{n}',x=f'{xy[n][0]:.6f}',y=f'{xy[n][1]:.6f}',type='priority',radius=str(policy['temporary_junction_radius_m']))
    es=ET.Element('edges')
    for e in edges:
        elem=ET.SubElement(es,'edge',id=e['id'],**{'from':e['from'],'to':e['to'],'numLanes':str(e['lanes']),'speed':f"{e['speed_m_per_s']:.6f}",'width':f"{e['lane_width_m']:.6f}",'priority':str(policy['temporary_priority']),'spreadType':'center','allow':'passenger','shape':' '.join(f'{x:.6f},{y:.6f}' for x,y in e['shape'])})
        for key,val in {'osm_way_id':e['source_way_id'],'m02_feature':e['source_feature_id'],'variant':mode,'direction_status':e['direction_source_status'],'data_status':'ASSUMPTION'}.items():ET.SubElement(elem,'param',key=key,value=str(val))
    cs=ET.Element('connections')
    for c in connections:ET.SubElement(cs,'connection',**{k:str(c[k]) for k in ['from','to','fromLane','toLane']})
    xml(dest/'nodes.nod.xml',ns);xml(dest/'edges.edg.xml',es);xml(dest/'connections.con.xml',cs)
    cfg=ET.Element('configuration');inp=ET.SubElement(cfg,'input')
    for key,value in [('node-files','nodes.nod.xml'),('edge-files','edges.edg.xml'),('connection-files','connections.con.xml')]:ET.SubElement(inp,key,value=value)
    output=ET.SubElement(cfg,'output');ET.SubElement(output,'output-file',value='initial.net.xml')
    processing=ET.SubElement(cfg,'processing')
    for key,value in [('lefthand','true'),('no-turnarounds','true'),('offset.disable-normalization','true'),('geometry.remove','false'),('junctions.join','false')]:ET.SubElement(processing,key,value=value)
    xml(dest/'build.netccfg',cfg)
    p=run([home/'bin/netconvert.exe','-c',dest/'build.netccfg'],dest/'netconvert-initial-log.json')
    if p.returncode:raise RuntimeError(mode+' initial NETCONVERT failed: '+p.stderr[-1500:])
    expected={(c['from'],c['to'],str(c['fromLane']),str(c['toLane'])) for c in connections}
    def actual(path):return {(c.get('from'),c.get('to'),c.get('fromLane'),c.get('toLane')) for c in ET.parse(path).getroot().findall('connection') if not c.get('from','').startswith(':')}
    extra=actual(dest/'initial.net.xml')-expected
    deletes=ET.Element('connections')
    for a,b,i,j in sorted(extra):ET.SubElement(deletes,'delete',**{'from':a,'to':b,'fromLane':i,'toLane':j})
    xml(dest/'remove-guessed.con.xml',deletes)
    p=run([home/'bin/netconvert.exe','--sumo-net-file',dest/'initial.net.xml','--connection-files',dest/'remove-guessed.con.xml','--output-file',dest/'network.net.xml','--no-turnarounds','true','--offset.disable-normalization','true'],dest/'netconvert-final-log.json')
    if p.returncode:raise RuntimeError(mode+' final NETCONVERT failed: '+p.stderr[-1500:])
    got=actual(dest/'network.net.xml')
    if got-expected:raise AssertionError('Unapproved generated connections survived')
    write(dest/'source-to-edge.json',{'variant':mode,'edges':edges})
    write(dest/'connection-provenance.json',{'variant':mode,'approved_connections':connections,'blocked_movements':blocked,'removed_guessed_connections':[list(c) for c in sorted(extra)],'approved_but_not_emitted':[list(c) for c in sorted(expected-got)]})
    overlay=ET.Element('additional')
    rail=load(ROOT/'geodata/railways/rail_tracks.geojson')['features'];fwd=Transformer.from_crs(4326,32749,always_xy=True)
    for i,f in enumerate(rail):
        coords=[fwd.transform(*p) for p in f['geometry']['coordinates']];ET.SubElement(overlay,'poly',id=f'rail_reference_{i}',type='STATIC_OSM_RAIL_REFERENCE_NOT_SIMULATED',color='1,0.8,0.2',fill='false',layer='10',lineWidth='1.5',shape=' '.join(f'{x-origin[0]:.6f},{y-origin[1]:.6f}' for x,y in coords))
    crossings=load(ROOT/'geodata/railways/level_crossings.geojson')['features']
    for f in crossings:
        x,y=fwd.transform(*f['geometry']['coordinates']);ET.SubElement(overlay,'poi',id='crossing_'+str(f['properties']['osm_id']),type='REFERENCE_ONLY_NO_CLOSURE',color='1,0.3,0.5',x=f'{x-origin[0]:.6f}',y=f'{y-origin[1]:.6f}',layer='20',width='8',height='8')
    xml(dest/'rail-reference.add.xml',overlay)
    sim=ET.Element('configuration');inp=ET.SubElement(sim,'input');ET.SubElement(inp,'net-file',value='network.net.xml');ET.SubElement(inp,'additional-files',value='rail-reference.add.xml');time=ET.SubElement(sim,'time');ET.SubElement(time,'begin',value='0');ET.SubElement(time,'end',value='0');xml(dest/'inspect.sumocfg',sim)
    p=run([home/'bin/sumo.exe','-c',dest/'inspect.sumocfg','--no-step-log','true'],dest/'sumo-load-log.json')
    if p.returncode:raise RuntimeError('SUMO network/overlay load failed: '+p.stderr[-1500:])
    root=ET.parse(dest/'network.net.xml').getroot();exportedges=[]
    byid={e['id']:e for e in edges};lanes=0
    for elem in root.findall('edge'):
        if elem.get('function')=='internal':continue
        eid=elem.get('id');source=byid[eid];laneelems=elem.findall('lane');lanes+=len(laneelems)
        geometry=[list(map(float,p.split(','))) for p in laneelems[0].get('shape').split()]
        exportedges.append({**source,'input_speed_m_per_s':source['speed_m_per_s'],'input_lane_width_m':source['lane_width_m'],'speed_m_per_s':float(laneelems[0].get('speed')),'lane_width_m':float(laneelems[0].get('width','3.2')),'shape':geometry,'sumo_lanes':[{'id':l.get('id'),'index':int(l.get('index')),'speed_m_per_s':float(l.get('speed')),'width_m':float(l.get('width','3.2')),'length_m':float(l.get('length')),'shape':[list(map(float,p.split(','))) for p in l.get('shape').split()]} for l in laneelems]})
    jns=[{'id':j.get('id'),'x':float(j.get('x')),'y':float(j.get('y')),'type':j.get('type'),'source_osm_node_id':int(j.get('id')[4:])} for j in root.findall('junction') if j.get('type')!='internal']
    comps=connected_components(edges);compindex={n:i for i,part in enumerate(comps) for n in part}
    for e in exportedges:e['component_id']=compindex[e['from']]
    endpoints=Counter()
    for e in edges:endpoints[e['from']]+=1;endpoints[e['to']]+=1
    qa={'variant':mode,'nodes':len(jns),'edges':len(exportedges),'lanes':lanes,'internal_edges':sum(e.get('function')=='internal' for e in root.findall('edge')),'lane_connections':len(got),'weak_components':len(comps),'component_node_sizes':[len(c) for c in comps],'dead_end_junctions':sum(j['type']=='dead_end' for j in jns),'unapproved_connections':len(got-expected),'withheld_generated_lane_connections':len(extra),'approved_not_emitted':len(expected-got),'source_direction_status_counts':dict(Counter(e['direction_source_status'] for e in edges)),'road_functions':dict(Counter(e['road_function'] for e in edges)),'field_verified':False,'semantic_network_sha256':xmlhash(dest/'network.net.xml'),'net_location':root.find('location').attrib,'strict_meaning':'Known directional evidence and continuity only; lane/speed/control assumptions remain' if mode=='strict' else 'Temporary direction assumptions on whitelisted highway classes; not field-validated routing'}
    original_components=load(ROOT/'geodata/quality_assurance/components.json')['components'];original_index={n:c['index'] for c in original_components for n in c['osm_node_ids']}
    edge_incoming=Counter(b for a,b,i,j in got);edge_outgoing=Counter(a for a,b,i,j in got)
    qa.update(no_incoming_connection_edges=sum(not edge_incoming[e['id']] for e in edges),no_outgoing_connection_edges=sum(not edge_outgoing[e['id']] for e in edges),netconvert_initial_warning_lines=sum(line.startswith('Warning:') for line in load(dest/'netconvert-initial-log.json')['stderr'].splitlines()),netconvert_final_warning_lines=sum(line.startswith('Warning:') for line in load(dest/'netconvert-final-log.json')['stderr'].splitlines()))
    used_components={original_index[n] for e in edges for n in e['osm_node_ids']}
    write(dest/'connectivity.json',{'summary':qa,'components':[{'id':i,'nodes':part,'m02_component_ids':sorted({original_index[int(n[4:])] for n in part}),'edge_ids':[e['id'] for e in edges if e['from'] in set(part)]} for i,part in enumerate(comps)],'m02_original_component_sizes':[c['node_count'] for c in original_components],'m02_components_with_no_imported_nodes':[c['index'] for c in original_components if c['index'] not in used_components],'no_incoming_connection_edge_ids':[e['id'] for e in edges if not edge_incoming[e['id']]],'no_outgoing_connection_edge_ids':[e['id'] for e in edges if not edge_outgoing[e['id']]],'note':'Weak node connectivity does not imply permitted turn reachability; actual DUAROUTER results and lane connection graph retained separately.'})
    internal_lanes={l.get('id'):[list(map(float,p.split(','))) for p in l.get('shape').split()] for e in root.findall('edge') if e.get('function')=='internal' for l in e.findall('lane')}
    emitted_connections=[{'from':c.get('from'),'to':c.get('to'),'fromLane':int(c.get('fromLane')),'toLane':int(c.get('toLane')),'shape':internal_lanes.get(c.get('via'),[]),'topology_status':'INFERRED','lane_assignment_status':'ASSUMPTION'} for c in root.findall('connection') if not c.get('from','').startswith(':')]
    rail_overlay=[{'id':p.get('id'),'shape':[list(map(float,c.split(','))) for c in p.get('shape').split()]} for p in overlay.findall('poly')]
    crossing_overlay=[{'id':p.get('id'),'x':float(p.get('x')),'y':float(p.get('y'))} for p in overlay.findall('poi')]
    boundary=next(f for f in load(ROOT/'frontend/public/geodata/m02/map-utm49s.json')['layers']['boundaries'] if f['id']=='boundary:core')
    coords=[]
    def flatten(value):
        if isinstance(value[0],(int,float)):coords.append(value)
        else:
            for part in value:flatten(part)
    flatten(boundary['geometry']['coordinates'])
    core_bounds=[min(p[0] for p in coords)-origin[0],min(p[1] for p in coords)-origin[1],max(p[0] for p in coords)-origin[0],max(p[1] for p in coords)-origin[1]]
    write(dest/'inspection.json',{'variant':mode,'crs':'EPSG:32749','origin_utm_m':origin,'edges':exportedges,'nodes':jns,'connections':emitted_connections,'qa':qa,'rail_overlay':rail_overlay,'crossing_overlay':crossing_overlay,'core_bounds':core_bounds,'policy':policy,'source_snapshot':'2026-10-31T04:34:22Z','attribution':'© OpenStreetMap contributors / ODbL 1.0'})
    return qa,exportedges,got

def routes(mode,edges,connections,home):
    dest=OUT/mode/'route-tests';dest.mkdir(exist_ok=True);lookup={e['id']:e for e in edges}
    main=[e for e in edges if e['road_function']=='main_arterial_road'];north=[e for e in main if e['shape'][-1][1]>e['shape'][0][1]];south=[e for e in main if e['shape'][-1][1]<e['shape'][0][1]]
    y=lambda e:sum(p[1] for p in e['shape'])/len(e['shape']);x=lambda e:sum(p[0] for p in e['shape'])/len(e['shape'])
    nbstart=min(north,key=y);nbend=max(north,key=y);sbstart=max(south,key=y);sbend=min(south,key=y)
    frontage=[e for e in edges if e['road_function']=='frontage_road'];frstart=max(frontage,key=y);frend=min(frontage,key=y)
    suk=[e for e in edges if e['name']=='Jalan Raya Sukodono'];sukin=[e for e in suk if e['shape'][-1][0]>e['shape'][0][0]];sukout=[e for e in suk if e['shape'][-1][0]<e['shape'][0][0]]
    ket=[e for e in edges if e['name']=='Jalan Raya Ketajen' and e['shape'][-1][0]>e['shape'][0][0]]
    # Target the actual eastern source way, never substitute a short pocket edge.
    keteast=[e for e in ket if e['source_way_id']==266287937]
    if not keteast:ketend=None
    else:ketend=max(keteast,key=x)
    definitions=[('northbound','Sidoarjo -> Surabaya',nbstart,nbend),('southbound','Surabaya -> Sidoarjo',sbstart,sbend),('feeder_to_main','Sukodono -> main north',min(sukin,key=x) if sukin else None,nbend),('main_to_feeder','main north -> Sukodono',sbstart,min(sukout,key=x) if sukout else None),('frontage_continuity','Frontage north -> south mapped extent',frstart,frend),('frontage_exit','Frontage -> Ketajen east access',frstart,ketend),('gedangan_junction','Main NB across Gedangan system',min(north,key=lambda e:abs(y(e)+150)),min(north,key=lambda e:abs(y(e)-100))),('station_junction','Ketajen across road/rail/frontage system',min(ket,key=x) if ket else None,ketend)]
    result=[];allowed={(a,b) for a,b,i,j in connections}
    for name,label,start,end in definitions:
        item={'test_id':name,'variant':mode,'direction_description':label,'starting_edge':start['id'] if start else None,'destination_edge':end['id'] if end else None,'validation_status':'STRICT_DIRECTION_WITH_PARAMETER_ASSUMPTIONS' if mode=='strict' else 'PROVISIONAL_ASSUMPTIONS','status':'NOT_FOUND','edges':[]}
        if not start or not end:
            item['reason']='Required endpoint is excluded by this variant direction/access policy';item['router_executed']=False
            fixture=ET.Element('routes');fixture.append(ET.Comment('Endpoint excluded by policy. No runnable trip or fabricated substitute.'));xml(dest/f'{name}.trips.xml',fixture);xml(dest/f'{name}.rou.xml',ET.Element('routes'));write(dest/f'{name}.router-log.json',{'executed':False,'reason':item['reason']})
            result.append(item);continue
        trips=ET.Element('routes');ET.SubElement(trips,'vType',id='topology_fixture',vClass='passenger');ET.SubElement(trips,'trip',id=name,type='topology_fixture',depart='0',**{'from':start['id'],'to':end['id']});xml(dest/f'{name}.trips.xml',trips)
        routefile=dest/f'{name}.rou.xml';p=run([home/'bin/duarouter.exe','-n',OUT/mode/'network.net.xml','-r',dest/f'{name}.trips.xml','-o',routefile,'--repair','false','--seed','42','--no-step-log','true'],dest/f'{name}.router-log.json');item['router_executed']=True;item['router_returncode']=p.returncode
        if p.returncode==0 and routefile.exists():
            route=ET.parse(routefile).getroot().find('.//vehicle/route')
            if route is not None:
                ids=route.get('edges').split();assert ids[0]==start['id'] and ids[-1]==end['id'];assert all((a,b) in allowed for a,b in zip(ids,ids[1:]));item.update(status='FOUND',edges=ids,reason='SUMO DUAROUTER route follows emitted whitelisted network connections',direction_statuses=sorted({lookup[e]['direction_source_status'] for e in ids}))
        if item['status']!='FOUND':item['reason']=p.stderr.strip() or 'Router did not emit a route; no synthetic route substituted'
        result.append(item)
    write(dest/'results.json',{'variant':mode,'fixture_only':True,'vehicles_simulated':False,'results':result})
    return result

def main():
    home=activate();policy=load(CONF/'policy.json');DOC.mkdir(exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    sources=['geodata/raw/gedangan-network.json','geodata/roads/all_roads.geojson','geodata/roads/main_arterial.geojson','geodata/roads/frontage.geojson','geodata/roads/feeders.geojson','geodata/junctions/road_junctions.geojson','geodata/railways/rail_tracks.geojson','geodata/railways/level_crossings.geojson','geodata/access_points/network_access.geojson','geodata/access_points/turn_restrictions.json','geodata/quality_assurance/components.json','frontend/public/geodata/m02/map-utm49s.json']
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}
    versions={}
    for exe in ['sumo','sumo-gui','netedit','netconvert','duarouter']:
        p=run([home/'bin'/f'{exe}.exe','--version'],DOC/f'{exe}-version.json');assert p.returncode==0 and '1.28.0' in p.stdout;versions[exe]=p.stdout.splitlines()[0]
    raw=load(ROOT/'geodata/raw/gedangan-network.json');nodes={e['id']:e for e in raw['elements'] if e['type']=='node'};features=load(ROOT/'geodata/roads/all_roads.geojson')['features'];relations=load(ROOT/'geodata/access_points/turn_restrictions.json')['relations'];fwd=Transformer.from_crs(4326,32749,always_xy=True);origin=list(fwd.transform(nodes[1359952188]['lon'],nodes[1359952188]['lat']));xy={nid:[x-origin[0],y-origin[1]] for nid,p in nodes.items() for x,y in [fwd.transform(p['lon'],p['lat'])]}
    special={n for r in relations for m in r['members'] if m['role']=='via' and m['type']=='node' for n in [m['ref']]};special|={nid for nid,n in nodes.items() if n.get('tags',{}).get('barrier') or n.get('tags',{}).get('railway')=='level_crossing' or n.get('tags',{}).get('highway')=='traffic_signals'}
    summaries={};route_results={}
    for mode in ['strict','provisional']:
        print('Building',mode,flush=True);edges,connections,blocked,decisions=construct(mode,features,nodes,xy,special,relations,policy)
        qa,exported,got=convert(mode,edges,connections,blocked,nodes,xy,origin,policy,home,relations);write(OUT/mode/'edge-decisions.json',{'variant':mode,'source_features':decisions});summaries[mode]=qa;route_results[mode]=routes(mode,exported,got,home)
        print(mode,qa['nodes'],'nodes',qa['edges'],'edges',qa['lanes'],'lanes',[(t['test_id'],t['status']) for t in route_results[mode]],flush=True)
    metadata={'milestone':3,'baseline_year':2026,'source_sha256':hashes,'sumo_versions':versions,'coordinate_origin_utm_m':origin,'policy':policy,'summaries':summaries,'no_traffic_demand':True,'field_verified':False,'rail_operations':False,'m02_sources_unchanged':hashes=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}}
    write(OUT/'network-metadata.json',metadata);write(DOC/'route-test-results.json',route_results)
    manifest={'metadata':'network-metadata.json','semantic_network_hashes':{v:summaries[v]['semantic_network_sha256'] for v in summaries},'source_sha256':hashes,'files':{str(p.relative_to(OUT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and p.name!='network-manifest.json'}};write(OUT/'network-manifest.json',manifest)
    web=ROOT/'frontend/public/network/m03';web.mkdir(parents=True,exist_ok=True)
    for mode in summaries:shutil.copy2(OUT/mode/'inspection.json',web/f'{mode}.json')
    write(web/'summary.json',{'summaries':summaries,'route_results':route_results,'source_snapshot':'2026-10-31T04:34:22Z','policy':policy})
    subprocess.run([sys.executable,str(CONF/'audit_network.py')],cwd=ROOT,check=True)

if __name__=='__main__':main()
