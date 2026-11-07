import unittest,copy,xml.etree.ElementTree as E,json,urllib.request
from backend.gedangan.m155_common import *
from backend.gedangan.m155_demand import default,generate
from backend.gedangan.m155_network import catalog,route
class Reality(unittest.TestCase):
 def test_versioned_network_frozen_no_geometry_bypass(self):
  self.assertEqual(sha(NETWORK),sha(PARENT));d=load(DOC/'network-topology-diff.json');self.assertTrue(all(v==0 for v in d['topology_diff'].values()));self.assertEqual(d['lane_count_diff'],0)
 def test_no_flyover_or_invented_edges(self):
  r=E.parse(NETWORK).getroot();self.assertFalse(any(e.get('id','').startswith('recovery_fo_')for e in r.findall('edge')));self.assertEqual(len(r.findall('edge')),len(E.parse(PARENT).getroot().findall('edge')))
 def test_all_roads_have_provenance_coordinates_and_connections(self):
  inv=load(DOC/'road-inventory.json');self.assertEqual(len(inv),1961)
  for e in inv:self.assertTrue(e['source_way_id']);self.assertTrue(e['geographic_coordinates']);self.assertTrue(e['lanes']);self.assertIn(e['source_status'],['VERIFIED FROM SOURCE','UNKNOWN / REQUIRES FIELD CHECK']);self.assertEqual(e['physical_rule_status'],'PROVISIONAL')
 def test_government_reference_retained_with_rights_and_hash(self):
  refs=load(DOC/'source-register.json');geo=next(r for r in refs if r['id']=='S-GOV-GEO');self.assertEqual(geo['status'],'RETRIEVED');self.assertEqual(geo['sha256'],sha(ROOT/geo['local_file']));self.assertGreater(len(load(DOC/'technical-map.json')['government']),0)
 def test_facts_partial_not_field_certification(self):
  d=load(DOC/'network-reality-audit.json');self.assertEqual(d['source_status'],'PARTIAL');self.assertEqual(d['physical_calibration_verified_edges'],0);self.assertEqual(d['visual_quality'].split(';')[0],'PENDING');self.assertGreater(d['frontage_m15_anchor_distance_from_crossing_m'],1000);self.assertTrue(d['overlapping_approach_route_edges'])
 def test_same_seed_and_demand_reproducible(self):
  r=default();self.assertEqual(generate(r),generate(copy.deepcopy(r)));r['seed']=43;self.assertNotEqual(generate(r)['cohort_sha256'],generate(default())['cohort_sha256'])
 def test_rate_and_total_conversion_remain_explicit(self):
  r=default();r.update(duration_s=900,execution_horizon_s=900);d=generate(r);self.assertEqual(d['total'],750);r['volume_interpretation']='total';d=generate(r);self.assertEqual(d['total'],3000);self.assertEqual(d['volume']['equivalent_hourly_demand'],12000)
 def test_long_execution_does_not_repeat_demand(self):
  r=default();a=generate(r);r['execution_horizon_s']=7200;b=generate(r);self.assertEqual(a['requests'],b['requests']);self.assertEqual(b['total'],3000);self.assertTrue(all(q['depart_seconds']<3600 for q in b['requests']))
 def test_custom_unsupported_classes_not_substituted(self):
  r=default();r.update(total=50);r['weights']={k:100 if k=='bicycle'else 0 for k in r['weights']};d=generate(r);self.assertEqual(d['total'],50);self.assertEqual(d['failed_routes'],50);self.assertTrue(all(q['vehicle_type_id']=='bicycle'for q in d['requests']))
 def test_manual_all_classes_and_exact_allocation_preserved(self):
  r=default();r.update(mode='manual',counts={k:3 for k in r['counts']},volume_interpretation='total',approach_mode='exact',approaches={k:30 if k=='northbound'else 0 for k in r['approaches']});d=generate(r);self.assertEqual(d['total'],30);self.assertEqual(len(set(q['vehicle_type_id']for q in d['requests'])),10);self.assertEqual(d['approach_allocation']['northbound'],30)
 def test_all_offered_routes_follow_existing_connections(self):
  cs={(c.get('from'),c.get('to'))for c in E.parse(NETWORK).getroot().findall('connection')}
  for a in catalog()['approaches']:
   for t,m in a['movements'].items():
    r=route('car',a['id'],t)
    if r['edges']:self.assertTrue(all((x,y)in cs for x,y in zip(r['edges'],r['edges'][1:])))
 def test_real_four_load_levels_accounting(self):
  rr=load(DOC/'one-hour-results.json');self.assertEqual([r['requested']for r in rr],[500,1000,3000,5000])
  for r in rr:self.assertEqual(r['requested'],r['routed']+r['failed_routes']);self.assertEqual(r['routed'],r['departed']+r['not_departed']);self.assertEqual(r['departed'],r['arrived']+r['active']);self.assertFalse(r['teleports']);self.assertFalse(r['collisions']);self.assertFalse(r['illegal_permissions'])
 def test_m15_first_hour_reproduced_on_final_network(self):
  r=load(DOC/'cases/baseline-3000.json');self.assertEqual([r[k]for k in ['requested','routed','departed','arrived','active','not_departed']],[3000,3000,1914,1346,568,1086]);self.assertEqual(r['network_sha256'],sha(NETWORK))
 def test_controlled_pairs_keep_full_cohort_not_just_seed(self):
  rows=load(DOC/'controlled-comparisons.json')['comparisons'];self.assertEqual(len(rows),4);self.assertTrue(all(r['same_full_request_class_route_departure_cohort']for r in rows));self.assertEqual(len({r['cohort_sha256']for r in rows}),1);self.assertEqual(rows[0]['first_hour'],rows[1]['first_hour']);self.assertTrue(rows[1]['discharge_time_censored']);self.assertEqual(rows[1]['end']['not_departed'],454)
 def test_pending_percent_denominator_unique_not_samples(self):
  r=load(DOC/'cases/baseline-3000.json');d=load(DOC/'rootcause'/(r['run_id']+'.json'));self.assertEqual(d['denominator_unique_pending_ids'],1086);self.assertEqual(len({q['id']for q in d['ids']}),1086);self.assertAlmostEqual(sum(q['percent_of_unique_pending']for q in d['evidence_coverage']),100);self.assertEqual(d['pending_on_origin_edges_under5m'],0);self.assertIn('UNRESOLVED',d['full_causal_assignment'])
 def test_rail_actual_track_and_steady_red_entry(self):
  r=load(DOC/'cases/baseline-3000.json');a=load(DOC/'rail-audits'/(r['run_id']+'.json'));self.assertFalse(a['train_lane_geometry_offset_above_0_03m']);self.assertFalse(a['steady_red_first_entry_samples']);self.assertGreater(len(a['train_front_crossing_sample_intervals']),0);self.assertGreater(a['closed_crossing_stopped_road_samples'],0)
 def test_scenario_save_and_reload(self):
  r=default();r['name']='M15.5 scenario roundtrip test';q=urllib.request.Request('http://127.0.0.1:5201/api/scenarios',data=json.dumps(r).encode(),headers={'Content-Type':'application/json'});saved=json.load(urllib.request.urlopen(q));self.assertEqual(saved['generated']['total'],3000);self.assertIn(saved,json.load(urllib.request.urlopen('http://127.0.0.1:5201/api/scenarios')))
if __name__=='__main__':unittest.main()
