"""
T21 CANCER PATHWAY MANAGEMENT SYSTEM
Complete AI-powered cancer pathway tracking for 2WW and 62-day targets

Features:
- 2-Week Wait (2WW) pathway tracking
- 62-day cancer pathway management
- Cancer PTL (Patient Tracking List)
- AI breach prediction for cancer pathways
- Cancer data sets management
- Multi-disciplinary team (MDT) integration
- Cancer milestone tracking
- Automated reporting for cancer targets

For Cancer Data Officers, Cancer Pathway Trackers, and Cancer Navigators
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Import Supabase functions for permanent storage
try:
    from supabase_database import (
        add_cancer_patient as supabase_add_cancer_patient,
        get_cancer_patients_for_user,
        update_cancer_patient as supabase_update_cancer_patient,
        delete_cancer_patient as supabase_delete_cancer_patient
    )
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available for Cancer Module - using fallback storage")


def get_current_user_email():
    """Get current logged-in user's email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


# Import universal data persistence
try:
    from universal_data_persistence import load_cancer_patients, save_cancer_patients
except:
    # Fallback if not available
    def load_cancer_patients(): return []
    def save_cancer_patients(data): pass


def is_admin_or_supervisor():
    """Check if current user is admin, staff, or tutor (can see all data)"""
    try:
        import streamlit as st
        user_email = st.session_state.get('user_email', '')
        user_type = st.session_state.get('user_type', 'student')
        
        # Check user type
        if user_type in ['admin', 'staff', 'tutor', 'partner']:
            return True
        
        # Check email domain
        if any(domain in user_email.lower() for domain in ['@t21services', '@admin', '@staff', '@tutor']):
            return True
        
        return False
    except:
        return False


def load_cancer_ptl():
    """Load cancer PTL database - ADMINS SEE ALL DATA, students see only their own"""
    user_email = get_current_user_email()
    is_supervisor = is_admin_or_supervisor()
    
    print(f"🔍 DEBUG Cancer PTL: Loading for user: {user_email} (Admin: {is_supervisor})")
    
    if SUPABASE_ENABLED:
        if is_supervisor:
            # ADMINS/STAFF/TUTORS SEE ALL DATA
            try:
                from supabase_database import supabase
                result = supabase.table('cancer_pathways').select('*').execute()
                patients = result.data if result.data else []
                print(f"🔍 DEBUG Cancer PTL: ADMIN MODE - Loaded {len(patients)} patients (ALL USERS)")
            except:
                patients = get_cancer_patients_for_user(user_email)
                print(f"🔍 DEBUG Cancer PTL: Fallback to user mode - {len(patients)} patients")
        else:
            # STUDENTS SEE ONLY THEIR OWN DATA
            patients = get_cancer_patients_for_user(user_email)
            print(f"🔍 DEBUG Cancer PTL: STUDENT MODE - {len(patients)} patients for {user_email}")
        
        return {'patients': patients}
    else:
        # Use universal data persistence (per-user files)
        patients = load_cancer_patients()
        print(f"🔍 DEBUG Cancer PTL: Fallback mode - {len(patients)} patients")
        return {'patients': patients}


def save_cancer_ptl(data):
    """Save cancer PTL database - Now uses per-user permanent storage"""
    if SUPABASE_ENABLED:
        # Supabase saves happen in individual functions
        pass
    else:
        # Use universal data persistence (per-user files)
        if 'patients' in data:
            save_cancer_patients(data['patients'])


def calculate_cancer_days_waiting(start_date: str) -> int:
    """Calculate days from cancer pathway start"""
    try:
        start = datetime.fromisoformat(start_date)
        now = datetime.now()
        return (now - start).days
    except:
        return 0


