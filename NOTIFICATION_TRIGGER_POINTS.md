# 🎯 NOTIFICATION TRIGGER POINTS - WHEN & WHERE

**Complete guide to WHEN notifications fire and WHICH modules trigger them**

---

## 📊 **MODULE-BY-MODULE TRIGGER POINTS**

### **1️⃣ STUDENT ENROLLMENT / REGISTRATION**

#### **Module:** Student Registration / Sign Up
#### **File:** `student_auth.py` or similar

**Trigger Point:**
```python
# WHEN: Student completes registration
def register_student(email, name, tier):
    # Your existing code...
    save_student(student_data)
    
    # 🔔 TRIGGER NOTIFICATION HERE:
    from complete_notification_triggers import notify_student_enrolled
    notify_student_enrolled(email, name, "RTT Training", tier)
    # → Green pop-up + Welcome email + In-app
```

**What Happens:**
- ✅ Student gets GREEN pop-up: "🎉 Welcome to T21!"
- ✅ Student gets welcome email with login details
- ✅ In-app notification created
- ✅ Admin gets notification (in-app only)

---

### **2️⃣ LEARNING PORTAL / COURSE ENROLLMENT**

#### **Module:** Learning Portal
#### **Files:** `lms_*.py` or learning module files

**Trigger Point 1: Course Enrollment**
```python
# WHEN: Student enrolls in a course
def enroll_in_course(student_email, course_name):
    save_enrollment(enrollment_data)
    
    # 🔔 TRIGGER:
    from complete_notification_triggers import notify_student_enrolled
    notify_student_enrolled(student_email, student_name, course_name, tier)
    # → Email confirmation + In-app
```

**Trigger Point 2: Course Completion**
```python
# WHEN: Student completes all modules in course
def mark_course_complete(student_email, course_name):
    save_completion(completion_data)
    
    # 🔔 TRIGGER:
    from complete_notification_triggers import notify_student_course_completed
    notify_student_course_completed(student_email, student_name, course_name)
    # → Green pop-up + Celebration email + In-app
```

**Trigger Point 3: New Content Added**
```python
# WHEN: Admin adds new scenario/video/content
def add_new_content(content_type, content_name):
    save_content(content_data)
    
    # Get all enrolled students
    students = get_enrolled_students()
    
    # 🔔 TRIGGER for each student:
    for student in students:
        notify_student_new_content(student.email, content_type, content_name)
    # → Email + In-app to all students
```

---

### **3️⃣ ASSIGNMENTS / HOMEWORK**

#### **Module:** Teaching & Assessment
#### **Files:** `assignment_*.py` or teaching modules

**Trigger Point 1: Assignment Created**
```python
# WHEN: Teacher creates assignment with deadline
def create_assignment(assignment_data):
    save_assignment(assignment_data)
    
    # Schedule reminder notifications (run daily)
    # See section on "Daily Automated Checks"
```

**Trigger Point 2: Assignment Submitted**
```python
# WHEN: Student submits assignment
def submit_assignment(student_email, assignment_name, teacher_email):
    save_submission(submission_data)
    
    # 🔔 TRIGGER to teacher:
    from complete_notification_triggers import notify_teacher_assignment_submitted
    notify_teacher_assignment_submitted(teacher_email, student_name, assignment_name)
    # → Email to teacher + In-app
```

**Trigger Point 3: Assignment Graded**
```python
# WHEN: Teacher grades assignment
def grade_assignment(student_email, assignment_name, grade, feedback):
    save_grade(grade_data)
    
    # 🔔 TRIGGER to student:
    from complete_notification_triggers import notify_student_assignment_graded
    notify_student_assignment_graded(student_email, assignment_name, grade, feedback)
    # → Green pop-up + Email + In-app
```

---

### **4️⃣ CERTIFICATION / EXAMS**

#### **Module:** Training & Certification
#### **Files:** `certification_advanced.py`, exam modules

**Trigger Point 1: Exam Available**
```python
# WHEN: Exam becomes available to student
def make_exam_available(student_email, exam_name, deadline):
    update_exam_status(exam_data)
    
    # 🔔 TRIGGER:
    from complete_notification_triggers import notify_student_exam_available
    notify_student_exam_available(student_email, exam_name, deadline)
    # → Email + In-app
```

**Trigger Point 2: Exam Completed & Graded**
```python
# WHEN: Student finishes exam and results are calculated
def complete_exam(student_email, exam_name, score):
    save_exam_result(result_data)
    
    passed = score >= 70  # Your pass threshold
    
    # 🔔 TRIGGER:
    from complete_notification_triggers import notify_student_exam_result
    notify_student_exam_result(student_email, exam_name, score, passed)
    # → If passed: Green pop-up + Congratulations email
    # → If failed: Email with encouragement
```

