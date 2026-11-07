"""Derived audits of actual emitted SUMO lane connectivity and provenance."""
from collections import Counter,defaultdict
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'simulation/network/m03';DOC=ROOT/'documentation/m03'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,data):p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def partitions(ids,pairs,directed=False):
    graph={i:set() for i in ids};reverse={i:set() for i in ids}
    for a,b in pairs:graph[a].add(b);reverse[b].add(a)
    if not directed:
        for a,b in pairs:graph[b].add(a)
    seen=set();order=[]
    for root in sorted(ids):
        if root in seen:continue
        stack=[(root,False)]
        while stack:
            node,finished=stack.pop()
            if finished:order.append(node);continue
            if node in seen:continue
            seen.add(node);stack.append((node,True));stack.extend((n,False) for n in sorted(graph[node],reverse=True) if n not in seen)
    if not directed:
        # A second DFS on undirected graph returns weak components.
        reverse=graph
    seen=set();groups=[]
    for root in reversed(order):
        if root in seen:continue
        part=[];stack=[root];seen.add(root)
        while stack:
            node=stack.pop();part.append(node)
            for n in reverse[node]:
                if n not in seen:seen.add(n);stack.append(n)
        groups.append(sorted(part))
    return sorted(groups,key=lambda g:(-len(g),g[0]))

