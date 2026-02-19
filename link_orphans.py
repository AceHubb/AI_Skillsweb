
import json
import os

# Helper to load/save JSON
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

CARDS_FILE = r'c:\PythonApplications\AI_Skillsweb\cards.json'
RELS_FILE = r'c:\PythonApplications\AI_Skillsweb\relationships.json'
REPORT_FILE = r'c:\PythonApplications\AI_Skillsweb\tree_view_report.txt'

# Load Data
cards_data = load_json(CARDS_FILE)
rels_data = load_json(RELS_FILE)

cards_list = cards_data.get('cards', cards_data)
rels_list = rels_data.get('relationships', rels_data)

# Map IDs for quick lookup
card_map = {c['id']: c for c in cards_list}

# Track existing relationships to avoid duplicates
existing_relationships = set()
for r in rels_list:
    src = r.get('source') or r.get('from')
    tgt = r.get('target') or r.get('to')
    rtype = r.get('type')
    if src and tgt and rtype == 'contains':
        existing_relationships.add((src, tgt))

new_rels = []

def add_rel(parent_id, child_id):
    if (parent_id, child_id) not in existing_relationships:
        new_rels.append({
            "source": parent_id,
            "target": child_id,
            "type": "contains",
            "value": 1
        })
        existing_relationships.add((parent_id, child_id))
        print(f"Linking {child_id} -> {parent_id}")

# --- MAPPING LOGIC ---

# 1. Cloud & Hosting (AWS, GCP, Azure) -> 010_stack_cloud_hosting
# We'll create intermediate 'stack' cards if they don't logically exist, 
# but for now let's map to the best existing fit.
# Looking at tree report: 010_stack_cloud_hosting exists. 
# Also 1000_aws, 1002_monitoring_scaling (Google), 10046_microsoft_azure are likely 'Heads' for these.

# Let's see if 1000_aws exists and is a good parent for aws items.
# Or if we should link 1000_aws TO 010_stack_cloud_hosting first.

if '1000_aws' in card_map:
    add_rel('010_stack_cloud_hosting', '1000_aws')
    
    # Link all AWS orphans to 1000_aws
    aws_orphans = [
        '10023_aws_compute_the_engine', '10024_aws_storage_the_memory', 
        '10025_aws_ai_machine_learning_the_intelligence', '10026_aws_databases_the_ledger',
        '10027_aws_networking_the_nervous_system', '10028_aws_key_services_vpc_isolated_network',
        '10029_aws_security_identity_the_guardrails', '10030_aws_analytics_the_insights',
        '10031_aws_application_integration_the_glue', '10032_aws_key_services_sqs_queues',
        '10033_aws_management_governance_the_oversight', '10034_aws_developer_tools_the_workbench',
        '1471_aws_amaxon_web_services', '1472_aws_career_paths', '1473_aws_newworking', 
        '1474_begining_aws'
    ]
    for oid in aws_orphans:
        if oid in card_map:
            add_rel('1000_aws', oid)

# Google Cloud Orphans
if '1002_monitoring_scaling' in card_map: # This seems to be the Google Cloud generic card based on report
    # Rename title maybe? But let's just link for now.
    add_rel('010_stack_cloud_hosting', '1002_monitoring_scaling')
    
    gcp_orphans = [
        '10047_google_cloud_compute_the_engine', '10048_google_cloud_storage_the_memory',
        '10049_google_cloud_ai_machine_learning_the_intelligence', '10050_google_cloud_data_analytics_the_brain',
        '10051_google_cloud_databases_the_ledger', '10052_google_cloud_networking_the_nervous_system',
        '10053_google_cloud_security_identity_the_guardrails', '10054_google_cloud_management_operations_the_oversight',
        '10055_google_cloud_application_integration_the_glue', '10056_google_cloud_developer_tools_firebase_the_workbench'
    ]
    for oid in gcp_orphans:
        if oid in card_map:
            add_rel('1002_monitoring_scaling', oid)

