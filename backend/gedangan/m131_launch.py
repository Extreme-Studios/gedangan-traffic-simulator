import urllib.request,subprocess,webbrowser,time
from .m131_database import DOC131
from .m13_common import *
def healthy():
 try:
  with urllib.request.urlopen('http://127.0.0.1:5198/api/health',timeout=1)as r:return json.load(r).get('service')=='Gedangan M13.1 public evidence archive'
 except Exception:return False
def main():
 if not healthy():
  DOC131.mkdir(parents=True,exist_ok=True)
  with (DOC131/'launcher.log').open('a')as log:subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-m','backend.gedangan.m131_server'],cwd=ROOT,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
  for _ in range(40):
   if healthy():break
   time.sleep(.25)
 if healthy():webbrowser.open('http://127.0.0.1:5198/')
if __name__=='__main__':main()
