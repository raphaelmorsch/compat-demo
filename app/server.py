import http.server
import socketserver
import os
import socket
import json
import urllib.parse
import subprocess

PORT = int(os.environ.get("PORT", "8080"))

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

        # Root
        if path == "/":
            self._send_response(200, "OK - compat demo running\n")

        # Health endpoint
        elif path == "/health":
            self._send_response(200, "healthy\n")

        # Info endpoint
        elif path == "/info":
            data = {
                "hostname": socket.gethostname(),
                "pod_ip": get_ip(),
                "port": PORT,
                "env": dict(os.environ)
            }
            self._send_response(
                200,
                json.dumps(data, indent=2),
                content_type="application/json"
            )

        # DNS test: /dns?host=google.com
        elif path == "/dns":
            host = query.get("host", [""])[0]
            if not host:
                self._send_response(400, "missing ?host=\n")
                return
            try:
                ip = socket.gethostbyname(host)
                self._send_response(200, f"{host} -> {ip}\n")
            except Exception as e:
                self._send_response(500, f"DNS error: {str(e)}\n")

        # TCP test: /tcp?host=google.com&port=443
        elif path == "/tcp":
            host = query.get("host", [""])[0]
            port = int(query.get("port", [0])[0])
            if not host or not port:
                self._send_response(400, "missing ?host=&port=\n")
                return
            try:
                with socket.create_connection((host, port), timeout=5):
                    self._send_response(200, f"TCP connection to {host}:{port} successful\n")
            except Exception as e:
                self._send_response(500, f"TCP error: {str(e)}\n")

        # Exec ping (se instalado no container)
        elif path == "/ping":
            host = query.get("host", [""])[0]
            if not host:
                self._send_response(400, "missing ?host=\n")
                return
            try:
                result = subprocess.run(
                    ["ping", "-c", "2", host],
                    capture_output=True,
                    text=True
                )
                self._send_response(200, result.stdout)
            except Exception as e:
                self._send_response(500, f"Ping error: {str(e)}\n")

        else:
            self._send_response(404, "Not found\n")

    def log_message(self, format, *args):
        # Loga no stdout do container
        print(f"{self.client_address[0]} - {format % args}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()