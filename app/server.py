import http.server
import socketserver
import os
import socket
import json
import urllib.parse

PORT = int(os.environ.get("PORT", "8080"))
APP_VERSION = os.environ.get("APP_VERSION", "2.0")

def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "unknown"

class Handler(http.server.BaseHTTPRequestHandler):
    def _send_response(self, code=200, body="", content_type="text/plain"):
        self.send_response(code)
        self.send_header("Content-type", f"{content_type}; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/":
            self._send_response(200, "OK - compat demo running\n")

        elif path == "/health":
            self._send_response(200, "healthy\n")

        elif path == "/info":
            data = {
                "hostname": socket.gethostname(),
                "pod_ip": get_ip(),
                "port": PORT,
                "app_version": APP_VERSION
            }
            self._send_response(200, json.dumps(data, indent=2), "application/json")

        elif path == "/version":
            self._send_response(200, f"compat-demo version {APP_VERSION}\n")

        elif path == "/headers":
            headers = {k: v for k, v in self.headers.items()}
            self._send_response(200, json.dumps(headers, indent=2), "application/json")

        elif path == "/echo":
            msg = query.get("msg", [""])[0]
            if not msg:
                self._send_response(400, "missing ?msg=\n")
                return
            self._send_response(200, f"echo: {msg}\n")

        else:
            self._send_response(404, "Not found\n")

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()