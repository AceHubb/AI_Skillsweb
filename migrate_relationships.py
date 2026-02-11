import json
import os

files = [
    r"c:\PythonApplications\Aardvarkscratch\relationships.json",
    r"c:\PythonApplications\AI_Skillsweb\relationships.json"
]

def migrate_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if 'relationships' not in data:
            print(f"No 'relationships' key in {filepath}")
            return

        modified = False
        for rel in data['relationships']:
            if 'strength' not in rel:
                rel['strength'] = "1"
                modified = True
        
        if modified:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Updated {filepath}")
        else:
            print(f"No changes needed for {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

for f in files:
    migrate_file(f)
