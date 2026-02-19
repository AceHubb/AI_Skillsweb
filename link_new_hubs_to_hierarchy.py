
import json

RELS_FILE = r'c:\PythonApplications\AI_Skillsweb\relationships.json'
REPORT_FILE = r'c:\PythonApplications\AI_Skillsweb\tree_view_report.txt'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    print("Loading relationships...")
    rels_data = load_json(RELS_FILE)
    rels_list = rels_data.get('relationships', rels_data)

    parent_id = "006_stack_legacy_modernisation"
    children = [
        "013_stack_executive_management",
        "014_stack_industry_verticals",
        "015_stack_visual_portfolio"
    ]

    existing_pairs = set()
    for r in rels_list:
        if r.get('type') == 'contains':
            src = r.get('source') or r.get('from')
            tgt = r.get('target') or r.get('to')
            existing_pairs.add((src, tgt))

    added_count = 0
    for child in children:
        if (parent_id, child) not in existing_pairs:
            rels_list.append({
                "source": parent_id,
                "target": child,
                "type": "contains",
                "value": 1
            })
            print(f"Linking {parent_id} -> {child}")
            added_count += 1
        else:
            print(f"Link {parent_id} -> {child} already exists.")

    if added_count > 0:
        if isinstance(rels_data, dict):
             rels_data['relationships'] = rels_list
        else:
             rels_data = rels_list
        save_json(RELS_FILE, rels_data)
        print(f"Saved {added_count} new relationships to {RELS_FILE}")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    main()
