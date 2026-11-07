"""M15 isolated staging; parent milestones are immutable."""
from .m13_common import ROOT,load,sha,identity,now
from .m14_common import save
from pathlib import Path
import json
DOC=ROOT/'documentation/m15';DATA=ROOT/'staging/m15';RUNS=ROOT/'simulation/runs/m15';SCENARIOS=DATA/'scenarios';NETWORK=ROOT/'simulation/network/m051/provisional/network.net.xml'
def protect():
 p=DOC/'preservation-before.json'
 if p.exists():return load(p)
 files={}
 roots=['backend/gedangan','frontend/src','frontend/dist-m14','simulation/network','simulation/runs/m14','documentation/m14','geodata','configuration','data/historical/m13','data/official/m13_1','staging/m14']
 for rel in roots:
  for q in (ROOT/rel).rglob('*'):
   if q.is_file()and'__pycache__'not in q.parts and not q.name.startswith('m15_')and q.suffix not in ['.pyc','.tmp','.log-wal','.log-shm']:files[q.relative_to(ROOT).as_posix()]=sha(q)
 for q in ROOT.glob('M*.md'):
  if not q.name.startswith('M15'):files[q.name]=sha(q)
 for rel in ['FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip','FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe']:
  q=ROOT/rel
  if q.exists():files[rel]=sha(q)
 value={'created_utc':now(),'files':files,'note':'Read-only source/data/network plus all existing M14 outputs. M15 uses separate source/staging/run/report namespaces.'};save(p,value);return value
def verify_protection():
 b=protect();changed=[p for p,h in b['files'].items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h];v={'checked':len(b['files']),'status':'PASS'if not changed else'FAIL','changed':changed};save(DOC/'preservation-after.json',v);return v
