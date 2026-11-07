"""Offline local survey workbench; bounded JSON, immutable records, no video upload."""
import json,gzip,mimetypes,threading,argparse,traceback
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from .m04_demand import ROOT
from .m085_survey import SurveyStore,DATA,uid
from .m085_export import export_session
from .m085_assets import map_data
from .m085_observer_qc import compare_counts
from .m085_video_annotation import hash_file

def handler(store,ports):
 class Handler(BaseHTTPRequestHandler):
  protocol_version='HTTP/1.1'
  def log_message(self,*args):pass
  def handle(self):
   try:super().handle()
   except (BrokenPipeError,ConnectionAbortedError,ConnectionResetError):pass
  def allowed(self):return self.headers.get('Host') in [f'127.0.0.1:{p}' for p in ports] and self.headers.get('Origin') in [None]+[f'http://127.0.0.1:{p}' for p in ports]
  def reply(self,value,status=200):
   data=json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode();compressed='gzip' in self.headers.get('Accept-Encoding','') and len(data)>1024
   if compressed:data=gzip.compress(data,compresslevel=3)
   self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Connection','close');self.send_header('Transfer-Encoding','chunked')
   if compressed:self.send_header('Content-Encoding','gzip')
   self.end_headers()
   for i in range(0,len(data),16384):chunk=data[i:i+16384];self.wfile.write(f'{len(chunk):X}\r\n'.encode()+chunk+b'\r\n')
   self.wfile.write(b'0\r\n\r\n');self.wfile.flush()
  def file(self,path,attachment=False):
   path=Path(path)
   if not path.is_file():return self.reply({'error':'Berkas tidak ditemukan'},404)
   self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream');self.send_header('Transfer-Encoding','chunked');self.send_header('Cache-Control','no-store');self.send_header('Connection','close');self.send_header('X-Content-Type-Options','nosniff')
   if attachment:self.send_header('Content-Disposition','attachment; filename="'+path.name.replace('"','')+'"')
   if path.suffix=='.html':self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' blob: data:; media-src 'self' blob:; worker-src 'self' blob:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
   self.end_headers()
   with path.open('rb') as stream:
    for chunk in iter(lambda:stream.read(16384),b''):self.wfile.write(f'{len(chunk):X}\r\n'.encode()+chunk+b'\r\n')
   self.wfile.write(b'0\r\n\r\n');self.wfile.flush()
  def do_GET(self):
   if not self.allowed():return self.reply({'error':'Host/Origin ditolak'},403)
   parsed=urlparse(self.path);q=parse_qs(parsed.query);path=parsed.path
   try:
    if path=='/api/m085/state':return self.reply(store.state())
    if path=='/api/m085/ledger':return self.reply(store.ledger(q['session_id'][0],int(q.get('offset',['0'])[0]),int(q.get('limit',['50'])[0])))
    if path=='/api/m085/map':return self.reply(map_data(q['location_id'][0]))
    if path=='/api/m085/qc':return self.reply(compare_counts(store,q['a'][0],q['b'][0]))
    if path=='/api/m085/integrity':return self.reply(store.integrity())
    if path=='/api/m085/audit':
     offset=int(q.get('offset',['0'])[0]);limit=min(100,max(1,int(q.get('limit',['30'])[0])))
     with store.lock,store.connect() as c:return self.reply({'audit':[dict(r) for r in c.execute('SELECT * FROM audit ORDER BY seq DESC LIMIT ? OFFSET ?',(limit,offset))],'rejected':[dict(r) for r in c.execute('SELECT id,command_id,action,reason,created_at FROM rejected_commands ORDER BY rowid DESC LIMIT ? OFFSET ?',(limit,offset))]})
    if path=='/api/m085/exports':return self.reply([json.loads(p.read_text(encoding='utf-8')) for p in sorted((store.root/'exports').glob('*/summary.json'),key=lambda p:p.stat().st_mtime,reverse=True)[:30]])
    if path=='/api/m085/backups':return self.reply([{'id':p.stem,'bytes':p.stat().st_size,'modified':p.stat().st_mtime} for p in sorted((store.root/'backups').glob('*.zip'),key=lambda p:p.stat().st_mtime,reverse=True)[:50]])
    if path=='/api/m085/download':
     kind=q['kind'][0];key=q['id'][0]
     from .m085_provenance import identifier
     identifier(key)
     if kind not in ['exports','backups']:raise ValueError('Kategori unduhan tidak valid')
     name=q.get('file',[None])[0]
     if name:
      if kind!='exports' or name not in ['traffic_count.csv','traffic_count.json','queue.csv','queue.json','travel_time.csv','travel_time.json','signal.csv','signal.json','railway.csv','railway.json','geometry.csv','geometry.json','provenance.json','manifest.json','preimport-rejected.json','m06-rejected.json']:raise ValueError('Berkas unduhan tidak valid')
      return self.file(store.root/kind/key/name,True)
     return self.file(store.root/kind/(key+'.zip'),True)
    static=ROOT/'frontend/dist-m085';relative='survey.html' if path=='/' else path.lstrip('/');target=(static/relative).resolve()
    if not target.is_relative_to(static.resolve()):raise ValueError('Path tidak valid')
    return self.file(target)
   except (ValueError,KeyError,StopIteration) as e:return self.reply({'error':str(e)},400)
   except Exception as e:return self.reply({'error':'Penyimpanan/layanan lokal gagal: '+str(e)},500)
  def body(self):
   n=int(self.headers.get('Content-Length','0'))
   if not 0<n<=16*1024*1024:raise ValueError('Ukuran JSON dibatasi16MiB; video asli tidak boleh diupload')
   self.connection.settimeout(30);return json.loads(self.rfile.read(n),parse_constant=lambda s:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))
  def do_POST(self):
   if not self.allowed():return self.reply({'error':'Host/Origin ditolak'},403)
   try:
    path=urlparse(self.path).path
    if path=='/api/m085/restore-upload':
     n=int(self.headers.get('Content-Length','0'))
     if not 0<n<=128*1024*1024:raise ValueError('Backup ZIP dibatasi128MiB; tidak boleh berisi video')
     target=store.root/'restore-uploads'/(uid()+'.zip');target.parent.mkdir(exist_ok=True);self.connection.settimeout(30)
     with target.open('wb') as out:
      remaining=n
      while remaining:
       chunk=self.rfile.read(min(65536,remaining))
       if not chunk:raise ValueError('Upload backup terputus; staging dipertahankan')
       out.write(chunk);remaining-=len(chunk)
     return self.reply(store.restore(target,self.headers.get('X-Restore-Confirmation','')))
    if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.reply({'error':'JSON diperlukan; tidak ada endpoint upload video'},415)
    p=self.body()
    if path=='/api/m085/command':return self.reply(store.command(p['action'],p.get('payload',{}),p['command_id']))
    if path=='/api/m085/export':return self.reply(export_session(store,p['session_id']))
    if path=='/api/m085/backup':return self.reply(store.backup())
    if path=='/api/m085/restore':
     from .m085_provenance import identifier
     return self.reply(store.restore(store.root/'backups'/(identifier(p['backup_id'])+'.zip'),p.get('confirmation')))
    if path=='/api/m085/hash-local-file':return self.reply(hash_file(p['path']))
    return self.reply({'error':'Endpoint tidak ditemukan'},404)
   except (ValueError,KeyError,TypeError) as e:return self.reply({'error':str(e)},400)
   except Exception as e:return self.reply({'error':'Penyimpanan/layanan lokal gagal: '+str(e)},500)
 return Handler
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--data-dir',type=Path,default=DATA);parser.add_argument('--api-port',type=int,default=8774);parser.add_argument('--ui-port',type=int,default=5184);parser.add_argument('--api-only',action='store_true');parser.add_argument('--synthetic-environment',action='store_true');a=parser.parse_args();store=SurveyStore(a.data_dir,a.synthetic_environment);cls=handler(store,[a.api_port,a.ui_port]);api=ThreadingHTTPServer(('127.0.0.1',a.api_port),cls)
 if not a.api_only:threading.Thread(target=ThreadingHTTPServer(('127.0.0.1',a.ui_port),cls).serve_forever,daemon=True).start()
 print(f'M08.5 offline workbench http://127.0.0.1:{a.ui_port}/survey.html; API{a.api_port}; database{store.path}',flush=True);api.serve_forever()
if __name__=='__main__':main()
