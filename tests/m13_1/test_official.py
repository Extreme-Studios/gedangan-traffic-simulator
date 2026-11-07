"""Real downloaded evidence + isolated synthetic software fixtures for admission gates."""
import unittest,tempfile,threading,urllib.request,urllib.error,base64
from backend.gedangan.m13_common import *
from backend.gedangan.m131_database import Store,DOC131,DB131
from backend.gedangan.m131_server import handler,ThreadingHTTPServer
class OfficialEvidence(unittest.TestCase):
 def test_01_original_complete_files_SHA_and_parser_evidence(self):
  m=load(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json');files=[r for r in m['files']if r['complete_binary_file']];self.assertEqual(len(files),32)
  for r in files:self.assertEqual(sha(ROOT/r['original_path']),r['sha256']);self.assertEqual(r['inspection_status'],'INSPECTED')
 def test_02_dedup_original_hash_reuse(self):
  m=load(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json');self.assertEqual(m['existing_complete_originals_reused_by_sha256'],2);self.assertEqual(m['new_distinct_complete_binary_files_saved'],30)
 def test_03_all_15_actual_datastore_tables_read(self):
  files=list((DOC131/'datastore').glob('*.json'));self.assertEqual(len(files),15)
  for p in files:r=load(p)['result'];self.assertEqual(len(r['records']),r['total'])
 def test_04_official_SMP_never_physical_vehicle_count(self):
  rows=[r for r in load(DOC131/'reference-aggregates.json')if r['source_id']=='DISHUB_VC_2022'];self.assertEqual(len(rows),43)
  for r in rows:self.assertEqual(r['unit'],'smp/hour');self.assertIsNone(r['vehicle_count']);self.assertIsNone(r['observation_date']);self.assertIsNone(r['interval_start']);self.assertFalse(r['calendar_eligible'])
 def test_05_PNL_real_counts_source_dates_not_publication_or_hourly_fill(self):
  rows=[r for r in load(DOC131/'reference-aggregates.json')if r['source_id']=='PNL_JENGGOLO_2023'];self.assertEqual(len(rows),49);self.assertEqual(sum(r['vehicle_count']for r in rows),15478);self.assertEqual(max(r['observation_date']for r in rows),'2023-12-03')
  for r in rows:self.assertEqual(r['unit'],'vehicles/12h');self.assertEqual(r['quality_class'],'B');self.assertFalse(r['calendar_eligible']);self.assertIsNone(r['network_edge']);self.assertEqual(r['direction'],'BOTH_DIRECTIONS_COMBINED')
 def test_06_BPS_metadata_export_is_plan_not_actual_count(self):
  r=next(r for r in load(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json')['files']if r['tag']=='BPS_2026_EXPORT');data=load(ROOT/r['original_path'])['kegiatan'];self.assertEqual(data['jd_pengumpulan_awal'],'2026-08-07');self.assertEqual(data['jd_diseminasi_awal'],'2027-01-04');self.assertEqual(r['quality_class'],'D');self.assertFalse(r['calendar_eligible'])
 def test_07_production_no_new_hourly_observations_and_no_schedule_promotion(self):
  store=Store();self.assertFalse(store.rows(eligible=True));self.assertEqual(len(store.reference_rows()),92)
  partial=load(DOC131/'partial-import.json');self.assertFalse(partial['staged_ids']);self.assertEqual(len(partial['quarantine']),49)
  for day in ['2026-08-07','2026-08-17','2024-08-15','2023-12-03','2025-05-16']:self.assertEqual(store.daily(day)['color'],'RED')
 def test_08_original_M13_and_actual_SUMO_preserved(self):
  origin=load(DOC131/'database-origin.json');self.assertEqual(sha(ROOT/'data/historical/m13/historical.sqlite'),origin['original_sha256']);p=load(DOC131/'preservation-verification.json');self.assertEqual(p['status'],'PASS');self.assertFalse(p['selected_SUMO_baseline_outputs_changed'])
 def test_09_corrupt_downloads_not_counted_as_complete(self):
  m=load(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json');self.assertEqual(len(m['corrupt_or_incomplete_pdf_downloads']),2)
  for r in m['corrupt_or_incomplete_pdf_downloads']:self.assertEqual(r['quality_class'],'E');self.assertFalse(r['complete_binary_file'])

class Admission(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.store=Store(Path(self.tmp.name)/'ISOLATED_SOFTWARE_TEST.sqlite',True)
  pair=self.store.scope()['pairs'][0];self.row={'observation_date':'2024-08-15','observation_time':'07:00:00','time_zone':'Asia/Jakarta','interval_start':'2024-08-15T07:00:00+07:00','interval_end':'2024-08-15T07:15:00+07:00',**pair,'vehicle_class':'car','vehicle_count':0,'measurement_unit':json.dumps({'vehicle_count':'vehicles/interval'})};self.source={'source_type':'OBSERVED_SECONDARY','quality_class':'B','source_name':'ISOLATED SOFTWARE_FIXTURE NOT REAL DATA','source_location':'ISOLATED TEST POINT','source_url':'https://example.invalid/software-fixture-only','survey_method':'Automated software test, not real survey'}
 def stage(self,rows=None,source=None):return self.store.import_bytes('ISOLATED.json',json.dumps(rows or[self.row]).encode(),source or self.source)
 def verify(self,r):return self.store.review(r['staged_ids'],'VERIFIED','AUTOMATED_SOFTWARE_TEST','ISOLATED FIXTURE, NOT FIELD EVIDENCE',True)
 def test_10_old_year_partial_hour_only_after_review(self):
  r=self.stage();self.assertEqual(self.store.daily('2024-08-15')['color'],'RED');self.verify(r);d=self.store.daily('2024-08-15');self.assertEqual(d['color'],'YELLOW');self.assertEqual(d['available_hours'],[7]);self.assertEqual(d['hours'][7]['available_cells'][0]['observed_seconds'],900);self.assertEqual(self.store.daily('2024-08-16')['color'],'RED')
 def test_11_multi_year_not_hardcoded_2026(self):
  for month in ['2022-01','2023-12','2024-08','2025-05','2026-08']:self.assertTrue(self.store.monthly(month)['days'])
 def test_12_qualityC_observed_promotion_rejected(self):
  with self.assertRaisesRegex(ValueError,'A or B'):self.stage(source={**self.source,'quality_class':'C'})
 def test_13_synthetic_source_never_verified(self):
  r=self.stage(source={**self.source,'source_type':'SYNTHETIC_TEST'})
  with self.assertRaisesRegex(ValueError,'never enter'):self.verify(r)
 def test_14_unknown_legacy_quality_not_promoted(self):
  r=self.stage()
  with connect(self.store.path)as c:
   with self.assertRaises(sqlite3.IntegrityError):c.execute('DELETE FROM source_quality')
 def test_15_duplicates_prevented(self):
  self.stage()
  with self.assertRaisesRegex(ValueError,'Duplicate file'):self.stage()
 def test_16_unit_and_location_validation(self):
  r=self.stage(rows=[{**self.row,'measurement_unit':json.dumps({'vehicle_count':'smp/hour'})},{**self.row,'road_segment':'ASSUMED_ROAD_NO_EVIDENCE'}]);self.assertFalse(r['staged_ids']);self.assertEqual(len(r['quarantine']),2)
 def test_17_12hour_aggregate_cannot_become_hourly(self):
  r=self.stage(rows=[{**self.row,'interval_end':'2024-08-15T19:00:00+07:00'}]);self.assertFalse(r['staged_ids']);self.assertEqual(len(r['quarantine']),1)
 def test_18_live_HTTP_month_import_review_refresh_and_missing_guard(self):
  server=ThreadingHTTPServer(('127.0.0.1',0),handler(self.store,0));port=server.server_port;server.RequestHandlerClass=handler(self.store,port);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  def call(path,body=None):
   req=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=json.dumps(body).encode()if body else None,headers={'Content-Type':'application/json'})
   with urllib.request.urlopen(req)as r:return json.load(r)
  try:
   self.assertEqual(call('/api/monthly?month=2024-08')['days'][14]['color'],'RED');r=call('/api/import',{'filename':'ISOLATED.json','base64':base64.b64encode(json.dumps([self.row]).encode()).decode(),'source':self.source});call('/api/review',{'ids':r['staged_ids'],'decision':'VERIFIED','reviewer':'AUTOMATED_SOFTWARE_TEST','note':'ISOLATED FIXTURE ONLY','evidence_checked':True});self.assertEqual(call('/api/monthly?month=2024-08')['days'][14]['color'],'YELLOW');self.assertEqual(call('/api/archive')['verified_observation_months'],['2024-08'])
   with self.assertRaises(urllib.error.HTTPError):call('/api/select',{'date':'2024-08-16','hour':7})
  finally:server.shutdown();server.server_close();thread.join()
if __name__=='__main__':unittest.main()
