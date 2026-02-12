import http.server
import socketserver
import json
import os
import datetime

PORT = 8002

class CardHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save/cards':
            filename = 'cards.json'
        elif self.path == '/save/relationships':
            filename = 'relationships.json'
        else:
            self.send_error(404, "Not Found")
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # Validate JSON before saving
            data = json.loads(post_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            # Get details for feedback
            abs_path = os.path.abspath(filename)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success", 
                "file": filename,
                "path": abs_path,
                "timestamp": timestamp
            }).encode())
            print(f"Saved {filename} at {timestamp}")
        except Exception as e:
            self.send_error(500, str(e))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

print(f"Starting Card Nexus Server...")
print(f"Open your browser to: http://localhost:{PORT}/card_manager.html")
print("Press Ctrl+C to stop.")

with socketserver.TCPServer(("", PORT), CardHandler) as httpd:
    httpd.serve_forever()
