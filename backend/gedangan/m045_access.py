"""Permission-only derived network and multiclass recorded simulation.

M03/M04 code and outputs are immutable. The M04 module is loaded as a private
adapter instance to reuse registry, OD, routing checks and lifecycle extraction.
No vClass ignoring, TraCI overrides, geometry edits or new movements.
"""
from collections import Counter,defaultdict
import copy
import importlib.util
import json
import math
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
CONF=ROOT/'configuration/access-m045';DOC=ROOT/'documentation/m045'
NET=ROOT/'simulation/network/m045';DEMAND=ROOT/'simulation/demand/m045';RUNS=ROOT/'simulation/runs/m045'
BASE=ROOT/'simulation/network/m03'
spec=importlib.util.spec_from_file_location('m045_private_m04_adapter',ROOT/'backend/gedangan/m04_demand.py');adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
load=adapter.load;save=adapter.save;sha=adapter.sha;xml=adapter.xml;execute=adapter.execute
adapter.M03=NET;adapter.DEMAND=DEMAND;adapter.RUNS=RUNS;adapter.DOC=DOC

def baseline_check():
    bad=[p for p,h in load(DOC/'previous-milestones-sha256.json').items() if sha(ROOT/p)!=h]
    if bad:raise RuntimeError('Immutable baseline drift: '+str(bad))

def class_access(edge,cls,variant,policy):
    tags=edge['tags'];direction='forward' if edge['sign']==1 else 'backward';chain=policy['access_hierarchy'][cls]
    relevant=[k for k in tags if any(k==base+':conditional' or k.startswith(base+':conditional:') or k==base+':'+direction+':conditional' or k==base+':lanes' or k==base+':lanes:'+direction for base in chain)]
    result={'allowed':False,'status':'MISSING','basis':'No positive source access or applicable classification rule','provenance_id':'M045-ACCESS-01','source_way_id':edge['source_way_id'],'source_tags':{k:v for k,v in tags.items() if any(k==base or k.startswith(base+':') for base in chain)},'field_legal_verified':False}
    if relevant:return {**result,'status':'INFERRED','basis':'Conservative quarantine of conditional/lane-specific access: '+','.join(relevant)}
    selected=None
    for base in chain:
        for key in [base,base+':'+direction]:
            if key in tags:selected=(key,tags[key].strip().lower())
    if selected:
        key,value=selected
        return {**result,'allowed':value in policy['positive_values'],'status':'VERIFIED' if value in policy['positive_values']+policy['denied_or_purpose_limited_values'] else 'MISSING','basis':f'Explicit OSM hierarchy {key}={value}; source verification only'}
    if tags.get('toll')=='yes' and cls=='motorcycle':return {**result,'basis':'Motorcycle toll-road legal access missing; no general highway inference applied'}
    rule=policy['role_rules'].get(edge['road_function'])
    if not rule:return result
    if cls in rule['inferred'] and tags.get('highway') in policy['public_road_highways']:return {**result,'allowed':True,'status':'INFERRED','basis':rule['reason']}
    if variant=='provisional' and cls in rule['provisional_assumption']:return {**result,'allowed':True,'status':'ASSUMPTION','basis':rule['reason']}
    return {**result,'basis':rule['reason']+' Class not admitted in this variant without explicit evidence.'}

def movement_denied(a,b,cls,relations):
    reasons=[];aliases={'motorcycle':['motorcycle'],'passenger':['motorcar'],'delivery':['goods'],'bus':['psv','bus'],'truck':['goods','hgv'],'trailer':['goods','hgv','hgv:articulated']}[cls]
    for rel in relations:
        members=rel.get('members',[]);tags=rel.get('tags',{});fr={m['ref'] for m in members if m['role']=='from' and m['type']=='way'};to={m['ref'] for m in members if m['role']=='to' and m['type']=='way'};via={m['ref'] for m in members if m['role']=='via' and m['type']=='way'};vn={m['ref'] for m in members if m['role']=='via' and m['type']=='node'}
        if a['source_way_id'] not in fr:continue
        node=int(a['to'][4:]);terms=[(key,value) for key,value in tags.items() if key=='restriction' or key=='restriction:conditional' or any(key=='restriction:'+al or key=='restriction:'+al+':conditional' for al in aliases)]
        for key,value in terms:
            # Do not restore generic movements previously withheld for exceptions in M03.
            kind=value.split('@')[0].strip();blocked=(b['source_way_id'] in via) or (node in vn and ((kind.startswith('no_') and b['source_way_id'] in to) or (kind.startswith('only_') and b['source_way_id'] not in to)))
            if blocked:reasons.append({'relation_id':rel['id'],'key':key,'value':value,'basis':'Source restriction; via-way/conditional conservatively quarantined, no dynamic legal model'})
    return reasons

