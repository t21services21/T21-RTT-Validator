"""
PARTIAL BOOKING LIST (PBL) SYSTEM
NHS-Compliant Workflow for Patients Awaiting First Appointment

WHAT IS PBL?
- Patients whose referral is accepted BUT no appointment slot available
- They are on PBL waiting for their FIRST appointment to be booked
- Once appointment is offered/booked, they automatically leave PBL
- Requires regular data cleansing and validation

NHS WORKFLOW:
1. Referral accepted → No slots available
2. Send acknowledgment email to patient
3. Add to Partial Booking List (PBL)
4. Monitor waiting times
5. When slot becomes available → Book appointment
6. Automatically remove from PBL when booked
7. Data cleansing to remove duplicates/errors

COMPLIANCE:
- RTT clock starts on referral receipt date
- PBL patients count toward RTT incomplete backlog
- Must be validated weekly
- Requires data cleansing by NHS experts
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# PBL Patient Structure
class PBLPatient:
    """Patient on Partial Booking List awaiting first appointment"""
    
    def __init__(self, patient_data: dict):
        self.nhs_number = patient_data.get('nhs_number')
        self.name = patient_data.get('name')
        self.dob = patient_data.get('dob')
        self.referral_date = patient_data.get('referral_date')
        self.specialty = patient_data.get('specialty')
        self.priority = patient_data.get('priority', 'Routine')
        self.contact_email = patient_data.get('email')
        self.contact_phone = patient_data.get('phone')
        self.referring_gp = patient_data.get('referring_gp')
        self.referral_reason = patient_data.get('referral_reason')
        self.added_to_pbl_date = patient_data.get('added_to_pbl_date', datetime.now().strftime('%Y-%m-%d'))
        self.acknowledgment_sent = patient_data.get('acknowledgment_sent', False)
        self.acknowledgment_date = patient_data.get('acknowledgment_date')
        self.weeks_waiting = self.calculate_weeks_waiting()
        self.rtt_breach_date = self.calculate_breach_date()
        self.status = patient_data.get('status', 'Active')
        self.notes = patient_data.get('notes', '')
        
    def calculate_weeks_waiting(self) -> int:
        """Calculate how many weeks patient has been waiting"""
        ref_date = datetime.strptime(self.referral_date, '%Y-%m-%d')
        days_waiting = (datetime.now() - ref_date).days
        return days_waiting // 7
    
    def calculate_breach_date(self) -> str:
        """Calculate when RTT will breach (18 weeks from referral)"""
        ref_date = datetime.strptime(self.referral_date, '%Y-%m-%d')
        breach_date = ref_date + timedelta(weeks=18)
        return breach_date.strftime('%Y-%m-%d')
    
    def days_until_breach(self) -> int:
        """Days until RTT breach"""
        breach_date = datetime.strptime(self.rtt_breach_date, '%Y-%m-%d')
        return (breach_date - datetime.now()).days
    
    def is_at_risk(self) -> bool:
        """Is patient at risk of RTT breach? (<4 weeks until breach)"""
        return self.days_until_breach() < 28
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            'nhs_number': self.nhs_number,
            'name': self.name,
            'dob': self.dob,
            'referral_date': self.referral_date,
            'specialty': self.specialty,
            'priority': self.priority,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'referring_gp': self.referring_gp,
            'referral_reason': self.referral_reason,
            'added_to_pbl_date': self.added_to_pbl_date,
            'acknowledgment_sent': self.acknowledgment_sent,
            'acknowledgment_date': self.acknowledgment_date,
            'weeks_waiting': self.weeks_waiting,
            'rtt_breach_date': self.rtt_breach_date,
            'days_until_breach': self.days_until_breach(),
            'is_at_risk': self.is_at_risk(),
            'status': self.status,
            'notes': self.notes
        }


# ============================================
# PBL MANAGEMENT FUNCTIONS
# ============================================

def add_to_pbl(patient_data: dict, send_acknowledgment: bool = True) -> dict:
    """
    Add patient to Partial Booking List
    
    Returns: {'success': bool, 'message': str, 'patient': dict}
    """
    try:
        # Create PBL patient
        pbl_patient = PBLPatient(patient_data)
        
        # Check if already on PBL
        existing_pbl = load_pbl_patients()
        if any(p['nhs_number'] == pbl_patient.nhs_number for p in existing_pbl):
            return {
                'success': False,
                'message': f"Patient {pbl_patient.nhs_number} already on PBL",
                'patient': None
            }
        
        # Send acknowledgment email if requested
        if send_acknowledgment and pbl_patient.contact_email:
            acknowledgment_result = send_pbl_acknowledgment_email(pbl_patient)
            pbl_patient.acknowledgment_sent = acknowledgment_result['sent']
            pbl_patient.acknowledgment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if acknowledgment_result['sent'] else None
        
        # Add to PBL
        existing_pbl.append(pbl_patient.to_dict())
        save_pbl_patients(existing_pbl)
        
        return {
            'success': True,
            'message': f"Patient {pbl_patient.name} added to PBL successfully",
            'patient': pbl_patient.to_dict()
        }
    
    except Exception as e:
        return {
            'success': False,
            'message': f"Error adding to PBL: {str(e)}",
            'patient': None
        }


def remove_from_pbl(nhs_number: str, reason: str = "Appointment Booked") -> dict:
    """
    Remove patient from PBL (usually because appointment was booked)
    
    Returns: {'success': bool, 'message': str}
    """
    try:
        pbl_patients = load_pbl_patients()
        
        # Find patient
        patient_found = False
        updated_pbl = []
        removed_patient = None
        
        for patient in pbl_patients:
            if patient['nhs_number'] == nhs_number:
                patient_found = True
                removed_patient = patient
                # Log removal
                log_pbl_removal(patient, reason)
            else:
                updated_pbl.append(patient)
        
        if not patient_found:
            return {
                'success': False,
                'message': f"Patient {nhs_number} not found on PBL"
            }
        
        # Save updated PBL
        save_pbl_patients(updated_pbl)
        
        return {
            'success': True,
            'message': f"Patient {removed_patient['name']} removed from PBL ({reason})"
        }
    
    except Exception as e:
        return {
            'success': False,
            'message': f"Error removing from PBL: {str(e)}"
        }


def load_pbl_patients() -> List[dict]:
    """Load all PBL patients"""
    try:
        with open('data/pbl_patients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []


def save_pbl_patients(patients: List[dict]):
    """Save PBL patients"""
    import os
    os.makedirs('data', exist_ok=True)
    with open('data/pbl_patients.json', 'w') as f:
        json.dump(patients, f, indent=2)


def log_pbl_removal(patient: dict, reason: str):
    """Log when patient removed from PBL for audit trail"""
    try:
        log_entry = {
            'nhs_number': patient['nhs_number'],
            'name': patient['name'],
            'removed_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reason': reason,
            'days_on_pbl': (datetime.now() - datetime.strptime(patient['added_to_pbl_date'], '%Y-%m-%d')).days
        }
        
        # Load existing log
        try:
            with open('data/pbl_removal_log.json', 'r') as f:
                log = json.load(f)
        except FileNotFoundError:
            log = []
        
        log.append(log_entry)
        
        # Save log
        import os
        os.makedirs('data', exist_ok=True)
        with open('data/pbl_removal_log.json', 'w') as f:
            json.dump(log, f, indent=2)
    
    except Exception as e:
        print(f"Error logging PBL removal: {e}")


# ============================================
# ACKNOWLEDGMENT EMAIL SYSTEM
# ============================================

def send_pbl_acknowledgment_email(patient: PBLPatient) -> dict:
    """
    Send acknowledgment email to patient confirming referral received
    and they're on PBL awaiting appointment
    
    Returns: {'sent': bool, 'message': str}
    """
    try:
        email_content = generate_pbl_acknowledgment_email(patient)
        
        # In production, integrate with NHS email system
        # For now, log the email
        log_email_sent(patient, email_content)
        
        return {
            'sent': True,
            'message': f"Acknowledgment email sent to {patient.contact_email}"
        }
    
    except Exception as e:
        return {
            'sent': False,
            'message': f"Failed to send email: {str(e)}"
        }


def generate_pbl_acknowledgment_email(patient: PBLPatient) -> str:
    """Generate acknowledgment email content"""
    
    email_template = f"""
