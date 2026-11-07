"""Independently reconcile persisted SUMO XML, permissions and playback outputs."""
import xml.etree.ElementTree as E,collections,gzip
from .m14_common import *
from .m14_network import catalog,route
from .m14_vehicles import registry

def audit(result):
 folder=RUNS/result['run_id'];d=load(folder/'demand.json');rows=load(folder/'vehicle-results.json');trips={q.get('id'):dict(q.attrib)for q in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo')};departed=sum(float(trips.get(q['id'],{}).get('depart','-1'))>=0 for q in rows);arrived=sum(float(trips.get(q['id'],{}).get('arrival','-1'))>=0 for q in rows);root=E.parse(NETWORK).getroot();connections={(c.get('from'),c.get('to'))for c in root.findall('connection')};via={c.get('via')for c in root.findall('connection')if c.get('tl')=='osm_859708050'and c.get('from','').startswith('m05_rail')};train_cross={};road_cross={c.get('via')for c in root.findall('connection')if c.get('tl')=='osm_859708050'and not c.get('from','').startswith('m05_rail')};train_times=collections.defaultdict(list);road_times=collections.defaultdict(list)
 for event,node in E.iterparse(folder/'fcd.xml',events=('end',)):
  if node.tag!='timestep':continue
  t=float(node.get('time'))
  for v in node.findall('vehicle'):
   if v.get('lane')in via:train_times[v.get('id')].append(t)
   if v.get('lane')in road_cross:road_times[v.get('id')].append(t)
  node.clear()
 for vid,times in train_times.items():train_cross[vid]={'first_sample_s':min(times),'last_sample_s':max(times)}
 idx=load(folder/'playback-index.json');frames=0;positions=0
 for chunk in idx['chunks']:
  with gzip.open(folder/chunk,'rt',encoding='utf-8')as f:data=json.load(f)
  frames+=len(data);positions+=sum(len(f['p'])for f in data)
 checks={'requested_exact':len(rows)==d['total']==result['requested'],'unique_ids':len({q['id']for q in rows})==len(rows),'routed_exact':sum(bool(q['edges'])for q in rows)==result['routed'],'departure_tripinfo_parity':departed==result['departed'],'arrival_tripinfo_parity':arrived==result['arrived'],'explicit_connections':all((a,b)in connections for q in rows for a,b in zip(q['edges'],q['edges'][1:])),'network_unchanged':sha(NETWORK)==result['network_sha256'],'no_flyover_routes':not any(e.startswith('recovery_fo_')for q in rows for e in q['edges']),'no_permission_collision_teleport_events':not(result['illegal_permissions']or result['collisions']or result['teleports']),'frames_conserved':frames==result['playback_frames'],'all_output_hashes_match':all(sha(folder/name)==h for name,h in load(folder/'output-manifest.json').items())}
 return {'run_id':result['run_id'],'checks':checks,'status':'PASS'if all(checks.values())else'FAIL','playback_frames':frames,'playback_positions':positions,'train_crossing_samples':train_cross,'road_vehicles_sampled_in_crossing':len(road_times),'failed_reasons':dict(collections.Counter(q.get('reason')for q in rows if not q['edges']))}

def main():
 rs=load(DOC/'sumo-benchmarks.json')+[load(DOC/'class-validation.json')]+list(load(DOC/'rail-sensitivity.json').values())+list(load(DOC/'signal-sensitivity.json').values());save(DOC/'xml-independent-audit.json',[audit(r)for r in rs]);save(DOC/'route-compatibility.json',[{'class':v['id'],'approach':a['id'],'turn':turn,**route(v['id'],a['id'],turn)}for v in registry()for a in catalog()['approaches']for turn in a['movements']]);save(DOC/'network-catalog.json',catalog());save(DOC/'vehicle-registry.json',registry());print(verify_protection(),flush=True)
if __name__=='__main__':main()
