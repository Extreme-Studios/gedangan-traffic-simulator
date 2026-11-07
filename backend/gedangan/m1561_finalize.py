"""Manifest for isolated environment correction; no fake visual evidence."""
from .m1561_common import *
def main():
 p=verify();assert p['status']=='PASS',p
 candidates=list((ROOT/'backend/gedangan').glob('m1561_*.py'))+list((ROOT/'frontend/src/m1561').rglob('*'))+list((ROOT/'frontend/dist-m1561').rglob('*'))+list((ROOT/'tests/m1561').glob('*.py'))+list(DATA.rglob('*'))+list(DOC.rglob('*'))+list(ROOT.glob('M15_6_1*.md'))+[ROOT/'frontend/m1561.html',ROOT/'frontend/vite.m1561.config.ts',ROOT/'frontend/tsconfig.m1561.json']
 files={f.relative_to(ROOT).as_posix():sha(f)for f in candidates if f.is_file()and'__pycache__'not in f.parts and f.name!='artifact-manifest.json'};save(DOC/'artifact-manifest.json',{'created_utc':now(),'network_sha256':sha(NETWORK),'preservation':p,'scope':'M15.6.1 source/build/references/static checks/reports and actual browser evidence. Visual verdict is recorded separately; evidence availability is not visual acceptance.','files':files});print(json.dumps({'manifest_files':len(files),'preservation':p},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
