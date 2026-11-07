"""Loopback research experiment UI with an actual queued SUMO worker.
Requires retained .venv + local SUMO toolchain; never masquerades as the M12 EXE.
"""
import argparse,threading,secrets,sqlite3,re,csv,io,mimetypes,os
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from functools import lru_cache
from .recovery_common import *
from .recovery_data import initialize,coverage,build_demand,DB
from .recovery_network import SCENARIOS,validate
from .recovery_engine import run,compare
POOL=ThreadPoolExecutor(max_workers=1);JOBS={};LOCK=threading.Lock();UI=ROOT/'frontend/realism_recovery'
def results():return sorted([load(p)for p in RUNS.glob('*/result.json')],key=lambda r:r['run_id'])

def progress_snapshots():
 rows=[]
 for p in RUNS.glob('*/progress.json'):
  try:value=load(p)
  except (ValueError,OSError):continue # A writer can be between truncate and flush; next poll retries.
  if value.get('status')in ['RUNNING_SUMO','ROUTING','STARTING_SUMO']:rows.append({'folder':p.parent.name,**value})
 return rows
def existing_run(key):
 if not re.fullmatch('[0-9a-f]{24}',key):raise ValueError('Invalid run identifier')
 p=RUNS/key/'result.json'
 if not p.is_file():raise ValueError('Run not complete or not available; no fallback replay')
 return load(p)
