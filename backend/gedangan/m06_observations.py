"""Typed local observations; NULL is missing, never silently zero."""
import csv,json,math,hashlib,shutil
from datetime import datetime,timedelta
from collections import defaultdict,Counter
from pathlib import Path
import jsonschema
from .m04_demand import ROOT,load,save,sha
CONF=ROOT/'configuration/calibration-m06';OBS=ROOT/'data/observations/m06'
KINDS={'traffic_count':{'count':('integer','vehicles'),'turning_movement':('string',None)},'travel_time':{'travel_time_s':('number','s'),'sample_count':('integer',None),'origin':('string',None),'destination':('string',None),'corridor':('string',None)},'queue':{'queue_length_m':('number','m'),'queue_count':('integer','vehicles'),'maximum_extent_m':('number','m'),'definition':('string',None),'boundary_censored':('boolean',None)},'signal':{k:('number','s') for k in ['green_s','yellow_s','red_s','cycle_s','offset_s']},'railway':{k:('string',None) for k in ['warning_start','closure','train_approach','train_pass','train_clearance','barrier_reopen','road_release','train_id']},'geometry':{'crs':('string',None),'survey_point':('array',None),'road_centerline':('array',None),'rail_centerline':('array',None),'lane_count':('integer',None),'lane_width_m':('number','m'),'stop_line':('array',None),'gate_position':('array',None),'crossing_angle_deg':('number','degrees'),'verified_track_count':('integer',None),'clearance':('object',None),'accuracy_m':('number','m')}}
BASE={'observation_id':{'type':'string','minLength':1},'kind':{'enum':list(KINDS)},'source_class':{'enum':['OBSERVED_FIELD','DEMO_SYNTHETIC']},'date':{'type':'string','format':'date'},'interval_start':{'type':'string','format':'date-time'},'interval_end':{'type':'string','format':'date-time'},'timezone':{'const':'Asia/Jakarta'},'location_id':{'type':'string','minLength':1},'approach':{'type':'string','minLength':1},'direction':{'type':'string','minLength':1},'vehicle_class':{'enum':['motorcycle','car','pickup_van','minibus','bus','light_truck','medium_truck','heavy_truck','trailer','oversize','all']},'method':{'type':'string','minLength':1},'observer_source':{'type':'string','minLength':1},'quality':{'enum':['VERIFIED','PROVISIONAL','REJECTED']},'confidence':{'enum':['HIGH','MEDIUM','LOW','UNKNOWN']},'provenance_id':{'type':'string','minLength':1},'uncertainty':{'type':['number','null'],'minimum':0},'notes':{'type':['string','null']}}
KINDS['signal'].update({k:('string',None) for k in ['intersection_id','signal_head_group','phase_id']})
KINDS['queue'].update({'observation_point':('string',None),'lane_group':('string',None),'length_unit':('string',None),'count_unit':('string',None)})
KINDS['railway'].update({'crossing_site_id':('string',None),'train_movement':('string',None)})
def schema(kind):
 props={**BASE,**{k:{'type':[t,'null'],**({'minimum':0} if t in ['integer','number'] else {})} for k,(t,u) in KINDS[kind].items()}};props['kind']={'const':kind}
 if kind=='geometry':
  pair={'type':'array','minItems':2,'maxItems':3,'items':{'type':'number'}}
  for key in ['survey_point','gate_position']:props[key]={'anyOf':[{'type':'null'},pair]}
  for key in ['road_centerline','rail_centerline','stop_line']:props[key]={'anyOf':[{'type':'null'},{'type':'array','minItems':2,'items':pair}]}
  for key in ['lane_count','verified_track_count','lane_width_m']:props[key]['minimum']=1 if key!='lane_width_m' else .01
 return {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'properties':props,'required':list(BASE)+list(KINDS[kind])}
def timestamp(s):
 d=datetime.fromisoformat(s)
 if d.utcoffset()!=timedelta(hours=7):raise ValueError('Timestamp must explicitly use +07:00')
 return d
def finite_tree(value):
 if isinstance(value,dict):return all(finite_tree(v) for v in value.values())
 if isinstance(value,list):return all(finite_tree(v) for v in value)
 return not isinstance(value,(int,float)) or isinstance(value,bool) or math.isfinite(value)

