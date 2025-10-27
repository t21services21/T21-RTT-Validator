"""
T21 MESSAGING SYSTEM - MODERN INTERFACE
Slack/Teams-style messaging with channels and DMs
"""

import streamlit as st
from datetime import datetime
from messaging_core import *
import time

def render_messaging_interface():
    """Main messaging interface - Slack/Teams style"""
    
    st.title("💬 Messages")
    
    # Get current user
    user_email = st.session_state.get('user_email', '')
    user_name = st.session_state.get('user_name', user_email.split('@')[0])
    
    if not user_email:
        st.warning("Please log in to use messaging")
        return
    
    # Update user presence
    update_user_presence(user_email, user_name, 'online')
    
    # Initialize session state
    if 'current_channel' not in st.session_state:
        st.session_state.current_channel = None
    if 'current_dm_user' not in st.session_state:
        st.session_state.current_dm_user = None
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'channels'  # 'channels' or 'dms'
    
    # Get unread count
    unread_count = get_unread_count(user_email)
    
    # Layout: Sidebar + Main Chat Area
    col_sidebar, col_main = st.columns([1, 3])
    
    with col_sidebar:
        render_sidebar(user_email, user_name, unread_count)
    
    with col_main:
        if st.session_state.view_mode == 'channels' and st.session_state.current_channel:
            render_channel_chat(user_email, user_name)
        elif st.session_state.view_mode == 'dms' and st.session_state.current_dm_user:
            render_dm_chat(user_email, user_name)
        else:
            render_welcome_screen()


def render_sidebar(user_email: str, user_name: str, unread_count: int):
    """Render sidebar with channels and DMs"""
    
    st.markdown(f"### {user_name} 🟢")
    
    if unread_count > 0:
        st.info(f"🔔 {unread_count} unread messages")
    
    st.markdown("---")
    
    # View mode tabs
    tab1, tab2 = st.tabs(["📢 Channels", "💬 Direct Messages"])
    
    with tab1:
        render_channels_list(user_email)
    
    with tab2:
        render_conversations_list(user_email)


def render_channels_list(user_email: str):
    """Render list of channels"""
    
    channels = get_user_channels(user_email)
    
    if not channels:
        st.info("No channels yet. Join a channel to start!")
        return
    
    for channel in channels:
        channel_id = channel['id']
        channel_name = channel['name']
        channel_type = channel.get('type', 'public')
        
        # Icon based on type
        if channel_type == 'announcement':
            icon = "📢"
        elif channel_type == 'private':
            icon = "🔒"
        else:
            icon = "#"
        
        # Check if current channel
        is_current = st.session_state.current_channel == channel_id
        
        # Button style
        button_type = "primary" if is_current else "secondary"
        
        if st.button(f"{icon} {channel_name}", key=f"channel_{channel_id}", type=button_type, use_container_width=True):
            st.session_state.current_channel = channel_id
            st.session_state.view_mode = 'channels'
            st.session_state.current_dm_user = None
            mark_notifications_read(user_email, channel_id)
            st.rerun()


def render_conversations_list(user_email: str):
    """Render list of DM conversations"""
    
    conversations = get_conversations(user_email)
    
    if not conversations:
        st.info("No conversations yet. Start a new one!")
        
        # New DM button
        if st.button("➕ New Message", use_container_width=True):
            st.session_state.show_new_dm = True
            st.rerun()
        return
    
    for conv in conversations:
        other_email = conv['other_email']
        other_name = conv['other_name']
        last_message = conv['last_message'][:30] + "..." if len(conv['last_message']) > 30 else conv['last_message']
        unread = conv.get('unread', False)
        
        # Check if current conversation
        is_current = st.session_state.current_dm_user == other_email
        
        # Button style
        button_type = "primary" if is_current else "secondary"
        
        # Unread indicator
        unread_badge = "🔴 " if unread else ""
        
        if st.button(f"{unread_badge}{other_name}\n{last_message}", key=f"dm_{other_email}", type=button_type, use_container_width=True):
            st.session_state.current_dm_user = other_email
            st.session_state.view_mode = 'dms'
            st.session_state.current_channel = None
            st.rerun()
    
    st.markdown("---")
    if st.button("➕ New Message", use_container_width=True):
        st.session_state.show_new_dm = True
        st.rerun()


def render_channel_chat(user_email: str, user_name: str):
    """Render channel chat area"""
    
    channel_id = st.session_state.current_channel
    channel_info = get_channel_info(channel_id)
    
    if not channel_info:
        st.error("Channel not found")
        return
    
    # Channel header
    st.markdown(f"## # {channel_info['name']}")
    if channel_info.get('description'):
        st.caption(channel_info['description'])
    
    st.markdown("---")
    
    # Messages area
    messages = get_channel_messages(channel_id, limit=100)
    
    # Display messages
    message_container = st.container()
    with message_container:
        if not messages:
            st.info("No messages yet. Be the first to say something!")
        else:
            for msg in messages:
                render_message(msg, user_email)
    
    st.markdown("---")
    
    # Message input
    with st.form(key=f"channel_message_form_{channel_id}", clear_on_submit=True):
        message_text = st.text_area("Type a message...", key=f"msg_input_{channel_id}", height=100)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            send_button = st.form_submit_button("📤 Send", type="primary")
        with col2:
            attach_button = st.form_submit_button("📎 Attach")
        
        if send_button and message_text.strip():
            # Check for @mentions
            mentions = extract_mentions(message_text)
            
            if send_channel_message(channel_id, user_email, user_name, message_text, mentions):
                st.success("Message sent!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Failed to send message")