def external_connections(root):return {(c.get('from'),c.get('to'),c.get('fromLane'),c.get('toLane')):c for c in root.findall('connection') if not c.get('from','').startswith(':')}

def geometry_signature(root):
    return {'location':root.find('location').attrib,'edges':{e.get('id'):{'from':e.get('from'),'to':e.get('to'),'lanes':[{k:l.get(k) for k in ['id','index','speed','length','width','shape']} for l in e.findall('lane')]} for e in root.findall('edge')},'junctions':{j.get('id'):{k:j.get(k) for k in ['x','y','shape','type']} for j in root.findall('junction')}}

def build_network(mode,home,policy,relations):
    folder=NET/mode;folder.mkdir(parents=True,exist_ok=True);base=ET.parse(BASE/mode/'network.net.xml').getroot();original=load(BASE/mode/'inspection.json');edges={e['id']:e for e in original['edges']};decisions={eid:{cls:class_access(e,cls,mode,policy) for cls in policy['classes']} for eid,e in edges.items()}
    ep=ET.Element('edges')
    for eid,e in edges.items():
        allowed=[cls for cls,r in decisions[eid].items() if r['allowed']];attrs={'id':eid,'allow':' '.join(allowed)} if allowed else {'id':eid,'disallow':'all'}
        elem=ET.SubElement(ep,'edge',**attrs)
        for lane in range(e['lanes']):ET.SubElement(elem,'lane',index=str(lane),**({'allow':' '.join(allowed)} if allowed else {'disallow':'all'}))
    xml(folder/'permissions.edg.xml',ep)
    cp=ET.Element('connections');movement=[]
    for key,c in external_connections(base).items():
        a,b,fl,tl=key;common=[];blocked={}
        for cls in policy['classes']:
            reasons=movement_denied(edges[a],edges[b],cls,relations)
            if decisions[a][cls]['allowed'] and decisions[b][cls]['allowed'] and not reasons:common.append(cls)
            if reasons:blocked[cls]=reasons
        ET.SubElement(cp,'connection',**{'from':a,'to':b,'fromLane':fl,'toLane':tl},**({'allow':' '.join(common)} if common else {'disallow':'all'}))
        movement.append({'from':a,'to':b,'fromLane':int(fl),'toLane':int(tl),'allow':common,'blocked_source_restrictions':blocked,'basis':'Intersection of edge permissions; source turn restrictions may further narrow. No new movement.'})
    xml(folder/'permissions.con.xml',cp)
    cfg=ET.Element('configuration');inp=ET.SubElement(cfg,'input')
    for k,v in [('sumo-net-file',BASE/mode/'network.net.xml'),('edge-files',folder/'permissions.edg.xml'),('connection-files',folder/'permissions.con.xml')]:ET.SubElement(inp,k,value=str(v))
    out=ET.SubElement(cfg,'output');ET.SubElement(out,'output-file',value=str(folder/'network.net.xml'));processing=ET.SubElement(cfg,'processing')
    for k,v in [('offset.disable-normalization','true'),('no-turnarounds','true'),('geometry.remove','false'),('junctions.join','false')]:ET.SubElement(processing,k,value=v)
    xml(folder/'build.netccfg',cfg);log=execute([home/'bin/netconvert.exe','-c',folder/'build.netccfg'],folder/'netconvert-log.json');assert log['returncode']==0,log['stderr']
    final=ET.parse(folder/'network.net.xml').getroot();assert not(set(external_connections(final))-set(external_connections(base))),'New connection generated'
    sig0=geometry_signature(base);sig1=geometry_signature(final)
    drift=[k for k in sig0 if sig0[k]!=sig1[k]]
    save(folder/'geometry-audit.json',{'baseline_sha256':sha(BASE/mode/'network.net.xml'),'corrected_sha256':sha(folder/'network.net.xml'),'geometry_sections_changed':drift,'original_connection_count':len(external_connections(base)),'corrected_connection_count':len(external_connections(final)),'new_connections':0})
    if drift:raise RuntimeError('Permission rebuild changed geometry: '+str(drift)+'; refuse silently altered network')
    import sumolib
    net=sumolib.net.readNet(str(folder/'network.net.xml'),withInternal=True);conn_lookup={tuple(str(c[k]) for k in ['from','to','fromLane','toLane']):c for c in movement};lanes={l.get('id'):l for e in final.findall('edge') for l in e.findall('lane')};internal_expect=defaultdict(set)
    for key,c in external_connections(final).items():
        allowed=conn_lookup[key]['allow']
        actual_connection=set(c.get('allow','').split()) if c.get('allow') is not None else set(policy['classes'])-set(c.get('disallow','').split())
        if c.get('disallow')=='all':actual_connection=set()
        assert actual_connection & set(policy['classes'])==set(allowed),(key,actual_connection,allowed)
        for cls in policy['classes']:
            assert net.getEdge(key[0]).getLane(int(key[2])).allows(cls)==decisions[key[0]][cls]['allowed']
            via=c.get('via')
            if via:internal_expect[via].update(allowed)
    internal_mismatch=[]
    for lid,expected in internal_expect.items():
        actual={cls for cls in policy['classes'] if net.getLane(lid).allows(cls)}
        if actual!=expected:internal_mismatch.append({'lane':lid,'expected':sorted(expected),'actual':sorted(actual)})
    assert not internal_mismatch,internal_mismatch[:3]
    for e in original['edges']:
        e['access_policy']=decisions[e['id']];e['allowed_vclasses']=[cls for cls in policy['classes'] if decisions[e['id']][cls]['allowed']]
        for lane in e['sumo_lanes']:lane['allowed_vclasses']=e['allowed_vclasses']
    for c in original['connections']:
        key=tuple(str(c[k]) for k in ['from','to','fromLane','toLane']);c['allowed_vclasses']=conn_lookup[key]['allow']
    original.update(network_family='M04.5_CORRECTED',baseline_network_sha256=sha(BASE/mode/'network.net.xml'),corrected_network_sha256=sha(folder/'network.net.xml'),access_policy_version=policy['version'])
    save(folder/'inspection.json',original);save(folder/'access-decisions.json',{'variant':mode,'source':'M03 OSM tags; no verified road-authority document available','edges':decisions,'movements':movement});save(folder/'permission-audit.json',{'internal_lane_mismatches':internal_mismatch,'internal_lanes_audited':len(internal_expect),'external_lane_permissions_consistent':True,'decision_counts':{cls:dict(Counter(r[cls]['status']+('_ALLOW' if r[cls]['allowed'] else '_DENY') for r in decisions.values())) for cls in policy['classes']}})
    shutil.copy2(BASE/mode/'rail-reference.add.xml',folder/'rail-reference.add.xml')
    return original

