"""
T21 SERVICES - SUPABASE DATABASE CONNECTION
Professional database connection for persistent user storage
"""

from supabase import create_client, Client
from datetime import datetime
import streamlit as st

# Try to get credentials from Streamlit secrets first, then from config file
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["service_key"]
except:
    # Fallback to config file for local testing
    try:
        from supabase_config_SAFE import SUPABASE_URL, SUPABASE_SERVICE_KEY
        SUPABASE_KEY = SUPABASE_SERVICE_KEY
    except ImportError:
        raise Exception("Supabase credentials not found! Add to Streamlit secrets or supabase_config_SAFE.py")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================
# PTL SYSTEM - PERMANENT STUDENT STORAGE
# ============================================

def add_ptl_patient(user_email, patient_data):
    """Add patient to PTL for specific user - PERMANENT STORAGE"""
    try:
        patient_data['user_email'] = user_email
        patient_data['created_at'] = datetime.now().isoformat()
        patient_data['updated_at'] = datetime.now().isoformat()
        
        result = supabase.table('ptl_patients').insert(patient_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)


def get_ptl_patients_for_user(user_email):
    """Get all PTL patients for specific user - ONLY THEIR DATA"""
    try:
        result = supabase.table('ptl_patients').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting PTL patients: {e}")
        return []


def get_ptl_patient_by_id(patient_id, user_email):
    """Get specific patient - ONLY if belongs to user"""
    try:
        result = supabase.table('ptl_patients').select('*').eq('patient_id', patient_id).eq('user_email', user_email).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error getting patient: {e}")
        return None


def update_ptl_patient(patient_id, user_email, updates):
    """Update patient - ONLY if belongs to user"""
    try:
        updates['updated_at'] = datetime.now().isoformat()
        result = supabase.table('ptl_patients').update(updates).eq('patient_id', patient_id).eq('user_email', user_email).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)


def delete_ptl_patient(patient_id, user_email):
    """Delete patient - ONLY if belongs to user"""
    try:
        result = supabase.table('ptl_patients').delete().eq('patient_id', patient_id).eq('user_email', user_email).execute()
        return True
    except Exception as e:
        return False


