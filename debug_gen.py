import html
import os
import json

def generate_raw_view_test():
    print("Testing generation...")
    try:
        try:
            with open('cards.json', 'r', encoding='utf-8') as f:
                cards_data = html.escape(f.read())
            print(f"Read cards.json ({len(cards_data)} bytes)")
        except Exception as e:
            cards_data = f"Error reading cards.json: {e}"
            print(cards_data)

        try:
            with open('relationships.json', 'r', encoding='utf-8') as f:
                relationships_data = html.escape(f.read())
            print(f"Read relationships.json ({len(relationships_data)} bytes)")
        except Exception as e:
            relationships_data = f"Error reading relationships.json: {e}"
            print(relationships_data)

        # Simplified f-string approach (no .format())
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
        
        output_path = 'raw_data.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully generated {output_path}")
        
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_raw_view_test()
