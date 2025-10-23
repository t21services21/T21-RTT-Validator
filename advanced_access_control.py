"""
T21 ADVANCED ACCESS CONTROL SYSTEM
Complete role-based access control for Students, Staff, and Admins

Features:
- Multiple user types (Student, Staff, Admin, Super Admin)
- Granular feature permissions
- Account suspension/termination
- Audit logging
- Custom permission management
"""

from datetime import datetime, timedelta
import json
import hashlib

# ============================================
# USER TYPES & ROLES
# ============================================

USER_TYPES = {
    # ========== STUDENTS ==========
    "student_trial": {
        "type": "student",
        "name": "Trial Student",
        "duration_days": 7,
        "price": 0,
        "max_logins_per_day": 10,
        "features": {
            "pathway_validator": "limited",  # 20 per day
            "clinic_letter_interpreter": "limited",
            "training_library": "limited",  # 5 scenarios
            "interactive_learning": "limited",  # 10 quizzes/day
            "ai_tutor": "limited",  # 5 questions/day
            "certification_exam": False,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": False,
            "breach_calculator": "limited",
            "admin_panel": False,
            "staff_tools": False
        }
    },
    
    "student_basic": {
        "type": "student",
        "name": "Basic Student",
        "duration_days": 90,
        "price": 599,
        "max_logins_per_day": 20,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": "limited",  # 10 questions/day
            "certification_exam": False,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": False,
            "breach_calculator": "limited",
            "admin_panel": False,
            "staff_tools": False
        }
    },
    
    "student_professional": {
        "type": "student",
        "name": "Professional Student",
        "duration_days": 180,
        "price": 999,
        "max_logins_per_day": 50,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,  # Unlimited
            "certification_exam": False,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": True,
            "breach_calculator": True,
            "admin_panel": False,
            "staff_tools": False
        }
    },
    
    "student_ultimate": {
        "type": "student",
        "name": "Ultimate Student",
        "duration_days": 365,
        "price": 1499,
        "max_logins_per_day": 100,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": True,
            "breach_calculator": True,
            "admin_panel": False,
            "staff_tools": False,
            "priority_support": True
        }
    },
    
    # ========== T21 STAFF ==========
    "staff_trainer": {
        "type": "staff",
        "name": "T21 Trainer",
        "duration_days": 365,
        "price": 0,
        "max_logins_per_day": 200,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": True,
            "breach_calculator": True,
            "admin_panel": "limited",  # View only
            "staff_tools": True,
            "student_management": "view",  # Can view students
            "create_content": True,  # Can create scenarios
            "grade_exams": True
        }
    },
    
    "staff_support": {
        "type": "staff",
        "name": "T21 Support Staff",
        "duration_days": 365,
        "price": 0,
        "max_logins_per_day": 150,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": False,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": False,
            "breach_calculator": True,
            "admin_panel": "limited",  # View only
            "staff_tools": True,
            "student_management": "view",  # Can view students
            "support_tickets": True
        }
    },
    
    # ========== TESTERS ==========
    "tester": {
        "type": "tester",
        "name": "Module Tester",
        "duration_days": 365,
        "price": 0,
        "max_logins_per_day": 500,
        "features": {
            # ALL FEATURES except user management/access control
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": True,
            "breach_calculator": True,
            "admin_panel": False,  # NO admin panel
            "staff_tools": True,
            "student_management": "view",  # Can view but not manage
            "create_content": True,
            "grade_exams": True,
            "support_tickets": True,
            "all_modules": True  # Access to all modules for testing
        }
    },
    
    # ========== ADMINISTRATORS ==========
    "admin": {
        "type": "admin",
        "name": "Administrator",
        "duration_days": 9999,
        "price": 0,
        "max_logins_per_day": 500,
        "features": {
            # All features enabled
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": True,
            "breach_calculator": True,
            "admin_panel": True,  # Full access
            "staff_tools": True,
            "student_management": "full",  # Full control
            "staff_management": "full",  # Can manage staff
            "create_content": True,
            "grade_exams": True,
            "system_settings": True,
            "revenue_reports": True,
            "audit_logs": True,
            "license_management": True
        }
    },
    
    "super_admin": {
        "type": "super_admin",
        "name": "Super Administrator",
        "duration_days": 9999,
        "price": 0,
        "max_logins_per_day": 999,
        "features": {
            # ALL FEATURES - NO RESTRICTIONS
            "all_access": True,
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": True,
            "breach_calculator": True,
            "admin_panel": True,
            "staff_tools": True,
            "student_management": "full",
            "staff_management": "full",
            "admin_management": "full",  # Can manage admins
            "create_content": True,
            "grade_exams": True,
            "system_settings": True,
            "revenue_reports": True,
            "audit_logs": True,
            "license_management": True,
            "database_access": True,
            "terminate_accounts": True
        }
    },
    
    # BACKWARDS COMPATIBILITY - Generic "staff" role
    "staff": {
        "type": "staff",
        "name": "Staff Member",
        "duration_days": 9999,
        "price": 0,
        "max_logins_per_day": 500,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "pas_practice": True,
            "breach_calculator": True,
            "admin_panel": True,  # Full admin access
            "staff_tools": True,
            "student_management": "full",
            "staff_management": "full",
            "create_content": True,
            "grade_exams": True,
            "system_settings": True,
            "revenue_reports": True,
            "audit_logs": True,
            "license_management": True
        }
    }
}


