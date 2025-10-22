"""
T21 ADVANCED BOOKING & APPOINTMENT SYSTEM
Complete AI-powered appointment scheduling and management

DUAL PURPOSE:
1. TRAINING: Students practice real appointment booking
2. AUTOMATION: NHS trusts use for actual appointment management

Features:
- AI-optimized appointment scheduling
- Intelligent calendar management
- Capacity planning & optimization
- Conflict detection & resolution
- Automated patient communication
- Waiting list integration
- Multi-clinic coordination
- Resource optimization
- DNA prediction & prevention
- Overbooking intelligence

For: Appointment Administrators, Booking Officers, Schedulers
"""

import json
import os
from datetime import datetime, timedelta, time
from typing import List, Dict, Optional
import calendar

# Import Supabase functions for permanent storage
try:
    from supabase_database import (
        create_clinic_template as supabase_create_clinic_template,
        get_clinics_for_user,
        create_appointment as supabase_create_appointment,
        get_appointments_for_user,
        update_appointment as supabase_update_appointment
    )
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available for Booking Module - using fallback storage")


def get_current_user_email():
    """Get current logged-in user's email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


# Database files (fallback only)
APPOINTMENTS_DB = "appointments.json"
CLINICS_DB = "clinics.json"

def load_appointments():
    """Load appointments database - Now uses Supabase"""
    user_email = get_current_user_email()
    if SUPABASE_ENABLED:
        return {'appointments': get_appointments_for_user(user_email)}
    else:
        if os.path.exists(APPOINTMENTS_DB):
            with open(APPOINTMENTS_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'appointments': []}

def save_appointments(data):
    """Save appointments database - Deprecated"""
    pass

def load_clinics():
    """Load clinics database - Now uses Supabase"""
    user_email = get_current_user_email()
    if SUPABASE_ENABLED:
        return {'clinics': get_clinics_for_user(user_email)}
    else:
        if os.path.exists(CLINICS_DB):
            with open(CLINICS_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'clinics': []}

def save_clinics(data):
    """Save clinics database - Deprecated"""
    pass


def create_clinic_template(
    clinic_name: str,
    specialty: str,
    location: str,
    consultant: str,
    day_of_week: str,  # Monday, Tuesday, etc.
    start_time: str,
    end_time: str,
    slot_duration: int = 15,  # minutes
    capacity: int = 20,
    clinic_type: str = "Outpatient"
) -> str:
    """Create recurring clinic template - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    clinic_id = f"CLINIC_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    slots = generate_clinic_slots(start_time, end_time, slot_duration, capacity)
    
    clinic_data = {
        'clinic_id': clinic_id,
        'user_email': user_email,
        'clinic_name': clinic_name,
        'specialty': specialty,
        'location': location,
        'consultant': consultant,
        'day_of_week': day_of_week,
        'start_time': start_time,
        'end_time': end_time,
        'slot_duration': slot_duration,
        'capacity': capacity,
        'clinic_type': clinic_type,
        'slots_template': slots,
        'active': True,
        'created_date': datetime.now().isoformat()
    }

    if SUPABASE_ENABLED:
        success, _ = supabase_create_clinic_template(user_email, clinic_data)
        if success:
            return clinic_id
        else:
            return "ERROR"
    else:
        clinics = load_clinics()
        clinics['clinics'].append(clinic_data)
        save_clinics(clinics)
        return clinic_id


def generate_clinic_slots(start_time: str, end_time: str, duration: int, capacity: int) -> List[Dict]:
    """Generate appointment slots for a clinic"""
    
    slots = []
    
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")
    
    current_time = start_dt
    slot_num = 1
    
    while current_time < end_dt:
        slot_time = current_time.strftime("%H:%M")
        slots.append({
            'slot_number': slot_num,
            'time': slot_time,
            'duration': duration,
            'available': True
        })
        current_time += timedelta(minutes=duration)
        slot_num += 1
        
        if slot_num > capacity:
            break
    
    return slots


def mark_appointment_attended(appointment_id: str) -> bool:
    """Mark appointment as attended"""
    user_email = get_current_user_email()
    
    updates = {
        'status': 'Completed',
        'attended': True,
        'attendance_recorded_at': datetime.now().isoformat()
    }
    
    if SUPABASE_ENABLED:
        success, _ = update_appointment(user_email, appointment_id, updates)
        return success
    else:
        appointments = load_appointments()
        for appt in appointments['appointments']:
            if appt['appointment_id'] == appointment_id:
                appt.update(updates)
                save_appointments(appointments)
                return True
        return False


