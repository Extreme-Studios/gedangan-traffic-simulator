"""Local transactional survey store. Raw events and audit history are append-only."""
import sqlite3,json,threading,uuid,os,shutil,zipfile,hashlib
from pathlib import Path
from contextlib import contextmanager
from datetime import timedelta
from .m04_demand import ROOT,load
from .m085_provenance import now,clock,canonical,fingerprint,identifier,number,text,SOURCES,interval
from .m085_video_annotation import validate_media,observation_time,anonymous_token
DATA=ROOT/'data/surveys/m085';CLASSES=['motorcycle','car','pickup_van','minibus','bus','light_truck','medium_truck','heavy_truck','trailer','oversize'];MOVEMENTS=['straight','left','right','other_legal','unknown'];TRAINING=['classification','clock_sync','coverage','duplicate_control','privacy_safety'];RAIL_EVENTS=['warning_starts','barrier_begins_closing','road_fully_closed','train_approaches','train_arrives','train_passes','train_clears','barrier_begins_reopening','barrier_fully_opens','road_traffic_released']
def uid():return str(uuid.uuid4())
def decode(row):return json.loads(row['body'])
def privacy_payload(value):
 if isinstance(value,dict):
  forbidden={'video_data','video_bytes','frame_data','frame_bytes','frames','base64','license_plate','driver_identity','face_embedding'}
  return {k:('[REDACTED_FORBIDDEN_CONTENT]' if k.lower() in forbidden else privacy_payload(v)) for k,v in value.items()}
 if isinstance(value,list):return [privacy_payload(v) for v in value]
 if isinstance(value,str) and value.startswith('data:'):return '[REDACTED_FORBIDDEN_CONTENT]'
 return value
class ClosingConnection(sqlite3.Connection):
 def __exit__(self,*args):
  try:return super().__exit__(*args)
  finally:self.close()
