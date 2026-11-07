"""Verify pre-recovery source/research/release checkpoint, without touching old data."""
from .recovery_common import *
def main():
 snapshot=load(DOC/'checkpoint/BASELINE_SHA256.json');bad=[];new_receipt=[]
 for r,h in snapshot['files'].items():
  if r=='documentation/storage_cleanup/recovery-checkpoint-start.log':
   new_receipt.append({'path':r,'reason':'This receipt was created empty by the command starting the current recovery checkpoint, then filled by that same command; not an M01-M12 source/data file. Original baseline hash retained unedited.','initial_sha256':h,'now_sha256':sha(ROOT/r)if(ROOT/r).exists()else None});continue
  if not(ROOT/r).is_file()or sha(ROOT/r)!=h:bad.append(r)
 old=load(DOC/'checkpoint/RELEASE_CHECKPOINT.json');release=ROOT/old['canonical_old_release'];value={'status':'PASS'if not bad and sha(release)==old['sha256']else'FAIL','checkpoint_files':len(snapshot['files']),'unchanged_preexisting_files':len(snapshot['files'])-len(new_receipt)-len(bad),'changed_or_missing':bad,'new_work_receipt_exception':new_receipt,'old_M12_release_sha256':sha(release),'old_M12_release_unchanged':sha(release)==old['sha256'],'source_checkpoint_zip_sha256':sha(DOC/'checkpoint/SOURCE_CHECKPOINT.zip'),'source_checkpoint_zip_matches':sha(DOC/'checkpoint/SOURCE_CHECKPOINT.zip')==old['source_zip_sha256'],'research_dataset_deleted':False,'github_uploaded':False};save(DOC/'preservation-verification.json',value);print(json.dumps(value),flush=True)
if __name__=='__main__':main()
