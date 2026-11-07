"""Transitive provenance and preserved parent evidence for visual staging."""
from .m156_common import *
def main():
 p=verify();assert p['status']=='PASS',p
 files={};candidates=list((ROOT/'backend/gedangan').glob('m156_*.py'))+list((ROOT/'frontend/src/m156').rglob('*'))+list((ROOT/'frontend/dist-m156').rglob('*'))+list((ROOT/'tests/m156').glob('*.py'))+list(ROOT.glob('M15_6*.md'))+list(DATA.rglob('*'))+list(DOC.rglob('*'))+[ROOT/'frontend/m156.html',ROOT/'frontend/tsconfig.m156.json',ROOT/'frontend/vite.m156.config.ts']
 for folder in RUNS.iterdir():
  if folder.is_dir():candidates+=[folder/n for n in ['input-manifest.json','source-snapshot.json','output-manifest.json','result.json']]
 for f in candidates:
  if f.is_file()and f.name!='artifact-manifest.json'and'__pycache__'not in f.parts:files[f.relative_to(ROOT).as_posix()]=sha(f)
 save(DOC/'artifact-manifest.json',{'created_utc':now(),'scope':'M15.6 source/build/reports/evidence; actual new run manifests reference raw outputs by SHA. Parent recordings remain read-only referenced by baseline-run-references.json. Browser measurements are a bounded snapshot; later live session logs may append without rewriting listed artifacts.','network_sha256':sha(NETWORK),'preservation':p,'files':files});print(json.dumps({'preservation':p,'manifest_files':len(files)},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
