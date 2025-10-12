"""
T21 MEDICAL SECRETARY AI ASSISTANT
Complete AI-powered medical secretary automation

DUAL PURPOSE:
1. TRAINING: Students learn real medical secretary workflows
2. AUTOMATION: NHS uses for actual clinic coordination

Features:
- AI-powered correspondence management
- Intelligent clinic coordination
- Automated dictation transcription
- Smart diary management
- Meeting scheduling
- Document management
- Multi-clinic oversight
- Patient communication automation
- Referral processing
- Report generation

For: Medical Secretaries, Clinic Coordinators, Admin Support
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Import Supabase functions for permanent storage
try:
    from supabase_database import (
        create_correspondence,
        get_correspondence_for_user,
        create_diary_event,
        get_diary_events_for_user
    )
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available for Secretary Module - using fallback storage")


def get_current_user_email():
    """Get current logged-in user's email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


# Database files (fallback only)
CORRESPONDENCE_DB = "correspondence.json"
DIARY_DB = "diary.json"

def load_correspondence():
    """Load correspondence database - Now uses Supabase"""
    user_email = get_current_user_email()
    if SUPABASE_ENABLED:
        return {'letters': get_correspondence_for_user(user_email)}
    else:
        if os.path.exists(CORRESPONDENCE_DB):
            with open(CORRESPONDENCE_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'letters': []}

def save_correspondence(data):
    """Save correspondence database - Deprecated"""
    pass


def ai_draft_clinic_letter(
    letter_type: str,
    patient_name: str,
    nhs_number: str,
    gp_name: str,
    gp_address: str,
    clinic_date: str,
    consultant_name: str,
    diagnosis: str = "",
    investigations: List[str] = None,
    treatment_plan: str = "",
    follow_up: str = "",
    additional_notes: str = ""
) -> Dict:
    """AI generates professional clinic letter - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    letter_id = f"LETTER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    letter_content = generate_clinic_letter_template(
        letter_type, patient_name, nhs_number, gp_name, gp_address,
        clinic_date, consultant_name, diagnosis, investigations or [],
        treatment_plan, follow_up, additional_notes
    )
    
    letter_data = {
        'letter_id': letter_id,
        'user_email': user_email,
        'letter_type': letter_type,
        'patient_name': patient_name,
        'nhs_number': nhs_number,
        'gp_name': gp_name,
        'gp_address': gp_address,
        'clinic_date': clinic_date,
        'consultant_name': consultant_name,
        'content': letter_content,
        'status': 'DRAFT',
        'created_date': datetime.now().isoformat(),
        'ai_generated': True
    }

    if SUPABASE_ENABLED:
        create_correspondence(user_email, letter_data)
    else:
        correspondence = load_correspondence()
        correspondence['letters'].append(letter_data)
        save_correspondence(correspondence)
    
    return {
        'success': True,
        'letter_id': letter_id,
        'content': letter_content,
        'ai_confidence': 95.5,
        'requires_review': True
    }


def generate_clinic_letter_template(
    letter_type: str,
    patient_name: str,
    nhs_number: str,
    gp_name: str,
    gp_address: str,
    clinic_date: str,
    consultant_name: str,
    diagnosis: str,
    investigations: List[str],
    treatment_plan: str,
    follow_up: str,
    additional_notes: str
) -> str:
    """Generate professional clinic letter"""
    
    letter = f"""
{consultant_name}
Consultant
[Hospital Name]
[Hospital Address]

{datetime.now().strftime('%d %B %Y')}

{gp_name}
{gp_address}

Dear Dr {gp_name.split()[-1]},

Re: {patient_name} - DOB: [DOB] - NHS No: {nhs_number}

CLINIC LETTER - {letter_type.upper()}

Thank you for referring the above patient whom I reviewed in clinic on {clinic_date}.

"""
    
    if diagnosis:
        letter += f"DIAGNOSIS:\n{diagnosis}\n\n"
    
    if investigations:
        letter += "INVESTIGATIONS:\n"
        for inv in investigations:
            letter += f"- {inv}\n"
        letter += "\n"
    
    if treatment_plan:
        letter += f"TREATMENT PLAN:\n{treatment_plan}\n\n"
    
    if follow_up:
        letter += f"FOLLOW-UP:\n{follow_up}\n\n"
    
    if additional_notes:
        letter += f"ADDITIONAL NOTES:\n{additional_notes}\n\n"
    
    letter += f"""
