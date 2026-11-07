import unittest,copy,xml.etree.ElementTree as E,json,urllib.request,urllib.error,collections,gzip
from backend.gedangan.m15_common import *
from backend.gedangan.m15_demand import default,generate,volume
from backend.gedangan.m15_network import catalog,route
from backend.gedangan.m14_vehicles import registry
class Validation(unittest.TestCase):
 def test_hourly_and_total_are_distinct(self):
  r=default();r['duration_s']=900;self.assertEqual(generate(r)['total'],750);r['volume_interpretation']='total';self.assertEqual(generate(r)['total'],3000);self.assertEqual(volume(r)['equivalent_hourly_demand'],12000)
 def test_full_hour_conserves_3000(self):
  r=default();d=generate(r);self.assertEqual(d['total'],3000);self.assertEqual(d['volume']['equivalent_hourly_demand'],3000);self.assertEqual(sum(d['composition'].values()),3000);self.assertEqual(sum(d['approach_allocation'].values()),3000)
 def test_fractional_rate_conversion_explicit(self):
  r=default();r.update(total=7,duration_s=900,warmup_s=0);v=volume(r);self.assertEqual(v['unrounded_requests'],1.75);self.assertEqual(v['requested_physical'],2)
 def test_manual_class_hourly_rounding_conserved(self):
  r=default();r.update(mode='manual',counts={v['id']:3 for v in registry()},duration_s=900);d=generate(r);self.assertEqual(d['total'],8);self.assertEqual(sum(d['composition'].values()),8)
 def test_runnable_defaults_supported_not_relabelled(self):
  r=default();d=generate(r);self.assertEqual(d['failed_routes'],0);self.assertEqual(r['weights']['bicycle'],0);self.assertEqual(r['weights']['becak_nonmotor'],0)
 def test_custom_unsupported_counts_retained(self):
  r=default();r['weights']={k:100 if k=='bicycle'else 0 for k in r['weights']};r['total']=23;d=generate(r);self.assertEqual(d['total'],23);self.assertEqual(d['failed_routes'],23);self.assertEqual(d['composition']['bicycle'],23)
 def test_seed_identity_and_variation(self):
  r=default();self.assertEqual(generate(r),generate(copy.deepcopy(r)));b=copy.deepcopy(r);b['seed']+=1;self.assertNotEqual(generate(r)['cohort_sha256'],generate(b)['cohort_sha256'])
 def test_legal_macro_turns_existing_not_new(self):
  c=catalog();aa={a['id']:a for a in c['approaches']};self.assertTrue(aa['ketajen']['movements']['right']['available']);self.assertTrue(aa['sukodono']['movements']['left']['available']);self.assertFalse(aa['northbound']['movements']['right']['available']);self.assertFalse(any(a['movements']['uturn']['available']for a in c['approaches']));self.assertEqual(route('car','northbound','right')['route_status'],'UNROUTABLE')
 def test_each_candidate_follows_actual_connections(self):
  cs={(q.get('from'),q.get('to'))for q in E.parse(NETWORK).getroot().findall('connection')}
  for a in catalog()['approaches']:
   for turn,m in a['movements'].items():
    for c in m['candidates']:
     edges=c['prefix']+c['suffix'];self.assertTrue(all((x,y)in cs for x,y in zip(edges,edges[1:])))
 def test_each_routable_class_passes_lane_connections(self):
  from backend.gedangan.recovery_routing import graph
  for v in registry():
   if not v['source_type_id']:continue
   adj,legal,_=graph(str(NETWORK.resolve()),sha(NETWORK),v['source_type_id'])
   for a in catalog()['approaches']:
    for t in a['movements']:
     r=route(v['id'],a['id'],t)
     if r['edges']:self.assertTrue(all(e in legal for e in r['edges']));self.assertTrue(all(b in adj.get(x,{})for x,b in zip(r['edges'],r['edges'][1:])))
 def test_warmup_is_exclusion_not_hidden_extra(self):
  r=default();d=generate(r);self.assertEqual(d['warmup']['analysis_start_s'],300);self.assertEqual(d['warmup']['extra_vehicles'],0);self.assertEqual(len(d['requests']),3000);r['warmup_s']=3600
  with self.assertRaises(ValueError):generate(r)
 def test_actual_legal_turns_loaded_moved_arrived(self):
  r=load(DOC/'actual-turns.json');qs=load(RUNS/r['run_id']/'vehicle-results.json');self.assertEqual(r['requested'],120);self.assertEqual(r['routed'],120);self.assertEqual(r['departed'],120);self.assertEqual(r['moved'],120)
  for a in catalog()['approaches']:
   for t,m in a['movements'].items():
    if m['available']:self.assertTrue(any(q['approach']==a['id']and q['turn']==t and q['arrived']for q in qs))
 def test_geometry_stays_partial_and_renderer_aligned(self):
  a=load(DOC/'geometry-audit.json');self.assertEqual(a['status'],'PARTIAL');self.assertEqual(a['renderer_lane_shape_error_m'],0);self.assertEqual(a['new_edges'],0);self.assertEqual(a['new_connections'],0);self.assertTrue(any(x['status'].startswith('UNVERIFIED')for x in a['named_corridors']))
 def test_no_baseline_mutation_or_flyover(self):
  self.assertEqual(sha(NETWORK),'0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c');self.assertFalse(any(e.get('id','').startswith('recovery_fo_')for e in E.parse(NETWORK).getroot().findall('edge')))
 def test_one_hour_actual_lifecycle(self):
  results=load(DOC/'one-hour-results.json');self.assertEqual([r['requested']for r in results],[500,1000,3000,5000])
  for r in results:
   self.assertEqual(r['request']['duration_s'],3600);self.assertEqual(r['requested'],r['routed']+r['failed_routes']);self.assertEqual(r['routed'],r['departed']+r['not_departed']);self.assertEqual(r['departed'],r['arrived']+r['active']);self.assertFalse(r['teleports']);self.assertFalse(r['illegal_permissions']);self.assertFalse(r['collisions']);self.assertGreater(r['moved'],0)
 def test_per_approach_reconciles_all_counts(self):
  for r in load(DOC/'one-hour-results.json'):
   for field,total in [('input','requested'),('entering','departed'),('exiting','arrived'),('pending','not_departed'),('failed','failed_routes'),('routed','routed')]:self.assertEqual(sum(a[field]for a in r['analysis']['approaches']),r[total])
 def test_pending_diagnostics_have_observed_gaps(self):
  r=load(DOC/'one-hour-results.json')[-1];samples=load(RUNS/r['run_id']/'insertion-samples.json');self.assertGreater(r['not_departed'],0);self.assertTrue(samples);self.assertTrue(all('nominal_required_m'in g and'class_allowed'in g and'observed_entry_free_m'in g for s in samples for g in s['lane_evidence']));self.assertTrue(any('UNRESOLVED'in s['reason']or'SHORTAGE'in s['reason']for s in samples))
 def test_controls_apply_not_just_ui(self):
  pairs=load(DOC/'signal-sensitivity.json');a,b=pairs.values();self.assertNotEqual(a['signal_transitions'],b['signal_transitions']);self.assertNotEqual(a['departed_mean_waiting_s'],b['departed_mean_waiting_s']);self.assertEqual(load(RUNS/a['run_id']/'demand.json')['cohort_sha256'],load(RUNS/b['run_id']/'demand.json')['cohort_sha256'])
 def test_railway_affects_wait(self):
  p=load(DOC/'rail-sensitivity.json');a,b=p.values();self.assertGreater(a['departed_mean_waiting_s'],b['departed_mean_waiting_s']);self.assertEqual(load(RUNS/a['run_id']/'demand.json')['cohort_sha256'],load(RUNS/b['run_id']/'demand.json')['cohort_sha256'])
 def test_api_scenario_roundtrip_and_security(self):
  r=default();r['name']='M15 test save/load';q=urllib.request.Request('http://127.0.0.1:5200/api/scenarios',data=json.dumps(r).encode(),headers={'Content-Type':'application/json'});saved=json.load(urllib.request.urlopen(q));self.assertEqual(saved['generated']['total'],3000);self.assertIn(saved,json.load(urllib.request.urlopen('http://127.0.0.1:5200/api/scenarios')))
  q=urllib.request.Request('http://127.0.0.1:5200/api/catalog',headers={'Origin':'https://example.invalid'})
  with self.assertRaises(urllib.error.HTTPError)as cm:urllib.request.urlopen(q)
  self.assertEqual(cm.exception.code,403)
 def test_rejected_custom_preview_explains_without_substitution(self):
  r=default();r['total']=10;r['weights']={k:100 if k=='bicycle'else 0 for k in r['weights']};q=urllib.request.Request('http://127.0.0.1:5200/api/preview',data=json.dumps(r).encode(),headers={'Content-Type':'application/json'});d=json.load(urllib.request.urlopen(q));self.assertEqual(d['composition']['bicycle'],10);self.assertEqual(d['failed_routes'],10);self.assertEqual(sum(s['count']for s in d['failure_summary']),10);self.assertTrue(all(s['reason']=='NO_BICYCLE_LANE_PERMISSION'for s in d['failure_summary']))
if __name__=='__main__':unittest.main()
