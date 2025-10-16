"""
COMPREHENSIVE NOTIFICATION SYSTEM
In-app notifications, pop-ups, badges, and alerts

FEATURES:
- Real-time notifications (pop-ups)
- Notification badges (unread counts)
- Notification center (view all)
- Email + in-app dual delivery
- Priority levels (info, warning, urgent)
- User preferences (email on/off)
- Auto-clear old notifications

TYPES:
- System alerts
- Tier upgrade requests
- Message notifications
- Approval requests
- Staff additions
- Password resets
- And much more!
"""

from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional

# Notification types
class NotificationType:
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    URGENT = "urgent"
    MESSAGE = "message"
    APPROVAL = "approval"
    SYSTEM = "system"

# Notification priority
class NotificationPriority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Notification:
    """Single notification object"""
    
    def __init__(self, notification_data: dict):
        self.id = notification_data.get('id', self._generate_id())
        self.user_email = notification_data.get('user_email')
        self.type = notification_data.get('type', NotificationType.INFO)
        self.priority = notification_data.get('priority', NotificationPriority.MEDIUM)
        self.title = notification_data.get('title')
        self.message = notification_data.get('message')
        self.action_url = notification_data.get('action_url')
        self.action_label = notification_data.get('action_label', 'View')
        self.created_at = notification_data.get('created_at', datetime.now().isoformat())
        self.read = notification_data.get('read', False)
        self.email_sent = notification_data.get('email_sent', False)
        self.metadata = notification_data.get('metadata', {})
    
    def _generate_id(self):
        """Generate unique notification ID"""
        import uuid
        return f"notif_{uuid.uuid4().hex[:12]}"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_email': self.user_email,
            'type': self.type,
            'priority': self.priority,
            'title': self.title,
            'message': self.message,
            'action_url': self.action_url,
            'action_label': self.action_label,
            'created_at': self.created_at,
            'read': self.read,
            'email_sent': self.email_sent,
            'metadata': self.metadata
        }


# ============================================
# NOTIFICATION CREATION FUNCTIONS
# ============================================

def create_notification(user_email: str, title: str, message: str, 
                       notification_type: str = NotificationType.INFO,
                       priority: int = NotificationPriority.MEDIUM,
                       action_url: str = None,
                       action_label: str = "View",
                       send_email: bool = True,
                       metadata: dict = None) -> Notification:
    """
    Create a new notification
    
    Args:
        user_email: Recipient email
        title: Notification title
        message: Notification message
        notification_type: Type (info, success, warning, urgent, message, approval)
        priority: Priority level (1-4)
        action_url: Optional URL for action button
        action_label: Label for action button
        send_email: Whether to also send email
        metadata: Additional data
    
    Returns:
        Notification object
    """
    notif_data = {
        'user_email': user_email,
        'title': title,
        'message': message,
        'type': notification_type,
        'priority': priority,
        'action_url': action_url,
        'action_label': action_label,
        'metadata': metadata or {}
    }
    
    notification = Notification(notif_data)
    
    # Save notification
    save_notification(notification)
    
    # Send email if requested and user preferences allow
    if send_email and should_send_email(user_email, notification_type):
        send_notification_email(notification)
        notification.email_sent = True
        save_notification(notification)
    
    return notification


def save_notification(notification: Notification):
    """Save notification to database"""
    try:
        # Load existing notifications
        notifications = load_all_notifications()
        
        # Add or update
        existing_index = None
        for i, notif in enumerate(notifications):
            if notif['id'] == notification.id:
                existing_index = i
                break
        
        if existing_index is not None:
            notifications[existing_index] = notification.to_dict()
        else:
            notifications.append(notification.to_dict())
        
        # Save to file
        os.makedirs('data/notifications', exist_ok=True)
        with open('data/notifications/all_notifications.json', 'w') as f:
            json.dump(notifications, f, indent=2)
    
    except Exception as e:
        print(f"Error saving notification: {e}")


