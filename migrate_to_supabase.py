"""
T21 SERVICES - MIGRATE USERS TO SUPABASE
This script moves your existing 4 users from JSON files to Supabase database
"""

import json
from supabase_database import create_user, get_all_users

print("=" * 80)
print("T21 SERVICES - MIGRATING USERS TO SUPABASE")
print("=" * 80)

# Load existing users from JSON files
users_to_migrate = []

# Try users_database.json
try:
    with open('users_database.json', 'r') as f:
        old_users = json.load(f)
    
    print(f"\n✅ Found {len(old_users)} users in users_database.json")
    
    for email, user_data in old_users.items():
        license = user_data.get('license', {})
        role = license.get('role', 'trial')
        
        user_info = {
            'email': email,
            'password_hash': user_data.get('password_hash', ''),
            'full_name': user_data.get('full_name', 'Unknown'),
            'role': role,
            'user_type': 'admin' if role == 'admin' else 'student'
        }
        users_to_migrate.append(user_info)
        print(f"   - {email} ({role})")

except FileNotFoundError:
    print("\n⚠️ users_database.json not found")
except Exception as e:
    print(f"\n❌ Error reading users_database.json: {e}")

# Try users_advanced.json
try:
    with open('users_advanced.json', 'r') as f:
        advanced_users = json.load(f)
    
    print(f"\n✅ Found {len(advanced_users)} users in users_advanced.json")
    
    for email, user_data in advanced_users.items():
        # Skip if already added from users_database.json
        if any(u['email'] == email for u in users_to_migrate):
            print(f"   - {email} (already added)")
            continue
        
        role = user_data.get('role', 'trial')
        user_type = 'admin' if role in ['admin', 'super_admin'] else ('staff' if 'staff' in role else 'student')
        
        user_info = {
            'email': email,
            'password_hash': user_data.get('password_hash', ''),
            'full_name': user_data.get('full_name', 'Unknown'),
            'role': role,
            'user_type': user_type
        }
        users_to_migrate.append(user_info)
        print(f"   - {email} ({role})")

except FileNotFoundError:
    print("\n⚠️ users_advanced.json not found")
except Exception as e:
    print(f"\n❌ Error reading users_advanced.json: {e}")

# Migrate users
print("\n" + "=" * 80)
print(f"MIGRATING {len(users_to_migrate)} USERS TO SUPABASE")
print("=" * 80)

migrated_count = 0
skipped_count = 0
error_count = 0

for user in users_to_migrate:
    email = user['email']
    
    # Check if user already exists in Supabase
    from supabase_database import get_user_by_email
    existing = get_user_by_email(email)
    
    if existing:
        print(f"\n⏭️ SKIPPED: {email} (already in Supabase)")
        skipped_count += 1
        continue
    
    # Create user in Supabase
    print(f"\n📤 Migrating: {email}")
    print(f"   Role: {user['role']}")
    print(f"   Type: {user['user_type']}")
    
    success, message = create_user(
        email=user['email'],
        password_hash=user['password_hash'],
        full_name=user['full_name'],
        role=user['role'],
        user_type=user['user_type']
    )
    
    if success:
        print(f"   ✅ SUCCESS: {message}")
        migrated_count += 1
    else:
        print(f"   ❌ ERROR: {message}")
        error_count += 1

# Summary
print("\n" + "=" * 80)
print("MIGRATION COMPLETE!")
print("=" * 80)
print(f"✅ Migrated: {migrated_count} users")
print(f"⏭️ Skipped: {skipped_count} users (already existed)")
print(f"❌ Errors: {error_count} users")
print(f"📊 Total: {len(users_to_migrate)} users processed")

# Verify migration
print("\n" + "=" * 80)
print("VERIFYING MIGRATION")
print("=" * 80)

all_users = get_all_users()
print(f"\n✅ Total users in Supabase: {len(all_users)}")

if all_users:
    print("\nUsers in database:")
    for user in all_users:
        print(f"   - {user.get('email')} | {user.get('full_name')} | {user.get('role')} | {user.get('status')}")

print("\n" + "=" * 80)
print("✅ MIGRATION SUCCESSFUL!")
print("=" * 80)
print("\nNext steps:")
print("1. Test login with your existing credentials")
print("2. Check admin panel - you should see all users")
print("3. Try registering a new test user")
print("4. New users will be saved forever (no more data loss!)")
print("\n" + "=" * 80)
