"""
T21 PTL SYSTEM - PATIENT TRACKING LIST
Complete NHS-style Patient Tracking List for RTT Management

Features:
- View all patients awaiting treatment
- Track RTT clock status
- Monitor weeks waiting
- Identify breach risks
- Filter and search
- Export to Excel
- Real-time updates
- Color-coded alerts

This is the CORE tool NHS RTT coordinators use daily!
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Import Supabase functions for permanent storage
try:
    from supabase_database import (
        add_ptl_patient,
        get_ptl_patients_for_user,
        get_ptl_patient_by_id,
        update_ptl_patient,
        delete_ptl_patient,
        get_ptl_stats_for_user
    )
    SUPABASE_ENABLED = True
except:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available - using fallback storage")


# Database files (fallback only)
PTL_DATABASE = "ptl_patients.json"
PTL_HISTORY = "ptl_history.json"


def get_current_user_email():
    """Get current logged-in user's email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


def load_ptl():
    """Load PTL database - Now uses Supabase for permanent per-user storage"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        # Use Supabase - PERMANENT STORAGE
        patients = get_ptl_patients_for_user(user_email)
        return {'patients': patients}
    else:
        # Fallback to session/file storage
        try:
            import streamlit as st
            if 'ptl_data' not in st.session_state:
                if os.path.exists(PTL_DATABASE):
                    with open(PTL_DATABASE, 'r', encoding='utf-8') as f:
                        st.session_state.ptl_data = json.load(f)
                else:
                    st.session_state.ptl_data = {'patients': []}
            return st.session_state.ptl_data
        except:
            if os.path.exists(PTL_DATABASE):
                with open(PTL_DATABASE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {'patients': []}


def save_ptl(data):
    """Save PTL database - Now saves to Supabase permanently"""
    # Supabase saves happen in individual functions
    # This function kept for compatibility but does nothing
    pass


def generate_patient_id():
    """Generate unique patient ID"""
    return f"PTL{datetime.now().strftime('%Y%m%d%H%M%S')}"


def calculate_weeks_waiting(clock_start_date: str) -> int:
    """Calculate weeks waiting from clock start date"""
    try:
        start = datetime.fromisoformat(clock_start_date)
        now = datetime.now()
        days = (now - start).days
        return days // 7
    except:
        return 0


def calculate_days_waiting(clock_start_date: str) -> int:
    """Calculate days waiting from clock start date"""
    try:
        start = datetime.fromisoformat(clock_start_date)
        now = datetime.now()
        return (now - start).days
    except:
        return 0


def get_breach_status(days_waiting: int, pathway_type: str = "routine") -> Dict:
    """
    Determine breach status based on days waiting
    
    Returns:
        Dict with status, color, days_to_breach
    """
    
    # RTT targets
    if pathway_type == "routine":
        target_days = 126  # 18 weeks
    elif pathway_type == "2ww":
        target_days = 14  # 2 week wait
    elif pathway_type == "62day":
        target_days = 62  # Cancer 62-day
    else:
        target_days = 126
    
    days_to_breach = target_days - days_waiting
    
    if days_waiting >= target_days:
        return {
            'status': 'BREACH',
            'color': 'red',
            'days_to_breach': days_to_breach,
            'alert_level': 'CRITICAL'
        }
    elif days_to_breach <= 7:
        return {
            'status': 'IMMINENT BREACH',
            'color': 'orange',
            'days_to_breach': days_to_breach,
            'alert_level': 'HIGH'
        }
    elif days_to_breach <= 14:
        return {
            'status': 'AT RISK',
            'color': 'yellow',
            'days_to_breach': days_to_breach,
            'alert_level': 'MEDIUM'
        }
    else:
        return {
            'status': 'ON TRACK',
            'color': 'green',
            'days_to_breach': days_to_breach,
            'alert_level': 'LOW'
        }


def add_patient_to_ptl(
    patient_name: str,
    nhs_number: str,
    specialty: str,
    referral_date: str,
    referral_source: str,
    pathway_type: str = "routine",
    priority: str = "Routine",
    current_status: str = "Awaiting First Appointment",
    consultant: str = "",
    contact_number: str = "",
    notes: str = ""
) -> str:
    """
    Add patient to PTL - NOW WITH PERMANENT STORAGE!
    Saves to Supabase database with user's email
    
    Returns:
        patient_id
    """
    
    patient_id = generate_patient_id()
    user_email = get_current_user_email()
    
    patient = {
        'patient_id': patient_id,
        'patient_name': patient_name,
        'nhs_number': nhs_number,
        'specialty': specialty,
        'referral_date': referral_date,
        'referral_source': referral_source,
        'clock_start_date': referral_date,
        'pathway_type': pathway_type,
        'priority': priority,
        'current_status': current_status,
        'consultant': consultant,
        'contact_number': contact_number,
        'rtt_code': '10',  # Initial referral
        'clock_status': 'ACTIVE',
        'notes': notes,
        'added_date': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat(),
        'appointments': [],  # JSONB - store as list, not string
        'events': [{
            'date': referral_date,
            'code': '10',
            'description': f'Referral from {referral_source}',
            'added_by': user_email
        }]  # JSONB - store as list, not string
    }
    
    if SUPABASE_ENABLED:
        # Save to Supabase - PERMANENT!
        success, result = add_ptl_patient(user_email, patient)
        if success:
            return patient_id
        else:
            print(f"Error saving patient: {result}")
            return patient_id
    else:
        # Fallback to old method
        ptl = load_ptl()
        ptl['patients'].append(patient)
        save_ptl(ptl)
        return patient_id


def update_patient_status(
    patient_id: str,
    new_status: str,
    rtt_code: str = None,
    notes: str = ""
) -> bool:
    """Update patient status on PTL - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        # Update in Supabase
        updates = {
            'current_status': new_status,
            'last_updated': datetime.now().isoformat()
        }
        
        if rtt_code:
            updates['rtt_code'] = rtt_code
        
        if notes:
            # Append to existing notes
            updates['notes'] = notes
        
        # Get current patient to append to events
        patient = get_ptl_patient_by_id(patient_id, user_email)
        if patient:
            current_events = patient.get('events', [])
            current_events.append({
                'date': datetime.now().isoformat(),
                'code': rtt_code or patient.get('rtt_code', ''),
                'description': new_status,
                'notes': notes,
                'added_by': user_email
            })
            updates['events'] = current_events
        
        success, result = update_ptl_patient(patient_id, user_email, updates)
        return success
    else:
        # Fallback to old method
        ptl = load_ptl()
        
        for patient in ptl['patients']:
            if patient['patient_id'] == patient_id:
                patient['current_status'] = new_status
                if rtt_code:
                    patient['rtt_code'] = rtt_code
                if notes:
                    patient['notes'] = notes
                patient['last_updated'] = datetime.now().isoformat()
                
                patient['events'].append({
                    'date': datetime.now().isoformat(),
                    'code': rtt_code or patient['rtt_code'],
                    'description': new_status,
                    'notes': notes,
                    'added_by': 'System'
                })
                
                save_ptl(ptl)
                return True
        
        return False


