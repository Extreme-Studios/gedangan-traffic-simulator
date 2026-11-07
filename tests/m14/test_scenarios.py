import unittest,copy,json,urllib.request,urllib.error,xml.etree.ElementTree as E
from backend.gedangan.m14_common import *
from backend.gedangan.m14_demand import default,generate
from backend.gedangan.m14_network import catalog,route
from backend.gedangan.m14_vehicles import registry

class Scenarios(unittest.TestCase):
 def test_manual_exact_all_ten(self):
  r=default();r['mode']='manual';r['counts']={v['id']:i+1 for i,v in enumerate(registry())};d=generate(r);self.assertEqual(d['total'],55);self.assertEqual(d['composition'],r['counts']);self.assertEqual(len(d['requests']),55)
 def test_random_exact_rounding_and_ids(self):
  for n in [1,7,499,500,1000,2998,3000,5000]:
   r=default();r['total']=n;d=generate(r);self.assertEqual(len(d['requests']),n);self.assertEqual(sum(d['composition'].values()),n);self.assertEqual(len({v['id']for v in d['requests']}),n);self.assertEqual(sum(b['count']for b in d['departure_histogram']),n)
 def test_reproducible_and_new_seed(self):
  a=default();b=copy.deepcopy(a);self.assertEqual(generate(a),generate(b));b['seed']=43;self.assertNotEqual(generate(a)['cohort_sha256'],generate(b)['cohort_sha256']);self.assertNotEqual(generate(a)['composition'],generate(b)['composition'])
 def test_exact_approach_and_turn(self):
  r=default();r['total']=101;r['approach_mode']='exact';r['approaches']={k:101 if k=='southbound'else 0 for k in r['approaches']};r['turns']['southbound']={'straight':55,'left':45,'right':0,'uturn':0};d=generate(r);self.assertEqual(d['approach_allocation']['southbound'],101);self.assertEqual(d['turn_allocation']['southbound']['left'],45)
 def test_blocked_turn_retained_no_substitution(self):
  r=default();r['total']=10;r['approaches']={k:100 if k=='northbound'else 0 for k in r['approaches']};r['turns']['northbound']={'straight':0,'left':0,'right':100,'uturn':0};d=generate(r);self.assertEqual(d['failed_routes'],10);self.assertTrue(all(q['turn']=='right'and not q['edges']for q in d['requests']))
 def test_slow_classes_denied(self):
  for k in ['becak_nonmotor','bicycle']:
   for a in catalog()['approaches']:self.assertEqual(route(k,a['id'],'straight')['route_status'],'UNROUTABLE')
 def test_actual_routes_and_connections(self):
  root=E.parse(NETWORK).getroot();cs={(c.get('from'),c.get('to'))for c in root.findall('connection')}
  for v in registry():
   for a in catalog()['approaches']:
    for turn in a['movements']:
     r=route(v['id'],a['id'],turn)
     if r['edges']:
      self.assertTrue(all((x,y)in cs for x,y in zip(r['edges'],r['edges'][1:])));self.assertIn((r['mandatory_turn_from'],r['mandatory_turn_to']),list(zip(r['edges'],r['edges'][1:])))
 def test_temporal_modes_and_horizons(self):
  for h in [900,1800,3600,5400,7200,1234]:
   for mode in ['uniform','peak','custom']:
    r=default();r['total']=73;r['duration_s']=h;r['temporal']['mode']=mode;b=(h+299)//300;r['temporal']['weights']=[100/b]*b;d=generate(r);times=[q['depart_seconds']for q in d['requests']];self.assertTrue(all(0<t<h for t in times));self.assertGreater(len(set(times)),1);self.assertEqual(sum(x['count']for x in d['departure_histogram']),73)
 def test_invalid_inputs_rejected(self):
  mutations=[lambda r:r.update(total=-1),lambda r:r.update(seed=1.5),lambda r:r['weights'].update(car=21),lambda r:r['approaches'].update(frontage=50),lambda r:r['turns']['northbound'].update(left=10),lambda r:r.update(date='2026-02-30')]
  for fn in mutations:
   r=default();fn(r)
   with self.assertRaises((ValueError,KeyError)):generate(r)
 def test_network_unchanged_and_no_flyover(self):
  self.assertEqual(sha(NETWORK),'0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c');self.assertFalse(any(e.get('id','').startswith('recovery_fo_')for e in E.parse(NETWORK).getroot().findall('edge')))
 def test_actual_benchmark_lifecycle(self):
  rs=load(DOC/'sumo-benchmarks.json');self.assertEqual([r['requested']for r in rs],[500,1000,3000,5000])
  for r in rs:
   self.assertIn('1.28.0',r['sumo_version'][1]);self.assertEqual(r['requested'],r['routed']+r['failed_routes']);self.assertEqual(r['routed'],r['departed']+r['not_departed']);self.assertEqual(r['departed'],r['arrived']+r['active']);self.assertFalse(r['illegal_permissions']);self.assertFalse(r['teleports']);self.assertFalse(r['collisions']);self.assertGreater(r['moved'],0)
 def test_save_reload_api(self):
  r=default();r['name']='M14 automated save/load evidence';req=urllib.request.Request('http://127.0.0.1:5199/api/scenarios',data=json.dumps(r).encode(),headers={'Content-Type':'application/json'});saved=json.load(urllib.request.urlopen(req));items=json.load(urllib.request.urlopen('http://127.0.0.1:5199/api/scenarios'));self.assertIn(saved,items);self.assertEqual(generate(saved['request'])['cohort_sha256'],generate(r)['cohort_sha256'])
 def test_origin_denied(self):
  r=urllib.request.Request('http://127.0.0.1:5199/api/catalog',headers={'Origin':'https://example.invalid'})
  with self.assertRaises(urllib.error.HTTPError)as cm:urllib.request.urlopen(r)
  self.assertEqual(cm.exception.code,403)
if __name__=='__main__':unittest.main()
