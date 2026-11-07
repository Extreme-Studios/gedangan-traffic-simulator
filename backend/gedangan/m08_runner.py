"""Private M07 driver reuse. No mutation of old modules, networks, outputs or cohorts."""
import importlib.util,copy,xml.etree.ElementTree as E
from .m04_demand import ROOT,load,save,sha,activate
from .m07_growth import fingerprint
from .m07_projection import baseline,project
from .m07_scenarios import read as growth
from .m08_scenarios import read,validate,LABEL,signal_candidate
from .m08_network import build
from .m08_interventions import cohort,apply_schedule,identity
RUNS=ROOT/'simulation/runs/m08';DOC=ROOT/'documentation/m08'
def driver():
 spec=importlib.util.spec_from_file_location('backend.gedangan.m08_private_m07',ROOT/'backend/gedangan/m07_runner.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.RUNS=RUNS;module.DOC=DOC;module.LABEL=LABEL;return module
def snapshot_sources():
 paths=[ROOT/'backend/gedangan'/n for n in ['m07_runner.py','m07_projection.py','m07_growth.py','m07_scenarios.py','m07_analysis.py','m045_access.py','m04_demand.py','m051_causality.py','m08_scenarios.py','m08_network.py','m08_runner.py','m08_interventions.py']]
 return {str(p.relative_to(ROOT)):sha(p) for p in paths}
def safety(folder,result):
 root=E.parse(ROOT/result['network_path']).getroot();lanes={l.get('id'):l for e in root.findall('edge') for l in e.findall('lane')};cross={c.get('via') for c in root.findall('connection') if c.get('tl')=='osm_859708050' and not c.get('from').startswith('m05_rail_')};events=[e for e in result['rail_events'] if e['controller']=='osm_859708050'];index=0;state='';illegal=[];closed=[];road_on_rail=[];samples=0
 for _,step in E.iterparse(folder/'fcd.xml',events=['end']):
  if step.tag!='timestep':continue
  time=float(step.get('time'))+.5
  while index<len(events) and events[index]['time']<=time:state=events[index]['state'];index+=1
  for v in step:
   samples+=1;lane=v.get('lane');typ=v.get('type')
   if typ!='m05_train' and lane.startswith('m05_rail_'):road_on_rail.append({'time':time,'id':v.get('id'),'lane':lane})
   if typ!='m05_train' and lane in cross and state and set(state)<=set('rR'):closed.append({'time':time,'id':v.get('id'),'lane':lane})
  step.clear()
 audit={'samples':samples,'road_on_rail':road_on_rail,'road_inside_crossing_when_all_closed_red':closed,'illegal_lane_events':result['illegal_permissions'],'teleports':result['teleports'],'collisions':result['collisions'],'emergency_braking':'NOT_MEASURED — no calibrated emergency braking safety threshold','physical_safety_certification':False,'scope':'0.5s FCD road/rail occupancy and driver lane permission checks. Collision0 is not physical clearance/swept-path certification.'};save(folder/'m08-safety.json',audit)
 return audit
def run(sid='S00',year=2026,growth_id='REFERENCE',seed=42,family='pilot-provisional',specification=None,force_folder=None):
 spec=copy.deepcopy(specification or read(sid));validate(spec);network,manifest=build(spec,family);base=baseline();g=growth(growth_id);projection=project(year,g,base);mode='strict' if family.endswith('strict') else 'provisional';original=cohort(projection,base,mode,seed);effective,deferred=apply_schedule(original,spec)
 module=driver();module.NETWORKS={family:network/'network.net.xml'};sig={'version':'m08-1','scenario_specification':spec,'scenario_spec_hash':fingerprint(spec),'derivative_manifest_sha256':sha(network/'manifest.json'),'projection_hash':projection['projection_hash'],'cohort_sha256':identity(original),'effective_schedule_sha256':identity(effective),'network_sha256':manifest['scenario_network_sha256'],'seed':seed,'family':family,'sources':snapshot_sources(),'vehicle_registry_sha256':sha(ROOT/'configuration/demand-m04/vehicle-registry.json'),'railway_config_sha256':sha(ROOT/'configuration/railway-m05/pilot.json'),'sumo_sha256':sha(activate()/'bin/sumo.exe'),'control_schedule':'Trains70/970s for pilot-provisional, original crossing settings; road timing only changes underS01','measurement_window_s':[0,2100],'demand_window_s':[0,1800],'warmup_s':0,'optional_drain_s':0}
 key=fingerprint(sig)[:20];folder=force_folder or RUNS/key
 if (folder/'m08-result.json').exists():
  if load(folder/'m08-input.json')!=sig:raise ValueError('M08 cache signature mismatch')
  for name,h in load(folder/'m08-output-manifest.json').items():
   if sha(folder/name)!=h:raise ValueError('M08 cached output drift: '+name)
  result=load(folder/'m08-result.json');return result
 module.signature=lambda p,n,s,o:sig;module.requests=lambda *args,**kwargs:effective
 # The inherited driver/causal parser use original function globals from this isolated instance.
 result=module.run(projection,family,seed,base,force_folder=folder);save(folder/'m08-input.json',sig);save(folder/'cohort-original.json',original);save(folder/'deferral-ledger.json',deferred)
 last=E.parse(folder/'summary.xml').getroot()[-1];trains=[t for t in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo') if t.get('vType')=='m05_train'];loaded=int(last.get('loaded'))-len(trains)
 if loaded!=result['routable']:raise ValueError('Loaded SUMO summary reconciliation failed')
 departures=set(load(folder/'lifecycle.json')['departed']);arrivals=set(load(folder/'lifecycle.json')['arrived']);deferrals=[r for r in deferred if r['deferred']]
 result={**result,'run_id':key,'solution_id':spec['id'],'solution_version':spec['version'],'solution_name':spec['name'],'growth_scenario':growth_id,'label':LABEL,'loaded_raw_driver_event_samples':result['loaded'],'loaded':loaded,'cohort_sha256':identity(original),'effective_schedule_sha256':identity(effective),'intervention_manifest':manifest,'m08_input':sig,'deferral':{'demand_deferred':len(deferrals),'deferred_vehicle_seconds':sum(r['deferred_seconds'] for r in deferrals),'deferred_departed':sum(r['id'] in departures for r in deferrals),'deferred_arrived':sum(r['id'] in arrivals for r in deferrals),'displaced_outside_demand_window':sum(r['displaced_outside_demand_window'] for r in deferred),'outside_measurement_horizon':sum(r['outside_measurement_horizon'] for r in deferred),'note':'Original requested demand preserved. Delaying trucks has explicit departure opportunity cost; no claim of demand disappearance.'},'validation_status':'SIMULATED — NEEDS FIELD VERIFICATION','cache_status':'FRESH_AT_CREATION'}
 result['safety_audit']=safety(folder,result);save(folder/'m08-result.json',result);save(folder/'m08-output-manifest.json',{p.name:sha(p) for p in folder.iterdir() if p.is_file() and p.name!='m08-output-manifest.json'});print('M08',spec['id'],year,growth_id,seed,'requested',result['requested'],'arrived',result['arrived'],'unserved',result['unserved_total_at_horizon'],flush=True);return result
def train_signal():
 candidates=[]
 for green in [8,12,16]:
  r=run('S01',2026,seed=11,specification=signal_candidate(green));cohorts=r['od'];cost=sum(c['waiting_s_departed_including_unfinished']['mean']*c['departed'] for c in cohorts.values() if c['waiting_s_departed_including_unfinished']['mean'] is not None)+2100*r['unserved_total_at_horizon'];worst=max((c['waiting_s_departed_including_unfinished']['mean'] or 0 for c in cohorts.values()),default=0);candidates.append({'green':green,'run_id':r['run_id'],'cost':cost+worst*len(cohorts),'unserved':r['unserved_total_at_horizon'],'worst_OD_wait_mean_s':worst,'note':'Missing/unfinished trips penalized; worstOD waiting term prevents one-direction-only selection. No empirical objective.'})
 best=min(candidates,key=lambda c:(c['cost'],c['green']));choice=signal_candidate(best['green']);save(DOC/'signal-training.json',{'training_year':2026,'training_growth':'REFERENCE','training_seed':11,'evaluation_seeds':[42,43],'candidate_grid':[8,12,16],'yellow':3,'all_red':2,'candidates':candidates,'selected':choice,'selection_objective':'Sum departed-cohort waiting +2100s each unserved request + worstOD waiting mean×ODcount. Arrived-only duration not selection criterion. All approaches retained.','limitations':'Bounded software experiment; not optimal field timing; no selection on evaluation seeds'});return choice
def batch():
 from .m08_scenarios import initialize
 initialize();DOC.mkdir(parents=True,exist_ok=True);choice=train_signal() if not (DOC/'signal-training.json').exists() else load(DOC/'signal-training.json')['selected'];jobs=[]
 for year in [2026,2030,2040]:
  for seed in ([42,43] if year in [2026,2040] else [42]):
   for sid in ['S00','S01','S02','S03','S04']:jobs.append({'solution':sid,'year':year,'seed':seed})
 jobs.extend([{'solution':s,'year':2035,'seed':42} for s in ['S00','S01']]);done=[]
 for j in jobs:
  save(DOC/'run-queue.json',{'status':'RUNNING','concurrency':1,'total':len(jobs),'completed':done,'next':j});r=run(j['solution'],j['year'],seed=j['seed'],specification=choice if j['solution']=='S01' else None);done.append({**j,'run_id':r['run_id']})
 save(DOC/'run-queue.json',{'status':'COMPLETE','concurrency':1,'total':len(jobs),'completed':done})
if __name__=='__main__':batch()