def add_appointment(
    patient_id: str,
    appointment_date: str,
    appointment_type: str,
    location: str = "",
    notes: str = ""
) -> bool:
    """Add appointment to patient record"""
    
    ptl = load_ptl()
    
    for patient in ptl['patients']:
        if patient['patient_id'] == patient_id:
            appointment = {
                'date': appointment_date,
                'type': appointment_type,
                'location': location,
                'notes': notes,
                'added_date': datetime.now().isoformat()
            }
            
            patient['appointments'].append(appointment)
            patient['last_updated'] = datetime.now().isoformat()
            
            save_ptl(ptl)
            return True
    
    return False


def remove_from_ptl(patient_id: str) -> bool:
    """Remove patient from PTL - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        # Delete from Supabase
        success = delete_ptl_patient(patient_id, user_email)
        return success
    else:
        # Fallback to old method
        ptl = load_ptl()
        
        for i, patient in enumerate(ptl['patients']):
            if patient['patient_id'] == patient_id:
                # Remove from active PTL
                ptl['patients'].pop(i)
                save_ptl(ptl)
                return True
        
        return False


def archive_patient(patient: Dict, reason: str):
    """Archive patient to history"""
    
    if os.path.exists(PTL_HISTORY):
        with open(PTL_HISTORY, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = {'archived_patients': []}
    
    patient['archive_date'] = datetime.now().isoformat()
    patient['archive_reason'] = reason
    
    history['archived_patients'].append(patient)
    
    with open(PTL_HISTORY, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)


def get_all_patients() -> List[Dict]:
    """Get all patients on PTL"""
    ptl = load_ptl()
    return ptl['patients']


def get_patient_by_id(patient_id: str) -> Optional[Dict]:
    """Get specific patient"""
    ptl = load_ptl()
    for patient in ptl['patients']:
        if patient['patient_id'] == patient_id:
            return patient
    return None


def search_patients(
    query: str = "",
    specialty: str = None,
    priority: str = None,
    breach_risk: str = None,
    status: str = None
) -> List[Dict]:
    """
    Search and filter PTL
    
    Args:
        query: Search term (name, NHS number)
        specialty: Filter by specialty
        priority: Filter by priority
        breach_risk: Filter by breach risk (HIGH, MEDIUM, LOW)
        status: Filter by current status
    """
    
    patients = get_all_patients()
    results = []
    
    for patient in patients:
        # Text search
        if query:
            query_lower = query.lower()
            if (query_lower not in patient['patient_name'].lower() and
                query_lower not in patient['nhs_number'].lower()):
                continue
        
        # Specialty filter
        if specialty and patient['specialty'] != specialty:
            continue
        
        # Priority filter
        if priority and patient['priority'] != priority:
            continue
        
        # Status filter
        if status and patient['current_status'] != status:
            continue
        
        # Breach risk filter
        if breach_risk:
            days = calculate_days_waiting(patient['clock_start_date'])
            breach_status = get_breach_status(days, patient.get('pathway_type', 'routine'))
            if breach_status['alert_level'] != breach_risk:
                continue
        
        results.append(patient)
    
    return results


def get_ptl_stats() -> Dict:
    """Get PTL statistics"""
    
    patients = get_all_patients()
    
    stats = {
        'total_patients': len(patients),
        'specialties': {},
        'priorities': {},
        'breach_risks': {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        },
        'avg_weeks_waiting': 0,
        'longest_wait_weeks': 0,
        'breaches': 0
    }
    
    if not patients:
        return stats
    
    total_days = 0
    max_days = 0
    
    for patient in patients:
        # Specialty count
        specialty = patient['specialty']
        stats['specialties'][specialty] = stats['specialties'].get(specialty, 0) + 1
        
        # Priority count
        priority = patient['priority']
        stats['priorities'][priority] = stats['priorities'].get(priority, 0) + 1
        
        # Calculate waiting time
        days = calculate_days_waiting(patient['clock_start_date'])
        total_days += days
        if days > max_days:
            max_days = days
        
        # Breach status
        breach_status = get_breach_status(days, patient.get('pathway_type', 'routine'))
        stats['breach_risks'][breach_status['alert_level']] += 1
        
        if breach_status['status'] == 'BREACH':
            stats['breaches'] += 1
    
    stats['avg_weeks_waiting'] = (total_days // len(patients)) // 7
    stats['longest_wait_weeks'] = max_days // 7
    
    return stats


def export_ptl_to_csv() -> str:
    """Export PTL to CSV format"""
    
    patients = get_all_patients()
    
    if not patients:
        return ""
    
    # CSV header
    csv_content = "Patient ID,Name,NHS Number,Specialty,Referral Date,Weeks Waiting,Days Waiting,Status,Priority,Breach Risk,Days to Breach,Consultant,Contact\n"
    
    for patient in patients:
        days = calculate_days_waiting(patient['clock_start_date'])
        weeks = days // 7
        breach_status = get_breach_status(days, patient.get('pathway_type', 'routine'))
        
        csv_content += f"{patient['patient_id']},"
        csv_content += f"\"{patient['patient_name']}\","
        csv_content += f"{patient['nhs_number']},"
        csv_content += f"{patient['specialty']},"
        csv_content += f"{patient['referral_date']},"
        csv_content += f"{weeks},"
        csv_content += f"{days},"
        csv_content += f"\"{patient['current_status']}\","
        csv_content += f"{patient['priority']},"
        csv_content += f"{breach_status['status']},"
        csv_content += f"{breach_status['days_to_breach']},"
        csv_content += f"\"{patient.get('consultant', '')}\","
        csv_content += f"{patient.get('contact_number', '')}\n"
    
    return csv_content


def get_breach_risk_patients(risk_level: str = "HIGH") -> List[Dict]:
    """Get patients at specified breach risk level"""
    
    patients = get_all_patients()
    at_risk = []
    
    for patient in patients:
        days = calculate_days_waiting(patient['clock_start_date'])
        breach_status = get_breach_status(days, patient.get('pathway_type', 'routine'))
        
        if breach_status['alert_level'] == risk_level:
            patient['breach_info'] = breach_status
            patient['days_waiting'] = days
            patient['weeks_waiting'] = days // 7
            at_risk.append(patient)
    
    # Sort by days to breach (most urgent first)
    at_risk.sort(key=lambda x: x['breach_info']['days_to_breach'])
    
    return at_risk