@lru_cache(maxsize=6)
def playback(key,checksum):return load(RUNS/key/'playback.json')
@lru_cache(maxsize=12)
def netview(path,checksum):
 import xml.etree.ElementTree as E
 r=E.parse(path).getroot();meta={e['id']:e for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']};edges=[]
 for e in r.findall('edge'):
  if e.get('function')=='internal':continue
  lanes=e.findall('lane');m=meta.get(e.get('id'),{});edges.append({'id':e.get('id'),'name':m.get('name'),'role':m.get('road_function','concept_flyover'if e.get('id').startswith('recovery_fo_')else'railway'),'lanes':[{'id':l.get('id'),'allow':l.get('allow'),'disallow':l.get('disallow'),'shape':[[float(v)for v in p.split(',')]for p in l.get('shape').split()]}for l in lanes]})
 return {'network_sha256':checksum,'location':dict(r.find('location').attrib),'edges':edges,'style':'Technical actual model geometry. Not a field-validated or photorealistic map.'}
def record_job(key,req,status,runpath=None,error=None):
 with sqlite3.connect(DB)as c:c.execute('INSERT INTO experiments VALUES(?,?,?,?,?,?) ON CONFLICT(id)DO UPDATE SET status=excluded.status,run_path=excluded.run_path,error=excluded.error',(key,datetime.now(timezone.utc).isoformat(),json.dumps(req),status,runpath,error))
def worker(key,req):
 with LOCK:JOBS[key]={'id':key,'status':'RUNNING','request':req}
 record_job(key,req,'RUNNING')
 try:
  result=run(req)
  with LOCK:JOBS[key].update(status='COMPLETE',run_id=result['run_id'])
  record_job(key,req,'COMPLETE',result['run_id'])
 except Exception as exc:
  with LOCK:JOBS[key].update(status='FAILED',error=str(exc))
  record_job(key,req,'FAILED',error=str(exc))
def handler(port,token):
 class Handler(BaseHTTPRequestHandler):
  protocol_version='HTTP/1.1'
  def log_message(self,*a):pass
  def allowed(self):return self.headers.get('Host')==f'127.0.0.1:{port}'and self.headers.get('Origin')in[None,f'http://127.0.0.1:{port}']
  def send(self,data,kind='application/json; charset=utf-8',status=200,filename=None):
   self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Transfer-Encoding','chunked');self.send_header('Connection','close');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; frame-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'")
   if filename:self.send_header('Content-Disposition','attachment; filename="'+filename+'"')
   self.end_headers()
   try:
    for i in range(0,len(data),16384):
     chunk=data[i:i+16384];self.wfile.write(f'{len(chunk):X}\r\n'.encode()+chunk+b'\r\n')
    self.wfile.write(b'0\r\n\r\n');self.wfile.flush()
   except(BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
  def reply(self,v,status=200):return self.send(json.dumps(v,ensure_ascii=False,allow_nan=False).encode(),status=status)
  def do_GET(self):
   if not self.allowed():return self.reply({'error':'Host/Origin denied'},403)
   parsed=urlparse(self.path);path=parsed.path;q=parse_qs(parsed.query)
   try:
    if path=='/api/health':return self.reply({'service':'gedangan-functional-recovery','port':port,'token':token,'engine':'ACTUAL LOCAL SUMO1.28.0','old_presentation_EXE_unchanged':True})
    if path=='/api/state':
     rs=results()
     with LOCK:jobs=copy_jobs={k:dict(v)for k,v in JOBS.items()}
     progress=progress_snapshots()
     return self.reply({'runs':rs,'jobs':jobs,'progress':progress,'scenarios':SCENARIOS,'coverage':coverage(),'empirical_2026':'MISSING / NOT CALIBRATED','research_dependencies':'Project .venv + SUMO1.28.0; old portable EXE remains cached-presentation-only'})
    if path=='/api/coverage':return self.reply(coverage())
    if path=='/api/preview':
     req=json.loads(q['request'][0]);d=build_demand(req);return self.reply({k:v for k,v in d.items()if k!='requests'})
    if path=='/api/network':
     key=q.get('run',[None])[0];r=existing_run(key)if key else None;p=ROOT/r['network_path']if r else PARENT;return self.reply(netview(str(p),sha(p)))
    if path=='/api/playback':
     key=q['run'][0];r=existing_run(key);p=RUNS/key/'playback.json';data=playback(key,sha(p));start=max(0,int(q.get('offset',['0'])[0]));limit=min(120,max(1,int(q.get('limit',['60'])[0])));return self.reply({'run_id':key,'network_sha256':data['network_sha256'],'total_frames':len(data['frames']),'offset':start,'frames':data['frames'][start:start+limit],'actual_SUMO':True,'measurement_start_elapsed_s':r['warmup_s']})
    if path=='/api/compare':return self.reply(compare(existing_run(q['baseline'][0]),existing_run(q['after'][0])))
    if path=='/api/export':
     key=q['run'][0];r=existing_run(key);data={'run':r,'network_manifest':load((ROOT/r['network_path']).parent/'manifest.json'),'edge_impact':load(RUNS/key/'edge-impact.json'),'vehicle_results':load(RUNS/key/'vehicle-results.json')}
     if q.get('format',['json'])[0]=='csv':
      s=io.StringIO();w=csv.writer(s);w.writerow(['id','class','OD','route_before','route_after','rerouted','lost_route','added_distance_m','actual_duration_s','duration_censored','departed','arrived','running_at_end','not_departed','classification'])
      for v in data['vehicle_results']:w.writerow([v['id'],v['vehicle_type_id'],v['od_id'],' '.join(v['route_before']),' '.join(v['route_after']),v['rerouted'],v['lost_route'],v['added_distance_m'],v['actual_duration_s'],v['duration_censored'],v['departed'],v['arrived'],v['running_at_end'],v['not_departed'],v['classification']])
      return self.send(('\ufeff'+s.getvalue()).encode(),'text/csv; charset=utf-8',filename='Gedangan_experiment_'+key+'.csv')
     return self.send(json.dumps(data,ensure_ascii=False,indent=2).encode(),'application/json',filename='Gedangan_experiment_'+key+'.json')
    if path.startswith('/evidence/'):
     p=(DOC/path[10:]).resolve()
     if not p.is_relative_to(DOC.resolve())or p.suffix not in['.md','.json','.svg','.geojson']:raise ValueError('Evidence path not permitted')
     return self.send(p.read_bytes(),mimetypes.guess_type(p.name)[0]or'application/octet-stream')
    p=(UI/('index.html'if path=='/'else path.lstrip('/'))).resolve()
    if not p.is_relative_to(UI.resolve())or not p.is_file():return self.reply({'error':'File not found'},404)
    return self.send(p.read_bytes(),mimetypes.guess_type(p.name)[0]or'application/octet-stream')
   except(ValueError,KeyError,FileNotFoundError)as exc:return self.reply({'error':str(exc)},400)
   except Exception as exc:return self.reply({'error':'Experiment service error: '+str(exc)},500)
  def do_POST(self):
   if not self.allowed():return self.reply({'error':'Host/Origin denied'},403)
   try:
    size=int(self.headers.get('Content-Length','0'))
    if not 0<size<=131072:raise ValueError('Request size bounded128KiB')
    req=json.loads(self.rfile.read(size))
    if self.path=='/api/run':
     build_demand(req);validate(req.get('scenario',{'id':'S00'}));key=identity({'request':req,'queued_utc':datetime.now(timezone.utc).isoformat()})[:24]
     with LOCK:
      if any(v['status']in ['RUNNING','QUEUED']for v in JOBS.values()):return self.reply({'error':'One actual SUMO job at a time; wait for current job'},409)
      JOBS[key]={'id':key,'status':'QUEUED','request':req}
     record_job(key,req,'QUEUED');POOL.submit(worker,key,req);return self.reply({'job_id':key,'status':'QUEUED','engine':'SUMO1.28.0'})
    if self.path=='/api/shutdown':
     if req.get('token')!=token:return self.reply({'error':'Invalid shutdown token'},403)
     with LOCK:
      if any(j['status']in ['RUNNING','QUEUED']for j in JOBS.values()):return self.reply({'error':'Wait for actual SUMO job completion before shutdown'},409)
     self.reply({'closed':True});threading.Thread(target=self.server.shutdown,daemon=True).start();return
    return self.reply({'error':'Unknown endpoint'},404)
   except(ValueError,KeyError,TypeError)as exc:return self.reply({'error':str(exc)},400)
 return Handler
def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=5196);a=p.parse_args();initialize();RUNS.mkdir(parents=True,exist_ok=True)
 with sqlite3.connect(DB)as c:c.execute("UPDATE experiments SET status='INTERRUPTED',error='Research service restarted; inspect retained outputs before resubmitting' WHERE status IN ('QUEUED','RUNNING')")
 server=ThreadingHTTPServer(('127.0.0.1',a.port),handler(a.port,secrets.token_urlsafe(24)));print(f'Gedangan Functional Recovery http://127.0.0.1:{a.port} - ACTUAL SUMO runner, separate from old M12',flush=True)
 try:server.serve_forever()
 finally:server.server_close();POOL.shutdown(wait=True)
if __name__=='__main__':main()