def validate(row,provenance):
 if row.get('kind') not in KINDS:raise ValueError('Unknown observation kind')
 jsonschema.Draft202012Validator(schema(row['kind']),format_checker=jsonschema.FormatChecker()).validate(row)
 if not finite_tree(row):raise ValueError('Nonfinite numeric observation')
 if row['quality']=='REJECTED':raise ValueError('Source quality rejected; preserve in rejection log')
 a,b=timestamp(row['interval_start']),timestamp(row['interval_end'])
 if a>=b or a.date().isoformat()!=row['date']:raise ValueError('Invalid observation date/window')
 p=provenance.get(row['provenance_id'])
 if not p or not all(p.get(k) for k in ['source_title','source_uri','license_notes','method','spatial_scope','accessed_on']):raise ValueError('Missing complete provenance')
 if row['source_class']=='OBSERVED_FIELD' and (p.get('source_class')!='OBSERVED_FIELD' or not p.get('field_evidence_verified')):raise ValueError('Observed source lacks independently reviewed field evidence')
 flags=[]
 if row['kind']=='travel_time' and row['travel_time_s'] is not None and (row['sample_count'] is None or row['sample_count']<1):raise ValueError('Measured travel time requires at least one documented sample')
 if any(row[k] is None for k in KINDS[row['kind']]):flags.append('MISSING_VALUES')
 if (b-a).total_seconds()!=900:flags.append('NONSTANDARD_INTERVAL_KEEP_ORIGINAL')
 if row['kind']=='traffic_count' and row['count'] is not None and row['count']>10000:flags.append('OUTLIER_REVIEW_NOT_DELETED')
 if row['kind']=='queue' and row['definition'] is None:flags.append('QUEUE_DEFINITION_MISSING')
 if row['kind']=='queue' and (row['length_unit'] not in [None,'m'] or row['count_unit'] not in [None,'vehicles']):raise ValueError('Queue units must be m and vehicles, not interchangeable')
 if row['kind']=='signal' and all(row[x] is not None for x in ['green_s','yellow_s','red_s','cycle_s']) and abs(sum(row[x] for x in ['green_s','yellow_s','red_s'])-row['cycle_s'])>.01:flags.append('SIGNAL_PHASE_SUM_REVIEW')
 if row['kind']=='railway':
  times=[timestamp(row[k]) for k in ['warning_start','closure','train_pass','train_clearance','barrier_reopen','road_release'] if row[k] is not None]
  if times!=sorted(times):raise ValueError('Railway event chronology invalid')
 return flags
def fingerprint(r):return tuple(r.get(k) for k in ['kind','date','interval_start','interval_end','location_id','approach','direction','vehicle_class','turning_movement','origin','destination'])
def normalize_csv(row,kind):
 result={k:None if v is None or v.strip() in ['', 'NULL','MISSING'] else v for k,v in row.items()}
 for k,(typ,_) in KINDS[kind].items():
  if result.get(k) is not None:
   if typ=='integer':result[k]=int(result[k])
   elif typ=='number':result[k]=float(result[k])
   elif typ=='boolean':
    if result[k].lower() not in ['true','false']:raise ValueError('Boolean must be true/false')
    result[k]=result[k].lower()=='true'
   elif typ in ['array','object']:result[k]=json.loads(result[k])
 if result.get('uncertainty') is not None:result['uncertainty']=float(result['uncertainty'])
 return result
