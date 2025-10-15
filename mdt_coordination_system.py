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

# Import Supabase functions for permanent storage
try:
    from supabase_database import (
        create_mdt_meeting as supabase_create_mdt_meeting,
        get_mdt_meetings_for_user,
        update_mdt_meeting as supabase_update_mdt_meeting,
        delete_mdt_meeting as supabase_delete_mdt_meeting
    )
    SUPABASE_ENABLED = True
except ImportError:
    SUPABASE_ENABLED = False
    print("⚠️ Supabase not available for MDT Module - using fallback storage")


def get_current_user_email():
    """Get current logged-in user's email"""
    try:
        import streamlit as st
        return st.session_state.get('user_email', 'demo@t21services.co.uk')
    except:
        return 'demo@t21services.co.uk'


# Database files (fallback only)
MDT_MEETINGS_DB = "mdt_meetings.json"


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


def load_mdt_meetings():
    """Load MDT meetings database - ADMINS SEE ALL DATA, students see only their own"""
    user_email = get_current_user_email()
    is_supervisor = is_admin_or_supervisor()
    
    print(f"🔍 DEBUG MDT: Loading for user: {user_email} (Admin: {is_supervisor})")
    
    if SUPABASE_ENABLED:
        if is_supervisor:
            # ADMINS/STAFF/TUTORS SEE ALL DATA
            try:
                from supabase_database import supabase
                result = supabase.table('mdt_meetings').select('*').execute()
                meetings = result.data if result.data else []
                print(f"🔍 DEBUG MDT: ADMIN MODE - Loaded {len(meetings)} meetings (ALL USERS)")
            except Exception as e:
                print(f"Error loading all MDT data: {e}")
                meetings = get_mdt_meetings_for_user(user_email)
                print(f"🔍 DEBUG MDT: Fallback to user mode - {len(meetings)} meetings")
        else:
            # STUDENTS SEE ONLY THEIR OWN DATA
            meetings = get_mdt_meetings_for_user(user_email)
            print(f"🔍 DEBUG MDT: STUDENT MODE - {len(meetings)} meetings for {user_email}")
        
        return {'meetings': meetings}
    else:
        if os.path.exists(MDT_MEETINGS_DB):
            with open(MDT_MEETINGS_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'meetings': []}


