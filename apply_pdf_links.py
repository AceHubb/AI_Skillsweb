import json
import os

cards_path = 'c:/PythonApplications/AI_Skillsweb/cards.json'
mapping_path = 'c:/PythonApplications/AI_Skillsweb/pdf_mapping.json'

try:
    with open(cards_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)
    
    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    cards = cards_data.get('cards', cards_data)
    
    count = 0
    for pdf_name, card_id in mapping.items():
        # Find card
        card = next((c for c in cards if c['id'] == card_id), None)
        if card:
            # Add or update media field
            # If media exists, append if not present. If not, create list.
            if 'media' not in card:
                card['media'] = []
            
            pdf_path = f"pdf/{pdf_name}"
            if pdf_path not in card['media']:
                card['media'].append(pdf_path)
                count += 1
                print(f"Linked {pdf_name} -> {card['title']} ({card_id})")

    if count > 0:
        with open(cards_path, 'w', encoding='utf-8') as f:
            json.dump(cards_data, f, indent=2)
        print(f"Successfully updated {count} cards with PDFs.")
    else:
        print("No updates needed.")

except Exception as e:
    print(f"Error: {e}")
