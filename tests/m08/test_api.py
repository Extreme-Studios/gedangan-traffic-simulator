import unittest,threading,urllib.request,urllib.error,json,gzip
import tempfile
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from backend.gedangan import m08_server as server
class SolutionHTTPTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start();cls.url=f'http://127.0.0.1:{cls.http.server_port}/api/m08/'
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.thread.join()
 def request(self,path,body=None,headers=None):
  req=urllib.request.Request(self.url+path,data=json.dumps(body).encode() if body else None,headers={'Host':'127.0.0.1:8773','Accept-Encoding':'gzip',**({'Content-Type':'application/json'} if body else {}),**(headers or {})})
  with urllib.request.urlopen(req,timeout=30) as response:
   raw=response.read();decoded=gzip.decompress(raw) if response.headers.get('Content-Encoding')=='gzip' else raw;return json.loads(decoded)
 def test_state_catalog_and_unknown_costs_are_honest(self):
  s=self.request('state');self.assertEqual(len(s['catalog']),8);self.assertEqual(s['M09_started'],False);self.assertTrue(all(c['performance_metrics'] is None for c in s['feasibility']));self.assertIn('NO DEFENSIBLE',s['evaluation']['overall_winner'])
 def test_large_uncompressed_state_is_complete_across_connections(self):
  expected={r['run_id'] for r in server.results()}
  for _ in range(3):
   state=self.request('state',headers={'Accept-Encoding':'identity'});self.assertEqual({r['run_id'] for r in state['runs']},expected);self.assertEqual(len(state['catalog']),8)
 def test_concept_only_POST_never_starts_SUMO(self):
  before=dict(server.JOBS)
  for sid in ['S05','S06','S07']:
   with self.assertRaises(urllib.error.HTTPError) as error:self.request('run',{'solution':sid,'year':2026,'growth':'REFERENCE','seed':42})
   self.assertEqual(error.exception.code,400)
  self.assertEqual(server.JOBS,before)
 def test_incompatible_parent_rejected_before_job(self):
  for sid,family in [('S01','corrected-provisional'),('S02','pilot-strict'),('S03','pilot-strict')]:
   with self.assertRaises(urllib.error.HTTPError) as error:self.request('run',{'solution':sid,'year':2026,'growth':'REFERENCE','seed':42,'family':family})
   self.assertEqual(error.exception.code,400)
  value=self.request('map?solution=S01&family=corrected-provisional');self.assertEqual(value['manifest']['parameters'],{});self.assertTrue(value['manifest']['geometry_unchanged'])
 def test_origin_and_host_denied(self):
  for h in [{'Host':'outside.example'},{'Origin':'https://outside.example'}]:
   with self.assertRaises(urllib.error.HTTPError) as error:self.request('state',headers=h)
   self.assertEqual(error.exception.code,403)
 def test_concept_map_has_no_generated_ramps(self):
  value=self.request('map?solution=S06&family=pilot-provisional');self.assertTrue(value['no_new_ramps']);self.assertEqual(value['concept']['modelability'],'NOT_SIMULATION_READY');self.assertFalse(any('flyover' in e['id'].lower() for e in value['roads']))
 def test_actual_comparison_HTTP_censoring_and_parity(self):
  rr=server.results();a=next(r for r in rr if r['solution_id']=='S00' and r['year']==2026 and r['seed']==42 and r['growth_scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional');b=next(r for r in rr if r['solution_id']=='S01' and r['year']==2026 and r['seed']==42 and r['growth_scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional');value=self.request(f"compare?a={a['run_id']}&b={b['run_id']}");self.assertTrue(value['parity']['comparable']);self.assertIsNotNone(value['censoring_warning']);self.assertEqual(value['deltas']['requested'],0)
 def test_playback_only_actual_recorded_frames(self):
  rr=server.results();a=next(r for r in rr if r['solution_id']=='S00' and r['year']==2026 and r['seed']==42 and r['growth_scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional');v=self.request('playback?run_id='+a['run_id']+'&offset=40');self.assertEqual(v['frames'][0]['time'],200.5);self.assertEqual(v['run_id'],a['run_id']);self.assertLessEqual(len(v['frames']),5)
 def test_offline_worker_queue_rejects_interactive_job(self):
  with tempfile.TemporaryDirectory() as tmp,patch.object(server,'DOC',Path(tmp)):
   (Path(tmp)/'offline-stage.json').write_text(json.dumps({'status':'RUNNING'}));before=dict(server.JOBS)
   with self.assertRaises(urllib.error.HTTPError) as e:self.request('run',{'solution':'S04','year':2035,'growth':'REFERENCE','seed':42,'family':'pilot-provisional'})
   self.assertEqual(e.exception.code,409);self.assertEqual(before,server.JOBS)
 def test_signal_markers_reference_actual_recorded_controllers(self):
  value=self.request('map?solution=S01&family=pilot-provisional');r=next(r for r in server.results() if r['solution_id']=='S01' and r['year']==2026 and r['seed']==42 and r['growth_scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional');controllers={e['controller'] for e in r['rail_events']};self.assertTrue(all(set(s['controllers'])<=controllers for s in value['signals']));self.assertTrue(any('m05_gedangan' in s['controllers'] for s in value['signals']))
 def test_spillback_index_uses_real_causal_events_and_recorded_vehicle(self):
  r=next(r for r in server.results() if r['solution_id']=='S01' and r['growth_scenario']=='HIGH');value=self.request('playback?run_id='+r['run_id']+'&offset=140');self.assertEqual(len(value['spillback_events']),r['verified_in_model_spillback']);frame=value['frames'][0];active=[e for e in value['spillback_events'] if e['start']<=frame['time']<=e['end']];self.assertTrue(active);self.assertTrue(any(e['vehicle'] in {v['id'] for v in frame['vehicles']} for e in active));self.assertTrue(all(e['cause']=='VERIFIED_SPILLBACK' for e in value['spillback_events']))
