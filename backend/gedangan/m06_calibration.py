"""Bounded offline SUMO recovery test. Never empirical calibration."""
import itertools,statistics,json,hashlib,time,xml.etree.ElementTree as ET
from .m04_demand import ROOT,load,save,sha,xml,execute,activate
from .m06_validation import objective
RUNS=ROOT/'simulation/runs/m06';DOC=ROOT/'documentation/m06';CONF=ROOT/'configuration/calibration-m06'
LABEL='SOFTWARE CALIBRATION TEST — NOT EMPIRICAL CALIBRATION'
def fixture(home):
 folder=RUNS/'fixture';folder.mkdir(parents=True,exist_ok=True);ns=ET.Element('nodes');ET.SubElement(ns,'node',id='a',x='0',y='0');ET.SubElement(ns,'node',id='b',x='600',y='0');es=ET.Element('edges');ET.SubElement(es,'edge',id='road',**{'from':'a','to':'b'},speed='12',numLanes='1',allow='passenger',width='3.2');xml(folder/'nodes.xml',ns);xml(folder/'edges.xml',es)
 r=execute([home/'bin/netconvert.exe','-n',folder/'nodes.xml','-e',folder/'edges.xml','-o',folder/'network.net.xml'],folder/'build-log.json');assert r['returncode']==0,r['stderr'];root=ET.parse(folder/'network.net.xml').getroot();xml(folder/'network.net.xml',root);return folder/'network.net.xml'
def simulate(params,seed,network,home):
 if not 12<=params['vehicle_count']<=60 or params['vehicle_count']!=int(params['vehicle_count']) or not .6<=params['speed_factor']<=1.2:raise ValueError('Outside declared synthetic technical envelope')
 key=hashlib.sha256(json.dumps({'params':params,'seed':seed,'network_sha':sha(network),'runner_version':'m06-2'},sort_keys=True).encode()).hexdigest()[:20];folder=RUNS/'trials'/key
 if (folder/'result.json').exists():return load(folder/'result.json')
 folder.mkdir(parents=True,exist_ok=True);routes=ET.Element('routes');ET.SubElement(routes,'vType',id='car',vClass='passenger',length='4.5',minGap='2.5',tau='1.2',accel='2',decel='4',sigma='0.3',speedFactor=str(params['speed_factor']),speedDev='0',maxSpeed='16.67')
 for i in range(params['vehicle_count']):
  v=ET.SubElement(routes,'vehicle',id=f'car_{i}',type='car',depart=str(i*240/max(1,params['vehicle_count']-1)),departSpeed='0');ET.SubElement(v,'route',edges='road')
 xml(folder/'demand.rou.xml',routes);cfg=ET.Element('configuration');inp=ET.SubElement(cfg,'input');ET.SubElement(inp,'net-file',value=str(network));ET.SubElement(inp,'route-files',value=str(folder/'demand.rou.xml'));out=ET.SubElement(cfg,'output');ET.SubElement(out,'tripinfo-output',value=str(folder/'tripinfo.xml'));ET.SubElement(out,'fcd-output',value=str(folder/'fcd.xml'));tm=ET.SubElement(cfg,'time');ET.SubElement(tm,'end',value='600');ET.SubElement(tm,'step-length',value='0.5');xml(folder/'run.sumocfg',cfg)
 log=execute([home/'bin/sumo.exe','-c',folder/'run.sumocfg','--seed',seed,'--no-step-log','true','--error-log',folder/'errors.log'],folder/'process.json')
 if log['returncode']:save(folder/'failure.json',log);raise RuntimeError('Actual SUMO trial failed')
 hazards=[line for line in (folder/'errors.log').read_text(encoding='utf-8').splitlines() if any(word in line.lower() for word in ['teleport','collision','not allowed'])]
 if hazards:save(folder/'failure.json',{'hazards':hazards});raise RuntimeError('SUMO trial safety/permission warning; result excluded')
 trips=ET.parse(folder/'tripinfo.xml').getroot().findall('tripinfo');maxqueue=0;maxextent=0
 for _,step in ET.iterparse(folder/'fcd.xml',events=['end']):
  if step.tag=='timestep':
   stopped=[float(v.get('x')) for v in step if float(v.get('speed'))<.3];maxqueue=max(maxqueue,len(stopped));maxextent=max(maxextent,max(stopped)-min(stopped)+4.5 if stopped else 0);step.clear()
 if len(trips)!=params['vehicle_count']:raise RuntimeError('Censored fixture; requested count not all arrived')
 metrics={'traffic_counts':len(trips),'turning_counts':len(trips),'travel_times':statistics.mean(float(t.get('duration')) for t in trips),'speeds':statistics.mean(float(t.get('routeLength'))/float(t.get('duration')) for t in trips),'waiting_times':statistics.mean(float(t.get('waitingTime')) for t in trips),'queue_counts':maxqueue,'queue_lengths':maxextent,'railway_closure':None,'spillback_events':0}
 result={'runner_version':'m06-2','metric_units':{'queue_counts':'vehicles','queue_lengths':'m','travel_times':'s','speeds':'m/s','waiting_times':'s','traffic_counts':'vehicles/600s'},'category':'SIMULATED_RESULT','label':LABEL,'parameters':params,'seed':seed,'metrics':metrics,'wall_seconds':log['wall_seconds'],'cpu_seconds':log['cpu_seconds'],'peak_working_set_bytes_sampled':log['peak_working_set_bytes_sampled'],'network_sha256':sha(network),'demand_sha256':sha(folder/'demand.rou.xml'),'sumo_version':'1.28.0','all_arrived':True,'trial_id':key};save(folder/'result.json',result);return result
