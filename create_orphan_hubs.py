
import json

CARDS_FILE = r'c:\PythonApplications\AI_Skillsweb\cards.json'
RELS_FILE = r'c:\PythonApplications\AI_Skillsweb\relationships.json'
CONFIG_FILE = r'c:\PythonApplications\AI_Skillsweb\pathfinder_config.json'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    print("Loading data...")
    cards_data = load_json(CARDS_FILE)
    rels_data = load_json(RELS_FILE)
    config_data = load_json(CONFIG_FILE)

    cards_list = cards_data.get('cards', cards_data)
    rels_list = rels_data.get('relationships', rels_data)

    existing_ids = {c['id'] for c in cards_list}

    # 1. Create New Parent Cards
    new_cards = [
        {
            "id": "013_stack_executive_management",
            "title": "Executive Management & Strategy",
            "type": "stack",
            "description": "High-level operational strategy, financial optimization, and stakeholder governance.",
            "frontBackgroundColor": "slategray"
        },
        {
            "id": "014_stack_industry_verticals",
            "title": "Industry Domain Expertise",
            "type": "stack",
            "description": "Specialized experience in Finance, Healthcare, Oil & Gas, and Engineering sectors.",
            "frontBackgroundColor": "darkgoldenrod"
        },
        {
            "id": "015_stack_visual_portfolio",
            "title": "Visual Portfolio & Media",
            "type": "stack",
            "description": "A collection of diagrams, dashboards, and video assets demonstrating real-world output.",
            "frontBackgroundColor": "darkcyan"
        }
    ]

    added_count = 0
    for nc in new_cards:
        if nc['id'] not in existing_ids:
            cards_list.append(nc)
            print(f"Created Card: {nc['title']}")
            added_count += 1
    
    # 2. Link Orphans
    new_rels = []
    
    # -- Executive Management --
    exec_children = [
        '1364_change_management_adoption', '1396_stakeholder_vendor_management',
        '1397_process_management', '1399_tender_management',
        '1360_financial_performance_optimization', '1465_engineering_project_support',
        '101_critical_path', '1398_document_management', '1462_procurement_planning'
    ]
    for child in exec_children:
        new_rels.append({"source": "013_stack_executive_management", "target": child, "type": "contains", "value": 1})

    # -- Industry Verticals --
    industry_children = [
        '1400_healthcare_systems_multiple', '1401_healthcare_commissioning_finance',
        '1404_online_payment_collection_backend', '1394_project_management_systems_oil_gas',
        '1402_banking_stp_trade_reconciliation'
    ]
    for child in industry_children:
        new_rels.append({"source": "014_stack_industry_verticals", "target": child, "type": "contains", "value": 1})

    # -- Visual Portfolio --
    visual_children = [
        '10071_video_interview', '10072_video_homemade',
        '10001_media_gantt_chart', '10002_media_architecture_diagram', '10003_media_pm_dashboard',
        '10004_media_er_diagram', '10005_media_star_schema', '10006_media_plsql_pipeline',
        '10007_media_tsql_pipeline', '10008_media_pipeline_diagram', '10009_media_dataset_flow',
        '10010_media_kpi_dashboard', '10011_media_control_chart', '10012_media_process_diagram',
        '10013_media_crypto_dashboard', '10014_media_before_after_architecture',
        '10015_media_gui_screenshot', '10016_media_ci_cd_pipeline', '10017_media_ai_workflow',
        '10018_media_transaction_workflow', '10019_media_cloud_architecture',
        '10020_media_anonymized_flow', '10021_media_control_charts', '10022_media_methodology_visuals'
    ]
    for child in visual_children:
        new_rels.append({"source": "015_stack_visual_portfolio", "target": child, "type": "contains", "value": 1})

    # Add to relationships
    # Check for existing to avoid duplicates
    existing_pairs = set()
    for r in rels_list:
        if r.get('type') == 'contains':
            existing_pairs.add((r.get('source') or r.get('from'), r.get('target') or r.get('to')))
            
    added_rels = 0
    for r in new_rels:
        if (r['source'], r['target']) not in existing_pairs:
             rels_list.append(r)
             added_rels += 1

    print(f"Added {added_rels} new relationships.")

    # 3. Update Pathfinder Config (Add to Trails)
    # Legacy Rescue -> 013, 014
    # Safe Innovation -> 015
    
    trails = config_data.get('trails', [])
    updated_config = False
    
    for trail in trails:
        tid = trail.get('id')
        seeds = trail.get('seeds', [])
        
        if tid == 'legacy_rescue':
            if '013_stack_executive_management' not in seeds:
                seeds.append('013_stack_executive_management')
                updated_config = True
            if '014_stack_industry_verticals' not in seeds:
                seeds.append('014_stack_industry_verticals')
                updated_config = True
        
        if tid == 'safe_innovation':
            if '015_stack_visual_portfolio' not in seeds:
                seeds.append('015_stack_visual_portfolio')
                updated_config = True
                
    if added_count > 0:
        if isinstance(cards_data, dict):
             cards_data['cards'] = cards_list
        else:
             cards_data = cards_list
        save_json(CARDS_FILE, cards_data)
        print("Updated cards.json")

    if added_rels > 0:
        if isinstance(rels_data, dict):
             rels_data['relationships'] = rels_list
        else:
             rels_data = rels_list
        save_json(RELS_FILE, rels_data)
        print("Updated relationships.json")

    if updated_config:
        save_json(CONFIG_FILE, config_data)
        print("Updated paths in pathfinder_config.json")

if __name__ == "__main__":
    main()
