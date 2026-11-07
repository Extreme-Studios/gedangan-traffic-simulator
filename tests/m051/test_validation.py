import unittest,math,xml.etree.ElementTree as E
from pathlib import Path
from backend.gedangan.m04_demand import ROOT,load,sha
from backend.gedangan.m051_causality import classify,analyze_trace
D=ROOT/'documentation/m051';R=ROOT/'simulation/runs/m051'
class ValidationM051Tests(unittest.TestCase):
 def test_all_preexisting_baseline_hashes_unchanged(self):
  self.assertFalse([p for p,h in load(D/'baseline-sha256.json').items() if sha(ROOT/p)!=h])
 def test_full_snapshot_archive_exists(self):
  m=load(D/'snapshot-manifest.json');self.assertEqual(m['sha256'],sha(ROOT/m['archive']));self.assertEqual(m['entries'],len(load(D/'baseline-sha256.json')))
 def test_geometry_differences_quantified_not_claimed_safe(self):
  g=load(D/'geometry.json');d=g['differences'];self.assertEqual(len([x for x in d if x['kind']=='edge' and not x['internal']]),4);self.assertEqual(len([x for x in d if x['kind']=='lane' and not x['internal']]),7);self.assertIn('NEEDS FIELD',g['status']);self.assertTrue(all(math.isfinite(x['hausdorff_m']) for x in d))
 def test_source_center_kept_at_source(self):
  g=load(D/'geometry.json');self.assertFalse(g['source_node_coordinates_changed']);self.assertLess(g['model_center_offset_m'],.01) # XML coordinate rounding, not a physical safety tolerance.
 def test_two_road_stop_lines_not_rail_stop_line(self):
  g=load(D/'geometry.json');self.assertEqual(len(g['stop_lines']),2)
  for s in g['stop_lines']:self.assertTrue(s['lane'].startswith('w1240685448'));self.assertGreater(s['distance_to_rail_centerline_m'],0);self.assertEqual(s['status'],'NEEDS FIELD VERIFICATION')
 def test_connectors_measured_and_continuous_at_xml_precision(self):
  cs=load(D/'geometry.json')['connections'];self.assertEqual(len(cs),2)
  for c in cs:self.assertLessEqual(c['incoming_gap_m'],.02);self.assertLessEqual(c['outgoing_gap_m'],.02);self.assertTrue(c['road_crosses_rail_geometrically'])
 def test_network_copy_immutable_topology_and_access(self):
  for mode in ['strict','provisional','provisional-block-control']:self.assertEqual(sha(ROOT/f'simulation/network/m051/{mode}/network.net.xml'),sha(ROOT/f'simulation/network/m05/{mode}/network.net.xml'))
 def test_actual_positive_storage_has_recovery(self):
  events=load(R/'positive_storage/causal-events.json');e=next(e for e in events if e['cause']=='VERIFIED_SPILLBACK');self.assertGreaterEqual(e['duration_s'],5);self.assertIsNotNone(e['recovery']);self.assertIn(e['recovery']['evidence'][1]['lane'],[e['downstream_lane'],e['recovery']['evidence'][0]['next_link'][1]])
  for r in e['evidence']:self.assertTrue(r['valid_source_movement']);self.assertTrue(r['next_link'][3]);self.assertFalse(r['next_link'][4]);self.assertLessEqual(r['queue_head_to_end_m'],10);self.assertLessEqual(r['queue_tail_rear_m'],5);self.assertLessEqual(r['maximum_stopped_body_gap_m'],10)
 def test_actual_negative_free_rejects_spillback(self):
  self.assertFalse(any(e['cause']=='VERIFIED_SPILLBACK' for e in load(R/'negative_free/causal-events.json')))
  for name in ['positive_storage','negative_free','negative_signal']:
   trips=E.parse(R/name/'tripinfo.xml').getroot().findall('tripinfo');self.assertEqual(len(trips),25);self.assertTrue(all(not v.get('vaporized') for v in trips));r=load(R/name/'result.json');self.assertFalse(r['collisions']);self.assertFalse(r['teleports'])
 def test_actual_negative_red_is_signal_queue(self):
  es=load(R/'negative_signal/causal-events.json');self.assertTrue(any(e['cause']=='SIGNAL_QUEUE' for e in es));self.assertFalse(any(e['cause']=='VERIFIED_SPILLBACK' for e in es))
 def test_railway_queue_has_actual_current_crossing_red(self):
  es=load(R/'C_single_seed42/causal-events.json');e=next(e for e in es if e['cause']=='RAILWAY_QUEUE');self.assertEqual(e['evidence'][0]['movement_controller'],'osm_859708050');self.assertIn(e['evidence'][0]['next_link'][5],'rRyu')
 def test_conflict_and_red_cannot_verify_storage(self):
  row={'next_link':['down','via',True,True,True,'G','s',5],'valid_source_movement':True,'queue_count':2,'entry_free_m':0,'required_entry_space_m':7};self.assertEqual(classify(row),'MULTI_CAUSAL_EVENT');row['next_link']=['down','via',False,False,False,'r','s',5];self.assertEqual(classify(row),'MULTI_CAUSAL_EVENT')
 def test_lone_vehicle_near_entry_not_full_downstream_queue(self):
  row={'next_link':['down','via',True,True,False,'G','s',5],'valid_source_movement':True,'queue_count':1,'entry_free_m':1,'required_entry_space_m':7,'is_lane_head':True,'distance_to_lane_end_m':1,'queue_tail_rear_m':1,'queue_head_to_end_m':80,'maximum_stopped_body_gap_m':0};self.assertNotEqual(classify(row),'STORAGE_BLOCKAGE_CANDIDATE')
 def test_each_gedangan_verified_event_has_all_evidence(self):
  for p in R.glob('*seed*/causal-events.json'):
   for e in load(p):
    if e['cause']!='VERIFIED_SPILLBACK':continue
    self.assertGreaterEqual(e['duration_s'],5);self.assertTrue(e['recovery']);self.assertGreaterEqual(e['recovery']['moving_at'],e['recovery']['space_available_at'])
    for r in e['evidence']:self.assertTrue(r['valid_source_movement']);self.assertTrue(r['next_link'][3]);self.assertFalse(r['next_link'][4]);self.assertLessEqual(r['queue_tail_rear_m'],5);self.assertLessEqual(r['queue_head_to_end_m'],10)
 def test_physics_and_demand_match_m05_read_only_replay(self):
  rows=load(D/'reproducibility.json')['runs'];self.assertEqual({r['run'] for r in rows},{p.parent.name for p in (ROOT/'simulation/runs/m05').glob('*/playback.json')})
  for r in rows:self.assertTrue(r['demand_equal_to_m05']);self.assertTrue(r['tripinfo_elements_equal_to_m05']);self.assertTrue(r['fcd_elements_digest_equal_to_m05'])
 def test_actual_new_run_safety(self):
  rows=load(D/'safety.json');self.assertEqual({r['run'] for r in rows},{p.parent.name for p in (ROOT/'simulation/runs/m05').glob('*/playback.json')})
  for r in rows:self.assertGreater(r['samples'],0);self.assertFalse(r['illegal_lane_samples']);self.assertFalse(r['road_crossing_closed_samples']);self.assertFalse(r['collisions']);self.assertFalse(r['teleports'])
 def test_occupancy_units_separated_from_raw_value(self):
  e=next(e for e in load(R/'positive_storage/causal-events.json') if e['cause']=='VERIFIED_SPILLBACK');r=e['evidence'][0];self.assertIn('sumo_occupancy_raw',r);self.assertGreater(r['occupancy_percent'],50);self.assertLessEqual(r['occupancy_percent'],100);self.assertIn('DERIVED',r['occupancy_method']);self.assertNotEqual(r['sumo_occupancy_raw'],r['occupancy_percent'])
 def test_deterministic_classification_from_trace(self):
  p=R/'positive_storage';analyze_trace(p);before=sha(p/'causal-events.json');analyze_trace(p);self.assertEqual(before,sha(p/'causal-events.json'))
if __name__=='__main__':unittest.main()
