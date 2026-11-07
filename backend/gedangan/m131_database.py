"""M13.1 separate database, unrestricted month selection, strict hourly evidence gate."""
from .m13_common import *
from .m13_database import Store as BaseStore
DB131=ROOT/'data/official/m13_1/historical_v2.sqlite';DOC131=ROOT/'documentation/m13_1'
class Store(BaseStore):
 def __init__(self,path=DB131,test_fixture=False):
  super().__init__(path,test_fixture)
  with connect(self.path)as c:
   c.execute('CREATE TABLE IF NOT EXISTS reference_aggregates(id TEXT PRIMARY KEY,source_sha256 TEXT NOT NULL,quality_class TEXT NOT NULL CHECK(quality_class IN (\'B\',\'C\')),payload TEXT NOT NULL)')
   c.execute('CREATE TABLE IF NOT EXISTS source_quality(source_id TEXT PRIMARY KEY REFERENCES sources(id),quality_class TEXT NOT NULL CHECK(quality_class IN (\'A\',\'B\',\'C\',\'D\',\'E\')),claim TEXT NOT NULL)')
   for op in ['UPDATE','DELETE']:c.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_aggregates_{op} BEFORE {op} ON reference_aggregates BEGIN SELECT RAISE(ABORT,'Immutable aggregate source evidence'); END")
   for op in ['UPDATE','DELETE']:c.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_source_quality_{op} BEFORE {op} ON source_quality BEGIN SELECT RAISE(ABORT,'Immutable source quality'); END")
 def scope(self,filters=None):
  # Reuse default declared points but add actual reviewed points from any observation year.
  with connect(self.path,True)as c:
   scope=json.loads(c.execute("SELECT value FROM metadata WHERE key='coverage_scope'").fetchone()[0]);pairs=[dict(r)for r in c.execute("SELECT DISTINCT road_segment,direction FROM observation_records WHERE source_type IN ('OBSERVED_PRIMARY','OBSERVED_SECONDARY') AND current_verification_status='VERIFIED' AND observation_status='OBSERVED' AND direction!='UNSPECIFIED'")]
  for pair in pairs:
   if pair not in scope['pairs']:scope['pairs'].append(pair)
  if filters:
   for k in ['road_segment','direction']:
    if filters.get(k):scope['pairs']=[p for p in scope['pairs']if p[k]==filters[k]]
   for k,values in [('vehicle_class',CLASSES),('parameter',METRICS)]:
    if filters.get(k):
     if filters[k]not in values:raise ValueError('Unknown scope '+k)
     scope['vehicle_classes'if k=='vehicle_class'else'parameters']=[filters[k]]
  if not scope['pairs']:raise ValueError('No declared monitoring point matches scope')
  scope['name']='M13.1 multi-year monitored scope; not complete geographic coverage';return scope
 def hour(self,date_value,hour,filters=None,rows=None):
  d=date.fromisoformat(date_value)
  if not 1900<=d.year<=2100 or not 0<=hour<=23:raise ValueError('Supported calendar1900..2100, hour0..23')
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
 def monthly(self,month,filters=None):
  first=date.fromisoformat(month+'-01')
  if not 1900<=first.year<=2100:raise ValueError('Supported calendar1900..2100')
  days=[];cursor=first
  while cursor.month==first.month:
   d=self.daily(cursor.isoformat(),filters);days.append({k:v for k,v in d.items()if k!='hours'});cursor+=timedelta(days=1)
  return {'month':month,'days':days,'scope':self.scope(filters),'dataset_version':self.version(),'test_database':self.test_fixture}
 def dimensions(self,dimension):
  if dimension not in ['road_segment','direction','vehicle_class']:raise ValueError('Unknown dimension')
  values={}
  for r in self.rows(eligible=True):
   item=values.setdefault(r[dimension],{'records':0,'dates':set(),'source_ids':set()});item['records']+=1;item['dates'].add(r['observation_date']);item['source_ids'].add(r['source_id'])
  scope=self.scope();expected=CLASSES if dimension=='vehicle_class'else{p[dimension]for p in scope['pairs']}
  for k in expected:values.setdefault(k,{'records':0,'dates':set(),'source_ids':set()})
  return {'dimension':dimension,'items':[{dimension:k,'status':'OBSERVED'if v['records']else'MISSING',**{x:sorted(y)if isinstance(y,set)else y for x,y in v.items()}}for k,v in values.items()],'dataset_version':self.version()}
 def import_bytes(self,filename,body,source):
  if source.get('source_type')in ['OBSERVED_PRIMARY','OBSERVED_SECONDARY']and source.get('quality_class')not in ['A','B']:raise ValueError('M13.1 observation imports require explicit quality_class A or B; C/D/E excluded')
  result=super().import_bytes(filename,body,source)
  with connect(self.path)as c:c.execute('INSERT INTO source_quality VALUES(?,?,?)',(result['source_id'],source.get('quality_class','C'),json.dumps(source,ensure_ascii=False)))
  return result
 def review(self,ids,decision,reviewer,note,evidence_checked):
  if decision=='VERIFIED':
   with connect(self.path,True)as c:
    for oid in ids:
     row=c.execute('SELECT q.quality_class FROM observations o JOIN source_quality q ON q.source_id=o.source_id WHERE o.id=?',(oid,)).fetchone()
     if row is None or row[0]not in ['A','B']:raise ValueError('No reviewed A/B source mapping; copied legacy/C/D/E records cannot be promoted automatically')
  return super().review(ids,decision,reviewer,note,evidence_checked)
 def reference_rows(self):
  with connect(self.path,True)as c:return [json.loads(r[0])for r in c.execute('SELECT payload FROM reference_aggregates ORDER BY id')]
 def add_aggregates(self,rows):
  with connect(self.path)as c:
   for row in rows:
    if row['quality_class']not in ['B','C']or row.get('calendar_eligible')is not False:raise ValueError('Unadmitted partial/aggregate evidence must stay excluded from hourly calendar')
    c.execute('INSERT OR IGNORE INTO reference_aggregates VALUES(?,?,?,?)',(identity(row),row['source_sha256'],row['quality_class'],json.dumps(row,ensure_ascii=False,allow_nan=False)))
 def archive_months(self):
  observed=sorted({r['observation_date'][:7]for r in self.rows(eligible=True)});aggregates=sorted({r['observation_date'][:7]for r in self.reference_rows()if r.get('observation_date')})
  return {'verified_observation_months':observed,'reference_aggregate_months':aggregates,'unverified_source_months':sorted({r['observation_date'][:7]for r in self.rows()if r['current_verification_status']!='VERIFIED'}),'all_months_selectable':'1900-01..2100-12','aggregates_activate_historical_hours':False}
def initialize():
 DOC131.mkdir(parents=True,exist_ok=True);DB131.parent.mkdir(parents=True,exist_ok=True)
 if not DB131.exists():
  original=sha(DB)
  with connect(DB,True)as source,connect(DB131)as target:source.backup(target)
  save(DOC131/'database-origin.json',{'source':str(DB.relative_to(ROOT)),'original_sha256':original,'copy_method':'SQLite read-only backup into new M13.1 database','original_unchanged':sha(DB)==original,'created_utc':now()})
 return Store()
