"""
Check Supabase directly - no filters, no processing
"""

from supabase_database import supabase

print("=" * 70)
print("DIRECT SUPABASE QUERY - NO FILTERS")
print("=" * 70)

try:
    # Get ALL users from Supabase - no filters
    result = supabase.table('users').select('*').execute()
    
    if result.data:
        print(f"\nTotal users in Supabase: {len(result.data)}")
        print("\nAll users:")
        print("-" * 70)
        
        for user in result.data:
            email = user.get('email', 'N/A')
            name = user.get('full_name', 'N/A')
            role = user.get('role', 'N/A')
            user_type = user.get('user_type', 'NOT SET')
            status = user.get('status', 'N/A')
            
            print(f"\n📧 {email}")
            print(f"   Name: {name}")
            print(f"   Role: {role}")
            print(f"   User Type: {user_type}")
            print(f"   Status: {status}")
        
        print("\n" + "=" * 70)
        
        # Check specific users
        print("\nChecking specific users:")
        print("-" * 70)
        
        check_emails = [
            'lawunmilatinwo@outlook.com',
            'training@t21services.co.uk'
        ]
        
        for email in check_emails:
            found = any(u['email'] == email for u in result.data)
            if found:
                user = next(u for u in result.data if u['email'] == email)
                print(f"\n✅ {email}")
                print(f"   Role: {user.get('role')}")
                print(f"   User Type: {user.get('user_type', 'NOT SET')}")
                print(f"   Status: {user.get('status')}")
            else:
                print(f"\n❌ {email} - NOT IN DATABASE")
    
    else:
        print("\n❌ No users found in Supabase!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
