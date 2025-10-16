"""
COMPLETE NOTIFICATION TRIGGERS - ALL USER TYPES
Automatic notifications for EVERYONE: Students, Learners, Staff, NHS, Teachers, Admins

EVERY action triggers appropriate notifications automatically!
"""

from notification_system import create_notification, NotificationType, NotificationPriority
from email_service import send_email


# ============================================
# STUDENT / LEARNER NOTIFICATIONS
# ============================================

def notify_student_enrolled(student_email: str, student_name: str, course_name: str, tier: str):
    """Student enrolled in course"""
    # Welcome notification
    create_notification(
        user_email=student_email,
        title="🎉 Welcome to T21 RTT Training!",
        message=f"You're enrolled in {course_name} ({tier}). Let's get started!",
        notification_type=NotificationType.SUCCESS,
        priority=NotificationPriority.HIGH,
        send_email=True,
        action_url="/learning-portal",
        action_label="Start Learning"
    )


def notify_student_assignment_due(student_email: str, assignment_name: str, due_date: str, hours_remaining: int):
    """Assignment due soon"""
    if hours_remaining <= 24:
        priority = NotificationPriority.URGENT  # Pop-up!
        title = "🚨 Assignment Due Tomorrow!"
    elif hours_remaining <= 72:
        priority = NotificationPriority.HIGH
        title = "⚠️ Assignment Due Soon!"
    else:
        priority = NotificationPriority.MEDIUM
        title = "📝 Assignment Reminder"
    
    create_notification(
        user_email=student_email,
        title=title,
        message=f"{assignment_name} is due on {due_date}",
        notification_type=NotificationType.WARNING if hours_remaining <= 24 else NotificationType.INFO,
        priority=priority,
        send_email=True,
        action_url="/assignments"
    )


def notify_student_assignment_graded(student_email: str, assignment_name: str, grade: str, feedback: str):
    """Assignment has been graded"""
    create_notification(
        user_email=student_email,
        title="✅ Assignment Graded!",
        message=f"{assignment_name} - Grade: {grade}",
        notification_type=NotificationType.SUCCESS,
        priority=NotificationPriority.HIGH,  # Pop-up for good news!
        send_email=True,
        action_url="/assignments",
        metadata={'feedback': feedback}
    )


def notify_student_course_completed(student_email: str, student_name: str, course_name: str):
    """Student completed a course"""
    create_notification(
        user_email=student_email,
        title="🎓 Course Completed!",
        message=f"Congratulations! You completed {course_name}",
        notification_type=NotificationType.SUCCESS,
        priority=NotificationPriority.HIGH,  # Pop-up celebration!
        send_email=True,
        action_url="/certificates"
    )


def notify_student_certificate_issued(student_email: str, student_name: str, certificate_type: str, level: str):
    """Certificate issued to student"""
    create_notification(
        user_email=student_email,
        title="🏆 Certificate Issued!",
        message=f"Your {certificate_type} - {level} certificate is ready!",
        notification_type=NotificationType.SUCCESS,
        priority=NotificationPriority.URGENT,  # Pop-up celebration!
        send_email=True,
        action_url="/certificates",
        action_label="Download Certificate"
    )


def notify_student_exam_available(student_email: str, exam_name: str, deadline: str):
    """Exam is now available"""
    create_notification(
        user_email=student_email,
        title="📝 Exam Available!",
        message=f"{exam_name} is now available. Deadline: {deadline}",
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.HIGH,
        send_email=True,
        action_url="/exams",
        action_label="Take Exam"
    )


def notify_student_exam_result(student_email: str, exam_name: str, score: int, passed: bool):
    """Exam result available"""
    if passed:
        title = "🎉 Exam Passed!"
        msg = f"Congratulations! You scored {score}% on {exam_name}"
        notif_type = NotificationType.SUCCESS
        priority = NotificationPriority.HIGH  # Pop-up for success!
    else:
        title = "📊 Exam Results"
        msg = f"You scored {score}% on {exam_name}. You can retake it!"
        notif_type = NotificationType.INFO
        priority = NotificationPriority.MEDIUM
    
    create_notification(
        user_email=student_email,
        title=title,
        message=msg,
        notification_type=notif_type,
        priority=priority,
        send_email=True,
        action_url="/exams"
    )


def notify_student_teacher_replied(student_email: str, teacher_name: str, subject: str):
    """Teacher replied to student's question"""
    create_notification(
        user_email=student_email,
        title="💬 Teacher Replied!",
        message=f"{teacher_name} replied to: {subject}",
        notification_type=NotificationType.MESSAGE,
        priority=NotificationPriority.MEDIUM,
        send_email=True,
        action_url="/messages",
        action_label="Read Reply"
    )


