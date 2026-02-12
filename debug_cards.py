import json

try:
    with open('cards.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cards = data.get('cards', [])
    target = next((c for c in cards if c['id'] == '001_stack_development_leadership'), None)
    
    if target:
        print("FOUND CARD:")
        print(json.dumps(target, indent=2))
    else:
        print("Card 001_stack_development_leadership NOT FOUND.")
        print("Stack cards found:")
        for c in cards:
            if c.get('type') == 'stack':
                print(f"- {c.get('id')}: {c.get('title')}")

except Exception as e:
    print(f"Error: {e}")
