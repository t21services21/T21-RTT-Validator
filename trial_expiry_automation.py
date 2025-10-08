"""
T21 SERVICES - TRIAL EXPIRY AUTOMATION
Automatically send warning emails to users whose trials are expiring

Features:
- Check all trial users
- Send 24-hour warning
- Send 1-hour warning
- Send expired notification
- Track email history to avoid duplicates
"""

import json
import os
from datetime import datetime
from student_auth import list_all_students
from email_service import send_trial_expiry_warning, send_trial_expired_email


EMAIL_HISTORY_FILE = "trial_email_history.json"


def load_email_history():
    """Load email history to avoid sending duplicates"""
    if os.path.exists(EMAIL_HISTORY_FILE):
        try:
            with open(EMAIL_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_email_history(history):
    """Save email history"""
    with open(EMAIL_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def check_and_send_expiry_warnings():
    """
    Check all trial users and send appropriate warning emails
    Returns: dict with statistics
    """
    stats = {
        "checked": 0,
        "24hr_warnings": 0,
        "1hr_warnings": 0,
        "expired_notices": 0,
        "errors": 0
    }
    
    try:
        # Get all students
        all_students = list_all_students()
        email_history = load_email_history()
        
        for student in all_students:
            stats["checked"] += 1
            
            # Only process trial users
            if student['role'] != 'trial':
                continue
            
            email = student['email']
            full_name = student['full_name']
            days_remaining = student['days_remaining']
            
            # Initialize history for this user if not exists
            if email not in email_history:
                email_history[email] = {
                    "24hr_sent": False,
                    "1hr_sent": False,
                    "expired_sent": False
                }
            
            user_history = email_history[email]
            hours_remaining = days_remaining * 24
            
            # Check if trial expired
            if hours_remaining <= 0 and not user_history["expired_sent"]:
                try:
                    if send_trial_expired_email(email, full_name):
                        user_history["expired_sent"] = True
                        stats["expired_notices"] += 1
                        print(f"✅ Sent expired notice to {email}")
                except Exception as e:
                    stats["errors"] += 1
                    print(f"❌ Error sending expired notice to {email}: {e}")
            
            # Check if 1 hour or less remaining
            elif 0 < hours_remaining <= 1 and not user_history["1hr_sent"]:
                try:
                    if send_trial_expiry_warning(email, full_name, 1):
                        user_history["1hr_sent"] = True
                        stats["1hr_warnings"] += 1
                        print(f"✅ Sent 1hr warning to {email}")
                except Exception as e:
                    stats["errors"] += 1
                    print(f"❌ Error sending 1hr warning to {email}: {e}")
            
            # Check if 24 hours or less remaining
            elif 1 < hours_remaining <= 24 and not user_history["24hr_sent"]:
                try:
                    if send_trial_expiry_warning(email, full_name, 24):
                        user_history["24hr_sent"] = True
                        stats["24hr_warnings"] += 1
                        print(f"✅ Sent 24hr warning to {email}")
                except Exception as e:
                    stats["errors"] += 1
                    print(f"❌ Error sending 24hr warning to {email}: {e}")
        
        # Save updated history
        save_email_history(email_history)
        
    except Exception as e:
        print(f"❌ Fatal error in check_and_send_expiry_warnings: {e}")
        stats["errors"] += 1
    
    return stats


def get_trial_users_status():
    """Get status of all trial users for admin dashboard"""
    trial_users = []
    
    try:
        all_students = list_all_students()
        email_history = load_email_history()
        
        for student in all_students:
            if student['role'] == 'trial':
                email = student['email']
                hours_remaining = student['days_remaining'] * 24
                
                user_history = email_history.get(email, {
                    "24hr_sent": False,
                    "1hr_sent": False,
                    "expired_sent": False
                })
                
                trial_users.append({
                    "email": email,
                    "full_name": student['full_name'],
                    "hours_remaining": hours_remaining,
                    "status": student['status'],
                    "24hr_sent": user_history.get("24hr_sent", False),
                    "1hr_sent": user_history.get("1hr_sent", False),
                    "expired_sent": user_history.get("expired_sent", False)
                })
    
    except Exception as e:
        print(f"Error getting trial users status: {e}")
    
    return trial_users


def reset_email_history_for_user(email):
    """Reset email history for a specific user (useful for testing)"""
    history = load_email_history()
    if email in history:
        del history[email]
        save_email_history(history)
        return True
    return False