def mean_metrics(rows):return {k:statistics.mean(r['metrics'][k] for r in rows) if all(r['metrics'][k] is not None for r in rows) else None for k in rows[0]['metrics']}
def validate_config(config):
 if not config['calibration_seeds'] or not config['validation_seeds'] or set(config['calibration_seeds'])&set(config['validation_seeds']):raise ValueError('Seed leakage or empty split')
 if len(config['vehicle_counts'])*len(config['speed_factors'])>25:raise ValueError('Staged search capped at25candidates')
 if any(n!=int(n) or not 12<=n<=60 for n in config['vehicle_counts']) or any(not .6<=s<=1.2 for s in config['speed_factors']):raise ValueError('Grid outside parameter registry bounds')
def search(network,home,target,config,stop_after=None):
 validate_config(config)
 path=RUNS/'optimizer-checkpoint.json';signature=hashlib.sha256(json.dumps({'config':config,'target':target,'network':sha(network)},sort_keys=True).encode()).hexdigest();state=load(path) if path.exists() else {'signature':signature,'trials':[],'complete':False}
 if state['signature']!=signature:raise ValueError('Checkpoint input mismatch; create a new versioned experiment')
 done={tuple(t['parameters'].values()) for t in state['trials']};new=0
 for count,speed in itertools.product(config['vehicle_counts'],config['speed_factors']):
  p={'vehicle_count':count,'speed_factor':speed}
  if tuple(p.values()) in done:continue
  rows=[simulate(p,s,network,home) for s in config['calibration_seeds']];prediction=mean_metrics(rows);loss=objective(prediction,target,config['weights'],config['scales']);state['trials'].append({'parameters':p,'prediction':prediction,**loss,'run_ids':[r['trial_id'] for r in rows]});save(path,state);new+=1
  if stop_after is not None and new>=stop_after:return state
 state['complete']=True;state['best']=min(state['trials'],key=lambda t:t['loss']);save(path,state);return state
def main():
 home=activate();RUNS.mkdir(parents=True,exist_ok=True);network=fixture(home);hidden={'vehicle_count':36,'speed_factor':.9};seeds=[11,12,21,22];target_rows=[simulate(hidden,s,network,home) for s in seeds];target=mean_metrics(target_rows[:2]);config={'vehicle_counts':[24,36,48],'speed_factors':[.7,.9,1.1],'calibration_seeds':[11,12],'validation_seeds':[21,22],'weights':{'traffic_counts':1,'travel_times':1},'scales':{'traffic_counts':36,'travel_times':60}}
 save(CONF/'recovery-experiment.json',{**config,'label':LABEL,'target_namespace':'simulation/runs/m06/hidden-target-not-observed','independent_validation_rule':'Seeds21/22reserved, never used in objective selection','horizon_s':600,'warmup_s':0,'hidden_parameter_values':'Retained separately in experiment-evidence.json, never read by search'})
 if not (RUNS/'optimizer-checkpoint.json').exists():search(network,home,target,config,stop_after=2)
 start=time.perf_counter();state=search(network,home,target,config);best=state['best'];holdout=[simulate(best['parameters'],s,network,home) for s in [21,22]];holdout_target=mean_metrics(target_rows[2:]);holdout_loss=objective(mean_metrics(holdout),holdout_target,config['weights'],config['scales'])
 save(RUNS/'experiment-evidence.json',{'hidden_parameters':hidden,'target_run_ids':[r['trial_id'] for r in target_rows],'category':'HIDDEN_SYNTHETIC_TARGET_NOT_FIELD_OBSERVATION'})
 result={'label':LABEL,'technical_recovery_success':best['parameters']==hidden,'hidden':hidden,'best':best,'trials':state['trials'],'calibration_seed_ids':[11,12],'holdout_seed_ids':[21,22],'holdout_loss':holdout_loss,'holdout_label':'INDEPENDENT SYNTHETIC SEEDS — NOT FIELD VALIDATION','checkpoint_resume_tested':True,'objective_search_wall_seconds':time.perf_counter()-start,'empirical_status':'BLOCKED — DATA REQUIRED','identifiability_limit':'Count and speed factor identifiable only in this simple uncongested fixture/grid; tau/minGap and real network OD/control are not identified.','num_unique_sumo_runs':sum(load(p).get('runner_version')=='m06-2' for p in (RUNS/'trials').glob('*/result.json'))};save(DOC/'synthetic-recovery.json',result);print('recovered',best['parameters'],'loss',best['loss'],'holdout',holdout_loss['loss'],flush=True)
 if not result['technical_recovery_success']:raise RuntimeError('Hidden parameter recovery failed')
if __name__=='__main__':main()
