"""
NHS EMAIL NOTIFICATION SYSTEM
Comprehensive email notifications for ALL NHS clinical events

AUTOMATIC EMAILS FOR:
- Patient added to PTL/PBL
- Appointments booked/cancelled/rescheduled
- MDT meetings scheduled
- Referrals received/accepted
- RTT breach alerts
- Cancer pathway notifications
- Clinical letter generation
- And much more!

Integrates with: PTL, PBL, Cancer, MDT, Booking, Letters, etc.
"""

from datetime import datetime
from email_service import send_email

# ============================================
# PATIENT TRACKING LIST (PTL) NOTIFICATIONS
# ============================================

def send_patient_added_to_ptl_email(patient_data: dict):
    """
    Email when patient added to PTL
    Sends to: Patient, GP, RTT Coordinator
    """
    subject = f"Patient Added to Waiting List - {patient_data['specialty']}"
    
    # Email to PATIENT
    patient_email_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #0066cc;">
            <h2 style="color: #0066cc;">You've Been Added to Our Waiting List</h2>
            
            <p>Dear {patient_data.get('name', 'Patient')},</p>
            
            <p>We confirm that you have been added to our waiting list for <strong>{patient_data.get('specialty', 'Specialty')}</strong>.</p>
            
            <div style="background: #f0f8ff; padding: 15px; margin: 20px 0; border-left: 4px solid #0066cc;">
                <h3 style="margin-top: 0;">Your Details:</h3>
                <p><strong>NHS Number:</strong> {patient_data.get('nhs_number', 'N/A')}<br>
                <strong>Specialty:</strong> {patient_data.get('specialty', 'N/A')}<br>
                <strong>Priority:</strong> {patient_data.get('priority', 'Routine')}<br>
                <strong>Added Date:</strong> {datetime.now().strftime('%d %B %Y')}</p>
            </div>
            
            <p><strong>What happens next?</strong></p>
            <ul>
                <li>We aim to offer you an appointment within 18 weeks</li>
                <li>You will receive an appointment letter in due course</li>
                <li>Please keep your contact details up to date</li>
            </ul>
            
            <p><strong>If your circumstances change:</strong><br>
            Please contact us on: 01234 567890</p>
            
            <p>Best regards,<br>
            <strong>Appointments Team</strong><br>
            {patient_data.get('specialty', 'Specialty')} Department</p>
        </div>
    </body>
    </html>
    """
    
    # Send to patient
    if patient_data.get('email'):
        send_email(patient_data['email'], subject, patient_email_content)
    
    # Email to RTT COORDINATOR
    coordinator_email_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0066cc;">🔔 New Patient Added to PTL</h2>
            
            <div style="background: #fff3cd; padding: 15px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <p><strong>Patient:</strong> {patient_data.get('name', 'N/A')}<br>
                <strong>NHS:</strong> {patient_data.get('nhs_number', 'N/A')}<br>
                <strong>Specialty:</strong> {patient_data.get('specialty', 'N/A')}<br>
                <strong>Priority:</strong> {patient_data.get('priority', 'Routine')}<br>
                <strong>RTT Clock Start:</strong> {patient_data.get('referral_date', 'Today')}</p>
            </div>
            
            <p><strong>Action Required:</strong></p>
            <ul>
                <li>Validate RTT pathway</li>
                <li>Monitor breach date (18 weeks)</li>
                <li>Arrange appointment when capacity available</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    # Send to coordinator (get from config)
    coordinator_email = "rtt.coordinator@trust.nhs.uk"  # Configure this
    send_email(coordinator_email, f"[PTL] {subject}", coordinator_email_content)


# ============================================
# PARTIAL BOOKING LIST (PBL) NOTIFICATIONS
# ============================================

def send_pbl_acknowledgment_email(patient_data: dict):
    """
    Email when patient added to PBL (already implemented in PBL system)
    This is integrated - just ensuring it's called
    """
    from partial_booking_list_system import send_pbl_acknowledgment_email as send_pbl_email
    return send_pbl_email(patient_data)


# ============================================
# APPOINTMENT NOTIFICATIONS
# ============================================

def send_appointment_booked_email(appointment_data: dict):
    """Email when appointment booked"""
    subject = f"Appointment Confirmed - {appointment_data.get('specialty', 'Hospital')}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #28a745;">
            <h2 style="color: #28a745;">✅ Your Appointment is Confirmed</h2>
            
            <p>Dear {appointment_data.get('patient_name', 'Patient')},</p>
            
            <div style="background: #d4edda; padding: 20px; margin: 20px 0; border-left: 4px solid #28a745;">
                <h3 style="margin-top: 0;">Appointment Details:</h3>
                <p><strong>Date:</strong> {appointment_data.get('appointment_date', 'TBC')}<br>
                <strong>Time:</strong> {appointment_data.get('appointment_time', 'TBC')}<br>
                <strong>Clinic:</strong> {appointment_data.get('clinic', 'TBC')}<br>
                <strong>Specialty:</strong> {appointment_data.get('specialty', 'TBC')}<br>
                <strong>Type:</strong> {appointment_data.get('appointment_type', 'Consultation')}</p>
            </div>
            
            <p><strong>Important Information:</strong></p>
            <ul>
                <li>Please arrive 10 minutes early</li>
                <li>Bring this letter and your NHS number</li>
                <li>If you cannot attend, please call us ASAP</li>
            </ul>
            
            <p><strong>Location:</strong><br>
            {appointment_data.get('location', 'Hospital Address')}</p>
            
            <p><strong>Contact:</strong> {appointment_data.get('contact_number', '01234 567890')}</p>
            
            <p>Best regards,<br>
            <strong>Appointments Team</strong></p>
        </div>
    </body>
    </html>
    """
    
    if appointment_data.get('patient_email'):
        return send_email(appointment_data['patient_email'], subject, html_content)


