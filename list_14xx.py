import json

cards_path = 'c:/PythonApplications/AI_Skillsweb/cards.json'

try:
    with open(cards_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)

    cards = cards_data.get('cards', cards_data)
    
    print(f"{'ID':<35} | {'Title'}")
    print("-" * 80)

    count = 0
    for card in cards:
        cid = card.get('id', '')
        if cid.startswith('14'):
            print(f"{cid:<35} | {card.get('title', 'NO TITLE')}")
            count += 1
            
    print(f"\nTotal 14xx Cards: {count}")

except Exception as e:
    print(f"Error: {e}")
