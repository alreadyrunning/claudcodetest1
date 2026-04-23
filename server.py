import http.server
import json
import os

PORT = 8000
PROGRESS_FILE = "progress.json"


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/load":
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, "r") as f:
                    data = f.read()
            else:
                data = "{}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data.encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/save":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            with open(PROGRESS_FILE, "w") as f:
                f.write(body.decode())
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # silence request logs


print(f"Server running at http://localhost:{PORT}")
print("Open learning-path.html in your browser at that address.")
print("Press Ctrl+C to stop.\n")

with http.server.HTTPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
