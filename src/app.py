import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_NAME = os.getenv("APP_NAME", "Jenkins CI/CD Demo")
APP_ENV = os.getenv("APP_ENV", "production")
PORT = int(os.getenv("PORT", "8080"))

def health_payload():
    return {
        "status": "ok",
        "app": APP_NAME,
        "environment": APP_ENV
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps(health_payload()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            body = f"{APP_NAME} is running in {APP_ENV} mode.\n".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"{APP_NAME} listening on port {PORT}")
    server.serve_forever()
