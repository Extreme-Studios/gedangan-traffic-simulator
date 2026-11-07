"""Immutable pre-M09 checkpoint. No old milestone writes."""
import os,json,hashlib,zipfile
from pathlib import Path
from datetime import datetime,timezone
from .m04_demand import ROOT
DOC=ROOT/'documentation/m09'
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def excluded(p):
 s=p.replace('\\','/').lower();return any(x in s for x in ['/m09/','/presentation-m09/','/dist-m09/']) or Path(s).name.startswith(('m09_','milestone_09','start_gedangan_presentation','rebuild_presentation_m09','vite.presentation.')) or s=='frontend/presentation.html'
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
 scope={'created_utc':datetime.now(timezone.utc).isoformat(),'files':len(values),'bytes':total,'source_checkpoint_files':len(source),'source_checkpoint_sha256':digest(DOC/'source-checkpoint.zip'),'exclusions':['installed dependencies/toolchain','caches/locks','live SQLite files/WAL','M09 namespace'],'M10_started':False};(DOC/'baseline-scope.json').write_text(json.dumps(scope,indent=2)+'\n',encoding='utf-8');print(json.dumps(scope),flush=True)
def verify():
 values=json.loads((DOC/'baseline-sha256.json').read_text());bad=[p for p,h in values.items() if not (ROOT/p).is_file() or digest(ROOT/p)!=h]
 if bad:raise ValueError('Old artifact changed: '+str(bad))
 return len(values)
if __name__=='__main__':
 import sys
 print(verify()) if '--verify' in sys.argv else snapshot()
