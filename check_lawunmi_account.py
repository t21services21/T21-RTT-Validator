"""
CHECK IF LAWUNMI'S ACCOUNT EXISTS
Searches all databases (Supabase, JSON, local files)
"""

def check_lawunmi():
    """Check if Lawunmi's account exists in any database"""
    
    email = "lawunmilatinwo@outlook.com"
    
    print("=" * 60)
    print("CHECKING FOR LAWUNMI'S ACCOUNT")
    print("=" * 60)
    print(f"\nSearching for: {email}\n")
    
    found = False
    
    # CHECK 1: Supabase
    print("1️⃣ Checking Supabase Database...")
    try:
        from supabase_database import supabase
        result = supabase.table('users').select('*').eq('email', email).execute()
        
        if result.data:
            print("✅ FOUND in Supabase!")
            user = result.data[0]
            print(f"   Name: {user.get('full_name')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Status: {user.get('status')}")
            print(f"   Created: {user.get('created_at')}")
            found = True
        else:
            print("❌ NOT FOUND in Supabase")
    except Exception as e:
        print(f"⚠️  Supabase check failed: {e}")
    
    # CHECK 2: Local JSON (users_advanced.json)
    print("\n2️⃣ Checking Local JSON Database (users_advanced.json)...")
    try:
        import json
        import os
        
        if os.path.exists('users_advanced.json'):
            with open('users_advanced.json', 'r') as f:
                users = json.load(f)
            
            if email in users:
                print("✅ FOUND in users_advanced.json!")
                user = users[email]
                print(f"   Name: {user.get('full_name')}")
                print(f"   Role: {user.get('role')}")
                found = True
            else:
                print("❌ NOT FOUND in users_advanced.json")
        else:
            print("⚠️  users_advanced.json doesn't exist")
    except Exception as e:
        print(f"⚠️  JSON check failed: {e}")
    
    # CHECK 3: User License System
    print("\n3️⃣ Checking User License System...")
    try:
        from user_license_system import load_all_licenses
        
        licenses = load_all_licenses()
        
        for license in licenses:
            if license.email == email:
                print("✅ FOUND in User License System!")
                print(f"   Name: {license.full_name}")
                print(f"   Role: {license.role}")
                found = True
                break
        else:
            print("❌ NOT FOUND in User License System")
    except Exception as e:
        print(f"⚠️  License system check failed: {e}")
    
    # CHECK 4: What Admin Panel sees
    print("\n4️⃣ Checking what Admin Panel would see...")
    try:
        from admin_management import get_all_users
        
        all_users = get_all_users()
        
        lawunmi_in_list = [u for u in all_users if u['email'] == email]
        
        if lawunmi_in_list:
            print("✅ Admin Panel SHOULD SEE this account!")
            user = lawunmi_in_list[0]
            print(f"   Name: {user.get('full_name')}")
            print(f"   Role: {user.get('role_name')}")
        else:
            print("❌ Admin Panel CANNOT SEE this account!")
            print(f"   Total users Admin Panel sees: {len(all_users)}")
            print("\n   Emails Admin Panel can see:")
            for u in all_users[:10]:  # Show first 10
                print(f"   - {u['email']}")
    except Exception as e:
        print(f"⚠️  Admin Panel check failed: {e}")
    
    # SUMMARY
    print("\n" + "=" * 60)
    if found:
        print("✅ ACCOUNT EXISTS but Admin Panel can't see it!")
        print("\nPossible reasons:")
        print("1. Database connection issue in Admin Panel")
        print("2. Different database being queried")
        print("3. Cached data not refreshed")
        print("\nSolution: Create account in LOCAL database too")
    else:
        print("❌ ACCOUNT DOES NOT EXIST in ANY database!")
        print("\nSolution: Run setup_admin_account.py again")
    print("=" * 60)
    
    return found


if __name__ == "__main__":
    check_lawunmi()
