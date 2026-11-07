"""Actual post-cleanup sizes, verified gates and a non-upload backup plan."""
import os,json,hashlib
from pathlib import Path
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'documentation/storage_cleanup'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def scan():
 files=[];folders=defaultdict(int);links=[]
 for parent,dirs,names in os.walk(ROOT,followlinks=False):
  keep=[]
  for d in dirs:
   p=Path(parent)/d
   if p.is_junction()or p.is_symlink():links.append(p.relative_to(ROOT).as_posix())
   else:keep.append(d)
  dirs[:]=keep
  for n in names:
   p=Path(parent)/n;r=p.relative_to(ROOT);size=p.stat().st_size;files.append({'path':r.as_posix(),'bytes':size})
   for q in r.parents:
    if str(q)!='.':folders[q.as_posix()]+=size
 return files,folders,links
def fmt(v):return f'{v:,} bytes / {v/2**30:.3f} GiB'
def main():
 before=read(ROOT/'STORAGE_INVENTORY_BEFORE.json');deleted=read(ROOT/'STORAGE_DELETED_FILES_MANIFEST.json');protected=read(OUT/'PROTECTED_VERIFICATION.json');reg=read(OUT/'regression.json');qa={n:read(OUT/'qa'/f'{n}.json')for n in ['application','presentation','survey','synchronization-performance','lifecycle']};archive=read(ROOT/'FINAL_RELEASE/ARCHIVE_MANIFEST.json')
 assert protected['status']=='PASS'and reg['status']=='PASS';assert all(v['status']=='PASS'for v in qa.values());assert len(deleted['files'])==8075
 blocked={'action':'Remove two upstream pytest-only source-data files in FINAL_RELEASE/APPLICATION/_internal/jsonschema_specifications/tests','bytes':1106,'status':'NOT EXECUTED - AUTOMATIC APPROVAL REVIEW REJECTED','reason':'blocked by policy; tool rejected process creation before command executed','consequence':'Both files retained. No repack or runtime/build manifest change. Canonical M12 ZIP hash unchanged. No workaround or retry used.'};(OUT/'BLOCKED_RELEASE_TRIM.json').write_text(json.dumps(blocked,indent=2),encoding='utf-8')
 bclass=Counter();buckets=Counter()
 for f in deleted['files']:
  r=f['path'];bclass[f['classification']]+=f['bytes']
  if '__pycache__'in Path(r).parts or '/node_modules/.vite/'in r:kind='Generated Python/Vite cache'
  elif 'extracted portable'in r or '/package-smoke/'in r:kind='Disposable extracted smoke-test copies'
  elif '/frozen/'in r or '/freeze-work/'in r:kind='Intermediate executable build'
  elif r.endswith('.zip'):kind='Obsolete reproducible package ZIPs'
  elif '/ffmpeg-'in r:kind='Duplicate task-local FFmpeg'
  elif r.startswith('frontend/dist-'):kind='Unused duplicate publicDir assets'
  else:kind='Chart authoring scratch'
  buckets[kind]+=f['bytes']
 files,folders,links=scan();total=sum(f['bytes']for f in files);net=before['bytes']-total;top=sorted(folders.items(),key=lambda x:x[1],reverse=True)[:20]
 # Conservative, explicit source Git upload list. Scientific data and binaries separately backed up.
 git=[];sourceprefix=('backend/','tests/','configuration/','frontend/src/','frontend/m12/')
 for f in files:
  r=f['path'];p=Path(r);take=False
  if '__pycache__'in p.parts:continue
  if r.startswith(sourceprefix):take=True
  elif r.startswith('presentation_demo/m11/build/')and p.suffix in ['.mjs','.py']:take=True
  elif r.startswith('documentation/storage_cleanup/')and p.suffix in ['.py','.ps1']:take=True
  elif r=='documentation/m12/GEDANGAN_TRAFFIC_SIMULATOR.spec':take=True
  elif len(p.parts)==2 and p.parts[0]=='frontend'and p.suffix in ['.json','.ts','.html']:take=True
  elif len(p.parts)==1 and p.suffix in ['.md','.bat']:take=True
  elif r=='.gitignore':take=True
  elif r.startswith('documentation/')and p.suffix=='.md'and not any(s in r for s in ['build-env/','extracted portable','freeze-work/','frozen/','qa/survey-profile']):take=True
  if take:git.append(f)
 gitbytes=sum(f['bytes']for f in git);(OUT/'GITHUB_SOURCE_ALLOWLIST.json').write_text(json.dumps({'not_uploaded':True,'files':git,'bytes':gitbytes},indent=2),encoding='utf-8')
 release=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR';releasebytes=sum(f['bytes']for f in files if f['path'].startswith('FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/'));runtime=folders['FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/APPLICATION'];presentation=folders.get('FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/PRESENTATION',0);video=folders.get('FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/VIDEO',0);rootfinal=folders.get('FINAL_RELEASE',0)
 data={'status':'PASS_WITH_RELEASE_HYGIENE_LIMITATION','scope':'Logical filesystem sizes, no junction traversal; includes newly generated cleanup evidence in AFTER; BEFORE excluded its own nascent audit script','before_bytes':before['bytes'],'before_files':before['file_count'],'after_bytes':total,'after_files':len(files),'verified_deleted_bytes':deleted['deleted_bytes'],'verified_deleted_files':deleted['deleted_count'],'net_size_reduction_bytes':net,'net_reduction_percent':100*net/before['bytes'],'audit_and_qa_growth_bytes':deleted['deleted_bytes']-net,'deleted_by_class':dict(bclass),'deleted_by_bucket':dict(buckets),'duplicate_redundancy_before_upper_bound':before['duplicate_redundant_upper_bound_bytes'],'protected_research_bytes':protected['research_bytes'],'protected_research_files':protected['research_files'],'final_application_payload_bytes':runtime,'canonical_unpacked_release_bytes':releasebytes,'final_release_folder_including_zip_bytes':rootfinal,'final_portable_zip_bytes':archive['bytes'],'presentation_docs_bytes':presentation,'separate_release_video_bytes':video,'source_git_upload_bytes':gitbytes,'source_git_upload_files':len(git),'remaining_top20_folders':[{'path':p,'bytes':s,'percent':100*s/total}for p,s in top],'blocked_release_trim':blocked,'github_uploaded':False,'paid_service_enabled':False,'junctions_untouched':links}
 def table(values):return '\n'.join(['| Category | Bytes | GiB |','|---|---:|---:|']+[f'| {k} | {v:,} | {v/2**30:.3f} |'for k,v in values])
 sizes=table([('Workspace BEFORE',before['bytes']),('Workspace AFTER',total),('Actual files deleted',deleted['deleted_bytes']),('Net reduction incl new audit/QA',net),('Retained research (simulation/geodata/data)',protected['research_bytes']),('Source Git allowlist',gitbytes),('Application runtime payload',runtime),('Unpacked canonical release',releasebytes),('Presentation documents',presentation),('Separate Full HD video',video),('Portable ZIP',archive['bytes'])])
 toptext='\n'.join(['| Remaining folder | Bytes | GiB | % workspace |','|---|---:|---:|---:|']+[f'| {p} | {s:,} | {s/2**30:.3f} | {100*s/total:.2f}% |'for p,s in top])
 note='Ukuran logis byte isi file, bukan allocated clusters/free-space Windows. Junction eksternal tidak diikuti atau dihapus. Folder bertingkat saling mencakup. BEFORE tidak memasukkan script audit baru; AFTER memasukkan seluruh bukti audit/QA baru, sehingga net reduction lebih kecil dari bytes deleted. Pengukuran diambil tepat sebelum penulisan laporan ini; hanya pertumbuhan kecil teks laporan/JSON setelah titik ukur yang terpisah.'
 after=f'''# STORAGE AUDIT AFTER
{sizes}

Reduction: {100*net/before['bytes']:.2f}% net. {deleted['deleted_count']:,} file benar-benar dihapus. {note}

## Deleted categories
{table(buckets.items())}

## Remaining largest 20 folders
{toptext}

## Regression
{reg['passed']} functional tests pass / {reg['run']} run; {len(reg['skipped'])} service-dependent skip. Five old complete-workspace hash checks explicitly replaced by maintenance retained-file hashes, not silently passed. {protected['retained_files_verified']:,} surviving baseline files match SHA256; {protected['protected_source_and_input_files']:,} source/input files and {protected['research_files']:,} research files unchanged. 866 final release manifest members match. Actual EXE, external-network-blocked Chrome, 23 indexes/chunks, playback, year/growth, split, signal/rail, presentation, exports, survey browser persistence and host restart/clean shutdown PASS. Main user workspace never used for test fixtures.

## Remaining release hygiene limitation
Two upstream pytest-only source data files, 1,106 bytes, remain in the frozen release. Automatic approval review rejected their additional removal with reason "blocked by policy". No workaround/retry. EXE, runtime manifests and canonical ZIP remain unchanged. No venv/node_modules/developer SDK/browser cache/QA database is shipped. QA_EVIDENCE remains deliberately shipped evidence, not test execution dependency.
'''
 (ROOT/'STORAGE_AUDIT_AFTER.md').write_text(after,encoding='utf-8')
 report=f'''# STORAGE CLEANUP REPORT
## Result
**Safe workspace cleanup and simulator regression PASS; tiny final-release hygiene exception retained.**

{sizes}

## Why it reached 18 GB
Actual starting size {fmt(before['bytes'])}. Research SUMO outputs dominate: simulation/runs M08 6,169,411,073 bytes, M07 3,088,589,130, M05.1 1,951,556,333 and M05 922,252,962. These include unique FCD XML, priority traces, event logs and valid run manifests, so no scientific runs were deleted. Several older Vite builds also copied unrelated public datasets automatically, creating 2,296,034,466 bytes of unused identical assets. M10-M12 smoke tests left multiple full package extractions and two identical task-local FFmpeg binaries. A 623,968,713-byte M05.1 original baseline ZIP remains protected as research history.

## Garbage versus identical copies
{table([('B reproducible artifacts removed',bclass['B']),('C verified redundant copies removed',bclass['C']),('All hash-duplicate redundancy upper bound BEFORE',before['duplicate_redundant_upper_bound_bytes'])])}
Hash duplicates alone did not authorize deletion. Scientific identical runs, canonical public data and necessary runtime copies retain their paths. No hardlinks/junction substitutions were used. Canonical FFmpeg on the machine was verified byte-identical before removing task-local copies. Historical M10/M11 ZIPs were removed as regenerable package products; reports, source, manifests, final slide deck/PDF/video and QA remain. M12 FINAL_RELEASE is canonical.

## Actual deletion
{table(buckets.items())}
Every removal used an explicit file path checked inside the project and validated by SHA256 before deletion. No recursive delete, git clean/reset, move to external storage, source deletion or survey database deletion. SHA256, size, category, reason, canonical copy and recovery method are retained in STORAGE_DELETED_FILES_MANIFEST.json and deletion-audit.jsonl. Empty directories may remain and consume negligible metadata. {protected['approved_cache_paths_regenerated_by_tests']} approved cache paths were regenerated by regression; these were not misreported as current free space.

## Integrity and actual operation
21,990 preserved baseline file hashes match with zero changed/missing; all source/network/OSM/rail/vehicle registry/OD/growth/intervention definitions, original scientific SUMO outputs and cached replay inputs remain. Scientific set: {protected['research_files']:,} files, {fmt(protected['research_bytes'])}. This includes every source output referenced by the 23 M09/M12 recording indexes. Runtime preflight verifies every index, chunk and scene.

- Functional legacy suite: {reg['passed']} pass, {len(reg['skipped'])} skip out of {reg['run']} run. Five historical whole-workspace hash tests not applicable to intentional artifact cleanup are explicitly listed and replaced by full retained-file hashes. Original tests/checkpoints were not edited.
- 31 M10 core assertions pass, including 23-run accounting and camera transforms.
- Actual Windows EXE started with system-only PATH; no external Python, Node or SUMO needed. Duplicate startup uses same PID; survey events {qa['lifecycle']['survey_raw_events_before']} -> {qa['lifecycle']['survey_raw_events_after_restart']} survive real host restart. Clean shutdown PASS.
- Actual Chrome: 3D geometry/movement, 2026/2030/2035/2040, HIGH demand, valid intervention/split comparison, fullscreen/camera, signal/rail snapshots, 10-section presentation, all 15 HTML slides, Full HD MP4, PDF/CSV/JSON exports and survey count/video/IndexedDB/mobile/recovery PASS. Every external application request blocked; no network/OS firewall setting changed.
- Final EXE SHA unchanged: {archive['tested_exe_sha256']}. Final portable ZIP unchanged: {archive['sha256']}. ZIP CRC and all 866 content manifest members PASS.

## Final distribution inspection
The application is {fmt(runtime)}; full unpacked user bundle {fmt(releasebytes)}; final ZIP {fmt(archive['bytes'])}. These are separate from the roughly 12.5 GB scientific data, not a 15 GB Windows app. Presentation/video copies still consumed through relative paths remain intentionally intact. No live research data, venv or Node dependencies are included in the release.

Review rejected the additional removal of two pytest source data files totaling 1,106 bytes ("blocked by policy"). Both remain; no repack command ran. This narrowly limits final package hygiene, not functionality. No attempt to bypass the review. Details: documentation/storage_cleanup/BLOCKED_RELEASE_TRIM.json.

## Reproduction and backup
Research .venv, frontend node_modules (except Vite cache), M12 build-env (except bytecode), pinned requirements/package-lock, source implementations, SUMO 1.28.0 toolchain/download and original scientific data remain. No full dependency environment was removed, so rebuilding an environment after deletion was unnecessary. Deleted static copies regenerate from frontend/public with the retained Vite configs; package extraction and PyInstaller intermediates regenerate from retained recipes. Task-local FFmpeg can be restored from verified installed canonical binary if the historical recordVideo harness expects its old path. Deleted M10/M11 packaging outputs can be generated from retained materials; byte-for-byte historical ZIP timestamps are not promised.

GitHub source allowlist: {len(git):,} files, {fmt(gitbytes)} uncompressed. This excludes research data, runtime binaries and immutable checkpoints, which require separate backup. Project is not a Git repository currently; no remote backup has been verified or created. No upload, service purchase or paid LFS activation occurred. See GITHUB_BACKUP_PLAN_AFTER_CLEANUP.md. Scientific archives were not relocated.

{note}
'''
 (ROOT/'STORAGE_CLEANUP_REPORT.md').write_text(report,encoding='utf-8')
 backup=f'''# GITHUB BACKUP PLAN AFTER CLEANUP
## Current state
No Git repository exists in this directory; no upload has occurred. This is a preparation plan and measured file allowlist, not a claim of remote backup.

## 1. Minimal source Git repository
Explicit allowlist: documentation/storage_cleanup/GITHUB_SOURCE_ALLOWLIST.json. {len(git):,} files / {fmt(gitbytes)} before Git compression/history. Includes backend, tests/fixtures, frontend source/config/HTML/package lock, research configs, root launchers and human-readable milestone documentation. Do not use git add -A on the whole research workspace. Existing .gitignore covers some caches/runs but not all large archives/builds, so review the allowlist and exclusions before staging. Scan for secrets and human survey identifiers before any upload. No actual credentials printed or uploaded in this task.

## 2. Scientific research data
Keep a separate immutable archive with inventory SHA256: simulation/, geodata/, data/, frontend/public/ originals, calibration schemas, provenance, seeds/OD/registry, documentation source registers and milestone baseline checkpoint ZIPs. Actual simulation/geodata/data {fmt(protected['research_bytes'])}; frontend/public {fmt(folders.get('frontend/public',0))}; toolchain {fmt(folders.get('toolchain',0))}. Preserve original observation databases/video permissions and use local SQLite backup while stopped; do not place unreviewed private survey data in a public repository. No data was moved to a new storage destination.

## 3. Windows release
One canonical FINAL_RELEASE portable ZIP: {fmt(archive['bytes'])}; SHA256 {archive['sha256']}. Store as a release asset after explicit user upload authorization; avoid committing EXE/runtime/ZIP to source history. GitHub blocks ordinary Git files larger than 100 MiB and documents Releases as an option for distributing binaries. [GitHub official large-file guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github?platform=windows). Check available quotas and privacy before any LFS choice; no paid service is activated here.

## 4. Presentation assets
M11 canonical slide/PPTX/PDF/MP4 and final user manuals already included in the Windows release; do not separately upload their duplicate copies unless editorial source backup is required. Keep presentation_demo/m11/build authoring source plus generated slide images and external authoring runtime requirements. M10/M11 reports remain historical; cleanup manifest records retired packaging products.

## 5. Recovery verification
Clone source into a new location, restore separately inventoried research data and approved survey backup, restore pinned dependencies from requirements/package-lock, verify SUMO toolchain/hash, rebuild in a disposable directory, and run actual EXE/playback/importer/export checks. Verify the final release ZIP hash independently. Record source commit, release hash and scientific dataset manifest together. Until that restore has actually been performed, do not describe the whole scientific project as remotely backed up or remotely recoverable.

## Minimal upload answer
Source Git alone: {fmt(gitbytes)}. Ready-to-use app additionally: {fmt(archive['bytes'])}. Full scientific history is not covered by those two artifacts; the retained 12.5 GB scientific dataset, original public exports, toolchain and checkpoint archives need their own explicit backup. No file removed merely to fit a GitHub target size.
'''
 (ROOT/'GITHUB_BACKUP_PLAN_AFTER_CLEANUP.md').write_text(backup,encoding='utf-8')
 execution=read(ROOT/'STORAGE_CLEANUP_EXECUTION.json');execution['status']='PASS_WITH_RELEASE_HYGIENE_LIMITATION';execution['regression']='PASS';execution['protected_hashes']='PASS';execution['blocked_release_trim']=blocked;(ROOT/'STORAGE_CLEANUP_EXECUTION.json').write_text(json.dumps(execution,indent=2),encoding='utf-8')
 # One final filesystem remeasurement includes the reports just written. Size values above
 # retain their explicit measurement point, and this machine-readable receipt is exact then.
 finalfiles,finalfolders,_=scan();data['after_bytes_including_written_reports']=sum(f['bytes']for f in finalfiles);data['after_files_including_written_reports']=len(finalfiles);(OUT/'STORAGE_MEASUREMENTS.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
 print(json.dumps({k:data[k]for k in ['status','before_bytes','after_bytes','verified_deleted_bytes','net_size_reduction_bytes','net_reduction_percent','final_application_payload_bytes','final_portable_zip_bytes','source_git_upload_bytes','after_bytes_including_written_reports']}),flush=True)
if __name__=='__main__':main()
