"""
CLINICAL LETTER GENERATOR
Generate professional clinical letters from MDT decisions, referrals, appointments

Features:
- MDT outcome letters to GP
- MDT outcome letters to patient
- Referral letters
- Appointment confirmation letters
- Discharge summaries
- Template management
"""

from datetime import datetime
from typing import Dict, Optional
import streamlit as st


def generate_mdt_gp_letter(
    patient_name: str,
    nhs_number: str,
    gp_name: str,
    gp_practice: str,
    meeting_date: str,
    specialty: str,
    diagnosis: str,
    mdt_outcome: str,
    mdt_decision: str,
    actions: list,
    next_steps: str,
    consultant_name: str = "Consultant"
) -> str:
    """Generate letter to GP from MDT outcome"""
    
    letter = f"""
{gp_practice}
{gp_name}

Date: {datetime.now().strftime('%d %B %Y')}

Dear Dr {gp_name},

RE: {patient_name} (NHS: {nhs_number})

I am writing to inform you of the outcome of the Multi-Disciplinary Team (MDT) meeting held on {meeting_date}, where your patient was discussed.

PATIENT DETAILS:
Name: {patient_name}
NHS Number: {nhs_number}
Date of MDT: {meeting_date}
Specialty: {specialty}

CLINICAL SUMMARY:
Diagnosis: {diagnosis}

MDT DISCUSSION:
The case was presented and discussed at our {specialty} MDT meeting. The consensus of the multidisciplinary team was:

Outcome: {mdt_outcome}

MANAGEMENT PLAN:
{mdt_decision}

ACTIONS AGREED:
"""
    
    for idx, action in enumerate(actions, 1):
        letter += f"{idx}. {action}\n"
    
    letter += f"""
NEXT STEPS:
{next_steps}

We will continue to keep you informed of your patient's progress. Please do not hesitate to contact us if you require any further information.

Yours sincerely,

{consultant_name}
{specialty} Consultant

cc: Patient
"""
    
    return letter


def generate_mdt_patient_letter(
    patient_name: str,
    patient_address: str,
    meeting_date: str,
    specialty: str,
    diagnosis: str,
    mdt_outcome: str,
    treatment_plan: str,
    next_appointment: str,
    contact_number: str,
    consultant_name: str = "Consultant"
) -> str:
    """Generate letter to patient from MDT outcome"""
    
    letter = f"""
{patient_name}
{patient_address}

Date: {datetime.now().strftime('%d %B %Y')}

Dear {patient_name},

RE: Your recent hospital appointment and treatment plan

Thank you for allowing us to discuss your care at our Multi-Disciplinary Team (MDT) meeting on {meeting_date}.

WHAT WE DISCUSSED:
Your case was discussed by a team of specialist doctors and healthcare professionals from different areas. This helps us ensure you receive the best possible care.

Diagnosis: {diagnosis}

RECOMMENDED TREATMENT:
Following careful consideration, the team has recommended:

{treatment_plan}

WHAT HAPPENS NEXT:
{next_appointment}

IMPORTANT INFORMATION:
- Please attend all scheduled appointments
- Bring this letter with you to your next appointment
- Contact us immediately if you have any concerns
- Keep your GP informed of any changes

If you have any questions about this letter or your treatment, please contact:
{specialty} Department
Telephone: {contact_number}

We are here to support you throughout your treatment.

Yours sincerely,

{consultant_name}
{specialty} Consultant

cc: GP
"""
    
    return letter


def generate_appointment_confirmation_letter(
    patient_name: str,
    patient_address: str,
    nhs_number: str,
    appointment_date: str,
    appointment_time: str,
    appointment_type: str,
    location: str,
    consultant_name: str,
    specialty: str,
    special_instructions: str = "",
    contact_number: str = "01234 567890"
) -> str:
    """Generate appointment confirmation letter"""
    
    letter = f"""
{patient_name}
{patient_address}

Date: {datetime.now().strftime('%d %B %Y')}

Dear {patient_name},

RE: Appointment Confirmation (NHS: {nhs_number})

APPOINTMENT DETAILS:
Date: {appointment_date}
Time: {appointment_time}
Type: {appointment_type}
Location: {location}
Consultant: {consultant_name}
Specialty: {specialty}

IMPORTANT - PLEASE READ:

BEFORE YOUR APPOINTMENT:
- Arrive 10 minutes early
- Bring this letter with you
- Bring a list of current medications
- Bring any relevant medical records or test results

"""
    
    if special_instructions:
        letter += f"""SPECIAL INSTRUCTIONS:
{special_instructions}

"""
    
    letter += f"""IF YOU CANNOT ATTEND:
Please contact us as soon as possible on {contact_number} so we can offer the appointment to another patient.

Missing appointments without notice (DNA) affects other patients waiting for care.

PARKING:
Limited parking is available on site. Please allow extra time.

CONTACT DETAILS:
Telephone: {contact_number}
Monday to Friday: 9:00 AM - 5:00 PM

We look forward to seeing you at your appointment.

Yours sincerely,

Appointments Team
{specialty} Department
"""
    
    return letter


