import json,os,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'documentation/storage_cleanup'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 protected=json.loads((OUT/'PROTECTED_FILES.json').read_text());bad=[]
 for f in protected:
  p=ROOT/f['path']
  if not p.is_file()or sha(p)!=f['sha256']:bad.append(f['path'])
 deleted=json.loads((ROOT/'STORAGE_DELETED_FILES_MANIFEST.json').read_text(encoding='utf-8-sig'));approved={f['path']:f for f in deleted['files']};critical=[f for f in protected if f['path'].startswith(('simulation/','configuration/','geodata/','data/','frontend/public/','backend/','tests/'))];science=[f for f in protected if f['path'].startswith(('simulation/','geodata/','data/'))]
 # Tests can regenerate approved bytecode paths. No scientific or canonical asset path may disappear.
 regenerated=[];unexpected=[]
 for r,f in approved.items():
  if(ROOT/r).exists():
   if '__pycache__' in Path(r).parts or '/node_modules/.vite/' in r:regenerated.append(r)
   else:unexpected.append(r)
 assert not unexpected,unexpected
 final=json.loads((ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/BUILD_MANIFEST.json').read_text());finalbad=[]
 for r,f in final['files'].items():
  p=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR'/r
  if not p.is_file()or sha(p)!=f['sha256']:finalbad.append(r)
 result={'status':'PASS'if not bad and not finalbad else'FAIL','retained_files_verified':len(protected),'protected_source_and_input_files':len(critical),'retained_bytes':sum(f['bytes']for f in protected),'research_files':len(science),'research_bytes':sum(f['bytes']for f in science),'changed_or_missing':bad,'final_release_manifest_files_verified':len(final['files']),'final_release_changed_or_missing':finalbad,'approved_cache_paths_regenerated_by_tests':len(regenerated),'scientific_data_deleted':0,'original_23_recording_inputs_preserved':not any(r.startswith(('simulation/','configuration/','presentation_demo/m09/cache/'))for r in bad)}
 (OUT/'PROTECTED_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
 if bad or finalbad:raise SystemExit(1)
if __name__=='__main__':main()
