import json
import difflib
import os

cards_path = 'c:/PythonApplications/AI_Skillsweb/cards.json'
pdf_list = [
    "Advanced_Applied_Ana.pdf",
    "AI-Driven_Private_Do.pdf",
    "Artificial_Intellige.pdf",
    "Azure_Cloud_Infrastr.pdf",
    "Backend_Application_.pdf",
    "Computing_Foundation.pdf",
    "Cost_Control_in_High.pdf",
    "Dashboard_Architectu.pdf",
    "Database_Platform_De.pdf",
    "Database_Schema_Desi.pdf",
    "Data_Warehouse_and_D.pdf",
    "Delivery_Methodology.pdf",
    "Document_Maintenance.pdf",
    "GDPR_and_Data_Privac.pdf",
    "Google_Cloud_Securit.pdf",
    "GUI_Design_and_Rapid.pdf",
    "High-Volatility_Data.pdf",
    "Identity_Management_.pdf",
    "Infrastructure_as_a_.pdf",
    "Inventory_and_Operat.pdf",
    "KPI_and_Metrics_Desi.pdf",
    "Legacy_Codebase_Mode.pdf",
    "Microservices_Archit.pdf",
    "Microsoft_Security_E.pdf",
    "Operational_Reportin.pdf",
    "Orchestrating_Large-.pdf",
    "Planning_and_Schedul.pdf",
    "Platform_Security_Mo.pdf",
    "Policy,_Compliance,_.pdf",
    "Process_Improvement_.pdf",
    "Project_Management_R.pdf",
    "Requirements_Gatheri.pdf",
    "Software_Delivery_Me.pdf",
    "SQL_and_Relational_D.pdf",
    "Straight-Through_Pro.pdf",
    "Strategic_KPI_Defini.pdf",
    "Structural_Integrity.pdf",
    "System_Monitoring,_S.pdf",
    "Technical_Authorship.pdf",
    "Vector_Databases_AI.pdf"
]

try:
    with open(cards_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)

    cards = cards_data.get('cards', cards_data)
    
    # Filter for all cards that are NOT stacks or headings
    target_cards = [c for c in cards if 'stack' not in c.get('type', '') and 'heading' not in c.get('title', '').lower()]
    
    # Also include other potential matches if needed, but focus on 14xx first as requested
    # If 14xx doesn't match, we might look at others.
    
    matches = []
    
    print(f"{'PDF Filename':<35} | {'Match Score':<5} | {'Card Title'}")
    print("-" * 80)

    cached_matches = {}

    for pdf in pdf_list:
        # heuristic: clean pdf name
        clean_name = pdf.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        best_ratio = 0
        best_card = None
        
        for card in target_cards:
            title = card.get('title', '')
            # Simple fuzzy match
            ratio = difflib.SequenceMatcher(None, clean_name.lower(), title.lower()).ratio()
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_card = card
        
        if best_ratio > 0.4: # Threshold
            matches.append({
                "pdf": pdf,
                "card_id": best_card['id'],
                "card_title": best_card['title'],
                "score": best_ratio
            })
            print(f"{pdf:<35} | {best_ratio:.2f}  | {best_card['title']}")
            cached_matches[pdf] = best_card['id']
        else:
            print(f"{pdf:<35} | {best_ratio:.2f}  | ** NO GOOD MATCH **")

    # Save mapping for next step
    with open('c:/PythonApplications/AI_Skillsweb/pdf_mapping.json', 'w') as f:
        json.dump(cached_matches, f, indent=2)

except Exception as e:
    print(f"Error: {e}")
