"""Loopback-only staging app; one worker, isolated scenario store, no database import."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import json,mimetypes,uuid,threading,traceback,gzip
from .m155_common import *
from .m155_demand import generate,default
from .m14_vehicles import registry,PROFILES
from .m155_network import catalog,route
from .m155_engine import run
from .m09_export import scene
UI=ROOT/'frontend/dist-m155';jobs={};pool=ThreadPoolExecutor(max_workers=1);lock=threading.Lock()
def job(key,req):
 jobs[key]={'status':'GENERATING','job_id':key}
 try:
  def update(value):jobs[key]={'status':'GENERATING','job_id':key,'progress':value}
  result=run(req,on_progress=update)
  from .m155_edge_inspection import audit
  update({'stage':'DERIVING_FCD_EDGE_COUNTS'});audit(result)
  jobs[key]={'status':'COMPLETE','job_id':key,'run_id':result['run_id'],'result':result}
 except Exception as exc:jobs[key]={'status':'FAILED','job_id':key,'error':str(exc)};traceback.print_exc()
def handler(port):
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def allowed(self):return self.headers.get('Host')in[f'127.0.0.1:{port}',f'localhost:{port}']and self.headers.get('Origin')in[None,f'http://127.0.0.1:{port}',f'http://localhost:{port}']
  def send(self,value,code=200,kind='application/json; charset=utf-8',encoding=None):
   raw=value if isinstance(value,bytes)else json.dumps(value,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
   if encoding:self.send_header('Content-Encoding',encoding)
   self.end_headers()
   try:self.wfile.write(raw)
   except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
  def do_GET(self):
   if not self.allowed():return self.send({'error':'Host/Origin denied'},403)
   path=urlparse(self.path).path;parts=path.strip('/').split('/')
   try:
    if path=='/api/catalog':return self.send({'network':catalog(),'vehicles':registry(),'profiles':{'Runnable Demo (assumption)':[default()['weights'][v['id']]for v in registry()],**PROFILES},'support':{v['id']:{a['id']:{t:route(v['id'],a['id'],t)['route_status']=='ROUTABLE'for t in a['movements']}for a in catalog()['approaches']}for v in registry()},'default':default()})
    if path=='/api/technical-map':return self.send(load(DOC/'technical-map.json'))
    if path=='/api/geometry-audit':return self.send(load(DOC/'network-reality-audit.json'))
    if len(parts)==3 and parts[:2]==['api','edge-inspection']:
     if not all(c in '0123456789abcdef'for c in parts[2])or len(parts[2])!=24:return self.send({'error':'Invalid run ID'},400)
     p=DOC/'edge-inspection'/(parts[2]+'.json')
     return self.send(load(p)if p.exists()else{'status':'MISSING','definition':'Independent FCD edge audit not yet generated for this run'})
    if path=='/api/scene':return self.send(scene(NETWORK))
    if path=='/api/runs':return self.send([load(p)for p in sorted(RUNS.glob('*/result.json'),key=lambda p:p.stat().st_mtime,reverse=True)])
    if path=='/api/scenarios':return self.send([load(p)for p in SCENARIOS.glob('*.json')])
    if len(parts)==3 and parts[:2]==['api','jobs']:
     value=dict(jobs.get(parts[2],{'status':'NOT_FOUND'}))
     return self.send(value)
    if len(parts)==4 and parts[:2]==['api','run']:
     p=(RUNS/parts[2]/parts[3]).resolve()
     if not p.is_relative_to(RUNS.resolve())or not p.is_file():return self.send({'error':'Not found'},404)
     if p.suffix=='.gz':return self.send(p.read_bytes(),kind='application/json',encoding='gzip')
     if p.suffix!='.json':return self.send({'error':'JSON outputs only'},400)
     return self.send(p.read_bytes())
    p=(UI/('m155.html'if path=='/'else path.lstrip('/'))).resolve()
    if not p.is_relative_to(UI.resolve())or not p.is_file():return self.send({'error':'Not found'},404)
    return self.send(p.read_bytes(),kind=mimetypes.guess_type(p.name)[0]or'application/octet-stream')
   except Exception as exc:return self.send({'error':str(exc)},400)
  def do_POST(self):
   if not self.allowed():return self.send({'error':'Host/Origin denied'},403)
   try:
    n=int(self.headers.get('Content-Length','0'));path=urlparse(self.path).path
    if path=='/api/video':
     if not 0<n<=100000000:raise ValueError('Video size limit 100MB')
     target=DOC/'evidence/actual-playback.webm';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(self.rfile.read(n));return self.send({'saved':str(target),'bytes':n})
    if not 0<n<=1000000:raise ValueError('Request size limit 1MB')
    value=json.loads(self.rfile.read(n))
    if path=='/api/preview':
     from .m155_failures import summarize
     d=generate(value);return self.send({**{k:v for k,v in d.items()if k!='requests'},'failure_summary':summarize(d)})
    if path=='/api/generate':
     generate(value)
     with lock:
      if any(v['status']in['QUEUED','GENERATING']for v in jobs.values()):return self.send({'error':'A simulation is already running'},409)
      key=uuid.uuid4().hex;jobs[key]={'status':'QUEUED','job_id':key};pool.submit(job,key,value)
     return self.send({'job_id':key},202)
    if path=='/api/scenarios':
     demand=generate(value);key=uuid.uuid4().hex;item={'id':key,'saved_utc':now(),'request':value,'generated':{k:v for k,v in demand.items()if k not in ['request','requests']}};save(SCENARIOS/(key+'.json'),item);return self.send(item)
    if path=='/api/performance':
     save(DOC/'browser-performance'/f'{uuid.uuid4().hex}.json',{'recorded_utc':now(),**value});return self.send({'saved':True})
    return self.send({'error':'Not found'},404)
   except Exception as exc:return self.send({'error':str(exc)},400)
 return Handler
def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=5201);a=p.parse_args();protect();server=ThreadingHTTPServer(('127.0.0.1',a.port),handler(a.port));print(f'M15.5 staging http://127.0.0.1:{a.port}/',flush=True);server.serve_forever()
if __name__=='__main__':main()