# Preserve original M04 validation functions before installing private adapter hooks.
original_precheck=adapter.precheck
source_shapes={}
def install_screens():
    global source_shapes
    source_shapes={mode:{e['id']:e['shape'] for e in load(BASE/mode/'source-to-edge.json')['edges']} for mode in ['strict','provisional']}
    # Isolated hooks leave the original M04 module and outputs unchanged.
    adapter.precheck=lambda q,v,es,net: type_screen_impl(q,v,es,net)
    adapter.validate_route=lambda ids,q,v,es,net,cs:route_screen_impl(ids,q,v,es,net,cs)

def type_screen_impl(q,v,es,net):
    reason=original_precheck(q,v,es,net)
    if reason:return reason
    for eid in [q['origin_edge'],q['destination_edge']]:
        tags=es[eid]['tags']
        if any(k.startswith(base+':') for k in tags for base in ['maxwidth','maxlength','maxheight','maxweight','maxaxleload','maxweightrating']):return 'CONDITIONAL_OR_SPECIAL_CLEARANCE_UNRESOLVED'
        for key,param in [('maxwidth','width'),('maxlength','length'),('maxheight','height')]:
            if key in tags:
                try:limit=float(tags[key].replace(' m',''))
                except ValueError:return 'UNPARSED_GEOMETRY_RESTRICTION: '+key
                if v['parameters'][param]>limit:return 'EXPLICIT_DIMENSION_LIMIT: '+key
        if any(k in tags for k in ['maxweight','maxaxleload','maxweightrating']):return 'LOAD_CLEARANCE_MISSING'
    return None