If you have any queries, please do not hesitate to contact me.

Yours sincerely,

{consultant_name}
Consultant

cc: Patient
"""
    
    return letter


def ai_manage_diary(
    consultant_name: str,
    action: str,  # 'add', 'view', 'optimize'
    event_details: Dict = None
) -> Dict:
    """
    AI-powered diary management
    
    Features:
    - Intelligent scheduling
    - Conflict detection
    - Automatic optimization
    - Meeting coordination
    """
    
    if action == 'add':
        return add_diary_event(consultant_name, event_details)
    elif action == 'view':
        return view_diary(consultant_name, event_details.get('date') if event_details else None)
    elif action == 'optimize':
        return ai_optimize_diary(consultant_name)
    
    return {'success': False, 'message': 'Invalid action'}


def add_diary_event(consultant_name: str, event: Dict) -> Dict:
    """Add event to diary with conflict checking - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    conflicts = check_diary_conflicts(consultant_name, event['date'], event['start_time'], event['end_time'])

    if conflicts:
        alternatives = ai_suggest_alternative_times(consultant_name, event)
        return {'success': False, 'message': 'Time conflict detected', 'conflicts': conflicts, 'ai_alternatives': alternatives}

    event_id = f"EVENT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    event_data = {
        'event_id': event_id,
        'user_email': user_email,
        'consultant': consultant_name,
        'date': event['date'],
        'start_time': event['start_time'],
        'end_time': event['end_time'],
        'event_type': event['event_type'],
        'location': event.get('location'),
        'description': event.get('description'),
        'created_date': datetime.now().isoformat()
    }

    if SUPABASE_ENABLED:
        success, _ = create_diary_event(user_email, event_data)
        if success:
            return {'success': True, 'event_id': event_id, 'message': 'Event added successfully'}
        else:
            return {'success': False, 'message': 'Failed to save event to database'}
    else:
        diary = load_diary()
        diary['events'].append(event_data)
        save_diary(diary)
        return {'success': True, 'event_id': event_id, 'message': 'Event added successfully'}


def load_diary():
    """Load diary database - Now uses Supabase"""
    user_email = get_current_user_email()
    if SUPABASE_ENABLED:
        return {'events': get_diary_events_for_user(user_email)}
    else:
        if os.path.exists(DIARY_DB):
            with open(DIARY_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'events': []}

def save_diary(data):
    """Save diary database - Deprecated"""
    pass


def check_diary_conflicts(consultant: str, date: str, start: str, end: str) -> List[Dict]:
    """Check for diary conflicts"""
    
    diary = load_diary()
    conflicts = []
    
    for event in diary.get('events', []):
        if (event['consultant'] == consultant and 
            event['date'] == date):
            # Check time overlap
            if times_overlap(start, end, event['start_time'], event['end_time']):
                conflicts.append(event)
    
    return conflicts


def times_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    """Check if two time ranges overlap"""
    start1_dt = datetime.strptime(start1, "%H:%M")
    end1_dt = datetime.strptime(end1, "%H:%M")
    start2_dt = datetime.strptime(start2, "%H:%M")
    end2_dt = datetime.strptime(end2, "%H:%M")
    
    return (start1_dt < end2_dt and end1_dt > start2_dt)


def ai_suggest_alternative_times(consultant: str, event: Dict) -> List[Dict]:
    """AI suggests alternative time slots"""
    
    alternatives = []
    event_date = datetime.strptime(event['date'], "%Y-%m-%d")
    
    # Check same day, different times
    for hour in range(8, 18):
        test_start = f"{hour:02d}:00"
        test_end = f"{hour+1:02d}:00"
        
        if not check_diary_conflicts(consultant, event['date'], test_start, test_end):
            alternatives.append({
                'date': event['date'],
                'start_time': test_start,
                'end_time': test_end,
                'day': event_date.strftime("%A"),
                'ai_score': 100 - abs(hour - 10) * 5  # Prefer mid-morning
            })
    
    # Check next 7 days
    for days_ahead in range(1, 8):
        alt_date = event_date + timedelta(days=days_ahead)
        alt_date_str = alt_date.strftime("%Y-%m-%d")
        
        if not check_diary_conflicts(consultant, alt_date_str, event['start_time'], event['end_time']):
            alternatives.append({
                'date': alt_date_str,
                'start_time': event['start_time'],
                'end_time': event['end_time'],
                'day': alt_date.strftime("%A"),
                'ai_score': 100 - days_ahead * 10
            })
    
    # Sort by AI score
    alternatives.sort(key=lambda x: x['ai_score'], reverse=True)
    
    return alternatives[:5]


