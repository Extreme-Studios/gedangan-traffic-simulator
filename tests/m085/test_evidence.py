import unittest,tempfile,json,hashlib,zipfile,io,threading,http.client,socket
from pathlib import Path
from unittest.mock import patch
from backend.gedangan.m085_survey import SurveyStore,uid,CLASSES
from backend.gedangan.m085_provenance import clock,gate_source
from backend.gedangan.m085_export import export_session,materialize
from backend.gedangan.m085_video_annotation import hash_file,observation_time
from backend.gedangan.m085_observer_qc import compare_counts
from backend.gedangan.m085_server import handler
from http.server import ThreadingHTTPServer
from datetime import timedelta
class EvidenceTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='m085-evidence-');self.store=SurveyStore(Path(self.temp.name),True);self.s=self.cmd('demo_create',{});self.sid=self.s['id']
 def tearDown(self):self.temp.cleanup()
 def cmd(self,a,p):return self.store.command(a,p,uid())
 def t(self,n=0):return (clock(self.s['start'])+timedelta(seconds=n)).isoformat()
 def media(self,known=False):
  m=self.cmd('media_register',{'filename':'synthetic.mp4','size':123,'sha256':'a'*64,'duration_s':120,'recording_start':self.t() if known else None,'permission_confirmed':True});self.cmd('media_attach',{'session_id':self.sid,'media_id':m['id']});return m
 def event(self,kind='COUNT',**p):return self.cmd('event_add',{'session_id':self.sid,'type':kind,'data':{'timestamp':self.t(10),'vehicle_class':'car','approach':'MAIN_NB','direction':'northbound','movement':'straight','lane_group':'A','confidence':'HIGH',**p}})
 def video(self,m,sec=10,token=None,**p):return self.event(media_id=m['id'],video_seconds=sec,vehicle_token=token or 'ANON_'+uid(),**p)
 def test_timezone_does_not_guess_utc_or_naive(self):
  for t in ['2026-01-01T00:00:00','2026-01-01T00:00:00Z','2026-01-01T00:00:00+08:00']:
   with self.assertRaises(ValueError):clock(t)
 def test_unknown_clock_quarantined_not_replaced_by_file_date(self):
  m=self.media();self.video(m);v=export_session(self.store,self.sid);self.assertEqual(v['rows'],0);self.assertEqual(v['preimport_rejected'],1);e=self.store.ledger(self.sid)['events'][0];self.assertIsNone(e['timestamp']);self.assertEqual(e['time_status'],'VIDEO_TIME_ONLY')
 def test_known_clock_exact_mapping_and_offset(self):
  m=self.media(True);self.assertEqual(observation_time({**m,'clock_offset_s':3},10),clock(self.t(13)).isoformat(timespec='milliseconds'));self.video(m,10);self.assertEqual(clock(self.store.ledger(self.sid)['events'][0]['timestamp']),clock(self.t(10)))
 def test_late_clock_review_preserves_original_raw_and_exports_new_mapping(self):
  m=self.media();e=self.video(m)
  self.event('COVERAGE',media_id=m['id'],video_seconds=20,classes=['car'],review_start_s=0,review_end_s=120,coverage_status='COMPLETE')
  with self.store.connect() as c:before=c.execute('SELECT body FROM raw_events WHERE id=?',(e['event_id'],)).fetchone()[0]
  self.cmd('media_clock_review',{'media_id':m['id'],'recording_start':self.t(),'reviewer':'DEMO_REVIEWER','confirmed_recording_clock':True,'evidence_reference':'SYNTHETIC software clock fixture'})
  v=export_session(self.store,self.sid);self.assertEqual(v['rows'],1);self.assertEqual(v['m06_rejected'],0)
  with self.store.connect() as c:self.assertEqual(before,c.execute('SELECT body FROM raw_events WHERE id=?',(e['event_id'],)).fetchone()[0])
  self.store.integrity()
 def test_same_vehicle_token_rejected_and_rewind_requires_reason(self):
  m=self.media();token='ANON_'+uid();self.video(m,20,token)
  with self.assertRaises(ValueError):self.video(m,30,token)
  with self.assertRaises(ValueError):self.video(m,10)
  self.video(m,10,distinct_vehicle_reason='Different unseen synthetic token reviewed by operator');self.assertEqual(self.store.state()['raw_events'],2)
 def test_same_hash_new_reference_does_not_bypass_replay_guard(self):
  m=self.media();token='ANON_'+uid();self.video(m,20,token);s=self.cmd('demo_create',{});self.sid=s['id'];m2=self.media()
  with self.assertRaises(ValueError):self.video(m2,30,token)
 def test_independent_observer_can_annotate_same_vehicle(self):
  m=self.media();token='ANON_'+uid();self.video(m,20,token);s=self.cmd('session_save',{**self.s,'id':uid(),'observer_id':'DEMO_REVIEWER'});self.sid=s['id'];self.cmd('session_status',{'session_id':self.sid,'status':'READY'});self.cmd('session_status',{'session_id':self.sid,'status':'IN_PROGRESS'});m2=self.media();self.video(m2,20,token);self.assertEqual(self.store.state()['raw_events'],2)
 def test_queue_count_is_not_meter_length_and_censoring_retained(self):
  self.event('QUEUE',queue_count=7,queue_length_m=None,boundary_censored=True,definition='visible stopped queue',observation_end=self.t(20));v=export_session(self.store,self.sid);rows=json.loads((self.store.root/'exports'/v['id']/'queue.json').read_text());self.assertEqual(rows[0]['queue_count'],7);self.assertIsNone(rows[0]['queue_length_m']);self.assertTrue(rows[0]['boundary_censored'])
  with self.assertRaises(ValueError):self.event('QUEUE',queue_length_m=30,boundary_censored=False,definition='queue')
 def test_signal_and_rail_sequence_rejected(self):
  with self.assertRaises(ValueError):self.event('SIGNAL',signal_group='head',phase='1',green_start=self.t(20),green_end=self.t(10))
  with self.assertRaises(ValueError):self.event('RAILWAY',closure_id='c',train_id='t',warning_starts=self.t(20),road_fully_closed=self.t(10))
 def test_video_sequence_validated_without_recording_clock(self):
  m=self.media()
  with self.assertRaises(ValueError):self.event('SIGNAL',media_id=m['id'],video_seconds=20,signal_group='h',phase='1',video_event_seconds={'green_start':20,'green_end':10})
 def test_video_travel_duration_without_fabricated_clock(self):
  m=self.media();self.event('TRAVEL_TIME',media_id=m['id'],video_seconds=30,video_start_s=10,video_end_s=30,origin='A',destination='B',corridor='fixture',route='A-B',sample_token='ANON_'+uid(),method='VIDEO_ANONYMOUS_ENDPOINTS');e=self.store.ledger(self.sid)['events'][0];self.assertEqual(e['travel_time_s'],20);self.assertIsNone(e['start_timestamp']);self.assertEqual(export_session(self.store,self.sid)['rows'],0)
 def test_geometry_units_crs_and_transactional_rejected_rows(self):
  p={'survey_point':[999,999],'crs':'EPSG:4326','units':'m','instrument':'GNSS','measurement_method':'survey','source':'fixture','accuracy_m':3}
  with self.assertRaises(ValueError):self.event('GEOMETRY',**p)
  with self.assertRaises(ValueError):self.event('GEOMETRY',**{**p,'survey_point':[112,-7],'units':'pixels'})
  text='timestamp,observation_end,x,y,crs,units,instrument,measurement_method,accuracy_m,source\n'+self.t()+','+self.t(10)+',112,-7,EPSG:4326,m,GNSS,survey,3,SYNTHETIC\n'+self.t()+',,999,999,EPSG:4326,m,GNSS,survey,3,SYNTHETIC\n'
  v=self.cmd('geometry_import',{'session_id':self.sid,'csv_text':text,'filename':'synthetic.csv','sha256':hashlib.sha256(text.encode()).hexdigest()});self.assertEqual(v['accepted'],1);self.assertEqual(len(v['rejected']),1);self.store.integrity()
 def test_no_synthetic_promotion_or_reference_promotion(self):
  self.assertEqual(gate_source(self.s,{'decision':'APPROVED'}),'DEMO_SYNTHETIC')
  for source in ['SIMULATED_RESULT','MISSING','ASSUMPTION','VIDEO_OBSERVATION','OBSERVED_FIELD']:
   with self.assertRaises(ValueError):gate_source({**self.s,'source_class':source},{})
  with self.assertRaises(ValueError):self.cmd('recon_save',{'location_id':'MAIN_NB','observer_id':'DEMO_OBSERVER','source_class':'OBSERVED_FIELD'})
 def test_forbidden_media_bytes_redacted_even_in_rejected_log(self):
  secret='PRIVATE_BINARY_MARKER'
  with self.assertRaises(ValueError):self.cmd('media_register',{'video_data':secret})
  with self.store.connect() as c:self.assertNotIn(secret,c.execute('SELECT body FROM rejected_commands').fetchone()[0])
  self.store.integrity()
 def test_source_hash_streams_existing_synthetic_video(self):
  fixture=Path(__file__).resolve().parents[1]/'fixtures/m085/synthetic-annotation.mp4';v=hash_file(fixture);self.assertEqual(v['sha256'],hashlib.sha256(fixture.read_bytes()).hexdigest());self.assertGreater(v['size'],1000)
 def test_backup_corruption_never_switches_active_pointer(self):
  self.event();v=self.store.backup();old=self.store.path;bad=self.store.root/'bad.zip'
  with zipfile.ZipFile(self.store.root/'backups'/(v['id']+'.zip')) as src,zipfile.ZipFile(bad,'w') as out:
   for name in src.namelist():out.writestr(name,b'corrupt' if name=='survey.sqlite' else src.read(name))
  with self.assertRaises(ValueError):self.store.restore(bad,'RESTORE_AS_NEW_BRANCH')
  self.assertEqual(self.store.path,old);self.assertEqual(SurveyStore(self.store.root,True).state()['raw_events'],1)
 def test_qc_missing_not_zero_and_independent_adjudication(self):
  a=self.cmd('session_save',{**self.s,'id':uid(),'sample_group':'shared'});b=self.cmd('session_save',{**self.s,'id':uid(),'sample_group':'shared','observer_id':'DEMO_REVIEWER'})
  for s,count in [(a,2),(b,1)]:
   self.sid=s['id'];self.cmd('session_status',{'session_id':self.sid,'status':'READY'});self.cmd('session_status',{'session_id':self.sid,'status':'IN_PROGRESS'})
   for _ in range(count):self.event()
   self.event('COVERAGE',classes=['car'],coverage_status='COMPLETE',coverage_start=self.t(),coverage_end=self.t(900))
  q=compare_counts(self.store,a['id'],b['id']);self.assertEqual(q['rows'][0]['absolute_difference'],1);self.assertAlmostEqual(q['rows'][0]['relative_difference'],2/3)
  self.cmd('observer_save',{'id':'INDEPENDENT','name':'synthetic reviewer','roles':['REVIEWER'],'training':[]});self.cmd('qc_adjudicate',{'session_A':a['id'],'session_B':b['id'],'comparison_id':q['id'],'reviewer':'INDEPENDENT','selection':'RECOUNT_REQUIRED','reason':'fixture discrepancy'});self.assertFalse(q['automatic_average'])
  with self.assertRaises(ValueError):compare_counts(self.store,a['id'],a['id'])
 def test_offline_backend_no_external_connection_and_paged_ledger(self):
  with patch.object(socket,'create_connection',side_effect=AssertionError('External connection forbidden')):
   for _ in range(105):self.event()
   self.assertEqual(len(self.store.ledger(self.sid,50,50)['events']),50);self.assertEqual(len(self.store.ledger(self.sid,100,50)['events']),5);self.store.backup();self.store.integrity()
 def test_http_host_origin_and_production_static_transport(self):
  static=self.store.root/'frontend/dist-m085';static.mkdir(parents=True);(static/'survey.html').write_text('<!doctype html><title>M085 test transport</title>',encoding='utf-8')
  server=ThreadingHTTPServer(('127.0.0.1',0),handler(self.store,[]));port=server.server_port;server.RequestHandlerClass=handler(self.store,[port]);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   with patch('backend.gedangan.m085_server.ROOT',self.store.root):
    for path,headers,status in [('/api/m085/state',{},200),('/api/m085/state',{'Origin':'https://external.invalid'},403),('/survey.html',{},200),('/api/m085/state',{'Host':'evil.invalid'},403)]:
     c=http.client.HTTPConnection('127.0.0.1',port);c.request('GET',path,headers=headers);r=c.getresponse();data=r.read();self.assertEqual(r.status,status);self.assertEqual(r.getheader('Transfer-Encoding'),'chunked');self.assertTrue(data);c.close()
  finally:server.shutdown();server.server_close();thread.join()
 def test_confidence_and_overlapping_coverage_do_not_create_verified_volume(self):
  self.event();self.event('COVERAGE',classes=['car'],coverage_status='COMPLETE',coverage_start=self.t(),coverage_end=self.t(900));v=export_session(self.store,self.sid);row=json.loads((self.store.root/'exports'/v['id']/'traffic_count.json').read_text())[0];self.assertEqual(row['confidence'],'HIGH');self.assertEqual(row['count'],1)
  self.event('COVERAGE',classes=['car'],coverage_status='COMPLETE',coverage_start=self.t(),coverage_end=self.t(900));v=export_session(self.store,self.sid);row=json.loads((self.store.root/'exports'/v['id']/'traffic_count.json').read_text())[0];self.assertIsNone(row['count']);self.assertIn('OVERLAPPING_COVERAGE_REVIEW',row['notes'])
 def test_projection_tamper_is_detected(self):
  self.event()
  with self.store.connect() as c:c.execute("UPDATE current_events SET active=0")
  with self.assertRaises(ValueError):self.store.integrity()
 def test_additional_trains_and_missing_signal_are_preserved(self):
  self.event('RAILWAY',closure_id='closure',train_id='primary',warning_starts=self.t(0),road_traffic_released=self.t(100),additional_train_movements=[{'train_id':'second','train_approaches':self.t(50),'train_passes':self.t(60),'train_clears':self.t(70)}]);self.event('SIGNAL',signal_group='one-visible-head',phase='partial',green_start=self.t(),green_end=self.t(20));v=export_session(self.store,self.sid);folder=self.store.root/'exports'/v['id'];rail=json.loads((folder/'railway.json').read_text())[0];signal=json.loads((folder/'signal.json').read_text())[0];self.assertIn('second',rail['notes']);self.assertIsNone(signal['red_s']);self.assertIsNone(signal['cycle_s'])
