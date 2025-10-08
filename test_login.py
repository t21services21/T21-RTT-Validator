"""
Test admin login - Debug script
"""
import json
import hashlib

print("=" * 60)
print("TESTING ADMIN LOGIN")
print("=" * 60)
print()

# Test credentials
email = "admin@t21services.co.uk"
password = "admin123"

print(f"Testing login for: {email}")
print(f"Password: {password}")
print()

# Hash the password
password_hash = hashlib.sha256(password.encode()).hexdigest()
print(f"Password hash: {password_hash}")
print()

# Check users_advanced.json
print("Checking users_advanced.json...")
try:
    with open("users_advanced.json", 'r') as f:
        users_advanced = json.load(f)
    
    if email in users_advanced:
        print(f"[OK] Found in users_advanced.json")
        stored_hash = users_advanced[email].get("password_hash")
        print(f"Stored hash:   {stored_hash}")
        print(f"Computed hash: {password_hash}")
        
        if stored_hash == password_hash:
            print("[OK] PASSWORD MATCH!")
        else:
            print("[FAIL] PASSWORD MISMATCH!")
    else:
        print(f"[FAIL] Email not found in users_advanced.json")
except Exception as e:
    print(f"[ERROR] Error reading users_advanced.json: {e}")

print()

# Check users_database.json
print("Checking users_database.json...")
try:
    with open("users_database.json", 'r') as f:
        users_database = json.load(f)
    
    if email in users_database:
        print(f"[OK] Found in users_database.json")
        stored_hash = users_database[email].get("password_hash")
        print(f"Stored hash:   {stored_hash}")
        print(f"Computed hash: {password_hash}")
        
        if stored_hash == password_hash:
            print("[OK] PASSWORD MATCH!")
        else:
            print("[FAIL] PASSWORD MISMATCH!")
    else:
        print(f"[FAIL] Email not found in users_database.json")
except Exception as e:
    print(f"[ERROR] Error reading users_database.json: {e}")

print()
print("=" * 60)
print("CONCLUSION:")
print("=" * 60)

if stored_hash == password_hash:
    print("[OK] LOGIN SHOULD WORK!")
    print()
    print("If it's still not working in the app:")
    print("1. Make sure Streamlit is restarted")
    print("2. Clear browser cache (Ctrl+Shift+Delete)")
    print("3. Try in incognito/private window")
else:
    print("[FAIL] PASSWORD HASH DOESN'T MATCH")
    print()
    print("The database needs to be updated!")

print("=" * 60)
