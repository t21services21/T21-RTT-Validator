"""
T21 STUDENT AUTHENTICATION SYSTEM
Simple authentication for student access

Features:
- Student login/registration
- License activation
- Session management
- Password hashing
"""

import hashlib
import json
import os
from datetime import datetime
from access_control import UserLicense, generate_license_key

# ============================================
# USER DATABASE (Simple JSON storage)
# ============================================

USERS_FILE = "users_database.json"


def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    """Save users to JSON file with date serialization"""
    from datetime import date, datetime
    
    def convert_dates(obj):
        """Convert date/datetime objects to strings"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: convert_dates(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_dates(item) for item in obj]
        return obj
    
    # Convert all dates to strings
    users_serializable = convert_dates(users)
    
    with open(USERS_FILE, 'w') as f:
        json.dump(users_serializable, f, indent=2)


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================
# AUTHENTICATION FUNCTIONS
# ============================================

def register_student(email, password, full_name, role="trial", license_key=None):
    """
    Register new student
    Returns: (success: bool, message: str, user_license: UserLicense or None)
    """
    users = load_users()
    
    # Check if email already exists
    if email in users:
        return False, "Email already registered", None
    
    # Create user
    user_id = hashlib.md5(email.encode()).hexdigest()[:12]
    
    # Create license
    if license_key:
        # Validate and use provided license key
        # (In production, you'd validate against your license database)
        user_license = UserLicense(user_id, email, role="basic")  # Assume basic for now
    else:
        # Create trial license
        user_license = UserLicense(user_id, email, role=role)
    
    # Generate license key
    if not license_key:
        license_key = generate_license_key(email, role, user_license.days_remaining())
    
    # Store user
    users[email] = {
        "user_id": user_id,
        "email": email,
        "password_hash": hash_password(password),
        "full_name": full_name,
        "license": user_license.to_dict(),
        "license_key": license_key,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    save_users(users)
    
    return True, f"Registration successful! Trial license activated ({user_license.days_remaining()} days)", user_license


def login_student(email, password):
    """
    Login student
    Returns: (success: bool, message: str, user_license: UserLicense or None)
    """
    users = load_users()
    
    # Check if user exists
    if email not in users:
        return False, "Email not found", None
    
    user = users[email]
    
    # Check password
    if hash_password(password) != user["password_hash"]:
        return False, "Incorrect password", None
    
    # Load license
    user_license = UserLicense.from_dict(user["license"])
    
    # Check if active
    if not user_license.is_active():
        return False, f"License expired on {user_license.expiry_date.strftime('%d/%m/%Y')}. Please renew.", user_license
    
    # Update last login
    user["last_login"] = datetime.now().isoformat()
    user_license.usage["total_logins"] += 1
    user_license.usage["last_login"] = datetime.now().isoformat()
    user["license"] = user_license.to_dict()
    
    save_users(users)
    
    return True, "Login successful!", user_license


def activate_license(email, license_key):
    """
    Activate license key for existing user
    Returns: (success: bool, message: str)
    """
    users = load_users()
    
    if email not in users:
        return False, "Email not found"
    
    # In production, validate license key against your database
    # For now, just update the role
    
    user = users[email]
    user_license = UserLicense.from_dict(user["license"])
    
    # Upgrade to Professional (example)
    user_license.upgrade_role("professional")
    
    user["license"] = user_license.to_dict()
    user["license_key"] = license_key
    
    save_users(users)
    
    return True, f"License activated! Upgraded to {user_license.role.title()}. Expires: {user_license.expiry_date.strftime('%d/%m/%Y')}"


def upgrade_student(email, new_role, extend_days=None):
    """
    Upgrade student to new role
    Returns: (success: bool, message: str)
    """
    users = load_users()
    
    if email not in users:
        return False, "Email not found"
    
    user = users[email]
    user_license = UserLicense.from_dict(user["license"])
    
    old_role = user_license.role
    user_license.upgrade_role(new_role, extend_expiry=True)
    
    if extend_days:
        user_license.extend_license(extend_days)
    
    user["license"] = user_license.to_dict()
    
    save_users(users)
    
    return True, f"Upgraded from {old_role.title()} to {new_role.title()}! Expires: {user_license.expiry_date.strftime('%d/%m/%Y')}"


def get_student_info(email):
    """Get student information"""
    users = load_users()
    
    if email not in users:
        return None
    
    user = users[email]
    user_license = UserLicense.from_dict(user["license"])
    
    return {
        "full_name": user["full_name"],
        "email": user["email"],
        "license": user_license,
        "license_key": user["license_key"],
        "created_at": user["created_at"],
        "last_login": user.get("last_login", "Never")
    }


# ============================================
# ADMIN FUNCTIONS
# ============================================

def list_all_students():
    """List all students (admin only)"""
    users = load_users()
    
    students = []
    for email, user in users.items():
        license = UserLicense.from_dict(user["license"])
        students.append({
            "email": email,
            "full_name": user["full_name"],
            "role": license.role,
            "status": "Active" if license.is_active() else "Expired",
            "expiry": license.expiry_date.strftime("%d/%m/%Y"),
            "days_remaining": license.days_remaining()
        })
    
    return students


def extend_student_license(email, days):
    """Extend student license (admin only)"""
    users = load_users()
    
    if email not in users:
        return False, "Email not found"
    
    user = users[email]
    license = UserLicense.from_dict(user["license"])
    license.extend_license(days)
    
    user["license"] = license.to_dict()
    save_users(users)
    
    return True, f"Extended license by {days} days. New expiry: {license.expiry_date.strftime('%d/%m/%Y')}"


def delete_student(email):
    """Delete student account (admin only)"""
    users = load_users()
    
    if email in users:
        del users[email]
        save_users(users)
        return True, "Student account deleted"
    
    return False, "Email not found"
