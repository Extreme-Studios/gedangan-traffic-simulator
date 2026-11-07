from pathlib import Path
import subprocess,sys,webbrowser,urllib.request,time
ROOT=Path(__file__).resolve().parents[2];url='http://127.0.0.1:5180/validation.html'
try:
 with urllib.request.urlopen(url,timeout=2) as response:active=response.status==200
except Exception:active=False
if not active:subprocess.Popen(['cmd','/c','npx','vite','--config','vite.validation.config.ts'],cwd=ROOT/'frontend',creationflags=subprocess.CREATE_NO_WINDOW)
deadline=time.monotonic()+15
while not active and time.monotonic()<deadline:
 try:
  with urllib.request.urlopen(url,timeout=1) as response:active=response.status==200
 except Exception:time.sleep(.2)
if not active:raise SystemExit('M05.1 server did not become ready within15s')
print(url)
if '--no-browser' not in sys.argv:webbrowser.open(url)