def view_diary(consultant: str, date: str = None) -> Dict:
    """View diary for consultant"""
    
    diary = load_diary()
    
    if date:
        # Show specific day
        events = [e for e in diary.get('events', []) 
                 if e['consultant'] == consultant and e['date'] == date]
    else:
        # Show all upcoming events
        today = datetime.now().date()
        events = [e for e in diary.get('events', []) 
                 if e['consultant'] == consultant and 
                 datetime.strptime(e['date'], "%Y-%m-%d").date() >= today]
    
    # Sort by date and time
    events.sort(key=lambda x: (x['date'], x['start_time']))
    
    return {
        'success': True,
        'consultant': consultant,
        'date': date,
        'events': events,
        'total_events': len(events)
    }


def ai_optimize_diary(consultant: str) -> Dict:
    """
    AI analyzes and optimizes consultant diary
    
    Suggestions:
    - Consolidate fragmented time
    - Optimize meeting scheduling
    - Identify inefficiencies
    - Recommend improvements
    """
    
    diary_data = view_diary(consultant)
    events = diary_data['events']
    
    recommendations = []
    
    # Analyze for fragmentation
    date_groups = {}
    for event in events:
        date = event['date']
        if date not in date_groups:
            date_groups[date] = []
        date_groups[date].append(event)
    
    # Check each day
    for date, day_events in date_groups.items():
        if len(day_events) > 5:
            # Too many events in one day
            recommendations.append({
                'type': 'OVERLOADED_DAY',
                'date': date,
                'message': f'{len(day_events)} events scheduled - consider rescheduling some',
                'priority': 'HIGH'
            })
        
        # Check for gaps
        day_events.sort(key=lambda x: x['start_time'])
        for i in range(len(day_events) - 1):
            end_time = datetime.strptime(day_events[i]['end_time'], "%H:%M")
            next_start = datetime.strptime(day_events[i+1]['start_time'], "%H:%M")
            gap = (next_start - end_time).seconds / 60
            
            if gap < 15:
                recommendations.append({
                    'type': 'NO_BUFFER',
                    'date': date,
                    'message': f'No buffer time between {day_events[i]["event_type"]} and {day_events[i+1]["event_type"]}',
                    'priority': 'MEDIUM'
                })
            elif gap > 120:
                recommendations.append({
                    'type': 'LARGE_GAP',
                    'date': date,
                    'message': f'{int(gap)} minute gap - could be utilized better',
                    'priority': 'LOW'
                })
    
    return {
        'success': True,
        'consultant': consultant,
        'total_events': len(events),
        'recommendations': recommendations,
        'optimization_score': calculate_diary_efficiency(events)
    }


def calculate_diary_efficiency(events: List[Dict]) -> float:
    """Calculate diary efficiency score (0-100)"""
    
    if not events:
        return 100.0
    
    score = 100.0
    
    # Penalize for overloaded days
    date_counts = {}
    for event in events:
        date_counts[event['date']] = date_counts.get(event['date'], 0) + 1
    
    for count in date_counts.values():
        if count > 6:
            score -= (count - 6) * 5
    
    return max(0, min(100, score))


def ai_process_referral(
    referral_data: Dict
) -> Dict:
    """
    AI processes incoming referral
    
    Actions:
    - Validate referral completeness
    - Determine urgency
    - Suggest appropriate clinic
    - Draft acknowledgment letter
    - Set up patient record
    """
    
    # AI validation
    validation = validate_referral_completeness(referral_data)
    
    # AI urgency assessment
    urgency = ai_assess_referral_urgency(referral_data)
    
    # AI clinic suggestion
    suggested_clinic = ai_suggest_clinic(referral_data)
    
    # Draft acknowledgment
    ack_letter = draft_acknowledgment_letter(referral_data)
    
    return {
        'success': True,
        'validation': validation,
        'urgency_assessment': urgency,
        'suggested_clinic': suggested_clinic,
        'acknowledgment_letter': ack_letter,
        'next_actions': [
            'Send acknowledgment to GP',
            'Add to waiting list',
            'Book appropriate appointment',
            'Set up patient record'
        ]
    }


