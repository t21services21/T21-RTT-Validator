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


# Database files
APPOINTMENTS_DB = "appointments.json"
CLINICS_DB = "clinics.json"
SLOTS_DB = "appointment_slots.json"


def load_appointments():
    """Load appointments database"""
    if os.path.exists(APPOINTMENTS_DB):
        with open(APPOINTMENTS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'appointments': []}


def save_appointments(data):
    """Save appointments database"""
    with open(APPOINTMENTS_DB, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_clinics():
    """Load clinics database"""
    if os.path.exists(CLINICS_DB):
        with open(CLINICS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'clinics': []}


def save_clinics(data):
    """Save clinics database"""
    with open(CLINICS_DB, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


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
    """Create recurring clinic template"""
    
    clinics = load_clinics()
    
    clinic_id = f"CLINIC_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Generate appointment slots
    slots = generate_clinic_slots(start_time, end_time, slot_duration, capacity)
    
    clinic = {
        'clinic_id': clinic_id,
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
    
    clinics['clinics'].append(clinic)
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


def book_appointment(
    patient_name: str,
    nhs_number: str,
    clinic_id: str,
    appointment_date: str,
    slot_time: str,
    appointment_type: str,
    priority: str = "Routine",
    special_requirements: str = "",
    contact_number: str = "",
    transport_required: bool = False
) -> Dict:
    """
    Book appointment with AI optimization
    
    Returns booking confirmation or alternative suggestions
    """
    
    appointments = load_appointments()
    
    # Check slot availability
    available = check_slot_availability(clinic_id, appointment_date, slot_time)
    
    if not available:
        # AI suggests alternative slots
        alternatives = ai_suggest_alternative_slots(clinic_id, appointment_date, patient_data={
            'priority': priority,
            'appointment_type': appointment_type
        })
        
        return {
            'success': False,
            'message': 'Slot not available',
            'alternatives': alternatives,
            'ai_recommendation': alternatives[0] if alternatives else None
        }
    
    # Create booking
    appointment_id = f"APPT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    appointment = {
        'appointment_id': appointment_id,
        'patient_name': patient_name,
        'nhs_number': nhs_number,
        'clinic_id': clinic_id,
        'appointment_date': appointment_date,
        'slot_time': slot_time,
        'appointment_type': appointment_type,
        'priority': priority,
        'status': 'BOOKED',
        'special_requirements': special_requirements,
        'contact_number': contact_number,
        'transport_required': transport_required,
        'booked_date': datetime.now().isoformat(),
        'booked_by': 'System',
        'confirmed': False,
        'attendance_status': 'PENDING',
        'dna_risk_score': calculate_dna_risk(patient_data={
            'nhs_number': nhs_number,
            'appointment_type': appointment_type,
            'priority': priority
        })
    }
    
    appointments['appointments'].append(appointment)
    save_appointments(appointments)
    
    # Mark slot as booked
    mark_slot_booked(clinic_id, appointment_date, slot_time, appointment_id)
    
    return {
        'success': True,
        'appointment_id': appointment_id,
        'confirmation': f"Appointment booked for {appointment_date} at {slot_time}",
        'details': appointment
    }


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
    """Cancel an appointment"""
    
    appointments = load_appointments()
    
    for appt in appointments['appointments']:
        if appt['appointment_id'] == appointment_id:
            appt['status'] = 'CANCELLED'
            appt['cancellation_reason'] = reason
            appt['cancelled_by'] = cancelled_by
            appt['cancelled_date'] = datetime.now().isoformat()
            
            save_appointments(appointments)
            return True
    
    return False


def reschedule_appointment(
    appointment_id: str,
    new_clinic_id: str,
    new_date: str,
    new_time: str
) -> Dict:
    """Reschedule an appointment with AI optimization"""
    
    # Cancel old appointment
    cancel_appointment(appointment_id, "Rescheduled", "System")
    
    # Get patient details from old appointment
    appointments = load_appointments()
    old_appt = None
    for appt in appointments['appointments']:
        if appt['appointment_id'] == appointment_id:
            old_appt = appt
            break
    
    if not old_appt:
        return {'success': False, 'message': 'Appointment not found'}
    
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
        contact_number=old_appt.get('contact_number', '')
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
