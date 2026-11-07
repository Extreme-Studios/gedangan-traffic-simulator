import json,hashlib,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REL=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 manifest=json.loads((REL/'BUILD_MANIFEST.json').read_text());archive=json.loads((ROOT/'FINAL_RELEASE/ARCHIVE_MANIFEST.json').read_text());bad=[]
 for r,v in manifest['files'].items():
  if not(REL/r).is_file()or sha(REL/r)!=v['sha256']:bad.append(r)
 assert not bad,bad
 target=ROOT/'FINAL_RELEASE'/archive['file'];assert sha(target)==archive['sha256']
 with zipfile.ZipFile(target) as z:
  assert z.testzip()is None
  for r,v in manifest['files'].items():
   assert hashlib.sha256(z.read('GEDANGAN_TRAFFIC_SIMULATOR/'+r)).hexdigest()==v['sha256'],r
  assert not any('/USER_DATA/' in n for n in z.namelist())
 result={'status':'PASS','manifest_files_verified':len(manifest['files']),'archive_files':archive['files'],'archive_sha256':archive['sha256'],'actual_tested_exe_matches':sha(REL/'APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe')==manifest['tested_exe_sha256'],'qa_survey_data_distributed':False,'release_date':manifest['release_date']}
 (ROOT/'FINAL_RELEASE/FINAL_ARCHIVE_VERIFICATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
