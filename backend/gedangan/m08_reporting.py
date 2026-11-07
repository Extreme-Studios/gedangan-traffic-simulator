"""Publish derived comparison/evidence. Never overwrites M07 reports or outputs."""
import xml.etree.ElementTree as E
from datetime import datetime,timezone
from pathlib import Path
from .m04_demand import ROOT,load,save,sha,registry
from .m08_scenarios import read
from .m08_comparison import compare
from .m08_evaluation import evaluate
from .m08_feasibility import main as feasibility
RUNS=ROOT/'simulation/runs/m08';DOC=ROOT/'documentation/m08';COMP=ROOT/'simulation/comparisons/m08'
def results():
 # The result is written before its final integrity manifest. Never expose a half-published run.
 return [load(p) for p in RUNS.glob('*/m08-result.json') if not p.parent.name.startswith('fresh-reproduction') and (p.parent/'m08-output-manifest.json').exists()]
def baseline_check():
 before=load(DOC/'baseline-sha256.json');bad=[p for p,h in before.items() if sha(ROOT/p)!=h]
 if bad:raise ValueError('M01–M07 baseline drift: '+str(bad))
 return len(before)
def queue_audit(folder):
 playback=load(folder/'playback.json');lanes={};dims={v['id']:v['parameters']['length'] for v in registry()};summary={'sample_period_s':playback['sample_period_s'],'queues_are_actual_recorded_samples':True,'queue_count_not_meters':True,'tail_definition':'Rear-most stopped front position minus registered body length; may extend below lane0 and then is boundary-censored, not reconstructed across prior edge.'}
 for frame in playback['frames']:
  for lane,q in frame['queues'].items():
   cell=lanes.setdefault(lane,{'max_count':0,'max_extent_m':0,'minimum_tail_m':None,'boundary_censored_samples':0,'recorded_queue_samples':0});cell['max_count']=max(cell['max_count'],q['count']);cell['max_extent_m']=max(cell['max_extent_m'],q['extent_m']);cell['boundary_censored_samples']+=q['boundary_censored'];cell['recorded_queue_samples']+=1
   fronts=[v['pos'] for v in frame['vehicles'] if v['lane']==lane and v['speed']<.3]
   if fronts:
    tails=[v['pos']-dims[v['type']] for v in frame['vehicles'] if v['lane']==lane and v['speed']<.3];cell['minimum_tail_front_m']=min(cell.get('minimum_tail_front_m',float('inf')),min(fronts));cell['minimum_tail_m']=min(cell['minimum_tail_m'] if cell['minimum_tail_m'] is not None else float('inf'),min(tails))
 summary['lanes']=lanes;save(folder/'m08-queue-audit.json',summary);return summary

def rerouting(a,b):
 before={q['id']:q for q in load(RUNS/a['run_id']/'route-ledger.json')};after={q['id']:q for q in load(RUNS/b['run_id']/'route-ledger.json')};changed=[];new_failed=[];recovered=[]
 if set(before)!=set(after):raise ValueError('Rerouting audit request identity mismatch')
 for vid,old in before.items():
  new=after[vid]
  for key in ['od_id','vehicle_type_id','origin_edge','destination_edge']:
   if old[key]!=new[key]:raise ValueError('Rerouting changed original OD/type endpoint')
  if old['route_status']=='ROUTABLE' and new['route_status']=='ROUTABLE' and old['edges']!=new['edges']:changed.append(vid)
  if old['route_status']=='ROUTABLE' and new['route_status']!='ROUTABLE':new_failed.append(vid)
  if old['route_status']!='ROUTABLE' and new['route_status']=='ROUTABLE':recovered.append(vid)
 return {'baseline':a['run_id'],'intervention':b['run_id'],'solution':b['solution_id'],'year':b['year'],'growth':b['growth_scenario'],'seed':b['seed'],'family':b['network_variant'],'requested':len(before),'OD_and_type_endpoints_unchanged':True,'rerouted_legal_count':len(changed),'rerouted_legal_ids':changed,'new_failed_count':len(new_failed),'new_failed_ids':new_failed,'became_routable_count':len(recovered),'became_routable_ids':recovered,'evidence':'Actual DUAROUTER route-ledger rows; both routable variants passed inherited source/access/conditional/vehicle screens. This is not field legal certification.'}
def publish():
 DOC.mkdir(parents=True,exist_ok=True);COMP.mkdir(parents=True,exist_ok=True);runs=results();comparisons=[];routes=[]
 for b in runs:
  if b['solution_id']=='S00' or b['seed'] not in [42,43]:continue
  a=next((r for r in runs if r['solution_id']=='S00' and r['year']==b['year'] and r['growth_scenario']==b['growth_scenario'] and r['seed']==b['seed'] and r['m08_input']['family']==b['m08_input']['family']),None)
  if a:
   value=compare(a,b);save(COMP/(a['run_id']+'--'+b['run_id']+'.json'),value);comparisons.append(value);routes.append(rerouting(a,b))
 for r in runs:queue_audit(RUNS/r['run_id'])
 save(DOC/'run-summary.json',runs);save(DOC/'comparisons.json',comparisons);save(DOC/'rerouting-audits.json',routes);save(DOC/'evaluation.json',evaluate(runs));feasibility()
 save(DOC/'coverage.json',{'runs_completed':len(runs),'comparisons':len(comparisons),'years_run':sorted({r['year'] for r in runs}),'seeds_run':sorted({r['seed'] for r in runs}),'solutions_run':sorted({r['solution_id'] for r in runs}),'growth_run':sorted({r['growth_scenario'] for r in runs}),'configured_years':list(range(2026,2041)),'configured_growth':['LOW','REFERENCE','HIGH','Existing custom M07 scenarios'],'unrun_combinations':'NOT RUN, not zero metrics','S05':'STRUCTURALLY_BLOCKED','S06':'CONCEPT_ONLY','S07':'CONCEPT_ONLY','M09_started':False})
 print('M08 published',len(runs),'actual runs',len(comparisons),'paired comparisons',flush=True)
def reproduce():
 from .m08_runner import run
 from .m07_validation import physics_digest
 b=RUNS/'fresh-reproduction'
 if (b/'m08-result.json').exists():b=RUNS/('fresh-reproduction-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'))
 p=run('S00',2026,seed=42);fresh=run('S00',2026,seed=42,force_folder=b);a=RUNS/p['run_id'];same={name:physics_digest(a/name)==physics_digest(b/name) for name in ['tripinfo.xml','fcd.xml']}
 if not all(same.values()):raise ValueError('Fresh M08 physics mismatch')
 before=sha(a/'m08-output-manifest.json');run('S00',2026,seed=42);assert sha(a/'m08-output-manifest.json')==before
 save(DOC/'reproducibility.json',{'fresh_independent_SUMO_run':str(b.relative_to(ROOT)),'physics_equal':same,'cache_manifest_unchanged':True,'baseline_files_checked':baseline_check(),'original_files_drift':[],'method':'Exact numeric XML attributes excluding process/path headers; original input cohort preserved.'})
if __name__=='__main__':
 import sys
 reproduce() if '--reproduce' in sys.argv else publish()
