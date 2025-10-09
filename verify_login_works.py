"""
Verify login credentials work
"""
import json
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Test passwords
print("="*60)
print("TESTING LOGIN CREDENTIALS")
print("="*60)

# Load database
with open('users_advanced.json', 'r') as f:
    users = json.load(f)

# Test staff
staff_email = "staff@t21services.co.uk"
staff_password = "staff123"
staff_hash = hash_password(staff_password)

print(f"\nSTAFF LOGIN TEST:")
print(f"Email: {staff_email}")
print(f"Password: {staff_password}")
print(f"Generated hash: {staff_hash}")

if staff_email in users:
    stored_hash = users[staff_email].get("password_hash")
    print(f"Stored hash:    {stored_hash}")
    if stored_hash == staff_hash:
        print("STAFF PASSWORD MATCHES!")
    else:
        print("STAFF PASSWORD DOES NOT MATCH!")
        print("\nDEBUG INFO:")
        print(f"Role: {users[staff_email].get('role')}")
        print(f"User Type: {users[staff_email].get('user_type')}")
else:
    print("STAFF EMAIL NOT FOUND IN DATABASE!")

# Test admin
admin_email = "admin@t21services.co.uk"
admin_password = "admin123"
admin_hash = hash_password(admin_password)

print(f"\n{'='*60}")
print(f"ADMIN LOGIN TEST:")
print(f"Email: {admin_email}")
print(f"Password: {admin_password}")
print(f"Generated hash: {admin_hash}")

if admin_email in users:
    stored_hash = users[admin_email].get("password_hash")
    print(f"Stored hash:    {stored_hash}")
    if stored_hash == admin_hash:
        print("ADMIN PASSWORD MATCHES!")
    else:
        print("ADMIN PASSWORD DOES NOT MATCH!")
        print("\nDEBUG INFO:")
        print(f"Role: {users[admin_email].get('role')}")
        print(f"User Type: {users[admin_email].get('user_type')}")
else:
    print("ADMIN EMAIL NOT FOUND IN DATABASE!")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
