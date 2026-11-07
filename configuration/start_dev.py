"""Own both local processes and stop them on exit. Does not install anything."""
import argparse
import json
import shutil
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]

def prerequisites():
    if sys.version_info < (3,12):raise RuntimeError('Python 3.12+ diperlukan.')
    node=shutil.which('node')
    if not node:raise RuntimeError('Node.js belum tersedia. Baca README.md.')
    version=subprocess.check_output([node,'--version'],text=True).strip().lstrip('v')
    if tuple(int(x) for x in version.split('.')[:2]) < (22,12):
        raise RuntimeError('Launcher proyek memerlukan Node.js 22.12+ (audit: Node 24).')
    vite=ROOT/'frontend/node_modules/vite/bin/vite.js'
    if not vite.is_file():raise RuntimeError('Dependensi frontend belum tersedia. Jalankan npm ci di folder frontend.')
    for port in (5173,8765):
        with socket.socket() as s:
            try:s.bind(('127.0.0.1',port))
            except OSError as e:raise RuntimeError(f'Port {port} sedang dipakai. Tutup proses terkait sebelum menjalankan launcher.') from e
    return node,vite

def main():
    parser=argparse.ArgumentParser(description='Gedangan M01 development launcher; no real simulation')
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--no-browser',action='store_true')
    args=parser.parse_args()
    children=[]
    try:
        node,vite=prerequisites()
        print('Prerequisites PASS. FOUNDATION / ENGINE NOT CONNECTED.',flush=True)
        if args.check:return 0
        children.append(subprocess.Popen([sys.executable,'-m','backend.server'],cwd=ROOT))
        children.append(subprocess.Popen([node,str(vite),'--host','127.0.0.1','--port','5173','--strictPort'],cwd=ROOT/'frontend'))
        ready=False
        for _ in range(100):
            if any(p.poll() is not None for p in children):raise RuntimeError('Proses lokal berhenti saat startup. Periksa error di atas.')
            try:
                with urlopen('http://127.0.0.1:8765/api/health',timeout=.3) as res: health=json.load(res)
                with urlopen('http://127.0.0.1:5173',timeout=.3) as res: page=res.read().decode()
                if health.get('service')=='gedangan-foundation' and 'Gedangan Traffic Simulator' in page:ready=True;break
            except (OSError,ValueError):pass
            time.sleep(.2)
        if not ready:raise RuntimeError('Startup timeout. Backend/frontend belum siap.')
        print('Buka http://127.0.0.1:5173 | Ctrl+C menghentikan kedua server.',flush=True)
        if not args.no_browser:webbrowser.open('http://127.0.0.1:5173')
        while all(p.poll() is None for p in children):time.sleep(.5)
        raise RuntimeError('Salah satu server berhenti. Keduanya akan dihentikan.')
    except KeyboardInterrupt:
        print('\nMenghentikan server lokal.',flush=True);return 0
    except (RuntimeError,OSError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 1
    finally:
        for child in reversed(children):
            if child.poll() is None:child.terminate()
        for child in children:
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();child.wait()

if __name__=='__main__':sys.exit(main())
