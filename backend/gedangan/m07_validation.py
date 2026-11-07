"""Sensitivity experiments with named confounds and immutable actual networks."""
import copy,xml.etree.ElementTree as E,hashlib,json
from .m04_demand import ROOT,load,save,sha
from .m07_projection import project,baseline
from .m07_scenarios import read
from .m07_growth import fingerprint
def baseline_check():
 files=load(ROOT/'documentation/m07/baseline-sha256.json');bad=[p for p,h in files.items() if sha(ROOT/p)!=h]
 if bad:raise RuntimeError('M01–M06 drift: '+str(bad))
 return len(files)
def physics_digest(path):
 root=E.parse(path).getroot();return fingerprint([{'tag':e.tag,'attributes':dict(e.attrib),'children':[dict(v.attrib) for v in e]} for e in root])
def _sensitivity():
 from .m07_runner import run
 base=baseline();scenario=read('REFERENCE');ref=project(2040,scenario,base);reference=run(ref);experiments=[]
 mix=copy.deepcopy(base)
 for c in mix['cells']:c['count']=round(c['count']*(1.5 if c['vehicle_class']=='car' else .75 if c['vehicle_class']=='motorcycle' else 1))
 # Explicit changed baseline uncertainty, not claimed constant-total composition.
 experiments.append(('class_mix_and_baseline_uncertainty',project(2040,scenario,mix),mix,{},'Car×1.5/motorcycle×0.75 rounded baseline sensitivity; total can change, confounded baseline+mix, not pure growth.'))
 od=copy.deepcopy(base)
 for c in od['cells']:c['count']=round(c['count']*(1.5 if c['od_id']=='northbound' else .5 if c['od_id']=='southbound' else 1))
 experiments.append(('OD_distribution',project(2040,scenario,od),od,{},'NB×1.5/SB×0.5 baseline cells; total rounding explicit; otherODunchanged.'))
 experiments.append(('departure_profile',project(2040,scenario,base,{'0':.75,'900':.25}),base,{},'Explicit75/25 two-interval profile; no factual peak spreading claim.'))
 experiments.append(('rail_frequency',ref,base,{'trains':[70,370,970,1270]},'Synthetic train schedule doubles; distinct control scenario, excluded pure-growth comparison.'))
 experiments.append(('signal_control',ref,base,{'signal_off':True},'Existing signal controller off only for isolated sensitivity; no network changes.'))
 experiments.append(('behavior_capacity_proxy',ref,base,{'tau_multiplier':1.25},'Headway sensitivity; not a bound on physical road capacity. Actual lane/geometry capacity remains unknown.'))
 rows=[]
 for name,p,b,options,note in experiments:
  r=run(p,base=b,options=options);rows.append({'name':name,'run_id':r['run_id'],'reference_run_id':reference['run_id'],'requested':r['requested'],'arrived':r['arrived'],'pending':r['not_departed'],'max_queue_count':r['max_stopped_count'],'max_queue_extent_m':r['max_lane_queue_extent_m'],'note':note})
 stress=copy.deepcopy(base)
 for c in stress['cells']:c['count']*=2
 from .m07_runner import signature,NETWORKS,RUNS
 p=project(2040,scenario,stress);options={'trains':[70,970],'signal_off':False,'burst':True,'tau_multiplier':1};key=fingerprint(signature(p,NETWORKS['pilot-provisional'],42,options))[:20];failure=RUNS/key/'failure.json'
 try:
  if failure.exists():raise RuntimeError(load(failure)['error'])
  r=run(p,base=stress,options={'burst':True});rows.append({'name':'bounded_burst_stress','status':'COMPLETE','run_id':r['run_id'],'requested':r['requested'],'arrived':r['arrived'],'not_departed':r['not_departed'],'running':r['running_at_end'],'diagnostic':r['diagnostic'],'note':'Twofold synthetic baseline and30s burst; deliberate saturation diagnostic, not year growth forecast.'})
 except RuntimeError as exc:
  if 'bounded per-run wall time' not in str(exc):raise
  rows.append({'name':'bounded_burst_stress','status':'FAILED_RESOURCE_BUDGET','run_id':key,'requested':p['requested'],'failure':str(failure.relative_to(ROOT)),'error':str(exc),'note':'No completed fixed-horizon metrics invented. HIGH2040 primary run separately proves insertion censoring.'})
 save(ROOT/'documentation/m07/sensitivity.json',{'experiments':rows,'growth_rate_uncertainty':'LOW/REFERENCE/HIGH scenarios, no probabilistic CI','baseline_uncertainty':'NOT_CALIBRATED; synthetic total/source arbitrary','OD_composition_uncertainty':'Model OD anchors and class shares unverified','network_geometry_uncertainty':'M051 stop-line/short-lane/clearance and Strict gaps persist; no geometry correction','behavior_uncertainty':'Registry assumptions; headway proxy sensitivity is not a capacity estimate','random_seed_variation':'Seeds42/43 separately recorded; cannot cover missing-data uncertainty','scenario_ranges_not_confidence_intervals':True})
def sensitivity():
 save(ROOT/'documentation/m07/experiment-lock.json',{'status':'RUNNING','task':'sensitivity'})
 try:return _sensitivity()
 finally:save(ROOT/'documentation/m07/experiment-lock.json',{'status':'IDLE'})

def reproduce():
 from .m07_runner import run,RUNS
 p=project(2026,read('REFERENCE'));first=run(p);folder=RUNS/'fresh-reproduction';fresh=run(p,force_folder=folder)
 a=RUNS/first['run_id'];equal={name:physics_digest(a/name)==physics_digest(folder/name) for name in ['tripinfo.xml','fcd.xml']}
 if not all(equal.values()):raise RuntimeError('Fresh SUMO physics mismatch')
 before=sha(a/'output-manifest.json');cached=run(p);assert sha(a/'output-manifest.json')==before
 save(ROOT/'documentation/m07/reproducibility.json',{'fresh_run':str(folder.relative_to(ROOT)),'physics_attributes_equal':equal,'cache_output_manifest_unchanged':True,'baseline_files_checked':baseline_check(),'source_integrity':'PASS','hash_policy':'All output files checked on cache hit; fresh independent SUMO replay compares numeric XML attributes excluding process headers/paths.'})
if __name__=='__main__':
 import sys
 sensitivity() if '--sensitivity' in sys.argv else reproduce()
