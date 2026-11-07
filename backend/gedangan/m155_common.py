"""M15.5 isolated reality-check work; all parent evidence stays immutable."""
from .m13_common import ROOT,load,sha,identity,now
from .m14_common import save
from pathlib import Path
import json
DOC=ROOT/'documentation/m155';DATA=ROOT/'staging/m155';RUNS=ROOT/'simulation/runs/m155';SCENARIOS=DATA/'scenarios';PARENT=ROOT/'simulation/network/m051/provisional/network.net.xml';NETWORK=ROOT/'simulation/network/m155/provisional/network.net.xml'
def protect():
 p=DOC/'preservation-before.json'
 if p.exists():return load(p)
 files={}
 for rel in ['backend/gedangan','frontend/src','frontend/dist-m14','frontend/dist-m15','simulation/network','simulation/runs/m14','simulation/runs/m15','documentation/m14','documentation/m15','geodata','configuration','data/historical/m13','data/official/m13_1','staging/m14','staging/m15/scenarios']:
  for q in (ROOT/rel).rglob('*'):
   if q.is_file()and'__pycache__'not in q.parts and not q.name.startswith('m155_')and q.suffix not in ['.pyc','.tmp']:files[q.relative_to(ROOT).as_posix()]=sha(q)
 for q in ROOT.glob('M*.md'):
  if not q.name.startswith('M15_5'):files[q.name]=sha(q)
 for rel in ['FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip','FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe']:
  q=ROOT/rel
  if q.exists():files[rel]=sha(q)
 save(p,{'created_utc':now(),'files':files,'scope':'M01–M15 existing source/evidence/networks plus M12 release; separate M15.5 namespaces'});return load(p)
def verify_protection():
 b=protect();changed=[p for p,h in b['files'].items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h];v={'checked':len(b['files']),'status':'PASS'if not changed else'FAIL','changed':changed};save(DOC/'preservation-after.json',v);return v
def freeze():
 protect();NETWORK.parent.mkdir(parents=True,exist_ok=True)
 if not NETWORK.exists():NETWORK.write_bytes(PARENT.read_bytes())
 assert sha(NETWORK)==sha(PARENT)
 save(DOC/'network-version.json',{'version':'m155-existing-provisional-1','parent':str(PARENT.relative_to(ROOT)),'parent_sha256':sha(PARENT),'network':str(NETWORK.relative_to(ROOT)),'network_sha256':sha(NETWORK),'change':'BYTE_IDENTICAL_FROZEN_COPY; no source-proven geometry edit','geospatial_acceptance':'PARTIAL','watermark':'PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED','new_roads':0,'new_connections':0})
