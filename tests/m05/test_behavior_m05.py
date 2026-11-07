"""Validate retained actual SUMO phenomena and immutable source, not success flags."""
import unittest,xml.etree.ElementTree as ET
from pathlib import Path
from backend.gedangan.m04_demand import ROOT,load,sha,activate
from backend.gedangan.m045_access import external_connections
from backend.gedangan.m05_queues import observe,spillback_candidate
D=ROOT/'documentation/m05';N=ROOT/'simulation/network/m05';R=ROOT/'simulation/runs/m05'
class BehaviorM05Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  activate();cls.results=load(D/'scenario-results.json');cls.byname={r['name']:r for r in cls.results};cls.pilot=ET.parse(N/'provisional/network.net.xml').getroot();cls.single=load(R/'C_single_seed42/playback.json');cls.signals=load(R/'B_signal_seed42/playback.json')
 def test_previous_milestones_immutable(self):
  self.assertFalse([p for p,h in load(D/'previous-milestones-sha256.json').items() if sha(ROOT/p)!=h])
 def test_road_movements_and_permissions_identical(self):
  for mode in ['strict','provisional']:
   before=external_connections(ET.parse(ROOT/f'simulation/network/m045/{mode}/network.net.xml').getroot());after={k:v for k,v in external_connections(ET.parse(N/mode/'network.net.xml').getroot()).items() if not k[0].startswith('m05_rail_')};self.assertEqual(set(before),set(after))
   for k in before:
    for key in ['allow','disallow']:self.assertEqual(before[k].get(key),after[k].get(key))
 def test_left_hand_and_no_access_bypass(self):
  self.assertEqual(self.pilot.get('lefthand'),'true')
  for p in R.glob('*/demand.rou.xml'):
   for v in ET.parse(p).getroot().findall('vType'):self.assertNotEqual(v.get('vClass'),'ignoring');self.assertNotEqual(v.get('id'),'oversize')
 def test_actual_multiclass_motion_and_arrival(self):
  per=self.byname['A_free_seed42']['per_type'];self.assertEqual(len(per),9)
  for v in per.values():self.assertEqual(v['requested'],v['arrived']);self.assertEqual(v['departed'],v['moved'])
 def test_actual_routes_respect_class_permissions(self):
  import sumolib
  net=sumolib.net.readNet(str(N/'provisional/network.net.xml'),withInternal=True);types={v['id']:v['sumo_vclass'] for v in load(ROOT/'configuration/demand-m04/vehicle-registry.json')['vehicles']}
  for v in load(R/'A_free_seed42/demand.json')['vehicles']:
   cls=types[v['type']]
   for eid in v['edges']:self.assertTrue(net.getEdge(eid).allows(cls),(v['id'],eid,cls))
   for a,b in zip(v['edges'],v['edges'][1:]):self.assertTrue(any(c.allows(cls) for c in net.getEdge(a).getConnections(net.getEdge(b))),(a,b,cls))
 def test_sublane_actual_geometry_and_clearance(self):
  a,b=load(D/'sublane-results.json');self.assertEqual(a['arrived'],6);self.assertEqual(b['arrived'],6);self.assertFalse(a['overlap_observations'])
  pairs={tuple(p['pair']) for p in b['overlap_observations']};self.assertIn(('motor_a','motor_b'),pairs);self.assertIn(('car_a','motor_car'),pairs);self.assertNotIn(('truck','motor_truck'),pairs)
  self.assertGreaterEqual(min(p['lateral_body_gap_m'] for p in b['overlap_observations']),.25);self.assertGreater(max(b['lateral_span_m'].values()),0)
 def test_signal_link_indices_and_protected_green(self):
  tl=next(x for x in self.pilot.findall('tlLogic') if x.get('id')=='m05_gedangan');links=[c for c in self.pilot.findall('connection') if c.get('tl')=='m05_gedangan'];indices={int(c.get('linkIndex')) for c in links};count=max(indices)+1;self.assertEqual(indices,set(range(count)));greens=set()
  for p in tl.findall('phase'):
   state=p.get('state');self.assertEqual(len(state),count);self.assertLessEqual(state.count('G'),1);greens.update(i for i,s in enumerate(state) if s=='G')
  self.assertEqual(greens,indices);self.assertTrue(any(set(p.get('state'))=={'r'} for p in tl.findall('phase')))
 def test_actual_signal_transition_stop_release(self):
  states={e['state'] for e in self.signals['events'] if e['controller']=='m05_gedangan'};self.assertGreater(len(states),10)
  evidence=self.byname['B_signal_seed42']['signal_stopped_then_released'];self.assertGreater(len(evidence),10)
  for e in evidence:self.assertGreater(e['green_release_time'],e['red_stop']['time'])
 def test_rail_source_chain_main_not_siding(self):
  p=load(N/'provisional/rail-provenance.json');self.assertEqual([f['properties']['osm_id'] for f in p['source_features']],[1330582009,562358494,1330582010]);self.assertTrue(all(f['properties']['tags']['usage']=='main' for f in p['source_features']));self.assertIn(859708050,p['source_node_chain']);self.assertNotIn(1268453702,[f['properties']['osm_id'] for f in p['source_features']])
 def test_train_and_road_lane_separation(self):
  for f in self.single['frames']:
   for v in f['vehicles']:
    if v['type']=='m05_train':self.assertTrue(v['lane'].startswith(('m05_rail_',':osm_')));self.assertFalse(v['lane'].startswith('w'))
    else:self.assertFalse(v['lane'].startswith('m05_rail_'))
 def test_actual_train_crossing_and_road_stop_release(self):
  r=self.byname['C_single_seed42'];e=r['rail_event_evidence'][0];self.assertLess(e['approach_120m'],e['front_entry']);self.assertLess(e['front_entry'],e['rear_exit']);self.assertGreater(r['rail_gate_stop_vehicle_seconds'],0);self.assertTrue(r['gate_stopped_then_released']);self.assertFalse(r['road_inside_crossing_while_red_samples'])
  states=[e['state'] for e in self.single['events'] if e['controller']=='osm_859708050'];self.assertEqual(states,['GG','yy','rr','uu','GG'])
 def test_consecutive_train_no_unsafe_road_reopening(self):
  d=load(R/'H_close_block_control/playback.json');states=[e for e in d['events'] if e['controller']=='osm_859708050'];reds=[e['time'] for e in states if e['state']=='rr'];self.assertEqual(len(reds),2);self.assertFalse(any(e['state']=='GG' and reds[0]<e['time']<reds[1] for e in states));self.assertEqual(d['result']['arrived'],116);self.assertFalse(d['result']['teleports']);self.assertFalse(d['result']['collisions'])
 def test_queue_metrics_actual_fcd(self):
  frame=max(self.single['frames'],key=lambda f:sum(q['count'] for q in f['queues'].values()));expected=observe(frame['vehicles'],{})
  self.assertEqual(sum(q['count'] for q in frame['queues'].values()),sum(q['count'] for q in expected.values()));self.assertGreater(sum(q['count'] for q in expected.values()),0)
 def test_e2_real_output_and_occupancy(self):
  samples=ET.parse(R/'G_e2_instrumented/e2.xml').getroot().findall('interval');self.assertEqual(len(samples),1800);self.assertGreater(max(float(x.get('maxJamLengthInVehicles')) for x in samples),0);self.assertGreater(max(float(x.get('maxOccupancy')) for x in samples),0)
 def test_actual_isolated_spillback_positive_control(self):
  r=load(R/'spillback-fixture/result.json');self.assertIsNotNone(r['first_detection_s']);self.assertEqual(r['arrived'],25);o=[x for x in r['observations'] if x['detected']];self.assertTrue(o)
  for x in o:self.assertLess(x['tail_m'],5);self.assertTrue(x['upstream_green']);self.assertTrue(x['upstream_stopped']);self.assertGreaterEqual(x['continuous_blocked_s'],5)
 def test_long_queue_alone_is_not_spillback(self):
  self.assertFalse(spillback_candidate({'tail_position':2},False,True,20));self.assertFalse(spillback_candidate({'tail_position':2},True,False,20));self.assertFalse(spillback_candidate({'tail_position':2},True,True,4.9))
 def test_trip_accounting_and_no_unexplained_teleport(self):
  for r in self.results:
   self.assertEqual(r['requested_road']+r['requested_train'],r['arrived']+len(r['running'])+r['not_departed']);self.assertEqual(r['loaded'],r['requested_road']+r['requested_train']);self.assertFalse(r['teleports']);self.assertFalse(r['collisions'])
 def test_paired_experiments_identical_inputs(self):
  p=load(D/'paired-comparisons.json');self.assertEqual(len(p),14);self.assertTrue(all(x['identical_demand'] and x['identical_network'] for x in p))
 def test_fcd_playback_positions_consistent(self):
  root=ET.parse(R/'C_single_seed42/fcd.xml').getroot();frame=self.single['frames'][108];step=next(t for t in root if abs(float(t.get('time'))-(frame['time']-.5))<1e-6);actual={v.get('id'):v for v in step}
  for v in frame['vehicles']:
   self.assertIn(v['id'],actual);self.assertAlmostEqual(v['x'],float(actual[v['id']].get('x')),delta=.02);self.assertAlmostEqual(v['speed'],float(actual[v['id']].get('speed')),delta=.02)
 def test_deterministic_rebuild_and_repeat(self):
  r=load(D/'reproducibility.json');self.assertEqual(r['network_before'],r['network_after'])
  for p,h in r['network_after'].items():self.assertEqual(sha(ROOT/p),h)
  a=R/'C_single_seed42';b=R/'I_repro_single_seed42';self.assertEqual(sha(a/'demand.json'),sha(b/'demand.json'))
  for f in ['tripinfo.xml','summary.xml','fcd.xml']:self.assertEqual(ET.tostring(ET.parse(a/f).getroot()),ET.tostring(ET.parse(b/f).getroot()))
 def test_all_half_second_samples_obey_lane_access(self):
  audits=load(D/'safety-audits.json');self.assertEqual(len(audits),len(self.results))
  for a in audits:self.assertGreater(a['samples_checked'],0);self.assertFalse(a['illegal_lane_samples']);self.assertFalse(a['road_internal_crossing_samples_during_closed_red'])
 def test_source_positions_nodes_retained(self):
  for mode in ['strict','provisional']:
   before=ET.parse(ROOT/f'simulation/network/m045/{mode}/network.net.xml').getroot();after={j.get('id'):j for j in ET.parse(N/mode/'network.net.xml').getroot().findall('junction')}
   for j in before.findall('junction'):
    if j.get('id').startswith(':'):continue
    for key in ['x','y']:self.assertEqual(j.get(key),after[j.get('id')].get(key))
if __name__=='__main__':unittest.main()
