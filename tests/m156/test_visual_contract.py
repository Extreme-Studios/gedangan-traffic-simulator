import unittest,copy,json,urllib.request,xml.etree.ElementTree as E
from backend.gedangan.m156_common import *
from backend.gedangan.m155_demand import default,generate
from backend.gedangan.m15_demand import generate as parent_generate
class Contract(unittest.TestCase):
 def test_network_byte_frozen(self):self.assertEqual(sha(NETWORK),EXPECTED)
 def test_source_scene_geometries_exact(self):
  from backend.gedangan.m09_export import scene
  a=load(DOC/'scene.json');b=scene(NETWORK);self.assertEqual(a['lanes'],b['lanes']);self.assertEqual(a['junctions'],b['junctions']);self.assertEqual(a['heads'],b['heads'])
 def test_no_new_flyover_edges_or_connections(self):
  a=E.parse(NETWORK).getroot();b=E.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();self.assertEqual(E.tostring(a),E.tostring(b));self.assertFalse(any('flyover'in e.get('id','').lower()for e in a.findall('edge')))
 def test_registry_geometry_envelopes_ground_and_distinction(self):
  a=load(DOC/'vehicle-asset-audit.json');self.assertEqual(a['classes'],10);self.assertEqual(a['distinct_geometry_hashes'],10)
  for r in a['results']:
   self.assertAlmostEqual(r['minimum_y'],0)
   for x,y in zip(r['dimensions_sumo_lwh'],r['rendered_lwh']):self.assertAlmostEqual(x,y,places=5)
 def test_demand_cohort_unchanged(self):
  r=default();r.update(total=100);self.assertEqual(generate(r)['requests'],parent_generate(copy.deepcopy(r))['requests'])
 def test_train_coaches_keep_full_scale(self):
  r=load(DOC/'train-asset-audit.json');self.assertEqual(r['status'],'PASS');self.assertEqual(r['coaches'],8);self.assertTrue(all(9<=v<=10.1 for v in r['coach_local_lengths']))
 def test_custom_rejected_class_not_substituted(self):
  r=default();r.update(total=10,weights={k:100 if k=='bicycle'else 0 for k in r['weights']});d=generate(r);self.assertEqual(d['failed_routes'],10);self.assertTrue(all(q['vehicle_type_id']=='bicycle'for q in d['requests']))
 def test_actual_sumo_counts_equal_parent_with_same_cohort(self):
  d=load(DOC/'traffic-equivalence.json');self.assertEqual(d['status'],'PASS');self.assertTrue(d['exact_full_request_cohort_equal']);self.assertEqual(d['actual_counts_equal']['arrived'],93);self.assertEqual(d['actual_counts_equal']['not_departed'],0)
 def test_actual_xml_fcd_audit_pass(self):
  d=load(DOC/'traffic-equivalence.json');a=load(DOC/'xml-audits'/(d['new_run']+'.json'));self.assertEqual(a['status'],'PASS');self.assertTrue(all(a['checks'].values()))
 def test_retained_run_result_hashes_unchanged(self):
  for r in load(DOC/'baseline-run-references.json'):self.assertEqual(sha(PARENT_RUNS/r['run_id']/'result.json'),r['result_sha256']);self.assertEqual(sha(PARENT_RUNS/r['run_id']/'output-manifest.json'),r['output_manifest_sha256'])
 def test_api_parent_and_new_recordings_accessible_separately(self):
  rows=json.load(urllib.request.urlopen('http://127.0.0.1:5202/api/runs'));ids={r['run_id']for r in rows};self.assertIn('cc419452a995456df324fd05',ids);self.assertIn(load(DOC/'traffic-equivalence.json')['new_run'],ids)
 def test_api_manual_save_load_keeps_totals(self):
  r=default();r.update(name='M15.6 backend manual regression',mode='manual',counts={k:2 for k in r['counts']});q=urllib.request.Request('http://127.0.0.1:5202/api/scenarios',data=json.dumps(r).encode(),headers={'Content-Type':'application/json'});s=json.load(urllib.request.urlopen(q));self.assertEqual(s['generated']['total'],20);self.assertEqual(s['request'],r);self.assertIn(s,json.load(urllib.request.urlopen('http://127.0.0.1:5202/api/scenarios')))
if __name__=='__main__':unittest.main()
