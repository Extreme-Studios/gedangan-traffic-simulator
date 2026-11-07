"""M08.5 preflight and immutable M01–M08 inventory; no old generators invoked."""
import os,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];DOC=ROOT/'documentation/m085'
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def new_namespace(relative):
 p=relative.replace('\\','/').lower()
 return any(x in p for x in ['/m085/','/survey-m085/','/templates/m085/','/survey-media/']) or Path(p).name.startswith(('m085_','m085-','start_survey_m085','rebuild_survey_m085','milestone_08_5','vite.survey.')) or p=='frontend/survey.html'
def snapshot():
 DOC.mkdir(parents=True,exist_ok=True);target=DOC/'baseline-sha256.json'
 if target.exists():raise ValueError('M08.5 baseline already recorded; never overwrite')
 values={};size=0
 for parent,dirs,files in os.walk(ROOT):
  dirs[:]=[d for d in dirs if d not in ['.venv','node_modules','__pycache__','.git','toolchain'] and not new_namespace(str((Path(parent)/d).relative_to(ROOT))+'/')]
  for name in files:
   path=Path(parent)/name;relative=path.relative_to(ROOT).as_posix()
   if new_namespace(relative) or path.suffix in ['.pyc','.lock'] or name in ['Thumbs.db','.DS_Store']:continue
   values[relative]=digest(path);size+=path.stat().st_size
 target.write_text(json.dumps(values,indent=2)+'\n',encoding='utf-8')
 (DOC/'baseline-scope.json').write_text(json.dumps({'recorded_utc':datetime.now(timezone.utc).isoformat(),'files':len(values),'bytes':size,'scope':'All existing project files, including source/configuration/datasets/geodata/simulation outputs/reports/frontend builds. Dependencies .venv/node_modules/toolchain, caches and lock files excluded; M08.5 namespace excluded.','dependency_references':['frontend/package-lock.json','tests/requirements-lock.txt','documentation/m08/toolchain-sha256.json'],'M09_started':False},indent=2)+'\n',encoding='utf-8');print('M08.5 immutable baseline',len(values),'files',size,'bytes',flush=True)
def verify():
 values=json.loads((DOC/'baseline-sha256.json').read_text(encoding='utf-8'));bad=[p for p,h in values.items() if not (ROOT/p).is_file() or digest(ROOT/p)!=h]
 if bad:raise ValueError('Old artifact changed: '+str(bad))
 return len(values)
if __name__=='__main__':
 import sys
 print(verify()) if '--verify' in sys.argv else snapshot()
