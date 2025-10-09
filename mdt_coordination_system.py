"""
T21 MDT (MULTI-DISCIPLINARY TEAM) COORDINATION SYSTEM
Complete AI-powered MDT meeting and patient management

Features:
- MDT meeting scheduling and management
- Patient list management for MDT
- Outcome recording
- Action tracking
- Automatic reporting
- AI recommendations for MDT decisions

For MDT Administrators and MDT Coordinators
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# Database files
MDT_MEETINGS_DB = "mdt_meetings.json"
MDT_PATIENTS_DB = "mdt_patients.json"


def load_mdt_meetings():
    """Load MDT meetings database"""
    if os.path.exists(MDT_MEETINGS_DB):
        with open(MDT_MEETINGS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'meetings': []}


def save_mdt_meetings(data):
    """Save MDT meetings database"""
    with open(MDT_MEETINGS_DB, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_mdt_patients():
    """Load MDT patients database"""
    if os.path.exists(MDT_PATIENTS_DB):
        with open(MDT_PATIENTS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'patients': []}


def save_mdt_patients(data):
    """Save MDT patients database"""
    with open(MDT_PATIENTS_DB, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def create_mdt_meeting(
    meeting_date: str,
    meeting_time: str,
    specialty: str,
    location: str,
    chair: str,
    attendees: List[str],
    meeting_type: str = "Regular",
    notes: str = ""
) -> str:
    """Create new MDT meeting"""
    
    meetings = load_mdt_meetings()
    
    meeting_id = f"MDT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    meeting = {
        'meeting_id': meeting_id,
        'meeting_date': meeting_date,
        'meeting_time': meeting_time,
        'specialty': specialty,
        'location': location,
        'chair': chair,
        'attendees': attendees,
        'meeting_type': meeting_type,
        'status': 'SCHEDULED',
        'patients': [],
        'outcomes': [],
        'notes': notes,
        'created_date': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat()
    }
    
    meetings['meetings'].append(meeting)
    save_mdt_meetings(meetings)
    
    return meeting_id


def add_patient_to_mdt(
    meeting_id: str,
    patient_name: str,
    nhs_number: str,
    diagnosis: str,
    presenting_clinician: str,
    discussion_points: str,
    urgency: str = "Standard",
    presentation_order: int = None
) -> bool:
    """Add patient to MDT meeting"""
    
    meetings = load_mdt_meetings()
    
    for meeting in meetings['meetings']:
        if meeting['meeting_id'] == meeting_id:
            # Determine presentation order
            if presentation_order is None:
                presentation_order = len(meeting['patients']) + 1
            
            patient = {
                'patient_name': patient_name,
                'nhs_number': nhs_number,
                'diagnosis': diagnosis,
                'presenting_clinician': presenting_clinician,
                'discussion_points': discussion_points,
                'urgency': urgency,
                'presentation_order': presentation_order,
                'outcome': '',
                'decision': '',
                'actions': [],
                'discussed': False,
                'added_date': datetime.now().isoformat()
            }
            
            meeting['patients'].append(patient)
            meeting['last_updated'] = datetime.now().isoformat()
            
            save_mdt_meetings(meetings)
            return True
    
    return False


def record_mdt_outcome(
    meeting_id: str,
    nhs_number: str,
    outcome: str,
    decision: str,
    actions: List[str],
    next_steps: str = ""
) -> bool:
    """Record MDT outcome for a patient"""
    
    meetings = load_mdt_meetings()
    
    for meeting in meetings['meetings']:
        if meeting['meeting_id'] == meeting_id:
            for patient in meeting['patients']:
                if patient['nhs_number'] == nhs_number:
                    patient['outcome'] = outcome
                    patient['decision'] = decision
                    patient['actions'] = actions
                    patient['next_steps'] = next_steps
                    patient['discussed'] = True
                    patient['outcome_recorded_date'] = datetime.now().isoformat()
                    
                    meeting['last_updated'] = datetime.now().isoformat()
                    save_mdt_meetings(meetings)
                    return True
    
    return False


def complete_mdt_meeting(meeting_id: str, summary: str = "") -> bool:
    """Mark MDT meeting as completed"""
    
    meetings = load_mdt_meetings()
    
    for meeting in meetings['meetings']:
        if meeting['meeting_id'] == meeting_id:
            meeting['status'] = 'COMPLETED'
            meeting['completion_date'] = datetime.now().isoformat()
            meeting['summary'] = summary
            
            # Count outcomes
            total_patients = len(meeting['patients'])
            discussed = sum(1 for p in meeting['patients'] if p['discussed'])
            
            meeting['total_patients'] = total_patients
            meeting['discussed_count'] = discussed
            meeting['not_discussed_count'] = total_patients - discussed
            
            save_mdt_meetings(meetings)
            return True
    
    return False


def get_all_mdt_meetings() -> List[Dict]:
    """Get all MDT meetings"""
    meetings = load_mdt_meetings()
    return meetings['meetings']


def get_upcoming_mdt_meetings() -> List[Dict]:
    """Get upcoming MDT meetings"""
    meetings = get_all_mdt_meetings()
    today = datetime.now().date()
    
    upcoming = []
    for meeting in meetings:
        if meeting['status'] != 'COMPLETED':
            meeting_date = datetime.fromisoformat(meeting['meeting_date']).date()
            if meeting_date >= today:
                upcoming.append(meeting)
    
    # Sort by date
    upcoming.sort(key=lambda x: x['meeting_date'])
    
    return upcoming


def get_mdt_meeting_by_id(meeting_id: str) -> Optional[Dict]:
    """Get specific MDT meeting"""
    meetings = get_all_mdt_meetings()
    for meeting in meetings:
        if meeting['meeting_id'] == meeting_id:
            return meeting
    return None


def search_mdt_meetings(
    specialty: str = None,
    status: str = None,
    date_from: str = None,
    date_to: str = None
) -> List[Dict]:
    """Search MDT meetings"""
    
    meetings = get_all_mdt_meetings()
    results = []
    
    for meeting in meetings:
        # Specialty filter
        if specialty and meeting['specialty'] != specialty:
            continue
        
        # Status filter
        if status and meeting['status'] != status:
            continue
        
        # Date range filter
        if date_from:
            if meeting['meeting_date'] < date_from:
                continue
        
        if date_to:
            if meeting['meeting_date'] > date_to:
                continue
        
        results.append(meeting)
    
    return results


def get_mdt_stats() -> Dict:
    """Get MDT statistics"""
    
    meetings = get_all_mdt_meetings()
    
    stats = {
        'total_meetings': len(meetings),
        'scheduled': 0,
        'completed': 0,
        'cancelled': 0,
        'total_patients_discussed': 0,
        'specialties': {},
        'upcoming_count': 0,
        'this_week': 0,
        'this_month': 0
    }
    
    if not meetings:
        return stats
    
    today = datetime.now().date()
    week_from_now = today + timedelta(days=7)
    month_from_now = today + timedelta(days=30)
    
    for meeting in meetings:
        # Count by status
        stats[meeting['status'].lower()] = stats.get(meeting['status'].lower(), 0) + 1
        
        # Count by specialty
        specialty = meeting['specialty']
        stats['specialties'][specialty] = stats['specialties'].get(specialty, 0) + 1
        
        # Count patients discussed
        if meeting['status'] == 'COMPLETED':
            stats['total_patients_discussed'] += meeting.get('discussed_count', 0)
        
        # Upcoming meetings
        meeting_date = datetime.fromisoformat(meeting['meeting_date']).date()
        if meeting_date >= today and meeting['status'] != 'COMPLETED':
            stats['upcoming_count'] += 1
            
            if meeting_date <= week_from_now:
                stats['this_week'] += 1
            
            if meeting_date <= month_from_now:
                stats['this_month'] += 1
    
    return stats


def ai_recommend_mdt_decision(patient_data: Dict) -> Dict:
    """
    AI recommendation for MDT decision
    Provides suggested questions and considerations
    """
    
    diagnosis = patient_data.get('diagnosis', '')
    urgency = patient_data.get('urgency', 'Standard')
    discussion_points = patient_data.get('discussion_points', '')
    
    # AI-powered recommendations (simplified - would use GPT-4 in production)
    recommendations = {
        'suggested_questions': [
            "What is the current staging?",
            "What treatment options have been considered?",
            "What is the patient's performance status?",
            "Are there any contraindications for treatment?",
            "What are the patient's preferences?",
            "What is the timeline for treatment?"
        ],
        'considerations': [
            "Patient fitness for treatment",
            "Evidence-based treatment protocols",
            "Multi-modal treatment options",
            "Clinical trial eligibility",
            "Palliative care needs",
            "Patient support requirements"
        ],
        'typical_outcomes': [
            "Proceed to surgery",
            "Chemotherapy recommended",
            "Radiotherapy recommended",
            "Combined modality treatment",
            "Further investigations needed",
            "Palliative care referral",
            "Continue active monitoring"
        ],
        'urgency_recommendation': 'Urgent' if urgency == 'Urgent' else 'Standard',
        'priority_level': 'HIGH' if urgency == 'Urgent' else 'STANDARD'
    }
    
    return recommendations


def export_mdt_meeting_report(meeting_id: str) -> str:
    """Export MDT meeting report"""
    
    meeting = get_mdt_meeting_by_id(meeting_id)
    
    if not meeting:
        return ""
    
    report = f"""
