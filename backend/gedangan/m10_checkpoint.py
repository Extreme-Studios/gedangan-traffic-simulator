"""Immutable pre-M10 checkpoint. No old milestone writes."""
import os,json,hashlib,zipfile
from pathlib import Path
from datetime import datetime,timezone
from .m04_demand import ROOT
DOC=ROOT/'documentation/m10'
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def excluded(p):
 s=p.replace('\\','/').lower();return any(x in s for x in ['/m10/','/presentation-m10/','/dist-m10']) or Path(s).name.startswith(('m10_','milestone_10','start_gedangan_m10','rebuild_visual_m10','vite.visual.')) or s=='frontend/visual.html' or s=='presentation_demo/m09/qa/browser-performance.jsonl'
def snapshot():
 DOC.mkdir(parents=True,exist_ok=True);target=DOC/'baseline-sha256.json'
 if target.exists():raise ValueError('Checkpoint exists; cannot replace')
 values={};total=0;source=[]
 for parent,dirs,files in os.walk(ROOT):
  dirs[:]=[d for d in dirs if d not in ['.venv','node_modules','__pycache__','.git','toolchain'] and not excluded(str((Path(parent)/d).relative_to(ROOT))+'/')]
  for name in files:
   p=Path(parent)/name;r=p.relative_to(ROOT).as_posix()
   if excluded(r) or p.suffix in ['.pyc','.lock','.sqlite','-wal','-shm'] or name.endswith(('.sqlite-wal','.sqlite-shm')):continue
   values[r]=digest(p);total+=p.stat().st_size
   if r.startswith(('backend/','configuration/','documentation/','frontend/src/','tests/')) and p.suffix in ['.py','.ts','.tsx','.css','.md','.json','.cjs','.txt'] and p.stat().st_size<5*1024*1024:source.append(p)
 target.write_text(json.dumps(values,indent=2)+'\n',encoding='utf-8')
 with zipfile.ZipFile(DOC/'source-checkpoint.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in source:z.write(p,p.relative_to(ROOT))
 scope={'created_utc':datetime.now(timezone.utc).isoformat(),'files':len(values),'bytes':total,'source_checkpoint_files':len(source),'source_checkpoint_sha256':digest(DOC/'source-checkpoint.zip'),'exclusions':['installed dependencies/toolchain','caches/locks','live SQLite files/WAL','M10 namespace','M09 append-only runtime performance telemetry'],'M11_started':False};(DOC/'baseline-scope.json').write_text(json.dumps(scope,indent=2)+'\n',encoding='utf-8');print(json.dumps(scope),flush=True)
def verify():
 values=json.loads((DOC/'baseline-sha256.json').read_text());bad=[p for p,h in values.items() if not (ROOT/p).is_file() or digest(ROOT/p)!=h]
 if bad:raise ValueError('Old artifact changed: '+str(bad))
 return len(values)
if __name__=='__main__':
 import sys
 print(verify()) if '--verify' in sys.argv else snapshot()
