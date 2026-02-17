
import json
import re

try:
    with open('c:/PythonApplications/AI_Skillsweb/cards.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cards = data.get('cards', [])
    updated = False
    
    for card in cards:
        media = card.get('media', [])
        new_media = []
        if isinstance(media, list):
            for m in media:
                # Split comma separated if any (legacy check)
                parts = [s.strip() for s in m.split(',')]
                cleaned_parts = []
                for p in parts:
                    # Remove pdf/ or images/ prefix (case insensitive, forward or backslash)
                    clean = re.sub(r'^(pdf|images)[\\/]', '', p, flags=re.IGNORECASE)
                    cleaned_parts.append(clean)
                
                # Check if any change occurred
                joined = ', '.join(cleaned_parts)
                if joined != m:
                    updated = True
                new_media.append(joined)
            
            card['media'] = new_media
        elif isinstance(media, str):
            # Handle string case just in case
            parts = [s.strip() for s in media.split(',')]
            cleaned_parts = []
            for p in parts:
                clean = re.sub(r'^(pdf|images)[\\/]', '', p, flags=re.IGNORECASE)
                cleaned_parts.append(clean)
            
            joined = ', '.join(cleaned_parts)
            if joined != media:
                updated = True
            card['media'] = [joined] # Convert to list? Or keep as string? better stick to list per schema.

    if updated:
        with open('c:/PythonApplications/AI_Skillsweb/cards.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Successfully cleaned media paths in cards.json")
    else:
        print("No changes needed.")

except Exception as e:
    print(f"Error: {e}")
