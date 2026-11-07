"""Start two loopback services without touching old launchers/data."""
from pathlib import Path
import subprocess,urllib.request,time,sys,webbrowser
ROOT=Path(__file__).resolve().parents[2]
def ready(url):
 try:
  with urllib.request.urlopen(url,timeout=2) as response:return response.status==200
 except Exception:return False
api='http://127.0.0.1:8772/api/m07/state';url='http://127.0.0.1:5182/projection.html'
if not ready(api):subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-m','backend.gedangan.m07_server'],cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW)
if not ready(url):subprocess.Popen(['cmd','/c','npx','vite','--config','vite.projection.config.ts'],cwd=ROOT/'frontend',creationflags=subprocess.CREATE_NO_WINDOW)
deadline=time.monotonic()+25
while time.monotonic()<deadline and not (ready(api) and ready(url)):time.sleep(.2)
if not ready(api) or not ready(url):raise SystemExit('M07 API/UI not ready. Check ports8772/5182 and local dependencies.')
print(url)
if '--no-browser' not in sys.argv:webbrowser.open(url)
