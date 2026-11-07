"""Final integrity verification of saved actual evidence, independent of SUMO execution."""
from .recovery_common import *
from .recovery_data import build_demand

def main():
 rows=[];baseline=load(DOC/'checkpoint/BASELINE_SHA256.json')['files'];inherited={p:sha(ROOT/p)for p in baseline if p.startswith(('backend/gedangan/m04','configuration/demand-m04/','configuration/railway-m05/'))and(ROOT/p).is_file()}
 assert all(h==baseline[p]for p,h in inherited.items())
 for p in sorted(RUNS.glob('*/result.json')):
  folder=p.parent;r=load(p);inputs=load(folder/'input-manifest.json');manifest=load(folder/'output-manifest.json');errors=[]
  for n,h in manifest.items():
   if not(folder/n).is_file()or sha(folder/n)!=h:errors.append('OUTPUT_HASH:'+n)
  if sha(ROOT/r['network_path'])!=r['network_sha256']:errors.append('NETWORK_HASH')
  if build_demand(r['request'])['cohort_sha256']!=r['cohort_sha256']:errors.append('CURRENT_DEMAND_COHORT_CHANGED')
  sourcepaths={}
  for n,h in inputs['sources'].items():
   current=ROOT/n if '/'in n or '\\'in n else ROOT/'backend/gedangan'/n
   archived=DOC/'runner_revision1'/n
   source=current if current.is_file()and sha(current)==h else archived
   if not source.is_file()or sha(source)!=h:errors.append('RUNNER_REVISION_MISSING:'+n)
   else:sourcepaths[n]=str(source.relative_to(ROOT))
  countok=r['requested']==r['routed']+r['failed_routes']and r['routed']==r['departed']+r['not_departed']and r['departed']==r['arrived']+r['running_at_end']
  if not countok:errors.append('MASS_BALANCE')
  rows.append({'run_id':folder.name,'verified_output_files':len(manifest),'source_revision_paths':sourcepaths,'status':'PASS'if not errors else'FAIL','errors':errors})
 result={'status':'PASS'if all(r['status']=='PASS'for r in rows)else'FAIL','successful_run_evidence':rows,'inherited_source_hashes_verified_against_initial_checkpoint':inherited,'legacy_regression_scope':'Preexisting source/data/archive SHA preservation checked separately. This is not a claim that every historical milestone test was rerun.','original_raw_outputs_modified':False};save(DOC/'final-evidence-verification.json',result);print(result['status'],len(rows),'saved actual runs',flush=True)
if __name__=='__main__':main()