**Trigger Point 3: Certificate Issued**
```python
# WHEN: Certificate is generated (after passing exam)
def issue_certificate(student_email, student_name, cert_type, level):
    generate_certificate(cert_data)
    
    # 🔔 TRIGGER:
    from complete_notification_triggers import notify_student_certificate_issued
    notify_student_certificate_issued(student_email, student_name, cert_type, level)
    # → Green pop-up "🏆 Certificate Ready!" + Email + In-app
```

---

### **5️⃣ MESSAGING SYSTEM**

#### **Module:** Messages
#### **Files:** `messaging_system.py`, `messaging_ui.py`

**Trigger Point 1: Message Sent**
```python
# WHEN: Message is sent (already built into messaging_system.py)
def send_message(from_email, to_email, subject, body):
    save_message(message_data)
    
    # 🔔 TRIGGER (already in messaging_system.py):
    notify_new_message(message)  # Calls notification system automatically
    # → Email + In-app + Badge
```

**Trigger Point 2: Teacher Replies**
```python
# WHEN: Teacher replies to student question
def reply_to_message(message_id, from_teacher_email, body):
    save_reply(reply_data)
    
    # 🔔 TRIGGER:
    from complete_notification_triggers import notify_student_teacher_replied
    notify_student_teacher_replied(student_email, teacher_name, original_subject)
    # → Email + In-app
```

---

### **6️⃣ APPROVAL SYSTEM**

#### **Module:** Approvals
#### **Files:** `approval_system.py`, `approval_ui.py`

**Trigger Point 1: Request Submitted**
```python
# WHEN: Student submits tier upgrade request (already built-in)
def submit_tier_upgrade_request(requester_email, current_tier, requested_tier):
    save_request(request_data)
    
    # 🔔 TRIGGER (already in approval_system.py):
    notify_approvers_new_request(request)  # Calls notification system
    # → Admin gets pop-up + Email + In-app
    # → Student gets confirmation email + In-app
```

**Trigger Point 2: Request Approved**
```python
# WHEN: Admin approves request (already built-in)
def approve_request(request_id, approver_email):
    update_request_status(request_id, 'approved')
    
    # 🔔 TRIGGER (already in approval_system.py):
    notify_requester_approved(request)
    # → Student gets GREEN pop-up "🎉 Approved!" + Email + In-app
```

**Trigger Point 3: Request Rejected**
```python
# WHEN: Admin rejects request (already built-in)
def reject_request(request_id, reason):
    update_request_status(request_id, 'rejected')
    
    # 🔔 TRIGGER (already in approval_system.py):
    notify_requester_rejected(request)
    # → Student gets email with reason + In-app
```

---

### **7️⃣ PAYMENT PROCESSING**

#### **Module:** Payment System
#### **Files:** Payment processing modules

**Trigger Point: Payment Received**
```python
# WHEN: Payment is successfully processed
def process_payment(student_email, amount, tier):
    save_payment(payment_data)
    upgrade_tier(student_email, tier)
    
    # 🔔 TRIGGER to student:
    from complete_notification_triggers import notify_student_payment_received
    notify_student_payment_received(student_email, amount, tier)
    # → Green pop-up + Receipt email + In-app
    
    # 🔔 TRIGGER to admin:
    from complete_notification_triggers import notify_admin_payment_received
    notify_admin_payment_received(admin_email, student_name, amount, tier)
    # → Email + In-app
```

---

### **8️⃣ TRIAL EXPIRATION**

#### **Module:** Trial Management
#### **Files:** `trial_expiry_automation.py` or user management

**Trigger Point: Daily Check (Automated)**
```python
# WHEN: Daily cron job runs (see "Daily Automated Checks" section)
def check_trial_expirations():
    expiring_trials = get_expiring_trials()
    
    for trial in expiring_trials:
        hours_remaining = calculate_hours(trial.expiry_date)
        
        # Send notifications at 7 days, 3 days, 1 day
        if hours_remaining in [168, 72, 24]:  # 7, 3, 1 days
            # 🔔 TRIGGER:
            from complete_notification_triggers import notify_student_trial_expiring
            notify_student_trial_expiring(trial.email, hours_remaining)
            # → If 24h: RED pop-up + Urgent email
            # → If 7d: Email reminder
```

---

### **9️⃣ PTL (Patient Tracking List)**

#### **Module:** PTL Management
#### **Files:** `ptl_system.py`, `ptl_ui.py`

**Trigger Point 1: Patient Added**
```python
# WHEN: Patient added to PTL
def add_patient_to_ptl(patient_data, staff_email):
    save_patient(patient_data)
    
    # 🔔 TRIGGER to staff:
    from complete_notification_triggers import notify_nhs_patient_added_ptl
    notify_nhs_patient_added_ptl(staff_email, patient_data['name'], 
                                  patient_data['specialty'], patient_data['priority'])
    # → Email + In-app
```

