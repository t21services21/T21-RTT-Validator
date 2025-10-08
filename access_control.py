"""
T21 STUDENT ACCESS CONTROL SYSTEM
Role-Based Access Control (RBAC) with Time-Based Licensing

Features:
- Multiple user roles (Trial, Basic, Professional, Ultimate, Admin)
- Feature-level permissions
- Time-based license expiry
- Usage tracking
- License key validation
"""

from datetime import datetime, timedelta
import hashlib
import json

# ============================================
# ROLES & PERMISSIONS
# ============================================

ROLES = {
    "trial": {
        "name": "Trial Access",
        "duration_days": 7,
        "price": 0,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": "limited",  # Only 5 scenarios
            "interactive_learning": "limited",  # Only 10 quizzes
            "ai_tutor": "limited",  # 5 questions per day
            "certification_exam": False,
            "cv_builder": True,
            "job_interview_prep": True,
            "interactive_reports": False,
            "pas_practice": False,
            "breach_calculator": "limited",  # Single patient only
            "jobs_board": False
        },
        "limits": {
            "training_scenarios": 5,
            "quizzes_per_day": 10,
            "ai_questions_per_day": 5,
            "validations_per_day": 20
        }
    },
    
    "basic": {
        "name": "Basic Student",
        "duration_days": 90,  # 3 months
        "price": 599,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,  # All 40 scenarios
            "interactive_learning": True,  # All quizzes
            "ai_tutor": "limited",  # 10 questions per day
            "certification_exam": False,  # Must purchase separately
            "cv_builder": True,
            "job_interview_prep": True,
            "interactive_reports": False,
            "pas_practice": False,
            "breach_calculator": "limited",
            "jobs_board": False
        },
        "limits": {
            "training_scenarios": 40,
            "quizzes_per_day": 50,
            "ai_questions_per_day": 10,
            "validations_per_day": 100
        }
    },
    
    "professional": {
        "name": "Professional Student",
        "duration_days": 180,  # 6 months
        "price": 999,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,  # Unlimited
            "certification_exam": False,  # Must purchase separately
            "cv_builder": True,
            "job_interview_prep": True,
            "interactive_reports": True,
            "pas_practice": True,  # Access to PAS system
            "breach_calculator": True,  # Full batch processing
            "jobs_board": True
        },
        "limits": {
            "training_scenarios": "unlimited",
            "quizzes_per_day": "unlimited",
            "ai_questions_per_day": "unlimited",
            "validations_per_day": "unlimited"
        }
    },
    
    "ultimate": {
        "name": "Ultimate Package",
        "duration_days": 365,  # 1 year
        "price": 1499,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,  # Included!
            "cv_builder": True,
            "job_interview_prep": True,
            "interactive_reports": True,
            "pas_practice": True,
            "breach_calculator": True,
            "jobs_board": True,
            "priority_support": True,
            "video_lessons": True
        },
        "limits": {
            "training_scenarios": "unlimited",
            "quizzes_per_day": "unlimited",
            "ai_questions_per_day": "unlimited",
            "validations_per_day": "unlimited",
            "certification_attempts": 3
        }
    },
    
    "nhs_trust": {
        "name": "NHS Trust License",
        "duration_days": 365,
        "price": 5000,  # Per trust
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "interactive_reports": True,
            "pas_practice": True,
            "breach_calculator": True,
            "jobs_board": True,
            "admin_dashboard": True,
            "bulk_user_management": True,
            "custom_branding": False  # Add-on
        },
        "limits": {
            "max_students": 50,
            "training_scenarios": "unlimited",
            "quizzes_per_day": "unlimited",
            "ai_questions_per_day": "unlimited",
            "validations_per_day": "unlimited"
        }
    },
    
    "admin": {
        "name": "Administrator",
        "duration_days": 9999,
        "price": 0,
        "features": {
            "pathway_validator": True,
            "clinic_letter_interpreter": True,
            "training_library": True,
            "interactive_learning": True,
            "ai_tutor": True,
            "certification_exam": True,
            "cv_builder": True,
            "job_interview_prep": True,
            "interactive_reports": True,
            "pas_practice": True,
            "breach_calculator": True,
            "jobs_board": True,
            "admin_dashboard": True,
            "user_management": True,
            "analytics": True,
            "all_features": True
        },
        "limits": {}
    }
}


