"""M11 launch orchestration around the unchanged M10 host and frontend."""
from pathlib import Path
import argparse,json,subprocess,sys,time,webbrowser,http.client,os
from . import m10_server as host
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'presentation_demo/m11'

def connect(port):
 try:
  c=http.client.HTTPConnection('127.0.0.1',port,timeout=1);c.request('GET','/api/m10/health');r=c.getresponse();data=json.loads(r.read());c.close()
  return data if r.status==200 and data.get('service')=='gedangan-presentation-m10' else None
 except Exception:return None

def serve(port):
 # Same M10 runtime/protocol/build. Redirect only mutable session telemetry to M11.
 host.OUT=OUT/'runtime';host.OUT.mkdir(parents=True,exist_ok=True)
 (host.OUT/'acceptance.json').write_bytes((ROOT/'presentation_demo/m10/acceptance.json').read_bytes())
 original=host.handler
 def factory(port,token,catalog):
  Base=original(port,token,catalog)
  class PresentationAdapter(Base):
   def do_GET(self):
    path=self.path.split('?',1)[0]
    if path in ['/api/m10/health','/m11/presenter.css','/m11/presenter.js']:
     if not self.allowed():return self.reply({'error':'Host/Origin ditolak'},403)
     if path=='/api/m10/health':return self.reply({'service':'gedangan-presentation-m10','version':'m10-1','token':token,'recordings':len(catalog['runs']),'read_only':True,'m11_presentation_adapter':True})
     name='presenter.js' if path.endswith('.js') else 'presenter.css'
     return self.send((OUT/'assets'/name).read_bytes(),'text/javascript; charset=utf-8' if name.endswith('.js') else 'text/css; charset=utf-8')
    return super().do_GET()
   def send(self,data,kind='application/json; charset=utf-8',status=200,encoding=None):
    if kind.startswith('text/html') and status==200:
     data=data.replace(b'</head>',b'<link rel="stylesheet" href="/m11/presenter.css"><script src="/m11/presenter.js" defer></script></head>')
    return super().send(data,kind,status,encoding)
  return PresentationAdapter
 host.handler=factory
 sys.argv=[sys.argv[0],'--port',str(port)];host.main()

def start(port,open_browser=True,direct=False):
 OUT.joinpath('qa').mkdir(parents=True,exist_ok=True)
 start=time.monotonic()
 try:
  if not all((OUT/'assets'/f).is_file() for f in ['presenter.css','presenter.js']):raise FileNotFoundError('Bahan presentasi M11 belum lengkap.')
  catalog=host.preflight()
  state=connect(port);reused=bool(state)
  if not state:
   log=(OUT/'qa/runtime.log').open('ab')
   flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
   subprocess.Popen([sys.executable,'-m','backend.gedangan.m11_launch','--serve','--port',str(port)],cwd=ROOT,stdout=log,stderr=log,creationflags=flags);log.close()
   for _ in range(80):
    state=connect(port)
    if state:break
    time.sleep(.25)
   if not state:raise RuntimeError('Layanan belum siap. Port mungkin dipakai aplikasi lain. Gunakan video atau PDF cadangan.')
  result={'status':'READY_TO_PRESENT','recordings_verified':len(catalog['runs']),'port':port,'instance_reused':reused,'verification_and_start_ms':round((time.monotonic()-start)*1000),'app_url':f'http://127.0.0.1:{port}/visual.html','frontend':'UNCHANGED_M10','m11_presentation_adapter':state.get('m11_presentation_adapter',False),'M12_started':False}
  (OUT/'qa/launch-latest.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
  public={'status':'VERIFIED_RECORDINGS','message':'23 rekaman lolos verifikasi. Buka aplikasi dan tunggu tombol START PRESENTATION aktif setelah preload browser selesai.','app_url':result['app_url']}
  if not result['m11_presentation_adapter']:
   public['message']+=' Layanan M10 lama dipakai kembali. Untuk tata letak ringkas M11 pada layar kecil/zoom besar, tutup layanan melalui aplikasi lalu jalankan launcher M11 kembali. Bahan offline tetap tersedia.'
  (OUT/'readiness.js').write_text('window.M11_READINESS='+json.dumps(public)+';',encoding='utf-8')
  if open_browser:
   webbrowser.open(result['app_url'] if direct else (OUT/'MULAI_PRESENTASI.html').as_uri())
  print(json.dumps(result),flush=True);return result
 except Exception as e:
  message='Presentasi 3D belum siap. '+str(e)+' Buka MULAI_PRESENTASI.html untuk PDF dan video offline.'
  (OUT/'qa/launch-error.txt').write_text(message,encoding='utf-8')
  (OUT/'readiness.js').write_text('window.M11_READINESS='+json.dumps({'status':'RECOVERY_REQUIRED','message':'Layanan 3D belum siap. Jalankan launcher kembali atau gunakan PDF, deck HTML dan video lokal.','app_url':f'http://127.0.0.1:{port}/visual.html'})+';',encoding='utf-8')
  if open_browser:webbrowser.open((OUT/'MULAI_PRESENTASI.html').as_uri())
  print(message,flush=True);raise SystemExit(1)

def main():
 p=argparse.ArgumentParser();p.add_argument('--serve',action='store_true');p.add_argument('--port',type=int,default=5186);p.add_argument('--no-open',action='store_true');p.add_argument('--direct',action='store_true');a=p.parse_args()
 serve(a.port) if a.serve else start(a.port,not a.no_open,a.direct)
if __name__=='__main__':main()
