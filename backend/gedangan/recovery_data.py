"""Sparse historical evidence; exact target lookup fails closed. No fabricated calendar."""
import sqlite3,math,random
from datetime import datetime,date,timedelta,time,timezone
from .recovery_common import *
DB=DATA/'historical.sqlite';STATUSES=['OBSERVED','REFERENCE_BASED_ESTIMATE','SYNTHETIC_SCENARIO','MISSING'];CLASSES=['motorcycle','car','pickup_van','minibus','bus','light_truck','medium_truck','heavy_truck','trailer','oversize']
# Table 1, p927: two weekday surveys and one Sunday. Do not copy aggregate
# three-period sum as an hourly volume; direction is not established by the table.
REFERENCE={'2023-05-09':{7:[3553,1905,36,496],12:[2989,1743,34,525],17:[3396,2073,26,396]},'2023-05-11':{7:[3323,1823,27,455],12:[2820,1642,28,499],17:[3238,1964,15,361]},'2023-05-14':{7:[2574,1517,26,412],12:[2398,1349,24,462],17:[2662,1471,13,356]}}
def initialize():
 DATA.mkdir(parents=True,exist_ok=True)
 with sqlite3.connect(DB)as c:
  c.executescript('''PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS evidence(id TEXT PRIMARY KEY,date TEXT NOT NULL,day_type TEXT NOT NULL,start_wib TEXT NOT NULL,end_wib TEXT NOT NULL,interval_s INTEGER,road_segment TEXT,direction TEXT,entry_edge TEXT,exit_edge TEXT,vehicle_class TEXT,metric TEXT,value REAL,unit TEXT,status TEXT CHECK(status IN ('OBSERVED','REFERENCE_BASED_ESTIMATE','SYNTHETIC_SCENARIO','MISSING')),source_id TEXT,source_year INTEGER,provenance_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS dataset_versions(id TEXT PRIMARY KEY,created_utc TEXT,sha256 TEXT,source_manifest TEXT);
CREATE TABLE IF NOT EXISTS experiments(id TEXT PRIMARY KEY,created_utc TEXT,request_json TEXT,status TEXT,run_path TEXT,error TEXT);
CREATE TRIGGER IF NOT EXISTS evidence_no_update BEFORE UPDATE ON evidence BEGIN SELECT RAISE(ABORT,'Evidence is immutable; add a version'); END;
CREATE TRIGGER IF NOT EXISTS evidence_no_delete BEFORE DELETE ON evidence BEGIN SELECT RAISE(ABORT,'Evidence is immutable'); END;''')
  for d,periods in REFERENCE.items():
   for hour,counts in periods.items():
    for cls,value in zip(['motorcycle','car','bus','truck_aggregate'],counts):
     row={'source_id':'REFERENCE_2023','table':'Table1 p927','source_url':'https://ejournal.undip.ac.id/index.php/ilmulingkungan/article/download/56951/pdf','spatial_scope':'Ahmad Yani area affected by Aloha construction, not a verified core-intersection count station','direction':'UNSPECIFIED in table','aggregation':'One hour; raw15-minute data unavailable','target_2026_eligible':False,'measurement_not_field_verified_by_this_project':True}
     key=identity([d,hour,cls,'REFERENCE_2023'])[:24];c.execute('INSERT OR IGNORE INTO evidence VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(key,d,'WEEKEND'if date.fromisoformat(d).weekday()>=5 else'WEEKDAY',f'{hour:02d}:00',f'{hour+1:02d}:00',3600,'AHMAD_YANI_REFERENCE_AREA','UNSPECIFIED',None,None,cls,'traffic_count',value,'vehicles/hour','OBSERVED','REFERENCE_2023',2023,json.dumps(row)))
  source=DOC/'sources/REFERENCE_2023.pdf';key=identity(REFERENCE);c.execute('INSERT OR IGNORE INTO dataset_versions VALUES(?,?,?,?)',(key,datetime.now(timezone.utc).isoformat(),sha(source)if source.exists()else'MISSING',json.dumps({'source':'REFERENCE_2023','retained_records':36,'original_scope_only':True})))
 save(DOC/'historical-schema.json',{'database':str(DB.relative_to(ROOT)),'version':'recovery-data-1','fields':['date','day_type','WIB interval','road_segment','direction','entry_edge','exit_edge','vehicle_class','metric','value','unit','status','source_id','source_year','provenance'],'statuses':STATUSES,'target_window':['2026-08-01','2026-10-31'],'target_exact_observed_records':0,'null_policy':'Missing is not zero. Sparse source records only; target dates are evaluated by coverage lookup, not populated with simulated observations.','historical_source':'2023 weekday/weekend aggregate hour counts; direction/turning/signal/railway/travel time/queue for target periods MISSING','data_quality':['No claim whole-day totals from sums of selected one-hour samples','No June14 Sunday transfer: source date/day mismatch is excluded','2022 source vehicle/skr conversion not used because original PDF403 and no verified raw full series']})
 return coverage()
def coverage():
 with sqlite3.connect(DB)as c:rows=c.execute('SELECT date,start_wib,vehicle_class,value,status FROM evidence ORDER BY date,start_wib,vehicle_class').fetchall()
 return {'target_start':'2026-08-01','target_end':'2026-10-31','days':92,'quarter_hour_slots_per_direction':92*96,'observed_2026_records':0,'reference_2023_records':len(rows),'target_status':'MISSING','reference':REFERENCE,'missing_metrics':['directional count','turning movement','signal timing','railway events','travel time','queue','entry/exit OD','15-minute sub-hour shape'],'reference_limits':['Spatial transfer from Aloha-affected Ahmad Yani area','Direction split unavailable','Publication is historical2023, not measured2026','Counts for one-hour windows only; no all-day interpolation'],'calendar_rule':'Weekday/weekend uses selected local date; holidays not inferred without a verified calendar source.'}
def calendar(req):
 d=date.fromisoformat(req['date']);t=time.fromisoformat(req['time']);hour=t.hour
 return {'date':d.isoformat(),'time_wib':t.isoformat(timespec='minutes'),'weekday':d.strftime('%A'),'day_type':'WEEKEND'if d.weekday()>=5 else'WEEKDAY','period':'MORNING'if 6<=hour<9 else'EVENING'if 16<=hour<21 else'MIDDAY'if 9<=hour<16 else'NIGHT_OFFPEAK','year':d.year,'WIB_utc_offset':'+07:00'}
def hourly(req,hour,cal):
 mode=req.get('demand_mode','EXACT_OBSERVED');flows=[]
 if mode=='EXACT_OBSERVED':
  from .recovery_observed import lookup
  from .recovery_routing import movements
  flows=lookup(DB,cal['date'],cal.get('lookup_time_wib',cal['time_wib']));known=movements()
  for f in flows:
   if f['vehicle_type_id']not in CLASSES or f['od_id']not in known or any(f[k]!=known[f['od_id']][k]for k in ['origin_edge','destination_edge']):raise ValueError('MISSING: observation endpoints/class do not match a supported reviewed OD; no substituted endpoints')
 elif mode=='REFERENCE_ESTIMATE':
  if hour not in [7,12,17]:raise ValueError('MISSING: historical source only covers07-08,12-13,17-18. No evidence to interpolate other hours automatically.')
  if req.get('acknowledge_estimate')is not True:raise ValueError('Explicit acknowledgement of historical/spatial/directional estimate assumptions required')
  samples=[v[hour]for d,v in REFERENCE.items()if('WEEKEND'if date.fromisoformat(d).weekday()>=5 else'WEEKDAY')==cal['day_type']]
  split=float(req.get('northbound_share',.5));scale=float(req.get('demand_scale',1));turn=float(req.get('turn_share',0))
  if not .3<=split<=.7 or not .5<=scale<=1.5 or not 0<=turn<=.25:raise ValueError('Declared sensitivity bounds: NB share0.3..0.7, scale0.5..1.5, turn0..0.25')
  for i,cls in enumerate(['motorcycle','car','bus','light_truck']):
   values=[s[i]for s in samples];mean=sum(values)/len(values);low=.6*min(values);high=1.4*max(values)
   for od,share in [('northbound',split),('southbound',1-split)]:
    flows.append({'od_id':od,'vehicle_type_id':cls,'veh_per_hour':mean*scale*share*(1-turn),'range_vph':[low*scale*.3*(1-turn),high*scale*.7*(1-turn)],'status':'REFERENCE_BASED_ESTIMATE','source_id':'REFERENCE_2023','assumptions':['A-TRANSFER: old adjacent spatial/context transfer, growth factor1 unless explicit scale','A-DIR: source aggregate treated as both directions; NB share is sensitivity assumption, not measured','A-TIME: uniform within the source hour; sub-hour proportions not observed',*(['A-TRUCK: generic published truck assigned light_truck only; no automatic heavy/trailer admission']if cls=='light_truck'else[])]})
   if turn:
    flows.append({'od_id':'main_to_feeder','vehicle_type_id':cls,'veh_per_hour':mean*scale*(1-split)*turn,'range_vph':None,'status':'SYNTHETIC_SCENARIO','source_id':'A-TURN-SENSITIVITY','assumptions':['Unmeasured turning fraction; carved from SB aggregate, not added free demand']})
    flows.append({'od_id':'north_to_ketajen','vehicle_type_id':cls,'veh_per_hour':mean*scale*split*turn,'range_vph':None,'status':'SYNTHETIC_SCENARIO','source_id':'A-TURN-SENSITIVITY','assumptions':['Unmeasured turning fraction; carved from NB estimate, not an observed OD']})
 elif mode=='SYNTHETIC_SCENARIO':
  if req.get('acknowledge_estimate')is not True:raise ValueError('Explicit synthetic scenario acknowledgement required')
  inputflows=req.get('flows',[])
  if not inputflows:raise ValueError('Provide explicit OD/class/veh_per_hour synthetic flows')
  for f in inputflows:
   n=float(f['veh_per_hour'])
   if not math.isfinite(n)or not 0<=n<=10000 or f['vehicle_type_id']not in CLASSES:raise ValueError('Invalid synthetic flow')
   flows.append({**f,'veh_per_hour':n,'status':'SYNTHETIC_SCENARIO','range_vph':None,'source_id':'USER_EXPLICIT_INPUT','assumptions':['Software/engineering what-if input; not observed volume']})
 else:raise ValueError('Unknown demand mode')
 allowed=req.get('vehicle_types',CLASSES)
 if not set(allowed)<=set(CLASSES):raise ValueError('Unknown vehicle class')
 return [f for f in flows if f['vehicle_type_id']in allowed]
def build_demand(req):
 cal=calendar(req);horizon=int(req.get('horizon_s',900));warm=int(req.get('warmup_s',300));seed=int(req.get('seed',42))
 if not 60<=horizon<=3600 or not 0<=warm<=1800 or not 0<=seed<=2147483647:raise ValueError('Bounded horizon60..3600s, warmup0..1800s, valid seed required')
 selected=datetime.fromisoformat(cal['date']+'T'+cal['time_wib']+':00+07:00');start=selected-timedelta(seconds=warm);end=selected+timedelta(seconds=horizon);cursor=start;ledger=[];requests=[];rng=random.Random(seed)
 # Warm-up fallback is explicit: a chosen-hour stationary initialization, not prior-hour evidence.
 while cursor<end:
  stop=min(end,(cursor.replace(minute=(cursor.minute//15)*15,second=0,microsecond=0)+timedelta(minutes=15)));elapsed=(cursor-start).total_seconds();span=(stop-cursor).total_seconds();initial=cursor<selected
  refhour=selected.hour if initial and req.get('warmup_profile','STATIONARY_SELECTED_HOUR')=='STATIONARY_SELECTED_HOUR'else cursor.hour
  lookupclock=selected if initial and req.get('warmup_profile','STATIONARY_SELECTED_HOUR')=='STATIONARY_SELECTED_HOUR'else cursor
  flows=hourly(req,refhour,{**cal,'date':lookupclock.date().isoformat(),'lookup_time_wib':lookupclock.strftime('%H:%M'),'day_type':'WEEKEND'if lookupclock.weekday()>=5 else'WEEKDAY'})
  if initial and req.get('demand_mode')=='EXACT_OBSERVED':flows=[{**f,'status':'REFERENCE_BASED_ESTIMATE','assumptions':f['assumptions']+['Warm-up stationary transfer of selected observation; prior interval state not measured']}for f in flows]
  for f in flows:
   # Cumulative rounding conserves a flat profile across the exact selected window.
   n=round(f['veh_per_hour']*(elapsed+span)/3600)-round(f['veh_per_hour']*elapsed/3600)
   ledger.append({**f,'interval_start_wib':cursor.isoformat(),'interval_end_wib':stop.isoformat(),'elapsed_start_s':elapsed,'elapsed_end_s':elapsed+span,'requested':n,'warmup':initial,'warmup_assumption':'Stationary selected-hour demand before selected time; prior-hour observed state MISSING'if initial else None})
   for i in range(n):
    key=f"r_{f['od_id']}_{f['vehicle_type_id']}_{len(requests):06d}";requests.append({'id':key,'od_id':f['od_id'],'vehicle_type_id':f['vehicle_type_id'],'depart_seconds':round(elapsed+(i+rng.random())*span/max(n,1),4),'warmup':initial,'classification':f['status']})
  cursor=stop
 if len(requests)>12000:raise ValueError('Bounded12000 requests per run exceeded; shorten horizon or use a deliberate staged batch')
 result={'calendar':cal,'horizon_s':horizon,'warmup_s':warm,'total_s':horizon+warm,'elapsed_zero_wib':start.isoformat(),'measurement_start_wib':selected.isoformat(),'measurement_end_wib':end.isoformat(),'seed':seed,'ledger':ledger,'requested':len(requests),'warmup_requested':sum(q['warmup']for q in requests),'requests':sorted(requests,key=lambda q:(q['depart_seconds'],q['id'])),'status':req.get('demand_mode','EXACT_OBSERVED'),'is_observed_target':False,'uncertainty':'Source sample envelope enlarged by ±40% transfer sensitivity; not a statistical confidence interval. Direction, turning, truck subclass and sub-hour shape unmeasured.'};result['cohort_sha256']=identity(result['requests']);return result
if __name__=='__main__':print(json.dumps(initialize()),flush=True)
