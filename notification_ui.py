"""
NOTIFICATION UI - Pop-ups, Badges, Notification Center

FEATURES:
- Notification badge (unread count)
- Pop-up notifications (for urgent items)
- Notification center (view all)
- Mark as read
- Delete notifications
- Notification preferences
"""

import streamlit as st
from notification_system import (
    get_user_notifications,
    get_unread_count,
    mark_as_read,
    mark_all_as_read,
    delete_notification,
    NotificationType
)


def render_notification_badge():
    """
    Render notification badge in sidebar
    Shows unread count
    """
    try:
        if 'user_email' not in st.session_state:
            return
        
        user_email = st.session_state.user_email
        unread_count = get_unread_count(user_email)
        
        if unread_count > 0:
            st.sidebar.markdown(f"""
            <div style="background: #dc3545; color: white; border-radius: 50%; 
                        width: 30px; height: 30px; display: flex; align-items: center; 
                        justify-content: center; font-weight: bold; margin: 10px auto;">
                {unread_count}
            </div>
            <p style="text-align: center; font-size: 12px; margin-top: -5px;">
            🔔 Notifications
            </p>
            """, unsafe_allow_html=True)
            
            # Show button to open notification center
            if st.sidebar.button("📬 View Notifications", use_container_width=True, key="view_notifications_btn"):
                st.session_state['show_notifications'] = True
                st.rerun()
    
    except Exception as e:
        print(f"Error rendering notification badge: {e}")


def render_notification_center():
    """
    Render full notification center
    """
    st.header("🔔 Notification Center")
    
    if 'user_email' not in st.session_state:
        st.warning("Please login to view notifications")
        return
    
    user_email = st.session_state.user_email
    
    # Actions
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### Your Notifications")
    with col2:
        if st.button("✅ Mark All Read", key="mark_all_read_btn"):
            mark_all_as_read(user_email)
            st.success("All notifications marked as read")
            st.rerun()
    with col3:
        show_read = st.checkbox("Show Read", value=False, key="show_read_notifs")
    
    # Get notifications
    all_notifs = get_user_notifications(user_email, unread_only=not show_read)
    
    if not all_notifs:
        st.info("📭 No notifications to show")
        return
    
    # Display notifications
    for notif in all_notifs:
        render_notification_card(notif)


def render_notification_card(notification):
    """Render single notification card"""
    
    # Icon based on type
    icons = {
        NotificationType.INFO: "ℹ️",
        NotificationType.SUCCESS: "✅",
        NotificationType.WARNING: "⚠️",
        NotificationType.URGENT: "🚨",
        NotificationType.MESSAGE: "💬",
        NotificationType.APPROVAL: "🔔",
        NotificationType.SYSTEM: "⚙️"
    }
    icon = icons.get(notification.type, "📬")
    
    # Color based on priority
    colors = {
        1: "#17a2b8",  # Low - blue
        2: "#28a745",  # Medium - green
        3: "#ffc107",  # High - orange
        4: "#dc3545"   # Urgent - red
    }
    color = colors.get(notification.priority, "#6c757d")
    
    # Background if unread
    bg_color = "#f8f9fa" if not notification.read else "white"
    
    with st.container():
        st.markdown(f"""
        <div style="border-left: 4px solid {color}; padding: 15px; 
                    background: {bg_color}; margin: 10px 0; border-radius: 5px;">
            <p style="margin: 0; font-weight: bold; font-size: 16px;">
                {icon} {notification.title}
            </p>
            <p style="margin: 5px 0; color: #666;">
                {notification.message}
            </p>
            <p style="margin: 5px 0; font-size: 12px; color: #999;">
                {notification.created_at[:19].replace('T', ' ')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if notification.action_url:
                if st.button(notification.action_label, key=f"action_{notification.id}"):
                    # Navigate to action URL
                    st.session_state['navigation_target'] = notification.action_url
                    mark_as_read(notification.id)
                    st.rerun()
        
        with col2:
            if not notification.read:
                if st.button("✓ Mark Read", key=f"read_{notification.id}"):
                    mark_as_read(notification.id)
                    st.rerun()
        
        with col3:
            if st.button("🗑️ Delete", key=f"del_{notification.id}"):
                delete_notification(notification.id)
                st.rerun()


def show_popup_notification(notification):
    """
    Show pop-up notification using Streamlit toast/success/warning/error
    For urgent/high priority notifications
    """
    if notification.priority >= 3:  # High or Urgent
        if notification.type == NotificationType.URGENT:
            st.error(f"🚨 {notification.title}: {notification.message}")
        elif notification.type == NotificationType.WARNING:
            st.warning(f"⚠️ {notification.title}: {notification.message}")
        elif notification.type == NotificationType.SUCCESS:
            st.success(f"✅ {notification.title}: {notification.message}")
        else:
            st.info(f"🔔 {notification.title}: {notification.message}")


def check_and_show_new_notifications():
    """
    Check for new unread notifications and show pop-ups
    Call this on every page load
    """
    try:
        if 'user_email' not in st.session_state:
            return
        
        if 'last_notification_check' not in st.session_state:
            st.session_state['last_notification_check'] = []
        
        user_email = st.session_state.user_email
        unread_notifs = get_user_notifications(user_email, unread_only=True)
        
        # Show pop-ups for new notifications (not shown before)
        for notif in unread_notifs:
            if notif.id not in st.session_state['last_notification_check']:
                if notif.priority >= 3:  # High or urgent
                    show_popup_notification(notif)
                
                st.session_state['last_notification_check'].append(notif.id)
        
        # Keep only last 50 IDs
        st.session_state['last_notification_check'] = st.session_state['last_notification_check'][-50:]
    
    except Exception as e:
        print(f"Error checking notifications: {e}")


# Export
__all__ = [
    'render_notification_badge',
    'render_notification_center',
    'check_and_show_new_notifications'
]
