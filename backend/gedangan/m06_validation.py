"""Loss, holdout, synchronization and empirical release guards."""
import math,statistics
from datetime import datetime
from .m04_demand import ROOT,load
def errors(sim,obs):
 pairs=[(s,o) for s,o in zip(sim,obs) if s is not None and o is not None]
 if len(sim)!=len(obs):raise ValueError('Pair alignment required')
 if not pairs:return {'n':0,'MAE':None,'RMSE':None,'bias':None,'relative_error':None}
 if any(not math.isfinite(x) for p in pairs for x in p):raise ValueError('Nonfinite metric')
 ds=[s-o for s,o in pairs]
 return {'n':len(pairs),'MAE':statistics.mean(abs(x) for x in ds),'RMSE':math.sqrt(statistics.mean(x*x for x in ds)),'bias':statistics.mean(ds),'relative_error':statistics.mean(abs(s-o)/max(abs(o),1) for s,o in pairs),'zero_denominator_policy':'max(abs(observed),1 original metric unit); not conventional percentage at zero'}
def geh(sim,obs,interval_s,unit):
 if unit!='vehicles' or interval_s!=3600:raise ValueError('GEH only for directly observed hourly vehicle counts; no short interval scaling used')
 if min(sim,obs)<0:raise ValueError('negative count')
 return 0 if sim+obs==0 else math.sqrt(2*(sim-obs)**2/(sim+obs))
def objective(pred,target,weights,scales):
 terms={};missing=[]
 for key,w in weights.items():
  if not math.isfinite(w) or not math.isfinite(scales.get(key,0)) or w<0 or scales.get(key,0)<=0:raise ValueError('Invalid objective weight/normalization scale')
  p,o=pred.get(key),target.get(key)
  if p is None or o is None:missing.append(key);continue
  if not math.isfinite(p) or not math.isfinite(o):raise ValueError('Nonfinite objective input')
  terms[key]={'observed_or_fixture_target':o,'predicted':p,'normalized_squared_error':((p-o)/scales[key])**2,'weight':w}
 if missing:raise ValueError('Requested loss metrics missing: '+str(missing))
 if not terms or sum(x['weight'] for x in terms.values())<=0:raise ValueError('No weighted evidence')
 return {'loss':sum(x['normalized_squared_error']*x['weight'] for x in terms.values())/sum(x['weight'] for x in terms.values()),'terms':terms}
def split(records,holdout_groups,group='date'):
 if not records:raise ValueError('INDEPENDENT VALIDATION NOT POSSIBLE WITH AVAILABLE DATA')
 train=[r for r in records if r[group] not in holdout_groups];test=[r for r in records if r[group] in holdout_groups]
 if not train or not test:raise ValueError('Independent holdout insufficient')
 assert_disjoint(train,test);return train,test
def assert_disjoint(train,test):
 ids=lambda rs:{r['observation_id'] for r in rs}
 identity=lambda r:tuple(r.get(k) for k in ['date','interval_start','interval_end','location_id','vehicle_class','kind','approach','direction','turning_movement'])
 if ids(train)&ids(test) or {identity(r) for r in train}&{identity(r) for r in test}:raise ValueError('Calibration/validation leakage')
def distribution_distance(a,b):
 if not a or not b:return None
 if any(not math.isfinite(x) for x in a+b):raise ValueError('Nonfinite distribution')
 return max(abs(sum(v<=x for v in a)/len(a)-sum(v<=x for v in b)/len(b)) for x in sorted(set(a+b)))
def empirical_gate(records,structural,validation=None):
 reasons=[]
 if not records:reasons.append('NO VERIFIED 2026 OBSERVATIONS AVAILABLE')
 if any(r.get('source_class')!='OBSERVED_FIELD' or r.get('quality')!='VERIFIED' or not r.get('date','').startswith('2026-') for r in records):reasons.append('Records not verified2026 field observations')
 if structural:reasons.append('Structural readiness review required for each selected location/metric')
 if not validation or not validation.get('independent_observations') or not validation.get('predeclared_acceptance_justification') or not validation.get('reviewed'):reasons.append('Independent validation and study-specific acceptance review incomplete')
 return {'enabled':not reasons,'status':'BLOCKED — DATA REQUIRED' if reasons else 'READY_FOR_REVIEW','reasons':reasons,'auto_calibrated_label':False}
def match_events(simulated,observed,tolerance_s=5):
 matches=[];unmatched_sim=[];available=set(range(len(observed)))
 for s in simulated:
  candidates=[]
  for i in available:
   o=observed[i]
   if s['location_id']!=o['location_id'] or s['affected_edge']!=o['affected_edge'] or s.get('trigger')!=o.get('trigger'):continue
   error=abs(s['start_s']-o['start_s']);uncertainty=o.get('uncertainty_s',0)
   if error<=tolerance_s+uncertainty and min(s['end_s'],o['end_s'])>=max(s['start_s'],o['start_s']):candidates.append((error,i))
  if candidates:
   _,i=min(candidates);available.remove(i);matches.append({'simulated':s,'observed':observed[i],'start_error_s':s['start_s']-observed[i]['start_s'],'duration_error_s':(s['end_s']-s['start_s'])-(observed[i]['end_s']-observed[i]['start_s']),'recovery_error_s':None if s.get('recovery_s') is None or observed[i].get('recovery_s') is None else s['recovery_s']-observed[i]['recovery_s']})
  else:unmatched_sim.append(s)
 return {'matched':matches,'unmatched_simulated':unmatched_sim,'unmatched_observed':[observed[i] for i in sorted(available)],'status':'NO OBSERVED EVIDENCE — NOT FIELD VALIDATED' if not observed else 'MATCHING_DIAGNOSTIC_ONLY','tolerance_s':tolerance_s,'note':'Greedy nearest eligible event, one-to-one; tolerance is study input, not universal validation threshold.'}
def railway_alignment(row):
 fields=['warning_start','closure','train_pass','train_clearance','barrier_reopen','road_release'];missing=[k for k in fields if row.get(k) is None];times=[datetime.fromisoformat(row[k]) for k in fields if row.get(k)]
 return {'complete':not missing,'missing':missing,'chronological':times==sorted(times),'closure_duration_s':(datetime.fromisoformat(row['road_release'])-datetime.fromisoformat(row['closure'])).total_seconds() if row.get('road_release') and row.get('closure') else None,'schedule_is_closure':False,'geometry_status':'PROVISIONAL — NEEDS FIELD SURVEY'}
