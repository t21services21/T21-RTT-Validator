"""
ACCOUNT SECURITY UI - User-Facing Security Dashboard
Allows users to manage devices, view login history, security settings
"""

import streamlit as st
from datetime import datetime
from account_security_system import (
    get_user_security_info,
    remove_device,
    end_all_sessions,
    get_device_fingerprint,
    SECURITY_CONFIG
)


def render_security_dashboard(email: str):
    """Render complete security dashboard for user"""
    
    st.title("🔒 Account Security")
    
    # Get security info
    security_info = get_user_security_info(email)
    
    # Security overview
    st.markdown("## 📊 Security Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Registered Devices",
            f"{len(security_info['devices'])}/{SECURITY_CONFIG['max_devices']}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Active Sessions",
            f"{security_info['active_sessions']}/{SECURITY_CONFIG['max_concurrent_sessions']}",
            delta=None
        )
    
    with col3:
        suspicious_count = len(security_info['suspicious_activity'])
        st.metric(
            "Security Alerts",
            suspicious_count,
            delta=None
        )
    
    with col4:
        st.metric(
            "2FA Status",
            "✅ Enabled" if st.session_state.get('2fa_verified', False) else "❌ Disabled",
            delta=None
        )
    
    # Show suspicious activity alerts
    if security_info['suspicious_activity']:
        st.markdown("---")
        st.markdown("### ⚠️ Security Alerts")
        for activity in security_info['suspicious_activity']:
            if activity['severity'] == 'high':
                st.error(f"🚨 **{activity['message']}**")
            elif activity['severity'] == 'medium':
                st.warning(f"⚠️ **{activity['message']}**")
            else:
                st.info(f"ℹ️ **{activity['message']}**")
            
            if activity.get('details'):
                with st.expander("View Details"):
                    st.write(activity['details'])
    
    st.markdown("---")
    
    # Tabs for different security sections
    tabs = st.tabs([
        "🖥️ Devices",
        "📝 Login History",
        "⚙️ Settings",
        "🛡️ Advanced"
    ])
    
    with tabs[0]:
        render_devices_section(email, security_info)
    
    with tabs[1]:
        render_login_history(email, security_info)
    
    with tabs[2]:
        render_security_settings(email)
    
    with tabs[3]:
        render_advanced_security(email, security_info)