def render_dm_chat(user_email: str, user_name: str):
    """Render direct message chat area"""
    
    other_email = st.session_state.current_dm_user
    
    # Get other user's info
    other_status = get_user_status(other_email)
    other_name = other_status.get('user_name', other_email.split('@')[0])
    status = other_status.get('status', 'offline')
    
    # Status indicator
    status_emoji = {
        'online': '🟢',
        'away': '🟡',
        'busy': '🔴',
        'offline': '⚫'
    }.get(status, '⚫')
    
    # DM header
    st.markdown(f"## {status_emoji} {other_name}")
    st.caption(other_email)
    
    st.markdown("---")
    
    # Messages area
    messages = get_direct_messages(user_email, other_email, limit=100)
    
    # Display messages
    message_container = st.container()
    with message_container:
        if not messages:
            st.info("No messages yet. Start the conversation!")
        else:
            for msg in messages:
                render_dm_message(msg, user_email)
                
                # Mark as read if recipient
                if msg['recipient_email'] == user_email and not msg.get('read_at'):
                    mark_dm_as_read(msg['id'])
    
    st.markdown("---")
    
    # Message input
    with st.form(key=f"dm_message_form_{other_email}", clear_on_submit=True):
        message_text = st.text_area("Type a message...", key=f"dm_input_{other_email}", height=100)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            send_button = st.form_submit_button("📤 Send", type="primary")
        with col2:
            attach_button = st.form_submit_button("📎 Attach")
        
        if send_button and message_text.strip():
            if send_direct_message(user_email, user_name, other_email, other_name, message_text):
                st.success("Message sent!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Failed to send message")


def render_message(msg: Dict, current_user_email: str):
    """Render a single channel message"""
    
    sender_name = msg.get('sender_name', 'Unknown')
    sender_email = msg.get('sender_email', '')
    content = msg.get('content', '')
    created_at = msg.get('created_at', '')
    
    # Format timestamp
    try:
        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        time_str = dt.strftime("%I:%M %p")
    except:
        time_str = ""
    
    # Check if own message
    is_own = sender_email == current_user_email
    
    # Message styling
    if is_own:
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0;">
            <strong>{sender_name}</strong> <small style="color: #666;">{time_str}</small><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 10px; margin: 5px 0;">
            <strong>{sender_name}</strong> <small style="color: #666;">{time_str}</small><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    
    # Reactions
    reactions = get_message_reactions(msg['id'])
    if reactions:
        reaction_counts = {}
        for r in reactions:
            emoji = r['emoji']
            reaction_counts[emoji] = reaction_counts.get(emoji, 0) + 1
        
        reaction_str = " ".join([f"{emoji} {count}" for emoji, count in reaction_counts.items()])
        st.caption(reaction_str)


def render_dm_message(msg: Dict, current_user_email: str):
    """Render a single DM message"""
    
    sender_email = msg.get('sender_email', '')
    sender_name = msg.get('sender_name', 'Unknown')
    content = msg.get('content', '')
    created_at = msg.get('created_at', '')
    
    # Format timestamp
    try:
        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        time_str = dt.strftime("%I:%M %p")
    except:
        time_str = ""
    
    # Check if own message
    is_own = sender_email == current_user_email
    
    # Message styling
    if is_own:
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: right;">
            <small style="color: #666;">{time_str}</small><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 10px; margin: 5px 0;">
            <strong>{sender_name}</strong> <small style="color: #666;">{time_str}</small><br>
            {content}
        </div>
        """, unsafe_allow_html=True)


def render_welcome_screen():
    """Render welcome screen when no channel/DM selected"""
    
    st.markdown("""
    ## 👋 Welcome to T21 Messaging!
    
    **Get started:**
    - 📢 Select a channel from the sidebar to join conversations
    - 💬 Click on a direct message to chat 1-on-1
    - ➕ Start a new conversation
    
    **Features:**
    - Real-time messaging
    - File attachments
    - @mentions
    - Message reactions
    - Online presence
    
    **Select a channel or conversation to begin!**
    """)


def extract_mentions(text: str) -> List[str]:
    """Extract @mentions from message text"""
    import re
    mentions = re.findall(r'@(\S+)', text)
    return mentions


# ============================================
# HELPER FUNCTIONS
# ============================================

def show_new_dm_dialog():
    """Show dialog to start new DM"""
    
    st.subheader("➕ New Message")
    
    # Get list of users (you'd need to implement this)
    # For now, just a text input
    recipient_email = st.text_input("Recipient Email")
    message_text = st.text_area("Message")
    
    if st.button("Send"):
        user_email = st.session_state.get('user_email', '')
        user_name = st.session_state.get('user_name', '')
        
        if recipient_email and message_text:
            if send_direct_message(user_email, user_name, recipient_email, recipient_email.split('@')[0], message_text):
                st.success("Message sent!")
                st.session_state.show_new_dm = False
                st.session_state.current_dm_user = recipient_email
                st.session_state.view_mode = 'dms'
                st.rerun()