# ============================================
# USER LICENSE CLASS
# ============================================

class UserLicense:
    """Manage individual user license and permissions"""
    
    def __init__(self, user_id, email, role="trial", start_date=None, custom_expiry=None):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.start_date = start_date or datetime.now()
        
        # Calculate expiry
        if custom_expiry:
            self.expiry_date = custom_expiry
        else:
            duration = ROLES[role]["duration_days"]
            self.expiry_date = self.start_date + timedelta(days=duration)
        
        # Usage tracking
        self.usage = {
            "ai_questions_today": 0,
            "quizzes_today": 0,
            "validations_today": 0,
            "last_reset_date": datetime.now().date(),
            "certification_attempts": 0,
            "total_logins": 0,
            "last_login": None
        }
    
    def is_active(self):
        """Check if license is still active"""
        return datetime.now() <= self.expiry_date
    
    def days_remaining(self):
        """Get days remaining on license"""
        if not self.is_active():
            return 0
        delta = self.expiry_date - datetime.now()
        return delta.days
    
    def has_feature(self, feature_name):
        """Check if user has access to a feature"""
        if not self.is_active():
            return False
        
        role_features = ROLES[self.role]["features"]
        
        if feature_name not in role_features:
            return False
        
        feature_access = role_features[feature_name]
        
        # Full access
        if feature_access is True:
            return True
        
        # No access
        if feature_access is False:
            return False
        
        # Limited access - check daily limits
        if feature_access == "limited":
            return self._check_usage_limit(feature_name)
        
        return False
    
    def _check_usage_limit(self, feature_name):
        """Check if user has exceeded daily usage limits"""
        # Reset daily counters if new day
        today = datetime.now().date()
        if self.usage["last_reset_date"] != today:
            self.usage["ai_questions_today"] = 0
            self.usage["quizzes_today"] = 0
            self.usage["validations_today"] = 0
            self.usage["last_reset_date"] = today
        
        limits = ROLES[self.role]["limits"]
        
        # AI Tutor check
        if "ai_tutor" in feature_name or "ai_questions" in feature_name:
            if "ai_questions_per_day" in limits:
                limit = limits["ai_questions_per_day"]
                if limit == "unlimited":
                    return True
                return self.usage["ai_questions_today"] < limit
        
        # Quiz check
        if "quiz" in feature_name or "interactive_learning" in feature_name:
            if "quizzes_per_day" in limits:
                limit = limits["quizzes_per_day"]
                if limit == "unlimited":
                    return True
                return self.usage["quizzes_today"] < limit
        
        # Validation check
        if "validator" in feature_name or "pathway" in feature_name:
            if "validations_per_day" in limits:
                limit = limits["validations_per_day"]
                if limit == "unlimited":
                    return True
                return self.usage["validations_today"] < limit
        
        return True
    
    def increment_usage(self, feature_type):
        """Increment usage counter"""
        if feature_type == "ai_question":
            self.usage["ai_questions_today"] += 1
        elif feature_type == "quiz":
            self.usage["quizzes_today"] += 1
        elif feature_type == "validation":
            self.usage["validations_today"] += 1
        elif feature_type == "certification_attempt":
            self.usage["certification_attempts"] += 1
    
    def get_usage_summary(self):
        """Get usage summary for display"""
        limits = ROLES[self.role]["limits"]
        
        summary = {
            "role": ROLES[self.role]["name"],
            "status": "Active" if self.is_active() else "Expired",
            "days_remaining": self.days_remaining(),
            "expiry_date": self.expiry_date.strftime("%d/%m/%Y"),
            "usage_today": {}
        }
        
        # AI Questions
        if "ai_questions_per_day" in limits:
            limit = limits["ai_questions_per_day"]
            used = self.usage["ai_questions_today"]
            summary["usage_today"]["AI Questions"] = f"{used}/{limit if limit != 'unlimited' else '∞'}"
        
        # Quizzes
        if "quizzes_per_day" in limits:
            limit = limits["quizzes_per_day"]
            used = self.usage["quizzes_today"]
            summary["usage_today"]["Quizzes"] = f"{used}/{limit if limit != 'unlimited' else '∞'}"
        
        # Validations
        if "validations_per_day" in limits:
            limit = limits["validations_per_day"]
            used = self.usage["validations_today"]
            summary["usage_today"]["Validations"] = f"{used}/{limit if limit != 'unlimited' else '∞'}"
        
        return summary
    
    def upgrade_role(self, new_role, extend_expiry=True):
        """Upgrade user to new role"""
        old_expiry = self.expiry_date
        self.role = new_role
        
        if extend_expiry:
            # Extend expiry by new role duration
            duration = ROLES[new_role]["duration_days"]
            self.expiry_date = datetime.now() + timedelta(days=duration)
        else:
            # Keep same expiry
            self.expiry_date = old_expiry
    
    def extend_license(self, days):
        """Extend license by X days"""
        self.expiry_date += timedelta(days=days)
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "role": self.role,
            "start_date": self.start_date.isoformat(),
            "expiry_date": self.expiry_date.isoformat(),
            "usage": self.usage
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        license = cls(
            user_id=data["user_id"],
            email=data["email"],
            role=data["role"],
            start_date=datetime.fromisoformat(data["start_date"]),
            custom_expiry=datetime.fromisoformat(data["expiry_date"])
        )
        license.usage = data.get("usage", license.usage)
        return license


