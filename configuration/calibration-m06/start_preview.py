"""Start the isolated M06 preview without changing observations or previous viewers."""
from pathlib import Path
import subprocess,sys,time,urllib.request,webbrowser
ROOT=Path(__file__).resolve().parents[2]
URL='http://127.0.0.1:5181/calibration.html'
def ready():
 try:
  with urllib.request.urlopen(URL,timeout=1) as response:return response.status==200 and b'Calibration Lab' in response.read()
 except Exception:return False
if not ready():
 subprocess.Popen(['cmd','/c','npx','vite','--config','vite.calibration.config.ts'],cwd=ROOT/'frontend',creationflags=subprocess.CREATE_NO_WINDOW)
deadline=time.monotonic()+20
while not ready() and time.monotonic()<deadline:time.sleep(.2)
if not ready():raise SystemExit('M06 preview did not become ready on port5181; check for a port conflict.')
print(URL)
if '--no-browser' not in sys.argv:webbrowser.open(URL)