def get_cancer_breach_status(days_waiting: int, pathway_type: str) -> Dict:
    """
    Determine breach status for cancer pathways
    
    Args:
        days_waiting: Days since pathway start
        pathway_type: '2ww' or '62day'
        
    Returns:
        Dict with status, color, days_to_breach
    """
    
    if pathway_type == "2ww":
        target_days = 14  # 2 weeks for first appointment
    elif pathway_type == "62day":
        target_days = 62  # 62 days from referral to treatment
    elif pathway_type == "31day":
        target_days = 31  # 31 days from decision to treat to treatment
    else:
        target_days = 62
    
    days_to_breach = target_days - days_waiting
    
    if days_waiting >= target_days:
        return {
            'status': 'BREACH',
            'color': 'red',
            'days_to_breach': days_to_breach,
            'alert_level': 'CRITICAL',
            'action': 'IMMEDIATE ESCALATION REQUIRED'
        }
    elif days_to_breach <= 3:
        return {
            'status': 'IMMINENT BREACH',
            'color': 'orange',
            'days_to_breach': days_to_breach,
            'alert_level': 'HIGH',
            'action': 'URGENT ACTION NEEDED'
        }
    elif days_to_breach <= 7:
        return {
            'status': 'AT RISK',
            'color': 'yellow',
            'days_to_breach': days_to_breach,
            'alert_level': 'MEDIUM',
            'action': 'MONITOR CLOSELY'
        }
    else:
        return {
            'status': 'ON TRACK',
            'color': 'green',
            'days_to_breach': days_to_breach,
            'alert_level': 'LOW',
            'action': 'STANDARD MONITORING'
        }