def route_screen_impl(ids,q,v,es,net,cs):
    if not ids or ids[0]!=q['origin_edge'] or ids[-1]!=q['destination_edge']:return 'ROUTER_ENDPOINT_MISMATCH'
    for eid in ids:
        reason=type_screen_impl({**q,'origin_edge':eid,'destination_edge':eid},v,es,net)
        if reason:return reason
        if not es[eid]['access_policy'][v['sumo_vclass']]['allowed']:return 'SOURCE_CLASS_ACCESS_POLICY_DENIED'
    for a,b in zip(ids,ids[1:]):
        if not any(c['from']==a and c['to']==b and v['sumo_vclass'] in c['allowed_vclasses'] and net.getEdge(a).getLane(c['fromLane']).allows(v['sumo_vclass']) and net.getEdge(b).getLane(c['toLane']).allows(v['sumo_vclass']) for c in cs):return 'LANE_CONNECTION_CLASS_PERMISSION_DENIED'
    if v['id']=='trailer':
        if q['network_variant']!='provisional':return 'TRAILER_TRIAL_PROVISIONAL_ONLY'
        for a,b in zip(ids,ids[1:]):
            def vector(e,last):
                pts=source_shapes[q['network_variant']][e];pairs=list(zip(pts,pts[1:]));pairs=reversed(pairs) if last else pairs
                return next((y[0]-x[0],y[1]-x[1]) for x,y in pairs if math.dist(x,y)>1e-6)
            u=vector(a,True);w=vector(b,False);angle=math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(u,w))/(math.hypot(*u)*math.hypot(*w))))))
            if angle>25:return 'TRAILER_CONNECTOR_DEFLECTION_SCREEN_FAILED'
    return None

def simulate(mode,profile,rows,folder,home,config):
    rid=f'm045-{mode}-{profile}-seed{config["seed"]}';out=RUNS/rid;out.mkdir(parents=True,exist_ok=True)
    c=ET.Element('configuration');inp=ET.SubElement(c,'input');ET.SubElement(inp,'net-file',value=str(NET/mode/'network.net.xml'));ET.SubElement(inp,'route-files',value=str(folder/'vehicle-types.rou.xml')+','+str(folder/'accepted.rou.xml'))
    t=ET.SubElement(c,'time')
    for k,v in [('begin',0),('end',2100),('step-length',1)]:ET.SubElement(t,k,value=str(v))
    r=ET.SubElement(c,'random_number');ET.SubElement(r,'seed',value=str(config['seed']));proc=ET.SubElement(c,'processing');ET.SubElement(proc,'time-to-teleport',value='300')
    o=ET.SubElement(c,'output')
    for k,v in [('tripinfo-output',out/'tripinfo.xml'),('tripinfo-output.write-unfinished','true'),('tripinfo-output.write-undeparted','true'),('fcd-output',out/'fcd.xml'),('device.fcd.period','1'),('fcd-output.attributes','id,x,y,speed,lane,pos,type'),('summary-output',out/'summary.xml'),('statistic-output',out/'statistics.xml')]:ET.SubElement(o,k,value=str(v))
    report=ET.SubElement(c,'report');ET.SubElement(report,'no-step-log',value='true');xml(out/'run.sumocfg',c)
    log=execute([home/'bin/sumo.exe','-c',out/'run.sumocfg','--xml-validation','always'],out/'simulation-log.json');assert log['returncode']==0,log['stderr']
    metrics=adapter.analyze_run(out,rows,config,log,sha(NET/mode/'network.net.xml'),rid);metrics.update(network_variant=mode,profile=profile,network_family='M04.5_CORRECTED',trajectory_period_seconds=1,vehicle_registry_sha256=sha(ROOT/'configuration/demand-m04/vehicle-registry.json'),od_matrix_sha256=sha(ROOT/'simulation/demand/m04/od-matrix.fixture.json'))
    save(out/'metrics.json',metrics)
    # Correct the inherited exporter description: actual M04.5 samples are every second.
    tr=load(out/'trajectory.json');tr['source']='Actual SUMO FCD, sampled every 1 second; no interpolation';save(out/'trajectory.json',tr)
    states=load(out/'vehicle-states.json')['states'];perclass={v['id']:{'requested':sum(q['vehicle_type_id']==v['id'] for q in rows),'routable':sum(q['vehicle_type_id']==v['id'] and q['route_status']=='ROUTABLE' for q in rows),'loaded':sum(s['vehicle_type_id']==v['id'] and s['tripinfo'] is not None for s in states),'departed':sum(s['vehicle_type_id']==v['id'] and s['actual_depart_seconds'] is not None for s in states),'moved':sum(s['vehicle_type_id']==v['id'] and s['moved_in_recorded_fcd'] for s in states),'arrived':sum(s['vehicle_type_id']==v['id'] and s['status']=='ARRIVED' for s in states)} for v in adapter.registry()};save(out/'class-lifecycle.json',perclass)
    return metrics

