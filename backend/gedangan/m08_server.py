"""Loopback solution comparison API; no executable networks for concept-only catalog entries."""
import json,gzip,threading,uuid,time,xml.etree.ElementTree as E
from datetime import datetime,timezone
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse,parse_qs
from .m04_demand import ROOT,load,save
from .m07_scenarios import read as growth
from .m08_scenarios import read,LABEL
from .m08_runner import run,RUNS,DOC
from .m08_network import build
from .m08_reporting import results
from .m08_comparison import compare
from .m08_evaluation import evaluate
from .m08_feasibility import assess
from .m08_lock import worker
from .m08_toolchain import verify as verify_toolchain
from .m08_playback import spillback_index
COMPATIBILITY={sid:(['pilot-provisional','pilot-strict','corrected-provisional'] if sid in ['S00','S04'] else ['pilot-provisional','pilot-strict'] if sid=='S01' else ['pilot-provisional','corrected-provisional'] if sid in ['S02','S03'] else []) for sid in [f'S{i:02d}' for i in range(8)]}
POOL=ThreadPoolExecutor(max_workers=1);LOCK=threading.Lock();JOBS=load(DOC/'interactive-jobs.json') if (DOC/'interactive-jobs.json').exists() else {}
for job in JOBS.values():
 if job['status'] in ['QUEUED','RUNNING']:job.update(status='INTERRUPTED',error='API restarted before completion; inspect retained run/progress artifacts before retry')
def checkpoint(name):
 path=DOC/name
 if not path.exists():return {}
 for attempt in range(4):
  try:return load(path)
  except json.JSONDecodeError:
   if attempt==3:raise
   time.sleep(.02)

def chosen(sid):return load(DOC/'signal-training.json')['selected'] if sid=='S01' and (DOC/'signal-training.json').exists() else read(sid)
def slim(r):
 value={k:v for k,v in r.items() if k not in ['m08_input','input_signature','rail_events','queue_duration_lane_seconds','lane_occupancy_percent_conditional_on_nonempty','intervention_manifest','od']}
 # Polling needs only the two conditional means used by the cards. Complete OD/class
 # evidence remains in the comparison endpoint and immutable actual run files.
 value['od']={key:{'departed':cell['departed'],**{metric:{'mean':cell[metric]['mean']} for metric in ['waiting_s_departed_including_unfinished','elapsed_trip_duration_s_departed_including_unfinished']}} for key,cell in r['od'].items()}
 return value
def do_job(key,sid,year,g,seed,family):
 JOBS[key].update(status='RUNNING',started_utc=datetime.now(timezone.utc).isoformat());save(DOC/'interactive-jobs.json',JOBS)
 try:
  with worker():
   verify_toolchain()
   existing={r['run_id'] for r in results()};a=run('S00',year,g,seed,family);b=run(sid,year,g,seed,family,specification=chosen(sid));JOBS[key].update(status='COMPLETE',baseline_run=a['run_id'],intervention_run=b['run_id'],cached_baseline=a['run_id'] in existing,cached_intervention=b['run_id'] in existing)
 except Exception as e:JOBS[key].update(status='FAILED',error=str(e))
 finally:JOBS[key]['finished_utc']=datetime.now(timezone.utc).isoformat();save(DOC/'interactive-jobs.json',JOBS)
