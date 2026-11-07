"""Actual localhost HTTP tests, including wire compression and origin rejection."""
import unittest,threading,urllib.request,urllib.error,json,gzip,tempfile
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from backend.gedangan import m07_server as server
from backend.gedangan.m07_scenarios import read
from backend.gedangan.m04_demand import sha,ROOT
class ProjectionHTTPTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start();cls.url=f'http://127.0.0.1:{cls.http.server_port}/api/m07/'
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.thread.join()
 def request(self,path,body=None,headers=None):
  request=urllib.request.Request(self.url+path,data=json.dumps(body).encode() if body else None,headers={'Host':'127.0.0.1:8772','Accept-Encoding':'gzip',**({'Content-Type':'application/json'} if body else {}),**(headers or {})})
  with urllib.request.urlopen(request,timeout=10) as response:
   raw=response.read();decoded=gzip.decompress(raw) if response.headers.get('Content-Encoding')=='gzip' else raw;return json.loads(decoded),len(raw),len(decoded)
 def test_real_HTTP_years_expected_and_compressed(self):
  for year,expected in [(2026,240),(2030,269),(2035,311),(2040,360)]:
   value,wire,decoded=self.request(f'project?year={year}&scenario_id=REFERENCE');self.assertEqual(value['requested'],expected);self.assertLess(wire,decoded);self.assertNotIn('annual_schedule',value['cells'][0]);self.assertIn('annual_schedule_note',value)
 def test_origin_and_host_rejected(self):
  for headers in [{'Origin':'https://untrusted.example'},{'Host':'untrusted.example'}]:
   with self.assertRaises(urllib.error.HTTPError) as error:self.request('state',headers=headers)
   self.assertEqual(error.exception.code,403)
 def test_display_map_matches_selected_actual_network(self):
  import xml.etree.ElementTree as E
  from backend.gedangan.m07_runner import NETWORKS
  for variant,path in NETWORKS.items():
   value,_,_=self.request('map?network='+variant);expected={e.get('id') for e in E.parse(path).getroot().findall('edge') if e.get('function')!='internal'};self.assertEqual({r['id'] for r in value['roads']},expected)
 def test_invalid_year_and_missing_scenario_are_errors(self):
  for path in ['project?year=2041&scenario_id=REFERENCE','project?year=2030&scenario_id=NOT_AVAILABLE']:
   with self.assertRaises(urllib.error.HTTPError) as error:self.request(path)
   self.assertEqual(error.exception.code,400)
 def test_custom_save_creates_versioned_file_preserves_presets(self):
  before={name:sha(ROOT/f'configuration/growth-m07/{name}.json') for name in ['LOW','REFERENCE','HIGH']}
  with tempfile.TemporaryDirectory() as tmp,patch.object(server,'CONF',Path(tmp)):
   value,_,_=self.request('scenario',{'scenario':read('REFERENCE')});self.assertTrue(value['id'].startswith('CUSTOM_'));self.assertTrue((Path(tmp)/(value['id']+'.json')).exists())
  self.assertEqual(before,{name:sha(ROOT/f'configuration/growth-m07/{name}.json') for name in before})
 def test_playback_pages_are_actual_bounded_frames(self):
  runs=server.results();run=next(r for r in runs if r['year']==2026 and r['scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional' and r['seed']==42)
  value,_,_=self.request('playback?run_id='+run['run_id']+'&offset=40');self.assertEqual(value['offset'],40);self.assertLessEqual(len(value['frames']),5);self.assertEqual(value['frames'][0]['time'],200.5);self.assertGreater(value['total_frames'],len(value['frames']))