# Azure Orphans
if '10046_microsoft_azure' in card_map:
    add_rel('010_stack_cloud_hosting', '10046_microsoft_azure')
    # Azure specific orphans seem less prevalent in the orphan list but generic ones might map here.
    # Lines 52-60 seem to be Generic Cloud Capabilities (Compute, Storage...) - 10036 to 10045.
    # These might be Azure or General. Let's map them to 010_stack_cloud_hosting directly for now 
    # OR create a "Cloud Fundamentals" card. 
    # Use 010_stack_cloud_hosting directly for these generics.
    
    cloud_generics = [
        '10036_compute_the_engine', '10037_storage_the_memory', '10039_databases_the_ledger',
        '10040_networking_the_nervous_system', '10041_identity_security_the_guardrails',
        '10042_analytics_the_insights', '10043_integration_the_glue', '10044_management_governance_the_oversight',
        '10045_developer_tools_the_workbench'
    ]
    for oid in cloud_generics:
        if oid in card_map:
            add_rel('010_stack_cloud_hosting', oid)

# 2. Analytics & Reporting -> 004_stack_analytics_reporting
# Parent: 1265_analytics (Generic Analytics) seemed like a good sub-parent.
if '1265_analytics' in card_map:
    analytics_orphans_generic = [
        '1271_descriptive_analytics', '1272_diagnostic_analytics', '1273_predictive_analytics', '1274_prescriptive_analytics',
        '1275_exploratory_data_analysis_eda', '1276_statistical_analysis', '1277_trend_time_series_analysis',
        '1278_segmentation_cohort_analysis', '1279_forecasting', '1280_anomaly_detection',
        '1302_customer_segmentation_behaviour_analysis', '1303_predictive_analytics_forecasting',
        '1304_anomaly_detection_fraud_analytics', '1305_trend_analysis_market_insights',
        '1306_performance_optimization_operational_analytics' # from Business Analysis stack maybe? but fits here too
    ]
    for oid in analytics_orphans_generic:
        if oid in card_map:
            add_rel('1265_analytics', oid)

# Analytics Dashboard/KPIs
if '1269_dashboard_architecture' in card_map:
    dashboard_orphans = [
        '1294_dashboard_architecture', '1296_dashboard_requirements_audience', '1297_information_hierarchy_layout',
        '1298_visualization_selection_best_practices', '1299_interactivity_drill_downs', '1300_dashboard_performance_maintenance',
        '1307_layout_visual_design', '1308_navigation_interactivity', '1309_user_experience_ux'
    ]
    for oid in dashboard_orphans:
         if oid in card_map:
            add_rel('1269_dashboard_architecture', oid)

if '1267_kpi_metrics_design' in card_map:
     kpi_orphans = [
        '1282_kpi_identification', '1283_metric_definition_calculation', '1284_leading_vs_lagging_indicators',
        '1287_kpi_governance_quality'
     ]
     for oid in kpi_orphans:
         if oid in card_map:
            add_rel('1267_kpi_metrics_design', oid)

# 3. Governance & Compliance -> 011_stack_governance_compliance
# Sub-parents: 0111_governance and 0112_compliance exist.

if '0112_compliance' in card_map:
    compliance_orphans = [
        '1100_gdpr', '1102_policy_compliance', '1206_gdpr_eu_uk_gdpr', '1207_uk_data_protection_act_2018',
        '1208_eprivacy_directive_pecr', '1209_ccpa_cpra', '1210_pipeda', '1211_lgpd',
        '1213_iso_27001', '1214_iso_27701', '1215_soc_2', '1216_nist_cybersecurity_framework',
        '1217_cyber_essentials_cyber_essentials_plus', '1221_pci_dss', '1222_sox', '1223_basel_iii', '1224_hipaa',
        '1225_gxp_gamp5', '1226_fda_21_cfr_part_11', '1227_iso_9001', '1228_iso_22301', '1261_gdpr_compliance'
    ]
    for oid in compliance_orphans:
        if oid in card_map:
            add_rel('0112_compliance', oid)

if '0111_governance' in card_map:
    governance_orphans = [
        '1229_coso', '1231_corporate_organizational_governance', '1233_it_governance', '1234_information_governance_nhs_healthcare',
        '1236_corporate_governance_codes', '1237_oecd_corporate_governance_principles', '1238_board_oversight_audit_committees_risk_committees_etc',
        '1239_data_ownership_stewardship', '1240_data_quality_management', '1241_data_classification', '1242_retention_deletion_policies',
        '1244_metadata_management', '1245_common_frameworks', '1246_dama_dmbok', '1247_dcam', '1248_enterprise_data_governance_frameworks',
        '1249_cobit', '1250_itil', '1251_iso_38500', '1252_combines', '1253_often_includes',
        '1254_data_protection', '1255_records_management', '1256_information_security', '1257_data_sharing_controls',
        '1258_records_retention', '1259_secure_disposal', '1260_information_lifecycle_management',
        '1262_iso_31000', '1263_coso', '1264_three_lines_model', '1270_something_specific_from_our_experience'
    ]
    for oid in governance_orphans:
        if oid in card_map:
            add_rel('0111_governance', oid)

