"""Loopback-only Projection Lab API, versioned custom scenarios, one queued SUMO worker."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse,parse_qs
import json,re,uuid,threading,gzip,xml.etree.ElementTree as ET
from functools import lru_cache
from .m04_demand import ROOT,load,save
from .m07_growth import fingerprint
from .m07_scenarios import read,validate,CONF
from .m07_projection import baseline,project
from .m07_runner import RUNS,run,NETWORKS
from .m07_analysis import compare
from .m07_lifecycle_audit import audited_result
POOL=ThreadPoolExecutor(max_workers=1);JOBS={};LOCK=threading.Lock()
@lru_cache(maxsize=3)
def network_map(variant):
 if variant not in NETWORKS:raise ValueError('Unknown network map variant')
 root=ET.parse(NETWORKS[variant]).getroot()
 return {'variant':variant,'roads':[{'id':e.get('id'),'role':'rail' if e.get('id').startswith('m05_rail_') else 'road','points':[[float(v) for v in p.split(',')] for p in e.find('lane').get('shape').split()]} for e in root.findall('edge') if e.get('function')!='internal']}

def results():return [audited_result(p.parent) for p in RUNS.glob('*/result.json') if p.parent.name!='fresh-reproduction' and load(p).get('status')=='ACTUAL_SUMO_RESULT']
def state():
 rs=[{**{k:v for k,v in r.items() if k not in ['rail_events','input_signature','queue_duration_lane_seconds','lane_occupancy_percent_conditional_on_nonempty','loaded_reconciliation']},'od':{od:{k:v for k,v in cell.items() if not isinstance(v,dict)} for od,cell in r['od'].items()}} for r in results()];return {'baseline':baseline(),'scenarios':[read(n) for n in ['LOW','REFERENCE','HIGH']]+[read(p.stem) for p in sorted(CONF.glob('CUSTOM_*.json'))],'runs':rs,'jobs':JOBS,'offline_queue':load(ROOT/'documentation/m07/run-queue.json') if (ROOT/'documentation/m07/run-queue.json').exists() else {},'experiment_lock':load(ROOT/'documentation/m07/experiment-lock.json') if (ROOT/'documentation/m07/experiment-lock.json').exists() else {},'sources':load(ROOT/'documentation/m07/source-register.json'),'empirical_status':'BLOCKED — BASELINE AND GROWTH EVIDENCE REQUIRED','M08_started':False}
def job(key,p,variant,seed):
 with LOCK:JOBS[key]['status']='RUNNING';save(ROOT/'documentation/m07/interactive-jobs.json',JOBS)
 try:
  result=run(p,variant,seed)
  with LOCK:JOBS[key].update(status='COMPLETE',run_id=result['run_id'])
 except Exception as e:
  with LOCK:JOBS[key].update(status='FAILED',error=str(e))
 finally:save(ROOT/'documentation/m07/interactive-jobs.json',JOBS)
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def reply(self,value,status=200):
  data=json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode();compressed='gzip' in self.headers.get('Accept-Encoding','') and len(data)>1024
  if compressed:data=gzip.compress(data,compresslevel=3)
  self.send_response(status)
  if compressed:self.send_header('Content-Encoding','gzip');self.send_header('Vary','Accept-Encoding')
  self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Connection','close');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def allowed(self):
  return self.headers.get('Host') in ['127.0.0.1:8772','127.0.0.1:5182'] and self.headers.get('Origin') in [None,'http://127.0.0.1:5182']
 def do_GET(self):
  if not self.allowed():return self.reply({'error':'Origin/Host denied'},403)
  try:
   path=urlparse(self.path)
   if path.path=='/api/m07/state':return self.reply(state())
   if path.path=='/api/m07/map':return self.reply(network_map(parse_qs(path.query)['network'][0]))
   if path.path=='/api/m07/project':
    q=parse_qs(path.query)
    if 'scenario_id' in q:scenario=read(q['scenario_id'][0])
    else:
     source=q['base'][0];scenario=read(source);rates=json.loads(q['rates'][0])
     if len(rates)!=len(scenario['rules']):raise ValueError('Custom rate count mismatch')
     scenario.update(id='CUSTOM_DRAFT',origin_scenario=source)
     for rule,rate in zip(scenario['rules'],rates):rule['schedule']={'mode':'constant','rate':rate}
    validate(scenario);projection=project(int(q['year'][0]),scenario);projection['cells']=[{k:v for k,v in c.items() if k!='annual_schedule'} for c in projection['cells']];projection['annual_schedule_note']='Full annual schedules retained in canonical projection audit and run projection.json';return self.reply(projection)
   if path.path=='/api/m07/result':
    rid=parse_qs(path.query).get('run_id',[''])[0]
    if not re.fullmatch('[0-9a-f]{20}',rid):raise ValueError('Invalid run ID')
    return self.reply({k:v for k,v in audited_result(RUNS/rid).items() if k not in ['rail_events','input_signature']})
   if path.path=='/api/m07/playback':
    rid=parse_qs(path.query).get('run_id',[''])[0]
    if not re.fullmatch('[0-9a-f]{20}',rid):raise ValueError('Invalid run ID')
    recording=load(RUNS/rid/'playback.json');q=parse_qs(path.query);offset=int(q.get('offset',['0'])[0])
    if offset<0 or offset>=len(recording['frames']):raise ValueError('Frame offset outside recording')
    frames=recording['frames'][offset:offset+5];times=[f['time'] for f in frames]
    return self.reply({'label':recording['label'],'source':recording['source'],'sample_period_s':recording['sample_period_s'],'total_frames':len(recording['frames']),'offset':offset,'frames':frames,'events':[e for e in recording['events'] if min(times)<=e['time']<=max(times)]})
   if path.path=='/api/m07/compare':
    q=parse_qs(path.query);lookup={r['run_id']:r for r in results()};return self.reply(compare(lookup[q['a'][0]],lookup[q['b'][0]]))
   return self.reply({'error':'Not found'},404)
  except Exception as e:self.reply({'error':str(e)},400)
 def do_POST(self):
  if not self.allowed() or self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.reply({'error':'Origin/Host/Content-Type denied'},403)
  try:
   size=int(self.headers.get('Content-Length','0'))
   if not 0<size<=150000:raise ValueError('Body size outside limit')
   self.connection.settimeout(10);raw=self.rfile.read(size);body=json.loads(raw);scenario=body.get('scenario');validate(scenario)
   if self.path=='/api/m07/scenario':
    custom={**scenario,'id':'CUSTOM_'+fingerprint(scenario)[:12]};path=CONF/(custom['id']+'.json')
    if not path.exists():save(path,custom)
    return self.reply(custom)
   p=project(body['year'],scenario)
   if self.path=='/api/m07/project':return self.reply(p)
   if self.path=='/api/m07/run':
    if body.get('network','pilot-provisional') not in ['pilot-provisional','pilot-strict','corrected-provisional'] or body.get('seed',42) not in [42,43]:raise ValueError('Unsupported bounded run variant/seed')
    offline=ROOT/'documentation/m07/run-queue.json'
    experiment=ROOT/'documentation/m07/experiment-lock.json'
    if (offline.exists() and load(offline)['status']=='RUNNING') or (experiment.exists() and load(experiment)['status']=='RUNNING'):return self.reply({'error':'Offline precompute running sequentially; wait for completion'},409)
    with LOCK:
     if any(v['status'] in ['QUEUED','RUNNING'] for v in JOBS.values()):return self.reply({'error':'One SUMO run at a time; queue busy'},409)
     key=uuid.uuid4().hex;JOBS[key]={'status':'QUEUED','year':p['year'],'scenario':p['scenario']}
    POOL.submit(job,key,p,body.get('network','pilot-provisional'),body.get('seed',42));return self.reply({'job_id':key},202)
   return self.reply({'error':'Not found'},404)
  except Exception as e:self.reply({'error':str(e)},400)
if __name__=='__main__':
 print('M07 API127.0.0.1:8772; single SUMO worker; no empirical forecast',flush=True);ThreadingHTTPServer(('127.0.0.1',8772),Handler).serve_forever()
