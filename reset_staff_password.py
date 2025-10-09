"""
Quick script to reset staff password
"""
import json
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users database
with open('users_database.json', 'r') as f:
    users_db = json.load(f)

# Load advanced users database
with open('users_advanced.json', 'r') as f:
    users_advanced = json.load(f)

# Set new password
new_password = "staff123"
new_hash = hash_password(new_password)

print(f"New password: {new_password}")
print(f"New hash: {new_hash}")

# Update both databases
if "staff@t21services.co.uk" in users_db:
    users_db["staff@t21services.co.uk"]["password_hash"] = new_hash
    print("Updated users_database.json")

if "staff@t21services.co.uk" in users_advanced:
    users_advanced["staff@t21services.co.uk"]["password_hash"] = new_hash
    print("Updated users_advanced.json")

if "admin@t21services.co.uk" in users_db:
    admin_hash = hash_password("admin123")
    users_db["admin@t21services.co.uk"]["password_hash"] = admin_hash
    print("Updated admin password too")

if "admin@t21services.co.uk" in users_advanced:
    admin_hash = hash_password("admin123")
    users_advanced["admin@t21services.co.uk"]["password_hash"] = admin_hash
    print("Updated admin password in advanced DB")

# Save both databases
with open('users_database.json', 'w') as f:
    json.dump(users_db, f, indent=2)
    print("Saved users_database.json")

with open('users_advanced.json', 'w') as f:
    json.dump(users_advanced, f, indent=2)
    print("Saved users_advanced.json")

print("\n" + "="*60)
print("PASSWORD RESET COMPLETE!")
print("="*60)
print("\nNEW CREDENTIALS:")
print("-"*60)
print("STAFF:")
print("  Email:    staff@t21services.co.uk")
print("  Password: staff123")
print()
print("ADMIN:")
print("  Email:    admin@t21services.co.uk")
print("  Password: admin123")
print("-"*60)
print("\nTry logging in now with these credentials!")
