"""
APPLY HUGE SUCCESS MESSAGES TO ALL MODULES
This script updates all st.success() calls to use the new huge success component
"""

import os
import re

# List of files to update (from grep search)
files_to_update = [
    'ai_validator_ui.py',
    'medical_secretary_ui.py',
    'pages/dna_management.py',
    'advanced_booking_ui.py',
    'lms_course_manager.py',
    'lms_reviews_ui.py',
    'lms_system.py',
    'admin_ai_training.py',
    'admin_bulk_email.py',
    'admin_personal_message_ui.py',
    'clinic_letter_interpreter_INTERACTIVE.py',
    'clinic_letter_interpreter_pro.py',
    'document_management_ui.py',
    'episode_management_ui.py',
    'information_governance_ui.py',
    'job_automation_staff_setup.py',
    'pages/cancellation_management.py',
    'pages/communications_tracker.py',
    'pages/consent_manager.py',
    'pages/contact_us.py',
    'pages/dna_management_simple.py',
    'pages/transfer_of_care.py',
    'policy_sop_generator.py',
    'ptl_ui.py',
    'student_access_management.py',
    'student_portfolio_ui.py',
    'teacher_dashboard.py',
    'trust_customization_ui.py'
]

def add_import_if_missing(content):
    """Add import statement if not already present"""
    if 'from success_message_component import show_huge_success' not in content:
        # Find the last import statement
        import_pattern = r'^(import .*|from .* import .*)\n'
        imports = list(re.finditer(import_pattern, content, re.MULTILINE))
        
        if imports:
            # Add after last import
            last_import = imports[-1]
            insert_pos = last_import.end()
            content = (content[:insert_pos] + 
                      'from success_message_component import show_huge_success\n' +
                      content[insert_pos:])
        else:
            # Add at beginning after docstring
            docstring_end = content.find('"""', 3)
            if docstring_end > 0:
                insert_pos = content.find('\n', docstring_end) + 1
                content = (content[:insert_pos] + 
                          '\nfrom success_message_component import show_huge_success\n' +
                          content[insert_pos:])
    
    return content

def update_file(filepath):
    """Update a single file"""
    if not os.path.exists(filepath):
        print(f"⚠️  Skipped (not found): {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add import
        content = add_import_if_missing(content)
        
        # Pattern to match st.success with "successfully" or "SUCCESS"
        # This is a simple pattern - may need manual review
        success_pattern = r'st\.success\((f?"""[\s\S]*?(?:successfully|SUCCESS|SUCCESSFUL)[\s\S]*?""")\)'
        
        matches = list(re.finditer(success_pattern, content, re.IGNORECASE))
        
        if matches:
            print(f"\n📝 {filepath}")
            print(f"   Found {len(matches)} success message(s)")
            
            # For now, just add a comment to manually review
            # Full automation would require understanding context
            for match in matches:
                print(f"   - Line ~{content[:match.start()].count(chr(10)) + 1}")
        
        # Save if import was added
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    print("🚀 APPLYING HUGE SUCCESS MESSAGES TO ALL MODULES")
    print("=" * 60)
    
    updated = 0
    
    for filepath in files_to_update:
        if update_file(filepath):
            updated += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Added imports to {updated} files")
    print("\n⚠️  MANUAL REVIEW NEEDED:")
    print("   The import has been added to all files.")
    print("   You need to manually replace st.success() with show_huge_success()")
    print("   in the files listed above.")
    print("\n💡 TIP: Search for 'st.success' in each file and replace with:")
    print("   show_huge_success(title='YOUR_TITLE', subtitle='...')")

if __name__ == "__main__":
    main()
