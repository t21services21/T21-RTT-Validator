"""
T21 SERVICES - MODULAR ACCESS CONTROL SYSTEM
Hierarchical permission system for granular access control

Features:
- Hierarchical module structure (Parent → Child modules)
- Individual scenario access in Training Library
- Individual course access in LMS
- Package-based access (bundle multiple modules)
- Role-based default access
- User-specific overrides
- Module marketplace (sell individual modules)
"""

import json
import os
from typing import Dict, List, Optional


# ============================================
# MODULE HIERARCHY DEFINITION
# ============================================

MODULE_HIERARCHY = {
    "RTT Training": {
        "id": "rtt_training",
        "parent": None,
        "children": {
            "Training Library": {
                "id": "training_library",
                "parent": "rtt_training",
                "children": {
                    "Scenario 1: Standard Referral": {"id": "scenario_01"},
                    "Scenario 2: Urgent Referral": {"id": "scenario_02"},
                    "Scenario 3: Two Week Wait": {"id": "scenario_03"},
                    "Scenario 4: DNA Appointment": {"id": "scenario_04"},
                    "Scenario 5: Patient Cancellation": {"id": "scenario_05"},
                    "Scenario 6: Hospital Cancellation": {"id": "scenario_06"},
                    "Scenario 7: Clock Pause": {"id": "scenario_07"},
                    "Scenario 8: Clock Restart": {"id": "scenario_08"},
                    "Scenario 9: Diagnostic Wait": {"id": "scenario_09"},
                    "Scenario 10: Treatment Wait": {"id": "scenario_10"},
                    # ... more scenarios
                }
            },
            "Interactive Learning": {
                "id": "interactive_learning",
                "parent": "rtt_training",
                "children": {
                    "Quiz Mode": {"id": "quiz_mode"},
                    "Challenge Mode": {"id": "challenge_mode"},
                    "Time Attack": {"id": "time_attack"},
                    "Leaderboard": {"id": "leaderboard"},
                }
            },
            "AI RTT Tutor": {
                "id": "ai_tutor",
                "parent": "rtt_training",
                "children": None
            },
            "Certification Exam": {
                "id": "certification_exam",
                "parent": "rtt_training",
                "children": {
                    "Practice Exam": {"id": "practice_exam"},
                    "Official Exam": {"id": "official_exam"},
                    "Exam Results": {"id": "exam_results"},
                }
            }
        }
    },
    
    "RTT Tools": {
        "id": "rtt_tools",
        "parent": None,
        "children": {
            "Pathway Validator": {"id": "pathway_validator"},
            "Clinic Letter Interpreter": {"id": "clinic_interpreter"},
            "Timeline Auditor": {"id": "timeline_auditor"},
            "Registration Validator": {"id": "registration_validator"},
            "Appointment Checker": {"id": "appointment_checker"},
            "Comment Generator": {"id": "comment_generator"},
            "Letter Creator": {"id": "letter_creator"},
        }
    },
    
    "LMS - Learning Management": {
        "id": "lms",
        "parent": None,
        "children": {
            "Course Catalog": {"id": "course_catalog"},
            "My Courses": {"id": "my_courses"},
            "Certificates": {"id": "certificates"},
            # Individual courses added dynamically
        }
    },
    
    "Career Tools": {
        "id": "career_tools",
        "parent": None,
        "children": {
            "Job Interview Prep": {"id": "interview_prep"},
            "CV Builder": {"id": "cv_builder"},
        }
    },
    
    "Analytics & Reports": {
        "id": "analytics",
        "parent": None,
        "children": {
            "Dashboard": {"id": "dashboard"},
            "Smart Alerts": {"id": "smart_alerts"},
            "Validation History": {"id": "validation_history"},
            "Interactive Reports": {"id": "interactive_reports"},
        }
    },
    
    "Staff Management": {
        "id": "staff_management",
        "parent": None,
        "children": {
            "Staff Directory": {"id": "staff_directory"},
            "Scheduling": {"id": "scheduling"},
            "Task Management": {"id": "task_management"},
            "Performance": {"id": "performance"},
        }
    },
    
    "Admin Tools": {
        "id": "admin_tools",
        "parent": None,
        "children": {
            "User Management": {"id": "user_management"},
            "Module Access Control": {"id": "module_access"},
            "Bulk Email": {"id": "bulk_email"},
            "Personal Messages": {"id": "personal_messages"},
            "Trial Automation": {"id": "trial_automation"},
            "Course Management": {"id": "course_management"},
        }
    }
}