**Trigger Point 2: RTT Breach Alert (Automated Daily)**
```python
# WHEN: Daily check detects breach risk
def check_rtt_breaches():
    at_risk_patients = get_breach_risks()
    
    for patient in at_risk_patients:
        days_remaining = calculate_days_to_breach(patient)
        
        if days_remaining < 28:
            # 🔔 TRIGGER:
            from complete_notification_triggers import notify_nhs_rtt_breach_alert
            notify_nhs_rtt_breach_alert(coordinator_email, patient['name'], days_remaining)
            # → If <14 days: RED pop-up + Urgent email
            # → If 14-28 days: Email warning
```

---

### **🔟 PBL (Partial Booking List)**

#### **Module:** Partial Booking List
#### **Files:** `partial_booking_list_system.py`, `partial_booking_list_ui.py`

**Trigger Point: Patient Added to PBL**
```python
# WHEN: Patient added to PBL (already built-in!)
def add_to_pbl(patient_data):
    save_to_pbl(patient_data)
    
    # 🔔 TRIGGER (already in partial_booking_list_system.py):
    send_pbl_acknowledgment_email(patient_data)
    # → Email to patient + Email to coordinator + In-app
```

---

### **1️⃣1️⃣ ADVANCED BOOKING**

#### **Module:** Advanced Booking System
#### **Files:** `advanced_booking_system.py`, `advanced_booking_ui.py`

**Trigger Point 1: Appointment Booked**
```python
# WHEN: Appointment is booked
def book_appointment(appointment_data, patient_email):
    save_appointment(appointment_data)
    
    # 🔔 TRIGGER to patient:
    from complete_notification_triggers import notify_nhs_appointment_booked
    notify_nhs_appointment_booked(patient_email, appt_date, appt_time, clinic)
    # → Email confirmation + In-app
```

**Trigger Point 2: Appointment Cancelled**
```python
# WHEN: Appointment is cancelled
def cancel_appointment(appointment_data, patient_email):
    update_appointment_status('cancelled')
    
    # 🔔 TRIGGER:
    from nhs_email_notifications import send_appointment_cancelled_email
    send_appointment_cancelled_email(appointment_data)
    # → Email + In-app
```

---

### **1️⃣2️⃣ CANCER PATHWAYS**

#### **Module:** Cancer Pathways
#### **Files:** `cancer_pathway_system.py`, `cancer_pathway_ui.py`

**Trigger Point: 2WW Referral Received**
```python
# WHEN: 2-Week-Wait referral received
def add_2ww_referral(patient_data, coordinator_email):
    save_2ww_referral(patient_data)
    
    # 🔔 TRIGGER:
    from complete_notification_triggers import notify_nhs_2ww_referral
    notify_nhs_2ww_referral(coordinator_email, patient_data['name'], 
                            patient_data['specialty'])
    # → RED pop-up "🚨 2WW REFERRAL!" + Urgent email + In-app
```

---

### **1️⃣3️⃣ MDT COORDINATION**

#### **Module:** MDT Coordination
#### **Files:** `mdt_coordination_system.py`, `mdt_coordination_ui.py`

**Trigger Point: MDT Meeting Scheduled**
```python
# WHEN: MDT meeting is scheduled
def schedule_mdt_meeting(meeting_data, attendees):
    save_mdt_meeting(meeting_data)
    
    # 🔔 TRIGGER to all attendees:
    for attendee_email in attendees:
        from complete_notification_triggers import notify_nhs_mdt_meeting_scheduled
        notify_nhs_mdt_meeting_scheduled(attendee_email, meeting_data['date'],
                                         meeting_data['specialty'], patient_count)
        # → Email calendar invite + In-app
```

---

### **1️⃣4️⃣ SUPPORT TICKETS**

#### **Module:** Support System
#### **Files:** Support ticket modules

**Trigger Point: Support Ticket Created**
```python
# WHEN: User creates support ticket
def create_support_ticket(user_email, subject, description, priority):
    save_ticket(ticket_data)
    
    # 🔔 TRIGGER to admin:
    from complete_notification_triggers import notify_admin_support_ticket
    notify_admin_support_ticket(admin_email, user_name, subject, priority)
    # → If urgent: ORANGE pop-up + Email
    # → If normal: Email + In-app
```

---

## ⏰ **DAILY AUTOMATED CHECKS**

Create a file: `daily_notification_checks.py`

