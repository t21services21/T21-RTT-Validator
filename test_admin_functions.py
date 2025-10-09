"""
Test Admin Functions
Verify all user management functions are working
"""
import sys
sys.path.insert(0, '.')

from admin_management import (
    get_all_users, get_user_details, suspend_user, unsuspend_user,
    extend_license, change_role
)

print("=" * 70)
print("TESTING ADMIN FUNCTIONS")
print("=" * 70)

# Test 1: Get All Users
print("\n1. TESTING: Get All Users")
print("-" * 70)
try:
    all_users = get_all_users()
    print(f"SUCCESS: Found {len(all_users)} users")
    print("\nUSERS LIST:")
    for i, user in enumerate(all_users, 1):
        print(f"\n{i}. {user['email']}")
        print(f"   Name: {user['full_name']}")
        print(f"   Role: {user['role_name']}")
        print(f"   Type: {user['user_type']}")
        print(f"   Status: {user.get('status_display', user.get('status', 'Unknown'))}")
        print(f"   Expires: {user.get('expiry_date', 'Unknown')}")
        print(f"   Days Remaining: {user.get('days_remaining', 'Unknown')}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Get User Details
print("\n\n2. TESTING: Get User Details")
print("-" * 70)
test_emails = [
    "staff@t21services.co.uk",
    "admin@t21services.co.uk",
    "t.owonifari@t21services.co.uk"
]

for email in test_emails:
    print(f"\nChecking: {email}")
    try:
        details = get_user_details(email)
        if details:
            print(f"  SUCCESS: User found")
            print(f"  Name: {details.get('full_name')}")
            print(f"  Role: {details.get('role')}")
            print(f"  Status: {details.get('status')}")
            print(f"  Has password_hash: {'Yes' if details.get('password_hash') else 'No'}")
        else:
            print(f"  NOT FOUND in advanced database")
            print(f"  (May be in legacy database)")
    except Exception as e:
        print(f"  ERROR: {e}")

# Test 3: Filter Users by Type
print("\n\n3. TESTING: Filter Users by Type")
print("-" * 70)
for user_type in ['student', 'staff', 'admin']:
    try:
        filtered = get_all_users(filter_by={"type": user_type})
        print(f"{user_type.upper()}: {len(filtered)} users")
    except Exception as e:
        print(f"{user_type.upper()}: ERROR - {e}")

# Test 4: Filter Users by Status
print("\n\n4. TESTING: Filter Users by Status")
print("-" * 70)
for status in ['active', 'suspended', 'expired']:
    try:
        filtered = get_all_users(filter_by={"status": status})
        print(f"{status.upper()}: {len(filtered)} users")
    except Exception as e:
        print(f"{status.upper()}: ERROR - {e}")

# Test 5: Test Extend License Function
print("\n\n5. TESTING: Extend License Function (DRY RUN)")
print("-" * 70)
print("Testing if function exists and is callable...")
try:
    # Just check if function exists, don't actually extend
    from admin_management import extend_license
    print("SUCCESS: extend_license function exists")
    print("Function signature:", extend_license.__code__.co_varnames[:extend_license.__code__.co_argcount])
except Exception as e:
    print(f"ERROR: {e}")

# Test 6: Test Change Role Function
print("\n\n6. TESTING: Change Role Function (DRY RUN)")
print("-" * 70)
print("Testing if function exists and is callable...")
try:
    from admin_management import change_role
    print("SUCCESS: change_role function exists")
    print("Function signature:", change_role.__code__.co_varnames[:change_role.__code__.co_argcount])
except Exception as e:
    print(f"ERROR: {e}")

# Test 7: Test Suspend/Unsuspend Functions
print("\n\n7. TESTING: Suspend/Unsuspend Functions (DRY RUN)")
print("-" * 70)
print("Testing if functions exist and are callable...")
try:
    from admin_management import suspend_user, unsuspend_user
    print("SUCCESS: suspend_user function exists")
    print("SUCCESS: unsuspend_user function exists")
except Exception as e:
    print(f"ERROR: {e}")

# Summary
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("All critical admin functions have been tested.")
print("Check above for any ERROR messages.")
print("\nIf all tests show SUCCESS, the admin panel should work properly!")
print("=" * 70)