def add_cancer_patient(
    patient_name: str,
    nhs_number: str,
    cancer_type: str,
    pathway_type: str,  # '2ww', '62day', '31day'
    referral_date: str,
    referring_clinician: str,
    primary_site: str,
    suspected_diagnosis: str,
    urgency: str = "Standard",
    contact_number: str = "",
    notes: str = ""
) -> str:
    """Add patient to cancer PTL - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    patient_id = f"CANCER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    patient_data = {
        'pathway_id': patient_id,  # CRITICAL FIX: Table expects pathway_id, not patient_id
        'patient_name': patient_name,
        'nhs_number': nhs_number,
        'cancer_type': cancer_type,
        'pathway_type': pathway_type,
        'referral_date': referral_date,
        'pathway_start_date': referral_date,
        'referring_clinician': referring_clinician,
        'primary_site': primary_site,
        'suspected_diagnosis': suspected_diagnosis,
        'urgency': urgency,
        'contact_number': contact_number,
        'current_status': 'Awaiting First Appointment' if pathway_type == '2ww' else 'Awaiting Diagnostics',
        'pathway_status': 'ACTIVE',
        'notes': notes,
        'added_date': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat(),
        'milestones': [],
        'appointments': [],
        'diagnostics': [],
        'mdt_dates': [],
        'events': [{
            'date': referral_date,
            'milestone': 'REFERRAL_RECEIVED',
            'description': f'{pathway_type.upper()} referral from {referring_clinician}',
            'days_from_start': 0
        }]
    }

    if SUPABASE_ENABLED:
        success, result = supabase_add_cancer_patient(user_email, patient_data)
        if success:
            return patient_id
        else:
            print(f"Error saving cancer patient to Supabase: {result}")
            # Still return patient_id for fallback UI to work
            return patient_id
    else:
        ptl = load_cancer_ptl()
        ptl['patients'].append(patient_data)
        save_cancer_ptl(ptl)
        return patient_id


def add_cancer_milestone(
    patient_id: str,
    milestone_type: str,  # 'FIRST_SEEN', 'DIAGNOSTIC_TEST', 'MDT_DISCUSSION', 'DECISION_TO_TREAT', 'TREATMENT_START'
    milestone_date: str,
    description: str,
    performed_by: str = ""
) -> bool:
    """Add milestone to cancer pathway"""
    
    ptl = load_cancer_ptl()
    
    for patient in ptl['patients']:
        if patient.get('pathway_id') == patient_id or patient.get('patient_id') == patient_id:
            # Calculate days from pathway start
            start_date = datetime.fromisoformat(patient['pathway_start_date'])
            milestone_dt = datetime.fromisoformat(milestone_date)
            days_from_start = (milestone_dt - start_date).days
            
            milestone = {
                'milestone_type': milestone_type,
                'date': milestone_date,
                'description': description,
                'performed_by': performed_by,
                'days_from_start': days_from_start,
                'added_date': datetime.now().isoformat()
            }
            
            patient['milestones'].append(milestone)
            patient['last_updated'] = datetime.now().isoformat()
            
            # Update status based on milestone
            if milestone_type == 'FIRST_SEEN':
                patient['current_status'] = 'First Seen - Awaiting Diagnostics'
            elif milestone_type == 'DIAGNOSTIC_TEST':
                patient['current_status'] = 'Diagnostics in Progress'
            elif milestone_type == 'MDT_DISCUSSION':
                patient['current_status'] = 'Discussed at MDT'
            elif milestone_type == 'DECISION_TO_TREAT':
                patient['current_status'] = 'Decision to Treat Made'
            elif milestone_type == 'TREATMENT_START':
                patient['current_status'] = 'Treatment Started'
                patient['pathway_status'] = 'COMPLETED'
            
            save_cancer_ptl(ptl)
            return True
    
    return False


def get_all_cancer_patients() -> List[Dict]:
    """Get all patients on cancer PTL - ADMINS SEE ALL, students see own"""
    # Use load_cancer_ptl which has admin logic built-in
    ptl = load_cancer_ptl()
    return ptl.get('patients', [])


def get_cancer_patient_by_id(patient_id: str) -> Optional[Dict]:
    """Get specific cancer patient"""
    ptl = load_cancer_ptl()
    for patient in ptl['patients']:
        if patient.get('pathway_id') == patient_id or patient.get('patient_id') == patient_id:
            return patient
    return None


def search_cancer_patients(
    query: str = "",
    cancer_type: str = None,
    pathway_type: str = None,
    breach_risk: str = None
) -> List[Dict]:
    """Search and filter cancer PTL"""
    
    patients = get_all_cancer_patients()
    results = []
    
    for patient in patients:
        # Text search
        if query:
            query_lower = query.lower()
            if (query_lower not in patient['patient_name'].lower() and
                query_lower not in patient['nhs_number'].lower()):
                continue
        
        # Cancer type filter
        if cancer_type and patient['cancer_type'] != cancer_type:
            continue
        
        # Pathway type filter
        if pathway_type and patient['pathway_type'] != pathway_type:
            continue
        
        # Breach risk filter
        if breach_risk:
            days = calculate_cancer_days_waiting(patient['pathway_start_date'])
            breach_status = get_cancer_breach_status(days, patient['pathway_type'])
            if breach_status['alert_level'] != breach_risk:
                continue
        
        results.append(patient)
    
    return results


def get_cancer_ptl_stats() -> Dict:
    """Get cancer PTL statistics"""
    
    patients = get_all_cancer_patients()
    
    stats = {
        'total_patients': len(patients),
        'cancer_types': {},
        'pathway_types': {},
        'breach_risks': {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        },
        'breaches': 0,
        '2ww_breaches': 0,
        '62day_breaches': 0,
        'active_pathways': 0,
        'completed_pathways': 0
    }
    
    if not patients:
        return stats
    
    for patient in patients:
        # Count by cancer type
        cancer_type = patient['cancer_type']
        stats['cancer_types'][cancer_type] = stats['cancer_types'].get(cancer_type, 0) + 1
        
        # Count by pathway type
        pathway_type = patient['pathway_type']
        stats['pathway_types'][pathway_type] = stats['pathway_types'].get(pathway_type, 0) + 1
        
        # Count pathway status
        if patient['pathway_status'] == 'ACTIVE':
            stats['active_pathways'] += 1
        else:
            stats['completed_pathways'] += 1
        
        # Calculate breach status
        days = calculate_cancer_days_waiting(patient['pathway_start_date'])
        breach_status = get_cancer_breach_status(days, pathway_type)
        stats['breach_risks'][breach_status['alert_level']] += 1
        
        if breach_status['status'] == 'BREACH':
            stats['breaches'] += 1
            if pathway_type == '2ww':
                stats['2ww_breaches'] += 1
            elif pathway_type == '62day':
                stats['62day_breaches'] += 1
    
    return stats


def ai_predict_cancer_breach(patient_data: Dict) -> Dict:
    """
    AI prediction of cancer pathway breach
    Uses similar logic to main PTL but with cancer-specific targets
    """
    
    days_waiting = patient_data.get('days_waiting', 0)
    pathway_type = patient_data.get('pathway_type', '62day')
    cancer_type = patient_data.get('cancer_type', 'Unknown')
    milestones_completed = len(patient_data.get('milestones', []))
    
    # Calculate expected milestones based on days
    if pathway_type == '2ww':
        target_days = 14
        expected_milestones = 1  # Should have first appointment
    elif pathway_type == '62day':
        target_days = 62
        # Expected milestones based on days elapsed
        if days_waiting < 14:
            expected_milestones = 0
        elif days_waiting < 28:
            expected_milestones = 1  # First seen
        elif days_waiting < 42:
            expected_milestones = 2  # Diagnostics
        else:
            expected_milestones = 3  # MDT discussed
    else:
        target_days = 31
        expected_milestones = 2
    
    days_to_breach = target_days - days_waiting
    
    # Calculate risk score
    milestone_deficit = max(0, expected_milestones - milestones_completed)
    risk_score = max(0, min(100, 100 - (days_to_breach / target_days * 100) + (milestone_deficit * 20)))
    
    # Determine priority
    if risk_score >= 80:
        priority = "CRITICAL"
        actions = [
            f"URGENT: Only {days_to_breach} days to breach!",
            "Escalate to Cancer Manager immediately",
            "Contact patient urgently",
            "Fast-track all outstanding appointments",
            "Consider emergency MDT discussion"
        ]
    elif risk_score >= 60:
        priority = "HIGH"
        actions = [
            f"High priority: {days_to_breach} days remaining",
            "Book outstanding appointments within 48 hours",
            "Ensure diagnostics expedited",
            "Prepare for MDT this week"
        ]
    elif risk_score >= 40:
        priority = "MEDIUM"
        actions = [
            "Monitor progress closely",
            "Ensure appointments on schedule",
            "Check for any delays"
        ]
    else:
        priority = "LOW"
        actions = [
            "Standard monitoring",
            "Continue as planned"
        ]
    
    return {
        'success': True,
        'ai_powered': True,
        'breach_risk_score': risk_score,
        'priority_level': priority,
        'days_to_breach': days_to_breach,
        'pathway_type': pathway_type,
        'target_days': target_days,
        'milestones_completed': milestones_completed,
        'milestones_expected': expected_milestones,
        'milestone_deficit': milestone_deficit,
        'recommended_actions': actions,
        'prediction_time': datetime.now().isoformat()
    }


def export_cancer_ptl_to_csv() -> str:
    """Export cancer PTL to CSV"""
    
    patients = get_all_cancer_patients()
    
    if not patients:
        return ""
    
    # CSV header
    csv_content = "Patient ID,Name,NHS Number,Cancer Type,Pathway Type,Referral Date,Days Waiting,Status,Breach Risk,Days to Breach,Milestones Completed\n"
    
    for patient in patients:
        days = calculate_cancer_days_waiting(patient['pathway_start_date'])
        breach_status = get_cancer_breach_status(days, patient['pathway_type'])
        
        csv_content += f"{patient['patient_id']},"
        csv_content += f"\"{patient['patient_name']}\","
        csv_content += f"{patient['nhs_number']},"
        csv_content += f"{patient['cancer_type']},"
        csv_content += f"{patient['pathway_type'].upper()},"
        csv_content += f"{patient['referral_date']},"
        csv_content += f"{days},"
        csv_content += f"\"{patient['current_status']}\","
        csv_content += f"{breach_status['status']},"
        csv_content += f"{breach_status['days_to_breach']},"
        csv_content += f"{len(patient['milestones'])}\n"
    
    return csv_content


# Cancer types supported
CANCER_TYPES = [
    "Breast",
    "Lung",
    "Colorectal",
    "Prostate",
    "Skin (Melanoma)",
    "Bladder",
    "Kidney",
    "Ovarian",
    "Head & Neck",
    "Brain/CNS",
    "Haematological (Blood)",
    "Gastric (Stomach)",
    "Pancreatic",
    "Liver",
    "Oesophageal",
    "Testicular",
    "Cervical",
    "Endometrial (Womb)",
    "Thyroid",
    "Unknown Primary",
    "Other"
]


# Cancer pathway milestones
CANCER_MILESTONES = {
    '2ww': [
        'REFERRAL_RECEIVED',
        'FIRST_SEEN',
        'DIAGNOSTIC_TEST',
        'RESULTS_REVIEWED',
        'DECISION_MADE'
    ],
    '62day': [
        'REFERRAL_RECEIVED',
        'FIRST_SEEN',
        'DIAGNOSTIC_TEST',
        'MDT_DISCUSSION',
        'DECISION_TO_TREAT',
        'TREATMENT_PLAN',
        'TREATMENT_START'
    ],
    '31day': [
        'DECISION_TO_TREAT',
        'PRE_TREATMENT_ASSESSMENT',
        'TREATMENT_PLAN',
        'TREATMENT_START'
    ]
}