```python
"""
Run this daily (via cron job or scheduler)
Checks for events that need notifications
"""

from complete_notification_triggers import (
    notify_student_assignment_due,
    notify_student_trial_expiring,
    notify_nhs_rtt_breach_alert,
    notify_teacher_student_struggling
)

def run_daily_checks():
    """Run daily at midnight or 6am"""
    
    # 1. CHECK ASSIGNMENTS DUE SOON
    assignments = get_upcoming_assignments()
    for assignment in assignments:
        hours_until_due = calculate_hours(assignment['due_date'])
        
        # Notify at 7 days, 3 days, 1 day
        if hours_until_due <= 168:  # 7 days
            notify_student_assignment_due(
                student_email=assignment['student_email'],
                assignment_name=assignment['name'],
                due_date=assignment['due_date'],
                hours_remaining=hours_until_due
            )
    
    # 2. CHECK TRIAL EXPIRATIONS
    trials = get_expiring_trials()
    for trial in trials:
        hours_remaining = calculate_hours(trial['expiry_date'])
        
        # Notify at 7, 3, 1 days
        if hours_remaining in [168, 72, 24]:
            notify_student_trial_expiring(trial['email'], hours_remaining)
    
    # 3. CHECK RTT BREACHES
    patients = get_ptl_patients()
    for patient in patients:
        days_remaining = calculate_days_to_breach(patient)
        
        # Alert if < 28 days
        if days_remaining < 28:
            notify_nhs_rtt_breach_alert(
                staff_email=get_coordinator_email(),
                patient_name=patient['name'],
                days_remaining=days_remaining
            )
    
    # 4. CHECK STRUGGLING STUDENTS
    students = get_all_students()
    for student in students:
        recent_scores = get_recent_scores(student.email)
        avg_score = calculate_average(recent_scores)
        
        # Alert teacher if student averaging <60%
        if avg_score < 60:
            notify_teacher_student_struggling(
                teacher_email=student.teacher_email,
                student_name=student.name,
                course_name=student.current_course,
                score=avg_score
            )

# Schedule this to run daily
if __name__ == "__main__":
    run_daily_checks()
```

---

## 📊 **SUMMARY TABLE: WHERE TO ADD NOTIFICATIONS**

| Module | File | Event | Function to Call |
|--------|------|-------|------------------|
| **Student Registration** | `student_auth.py` | Student signs up | `notify_student_enrolled()` |
| **Course Enrollment** | `lms_*.py` | Enrolls in course | `notify_student_enrolled()` |
| **Course Completion** | `lms_*.py` | Completes course | `notify_student_course_completed()` |
| **Assignments** | Assignment modules | Assignment graded | `notify_student_assignment_graded()` |
| **Exams** | `certification_*.py` | Exam result | `notify_student_exam_result()` |
| **Certificates** | Certificate modules | Cert issued | `notify_student_certificate_issued()` |
| **Messages** | `messaging_system.py` | Message sent | Already built-in! |
| **Approvals** | `approval_system.py` | Request approved/rejected | Already built-in! |
| **Payments** | Payment modules | Payment received | `notify_student_payment_received()` |
| **PTL** | `ptl_system.py` | Patient added | `notify_nhs_patient_added_ptl()` |
| **PBL** | `partial_booking_list_system.py` | Patient added | Already built-in! |
| **Booking** | `advanced_booking_system.py` | Appointment booked | `notify_nhs_appointment_booked()` |
| **Cancer** | `cancer_pathway_system.py` | 2WW referral | `notify_nhs_2ww_referral()` |
| **MDT** | `mdt_coordination_system.py` | Meeting scheduled | `notify_nhs_mdt_meeting_scheduled()` |
| **Daily Checks** | `daily_notification_checks.py` | Run daily | Multiple checks |

---

## ✅ **WHAT'S ALREADY BUILT-IN**

These modules ALREADY send notifications (no action needed):

- ✅ **Messaging System** - Automatically notifies on new messages
- ✅ **Approval System** - Automatically notifies on requests/approvals
- ✅ **PBL System** - Automatically sends acknowledgment emails

---

## 🎯 **QUICK START INTEGRATION**

### **Step 1: Add to ONE module** (test it)

Pick the most important module (e.g., Student Enrollment):

```python
# In your student enrollment file
from complete_notification_triggers import notify_student_enrolled

# Find where student is saved
def enroll_student(email, name, course, tier):
    save_student(data)
    
    # ADD THIS LINE:
    notify_student_enrolled(email, name, course, tier)
```

### **Step 2: Test it**
- Create a test student
- Check if they get green pop-up
- Check if email arrives
- Check if in-app notification shows

### **Step 3: Roll out to other modules**
- Once tested, add to all other modules
- Follow the table above
- 10 minutes per module

---

**Your notifications will now fire automatically at the EXACT right moment in each module!** 🎉

---

*Notification Trigger Points Guide*  
*Created: 16 October 2025*  
*Coverage: All 14 major modules*  
*Status: Ready to integrate*