def notify_student_trial_expiring(student_email: str, hours_remaining: int):
    """Trial expiring soon"""
    if hours_remaining <= 24:
        priority = NotificationPriority.URGENT  # Red pop-up!
        title = "🚨 Trial Expires Tomorrow!"
    elif hours_remaining <= 168:  # 7 days
        priority = NotificationPriority.HIGH
        title = "⏰ Trial Expiring Soon!"
    else:
        priority = NotificationPriority.MEDIUM
        title = "⏰ Trial Reminder"
    
    create_notification(
        user_email=student_email,
        title=title,
        message=f"Your trial expires in {hours_remaining} hours. Upgrade to keep learning!",
        notification_type=NotificationType.WARNING,
        priority=priority,
        send_email=True,
        action_url="/upgrade",
        action_label="Upgrade Now"
    )


def notify_student_payment_received(student_email: str, amount: str, tier: str):
    """Payment received and processed"""
    create_notification(
        user_email=student_email,
        title="✅ Payment Received!",
        message=f"Your payment of {amount} for {tier} has been processed. Thank you!",
        notification_type=NotificationType.SUCCESS,
        priority=NotificationPriority.HIGH,  # Pop-up confirmation!
        send_email=True,
        action_url="/my-account"
    )


def notify_student_new_content(student_email: str, content_type: str, content_name: str):
    """New content available (scenarios, videos, etc.)"""
    create_notification(
        user_email=student_email,
        title="🆕 New Content Available!",
        message=f"New {content_type}: {content_name} has been added!",
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.MEDIUM,
        send_email=True,
        action_url="/learning-portal",
        action_label="View Content"
    )


# ============================================
# TEACHER / INSTRUCTOR NOTIFICATIONS
# ============================================

def notify_teacher_student_question(teacher_email: str, student_name: str, subject: str):
    """Student sent a question"""
    create_notification(
        user_email=teacher_email,
        title="💬 Student Question",
        message=f"{student_name} asked: {subject}",
        notification_type=NotificationType.MESSAGE,
        priority=NotificationPriority.MEDIUM,
        send_email=True,
        action_url="/messages",
        action_label="Reply"
    )


def notify_teacher_assignment_submitted(teacher_email: str, student_name: str, assignment_name: str):
    """Student submitted assignment"""
    create_notification(
        user_email=teacher_email,
        title="📝 Assignment Submitted",
        message=f"{student_name} submitted {assignment_name}",
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.MEDIUM,
        send_email=True,
        action_url="/grading",
        action_label="Grade Assignment"
    )


def notify_teacher_new_student_enrolled(teacher_email: str, student_name: str, course_name: str):
    """New student enrolled in teacher's course"""
    create_notification(
        user_email=teacher_email,
        title="🎓 New Student Enrolled",
        message=f"{student_name} enrolled in {course_name}",
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.LOW,
        send_email=True,
        action_url="/students"
    )


def notify_teacher_student_struggling(teacher_email: str, student_name: str, course_name: str, score: int):
    """Student struggling (low scores)"""
    create_notification(
        user_email=teacher_email,
        title="⚠️ Student Needs Help",
        message=f"{student_name} is struggling in {course_name} (score: {score}%)",
        notification_type=NotificationType.WARNING,
        priority=NotificationPriority.HIGH,
        send_email=True,
        action_url="/students",
        action_label="Contact Student"
    )


# ============================================
# ADMIN NOTIFICATIONS
# ============================================

def notify_admin_new_registration(admin_email: str, user_name: str, user_email: str, tier: str):
    """New user registered"""
    create_notification(
        user_email=admin_email,
        title="👤 New Registration",
        message=f"{user_name} ({user_email}) registered for {tier}",
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.LOW,
        send_email=False,  # Too frequent
        action_url="/admin/users"
    )


def notify_admin_payment_received(admin_email: str, user_name: str, amount: str, tier: str):
    """Payment received"""
    create_notification(
        user_email=admin_email,
        title="💰 Payment Received",
        message=f"{user_name} paid {amount} for {tier}",
        notification_type=NotificationType.SUCCESS,
        priority=NotificationPriority.MEDIUM,
        send_email=True,
        action_url="/admin/payments"
    )


def notify_admin_support_ticket(admin_email: str, user_name: str, subject: str, priority: str):
    """New support ticket"""
    if priority == "urgent":
        notif_priority = NotificationPriority.URGENT  # Pop-up!
    elif priority == "high":
        notif_priority = NotificationPriority.HIGH
    else:
        notif_priority = NotificationPriority.MEDIUM
    
    create_notification(
        user_email=admin_email,
        title=f"🎫 Support Ticket ({priority.upper()})",
        message=f"{user_name}: {subject}",
        notification_type=NotificationType.APPROVAL,
        priority=notif_priority,
        send_email=True,
        action_url="/admin/support",
        action_label="View Ticket"
    )


