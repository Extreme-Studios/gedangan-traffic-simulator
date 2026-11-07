import unittest,tempfile,json,sqlite3
from pathlib import Path
from datetime import timedelta
from backend.gedangan.m085_survey import SurveyStore,uid,CLASSES,RAIL_EVENTS
from backend.gedangan.m085_provenance import clock
from backend.gedangan.m085_export import export_session
class SurveyStoreTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='m085-synthetic-');self.store=SurveyStore(Path(self.temp.name),synthetic_only=True);self.session=self.cmd('demo_create',{});self.sid=self.session['id']
 def tearDown(self):self.temp.cleanup()
 def cmd(self,action,p,command_id=None):return self.store.command(action,p,command_id or uid())
 def t(self,seconds=10):return (clock(self.session['start'])+timedelta(seconds=seconds)).isoformat()
 def event(self,kind='COUNT',**kwargs):return self.cmd('event_add',{'session_id':self.sid,'event_id':uid(),'type':kind,'data':{'timestamp':self.t(),'vehicle_class':'car','direction':'northbound','approach':'MAIN_NB','movement':'straight','lane_group':'ALL_VISIBLE','confidence':'UNKNOWN',**kwargs}})
 def coverage(self,classes=None,status='COMPLETE',start=0,end=900):return self.event('COVERAGE',classes=classes or ['car'],coverage_status=status,coverage_start=self.t(start),coverage_end=self.t(end))
 def test_seven_planned_locations_and_no_field_verification(self):
  s=self.store.state();self.assertEqual(len(s['locations']),7);self.assertTrue(all(l['status']=='PLANNED' and l['field_coordinates'] is None for l in s['locations']));self.assertEqual(s['raw_events'],0)
 def test_idempotency_does_not_silently_drop_a_different_payload(self):
  key=uid();event={'session_id':self.sid,'event_id':uid(),'type':'COUNT','data':{'timestamp':self.t(),'vehicle_class':'car','approach':'MAIN_NB','direction':'northbound','movement':'straight','lane_group':'all'}};a=self.cmd('event_add',event,key);self.assertEqual(self.cmd('event_add',event,key),a)
  with self.assertRaises(ValueError):self.cmd('event_add',{**event,'event_id':uid()},key)
  self.assertEqual(self.store.state()['raw_events'],1);self.assertTrue(self.store.integrity()['immutable_triggers'])
 def test_raw_immutable_undo_and_edit_are_append_only(self):
  e=self.event();self.cmd('event_correct',{'session_id':self.sid,'event_id':e['event_id'],'actor':'DEMO_OBSERVER','reason':'synthetic correction','patch':{'vehicle_class':'motorcycle'}})
  with self.store.connect() as c:
   raw=c.execute('SELECT body FROM raw_events WHERE id=?',(e['event_id'],)).fetchone()[0];self.assertEqual(json.loads(raw)['vehicle_class'],'car')
   with self.assertRaises(sqlite3.IntegrityError):c.execute('DELETE FROM raw_events')
  self.cmd('undo',{'session_id':self.sid,'actor':'DEMO_OBSERVER','reason':'synthetic undo'});self.assertEqual(self.store.ledger(self.sid)['summary'],[]);self.store.integrity()
 def test_pause_prevents_new_count_but_allows_correction(self):
  self.event();self.cmd('pause',{'session_id':self.sid,'paused':True})
  with self.assertRaises(ValueError):self.event()
  self.cmd('undo',{'session_id':self.sid,'actor':'DEMO_OBSERVER','reason':'remove duplicate while paused'});self.store.integrity()
 def test_all_ten_classes_can_be_observed_even_oversize_model_is_blocked(self):
  for cls in CLASSES:self.event(vehicle_class=cls)
  self.assertEqual({r['cls'] for r in self.store.ledger(self.sid)['summary']},set(CLASSES))
 def test_zero_requires_explicit_complete_coverage(self):
  self.event();self.coverage(['car','motorcycle']);result=export_session(self.store,self.sid);folder=self.store.root/'exports'/result['id'];rows=json.loads((folder/'traffic_count.json').read_text());self.assertEqual({r['vehicle_class']:r['count'] for r in rows},{'car':1,'motorcycle':0});self.assertFalse(result['m06_rejected'])
 def test_unreviewed_count_remains_null_with_partial_evidence(self):
  self.event();result=export_session(self.store,self.sid);row=json.loads((self.store.root/'exports'/result['id']/'traffic_count.json').read_text())[0];self.assertIsNone(row['count']);self.assertEqual(json.loads(row['notes'])['extra']['partial_count'],1)
 def test_interval_boundary_and_short_video_coverage_not_rounded_into_fake_volume(self):
  self.event(timestamp=self.t(899));self.event(timestamp=self.t(900));self.coverage(start=0,end=1800);r=export_session(self.store,self.sid);rows=json.loads((self.store.root/'exports'/r['id']/'traffic_count.json').read_text());self.assertEqual([x['count'] for x in rows],[1,1])
 def test_backup_restore_is_new_branch_and_preserves_previous_raw(self):
  self.event();backup=self.store.backup();old=self.store.path;self.event();self.assertEqual(self.store.state()['raw_events'],2);r=self.store.restore(self.store.root/'backups'/(backup['id']+'.zip'),'RESTORE_AS_NEW_BRANCH');self.assertEqual(self.store.state()['raw_events'],1);self.assertTrue(old.exists());self.assertNotEqual(old,self.store.path);self.store.integrity()
 def test_all_six_M06_JSON_and_CSV_roundtrip(self):
  self.event();self.coverage(['car','motorcycle'])
  self.event('QUEUE',observation_end=self.t(20),queue_count=0,queue_length_m=None,maximum_extent_m=None,definition='Synthetic front-to-rear snapshot',boundary_censored=True)
  self.event('TRAVEL_TIME',start_timestamp=self.t(10),end_timestamp=self.t(70),origin='A',destination='B',corridor='Synthetic corridor',route='A>B',sample_token='ANON_12345678',method='AUTHORIZED_PROBE')
  self.event('SIGNAL',signal_group='SYNTHETIC_HEAD',phase='one',green_start=self.t(0),green_end=self.t(30),yellow_start=self.t(30),yellow_end=self.t(33),red_start=self.t(33),red_end=self.t(60))
  self.event('RAILWAY',closure_id='DEMO_CLOSURE',train_id='DEMO_TRAIN',**{k:self.t(i) for i,k in enumerate(RAIL_EVENTS)})
  self.event('GEOMETRY',observation_end=self.t(20),crs='EPSG:32749',units='m',instrument='SYNTHETIC_FIXTURE',measurement_method='SOFTWARE_TEST',accuracy_m=1,survey_point=[1000,2000],source='DEMO SYNTHETIC')
  r=export_session(self.store,self.sid);self.assertFalse(r['preimport_rejected']);self.assertFalse(r['m06_rejected']);self.assertEqual(len(r['import_preview']),12);self.assertTrue(all(v['accepted'] for v in r['import_preview']));folder=self.store.root/'exports'/r['id'];rail=json.loads((folder/'railway.json').read_text())[0];self.assertEqual(len(json.loads(rail['notes'])['extra']['extra_railway_events']),10)
