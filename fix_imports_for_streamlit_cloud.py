"""
Fix import paths for Streamlit Cloud deployment
The sys.path.append('..') doesn't work on Streamlit Cloud
"""

import os
import re

MODULES = [
    'dna_management.py',
    'cancellation_management.py',
    'patient_choice.py',
    'waiting_list_validator.py',
    'transfer_of_care.py',
    'clinical_exceptions.py',
    'capacity_planner.py',
    'consent_manager.py',
    'commissioner_reporting.py',
    'audit_trail.py',
    'communications_tracker.py',
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
    'student_progress_monitor.py',
]

BAD_IMPORT = """import sys
sys.path.append('..')
from universal_crud import"""

GOOD_IMPORT = """import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from universal_crud import"""

def fix_module(filename):
    filepath = f'pages/{filename}'
    
    if not os.path.exists(filepath):
        print(f"[SKIP] {filename} - not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'sys.path.append' not in content:
        print(f"[SKIP] {filename} - no bad import")
        return False
    
    # Replace the bad import
    content = content.replace(BAD_IMPORT, GOOD_IMPORT)
    
    # Also ensure 'os' is imported at top
    if 'import os' not in content and 'from universal_crud import' in content:
        # Add os import if missing
        content = content.replace('import sys', 'import os\nimport sys', 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Fixed: {filename}")
    return True

if __name__ == "__main__":
    print("Fixing import paths for Streamlit Cloud...")
    print("=" * 50)
    
    fixed_count = 0
    for filename in MODULES:
        if fix_module(filename):
            fixed_count += 1
    
    print("=" * 50)
    print(f"Complete! Fixed {fixed_count}/{len(MODULES)} modules")