def get_ptl_stats_for_user(user_email):
    """Get PTL statistics for user's data only"""
    try:
        patients = get_ptl_patients_for_user(user_email)
        
        total = len(patients)
        active_breaches = sum(1 for p in patients if p.get('clock_status') == 'BREACH')
        
        # Calculate average wait
        from datetime import datetime as dt
        total_days = 0
        max_days = 0
        
        for p in patients:
            try:
                start_date = dt.fromisoformat(p.get('clock_start_date', ''))
                days = (dt.now() - start_date).days
                total_days += days
                max_days = max(max_days, days)
            except:
                pass
        
        avg_weeks = (total_days / total / 7) if total > 0 else 0
        max_weeks = max_days / 7
        
        return {
            'total_patients': total,
            'active_breaches': active_breaches,
            'avg_wait_weeks': round(avg_weeks, 1),
            'max_wait_weeks': round(max_weeks, 1)
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {
            'total_patients': 0,
            'active_breaches': 0,
            'avg_wait_weeks': 0,
            'max_wait_weeks': 0
        }


def create_user(email, password_hash, full_name, role="trial", user_type="student"):
    """Create new user in Supabase"""
    try:
        from datetime import timedelta
        
        # Calculate expiry date based on role
        expiry_days = {
            "trial": 2,
            "student_basic": 90,
            "student_professional": 180,
            "student_ultimate": 365,
            "staff": 3650,
            "admin": 3650,
            "super_admin": 3650
        }
        
        expiry_date = datetime.now() + timedelta(days=expiry_days.get(role, 2))
        
        data = {
            "email": email,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": role,
            "user_type": user_type,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "expiry_date": expiry_date.isoformat()
        }
        
        result = supabase.table("users").insert(data).execute()
        return True, "User created successfully!"
    
    except Exception as e:
        return False, f"Error creating user: {str(e)}"


def get_user_by_email(email):
    """Get user by email"""
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def get_all_users():
    """Get all users"""
    try:
        result = supabase.table("users").select("*").execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting users: {e}")
        return []


def update_user_last_login(email):
    """Update user's last login time"""
    try:
        supabase.table("users").update({
            "last_login": datetime.now().isoformat()
        }).eq("email", email).execute()
        return True
    except Exception as e:
        print(f"Error updating last login: {e}")
        return False


def track_user_login(email, success, ip_address=None, city=None, country=None, device=None, browser=None):
    """Track user login attempt"""
    try:
        data = {
            "user_email": email,
            "login_time": datetime.now().isoformat(),
            "success": success,
            "ip_address": ip_address,
            "city": city,
            "country": country,
            "device": device,
            "browser": browser
        }
        supabase.table("user_tracking").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error tracking login: {e}")
        return False


def grant_module_access(user_email, module_name, granted_by):
    """Grant module access to user"""
    try:
        data = {
            "user_email": user_email,
            "module_name": module_name,
            "granted_at": datetime.now().isoformat(),
            "granted_by": granted_by
        }
        supabase.table("module_access").insert(data).execute()
        return True, "Module access granted!"
    except Exception as e:
        return False, f"Error granting access: {str(e)}"


def get_user_modules(user_email):
    """Get all modules user has access to"""
    try:
        result = supabase.table("module_access").select("module_name").eq("user_email", user_email).execute()
        if result.data:
            return [item["module_name"] for item in result.data]
        return []
    except Exception as e:
        print(f"Error getting modules: {e}")
        return []


def revoke_module_access(user_email, module_name):
    """Revoke module access from user"""
    try:
        supabase.table("module_access").delete().eq("user_email", user_email).eq("module_name", module_name).execute()
        return True, "Module access revoked!"
    except Exception as e:
        return False, f"Error revoking access: {str(e)}"


# Test connection
def test_connection():
    """Test Supabase connection"""
    try:
        result = supabase.table("users").select("count", count="exact").execute()
        print(f"✅ Supabase connected! {result.count} users in database.")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


# ============================================
# TWO-FACTOR AUTHENTICATION (2FA) FUNCTIONS
# ============================================

def enable_2fa(email, secret, backup_codes):
    """
    Enable 2FA for a user
    
    Args:
        email: User email
        secret: TOTP secret (base32)
        backup_codes: List of backup codes
    
    Returns:
        bool: Success status
    """
    try:
        import json
        supabase.table("users").update({
            "two_factor_secret": secret,
            "two_factor_backup_codes": json.dumps(backup_codes),
            "two_factor_enabled": True,
            "two_factor_enabled_at": datetime.now().isoformat()
        }).eq("email", email).execute()
        return True
    except Exception as e:
        print(f"Error enabling 2FA: {e}")
        return False


def disable_2fa(email):
    """Disable 2FA for a user"""
    try:
        supabase.table("users").update({
            "two_factor_secret": None,
            "two_factor_backup_codes": None,
            "two_factor_enabled": False
        }).eq("email", email).execute()
        return True
    except Exception as e:
        print(f"Error disabling 2FA: {e}")
        return False


def use_backup_code(email, code):
    """
    Use a backup code and remove it from the list
    
    Args:
        email: User email
        code: Backup code to use
    
    Returns:
        bool: True if code was valid and used
    """
    try:
        import json
        user = get_user_by_email(email)
        if not user or not user.get('two_factor_backup_codes'):
            return False
        
        backup_codes = json.loads(user['two_factor_backup_codes'])
        
        if code in backup_codes:
            # Remove used code
            backup_codes.remove(code)
            
            # Update database
            supabase.table("users").update({
                "two_factor_backup_codes": json.dumps(backup_codes)
            }).eq("email", email).execute()
            
            return True
        
        return False
    except Exception as e:
        print(f"Error using backup code: {e}")
        return False


if __name__ == "__main__":
    # Test connection when run directly
    print("Testing Supabase connection...")
    test_connection()
