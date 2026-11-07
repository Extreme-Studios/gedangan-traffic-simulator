import json,hashlib,zipfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'documentation/storage_cleanup';REL=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 rows=json.loads((OUT/'RELEASE_TRIM_DRY_RUN.json').read_text())['files'];ledger=json.loads((ROOT/'STORAGE_DELETED_FILES_MANIFEST.json').read_text(encoding='utf-8-sig'));plan=json.loads((ROOT/'SAFE_DELETE_CANDIDATES.json').read_text());changed=[]
 for r in rows:
  assert not(ROOT/r['path']).exists();entry={**r,'deleted_at':datetime.now(timezone.utc).isoformat(),'verified_absent':True};ledger['files'].append(entry);plan['candidates'].append(r)
 runtime=REL/'APPLICATION/release/runtime-manifest.json';values=json.loads(runtime.read_text())
 for r in rows:del values[r['path'].split('/APPLICATION/')[1]]
 changed.append({'path':runtime.relative_to(ROOT).as_posix(),'before_sha256':sha(runtime)});runtime.write_text(json.dumps(values,indent=2),encoding='utf-8');changed[-1]['after_sha256']=sha(runtime)
 note=REL/'POST_M12_CLEANUP_NOTES.md';note.write_text('Post-M12 storage cleanup removed two upstream pytest-only source data files (1106 bytes) from _internal/jsonschema_specifications/tests. Runtime schemas, Python binary, application executable, recordings, research source and user data remain unchanged. Runtime and build manifests/portable ZIP were refreshed. Original M12 acceptance remains historical; see project STORAGE_CLEANUP_REPORT.md for actual post-cleanup tests.\n',encoding='utf-8')
 bpath=REL/'BUILD_MANIFEST.json';build=json.loads(bpath.read_text());oldbuild=sha(bpath)
 for r in rows:build['files'].pop(r['path'].split('/GEDANGAN_TRAFFIC_SIMULATOR/')[1])
 build['files']['APPLICATION/release/runtime-manifest.json']={'sha256':sha(runtime),'bytes':runtime.stat().st_size};build['files'][note.name]={'sha256':sha(note),'bytes':note.stat().st_size};build['post_m12_cleanup']={'type':'Remove upstream pytest-only source data; executable unchanged','original_exe_sha256':build['tested_exe_sha256']}
 bpath.write_text(json.dumps(build,indent=2),encoding='utf-8');changed.append({'path':bpath.relative_to(ROOT).as_posix(),'before_sha256':oldbuild,'after_sha256':sha(bpath)})
 mirror=REL/'MANIFESTS/BUILD_MANIFEST.json';old=sha(mirror);mirror.write_bytes(bpath.read_bytes());changed.append({'path':mirror.relative_to(ROOT).as_posix(),'before_sha256':old,'after_sha256':sha(mirror)})
 oldarchive=json.loads((ROOT/'FINAL_RELEASE/ARCHIVE_MANIFEST.json').read_text());(OUT/'ORIGINAL_M12_ARCHIVE_MANIFEST.json').write_text(json.dumps(oldarchive,indent=2))
 target=ROOT/'FINAL_RELEASE'/oldarchive['file'];oldsha=oldarchive['sha256']
 with zipfile.ZipFile(target,'w')as z:
  for p in REL.rglob('*'):
   if p.is_file()and 'USER_DATA'not in p.relative_to(REL).parts and p.name!='ARCHIVE_MANIFEST.json':z.write(p,'GEDANGAN_TRAFFIC_SIMULATOR/'+p.relative_to(REL).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix in ['.gz','.png','.pdf','.pptx','.mp4']else zipfile.ZIP_DEFLATED)
 with zipfile.ZipFile(target)as z:assert z.testzip()is None;count=len(z.namelist())
 archive={**oldarchive,'bytes':target.stat().st_size,'sha256':sha(target),'files':count,'post_m12_cleanup':'Only two upstream pytest source data files removed; executable unchanged'}
 ap=ROOT/'FINAL_RELEASE/ARCHIVE_MANIFEST.json';changed.append({'path':ap.relative_to(ROOT).as_posix(),'before_sha256':sha(ap)});ap.write_text(json.dumps(archive,indent=2));changed[-1]['after_sha256']=sha(ap);changed.append({'path':target.relative_to(ROOT).as_posix(),'before_sha256':oldsha,'after_sha256':archive['sha256']})
 ledger['deleted_count']=len(ledger['files']);ledger['deleted_bytes']=sum(r['bytes']for r in ledger['files']);(ROOT/'STORAGE_DELETED_FILES_MANIFEST.json').write_text(json.dumps(ledger,indent=2),encoding='utf-8');plan['files']=len(plan['candidates']);plan['bytes']=ledger['deleted_bytes'];(ROOT/'SAFE_DELETE_CANDIDATES.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
 execution=json.loads((ROOT/'STORAGE_CLEANUP_EXECUTION.json').read_text(encoding='utf-8-sig'));execution.update(deleted_files=ledger['deleted_count'],explicit_file_targets=ledger['deleted_count'],deleted_bytes=ledger['deleted_bytes'],dry_run_plan_sha256=sha(ROOT/'SAFE_DELETE_CANDIDATES.json'),release_trim_addendum='documentation/storage_cleanup/RELEASE_TRIM_DRY_RUN.json');(ROOT/'STORAGE_CLEANUP_EXECUTION.json').write_text(json.dumps(execution,indent=2))
 (OUT/'AUTHORIZED_RELEASE_METADATA_CHANGES.json').write_text(json.dumps({'changes':changed,'source_or_simulation_changed':False,'executable_sha256':sha(REL/'APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe')},indent=2));print(json.dumps({'removed_test_source_bytes':1106,'archive':archive}))
if __name__=='__main__':main()
