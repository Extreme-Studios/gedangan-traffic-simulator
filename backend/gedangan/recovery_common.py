"""Isolated functional recovery namespace; M01-M12 remain immutable."""
from pathlib import Path
import json,hashlib,os,zipfile
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];DOC=ROOT/'documentation/realism_recovery';CONF=ROOT/'configuration/realism_recovery';RUNS=ROOT/'simulation/runs/realism_recovery';NETS=ROOT/'simulation/network/realism_recovery';DATA=ROOT/'data/realism_recovery';PARENT=ROOT/'simulation/network/m051/provisional/network.net.xml'
def save(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def identity(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def checkpoint():
 target=DOC/'checkpoint/BASELINE_SHA256.json'
 if target.exists():return len(load(target)['files'])
 files={};sources=[];DOC.mkdir(parents=True,exist_ok=True)
 for parent,dirs,names in os.walk(ROOT,followlinks=False):
  dirs[:]=[d for d in dirs if d not in ['.venv','node_modules','__pycache__','build-env','USER_DATA','.git']and not(Path(parent)/d).is_junction()and d!='realism_recovery']
  for n in names:
   p=Path(parent)/n;r=p.relative_to(ROOT).as_posix()
   if n.startswith('recovery_')or n.startswith('GEDANGAN_')and n.endswith('.md')or p.suffix in ['.pyc','.sqlite']or n.endswith(('.sqlite-wal','.sqlite-shm'))or n in ['runtime-launch.log','browser-performance.jsonl','last-start.json','readiness.js']:continue
   files[r]=sha(p)
   if r.startswith(('backend/','frontend/src/','frontend/m12/','configuration/','tests/'))and p.suffix in ['.py','.tsx','.ts','.css','.html','.json','.cjs']:sources.append(p)
 target.parent.mkdir(parents=True,exist_ok=True);save(target,{'created_utc':datetime.now(timezone.utc).isoformat(),'files':files,'scope':'Current post-cleanup M01-M12 source/data/output/release retained in place. Dependencies/live DB/runtime telemetry excluded. No research archive duplicated or deleted.'})
 with zipfile.ZipFile(target.parent/'SOURCE_CHECKPOINT.zip','w',zipfile.ZIP_DEFLATED)as z:
  for p in sources:z.write(p,p.relative_to(ROOT).as_posix())
 save(target.parent/'RELEASE_CHECKPOINT.json',{'canonical_old_release':'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip','sha256':sha(ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip'),'source_zip_sha256':sha(target.parent/'SOURCE_CHECKPOINT.zip'),'unchanged_in_place':True,'files':len(files)})
 return len(files)
if __name__=='__main__':print(checkpoint(),flush=True)
