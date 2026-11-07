"""Reviewed observations only; availability measures interval unions, never row counts."""
import csv,io,math,re,zipfile,xml.etree.ElementTree as ET,uuid
from functools import lru_cache
from .m13_common import *
@lru_cache(maxsize=1)
def road_catalog():return {e['id']for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']}

def default_scope():
 od=load(ROOT/'simulation/demand/m04/od-matrix.fixture.json')['movements'];pairs=[]
 for name,direction in [('northbound','NB'),('southbound','SB')]:
  ends=next(x for x in od if x['id']==name)['endpoints']['provisional'];pairs.append({'road_segment':ends['origin_edge'],'direction':direction})
 return {'name':'Dua titik monitor koridor utama NB/SB, 10 kelas, 5 parameter, seluruh 24 jam. Bukan seluruh ruas Gedangan.','pairs':pairs,'vehicle_classes':CLASSES,'parameters':METRICS,'timezone':'Asia/Jakarta','full_day_hours':24,'interval_rule':'Union of verified observed intervals per road/direction/class/parameter; count is never prorated.'}

def spreadsheet_rows(body):
 """Read XLSX cell values without calculation; reject formulas and ambiguous headers."""
 ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 with zipfile.ZipFile(io.BytesIO(body))as z:
  if sum(i.file_size for i in z.infolist())>30000000:raise ValueError('XLSX expanded file limit30MB')
  strings=[]
  if 'xl/sharedStrings.xml'in z.namelist():strings=[''.join(e.itertext())for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
  sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'));rows=[]
  for row in sheet.findall('s:sheetData/s:row',ns):
   values={}
   for cell in row.findall('s:c',ns):
    if cell.find('s:f',ns)is not None:raise ValueError('Formula cells not accepted as raw observation evidence')
    letters=re.match(r'[A-Z]+',cell.get('r','')).group();index=0
    for char in letters:index=index*26+ord(char)-64
    v=cell.find('s:v',ns);value=v.text if v is not None else ''.join(cell.find('s:is',ns).itertext())if cell.find('s:is',ns)is not None else None
    if cell.get('t')=='s'and value is not None:value=strings[int(value)]
    values[index-1]=value
   rows.append(values)
  if not rows:return []
  headers=[rows[0].get(i)for i in range(max(rows[0])+1)]
  if not all(headers)or len(set(headers))!=len(headers):raise ValueError('Blank/duplicate XLSX headers')
  return [{h:r.get(i)for i,h in enumerate(headers)}for r in rows[1:]if any(v not in [None,'']for v in r.values())]

class Store:
 def __init__(self,path=DB,test_fixture=False):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True);self.test_fixture=test_fixture
  with connect(self.path)as c:
   c.executescript('''CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY,source_type TEXT NOT NULL CHECK(source_type IN ('OBSERVED_PRIMARY','OBSERVED_SECONDARY','REFERENCE_STUDY','SIMULATION_OUTPUT','SYNTHETIC_TEST','MISSING')),name TEXT NOT NULL,location TEXT NOT NULL,url TEXT,method TEXT NOT NULL,sha256 TEXT NOT NULL,archive_path TEXT NOT NULL,created_utc TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS batches(id TEXT PRIMARY KEY,source_id TEXT REFERENCES sources(id),filename TEXT,sha256 TEXT UNIQUE,rows INTEGER,created_utc TEXT);
CREATE TABLE IF NOT EXISTS observations(id TEXT PRIMARY KEY,fingerprint TEXT UNIQUE,source_id TEXT NOT NULL REFERENCES sources(id),batch_id TEXT REFERENCES batches(id),observation_date TEXT NOT NULL,observation_time TEXT NOT NULL,time_zone TEXT NOT NULL CHECK(time_zone='Asia/Jakarta'),interval_start TEXT NOT NULL,interval_end TEXT NOT NULL,road_segment TEXT NOT NULL,direction TEXT NOT NULL,vehicle_class TEXT NOT NULL,vehicle_count INTEGER CHECK(vehicle_count IS NULL OR vehicle_count>=0),turning_movement TEXT,speed REAL CHECK(speed IS NULL OR speed>=0),queue_length REAL CHECK(queue_length IS NULL OR queue_length>=0),travel_time REAL CHECK(travel_time IS NULL OR travel_time>=0),measurement_unit TEXT NOT NULL,observation_status TEXT NOT NULL,verification_status TEXT NOT NULL,provenance_json TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS observations_date ON observations(observation_date,road_segment,direction,vehicle_class);
CREATE TABLE IF NOT EXISTS quarantine(id TEXT PRIMARY KEY,batch_id TEXT,row_number INTEGER,payload TEXT,reasons TEXT,created_utc TEXT);
CREATE TABLE IF NOT EXISTS reviews(seq INTEGER PRIMARY KEY,observation_id TEXT NOT NULL REFERENCES observations(id),decision TEXT NOT NULL CHECK(decision IN ('VERIFIED','REJECTED')),reviewer TEXT NOT NULL,note TEXT NOT NULL,evidence_checked INTEGER NOT NULL CHECK(evidence_checked=1),created_utc TEXT NOT NULL);
CREATE VIEW IF NOT EXISTS observation_records AS SELECT o.*,s.source_type,s.name AS source_name,s.location AS source_location,s.url AS source_url,s.method AS survey_method,s.sha256 AS source_sha256,COALESCE((SELECT decision FROM reviews r WHERE r.observation_id=o.id ORDER BY seq DESC LIMIT 1),o.verification_status) AS current_verification_status FROM observations o JOIN sources s ON s.id=o.source_id;''')
   for t in ['sources','batches','observations','quarantine','reviews']:
    for op in ['UPDATE','DELETE']:c.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_{t}_{op} BEFORE {op} ON {t} BEGIN SELECT RAISE(ABORT,'Append-only M13 source/observation/audit'); END")
   meta={'schema_version':'m13-1','test_fixture':test_fixture,'coverage_scope':default_scope()}
   for k,v in meta.items():c.execute('INSERT OR IGNORE INTO metadata VALUES(?,?)',(k,json.dumps(v)))
   stored=json.loads(c.execute("SELECT value FROM metadata WHERE key='test_fixture'").fetchone()[0])
   if stored!=test_fixture:raise ValueError('Test/production database boundary mismatch')
 def scope(self,filters=None):
  with connect(self.path,True)as c:
   scope=json.loads(c.execute("SELECT value FROM metadata WHERE key='coverage_scope'").fetchone()[0])
   actual=c.execute("SELECT DISTINCT road_segment,direction FROM observation_records WHERE observation_date>=? AND observation_date<=? AND source_type IN ('OBSERVED_PRIMARY','OBSERVED_SECONDARY') AND current_verification_status='VERIFIED' AND observation_status='OBSERVED' AND direction!='UNSPECIFIED'",(START.isoformat(),END.isoformat())).fetchall()
  for pair in actual:
   value=dict(pair)
   if value not in scope['pairs']:scope['pairs'].append(value)
  scope['name']='Default two NB/SB monitor points plus additional verified target measurement points; displayed scope only, not every road in Gedangan.'
  if filters:
   for key in ['road_segment','direction']:
    if filters.get(key):scope['pairs']=[p for p in scope['pairs']if p[key]==filters[key]]
   if filters.get('vehicle_class'):
    if filters['vehicle_class']not in CLASSES:raise ValueError('Unknown vehicle class')
    scope['vehicle_classes']=[filters['vehicle_class']]
   if filters.get('parameter'):
    if filters['parameter']not in METRICS:raise ValueError('Unknown parameter')
    scope['parameters']=[filters['parameter']]
  if not scope['pairs']:raise ValueError('Filter outside declared monitoring scope; no denominator invented')
  return scope
 def version(self):
  with connect(self.path,True)as c:return identity([c.execute('SELECT COUNT(*) FROM observations').fetchone()[0],c.execute('SELECT COALESCE(MAX(seq),0) FROM reviews').fetchone()[0],c.execute('SELECT COUNT(*) FROM quarantine').fetchone()[0]])[:20]
 def rows(self,date_value=None,eligible=False):
  with connect(self.path,True)as c:
   conditions=[];args=[]
   if date_value:conditions.append('observation_date=?');args.append(date_value)
   if eligible:conditions.append("source_type IN ('OBSERVED_PRIMARY','OBSERVED_SECONDARY') AND current_verification_status='VERIFIED' AND observation_status='OBSERVED'")
   return [dict(r)for r in c.execute('SELECT * FROM observation_records'+(' WHERE '+' AND '.join(conditions)if conditions else''),args)]
 def validate(self,row):
  row={k:(None if v is None or v==''else v)for k,v in row.items()};d=date.fromisoformat(str(row.get('observation_date','')))
  start=datetime.fromisoformat(str(row.get('interval_start','')));end=datetime.fromisoformat(str(row.get('interval_end','')))
  if row.get('time_zone')!='Asia/Jakarta'or start.utcoffset()!=timedelta(hours=7)or end.utcoffset()!=timedelta(hours=7):raise ValueError('Time must use Asia/Jakarta with explicit +07:00 interval')
  if start.date()!=d or not 0<(end-start).total_seconds()<=3600:raise ValueError('Inconsistent date/interval; max3600s; no invented redistribution')
  if str(row.get('observation_time'))!=start.strftime('%H:%M:%S'):raise ValueError('observation_time must match interval start HH:MM:SS')
  if row.get('road_segment')not in road_catalog():raise ValueError('Road segment not in audited existing road catalog')
  if row.get('direction')not in ['NB','SB','EB','WB','UNSPECIFIED']:raise ValueError('Unknown/missing direction')
  if row.get('vehicle_class')not in CLASSES+['truck_aggregate']:raise ValueError('Unknown/missing vehicle class')
  units=row.get('measurement_unit');units=json.loads(units)if isinstance(units,str)else units
  if not isinstance(units,dict):raise ValueError('measurement_unit must explicitly map each supplied metric to its unit')
  allowed={'vehicle_count':['vehicles/interval'],'turning_movement':['category'],'speed':['km/h','m/s'],'queue_length':['m','vehicles'],'travel_time':['s']}
  for k in METRICS:
   value=row.get(k)
   if value is None:continue
   if units.get(k)not in allowed[k]:raise ValueError('Missing/unsupported measurement unit: '+k)
   if k=='turning_movement':
    if value not in ['straight','left','right','u_turn','all_movements']:raise ValueError('Unknown turning movement')
   else:
    if isinstance(value,bool):raise ValueError('Boolean is not a measured number')
    num=float(value)
    if not math.isfinite(num)or num<0 or(k=='vehicle_count'and not num.is_integer()):raise ValueError('Invalid measured number: '+k)
    row[k]=int(num)if k=='vehicle_count'else num
  if not any(row.get(k)is not None for k in METRICS):raise ValueError('No measured parameters supplied')
  row['measurement_unit']=json.dumps(units,sort_keys=True);return row
 def import_bytes(self,filename,body,source):
  if len(body)>6000000:raise ValueError('Import limit6MB')
  required=['source_type','source_name','source_location','survey_method']
  if any(not isinstance(source.get(k),str)or not source[k].strip()for k in required)or source['source_type']not in TYPES:raise ValueError('Source type/name/location/method required')
  if not self.test_fixture and source['source_type']in TYPES[:2]and any(t in json.dumps(source).lower()for t in ['synthetic','fixture','software_test']):raise ValueError('Software test source cannot be promoted to production observations')
  if source['source_type']=='OBSERVED_SECONDARY'and not source.get('source_url'):raise ValueError('Published secondary observation requires original publication URL')
  suffix=Path(filename).suffix.lower()
  if suffix=='.csv':
   reader=csv.DictReader(io.StringIO(body.decode('utf-8-sig')))
   if not reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames):raise ValueError('Missing/duplicate CSV headers')
   rows=list(reader)
  elif suffix=='.xlsx':rows=spreadsheet_rows(body)
  elif suffix=='.json':
   rows=json.loads(body)
   if not isinstance(rows,list):raise ValueError('JSON import must be an array of observation rows')
  else:raise ValueError('Supported imports: UTF8 CSV, XLSX first sheet, JSON array; legacy databases must be explicitly mapped/exported, never merged blindly')
  if not 0<len(rows)<=20000:raise ValueError('Import requires1..20000rows')
  digest=hashlib.sha256(body).hexdigest();sid=identity({**source,'file_sha256':digest})[:24];bid=str(uuid.uuid4());archive=self.path.parent/'source_archive'/(digest+suffix);archive.parent.mkdir(parents=True,exist_ok=True)
  if archive.exists()and sha(archive)!=digest:raise ValueError('Archived source integrity failure')
  if not archive.exists():archive.write_bytes(body)
  accepted=[];bad=[]
  with connect(self.path)as c:
   if c.execute('SELECT 1 FROM batches WHERE sha256=?',(digest,)).fetchone():raise ValueError('Duplicate file content already imported')
   c.execute('INSERT OR IGNORE INTO sources VALUES(?,?,?,?,?,?,?,?,?)',(sid,source['source_type'],source['source_name'],source['source_location'],source.get('source_url'),source['survey_method'],digest,str(archive),now()))
   c.execute('INSERT INTO batches VALUES(?,?,?,?,?,?)',(bid,sid,Path(filename).name,digest,len(rows),now()))
   for i,raw in enumerate(rows,2):
    try:
     if not isinstance(raw,dict):raise ValueError('Observation row must be an object with named fields')
     if raw.get('source_type')and raw['source_type']!=source['source_type']:raise ValueError('Row source classification conflicts with source register')
     if raw.get('observation_status')and raw['observation_status']not in ['OBSERVED',source['source_type']]:raise ValueError('Row status cannot be relabeled as an observation')
     row=self.validate(raw);params={k:row.get(k)for k in METRICS};natural=[row['observation_date'],row['interval_start'],row['interval_end'],row['road_segment'],row['direction'],row['vehicle_class'],row.get('turning_movement')]
     fingerprint=identity([sid,natural,params,row['measurement_unit']])
     # Duplicate/overlapping per-metric intervals require review, never count twice.
     overlaps=c.execute('SELECT * FROM observations WHERE road_segment=? AND direction=? AND vehicle_class=? AND interval_start<? AND interval_end>?',(row['road_segment'],row['direction'],row['vehicle_class'],row['interval_end'],row['interval_start'])).fetchall()
     if any(any(row.get(k)is not None and r[k]is not None for k in METRICS)for r in overlaps):raise ValueError('Duplicate/overlapping observation metrics; explicit adjudication required')
     oid=str(uuid.uuid4());values=[row['observation_date'],row['observation_time'],'Asia/Jakarta',row['interval_start'],row['interval_end'],row['road_segment'],row['direction'],row['vehicle_class'],*params.values(),row['measurement_unit'],'OBSERVED'if source['source_type']in TYPES[:2]else source['source_type'],'PENDING_REVIEW',json.dumps({'raw_row':i,'original_filename':Path(filename).name,'file_sha256':digest,'test_database':self.test_fixture})]
     c.execute('INSERT INTO observations VALUES('+','.join('?'for _ in range(21))+')',[oid,fingerprint,sid,bid,*values]);accepted.append(oid)
    except (ValueError,TypeError,KeyError,OverflowError,sqlite3.IntegrityError)as exc:
     qid=str(uuid.uuid4());c.execute('INSERT INTO quarantine VALUES(?,?,?,?,?,?)',(qid,bid,i,json.dumps(raw,ensure_ascii=False),str(exc),now()));bad.append({'row':i,'reason':str(exc)})
  return {'batch_id':bid,'source_id':sid,'sha256':digest,'staged_ids':accepted,'quarantine':bad,'status':'PENDING_REVIEW','calendar_updated':False,'dataset_version':self.version()}
 def review(self,ids,decision,reviewer,note,evidence_checked):
  if decision not in ['VERIFIED','REJECTED']or not reviewer.strip()or not note.strip()or evidence_checked is not True:raise ValueError('Explicit reviewer, evidence check, decision and note required')
  if not ids or len(ids)>20000:raise ValueError('Review observation IDs required')
  with connect(self.path)as c:
   for oid in ids:
    row=c.execute('SELECT * FROM observation_records WHERE id=?',(oid,)).fetchone()
    if row is None:raise ValueError('Unknown staged observation')
    if decision=='VERIFIED'and row['source_type']not in TYPES[:2]:raise ValueError('Reference/simulation/test can never enter historical observation calendar')
    c.execute('INSERT INTO reviews(observation_id,decision,reviewer,note,evidence_checked,created_utc)VALUES(?,?,?,?,1,?)',(oid,decision,reviewer,note,now()))
  return {'reviewed':len(ids),'decision':decision,'dataset_version':self.version()}
 def hour(self,date_value,hour,filters=None,rows=None):
  d=date.fromisoformat(date_value)
  if not START<=d<=END or not 0<=hour<=23:raise ValueError('Outside M13 date/hour window')
  scope=self.scope(filters);rows=self.rows(date_value,True)if rows is None else rows;t=datetime.fromisoformat(f'{date_value}T{hour:02d}:00:00+07:00');end=t+timedelta(hours=1);cells=[];ids=set();sources=set()
  for pair in scope['pairs']:
   for cls in scope['vehicle_classes']:
    matching=[r for r in rows if r['road_segment']==pair['road_segment']and r['direction']==pair['direction']and r['vehicle_class']==cls]
    for metric in scope['parameters']:
     intervals=[];evidence=[]
     for r in matching:
      if r[metric]is None:continue
      a=max(t,datetime.fromisoformat(r['interval_start']));b=min(end,datetime.fromisoformat(r['interval_end']))
      if a<b:intervals.append((a,b));evidence.append({'observation_id':r['id'],'interval_start':r['interval_start'],'interval_end':r['interval_end'],'value':r[metric],'unit':json.loads(r['measurement_unit']).get(metric),'source_id':r['source_id']});ids.add(r['id']);sources.add(r['source_id'])
     finish=t;seconds=0
     for a,b in sorted(intervals):
      if b>finish:seconds+=(b-max(a,finish)).total_seconds();finish=b
     cells.append({**pair,'vehicle_class':cls,'parameter':metric,'observed_seconds':seconds,'status':'OBSERVED'if seconds==3600 else'PARTIAL'if seconds else'MISSING','evidence':evidence})
  seconds=sum(x['observed_seconds']for x in cells);status='OBSERVED'if all(x['status']=='OBSERVED'for x in cells)else'PARTIAL'if seconds else'MISSING'
  return {'date':date_value,'hour':hour,'interval_start':t.isoformat(),'interval_end':end.isoformat(),'status':status,'disabled':status=='MISSING','historical_simulation_eligible':any(x['parameter']=='vehicle_count'and x['observed_seconds']>0 for x in cells),'available_parameters':sorted({x['parameter']for x in cells if x['observed_seconds']>0}),'observations':len(ids),'source_ids':sorted(sources),'observed_cell_seconds':seconds,'expected_cell_seconds':len(cells)*3600,'missing_or_partial_cells':[x for x in cells if x['status']!='OBSERVED'],'available_cells':[x for x in cells if x['observed_seconds']>0],'scope':scope}
 def daily(self,day,filters=None):
  rows=self.rows(day,True);hours=[self.hour(day,h,filters,rows)for h in range(24)];some=any(h['status']!='MISSING'for h in hours);complete=all(h['status']=='OBSERVED'for h in hours)
  return {'date':day,'status':'COMPLETE'if complete else'PARTIAL'if some else'MISSING','color':'GREEN'if complete else'YELLOW'if some else'RED','historical_simulation_eligible':any(h['historical_simulation_eligible']for h in hours),'available_hours':[h['hour']for h in hours if h['status']!='MISSING'],'complete_hours':sum(h['status']=='OBSERVED'for h in hours),'partial_hours':sum(h['status']=='PARTIAL'for h in hours),'missing_hours':sum(h['status']=='MISSING'for h in hours),'source_ids':sorted({s for h in hours for s in h['source_ids']}),'scope':self.scope(filters),'hours':hours,'reason':'Cakupan dihitung terhadap seluruh scope dan24jam; satu jam/arah tidak menjadikan tanggal lengkap.'if some else'Tidak ada observasi terverifikasi pada tanggal dan cakupan ini. Tidak diganti data hari lain atau hasil simulasi.','dataset_version':self.version()}
 def monthly(self,month,filters=None):
  first=date.fromisoformat(month+'-01')
  if first.year!=2026 or first.month not in [8,9,10]:raise ValueError('M13 covers August through October2026')
  days=[];cursor=first
  while cursor.month==first.month:
   day=self.daily(cursor.isoformat(),filters);days.append({k:v for k,v in day.items()if k!='hours'});cursor+=timedelta(days=1)
  return {'month':month,'days':days,'scope':self.scope(filters),'dataset_version':self.version(),'test_database':self.test_fixture}
 def provenance(self):
  with connect(self.path,True)as c:return {'sources':[dict(r)for r in c.execute('SELECT * FROM sources')],'reviews':[dict(r)for r in c.execute('SELECT * FROM reviews ORDER BY seq')],'quarantine_count':c.execute('SELECT COUNT(*) FROM quarantine').fetchone()[0]}
 def dimensions(self,dimension):
  if dimension not in ['road_segment','direction','vehicle_class']:raise ValueError('Unknown coverage dimension')
  counts={}
  for r in self.rows(eligible=True):
   if START.isoformat()<=r['observation_date']<=END.isoformat():
    item=counts.setdefault(r[dimension],{'records':0,'dates':set(),'source_ids':set()});item['records']+=1;item['dates'].add(r['observation_date']);item['source_ids'].add(r['source_id'])
  scope=self.scope();expected=scope['vehicle_classes']if dimension=='vehicle_class'else sorted({p[dimension]for p in scope['pairs']})
  for key in expected:counts.setdefault(key,{'records':0,'dates':set(),'source_ids':set()})
  return {'dimension':dimension,'scope_note':'Expected monitoring scope plus any other actually verified source coverage; zero records means MISSING, not zero vehicles.','items':[{dimension:k,'status':'OBSERVED'if r['records']else'MISSING',**{a:sorted(v)if isinstance(v,set)else v for a,v in r.items()}}for k,r in counts.items()],'dataset_version':self.version()}
