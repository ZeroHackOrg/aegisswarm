# src/aegisswarm/cli/telemetry_ui.py
import json
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import List

LIVE_THREAT_FEED: List[dict] = []


class TelemetryMeshHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/api/v1/swarm/alerts":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"system_state": "active", "threats": LIVE_THREAT_FEED}).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = f"""
            <html>
                <head><title>AegisSwarm Control Hub</title></head>
                <body style='font-family:sans-serif; background:#06090c; color:#ff4444; padding:40px;'>
                    <h1>🛡️ AegisSwarm Defensive Grid Control Center</h1>
                    <p>Status: <span style="color:#00ffcc;">MONITORING SYSTEM ENVIRONMENT INTERFACES</span></p>
                    <div style='background:#0d1117; border:1px solid #21262d; padding:20px; border-radius:8px; box-shadow: 0 4px 10px rgba(255,0,0,0.1);'>
                        <h3>Captured Autonomous Virus Events: {len(LIVE_THREAT_FEED)}</h3>
                    </div>
                </body>
            </html>
            """
            self.wfile.write(html.encode())


def run_telemetry_console(port: int = 9999, feed_store: list = None) -> HTTPServer:
    global LIVE_THREAT_FEED
    if feed_store is not None:
        LIVE_THREAT_FEED = feed_store
    server = HTTPServer(("", port), TelemetryMeshHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"📡 [AegisSwarm Web Interface] Live analytics grid ready at http://localhost:{port}")
    return server