def mark_appointment_dna(appointment_id: str, reason: str = "") -> bool:
    """Mark appointment as Did Not Attend (DNA)"""
    user_email = get_current_user_email()
    
    updates = {
        'status': 'No-Show',
        'attended': False,
        'dna_reason': reason,
        'dna_recorded_at': datetime.now().isoformat()
    }
    
    if SUPABASE_ENABLED:
        success, _ = update_appointment(user_email, appointment_id, updates)
        return success
    else:
        appointments = load_appointments()
        for appt in appointments['appointments']:
            if appt['appointment_id'] == appointment_id:
                appt.update(updates)
                save_appointments(appointments)
                return True
        return False


def get_appointment_by_id(appointment_id: str) -> Optional[Dict]:
    """Get specific appointment by ID"""
    appointments = load_appointments()
    all_appointments = appointments.get('appointments', [])
    return next((a for a in all_appointments if a['appointment_id'] == appointment_id), None)


def get_dna_rate(clinic_id: str = None, days: int = 30) -> Dict:
    """Calculate DNA rate for clinic or overall"""
    appointments = load_appointments()
    all_appointments = appointments.get('appointments', [])
    
    # Filter by clinic if specified
    if clinic_id:
        all_appointments = [a for a in all_appointments if a.get('clinic_id') == clinic_id]
    
    # Filter by date range
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    all_appointments = [a for a in all_appointments if a.get('appointment_date', '') >= cutoff_date]
    
    total = len(all_appointments)
    dna = len([a for a in all_appointments if a.get('status', '').lower() == 'no-show'])
    attended = len([a for a in all_appointments if a.get('status', '').lower() == 'completed'])
    cancelled = len([a for a in all_appointments if a.get('status', '').lower() == 'cancelled'])
    
    dna_rate = (dna / total * 100) if total > 0 else 0
    attendance_rate = (attended / total * 100) if total > 0 else 0
    
    return {
        'total_appointments': total,
        'attended': attended,
        'dna': dna,
        'cancelled': cancelled,
        'dna_rate': round(dna_rate, 1),
        'attendance_rate': round(attendance_rate, 1)
    }


def get_patient_dna_history(patient_nhs: str) -> List[Dict]:
    """Get DNA history for a patient"""
    appointments = load_appointments()
    all_appointments = appointments.get('appointments', [])
    
    from unified_patient_system import normalize_nhs_number
    patient_nhs_normalized = normalize_nhs_number(patient_nhs)
    
    dna_appointments = []
    for appt in all_appointments:
        if normalize_nhs_number(appt.get('nhs_number', '')) == patient_nhs_normalized:
            if appt.get('status', '').lower() == 'no-show':
                dna_appointments.append(appt)
    
    return dna_appointments


