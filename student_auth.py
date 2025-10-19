"""
T21 STUDENT AUTHENTICATION SYSTEM
Simple authentication for student access

Features:
- Student login/registration
- License activation
- Session management
- Password hashing
- Email notifications
- Password reset
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from access_control import UserLicense, generate_license_key
from email_service import send_welcome_email, generate_reset_code, send_password_reset_email

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
    
    # Send welcome email
    try:
        send_welcome_email(email, full_name, trial_hours=48)
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
        # Continue even if email fails
    
    return True, f"Registration successful! 48-hour trial activated. Check your email!", user_license


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


# ============================================
# PASSWORD RESET FUNCTIONS
# ============================================

# In-memory storage for reset codes (in production, use Redis or database)
RESET_CODES = {}

def request_password_reset(email):
    """
    Request password reset - generates code and sends email
    Works with both Supabase and local JSON storage
    Returns: (success: bool, message: str)
    """
    # Check Supabase first
    user_found = False
    try:
        from supabase_database import get_user_by_email
        supabase_user = get_user_by_email(email)
        if supabase_user:
            user_found = True
    except:
        pass
    
    # Check local JSON if not in Supabase
    if not user_found:
        users = load_users()
        if email in users:
            user_found = True
    
    if not user_found:
        # For security, don't reveal if email exists
        return True, "If this email exists, a reset code has been sent."
    
    # Generate 6-digit code
    reset_code = generate_reset_code()
    
    # Store code with expiry (15 minutes)
    RESET_CODES[email] = {
        "code": reset_code,
        "expiry": datetime.now() + timedelta(minutes=15)
    }
    
    # Send email
    try:
        send_password_reset_email(email, reset_code)
        return True, "Reset code sent to your email. Check your inbox!"
    except Exception as e:
        print(f"Failed to send reset email: {e}")
        return False, "Failed to send reset email. Please try again."


def verify_reset_code(email, code):
    """
    Verify reset code
    Returns: (valid: bool, message: str)
    """
    if email not in RESET_CODES:
        return False, "Invalid or expired code"
    
    stored_data = RESET_CODES[email]
    
    # Check expiry
    if datetime.now() > stored_data["expiry"]:
        del RESET_CODES[email]
        return False, "Code expired. Please request a new one."
    
    # Check code
    if stored_data["code"] != code:
        return False, "Invalid code"
    
    return True, "Code verified!"


def reset_password(email, code, new_password):
    """
    Reset password with verified code
    Works with both Supabase and local JSON storage
    Returns: (success: bool, message: str)
    """
    # Verify code first
    valid, message = verify_reset_code(email, code)
    if not valid:
        return False, message
    
    # Try Supabase first
    password_updated = False
    try:
        from supabase_database import supabase, SUPABASE_AVAILABLE
        if SUPABASE_AVAILABLE and supabase:
            supabase_user = supabase.table('users').select('*').eq('email', email).execute()
            if supabase_user.data:
                # Update password in Supabase
                new_hash = hash_password(new_password)
                supabase.table('users').update({'password_hash': new_hash}).eq('email', email).execute()
                password_updated = True
    except Exception as e:
        print(f"Supabase password update failed: {e}")
    
    # Try local JSON if Supabase failed
    if not password_updated:
        users = load_users()
        
        if email not in users:
            return False, "Email not found"
        
        users[email]["password_hash"] = hash_password(new_password)
        save_users(users)
        password_updated = True
    
    # Delete used code
    if email in RESET_CODES:
        del RESET_CODES[email]
    
    if password_updated:
        return True, "Password reset successful! You can now login with your new password."
    else:
        return False, "Failed to update password. Please try again or contact support."


def delete_student(email):
    """Delete student account (admin only)"""
    users = load_users()
    
    if email in users:
        del users[email]
        save_users(users)
        return True, "Student account deleted"
    
    return False, "Email not found"
