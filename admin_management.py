"""
T21 ADMIN MANAGEMENT SYSTEM
Complete admin panel for managing students, staff, and permissions

Features:
- User management (create, suspend, terminate, delete)
- Permission management (grant, revoke)
- License management (extend, upgrade, downgrade)
- Audit logs
- Revenue tracking
- Analytics
"""

import json
import os
from datetime import datetime
from advanced_access_control import UserAccount, USER_TYPES, ACCOUNT_STATUS
import hashlib

USERS_DB_FILE = "users_advanced.json"
AUDIT_LOG_FILE = "audit_log.json"


# ============================================
# DATABASE OPERATIONS
# ============================================

def load_users_db():
    """Load users database"""
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'r') as f:
            data = json.load(f)
            users = {}
            for email, user_data in data.items():
                users[email] = UserAccount.from_dict(user_data)
            return users
    return {}


def save_users_db(users):
    """Save users database"""
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
    
    data = {}
    for email, user in users.items():
        user_dict = user.to_dict()
        data[email] = convert_dates(user_dict)
    
    with open(USERS_DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def log_audit(action, performed_by, target_user, details=""):
    """Log admin action to audit trail"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "performed_by": performed_by,
        "target_user": target_user,
        "details": details
    }
    
    # Load existing logs
    logs = []
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, 'r') as f:
            logs = json.load(f)
    
    # Add new log
    logs.append(log_entry)
    
    # Save logs (keep last 1000 entries)
    with open(AUDIT_LOG_FILE, 'w') as f:
        json.dump(logs[-1000:], f, indent=2)


def hash_password(password):
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================
# USER MANAGEMENT
# ============================================

def create_user(email, password, full_name, role, created_by_email, custom_expiry=None):
    """Create new user account with optional custom expiry date"""
    users = load_users_db()
    
    # Check if exists
    if email in users:
        return False, "Email already exists"
    
    # Validate role
    if role not in USER_TYPES:
        return False, f"Invalid role: {role}"
    
    # Check permissions of creator
    creator = users.get(created_by_email)
    
    # If creator not in advanced DB, check old DB (for backwards compatibility)
    if not creator:
        import json
        import os
        if os.path.exists("users_database.json"):
            with open("users_database.json", 'r') as f:
                old_users = json.load(f)
            if created_by_email in old_users:
                old_user_role = old_users[created_by_email].get("license", {}).get("role")
                if old_user_role == "admin":
                    # Old admin has all permissions, skip further checks
                    creator = "old_admin"
    
    if not creator:
        return False, "Creator account not found"
    
    # Check if creator has permission to create this type of user
    # Skip permission check for old admins (they have full access)
    if creator != "old_admin":
        target_type = USER_TYPES[role]["type"]
        
        if target_type == "student":
            if not creator.has_permission("student_management"):
                return False, "No permission to create students"
        elif target_type == "staff":
            if not creator.has_permission("staff_management"):
                return False, "No permission to create staff"
        elif target_type in ["admin", "super_admin"]:
            if not creator.has_permission("admin_management"):
                return False, "No permission to create admins"
    
    # Create user
    user_id = hashlib.md5(email.encode()).hexdigest()[:12]
    user = UserAccount(user_id, email, role, full_name, created_by=created_by_email)
    
    # Set custom expiry if provided
    if custom_expiry:
        user.expiry_date = custom_expiry
        user.add_note(f"Custom expiry set to {custom_expiry.strftime('%d/%m/%Y %H:%M')} by {created_by_email}")
    
    # Store with password
    users[email] = user
    
    # Store password separately (in real app, use separate secure storage)
    user_dict = user.to_dict()
    user_dict["password_hash"] = hash_password(password)
    
    users[email] = UserAccount.from_dict(user_dict)
    
    # Re-apply custom expiry after from_dict (to ensure it's saved)
    if custom_expiry:
        users[email].expiry_date = custom_expiry
    
    save_users_db(users)
    
    expiry_info = f" (Expires: {custom_expiry.strftime('%d/%m/%Y %H:%M')})" if custom_expiry else ""
    log_audit("CREATE_USER", created_by_email, email, f"Role: {role}{expiry_info}")
    
    return True, f"User created successfully: {email}{expiry_info}"


def suspend_user(target_email, reason, suspended_by_email):
    """Suspend user account"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    target_user = users[target_email]
    suspender = users.get(suspended_by_email)
    
    if not suspender:
        return False, "Suspender account not found"
    
    # Check permissions
    if not suspender.has_permission("student_management") and not suspender.has_permission("staff_management"):
        return False, "No permission to suspend users"
    
    # Cannot suspend yourself
    if target_email == suspended_by_email:
        return False, "Cannot suspend your own account"
    
    # Suspend user
    target_user.suspend(reason, suspended_by_email)
    
    save_users_db(users)
    log_audit("SUSPEND_USER", suspended_by_email, target_email, f"Reason: {reason}")
    
    return True, f"User suspended: {target_email}"


def unsuspend_user(target_email, unsuspended_by_email):
    """Unsuspend user account"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    target_user = users[target_email]
    unsuspender = users.get(unsuspended_by_email)
    
    if not unsuspender:
        return False, "Unsuspender account not found"
    
    # Check permissions
    if not unsuspender.has_permission("student_management") and not unsuspender.has_permission("staff_management"):
        return False, "No permission to unsuspend users"
    
    # Unsuspend user
    target_user.unsuspend(unsuspended_by_email)
    
    save_users_db(users)
    log_audit("UNSUSPEND_USER", unsuspended_by_email, target_email, "Account reactivated")
    
    return True, f"User unsuspended: {target_email}"


def terminate_user(target_email, reason, terminated_by_email):
    """Permanently terminate user account"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    target_user = users[target_email]
    terminator = users.get(terminated_by_email)
    
    if not terminator:
        return False, "Terminator account not found"
    
    # Check permissions (only super admin can terminate)
    if not terminator.has_permission("terminate_accounts"):
        return False, "Only Super Admin can terminate accounts"
    
    # Cannot terminate yourself
    if target_email == terminated_by_email:
        return False, "Cannot terminate your own account"
    
    # Terminate user
    target_user.terminate(reason, terminated_by_email)
    
    save_users_db(users)
    log_audit("TERMINATE_USER", terminated_by_email, target_email, f"PERMANENT TERMINATION: {reason}")
    
    return True, f"User TERMINATED: {target_email}"


def delete_user(target_email, deleted_by_email):
    """Delete user account (complete removal)"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    deleter = users.get(deleted_by_email)
    
    if not deleter:
        return False, "Deleter account not found"
    
    # Check permissions
    if not deleter.has_permission("database_access"):
        return False, "Only Super Admin can delete accounts"
    
    # Cannot delete yourself
    if target_email == deleted_by_email:
        return False, "Cannot delete your own account"
    
    # Delete user
    del users[target_email]
    
    save_users_db(users)
    log_audit("DELETE_USER", deleted_by_email, target_email, "Account permanently deleted from database")
    
    return True, f"User deleted: {target_email}"


# ============================================
# PERMISSION MANAGEMENT
# ============================================

def grant_custom_permission(target_email, feature_name, granted_by_email):
    """Grant custom permission to user"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    target_user = users[target_email]
    granter = users.get(granted_by_email)
    
    if not granter:
        return False, "Granter account not found"
    
    # Check permissions
    if not granter.has_permission("license_management"):
        return False, "No permission to grant custom permissions"
    
    # Grant permission
    target_user.grant_permission(feature_name, granted_by_email)
    
    save_users_db(users)
    log_audit("GRANT_PERMISSION", granted_by_email, target_email, f"Feature: {feature_name}")
    
    return True, f"Permission granted: {feature_name} to {target_email}"


def revoke_custom_permission(target_email, feature_name, revoked_by_email):
    """Revoke custom permission from user"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    target_user = users[target_email]
    revoker = users.get(revoked_by_email)
    
    if not revoker:
        return False, "Revoker account not found"
    
    # Check permissions
    if not revoker.has_permission("license_management"):
        return False, "No permission to revoke custom permissions"
    
    # Revoke permission
    target_user.revoke_permission(feature_name, revoked_by_email)
    
    save_users_db(users)
    log_audit("REVOKE_PERMISSION", revoked_by_email, target_email, f"Feature: {feature_name}")
    
    return True, f"Permission revoked: {feature_name} from {target_email}"


# ============================================
# LICENSE MANAGEMENT
# ============================================

def extend_license(target_email, days, extended_by_email):
    """Extend user license"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    target_user = users[target_email]
    extender = users.get(extended_by_email)
    
    if not extender:
        return False, "Extender account not found"
    
    # Check permissions
    if not extender.has_permission("license_management"):
        return False, "No permission to extend licenses"
    
    # Extend license
    target_user.extend_license(days, extended_by_email)
    
    save_users_db(users)
    log_audit("EXTEND_LICENSE", extended_by_email, target_email, f"Extended by {days} days")
    
    return True, f"License extended: {target_email} by {days} days"


def change_role(target_email, new_role, changed_by_email):
    """Change user role"""
    users = load_users_db()
    
    if target_email not in users:
        return False, "User not found"
    
    if new_role not in USER_TYPES:
        return False, f"Invalid role: {new_role}"
    
    target_user = users[target_email]
    changer = users.get(changed_by_email)
    
    if not changer:
        return False, "Changer account not found"
    
    # Check permissions
    target_type = USER_TYPES[new_role]["type"]
    
    if target_type == "student":
        if not changer.has_permission("student_management"):
            return False, "No permission to change student roles"
    elif target_type == "staff":
        if changer.has_permission("staff_management") != "full":
            return False, "No permission to change staff roles"
    elif target_type in ["admin", "super_admin"]:
        if not changer.has_permission("admin_management"):
            return False, "No permission to change admin roles"
    
    # Change role
    old_role = target_user.role
    target_user.change_role(new_role, changed_by_email)
    
    save_users_db(users)
    log_audit("CHANGE_ROLE", changed_by_email, target_email, f"From {old_role} to {new_role}")
    
    return True, f"Role changed: {target_email} from {old_role} to {new_role}"


# ============================================
# ANALYTICS & REPORTING
# ============================================

def get_all_users(filter_by=None):
    """Get all users with optional filtering from both databases"""
    users = load_users_db()
    
    user_list = []
    
    # Get users from NEW database
    for email, user in users.items():
        summary = user.get_summary()
        
        # Apply filters
        if filter_by:
            if filter_by.get("type"):
                if summary["user_type"] != filter_by["type"]:
                    continue
            if filter_by.get("status"):
                if summary["status"] != filter_by["status"]:
                    continue
            if filter_by.get("role"):
                if summary["role"] != filter_by["role"]:
                    continue
        
        user_list.append(summary)
    
    # Also get users from OLD database (users_database.json)
    import json
    import os
    if os.path.exists("users_database.json"):
        with open("users_database.json", 'r') as f:
            old_users = json.load(f)
        
        for email, old_user in old_users.items():
            # Skip if already in new database
            if email in users:
                continue
            
            # Convert old format to summary format
            license = old_user.get("license", {})
            role = license.get("role", "unknown")
            
            from datetime import datetime
            expiry_str = license.get("expiry_date", "")
            try:
                expiry_dt = datetime.fromisoformat(expiry_str)
                days_remaining = (expiry_dt - datetime.now()).days
            except:
                expiry_dt = datetime.now()
                days_remaining = 0
            
            summary = {
                "email": email,
                "full_name": old_user.get("full_name", "Unknown"),
                "role": role,
                "role_name": "Administrator" if role == "admin" else role.title(),
                "user_type": "admin" if role == "admin" else "student",
                "status": "active",
                "status_display": "Active (Legacy Account)",
                "created_at": old_user.get("created_at", "Unknown"),
                "expiry_date": expiry_dt.strftime("%d/%m/%Y"),
                "days_remaining": days_remaining
            }
            
            # Apply filters
            if filter_by:
                if filter_by.get("type") and summary["user_type"] != filter_by["type"]:
                    continue
                if filter_by.get("status") and "active" != filter_by["status"]:
                    continue
            
            user_list.append(summary)
    
    return user_list


def get_user_details(email):
    """Get detailed user information"""
    users = load_users_db()
    
    if email not in users:
        return None
    
    user = users[email]
    details = user.get_summary()
    
    # Add additional details
    details["features"] = USER_TYPES[user.role]["features"]
    details["custom_permissions"] = user.custom_permissions
    details["notes"] = user.notes
    details["usage"] = user.usage
    
    return details


def get_revenue_stats():
    """Get revenue statistics"""
    users = load_users_db()
    
    total_revenue = 0
    revenue_by_role = {}
    active_students = 0
    
    for email, user in users.items():
        if user.status == "active" and USER_TYPES[user.role]["type"] == "student":
            price = USER_TYPES[user.role]["price"]
            total_revenue += price
            
            role_name = USER_TYPES[user.role]["name"]
            if role_name not in revenue_by_role:
                revenue_by_role[role_name] = {"count": 0, "revenue": 0}
            
            revenue_by_role[role_name]["count"] += 1
            revenue_by_role[role_name]["revenue"] += price
            
            active_students += 1
    
    return {
        "total_revenue": total_revenue,
        "active_students": active_students,
        "revenue_by_role": revenue_by_role
    }


def get_audit_log(limit=100):
    """Get recent audit log entries"""
    if not os.path.exists(AUDIT_LOG_FILE):
        return []
    
    with open(AUDIT_LOG_FILE, 'r') as f:
        logs = json.load(f)
    
    # Return most recent first
    return logs[-limit:][::-1]


def get_platform_stats():
    """Get overall platform statistics"""
    users = load_users_db()
    
    stats = {
        "total_users": len(users),
        "active_users": 0,
        "suspended_users": 0,
        "expired_users": 0,
        "terminated_users": 0,
        "students": 0,
        "staff": 0,
        "admins": 0,
        "total_logins": 0
    }
    
    for email, user in users.items():
        user_type = USER_TYPES[user.role]["type"]
        
        if user.status == "active":
            stats["active_users"] += 1
        elif user.status == "suspended":
            stats["suspended_users"] += 1
        elif user.status == "expired":
            stats["expired_users"] += 1
        elif user.status == "terminated":
            stats["terminated_users"] += 1
        
        if user_type == "student":
            stats["students"] += 1
        elif user_type == "staff":
            stats["staff"] += 1
        elif user_type in ["admin", "super_admin"]:
            stats["admins"] += 1
        
        stats["total_logins"] += user.usage.get("total_logins", 0)
    
    return stats