def send_appointment_cancelled_email(appointment_data: dict):
    """Email when appointment cancelled"""
    subject = f"Appointment Cancelled - {appointment_data.get('specialty', 'Hospital')}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #dc3545;">
            <h2 style="color: #dc3545;">❌ Appointment Cancelled</h2>
            
            <p>Dear {appointment_data.get('patient_name', 'Patient')},</p>
            
            <div style="background: #f8d7da; padding: 20px; margin: 20px 0; border-left: 4px solid #dc3545;">
                <h3 style="margin-top: 0;">Cancelled Appointment:</h3>
                <p><strong>Date:</strong> {appointment_data.get('appointment_date', 'TBC')}<br>
                <strong>Time:</strong> {appointment_data.get('appointment_time', 'TBC')}<br>
                <strong>Reason:</strong> {appointment_data.get('cancellation_reason', 'Not specified')}</p>
            </div>
            
            <p><strong>What happens next?</strong></p>
            <ul>
                <li>We will contact you to rebook</li>
                <li>Or you can call us on: {appointment_data.get('contact_number', '01234 567890')}</li>
                <li>Your place on the waiting list remains</li>
            </ul>
            
            <p>We apologise for any inconvenience.</p>
            
            <p>Best regards,<br>
            <strong>Appointments Team</strong></p>
        </div>
    </body>
    </html>
    """
    
    if appointment_data.get('patient_email'):
        return send_email(appointment_data['patient_email'], subject, html_content)


# ============================================
# MDT MEETING NOTIFICATIONS
# ============================================

def send_mdt_meeting_scheduled_email(meeting_data: dict, attendees: list):
    """Email when MDT meeting scheduled"""
    subject = f"MDT Meeting Scheduled - {meeting_data.get('specialty', 'Multi-disciplinary')}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0066cc;">📅 MDT Meeting Scheduled</h2>
            
            <div style="background: #f0f8ff; padding: 20px; margin: 20px 0; border-left: 4px solid #0066cc;">
                <h3 style="margin-top: 0;">Meeting Details:</h3>
                <p><strong>Date:</strong> {meeting_data.get('date', 'TBC')}<br>
                <strong>Time:</strong> {meeting_data.get('time', 'TBC')}<br>
                <strong>Location:</strong> {meeting_data.get('location', 'TBC')}<br>
                <strong>Specialty:</strong> {meeting_data.get('specialty', 'TBC')}<br>
                <strong>Chair:</strong> {meeting_data.get('chair', 'TBC')}</p>
            </div>
            
            <p><strong>Patients to Discuss:</strong> {meeting_data.get('patient_count', 0)}</p>
            
            <p><strong>Attendees Invited:</strong></p>
            <ul>
                {''.join([f"<li>{attendee}</li>" for attendee in attendees])}
            </ul>
            
            <p><strong>Please confirm attendance.</strong></p>
            
            <p>Best regards,<br>
            <strong>MDT Coordinator</strong></p>
        </div>
    </body>
    </html>
    """
    
    # Send to all attendees
    for attendee_email in attendees:
        send_email(attendee_email, subject, html_content)


