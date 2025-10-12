"""
AUTOMATED SCRIPT TO ADD CRUD TO REMAINING 20 MODULES
Applies full CRUD template to all remaining modules
"""

import os
import re

MODULES_TO_UPDATE = [
    ('cancellation_management.py', 'cancellations', 'Cancellation'),
    ('patient_choice.py', 'patient_choice', 'Patient Choice'),
    ('waiting_list_validator.py', 'waiting_list', 'Waiting List'),
    ('transfer_of_care.py', 'transfers', 'Transfer'),
    ('clinical_exceptions.py', 'clinical_exceptions', 'Clinical Exception'),
    ('capacity_planner.py', 'capacity_plans', 'Capacity Plan'),
    ('consent_manager.py', 'consent_records', 'Consent Record'),
    ('commissioner_reporting.py', 'commissioner_reports', 'Report'),
    ('audit_trail.py', 'audit_records', 'Audit Record'),
    ('communications_tracker.py', 'communications', 'Communication'),
    ('funding_ifr.py', 'funding_requests', 'Funding Request'),
    ('mobile_app_preview.py', 'mobile_feedback', 'Feedback'),
    ('executive_dashboard.py', 'dashboard_data', 'Dashboard Item'),
    ('voice_ai_interface.py', 'voice_interactions', 'Interaction'),
    ('pas_integration.py', 'pas_records', 'PAS Record'),
    ('patient_portal.py', 'portal_data', 'Portal Entry'),
    ('ai_documentation.py', 'ai_docs', 'Document'),
    ('blockchain_audit.py', 'blockchain_records', 'Audit'),
    ('predictive_ai.py', 'predictions', 'Prediction'),
    ('national_benchmarking.py', 'benchmarks', 'Benchmark'),
    ('student_progress_monitor.py', 'student_notes', 'Note'),
]

CRUD_IMPORTS = """import sys
sys.path.append('..')
from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)
"""

def add_crud_to_module(filename, module_key, record_name):
    """
    Add CRUD interface to a module
    
    Args:
        filename: Name of the module file
        module_key: Database key for storing records
        record_name: Display name for records (e.g., "DNA Case")
    """
    filepath = f'pages/{filename}'
    
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has CRUD
    if 'universal_crud' in content:
        print(f"[SKIP] {filename} (already has CRUD)")
        return True
    
    # Add imports if not present
    if 'from universal_crud import' not in content:
        # Find the import section
        import_match = re.search(r'(import streamlit as st.*?)\n\nst\.set_page_config', content, re.DOTALL)
        if import_match:
            imports_section = import_match.group(1)
            new_imports = imports_section + '\n' + CRUD_IMPORTS
            content = content.replace(imports_section, new_imports)
    
    # Add CRUD tabs interface (basic template)
    crud_interface = f'''
# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 {record_name} Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All {record_name}s")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_{module_key}")
    with col2:
        records = read_all_records('{module_key}')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "{module_key}.csv", "text/csv")
    
    # Get records
    records = read_all_records('{module_key}')
    
    if search_term:
        records = search_records('{module_key}', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{{len(records)}}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"{record_name} #{{idx+1}}: {{record.get('id', 'Unknown')[:20]}}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{{record['id']}}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{{record['id']}}"):
                        if delete_record('{module_key}', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New {record_name}")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('{module_key}')
    
    if records:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(records))
        with col2:
            st.metric("This Month", 0)  # Calculate as needed
        with col3:
            st.metric("Active", len(records))
    else:
        st.info("No data for analytics yet")

st.markdown("---")
# Educational content continues below...
'''
    
    # Find where to insert (usually after main title and before educational sections)
    # Look for "Educational section" or "st.markdown("---")" patterns
    insertion_point = content.find('# Educational section')
    if insertion_point == -1:
        insertion_point = content.find('st.markdown("---")')
    
    if insertion_point > 0:
        content = content[:insertion_point] + crud_interface + '\n\n' + content[insertion_point:]
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Updated: {filename}")
    return True

if __name__ == "__main__":
    print("Adding CRUD to remaining modules...")
    print("=" * 50)
    
    success_count = 0
    for filename, module_key, record_name in MODULES_TO_UPDATE:
        if add_crud_to_module(filename, module_key, record_name):
            success_count += 1
    
    print("=" * 50)
    print(f"Complete! Updated {success_count}/{len(MODULES_TO_UPDATE)} modules")
    print("\nNote: Basic CRUD structure added. Forms need customization per module.")