def save_mdt_meetings(data):
    """Save MDT meetings database - Deprecated, Supabase saves happen in individual functions"""
    pass


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
    """Create new MDT meeting - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    meeting_id = f"MDT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # CRITICAL FIX: Only send fields that EXIST in SQL table!
    meeting_data = {
        'meeting_id': meeting_id,
        'meeting_date': meeting_date,
        'meeting_time': meeting_time,
        'specialty': specialty,
        'location': location,
        'chair_person': chair,  # FIXED: Was 'chair', SQL expects 'chair_person'
        'attendees': attendees if isinstance(attendees, list) else [attendees],
        'patients_discussed': [],  # FIXED: Was 'patients', SQL expects 'patients_discussed'
        'decisions': [],  # FIXED: Was 'outcomes', SQL expects 'decisions'
        'action_points': [],
        'notes': f"Meeting Type: {meeting_type}\n{notes}",  # Store meeting_type in notes
        'status': 'scheduled'  # FIXED: lowercase to match SQL default
    }

    if SUPABASE_ENABLED:
        success, result = supabase_create_mdt_meeting(user_email, meeting_data)
        if success:
            return meeting_id
        else:
            # CRITICAL: Show error to user instead of hiding it!
            import streamlit as st
            st.error(f"❌ DATABASE ERROR: {result}")
            st.error("⚠️ Meeting NOT saved to database! Check error above.")
            print(f"Error saving MDT meeting to Supabase: {result}")
            raise Exception(f"Failed to save MDT meeting: {result}")
    else:
        meetings = load_mdt_meetings()
        meetings['meetings'].append(meeting_data)
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
    """Add patient to MDT meeting - NOW WITH SUPABASE!"""
    
    user_email = get_current_user_email()
    meeting = get_mdt_meeting_by_id(meeting_id)

    if not meeting:
        return False

    if presentation_order is None:
        current_patients = meeting.get('patients_discussed') or meeting.get('patients', [])
        presentation_order = len(current_patients) + 1

    patient_data = {
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

    # The 'patients_discussed' field is a JSONB array. We need to append to it.
    current_patients = meeting.get('patients_discussed') or meeting.get('patients', [])
    current_patients.append(patient_data)

    updates = {
        'patients_discussed': current_patients,
        'updated_at': datetime.now().isoformat()
    }

    if SUPABASE_ENABLED:
        success, _ = supabase_update_mdt_meeting(user_email, meeting_id, updates)
        return success
    else:
        # Fallback logic
        meetings = load_mdt_meetings()
        for m in meetings['meetings']:
            if m['meeting_id'] == meeting_id:
                m['patients_discussed'] = current_patients
                m['updated_at'] = datetime.now().isoformat()
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
    """Record MDT outcome for a patient - NOW WITH SUPABASE!"""

    user_email = get_current_user_email()
    meeting = get_mdt_meeting_by_id(meeting_id)

    if not meeting:
        return False

    # CRITICAL FIX: Use correct field name
    patients = meeting.get('patients_discussed') or meeting.get('patients', [])
    patient_updated = False
    for patient in patients:
        if patient.get('nhs_number') == nhs_number:
            patient['outcome'] = outcome
            patient['decision'] = decision
            patient['actions'] = actions
            patient['next_steps'] = next_steps
            patient['discussed'] = True
            patient['outcome_recorded_date'] = datetime.now().isoformat()
            patient_updated = True
            break

    if not patient_updated:
        return False

    updates = {
        'patients_discussed': patients,
        'updated_at': datetime.now().isoformat()
    }

    if SUPABASE_ENABLED:
        success, _ = supabase_update_mdt_meeting(user_email, meeting_id, updates)
        return success
    else:
        # Fallback logic
        meetings = load_mdt_meetings()
        for m in meetings['meetings']:
            if m['meeting_id'] == meeting_id:
                m['patients_discussed'] = patients
                m['updated_at'] = datetime.now().isoformat()
                save_mdt_meetings(meetings)
                return True
        return False


def complete_mdt_meeting(meeting_id: str, summary: str = "") -> bool:
    """Mark MDT meeting as completed - NOW WITH SUPABASE!"""

    user_email = get_current_user_email()
    meeting = get_mdt_meeting_by_id(meeting_id)

    if not meeting:
        return False

    # Get patients list (handle both old and new field names)
    patients = meeting.get('patients_discussed') or meeting.get('patients', [])
    total_patients = len(patients)
    discussed = sum(1 for p in patients if p.get('discussed'))

    updates = {
        'status': 'completed',  # FIXED: lowercase
        'notes': f"{meeting.get('notes', '')}\n\nMeeting Summary:\n{summary}\nTotal patients: {total_patients}\nDiscussed: {discussed}",
        'updated_at': datetime.now().isoformat()
    }

    if SUPABASE_ENABLED:
        success, _ = supabase_update_mdt_meeting(user_email, meeting_id, updates)
        return success
    else:
        # Fallback logic
        meetings = load_mdt_meetings()
        for m in meetings['meetings']:
            if m['meeting_id'] == meeting_id:
                m.update(updates)
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
    
    print(f"🔍 DEBUG: Total meetings loaded: {len(meetings)}")
    
    upcoming = []
    for meeting in meetings:
        try:
            # Check status (handle both upper and lowercase)
            status = meeting.get('status', '').lower()
            if status not in ['completed', 'cancelled']:
                # Handle different date formats
                meeting_date_str = str(meeting.get('meeting_date', ''))
                
                # Try to parse date
                try:
                    if 'T' in meeting_date_str:  # ISO format with time
                        meeting_date = datetime.fromisoformat(meeting_date_str).date()
                    else:  # Just date
                        meeting_date = datetime.fromisoformat(meeting_date_str).date()
                except:
                    # Try alternative parsing
                    meeting_date = datetime.strptime(meeting_date_str, '%Y-%m-%d').date()
                
                print(f"🔍 DEBUG: Meeting {meeting['meeting_id']} - Date: {meeting_date}, Today: {today}, Status: {status}")
                
                if meeting_date >= today:
                    upcoming.append(meeting)
                    print(f"✅ DEBUG: Meeting {meeting['meeting_id']} is upcoming!")
        except Exception as e:
            print(f"❌ ERROR processing meeting {meeting.get('meeting_id', 'unknown')}: {e}")
            continue
    
    print(f"🔍 DEBUG: Found {len(upcoming)} upcoming meetings")
    
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
        try:
            # Count by status (handle both cases)
            status = meeting.get('status', 'unknown').lower()
            stats[status] = stats.get(status, 0) + 1
            
            # Count by specialty
            specialty = meeting.get('specialty', 'Unknown')
            stats['specialties'][specialty] = stats['specialties'].get(specialty, 0) + 1
            
            # Count patients discussed (handle both cases)
            if status == 'completed':
                patients = meeting.get('patients_discussed') or meeting.get('patients', [])
                discussed = sum(1 for p in patients if p.get('discussed'))
                stats['total_patients_discussed'] += discussed
            
            # Upcoming meetings - handle date parsing
            try:
                meeting_date_str = str(meeting.get('meeting_date', ''))
                if 'T' in meeting_date_str:
                    meeting_date = datetime.fromisoformat(meeting_date_str).date()
                else:
                    meeting_date = datetime.strptime(meeting_date_str, '%Y-%m-%d').date()
                
                # Check if upcoming (not completed/cancelled)
                if meeting_date >= today and status not in ['completed', 'cancelled']:
                    stats['upcoming_count'] += 1
                    
                    if meeting_date <= week_from_now:
                        stats['this_week'] += 1
                    
                    if meeting_date <= month_from_now:
                        stats['this_month'] += 1
            except Exception as date_err:
                print(f"⚠️ ERROR parsing date for meeting {meeting.get('meeting_id')}: {date_err}")
        except Exception as e:
            print(f"⚠️ ERROR processing meeting stats: {e}")
            continue
    
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
Chair: {meeting.get('chair_person') or meeting.get('chair', 'N/A')}

ATTENDEES:
{chr(10).join(f'- {attendee}' for attendee in meeting.get('attendees', []))}

PATIENTS DISCUSSED: {len([p for p in (meeting.get('patients_discussed') or meeting.get('patients', [])) if p.get('discussed')])} / {len(meeting.get('patients_discussed') or meeting.get('patients', []))}

PATIENT OUTCOMES:
"""
    
    patients = meeting.get('patients_discussed') or meeting.get('patients', [])
    for i, patient in enumerate(patients, 1):
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