def render_devices_section(email: str, security_info: dict):
    """Render registered devices management"""
    
    st.markdown("### 🖥️ Registered Devices")
    
    st.info(f"""
    **Device Limit:** {len(security_info['devices'])}/{SECURITY_CONFIG['max_devices']} devices registered
    
    You can register up to {SECURITY_CONFIG['max_devices']} devices. Each device is identified by its unique characteristics (browser, system, etc.).
    
    **Why limit devices?** This prevents account sharing and keeps your account secure.
    """)
    
    if not security_info['devices']:
        st.warning("No devices registered yet. Your current device will be registered automatically.")
        return
    
    # Current device fingerprint
    current_device = get_device_fingerprint()
    
    st.markdown("---")
    
    for idx, device in enumerate(security_info['devices']):
        is_current = device['fingerprint'] == current_device
        
        # Device card
        with st.container():
            if is_current:
                st.markdown(f"""
                <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background-color: #e8f5e9; margin-bottom: 15px;">
                    <h4>🟢 {device['name']} (Current Device)</h4>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h4>🖥️ {device['name']}</h4>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Registered:** {datetime.fromisoformat(device['registered']).strftime('%B %d, %Y at %I:%M %p')}")
                st.write(f"**Last Used:** {datetime.fromisoformat(device['last_used']).strftime('%B %d, %Y at %I:%M %p')}")
                st.write(f"**Location:** {device.get('location', 'Unknown')}")
                st.write(f"**IP:** {device.get('ip', 'Unknown')}")
            
            with col2:
                if not is_current and len(security_info['devices']) > 1:
                    if st.button("🗑️ Remove", key=f"remove_device_{idx}"):
                        success, message = remove_device(email, device['fingerprint'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                elif is_current:
                    st.info("Current device cannot be removed")
    
    st.markdown("---")
    
    # Logout all sessions button
    if len(security_info['devices']) > 1 or security_info['active_sessions'] > 0:
        st.markdown("### 🚪 Security Actions")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🚪 Logout All Devices", type="secondary"):
                end_all_sessions(email)
                st.success("✅ All sessions terminated! Other devices will be logged out.")
                st.info("You'll remain logged in on this device.")
        
        with col_b:
            if st.button("🔄 Refresh Device List"):
                st.rerun()


def render_login_history(email: str, security_info: dict):
    """Render login history"""
    
    st.markdown("### 📝 Recent Login Activity")
    
    st.info("Monitor your account access to detect unauthorized logins.")
    
    if not security_info['login_history']:
        st.warning("No login history available yet.")
        return
    
    # Display login history (most recent first)
    for idx, login in enumerate(reversed(security_info['login_history'])):
        timestamp = datetime.fromisoformat(login['timestamp'])
        
        # Check if recent (last 24 hours)
        is_recent = (datetime.now() - timestamp).total_seconds() < 86400
        
        with st.container():
            if is_recent:
                st.markdown(f"""
                <div style="border-left: 4px solid #4CAF50; padding: 10px; margin-bottom: 10px; background-color: #f1f8f4;">
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="border-left: 4px solid #ccc; padding: 10px; margin-bottom: 10px;">
                """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**📅 {timestamp.strftime('%B %d, %Y')}**")
                st.write(f"🕐 {timestamp.strftime('%I:%M %p')}")
            
            with col2:
                st.write(f"**Location:** {login.get('location', 'Unknown')}")
                st.write(f"**IP:** {login.get('ip', 'Unknown')}")
            
            with col3:
                if login.get('success', True):
                    st.success("✅ Success")
                else:
                    st.error("❌ Failed")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"Showing last {len(security_info['login_history'])} logins")


def render_security_settings(email: str):
    """Render security settings"""
    
    st.markdown("### ⚙️ Security Settings")
    
    # Session timeout
    st.markdown("#### ⏱️ Session Timeout")
    st.info(f"""
    **Current Setting:** {SECURITY_CONFIG['session_timeout_minutes']} minutes
    
    You'll be automatically logged out after {SECURITY_CONFIG['session_timeout_minutes']} minutes of inactivity.
    This protects your account if you forget to log out.
    """)
    
    # 2FA
    st.markdown("#### 🔐 Two-Factor Authentication (2FA)")
    
    is_2fa_enabled = st.session_state.get('2fa_verified', False)
    
    if is_2fa_enabled:
        st.success("✅ **2FA is ENABLED** - Your account has extra protection!")
        st.write("You're required to verify your identity with a code sent to your email for sensitive actions.")
        
        if st.button("❌ Disable 2FA (Not Recommended)"):
            st.session_state['2fa_verified'] = False
            st.warning("2FA has been disabled. Your account is less secure.")
            st.rerun()
    else:
        st.warning("❌ **2FA is DISABLED** - Your account is at risk!")
        st.write("Enable 2FA for extra security. You'll receive a verification code by email for important actions.")
        
        if st.button("✅ Enable 2FA (Recommended)", type="primary"):
            st.session_state['2fa_verified'] = True
            st.success("2FA has been enabled! You'll be asked to verify important actions.")
            st.rerun()
    
    # Email notifications
    st.markdown("#### 📧 Email Notifications")
    
    notify_new_device = st.checkbox(
        "Notify me when a new device is registered",
        value=True,
        help="Get an email alert when your account is accessed from a new device"
    )
    
    notify_new_location = st.checkbox(
        "Notify me when logging in from a new location",
        value=True,
        help="Get an email alert when your account is accessed from a different location"
    )
    
    notify_failed_login = st.checkbox(
        "Notify me about failed login attempts",
        value=True,
        help="Get an email alert when someone tries to access your account with wrong password"
    )
    
    if st.button("💾 Save Notification Settings"):
        st.success("✅ Notification settings saved!")


def render_advanced_security(email: str, security_info: dict):
    """Render advanced security features"""
    
    st.markdown("### 🛡️ Advanced Security")
    
    # Security score
    st.markdown("#### 🎯 Security Score")
    
    score = calculate_security_score(security_info)
    
    if score >= 80:
        st.success(f"**Excellent!** Your security score is {score}/100")
    elif score >= 60:
        st.warning(f"**Good** - Your security score is {score}/100")
    else:
        st.error(f"**Needs Improvement** - Your security score is {score}/100")
    
    # Progress bar
    st.progress(score / 100)
    
    # Recommendations
    st.markdown("#### 💡 Recommendations")
    
    recommendations = []
    
    if not st.session_state.get('2fa_verified', False):
        recommendations.append("🔐 Enable Two-Factor Authentication (2FA)")
    
    if len(security_info['devices']) >= SECURITY_CONFIG['max_devices']:
        recommendations.append("🖥️ Remove old/unused devices")
    
    if security_info['suspicious_activity']:
        recommendations.append("⚠️ Review suspicious activity alerts")
    
    if not recommendations:
        st.success("✅ No security recommendations - You're all set!")
    else:
        for rec in recommendations:
            st.info(f"• {rec}")
    
    # Concurrent session info
    st.markdown("#### 📱 Concurrent Sessions")
    st.info(f"""
    **Session Limit:** Maximum {SECURITY_CONFIG['max_concurrent_sessions']} active session at a time
    
    **Why?** This prevents account sharing. If you try to log in while already logged in elsewhere, 
    you'll need to log out from the other device first.
    
    **Current:** {security_info['active_sessions']} active session(s)
    """)
    
    # Device limit info
    st.markdown("#### 🖥️ Device Management")
    st.info(f"""
    **Device Limit:** Maximum {SECURITY_CONFIG['max_devices']} registered devices
    
    **Why?** Limits how many different devices can access your account. Prevents widespread sharing.
    
    **Current:** {len(security_info['devices'])} device(s) registered
    """)
    
    # Data & Privacy
    st.markdown("#### 🔒 Data & Privacy")
    
    with st.expander("What data do we collect?"):
        st.markdown("""
        **For Security Purposes, We Track:**
        - Device fingerprints (browser type, screen size, etc.)
        - IP addresses (approximate location)
        - Login timestamps
        - Session activity
        
        **We DO NOT Track:**
        - Your exact physical location
        - Browsing history outside this platform
        - Personal files or data
        - Any sensitive personal information
        
        **Why?** This data helps us:
        - Detect unauthorized access
        - Prevent account sharing
        - Protect your certification integrity
        - Maintain platform security
        """)
    
    with st.expander("How long do we keep this data?"):
        st.markdown("""
        **Login History:** Last 20 logins (typically 1-3 months)
        **Device Data:** Until you remove the device or account is deleted
        **Security Events:** Last 100 events
        
        All security data is encrypted and stored securely.
        """)


def calculate_security_score(security_info: dict) -> int:
    """Calculate security score based on user's security settings"""
    score = 0
    
    # 2FA enabled (+30 points)
    if st.session_state.get('2fa_verified', False):
        score += 30
    
    # Not at device limit (+20 points)
    if len(security_info['devices']) < SECURITY_CONFIG['max_devices']:
        score += 20
    
    # No suspicious activity (+20 points)
    if not security_info['suspicious_activity']:
        score += 20
    
    # Active sessions within limit (+15 points)
    if security_info['active_sessions'] <= SECURITY_CONFIG['max_concurrent_sessions']:
        score += 15
    
    # Has login history (account being used) (+15 points)
    if len(security_info['login_history']) > 0:
        score += 15
    
    return score


def render_security_banner():
    """Render security warning banner if issues detected"""
    
    if not st.session_state.get('logged_in', False):
        return
    
    email = st.session_state.get('user_email')
    if not email:
        return
    
    # Check for security issues
    security_info = get_user_security_info(email)
    
    # Check for high-severity issues
    high_severity = [a for a in security_info['suspicious_activity'] if a['severity'] == 'high']
    
    if high_severity:
        st.error(f"""
        🚨 **Security Alert!** {len(high_severity)} security issue(s) detected.
        [View Security Dashboard](#) to review and take action.
        """)
    
    # Check if 2FA required but not enabled
    user_tier = st.session_state.get('user_type', 'trial')
    if user_tier in SECURITY_CONFIG['require_2fa_for_tiers']:
        if not st.session_state.get('2fa_verified', False):
            st.warning("""
            ⚠️ **Two-Factor Authentication Required!**
            Your account tier requires 2FA for enhanced security. 
            [Enable 2FA now](#) in Security Settings.
            """)


# Export main function
__all__ = ['render_security_dashboard', 'render_security_banner']
