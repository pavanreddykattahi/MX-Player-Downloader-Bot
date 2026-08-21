"""Health-check HTTP server wrapper.

Starts a minimal HTTP server on port 8000 (responds 200 OK to any GET),
then runs dkbotz.py as the main Telegram bot process in the same thread.
"""
import threading
import http.server


class _HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass  # suppress access logs


def _start_health_server(port: int = 8000):
    server = http.server.HTTPServer(("0.0.0.0", port), _HealthHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()


if __name__ == "__main__":
    _start_health_server(8000)
    # Run the bot — blocks until the process exits
    import runpy
    runpy.run_path("dkbotz.py", run_name="__main__")