def main():
    baseline_check();home=adapter.activate();policy=load(CONF/'policy.json')
    raw=load(ROOT/'geodata/raw/gedangan-network.json');relations=[r for r in raw['elements'] if r['type']=='relation' and (r.get('tags',{}).get('type')=='restriction' or any(k.startswith('restriction') for k in r.get('tags',{})))]
    for exe in ['sumo','netconvert','duarouter']:
        result=execute([home/'bin'/f'{exe}.exe','--version'],DOC/f'{exe}-version.json');assert result['returncode']==0 and '1.28.0' in result['stdout']
    for mode in ['strict','provisional']:build_network(mode,home,policy,relations);print('Built permission-only corrected',mode,flush=True)
    install_screens();matrix=load(ROOT/'simulation/demand/m04/od-matrix.fixture.json');config=load(ROOT/'configuration/demand-m04/demand-config.json');adapter.validate_inputs(adapter.registry(),config);results={};runs=[]
    for mode in ['strict','provisional']:
        requests=[{'id':f'm045_compat_{mode}_{m["id"]}_{v["id"]}','vehicle_type_id':v['id'],'od_id':m['id'],'origin_zone':m['origin_zone'],'destination_zone':m['destination_zone'],**m['endpoints'][mode],'depart_seconds':i*3,'network_variant':mode,'category':'SYNTHETIC_TEST','provenance_id':'S-DEMAND-01'} for i,(m,v) in enumerate((m,v) for m in matrix['movements'] for v in adapter.registry())]
        folder=DEMAND/'compatibility'/mode;rows=adapter.route_batch(folder,mode,requests,home);decorate_rows(mode,folder,rows);results[mode]=rows;runs.append(simulate(mode,'smoke',rows,folder,home,config));print(mode,'coverage',runs[-1]['routable_trips'],'routable',runs[-1]['arrived_vehicles'],'arrived',flush=True)
    for profile in ['low','medium','stress']:
        for mode in ['strict','provisional']:
            qs=adapter.generate(mode,profile,config,matrix)
            for q in qs:q['id']=q['id'].replace('m04_','m045_',1)
            folder=DEMAND/mode/profile;rows=adapter.route_batch(folder,mode,qs,home);decorate_rows(mode,folder,rows);runs.append(simulate(mode,profile,rows,folder,home,config));print(mode,profile,runs[-1]['requested_trips'],runs[-1]['routable_trips'],runs[-1]['arrived_vehicles'],'teleports',runs[-1]['teleported_vehicles'],flush=True)
    save(DOC/'compatibility-results.json',results);save(DOC/'run-summary.json',runs);baseline_check();publish(policy,results,runs);manifests()

def decorate_rows(mode,folder,rows):
    edges=adapter.edge_index(mode);vs={v['id']:v for v in adapter.registry()}
    for r in rows:
        r['reason']=r['reason'].replace('M03_LANE_PERMISSION_DENIED','M045_LANE_PERMISSION_DENIED')
        r['network_family']='M04.5_CORRECTED';r['access_provenance_id']='M045-ACCESS-01';r['access_statuses']=sorted({edges[e]['access_policy'][vs[r['vehicle_type_id']]['sumo_vclass']]['status'] for e in r['edges']});r['validation_status']='M045_PROVISIONAL_ACCESS_AND_DIRECTION_ASSUMPTIONS' if mode=='provisional' else 'M045_SOURCE_INFERRED_ACCESS_WITH_UNCALIBRATED_PARAMETERS'
    report=load(folder/'route-validation.json');report['results']=rows;save(folder/'route-validation.json',report);save(folder/'failed-trips.json',{'category':'SIMULATED_RESULT','failures':[r for r in rows if r['route_status']!='ROUTABLE']})

