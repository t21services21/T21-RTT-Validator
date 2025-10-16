"""
Fix passwords using SHA256 (what the app uses)
"""

import hashlib
from supabase_database import supabase

# Users to fix
users = [
    {'email': 'lawunmilatinwo@outlook.com', 'password': 'Admin2025!'},
    {'email': 'training@t21services.co.uk', 'password': 'Training2025!'}
]

print("=" * 70)
print("SETTING PASSWORDS (SHA256)")
print("=" * 70)

for user in users:
    email = user['email']
    password = user['password']
    
    # Create SHA256 hash (what the app uses!)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    print(f"\n📧 {email}")
    print(f"   Password: {password}")
    print(f"   Hash (SHA256): {password_hash[:50]}...")
    
    try:
        # Update in Supabase
        supabase.table('users').update({
            'password_hash': password_hash
        }).eq('email', email).execute()
        
        print(f"   ✅ Password set!")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ DONE - Users can now login!")
print("=" * 70)
print("\nLogin credentials:")
for user in users:
    print(f"\n📧 {user['email']}")
    print(f"🔑 {user['password']}")
print("\n" + "=" * 70)
