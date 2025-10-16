"""
CREATE LAWUNMI IN LOCAL DATABASE
So Admin Panel can see the account
"""

import json
import bcrypt
from datetime import datetime, timedelta
import os

def create_lawunmi_local():
    """Create Lawunmi's account in local JSON database"""
    
    email = "lawunmilatinwo@outlook.com"
    password = "Admin2025!"
    name = "Lawunmi Latinwo"
    role = "staff"  # Change to "admin" if they should have Admin Panel access
    
    print("=" * 60)
    print("CREATING LAWUNMI IN LOCAL DATABASE")
    print("=" * 60)
    print(f"\n📧 Email: {email}")
    print(f"👤 Name: {name}")
    print(f"🔑 Password: {password}")
    print(f"👔 Role: {role}")
    
    # Load existing database
    db_file = "users_advanced.json"
    
    if os.path.exists(db_file):
        with open(db_file, 'r') as f:
            users = json.load(f)
        print(f"\n✓ Loaded {len(users)} existing users from {db_file}")
    else:
        users = {}
        print(f"\n✓ Creating new {db_file}")
    
    # Check if already exists
    if email in users:
        print(f"\n⚠️  User already exists in local database!")
        print(f"   Current role: {users[email].get('role')}")
        update = input("Update? (y/n): ")
        if update.lower() != 'y':
            print("Cancelled")
            return
    
    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create user object
    users[email] = {
        'email': email,
        'password_hash': hashed_pw,
        'full_name': name,
        'role': role,
        'user_type': role,
        'status': 'active',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'trial_end_date': (datetime.now() + timedelta(days=365)).isoformat(),
        'total_logins': 0,
        'last_login': None,
        'custom_permissions': [],
        'notes': f'Created for testing - Full access except {"" if role == "admin" else "Admin Panel"}'
    }
    
    # Save
    with open(db_file, 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"\n✅ Account created in {db_file}!")
    print(f"\n📊 Total users now: {len(users)}")
    print(f"\n✅ Admin Panel should now see this account!")
    print(f"\n🔑 Login credentials:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Role: {role}")
    
    if role == 'staff':
        print(f"\n✅ Access: ALL modules EXCEPT Admin Panel")
    else:
        print(f"\n✅ Access: ALL modules INCLUDING Admin Panel")
    
    print("\n" + "=" * 60)
    print("DONE! Refresh Admin Panel to see the user.")
    print("=" * 60)


if __name__ == "__main__":
    create_lawunmi_local()
