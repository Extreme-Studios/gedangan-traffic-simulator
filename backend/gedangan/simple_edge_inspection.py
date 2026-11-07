"""Derived first FCD presence per road/vehicle; not a continuous detector count."""
import xml.etree.ElementTree as E
from collections import defaultdict
from .simple_common import *
def audit(r):
 folder=RUNS/r['run_id'];road={q['id']for q in load(folder/'vehicle-results.json')};seen=defaultdict(set);times=defaultdict(list)
 for _,n in E.iterparse(folder/'fcd.xml',events=('end',)):
  if n.tag!='timestep':continue
  t=float(n.get('time'))+.5
  for v in n.findall('vehicle'):
   if v.get('id')not in road:continue
   edge=v.get('lane').rsplit('_',1)[0];vid=v.get('id')
   if vid not in seen[edge]:seen[edge].add(vid);times[edge].append(t)
  n.clear()
 value={'run_id':r['run_id'],'definition':'Distinct road vehicles first observed on each edge in 0.5s FCD. Short-edge visits between samples may be absent; not a continuous detector count. Includes warmup; queue summaries exclude warmup.','first_observed_times_s':dict(times),'edge_diagnostics':load(folder/'edge-diagnostics.json')};save(DOC/'edge-inspection'/(r['run_id']+'.json'),value);print(r['run_id'],len(times),flush=True);return value
if __name__=='__main__':
 for p in sorted((DOC/'cases').glob('*.json')):audit(load(p))
 audit(load(DOC/'manual.json'))
