
import json
import os

cards_file = r'c:\PythonApplications\AI_Skillsweb\cards.json'

def update_cards():
    if not os.path.exists(cards_file):
        print(f"Error: {cards_file} not found.")
        return

    try:
        with open(cards_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'cards' not in data:
            print("Error: 'cards' key not found in JSON.")
            return

        modified_count = 0
        for card in data['cards']:
            if 'web' not in card:
                card['web'] = ""
                modified_count += 1
            if 'video' not in card:
                card['video'] = ""
                modified_count += 1
        
        with open(cards_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"Successfully updated {modified_count} fields in {len(data['cards'])} cards.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_cards()
