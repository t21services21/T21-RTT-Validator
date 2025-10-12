"""
Quick script to add back buttons to all new module pages
"""

import os

files_to_fix = [
    'dna_management.py',
    'cancellation_management.py', 
    'patient_choice.py',
    'waiting_list_validator.py',
    'transfer_of_care.py',
    'capacity_planner.py',
    'commissioner_reporting.py',
    'audit_trail.py',
    'communications_tracker.py',
    'consent_manager.py',
    'funding_ifr.py',
    'mobile_app_preview.py',
    'executive_dashboard.py',
    'voice_ai_interface.py',
    'pas_integration.py',
    'patient_portal.py',
    'ai_documentation.py',
    'blockchain_audit.py',
    'predictive_ai.py',
    'national_benchmarking.py',
    'student_progress_monitor.py'
]

back_button_code = """
# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
"""

fixed_count = 0
for filename in files_to_fix:
    filepath = f'pages/{filename}'
    if os.path.exists(filepath):
        # Check if already has back button
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'Back to Platform Dashboard' not in content:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(back_button_code)
            print(f"[OK] Fixed: {filename}")
            fixed_count += 1
        else:
            print(f"[SKIP] Already has button: {filename}")
    else:
        print(f"[NOT FOUND]: {filename}")

print(f"\nDone! Fixed {fixed_count} files")