def generate_referral_letter(
    patient_name: str,
    nhs_number: str,
    date_of_birth: str,
    referring_clinician: str,
    referring_specialty: str,
    receiving_clinician: str,
    receiving_specialty: str,
    referral_reason: str,
    clinical_history: str,
    current_medications: str,
    investigations: str,
    priority: str = "Routine"
) -> str:
    """Generate referral letter"""
    
    letter = f"""
{receiving_specialty} Department
{receiving_clinician}

Date: {datetime.now().strftime('%d %B %Y')}

Dear Dr {receiving_clinician},

RE: Referral - {patient_name} (NHS: {nhs_number})

I would be grateful if you could see this patient in your {receiving_specialty} clinic.

PATIENT DETAILS:
Name: {patient_name}
NHS Number: {nhs_number}
Date of Birth: {date_of_birth}
Priority: {priority}

REASON FOR REFERRAL:
{referral_reason}

CLINICAL HISTORY:
{clinical_history}

CURRENT MEDICATIONS:
{current_medications}

INVESTIGATIONS PERFORMED:
{investigations}

I would appreciate your expert opinion and management of this patient.

Thank you for your assistance.

Yours sincerely,

{referring_clinician}
{referring_specialty} Consultant
"""
    
    return letter


def generate_discharge_summary(
    patient_name: str,
    nhs_number: str,
    date_of_birth: str,
    admission_date: str,
    discharge_date: str,
    diagnosis: str,
    treatment_given: str,
    discharge_medications: str,
    follow_up_plan: str,
    gp_name: str,
    consultant_name: str,
    specialty: str
) -> str:
    """Generate discharge summary"""
    
    letter = f"""
GP Practice
Dr {gp_name}

Date: {datetime.now().strftime('%d %B %Y')}

Dear Dr {gp_name},

RE: Discharge Summary - {patient_name} (NHS: {nhs_number})

PATIENT DETAILS:
Name: {patient_name}
NHS Number: {nhs_number}
Date of Birth: {date_of_birth}

ADMISSION DETAILS:
Admission Date: {admission_date}
Discharge Date: {discharge_date}
Specialty: {specialty}
Consultant: {consultant_name}

DIAGNOSIS:
{diagnosis}

TREATMENT PROVIDED:
{treatment_given}

DISCHARGE MEDICATIONS:
{discharge_medications}

FOLLOW-UP ARRANGEMENTS:
{follow_up_plan}

Please do not hesitate to contact us if you require any further information.

Yours sincerely,

{consultant_name}
{specialty} Consultant
"""
    
    return letter


# Letter templates dictionary
LETTER_TEMPLATES = {
    'MDT_GP': {
        'name': 'MDT Outcome Letter to GP',
        'description': 'Inform GP of MDT decisions and management plan',
        'generator': generate_mdt_gp_letter
    },
    'MDT_PATIENT': {
        'name': 'MDT Outcome Letter to Patient',
        'description': 'Explain MDT decisions and treatment plan to patient',
        'generator': generate_mdt_patient_letter
    },
    'APPOINTMENT': {
        'name': 'Appointment Confirmation',
        'description': 'Confirm upcoming appointment details',
        'generator': generate_appointment_confirmation_letter
    },
    'REFERRAL': {
        'name': 'Referral Letter',
        'description': 'Refer patient to another specialty',
        'generator': generate_referral_letter
    },
    'DISCHARGE': {
        'name': 'Discharge Summary',
        'description': 'Summary of hospital admission and treatment',
        'generator': generate_discharge_summary
    }
}


def format_letter_for_print(letter_content: str) -> str:
    """Format letter for printing with proper styling"""
    
    # Add NHS header styling
    formatted = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20mm;
        }}
        .nhs-header {{
            border-bottom: 3px solid #005EB8;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .nhs-logo {{
            color: #005EB8;
            font-weight: bold;
            font-size: 18pt;
        }}
        pre {{
            white-space: pre-wrap;
            font-family: Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <div class="nhs-header">
        <div class="nhs-logo">NHS Trust</div>
    </div>
    <pre>{letter_content}</pre>
</body>
</html>
"""
    return formatted
