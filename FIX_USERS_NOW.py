"""
FINAL FIX - MAKE ALL USERS VISIBLE
No more diagnostics - just fix it
"""

import bcrypt
from datetime import datetime, timedelta
import json
import os

def fix_all_users():
    """Fix user visibility issues"""
    
    print("=" * 70)
    print("FIXING USER VISIBILITY ISSUES")
    print("=" * 70)
    
    # Users that should exist
    required_users = [
        {
            'email': 'lawunmilatinwo@outlook.com',
            'full_name': 'Lawunmi Latinwo',
            'password': 'Admin2025!',
            'role': 'staff',
            'user_type': 'staff'
        },
        {
            'email': 'training@t21services.co.uk',
            'full_name': 'Training Account',
            'password': 'Training2025!',
            'role': 'admin',
            'user_type': 'admin'
        }
    ]
    
    try:
        from supabase_database import supabase
        
        for user_info in required_users:
            email = user_info['email']
            print(f"\n🔍 Processing: {email}")
            
            # Check if exists in Supabase
            result = supabase.table('users').select('*').eq('email', email).execute()
            
            hashed_pw = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if result.data:
                # EXISTS - Update to ensure all fields correct
                print(f"   ✅ Found in Supabase - Updating...")
                
                update_data = {
                    'full_name': user_info['full_name'],
                    'password_hash': hashed_pw,
                    'role': user_info['role'],
                    'user_type': user_info['user_type'],  # ADD THIS FIELD!
                    'status': 'active',
                    'trial_end_date': (datetime.now() + timedelta(days=9999)).isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                supabase.table('users').update(update_data).eq('email', email).execute()
                print(f"   ✅ Updated with user_type={user_info['user_type']}")
            
            else:
                # DOESN'T EXIST - Create it
                print(f"   ⚠️  NOT in Supabase - Creating...")
                
                insert_data = {
                    'email': email,
                    'full_name': user_info['full_name'],
                    'password_hash': hashed_pw,
                    'role': user_info['role'],
                    'user_type': user_info['user_type'],  # ADD THIS FIELD!
                    'status': 'active',
                    'trial_end_date': (datetime.now() + timedelta(days=9999)).isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                supabase.table('users').insert(insert_data).execute()
                print(f"   ✅ Created in Supabase")
            
            # Also save to local JSON for backup
            db_file = "users_advanced.json"
            if os.path.exists(db_file):
                with open(db_file, 'r') as f:
                    users = json.load(f)
            else:
                users = {}
            
            users[email] = {
                'email': email,
                'full_name': user_info['full_name'],
                'password_hash': hashed_pw,
                'role': user_info['role'],
                'user_type': user_info['user_type'],
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'trial_end_date': (datetime.now() + timedelta(days=9999)).isoformat()
            }
            
            with open(db_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            print(f"   ✅ Saved to {db_file}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Now verify they appear in get_all_users()
    print("\n" + "=" * 70)
    print("VERIFICATION - Checking get_all_users()")
    print("=" * 70)
    
    try:
        from admin_management import get_all_users
        
        all_users = get_all_users()
        print(f"\nTotal users returned: {len(all_users)}")
        
        for user_info in required_users:
            email = user_info['email']
            found = any(u['email'] == email for u in all_users)
            
            if found:
                print(f"✅ {email} - VISIBLE in Admin Panel!")
            else:
                print(f"❌ {email} - STILL NOT VISIBLE!")
        
        print("\nAll emails in get_all_users():")
        for u in all_users:
            print(f"  - {u['email']} ({u.get('role', 'unknown')})")
    
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("✅ FIX COMPLETE - REFRESH ADMIN PANEL")
    print("=" * 70)
    print("\nCredentials:")
    for user_info in required_users:
        print(f"\n{user_info['email']}")
        print(f"  Password: {user_info['password']}")
        print(f"  Role: {user_info['role']}")
    print("\n" + "=" * 70)
    
    return True


if __name__ == "__main__":
    fix_all_users()