def publish(policy,compat,runs):
    web=ROOT/'frontend/public/access/m045';web.mkdir(parents=True,exist_ok=True)
    for mode in ['strict','provisional']:shutil.copy2(NET/mode/'inspection.json',web/f'{mode}.network.json')
    for run in runs:
        rid=run['run_id'];shutil.copy2(RUNS/rid/'trajectory.json',web/f'{rid}.trajectory.json');source=DEMAND/'compatibility'/run['network_variant'] if run['profile']=='smoke' else DEMAND/run['network_variant']/run['profile'];shutil.copy2(source/'route-validation.json',web/f'{rid}.routes.json');shutil.copy2(RUNS/rid/'class-lifecycle.json',web/f'{rid}.classes.json')
    originals=load(ROOT/'documentation/m04/run-summary.json')
    for run in originals:
        states=load(ROOT/'simulation/runs/m04'/run['run_id']/'vehicle-states.json')['states'];life={v['id']:{'requested':sum(s['vehicle_type_id']==v['id'] for s in states),'routable':sum(s['vehicle_type_id']==v['id'] and s['status']!='NOT_ROUTABLE' for s in states),'loaded':sum(s['vehicle_type_id']==v['id'] and s['tripinfo'] is not None for s in states),'departed':sum(s['vehicle_type_id']==v['id'] and s['actual_depart_seconds'] is not None for s in states),'moved':sum(s['vehicle_type_id']==v['id'] and s['moved_in_recorded_fcd'] for s in states),'arrived':sum(s['vehicle_type_id']==v['id'] and s['status']=='ARRIVED' for s in states)} for v in adapter.registry()};save(web/f'{run["run_id"]}.classes.json',life)
    save(web/'summary.json',{'label':adapter.LABEL,'sumo_version':'1.28.0','policy':policy,'runs':runs,'original_runs':originals,'registry':adapter.registry(),'zones':load(ROOT/'simulation/demand/m04/od-zones.json')['zones'],'matrix':load(ROOT/'simulation/demand/m04/od-matrix.fixture.json'),'compatibility':compat,'field_calibrated':False,'m05_started':False})

def manifests():
    inputpaths=[CONF/'policy.json',ROOT/'configuration/demand-m04/vehicle-registry.json',ROOT/'configuration/demand-m04/demand-config.json',ROOT/'simulation/demand/m04/od-matrix.fixture.json',ROOT/'geodata/raw/gedangan-network.json',Path(__file__),ROOT/'backend/gedangan/m04_demand.py']
    inputpaths += [BASE/mode/name for mode in ['strict','provisional'] for name in ['network.net.xml','inspection.json','source-to-edge.json']]
    inputpaths += [ROOT/'simulation/demand/m04/od-zones.json']
    sources={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in inputpaths}
    for mode in ['strict','provisional']:
        folder=NET/mode;save(folder/'manifest.json',{'variant':mode,'family':'M04.5_CORRECTED','baseline_sha256':sha(BASE/mode/'network.net.xml'),'input_sha256':sources,'files':{p.name:sha(p) for p in folder.iterdir() if p.is_file() and p.name!='manifest.json'}})
    for run in load(DOC/'run-summary.json'):
        folder=RUNS/run['run_id'];save(folder/'manifest.json',{'run_id':run['run_id'],'network_sha256':run['network_sha256'],'seed':run['seed'],'sumo_version':'1.28.0','simulation_period_seconds':[0,2100],'validation_status':'SYNTHETIC_NOT_CALIBRATED','input_sha256':sources,'files':{p.name:sha(p) for p in folder.iterdir() if p.is_file() and p.name!='manifest.json'}})
        batch=DEMAND/'compatibility'/run['network_variant'] if run['profile']=='smoke' else DEMAND/run['network_variant']/run['profile']
        save(batch/'manifest.json',{'run_id':run['run_id'],'network_sha256':run['network_sha256'],'seed':run['seed'],'sumo_version':'1.28.0','input_sha256':sources,'files':{p.name:sha(p) for p in batch.iterdir() if p.is_file() and p.name!='manifest.json'}})

if __name__=='__main__':main()
