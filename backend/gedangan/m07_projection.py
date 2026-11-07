"""M04/M06 baseline adapter and OD×class×15minute conservation ledger."""
import random
from .m04_demand import ROOT,load,save,registry,allocate
from .m07_growth import factor,integer_allocate,fingerprint,LABEL,CONDITIONAL
from .m07_scenarios import CONF,read,validate
OUT=ROOT/'simulation/projections/m07'
def baseline(kind='PROVISIONAL_SYNTHETIC_BASELINE',empirical=None):
 if kind=='EMPIRICALLY_CALIBRATED_BASELINE':
  gate=load(ROOT/'documentation/m06/empirical-gate.json');config=load(ROOT/'configuration/calibration-m06/baseline-2026.json')
  if not gate['enabled'] or gate['status']!='READY_FOR_REVIEW' or not config['empirical_baseline']['enabled'] or not empirical or not empirical.get('reviewed') or not empirical.get('independently_validated'):raise ValueError('M06 empirical gate BLOCKED — DATA REQUIRED')
  rows=empirical['cells'];assert all(c['count']>=0 and isinstance(c['count'],int) for c in rows)
  return {'kind':kind,'year':2026,'cells':rows,'source':empirical['provenance'],'status':'REVIEWED_EMPIRICAL_INPUT'}
 if kind!='PROVISIONAL_SYNTHETIC_BASELINE':raise ValueError('Unknown baseline adapter')
 cfg=load(ROOT/'configuration/demand-m04/demand-config.json');matrix=load(ROOT/'simulation/demand/m04/od-matrix.fixture.json')
 movements=matrix['movements']+[{'id':'ketajen_crossing','origin_zone':'station_crossing_west','destination_zone':'ketajen_crossing_east','endpoints':{'strict':{'origin_edge':None,'destination_edge':None},'provisional':{'origin_edge':'w1240685448_s1_p0_0_f','destination_edge':'w1240685448_s1_p2_0_f'}}}]
 weights={m['id']:(4 if m['id'] in ['northbound','southbound'] else 2 if m['id'].startswith('frontage') else 1) for m in movements}
 exact={f'{m["id"]}|{v}|{start}':120*weights[m['id']]/sum(weights.values())*share for m in movements for v,share in cfg['composition'].items() for start in [0,900]}
 counts,rounding=integer_allocate(exact);lookup={m['id']:m for m in movements};cells=[]
 for key in sorted(counts):
  od,cls,start=key.split('|');cells.append({'key':key,'od_id':od,'vehicle_class':cls,'interval_start':int(start),'interval_end':int(start)+900,'count':counts[key]})
 return {'kind':kind,'year':2026,'status':'2026 PROVISIONAL — NOT EMPIRICALLY CALIBRATED','label':LABEL,'source':'M04 composition + M04 medium120 requests/900s as software starting configuration; two intervals; explicit OD weights, not field volume','assumption_id':'M07-BASELINE-01','cells':cells,'movements':lookup,'rounding':rounding,'demand_window':[0,1800],'measurement_window':[0,2100],'day_period':'ILLUSTRATIVE_DAY — not a surveyed calendar date or peak','time_profile':'Preserve two 15-minute interval totals unless explicit profile override'}
def project(year,scenario,base=None,profile=None):
 validate(scenario);base=base or baseline();raw={};audit={};basecells=base['cells']
 if profile is not None:
  if set(profile)!={'0','900'} or any(v<0 for v in profile.values()) or abs(sum(profile.values())-1)>1e-9:raise ValueError('Explicit two-interval profile must sum1')
  totals={}
  for c in basecells:totals[(c['od_id'],c['vehicle_class'])]=totals.get((c['od_id'],c['vehicle_class']),0)+c['count']
 for c in basecells:
  f,steps=factor(year,scenario['rules'],c['vehicle_class'],c['od_id']);n=c['count'] if profile is None else totals[(c['od_id'],c['vehicle_class'])]*profile[str(c['interval_start'])]
  raw[c['key']]=n*f;audit[c['key']]={'factor':f,'annual_schedule':steps,'baseline_count':c['count']}
 counts,rounding=integer_allocate(raw);cells=[{**c,'count':counts[c['key']],'fractional_count':raw[c['key']],**audit[c['key']]} for c in basecells]
 result={'year':year,'scenario':scenario['id'],'scenario_hash':fingerprint(scenario),'baseline_hash':fingerprint(base),'baseline_kind':base['kind'],'label':LABEL,'conditional_label':CONDITIONAL,'status':'CONDITIONAL_SCENARIO_PROJECTION','cells':cells,'requested':sum(counts.values()),'baseline_requested':sum(c['count'] for c in basecells),'rounding':rounding,'profile_override':profile,'demand_window':base['demand_window'],'measurement_window':base['measurement_window'],'day_period':base['day_period']}
 result['projection_hash']=fingerprint(result);return result
def requests(projection,base,mode,seed=42,burst=False):
 rows=[];rng=random.Random(seed)
 for c in projection['cells']:
  move=base['movements'][c['od_id']];endpoints=move['endpoints'][mode]
  for i in range(c['count']):
   depart=c['interval_start']+(i+rng.random())*900/max(1,c['count'])
   if burst:depart=(i+rng.random())*30/max(1,c['count'])
   rows.append({'id':f'm07_{projection["year"]}_{projection["scenario"]}_{c["od_id"]}_{c["vehicle_class"]}_{c["interval_start"]}_{i:05d}','vehicle_type_id':c['vehicle_class'],'od_id':c['od_id'],'origin_zone':move['origin_zone'],'destination_zone':move['destination_zone'],**endpoints,'depart_seconds':round(depart,4),'interval_start_seconds':c['interval_start'],'interval_end_seconds':c['interval_end'],'network_variant':mode,'category':'SYNTHETIC_TEST','provenance_id':'M07-BASELINE-01'})
 return sorted(rows,key=lambda r:(r['depart_seconds'],r['id']))
def main():
 OUT.mkdir(parents=True,exist_ok=True);base=baseline();save(CONF/'baseline-adapter.json',base)
 for name in ['LOW','REFERENCE','HIGH']:
  for y in range(2026,2041):save(OUT/f'{name}-{y}.json',project(y,read(name),base))
 print('45 conditional demand projections generated; no SUMO metrics invented',flush=True)
if __name__=='__main__':main()