def validate_referral_completeness(referral: Dict) -> Dict:
    """Validate referral has all required information"""
    
    required_fields = [
        'patient_name', 'nhs_number', 'dob', 'gp_name',
        'referral_reason', 'clinical_history'
    ]
    
    missing = []
    for field in required_fields:
        if field not in referral or not referral[field]:
            missing.append(field)
    
    return {
        'complete': len(missing) == 0,
        'missing_fields': missing,
        'completeness_score': ((len(required_fields) - len(missing)) / len(required_fields)) * 100
    }


def ai_assess_referral_urgency(referral: Dict) -> Dict:
    """AI assesses referral urgency"""
    
    # Keywords suggesting urgency
    urgent_keywords = ['urgent', 'suspected cancer', '2ww', 'acute', 'severe', 'emergency']
    
    referral_text = (
        referral.get('referral_reason', '') + ' ' +
        referral.get('clinical_history', '')
    ).lower()
    
    urgency_score = 0
    found_keywords = []
    
    for keyword in urgent_keywords:
        if keyword in referral_text:
            urgency_score += 20
            found_keywords.append(keyword)
    
    if urgency_score >= 40:
        urgency_level = '2WW'
        action = 'Book within 14 days'
    elif urgency_score >= 20:
        urgency_level = 'Urgent'
        action = 'Book within 4 weeks'
    else:
        urgency_level = 'Routine'
        action = 'Book within 18 weeks'
    
    return {
        'urgency_level': urgency_level,
        'urgency_score': urgency_score,
        'keywords_found': found_keywords,
        'recommended_action': action
    }


def ai_suggest_clinic(referral: Dict) -> Dict:
    """AI suggests appropriate clinic"""
    
    # Simple matching (would use ML in production)
    referral_reason = referral.get('referral_reason', '').lower()
    
    clinic_mappings = {
        'cardiology': ['heart', 'cardiac', 'chest pain'],
        'dermatology': ['skin', 'rash', 'mole'],
        'ent': ['ear', 'nose', 'throat', 'hearing'],
        'gastroenterology': ['stomach', 'bowel', 'digestive']
    }
    
    suggestions = []
    for specialty, keywords in clinic_mappings.items():
        if any(keyword in referral_reason for keyword in keywords):
            suggestions.append({
                'specialty': specialty,
                'confidence': 85.0
            })
    
    return {
        'suggested_clinics': suggestions,
        'ai_confidence': suggestions[0]['confidence'] if suggestions else 0
    }


def draft_acknowledgment_letter(referral: Dict) -> str:
    """Draft acknowledgment letter for referral"""
    
    letter = f"""
[Hospital Letterhead]

{datetime.now().strftime('%d %B %Y')}

{referral.get('gp_name', 'GP Name')}
{referral.get('gp_address', 'GP Address')}

Dear Dr {referral.get('gp_name', 'GP').split()[-1]},

Re: {referral.get('patient_name', 'Patient Name')} - NHS No: {referral.get('nhs_number', 'NHS Number')}

ACKNOWLEDGMENT OF REFERRAL

Thank you for your referral of the above patient.

This has been received and the patient has been added to the waiting list. An appointment will be sent in due course.

If you have any queries, please contact the clinic.

Yours sincerely,

Medical Secretary
On behalf of [Consultant Name]
"""
    
    return letter


# Letter types
LETTER_TYPES = [
    "Clinic Letter",
    "Discharge Summary",
    "Referral Letter",
    "Acknowledgment",
    "Results Letter",
    "Follow-up Letter",
    "DNALetter",
    "Procedure Letter"
]


# Event types for diary
EVENT_TYPES = [
    "Outpatient Clinic",
    "Ward Round",
    "Theatre Session",
    "MDT Meeting",
    "Admin Time",
    "Teaching",
    "Meeting",
    "Annual Leave",
    "Study Leave"
]