class SurveyStore:
 def __init__(self,root=DATA,synthetic_only=False):
  self.synthetic_only=synthetic_only;self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True);self.lock=threading.RLock();self.pointer=self.root/'active-db.json'
  if not self.pointer.exists():self.pointer.write_text(canonical({'file':'survey.sqlite'}),encoding='utf-8')
  self.initialize()
 @property
 def path(self):
  name=json.loads(self.pointer.read_text())['file'];p=(self.root/name).resolve()
  if not p.is_relative_to(self.root.resolve()):raise ValueError('Invalid workspace pointer')
  return p
 def connect(self):
  c=sqlite3.connect(self.path,timeout=15,factory=ClosingConnection);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA journal_mode=WAL');c.execute('PRAGMA synchronous=FULL');return c
 @contextmanager
 def transaction(self):
  with self.lock:
   c=self.connect()
   try:c.execute('BEGIN IMMEDIATE');yield c;c.commit()
   except Exception:c.rollback();raise
   finally:c.close()
 def initialize(self):
  with self.connect() as c:
   c.executescript('''CREATE TABLE IF NOT EXISTS objects(id TEXT PRIMARY KEY,kind TEXT NOT NULL,body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS versions(seq INTEGER PRIMARY KEY,object_id TEXT,kind TEXT,body TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS raw_events(id TEXT PRIMARY KEY,session_id TEXT,type TEXT,body TEXT,sha256 TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS corrections(id TEXT PRIMARY KEY,event_id TEXT REFERENCES raw_events(id),body TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS current_events(id TEXT PRIMARY KEY,session_id TEXT,type TEXT,body TEXT,active INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS current_session ON current_events(session_id,type,active);
CREATE TABLE IF NOT EXISTS commands(id TEXT PRIMARY KEY,request_hash TEXT NOT NULL,result TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS rejected_commands(id TEXT PRIMARY KEY,command_id TEXT,action TEXT,body TEXT,reason TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS audit(seq INTEGER PRIMARY KEY,created_at TEXT,action TEXT,object_id TEXT,payload_hash TEXT,previous_hash TEXT,hash TEXT);
''')
   for table in ['raw_events','corrections','audit','versions','commands','rejected_commands']:
    for op in ['UPDATE','DELETE']:c.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_{table}_{op} BEFORE {op} ON {table} BEGIN SELECT RAISE(ABORT,'Immutable raw/audit record'); END")
   if not c.execute("SELECT 1 FROM objects WHERE kind='location'").fetchone():
    for p in load(ROOT/'documentation/m06/survey-plan.json'):
     value={**p,'id':p['location_id'],'status':'PLANNED','field_coordinates':None,'camera_position':None,'physical_verified':False,'latest_recon':None};self.put(c,'location',value['id'],value)
    self.put(c,'settings','settings',{'id':'settings','version':'m085-1','interval_seconds':900,'review_relative_difference':.1,'review_threshold_basis':'Illustrative review trigger, not a universal agreement standard','retention_days':None,'privacy':'Local references/hash/annotations only; no face, plate, driver identity or cloud upload','shortcuts':{str((i+1)%10):v for i,v in enumerate(CLASSES)}})
 def audit(self,c,action,key,payload):
  old=c.execute('SELECT hash FROM audit ORDER BY seq DESC LIMIT 1').fetchone();prev=old[0] if old else '0'*64;t=now();h=fingerprint([t,action,key,fingerprint(payload),prev]);c.execute('INSERT INTO audit(created_at,action,object_id,payload_hash,previous_hash,hash) VALUES(?,?,?,?,?,?)',(t,action,key,fingerprint(payload),prev,h))
 def put(self,c,kind,key,value):
  encoded=canonical(value);c.execute('INSERT INTO objects VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET kind=excluded.kind,body=excluded.body',(key,kind,encoded));c.execute('INSERT INTO versions(object_id,kind,body,created_at) VALUES(?,?,?,?)',(key,kind,encoded,now()));self.audit(c,kind.upper()+'_VERSION',key,value);return value
 def get(self,c,key,kind=None):
  row=c.execute('SELECT * FROM objects WHERE id=?',(key,)).fetchone()
  if not row or (kind and row['kind']!=kind):raise ValueError('Record tidak ditemukan: '+str(key))
  return decode(row)
 def objects(self,c,kind):return [decode(r) for r in c.execute('SELECT body FROM objects WHERE kind=? ORDER BY rowid',(kind,))]
 def events(self,c,sid,active=True):
  return [{'event_id':r['id'],'type':r['type'],**decode(r)} for r in c.execute('SELECT * FROM current_events WHERE session_id=?'+(' AND active=1' if active else '')+' ORDER BY rowid',(sid,))]
 def content_hash(self,c,sid):
  s=self.get(c,sid,'session');keys=['id','location_id','observer_id','source_class','start','end','direction','approach','camera_id','method','media_id'];media=self.get(c,s['media_id'],'media') if s.get('media_id') else None
  return fingerprint({'session':{k:s.get(k) for k in keys},'events':self.events(c,sid),'media':media})
 def invalidate(self,c,s):
  if s.get('review'):self.put(c,'session',s['id'],{**s,'review':None,'status':'NEEDS_REVIEW'})
 def record(self,c,s,event_type,p,event_id):
  if c.execute('SELECT 1 FROM raw_events WHERE id=?',(event_id,)).fetchone():raise ValueError('Event ID sudah ada; gunakan command ID yang sama untuk retry')
  body={**p,'session_id':s['id'],'observer_id':s['observer_id'],'source_class':s['source_class'],'observation_method':'VIDEO_ASSISTED_MANUAL' if p.get('media_id') else s['method'],'quality_flag':p.get('quality_flag') or 'UNREVIEWED','created_at':now()};self.validate_event(c,s,event_type,body)
  c.execute('INSERT INTO raw_events VALUES(?,?,?,?,?,?)',(event_id,s['id'],event_type,canonical(body),fingerprint(body),now()));c.execute('INSERT INTO current_events VALUES(?,?,?,?,1)',(event_id,s['id'],event_type,canonical(body)));self.audit(c,'EVENT_'+event_type,event_id,body);self.invalidate(c,s);return {'event_id':event_id,'saved':True}
 def validate_event(self,c,s,kind,p,exclude_id=None):
  if kind not in ['COUNT','QUEUE','TRAVEL_TIME','SIGNAL','RAILWAY','GEOMETRY','NOTE','INCIDENT','COVERAGE']:raise ValueError('Jenis pengamatan tidak dikenal')
  if not exclude_id and kind not in ['NOTE','COVERAGE'] and s['status']!='IN_PROGRESS':raise ValueError('Mulai sesi sebelum mencatat; sesi selesai hanya dapat dikoreksi melalui ledger')
  if not exclude_id and s.get('paused') and kind not in ['NOTE','INCIDENT','COVERAGE']:raise ValueError('Sesi dijeda; resume sebelum pencatatan')
  if p.get('confidence','UNKNOWN') not in ['HIGH','MEDIUM','LOW','UNKNOWN']:raise ValueError('Confidence tidak valid')
  if p.get('vehicle_class','all') not in CLASSES+['all']:raise ValueError('Kelas kendaraan bukan registry M04')
  if p.get('movement','straight') not in MOVEMENTS:raise ValueError('Gerakan belum dikenali; pilih unknown bila tidak terlihat')
  if p.get('media_id'):
   media=self.get(c,p['media_id'],'media')
   if s.get('media_id')!=media['id']:raise ValueError('Video tidak terhubung ke sesi ini')
   mapped=observation_time(media,p.get('video_seconds'));p['timestamp']=mapped;p['time_status']='KNOWN_RECORDING_CLOCK' if mapped else 'VIDEO_TIME_ONLY'
  else:
   clock(p.get('timestamp'));p['time_status']='EXPLICIT_JAKARTA_CLOCK'
  if p.get('timestamp'):
   t=clock(p['timestamp'])
   if not clock(s['start'])<=t<=clock(s['end']):raise ValueError('Timestamp di luar jendela sesi')
   p['interval_start'],p['interval_end']=interval(p['timestamp'])
  else:
   sec=p['video_seconds'];p['interval_start']='VIDEO:'+str(int(sec//900)*900);p['interval_end']='VIDEO:'+str((int(sec//900)+1)*900)
  if kind=='COUNT':
   if p.get('vehicle_class') not in CLASSES:raise ValueError('Pilih satu dari10 kategori M04')
   for key in ['approach','direction','movement','lane_group']:text(p.get(key),key)
   if p.get('media_id'):
    anonymous_token(p.get('vehicle_token'))
    for row in c.execute("SELECT id,body FROM current_events WHERE type='COUNT' AND active=1 AND json_extract(body,'$.observer_id')=?",(s['observer_id'],)):
     old=decode(row)
     if not old.get('media_id') or row['id']==exclude_id:continue
     original=self.get(c,old['media_id'],'media')
     if original['sha256']==media['sha256']:
      if old.get('vehicle_token')==p['vehicle_token']:raise ValueError('Token kendaraan sudah dihitung; koreksi melalui ledger, bukan count baru')
      if p['video_seconds']<=old.get('video_seconds',-1) and not p.get('distinct_vehicle_reason'):raise ValueError('Replay/rewind: konfirmasi kendaraan berbeda yang belum dihitung; alasan dicatat di audit')
  if kind=='QUEUE':
   for key in ['queue_count','queue_length_m','maximum_extent_m','duration_s']:number(p.get(key),key)
   if p.get('queue_count') is not None and not isinstance(p['queue_count'],int):raise ValueError('Queue count harus integer kendaraan')
   if p.get('queue_length_m') is not None:
    number(p.get('reference_distance_m'),'Jarak referensi',minimum=.001,nullable=False)
    if not (p.get('length_basis_verified') and p.get('reference_evidence')):raise ValueError('Meter membutuhkan reference distance dan bukti terukur/terverifikasi; tanpa itu LENGTH NOT MEASURED')
   if p.get('boundary_censored') not in [True,False]:raise ValueError('Nyatakan boundary censoring secara eksplisit')
   text(p.get('definition'),'Definisi queue');text(p.get('lane_group'),'Lane group')
  if kind=='TRAVEL_TIME':
   for key in ['origin','destination','corridor','route','sample_token']:text(p.get(key),key)
   anonymous_token(p['sample_token'])
   if p.get('media_id') and p.get('video_start_s') is not None and p.get('video_end_s') is not None:
    a,b=p['video_start_s'],p['video_end_s'];number(a,'Awal perjalanan video',nullable=False);number(b,'Akhir perjalanan video',nullable=False)
    if not 0<=a<=b<=media['duration_s']:raise ValueError('Window travel time video tidak valid')
    p['start_timestamp']=observation_time(media,a);p['end_timestamp']=observation_time(media,b);p['travel_time_s']=b-a
   else:
    a,b=clock(p['start_timestamp']),clock(p['end_timestamp'])
    if b<a:raise ValueError('Waktu akhir perjalanan mendahului awal')
    p['travel_time_s']=(b-a).total_seconds()
   if p.get('method') not in ['AUTHORIZED_PROBE','LOCAL_GPS','ANONYMOUS_TWO_OBSERVERS','VIDEO_ANONYMOUS_ENDPOINTS']:raise ValueError('Metode travel time tidak didukung')
  if kind=='SIGNAL':
   text(p.get('signal_group'),'Signal group');text(p.get('phase'),'Phase')
   previous=None
   for key in ['green_start','green_end','yellow_start','yellow_end','red_start','red_end']:
    value=p.get(key)
    if value is not None:
     t=clock(value)
     if previous and t<previous:raise ValueError('Urutan warna sinyal tidak kronologis')
     previous=t
   number(p.get('offset_s'),'Offset',minimum=-86400)
  if kind=='RAILWAY':
   text(p.get('closure_id'),'Closure ID');text(p.get('train_id'),'Train token');previous=None
   for key in RAIL_EVENTS:
    if p.get(key) is not None:
     t=clock(p[key])
     if previous and t<previous:raise ValueError('Urutan kejadian palang/kereta tidak kronologis')
     previous=t
   for train in p.get('additional_train_movements',[]):
    text(train.get('train_id'),'Additional train token');values=[clock(train[k]) for k in ['train_approaches','train_arrives','train_passes','train_clears'] if train.get(k)]
    if values!=sorted(values):raise ValueError('Urutan additional train movement tidak kronologis')
  if kind in ['SIGNAL','RAILWAY'] and p.get('media_id'):
   keys=RAIL_EVENTS if kind=='RAILWAY' else ['green_start','green_end','yellow_start','yellow_end','red_start','red_end'];values=[]
   for key in keys:
    sec=p.get('video_event_seconds',{}).get(key)
    if sec is not None:
     number(sec,key,nullable=False)
     if sec>media['duration_s']:raise ValueError('Event melewati video')
     values.append(sec)
   if values!=sorted(values):raise ValueError('Urutan event video tidak kronologis')
  if kind=='GEOMETRY':
   for key in ['crs','units','instrument','measurement_method','source']:text(p.get(key),key)
   if p['units']!='m':raise ValueError('Ukuran geometri lapangan memakai meter; koordinat mengikuti CRS eksplisit')
   number(p.get('accuracy_m'),'Akurasi',nullable=False);coords=p.get('survey_point')
   if not isinstance(coords,list) or len(coords) not in [2,3] or not all(isinstance(x,(int,float)) and not isinstance(x,bool) for x in coords):raise ValueError('Koordinat pengukuran wajib tersedia')
   canonical(coords)
   if p['crs']=='EPSG:4326' and (abs(coords[0])>180 or abs(coords[1])>90):raise ValueError('Koordinat EPSG:4326 di luar rentang longitude/latitude')
   for key in ['lane_width_m','storage_length_m','crossing_angle_deg','clearance_m']:number(p.get(key),key)
   for key in ['lane_count','verified_track_count']:
    if p.get(key) is not None and (not isinstance(p[key],int) or isinstance(p[key],bool) or p[key]<1):raise ValueError('Jumlah lajur/track harus integer positif atau NULL')
  for key in ['observation_end','start_timestamp','end_timestamp',*RAIL_EVENTS,'green_start','green_end','yellow_start','yellow_end','red_start','red_end']:
   if p.get(key) is not None and not clock(s['start'])<=clock(p[key])<=clock(s['end']):raise ValueError('Waktu kejadian di luar sesi: '+key)
  if p.get('observation_end') and p.get('timestamp') and clock(p['observation_end'])<clock(p['timestamp']):raise ValueError('Akhir pengamatan mendahului awal')
  if kind=='COVERAGE':
   if p.get('coverage_status') not in ['COMPLETE','PARTIAL','MISSING']:raise ValueError('Status coverage tidak valid')
   if not p.get('classes') or any(v not in CLASSES for v in p['classes']):raise ValueError('Nyatakan kelas yang benar-benar ditinjau')
   if p['coverage_status']=='COMPLETE' and s.get('pause_windows') and not p.get('media_id'):raise ValueError('Ada gap pause: interval manual tidak boleh diklaim lengkap; gunakan PARTIAL')
   if p.get('coverage_start') or p.get('coverage_end'):
    a,b=clock(p['coverage_start']),clock(p['coverage_end'])
    if not clock(s['start'])<=a<b<=clock(s['end']):raise ValueError('Coverage di luar periode sesi')
    if p['coverage_status']=='COMPLETE' and s['source_class']!='SYNTHETIC_TEST' and b>clock(now()):raise ValueError('Coverage masa depan belum diamati')
   if p.get('media_id'):
    number(p.get('review_start_s'),'Awal review video',nullable=False);number(p.get('review_end_s'),'Akhir review video',nullable=False)
    if not 0<=p['review_start_s']<p['review_end_s']<=media['duration_s']:raise ValueError('Rentang video yang direview tidak valid')
 def summary(self,c,sid):
  rows=c.execute("SELECT json_extract(body,'$.vehicle_class') cls,json_extract(body,'$.movement') movement,json_extract(body,'$.direction') direction,json_extract(body,'$.lane_group') lane,CASE WHEN json_extract(body,'$.media_id') IS NOT NULL THEN 'VIDEO:' || CAST(CAST(json_extract(body,'$.video_seconds')/900 AS INTEGER)*900 AS INTEGER) ELSE json_extract(body,'$.interval_start') END interval_start,COUNT(*) count FROM current_events WHERE session_id=? AND type='COUNT' AND active=1 GROUP BY cls,movement,direction,lane,interval_start",(sid,)).fetchall();return [dict(r) for r in rows]
 def state(self):
  with self.lock,self.connect() as c:return {'version':'m085-1','locations':self.objects(c,'location'),'observers':self.objects(c,'observer'),'sessions':self.objects(c,'session'),'media':self.objects(c,'media'),'settings':self.get(c,'settings'),'observed_data_status':'NOT YET COLLECTED' if not c.execute("SELECT 1 FROM current_events WHERE active=1 AND json_extract(body,'$.source_class') IN ('OBSERVED_FIELD','VIDEO_OBSERVATION') LIMIT 1").fetchone() else 'RAW_UNREVIEWED_OR_REVIEWED — NOT EMPIRICAL CALIBRATION','empirical_baseline':'BLOCKED — DATA REQUIRED','M09_started':False,'storage':'LOCAL_SQLITE_WAL','database_file':self.path.name,'raw_events':c.execute('SELECT COUNT(*) FROM raw_events').fetchone()[0],'session_recovery':True,'automatic_detection':False}
 def ledger(self,sid,offset=0,limit=50):
  if offset<0 or not 1<=limit<=100:raise ValueError('Pagination di luar batas')
  with self.lock,self.connect() as c:
   s=self.get(c,sid,'session');rows=c.execute('SELECT * FROM current_events WHERE session_id=? ORDER BY rowid DESC LIMIT ? OFFSET ?',(sid,limit,offset)).fetchall();return {'session':s,'summary':self.summary(c,sid),'events':[{'event_id':r['id'],'type':r['type'],'active':bool(r['active']),**decode(r)} for r in rows],'total':c.execute('SELECT COUNT(*) FROM current_events WHERE session_id=?',(sid,)).fetchone()[0],'offset':offset,'limit':limit}
 def command(self,action,p,command_id):
  identifier(command_id);p=json.loads(canonical(p))
  try:
   if privacy_payload(p)!=p:raise ValueError('Video/frame bytes dan identitas pengemudi tidak boleh disimpan; hanya metadata dan token anonim')
   with self.transaction() as c:
    old=c.execute('SELECT result,request_hash FROM commands WHERE id=?',(command_id,)).fetchone();request_hash=fingerprint([action,p])
    if old:
     if old['request_hash']!=request_hash:raise ValueError('Command ID dipakai ulang untuk payload berbeda; input tidak dihilangkan diam-diam')
     return json.loads(old['result'])
    result=self.apply(c,action,p);c.execute('INSERT INTO commands VALUES(?,?,?)',(command_id,request_hash,canonical(result)));self.audit(c,'COMMAND_COMMIT',command_id,{'request_hash':request_hash,'result_hash':fingerprint(result)});return result
  except Exception as e:
   with self.transaction() as c:
    safe=privacy_payload(p);rid=uid();body={'command_id':command_id,'action':action,'payload':safe,'reason':str(e)};c.execute('INSERT INTO rejected_commands VALUES(?,?,?,?,?,?)',(rid,command_id,action,canonical(safe),str(e),now()));self.audit(c,'REJECTED_COMMAND',rid,body)
   raise
 def apply(self,c,action,p):
  if action=='observer_save':
   key=identifier(p.get('id') or uid());text(p.get('name'),'Alias observer')
   if not set(p.get('roles',[]))<=set(['OBSERVER','REVIEWER']):raise ValueError('Role tidak valid')
   return self.put(c,'observer',key,{**p,'id':key,'training_complete':set(TRAINING)<=set(p.get('training',[]))})
  if action=='settings_save':
   old=self.get(c,'settings');keys=p.get('shortcuts',old['shortcuts']);values=list(keys.values())
   if len(keys)!=10 or len(set(values))!=10 or set(values)!=set(CLASSES) or any(len(k)!=1 for k in keys):raise ValueError('Sepuluh shortcut unik wajib memetakan sepuluh kelas M04')
   threshold=p.get('review_relative_difference',old['review_relative_difference']);number(threshold,'Threshold review',nullable=False)
   return self.put(c,'settings','settings',{**old,**p,'shortcuts':keys,'interval_seconds':900})
  if action=='recon_save':
   loc=self.get(c,p['location_id'],'location');actor=self.get(c,p['observer_id'],'observer')
   if p.get('source_class') not in ['OBSERVED_FIELD','SYNTHETIC_TEST']:raise ValueError('Nyatakan sumber reconnaissance')
   if self.synthetic_only and p['source_class']!='SYNTHETIC_TEST':raise ValueError('Workspace pengujian sintetis tidak menerima bukti field')
   key=uid();value={**p,'id':key,'recorded_at':now()};self.put(c,'recon',key,value)
   if p['source_class']=='OBSERVED_FIELD':self.put(c,'location',loc['id'],{**loc,'status':'NEEDS_RECONNAISSANCE','latest_recon':key,'physical_verified':False})
   return value
  if action=='location_status':
   loc=self.get(c,p['location_id'],'location');reviewer=self.get(c,p['reviewer'],'observer');status=p['status'];text(p.get('reason'),'Alasan perubahan status')
   if status not in ['PLANNED','NEEDS_RECONNAISSANCE','FIELD_VERIFIED','APPROVED_FOR_SURVEY','INACTIVE']:raise ValueError('Status lokasi tidak dikenal')
   if status in ['FIELD_VERIFIED','APPROVED_FOR_SURVEY']:
    recon=self.get(c,loc.get('latest_recon'),'recon')
    if recon['source_class']!='OBSERVED_FIELD' or not p.get('confirm_field_evidence') or 'REVIEWER' not in reviewer.get('roles',[]):raise ValueError('Verifikasi lokasi memerlukan reviewer dan konfirmasi bukti lapangan, bukan demo')
    for key in ['field_visit_date','evidence_reference','measurement_method','crs','observation_direction','visibility','safe_position_notes']:text(recon.get(key),key)
    coords=recon.get('field_coordinates')
    if not isinstance(coords,list) or len(coords)!=2:raise ValueError('Koordinat lapangan belum diukur')
    for x in coords:number(x,'Koordinat',minimum=-1e10,nullable=False)
    if recon['crs']=='EPSG:4326' and (abs(coords[0])>180 or abs(coords[1])>90):raise ValueError('Koordinat longitude/latitude di luar batas')
    number(recon.get('accuracy_m'),'Akurasi koordinat',nullable=False)
    if not recon.get('safe_observer_position') or not recon.get('legal_recording_permission'):raise ValueError('Posisi aman dan izin harus dikonfirmasi')
    if status=='APPROVED_FOR_SURVEY' and loc['status']!='FIELD_VERIFIED':raise ValueError('FIELD_VERIFIED harus ditinjau sebelum persetujuan survei')
   return self.put(c,'location',loc['id'],{**loc,'status':status,'physical_verified':status in ['FIELD_VERIFIED','APPROVED_FOR_SURVEY'],'reviewer':reviewer['id'],'reason':p['reason'],'field_coordinates':recon['field_coordinates'] if status in ['FIELD_VERIFIED','APPROVED_FOR_SURVEY'] else loc.get('field_coordinates')})
  if action=='session_save':
   key=identifier(p.get('id') or uid());self.get(c,p['location_id'],'location');self.get(c,p['observer_id'],'observer');start,end=clock(p['start']),clock(p['end'])
   if start>=end or (end-start).total_seconds()>86400:raise ValueError('Jendela sesi harus positif, maksimal24 jam')
   if p.get('source_class') not in SOURCES:raise ValueError('Source classification tidak valid')
   if self.synthetic_only and p['source_class']!='SYNTHETIC_TEST':raise ValueError('Workspace pengujian sintetis tidak menerima pengamatan field')
   for field in ['direction','approach','method']:text(p.get(field),field)
   old=c.execute('SELECT body FROM objects WHERE id=? AND kind=?',(key,'session')).fetchone()
   if old and c.execute('SELECT 1 FROM raw_events WHERE session_id=?',(key,)).fetchone():raise ValueError('Parameter sesi yang sudah mempunyai raw events tidak dapat ditimpa; buat sesi/revisi terpisah')
   return self.put(c,'session',key,{**p,'id':key,'status':'PLANNED','paused':False,'pause_windows':[],'review':None,'timezone':'Asia/Jakarta','created_at':now()})
  if action=='session_status':
   s=self.get(c,p['session_id'],'session');status=p['status']
   if status not in ['PLANNED','RECONNAISSANCE','READY','IN_PROGRESS','COMPLETED','NEEDS_REVIEW']:raise ValueError('Approval menggunakan proses review terpisah')
   if status in ['READY','IN_PROGRESS'] and s['source_class']!='SYNTHETIC_TEST':
    loc=self.get(c,s['location_id'],'location');observer=self.get(c,s['observer_id'],'observer')
    if loc['status']!='APPROVED_FOR_SURVEY' or not observer['training_complete']:raise ValueError('Reconnaissance/izin lokasi dan latihan observer belum lengkap')
   if status=='IN_PROGRESS' and s['status'] not in ['READY','IN_PROGRESS']:raise ValueError('Tinjau kesiapan sesi dahulu')
   return self.put(c,'session',s['id'],{**s,'status':status,'started_at':s.get('started_at') or (now() if status=='IN_PROGRESS' else None)})
  if action=='pause':
   s=self.get(c,p['session_id'],'session');t=clock(p.get('timestamp') or now()).isoformat();windows=s.get('pause_windows',[])
   if p['paused'] and not s.get('paused'):windows=windows+[{'start':t,'end':None}]
   elif not p['paused'] and s.get('paused'):windows=[*windows[:-1],{**windows[-1],'end':t}]
   return self.put(c,'session',s['id'],{**s,'paused':bool(p['paused']),'pause_windows':windows,'review':None})
  if action=='media_register':
   media=validate_media(p);key=identifier(p.get('id') or uid())
   old=c.execute('SELECT 1 FROM objects WHERE id=?',(key,)).fetchone()
   if old:raise ValueError('Media ID sudah terdaftar; metadata sumber immutable, daftar revisi baru bila koreksi diperlukan')
   return self.put(c,'media',key,{**media,'id':key,'registered_at':now(),'retention_status':'ACTIVE'})
  if action=='media_attach':
   s=self.get(c,p['session_id'],'session');m=self.get(c,p['media_id'],'media')
   if s['source_class'] not in ['VIDEO_OBSERVATION','SYNTHETIC_TEST'] or m.get('kind')=='PHOTO':raise ValueError('Gunakan sesi VIDEO_OBSERVATION untuk anotasi rekaman; foto hanya referensi reconnaissance')
   if s['source_class']=='VIDEO_OBSERVATION' and not m.get('permission_confirmed'):raise ValueError('Hak/izin rekaman belum dikonfirmasi')
   if c.execute('SELECT 1 FROM raw_events WHERE session_id=?',(s['id'],)).fetchone():raise ValueError('Pasang video sebelum annotation agar clock tidak berubah diam-diam')
   return self.put(c,'session',s['id'],{**s,'media_id':m['id'],'camera_id':m.get('camera_id'),'method':'VIDEO_ASSISTED_MANUAL','review':None})
  if action=='media_clock_review':
   m=self.get(c,p['media_id'],'media');reviewer=self.get(c,p['reviewer'],'observer');clock(p['recording_start']);number(p.get('clock_offset_s',0),'Offset clock',minimum=-86400,nullable=False);text(p.get('evidence_reference'),'Bukti clock video')
   if 'REVIEWER' not in reviewer.get('roles',[]) or not p.get('confirmed_recording_clock'):raise ValueError('Clock yang diketahui kemudian membutuhkan konfirmasi bukti dan reviewer')
   value={**m,'recording_start':p['recording_start'],'clock_offset_s':p.get('clock_offset_s',0),'time_status':'REVIEWED_CLOCK_MAPPING','clock_mapping_evidence':p,'original_clock_preserved_in_versions':True};self.put(c,'media',m['id'],value)
   for s in self.objects(c,'session'):
    if s.get('media_id')==m['id']:
     a,b=p.get('session_window_start') or s['start'],p.get('session_window_end') or s['end'];clock(a);clock(b);begin=clock(observation_time(value,0));end=clock(observation_time(value,value['duration_s']))
     if not clock(a)<=begin<end<=clock(b):raise ValueError('Sediakan window sesi sesuai clock video terverifikasi; raw lama tidak diubah')
     self.put(c,'session',s['id'],{**s,'start':a,'end':b,'review':None,'status':'NEEDS_REVIEW' if s.get('review') else s['status'],'time_mapping_reviewer':reviewer['id'],'original_window_preserved_in_versions':True})
   return value
  if action=='media_detach':
   m=self.get(c,p['media_id'],'media');text(p.get('reason'),'Alasan retention');self.audit(c,'MEDIA_REFERENCE_RETIRED',m['id'],p)
   return self.put(c,'media',m['id'],{**m,'retention_status':'REFERENCE_RETIRED','retired_at':now(),'retention_reason':p['reason'],'original_file_deleted_by_application':False})
  if action=='event_add':
   s=self.get(c,p['session_id'],'session');return self.record(c,s,p['type'],p['data'],identifier(p.get('event_id') or uid()))
  if action in ['event_correct','undo']:
   s=self.get(c,p['session_id'],'session');actor=self.get(c,p['actor'],'observer');text(p.get('reason'),'Alasan koreksi wajib tersedia')
   if action=='undo':row=c.execute('SELECT * FROM current_events WHERE session_id=? AND active=1 AND type=? ORDER BY rowid DESC LIMIT 1',(s['id'],'COUNT')).fetchone()
   else:row=c.execute('SELECT * FROM current_events WHERE id=? AND session_id=?',(p['event_id'],s['id'])).fetchone()
   if not row:raise ValueError('Tidak ada event yang dapat dikoreksi')
   old=decode(row);patch=p.get('patch',{});forbidden={'session_id','observer_id','source_class','created_at','media_id','vehicle_token'}
   if forbidden&set(patch):raise ValueError('Identitas/sumber raw tidak dapat diganti lewat koreksi')
   effective={**old,**patch};void=action=='undo' or bool(p.get('void'));self.validate_event(c,s,row['type'],effective,exclude_id=row['id'])
   effective_patch={k:v for k,v in effective.items() if k not in old or old[k]!=v};revision={'patch':effective_patch,'void':void,'reason':p['reason'],'actor':actor['id'],'duplicate_of':p.get('duplicate_of'),'prior_effective_sha256':fingerprint(old)};rid=uid();c.execute('INSERT INTO corrections VALUES(?,?,?,?)',(rid,row['id'],canonical(revision),now()));c.execute('UPDATE current_events SET body=?,active=? WHERE id=?',(canonical(effective),int(not void),row['id']));self.audit(c,'EVENT_CORRECTION',row['id'],revision);self.invalidate(c,s);return {'event_id':row['id'],'revision_id':rid,'active':not void}
  if action=='review':
   s=self.get(c,p['session_id'],'session');reviewer=self.get(c,p['reviewer'],'observer');text(p.get('reason'),'Catatan review')
   if reviewer['id']==s['observer_id'] or 'REVIEWER' not in reviewer.get('roles',[]):raise ValueError('Review memerlukan reviewer berbeda dari pencacah')
   if p.get('decision') not in ['APPROVED','NEEDS_REVIEW','REJECTED']:raise ValueError('Keputusan review tidak valid')
   if p['decision']=='APPROVED':
    if not p.get('human_reviewed'):raise ValueError('Konfirmasi human review diperlukan')
    if s['source_class']!='SYNTHETIC_TEST':
     from .m085_provenance import gate_source
     media=self.get(c,s['media_id'],'media') if s.get('media_id') else None;gate_source(s,p,media)
     if self.get(c,s['location_id'],'location')['status']!='APPROVED_FOR_SURVEY' or not p.get('evidence_reference'):raise ValueError('Bukti field/reconnaissance belum disetujui')
   review={**p,'reviewed_at':now(),'content_hash':self.content_hash(c,s['id'])};return self.put(c,'session',s['id'],{**s,'review':review,'status':p['decision']})
  if action=='qc_adjudicate':
   reviewer=self.get(c,p['reviewer'],'observer');text(p.get('reason'),'Alasan adjudikasi')
   if 'REVIEWER' not in reviewer.get('roles',[]) or p.get('selection') not in ['A','B','RECOUNT_REQUIRED']:raise ValueError('Pilih tally A/B atau recount; tidak ada rata-rata otomatis')
   from .m085_observer_qc import compare_counts
   comparison=compare_counts(self,p['session_A'],p['session_B'])
   if reviewer['id'] in [comparison['observer_A'],comparison['observer_B']] or comparison['id']!=p.get('comparison_id'):raise ValueError('Reviewer harus independen; comparison yang berubah harus dihitung ulang')
   key=uid();return self.put(c,'adjudication',key,{**p,'id':key,'created_at':now()})
  if action=='geometry_import':
   import csv,io
   s=self.get(c,p['session_id'],'session');content=text(p.get('csv_text'),'CSV GNSS');rows=list(csv.DictReader(io.StringIO(content.lstrip('\ufeff'))))
   if len(rows)>5000:raise ValueError('Impor geometri dibatasi5000 rows per transaksi')
   source_id=uid();accepted=[];rejected=[]
   for index,row in enumerate(rows):
    try:
     missing=lambda k:row.get(k) is None or row[k].strip()==''
     value={'timestamp':row.get('timestamp'),'observation_end':row.get('observation_end'),'vehicle_class':'all','crs':row.get('crs'),'units':row.get('units'),'instrument':row.get('instrument'),'measurement_method':row.get('measurement_method'),'source':row.get('source'),'accuracy_m':None if missing('accuracy_m') else float(row['accuracy_m']),'survey_point':[float(row['x']),float(row['y'])],'confidence':row.get('confidence') or 'UNKNOWN','source_document_id':source_id,'notes':row.get('notes')}
     for k in ['lane_width_m','storage_length_m','crossing_angle_deg','clearance_m']:value[k]=None if missing(k) else float(row[k])
     for k in ['lane_count','verified_track_count']:value[k]=None if missing(k) else int(row[k])
     self.validate_event(c,s,'GEOMETRY',value);accepted.append(value)
    except Exception as ex:rejected.append({'row_number':index+1,'raw':row,'reason':str(ex)})
   ids=[]
   for value in accepted:ids.append(self.record(c,s,'GEOMETRY',value,uid())['event_id'])
   value={'id':source_id,'session_id':s['id'],'filename':p.get('filename'),'original_file_sha256':p.get('sha256'),'submitted_text_sha256':hashlib.sha256(content.encode()).hexdigest(),'raw_csv':content,'accepted_event_ids':ids,'rejected':rejected,'source_class':s['source_class'],'created_at':now()};self.put(c,'geometry_import',source_id,value);return {'id':source_id,'accepted':len(ids),'rejected':rejected,'raw_preserved':True,'transactional':True}
  if action=='checkpoint':
   self.audit(c,'MANUAL_CHECKPOINT',p.get('session_id','workspace'),{'actor':p.get('actor'),'at':now()});return {'saved':True,'timestamp':now(),'database':self.path.name}
  if action=='demo_create':
   observer='DEMO_OBSERVER';reviewer='DEMO_REVIEWER'
   for oid in [observer,reviewer]:self.put(c,'observer',oid,{'id':oid,'name':oid,'roles':['OBSERVER','REVIEWER'],'training':TRAINING,'training_complete':True,'source_class':'SYNTHETIC_TEST'})
   start,end=interval(now());end=(clock(start)+timedelta(hours=2)).isoformat();sid=uid();s={'id':sid,'location_id':'MAIN_NB','observer_id':observer,'source_class':'SYNTHETIC_TEST','start':start,'end':end,'direction':'northbound','approach':'MAIN_NB','method':'MANUAL_COUNT','camera_id':None,'media_id':None,'status':'IN_PROGRESS','paused':False,'pause_windows':[],'review':None,'timezone':'Asia/Jakarta','notes':'DEMO SYNTHETIC — NOT OBSERVED GEDANGAN TRAFFIC.','created_at':now()};return self.put(c,'session',sid,s)
  raise ValueError('Action tidak dikenal: '+str(action))
 def integrity(self,path=None):
  c=sqlite3.connect(path or self.path);c.row_factory=sqlite3.Row
  try:
   if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite integrity gagal')
   previous='0'*64
   for r in c.execute('SELECT * FROM audit ORDER BY seq'):
    expected=fingerprint([r['created_at'],r['action'],r['object_id'],r['payload_hash'],previous])
    if r['previous_hash']!=previous or r['hash']!=expected:raise ValueError('Audit hash chain berubah')
    previous=r['hash']
   for r in c.execute('SELECT body,sha256 FROM raw_events'):
    if fingerprint(json.loads(r['body']))!=r['sha256']:raise ValueError('Raw payload hash berubah')
   proof={(r['action'],r['object_id'],r['payload_hash']) for r in c.execute('SELECT action,object_id,payload_hash FROM audit')};effective={}
   for r in c.execute('SELECT * FROM raw_events'):
    body=json.loads(r['body'])
    if ('EVENT_'+r['type'],r['id'],fingerprint(body)) not in proof:raise ValueError('Raw event tidak mempunyai audit proof')
    effective[r['id']]={'body':body,'active':True,'session_id':r['session_id'],'type':r['type']}
   for r in c.execute('SELECT * FROM corrections ORDER BY rowid'):
    revision=json.loads(r['body']);old=effective[r['event_id']]
    if revision['prior_effective_sha256']!=fingerprint(old['body']) or ('EVENT_CORRECTION',r['event_id'],fingerprint(revision)) not in proof:raise ValueError('Correction history tidak konsisten')
    old['body']={**old['body'],**revision['patch']};old['active']=not revision['void']
   for r in c.execute('SELECT * FROM current_events'):
    expected=effective.pop(r['id'],None)
    if not expected or json.loads(r['body'])!=expected['body'] or bool(r['active'])!=expected['active'] or r['session_id']!=expected['session_id'] or r['type']!=expected['type']:raise ValueError('Projection berbeda dari immutable history')
   if effective:raise ValueError('Raw events hilang dari projection')
   for r in c.execute('SELECT * FROM objects'):
    latest=c.execute('SELECT * FROM versions WHERE object_id=? ORDER BY seq DESC LIMIT 1',(r['id'],)).fetchone()
    if not latest or latest['body']!=r['body'] or (r['kind'].upper()+'_VERSION',r['id'],fingerprint(json.loads(r['body']))) not in proof:raise ValueError('Registry tidak sesuai version history')
   for r in c.execute('SELECT * FROM versions'):
    if (r['kind'].upper()+'_VERSION',r['object_id'],fingerprint(json.loads(r['body']))) not in proof:raise ValueError('Registry version history berubah')
   if {r[0] for r in c.execute('SELECT DISTINCT object_id FROM versions')}!={r[0] for r in c.execute('SELECT id FROM objects')}:raise ValueError('Registry object hilang dari version history')
   for r in c.execute('SELECT * FROM commands'):
    if ('COMMAND_COMMIT',r['id'],fingerprint({'request_hash':r['request_hash'],'result_hash':fingerprint(json.loads(r['result']))})) not in proof:raise ValueError('Command idempotency history berubah')
   for r in c.execute('SELECT * FROM rejected_commands'):
    if ('REJECTED_COMMAND',r['id'],fingerprint({'command_id':r['command_id'],'action':r['action'],'payload':json.loads(r['body']),'reason':r['reason']})) not in proof:raise ValueError('Rejected payload history berubah')
   required={f'immutable_{t}_{op}' for t in ['raw_events','corrections','audit','versions','commands','rejected_commands'] for op in ['UPDATE','DELETE']};triggers={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='trigger'")}
   if not required<=triggers:raise ValueError('Immutable triggers hilang')
   return {'sqlite':'ok','audit_tail':previous,'raw_events':c.execute('SELECT COUNT(*) FROM raw_events').fetchone()[0],'immutable_triggers':True}
  finally:c.close()
 def backup(self):
  from .m085_baseline import digest
  with self.lock:
   folder=self.root/'backups'/uid();folder.mkdir(parents=True);db=folder/'survey.sqlite'
   with self.connect() as source,sqlite3.connect(db,factory=ClosingConnection) as target:source.backup(target)
   check=self.integrity(db);manifest={'version':'m085-1','created_at':now(),'database_sha256':digest(db),'integrity':check,'contains_original_video':False,'schema_sha256':{k:digest(ROOT/f'configuration/calibration-m06/{k}.schema.json') for k in ['traffic_count','travel_time','queue','signal','railway','geometry']}}
   (folder/'manifest.json').write_text(canonical(manifest),encoding='utf-8');archive=folder.with_suffix('.zip')
   with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in folder.iterdir():z.write(p,p.name)
   return {'id':folder.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'contains_original_video':False,'integrity':check}
 def restore(self,archive,confirmation):
  if confirmation!='RESTORE_AS_NEW_BRANCH':raise ValueError('Konfirmasi restore sebagai cabang baru diperlukan; cabang lama tetap tersimpan')
  from .m085_baseline import digest
  with self.lock:
   branch=self.root/'restored'/uid();branch.mkdir(parents=True)
   try:
    with zipfile.ZipFile(archive) as z:
     if set(z.namelist())!={'survey.sqlite','manifest.json'} or any(i.file_size>128*1024*1024 for i in z.infolist()):raise ValueError('Backup ZIP tidak valid / terlalu besar')
     for name in z.namelist():
      with z.open(name) as src,(branch/name).open('wb') as dst:shutil.copyfileobj(src,dst,1024*1024)
    manifest=json.loads((branch/'manifest.json').read_text())
    if manifest['version']!='m085-1' or digest(branch/'survey.sqlite')!=manifest['database_sha256']:raise ValueError('Checksum backup tidak cocok')
    check=self.integrity(branch/'survey.sqlite');old=str(self.path.relative_to(self.root));temp=self.pointer.with_suffix('.tmp');temp.write_text(canonical({'file':str((branch/'survey.sqlite').relative_to(self.root)),'previous_branch':old}),encoding='utf-8');os.replace(temp,self.pointer)
    with self.transaction() as c:self.audit(c,'RESTORE_NEW_BRANCH',branch.name,{'previous_branch':old,'backup_sha256':digest(archive)})
    return {'restored':True,'database':str(self.path.relative_to(self.root)),'previous_branch_preserved':old,'integrity':check}
   except Exception:
    # Invalid staging material is retained for diagnosis; the active pointer has not changed.
    raise
