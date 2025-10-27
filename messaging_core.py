"""
T21 MESSAGING SYSTEM - CORE FUNCTIONS
Real-time messaging with Supabase backend

Features:
- Channels (group chats)
- Direct messages (1-on-1)
- Real-time updates
- File attachments
- Message reactions
- Typing indicators
- Online presence
- Notifications
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional
import uuid

# Import Supabase client
try:
    from supabase_client import get_supabase_client
except ImportError:
    try:
        from supabase_database import supabase as get_supabase_client
    except:
        def get_supabase_client():
            return None


# ============================================
# CHANNEL FUNCTIONS
# ============================================

def get_user_channels(user_email: str) -> List[Dict]:
    """Get all channels user is a member of"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        # Get channels user is member of
        response = supabase.table('channel_members')\
            .select('*, channels(*)')\
            .eq('user_email', user_email)\
            .execute()
        
        if response.data:
            channels = []
            for member in response.data:
                if member.get('channels'):
                    channel = member['channels']
                    channel['user_role'] = member.get('role')
                    channel['last_read_at'] = member.get('last_read_at')
                    channel['notifications'] = member.get('notifications')
                    channels.append(channel)
            return channels
        return []
    except Exception as e:
        st.error(f"Error loading channels: {str(e)}")
        return []


def get_channel_messages(channel_id: str, limit: int = 50) -> List[Dict]:
    """Get messages from a channel"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('messages')\
            .select('*')\
            .eq('channel_id', channel_id)\
            .eq('is_deleted', False)\
            .order('created_at', desc=False)\
            .limit(limit)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading messages: {str(e)}")
        return []


def send_channel_message(channel_id: str, sender_email: str, sender_name: str, content: str, mentions: List[str] = None) -> bool:
    """Send a message to a channel"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        message_data = {
            'channel_id': channel_id,
            'sender_email': sender_email,
            'sender_name': sender_name,
            'content': content,
            'mentions': mentions or [],
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('messages').insert(message_data).execute()
        
        # Create notifications for mentions
        if mentions and response.data:
            message_id = response.data[0]['id']
            create_mention_notifications(message_id, channel_id, mentions)
        
        return True
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        return False


def join_channel(channel_id: str, user_email: str, user_name: str) -> bool:
    """Join a channel"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        member_data = {
            'channel_id': channel_id,
            'user_email': user_email,
            'user_name': user_name,
            'role': 'member',
            'joined_at': datetime.now().isoformat()
        }
        
        supabase.table('channel_members').insert(member_data).execute()
        return True
    except Exception as e:
        # Might already be a member
        return False


def get_channel_members(channel_id: str) -> List[Dict]:
    """Get all members of a channel"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('channel_members')\
            .select('*')\
            .eq('channel_id', channel_id)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        return []


# ============================================
# DIRECT MESSAGE FUNCTIONS
# ============================================

