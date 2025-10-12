"""
T21 DATA MIGRATION UTILITY
One-time script to migrate data from old JSON files to the new Supabase database.
"""

import json
import os
import streamlit as st

# Import Supabase functions
try:
    from supabase_database import (
        add_ptl_patient,
        add_cancer_patient,
        create_mdt_meeting,
        create_clinic_template,
        create_appointment,
        create_correspondence,
        create_diary_event,
        create_audit_log
    )
    SUPABASE_ENABLED = True
except ImportError as e:
    SUPABASE_ENABLED = False
    print(f"Migration Error: Supabase not available. {e}")

def get_current_user_email():
    """Get current logged-in user's email"""
    return st.session_state.get('user_email', 'demo@t21services.co.uk')

def run_full_migration():
    """Runs the full data migration for all modules."""
    if not SUPABASE_ENABLED:
        st.error("Cannot run migration: Supabase connection is not configured.")
        return False

    user_email = get_current_user_email()
    results = {}

    st.info("Starting data migration... This may take a few moments.")

    # 1. PTL Patients
    results['ptl'] = migrate_ptl_data(user_email)
    
    # 2. Cancer Patients
    results['cancer'] = migrate_cancer_data(user_email)
    
    # 3. MDT Meetings
    results['mdt'] = migrate_mdt_data(user_email)
    
    # 4. Clinics and Appointments
    results['clinics'] = migrate_clinics_data(user_email)
    results['appointments'] = migrate_appointments_data(user_email)

    st.success("✅ Data migration complete!")
    st.json(results)
    return True

def migrate_ptl_data(user_email):
    """Migrates ptl_patients.json to Supabase."""
    filename = "ptl_patients.json"
    if not os.path.exists(filename):
        return {"status": "skipped", "reason": "File not found"}

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for patient in data.get('patients', []):
        # Ensure user_email is set for the new record
        patient['user_email'] = user_email
        add_ptl_patient(user_email, patient)
        count += 1
    
    st.write(f"- Migrated {count} PTL patients.")
    return {"status": "completed", "migrated_count": count}

def migrate_cancer_data(user_email):
    """Migrates cancer_ptl.json to Supabase."""
    filename = "cancer_ptl.json"
    if not os.path.exists(filename):
        return {"status": "skipped", "reason": "File not found"}

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for patient in data.get('patients', []):
        patient['user_email'] = user_email
        add_cancer_patient(user_email, patient)
        count += 1

    st.write(f"- Migrated {count} cancer patients.")
    return {"status": "completed", "migrated_count": count}

def migrate_mdt_data(user_email):
    """Migrates mdt_meetings.json to Supabase."""
    filename = "mdt_meetings.json"
    if not os.path.exists(filename):
        return {"status": "skipped", "reason": "File not found"}

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for meeting in data.get('meetings', []):
        meeting['user_email'] = user_email
        create_mdt_meeting(user_email, meeting)
        count += 1

    st.write(f"- Migrated {count} MDT meetings.")
    return {"status": "completed", "migrated_count": count}

def migrate_clinics_data(user_email):
    """Migrates clinics.json to Supabase."""
    filename = "clinics.json"
    if not os.path.exists(filename):
        return {"status": "skipped", "reason": "File not found"}

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for clinic in data.get('clinics', []):
        clinic['user_email'] = user_email
        create_clinic_template(user_email, clinic)
        count += 1

    st.write(f"- Migrated {count} clinic templates.")
    return {"status": "completed", "migrated_count": count}

def migrate_appointments_data(user_email):
    """Migrates appointments.json to Supabase."""
    filename = "appointments.json"
    if not os.path.exists(filename):
        return {"status": "skipped", "reason": "File not found"}

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for appt in data.get('appointments', []):
        appt['user_email'] = user_email
        create_appointment(user_email, appt)
        count += 1

    st.write(f"- Migrated {count} appointments.")
    return {"status": "completed", "migrated_count": count}
