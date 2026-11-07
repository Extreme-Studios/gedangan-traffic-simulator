"""Independent M05 localhost viewer launcher."""
from pathlib import Path
import subprocess,sys,urllib.request,webbrowser
ROOT=Path(__file__).resolve().parents[2]
url='http://127.0.0.1:5179/behavior.html'
try:
 with urllib.request.urlopen(url,timeout=2) as r:active=r.status==200
except Exception:active=False
if not active:
 subprocess.Popen(['cmd','/c','npx','vite','--config','vite.behavior.config.ts'],cwd=ROOT/'frontend',creationflags=subprocess.CREATE_NO_WINDOW)
print(url)
if '--no-browser' not in sys.argv:webbrowser.open(url)
