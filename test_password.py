"""
Test password hash - Run this to verify the correct password
"""
import hashlib

password = "Admin123!"
password_hash = hashlib.sha256(password.encode()).hexdigest()

print("=" * 60)
print("PASSWORD HASH TEST")
print("=" * 60)
print(f"Password: {password}")
print(f"Hash:     {password_hash}")
print("=" * 60)
print()
print("This hash should be in users_advanced.json")
print()

# Check if it matches
import json
with open("users_advanced.json", 'r') as f:
    users = json.load(f)
    
admin_user = users.get("admin@t21services.co.uk")
if admin_user:
    stored_hash = admin_user.get("password_hash")
    print(f"Stored hash:   {stored_hash}")
    print(f"Computed hash: {password_hash}")
    print()
    
    if stored_hash == password_hash:
        print("✅ MATCH! Password is correct!")
    else:
        print("❌ NO MATCH! Updating the file...")
        users["admin@t21services.co.uk"]["password_hash"] = password_hash
        with open("users_advanced.json", 'w') as f:
            json.dump(users, f, indent=2)
        print("✅ FIXED! Password hash updated!")
        print()
        print("Now restart your app and try logging in again!")
else:
    print("❌ Admin user not found in database!")

print("=" * 60)
