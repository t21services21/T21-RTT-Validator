"""
T21 PLATFORM - COMPREHENSIVE TESTING SCRIPT
Tests all critical functions before NHS demo
"""

import sys
import os
from datetime import datetime

# Test results
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def log_pass(test_name):
    test_results["passed"].append(test_name)
    print(f"[PASS] {test_name}")

def log_fail(test_name, error):
    test_results["failed"].append((test_name, error))
    print(f"[FAIL] {test_name} - {error}")

def log_warning(test_name, message):
    test_results["warnings"].append((test_name, message))
    print(f"[WARN] {test_name} - {message}")

print("="*60)
print("T21 PLATFORM - COMPREHENSIVE TEST SUITE")
print("="*60)
print()

# TEST 1: Import Core Modules
print("TEST 1: Core Module Imports")
print("-"*60)

try:
    import streamlit as st
    log_pass("Streamlit import")
except Exception as e:
    log_fail("Streamlit import", str(e))

try:
    import pandas as pd
    log_pass("Pandas import")
except Exception as e:
    log_fail("Pandas import", str(e))

try:
    from admin_panel_ui import render_admin_panel
    log_pass("Admin panel import")
except Exception as e:
    log_fail("Admin panel import", str(e))

try:
    from admin_user_tracking_ui import render_user_tracking_dashboard
    log_pass("User tracking import")
except Exception as e:
    log_fail("User tracking import", str(e))

try:
    from sidebar_manager import render_sidebar
    log_pass("Sidebar manager import")
except Exception as e:
    log_fail("Sidebar manager import", str(e))

try:
    from supabase_database import get_all_users, get_user_by_email
    log_pass("Supabase database import")
except Exception as e:
    log_fail("Supabase database import", str(e))

try:
    from student_auth import login_student, register_student
    log_pass("Student auth import")
except Exception as e:
    log_fail("Student auth import", str(e))

print()

# TEST 2: Database Functions
print("TEST 2: Database Functions")
print("-"*60)

try:
    from admin_management import load_users_db
    users = load_users_db()
    if isinstance(users, dict):
        log_pass(f"Load users DB ({len(users)} users)")
    else:
        log_fail("Load users DB", "Returned non-dict")
except Exception as e:
    log_fail("Load users DB", str(e))

try:
    from student_auth import list_all_students
    students = list_all_students()
    if isinstance(students, list):
        log_pass(f"List students ({len(students)} students)")
    else:
        log_fail("List students", "Returned non-list")
except Exception as e:
    log_fail("List students", str(e))

try:
    from supabase_database import get_all_users
    supabase_users = get_all_users()
    if isinstance(supabase_users, list):
        log_pass(f"Supabase get_all_users ({len(supabase_users)} users)")
    else:
        log_fail("Supabase get_all_users", "Returned non-list")
except Exception as e:
    log_fail("Supabase get_all_users", str(e))

print()

# TEST 3: User Tracking System
print("TEST 3: User Tracking System")
print("-"*60)

try:
    from user_tracking_system import get_all_users_tracking, load_tracking_db
    tracking_data = get_all_users_tracking()
    if isinstance(tracking_data, dict):
        log_pass(f"User tracking ({len(tracking_data)} tracked)")
    else:
        log_fail("User tracking", "Returned non-dict")
except Exception as e:
    log_fail("User tracking", str(e))

try:
    from user_tracking_system import get_user_tracking_summary
    # Test with fake email
    summary = get_user_tracking_summary("test@example.com")
    log_pass("User tracking summary function")
except Exception as e:
    log_fail("User tracking summary", str(e))

print()

# TEST 4: License System
print("TEST 4: License System")
print("-"*60)

try:
    from advanced_access_control import UserAccount
    log_pass("UserAccount class import")
except Exception as e:
    log_fail("UserAccount class import", str(e))

try:
    from license_manager import generate_license_key
    key = generate_license_key()
    if key and len(key) > 10:
        log_pass(f"Generate license key ({key[:8]}...)")
    else:
        log_fail("Generate license key", "Invalid key generated")
