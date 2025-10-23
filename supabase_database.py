"""
T21 SERVICES - SUPABASE DATABASE CONNECTION
Professional database connection for persistent user storage
"""

from supabase import create_client, Client
from datetime import datetime
import streamlit as st

# Try to get credentials from Streamlit secrets first, then from config file
SUPABASE_AVAILABLE = False
supabase = None

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    SUPABASE_AVAILABLE = True
except Exception as e:
    # Fallback to config file for local testing
    try:
        from supabase_config_SAFE import SUPABASE_URL, SUPABASE_SERVICE_KEY
        SUPABASE_KEY = SUPABASE_SERVICE_KEY
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        SUPABASE_AVAILABLE = True
    except Exception:
        # Supabase not available - system will work without it (degraded mode)
        print("⚠️ Supabase not configured. System running in local mode.")
        supabase = None
        SUPABASE_AVAILABLE = False


# ============================================
# PTL SYSTEM - PERMANENT STUDENT STORAGE
# ============================================

def add_ptl_patient(user_email, patient_data):
    """Add patient to PTL for specific user - PERMANENT STORAGE"""
    if not SUPABASE_AVAILABLE or supabase is None:
        return False, "Supabase not configured"
    
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
    if not SUPABASE_AVAILABLE or supabase is None:
        return []
    
    print(f"DEBUG: Fetching PTL patients for {user_email}")
    try:
        result = supabase.table('ptl_patients').select('*').eq('user_email', user_email).execute()
        
        # Detailed logging of the result
        print(f"DEBUG: Supabase query result for {user_email}: {result}")
        
        if hasattr(result, 'data') and isinstance(result.data, list):
            print(f"SUCCESS: Found {len(result.data)} patients for {user_email}.")
            return result.data
        else:
            print(f"WARNING: No data found or incorrect format for {user_email}. Result: {result}")
            return []
            
    except Exception as e:
        print(f"CRITICAL ERROR in get_ptl_patients_for_user: {e}")
        # Also print the Supabase client details to check if it's initialized
        print(f"DEBUG: Supabase client object: {supabase}")
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
# CANCER PATHWAY MODULE - PERMANENT STORAGE
# ============================================