FROM: {patient.specialty} Department
      NHS Trust Appointments Team

TO:   {patient.name}
      {patient.contact_email}

Date: {datetime.now().strftime('%d %B %Y')}

=====================================

Dear {patient.name},

RE: Acknowledgment of Referral - {patient.specialty}

We are writing to confirm that we have received and accepted your referral from {patient.referring_gp} for {patient.specialty} assessment.

**REFERRAL DETAILS:**
NHS Number: {patient.nhs_number}
Date of Birth: {patient.dob}
Referral Date: {datetime.strptime(patient.referral_date, '%Y-%m-%d').strftime('%d %B %Y')}
Specialty: {patient.specialty}
Priority: {patient.priority}

**WHAT HAPPENS NEXT:**

You have been added to our Partial Booking List as we currently do not have an available appointment slot. We will contact you as soon as an appointment becomes available.

**IMPORTANT INFORMATION:**

✅ Your referral has been ACCEPTED
✅ You are on our waiting list for an appointment
✅ We will contact you when a slot becomes available
✅ Please keep your contact details up to date

**Expected Wait Time:** We aim to offer you an appointment within {18 - patient.weeks_waiting} weeks to meet the NHS 18-week RTT standard.

**WHAT TO DO IF YOUR CONDITION WORSENS:**