def notify_admin_system_error(admin_email: str, error_type: str, error_message: str):
    """System error occurred"""
    create_notification(
        user_email=admin_email,
        title="🚨 System Error",
        message=f"{error_type}: {error_message}",
        notification_type=NotificationType.URGENT,
        priority=NotificationPriority.URGENT,  # Red pop-up!
        send_email=True,
        action_url="/admin/logs"
    )


# ============================================
# NHS STAFF NOTIFICATIONS (All from previous NHS email system)
# ============================================

def notify_nhs_patient_added_ptl(staff_email: str, patient_name: str, specialty: str, priority: str):
    """Patient added to PTL"""
    from nhs_email_notifications import send_patient_added_to_ptl_email
    
    # Also create in-app notification
    create_notification(
        user_email=staff_email,
        title="📋 Patient Added to PTL",
        message=f"{patient_name} - {specialty} ({priority})",
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.MEDIUM,
        send_email=False,  # Email handled by NHS system
        action_url="/ptl"
    )


def notify_nhs_rtt_breach_alert(staff_email: str, patient_name: str, days_remaining: int):
    """RTT breach alert"""
    if days_remaining < 14:
        priority = NotificationPriority.URGENT  # Red pop-up!
        title = "🚨 CRITICAL RTT BREACH!"
    elif days_remaining < 28:
        priority = NotificationPriority.HIGH
        title = "⚠️ RTT Breach Risk"
    else:
        priority = NotificationPriority.MEDIUM
        title = "📊 RTT Monitoring"
    
    create_notification(
        user_email=staff_email,
        title=title,
        message=f"{patient_name} - {days_remaining} days until breach",
        notification_type=NotificationType.URGENT if days_remaining < 14 else NotificationType.WARNING,
        priority=priority,
        send_email=True,
        action_url="/ptl",
        action_label="View Patient"
    )


def notify_nhs_appointment_booked(patient_email: str, appointment_date: str, appointment_time: str, clinic: str):
    """Appointment booked (to patient)"""
    from nhs_email_notifications import send_appointment_booked_email
    
    create_notification(
        user_email=patient_email,
        title="✅ Appointment Confirmed",
        message=f"Your appointment: {appointment_date} at {appointment_time} - {clinic}",
        notification_type=NotificationType.SUCCESS,
        priority=NotificationPriority.MEDIUM,
        send_email=False,  # Email handled by NHS system
        action_url="/my-appointments"
    )


def notify_nhs_2ww_referral(coordinator_email: str, patient_name: str, specialty: str):
    """2 Week Wait cancer referral"""
    create_notification(
        user_email=coordinator_email,
        title="🚨 2WW CANCER REFERRAL!",
        message=f"{patient_name} - {specialty}. Must book within 14 days!",
        notification_type=NotificationType.URGENT,
        priority=NotificationPriority.URGENT,  # Red pop-up!
        send_email=True,
        action_url="/cancer-pathways",
        action_label="Book Appointment"
    )


def notify_nhs_mdt_meeting_scheduled(attendee_email: str, meeting_date: str, specialty: str, patient_count: int):
    """MDT meeting scheduled"""
    create_notification(
        user_email=attendee_email,
        title="📅 MDT Meeting Scheduled",
        message=f"{specialty} MDT on {meeting_date} - {patient_count} patients",
        notification_type=NotificationType.INFO,
        priority=NotificationPriority.MEDIUM,
        send_email=True,
        action_url="/mdt",
        action_label="View Details"
    )


# ============================================
# AUTOMATED TRIGGERS (Call these from your modules)
# ============================================

# Export all notification functions
__all__ = [
    # Student
    'notify_student_enrolled',
    'notify_student_assignment_due',
    'notify_student_assignment_graded',
    'notify_student_course_completed',
    'notify_student_certificate_issued',
    'notify_student_exam_available',
    'notify_student_exam_result',
    'notify_student_teacher_replied',
    'notify_student_trial_expiring',
    'notify_student_payment_received',
    'notify_student_new_content',
    
    # Teacher
    'notify_teacher_student_question',
    'notify_teacher_assignment_submitted',
    'notify_teacher_new_student_enrolled',
    'notify_teacher_student_struggling',
    
    # Admin
    'notify_admin_new_registration',
    'notify_admin_payment_received',
    'notify_admin_support_ticket',
    'notify_admin_system_error',
    
    # NHS
    'notify_nhs_patient_added_ptl',
    'notify_nhs_rtt_breach_alert',
    'notify_nhs_appointment_booked',
    'notify_nhs_2ww_referral',
    'notify_nhs_mdt_meeting_scheduled'
]

print("✅ Complete notification triggers loaded for ALL user types!")
print("📧 Students, Learners, Teachers, NHS Staff, Admins - EVERYONE covered!")