def main():
    report={}
    with (OUT/'source-to-edge.csv').open('w',newline='',encoding='utf-8-sig') as file:
        fields=['variant','edge_id','source_way_id','source_feature_id','from_node','to_node','lanes','speed_m_per_s','lane_width_m','direction_status','lanes_status','speed_status','width_status','capacity_status','component_id']
        writer=csv.DictWriter(file,fieldnames=fields);writer.writeheader()
        for mode in ['strict','provisional']:
            n=load(OUT/mode/'inspection.json');byid={e['id']:e for e in n['edges']};pairs={(c['from'],c['to']) for c in n['connections']};weak=partitions(set(byid),pairs);strong=partitions(set(byid),pairs,True);decisions=load(OUT/mode/'edge-decisions.json')['source_features'];provenance=load(OUT/mode/'connection-provenance.json')
            report[mode]={'network':n['qa'],'actual_edge_transition_graph':{'weak_component_count':len(weak),'weak_component_edge_sizes':[len(p) for p in weak],'strong_component_count':len(strong),'strong_component_edge_sizes':[len(p) for p in strong],'note':'Graph uses emitted lane-to-lane movements, unlike weak source-node geometry graph.'},'source_features':dict(Counter(d['action'] for d in decisions)),'exclusion_reasons':dict(Counter(reason for d in decisions if d['action']=='EXCLUDED' for reason in d['reasons'])),'parameter_status':{field:dict(Counter(e['parameter_status'][field] for e in n['edges'])) for field in ['direction','lanes','speed','lane_width','capacity']},'blocked_movement_reasons':dict(Counter(c['reason'] for c in provenance['blocked_movements'])),'restrictions_applied_or_quarantined':sorted({rid for c in provenance['blocked_movements'] for rid in c['restriction_relation_ids']}),'bridge_tagged_edges':sum(e['tags'].get('bridge')=='yes' for e in n['edges']),'tunnel_tagged_edges':sum(e['tags'].get('tunnel')=='yes' for e in n['edges']),'grade_separation_policy':'Existing OSM node identity only, no geometric crossing merge. Bridge/tunnel tags retained; no surveyed vertical geometry.'}
            write(OUT/mode/'edge-transition-components.json',{'weak_components':weak,'strong_components':strong})
            for e in n['edges']:
                writer.writerow({'variant':mode,'edge_id':e['id'],'source_way_id':e['source_way_id'],'source_feature_id':e['source_feature_id'],'from_node':e['from'],'to_node':e['to'],'lanes':e['lanes'],'speed_m_per_s':e['speed_m_per_s'],'lane_width_m':e['lane_width_m'],'direction_status':e['parameter_status']['direction'],'lanes_status':e['parameter_status']['lanes'],'speed_status':e['parameter_status']['speed'],'width_status':e['parameter_status']['lane_width'],'capacity_status':'MISSING','component_id':e['component_id']})
    write(DOC/'qa-report.json',report)
    lines=['# M03 Connectivity and QA Report','','This report separates weak node geometry connectivity from permitted edge transitions. Neither is field-validated traffic legality.','','| Variant | Nodes | Edges | Lanes | Weak node components | Weak transition components | Strong transition components |','|---|---:|---:|---:|---:|---:|---:|']
    for mode,r in report.items():
        q=r['network'];g=r['actual_edge_transition_graph'];lines.append(f'| {mode} | {q["nodes"]} | {q["edges"]} | {q["lanes"]} | {q["weak_components"]} | {g["weak_component_count"]} | {g["strong_component_count"]} |')
    lines+=['','## Unresolved findings','','Strict excludes unsupported directions/cross-way turns. Provisional admits direction assumptions only for a highway whitelist. No components are joined to reduce the count. Every resulting geometric component maps to one original M02 component; see each connectivity.json.','', 'NETCONVERT warnings remain in the complete initial/final log JSON: sharp radii/angles, intersecting lane turns in provisional initial construction, and missing incoming/outgoing lane connections. Generated junction curves and lane assignment are assumptions. No automatic geometry straightening, intersection merging or field repair is claimed.','']
    for mode,r in report.items():
        q=r['network'];lines += [f'### {mode}',f'- No incoming movement: {q["no_incoming_connection_edges"]} edges; no outgoing: {q["no_outgoing_connection_edges"]}. These include boundary terminals, barrier quarantines and deliberate withheld turns.',f'- Warning lines: initial {q["netconvert_initial_warning_lines"]}, final {q["netconvert_final_warning_lines"]}; repeated-message summaries mean this is not a count of unique physical defects.',f'- Automatically generated lane connections removed: {q["withheld_generated_lane_connections"]}; unapproved connections remaining: {q["unapproved_connections"]}.',f'- Source decisions: {r["source_features"]}.',f'- Source restriction IDs applied/quarantined: {r["restrictions_applied_or_quarantined"]}.','']
        for field,counts in r['parameter_status'].items():lines.append(f'- {field}: {counts}')
    lines+=['','## Restrictions and grade separation','','Via-node restrictions prohibit exact source from/to ways. Via-way and conditional restrictions are conservatively quarantined at the from-way entry into via-ways, possibly blocking otherwise permitted movements; no claim of exact dynamic restriction modelling. Explicit U-turns/reverse movements are globally withheld. Missing turn/access tags do not prove real-world legality.','', 'Access/private/no/destination/customer/permit-class restrictions are excluded for the passenger test harness; mapped barrier nodes block transitions conservatively. Actual dynamic crossing operations and signal timing are deferred.','', 'Bridge/tunnel flags and node IDs are retained; different OSM nodes are never joined for spatial proximity, including grade-separated crossings. OSM source topology itself still needs field review.','', 'Both directions of the main corridor were tested by DUAROUTER. Strict has deliberately failed branch/endpoint cases; provisional successes are assumptions, not a calibrated traffic model. See route-test-results.json for endpoints, exact edge sequence, router execution and failure reasons.']
    (DOC/'CONNECTIVITY_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (DOC/'QA_REPORT.md').write_text('# M03 QA\n\nSee CONNECTIVITY_REPORT.md and qa-report.json for the generated audit. Automated constraints are in tests/test_network_m03.py. Original source hashes, netconvert warnings and withheld turns are retained, not suppressed. No field verification or calibrated traffic validity is asserted.\n',encoding='utf-8')
    manifest=load(OUT/'network-manifest.json');manifest['files']={str(p.relative_to(OUT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and p.name!='network-manifest.json'};write(OUT/'network-manifest.json',manifest)
    print('QA generated:',[(mode,r['actual_edge_transition_graph']['weak_component_count']) for mode,r in report.items()])

if __name__=='__main__':main()
