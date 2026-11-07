"""Explicit file-level dry-run. No deletion, no scientific data candidates."""
import json,re,hashlib,shutil,subprocess
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'documentation/storage_cleanup'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 data=json.loads((ROOT/'STORAGE_INVENTORY_BEFORE.json').read_text());files=data['files'];by={f['path']:f for f in files};candidates=[];allclasses=[];refs=[]
 # Current launcher and 3D host use dist-m10, not scratch extraction/freeze directories.
 for p in [ROOT/'backend/gedangan/m12_host.py',ROOT/'backend/gedangan/m12_release.py',ROOT/'backend/gedangan/m10_server.py',ROOT/'tests/m12/distribution.py',ROOT/'backend/gedangan/m10_package.py',ROOT/'backend/gedangan/m11_package.py']:
  refs.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'purpose':'Read consumers, runtime roots and regeneration recipes before selecting targets'})
 # Explicit per-app entrypoints; preserve all assets actually requested by that app.
 allowed={'dist-m02':({'geodata'},'mapping'),'dist-m03':({'network'},'network'),'dist-m04':({'network','demand'},'demand'),'dist-m045':({'access','network','demand'},'m045'),'dist-m05':({'m05'},'m05'),'dist-m051':({'m051'},'m051'),'dist-m06':({'m06'},'m06'),'dist-m07':(set(),'m07'),'dist-m08':(set(),'m08')}
 unused={}
 for build,(used,source)in allowed.items():
  src='\n'.join(p.read_text(encoding='utf-8')for p in(ROOT/'frontend/src'/source).glob('*')if p.suffix in ['.ts','.tsx','.css'])
  refs.append({'path':'frontend/src/'+source,'purpose':'Audited static fetch roots versus API-only app','static_roots_kept':sorted(used)})
  for p in (ROOT/'frontend'/build).iterdir():
   if not p.is_dir()or p.name=='assets'or p.name in used:continue
   canonical=ROOT/'frontend/public'/p.name
   if not canonical.is_dir():continue
   # Search built JS and source for static path and reject any ambiguity.
   compiled='\n'.join(q.read_text(encoding='utf-8')for q in(ROOT/'frontend'/build/'assets').glob('*.js'))
   if '/'+p.name+'/' in src or '/'+p.name+'/' in compiled:continue
   for r,f in by.items():
    if r.startswith(p.relative_to(ROOT).as_posix()+'/'):
     canon='frontend/public/'+p.name+'/'+r[len(p.relative_to(ROOT).as_posix())+1:]
     if canon not in by or by[canon]['sha256']!=f['sha256']:raise ValueError('Unverified public copy '+r)
     unused[r]=canon
 # Only explicitly known QA extraction directories. Original QA logs/screenshots retained.
 extractions=['documentation/m12/extracted portable final','documentation/m12/extracted portable test','documentation/m12/extracted portable v1','presentation_demo/m10/tooling/package-smoke','presentation_demo/m11/tooling/package-smoke']
 intermediates=['documentation/m12/frozen','documentation/m12/freeze-work']
 ffmpeg=shutil.which('ffmpeg');assert ffmpeg and Path(ffmpeg).is_file();canonical_ffmpeg=str(Path(ffmpeg).resolve());ffhash=sha(Path(ffmpeg))
 for f in files:
  r=f['path'];parts=Path(r).parts;classification='E';reason='Unknown or not individually reviewed; protected';candidate=None
  if r in unused:candidate=('C','Unused publicDir copy in a different app build; source and emitted JS do not request this static root',unused[r],'Vite build from retained frontend source/package-lock and canonical public assets; no path used by current runtime')
  elif any(r.startswith(p+'/')for p in extractions):candidate=('B','Disposable package extraction from recorded smoke test; not consumed by any current launcher','FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/','Extract current final portable ZIP and rerun retained package smoke test')
  elif any(r.startswith(p+'/')for p in intermediates):candidate=('B','PyInstaller intermediate/frozen staging; shipped binary remains in FINAL_RELEASE','FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/APPLICATION/','Retained documentation/m12/GEDANGAN_TRAFFIC_SIMULATOR.spec + retained build-env + m12_entry.py; build command in freeze.log')
  elif '__pycache__' in parts or any(x in parts for x in ['.pytest_cache','.mypy_cache','.ruff_cache'])or r.startswith('frontend/node_modules/.vite/'):
   if not r.startswith(('simulation/','data/','geodata/','configuration/','FINAL_RELEASE/')):candidate=('B','Interpreter/transpiler generated cache; source and installed dependency remain',None,'Python imports or Vite dev regenerate; research .venv/node_modules retained')
  elif r in ['presentation_demo/m10/tooling/playwright/ffmpeg-1011/ffmpeg-win64.exe','presentation_demo/m11/tooling/playwright/ffmpeg-1011/ffmpeg-win64.exe']:
   assert f['sha256']==ffhash;candidate=('C','Byte-identical task-local FFmpeg copy; installed canonical FFmpeg verified by SHA256',canonical_ffmpeg,'Copy canonical installed ffmpeg to task tooling if recordVideo tooling needs its old path')
  elif r in ['documentation/m12/portable-test.zip','presentation_demo/m10/GEDANGAN_M10_PRESENTATION_PACKAGE.zip','presentation_demo/m11/GEDANGAN_M11_PAKET_PRESENTASI.zip']:
   candidate=('B','Reproducible historical/package-test archive; current final release and historical source/reports/QA remain','FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip','M10/M11 package.py or tests/m12/distribution.py regenerate packaging; final M12 ZIP is canonical')
  elif r.startswith('.chart-data-'):
   candidate=('B','ArtifactTool intermediate chart embedded workbook snapshots; final native chart/PPTX and authoring source retained','presentation_demo/m11/M11_PRESENTASI_TEKNIS_GEDANGAN.pptx','Run retained presentation_demo/m11/build/deck.mjs using documented authoring runtime')
  if candidate:
   classification,reason,canonical,recovery=candidate
   # Never select real or even ambiguous survey stores, source, research runs or final release.
   assert not r.startswith(('simulation/','data/','geodata/','configuration/','FINAL_RELEASE/'))
   if r.endswith(('.sqlite','.sqlite-wal','.sqlite-shm')):raise ValueError('Protect all survey SQLite '+r)
   entry={**f,'classification':classification,'reason':reason,'canonical_copy':canonical,'dependency_references':['Current m12_host APP root and manifests exclude this target',*(['frontend source/built static-root check']if r in unused else ['Historical build/test recipe only; retained for regeneration'])],'recovery_or_rebuild_method':recovery,'confidence':'HIGH','action':'DELETE_FILE_DRY_RUN'};candidates.append(entry)
  elif r.startswith(('simulation/runs/','documentation/m051/baseline-complete.zip')):classification='D';reason='Unique historical scientific outputs/provenance or original milestone checkpoint preserved'
  elif r.startswith(('backend/','tests/','configuration/','geodata/','data/','simulation/network/','frontend/src/','frontend/public/','FINAL_RELEASE/','toolchain/'))or Path(r).suffix in ['.md','.bat','.ts','.tsx','.py']or 'node_modules' in parts or r.startswith('.venv/'):
   classification='A';reason='Source, scientific input, operational runtime, retained rebuild dependency, report or authoritative public data'
  allclasses.append({'path':r,'bytes':f['bytes'],'sha256':f['sha256'],'classification':classification,'reason':reason})
 selected={f['path']for f in candidates};assert len(selected)==len(candidates)
 # Source and input preservation is content based, not an old milestone whole-workspace claim.
 protected=[f for f in files if f['path']not in selected and not f['path'].startswith(('documentation/storage_cleanup/','FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/USER_DATA/'))and not f['path'].endswith(('.sqlite-wal','.sqlite-shm')) and f['path'].split('/')[-1]not in ['runtime-launch.log','browser-performance.jsonl','last-start.json','readiness.js']]
 summary={c:sum(f['bytes']for f in allclasses if f['classification']==c)for c in 'ABCDE'}
 result={'status':'DRY_RUN_VERIFIED','project_root':str(ROOT),'candidates':candidates,'files':len(candidates),'bytes':sum(f['bytes']for f in candidates),'bytes_by_class':summary,'reference_audit':refs,'retained_dependencies':['.venv','frontend/node_modules except .vite cache','documentation/m12/build-env except __pycache__'],'protected_science':['All simulation, geodata, configuration, data, original public data and survey SQLite','Original source of all 23 playback recordings and canonical final release','Milestone reports, final presentations/videos/screenshots and QA acceptance records'],'recovery_note':'Historical whole-workspace hash inventories retain intentional-deletion entries; cleanup deletion ledger explains them. No empirical source or final manifest path removed.'}
 (ROOT/'SAFE_DELETE_CANDIDATES.json').write_text(json.dumps(result,indent=2),encoding='utf-8');(OUT/'CLASSIFIED_STORAGE.json').write_text(json.dumps(allclasses,indent=2),encoding='utf-8');(OUT/'PROTECTED_FILES.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
 lines=['# Verified cleanup dry run',f"Files: {len(candidates):,}; bytes: {result['bytes']:,}; GiB: {result['bytes']/2**30:.3f}",'','No files deleted yet. File-level paths/hashes and consumer/rebuild evidence are in SAFE_DELETE_CANDIDATES.json.','', '## Approved classes','B generated caches/staging/extracted QA packages; C byte-identical unused frontend copies and task-local FFmpeg.','', '## Protected','All research runs/networks/input, original public datasets, source, release binary/runtime/cache/manifests, survey data, final presentations, milestone reports and QA records.','', '## Scope changes in historical inventories','Some old checkpoints enumerate temporary build copies. These manifests remain historical, and intentional deletions are recorded separately. Functional/scientific checks are performed against surviving source and actual final runtime.']
 (OUT/'DRY_RUN.md').write_text('\n'.join(lines),encoding='utf-8');print(json.dumps({'files':len(candidates),'bytes':result['bytes'],'gib':result['bytes']/2**30,'classes':summary,'unused_frontend_bytes':sum(by[r]['bytes']for r in unused),'protected_files':len(protected)}),flush=True)
if __name__=='__main__':main()
