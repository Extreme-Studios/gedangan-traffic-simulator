"""All numbers below are isolated software fixtures. Production database stays empty for2026."""
import unittest,tempfile,csv,io,zipfile,threading,urllib.request,urllib.error,base64
from backend.gedangan.m13_common import *
from backend.gedangan.m13_database import Store,spreadsheet_rows
from backend.gedangan.m13_server import handler,ThreadingHTTPServer
SOURCE={'source_type':'OBSERVED_PRIMARY','source_name':'ISOLATED SOFTWARE_FIXTURE NOT FIELD DATA','source_location':'ISOLATED SOFTWARE TEST','survey_method':'Automated software fixture only'}
def row(day='2026-08-02',hour=7,**overrides):
 from backend.gedangan.m13_database import default_scope
 pair=default_scope()['pairs'][0]
 return {'observation_date':day,'observation_time':f'{hour:02d}:00:00','time_zone':'Asia/Jakarta','interval_start':f'{day}T{hour:02d}:00:00+07:00','interval_end':f'{day}T{hour:02d}:15:00+07:00',**pair,'vehicle_class':'car','vehicle_count':0,'turning_movement':None,'speed':None,'queue_length':None,'travel_time':None,'measurement_unit':json.dumps({'vehicle_count':'vehicles/interval'}),**overrides}
