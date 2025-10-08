"""
Create admin account in the OLD system (works immediately!)
"""
import json
import hashlib
import os
from datetime import datetime, timedelta

# Admin credentials
ADMIN_EMAIL = "admin@t21services.co.uk"
ADMIN_PASSWORD = "admin123"  # Simple password (change after login!)
ADMIN_NAME = "T21 Administrator"

print("=" * 60)
print("CREATING ADMIN ACCOUNT")
print("=" * 60)
print()

# Create admin in OLD database format
user_id = hashlib.md5(ADMIN_EMAIL.encode()).hexdigest()[:12]

# Create license (super admin style)
from datetime import datetime, timedelta

license_data = {
    "user_id": user_id,
    "email": ADMIN_EMAIL,
    "role": "admin",  # Use 'admin' role
    "start_date": datetime.now().isoformat(),
    "expiry_date": (datetime.now() + timedelta(days=3650)).isoformat(),  # 10 years
    "usage": {
        "ai_questions_today": 0,
        "quizzes_today": 0,
        "validations_today": 0,
        "last_reset_date": datetime.now().date().isoformat(),
        "certification_attempts": 0,
        "total_logins": 0,
        "last_login": None
    }
}

# Create user record
user_data = {
    "user_id": user_id,
    "email": ADMIN_EMAIL,
    "password_hash": hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest(),
    "full_name": ADMIN_NAME,
    "license": license_data,
    "license_key": "ADMIN-SUPER-USER-KEY",
    "created_at": datetime.now().isoformat(),
    "last_login": None
}

# Load existing users or create new
users = {}
if os.path.exists("users_database.json"):
    with open("users_database.json", 'r') as f:
        users = json.load(f)

# Add admin
users[ADMIN_EMAIL] = user_data

# Save
with open("users_database.json", 'w') as f:
    json.dump(users, f, indent=2)

print("✅ ADMIN ACCOUNT CREATED!")
print()
print("=" * 60)
print("YOUR SIMPLE LOGIN:")
print("=" * 60)
print(f"Email:    {ADMIN_EMAIL}")
print(f"Password: {ADMIN_PASSWORD}")
print()
print("⚠️  THIS IS A SIMPLE PASSWORD!")
print("   Change it after first login!")
print()
print("=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Refresh your browser (F5)")
print("2. Login with the credentials above")
print("3. You'll have admin access!")
print()
print("=" * 60)
print("✅ Done! Try logging in now!")
print("=" * 60)
