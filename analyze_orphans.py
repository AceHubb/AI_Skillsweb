
import json
import re
from collections import defaultdict

CARDS_FILE = r'c:\PythonApplications\AI_Skillsweb\cards.json'
RELS_FILE = r'c:\PythonApplications\AI_Skillsweb\relationships.json'
REPORT_FILE = r'c:\PythonApplications\AI_Skillsweb\orphan_insight_report.txt'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze():
    print("Loading data...")
    cards_data = load_json(CARDS_FILE)
    rels_data = load_json(RELS_FILE)

    cards = cards_data.get('cards', cards_data)
    rels = rels_data.get('relationships', rels_data)

    card_map = {c['id']: c for c in cards}
    
    # identify parents
    has_parent = set()
    for r in rels:
        if r.get('type') == 'contains':
            tgt = r.get('target') or r.get('to')
            has_parent.add(tgt)

    # identify orphans
    orphans = []
    for cid, card in card_map.items():
        if cid not in has_parent:
            # Filter out some known roots if needed, but for now list all
            orphans.append(card)

    print(f"Found {len(orphans)} orphans.")

    # categorize
    categories = defaultdict(list)
    
    keywords = {
        'Cloud (AWS)': ['aws', 'amazon', 'cloud', 'ec2', 's3', 'lambda'],
        'Cloud (Google)': ['google', 'gcp', 'firebase', 'compute engine'],
        'Cloud (Azure)': ['azure', 'microsoft cloud', 'entra'],
        'Data & Analytics': ['data', 'analytics', 'sql', 'etl', 'dashboard', 'report', 'kpi', 'analysis'],
        'Management & Strategy': ['management', 'strategy', 'leadership', 'cost', 'planning', 'governance', 'compliance', 'process'],
        'Media & Visuals': ['media', 'diagram', 'chart', 'visual', 'screenshot', 'video'],
        'Development & Code': ['python', 'c#', 'java', 'code', 'programming', 'git', 'dev', 'api', 'sdk'],
        'Security': ['security', 'cyber', 'auth', 'identity', 'access', 'firewall'],
        'Healthcare': ['healthcare', 'nhs', 'medical', 'patient'],
        'Finance': ['finance', 'payment', 'banking', 'money', 'trading'],
        'Books': ['book', 'guide', 'reference', 'edition', 'author', 'reading'],
    }

    for card in orphans:
        matched = False
        text = (card.get('title', '') + ' ' + card.get('description', '') + ' ' + card.get('id', '')).lower()
        
        # Check specific types first
        if card.get('type') == 'media':
            categories['Media & Visuals'].append(card)
            continue

        for cat, keys in keywords.items():
            if any(k in text for k in keys):
                categories[cat].append(card)
                matched = True
                break # Assign to first matching category for simplicity
        
        if not matched:
            categories['Uncategorized'].append(card)

    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("ORPHAN CARD ANALYSIS REPORT\n")
        f.write("===========================\n")
        f.write(f"Total Orphans Found: {len(orphans)}\n\n")
        
        f.write("INSIGHTS & RECOMMENDATIONS\n")
        f.write("--------------------------\n")
        f.write("- **Cloud Catalog**: A large number of orphans are specific cloud services. Recommendation: Consolidate under '010_stack_cloud_hosting'.\n")
        f.write("- **Visual Portfolio**: Many orphans are media/diagrams. Recommendation: Link these to their specific subject matter cards rather than a generic 'Media' stack.\n")
        f.write("- **Management & Strategy**: There are high-level strategy cards that could form a new 'Executive' trail.\n\n")

        for cat, cards in categories.items():
            if not cards: continue
            f.write(f"\nCluster: {cat} ({len(cards)} items)\n")
            f.write("-" * (len(cat) + 12) + "\n")
            for c in cards:
                title = c.get('title', 'No Title')
                cid = c.get('id')
                desc = c.get('description', '')
                f.write(f"  * [{c.get('type','?')}] {title} ({cid})\n")
                if desc:
                    f.write(f"    - {desc[:100]}...\n")
    
    print(f"Report written to {REPORT_FILE}")

if __name__ == "__main__":
    analyze()