# ============================================
# ACCOUNT STATUS
# ============================================

ACCOUNT_STATUS = {
    "active": "Active - Full Access",
    "suspended": "Suspended - Access Denied",
    "expired": "Expired - Renewal Required",
    "terminated": "Terminated - Permanently Disabled",
    "pending": "Pending - Awaiting Activation"
}


# ============================================
# ENHANCED USER ACCOUNT CLASS
# ============================================

class UserAccount:
    """Enhanced user account with full access control"""
    
    def __init__(self, user_id=None, email=None, role=None, full_name=None, created_by="system", password_hash=None, user_type=None):
        self.user_id = user_id or email  # Use email as ID if no user_id
        self.email = email
        self.role = role or "trial"
        self.full_name = full_name or "User"
        self._user_type = user_type  # Store as private variable (used by property below)
        self.created_by = created_by
        self.created_at = datetime.now()
        self.password_hash = password_hash  # Store password hash
        
        # Account status
        self.status = "active"
        self.suspended_reason = None
        self.suspended_by = None
        self.suspended_at = None
        self.terminated_at = None
        
        # License info - Handle unknown roles gracefully
        if role not in USER_TYPES:
            # Default to admin if role not found (backwards compatibility)
            if "admin" in role.lower() or "staff" in role.lower():
                role = "admin"
            else:
                role = "student_trial"
            
        role_info = USER_TYPES.get(role, USER_TYPES["admin"])  # Fallback to admin
        self.duration_days = role_info["duration_days"]
        self.expiry_date = self.created_at + timedelta(days=self.duration_days)
        
        # Usage tracking
        self.usage = {
            "total_logins": 0,
            "last_login": None,
            "logins_today": 0,
            "last_login_date": None,
            "ai_questions_today": 0,
            "quizzes_today": 0,
            "validations_today": 0,
            "last_reset_date": datetime.now().date()
        }
        
        # Custom permissions (override defaults)
        self.custom_permissions = {}
        
        # Notes
        self.notes = []
    
    @property
    def user_type(self):
        """Get user type from role for backwards compatibility"""
        # If explicitly set during init, use that
        if hasattr(self, '_user_type') and self._user_type:
            return self._user_type
        
        # Otherwise, derive from role
        if self.role in ['admin', 'super_admin']:
            return 'admin'
        elif self.role in ['staff', 'staff_trainer', 'staff_support']:
            return 'staff'
        elif self.role.startswith('student_'):
            return 'student'
        else:
            # Fallback: check role type in USER_TYPES
            if self.role in USER_TYPES:
                return USER_TYPES[self.role].get('type', 'student')
            return 'student'
    
    def is_active(self):
        """Check if account is active"""
        if self.status == "terminated":
            return False
        if self.status == "suspended":
            return False
        
        # Safety check for expiry_date
        try:
            if hasattr(self.expiry_date, '__call__'):
                # If it's a method, call it
                expiry = self.expiry_date()
            else:
                expiry = self.expiry_date
            
            if datetime.now() > expiry:
                self.status = "expired"
                return False
        except:
            # If comparison fails, assume active
            pass
        
        return self.status == "active"
    
    def has_permission(self, feature_name):
        """Check if user has permission for a feature"""
        if not self.is_active():
            return False
        
        # Check custom permissions first
        if feature_name in self.custom_permissions:
            return self.custom_permissions[feature_name]
        
        # Check role permissions
        role_features = USER_TYPES[self.role]["features"]
        
        # Super admin has all access
        if role_features.get("all_access"):
            return True
        
        if feature_name not in role_features:
            return False
        
        permission = role_features[feature_name]
        
        if permission is True:
            return True
        elif permission is False:
            return False
        elif permission == "limited":
            return self._check_usage_limit(feature_name)
        elif permission == "view":
            return "view"  # Read-only access
        elif permission == "full":
            return "full"  # Full control
        
        return False
    
    def _check_usage_limit(self, feature_name):
        """Check usage limits"""
        # Reset daily counters if new day
        today = datetime.now().date()
        
        last_reset = self.usage.get("last_reset_date")
        if isinstance(last_reset, str):
            from datetime import datetime as dt
            last_reset = dt.fromisoformat(last_reset).date()
        
        if last_reset != today:
            self.usage["ai_questions_today"] = 0
            self.usage["quizzes_today"] = 0
            self.usage["validations_today"] = 0
            self.usage["last_reset_date"] = today.isoformat()
        
        # Check specific limits based on feature
        if "ai_tutor" in feature_name:
            if self.role == "student_trial":
                return self.usage["ai_questions_today"] < 5
            elif self.role == "student_basic":
                return self.usage["ai_questions_today"] < 10
        
        if "quiz" in feature_name or "interactive_learning" in feature_name:
            if self.role == "student_trial":
                return self.usage["quizzes_today"] < 10
            elif self.role == "student_basic":
                return self.usage["quizzes_today"] < 50
        
        if "validator" in feature_name or "pathway" in feature_name:
            if self.role == "student_trial":
                return self.usage["validations_today"] < 20
        
        return True
    
    def suspend(self, reason, suspended_by):
        """Suspend account"""
        self.status = "suspended"
        self.suspended_reason = reason
        self.suspended_by = suspended_by
        self.suspended_at = datetime.now()
        self.add_note(f"Account suspended by {suspended_by}: {reason}")
    
    def unsuspend(self, unsuspended_by):
        """Unsuspend account"""
        self.status = "active"
        old_reason = self.suspended_reason
        self.suspended_reason = None
        self.suspended_by = None
        self.suspended_at = None
        self.add_note(f"Account unsuspended by {unsuspended_by}. Previous reason: {old_reason}")
    
    def terminate(self, reason, terminated_by):
        """Permanently terminate account"""
        self.status = "terminated"
        self.terminated_at = datetime.now()
        self.add_note(f"Account TERMINATED by {terminated_by}: {reason}")
    
    def extend_license(self, days, extended_by):
        """Extend license"""
        old_expiry = self.expiry_date
        self.expiry_date += timedelta(days=days)
        self.add_note(f"License extended by {days} days by {extended_by}. New expiry: {self.expiry_date.strftime('%d/%m/%Y')}")
    
    def change_role(self, new_role, changed_by):
        """Change user role"""
        old_role = self.role
        self.role = new_role
        self.add_note(f"Role changed from {old_role} to {new_role} by {changed_by}")
    
    def grant_permission(self, feature_name, granted_by):
        """Grant custom permission"""
        self.custom_permissions[feature_name] = True
        self.add_note(f"Custom permission granted: {feature_name} by {granted_by}")
    
    def revoke_permission(self, feature_name, revoked_by):
        """Revoke custom permission"""
        self.custom_permissions[feature_name] = False
        self.add_note(f"Custom permission revoked: {feature_name} by {revoked_by}")
    
    def add_note(self, note):
        """Add note to account"""
        self.notes.append({
            "timestamp": datetime.now().isoformat(),
            "note": note
        })
    
    def record_login(self):
        """Record login"""
        today = datetime.now().date()
        
        # Reset daily counter if new day
        last_login_date = self.usage.get("last_login_date")
        if isinstance(last_login_date, str):
            from datetime import datetime as dt
            last_login_date = dt.fromisoformat(last_login_date).date()
        
        if last_login_date != today:
            self.usage["logins_today"] = 0
            self.usage["last_login_date"] = today.isoformat()
        
        self.usage["total_logins"] += 1
        self.usage["logins_today"] += 1
        self.usage["last_login"] = datetime.now().isoformat()
    
    def increment_usage(self, feature_type):
        """Increment usage counter"""
        if feature_type == "ai_question":
            self.usage["ai_questions_today"] += 1
        elif feature_type == "quiz":
            self.usage["quizzes_today"] += 1
        elif feature_type == "validation":
            self.usage["validations_today"] += 1
    
    def get_summary(self):
        """Get account summary"""
        # Safety check for expiry_date (might be method or datetime)
        try:
            if hasattr(self.expiry_date, '__call__'):
                expiry = self.expiry_date()
            else:
                expiry = self.expiry_date
            
            expiry_str = expiry.strftime("%d/%m/%Y")
            days_remaining = (expiry - datetime.now()).days if self.is_active() else 0
        except:
            expiry_str = "Unknown"
            days_remaining = 0
        
        return {
            "user_id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "role_name": USER_TYPES[self.role]["name"],
            "user_type": USER_TYPES[self.role]["type"],
            "status": self.status,
            "status_text": ACCOUNT_STATUS[self.status],
            "created_at": self.created_at.strftime("%d/%m/%Y"),
            "expiry_date": expiry_str,
            "days_remaining": days_remaining,
            "total_logins": self.usage["total_logins"],
            "last_login": self.usage.get("last_login", "Never"),
            "suspended_reason": self.suspended_reason,
            "custom_permissions": len(self.custom_permissions)
        }
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "password_hash": self.password_hash,  # Save password hash!
            "role": self.role,
            "full_name": self.full_name,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "suspended_reason": self.suspended_reason,
            "suspended_by": self.suspended_by,
            "suspended_at": self.suspended_at.isoformat() if self.suspended_at else None,
            "terminated_at": self.terminated_at.isoformat() if self.terminated_at else None,
            "expiry_date": self.expiry_date.isoformat(),
            "usage": self.usage,
            "custom_permissions": self.custom_permissions,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        account = cls(
            user_id=data["user_id"],
            email=data["email"],
            role=data["role"],
            full_name=data["full_name"],
            created_by=data.get("created_by", "system"),
            password_hash=data.get("password_hash")  # Load password hash!
        )
        account.created_at = datetime.fromisoformat(data["created_at"])
        account.status = data["status"]
        account.suspended_reason = data.get("suspended_reason")
        account.suspended_by = data.get("suspended_by")
        account.suspended_at = datetime.fromisoformat(data["suspended_at"]) if data.get("suspended_at") else None
        account.terminated_at = datetime.fromisoformat(data["terminated_at"]) if data.get("terminated_at") else None
        account.expiry_date = datetime.fromisoformat(data["expiry_date"])
        account.usage = data.get("usage", account.usage)
        account.custom_permissions = data.get("custom_permissions", {})
        account.notes = data.get("notes", [])
        return account
