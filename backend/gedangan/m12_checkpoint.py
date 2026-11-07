"""Write-once pre-release file hashes; earlier milestones remain immutable."""
import hashlib,json,os
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'documentation/m12'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def excluded(r):
 s=Path(str(r).lower())
 return any(x in s.parts for x in ['.venv','node_modules','__pycache__','.git','toolchain','final_release']) or any(x=='m12' for x in s.parts) or s.name.startswith(('m12_','start_gedangan_traffic_simulator','stop_gedangan_traffic_simulator','start_presentation','open_field_survey')) or s.suffix in ['.pyc','.sqlite','.lock'] or s.name.endswith(('.sqlite-wal','.sqlite-shm')) or s.name in ['browser-performance.jsonl','runtime.log','launch-latest.json','readiness.js']
def main():
 DOC.mkdir(parents=True,exist_ok=True);p=DOC/'BASELINE_SHA256.json'
 if p.exists():
  data=json.loads(p.read_text());bad=[r for r,h in data['files'].items() if not (ROOT/r).is_file() or digest(ROOT/r)!=h]
  print(json.dumps({'files':len(data['files']),'changed':bad}));return
 files={}
 for parent,dirs,names in os.walk(ROOT):
  dirs[:]=[d for d in dirs if not excluded((Path(parent)/d).relative_to(ROOT))]
  for n in names:
   f=Path(parent)/n;r=f.relative_to(ROOT)
   if not excluded(r):files[r.as_posix()]=digest(f)
 p.write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'files':files},indent=2),encoding='utf-8')
 print(json.dumps({'baseline_files':len(files),'sha256':digest(p)}))
if __name__=='__main__':main()
