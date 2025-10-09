"""
T21 SERVICES - MODULE ACCESS CONTROL SYSTEM
Admin interface to control which modules each role can access

Features:
- Configure access for each role (Trial, Basic, Professional, Admin, Staff)
- Toggle module visibility per role
- Save/load settings from JSON
- Easy admin interface
"""

import json
import os

# Default module access by role
DEFAULT_MODULE_ACCESS = {
    "🤖 AI Auto-Validator": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📊 Pathway Validator": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📝 Clinic Letter Interpreter": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📅 Timeline Auditor": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "👤 Patient Registration Validator": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📆 Appointment & Booking Checker": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "💬 Comment Line Generator": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "✍️ Clinic Letter Creator": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🎓 Training Library": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🎮 Interactive Learning Center": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": False,  # Staff don't need gamified learning
        "nhs_trust": True
    },
    "🎓 Certification Exam": {
        "trial": False,  # Trial can't take exam
        "basic": False,  # Basic can't take exam
        "professional": False,  # Professional can't take exam
        "ultimate": True,  # Only Ultimate and above
        "admin": True,
        "staff": False,
        "nhs_trust": True
    },
    "🤖 AI RTT Tutor": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "💼 Job Interview Prep": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": False,  # Admin doesn't need this
        "staff": False,  # Staff don't need this
        "nhs_trust": True
    },
    "📄 CV Builder": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": False,
        "staff": False,
        "nhs_trust": True
    },
    "📊 Interactive Reports": {
        "trial": False,  # Trial can't access reports
        "basic": False,  # Basic can't access reports
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📈 Dashboard & Analytics": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🚨 Smart Alerts": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📜 Validation History": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "⚙️ My Account & Upgrade": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🔧 Admin Panel": {
        "trial": False,
        "basic": False,
        "professional": False,
        "ultimate": False,
        "admin": True,  # Only admins
        "staff": False,
        "nhs_trust": False
    },
    "ℹ️ About RTT Rules": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📚 LMS - My Courses": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "👥 Staff Management": {
        "trial": False,
        "basic": False,
        "professional": False,
        "ultimate": False,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🛒 Module Marketplace": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🎓 My Academic Portal": {
        "trial": True,
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    }
}

MODULE_ACCESS_FILE = "module_access_settings.json"
USER_SPECIFIC_ACCESS_FILE = "user_specific_access.json"


def load_user_specific_access():
    """Load user-specific access overrides"""
    if os.path.exists(USER_SPECIFIC_ACCESS_FILE):
        try:
            with open(USER_SPECIFIC_ACCESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_user_specific_access(settings):
    """Save user-specific access overrides"""
    with open(USER_SPECIFIC_ACCESS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


def load_module_access():
    """Load module access settings from file"""
    if os.path.exists(MODULE_ACCESS_FILE):
        try:
            with open(MODULE_ACCESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_MODULE_ACCESS.copy()
    return DEFAULT_MODULE_ACCESS.copy()


def save_module_access(settings):
    """Save module access settings to file"""
    with open(MODULE_ACCESS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


def can_access_module(module_name, user_role, user_email=None):
    """
    Check if a user can access a specific module
    Checks user-specific overrides first, then role-based access
    
    Args:
        module_name: Name of the module (e.g., "📊 Pathway Validator")
        user_role: User's role (e.g., "trial", "basic", "admin")
        user_email: Optional email for user-specific overrides
    
    Returns:
        bool: True if user can access, False otherwise
    """
    # Check user-specific access first (overrides role-based)
    if user_email:
        user_settings = load_user_specific_access()
        if user_email in user_settings:
            if module_name in user_settings[user_email]:
                return user_settings[user_email][module_name]
    
    # Fall back to role-based access
    settings = load_module_access()
    
    if module_name not in settings:
        # If module not in settings, allow access by default
        return True
    
    return settings[module_name].get(user_role, False)


def get_accessible_modules(user_role, user_email=None):
    """
    Get list of modules a user can access
    Includes both role-based and user-specific access
    
    Args:
        user_role: User's role (e.g., "trial", "basic", "admin")
        user_email: Optional email for user-specific overrides
    
    Returns:
        list: List of module names the user can access
    """
    settings = load_module_access()
    user_settings = load_user_specific_access()
    accessible = []
    
    for module_name in settings.keys():
        # Check user-specific access first
        if user_email and user_email in user_settings:
            if module_name in user_settings[user_email]:
                if user_settings[user_email][module_name]:
                    accessible.append(module_name)
                continue
        
        # Fall back to role-based access
        if settings[module_name].get(user_role, False):
            accessible.append(module_name)
    
    return accessible


def grant_user_access(user_email, module_name):
    """Grant specific user access to a module"""
    user_settings = load_user_specific_access()
    
    if user_email not in user_settings:
        user_settings[user_email] = {}
    
    user_settings[user_email][module_name] = True
    save_user_specific_access(user_settings)


def revoke_user_access(user_email, module_name):
    """Revoke specific user access to a module"""
    user_settings = load_user_specific_access()
    
    if user_email not in user_settings:
        user_settings[user_email] = {}
    
    user_settings[user_email][module_name] = False
    save_user_specific_access(user_settings)


def get_user_specific_access(user_email):
    """Get all module access for a specific user"""
    user_settings = load_user_specific_access()
    return user_settings.get(user_email, {})


def get_all_modules():
    """Get list of all available modules"""
    return list(DEFAULT_MODULE_ACCESS.keys())


def get_all_roles():
    """Get list of all user roles"""
    return ["trial", "basic", "professional", "ultimate", "admin", "staff", "nhs_trust"]


def reset_to_defaults():
    """Reset module access to default settings"""
    save_module_access(DEFAULT_MODULE_ACCESS.copy())