def add_cancer_patient(user_email, patient_data):
    """Add a cancer patient for a specific user."""
    try:
        patient_data['user_email'] = user_email
        patient_data['created_at'] = datetime.now().isoformat()
        patient_data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('cancer_pathways').insert(patient_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_cancer_patients_for_user(user_email):
    """Get all cancer patients for a specific user."""
    try:
        result = supabase.table('cancer_pathways').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting cancer patients: {e}")
        return []

def update_cancer_patient(patient_id, user_email, updates):
    """Update a cancer patient's details."""
    try:
        updates['updated_at'] = datetime.now().isoformat()
        result = supabase.table('cancer_pathways').update(updates).eq('pathway_id', patient_id).eq('user_email', user_email).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def delete_cancer_patient(patient_id, user_email):
    """Delete a cancer patient."""
    try:
        supabase.table('cancer_pathways').delete().eq('pathway_id', patient_id).eq('user_email', user_email).execute()
        return True
    except Exception as e:
        return False, str(e)


# ============================================
# MDT COORDINATION MODULE - PERMANENT STORAGE
# ============================================

def create_mdt_meeting(user_email, meeting_data):
    """Create a new MDT meeting for a specific user."""
    try:
        meeting_data['user_email'] = user_email
        result = supabase.table('mdt_meetings').insert(meeting_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_mdt_meetings_for_user(user_email):
    """Get all MDT meetings for a specific user."""
    try:
        result = supabase.table('mdt_meetings').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting MDT meetings: {e}")
        return []

def update_mdt_meeting(user_email, meeting_id, updates):
    """Update an MDT meeting's details."""
    try:
        updates['updated_at'] = datetime.now().isoformat()  # FIXED: Was 'last_updated'
        result = supabase.table('mdt_meetings').update(updates).eq('meeting_id', meeting_id).eq('user_email', user_email).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def delete_mdt_meeting(user_email, meeting_id):
    """Delete an MDT meeting."""
    try:
        supabase.table('mdt_meetings').delete().eq('meeting_id', meeting_id).eq('user_email', user_email).execute()
        return True
    except Exception as e:
        return False, str(e)


# ============================================
# ADVANCED BOOKING SYSTEM - PERMANENT STORAGE
# ============================================

def create_clinic_template(user_email, clinic_data):
    """Create a new clinic template for a specific user."""
    try:
        clinic_data['user_email'] = user_email
        result = supabase.table('clinics').insert(clinic_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_clinics_for_user(user_email):
    """Get all clinic templates for a specific user."""
    try:
        result = supabase.table('clinics').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting clinics: {e}")
        return []

def create_appointment(user_email, appointment_data):
    """Create a new appointment for a specific user."""
    try:
        appointment_data['user_email'] = user_email
        print(f"🔍 Attempting to insert appointment: {appointment_data}")
        result = supabase.table('appointments').insert(appointment_data).execute()
        print(f"✅ Insert successful: {result.data}")
        return True, result.data[0] if result.data else None
    except Exception as e:
        print(f"❌ Insert failed: {str(e)}")
        print(f"📋 Appointment data that failed: {appointment_data}")
        return False, str(e)

def get_appointments_for_user(user_email):
    """Get all appointments for a specific user."""
    try:
        result = supabase.table('appointments').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting appointments: {e}")
        return []

def update_appointment(user_email, appointment_id, updates):
    """Update an appointment's details."""
    try:
        updates['updated_at'] = datetime.now().isoformat()  # FIXED: Was 'last_updated'
        result = supabase.table('appointments').update(updates).eq('appointment_id', appointment_id).eq('user_email', user_email).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)


# ============================================
# MEDICAL SECRETARY AI - PERMANENT STORAGE
# ============================================

def create_correspondence(user_email, letter_data):
    """Create a new correspondence letter for a specific user."""
    try:
        letter_data['user_email'] = user_email
        result = supabase.table('correspondence').insert(letter_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_correspondence_for_user(user_email):
    """Get all correspondence for a specific user."""
    try:
        result = supabase.table('correspondence').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting correspondence: {e}")
        return []

def create_diary_event(user_email, event_data):
    """Create a new diary event for a specific user."""
    try:
        event_data['user_email'] = user_email
        result = supabase.table('diary_events').insert(event_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_diary_events_for_user(user_email):
    """Get all diary events for a specific user."""
    try:
        result = supabase.table('diary_events').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting diary events: {e}")
        return []


# ============================================
# DATA QUALITY SYSTEM - PERMANENT STORAGE
# ============================================

def create_audit_log(user_email, audit_data):
    """Create a new audit log entry for a specific user."""
    try:
        audit_data['user_email'] = user_email
        result = supabase.table('audit_log').insert(audit_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_audit_logs_for_user(user_email):
    """Get all audit logs for a specific user."""
    try:
        result = supabase.table('audit_log').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting audit logs: {e}")
        return []


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


# ============================================
# TASK MANAGEMENT - PERMANENT STORAGE
# ============================================

def create_task(user_email, task_data):
    """Create a new task for a specific user."""
    try:
        task_data['user_email'] = user_email
        result = supabase.table('tasks').insert(task_data).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_tasks_for_user(user_email):
    """Get all tasks for a specific user."""
    try:
        result = supabase.table('tasks').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting tasks: {e}")
        return []

def update_task(user_email, task_id, updates):
    """Update a task's details."""
    try:
        updates['updated_at'] = datetime.now().isoformat()
        result = supabase.table('tasks').update(updates).eq('task_id', task_id).eq('user_email', user_email).execute()
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def delete_task(user_email, task_id):
    """Delete a task."""
    try:
        supabase.table('tasks').delete().eq('task_id', task_id).eq('user_email', user_email).execute()
        return True
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False

# Aliases for consistency
supabase_create_task = create_task
supabase_get_tasks_for_user = get_tasks_for_user
supabase_update_task = update_task
supabase_delete_task = delete_task


# ============================================
# DOCUMENT MANAGEMENT - PERMANENT STORAGE
# ============================================

def upload_document(user_email, document_id, file_data, filename, document_metadata):
    """Upload document to Supabase Storage and save metadata"""
    try:
        # Upload file to Supabase Storage bucket
        storage_path = f"{user_email}/{document_id}/{filename}"
        
        # Upload to storage
        supabase.storage.from_('documents').upload(
            path=storage_path,
            file=file_data,
            file_options={"content-type": "application/octet-stream"}
        )
        
        # Save metadata to database
        document_metadata['user_email'] = user_email
        document_metadata['storage_path'] = storage_path
        result = supabase.table('documents').insert(document_metadata).execute()
        
        return True, result.data[0] if result.data else None
    except Exception as e:
        return False, str(e)

def get_documents_for_patient(user_email, patient_nhs):
    """Get all documents for a specific patient"""
    try:
        result = supabase.table('documents').select('*').eq('user_email', user_email).eq('patient_nhs', patient_nhs).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting patient documents: {e}")
        return []

def get_all_documents_for_user(user_email):
    """Get all documents for a user"""
    try:
        result = supabase.table('documents').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting documents: {e}")
        return []

def delete_document(user_email, document_id):
    """Delete a document and its file"""
    try:
        # Get document to find storage path
        doc_result = supabase.table('documents').select('storage_path').eq('document_id', document_id).eq('user_email', user_email).execute()
        
        if doc_result.data:
            storage_path = doc_result.data[0].get('storage_path')
            
            # Delete from storage
            if storage_path:
                try:
                    supabase.storage.from_('documents').remove([storage_path])
                except:
                    pass  # Continue even if storage delete fails
            
            # Delete from database
            supabase.table('documents').delete().eq('document_id', document_id).eq('user_email', user_email).execute()
            return True
        
        return False
    except Exception as e:
        print(f"Error deleting document: {e}")
        return False

def download_document(user_email, document_id):
    """Download document file data"""
    try:
        # Get storage path
        doc_result = supabase.table('documents').select('storage_path').eq('document_id', document_id).eq('user_email', user_email).execute()
        
        if doc_result.data:
            storage_path = doc_result.data[0].get('storage_path')
            
            # Download from storage
            file_data = supabase.storage.from_('documents').download(storage_path)
            return file_data
        
        return None
    except Exception as e:
        print(f"Error downloading document: {e}")
        return None

# Aliases
supabase_upload_document = upload_document
supabase_get_documents_for_patient = get_documents_for_patient
supabase_get_all_documents = get_all_documents_for_user
supabase_delete_document = delete_document
supabase_download_document = download_document


if __name__ == "__main__":
    # Test connection when run directly
    print("Testing Supabase connection...")
    test_connection()
