"""
MASTER DATABASE SCHEMA - SINGLE SOURCE OF TRUTH
This file defines ALL field names used in the database
Use these constants throughout the codebase to prevent mismatches
"""

# ============================================
# PTL PATIENTS TABLE
# ============================================
PTL_TABLE = 'ptl_patients'
PTL_FIELDS = {
    'id': 'id',
    'patient_id': 'patient_id',
    'user_email': 'user_email',
    'patient_name': 'patient_name',
    'nhs_number': 'nhs_number',
    'specialty': 'specialty',
    'referral_date': 'referral_date',
    'referral_source': 'referral_source',
    'clock_start_date': 'clock_start_date',
    'pathway_type': 'pathway_type',
    'priority': 'priority',
    'current_status': 'current_status',
    'consultant': 'consultant',
    'contact_number': 'contact_number',
    'rtt_code': 'rtt_code',
    'clock_status': 'clock_status',
    'notes': 'notes',
    'added_date': 'added_date',
    'last_updated': 'last_updated',
    'appointments': 'appointments',
    'events': 'events',
    'created_at': 'created_at'
}

# ============================================
# CANCER PATHWAYS TABLE
# ============================================
CANCER_TABLE = 'cancer_pathways'
CANCER_FIELDS = {
    'id': 'id',
    'pathway_id': 'pathway_id',  # NOT patient_id!
    'user_email': 'user_email',
    'patient_name': 'patient_name',
    'nhs_number': 'nhs_number',
    'cancer_type': 'cancer_type',
    'referral_date': 'referral_date',
    'pathway_type': 'pathway_type',
    'clock_start_date': 'clock_start_date',  # NOT pathway_start_date!
    'target_date': 'target_date',
    'current_status': 'current_status',
    'milestones': 'milestones',
    'treatments': 'treatments',  # NOT appointments/diagnostics!
    'notes': 'notes',
    'created_at': 'created_at',
    'updated_at': 'updated_at'  # NOT last_updated!
}

# ============================================
# MDT MEETINGS TABLE
# ============================================
MDT_TABLE = 'mdt_meetings'
MDT_FIELDS = {
    'id': 'id',
    'meeting_id': 'meeting_id',
    'user_email': 'user_email',
    'meeting_date': 'meeting_date',
    'meeting_time': 'meeting_time',
    'specialty': 'specialty',
    'location': 'location',
    'chair_person': 'chair_person',  # NOT chair!
    'attendees': 'attendees',
    'patients_discussed': 'patients_discussed',  # NOT patients!
    'decisions': 'decisions',  # NOT outcomes!
    'action_points': 'action_points',
    'notes': 'notes',
    'status': 'status',
    'created_at': 'created_at',
    'updated_at': 'updated_at'  # NOT last_updated!
}

# ============================================
# APPOINTMENTS TABLE
# ============================================
APPOINTMENTS_TABLE = 'appointments'
APPOINTMENTS_FIELDS = {
    'id': 'id',
    'appointment_id': 'appointment_id',
    'user_email': 'user_email',
    'patient_id': 'patient_id',
    'patient_name': 'patient_name',
    'nhs_number': 'nhs_number',
    'appointment_date': 'appointment_date',
    'appointment_time': 'appointment_time',
    'specialty': 'specialty',
    'clinic_location': 'clinic_location',
    'appointment_type': 'appointment_type',
    'consultant': 'consultant',
    'status': 'status',
    'notes': 'notes',
    'created_at': 'created_at',
    'updated_at': 'updated_at'
}

# ============================================
# VALIDATION HISTORY TABLE
# ============================================
VALIDATION_TABLE = 'validation_history'
VALIDATION_FIELDS = {
    'id': 'id',
    'validation_id': 'validation_id',
    'user_email': 'user_email',
    'validation_type': 'validation_type',
    'patient_data': 'patient_data',
    'result': 'result',
    'is_valid': 'is_valid',
    'confidence_score': 'confidence_score',
    'issues': 'issues',
    'created_at': 'created_at'
}

# ============================================
# TRAINING PROGRESS TABLE
# ============================================
TRAINING_TABLE = 'training_progress'
TRAINING_FIELDS = {
    'id': 'id',
    'user_email': 'user_email',
    'scenario_id': 'scenario_id',
    'scenario_name': 'scenario_name',
    'completed': 'completed',
    'score': 'score',
    'time_taken': 'time_taken',
    'attempts': 'attempts',
    'completed_at': 'completed_at',
    'created_at': 'created_at'
}

# ============================================
# STATUS VALUES (STANDARDIZED)
# ============================================
STATUS_SCHEDULED = 'scheduled'
STATUS_COMPLETED = 'completed'
STATUS_CANCELLED = 'cancelled'
STATUS_IN_PROGRESS = 'in_progress'
STATUS_PENDING = 'pending'

# ============================================
# FIELD MAPPING HELPERS
# ============================================
def get_cancer_field_mapping():
    """Returns mapping of old field names to new ones for backward compatibility"""
    return {
        'patient_id': 'pathway_id',
        'pathway_start_date': 'clock_start_date',
        'last_updated': 'updated_at',
        'created_date': 'created_at'
    }

def get_mdt_field_mapping():
    """Returns mapping of old field names to new ones for backward compatibility"""
    return {
        'chair': 'chair_person',
        'patients': 'patients_discussed',
        'outcomes': 'decisions',
        'last_updated': 'updated_at',
        'created_date': 'created_at'
    }

# ============================================
# VALIDATION FUNCTIONS
# ============================================
def validate_cancer_record(record: dict) -> tuple[bool, list]:
    """Validate a cancer pathway record has all required fields"""
    required = ['pathway_id', 'user_email', 'patient_name', 'cancer_type', 'referral_date']
    missing = [f for f in required if f not in record]
    return len(missing) == 0, missing

def validate_mdt_record(record: dict) -> tuple[bool, list]:
    """Validate an MDT meeting record has all required fields"""
    required = ['meeting_id', 'meeting_date', 'specialty']
    missing = [f for f in required if f not in record]
    return len(missing) == 0, missing

def validate_ptl_record(record: dict) -> tuple[bool, list]:
    """Validate a PTL patient record has all required fields"""
    required = ['patient_id', 'user_email', 'patient_name', 'specialty']
    missing = [f for f in required if f not in record]
    return len(missing) == 0, missing
