"""Strict lookup of reviewed, located observations; source scope cannot be inferred.
Original historical rows with UNSPECIFIED direction never qualify for exact demand.
"""
import sqlite3,json,math
from contextlib import closing
from datetime import datetime,timedelta
def lookup(db,date_value,time_wib):
 minute=int(time_wib[3:5]);hour=int(time_wib[:2]);clock=hour*60+minute
 with closing(sqlite3.connect(db))as c:
  c.row_factory=sqlite3.Row;rows=[dict(r)for r in c.execute("SELECT * FROM evidence WHERE date=? AND metric='traffic_count' AND status='OBSERVED'",(date_value,))]
 selected=[]
 for row in rows:
  start=int(row['start_wib'][:2])*60+int(row['start_wib'][3:5]);end=int(row['end_wib'][:2])*60+int(row['end_wib'][3:5])
  if not start<=clock<end:continue
  prov=json.loads(row['provenance_json']);review=prov.get('review',{})
  if row['direction']=='UNSPECIFIED'or not row['entry_edge']or not row['exit_edge']or not prov.get('od_id')or not all(review.get(k)is True for k in ['source_evidence_verified','quality_reviewed','network_endpoints_verified']):continue
  if row['value']is None or not math.isfinite(row['value'])or row['value']<0:continue
  if row['interval_s']not in [900,3600]:continue
  if row['unit']=='vehicles/hour':rate=row['value']
  elif row['unit']=='vehicles/interval':rate=row['value']*3600/row['interval_s']
  else:continue
  selected.append({'od_id':prov['od_id'],'origin_edge':row['entry_edge'],'destination_edge':row['exit_edge'],'vehicle_type_id':row['vehicle_class'],'veh_per_hour':rate,'range_vph':None,'status':'OBSERVED','source_id':row['source_id'],'source_record_id':row['id'],'assumptions':['Observed demand input is not a calibrated/validated traffic model','Uniform departure within observed interval, unless separate sub-interval records supplied'],'observed_interval_start_wib':row['start_wib'],'observed_interval_end_wib':row['end_wib']})
 if not selected:raise ValueError('MISSING: no reviewed directional count with verified OD entry/exit for requested date/time. Historical aggregate records do not qualify.')
 if len({(r['od_id'],r['vehicle_type_id'])for r in selected})!=len(selected):raise ValueError('Overlapping observations for OD/class require human adjudication; not averaged automatically')
 return selected
