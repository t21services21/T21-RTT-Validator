"""
TEST SCRIPT - Verify all student_login.py imports work
Run this to confirm all modules and functions exist
"""

print("Testing student_login.py imports...")
print("=" * 50)

# Test 1: student_auth
try:
    from student_auth import login_student, register_student
    print("[OK] student_auth: login_student, register_student")
except Exception as e:
    print(f"[FAIL] student_auth: {e}")

# Test 2: advanced_access_control
try:
    from advanced_access_control import UserAccount
    print("[OK] advanced_access_control: UserAccount")
except Exception as e:
    print(f"[FAIL] advanced_access_control: {e}")

# Test 3: auth_persistence
try:
    from auth_persistence import initialize_auth_session, save_auth_cookie
    print("[OK] auth_persistence: initialize_auth_session, save_auth_cookie")
except Exception as e:
    print(f"[FAIL] auth_persistence: {e}")

# Test 4: supabase_database
try:
    from supabase_database import update_user_last_login, get_user_by_email, use_backup_code
    print("[OK] supabase_database: update_user_last_login, get_user_by_email, use_backup_code")
except Exception as e:
    print(f"[FAIL] supabase_database: {e}")

# Test 5: two_factor_auth
try:
    from two_factor_auth import verify_2fa_code
    print("[OK] two_factor_auth: verify_2fa_code")
except Exception as e:
    print(f"[FAIL] two_factor_auth: {e}")

# Test 6: hashlib
try:
    import hashlib
    print("[OK] hashlib (built-in)")
except Exception as e:
    print(f"[FAIL] hashlib: {e}")

print("=" * 50)
print("\nIf all show [OK], the imports are correct!")
print("If any show [FAIL], that module/function doesn't exist.")