def ingest(path,provenance,import_id,demo=False):
 import re
 if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',import_id):raise ValueError('Import ID must be a simple bounded identifier')
 path=Path(path);out=OBS/('synthetic-demo-imports' if demo else 'imports')/import_id
 if out.exists():raise ValueError('Import ID already exists; never overwrite raw input')
 out.mkdir(parents=True);shutil.copy2(path,out/('raw'+path.suffix));accepted=[];rejected=[];ids=set();keys=set();quality=[]
 rows=list(csv.DictReader(path.open(encoding='utf-8-sig',newline=''))) if path.suffix=='.csv' else load(path)
 for i,raw in enumerate(rows):
  try:
   r=normalize_csv(raw,raw.get('kind')) if path.suffix=='.csv' else raw;flags=validate(r,provenance)
   mapping=map_observation(r,load(CONF/'observation-mapping.json'))
   if mapping['status']=='NEEDS MANUAL REVIEW':flags.append('SPATIAL_MAPPING_NEEDS_MANUAL_REVIEW')
   if (r['source_class']=='DEMO_SYNTHETIC')!=demo:raise ValueError('Source category cannot enter this import namespace')
   if r['observation_id'] in ids or fingerprint(r) in keys:raise ValueError('Duplicate ID or measurement key')
   ids.add(r['observation_id']);keys.add(fingerprint(r));accepted.append(r);quality.append({'observation_id':r['observation_id'],'flags':flags})
  except Exception as e:rejected.append({'row_number':i+1,'raw':raw,'reason':str(e)})
 save(out/'normalized.json',accepted);save(out/'rejected.json',rejected);save(out/'quality-flags.json',quality);save(out/'summary.json',{'source_sha256':sha(path),'accepted':len(accepted),'rejected':len(rejected),'missing_is_zero':False,'category':'DEMO_SYNTHETIC' if demo else 'OBSERVED_FIELD','provenance':provenance})
 return accepted,rejected

def aggregate_counts(rows,start,end):
 a,b=timestamp(start),timestamp(end);rows=sorted(rows,key=lambda r:r['interval_start']);cursor=a;values=[]
 for r in rows:
  x,y=timestamp(r['interval_start']),timestamp(r['interval_end'])
  if x< a or y>b:raise ValueError('Never split a count interval without source detail')
  if x!=cursor:raise ValueError('Gap or overlap; no fabricated count allocation')
  if fingerprint({**r,'date':'','interval_start':'','interval_end':''})!=fingerprint({**rows[0],'date':'','interval_start':'','interval_end':''}):raise ValueError('Incompatible count strata')
  cursor=y;values.append(r['count'])
 if cursor!=b:raise ValueError('Incomplete temporal coverage')
 return None if any(v is None for v in values) else sum(values)

def map_observation(row,mappings):
 options=[m for m in mappings if m['location_id']==row['location_id'] and m['direction']==row['direction'] and (row.get('turning_movement') is None or m.get('turning_movement')==row['turning_movement'])]
 return {'status':'MAPPED_MODEL_REFERENCE' if len(options)==1 else 'NEEDS MANUAL REVIEW','candidates':options,'method':'Exact location/direction/movement registry; no proximity-only snap; physical mapping remains survey-dependent.'}
def aggregate_od(rows):
 groups=defaultdict(list)
 for r in rows:
  if not all(r.get(k) for k in ['origin','destination','vehicle_class','interval_start','interval_end']):raise ValueError('OD strata missing')
  if r.get('count') is not None and (isinstance(r['count'],bool) or not isinstance(r['count'],int) or r['count']<0):raise ValueError('OD count must be nonnegative integer or NULL')
  groups[tuple(r[k] for k in ['origin','destination','vehicle_class','interval_start','interval_end'])].append(r.get('count'))
 return [{'origin':k[0],'destination':k[1],'vehicle_class':k[2],'interval_start':k[3],'interval_end':k[4],'count':None if any(v is None for v in vs) else sum(vs)} for k,vs in groups.items()]
def turning_balance(approach_total,turns):
 if approach_total is None or any(t is None for t in turns):return {'status':'MISSING','difference':None}
 return {'status':'CONSISTENT' if approach_total==sum(turns) else 'REVIEW_REQUIRED','difference':sum(turns)-approach_total,'action':'Keep raw values; do not silently redistribute or discard outlier'}
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description='Local immutable CSV/JSON import. Defaults to real observed namespace; demo data requires --demo.')
 parser.add_argument('input');parser.add_argument('--provenance',required=True);parser.add_argument('--import-id',required=True);parser.add_argument('--demo',action='store_true');a=parser.parse_args()
 good,bad=ingest(a.input,load(a.provenance),a.import_id,a.demo);print('Accepted',len(good),'Rejected',len(bad))
