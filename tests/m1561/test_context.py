import unittest,math,xml.etree.ElementTree as E
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
from backend.gedangan.m1561_common import *
class LocationContext(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.scene=load(DOC/'scene.json');cls.env=cls.scene['environment']
 def test_network_hash_frozen(self):self.assertEqual(sha(NETWORK),EXPECTED)
 def test_source_lane_junction_signal_shapes_exact(self):
  old=load(ROOT/'documentation/m156/scene.json')
  for key in ['lanes','junctions','heads','presets','crossing','bounds']:self.assertEqual(self.scene[key],old[key])
 def test_lowrise_only(self):
  b=self.env['buildings'];self.assertGreater(len(b),100);self.assertTrue(all(r['height']<=6.4 and r['height']+r['roof_height']<=8.1 for r in b));self.assertEqual({r['kind']for r in b},{'house','ruko','workshop','station'})
 def test_assumptions_not_promoted_to_fact(self):
  self.assertEqual(self.env['status'],'ASSUMED CONTEXT MODEL');self.assertTrue(all(r['status']=='ASSUMED CONTEXT MODEL'and r['source']for r in self.env['buildings']))
 def test_entire_padded_building_envelope_avoids_roads_and_rail(self):
  s=self.scene;exclude=unary_union([LineString(l['shape']).buffer(7 if l['rail']else l['width']/2+2.5)for l in s['lanes']])
  for b in self.env['buildings']:self.assertFalse(Polygon(b['footprint']).intersects(exclude),b['id'])
 def test_no_overlapping_building_envelopes(self):
  polys=[Polygon(b['footprint'])for b in self.env['buildings']]
  for i,p in enumerate(polys):self.assertFalse(any(p.intersects(q)for q in polys[i+1:]))
 def test_station_is_near_source_node_but_explicit_assumption(self):
  b=next(b for b in self.env['buildings']if b['kind']=='station');p=self.env['station']['point'];self.assertLess(math.hypot(b['x']-p[0],b['y']-p[1]),55);self.assertIn('no footprint survey',b['source'])
 def test_source_photo_hash(self):
  r=load(DOC/'source-register.json')['sources'][0];self.assertEqual(sha(ROOT/r['local_file']),r['sha256']);self.assertEqual(r['license'],'CC-BY-SA4.0')
 def test_parent_results_unchanged(self):
  for r in load(ROOT/'documentation/m156/baseline-run-references.json'):self.assertEqual(sha(PARENT_RUNS/r['run_id']/'result.json'),r['result_sha256'])
 def test_no_new_traffic_topology(self):
  a=E.parse(NETWORK).getroot();b=E.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();self.assertEqual(E.tostring(a),E.tostring(b))
if __name__=='__main__':unittest.main()
