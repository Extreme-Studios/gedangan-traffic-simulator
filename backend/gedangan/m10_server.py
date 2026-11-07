"""Offline read-only presentation host with verified cache and clean shutdown."""
import argparse,json,gzip,threading,mimetypes,time,webbrowser,sys
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'presentation_demo/m10'
BASE_OUT=ROOT/'presentation_demo/m09'
CACHE=BASE_OUT/'cache'
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
PORT=5186
def preflight():
 catalog=load(CACHE/'catalog.json')
 if catalog!=load(BASE_OUT/'M09_DEMO_MANIFEST.json'):raise ValueError('Catalog/manifest mismatch; rebuild presentation cache')
 for r in catalog['runs']:
  p=CACHE/r['index']
  if digest(p)!=r['index_sha256']:raise ValueError('Recording index hash mismatch: '+r['id'])
  index=json.loads(gzip.decompress(p.read_bytes()))
  if index['network_sha256']!=r['network_sha256'] or index['cohort_sha256']!=r['cohort_sha256']:raise ValueError('Run identity mismatch')
  for c in index['chunks']:
   if digest(CACHE/c['path'])!=c['sha256']:raise ValueError('Trajectory chunk hash mismatch')
  scene=CACHE/index['scene']
  if not scene.is_file() or digest(scene)!=index['scene_sha256'] or json.loads(gzip.decompress(scene.read_bytes()))['network_sha256']!=r['network_sha256']:raise ValueError('Scene missing or mismatched')
 if not (ROOT/'frontend/dist-m10/visual.html').is_file():raise ValueError('Build 3D belum tersedia. Jalankan REBUILD_VISUAL_M10.bat.')
 return catalog
def handler(port,token,catalog):
 class Handler(BaseHTTPRequestHandler):
  protocol_version='HTTP/1.1'
  def log_message(self,*args):pass
  def handle(self):
   try:super().handle()
   except (ConnectionResetError,ConnectionAbortedError,BrokenPipeError):pass
  def allowed(self):return self.headers.get('Host')==f'127.0.0.1:{port}' and self.headers.get('Origin') in [None,f'http://127.0.0.1:{port}']
  def send(self,data,kind='application/json; charset=utf-8',status=200,encoding=None):
   self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Transfer-Encoding','chunked');self.send_header('Connection','close');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
   if encoding:self.send_header('Content-Encoding',encoding)
   self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self'; worker-src 'self' blob:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'");self.end_headers()
   for i in range(0,len(data),16384):chunk=data[i:i+16384];self.wfile.write(f'{len(chunk):X}\r\n'.encode()+chunk+b'\r\n')
   self.wfile.write(b'0\r\n\r\n');self.wfile.flush()
  def reply(self,v,status=200):return self.send(json.dumps(v,ensure_ascii=False,allow_nan=False).encode(),status=status)
  def do_GET(self):
   if not self.allowed():return self.reply({'error':'Host/Origin ditolak'},403)
   path=urlparse(self.path).path
   if path=='/api/m10/health':return self.reply({'service':'gedangan-presentation-m10','version':'m10-1','token':token,'recordings':len(catalog['runs']),'read_only':True,'status':'READY_TO_OPEN_NOT_VISUAL_ACCEPTANCE'})
   if path=='/api/m10/catalog':return self.reply({**catalog,'m10_status':load(OUT/'acceptance.json').get('status','IN_PROGRESS') if (OUT/'acceptance.json').is_file() else 'IN_PROGRESS'})
   folder=CACHE if path.startswith('/cache/') else ROOT/'frontend/dist-m10';relative=path[len('/cache/'):] if path.startswith('/cache/') else 'visual.html' if path=='/' else path.lstrip('/');p=(folder/relative).resolve()
   if not p.is_relative_to(folder.resolve()) or not p.is_file():return self.reply({'error':'Asset demo tidak tersedia; tidak ada fallback ke tahun/run lain'},404)
   compressed=p.suffix=='.gz';kind='application/json; charset=utf-8' if compressed or p.suffix=='.json' else mimetypes.guess_type(p.name)[0] or 'application/octet-stream';return self.send(p.read_bytes(),kind,encoding='gzip' if compressed else None)
  def do_POST(self):
   if not self.allowed():return self.reply({'error':'Host/Origin ditolak'},403)
   n=int(self.headers.get('Content-Length','0'))
   if not 0<n<65536:return self.reply({'error':'Request dibatasi'},400)
   try:p=json.loads(self.rfile.read(n))
   except Exception:return self.reply({'error':'JSON tidak valid'},400)
   if self.path=='/api/m10/shutdown' and p.get('token')==token:
    self.reply({'closed':True});threading.Thread(target=self.server.shutdown,daemon=True).start();return
   if self.path=='/api/m10/performance':
    # Only bounded numeric counters; no browsing history, paths or hardware identity.
    allowed=['fps_mean','fps_p5','draw_calls','triangles','geometries','textures','visible_vehicles','stalls_over_50ms','viewport','recording','scope'];v={k:p[k] for k in allowed if k in p};OUT.joinpath('qa').mkdir(exist_ok=True)
    with (OUT/'qa/browser-performance.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(v,allow_nan=False)+'\n')
    return self.reply({'saved':True})
   return self.reply({'error':'Tidak ada mutasi simulation/source melalui presentation host'},403)
 return Handler
def existing(port):
 import http.client
 try:
  c=http.client.HTTPConnection('127.0.0.1',port,timeout=2);c.request('GET','/api/m10/health');r=c.getresponse();v=json.loads(r.read());c.close();return v if v.get('service')=='gedangan-presentation-m10' else None
 except Exception:return None
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=PORT);parser.add_argument('--open',action='store_true');a=parser.parse_args();url=f'http://127.0.0.1:{a.port}/visual.html'
 if existing(a.port):
  if a.open:webbrowser.open(url)
  print('Presentation server sudah aktif: '+url,flush=True);return
 try:catalog=preflight()
 except Exception as e:print('Demo belum siap: '+str(e),flush=True);raise SystemExit(1)
 import secrets
 token=secrets.token_urlsafe(24)
 try:server=ThreadingHTTPServer(('127.0.0.1',a.port),handler(a.port,token,catalog))
 except OSError:print('Port dipakai aplikasi lain. Tidak dihentikan atau diubah. Jalankan dengan --port lain.',flush=True);raise SystemExit(1)
 print('Gedangan presentation: '+url+' · '+str(len(catalog['runs']))+' actual SUMO recordings. Ctrl+C atau Tutup layanan di aplikasi untuk berhenti.',flush=True)
 if a.open:threading.Timer(.3,lambda:webbrowser.open(url)).start()
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close();print('Presentation server ditutup dengan bersih.',flush=True)
if __name__=='__main__':main()
