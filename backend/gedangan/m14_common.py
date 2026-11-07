"""M14 additive staging; no historical database writes or existing network mutations."""
from .m13_common import ROOT,load,sha,identity,now
from pathlib import Path
from datetime import datetime,timedelta
import json,os
DOC=ROOT/'documentation/m14';DATA=ROOT/'staging/m14';RUNS=ROOT/'simulation/runs/m14';NETWORK=ROOT/'simulation/network/m051/provisional/network.net.xml';SCENARIOS=DATA/'scenarios'
def save(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8');os.replace(tmp,path)
def protect():
 p=DOC/'preservation-before.json'
 if p.exists():return load(p)
 files={}
 for rel in ['data/historical/m13/historical.sqlite','data/official/m13_1/historical_v2.sqlite','configuration/demand-m04/vehicle-registry.json','simulation/network/m051/provisional/network.net.xml','M13_HISTORICAL_COVERAGE.json','FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip']:
  q=ROOT/rel
  if q.exists():files[rel]=sha(q)
 for q in ROOT.glob('M13*.md'):files[q.relative_to(ROOT).as_posix()]=sha(q)
 value={'created_utc':now(),'files':files,'rule':'M14 writes only new source/staging/run/report namespaces; M12 and historical evidence untouched'};save(p,value);return value
def verify_protection():
 before=protect();changes=[r for r,h in before['files'].items()if not(ROOT/r).exists()or sha(ROOT/r)!=h];value={'status':'PASS'if not changes else'FAIL','changed':changes,'checked':len(before['files'])};save(DOC/'preservation-after.json',value);return value
