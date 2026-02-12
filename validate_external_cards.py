
import json
import os
from collections import Counter

cards_path = r'c:\PythonApplications\ai_skillsweb\cards.json'

print(f"Validating {cards_path}...")

try:
    with open(cards_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    data = json.loads(content)
    print("JSON Syntax: OK")
    
    if 'cards' not in data:
        print("Error: Root key 'cards' missing.")
    else:
        cards = data['cards']
        print(f"Card count: {len(cards)}")
        
        ids = [str(c.get('id', 'MISSING_ID')) for c in cards]
        
        # Check for duplicates
        counts = Counter(ids)
        dups = [id for id, count in counts.items() if count > 1]
        
        if dups:
            print(f"ERROR: Duplicate IDs found: {dups}")
        else:
            print("No duplicate IDs found.")
            
        # Check for missing titles or types
        for i, c in enumerate(cards):
            if 'id' not in c:
                print(f"Card at index {i} missing 'id'")
            if 'title' not in c:
                print(f"Card {c.get('id')} missing 'title'")
            if 'type' not in c:
                print(f"Card {c.get('id')} missing 'type'")

except json.JSONDecodeError as e:
    print(f"JSON Syntax Error: {e}")
    # Print context
    lines = content.splitlines()
    if e.lineno <= len(lines):
        print(f"Line {e.lineno}: {lines[e.lineno-1]}")
except Exception as e:
    print(f"Error: {e}")