MDT MEETING REPORT

Meeting ID: {meeting['meeting_id']}
Date: {meeting['meeting_date']}
Time: {meeting['meeting_time']}
Specialty: {meeting['specialty']}
Location: {meeting['location']}
Chair: {meeting['chair']}

ATTENDEES:
{chr(10).join(f'- {attendee}' for attendee in meeting['attendees'])}

PATIENTS DISCUSSED: {len([p for p in meeting['patients'] if p['discussed']])} / {len(meeting['patients'])}

PATIENT OUTCOMES:
"""
    
    for i, patient in enumerate(meeting['patients'], 1):
        report += f"""
{i}. {patient['patient_name']} (NHS: {patient['nhs_number']})
   Diagnosis: {patient['diagnosis']}
   Presenter: {patient['presenting_clinician']}
   """
        
        if patient['discussed']:
            report += f"""
   Outcome: {patient.get('outcome', 'Not recorded')}
   Decision: {patient.get('decision', 'Not recorded')}
   Actions: {', '.join(patient.get('actions', []))}
   """
        else:
            report += "   Status: NOT DISCUSSED\n"
    
    if meeting.get('summary'):
        report += f"\nMEETING SUMMARY:\n{meeting['summary']}\n"
    
    return report


# MDT specialties supported
MDT_SPECIALTIES = [
    "Cancer MDT",
    "Surgical MDT",
    "Medical MDT",
    "Radiology MDT",
    "Cardiac MDT",
    "Neurology MDT",
    "Respiratory MDT",
    "Gastroenterology MDT",
    "Orthopaedics MDT",
    "Other"
]


# Common MDT outcomes
MDT_OUTCOMES = [
    "Proceed to surgery",
    "Chemotherapy recommended",
    "Radiotherapy recommended",
    "Combined modality treatment",
    "Further investigations required",
    "Active surveillance",
    "Palliative care referral",
    "Discharge to GP",
    "Re-discuss at next MDT",
    "Second opinion required",
    "Clinical trial discussed",
    "Other"
]
