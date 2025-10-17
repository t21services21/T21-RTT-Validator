"""
ADMIN SECURITY MONITORING DASHBOARD
Allows staff/admin to monitor security across ALL users
Detect account sharing, suspicious patterns, etc.
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
from account_security_system import load_security_db, SECURITY_CONFIG


def render_admin_security_dashboard():
    """Main admin security monitoring dashboard"""
    
    st.title("🛡️ Security Monitoring Dashboard")
    st.caption("Admin Tool - Monitor platform-wide security")
    
    # Load all security data
    security_db = load_security_db()
    
    if not security_db:
        st.warning("No security data available yet.")
        return
    
    # Overview metrics
    render_security_overview(security_db)
    
    st.markdown("---")
    
    # Tabs for different views
    tabs = st.tabs([
        "🚨 Suspicious Accounts",
        "📊 Platform Statistics",
        "👥 User Details",
        "📈 Trends"
    ])
    
    with tabs[0]:
        render_suspicious_accounts(security_db)
    
    with tabs[1]:
        render_platform_statistics(security_db)
    
    with tabs[2]:
        render_user_search(security_db)
    
    with tabs[3]:
        render_security_trends(security_db)


def render_security_overview(security_db: dict):
    """Render high-level security overview"""
    
    st.markdown("## 📊 Platform Security Overview")
    
    # Calculate metrics
    total_users = len(security_db)
    total_devices = sum(len(user_data.get('devices', [])) for user_data in security_db.values())
    active_sessions = sum(count_active_sessions(user_data) for user_data in security_db.values())
    
    # Detect potential account sharing
    sharing_suspects = detect_account_sharing_patterns(security_db)
    
    # Count users at device limit
    at_device_limit = sum(1 for user_data in security_db.values() 
                          if len(user_data.get('devices', [])) >= SECURITY_CONFIG['max_devices'])
    
    # Display metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Users", total_users)
    
    with col2:
        st.metric("Total Devices", total_devices)
    
    with col3:
        st.metric("Active Sessions", active_sessions)
    
    with col4:
        st.metric(
            "Sharing Suspects",
            len(sharing_suspects),
            delta=None,
            help="Accounts with suspicious activity patterns"
        )
        if len(sharing_suspects) > 0:
            st.caption("⚠️ Needs review")
    
    with col5:
        st.metric(
            "At Device Limit",
            at_device_limit,
            delta=None,
            help=f"Users with {SECURITY_CONFIG['max_devices']}/{SECURITY_CONFIG['max_devices']} devices"
        )


def count_active_sessions(user_data: dict) -> int:
    """Count active sessions for a user"""
    current_time = datetime.now()
    timeout_minutes = SECURITY_CONFIG['session_timeout_minutes']
    
    active = 0
    for session in user_data.get('sessions', []):
        try:
            session_time = datetime.fromisoformat(session['last_activity'])
            if current_time - session_time < timedelta(minutes=timeout_minutes):
                active += 1
        except:
            pass
    
    return active


def detect_account_sharing_patterns(security_db: dict) -> List[Dict]:
    """
    Detect potential account sharing across all users
    Returns list of suspicious accounts with reasons
    """
    suspects = []
    
    for email, user_data in security_db.items():
        suspicion_reasons = []
        risk_score = 0
        
        # Pattern 1: Max devices registered (risk +3)
        if len(user_data.get('devices', [])) >= SECURITY_CONFIG['max_devices']:
            suspicion_reasons.append(f"At device limit ({len(user_data.get('devices', []))}/{SECURITY_CONFIG['max_devices']})")
            risk_score += 3
        
        # Pattern 2: Multiple locations in short time (risk +5)
        recent_logins = user_data.get('login_history', [])[-5:]
        if len(recent_logins) >= 3:
            locations = set(login.get('location', 'unknown') for login in recent_logins)
            if len(locations) >= 3:
                suspicion_reasons.append(f"Multiple locations ({len(locations)} different locations)")
                risk_score += 5
        
        # Pattern 3: Concurrent session attempts (risk +4)
        concurrent_attempts = sum(1 for event in user_data.get('security_events', [])
                                 if event.get('type') == 'concurrent_session_blocked')
        if concurrent_attempts > 0:
            suspicion_reasons.append(f"Concurrent login attempts ({concurrent_attempts} blocked)")
            risk_score += 4
        
        # Pattern 4: Different IPs within 1 hour (risk +4)
        recent_hour_logins = []
        current_time = datetime.now()
        for login in user_data.get('login_history', [])[-10:]:
            try:
                login_time = datetime.fromisoformat(login['timestamp'])
                if current_time - login_time < timedelta(hours=1):
                    recent_hour_logins.append(login)
            except:
                pass
        
        if len(recent_hour_logins) >= 2:
            ips = set(login.get('ip', 'unknown') for login in recent_hour_logins)
            if len(ips) >= 2:
                suspicion_reasons.append(f"Multiple IPs in 1 hour ({len(ips)} different IPs)")
                risk_score += 4
        
        # Pattern 5: High login frequency (risk +2)
        if len(user_data.get('login_history', [])) > 50:
            suspicion_reasons.append(f"High login frequency ({len(user_data.get('login_history', []))} logins)")
            risk_score += 2
        
        # If any suspicious patterns found, add to suspects
        if suspicion_reasons:
            suspects.append({
                'email': email,
                'reasons': suspicion_reasons,
                'risk_score': risk_score,
                'severity': 'HIGH' if risk_score >= 10 else 'MEDIUM' if risk_score >= 5 else 'LOW',
                'devices': len(user_data.get('devices', [])),
                'active_sessions': count_active_sessions(user_data),
                'total_logins': len(user_data.get('login_history', []))
            })
    
    # Sort by risk score (highest first)
    suspects.sort(key=lambda x: x['risk_score'], reverse=True)
    
    return suspects


def render_suspicious_accounts(security_db: dict):
    """Render list of suspicious accounts"""
    
    st.markdown("### 🚨 Suspicious Activity Detection")
    
    st.info("""
    **Automated Detection** - Accounts flagged based on:
    - Multiple device registrations
    - Multiple locations in short time
    - Concurrent session attempts
    - Different IPs within 1 hour
    - High login frequency
    """)
    
    # Detect suspicious patterns
    suspects = detect_account_sharing_patterns(security_db)
    
    if not suspects:
        st.success("✅ No suspicious activity detected! All accounts appear normal.")
        return
    
    st.warning(f"⚠️ Found {len(suspects)} account(s) with suspicious activity patterns")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        severity_filter = st.selectbox(
            "Filter by Severity",
            ["All", "HIGH", "MEDIUM", "LOW"]
        )
    
    with col2:
        min_risk_score = st.slider(
            "Minimum Risk Score",
            0, 20, 0
        )
    
    # Apply filters
    filtered_suspects = suspects
    if severity_filter != "All":
        filtered_suspects = [s for s in filtered_suspects if s['severity'] == severity_filter]
    filtered_suspects = [s for s in filtered_suspects if s['risk_score'] >= min_risk_score]
    
    st.markdown(f"**Showing {len(filtered_suspects)} account(s)**")
    
    # Display suspects
    for suspect in filtered_suspects:
        render_suspect_card(suspect, security_db)


def render_suspect_card(suspect: dict, security_db: dict):
    """Render individual suspicious account card"""
    
    # Color based on severity
    if suspect['severity'] == 'HIGH':
        border_color = "#d32f2f"
        bg_color = "#ffebee"
    elif suspect['severity'] == 'MEDIUM':
        border_color = "#f57c00"
        bg_color = "#fff3e0"
    else:
        border_color = "#fbc02d"
        bg_color = "#fffde7"
    
    with st.container():
        st.markdown(f"""
        <div style="border-left: 5px solid {border_color}; background-color: {bg_color}; 
                    padding: 15px; margin-bottom: 15px; border-radius: 5px;">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"**👤 {suspect['email']}**")
            st.markdown(f"**Risk Score:** {suspect['risk_score']} | **Severity:** {suspect['severity']}")
        
        with col2:
            st.markdown(f"**Devices:** {suspect['devices']}/{SECURITY_CONFIG['max_devices']}")
            st.markdown(f"**Active Sessions:** {suspect['active_sessions']}")
            st.markdown(f"**Total Logins:** {suspect['total_logins']}")
        
        with col3:
            if st.button("🔍 View Details", key=f"view_{suspect['email']}"):
                st.session_state[f"viewing_{suspect['email']}"] = True
        
        # Show reasons
        st.markdown("**⚠️ Suspicious Patterns:**")
        for reason in suspect['reasons']:
            st.caption(f"• {reason}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Show detailed view if requested
        if st.session_state.get(f"viewing_{suspect['email']}", False):
            render_user_security_details(suspect['email'], security_db)
            
            if st.button("✖️ Close", key=f"close_{suspect['email']}"):
                st.session_state[f"viewing_{suspect['email']}"] = False
                st.rerun()


def render_user_security_details(email: str, security_db: dict):
    """Render detailed security info for specific user"""
    
    if email not in security_db:
        st.error("User not found")
        return
    
    user_data = security_db[email]
    
    with st.expander("📋 Detailed Security Information", expanded=True):
        
        # Devices
        st.markdown("#### 🖥️ Registered Devices")
        for device in user_data.get('devices', []):
            st.write(f"• **{device['name']}** - Last used: {device['last_used']} - Location: {device.get('location', 'Unknown')}")
        
        # Recent logins
        st.markdown("#### 📝 Recent Login History")
        for login in user_data.get('login_history', [])[-10:]:
            st.write(f"• {login['timestamp']} - {login.get('location', 'Unknown')} - IP: {login.get('ip', 'Unknown')}")
        
        # Security events
        if user_data.get('security_events'):
            st.markdown("#### 🚨 Security Events")
            for event in user_data.get('security_events', [])[-10:]:
                st.write(f"• **{event['type']}** - {event['timestamp']}")


def render_platform_statistics(security_db: dict):
    """Render platform-wide security statistics"""
    
    st.markdown("### 📊 Platform Security Statistics")
    
    # Calculate stats
    total_users = len(security_db)
    total_devices = sum(len(user_data.get('devices', [])) for user_data in security_db.values())
    total_logins = sum(len(user_data.get('login_history', [])) for user_data in security_db.values())
    
    avg_devices = total_devices / total_users if total_users > 0 else 0
    avg_logins = total_logins / total_users if total_users > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Users", total_users)
        st.metric("Total Devices", total_devices)
        st.metric("Total Logins (All Time)", total_logins)
    
    with col2:
        st.metric("Avg Devices/User", f"{avg_devices:.2f}")
        st.metric("Avg Logins/User", f"{avg_logins:.1f}")
        st.metric("Device Limit", SECURITY_CONFIG['max_devices'])
    
    # Device distribution
    st.markdown("#### 📱 Device Distribution")
    
    device_counts = {}
    for user_data in security_db.values():
        count = len(user_data.get('devices', []))
        device_counts[count] = device_counts.get(count, 0) + 1
    
    for i in range(SECURITY_CONFIG['max_devices'] + 1):
        count = device_counts.get(i, 0)
        percentage = (count / total_users * 100) if total_users > 0 else 0
        st.write(f"**{i} devices:** {count} users ({percentage:.1f}%)")
        st.progress(percentage / 100)


def render_user_search(security_db: dict):
    """Search and view specific user security info"""
    
    st.markdown("### 👥 User Security Lookup")
    
    # Search
    search_email = st.text_input("🔍 Search by Email", placeholder="student@example.com")
    
    if search_email:
        if search_email in security_db:
            st.success(f"✅ Found user: {search_email}")
            render_user_security_details(search_email, security_db)
        else:
            st.error("❌ User not found in security database")
    else:
        st.info("Enter an email address to view security details")


def render_security_trends(security_db: dict):
    """Show security trends over time"""
    
    st.markdown("### 📈 Security Trends")
    
    st.info("**Coming Soon:** Historical trend analysis, charts, and predictive analytics")
    
    # For now, show some basic trends
    st.markdown("#### Recent Activity")
    
    # Count logins in last 24 hours, 7 days, 30 days
    current_time = datetime.now()
    
    logins_24h = 0
    logins_7d = 0
    logins_30d = 0
    
    for user_data in security_db.values():
        for login in user_data.get('login_history', []):
            try:
                login_time = datetime.fromisoformat(login['timestamp'])
                time_diff = current_time - login_time
                
                if time_diff < timedelta(hours=24):
                    logins_24h += 1
                if time_diff < timedelta(days=7):
                    logins_7d += 1
                if time_diff < timedelta(days=30):
                    logins_30d += 1
            except:
                pass
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Logins (24 hours)", logins_24h)
    
    with col2:
        st.metric("Logins (7 days)", logins_7d)
    
    with col3:
        st.metric("Logins (30 days)", logins_30d)


# Export main function
__all__ = ['render_admin_security_dashboard']