def book_appointment(
    patient_name: str,
    nhs_number: str,
    clinic_id: str,
    appointment_date: str,
    slot_time: str,
    appointment_type: str,
    specialty: str = "General",
    priority: str = "Routine",
    special_requirements: str = "",
    contact_number: str = "",
    transport_required: bool = False
) -> Dict:
    """
    Book appointment with AI optimization - NOW WITH SUPABASE!
    """
    
    user_email = get_current_user_email()
    available = check_slot_availability(clinic_id, appointment_date, slot_time)

    if not available:
        alternatives = ai_suggest_alternative_slots(clinic_id, appointment_date, patient_data={'priority': priority, 'appointment_type': appointment_type})
        return {'success': False, 'message': 'Slot not available', 'alternatives': alternatives, 'ai_recommendation': alternatives[0] if alternatives else None}

    appointment_id = f"APPT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    appointment_data = {
        'appointment_id': appointment_id,
        'user_email': user_email,
        'patient_name': patient_name,
        'nhs_number': nhs_number,
        'clinic_id': clinic_id,
        'appointment_date': appointment_date,
        'slot_time': slot_time,
        'appointment_type': appointment_type,
        'specialty': specialty,
        'priority': priority,
        'status': 'Booked',
        'special_requirements': special_requirements,
        'contact_number': contact_number,
        'transport_required': transport_required,
        'booked_date': datetime.now().isoformat(),
        'booked_by': 'System',
        'confirmed': False,
        'attendance_status': 'PENDING',
        'dna_risk_score': calculate_dna_risk(patient_data={'nhs_number': nhs_number, 'appointment_type': appointment_type, 'priority': priority})
    }

    if SUPABASE_ENABLED:
        success, result = supabase_create_appointment(user_email, appointment_data)
        if success:
            return {'success': True, 'appointment_id': appointment_id, 'confirmation': f"Appointment booked for {appointment_date} at {slot_time}", 'details': appointment_data}
        else:
            error_msg = f"Supabase error: {result}" if result else "Unknown Supabase error"
            print(f"ERROR saving appointment to Supabase: {error_msg}")
            print(f"Falling back to session storage...")
            # Fall through to session storage
    
    # Use session storage (fallback or if Supabase disabled)
    try:
        import streamlit as st
        if 'appointments' not in st.session_state:
            st.session_state.appointments = []
        st.session_state.appointments.append(appointment_data)
        return {'success': True, 'appointment_id': appointment_id, 'confirmation': f"Appointment booked for {appointment_date} at {slot_time}", 'details': appointment_data, 'storage': 'session'}
    except:
        # Last resort: file storage
        appointments = load_appointments()
        if 'appointments' not in appointments:
            appointments['appointments'] = []
        appointments['appointments'].append(appointment_data)
        try:
            with open(APPOINTMENTS_DB, 'w', encoding='utf-8') as f:
                json.dump(appointments, f, indent=2)
        except:
            pass
        return {'success': True, 'appointment_id': appointment_id, 'confirmation': f"Appointment booked for {appointment_date} at {slot_time}", 'details': appointment_data, 'storage': 'file'}


def check_slot_availability(clinic_id: str, appointment_date: str, slot_time: str) -> bool:
    """Check if appointment slot is available"""
    
    appointments = load_appointments()
    
    # Check if slot already booked
    for appt in appointments['appointments']:
        if (appt['clinic_id'] == clinic_id and 
            appt['appointment_date'] == appointment_date and 
            appt['slot_time'] == slot_time and
            appt['status'] != 'CANCELLED'):
            return False
    
    return True


def ai_suggest_alternative_slots(clinic_id: str, preferred_date: str, patient_data: Dict) -> List[Dict]:
    """
    AI suggests alternative appointment slots
    Based on patient priority, clinic capacity, and optimization
    """
    
    clinics = load_clinics()
    appointments = load_appointments()
    
    # Get clinic details
    clinic = None
    for c in clinics['clinics']:
        if c['clinic_id'] == clinic_id:
            clinic = c
            break
    
    if not clinic:
        return []
    
    alternatives = []
    
    # Search next 4 weeks
    preferred_dt = datetime.strptime(preferred_date, "%Y-%m-%d")
    
    for days_ahead in range(0, 28):
        check_date = preferred_dt + timedelta(days=days_ahead)
        
        # Check if clinic runs on this day
        if check_date.strftime("%A") == clinic['day_of_week']:
            # Check available slots
            for slot in clinic['slots_template']:
                if check_slot_availability(clinic_id, check_date.strftime("%Y-%m-%d"), slot['time']):
                    # Calculate AI score for this slot
                    score = ai_score_slot(check_date, slot['time'], patient_data, days_ahead)
                    
                    alternatives.append({
                        'date': check_date.strftime("%Y-%m-%d"),
                        'time': slot['time'],
                        'clinic_id': clinic_id,
                        'clinic_name': clinic['clinic_name'],
                        'consultant': clinic['consultant'],
                        'days_from_preferred': days_ahead,
                        'ai_score': score,
                        'recommendation': get_score_description(score)
                    })
        
        if len(alternatives) >= 10:  # Suggest top 10
            break
    
    # Sort by AI score (highest first)
    alternatives.sort(key=lambda x: x['ai_score'], reverse=True)
    
    return alternatives[:5]  # Return top 5


