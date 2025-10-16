"""
DEBUG WHY LAWUNMI IS MISSING
Check all databases and see where the data is
"""

def debug_missing_users():
    """Find where Lawunmi went!"""
    
    email = "lawunmilatinwo@outlook.com"
    
    print("=" * 70)
    print("DEBUGGING MISSING USERS")
    print("=" * 70)
    
    # ========================================
    # CHECK 1: Supabase Direct
    # ========================================
    print("\n1️⃣ SUPABASE DIRECT QUERY")
    print("-" * 70)
    try:
        from supabase_database import supabase
        
        # Get ALL users
        all_result = supabase.table('users').select('*').execute()
        print(f"Total users in Supabase: {len(all_result.data) if all_result.data else 0}")
        
        if all_result.data:
            print("\nAll emails in Supabase:")
            for user in all_result.data:
                print(f"  - {user.get('email')} | {user.get('role')} | {user.get('full_name')}")
        
        # Check for Lawunmi specifically
        lawunmi_result = supabase.table('users').select('*').eq('email', email).execute()
        
        if lawunmi_result.data:
            print(f"\n✅ LAWUNMI FOUND IN SUPABASE!")
            user = lawunmi_result.data[0]
            print(f"   Email: {user.get('email')}")
            print(f"   Name: {user.get('full_name')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Status: {user.get('status')}")
        else:
            print(f"\n❌ LAWUNMI NOT IN SUPABASE")
    
    except Exception as e:
        print(f"❌ Supabase error: {e}")
    
    # ========================================
    # CHECK 2: get_all_users() function
    # ========================================
    print("\n\n2️⃣ get_all_users() FUNCTION (What Admin Panel sees)")
    print("-" * 70)
    try:
        from admin_management import get_all_users
        
        all_users = get_all_users()
        print(f"Total users returned: {len(all_users)}")
        
        print("\nAll users from get_all_users():")
        for user in all_users:
            print(f"  - {user.get('email')} | {user.get('role')} | {user.get('full_name')}")
        
        # Check for Lawunmi
        lawunmi_users = [u for u in all_users if u.get('email') == email]
        
        if lawunmi_users:
            print(f"\n✅ LAWUNMI IN get_all_users()!")
        else:
            print(f"\n❌ LAWUNMI NOT IN get_all_users()!")
            print("\n🔍 THIS IS THE BUG - Supabase has it but get_all_users() doesn't return it!")
    
    except Exception as e:
        print(f"❌ get_all_users() error: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # CHECK 3: Local JSON files
    # ========================================
    print("\n\n3️⃣ LOCAL JSON FILES")
    print("-" * 70)
    
    import os
    import json
    
    json_files = ["users_advanced.json", "users_database.json"]
    
    for json_file in json_files:
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                print(f"\n{json_file}: {len(data)} users")
                
                if email in data:
                    print(f"  ✅ Lawunmi FOUND in {json_file}")
                    print(f"     Role: {data[email].get('role')}")
                else:
                    print(f"  ❌ Lawunmi NOT in {json_file}")
                    
                print(f"  All emails in {json_file}:")
                for e in list(data.keys())[:10]:  # Show first 10
                    print(f"    - {e}")
            
            except Exception as e:
                print(f"  ⚠️  Error reading {json_file}: {e}")
        else:
            print(f"\n{json_file}: DOESN'T EXIST")
    
    # ========================================
    # CHECK 4: Filters or Conversion Issues
    # ========================================
    print("\n\n4️⃣ CHECKING FOR FILTER/CONVERSION ISSUES")
    print("-" * 70)
    
    try:
        from supabase_database import get_all_users as get_supabase_users
        
        supabase_users = get_supabase_users()
        print(f"Supabase get_all_users(): {len(supabase_users)} users")
        
        lawunmi_supabase = [u for u in supabase_users if u.get('email') == email]
        
        if lawunmi_supabase:
            print(f"✅ Lawunmi in supabase_database.get_all_users()")
            user = lawunmi_supabase[0]
            print(f"\nLawunmi's data structure:")
            for key, value in user.items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ Lawunmi NOT in supabase_database.get_all_users()")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    print("\nIf Lawunmi is:")
    print("  ✅ In Supabase BUT ❌ NOT in get_all_users()")
    print("  → BUG in admin_management.py get_all_users() function")
    print("  → Supabase data not being properly converted/returned")
    print("\nIf Lawunmi is:")
    print("  ❌ NOT in Supabase")
    print("  → Account creation failed or was deleted")
    print("  → Need to re-create account")
    print("=" * 70)


if __name__ == "__main__":
    debug_missing_users()
