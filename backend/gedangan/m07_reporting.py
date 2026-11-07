"""Derived audits from actual M07 XML/recordings; never substitute projection for simulation."""
import xml.etree.ElementTree as E,statistics,shutil
from collections import defaultdict,Counter
from .m04_demand import ROOT,load,save,sha,registry
from .m07_runner import RUNS
from .m07_analysis import distribution,compare
from .m07_lifecycle_audit import audited_result
DOC=ROOT/'documentation/m07';PUBLIC=ROOT/'frontend/public/m07'
def supplement(folder):
 result=load(folder/'result.json');network=ROOT/result['network_path'];input_hashes={name:sha(folder/name) for name in ['result.json','fcd.xml','tripinfo.xml']};input_hashes['network']=sha(network);cached=folder/'supplementary-audit.json'
 if cached.exists():
  previous=load(cached)
  if previous.get('input_sha256')==input_hashes:return previous
 root=E.parse(network).getroot();lengths={l.get('id'):float(l.get('length')) for e in root.findall('edge') for l in e.findall('lane')};roles={e['id']:e['road_function'] for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']};dims={v['id']:v['parameters']['length'] for v in registry()};speeds=[];role_values=defaultdict(list);lane_sum=defaultdict(float);steps=0;hist=Counter();train_moved=set()
 for _,step in E.iterparse(folder/'fcd.xml',events=['end']):
  if step.tag!='timestep':continue
  steps+=1;by=defaultdict(list)
  for v in step.findall('vehicle'):
   speed=float(v.get('speed'));typ=v.get('type');lane=v.get('lane');pos=float(v.get('pos'))
   if typ=='m05_train':
    if speed>.1:train_moved.add(v.get('id'))
    continue
   speeds.append(speed);hist['stopped_<0.3' if speed<.3 else '0.3–5' if speed<5 else '5–10' if speed<10 else '10–20' if speed<20 else '>=20']+=1;role_values[roles.get(lane.rsplit('_',1)[0],'internal_or_other')].append(speed);by[lane].append((max(0,pos-dims[typ]),min(lengths[lane],pos)))
  for lane,intervals in by.items():
   covered=0;end=0
   for lo,hi in sorted(intervals):covered+=max(0,hi-max(end,lo));end=max(end,hi)
   lane_sum[lane]+=min(100,100*covered/lengths[lane])
  step.clear()
 trips=[dict(v.attrib) for v in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo') if v.get('vType')=='m05_train'];controls={int(c.get('linkIndex')) for c in root.findall('connection') if c.get('tl')=='osm_859708050' and not c.get('from').startswith('m05_rail_')};events=result['rail_events'];closed=False;start=None;windows=[]
 for event in events:
  if event['controller']!='osm_859708050':continue
  closing=any(event['state'][i] in 'rRyY' for i in controls)
  if closing and not closed:start=event['time'];closed=True
  if not closing and closed:windows.append({'start_s':start,'road_release_s':event['time'],'duration_s':event['time']-start,'right_censored':False});closed=False
 if closed:windows.append({'start_s':start,'road_release_s':None,'duration_s':2100-start,'right_censored':True})
 data={'input_sha256':input_hashes,'run_id':result['run_id'],'source':'Actual SUMO FCD, tripinfo and traffic-light events, fixed2100s','speed_units':'m/s','vehicle_time_sample_speed_distribution':distribution(speeds),'speed_histogram_samples':dict(hist),'segment_role_speed_distributions':{k:distribution(v) for k,v in role_values.items()},'lane_occupancy_percent_full_horizon':{k:value/steps for k,value in lane_sum.items()},'occupancy_definition':'Clipped union of front-assigned body footprints divided by lane length, each0.5s FCD sample; empty samples contribute0; bodies spanning another edge not reconstructed.','FCD_samples':steps,'actual_train_trips':trips,'train_ids_proven_moved':sorted(train_moved),'road_crossing_closed_windows':windows,'closure_definition':'Any existing road-controlled crossing link red/yellow; synthetic pilot link states, not field gate telemetry.','road_delay_note':'Stopped vehicle-seconds near next crossing red are contextual association only. Incremental causal rail delay needs paired counterfactual.','queue_recovery_note':'Recovery remains model-specific and geometry-provisional; M051 causal-event recovery evidence retained separately.'}
 save(folder/'supplementary-audit.json',data);return data
def publish():
 PUBLIC.mkdir(parents=True,exist_ok=True);results=[];supplements=[]
 for p in RUNS.glob('*/result.json'):
  r=load(p)
  if r.get('status')!='ACTUAL_SUMO_RESULT' or p.parent.name=='fresh-reproduction':continue
  r=audited_result(p.parent);results.append(r);supplements.append(supplement(p.parent))
 primary=[r for r in results if r['baseline_hash']==load(ROOT/'simulation/projections/m07/REFERENCE-2026.json')['baseline_hash'] and r['options']=={'trains':[70,970],'signal_off':False,'burst':False,'tau_multiplier':1}]
 comparisons=[]
 for b in primary:
  a=next((r for r in primary if r['year']==2026 and r['scenario']=='REFERENCE' and r['network_variant']==b['network_variant'] and r['seed']==b['seed']),None)
  if a:comparisons.append(compare(a,b))
 save(DOC/'run-summary.json',results);save(DOC/'comparison.json',comparisons);save(DOC/'supplementary-audits.json',supplements)
 for name in ['run-summary','comparison','source-register','sensitivity','reproducibility']:
  if (DOC/(name+'.json')).exists():shutil.copy2(DOC/(name+'.json'),PUBLIC/(name+'.json'))
 save(PUBLIC/'map.json',load(ROOT/'frontend/public/m06/map.json'))
 print('Published',len(results),'actual runs and',len(comparisons),'comparisons',flush=True)
if __name__=='__main__':publish()
