"""Export truthful readiness state and scientific report inputs."""
import shutil,statistics,xml.etree.ElementTree as ET
from .m04_demand import ROOT,load,save,sha
DOC=ROOT/'documentation/m06';PUBLIC=ROOT/'frontend/public/m06'
def publish():
 PUBLIC.mkdir(parents=True,exist_ok=True)
 for name in ['inventory','missing-register','survey-plan','structural-readiness','synthetic-recovery','uncertainty','empirical-gate','coverage','public-source-register','spillback-validation']:
  save(PUBLIC/(name+'.json'),load(DOC/(name+'.json')))
 for name in ['baseline-2026','parameter-registry','observation-mapping']:save(PUBLIC/(name+'.json'),load(ROOT/'configuration/calibration-m06'/(name+'.json')))
 templates=PUBLIC/'templates';templates.mkdir(exist_ok=True)
 for p in (ROOT/'data/templates/m06').iterdir():
  if p.suffix in ['.csv','.json','.xlsx']:shutil.copy2(p,templates/p.name)
 save(PUBLIC/'observations.json',load(ROOT/'data/observations/m06/normalized/observations.json'))
 runs=[load(p) for p in (ROOT/'simulation/runs/m06').rglob('result.json')]
 performance={'simulations':len(runs),'current_runner_simulations':sum(r.get('runner_version')=='m06-2' for r in runs),'retained_v1_diagnostics':sum(r.get('runner_version')!='m06-2' for r in runs),'seeds':sorted({r['seed'] for r in runs}),'wall_seconds_total':sum(r['wall_seconds'] for r in runs),'max_peak_working_set_bytes_sampled':max(r['peak_working_set_bytes_sampled'] or 0 for r in runs),'cpu_seconds_total':sum(r['cpu_seconds'] or 0 for r in runs),'failed_simulations':len(list((ROOT/'simulation/runs/m06').rglob('failure.json'))),'note':'Per-process Windows counters, sampled~20ms. Includes original and corrected unit-audit diagnostic versions plus fresh reproduction target/candidate/holdout runs; cached repeats do not execute again. No VRAM claim.'};save(DOC/'performance.json',performance);save(PUBLIC/'performance.json',performance)
 net=ET.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();roads=[{'id':e.get('id'),'role':'rail' if e.get('id').startswith('m05_rail_') else 'road','points':[[float(v) for v in p.split(',')] for p in e.find('lane').get('shape').split()]} for e in net.findall('edge') if e.get('function')!='internal'];save(PUBLIC/'map.json',{'roads':roads,'proposed':load(ROOT/'configuration/calibration-m06/observation-mapping.json'),'observed':[],'label':'PROPOSED SURVEY STATIONS — NOT VERIFIED OBSERVATION LOCATIONS','coordinate_system':'Local SUMO EPSG32749 offset, retained network; no external tiles'})
 save(DOC/'status.json',{'technical_readiness':'PENDING_FINAL_TESTS','empirical_baseline':'BLOCKED — DATA REQUIRED','empirical_phase':'BLOCKED — INSUFFICIENT OBSERVED DATA','observed_records':0,'baseline_year':2026,'M07_started':False})
if __name__=='__main__':publish()
