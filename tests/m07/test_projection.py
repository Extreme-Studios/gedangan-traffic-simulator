import unittest,copy,math,json,xml.etree.ElementTree as E
from decimal import Decimal
from backend.gedangan.m04_demand import ROOT,load,sha,registry
from backend.gedangan.m07_growth import factor,annual,resolve,integer_allocate,fingerprint
from backend.gedangan.m07_projection import baseline,project,requests
from backend.gedangan.m07_scenarios import read,validate
from backend.gedangan.m07_analysis import compare
from backend.gedangan.m07_validation import baseline_check
from backend.gedangan.m07_runner import RUNS,NETWORKS
DOC=ROOT/'documentation/m07'
def actual():return [load(p) for p in RUNS.glob('*/result.json') if p.parent.name!='fresh-reproduction' and load(p).get('status')=='ACTUAL_SUMO_RESULT']
class GrowthTests(unittest.TestCase):
 def setUp(self):self.s=read('REFERENCE');self.base=baseline();self.rule=copy.deepcopy(self.s['rules'][0])
 def test_2026_factor_one_for_every_class(self):
  for v in registry():self.assertEqual(factor(2026,[],v['id'],'northbound')[0],1)
 def test_constant_compound_independent_decimal(self):
  for year in range(2026,2041):self.assertAlmostEqual(factor(year,[self.rule],'motorcycle','southbound')[0],float(Decimal('1.025')**(year-2026)),12)
 def test_2027_one_application_not_off_by_one(self):self.assertEqual(factor(2027,[self.rule],'motorcycle','southbound')[0],1.025)
 def test_zero_growth(self):
  self.rule['schedule']['rate']=0;self.assertEqual(factor(2040,[self.rule],'motorcycle','southbound')[0],1)
 def test_negative_growth_reduces_without_negative(self):
  self.rule['schedule']['rate']=-.1;v=factor(2040,[self.rule],'motorcycle','southbound')[0];self.assertGreater(v,0);self.assertLess(v,1)
 def test_piecewise_independent_product(self):
  self.rule['schedule']={'mode':'piecewise','periods':[{'start':2027,'end':2030,'rate':.02},{'start':2031,'end':2040,'rate':.04}]};self.assertAlmostEqual(factor(2035,[self.rule],'motorcycle','southbound')[0],1.02**4*1.04**5)
 def test_year_specific_schedule(self):
  self.rule['schedule']={'mode':'year_specific','rates':{str(y):.01*(y-2026) for y in range(2027,2041)}};self.assertAlmostEqual(factor(2030,[self.rule],'motorcycle','southbound')[0],1.01*1.02*1.03*1.04)
 def test_missing_rate_rejected_not_zero(self):
  with self.assertRaises(ValueError):factor(2027,[],'motorcycle','northbound')
 def test_piecewise_gap_overlap_rejected(self):
  for periods in [[],[{'start':2027,'end':2040,'rate':0}]*2]:
   with self.assertRaises(ValueError):annual({'mode':'piecewise','periods':periods},2030)
 def test_unverified_local_growth_rejected(self):
  self.rule['status']='VERIFIED_LOCAL_TRAFFIC_GROWTH'
  with self.assertRaises(ValueError):resolve([self.rule],'motorcycle','northbound',2030)
 def test_missing_provenance_rejected(self):
  self.rule['provenance_id']=''
  with self.assertRaises(ValueError):resolve([self.rule],'motorcycle','southbound',2030)
 def test_no_geographic_silent_fallback(self):
  self.rule['geographic_scope']='Indonesia'
  with self.assertRaises(ValueError):resolve([self.rule],'motorcycle','southbound',2030)
 def test_verified_priority_over_assumption(self):
  verified={**self.rule,'id':'VERIFIED','status':'VERIFIED_LOCAL_TRAFFIC_GROWTH','local_flow_evidence_verified':True,'schedule':{'mode':'constant','rate':.01}}
  self.assertEqual(resolve([self.rule,verified],'motorcycle','southbound',2030)[0],.01)
 def test_final_OD_substitution_no_double_growth(self):
  value,_=factor(2030,self.s['rules'],'motorcycle','northbound');self.assertAlmostEqual(value,1.04**4);self.assertNotAlmostEqual(value,1.04**4*1.025**4)
 def test_rates_differ_by_class_and_OD(self):
  self.assertNotEqual(factor(2040,self.s['rules'],'motorcycle','southbound')[0],factor(2040,self.s['rules'],'car','southbound')[0]);self.assertNotEqual(factor(2040,self.s['rules'],'motorcycle','northbound')[0],factor(2040,self.s['rules'],'motorcycle','southbound')[0])
 def test_largest_remainder_independent_expected_tie(self):
  counts,a=integer_allocate({'b':1.25,'a':1.25,'c':.5});self.assertEqual(counts,{'b':1,'a':1,'c':1});self.assertEqual(a['rounded_total'],3)
 def test_integer_half_up_and_stable_order(self):
  a,_=integer_allocate({'b':.75,'a':.75});b,_=integer_allocate({'a':.75,'b':.75});self.assertEqual(a,b);self.assertEqual(sum(a.values()),2)
 def test_invalid_rates_and_counts(self):
  for value in [float('nan'),float('inf'),-.99,.21,True]:
   with self.assertRaises(ValueError):annual({'mode':'constant','rate':value},2027)
  with self.assertRaises(ValueError):integer_allocate({'x':-1})
 def test_all_years_fractional_expected_independently(self):
  for year in range(2026,2041):
   p=project(year,self.s,self.base);expected=0
   for c in self.base['cells']:
    r=.04 if c['vehicle_class']=='motorcycle' and c['od_id']=='northbound' else next(r['schedule']['rate'] for r in self.s['rules'] if r['vehicle_class']==c['vehicle_class'] and r['od_relation']=='*')
    expected+=c['count']*(1+r)**(year-2026)
   self.assertAlmostEqual(p['rounding']['exact_total'],expected,8);self.assertEqual(p['requested'],math.floor(expected+.5))
 def test_interval_class_OD_conservation(self):
  for name in ['LOW','REFERENCE','HIGH']:
   p=project(2040,read(name));self.assertEqual(sum(c['count'] for c in p['cells']),p['requested']);self.assertTrue(all(type(c['count'])==int and c['count']>=0 for c in p['cells']))
 def test_profile_override_preserves_fractional_total(self):
  a=project(2040,self.s);b=project(2040,self.s,profile={'0':.75,'900':.25});self.assertAlmostEqual(a['rounding']['exact_total'],b['rounding']['exact_total']);self.assertEqual(a['requested'],b['requested'])
 def test_requests_deterministic_unique_ID_and_seed(self):
  p=project(2035,self.s);a=requests(p,self.base,'provisional',42);b=requests(p,self.base,'provisional',42);c=requests(p,self.base,'provisional',43);self.assertEqual(a,b);self.assertNotEqual(a,c);self.assertEqual(len({r['id'] for r in a}),p['requested']);self.assertEqual({r['id'] for r in a},{r['id'] for r in c})
 def test_empirical_gate_cannot_be_bypassed(self):
  with self.assertRaises(ValueError):baseline('EMPIRICALLY_CALIBRATED_BASELINE',{'reviewed':True,'independently_validated':True})
 def test_custom_scenario_label_bounds_and_hash(self):
  c=copy.deepcopy(self.s);c['id']='CUSTOM_TEST';self.assertNotEqual(validate(c),validate(self.s));c['status']='OFFICIAL_FORECAST'
  with self.assertRaises(ValueError):validate(c)
 def test_future_empirical_adapter_preserves_contract_and_blocks_current_gate(self):
  from backend.gedangan.m07_baseline_adapter import resolve,validate_bundle
  bundle={**self.base,'provenance':'SYNTHETIC_CONTRACT_TEST_ONLY','review_document':'not-field-evidence','reviewed':True,'independently_validated':True,'m06_observation_sha256':'test-only'}
  self.assertEqual(validate_bundle(bundle)['cells'],self.base['cells'])
  with self.assertRaises(ValueError):resolve('EMPIRICALLY_CALIBRATED_BASELINE',bundle)
 def test_future_bundle_rejects_wrong_interval_or_empty_cells(self):
  from backend.gedangan.m07_baseline_adapter import validate_bundle
  with self.assertRaises(ValueError):validate_bundle({})
 def test_original_sources_immutable(self):self.assertGreater(baseline_check(),2800)
