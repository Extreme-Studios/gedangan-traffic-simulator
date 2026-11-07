"""Reuse healthy M13 service or start a hidden local server, then open calendar."""
import urllib.request,subprocess,webbrowser,time
from .m13_common import *
def healthy():
 try:
  with urllib.request.urlopen('http://127.0.0.1:5197/api/health',timeout=1)as r:return json.load(r).get('service')=='Gedangan M13 historical foundation'
 except Exception:return False
def main():
 if not healthy():
  DOC.mkdir(parents=True,exist_ok=True)
  with (DOC/'launcher-server.log').open('a')as log:subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-m','backend.gedangan.m13_server'],cwd=ROOT,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
  for _ in range(40):
   if healthy():break
   time.sleep(.25)
 if healthy():webbrowser.open('http://127.0.0.1:5197/')
 else:(DOC/'launch-error.txt').write_text('M13 service failed. Inspect launcher-server.log.',encoding='utf-8')
if __name__=='__main__':main()
