# src/aegisswarm/cli/telemetry_ui.py
"""
AegisSwarm Telemetry UI Dashboard
Provides a web-based operational control center for monitoring intercepted
autonomous viruses, AI credential stealers, and memory dump attacks.
"""

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
            
            rows = ""
            for alert in LIVE_THREAT_FEED[-15:]:
                badge_color = "#da3633" if "STEALER" in alert.get('summary','') else "#9e6a03"
                rows += f"""
                <tr>
                    <td>{alert.get('pid', 'N/A')}</td>
                    <td><code>{alert.get('comm', 'Unknown')}</code></td>
                    <td><span style="background: {badge_color}; color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">{alert.get('badge', '[AI_CREDENTIAL_STEALER]')}</span></td>
                    <td>{alert.get('summary', 'Decoy tripped')}</td>
                    <td><strong style="color: #f85149;">QUARANTINED</strong></td>
                </tr>
                """

            html = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>AegisSwarm Autonomous Threat Dashboard</title>
                    <style>
                        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #06090c; color: #c9d1d9; margin: 0; padding: 30px; }}
                        h1 {{ color: #58a6ff; }}
                        .card {{ background: #0d1117; border: 1px solid #21262d; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.4); }}
                        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #21262d; font-size: 14px; }}
                        th {{ color: #8b949e; }}
                        .hero {{ background: linear-gradient(135deg, #1f242c 0%, #11141a 100%); border-left: 5px solid #238636; padding: 15px 20px; border-radius: 6px; margin-bottom: 25px; }}
                    </style>
                </head>
                <body>
                    <h1>AegisSwarm Autonomous Defense & AI Stealer Trap</h1>
                    <p>Status: <strong style="color: #00ffcc;">ACTIVE DECOY MATRIX & NETWORK SANDBOX</strong></p>
                    
                    <div class="hero">
                        <h3>Anti-Malware & Anti-AI-Stealer Protection</h3>
                        <p>AegisSwarm protects your infrastructure by deploying fake LLM API keys, cloud credentials (<code>~/.aws/credentials</code>), and file decoys. When autonomous AI malware or credential harvesters attempt to read them, AegisSwarm instantly isolates their PID in a network sandbox.</p>
                    </div>

                    <div class="card">
                        <h3>Captured Threat Interceptions & Autonomous Quarantines ({len(LIVE_THREAT_FEED)})</h3>
                        <table>
                            <thead>
                                <tr><th>PID</th><th>Process</th><th>Threat Badge</th><th>Incident Details</th><th>Status</th></tr>
                            </thead>
                            <tbody>
                                {rows if rows else "<tr><td colspan='5' style='text-align:center; color:#8b949e;'>No active malware triggers recorded yet. Run `aswarm start` to simulate.</td></tr>"}
                            </tbody>
                        </table>
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
    print(f"[AegisSwarm Web Interface] Live analytics grid ready at http://localhost:{port}")
    return server
