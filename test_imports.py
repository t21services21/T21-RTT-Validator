"""
Quick import test to check if all new modules can be imported
Run this to see which imports are failing
"""
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("Testing imports...")

print("\n1. Testing executive_dashboard...")
try:
    from executive_dashboard import render_executive_dashboard
    print("   ✅ executive_dashboard - OK")
except Exception as e:
    print(f"   ❌ executive_dashboard - FAILED: {e}")

print("\n2. Testing unified_patient_ui...")
try:
    from unified_patient_ui import render_unified_patient_search
    print("   ✅ unified_patient_ui - OK")
except Exception as e:
    print(f"   ❌ unified_patient_ui - FAILED: {e}")

print("\n3. Testing task_management_ui...")
try:
    from task_management_ui import render_task_management
    print("   ✅ task_management_ui - OK")
except Exception as e:
    print(f"   ❌ task_management_ui - FAILED: {e}")

print("\n4. Testing clinical_letters_ui...")
try:
    from clinical_letters_ui import render_clinical_letters
    print("   ✅ clinical_letters_ui - OK")
except Exception as e:
    print(f"   ❌ clinical_letters_ui - FAILED: {e}")

print("\n5. Testing document_management_ui...")
try:
    from document_management_ui import render_document_management
    print("   ✅ document_management_ui - OK")
except Exception as e:
    print(f"   ❌ document_management_ui - FAILED: {e}")

print("\n6. Testing task_management_system...")
try:
    from task_management_system import get_task_stats
    print("   ✅ task_management_system - OK")
except Exception as e:
    print(f"   ❌ task_management_system - FAILED: {e}")

print("\n7. Testing document_management_system...")
try:
    from document_management_system import upload_document
    print("   ✅ document_management_system - OK")
except Exception as e:
    print(f"   ❌ document_management_system - FAILED: {e}")

print("\n8. Testing unified_patient_system...")
try:
    from unified_patient_system import find_patient_by_nhs
    print("   ✅ unified_patient_system - OK")
except Exception as e:
    print(f"   ❌ unified_patient_system - FAILED: {e}")

print("\n9. Testing clinical_letters...")
try:
    from clinical_letters import generate_mdt_gp_letter
    print("   ✅ clinical_letters - OK")
except Exception as e:
    print(f"   ❌ clinical_letters - FAILED: {e}")

print("\n✅ Import test complete!")
print("\nRun this with: python test_imports.py")
