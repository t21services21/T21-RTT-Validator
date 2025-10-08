"""
T21 CUSTOM EXPIRY DATE SETTER
Set specific expiry date/time for any user
"""

import json
from datetime import datetime
from admin_management import load_users_db, save_users_db

print("=" * 60)
print("T21 CUSTOM EXPIRY DATE SETTER")
print("=" * 60)
print()

# Load users
users = load_users_db()

if not users:
    print("❌ No users found. Please create admin account first.")
    print("Run: python setup_admin.py")
    exit()

print("Available users:")
print("-" * 60)
for idx, email in enumerate(users.keys(), 1):
    user = users[email]
    current_expiry = datetime.fromisoformat(user.to_dict()["expiry_date"])
    print(f"{idx}. {email}")
    print(f"   Role: {user.role}")
    print(f"   Current Expiry: {current_expiry.strftime('%d/%m/%Y %H:%M:%S')}")
    print()

# Get user email
user_email = input("Enter user email to set expiry for: ").strip()

if user_email not in users:
    print(f"❌ User not found: {user_email}")
    exit()

user = users[user_email]

print()
print(f"Setting expiry for: {user_email}")
print(f"Current expiry: {user.expiry_date.strftime('%d/%m/%Y %H:%M:%S')}")
print()

# Get custom expiry date
print("Enter new expiry date/time:")
print("Format: DD/MM/YYYY HH:MM")
print("Example: 31/12/2025 23:59")
print()

expiry_input = input("New expiry (DD/MM/YYYY HH:MM): ").strip()

try:
    # Parse the date
    new_expiry = datetime.strptime(expiry_input, "%d/%m/%Y %H:%M")
    
    # Update user expiry
    user.expiry_date = new_expiry
    
    # Add note
    user.add_note(f"Custom expiry date set to {new_expiry.strftime('%d/%m/%Y %H:%M:%S')} by admin")
    
    # Save
    save_users_db(users)
    
    print()
    print("=" * 60)
    print("✅ EXPIRY DATE UPDATED!")
    print("=" * 60)
    print(f"User: {user_email}")
    print(f"New Expiry: {new_expiry.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Calculate days remaining
    days_remaining = (new_expiry - datetime.now()).days
    print(f"Days Remaining: {days_remaining}")
    print()
    
    if days_remaining < 0:
        print("⚠️  WARNING: This date is in the past!")
        print("User account is now EXPIRED")
    elif days_remaining < 7:
        print("⚠️  WARNING: Less than 7 days remaining!")
    
    print()
    print("User will be able to access platform until:")
    print(f"  {new_expiry.strftime('%A, %d %B %Y at %H:%M:%S')}")
    print()
    print("=" * 60)

except ValueError as e:
    print(f"❌ Invalid date format: {e}")
    print("Please use format: DD/MM/YYYY HH:MM")
    print("Example: 31/12/2025 23:59")
