"""M13 availability + staged import/review. Separate read model from legacy runner."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from functools import lru_cache
import argparse,base64,mimetypes,threading
from .m13_database import Store
from .m13_common import *
from .m13_seed import seed
UI=ROOT/'frontend/m13'
def handler(store,port):
 @lru_cache(maxsize=100)
 def monthly(month,version,filter_json):return store.monthly(month,json.loads(filter_json))
 class Handler(BaseHTTPRequestHandler):
  protocol_version='HTTP/1.1'
  def log_message(self,*args):pass
  def allowed(self):return self.headers.get('Host')==f'127.0.0.1:{port}'and self.headers.get('Origin')in [None,f'http://127.0.0.1:{port}']
  def send(self,value,status=200,kind='application/json; charset=utf-8'):
   body=value if isinstance(value,bytes)else json.dumps(value,ensure_ascii=False,allow_nan=False).encode();self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'");self.send_header('Transfer-Encoding','chunked');self.send_header('Connection','close');self.end_headers()
   try:
    for i in range(0,len(body),16384):
     chunk=body[i:i+16384];self.wfile.write(f'{len(chunk):X}\r\n'.encode()+chunk+b'\r\n')
    self.wfile.write(b'0\r\n\r\n');self.wfile.flush()
   except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
  def do_GET(self):
   if not self.allowed():return self.send({'error':'Host/Origin denied'},403)
   u=urlparse(self.path);q={k:v[0]for k,v in parse_qs(u.query).items()};filters={k:q[k]for k in ['road_segment','direction','vehicle_class','parameter']if q.get(k)}
   try:
    if u.path=='/api/health':return self.send({'service':'Gedangan M13 historical foundation','dataset_version':store.version(),'test_database':store.test_fixture,'observed_calendar_only':True})
    if u.path=='/api/scope':return self.send(store.scope())
    if u.path=='/api/monthly':return self.send(monthly(q['month'],store.version(),json.dumps(filters,sort_keys=True)))
    if u.path=='/api/daily':return self.send(store.daily(q['date'],filters))
    if u.path=='/api/hourly':return self.send(store.hour(q['date'],int(q['hour']),filters))
    if u.path in ['/api/roads','/api/directions','/api/classes']:return self.send(store.dimensions({'/api/roads':'road_segment','/api/directions':'direction','/api/classes':'vehicle_class'}[u.path]))
    if u.path=='/api/provenance':return self.send(store.provenance())
    if u.path=='/api/source-audit':return self.send({'local':load(DOC/'source-file-audit.json'),'web':load(DOC/'web-source-audit.json'),'source_page_is_not_vehicle_dataset':True})
    if u.path=='/api/staged':return self.send({'rows':store.rows(),'test_database':store.test_fixture})
    if u.path=='/api/reference':
     from .recovery_data import build_demand
     request={'date':q['date'],'time':q['time'],'demand_mode':'REFERENCE_ESTIMATE','acknowledge_estimate':True,'horizon_s':900,'warmup_s':300,'seed':42};result=build_demand(request)
     return self.send({'mode':'REFERENCE-BASED TRAFFIC SCENARIO','historical_observation':False,'label':'ESTIMASI REFERENSI — BUKAN OBSERVASI HISTORIS','preview':{k:v for k,v in result.items()if k!='requests'},'runner_url':'http://127.0.0.1:5196/','automatic_runner_submission':False})
    if u.path=='/api/template':
     columns=['observation_date','observation_time','time_zone','interval_start','interval_end','road_segment','direction','vehicle_class','vehicle_count','turning_movement','speed','queue_length','travel_time','measurement_unit'];return self.send((','.join(columns)+'\r\n').encode(),kind='text/csv; charset=utf-8')
    p=(UI/('index.html'if u.path=='/'else u.path.lstrip('/'))).resolve()
    if not p.is_relative_to(UI.resolve())or not p.is_file():return self.send({'error':'Not found'},404)
    return self.send(p.read_bytes(),kind=mimetypes.guess_type(p.name)[0]or'application/octet-stream')
   except (KeyError,ValueError,TypeError,FileNotFoundError)as exc:return self.send({'error':str(exc)},400)
  def do_POST(self):
   if not self.allowed():return self.send({'error':'Host/Origin denied'},403)
   try:
    n=int(self.headers.get('Content-Length','0'))
    if not 0<n<=8500000:raise ValueError('Request size limit8.5MB')
    value=json.loads(self.rfile.read(n))
    if self.path=='/api/import':return self.send(store.import_bytes(value['filename'],base64.b64decode(value['base64'],validate=True),value['source']))
    if self.path=='/api/review':return self.send(store.review(value['ids'],value['decision'],value['reviewer'],value['note'],value['evidence_checked']))
    if self.path=='/api/select':
     result=store.hour(value['date'],int(value['hour']),value.get('filters'))
     if result['disabled']:raise ValueError('MISSING: historical hour disabled; no fallback to another date or estimate')
     return self.send({'selection':result,'automatic_imputation':False,'readiness':'Observation evidence selected; SUMO route/endpoints and calibration need a separate reviewed mapping. No historical simulation result claimed.'})
    return self.send({'error':'Not found'},404)
   except (KeyError,ValueError,TypeError,sqlite3.Error)as exc:return self.send({'error':str(exc)},400)
 return Handler
def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=5197);a=p.parse_args();store=Store();seed(store);server=ThreadingHTTPServer(('127.0.0.1',a.port),handler(store,a.port));print(f'M13 http://127.0.0.1:{a.port}/ - ACTUAL OBSERVATION AVAILABILITY ONLY',flush=True);server.serve_forever()
if __name__=='__main__':main()
