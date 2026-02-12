import json

try:
    with open('cards.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cards = data.get('cards', [])
    target = next((c for c in cards if c['id'] == '001_stack_development_leadership'), None)
    
    if target:
        target['description'] = "Leading software development teams to deliver high-quality solutions. Focus on mentorship, code quality, and architectural integrity. Balancing technical debt with feature delivery and fostering a culture of continuous improvement."
        print("Updated description for 001_stack_development_leadership")
        
        with open('cards.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            print("Saved cards.json")
    else:
        print("Card 001_stack_development_leadership NOT FOUND.")

except Exception as e:
    print(f"Error: {e}")
