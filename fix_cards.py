
import json

try:
    with open('c:/PythonApplications/AI_Skillsweb/cards.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cards = data.get('cards', [])
    updated = False
    
    for card in cards:
        # Fix 10071 Web URL
        web = card.get('web', '')
        if web.startswith('\\web\\'):
            print(f"Fixing web URL for card {card.get('id')}: {web}")
            card['web'] = web.replace('\\web\\', '')
            updated = True
        
        # Fix 10072 Video Path (and others)
        video = card.get('video', '')
        if video.startswith('\\videos\\'):
            # Ensure it is just 'videos/' or keep it if it works with backslashes but maybe without leading slash?
            # Browser usually needs forward slashes for URLs/src
            print(f"Fixing video path for card {card.get('id')}: {video}")
            card['video'] = video.replace('\\', '/')
            if card['video'].startswith('/'):
                 card['video'] = card['video'][1:] # Remove leading slash if it makes it absolute to root instead of relative
            updated = True

    if updated:
        with open('c:/PythonApplications/AI_Skillsweb/cards.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Successfully updated cards.json")
    else:
        print("No changes needed.")

except Exception as e:
    print(f"Error: {e}")
