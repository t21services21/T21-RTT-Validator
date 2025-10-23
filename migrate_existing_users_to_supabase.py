"""
MIGRATE EXISTING USERS TO SUPABASE
Run this ONCE to copy all users from local JSON to Supabase
"""

import json
import os
from supabase_database import create_user as supabase_create_user

def migrate_users():
    """Migrate all users from local JSON to Supabase"""
    
    # Load local users
    if not os.path.exists("users_database.json"):
        print("❌ No users_database.json found")
        return
    
    with open("users_database.json", 'r') as f:
        users = json.load(f)
    
    print(f"📊 Found {len(users)} users in local database")
    print("=" * 60)
    
    migrated = 0
    failed = 0
    skipped = 0
    
    for email, user_data in users.items():
        print(f"\n🔍 Processing: {email}")
        
        # Get user details
        full_name = user_data.get('full_name', 'Unknown')
        role = user_data.get('role', 'student_trial')
        password_hash = user_data.get('password_hash', '')
        
        if not password_hash:
            print(f"   ⚠️  Skipped: No password hash")
            skipped += 1
            continue
        
        # Determine user type from role
        user_type_map = {
            'student_trial': 'student',
            'student_basic': 'student',
            'student_professional': 'student',
            'student_ultimate': 'student',
            'staff_trainer': 'staff',
            'staff_support': 'staff',
            'tester': 'tester',
            'admin': 'admin',
            'super_admin': 'super_admin'
        }
        
        user_type = user_type_map.get(role, 'student')
        
        # Try to create in Supabase
        try:
            success, msg = supabase_create_user(email, password_hash, full_name, role, user_type)
            
            if success:
                print(f"   ✅ Migrated successfully")
                migrated += 1
            else:
                if "already exists" in msg.lower() or "duplicate" in msg.lower():
                    print(f"   ℹ️  Already in Supabase")
                    skipped += 1
                else:
                    print(f"   ❌ Failed: {msg}")
                    failed += 1
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 MIGRATION COMPLETE")
    print(f"   ✅ Migrated: {migrated}")
    print(f"   ℹ️  Skipped: {skipped}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📊 Total: {len(users)}")
    print("=" * 60)

if __name__ == "__main__":
    print("🚀 STARTING USER MIGRATION TO SUPABASE")
    print("=" * 60)
    migrate_users()
    print("\n✅ Done! Users can now log in.")
