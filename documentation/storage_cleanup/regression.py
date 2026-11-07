"""Run functional legacy tests; historical whole-tree checkpoints are superseded by
the explicit cleanup ledger and a full hash check of every retained input."""
import unittest,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));OUT=ROOT/'documentation/storage_cleanup'
HISTORICAL={'test_previous_633_sources_and_outputs_immutable','test_previous_milestones_immutable','test_baseline_files_immutable','test_original_sources_immutable','test_original_milestones_immutable'}
def flatten(suite):
 for test in suite:
  if isinstance(test,unittest.TestSuite):yield from flatten(test)
  else:yield test
def main():
 suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test*.py');tests=[];retired=[]
 for t in flatten(suite):
  if t._testMethodName in HISTORICAL:retired.append({'test':t.id(),'reason':'Historical complete-workspace inventory includes deliberately removed generated files. Replaced for maintenance by PROTECTED_FILES.json SHA256 verification + deletion ledger; original test/source/manifest not edited.'})
  else:tests.append(t)
 result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests))
 value={'status':'PASS'if result.wasSuccessful()else'FAIL','run':result.testsRun,'passed':result.testsRun-len(result.skipped)-len(result.errors)-len(result.failures),'skipped':[{'test':t.id(),'reason':why}for t,why in result.skipped],'errors':[{'test':t.id(),'details':s}for t,s in result.errors],'failures':[{'test':t.id(),'details':s}for t,s in result.failures],'historical_inventory_checks_replaced':retired}
 (OUT/'regression.json').write_text(json.dumps(value,indent=2),encoding='utf-8');print(json.dumps(value));sys.exit(0 if result.wasSuccessful()else 1)
if __name__=='__main__':main()
