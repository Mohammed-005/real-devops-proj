import os
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
APP_VERSION = os.environ.get("APP_VERSION", "v2")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

PORT = 7000

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/health':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
            return

        elif self.path == '/':
            visits = r.incr("visits")

            response = {
                    "status": "ok",
                    "version": APP_VERSION,
                    "visits": int(visits),
                    "service": "final-system"
                    }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.end_headers()

server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server running on port {PORT}")
server.serve_forever()