class ActualSUMOTests(unittest.TestCase):
 def setUp(self):self.runs=actual();self.first=next(r for r in self.runs if r['year']==2026 and r['network_variant']=='pilot-provisional' and r['seed']==42)
 def test_four_representative_years_two_seeds(self):
  self.assertTrue({(y,s) for y in [2026,2030,2035,2040] for s in [42,43]}<={(r['year'],r['seed']) for r in self.runs if r['scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional'})
 def test_actual_lifecycle_conservation_all_runs(self):
  for r in self.runs:self.assertEqual(r['requested'],r['failed_routes']+r['arrived']+r['running_at_end']+r['not_departed']);self.assertEqual(r['routable'],r['departed']+r['not_departed']);self.assertEqual(r['departed'],r['arrived']+r['running_at_end'])
 def test_oversize_rejected_explicitly(self):
  rows=load(RUNS/self.first['run_id']/'route-ledger.json');oversize=[r for r in rows if r['vehicle_type_id']=='oversize'];self.assertTrue(oversize);self.assertTrue(all('OVERSIZE' in r['reason'] and r['route_status']=='NOT_ROUTABLE' for r in oversize))
 def test_motor_and_several_nonpassenger_proven_motion(self):
  cls=self.first['class_lifecycle'];self.assertGreater(cls['motorcycle']['moved'],0);self.assertGreater(sum(v['moved']>0 for k,v in cls.items() if k not in ['motorcycle','car','oversize']),2)
 def test_actual_fcd_lane_permissions(self):
  from backend.gedangan.m04_demand import activate
  activate();import sumolib
  net=sumolib.net.readNet(str(NETWORKS['pilot-provisional']),withInternal=True);vclass={v['id']:v['sumo_vclass'] for v in registry()};checked=0
  for _,step in E.iterparse(RUNS/self.first['run_id']/'fcd.xml',events=['end']):
   if step.tag!='timestep':continue
   for v in step:
    if v.get('type')=='m05_train':continue
    checked+=1;self.assertTrue(net.getLane(v.get('lane')).allows(vclass[v.get('type')]))
   step.clear()
  self.assertGreater(checked,1000)
 def test_frontage_separate_and_heavy_not_forced(self):
  rows=load(RUNS/self.first['run_id']/'route-ledger.json');front=[r for r in rows if r['od_id']=='frontage_continuity'];self.assertTrue(any(r['route_status']=='ROUTABLE' for r in front));self.assertTrue(all(r['route_status']=='NOT_ROUTABLE' for r in front if r['vehicle_type_id'] in ['bus','medium_truck','heavy_truck','trailer','oversize']))
 def test_strict_and_provisional_failure_differences(self):
  strict=next(r for r in self.runs if r['network_variant']=='pilot-strict');self.assertGreater(strict['failed_routes'],self.first['failed_routes']);self.assertNotEqual(strict['network_sha256'],self.first['network_sha256'])
 def test_loaded_count_reconciles_to_actual_SUMO_summary(self):
  from backend.gedangan.m07_lifecycle_audit import audited_result
  for raw in self.runs:
   r=audited_result(RUNS/raw['run_id']);self.assertEqual(r['loaded'],r['routable']);self.assertGreaterEqual(r['loaded'],r['departed']);self.assertEqual(r['loaded_reconciliation']['raw_loaded_events_sampled_after_initial_step'],raw['loaded'])
 def test_no_silent_dropped_trips(self):
  for r in self.runs:
   rows=load(RUNS/r['run_id']/'route-ledger.json');self.assertEqual(len(rows),r['requested']);self.assertEqual(sum(q['route_status']=='NOT_ROUTABLE' for q in rows),r['failed_routes'])
 def test_unfinished_and_undeparted_XML_parser(self):
  self.assertTrue(any(r['censored'] for r in self.runs))
  for r in self.runs:
   values=load(RUNS/r['run_id']/'lifecycle.json')['trips'];self.assertEqual(len(values),r['routable']);self.assertEqual(sum(float(v['arrival'])<0 and float(v['depart'])>=0 for v in values.values()),r['running_at_end']);self.assertEqual(sum(float(v['depart'])<0 for v in values.values()),r['not_departed'])
 def test_no_recorded_illegal_teleport_or_collision(self):
  for r in self.runs:self.assertEqual(r['illegal_permissions'],[]);self.assertEqual(r['teleports'],[]);self.assertEqual(r['collisions'],[])
 def test_fixed_horizon_and_control_comparison(self):
  for r in self.runs:self.assertEqual(r['fixed_horizon_s'],2100);self.assertEqual(r['demand_window_s'],[0,1800]);self.assertEqual(r['optional_drain_s'],0)
  other=next(r for r in self.runs if r['year']==2040 and r['scenario']=='REFERENCE' and r['seed']==42 and r['baseline_hash']==self.first['baseline_hash'] and r['options']==self.first['options']);self.assertTrue(compare(self.first,other)['comparable_for_pure_growth']);self.assertIsNotNone(compare(self.first,other)['warning'])
 def test_control_or_network_mismatch_rejected_for_pure_growth(self):
  other=next(r for r in self.runs if r['network_variant']=='pilot-strict');self.assertFalse(compare(self.first,other)['comparable_for_pure_growth'])
 def test_saturation_exposes_pending_or_running(self):
  stress=next(v for v in load(DOC/'sensitivity.json')['experiments'] if v['name']=='bounded_burst_stress');high=next(r for r in self.runs if r['year']==2040 and r['scenario']=='HIGH');self.assertGreater(high['running_at_end']+high['not_departed'],0);self.assertTrue(high['censored']);self.assertIn('DEMAND EXCEEDS',high['diagnostic'])
  if stress['status']=='FAILED_RESOURCE_BUDGET':self.assertTrue((ROOT/stress['failure']).exists());self.assertNotIn('arrived',stress)
  else:self.assertEqual(stress['status'],'COMPLETE')
 def test_fresh_reproduction_and_cache(self):
  r=load(DOC/'reproducibility.json');self.assertTrue(all(r['physics_attributes_equal'].values()));self.assertTrue(r['cache_output_manifest_unchanged'])
 def test_actual_recorded_playback_not_random(self):
  p=load(RUNS/self.first['run_id']/'playback.json');self.assertTrue(p['frames']);self.assertEqual(p['sample_period_s'],5);self.assertIn('Actual SUMO',p['source'])
 def test_sensitivity_separates_uncertainties(self):
  s=load(DOC/'sensitivity.json');self.assertEqual(len(s['experiments']),7);self.assertTrue(s['scenario_ranges_not_confidence_intervals']);self.assertIn('NOT_CALIBRATED',s['baseline_uncertainty'])
 def test_public_sources_not_promoted_to_growth(self):
  s=load(DOC/'source-register.json');self.assertEqual(s['verified_local_growth_rates'],0);self.assertTrue(all(not r['verified_local_traffic_growth'] for r in s['sources']))
 def test_output_hashes_and_SUMO_actual_version(self):
  for r in self.runs:
   self.assertEqual(r['sumo_version'],'1.28.0');folder=RUNS/r['run_id']
   for name,h in load(folder/'output-manifest.json').items():self.assertEqual(sha(folder/name),h)
if __name__=='__main__':unittest.main()