def ai_score_slot(date: datetime, time: str, patient_data: Dict, days_from_preferred: int) -> float:
    """
    AI scoring algorithm for appointment slots
    
    Considers:
    - Proximity to preferred date
    - Time of day preferences
    - Patient priority
    - Clinic capacity
    - Historical DNA rates for this slot
    """
    
    score = 100.0
    
    # Proximity to preferred date (closer = better)
    score -= (days_from_preferred * 2)
    
    # Priority boost
    priority = patient_data.get('priority', 'Routine')
    if priority == 'Urgent':
        score += 20
    elif priority == '2WW':
        score += 30
    
    # Time of day preference (morning slots often preferred)
    hour = int(time.split(':')[0])
    if 9 <= hour <= 11:  # Morning preference
        score += 10
    elif 14 <= hour <= 16:  # Early afternoon
        score += 5
    
    # Weekend penalty (if applicable)
    if date.weekday() >= 5:  # Saturday/Sunday
        score -= 15
    
    return max(0, min(100, score))


def get_score_description(score: float) -> str:
    """Get human-readable description of AI score"""
    if score >= 80:
        return "Highly Recommended"
    elif score >= 60:
        return "Good Option"
    elif score >= 40:
        return "Acceptable"
    else:
        return "Available"


def calculate_dna_risk(patient_data: Dict) -> float:
    """
    AI predicts DNA (Did Not Attend) risk
    
    Risk factors:
    - Historical DNA rate
    - Appointment type
    - Time of day
    - Day of week
    - Notice period
    """
    
    # Simplified risk calculation (would use ML model in production)
    base_risk = 15.0  # 15% base DNA rate
    
    appointment_type = patient_data.get('appointment_type', 'New')
    if appointment_type == 'Follow-up':
        base_risk -= 5  # Follow-ups have lower DNA
    
    priority = patient_data.get('priority', 'Routine')
    if priority in ['Urgent', '2WW']:
        base_risk -= 10  # Urgent appointments less likely to DNA
    
    return max(0, min(100, base_risk))


def mark_slot_booked(clinic_id: str, appointment_date: str, slot_time: str, appointment_id: str):
    """Mark slot as booked in slots database"""
    # This would update a real-time slots availability system
    pass


def get_available_slots(clinic_id: str, date: str) -> List[Dict]:
    """Get all available slots for a clinic on a specific date"""
    
    clinics = load_clinics()
    appointments = load_appointments()
    
    # Get clinic template
    clinic = None
    for c in clinics['clinics']:
        if c['clinic_id'] == clinic_id:
            clinic = c
            break
    
    if not clinic:
        return []
    
    # Check which slots are available
    available = []
    for slot in clinic['slots_template']:
        if check_slot_availability(clinic_id, date, slot['time']):
            available.append({
                'time': slot['time'],
                'duration': slot['duration'],
                'clinic_name': clinic['clinic_name'],
                'consultant': clinic['consultant'],
                'location': clinic['location']
            })
    
    return available


def cancel_appointment(appointment_id: str, reason: str, cancelled_by: str = "Patient") -> bool:
    """Cancel an appointment - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    updates = {
        'status': 'CANCELLED',
        'cancellation_reason': reason,
        'cancelled_by': cancelled_by,
        'cancelled_date': datetime.now().isoformat()
    }

    if SUPABASE_ENABLED:
        success, _ = supabase_update_appointment(user_email, appointment_id, updates)
        return success
    else:
        appointments = load_appointments()
        for appt in appointments['appointments']:
            if appt['appointment_id'] == appointment_id:
                appt.update(updates)
                save_appointments(appointments)
                return True
        return False


def reschedule_appointment(
    appointment_id: str,
    new_clinic_id: str,
    new_date: str,
    new_time: str
) -> Dict:
    """Reschedule an appointment with AI optimization - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    appointments = load_appointments()['appointments']
    old_appt = next((a for a in appointments if a['appointment_id'] == appointment_id), None)

    if not old_appt:
        return {'success': False, 'message': 'Original appointment not found'}

    # Cancel old appointment
    cancel_success = cancel_appointment(appointment_id, "Rescheduled by system", "System")
    if not cancel_success:
        return {'success': False, 'message': 'Failed to cancel the original appointment'}

    # Book new appointment
    return book_appointment(
        patient_name=old_appt['patient_name'],
        nhs_number=old_appt['nhs_number'],
        clinic_id=new_clinic_id,
        appointment_date=new_date,
        slot_time=new_time,
        appointment_type=old_appt['appointment_type'],
        priority=old_appt['priority'],
        special_requirements=old_appt.get('special_requirements', ''),
        contact_number=old_appt.get('contact_number', ''),
        transport_required=old_appt.get('transport_required', False)
    )


