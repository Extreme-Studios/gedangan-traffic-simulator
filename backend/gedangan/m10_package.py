"""Package the offline M10 viewer with verified original recorded cache."""
from pathlib import Path
import json,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'presentation_demo/m10'

def main():
 files=set()
 for d in ['frontend/dist-m10','frontend/src/m10','tests/m10','presentation_demo/m09/cache','presentation_demo/m10/screenshots','presentation_demo/m10/qa','documentation/m10']:
  for p in (ROOT/d).rglob('*'):
   if p.is_file() and '__pycache__' not in str(p) and p.name!='browser-performance.jsonl':files.add(p)
 for p in OUT.glob('*'):
  if p.is_file() and p.name!='package-manifest.json' and p.suffix in ['.md','.json','.mp4','.png','.bat']:files.add(p)
 for name in ['START_GEDANGAN_M10.bat','REBUILD_VISUAL_M10.bat','frontend/visual.html','frontend/vite.visual.config.ts','frontend/package.json','frontend/package-lock.json','frontend/tsconfig.json','backend/__init__.py','backend/gedangan/__init__.py','presentation_demo/m09/M09_DEMO_MANIFEST.json']:
  p=ROOT/name
  if p.is_file():files.add(p)
 files.update((ROOT/'backend/gedangan').glob('m10_*.py'))
 files.update(p for p in (ROOT/'documentation').glob('*') if p.name.startswith(('MILESTONE_10','M10_')) and p.is_file())
 target=OUT/'GEDANGAN_M10_PRESENTATION_PACKAGE.zip'
 with zipfile.ZipFile(target,'w') as z:
  for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix in ['.gz','.mp4','.png','.zip'] else zipfile.ZIP_DEFLATED)
  z.writestr('READ_PACKAGE_FIRST.txt','Gedangan M10 offline viewer. Extract all files, then run START_GEDANGAN_M10.bat. Requires existing Python 3.12+ on PATH or the original project venv. No pip, Node, SUMO, internet or paid service is needed to run the viewer. This includes original read-only recording cache with its source manifest, not the entire 16 GB research workspace. Full legacy regression and 7055-file source verification apply to the original workspace; those old artifacts are deliberately not all copied here. Rebuilding the frontend requires the original local Node dependencies or reproducing package-lock separately. Empirical baseline remains blocked, demand and context illustrative, no M11/M12 started.\n')
 h=hashlib.sha256()
 with target.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 result={'package':target.name,'bytes':target.stat().st_size,'sha256':h.hexdigest(),'files':len(files)+1,'includes_original_recorded_cache':True,'includes_entire_research_workspace':False,'runtime':'existing Python 3.12+; stdlib viewer'}
 (OUT/'package-manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
