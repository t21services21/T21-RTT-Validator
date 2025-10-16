"""
COMPREHENSIVE MESSAGING SYSTEM
Student ↔ Teacher ↔ Admin Communication

FEATURES:
- Direct messages between users
- Group messages (cohorts, classes)
- Attachments support
- Read receipts
- Message threads
- Search and filters
- Auto-notify recipients (email + in-app)
- Archive messages

USE CASES:
- Student asks teacher a question
- Teacher broadcasts to class
- Admin sends announcements
- Support tickets
- Feedback and reviews
"""

from datetime import datetime
import json
import os
from typing import List, Dict, Optional
import uuid


class Message:
    """Single message object"""
    
    def __init__(self, message_data: dict):
        self.id = message_data.get('id', self._generate_id())
        self.from_email = message_data.get('from_email')
        self.from_name = message_data.get('from_name')
        self.to_email = message_data.get('to_email')  # Single recipient or list
        self.to_name = message_data.get('to_name')
        self.subject = message_data.get('subject')
        self.body = message_data.get('body')
        self.thread_id = message_data.get('thread_id', self.id)  # For replies
        self.attachments = message_data.get('attachments', [])
        self.created_at = message_data.get('created_at', datetime.now().isoformat())
        self.read = message_data.get('read', False)
        self.read_at = message_data.get('read_at')
        self.priority = message_data.get('priority', 'normal')  # normal, high, urgent
        self.category = message_data.get('category', 'general')  # general, question, support, announcement
        self.metadata = message_data.get('metadata', {})
    
    def _generate_id(self):
        return f"msg_{uuid.uuid4().hex[:12]}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'from_email': self.from_email,
            'from_name': self.from_name,
            'to_email': self.to_email,
            'to_name': self.to_name,
            'subject': self.subject,
            'body': self.body,
            'thread_id': self.thread_id,
            'attachments': self.attachments,
            'created_at': self.created_at,
            'read': self.read,
            'read_at': self.read_at,
            'priority': self.priority,
            'category': self.category,
            'metadata': self.metadata
        }


# ============================================
# MESSAGE MANAGEMENT
# ============================================

def send_message(from_email: str, from_name: str, to_email: str, to_name: str,
                subject: str, body: str, priority: str = 'normal',
                category: str = 'general', notify: bool = True) -> Message:
    """
    Send a message
    
    Args:
        from_email: Sender email
        from_name: Sender name
        to_email: Recipient email (can be list for multiple)
        to_name: Recipient name
        subject: Message subject
        body: Message body
        priority: normal, high, urgent
        category: general, question, support, announcement
        notify: Send notification to recipient
    
    Returns:
        Message object
    """
    message_data = {
        'from_email': from_email,
        'from_name': from_name,
        'to_email': to_email,
        'to_name': to_name,
        'subject': subject,
        'body': body,
        'priority': priority,
        'category': category
    }
    
    message = Message(message_data)
    
    # Save message
    save_message(message)
    
    # Send notification to recipient
    if notify:
        notify_new_message(message)
    
    return message


def reply_to_message(original_message_id: str, from_email: str, from_name: str,
                    body: str, notify: bool = True) -> Message:
    """Reply to an existing message"""
    
    # Get original message
    original = get_message_by_id(original_message_id)
    if not original:
        return None
    
    # Create reply
    reply_data = {
        'from_email': from_email,
        'from_name': from_name,
        'to_email': original.from_email,  # Reply to sender
        'to_name': original.from_name,
        'subject': f"Re: {original.subject}",
        'body': body,
        'thread_id': original.thread_id,  # Keep in same thread
        'priority': original.priority,
        'category': original.category
    }
    
    reply = Message(reply_data)
    save_message(reply)
    
    if notify:
        notify_new_message(reply)
    
    return reply


def save_message(message: Message):
    """Save message to database"""
    try:
        messages = load_all_messages()
        
        # Update or add
        existing_index = None
        for i, msg in enumerate(messages):
            if msg['id'] == message.id:
                existing_index = i
                break
        
        if existing_index is not None:
            messages[existing_index] = message.to_dict()
        else:
            messages.append(message.to_dict())
        
        os.makedirs('data/messages', exist_ok=True)
        with open('data/messages/all_messages.json', 'w') as f:
            json.dump(messages, f, indent=2)
    
    except Exception as e:
        print(f"Error saving message: {e}")