def get_direct_messages(user_email: str, other_email: str, limit: int = 50) -> List[Dict]:
    """Get direct messages between two users"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        # Get messages in both directions
        response = supabase.table('direct_messages')\
            .select('*')\
            .or_(f'and(sender_email.eq.{user_email},recipient_email.eq.{other_email}),and(sender_email.eq.{other_email},recipient_email.eq.{user_email})')\
            .eq('is_deleted', False)\
            .order('created_at', desc=False)\
            .limit(limit)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading DMs: {str(e)}")
        return []


def send_direct_message(sender_email: str, sender_name: str, recipient_email: str, recipient_name: str, content: str) -> bool:
    """Send a direct message"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        # Generate or get conversation ID
        conversation_id = generate_conversation_id(sender_email, recipient_email)
        
        dm_data = {
            'sender_email': sender_email,
            'sender_name': sender_name,
            'recipient_email': recipient_email,
            'recipient_name': recipient_name,
            'content': content,
            'conversation_id': conversation_id,
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('direct_messages').insert(dm_data).execute()
        
        # Create notification for recipient
        if response.data:
            dm_id = response.data[0]['id']
            create_dm_notification(dm_id, recipient_email)
        
        return True
    except Exception as e:
        st.error(f"Error sending DM: {str(e)}")
        return False


def get_conversations(user_email: str) -> List[Dict]:
    """Get all conversations for a user"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        # Get latest message from each conversation
        response = supabase.table('direct_messages')\
            .select('*')\
            .or_(f'sender_email.eq.{user_email},recipient_email.eq.{user_email}')\
            .eq('is_deleted', False)\
            .order('created_at', desc=True)\
            .execute()
        
        if not response.data:
            return []
        
        # Group by conversation and get latest
        conversations = {}
        for dm in response.data:
            conv_id = dm['conversation_id']
            if conv_id not in conversations:
                # Determine other user
                if dm['sender_email'] == user_email:
                    other_email = dm['recipient_email']
                    other_name = dm['recipient_name']
                else:
                    other_email = dm['sender_email']
                    other_name = dm['sender_name']
                
                conversations[conv_id] = {
                    'conversation_id': conv_id,
                    'other_email': other_email,
                    'other_name': other_name,
                    'last_message': dm['content'],
                    'last_message_time': dm['created_at'],
                    'unread': dm.get('read_at') is None and dm['recipient_email'] == user_email
                }
        
        return list(conversations.values())
    except Exception as e:
        st.error(f"Error loading conversations: {str(e)}")
        return []


def mark_dm_as_read(dm_id: str) -> bool:
    """Mark a direct message as read"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        supabase.table('direct_messages')\
            .update({'read_at': datetime.now().isoformat()})\
            .eq('id', dm_id)\
            .execute()
        return True
    except:
        return False


# ============================================
# NOTIFICATION FUNCTIONS
# ============================================

def get_unread_notifications(user_email: str) -> List[Dict]:
    """Get unread notifications for user"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('message_notifications')\
            .select('*')\
            .eq('user_email', user_email)\
            .eq('is_read', False)\
            .order('created_at', desc=True)\
            .execute()
        
        return response.data if response.data else []
    except:
        return []


def get_unread_count(user_email: str) -> int:
    """Get count of unread notifications"""
    notifications = get_unread_notifications(user_email)
    return len(notifications)


def create_mention_notifications(message_id: str, channel_id: str, mentioned_emails: List[str]):
    """Create notifications for mentioned users"""
    supabase = get_supabase_client()
    if not supabase:
        return
    
    try:
        notifications = []
        for email in mentioned_emails:
            notifications.append({
                'user_email': email,
                'message_id': message_id,
                'channel_id': channel_id,
                'notification_type': 'mention',
                'created_at': datetime.now().isoformat()
            })
        
        if notifications:
            supabase.table('message_notifications').insert(notifications).execute()
    except:
        pass


def create_dm_notification(dm_id: str, recipient_email: str):
    """Create notification for DM"""
    supabase = get_supabase_client()
    if not supabase:
        return
    
    try:
        notification = {
            'user_email': recipient_email,
            'dm_id': dm_id,
            'notification_type': 'dm',
            'created_at': datetime.now().isoformat()
        }
        
        supabase.table('message_notifications').insert(notification).execute()
    except:
        pass


def mark_notifications_read(user_email: str, channel_id: str = None):
    """Mark notifications as read"""
    supabase = get_supabase_client()
    if not supabase:
        return
    
    try:
        query = supabase.table('message_notifications')\
            .update({'is_read': True, 'read_at': datetime.now().isoformat()})\
            .eq('user_email', user_email)
        
        if channel_id:
            query = query.eq('channel_id', channel_id)
        
        query.execute()
    except:
        pass


# ============================================
# PRESENCE FUNCTIONS
# ============================================

def update_user_presence(user_email: str, user_name: str, status: str = 'online', custom_status: str = None):
    """Update user's online presence"""
    supabase = get_supabase_client()
    if not supabase:
        return
    
    try:
        presence_data = {
            'user_email': user_email,
            'user_name': user_name,
            'status': status,
            'custom_status': custom_status,
            'last_seen': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Upsert (insert or update)
        supabase.table('user_presence').upsert(presence_data).execute()
    except:
        pass


def get_online_users() -> List[Dict]:
    """Get list of online users"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('user_presence')\
            .select('*')\
            .eq('status', 'online')\
            .execute()
        
        return response.data if response.data else []
    except:
        return []


def get_user_status(user_email: str) -> Dict:
    """Get a user's presence status"""
    supabase = get_supabase_client()
    if not supabase:
        return {'status': 'offline'}
    
    try:
        response = supabase.table('user_presence')\
            .select('*')\
            .eq('user_email', user_email)\
            .execute()
        
        if response.data:
            return response.data[0]
        return {'status': 'offline'}
    except:
        return {'status': 'offline'}


# ============================================
# MESSAGE REACTIONS
# ============================================

def add_reaction(message_id: str, user_email: str, user_name: str, emoji: str) -> bool:
    """Add emoji reaction to message"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        reaction_data = {
            'message_id': message_id,
            'user_email': user_email,
            'user_name': user_name,
            'emoji': emoji,
            'created_at': datetime.now().isoformat()
        }
        
        supabase.table('message_reactions').insert(reaction_data).execute()
        return True
    except:
        return False


def get_message_reactions(message_id: str) -> List[Dict]:
    """Get all reactions for a message"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('message_reactions')\
            .select('*')\
            .eq('message_id', message_id)\
            .execute()
        
        return response.data if response.data else []
    except:
        return []


# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_conversation_id(email1: str, email2: str) -> str:
    """Generate consistent conversation ID for two users"""
    # Sort emails to ensure same ID regardless of order
    emails = sorted([email1, email2])
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{emails[0]}_{emails[1]}"))


def search_messages(user_email: str, query: str, channel_id: str = None) -> List[Dict]:
    """Search messages"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        # Search in channels user is member of
        if channel_id:
            response = supabase.table('messages')\
                .select('*')\
                .eq('channel_id', channel_id)\
                .ilike('content', f'%{query}%')\
                .execute()
        else:
            # Search all accessible messages
            user_channels = get_user_channels(user_email)
            channel_ids = [c['id'] for c in user_channels]
            
            response = supabase.table('messages')\
                .select('*')\
                .in_('channel_id', channel_ids)\
                .ilike('content', f'%{query}%')\
                .execute()
        
        return response.data if response.data else []
    except:
        return []


def get_channel_info(channel_id: str) -> Dict:
    """Get channel information"""
    supabase = get_supabase_client()
    if not supabase:
        return {}
    
    try:
        response = supabase.table('channels')\
            .select('*')\
            .eq('id', channel_id)\
            .execute()
        
        if response.data:
            return response.data[0]
        return {}
    except:
        return {}
