"""Independent XML/FCD/playback accounting and permissions verification."""
import xml.etree.ElementTree as E,gzip,math
from collections import Counter
from .m156_common import *
from .m14_vehicles import registry
def audit(result):
 from .recovery_routing import context
 folder=RUNS/result['run_id'];ledger=load(folder/'vehicle-results.json');trips={e.get('id'):e.attrib for e in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo')};net,*_=context(str(NETWORK.resolve()),sha(NETWORK));lanes={l.getID():l for e in net.getEdges(withInternal=True)for l in e.getLanes()};types={v['id']:v for v in registry()};ids={q['id']:q for q in ledger};idx=load(folder/'playback-index.json');connections={(c.get('from'),c.get('to'))for c in E.parse(NETWORK).getroot().findall('connection')};departed=sum(float(trips.get(q['id'],{}).get('depart',-1))>=0 for q in ledger);arrived=sum(float(trips.get(q['id'],{}).get('arrival',-1))>=0 for q in ledger);illegal=[];fcd_count=0;sample_ref={};chunks=idx['chunks']
 # FCD uses interval start, TraCI/playback uses post-step end. Check every300th frame.
 for _,n in E.iterparse(folder/'fcd.xml',events=('end',)):
  if n.tag!='timestep':continue
  t=round(float(n.get('time'))+.5,3);fcd_count+=1
  for v in n.findall('vehicle'):
   vid=v.get('id')
   if vid in ids and not lanes[v.get('lane')].allows(types[ids[vid]['vehicle_type_id']]['sumo_vclass']):illegal.append({'time':t,'vehicle':vid,'lane':v.get('lane')})
  if fcd_count%300==1:sample_ref[t]={v.get('id'):(float(v.get('x')),float(v.get('y')))for v in n.findall('vehicle')}
  n.clear()
 frames=positions=matches=0;maxerror=0
 for name in chunks:
  with gzip.open(folder/name,'rt',encoding='utf-8')as f:data=json.load(f)
  for frame in data:
   frames+=1;positions+=len(frame['p'])
   if frame['t']not in sample_ref:continue
   ref=sample_ref[frame['t']]
   for p in frame['p']:
    vid=idx['vehicles'][p[0]]['id']
    if vid in ref:matches+=1;maxerror=max(maxerror,math.hypot(p[1]-ref[vid][0],p[2]-ref[vid][1]))
 checks={'input_total_exact':len(ledger)==result['requested'],'ids_unique':len(ids)==len(ledger),'xml_departed_equal':departed==result['departed'],'xml_arrived_equal':arrived==result['arrived'],'requested_balance':result['requested']==result['routed']+result['failed_routes'],'routed_balance':result['routed']==result['departed']+result['not_departed'],'departed_balance':result['departed']==result['arrived']+result['active'],'explicit_connections':all((a,b)in connections for q in ledger for a,b in zip(q['edges'],q['edges'][1:])),'all_fcd_lane_permissions':not illegal,'playback_clock_and_xy':matches>0 and maxerror<=.02,'frames_equal_fcd':frames==fcd_count==result['playback_frames'],'output_hashes':all(sha(folder/n)==h for n,h in load(folder/'output-manifest.json').items()),'network_unchanged':sha(NETWORK)==result['network_sha256'],'no_unexplained_teleport_collision':not(result['teleports']or result['collisions'])}
 value={'run_id':result['run_id'],'status':'PASS'if all(checks.values())else'FAIL','checks':checks,'fcd_playback_clock_offset_s':.5,'matched_positions':matches,'maximum_xy_error_m':maxerror,'frames':frames,'positions':positions,'illegal':illegal,'failed_reasons':dict(Counter(q.get('reason')for q in ledger if not q['edges']))};save(DOC/'xml-audits'/(result['run_id']+'.json'),value);return value
def main():
 results=[load(p)for p in sorted((DOC/'cases').glob('*.json'))]+[load(DOC/'manual.json')];out=[]
 for r in results:out.append(audit(r));print(out[-1]['run_id'],out[-1]['status'],flush=True)
 save(DOC/'xml-audit-summary.json',out)
if __name__=='__main__':main()