def load_all_messages() -> List[dict]:
    """Load all messages"""
    try:
        with open('data/messages/all_messages.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []


def get_user_messages(user_email: str, folder: str = 'inbox') -> List[Message]:
    """
    Get messages for a user
    
    Args:
        user_email: User's email
        folder: 'inbox', 'sent', 'all'
    
    Returns:
        List of Message objects
    """
    all_messages = load_all_messages()
    
    if folder == 'inbox':
        user_messages = [Message(m) for m in all_messages if m['to_email'] == user_email]
    elif folder == 'sent':
        user_messages = [Message(m) for m in all_messages if m['from_email'] == user_email]
    else:  # all
        user_messages = [Message(m) for m in all_messages 
                        if m['to_email'] == user_email or m['from_email'] == user_email]
    
    # Sort by date (newest first)
    user_messages.sort(key=lambda x: x.created_at, reverse=True)
    
    return user_messages


def get_unread_message_count(user_email: str) -> int:
    """Get count of unread messages"""
    inbox = get_user_messages(user_email, folder='inbox')
    unread = [m for m in inbox if not m.read]
    return len(unread)


def get_message_by_id(message_id: str) -> Optional[Message]:
    """Get specific message by ID"""
    all_messages = load_all_messages()
    
    for msg in all_messages:
        if msg['id'] == message_id:
            return Message(msg)
    
    return None


def get_message_thread(thread_id: str) -> List[Message]:
    """Get all messages in a thread"""
    all_messages = load_all_messages()
    
    thread_messages = [Message(m) for m in all_messages if m['thread_id'] == thread_id]
    
    # Sort by date (oldest first for thread view)
    thread_messages.sort(key=lambda x: x.created_at)
    
    return thread_messages


def mark_message_as_read(message_id: str):
    """Mark message as read"""
    all_messages = load_all_messages()
    
    for msg in all_messages:
        if msg['id'] == message_id:
            msg['read'] = True
            msg['read_at'] = datetime.now().isoformat()
            break
    
    os.makedirs('data/messages', exist_ok=True)
    with open('data/messages/all_messages.json', 'w') as f:
        json.dump(all_messages, f, indent=2)


def delete_message(message_id: str, user_email: str):
    """Delete message (soft delete - just hide from user)"""
    all_messages = load_all_messages()
    
    for msg in all_messages:
        if msg['id'] == message_id:
            # Add to deleted_by list
            if 'deleted_by' not in msg['metadata']:
                msg['metadata']['deleted_by'] = []
            msg['metadata']['deleted_by'].append(user_email)
            break
    
    os.makedirs('data/messages', exist_ok=True)
    with open('data/messages/all_messages.json', 'w') as f:
        json.dump(all_messages, f, indent=2)


# ============================================
# NOTIFICATION INTEGRATION
# ============================================

def notify_new_message(message: Message):
    """Send notification when new message received"""
    try:
        from notification_system import create_notification, NotificationType, NotificationPriority
        
        # Determine priority
        priority_map = {
            'normal': NotificationPriority.MEDIUM,
            'high': NotificationPriority.HIGH,
            'urgent': NotificationPriority.URGENT
        }
        
        # Create notification
        create_notification(
            user_email=message.to_email,
            title=f"💬 New Message from {message.from_name}",
            message=f"Subject: {message.subject}",
            notification_type=NotificationType.MESSAGE,
            priority=priority_map.get(message.priority, NotificationPriority.MEDIUM),
            action_url="/messages",  # Link to messages page
            action_label="View Message",
            send_email=True,  # Also send email
            metadata={'message_id': message.id}
        )
    
    except Exception as e:
        print(f"Error sending message notification: {e}")


# ============================================
# BROADCAST MESSAGES
# ============================================

def broadcast_message(from_email: str, from_name: str, recipients: List[str],
                     subject: str, body: str, category: str = 'announcement'):
    """
    Send message to multiple recipients
    
    Args:
        from_email: Sender email
        from_name: Sender name
        recipients: List of recipient emails
        subject: Message subject
        body: Message body
        category: Message category
    """
    for recipient_email in recipients:
        send_message(
            from_email=from_email,
            from_name=from_name,
            to_email=recipient_email,
            to_name="Student",  # Could look up actual name
            subject=subject,
            body=body,
            priority='high',
            category=category,
            notify=True
        )


def get_cohort_emails(cohort_id: str) -> List[str]:
    """Get all student emails in a cohort"""
    # TODO: Integrate with your student management system
    # This is a placeholder
    return []


# Export
__all__ = [
    'Message',
    'send_message',
    'reply_to_message',
    'get_user_messages',
    'get_unread_message_count',
    'get_message_by_id',
    'get_message_thread',
    'mark_message_as_read',
    'delete_message',
    'broadcast_message'
]
