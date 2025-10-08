"""
T21 ADMIN ACCOUNT SETUP
Run this ONCE to create your admin account
"""

import json
from datetime import datetime, timedelta
from advanced_access_control import UserAccount
import hashlib

print("=" * 60)
print("T21 ADMIN ACCOUNT SETUP")
print("=" * 60)
print()

# YOUR ADMIN CREDENTIALS
ADMIN_EMAIL = "admin@t21services.co.uk"
ADMIN_PASSWORD = "Admin123!"  # CHANGE THIS AFTER FIRST LOGIN!
ADMIN_NAME = "T21 Administrator"

print("Creating Super Admin account...")
print()

# Create super admin account
super_admin = UserAccount(
    user_id="admin001",
    email=ADMIN_EMAIL,
    role="super_admin",
    full_name=ADMIN_NAME,
    created_by="system"
)

# Prepare user data
users_db = {
    ADMIN_EMAIL: super_admin.to_dict()
}

# Add password hash
users_db[ADMIN_EMAIL]["password_hash"] = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()

# Save to database
with open("users_advanced.json", "w") as f:
    json.dump(users_db, f, indent=2)

print("✅ SUPER ADMIN ACCOUNT CREATED!")
print()
print("=" * 60)
print("YOUR LOGIN DETAILS:")
print("=" * 60)
print(f"Email:    {ADMIN_EMAIL}")
print(f"Password: {ADMIN_PASSWORD}")
print()
print("⚠️  IMPORTANT: Change your password after first login!")
print()
print(f"Role: Super Administrator (Full Access)")
print(f"Created: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"Expires: Never")
print()
print("=" * 60)
print("WHAT YOU CAN DO:")
print("=" * 60)
print("✅ Create & manage all users")
print("✅ Suspend/Unsuspend accounts")
print("✅ Terminate accounts (permanent)")
print("✅ Delete users (complete removal)")
print("✅ Extend licenses")
print("✅ Change user roles")
print("✅ Grant/Revoke permissions")
print("✅ View revenue & analytics")
print("✅ Access audit logs")
print("✅ Manage other admins")
print()
print("=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Start the app:")
print("   py -3.12 -m streamlit run app.py")
print()
print(f"2. Login with:")
print(f"   Email: {ADMIN_EMAIL}")
print(f"   Password: {ADMIN_PASSWORD}")
print()
print("3. Go to '🔧 Admin Panel' in sidebar")
print()
print("4. Create your first student account!")
print()
print("=" * 60)
print("Setup complete! 🎉")
print("=" * 60)
