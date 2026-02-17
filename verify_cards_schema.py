
import json
import os
import sys

cards_file = r'c:\PythonApplications\AI_Skillsweb\cards.json'

def verify_cards():
    if not os.path.exists(cards_file):
        print(f"Error: {cards_file} not found.")
        sys.exit(1)

    try:
        with open(cards_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'cards' not in data:
            print("Error: 'cards' key not found in JSON.")
            sys.exit(1)

        missing_fields = []
        for i, card in enumerate(data['cards']):
            card_id = card.get('id', f'Index {i}')
            if 'web' not in card:
                missing_fields.append(f"Card {card_id} missing 'web'")
            if 'video' not in card:
                missing_fields.append(f"Card {card_id} missing 'video'")
        
        if missing_fields:
            print(f"FAILED: Found {len(missing_fields)} issues.")
            for issue in missing_fields[:10]:
                print(issue)
            if len(missing_fields) > 10:
                print("...")
            sys.exit(1)
        else:
            print(f"SUCCESS: All {len(data['cards'])} cards have 'web' and 'video' fields.")
            sys.exit(0)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_cards()