# ============================================
# ACCESS PACKAGES (Bundles)
# ============================================

ACCESS_PACKAGES = {
    "RTT Essentials": {
        "id": "rtt_essentials",
        "price": 299,
        "duration_days": 90,
        "modules": [
            "pathway_validator",
            "training_library",
            "scenario_01", "scenario_02", "scenario_03", "scenario_04", "scenario_05"
        ],
        "description": "Basic RTT tools and 5 training scenarios"
    },
    
    "RTT Professional": {
        "id": "rtt_professional",
        "price": 599,
        "duration_days": 180,
        "modules": [
            "rtt_tools",  # All RTT tools
            "training_library",  # All 40 scenarios
            "interactive_learning",
            "ai_tutor"
        ],
        "description": "Complete RTT toolkit with AI tutor"
    },
    
    "RTT Master + Certification": {
        "id": "rtt_master",
        "price": 999,
        "duration_days": 365,
        "modules": [
            "rtt_tools",
            "training_library",
            "interactive_learning",
            "ai_tutor",
            "certification_exam",
            "career_tools",
            "analytics"
        ],
        "description": "Everything + Certification Exam"
    },
    
    "Hospital Admin Package": {
        "id": "hospital_admin",
        "price": 399,
        "duration_days": 180,
        "modules": [
            "course_catalog",
            "my_courses",
            # Specific LMS courses for admin
        ],
        "description": "Hospital administration courses"
    },
    
    "Full Platform Access": {
        "id": "full_access",
        "price": 1499,
        "duration_days": 365,
        "modules": ["all"],  # Special: access to everything
        "description": "Complete platform access"
    }
}


# ============================================
# FILE PATHS
# ============================================

MODULAR_ACCESS_FILE = "modular_access_control.json"
USER_MODULE_ACCESS_FILE = "user_module_access.json"


# ============================================
# CORE FUNCTIONS
# ============================================