def load_all_notifications() -> List[dict]:
    """Load all notifications"""
    try:
        with open('data/notifications/all_notifications.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []


def get_user_notifications(user_email: str, unread_only: bool = False) -> List[Notification]:
    """Get notifications for a specific user"""
    all_notifs = load_all_notifications()
    
    user_notifs = [
        Notification(n) for n in all_notifs 
        if n['user_email'] == user_email
    ]
    
    if unread_only:
        user_notifs = [n for n in user_notifs if not n.read]
    
    # Sort by priority (urgent first) then date (newest first)
    user_notifs.sort(key=lambda x: (-x.priority, x.created_at), reverse=True)
    
    return user_notifs


def get_unread_count(user_email: str) -> int:
    """Get count of unread notifications"""
    unread = get_user_notifications(user_email, unread_only=True)
    return len(unread)


def mark_as_read(notification_id: str):
    """Mark notification as read"""
    all_notifs = load_all_notifications()
    
    for notif in all_notifs:
        if notif['id'] == notification_id:
            notif['read'] = True
            break
    
    # Save
    os.makedirs('data/notifications', exist_ok=True)
    with open('data/notifications/all_notifications.json', 'w') as f:
        json.dump(all_notifs, f, indent=2)


def mark_all_as_read(user_email: str):
    """Mark all user's notifications as read"""
    all_notifs = load_all_notifications()
    
    for notif in all_notifs:
        if notif['user_email'] == user_email:
            notif['read'] = True
    
    # Save
    os.makedirs('data/notifications', exist_ok=True)
    with open('data/notifications/all_notifications.json', 'w') as f:
        json.dump(all_notifs, f, indent=2)


def delete_notification(notification_id: str):
    """Delete a notification"""
    all_notifs = load_all_notifications()
    
    all_notifs = [n for n in all_notifs if n['id'] != notification_id]
    
    # Save
    os.makedirs('data/notifications', exist_ok=True)
    with open('data/notifications/all_notifications.json', 'w') as f:
        json.dump(all_notifs, f, indent=2)


def cleanup_old_notifications(days: int = 30):
    """Delete notifications older than X days"""
    all_notifs = load_all_notifications()
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    cleaned_notifs = [
        n for n in all_notifs
        if datetime.fromisoformat(n['created_at']) > cutoff_date
    ]
    
    # Save
    os.makedirs('data/notifications', exist_ok=True)
    with open('data/notifications/all_notifications.json', 'w') as f:
        json.dump(cleaned_notifs, f, indent=2)
    
    return len(all_notifs) - len(cleaned_notifs)


# ============================================
# NOTIFICATION PREFERENCES
# ============================================

def should_send_email(user_email: str, notification_type: str) -> bool:
    """Check if user wants email for this notification type"""
    try:
        # Load user preferences
        with open('data/notifications/preferences.json', 'r') as f:
            all_prefs = json.load(f)
        
        user_prefs = all_prefs.get(user_email, {})
        
        # Default: send all emails
        default_prefs = {
            NotificationType.INFO: True,
            NotificationType.SUCCESS: True,
            NotificationType.WARNING: True,
            NotificationType.URGENT: True,
            NotificationType.MESSAGE: True,
            NotificationType.APPROVAL: True,
            NotificationType.SYSTEM: True
        }
        
        return user_prefs.get(notification_type, default_prefs.get(notification_type, True))
    
    except FileNotFoundError:
        return True  # Default: send emails
    except Exception:
        return True


def update_notification_preferences(user_email: str, preferences: dict):
    """Update user's notification preferences"""
    try:
        # Load existing
        try:
            with open('data/notifications/preferences.json', 'r') as f:
                all_prefs = json.load(f)
        except FileNotFoundError:
            all_prefs = {}
        
        # Update
        all_prefs[user_email] = preferences
        
        # Save
        os.makedirs('data/notifications', exist_ok=True)
        with open('data/notifications/preferences.json', 'w') as f:
            json.dump(all_prefs, f, indent=2)
    
    except Exception as e:
        print(f"Error updating preferences: {e}")


# ============================================
# EMAIL INTEGRATION
# ============================================

def send_notification_email(notification: Notification):
    """Send email for notification"""
    try:
        from email_service import send_email
        
        # Create email content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #0066cc;">
                <h2 style="color: #0066cc;">📬 {notification.title}</h2>
                
                <div style="background: #f0f8ff; padding: 15px; margin: 20px 0; border-left: 4px solid #0066cc;">
                    <p>{notification.message}</p>
                </div>
                
                {f'<p><a href="{notification.action_url}" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">{notification.action_label}</a></p>' if notification.action_url else ''}
                
                <p style="font-size: 12px; color: #666; margin-top: 20px;">
                You received this because you have notifications enabled. 
                You can manage your notification preferences in your account settings.
                </p>
            </div>
        </body>
        </html>
        """
        
        send_email(
            to_email=notification.user_email,
            subject=notification.title,
            html_content=html_content
        )
    
    except Exception as e:
        print(f"Error sending notification email: {e}")


# Export functions
__all__ = [
    'Notification',
    'NotificationType',
    'NotificationPriority',
    'create_notification',
    'get_user_notifications',
    'get_unread_count',
    'mark_as_read',
    'mark_all_as_read',
    'delete_notification',
    'cleanup_old_notifications',
    'update_notification_preferences'
]
