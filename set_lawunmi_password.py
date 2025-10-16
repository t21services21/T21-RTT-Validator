"""
Set real password for Lawunmi
"""

import bcrypt
from supabase_database import supabase

# Generate real password hash
password = 'Admin2025!'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print("=" * 70)
print("SETTING LAWUNMI'S PASSWORD")
print("=" * 70)

print(f"\nPassword: {password}")
print(f"Hash: {hashed}")

try:
    # Update password
    result = supabase.table('users').update({
        'password_hash': hashed
    }).eq('email', 'lawunmilatinwo@outlook.com').execute()
    
    print("\n✅ Password updated!")
    print("\nLawunmi can now login with:")
    print(f"   Email: lawunmilatinwo@outlook.com")
    print(f"   Password: {password}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
