"""Fresh SUMO replay, actual interrupted/resumed search and immutable baseline checks."""
import json,hashlib,shutil,xml.etree.ElementTree as ET
from .m04_demand import ROOT,load,save,sha,activate
from . import m06_calibration as engine
DOC=ROOT/'documentation/m06'
def baseline_check():
 before=load(DOC/'baseline-sha256.json');bad=[p for p,h in before.items() if sha(ROOT/p)!=h]
 if bad:raise RuntimeError('Original baseline drift: '+str(bad))
 return len(before)
def physics_digest(path):
 root=ET.parse(path).getroot()
 return hashlib.sha256(json.dumps({'root':dict(root.attrib),'elements':[{'tag':e.tag,'attributes':dict(e.attrib),'children':[dict(v.attrib) for v in e]} for e in root]},sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 checked=baseline_check();home=activate();result=load(DOC/'synthetic-recovery.json');original=engine.RUNS;network=original/'fixture/network.net.xml';config=load(ROOT/'configuration/calibration-m06/recovery-experiment.json');target=result['best']['prediction'];before=sha(network);engine.fixture(home);after=sha(network);assert before==after
 try:
  engine.RUNS=original/'resume-reproduction';engine.RUNS.mkdir(exist_ok=True)
  checkpoint=engine.RUNS/'optimizer-checkpoint.json'
  if not checkpoint.exists():
   first=engine.search(network,home,target,config,stop_after=2);save(engine.RUNS/'interrupted-checkpoint.json',first)
  first=load(engine.RUNS/'interrupted-checkpoint.json');finished=engine.search(network,home,target,config)
  assert len(first['trials'])==2 and len(finished['trials'])==9 and finished['best']['parameters']==result['best']['parameters']
  # The bounded second search generated fresh processes; compare one actual trial to original output.
  trial_id=finished['best']['run_ids'][0];fresh=engine.RUNS/'trials'/trial_id;old=original/'trials'/trial_id
  match={f:physics_digest(old/f)==physics_digest(fresh/f) for f in ['tripinfo.xml','fcd.xml']};assert all(match.values())
  signature_before=sha(checkpoint);again=engine.search(network,home,target,config);assert sha(checkpoint)==signature_before
  save(DOC/'reproducibility.json',{'baseline_files_checked':checked,'baseline_drift':[],'network_before':before,'network_after':after,'fresh_search_initial_trials':len(first['trials']),'fresh_search_resumed_trials':len(finished['trials']),'fresh_recovered_parameters':finished['best']['parameters'],'repeat_best_physics_equal':match,'completed_checkpoint_idempotent':True,'identical_target_metrics':target,'label':engine.LABEL,'method':'Fresh independent SUMO candidate processes, true checkpoint after2candidates, resume remaining7; compare all tripinfo/FCD numeric attributes without process headers or XML whitespace.'})
 finally:engine.RUNS=original
 baseline_check();print('Fresh recovery/replay and immutable baseline verified')
if __name__=='__main__':main()