# 4. Books and Articles -> 1453_books_and_articles or The Trunk/Fruit
BOOKS_PARENT = '1453_books_and_articles'
if BOOKS_PARENT in card_map:
    book_orphans = [
        '1446_cialdini_influence', '1447_toyota_way', '1448_six_sigma_way', '1441_antifragile',
        '1443_blaise_intelligence', '1445_keller_one_thing', '1449_the_black_swan',
        '1451_thinking_fast_and_slow', '1452_algorithms_to_live_by',
        '1468_python', '1469_python_crash_course', '1470_python_programming',
        '1432_jesse_liberty_csharp', '1434_qlikview_business', '1435_tableau_data', '1436_power_bi_transform',
        '1428_feuerstein_plsql', '1429_oracle_reference'
    ]
    for oid in book_orphans:
        if oid in card_map:
            add_rel(BOOKS_PARENT, oid)

# 5. Media - Visual Portfolio -> Create new stack if needed, or link to "Project Management Reporting"
# Currently orphans. Let's link them to '102_pm_reporting' as a placeholder or '004_stack_analytics_reporting'
# A robust way is to create a new Stack: "Visual Examples & Media"
# But user asked to fit into *existing* structure.
# Many are "Diagrams", so '103_tech_authorship' (Technical Authorship) could be a home?
# Or '004_stack_analytics_reporting' for the dashboards.

# Let's map Dashboards to '1269_dashboard_architecture' sibling '1301_advanced_applied_analytics' (Showcase)
# It has description: "A showcase practical, high-value analytics work..."
if '1301_advanced_applied_analytics' in card_map:
    media_dashboard_orphans = [
        '10003_media_pm_dashboard', '10010_media_kpi_dashboard', '10013_media_crypto_dashboard',
        '10001_media_gantt_chart', '10011_media_control_chart', '10021_media_control_charts'
    ]
    for oid in media_dashboard_orphans:
        if oid in card_map:
             add_rel('1301_advanced_applied_analytics', oid)

# Map Diagrams to '103_tech_authorship' or '1201_doc_maintenance'
if '103_tech_authorship' in card_map:
    diagram_orphans = [
        '10002_media_architecture_diagram', '10004_media_er_diagram', '10005_media_star_schema',
        '10006_media_plsql_pipeline', '10007_media_tsql_pipeline', '10008_media_pipeline_diagram',
        '10009_media_dataset_flow', '10012_media_process_diagram', '10014_media_before_after_architecture',
        '10015_media_gui_screenshot', '10016_media_ci_cd_pipeline', '10017_media_ai_workflow',
        '10018_media_transaction_workflow', '10019_media_cloud_architecture', '10020_media_anonymized_flow',
        '10022_media_methodology_visuals'
    ]
    for oid in diagram_orphans:
        if oid in card_map:
            add_rel('103_tech_authorship', oid)

# 6. Specific Tech/Capabilities
# SQL & Databases -> 002_stack_data_engineering
if '002_stack_data_engineering' in card_map:
    tech_orphans = [
        '1312_sql_databases', '203_plsql_dev', '204_tsql_dev', '1319_bash_shell' # Bash maybe closer to Linux?
    ]
    for oid in tech_orphans:
        if oid in card_map:
            add_rel('002_stack_data_engineering', oid)
            
# Linux -> 10064_linux (in Enterprise Guardian > Taproot)
if '10064_linux' in card_map:
     linux_orphans = [
         '10057_linux_operating_systems_linux_administration', '10062_linux_environment_deployment_support',
         '10063_linux_security_environments_optional', '1319_bash_shell'
     ]
     for oid in linux_orphans:
         if oid in card_map:
             add_rel('10064_linux', oid)

# Save Update
if new_rels:
    rels_list.extend(new_rels)
    
    # Update dict if wrapped
    if isinstance(rels_data, dict):
        rels_data['relationships'] = rels_list
    else:
        rels_data = rels_list
        
    save_json(RELS_FILE, rels_data)
    print(f"Successfully added {len(new_rels)} new relationships.")
else:
    print("No new relationships to add.")