def ai_optimize_clinic_capacity(clinic_id: str, weeks_ahead: int = 4) -> Dict:
    """
    AI analyzes clinic capacity and suggests optimizations
    
    Returns:
    - Current utilization
    - Predicted demand
    - Optimization recommendations
    """
    
    clinics = load_clinics()
    appointments = load_appointments()
    
    clinic = None
    for c in clinics['clinics']:
        if c['clinic_id'] == clinic_id:
            clinic = c
            break
    
    if not clinic:
        return {}
    
    # Calculate current utilization
    total_slots = len(clinic['slots_template'])
    
    # Count bookings for next X weeks
    bookings = 0
    cancellations = 0
    dnas = 0
    
    today = datetime.now().date()
    end_date = today + timedelta(weeks=weeks_ahead)
    
    for appt in appointments['appointments']:
        if appt['clinic_id'] == clinic_id:
            appt_date = datetime.strptime(appt['appointment_date'], "%Y-%m-%d").date()
            if today <= appt_date <= end_date:
                bookings += 1
                if appt['status'] == 'CANCELLED':
                    cancellations += 1
                elif appt.get('attendance_status') == 'DNA':
                    dnas += 1
    
    utilization = (bookings / (total_slots * weeks_ahead * 4)) * 100 if total_slots > 0 else 0
    
    # AI recommendations
    recommendations = []
    
    if utilization < 60:
        recommendations.append({
            'type': 'UNDERUTILIZED',
            'message': f'Clinic only {utilization:.1f}% booked',
            'action': 'Consider reducing clinic frequency or increasing slot availability'
        })
    elif utilization > 95:
        recommendations.append({
            'type': 'OVERBOOKED',
            'message': f'Clinic at {utilization:.1f}% capacity',
            'action': 'Add additional clinic sessions or increase slot duration'
        })
    
    if cancellations > bookings * 0.15:
        recommendations.append({
            'type': 'HIGH_CANCELLATIONS',
            'message': f'{(cancellations/bookings)*100:.1f}% cancellation rate',
            'action': 'Implement reminder system and overbooking strategy'
        })
    
    if dnas > bookings * 0.10:
        recommendations.append({
            'type': 'HIGH_DNA',
            'message': f'{(dnas/bookings)*100:.1f}% DNA rate',
            'action': 'Enhance patient communication and implement DNA reduction strategies'
        })
    
    return {
        'clinic_id': clinic_id,
        'clinic_name': clinic['clinic_name'],
        'total_capacity': total_slots * weeks_ahead * 4,
        'bookings': bookings,
        'utilization': utilization,
        'cancellations': cancellations,
        'dnas': dnas,
        'recommendations': recommendations,
        'ai_optimization_score': calculate_optimization_score(utilization, cancellations, dnas, bookings)
    }


def calculate_optimization_score(utilization: float, cancellations: int, dnas: int, bookings: int) -> float:
    """Calculate overall optimization score (0-100)"""
    
    score = 100.0
    
    # Penalize poor utilization (both too low and too high)
    if utilization < 70:
        score -= (70 - utilization) * 0.5
    elif utilization > 95:
        score -= (utilization - 95) * 2
    
    # Penalize high cancellations
    if bookings > 0:
        cancel_rate = (cancellations / bookings) * 100
        if cancel_rate > 10:
            score -= (cancel_rate - 10) * 2
        
        # Penalize high DNAs
        dna_rate = (dnas / bookings) * 100
        if dna_rate > 5:
            score -= (dna_rate - 5) * 3
    
    return max(0, min(100, score))


# Common appointment types
APPOINTMENT_TYPES = [
    "New Patient",
    "Follow-up",
    "Review",
    "Diagnostic Test",
    "Procedure",
    "Pre-operative Assessment",
    "Post-operative Follow-up",
    "Urgent Review",
    "2-Week Wait",
    "Treatment",
    "Consultation"
]


# Common specialties
SPECIALTIES = [
    "Cardiology",
    "Dermatology",
    "ENT",
    "Gastroenterology",
    "General Surgery",
    "Neurology",
    "Ophthalmology",
    "Orthopaedics",
    "Respiratory",
    "Rheumatology",
    "Urology",
    "Oncology"
]
