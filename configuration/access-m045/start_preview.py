from pathlib import Path
import argparse
import shutil
import socket
import subprocess
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();child=None
    try:
        node=shutil.which('node');vite=ROOT/'frontend/node_modules/vite/bin/vite.js'
        if not node or not vite.is_file() or not (ROOT/'frontend/public/access/m045/summary.json').is_file():raise RuntimeError('M04.5 build output or frontend dependency missing')
        with socket.socket() as s:s.bind(('127.0.0.1',5178))
        print('M04.5 preview prerequisites PASS',flush=True)
        if args.check:return 0
        print('Internal browser: http://127.0.0.1:5178/multiclass.html',flush=True)
        child=subprocess.Popen([node,str(vite),'--config','vite.multiclass.config.ts'],cwd=ROOT/'frontend');return child.wait()
    except KeyboardInterrupt:return 0
    except (OSError,RuntimeError) as exc:print(str(exc));return 1
    finally:
        if child and child.poll() is None:
            child.terminate()
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();child.wait()
if __name__=='__main__':raise SystemExit(main())
