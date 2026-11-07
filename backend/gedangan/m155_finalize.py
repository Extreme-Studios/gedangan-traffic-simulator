"""Preservation and artifact hashes, without changing retained simulation evidence."""
from .m155_common import *
def main():
 p=verify_protection();assert p['status']=='PASS',p
 files={}
 candidates=list((ROOT/'backend/gedangan').glob('m155_*.py'))+list((ROOT/'frontend/src/m155').rglob('*'))+list((ROOT/'frontend/dist-m155').rglob('*'))+list((ROOT/'tests/m155').glob('*.py'))+list(ROOT.glob('M15_5*.md'))
 candidates+=list((ROOT/'staging/m155').rglob('*'))+[ROOT/'frontend/m155.html',ROOT/'frontend/tsconfig.m155.json',ROOT/'frontend/vite.m155.config.ts',NETWORK]
 candidates+=list(DOC.rglob('*'))
 for folder in RUNS.iterdir():
  if folder.is_dir():candidates +=[folder/n for n in ['input-manifest.json','source-snapshot.json','output-manifest.json','result.json']]
 for f in candidates:
  if f.is_file()and f.name!='artifact-manifest.json'and'__pycache__'not in f.parts:files[f.relative_to(ROOT).as_posix()]=sha(f)
 save(DOC/'artifact-manifest.json',{'created_utc':now(),'scope':'M15.5 source, reports, build, evidence and run manifests. Raw simulation output hashes are transitively recorded in each run/output-manifest.json, independently audited for eight main runs.','network_sha256':sha(NETWORK),'original_preservation':p,'files':files})
 print(json.dumps({'preservation':p,'manifest_files':len(files)},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
