"""Start the packaged M15.6.2 server and publish its assigned loopback port."""
import sys
import socket
import gzip
import json
from pathlib import Path
from http.server import ThreadingHTTPServer

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))

from backend.gedangan import m1562_server

if __name__ == "__main__":
    m1562_server.protect()
    with ThreadingHTTPServer(("127.0.0.1", 0), m1562_server.handler(0)) as server:
        port = server.server_address[1]
        class PortableHandler(m1562_server.handler(port)):
            protocol_version = "HTTP/1.1"

            def setup(self):
                self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                super().setup()

            def send(self, value, code=200, kind="application/json; charset=utf-8", encoding=None):
                if not encoding and "gzip" in self.headers.get("Accept-Encoding", ""):
                    raw = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode()
                    if len(raw) >= 16384:
                        return super().send(gzip.compress(raw, compresslevel=1), code, kind, "gzip")
                return super().send(value, code, kind, encoding)

        server.RequestHandlerClass = PortableHandler
        ready = Path(sys.argv[1])
        pending = ready.with_suffix(".tmp")
        pending.write_text(str(port), encoding="ascii")
        pending.replace(ready)
        server.serve_forever()