def body(rows):return json.dumps(rows).encode()
class HistoricalTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.store=Store(Path(self.tmp.name)/'isolated-test.sqlite',test_fixture=True)
 def stage(self,rows,source=None):return self.store.import_bytes('isolated-software-test.json',body(rows),source or SOURCE)
 def verify(self,r):return self.store.review(r['staged_ids'],'VERIFIED','AUTOMATED_TEST_ONLY','Fixture assertions; no real evidence claim',True)
 def test_01_no_data_red_and_all_hours_disabled(self):
  d=self.store.daily('2026-08-01');self.assertEqual(d['color'],'RED');self.assertEqual(d['missing_hours'],24);self.assertTrue(all(h['disabled']for h in d['hours']))
 def test_02_partial_only_after_review_and_missing_dimensions_explicit(self):
  r=self.stage([row()]);self.assertEqual(self.store.daily('2026-08-02')['color'],'RED');self.verify(r);d=self.store.daily('2026-08-02');self.assertEqual(d['color'],'YELLOW');self.assertEqual(d['available_hours'],[7]);h=d['hours'][7];self.assertEqual(h['available_cells'][0]['observed_seconds'],900);self.assertTrue(h['missing_or_partial_cells']);self.assertEqual(h['available_cells'][0]['evidence'][0]['value'],0)
 def test_03_full_scope_all_24hours_green(self):
  rows=[];scope=self.store.scope();day='2026-08-03'
  for hour in range(24):
   for pair in scope['pairs']:
    for cls in CLASSES:
     end=(datetime.fromisoformat(f'{day}T{hour:02d}:00:00+07:00')+timedelta(hours=1)).isoformat();rows.append(row(day,hour,**pair,vehicle_class=cls,interval_end=end,turning_movement='all_movements',speed=10,queue_length=0,travel_time=3,measurement_unit=json.dumps({'vehicle_count':'vehicles/interval','turning_movement':'category','speed':'km/h','queue_length':'m','travel_time':'s'})))
  r=self.stage(rows);self.assertFalse(r['quarantine']);self.verify(r);d=self.store.daily(day);self.assertEqual(d['color'],'GREEN');self.assertEqual(d['complete_hours'],24);self.assertEqual(len(d['hours'][7]['available_cells']),100);self.assertTrue(self.store.test_fixture)
 def test_04_reference_simulation_synthetic_never_calendar(self):
  for i,kind in enumerate(['REFERENCE_STUDY','SIMULATION_OUTPUT','SYNTHETIC_TEST']):
   r=self.stage([row(hour=i)],{**SOURCE,'source_type':kind})
   with self.assertRaisesRegex(ValueError,'never enter'):self.verify(r)
  self.assertEqual(self.store.daily('2026-08-02')['color'],'RED')
 def test_05_no_adjacent_date_fallback(self):
  self.verify(self.stage([row()]));self.assertEqual(self.store.daily('2026-08-01')['color'],'RED');self.assertEqual(self.store.daily('2026-08-03')['color'],'RED')
 def test_06_no_defaults_or_random_fill_NULL_retained(self):
  r=self.stage([row()]);self.verify(r);v=self.store.rows()[0];self.assertEqual(v['vehicle_count'],0);self.assertIsNone(v['speed']);self.assertIsNone(v['queue_length']);self.assertEqual(self.store.daily('2026-08-02')['hours'][6]['observations'],0)
 def test_07_import_changes_version_and_calendar_after_verification(self):
  old=self.store.version();self.assertEqual(self.store.monthly('2026-08')['days'][1]['color'],'RED');r=self.stage([row()]);self.verify(r);self.assertNotEqual(old,self.store.version());self.assertEqual(self.store.monthly('2026-08')['days'][1]['color'],'YELLOW')
 def test_08_provenance_archive_SHA_and_original_unchanged(self):
  data=body([row()]);r=self.store.import_bytes('original.json',data,SOURCE);source=self.store.provenance()['sources'][0];self.assertEqual(sha(source['archive_path']),hashlib.sha256(data).hexdigest());self.assertEqual(source['sha256'],r['sha256']);self.assertEqual(Path(source['archive_path']).read_bytes(),data)
 def test_09_invalid_duplicate_overlap_quarantined(self):
  rows=[row(vehicle_count=-1),row(vehicle_class='spaceship'),row(time_zone='UTC'),row(interval_end='2026-08-02T06:00:00+07:00'),row(),row(),['invalid unnamed row']];r=self.stage(rows);self.assertEqual(len(r['staged_ids']),1);self.assertEqual(len(r['quarantine']),6)
  with self.assertRaisesRegex(ValueError,'Duplicate file'):self.stage(rows)
 def test_10_database_append_only_and_fk_integrity(self):
  self.stage([row()])
  with connect(self.store.path)as c:
   with self.assertRaises(sqlite3.IntegrityError):c.execute('UPDATE observations SET vehicle_count=99')
   with self.assertRaises(sqlite3.IntegrityError):c.execute('DELETE FROM observations')
   self.assertEqual(c.execute('PRAGMA integrity_check').fetchone()[0],'ok');self.assertFalse(c.execute('PRAGMA foreign_key_check').fetchall())
 def test_11_no_unit_conversion_guess_or_rate_as_raw_count(self):
  for invalid in [row(measurement_unit='{}'),row(vehicle_count=1.5),row(speed=1),row(vehicle_count='NaN'),row(vehicle_count=None)]:
   with self.assertRaises(ValueError):self.store.validate(invalid)
 def test_12_half_hour_partial_and_no_completeness_from_count_only(self):
  r=self.stage([row(interval_end='2026-08-02T07:30:00+07:00')]);self.verify(r);h=self.store.hour('2026-08-02',7,{'road_segment':row()['road_segment'],'direction':'NB','vehicle_class':'car','parameter':'vehicle_count'});self.assertEqual(h['status'],'PARTIAL');self.assertEqual(h['available_cells'][0]['observed_seconds'],1800)
 def test_13_nonempty_review_and_rollback_required(self):
  r=self.stage([row()])
  with self.assertRaises(ValueError):self.store.review(r['staged_ids'],'VERIFIED','','',False)
  self.assertEqual(self.store.daily('2026-08-02')['color'],'RED')
 def test_14_classification_conflict_cannot_be_laundered(self):
  r=self.stage([row(source_type='SYNTHETIC_TEST')]);self.assertFalse(r['staged_ids']);self.assertEqual(len(r['quarantine']),1)
 def test_15_xlsx_values_read_and_formulas_rejected(self):
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w')as z:z.writestr('xl/worksheets/sheet1.xml','<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row><c r="A1" t="inlineStr"><is><t>vehicle_count</t></is></c></row><row><c r="A2"><v>0</v></c></row></sheetData></worksheet>')
  self.assertEqual(spreadsheet_rows(stream.getvalue()),[{'vehicle_count':'0'}])
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w')as z:z.writestr('xl/worksheets/sheet1.xml','<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row><c r="A1"><f>RAND()</f><v>0</v></c></row></sheetData></worksheet>')
  with self.assertRaisesRegex(ValueError,'Formula'):spreadsheet_rows(stream.getvalue())
 def test_16_live_HTTP_import_review_refresh_and_guard(self):
  server=ThreadingHTTPServer(('127.0.0.1',0),BaseHandler:=handler(self.store,0));port=server.server_port;server.RequestHandlerClass=handler(self.store,port);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  def call(path,value=None):
   req=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=json.dumps(value).encode()if value is not None else None,headers={'Content-Type':'application/json'})
   with urllib.request.urlopen(req)as response:return json.load(response)
  try:
   self.assertEqual(call('/api/monthly?month=2026-08')['days'][1]['color'],'RED')
   with self.assertRaises(urllib.error.HTTPError):call('/api/select',{'date':'2026-08-02','hour':7})
   r=call('/api/import',{'filename':'isolated.json','base64':base64.b64encode(body([row()])).decode(),'source':SOURCE});call('/api/review',{'ids':r['staged_ids'],'decision':'VERIFIED','reviewer':'AUTOMATED_TEST','note':'ISOLATED FIXTURE ONLY','evidence_checked':True});self.assertEqual(call('/api/monthly?month=2026-08')['days'][1]['color'],'YELLOW');self.assertFalse(call('/api/select',{'date':'2026-08-02','hour':7})['automatic_imputation'])
   self.assertTrue(call('/api/provenance')['sources']);self.assertEqual(sum(r['status']=='OBSERVED'for r in call('/api/roads')['items']),1)
  finally:server.shutdown();server.server_close();thread.join()
 def test_17_new_verified_monitor_point_automatically_enters_scope(self):
  r=self.stage([row(road_segment='w985823770_s0_p0_0_f',direction='EB')]);self.verify(r);self.assertEqual(self.store.daily('2026-08-02')['color'],'YELLOW');self.assertIn({'road_segment':'w985823770_s0_p0_0_f','direction':'EB'},self.store.scope()['pairs'])
 def test_18_fixture_source_explicitly_rejected_by_production_boundary(self):
  production=Store(Path(self.tmp.name)/'production-boundary.sqlite')
  with self.assertRaisesRegex(ValueError,'cannot be promoted'):production.import_bytes('fixture.json',body([row()]),SOURCE)
  self.assertFalse(production.rows())
 def test_19_CSV_import_preserves_zero_NULL_and_SHA(self):
  sample=row();text=io.StringIO();writer=csv.DictWriter(text,fieldnames=list(sample));writer.writeheader();writer.writerow(sample);r=self.store.import_bytes('fixture.csv',text.getvalue().encode(),SOURCE);self.assertEqual(len(r['staged_ids']),1);self.assertFalse(r['quarantine']);self.verify(r);self.assertEqual(self.store.rows()[0]['vehicle_count'],0);self.assertIsNone(self.store.rows()[0]['travel_time'])
 def test_20_interval_union_four_quarters_completes_only_selected_hour_scope(self):
  samples=[]
  for minute in [0,15,30,45]:
   start=datetime.fromisoformat('2026-08-02T07:00:00+07:00')+timedelta(minutes=minute);samples.append(row(observation_time=start.strftime('%H:%M:%S'),interval_start=start.isoformat(),interval_end=(start+timedelta(minutes=15)).isoformat()))
  r=self.stage(samples);self.verify(r);filters={'road_segment':row()['road_segment'],'direction':'NB','vehicle_class':'car','parameter':'vehicle_count'};self.assertEqual(self.store.hour('2026-08-02',7,filters)['status'],'OBSERVED');self.assertEqual(self.store.daily('2026-08-02')['color'],'YELLOW')
if __name__=='__main__':unittest.main()
