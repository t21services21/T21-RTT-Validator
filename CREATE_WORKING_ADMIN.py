"""
CREATE WORKING ADMIN - NO EMOJI ISSUES
Creates admin in BOTH old and new systems
"""
import json
import hashlib
import os
from datetime import datetime, timedelta

print("=" * 60)
print("CREATING ADMIN ACCOUNTS IN BOTH SYSTEMS")
print("=" * 60)
print()

# Admin credentials
ADMIN_EMAIL = "admin@t21services.co.uk"
ADMIN_PASSWORD = "Admin123!"
ADMIN_NAME = "T21 Administrator"

print("Creating admin accounts...")
print()

# =============================================
# SYSTEM 1: OLD DATABASE (users_database.json)
# =============================================
print("1. Creating in OLD system (users_database.json)...")

user_id = hashlib.md5(ADMIN_EMAIL.encode()).hexdigest()[:12]

license_data = {
    "user_id": user_id,
    "email": ADMIN_EMAIL,
    "role": "admin",
    "start_date": datetime.now().isoformat(),
    "expiry_date": (datetime.now() + timedelta(days=3650)).isoformat(),
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

user_data_old = {
    "user_id": user_id,
    "email": ADMIN_EMAIL,
    "password_hash": hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest(),
    "full_name": ADMIN_NAME,
    "license": license_data,
    "license_key": "ADMIN-SUPER-USER-KEY",
    "created_at": datetime.now().isoformat(),
    "last_login": None
}

users_old = {}
if os.path.exists("users_database.json"):
    with open("users_database.json", 'r') as f:
        users_old = json.load(f)

users_old[ADMIN_EMAIL] = user_data_old

with open("users_database.json", 'w') as f:
    json.dump(users_old, f, indent=2)

print("   DONE - Old system updated!")
print()

# =============================================
# SYSTEM 2: NEW DATABASE (users_advanced.json)
# =============================================
print("2. Creating in NEW system (users_advanced.json)...")

user_data_new = {
    "user_id": user_id,
    "email": ADMIN_EMAIL,
    "password_hash": hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest(),
    "user_type": "admin",
    "role": "super_admin",
    "full_name": ADMIN_NAME,
    "organization": "T21 Services Limited",
    "created_by": "system",
    "created_at": datetime.now().isoformat(),
    "status": "active",
    "suspended_reason": None,
    "suspended_by": None,
    "suspended_at": None,
    "terminated_at": None,
    "expiry_date": (datetime.now() + timedelta(days=3650)).isoformat(),
    "usage": {
        "total_logins": 0,
        "last_login": None,
        "logins_today": 0,
        "last_login_date": None,
        "ai_questions_today": 0,
        "quizzes_today": 0,
        "validations_today": 0,
        "last_reset_date": datetime.now().date().isoformat()
    },
    "custom_permissions": {},
    "notes": [
        {
            "timestamp": datetime.now().isoformat(),
            "note": "Admin account created by system"
        }
    ]
}

users_new = {}
if os.path.exists("users_advanced.json"):
    with open("users_advanced.json", 'r') as f:
        users_new = json.load(f)

users_new[ADMIN_EMAIL] = user_data_new

with open("users_advanced.json", 'w') as f:
    json.dump(users_new, f, indent=2)

print("   DONE - New system updated!")
print()

# =============================================
# STAFF ACCOUNT TOO
# =============================================
STAFF_EMAIL = "staff@t21services.co.uk"
STAFF_PASSWORD = "Staff123!"
STAFF_NAME = "T21 Staff Member"

print("3. Creating STAFF account in both systems...")

staff_id = hashlib.md5(STAFF_EMAIL.encode()).hexdigest()[:12]

# Old system
staff_license = {
    "user_id": staff_id,
    "email": STAFF_EMAIL,
    "role": "admin",
    "start_date": datetime.now().isoformat(),
    "expiry_date": (datetime.now() + timedelta(days=3650)).isoformat(),
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

staff_old = {
    "user_id": staff_id,
    "email": STAFF_EMAIL,
    "password_hash": hashlib.sha256(STAFF_PASSWORD.encode()).hexdigest(),
    "full_name": STAFF_NAME,
    "license": staff_license,
    "license_key": "STAFF-USER-KEY",
    "created_at": datetime.now().isoformat(),
    "last_login": None
}

users_old[STAFF_EMAIL] = staff_old
with open("users_database.json", 'w') as f:
    json.dump(users_old, f, indent=2)

# New system
staff_new = {
    "user_id": staff_id,
    "email": STAFF_EMAIL,
    "password_hash": hashlib.sha256(STAFF_PASSWORD.encode()).hexdigest(),
    "user_type": "staff",
    "role": "staff",
    "full_name": STAFF_NAME,
    "organization": "T21 Services Limited",
    "created_by": "system",
    "created_at": datetime.now().isoformat(),
    "status": "active",
    "suspended_reason": None,
    "suspended_by": None,
    "suspended_at": None,
    "terminated_at": None,
    "expiry_date": (datetime.now() + timedelta(days=3650)).isoformat(),
    "usage": {
        "total_logins": 0,
        "last_login": None,
        "logins_today": 0,
        "last_login_date": None,
        "ai_questions_today": 0,
        "quizzes_today": 0,
        "validations_today": 0,
        "last_reset_date": datetime.now().date().isoformat()
    },
    "custom_permissions": {},
    "notes": [
        {
            "timestamp": datetime.now().isoformat(),
            "note": "Staff account created by system"
        }
    ]
}

users_new[STAFF_EMAIL] = staff_new
with open("users_advanced.json", 'w') as f:
    json.dump(users_new, f, indent=2)

print("   DONE - Staff account created!")
print()

print("=" * 60)
print("SUCCESS! ACCOUNTS CREATED IN BOTH SYSTEMS!")
print("=" * 60)
print()
print("ADMIN LOGIN:")
print("-" * 60)
print(f"Email:    {ADMIN_EMAIL}")
print(f"Password: {ADMIN_PASSWORD}")
print(f"Role:     Super Admin")
print()
print("STAFF LOGIN:")
print("-" * 60)
print(f"Email:    {STAFF_EMAIL}")
print(f"Password: {STAFF_PASSWORD}")
print(f"Role:     Staff")
print()
print("=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Refresh your browser (F5)")
print("2. Login with ADMIN or STAFF credentials")
print("3. Check 'Staff & Partners' portal checkbox")
print("4. Full admin access!")
print()
print("=" * 60)
print("DONE! Try logging in now!")
print("=" * 60)
