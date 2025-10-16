"""
SHOW ALL USERS - NO FILTERS
Shows every user in every database to find missing ones
"""

def show_all_users():
    """Show all users from all sources"""
    
    print("=" * 70)
    print("SHOWING ALL USERS FROM ALL DATABASES")
    print("=" * 70)
    
    all_found = []
    
    # ========================================
    # SOURCE 1: SUPABASE
    # ========================================
    print("\n1️⃣ SUPABASE DATABASE")
    print("-" * 70)
    try:
        from supabase_database import supabase
        result = supabase.table('users').select('*').execute()
        
        if result.data:
            print(f"Total: {len(result.data)} users\n")
            for user in result.data:
                email = user.get('email')
                name = user.get('full_name', 'Unknown')
                role = user.get('role', 'Unknown')
                user_type = user.get('user_type', 'Not Set')
                status = user.get('status', 'Unknown')
                
                print(f"  📧 {email}")
                print(f"     Name: {name}")
                print(f"     Role: {role}")
                print(f"     Type: {user_type}")
                print(f"     Status: {status}")
                print()
                
                all_found.append({
                    'source': 'Supabase',
                    'email': email,
                    'name': name,
                    'role': role,
                    'type': user_type
                })
        else:
            print("NO USERS IN SUPABASE!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ========================================
    # SOURCE 2: users_advanced.json
    # ========================================
    print("\n2️⃣ LOCAL JSON (users_advanced.json)")
    print("-" * 70)
    try:
        import json
        import os
        
        if os.path.exists('users_advanced.json'):
            with open('users_advanced.json', 'r') as f:
                users = json.load(f)
            
            print(f"Total: {len(users)} users\n")
            for email, user in users.items():
                name = user.get('full_name', 'Unknown')
                role = user.get('role', 'Unknown')
                
                # Check if already found
                already_found = any(u['email'] == email for u in all_found)
                marker = "🔄 (Duplicate)" if already_found else "✅ (Unique)"
                
                print(f"  {marker} {email}")
                print(f"     Name: {name}")
                print(f"     Role: {role}")
                print()
                
                if not already_found:
                    all_found.append({
                        'source': 'users_advanced.json',
                        'email': email,
                        'name': name,
                        'role': role
                    })
        else:
            print("FILE DOESN'T EXIST!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ========================================
    # SOURCE 3: get_all_users() function
    # ========================================
    print("\n3️⃣ get_all_users() FUNCTION (What Admin Panel uses)")
    print("-" * 70)
    try:
        from admin_management import get_all_users
        
        admin_users = get_all_users()
        print(f"Total: {len(admin_users)} users returned\n")
        
        for user in admin_users:
            email = user.get('email')
            name = user.get('full_name', 'Unknown')
            role = user.get('role', 'Unknown')
            
            print(f"  ✅ {email}")
            print(f"     Name: {name}")
            print(f"     Role: {role}")
            print()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # ========================================
    # ANALYSIS
    # ========================================
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    
    print(f"\nTotal unique users across all databases: {len(all_found)}")
    print("\nAll emails found:")
    for user in all_found:
        print(f"  - {user['email']} ({user['source']})")
    
    # Check specific users
    print("\n" + "=" * 70)
    print("CHECKING SPECIFIC USERS")
    print("=" * 70)
    
    check_emails = [
        "lawunmilatinwo@outlook.com",
        "training@t21services.co.uk"
    ]
    
    for check_email in check_emails:
        print(f"\n🔍 {check_email}:")
        found_in = [u for u in all_found if u['email'] == check_email]
        
        if found_in:
            print(f"  ✅ FOUND in: {', '.join([u['source'] for u in found_in])}")
            for u in found_in:
                print(f"     Name: {u.get('name')}")
                print(f"     Role: {u.get('role')}")
        else:
            print(f"  ❌ NOT FOUND in any database!")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    show_all_users()
