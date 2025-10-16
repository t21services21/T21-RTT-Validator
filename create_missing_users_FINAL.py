"""
CREATE MISSING USERS - FINAL FIX
No more diagnostics - just create them!
"""

import bcrypt
from datetime import datetime, timedelta
from supabase_database import supabase

def create_missing_users():
    """Create lawunmi and training accounts"""
    
    print("=" * 70)
    print("CREATING MISSING USERS IN SUPABASE")
    print("=" * 70)
    
    users_to_create = [
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
    
    for user_info in users_to_create:
        email = user_info['email']
        print(f"\n{'='*70}")
        print(f"Processing: {email}")
        print('='*70)
        
        try:
            # Check if exists
            result = supabase.table('users').select('*').eq('email', email).execute()
            
            # Hash password
            hashed_pw = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            user_data = {
                'email': email,
                'full_name': user_info['full_name'],
                'password_hash': hashed_pw,
                'role': user_info['role'],
                'user_type': user_info['user_type'],
                'status': 'active',
                'trial_end_date': (datetime.now() + timedelta(days=9999)).isoformat(),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            if result.data and len(result.data) > 0:
                # EXISTS - Update it
                print(f"   ✅ Found in Supabase - UPDATING...")
                supabase.table('users').update(user_data).eq('email', email).execute()
                print(f"   ✅ UPDATED with user_type='{user_info['user_type']}'")
            else:
                # DOESN'T EXIST - Create it
                print(f"   ❌ NOT in Supabase - CREATING...")
                supabase.table('users').insert(user_data).execute()
                print(f"   ✅ CREATED with user_type='{user_info['user_type']}'")
            
            print(f"\n   📧 Email: {email}")
            print(f"   🔑 Password: {user_info['password']}")
            print(f"   👤 Role: {user_info['role']}")
            print(f"   🏷️  User Type: {user_info['user_type']}")
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Verify they now appear
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    
    try:
        all_users_result = supabase.table('users').select('email, full_name, role, user_type').execute()
        
        if all_users_result.data:
            print(f"\nTotal users in Supabase now: {len(all_users_result.data)}")
            print("\nAll users:")
            for u in all_users_result.data:
                print(f"  - {u['email']} | {u.get('role')} | user_type={u.get('user_type', 'NOT SET')}")
            
            # Check our specific users
            print("\n" + "-" * 70)
            for user_info in users_to_create:
                email = user_info['email']
                found = any(u['email'] == email for u in all_users_result.data)
                if found:
                    print(f"✅ {email} - NOW VISIBLE!")
                else:
                    print(f"❌ {email} - STILL MISSING!")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
    
    print("\n" + "=" * 70)
    print("✅ DONE - REFRESH ADMIN PANEL NOW!")
    print("=" * 70)


if __name__ == "__main__":
    create_missing_users()
