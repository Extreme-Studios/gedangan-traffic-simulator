from pathlib import Path
import subprocess,urllib.request,time,sys,webbrowser
ROOT=Path(__file__).resolve().parents[2]
def ready(url):
 try:
  with urllib.request.urlopen(url,timeout=2) as r:return r.status==200
 except Exception:return False
api='http://127.0.0.1:8773/api/m08/state';url='http://127.0.0.1:5183/solutions.html'
if not ready(api):subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-m','backend.gedangan.m08_server'],cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW)
if not ready(url):subprocess.Popen(['cmd','/c','npx','--no-install','vite','--config','vite.solutions.config.ts'],cwd=ROOT/'frontend',creationflags=subprocess.CREATE_NO_WINDOW)
deadline=time.monotonic()+25
while time.monotonic()<deadline and not (ready(api) and ready(url)):time.sleep(.2)
if not ready(api) or not ready(url):raise SystemExit('M08 API/UI not ready; inspect ports8773/5183. No new dependencies installed.')
print(url)
if '--no-browser' not in sys.argv:webbrowser.open(url)
