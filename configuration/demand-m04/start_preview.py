"""M04 loopback-only viewer, no simulation or browser auto-launch."""
import argparse
from pathlib import Path
import shutil
import socket
import subprocess
ROOT=Path(__file__).resolve().parents[2]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();child=None
    try:
        vite=ROOT/'frontend/node_modules/vite/bin/vite.js';node=shutil.which('node')
        if not node or not vite.is_file() or not (ROOT/'frontend/public/demand/m04/summary.json').is_file():raise RuntimeError('Missing M04 outputs or frontend dependencies. Read MILESTONE_04_README.md.')
        with socket.socket() as sock:sock.bind(('127.0.0.1',5176))
        print('M04 prerequisites PASS. Recorded synthetic results only.',flush=True)
        if args.check:return 0
        print('Codex internal browser: http://127.0.0.1:5176/demand.html',flush=True)
        child=subprocess.Popen([node,str(vite),'--config','vite.demand.config.ts'],cwd=ROOT/'frontend');return child.wait()
    except KeyboardInterrupt:return 0
    except (RuntimeError,OSError) as exc:print(str(exc));return 1
    finally:
        if child and child.poll() is None:
            child.terminate()
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();child.wait()
if __name__=='__main__':raise SystemExit(main())
