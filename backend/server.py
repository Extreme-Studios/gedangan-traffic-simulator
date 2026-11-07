"""Loopback-only read-only foundation API; Python standard library only."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from .gedangan.simulation_controller import SimulationController
from .gedangan.metrics_collector import MetricsCollector

ROOT = Path(__file__).resolve().parents[1]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/api/status':
            payload = SimulationController().status()
        elif path == '/api/metrics':
            payload = MetricsCollector().snapshot()
        elif path == '/api/config':
            payload = json.loads((ROOT / 'configuration' / 'project.json').read_text(encoding='utf-8'))
        elif path == '/api/health':
            payload = {'service': 'gedangan-foundation', 'healthy': True, 'simulation_running': False}
        else:
            self.respond(404, {'error': 'NOT_FOUND'})
            return
        self.respond(200, payload)

    def do_POST(self):
        # Consume bounded request bodies before rejecting, avoiding TCP resets on Windows.
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            self.respond(400, {'error': 'INVALID_CONTENT_LENGTH'})
            return
        if not 0 <= length <= 65536:
            self.respond(413, {'error': 'BODY_TOO_LARGE'})
            return
        self.connection.settimeout(3)
        if length:
            try:
                self.rfile.read(length)
            except OSError:
                self.respond(408, {'error': 'REQUEST_TIMEOUT'})
                return
        self.respond(409, {'error': 'FOUNDATION_ONLY', 'message': 'No simulation or data mutation available in M01.'})

    def respond(self, code, payload):
        data = json.dumps(payload, allow_nan=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    print(f'Gedangan FOUNDATION API http://127.0.0.1:{args.port} — ENGINE NOT CONNECTED', flush=True)
    try:
        ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
