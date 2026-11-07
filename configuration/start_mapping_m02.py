"""M02 local mapping preview. Never automatically launches Chrome/default browser."""
import argparse
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    child=None
    try:
        node=shutil.which('node')
        vite=ROOT/'frontend/node_modules/vite/bin/vite.js'
        data=ROOT/'frontend/public/geodata/m02/map-utm49s.json'
        if not node or not vite.exists() or not data.exists():raise RuntimeError('Node, dependency Vite, atau data peta belum tersedia. Baca MILESTONE_02_README.md.')
        with socket.socket() as s:
            try:s.bind(('127.0.0.1',5174))
            except OSError as e:raise RuntimeError('Port 5174 dipakai. Tutup preview M02 sebelumnya.') from e
        print('M02 mapping prerequisites PASS. No vehicle simulation.',flush=True)
        if args.check:return 0
        child=subprocess.Popen([node,str(vite),'--config','vite.mapping.config.ts'],cwd=ROOT/'frontend')
        for _ in range(100):
            if child.poll() is not None:raise RuntimeError('Vite berhenti saat startup.')
            try:
                with urlopen('http://127.0.0.1:5174/mapping.html',timeout=.4) as r:
                    if r.status==200:break
            except OSError:time.sleep(.2)
        else:raise RuntimeError('Startup timeout.')
        print('Buka di browser internal Codex: http://127.0.0.1:5174/mapping.html',flush=True)
        print('Tidak membuka Chrome otomatis. Ctrl+C menghentikan preview.',flush=True)
        child.wait()
        return child.returncode
    except KeyboardInterrupt:return 0
    except (OSError,RuntimeError) as exc:print(f'ERROR: {exc}',file=sys.stderr);return 1
    finally:
        if child and child.poll() is None:
            child.terminate()
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();child.wait()

if __name__=='__main__':sys.exit(main())
