import http.server
import socketserver
import json
import os
import datetime

import html

PORT = 8002

class CardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        super().do_GET()

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
            
            # Regenerate raw view on save
            generate_raw_view()

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

def generate_raw_view():
    try:
        try:
            with open('cards.json', 'r', encoding='utf-8') as f:
                cards_data = html.escape(f.read())
        except Exception as e:
            cards_data = f"Error reading cards.json: {e}"

        try:
            with open('relationships.json', 'r', encoding='utf-8') as f:
                relationships_data = html.escape(f.read())
        except Exception as e:
            relationships_data = f"Error reading relationships.json: {e}"

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Raw Data Viewer</title>
            <style>
                body {{ font-family: sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; }}
                h2 {{ color: #60a5fa; }}
                textarea {{ width: 100%; height: 400px; background-color: #1e293b; color: #cbd5e1; border: 1px solid #334155; padding: 10px; font-family: monospace; }}
                .container {{ display: flex; gap: 20px; flex-direction: column; }}
                @media (min-width: 768px) {{ .container {{ flex-direction: row; }} .box {{ flex: 1; }} }}
            </style>
        </head>
        <body>
            <h1>Raw Data Viewer</h1>
            <div class="container">
                <div class="box">
                    <h2>cards.json</h2>
                    <textarea readonly>{cards_data}</textarea>
                </div>
                <div class="box">
                    <h2>relationships.json</h2>
                    <textarea readonly>{relationships_data}</textarea>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open('raw_data.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Generated raw_data.html")
    except Exception as e:
        print(f"Failed to generate raw_data.html: {e}")

print(f"Starting Card Nexus Server...")
generate_raw_view() # Generate on startup
print(f"Open your browser to: http://localhost:{PORT}/card_manager.html")
print("Press Ctrl+C to stop.")

with socketserver.TCPServer(("", PORT), CardHandler) as httpd:
    httpd.serve_forever()