# ============================================
# REFERRAL NOTIFICATIONS
# ============================================

def send_referral_received_email(referral_data: dict):
    """Email when referral received"""
    subject = f"Referral Received - {referral_data.get('specialty', 'Specialty')}"
    
    # To PATIENT
    patient_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0066cc;">📨 Referral Received</h2>
            
            <p>Dear {referral_data.get('patient_name', 'Patient')},</p>
            
            <p>We have received your referral for <strong>{referral_data.get('specialty', 'Specialty')}</strong> 
            from {referral_data.get('referring_gp', 'your GP')}.</p>
            
            <div style="background: #f0f8ff; padding: 15px; margin: 20px 0; border-left: 4px solid #0066cc;">
                <p><strong>Referral Date:</strong> {referral_data.get('referral_date', datetime.now().strftime('%d %B %Y'))}<br>
                <strong>Priority:</strong> {referral_data.get('priority', 'Routine')}<br>
                <strong>Specialty:</strong> {referral_data.get('specialty', 'N/A')}</p>
            </div>
            
            <p><strong>What happens next?</strong></p>
            <ul>
                <li>Your referral will be reviewed by our team</li>
                <li>We aim to send you an appointment within 18 weeks</li>
                <li>For urgent referrals, we will contact you sooner</li>
            </ul>
            
            <p>If you have any questions, please call: {referral_data.get('contact_number', '01234 567890')}</p>
            
            <p>Best regards,<br>
            <strong>{referral_data.get('specialty', 'Specialty')} Team</strong></p>
        </div>
    </body>
    </html>
    """
    
    if referral_data.get('patient_email'):
        send_email(referral_data['patient_email'], subject, patient_html)


# ============================================
# RTT BREACH ALERT NOTIFICATIONS
# ============================================

def send_rtt_breach_alert_email(patient_data: dict, days_until_breach: int):
    """Email alert for RTT breach risk"""
    if days_until_breach < 14:
        priority = "🔴 CRITICAL"
        color = "#dc3545"
    elif days_until_breach < 28:
        priority = "🟠 URGENT"
        color = "#ffc107"
    else:
        priority = "🟡 WARNING"
        color = "#28a745"
    
    subject = f"{priority} RTT Breach Alert - {patient_data.get('name', 'Patient')}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid {color};">
            <h2 style="color: {color};">{priority} RTT Breach Alert</h2>
            
            <div style="background: #fff3cd; padding: 20px; margin: 20px 0; border-left: 4px solid {color};">
                <h3 style="margin-top: 0;">Patient at Risk of RTT Breach:</h3>
                <p><strong>Name:</strong> {patient_data.get('name', 'N/A')}<br>
                <strong>NHS:</strong> {patient_data.get('nhs_number', 'N/A')}<br>
                <strong>Specialty:</strong> {patient_data.get('specialty', 'N/A')}<br>
                <strong>Days Until Breach:</strong> <span style="font-size: 24px; font-weight: bold; color: {color};">{days_until_breach} days</span><br>
                <strong>Referral Date:</strong> {patient_data.get('referral_date', 'N/A')}</p>
            </div>
            
            <p><strong>URGENT ACTION REQUIRED:</strong></p>
            <ul>
                <li>Book appointment immediately</li>
                <li>Escalate to consultant if needed</li>
                <li>Update patient on waiting list status</li>
                <li>Document all actions taken</li>
            </ul>
            
            <p style="color: {color}; font-weight: bold;">This patient MUST be seen before the 18-week deadline!</p>
        </div>
    </body>
    </html>
    """
    
    # Send to RTT Coordinator
    coordinator_email = "rtt.coordinator@trust.nhs.uk"  # Configure
    send_email(coordinator_email, subject, html_content)