class Handler(BaseHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def transport(self,event,**values):
  if getattr(self,'path','')!='/api/m08/state' or not (DOC/'transport-debug.enabled').exists():return
  row={'utc':datetime.now(timezone.utc).isoformat(),'port':self.server.server_port,'client_port':self.client_address[1],'event':event,**values}
  with (DOC/'transport-events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
 def handle(self):
  try:super().handle()
  except (ConnectionAbortedError,ConnectionResetError,BrokenPipeError) as e:self.transport('connection_error',error=str(e))
 def log_message(self,*args):pass
 def reply(self,value,status=200):
  data=json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode();compressed='gzip' in self.headers.get('Accept-Encoding','') and len(data)>1024
  if compressed:data=gzip.compress(data,compresslevel=3)
  self.send_response(status)
  if compressed:self.send_header('Content-Encoding','gzip')
  chunked=len(data)>1024
  for k,v in [('Content-Type','application/json; charset=utf-8'),('Cache-Control','no-store'),('Connection','close'),('Transfer-Encoding','chunked') if chunked else ('Content-Length',str(len(data)))]:self.send_header(k,v)
  self.transport('headers',content_length=len(data),status=status,encoding='gzip' if compressed else 'identity')
  self.end_headers()
  if chunked:
   for start in range(0,len(data),16384):
    chunk=data[start:start+16384];self.wfile.write(f'{len(chunk):X}\r\n'.encode()+chunk+b'\r\n')
   self.wfile.write(b'0\r\n\r\n')
  else:self.wfile.write(data)
  self.wfile.flush();self.transport('body_written',bytes=len(data),chunked=chunked)
 def allowed(self):return self.headers.get('Host') in ['127.0.0.1:8773','127.0.0.1:5183'] and self.headers.get('Origin') in [None,'http://127.0.0.1:5183']
 def do_GET(self):
  if not self.allowed():return self.reply({'error':'Host/Origin denied'},403)
  try:
   path=urlparse(self.path);q=parse_qs(path.query)
   if path.path=='/api/m08/state':
    rr=results();return self.reply({'label':LABEL,'compatibility':COMPATIBILITY,'catalog':[chosen(f'S{i:02d}') for i in range(8)],'growth':['LOW','REFERENCE','HIGH']+[p.stem for p in (ROOT/'configuration/growth-m07').glob('CUSTOM_*.json')],'runs':[slim(r) for r in rr],'feasibility':[assess(s) for s in ['S06','S07']],'evaluation':evaluate(rr),'jobs':JOBS,'batch':checkpoint('run-queue.json') if (DOC/'run-queue.json').exists() else {},'offline':checkpoint('offline-stage.json') if (DOC/'offline-stage.json').exists() else {},'robustness':checkpoint('robustness-queue.json') if (DOC/'robustness-queue.json').exists() else {},'training':load(DOC/'signal-training.json') if (DOC/'signal-training.json').exists() else None,'browser_M07_closure':load(DOC/'m07-browser-closure.json'),'M09_started':False})
   if path.path=='/api/m08/compare':
    lookup={r['run_id']:r for r in results()};return self.reply(compare(lookup[q['a'][0]],lookup[q['b'][0]]))
   if path.path=='/api/m08/map':
    sid=q['solution'][0];family=q.get('family',['pilot-provisional'])[0];spec=chosen(sid);concept=sid in ['S06','S07'];fallback=spec['status'] not in ['SIMULATION_READY_PROVISIONAL','SIMULATED'] or family not in COMPATIBILITY[sid];folder,manifest=build(read('S00') if fallback else spec,family);root=E.parse(folder/'network.net.xml').getroot();roles={e['id']:e['road_function'] for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']}
    return self.reply({'roads':[{'id':e.get('id'),'role':'rail' if e.get('id').startswith('m05_rail_') else roles.get(e.get('id'),'road'),'points':[[float(v) for v in p.split(',')] for p in e.find('lane').get('shape').split()]} for e in root.findall('edge') if e.get('function')!='internal'],'signals':[{'id':j.get('id'),'controllers':sorted({c.get('tl') for c in root.findall('connection') if c.get('tl') and any(e.get('id')==c.get('from') and e.get('to')==j.get('id') for e in root.findall('edge'))}),'x':float(j.get('x')),'y':float(j.get('y'))} for j in root.findall('junction') if j.get('type') in ['traffic_light','rail_crossing']],'manifest':manifest,'concept':assess(sid) if concept else None,'affected_edges':[spec['parameters'][k] for k in ['from','to'] if k in spec['parameters']],'no_new_ramps':True})
   if path.path=='/api/m08/playback':
    rid=q['run_id'][0]
    if len(rid)!=20 or any(c not in '0123456789abcdef' for c in rid):raise ValueError('Invalid run ID')
    p=load(RUNS/rid/'playback.json');offset=int(q.get('offset',['0'])[0])
    if not 0<=offset<len(p['frames']):raise ValueError('Frame outside recording')
    return self.reply({'run_id':rid,'total_frames':len(p['frames']),'offset':offset,'sample_period_s':5,'frames':p['frames'][offset:offset+5],'spillback_events':spillback_index(RUNS/rid),'source':'Actual SUMO samples, no fabricated motion'})
   return self.reply({'error':'Not found'},404)
  except Exception as e:self.reply({'error':str(e)},400)
 def do_POST(self):
  if not self.allowed() or self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.reply({'error':'Host/Origin/Content-Type denied'},403)
  try:
   n=int(self.headers.get('Content-Length','0'))
   if not 0<n<20000:raise ValueError('Body size limit')
   self.connection.settimeout(10);v=json.loads(self.rfile.read(n));sid=v['solution'];spec=chosen(sid)
   if spec['status'] not in ['SIMULATION_READY_PROVISIONAL','SIMULATED']:raise ValueError('Run disabled: '+spec['status']+' / '+','.join(spec['blockers']))
   year=v['year'];seed=v.get('seed',42);family=v.get('family','pilot-provisional');g=v['growth'];growth(g)
   if family not in COMPATIBILITY[sid]:raise ValueError('Scenario structurally unavailable in selected parent; no invented controller or movement')
   if type(year)!=int or not 2026<=year<=2040 or seed not in [42,43] or family not in ['pilot-provisional','pilot-strict','corrected-provisional']:raise ValueError('Invalid bounded run selection')
   if self.path!='/api/m08/run':return self.reply({'error':'Not found'},404)
   if any((DOC/name).exists() and checkpoint(name).get('status')=='RUNNING' for name in ['run-queue.json','robustness-queue.json','offline-stage.json']):return self.reply({'error':'Sequential offline batch active'},409)
   with LOCK:
    if any(j['status'] in ['QUEUED','RUNNING'] for j in JOBS.values()):return self.reply({'error':'One job at a time'},409)
    key=uuid.uuid4().hex;JOBS[key]={'status':'QUEUED','solution':sid,'year':year,'growth':g,'seed':seed,'family':family,'queued_utc':datetime.now(timezone.utc).isoformat()}
   POOL.submit(do_job,key,sid,year,g,seed,family);return self.reply({'job_id':key},202)
  except Exception as e:self.reply({'error':str(e)},400)
if __name__=='__main__':print('M08 API127.0.0.1:8773, single bounded worker',flush=True);ThreadingHTTPServer(('127.0.0.1',8773),Handler).serve_forever()
