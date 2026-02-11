
import json
import os
from collections import Counter

cards_path = r'c:\PythonApplications\Aardvarkscratch\cards.json'
rels_path = r'c:\PythonApplications\Aardvarkscratch\relationships.json'

print(f"Validating integrity between {cards_path} and {rels_path}...")

try:
    with open(cards_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)
    with open(rels_path, 'r', encoding='utf-8') as f:
        rels_data = json.load(f)

    cards = cards_data.get('cards', [])
    existing_ids = set(c['id'] for c in cards)
    
    rels = rels_data.get('relationships', [])
    print(f"Loaded {len(cards)} cards and {len(rels)} relationships.")
    
    missing_ids = set()
    for i, r in enumerate(rels):
        src = r.get('from')
        dst = r.get('to')
        
        if src not in existing_ids:
            missing_ids.add(src)
            # print(f"Rel {i}: Source '{src}' not found in cards.")
            
        if dst not in existing_ids:
            missing_ids.add(dst)
            # print(f"Rel {i}: Target '{dst}' not found in cards.")
            
    if missing_ids:
        print(f"ERROR: {len(missing_ids)} IDs referenced in relationships are missing from cards.json:")
        for mid in sorted(list(missing_ids)):
            print(f" - {mid}")
    else:
        print("Integrity Check: OK. All relationship endpoints exist.")

except Exception as e:
    print(f"Error: {e}")
