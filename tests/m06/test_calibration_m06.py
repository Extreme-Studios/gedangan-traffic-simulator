import unittest,tempfile,json,csv,math,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
from backend.gedangan.m04_demand import ROOT,load,sha,save,activate
from backend.gedangan import m06_observations as obs
from backend.gedangan.m06_validation import errors,geh,objective,split,assert_disjoint,empirical_gate,match_events,railway_alignment,distribution_distance
from backend.gedangan.m06_calibration import validate_config,search
D=ROOT/'documentation/m06';C=ROOT/'configuration/calibration-m06'
class CalibrationM06Tests(unittest.TestCase):
 def setUp(self):
  self.row=load(ROOT/'data/observations/m06/synthetic-demo/example.json')[0];self.prov=load(ROOT/'data/observations/m06/synthetic-demo/provenance.json')
 def test_baseline_files_immutable(self):self.assertFalse([p for p,h in load(D/'baseline-sha256.json').items() if sha(ROOT/p)!=h])
 def test_six_schemas_accept_explicit_missing_not_fill_zero(self):
  for kind in obs.KINDS:
   row={**self.row,'kind':kind};row={k:v for k,v in row.items() if k in obs.BASE};row.update({k:None for k in obs.KINDS[kind]});self.assertIn('MISSING_VALUES',obs.validate(row,self.prov))
 def test_zero_valid_but_missing_stays_missing(self):
  self.assertEqual(obs.normalize_csv({k:('' if v is None else str(v)) for k,v in self.row.items()},'traffic_count')['count'],0)
  self.assertIsNone(obs.normalize_csv({**{k:('' if v is None else str(v)) for k,v in self.row.items()},'count':''},'traffic_count')['count'])
 def test_timezone_wrong_offset_rejected(self):
  with self.assertRaises(ValueError):obs.validate({**self.row,'interval_start':'2026-10-01T07:00:00+00:00'},self.prov)
 def test_undocumented_field_source_cannot_be_observed(self):
  with self.assertRaises(ValueError):obs.validate({**self.row,'source_class':'OBSERVED_FIELD'},self.prov)
 def test_negative_nan_count_and_invalid_class_rejected(self):
  for key,val in [('count',-1),('count',float('nan')),('vehicle_class','ignoring')]:
   with self.assertRaises(Exception):obs.validate({**self.row,key:val},self.prov)
 def test_interval_aggregation_zero_missing_and_gaps(self):
  rows=load(ROOT/'data/observations/m06/synthetic-demo/example.json');self.assertIsNone(obs.aggregate_counts(rows,rows[0]['interval_start'],rows[-1]['interval_end']));self.assertEqual(obs.aggregate_counts([{**r,'count':0} for r in rows],rows[0]['interval_start'],rows[-1]['interval_end']),0)
  with self.assertRaises(ValueError):obs.aggregate_counts(rows[:1],rows[0]['interval_start'],rows[-1]['interval_end'])
 def test_import_duplicate_reject_raw_retained(self):
  old=obs.OBS
  try:
   with tempfile.TemporaryDirectory() as tmp:
    obs.OBS=Path(tmp);f=Path(tmp)/'in.json';f.write_text(json.dumps([self.row,self.row]));a,b=obs.ingest(f,self.prov,'x',True);self.assertEqual((len(a),len(b)),(1,1));self.assertEqual(sha(f),sha(Path(tmp)/'synthetic-demo-imports/x/raw.json'))
    with self.assertRaises(ValueError):obs.ingest(f,self.prov,'x',True)
  finally:obs.OBS=old
 def test_csv_import_matches_json_zero(self):
  old=obs.OBS
  try:
   with tempfile.TemporaryDirectory() as tmp:
    obs.OBS=Path(tmp);f=Path(tmp)/'in.csv'
    with f.open('w',newline='',encoding='utf-8') as out:w=csv.DictWriter(out,fieldnames=self.row);w.writeheader();w.writerow(self.row)
    a,b=obs.ingest(f,self.prov,'csv',True);self.assertFalse(b);self.assertEqual(a[0]['count'],0)
  finally:obs.OBS=old
 def test_outlier_is_flagged_not_deleted(self):self.assertIn('OUTLIER_REVIEW_NOT_DELETED',obs.validate({**self.row,'count':12000},self.prov))
 def test_mapping_exact_and_ambiguity_manual_review(self):
  m=load(C/'observation-mapping.json');self.assertEqual(obs.map_observation(self.row,m)['status'],'MAPPED_MODEL_REFERENCE');self.assertEqual(obs.map_observation(self.row,m+[m[0]])['status'],'NEEDS MANUAL REVIEW');self.assertEqual(obs.map_observation({**self.row,'direction':'unknown'},m)['status'],'NEEDS MANUAL REVIEW')
 def test_mapping_uses_real_edges_and_lanes(self):
  root=ET.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();edges={e.get('id') for e in root.findall('edge')};lanes={l.get('id') for e in root.findall('edge') for l in e.findall('lane')}
  for m in load(C/'observation-mapping.json'):self.assertIn(m['edge_id'],edges);self.assertTrue(set(m['lane_ids'])<=lanes)
 def test_od_and_turning_aggregation(self):
  r={'origin':'A','destination':'B','vehicle_class':'car','interval_start':'s','interval_end':'e','count':0};self.assertEqual(obs.aggregate_od([r,r])[0]['count'],0);self.assertIsNone(obs.aggregate_od([r,{**r,'count':None}])[0]['count']);self.assertEqual(obs.turning_balance(10,[3,3,4])['status'],'CONSISTENT');self.assertEqual(obs.turning_balance(10,[3,3,5])['status'],'REVIEW_REQUIRED')
 def test_leakage_rejected_by_ids_and_measurement_identity(self):
  with self.assertRaises(ValueError):assert_disjoint([self.row],[self.row])
  with self.assertRaises(ValueError):assert_disjoint([self.row],[{**self.row,'observation_id':'other'}])
 def test_date_holdout_is_independent(self):
  rows=[self.row,{**self.row,'observation_id':'second','date':'2026-10-02','interval_start':'2026-10-02T07:00:00+07:00','interval_end':'2026-10-02T07:15:00+07:00'}];a,b=split(rows,{'2026-10-02'});self.assertEqual(len(a),1);self.assertEqual(len(b),1)
 def test_missing_field_data_blocks_empirical_even_recovered_fixture(self):
  gate=empirical_gate([],load(D/'structural-readiness.json'));self.assertFalse(gate['enabled']);self.assertFalse(load(C/'baseline-2026.json')['empirical_baseline']['enabled']);self.assertEqual(load(ROOT/'data/observations/m06/normalized/observations.json'),[])
 def test_loss_metrics_zero_and_missing_semantics(self):
  r=errors([0,3,None],[0,1,5]);self.assertEqual(r['n'],2);self.assertEqual(r['MAE'],1);self.assertEqual(r['bias'],1);self.assertIsNone(errors([None],[None])['RMSE']);self.assertEqual(geh(0,0,3600,'vehicles'),0)
  with self.assertRaises(ValueError):geh(3,4,900,'vehicles')
 def test_seven_objective_terms_and_missing_rejected(self):
  keys=['traffic_counts','turning_counts','travel_times','speeds','queue_lengths','waiting_times','railway_closure'];values={k:0 for k in keys};self.assertEqual(objective(values,values,{k:1 for k in keys},{k:1 for k in keys})['loss'],0)
  with self.assertRaises(ValueError):objective({},values,{'railway_closure':1},{'railway_closure':1})
 def test_hidden_synthetic_recovery_actual_sumo_outputs(self):
  r=load(D/'synthetic-recovery.json');self.assertEqual(r['best']['parameters'],load(ROOT/'simulation/runs/m06/experiment-evidence.json')['hidden_parameters']);self.assertEqual(len(r['trials']),9);self.assertEqual(r['best']['loss'],0);self.assertEqual(r['holdout_loss']['loss'],0);self.assertFalse(set(r['calibration_seed_ids'])&set(r['holdout_seed_ids']))
  for id in r['best']['run_ids']:self.assertEqual(len(ET.parse(ROOT/f'simulation/runs/m06/trials/{id}/tripinfo.xml').getroot().findall('tripinfo')),36)
 def test_nonfinite_nested_geometry_and_objective_rejected(self):
  self.assertFalse(obs.finite_tree({'point':[0,float('nan')]}))
  for prediction in [float('nan'),float('inf')]:
   with self.assertRaises(ValueError):objective({'x':prediction},{'x':1},{'x':1},{'x':1})
 def test_queue_units_count_and_meters_are_separate(self):
  r=load(D/'synthetic-recovery.json')
  for trial in r['best']['run_ids']:
   v=load(ROOT/f'simulation/runs/m06/trials/{trial}/result.json');self.assertEqual(v['metric_units']['queue_lengths'],'m');self.assertEqual(v['metric_units']['queue_counts'],'vehicles');self.assertIn('queue_counts',v['metrics'])
 def test_parameter_bounds_and_seed_leakage(self):
  config=load(C/'recovery-experiment.json');validate_config(config)
  with self.assertRaises(ValueError):validate_config({**config,'validation_seeds':config['calibration_seeds']})
  with self.assertRaises(ValueError):validate_config({**config,'speed_factors':[9]})
 def test_sensitivity_identifiability_not_empirical_precision(self):
  u=load(D/'uncertainty.json');self.assertTrue(u['identifiable_in_fixture']);self.assertGreater(abs(u['sensitivity'][1]['metric_derivatives']['travel_times']),0);self.assertIn('no empirical CI',u['parameter_uncertainty']);self.assertEqual(u['observation_quality'],'UNKNOWN — no field observations')
 def test_railway_alignment_not_timetable(self):
  r=railway_alignment({'closure':'2026-10-01T07:00:00+07:00','road_release':'2026-10-01T07:01:00+07:00'});self.assertEqual(r['closure_duration_s'],60);self.assertFalse(r['complete']);self.assertFalse(r['schedule_is_closure'])
 def test_geometry_blocks_queue_and_spillback_claims(self):
  s=next(s for s in load(D/'structural-readiness.json') if s['id']=='CROSSING_GEOMETRY');self.assertIn('queue',s['blocked_metrics']);self.assertTrue(s['short_lanes']);self.assertEqual(s['status'],'NEEDS_FIELD_SURVEY')
 def test_event_matching_one_to_one_unmatched_and_no_field_validation(self):
  s={'location_id':'A','affected_edge':'edge','trigger':'rail','start_s':10,'end_s':30,'recovery_s':35};o={**s,'start_s':11,'uncertainty_s':1};m=match_events([s,s],[o]);self.assertEqual(len(m['matched']),1);self.assertEqual(len(m['unmatched_simulated']),1);self.assertIn('NO OBSERVED',match_events([s],[])['status']);self.assertEqual(distribution_distance([1,2],[1,2]),0)
 def test_template_csvs_have_no_observed_rows_and_workbook_exported(self):
  folder=ROOT/'data/templates/m06'
  for p in folder.glob('*.csv'):
   with p.open(encoding='utf-8') as f:self.assertEqual(len(list(csv.DictReader(f))),0)
  with zipfile.ZipFile(folder/'Gedangan_Survey_Forms.xlsx') as z:self.assertIn('xl/workbook.xml',z.namelist())
 def test_reproduction_uses_fresh_processes_and_true_resume(self):
  r=load(D/'reproducibility.json');self.assertEqual(r['fresh_search_initial_trials'],2);self.assertEqual(r['fresh_search_resumed_trials'],9);self.assertTrue(all(r['repeat_best_physics_equal'].values()));self.assertTrue(r['completed_checkpoint_idempotent'])
 def test_fixture_runs_have_no_safety_or_permission_warnings(self):
  for p in (ROOT/'simulation/runs/m06').rglob('errors.log'):self.assertFalse(any(w in p.read_text(encoding='utf-8').lower() for w in ['teleport','collision','not allowed']))
 def test_ui_data_state_truthful(self):
  p=ROOT/'frontend/public/m06';self.assertEqual(load(p/'observations.json'),[]);self.assertFalse(load(p/'baseline-2026.json')['empirical_baseline']['enabled']);text=(ROOT/'frontend/src/m06/main.tsx').read_text(encoding='utf-8');self.assertIn('NO VERIFIED 2026 OBSERVATIONS AVAILABLE',text);self.assertIn('NOT EMPIRICAL CALIBRATION',text)
if __name__=='__main__':unittest.main()