except Exception as e:
    log_fail("Generate license key", str(e))

print()

# TEST 5: File Existence
print("TEST 5: Critical Files Exist")
print("-"*60)

critical_files = [
    "app.py",
    "requirements.txt",
    "admin_panel_ui.py",
    "admin_user_tracking_ui.py",
    "sidebar_manager.py",
    "supabase_database.py",
    "student_auth.py",
    "user_tracking_system.py",
    "advanced_access_control.py",
    "assets/logo.png",
    "pages/student_login.py",
    "pages/staff_login.py",
    "pages/nhs_login.py",
    "pages/contact_us.py",
    "pages/terms_of_service.py",
    "pages/privacy_policy.py"
]

for file_path in critical_files:
    if os.path.exists(file_path):
        log_pass(f"File exists: {file_path}")
    else:
        log_fail(f"File exists: {file_path}", "NOT FOUND")

print()

# TEST 6: Requirements Check
print("TEST 6: Requirements Installed")
print("-"*60)

required_packages = [
    "streamlit",
    "pandas",
    "supabase",
    "PyPDF2",
    "python-docx",
    "qrcode",
    "pyotp"
]

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
        log_pass(f"Package installed: {package}")
    except ImportError:
        log_fail(f"Package installed: {package}", "NOT INSTALLED")

print()

# TEST 7: Configuration Check
print("TEST 7: Configuration & Environment")
print("-"*60)

try:
    import streamlit as st
    # Check if secrets available
    if hasattr(st, 'secrets'):
        log_pass("Streamlit secrets available")
        try:
            supabase_url = st.secrets.get("SUPABASE_URL")
            if supabase_url:
                log_pass("Supabase URL configured")
            else:
                log_warning("Supabase URL", "Not found in secrets")
        except:
            log_warning("Supabase secrets", "Cannot access")
    else:
        log_warning("Streamlit secrets", "Not available (OK in local)")
except Exception as e:
    log_warning("Configuration check", str(e))

print()

# TEST 8: Date/Time Functions
print("TEST 8: Date/Time Functions")
print("-"*60)

try:
    from datetime import datetime, timedelta
    now = datetime.now()
    future = now + timedelta(days=30)
    log_pass(f"DateTime operations (Current: {now.strftime('%Y-%m-%d')})")
except Exception as e:
    log_fail("DateTime operations", str(e))

print()

# FINAL RESULTS
print("="*60)
print("TEST SUMMARY")
print("="*60)

total_tests = len(test_results["passed"]) + len(test_results["failed"])
pass_rate = (len(test_results["passed"]) / total_tests * 100) if total_tests > 0 else 0

print(f"\n[+] PASSED: {len(test_results['passed'])}")
print(f"[-] FAILED: {len(test_results['failed'])}")
print(f"[!] WARNINGS: {len(test_results['warnings'])}")
print(f"\nPASS RATE: {pass_rate:.1f}%")

if test_results["failed"]:
    print("\n" + "="*60)
    print("FAILED TESTS - NEED ATTENTION:")
    print("="*60)
    for test_name, error in test_results["failed"]:
        print(f"\n[-] {test_name}")
        print(f"   Error: {error}")

if test_results["warnings"]:
    print("\n" + "="*60)
    print("WARNINGS - REVIEW IF NEEDED:")
    print("="*60)
    for test_name, message in test_results["warnings"]:
        print(f"\n[!] {test_name}")
        print(f"   Message: {message}")

print("\n" + "="*60)
if pass_rate >= 90:
    print("EXCELLENT! Platform ready for demo!")
elif pass_rate >= 75:
    print("GOOD! Review failed tests and fix if critical.")
elif pass_rate >= 50:
    print("ATTENTION NEEDED! Several issues to fix.")
else:
    print("CRITICAL! Major issues - do not demo yet!")

print("="*60)
print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Exit with proper code
exit(0 if len(test_results["failed"]) == 0 else 1)