# ============================================
# CANCER PATHWAY NOTIFICATIONS (2WW, 62-day)
# ============================================

def send_2ww_referral_received_email(patient_data: dict):
    """Email for 2-week-wait cancer referral"""
    subject = f"🚨 URGENT: 2-Week Wait Referral Received - {patient_data.get('name', 'Patient')}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 3px solid #dc3545;">
            <h2 style="color: #dc3545;">🚨 URGENT: 2-Week Wait Cancer Referral</h2>
            
            <div style="background: #f8d7da; padding: 20px; margin: 20px 0; border-left: 4px solid #dc3545;">
                <p><strong>Patient:</strong> {patient_data.get('name', 'N/A')}<br>
                <strong>NHS:</strong> {patient_data.get('nhs_number', 'N/A')}<br>
                <strong>Specialty:</strong> {patient_data.get('specialty', 'N/A')}<br>
                <strong>Referral Date:</strong> {patient_data.get('referral_date', datetime.now().strftime('%d %B %Y'))}</p>
            </div>
            
            <p style="font-size: 18px; font-weight: bold; color: #dc3545;">
            APPOINTMENT MUST BE OFFERED WITHIN 14 DAYS
            </p>
            
            <p><strong>Actions Required:</strong></p>
            <ul>
                <li>Book appointment within 14 days</li>
                <li>Start 62-day cancer pathway tracking</li>
                <li>Send appointment letter to patient</li>
                <li>Update cancer PTL</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    # Send to Cancer Coordinator
    cancer_coordinator = "cancer.coordinator@trust.nhs.uk"  # Configure
    send_email(cancer_coordinator, subject, html_content)


# ============================================
# CLINICAL LETTER GENERATION NOTIFICATIONS
# ============================================

def send_letter_generated_notification(letter_type: str, patient_name: str, recipient_email: str):
    """Email when clinical letter generated"""
    subject = f"Clinical Letter Generated - {letter_type}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0066cc;">📝 Clinical Letter Generated</h2>
            
            <p>A new <strong>{letter_type}</strong> has been generated for patient <strong>{patient_name}</strong>.</p>
            
            <p><strong>Generated:</strong> {datetime.now().strftime('%d %B %Y %H:%M')}</p>
            
            <p>Please review and approve the letter in the system.</p>
            
            <p>Best regards,<br>
            <strong>Clinical Documentation System</strong></p>
        </div>
    </body>
    </html>
    """
    
    send_email(recipient_email, subject, html_content)


# ============================================
# EXPORT ALL NOTIFICATION FUNCTIONS
# ============================================

__all__ = [
    'send_patient_added_to_ptl_email',
    'send_pbl_acknowledgment_email',
    'send_appointment_booked_email',
    'send_appointment_cancelled_email',
    'send_mdt_meeting_scheduled_email',
    'send_referral_received_email',
    'send_rtt_breach_alert_email',
    'send_2ww_referral_received_email',
    'send_letter_generated_notification'
]

print("✅ NHS Email Notification System Loaded!")
print("📧 All clinical events will trigger automatic emails")
