"""
MESSAGING UI - Student ↔ Teacher ↔ Admin Communication

FEATURES:
- Inbox (received messages)
- Sent messages
- Compose new message
- Reply to message
- Thread view
- Unread badge
- Search messages
"""

import streamlit as st
from messaging_system import (
    send_message,
    reply_to_message,
    get_user_messages,
    get_unread_message_count,
    get_message_by_id,
    get_message_thread,
    mark_message_as_read,
    delete_message
)


def render_messaging_system():
    """Main messaging interface"""
    
    st.header("💬 Messages")
    
    if 'user_email' not in st.session_state:
        st.warning("Please login to view messages")
        return
    
    user_email = st.session_state.user_email
    user_name = st.session_state.get('user_name', 'User')
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📥 Inbox", "📤 Sent", "✉️ Compose"])
    
    with tab1:
        render_inbox(user_email)
    
    with tab2:
        render_sent_messages(user_email)
    
    with tab3:
        render_compose_message(user_email, user_name)


def render_inbox(user_email: str):
    """Render inbox"""
    
    st.subheader("📥 Inbox")
    
    # Get messages
    inbox_messages = get_user_messages(user_email, folder='inbox')
    unread_count = get_unread_message_count(user_email)
    
    if unread_count > 0:
        st.info(f"📬 You have {unread_count} unread message{'s' if unread_count > 1 else ''}")
    
    if not inbox_messages:
        st.info("📭 No messages in inbox")
        return
    
    # Display messages
    for message in inbox_messages:
        render_message_card(message, folder='inbox', user_email=user_email)


def render_sent_messages(user_email: str):
    """Render sent messages"""
    
    st.subheader("📤 Sent Messages")
    
    sent_messages = get_user_messages(user_email, folder='sent')
    
    if not sent_messages:
        st.info("📭 No sent messages")
        return
    
    # Display messages
    for message in sent_messages:
        render_message_card(message, folder='sent', user_email=user_email)


def render_message_card(message, folder: str, user_email: str):
    """Render single message card"""
    
    # Icon for priority
    priority_icons = {
        'normal': '✉️',
        'high': '⚠️',
        'urgent': '🚨'
    }
    icon = priority_icons.get(message.priority, '✉️')
    
    # Background if unread (inbox only)
    bg_color = "#fff3cd" if (folder == 'inbox' and not message.read) else "#f8f9fa"
    
    with st.expander(f"{icon} {message.subject} - From: {message.from_name if folder == 'inbox' else message.to_name}"):
        # Message details
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**From:** {message.from_name} ({message.from_email})")
            st.markdown(f"**To:** {message.to_name} ({message.to_email})")
            st.markdown(f"**Subject:** {message.subject}")
            st.markdown(f"**Date:** {message.created_at[:19].replace('T', ' ')}")
        
        with col2:
            st.markdown(f"**Priority:** {message.priority.title()}")
            st.markdown(f"**Category:** {message.category.title()}")
            if folder == 'inbox':
                st.markdown(f"**Status:** {'Unread' if not message.read else 'Read'}")
        
        st.markdown("---")
        st.markdown(message.body)
        
        # Actions
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if folder == 'inbox':
                if st.button("↩️ Reply", key=f"reply_{message.id}"):
                    st.session_state[f'reply_to_{message.id}'] = True
                    st.rerun()
        
        with col2:
            if folder == 'inbox' and not message.read:
                if st.button("✓ Mark Read", key=f"read_msg_{message.id}"):
                    mark_message_as_read(message.id)
                    st.rerun()
        
        with col3:
            if st.button("🗑️ Delete", key=f"del_msg_{message.id}"):
                delete_message(message.id, user_email)
                st.rerun()
        
        # Reply form (if replying)
        if st.session_state.get(f'reply_to_{message.id}', False):
            st.markdown("---")
            st.markdown("### ↩️ Reply")
            
            with st.form(key=f"reply_form_{message.id}"):
                reply_body = st.text_area("Your Reply", height=150, key=f"reply_body_{message.id}")
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    submit = st.form_submit_button("📤 Send Reply", type="primary")
                with col2:
                    cancel = st.form_submit_button("❌ Cancel")
                
                if submit and reply_body:
                    # Send reply
                    user_name = st.session_state.get('user_name', 'User')
                    reply_to_message(
                        original_message_id=message.id,
                        from_email=user_email,
                        from_name=user_name,
                        body=reply_body,
                        notify=True
                    )
                    
                    # Mark original as read
                    mark_message_as_read(message.id)
                    
                    st.success("✅ Reply sent!")
                    del st.session_state[f'reply_to_{message.id}']
                    st.rerun()
                
                if cancel:
                    del st.session_state[f'reply_to_{message.id}']
                    st.rerun()


