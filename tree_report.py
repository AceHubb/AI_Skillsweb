
import json
import os

# Define Paths
CARDS_FILE = r'c:\PythonApplications\AI_Skillsweb\cards.json'
RELS_FILE = r'c:\PythonApplications\AI_Skillsweb\relationships.json'
OUTPUT_FILE = r'c:\PythonApplications\AI_Skillsweb\tree_view_report.txt'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report():
    print(f"Loading data from {CARDS_FILE} and {RELS_FILE}...")
    
    try:
        cards_data = load_json(CARDS_FILE)
        rels_data = load_json(RELS_FILE)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    # Handle potentially wrapped JSON structure
    cards_list = cards_data.get('cards', cards_data) if isinstance(cards_data, dict) else cards_data
    rels_list = rels_data.get('relationships', rels_data) if isinstance(rels_data, dict) else rels_data

    # Map ID -> Card
    cards_map = {c['id']: c for c in cards_list}
    print(f"Loaded {len(cards_map)} cards from cards.json.")

    # Build Adjacency Map (Parent -> Children) and Parent Tracking
    adj = {}
    has_parent = set()
    all_involved_ids = set(cards_map.keys())

    for r in rels_list:
        if r.get('type') == 'contains':
            src = r.get('source') or r.get('from')
            tgt = r.get('target') or r.get('to')
            
            if src and tgt:
                all_involved_ids.add(src)
                all_involved_ids.add(tgt)
                
                if src not in adj:
                    adj[src] = []
                adj[src].append(tgt)
                has_parent.add(tgt)

    print(f"Total involved distinct IDs (Cards + Relationships): {len(all_involved_ids)}")

    # Identify Roots
    hierarchy_roots = []
    orphan_roots = []

    for cid in all_involved_ids:
        if cid not in has_parent:
            # Determine if it's a "Stack" root or regular "Orphan" root
            # Heuristics:
            # 1. Type is 'stack'
            # 2. ID contains 'stack'
            # 3. Has children (a root with children is essentially a stack/tree root)
            # 4. ID starts with known prefixes like '00'
            
            card = cards_map.get(cid)
            ctype = card.get('type', 'unknown').lower() if card else 'unknown'
            
            is_stack_like = False
            if ctype == 'stack':
                is_stack_like = True
            elif 'stack' in cid.lower():
                is_stack_like = True
            elif cid in adj and len(adj[cid]) > 0:
                # If it's a root and has children, treat it as a Hierarchy Root
                is_stack_like = True
            
            if is_stack_like:
                hierarchy_roots.append(cid)
            else:
                orphan_roots.append(cid)

    hierarchy_roots.sort()
    orphan_roots.sort()

    # Sort children for consistent output
    for pid in adj:
        adj[pid].sort()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("AI SKILLS WEB - TREE VIEW REPORT\n")
        f.write("================================\n\n")

        f.write(f"Total Unique IDs: {len(all_involved_ids)}\n")
        f.write(f"Cards found in JSON: {len(cards_map)}\n")
        f.write(f"Missing Cards (in rels only): {len(all_involved_ids) - len(cards_map)}\n")
        f.write(f"Hierarchy Roots: {len(hierarchy_roots)}\n")
        f.write(f"Orphan Roots (Cards with no parent and no children): {len(orphan_roots)}\n\n")

        def print_tree(node_id, prefix="", is_last=True):
            card = cards_map.get(node_id)
            if card:
                title = card.get('title', 'Unknown')
                ctype = card.get('type', '?')
                display_str = f"[{ctype}] {title} ({node_id})"
            else:
                display_str = f"[MISSING] {node_id}"
            
            connector = "└── " if is_last else "├── "
            f.write(f"{prefix}{connector}{display_str}\n")
            
            children = adj.get(node_id, [])
            count = len(children)
            
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            for i, child_id in enumerate(children):
                is_last_child = (i == count - 1)
                print_tree(child_id, new_prefix, is_last_child)

        f.write("HIERARCHY TREES (Roots with Children or declared Stacks)\n")
        f.write("------------------------------------------------------\n")
        if not hierarchy_roots:
            f.write("(None)\n")
        
        for root in hierarchy_roots:
            print_tree(root, "", True)
            f.write("\n")

        f.write("\nORPHANS (Isolated Cards)\n")
        f.write("------------------------\n")
        if not orphan_roots:
            f.write("(None)\n")

        for root in orphan_roots:
            print_tree(root, "", True)

    print(f"Report generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_report()