# ============================================
# LICENSE KEY GENERATION
# ============================================

def generate_license_key(email, role, duration_days):
    """Generate unique license key"""
    # Create unique string
    unique_string = f"{email}_{role}_{duration_days}_{datetime.now().timestamp()}"
    
    # Hash it
    hash_obj = hashlib.sha256(unique_string.encode())
    hash_hex = hash_obj.hexdigest()[:16].upper()
    
    # Format as license key: XXXX-XXXX-XXXX-XXXX
    key_parts = [hash_hex[i:i+4] for i in range(0, 16, 4)]
    license_key = "-".join(key_parts)
    
    return license_key


def validate_license_key(license_key, expected_email=None):
    """Validate license key format"""
    # Remove spaces and dashes
    clean_key = license_key.replace("-", "").replace(" ", "")
    
    # Check length (16 characters)
    if len(clean_key) != 16:
        return False
    
    # Check if hex
    try:
        int(clean_key, 16)
        return True
    except ValueError:
        return False


# ============================================
# FEATURE ACCESS CHECKER
# ============================================

def check_feature_access(user_license, feature_name):
    """
    Check if user has access to a feature
    Returns: (has_access: bool, message: str)
    """
    if not user_license:
        return False, "No active license found"
    
    if not user_license.is_active():
        return False, f"License expired on {user_license.expiry_date.strftime('%d/%m/%Y')}"
    
    if not user_license.has_feature(feature_name):
        role_name = ROLES[user_license.role]["name"]
        return False, f"Feature not available in {role_name}. Upgrade required."
    
    return True, "Access granted"


# ============================================
# UPGRADE PATHS
# ============================================

UPGRADE_PATHS = {
    "trial_to_basic": {
        "from": "trial",
        "to": "basic",
        "price": 599,
        "discount": 0
    },
    "trial_to_professional": {
        "from": "trial",
        "to": "professional",
        "price": 999,
        "discount": 0
    },
    "trial_to_ultimate": {
        "from": "trial",
        "to": "ultimate",
        "price": 1499,
        "discount": 100  # £100 off for trial users
    },
    "basic_to_professional": {
        "from": "basic",
        "to": "professional",
        "price": 400,  # Difference
        "discount": 0
    },
    "basic_to_ultimate": {
        "from": "basic",
        "to": "ultimate",
        "price": 900,  # Difference
        "discount": 50
    },
    "professional_to_ultimate": {
        "from": "professional",
        "to": "ultimate",
        "price": 500,  # Difference
        "discount": 0
    }
}


def get_upgrade_price(current_role, target_role):
    """Calculate upgrade price"""
    upgrade_key = f"{current_role}_to_{target_role}"
    
    if upgrade_key in UPGRADE_PATHS:
        upgrade = UPGRADE_PATHS[upgrade_key]
        final_price = upgrade["price"] - upgrade["discount"]
        return final_price, upgrade["discount"]
    
    # No upgrade path - full price
    return ROLES[target_role]["price"], 0