def render_compose_message(user_email: str, user_name: str):
    """Render compose new message form"""
    
    st.subheader("✉️ Compose New Message")
    
    with st.form("compose_message_form"):
        # Recipient selection
        recipient_type = st.radio("Send to:", ["Specific Person", "All Teachers", "All Students"], key="recipient_type")
        
        if recipient_type == "Specific Person":
            recipient_email = st.text_input("Recipient Email*", placeholder="teacher@example.com", key="recipient_email")
            recipient_name = st.text_input("Recipient Name", placeholder="Teacher Name", key="recipient_name")
        else:
            recipient_email = "broadcast"
            recipient_name = recipient_type
        
        # Message details
        subject = st.text_input("Subject*", placeholder="Enter subject", key="msg_subject")
        
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Priority", ["normal", "high", "urgent"], key="msg_priority")
        with col2:
            category = st.selectbox("Category", ["general", "question", "support", "announcement"], key="msg_category")
        
        body = st.text_area("Message*", height=200, placeholder="Type your message here...", key="msg_body")
        
        send_notification = st.checkbox("📧 Send email notification to recipient", value=True, key="send_notif")
        
        submit = st.form_submit_button("📤 Send Message", type="primary")
        
        if submit:
            if not subject or not body:
                st.error("❌ Please fill in subject and message")
            elif recipient_type == "Specific Person" and not recipient_email:
                st.error("❌ Please enter recipient email")
            else:
                # Send message
                if recipient_type == "Specific Person":
                    send_message(
                        from_email=user_email,
                        from_name=user_name,
                        to_email=recipient_email,
                        to_name=recipient_name or "User",
                        subject=subject,
                        body=body,
                        priority=priority,
                        category=category,
                        notify=send_notification
                    )
                    st.success(f"✅ Message sent to {recipient_name or recipient_email}!")
                else:
                    # Broadcast (implement broadcast logic)
                    st.info(f"Broadcasting to {recipient_type}... (Feature coming soon)")
                
                st.rerun()


def render_message_badge_sidebar():
    """Render message badge in sidebar"""
    try:
        if 'user_email' not in st.session_state:
            return
        
        user_email = st.session_state.user_email
        unread_count = get_unread_message_count(user_email)
        
        if unread_count > 0:
            st.sidebar.markdown(f"""
            <div style="background: #28a745; color: white; border-radius: 50%; 
                        width: 30px; height: 30px; display: flex; align-items: center; 
                        justify-content: center; font-weight: bold; margin: 10px auto;">
                {unread_count}
            </div>
            <p style="text-align: center; font-size: 12px; margin-top: -5px;">
            💬 Messages
            </p>
            """, unsafe_allow_html=True)
            
            if st.sidebar.button("💬 View Messages", use_container_width=True, key="view_messages_btn"):
                st.session_state['show_messages'] = True
                st.rerun()
    
    except Exception as e:
        print(f"Error rendering message badge: {e}")


# Export
__all__ = [
    'render_messaging_system',
    'render_message_badge_sidebar'
]
