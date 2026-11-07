import unittest,json,gzip,xml.etree.ElementTree as E,threading,http.client,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from backend.gedangan.m09_export import CACHE,OUT,scene
from backend.gedangan.m09_checkpoint import ROOT,digest
from backend.gedangan.m09_server import handler,preflight,existing
from backend.gedangan.m08_comparison import guard
class PresentationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=json.loads((CACHE/'catalog.json').read_text());cls.runs=cls.catalog['runs'];cls.default=next(r for r in cls.runs if r['id']==cls.catalog['default_run']);cls.record=json.loads(gzip.decompress((CACHE/cls.default['index']).read_bytes()));cls.scene=json.loads(gzip.decompress((CACHE/cls.record['scene']).read_bytes()))
 def test_four_reference_baselines_and_operational_pair_exist(self):
  self.assertEqual({r['year'] for r in self.runs if r['scenario']=='S00' and r['growth']=='REFERENCE'},{2026,2030,2035,2040});self.assertTrue(any(c['comparable'] for c in self.catalog['comparisons']))
 def test_all_selections_unique_not_mislabeled(self):
  keys=[(r['year'],r['growth'],r['scenario']) for r in self.runs];self.assertEqual(len(keys),len(set(keys)));self.assertEqual(len(self.runs),23)
 def test_full_year_growth_projection_tables(self):
  p=self.catalog['projections'];self.assertEqual(len(p),45)
  for r in p:self.assertEqual(sum(r['classes'].values()),r['requested']);self.assertEqual(sum(r['OD'].values()),r['requested'])
 def test_source_hashes_network_and_registry_match(self):
  for r in self.runs:
   i=json.loads(gzip.decompress((CACHE/r['index']).read_bytes()));self.assertEqual(digest(CACHE/r['index']),r['index_sha256']);self.assertEqual(digest(ROOT/'configuration/demand-m04/vehicle-registry.json'),i['vehicle_registry_sha256']);original=ROOT/i['source_run_folder']
   for name,h in i['source_files_sha256'].items():self.assertEqual(digest(original/name),h)
 def test_half_second_recordings_have_demonstrated_clock_offset(self):
  for r in self.runs:
   i=json.loads(gzip.decompress((CACHE/r['index']).read_bytes()));self.assertEqual(i['step_s'],.5);self.assertEqual(i['fcd_to_traci_offset_s'],.5);self.assertGreater(i['clock_evidence']['matching_samples'],0);self.assertLessEqual(i['clock_evidence']['maximum_xy_error_m'],.03)
 def test_exported_positions_and_heading_are_exact_FCD(self):
  rec=self.record;f=json.loads(gzip.decompress((CACHE/rec['chunks'][0]['path']).read_bytes()))['frames'];exported=next(x for x in f if x['p']);p=exported['p'][0];vid=rec['vehicles'][p[0]]['id']
  for _,step in E.iterparse(ROOT/rec['source_run_folder']/'fcd.xml',events=['end']):
   if step.tag=='timestep' and float(step.get('time'))+.5==exported['t']:
    raw=next(v for v in step if v.get('id')==vid);self.assertEqual(p[1:5],[float(raw.get(k)) for k in ['x','y','angle','speed']]);break
 def test_recording_chunks_integrity_and_contiguous_times(self):
  for chunk in self.record['chunks']:
   p=CACHE/chunk['path'];self.assertEqual(digest(p),chunk['sha256']);frames=json.loads(gzip.decompress(p.read_bytes()))['frames'];self.assertEqual(frames[0]['t'],chunk['start']);self.assertEqual(frames[-1]['t'],chunk['end']);self.assertTrue(all(b['t']-a['t']==.5 for a,b in zip(frames,frames[1:])))
 def test_lifetimes_and_no_oversize_fabrication(self):
  for v in self.record['vehicles']:self.assertLessEqual(v['first'],v['last']);self.assertNotEqual(v['type'],'oversize')
  self.assertTrue(self.record['train_visible']);self.assertFalse(self.record['teleports']);self.assertFalse(self.record['illegal_permissions'])
 def test_rail_is_separate_from_road_geometry(self):
  rail=[l for l in self.scene['lanes'] if l['rail']];self.assertTrue(rail);self.assertTrue(all(l['id'].startswith(('m05_rail_',':')) for l in rail));self.assertTrue(any(l['role']=='frontage_road' for l in self.scene['lanes']))
 def test_short_lanes_retained_authoritative(self):
  short=self.scene['short_lanes'];self.assertTrue(short);self.assertTrue(any(l['length']<.11 for l in short));self.assertIn('unchanged',self.scene['refinement'].lower())
 def test_signal_heads_are_per_actual_controlled_link(self):
  root=E.parse(ROOT/self.scene['source_network']).getroot();source={(c.get('tl'),int(c.get('linkIndex')),c.get('from')+'_'+c.get('fromLane')) for c in root.findall('connection') if c.get('tl')}
  for h in self.scene['heads']:self.assertIn((h['controller'],h['link'],h['lane']),source)
 def test_signal_and_rail_states_come_from_source_recording(self):
  original=json.loads((ROOT/self.record['source_run_folder']/'playback.json').read_text());self.assertEqual(original['events'],self.record['events']);self.assertTrue(any(e['controller']=='osm_859708050' and 'r' in e['state'].lower() for e in self.record['events']))
 def test_23_metrics_reconcile_fixed_horizon(self):
  for r in self.runs:
   i=json.loads(gzip.decompress((CACHE/r['index']).read_bytes()));m=i['metrics'];self.assertEqual(m['requested'],m['failed_routes']+m['arrived']+m['running_at_end']+m['not_departed']);self.assertEqual(m['unserved_total_at_horizon'],m['requested']-m['arrived']);self.assertIsNone(m['arrived_only_travel_s'])
 def test_all_comparisons_use_existing_guard(self):
  for pair in self.catalog['comparisons']:
   c=json.loads((CACHE/pair['path']).read_text());self.assertTrue(c['parity']['comparable']);self.assertNotEqual(c['baseline'],c['intervention']);self.assertEqual(c['status'],'CONDITIONAL_COMPARISON_NOT_POLICY_RECOMMENDATION')
 def test_flyover_and_underpass_have_no_executable_recording(self):
  self.assertFalse(any(r['scenario'] in ['S05','S06','S07'] for r in self.runs));self.assertTrue(all(s['status']=='CONCEPT_ONLY' for s in self.catalog['catalog'] if s['id'] in ['S06','S07']))
 def test_build_is_self_contained(self):
  html=(ROOT/'frontend/dist-m09/presentation.html').read_text();self.assertNotIn('https://',html);self.assertIn('/assets/',html);self.assertFalse((ROOT/'frontend/dist-m09/m08').exists())
 def test_http_transport_missing_asset_origin_and_clean_shutdown(self):
  server=ThreadingHTTPServer(('127.0.0.1',0),handler(0,'test',self.catalog));port=server.server_port;server.RequestHandlerClass=handler(port,'test',self.catalog);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   for path,headers,status in [('/api/m09/health',{},200),('/presentation.html',{},200),('/cache/not-existing.json.gz',{},404),('/api/m09/health',{'Origin':'https://external.invalid'},403)]:
    conn=http.client.HTTPConnection('127.0.0.1',port);conn.request('GET',path,headers=headers);r=conn.getresponse();self.assertEqual(r.status,status);self.assertEqual(r.getheader('Transfer-Encoding'),'chunked');self.assertTrue(r.read());conn.close()
   self.assertEqual(existing(port)['service'],'gedangan-presentation-m09');conn=http.client.HTTPConnection('127.0.0.1',port);conn.request('POST','/api/m09/shutdown',json.dumps({'token':'test'}),{'Content-Type':'application/json'});r=conn.getresponse();self.assertTrue(json.loads(r.read())['closed']);conn.close();thread.join(5);self.assertFalse(thread.is_alive())
  finally:server.shutdown();server.server_close()
 def test_duplicate_server_cli_does_not_bind_again(self):
  value=existing(5185)
  if not value:self.skipTest('Presentation service not running; transport duplicate identity tested separately')
  p=subprocess.run([sys.executable,'-m','backend.gedangan.m09_server','--port','5185'],cwd=ROOT,capture_output=True,text=True,timeout=20);self.assertEqual(p.returncode,0);self.assertIn('sudah aktif',p.stdout)
 def test_local_launcher_has_dependency_checks_and_auto_open(self):
  text=(ROOT/'START_GEDANGAN_PRESENTATION.bat').read_text();self.assertIn('if not exist',text);self.assertIn('m09_server --open',text);self.assertNotIn('netsh',text)
