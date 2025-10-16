"""
DEEP DIAGNOSTIC - Find WHY Lawunmi's account isn't showing
"""

def deep_diagnose():
    """Deep diagnostic of all databases and connections"""
    
    email = "lawunmilatinwo@outlook.com"
    
    print("=" * 70)
    print("DEEP DIAGNOSTIC - FINDING LAWUNMI'S ACCOUNT")
    print("=" * 70)
    print(f"\nSearching for: {email}\n")
    
    # ========================================
    # TEST 1: Direct Supabase Query
    # ========================================
    print("1️⃣ DIRECT SUPABASE QUERY")
    print("-" * 70)
    try:
        from supabase_database import supabase
        
        print("✓ Supabase imported")
        
        # Query directly
        result = supabase.table('users').select('*').eq('email', email).execute()
        
        print(f"✓ Query executed")
        print(f"   Result data: {result.data}")
        print(f"   Number of results: {len(result.data) if result.data else 0}")
        
        if result.data:
            print("\n✅ FOUND IN SUPABASE!")
            user = result.data[0]
            print(f"   Email: {user.get('email')}")
            print(f"   Name: {user.get('full_name')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Status: {user.get('status')}")
            print(f"   Created: {user.get('created_at')}")
        else:
            print("\n❌ NOT IN SUPABASE!")
    
    except ImportError as e:
        print(f"❌ Cannot import Supabase: {e}")
    except Exception as e:
        print(f"❌ Supabase query error: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # TEST 2: Supabase get_all_users()
    # ========================================
    print("\n\n2️⃣ SUPABASE get_all_users() FUNCTION")
    print("-" * 70)
    try:
        from supabase_database import get_all_users as get_supabase_users
        
        all_users = get_supabase_users()
        
        print(f"✓ Function executed")
        print(f"   Total users returned: {len(all_users)}")
        
        if all_users:
            print(f"\n   Sample users:")
            for i, u in enumerate(all_users[:5]):
                print(f"   {i+1}. {u.get('email')} - {u.get('full_name')}")
        
        # Check if lawunmi is in there
        lawunmi_users = [u for u in all_users if u.get('email') == email]
        
        if lawunmi_users:
            print(f"\n✅ LAWUNMI IS IN get_all_users()!")
        else:
            print(f"\n❌ LAWUNMI NOT IN get_all_users()!")
            print(f"\n   All emails from Supabase:")
            for u in all_users:
                print(f"   - {u.get('email')}")
    
    except ImportError:
        print("⚠️  Supabase get_all_users not available")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # TEST 3: Admin Panel's get_all_users()
    # ========================================
    print("\n\n3️⃣ ADMIN PANEL'S get_all_users() FUNCTION")
    print("-" * 70)
    try:
        from admin_management import get_all_users
        
        all_users = get_all_users()
        
        print(f"✓ Function executed")
        print(f"   Total users returned: {len(all_users)}")
        
        if all_users:
            print(f"\n   Users Admin Panel sees:")
            for i, u in enumerate(all_users):
                print(f"   {i+1}. {u.get('email')} - {u.get('full_name')}")
        
        # Check if lawunmi is in there
        lawunmi_in_list = [u for u in all_users if u.get('email') == email]
        
        if lawunmi_in_list:
            print(f"\n✅ ADMIN PANEL CAN SEE LAWUNMI!")
        else:
            print(f"\n❌ ADMIN PANEL CANNOT SEE LAWUNMI!")
            print(f"\n   This is why Lawunmi doesn't appear in the dropdown!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # TEST 4: Local JSON Files
    # ========================================
    print("\n\n4️⃣ LOCAL JSON DATABASE FILES")
    print("-" * 70)
    
    import os
    import json
    
    json_files = [
        "users_advanced.json",
        "users_database.json",
        "users.json"
    ]
    
    for json_file in json_files:
        print(f"\n   Checking {json_file}...")
        
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                print(f"   ✓ File exists - {len(data)} users")
                
                if email in data:
                    print(f"   ✅ FOUND Lawunmi in {json_file}!")
                    user = data[email]
                    print(f"      Name: {user.get('full_name')}")
                    print(f"      Role: {user.get('role')}")
                else:
                    print(f"   ❌ NOT in {json_file}")
                    
                    # Show what emails ARE in there
                    if len(data) <= 10:
                        print(f"      Emails in file:")
                        for e in data.keys():
                            print(f"      - {e}")
            
            except Exception as e:
                print(f"   ⚠️  Error reading file: {e}")
        else:
            print(f"   ⚠️  File doesn't exist")
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    print("\nIf Lawunmi is:")
    print("  ✅ In Supabase but NOT in Admin Panel → Supabase connection issue")
    print("  ❌ NOT in Supabase → Account was never created")
    print("  ✅ In JSON files → JSON database is being used instead")
    print("\nRECOMMENDED FIX:")
    print("  1. If NOT in Supabase: Run setup_admin_account.py")
    print("  2. If in Supabase but not showing: Check Supabase credentials")
    print("  3. Quick fix: Run create_lawunmi_local.py to add to JSON")
    print("=" * 70)


if __name__ == "__main__":
    deep_diagnose()
