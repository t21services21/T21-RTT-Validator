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

# ============================================
# MODULAR ACCESS CONTROL SYSTEM
# Each module can be sold/accessed separately
# ============================================

# MODULE DEFINITIONS
MODULES = {
    # MODULE 1: RTT VALIDATION
    "RTT_VALIDATION_MODULE": {
        "name": "RTT Validation Module",
        "description": "Complete RTT validation training & automation",
        "price_nhs": 50000,
        "price_individual": 999,
        "tools": ["🤖 AI Auto-Validator", "📊 Pathway Validator", "📅 Timeline Auditor"],
        "training": "40 RTT validation scenarios"
    },
    
    # MODULE 2: PATIENT PATHWAY
    "PATIENT_PATHWAY_MODULE": {
        "name": "Patient Pathway Module",
        "description": "Complete pathway coordination training & automation",
        "price_nhs": 75000,
        "price_individual": 1299,
        "tools": ["📋 PTL - Patient Tracking List", "🤖 AI Auto-Validator"],
        "training": "30 pathway coordination scenarios"
    },
    
    # MODULE 3: CANCER PATHWAY
    "CANCER_PATHWAY_MODULE": {
        "name": "Cancer Pathway Module",
        "description": "2WW/62-day cancer pathway training & automation",
        "price_nhs": 60000,
        "price_individual": 1199,
        "tools": ["🎗️ Cancer Pathways"],
        "training": "20 cancer pathway scenarios"
    },
    
    # MODULE 4: WAITING LIST
    "WAITING_LIST_MODULE": {
        "name": "Waiting List Module",
        "description": "Waiting list management training & automation",
        "price_nhs": 55000,
        "price_individual": 899,
        "tools": ["📋 PTL - Patient Tracking List"],
        "training": "20 waiting list scenarios"
    },
    
    # MODULE 5: APPOINTMENT SCHEDULER
    "APPOINTMENT_MODULE": {
        "name": "Appointment Scheduler Module",
        "description": "AI appointment scheduling training & automation",
        "price_nhs": 65000,
        "price_individual": 1099,
        "tools": ["📆 Appointment & Booking Checker", "📅 Advanced Booking System"],
        "training": "20 booking scenarios"
    },
    
    # MODULE 6: MDT COORDINATION
    "MDT_MODULE": {
        "name": "MDT Coordination Module",
        "description": "MDT meeting coordination training & automation",
        "price_nhs": 50000,
        "price_individual": 999,
        "tools": ["👥 MDT Coordination"],
        "training": "18 MDT scenarios"
    },
    
    # MODULE 7: MEDICAL SECRETARY
    "MEDICAL_SECRETARY_MODULE": {
        "name": "Medical Secretary Module",
        "description": "Complete medical secretary training & automation",
        "price_nhs": 70000,
        "price_individual": 1199,
        "tools": ["📝 Clinic Letter Interpreter", "✍️ Clinic Letter Creator", "📧 Medical Secretary AI"],
        "training": "25 secretary scenarios"
    },
    
    # MODULE 8: DATA QUALITY
    "DATA_QUALITY_MODULE": {
        "name": "Data Quality Module",
        "description": "Data quality & audit training & automation",
        "price_nhs": 60000,
        "price_individual": 999,
        "tools": ["📊 Data Quality System"],
        "training": "15 data quality scenarios"
    },
    
    # MODULE 9: AI KNOWLEDGE BASE
    "AI_KNOWLEDGE_MODULE": {
        "name": "AI Training & Knowledge Base",
        "description": "AI learns from YOUR training materials",
        "price_nhs": 40000,
        "price_individual": 599,
        "tools": ["🤖 AI Training"],
        "training": "AI knowledge management"
    },
    
    # MODULE 10: LMS
    "LMS_MODULE": {
        "name": "Professional LMS Module",
        "description": "Complete learning management system",
        "price_nhs": 45000,
        "price_individual": 799,
        "tools": ["📚 LMS Courses", "🎓 Training Library"],
        "training": "LMS administration"
    },
    
    # MODULE 11: SCHOOL MANAGEMENT
    "SCHOOL_MODULE": {
        "name": "School Management Module",
        "description": "Complete school/academy administration",
        "price_nhs": 50000,
        "price_individual": 999,
        "tools": ["🏫 School Management"],
        "training": "School administration"
    }
}

# BUNDLE PACKAGES
BUNDLES = {
    "STARTER": {
        "name": "Starter Bundle",
        "modules": ["RTT_VALIDATION_MODULE", "PATIENT_PATHWAY_MODULE", "WAITING_LIST_MODULE"],
        "price_nhs": 80000,
        "price_individual": 1499,
        "discount": "30%"
    },
    "PROFESSIONAL": {
        "name": "Professional Bundle",
        "modules": ["RTT_VALIDATION_MODULE", "PATIENT_PATHWAY_MODULE", "CANCER_PATHWAY_MODULE", 
                   "WAITING_LIST_MODULE", "APPOINTMENT_MODULE"],
        "price_nhs": 150000,
        "price_individual": 2999,
        "discount": "40%"
    },
    "ULTIMATE": {
        "name": "Ultimate Bundle",
        "modules": list(MODULES.keys()),
        "price_nhs": 250000,
        "price_individual": 4999,
        "discount": "50%"
    }
}

# Default module access by role
DEFAULT_MODULE_ACCESS = {
    "📋 PTL - Patient Tracking List": {
        "trial": True,  # Trial gets basic PTL access only
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🤖 AI Auto-Validator": {
        "trial": False,  # NO AI for trial users!
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🎗️ Cancer Pathways": {
        "trial": False,
        "basic": False,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "👥 MDT Coordination": {
        "trial": False,
        "basic": False,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📅 Advanced Booking System": {
        "trial": False,
        "basic": False,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📧 Medical Secretary AI": {
        "trial": False,
        "basic": False,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📊 Data Quality System": {
        "trial": False,
        "basic": False,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📊 Pathway Validator": {
        "trial": False,  # Trial = LIMITED access only
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📝 Clinic Letter Interpreter": {
        "trial": False,  # NO letter tools for trial
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📅 Timeline Auditor": {
        "trial": False,  # NO auditor for trial
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "👤 Patient Registration Validator": {
        "trial": False,  # NO validator for trial
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "📆 Appointment & Booking Checker": {
        "trial": False,  # NO booking tools for trial
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "💬 Comment Line Generator": {
        "trial": False,  # NO comment generator for trial
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "✍️ Clinic Letter Creator": {
        "trial": False,  # NO letter creator for trial
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
        "trial": False,  # NO interview prep for trial
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": False,  # Admin doesn't need this
        "staff": False,  # Staff don't need this
        "nhs_trust": True
    },
    "📄 CV Builder": {
        "trial": False,  # NO CV builder for trial
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
    },
    "🏥 PAS Integration Demo (Hands-On)": {
        "trial": True,  # ALL users - practical training/demo tool
        "basic": True,
        "professional": True,
        "ultimate": True,
        "admin": True,
        "staff": True,
        "nhs_trust": True
    },
    "🔌 Custom PAS Integration": {
        "trial": False,  # NHS Trusts and Admins ONLY
        "basic": False,
        "professional": False,
        "ultimate": False,
        "admin": True,  # Admin can configure
        "staff": False,
        "nhs_trust": True  # NHS trusts can request integration
    },
    "🎓 Practical Training Portal (All Courses)": {
        "trial": True,  # ALL users - external training system
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
