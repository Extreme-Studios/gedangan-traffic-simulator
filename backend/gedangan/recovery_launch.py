"""Convenient research launcher. Separate from unchanged frozen presentation EXE."""
import sys,subprocess,http.client,time,webbrowser,os,ctypes
from .recovery_common import *
PORT=5196
def health():
 try:
  c=http.client.HTTPConnection('127.0.0.1',PORT,timeout=1);c.request('GET','/api/health');r=c.getresponse();v=json.loads(r.read());c.close();return v if v.get('service')=='gedangan-functional-recovery'else None
 except Exception:return None
def main():
 try:
  from .m04_demand import activate
  activate();state=health()
  if not state:
   DOC.mkdir(parents=True,exist_ok=True);log=(DOC/'research-service.log').open('ab');p=subprocess.Popen([sys.executable,'-m','backend.gedangan.recovery_server'],cwd=ROOT,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt'else 0);log.close()
   for _ in range(100):
    state=health()
    if state:break
    if p.poll()is not None:raise RuntimeError('Layanan berhenti; periksa research-service.log. Port5196 mungkin digunakan aplikasi lain.')
    time.sleep(.2)
   if not state:raise RuntimeError('Layanan belum siap; tidak ada fallback ke EXE playback lama.')
  if '--no-open'not in sys.argv:webbrowser.open(f'http://127.0.0.1:{PORT}/')
  save(DOC/'last-research-launch.json',{'status':'READY','url':f'http://127.0.0.1:{PORT}/','engine':'Local SUMO1.28.0','dependency':'Research .venv + retained local SUMO toolchain; not embedded in old M12 release'})
 except Exception as exc:
  save(DOC/'launch-error.json',{'error':str(exc)})
  if os.name=='nt'and '--no-open'not in sys.argv:ctypes.windll.user32.MessageBoxW(None,'Gedangan research belum siap. '+str(exc),'Gedangan Traffic Research',16)
  raise SystemExit(1)
if __name__=='__main__':main()
