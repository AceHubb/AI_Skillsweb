
import json

try:
    with open('c:/PythonApplications/AI_Skillsweb/cards.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        cards = data.get('cards', [])
        found = False
        for card in cards:
            if '10072' in str(card.get('id', '')):
                print(f"Found card by ID 10072: {json.dumps(card, indent=2)}")
                found = True
            
            video = card.get('video', '')
            if 'Waal' in video:
                print(f"Found card by video path content 'Waal': {json.dumps(card, indent=2)}")
                found = True

        if not found:
            print("Card not found.")

except Exception as e:
    print(f"Error: {e}")
