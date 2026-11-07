"""Loopback preview; never opens Chrome and never runs a traffic simulation."""
import argparse
from pathlib import Path
import shutil
import socket
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();child=None
    try:
        node=shutil.which('node');vite=ROOT/'frontend/node_modules/vite/bin/vite.js'
        if not node or not vite.exists() or not (ROOT/'frontend/public/network/m03/strict.json').exists():raise RuntimeError('Missing Node/Vite/network export. See MILESTONE_03_README.md.')
        with socket.socket() as sock:sock.bind(('127.0.0.1',5175))
        print('M03 preview prerequisites PASS; no traffic simulation.',flush=True)
        if args.check:return 0
        print('Open in Codex internal browser: http://127.0.0.1:5175/network.html',flush=True)
        child=subprocess.Popen([node,str(vite),'--config','vite.network.config.ts'],cwd=ROOT/'frontend');return child.wait()
    except KeyboardInterrupt:return 0
    except (RuntimeError,OSError) as e:print(str(e),file=sys.stderr);return 1
    finally:
        if child and child.poll() is None:
            child.terminate()
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();child.wait()
if __name__=='__main__':sys.exit(main())