def load_user_module_access() -> Dict:
    """Load user-specific module access"""
    if os.path.exists(USER_MODULE_ACCESS_FILE):
        try:
            with open(USER_MODULE_ACCESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_user_module_access(data: Dict):
    """Save user-specific module access"""
    with open(USER_MODULE_ACCESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def grant_module_access(user_email: str, module_id: str, expiry_days: int = None):
    """Grant access to a specific module for a user"""
    access_data = load_user_module_access()
    
    if user_email not in access_data:
        access_data[user_email] = {}
    
    from datetime import datetime, timedelta
    
    expiry = None
    if expiry_days:
        expiry = (datetime.now() + timedelta(days=expiry_days)).isoformat()
    
    access_data[user_email][module_id] = {
        "granted_at": datetime.now().isoformat(),
        "expires_at": expiry,
        "status": "active"
    }
    
    save_user_module_access(access_data)


def revoke_module_access(user_email: str, module_id: str):
    """Revoke access to a specific module"""
    access_data = load_user_module_access()
    
    if user_email in access_data and module_id in access_data[user_email]:
        del access_data[user_email][module_id]
        save_user_module_access(access_data)


def grant_package_access(user_email: str, package_id: str):
    """Grant access to a package (bundle of modules)"""
    if package_id not in ACCESS_PACKAGES:
        return False
    
    package = ACCESS_PACKAGES[package_id]
    duration = package.get("duration_days")
    
    # Special case: full access
    if "all" in package["modules"]:
        grant_module_access(user_email, "full_access", duration)
        return True
    
    # Grant each module in package
    for module_id in package["modules"]:
        grant_module_access(user_email, module_id, duration)
    
    return True


def user_has_module_access(user_email: str, module_id: str) -> bool:
    """Check if user has access to a specific module"""
    access_data = load_user_module_access()
    
    if user_email not in access_data:
        return False
    
    # Check for full access
    if "full_access" in access_data[user_email]:
        full_access = access_data[user_email]["full_access"]
        if is_access_valid(full_access):
            return True
    
    # Check specific module
    if module_id in access_data[user_email]:
        module_access = access_data[user_email][module_id]
        return is_access_valid(module_access)
    
    # Check parent modules (hierarchical)
    parent_id = get_parent_module(module_id)
    if parent_id:
        if parent_id in access_data[user_email]:
            parent_access = access_data[user_email][parent_id]
            return is_access_valid(parent_access)
    
    return False


def is_access_valid(access_info: Dict) -> bool:
    """Check if access is still valid (not expired)"""
    if access_info.get("status") != "active":
        return False
    
    expiry = access_info.get("expires_at")
    if not expiry:
        return True  # No expiry = permanent access
    
    from datetime import datetime
    expiry_date = datetime.fromisoformat(expiry)
    
    return datetime.now() < expiry_date


def get_parent_module(module_id: str) -> Optional[str]:
    """Get parent module ID for hierarchical access check"""
    # This is a simplified version
    # In production, you'd traverse MODULE_HIERARCHY
    
    parent_map = {
        "scenario_01": "training_library",
        "scenario_02": "training_library",
        "scenario_03": "training_library",
        "scenario_04": "training_library",
        "scenario_05": "training_library",
        # ... more mappings
        "training_library": "rtt_training",
        "interactive_learning": "rtt_training",
        "ai_tutor": "rtt_training",
    }
    
    return parent_map.get(module_id)


def get_user_accessible_modules(user_email: str) -> List[str]:
    """Get list of all modules user has access to"""
    access_data = load_user_module_access()
    
    if user_email not in access_data:
        return []
    
    accessible = []
    
    for module_id, access_info in access_data[user_email].items():
        if is_access_valid(access_info):
            accessible.append(module_id)
    
    return accessible


def get_user_module_status(user_email: str, module_id: str) -> Dict:
    """Get detailed status of user's access to a module"""
    access_data = load_user_module_access()
    
    if user_email not in access_data or module_id not in access_data[user_email]:
        return {
            "has_access": False,
            "status": "no_access",
            "expires_at": None,
            "days_remaining": None
        }
    
    access_info = access_data[user_email][module_id]
    has_access = is_access_valid(access_info)
    
    days_remaining = None
    expiry = access_info.get("expires_at")
    
    if expiry:
        from datetime import datetime
        expiry_date = datetime.fromisoformat(expiry)
        delta = expiry_date - datetime.now()
        days_remaining = delta.days
    
    return {
        "has_access": has_access,
        "status": access_info.get("status"),
        "expires_at": expiry,
        "days_remaining": days_remaining,
        "granted_at": access_info.get("granted_at")
    }


def list_all_modules() -> List[Dict]:
    """List all available modules in the system"""
    modules = []
    
    def traverse(hierarchy, parent=None):
        for name, data in hierarchy.items():
            if isinstance(data, dict) and "id" in data:
                modules.append({
                    "name": name,
                    "id": data["id"],
                    "parent": data.get("parent"),
                    "has_children": data.get("children") is not None
                })
                
                if data.get("children"):
                    traverse(data["children"], data["id"])
    
    traverse(MODULE_HIERARCHY)
    
    return modules


def get_available_packages() -> List[Dict]:
    """Get all available access packages"""
    return [
        {
            "id": pkg_id,
            "name": pkg_id.replace("_", " ").title(),
            **pkg_data
        }
        for pkg_id, pkg_data in ACCESS_PACKAGES.items()
    ]
