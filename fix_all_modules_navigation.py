"""
Fix navigation in all new modules - replace render_navigation with sidebar_manager
"""

import os
import re

# List of all modules to fix
modules = [
    "dna_management.py",
    "cancellation_management.py",
    "patient_choice.py",
    "waiting_list_validator.py",
    "transfer_of_care.py",
    "clinical_exceptions.py",
    "capacity_planner.py",
    "consent_manager.py",
    "commissioner_reporting.py",
    "audit_trail.py",
    "communications_tracker.py",
    "funding_ifr.py",
    "mobile_app_preview.py",
    "executive_dashboard.py",
    "voice_ai_interface.py",
    "pas_integration.py",
    "patient_portal.py",
    "ai_documentation.py",
    "blockchain_audit.py",
    "predictive_ai.py",
    "national_benchmarking.py",
    "student_progress_monitor.py"
]

pages_dir = "pages"

for module in modules:
    filepath = os.path.join(pages_dir, module)
    
    if not os.path.exists(filepath):
        print(f"[SKIP] Not found: {module}")
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the import
        content = content.replace(
            "from navigation import render_navigation",
            "from sidebar_manager import render_sidebar"
        )
        
        # Replace the CSS that hides sidebar
        old_css = """st.markdown(\"\"\"
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
\"\"\", unsafe_allow_html=True)"""
        
        new_css = """st.markdown(\"\"\"
<style>
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 1rem !important;}
</style>
\"\"\", unsafe_allow_html=True)"""
        
        content = content.replace(old_css, new_css)
        
        # Replace render_navigation call with render_sidebar
        content = re.sub(
            r'render_navigation\(current_page="[^"]*"\)',
            'render_sidebar()',
            content
        )
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Fixed: {module}")
    
    except Exception as e:
        print(f"[ERROR] Error fixing {module}: {e}")

print("\n[SUCCESS] All modules updated!")
print("Now users can access all modules from the sidebar!")