If your symptoms worsen or you have concerns while waiting, please contact:
- Your GP surgery
- NHS 111 (for urgent advice)
- 999 (for emergencies)

**CONTACT INFORMATION:**

If your contact details change or you have any questions, please contact us:
- Phone: 01234 567890
- Email: appointments@trust.nhs.uk

**CANCELLATION:**

If you no longer require this appointment or have been seen elsewhere, please let us know immediately.

Thank you for your patience.

Yours sincerely,

Appointments Team
{patient.specialty} Department
NHS Trust

=====================================

This is an automated email. Please do not reply directly to this email.
For enquiries, please use the contact details above.
    """
    
    return email_template


def log_email_sent(patient: PBLPatient, email_content: str):
    """Log acknowledgment emails for audit trail"""
    try:
        import os
        os.makedirs('data/pbl_emails', exist_ok=True)
        
        filename = f"data/pbl_emails/{patient.nhs_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(email_content)
    except Exception as e:
        print(f"Error logging email: {e}")


# ============================================
# DATA CLEANSING FUNCTIONS
# ============================================

def validate_pbl_data() -> dict:
    """
    NHS Data Cleansing - Validate PBL data quality
    Returns issues that need expert review
    """
    pbl_patients = load_pbl_patients()
    
    issues = {
        'duplicates': [],
        'missing_data': [],
        'invalid_nhs_numbers': [],
        'overdue_acknowledgments': [],
        'breach_risks': [],
        'long_waiters': []
    }
    
    seen_nhs_numbers = set()
    
    for patient in pbl_patients:
        # Check for duplicates
        if patient['nhs_number'] in seen_nhs_numbers:
            issues['duplicates'].append(patient)
        seen_nhs_numbers.add(patient['nhs_number'])
        
        # Check for missing data
        required_fields = ['name', 'dob', 'contact_email', 'contact_phone']
        missing = [f for f in required_fields if not patient.get(f)]
        if missing:
            issues['missing_data'].append({
                'patient': patient,
                'missing_fields': missing
            })
        
        # Check NHS number format (basic validation)
        if not patient['nhs_number'] or len(patient['nhs_number'].replace(' ', '')) != 10:
            issues['invalid_nhs_numbers'].append(patient)
        
        # Check acknowledgment sent
        if not patient.get('acknowledgment_sent'):
            issues['overdue_acknowledgments'].append(patient)
        
        # Check breach risk
        if patient.get('days_until_breach', 999) < 28:
            issues['breach_risks'].append(patient)
        
        # Check long waiters (>12 weeks)
        if patient.get('weeks_waiting', 0) > 12:
            issues['long_waiters'].append(patient)
    
    return issues


def clean_pbl_duplicates() -> dict:
    """Remove duplicate entries from PBL"""
    pbl_patients = load_pbl_patients()
    
    seen = set()
    cleaned = []
    removed = []
    
    for patient in pbl_patients:
        nhs_num = patient['nhs_number']
        if nhs_num not in seen:
            seen.add(nhs_num)
            cleaned.append(patient)
        else:
            removed.append(patient)
    
    save_pbl_patients(cleaned)
    
    return {
        'removed_count': len(removed),
        'remaining_count': len(cleaned),
        'removed_patients': removed
    }


# Export functions
__all__ = [
    'PBLPatient',
    'add_to_pbl',
    'remove_from_pbl',
    'load_pbl_patients',
    'send_pbl_acknowledgment_email',
    'validate_pbl_data',
    'clean_pbl_duplicates'
]
