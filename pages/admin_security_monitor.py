"""
ADMIN SECURITY MONITORING DASHBOARD
View all users' security data, detect fraud, manage threats

Admin/Staff Only - Complete visibility into platform security

Features:
- All users overview
- High-risk accounts
- Active sessions monitoring
- Location tracking
- Device analytics
- Fraud detection
- Account sharing detection
- Real-time alerts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="Admin Security Monitor", page_icon="🛡️", layout="wide")

# Check if user is admin/staff
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access the Admin Security Monitor")
    st.stop()

user_email = st.session_state.user_email
user_role = st.session_state.get('user_license', {})
if hasattr(user_role, 'role'):
    user_role = user_role.role
elif hasattr(user_role, 'user_type'):
    user_role = user_role.user_type
else:
    user_role = 'student'

# Check if admin or staff
is_admin = user_role in ['super_admin', 'admin', 'staff', 'tester'] or 'admin@t21services' in user_email.lower()

if not is_admin:
    st.error("🚫 Access Denied - Admin/Staff Only")
    st.info("This page is restricted to administrators and staff members.")
    st.stop()

# Header
st.title("🛡️ Admin Security Monitoring Dashboard")
st.markdown(f"**Admin:** {user_email}")
st.markdown(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

st.divider()

# ============================================
# LOAD ALL USERS' SECURITY DATA
# ============================================

@st.cache_data(ttl=60)  # Cache for 1 minute
def load_all_security_data():
    """Load security data for all users"""
    try:
        from account_security_system import load_security_db
        db = load_security_db()
        return db
    except:
        return {}

security_db = load_all_security_data()

if not security_db:
    st.warning("No security data available yet.")
    st.stop()

# ============================================
# PLATFORM-WIDE METRICS
# ============================================

st.header("📊 Platform Security Overview")

# Calculate metrics
total_users = len(security_db)
total_sessions = sum(len(user_data.get('sessions', [])) for user_data in security_db.values())
total_devices = sum(len(user_data.get('devices', [])) for user_data in security_db.values())

# Calculate high-risk accounts
high_risk_accounts = 0
for email, user_data in security_db.items():
    try:
        from advanced_security_tracking import AnomalyDetector
        risk_score, _ = AnomalyDetector.calculate_risk_score(email, {})
        if risk_score > 60:
            high_risk_accounts += 1
    except:
        pass

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Total Users",
        value=total_users,
        delta=f"{total_sessions} active sessions"
    )

with col2:
    st.metric(
        label="🚨 High-Risk Accounts",
        value=high_risk_accounts,
        delta=f"{round(high_risk_accounts/total_users*100, 1)}% of users" if total_users > 0 else "0%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="💻 Total Devices",
        value=total_devices,
        delta=f"{round(total_devices/total_users, 1)} per user" if total_users > 0 else "0"
    )

with col4:
    # Count users with multiple recent locations
    suspicious_users = 0
    for user_data in security_db.values():
        recent_logins = user_data.get('login_history', [])[-10:]
        locations = set([l.get('location', 'Unknown') for l in recent_logins])
        if len(locations) > 3:
            suspicious_users += 1
    
    st.metric(
        label="⚠️ Suspicious Activity",
        value=suspicious_users,
        delta=f"{round(suspicious_users/total_users*100, 1)}% of users" if total_users > 0 else "0%",
        delta_color="inverse"
    )

st.divider()

# ============================================
# HIGH-RISK ACCOUNTS
# ============================================

st.header("🚨 High-Risk Accounts")

high_risk_data = []

for email, user_data in security_db.items():
    try:
        from advanced_security_tracking import AnomalyDetector
        risk_score, risk_reasons = AnomalyDetector.calculate_risk_score(email, {})
        
        if risk_score > 30:  # Show medium and high risk
            recent_logins = user_data.get('login_history', [])
            last_login = recent_logins[0] if recent_logins else {}
            
            high_risk_data.append({
                'Email': email,
                'Risk Score': risk_score,
                'Risk Level': '🔴 High' if risk_score > 60 else '🟡 Medium',
                'Last Login': last_login.get('timestamp', 'Never')[:19].replace('T', ' '),
                'Last IP': last_login.get('ip', 'Unknown'),
                'Last Location': last_login.get('location', 'Unknown'),
                'Active Sessions': len(user_data.get('sessions', [])),
                'Risk Reasons': ', '.join(risk_reasons) if risk_reasons else 'None'
            })
    except:
        pass

if high_risk_data:
    df_risk = pd.DataFrame(high_risk_data)
    df_risk = df_risk.sort_values('Risk Score', ascending=False)
    
    st.dataframe(
        df_risk,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Risk Score': st.column_config.ProgressColumn(
                'Risk Score',
                min_value=0,
                max_value=100,
                format='%d'
            )
        }
    )
    
    # Download button
    csv = df_risk.to_csv(index=False)
    st.download_button(
        label="📥 Download High-Risk Accounts (CSV)",
        data=csv,
        file_name=f"high_risk_accounts_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.success("✅ No high-risk accounts detected!")

st.divider()

# ============================================
# ALL USERS TABLE
# ============================================

st.header("👥 All Users Security Status")

# Search and filter
col_search, col_filter = st.columns([3, 1])

with col_search:
    search_term = st.text_input("🔍 Search by email", placeholder="Enter email address...")

with col_filter:
    risk_filter = st.selectbox(
        "Filter by Risk",
        ["All", "High Risk (60+)", "Medium Risk (30-60)", "Low Risk (0-30)"]
    )

# Build users table
users_data = []

for email, user_data in security_db.items():
    # Apply search filter
    if search_term and search_term.lower() not in email.lower():
        continue
    
    try:
        from advanced_security_tracking import AnomalyDetector
        risk_score, risk_reasons = AnomalyDetector.calculate_risk_score(email, {})
    except:
        risk_score = 0
        risk_reasons = []
    
    # Apply risk filter
    if risk_filter == "High Risk (60+)" and risk_score < 60:
        continue
    elif risk_filter == "Medium Risk (30-60)" and (risk_score < 30 or risk_score >= 60):
        continue
    elif risk_filter == "Low Risk (0-30)" and risk_score >= 30:
        continue
    
    recent_logins = user_data.get('login_history', [])
    last_login = recent_logins[0] if recent_logins else {}
    
    # Get unique locations and IPs
    unique_locations = len(set([l.get('location', 'Unknown') for l in recent_logins[-20:]]))
    unique_ips = len(set([l.get('ip', 'Unknown') for l in recent_logins[-20:]]))
    
    users_data.append({
        'Email': email,
        'Risk': risk_score,
        'Status': '🔴' if risk_score > 60 else '🟡' if risk_score > 30 else '🟢',
        'Sessions': len(user_data.get('sessions', [])),
        'Devices': len(user_data.get('devices', [])),
        'Locations': unique_locations,
        'IPs': unique_ips,
        'Last Login': last_login.get('timestamp', 'Never')[:19].replace('T', ' '),
        'Last IP': last_login.get('ip', 'Unknown'),
        'Last Location': last_login.get('location', 'Unknown')
    })

if users_data:
    df_users = pd.DataFrame(users_data)
    df_users = df_users.sort_values('Risk', ascending=False)
    
    st.dataframe(
        df_users,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Risk': st.column_config.ProgressColumn(
                'Risk Score',
                min_value=0,
                max_value=100,
                format='%d'
            )
        }
    )
    
    st.caption(f"Showing {len(users_data)} of {total_users} users")
else:
    st.info("No users match the current filters")

st.divider()

# ============================================
# ACTIVE SESSIONS MAP
# ============================================

st.header("🗺️ Active Sessions - Global View")

try:
    # Collect all active session locations
    session_locations = []
    
    for email, user_data in security_db.items():
        sessions = user_data.get('sessions', [])
        for session in sessions:
            geo = session.get('geolocation', {})
            if isinstance(geo, dict) and geo.get('latitude') and geo.get('longitude'):
                session_locations.append({
                    'lat': geo.get('latitude'),
                    'lon': geo.get('longitude'),
                    'email': email,
                    'city': geo.get('city', 'Unknown'),
                    'country': geo.get('country', 'Unknown'),
                    'ip': session.get('ip', 'Unknown'),
                    'device': session.get('device_type', 'Unknown')
                })
    
    if session_locations:
        df_map = pd.DataFrame(session_locations)
        
        fig_map = px.scatter_mapbox(
            df_map,
            lat='lat',
            lon='lon',
            hover_name='email',
            hover_data={'city': True, 'country': True, 'ip': True, 'device': True, 'lat': False, 'lon': False},
            zoom=1,
            height=500,
            color_discrete_sequence=['red']
        )
        
        fig_map.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption(f"📍 {len(session_locations)} active sessions worldwide")
    else:
        st.info("No active sessions with location data")
except Exception as e:
    st.warning(f"Unable to display map: {str(e)}")

st.divider()

# ============================================
# PLATFORM ANALYTICS
# ============================================

st.header("📈 Platform Security Analytics")

col_an1, col_an2, col_an3 = st.columns(3)

# Device types across all users
all_devices = {}
all_browsers = {}
all_os = {}

for user_data in security_db.values():
    for login in user_data.get('login_history', [])[-10:]:
        device = login.get('device_type', 'Unknown')
        browser = login.get('browser', 'Unknown')
        os = login.get('os', 'Unknown')
        
        all_devices[device] = all_devices.get(device, 0) + 1
        all_browsers[browser] = all_browsers.get(browser, 0) + 1
        all_os[os] = all_os.get(os, 0) + 1

with col_an1:
    st.subheader("Device Types")
    if all_devices:
        fig_devices = px.pie(
            values=list(all_devices.values()),
            names=list(all_devices.keys()),
            hole=0.4
        )
        fig_devices.update_layout(height=300)
        st.plotly_chart(fig_devices, use_container_width=True)

with col_an2:
    st.subheader("Browsers")
    if all_browsers:
        fig_browsers = px.pie(
            values=list(all_browsers.values()),
            names=list(all_browsers.keys()),
            hole=0.4
        )
        fig_browsers.update_layout(height=300)
        st.plotly_chart(fig_browsers, use_container_width=True)

with col_an3:
    st.subheader("Operating Systems")
    if all_os:
        fig_os = px.pie(
            values=list(all_os.values()),
            names=list(all_os.keys()),
            hole=0.4
        )
        fig_os.update_layout(height=300)
        st.plotly_chart(fig_os, use_container_width=True)

st.divider()

# ============================================
# ACCOUNT SHARING DETECTION
# ============================================

st.header("🚨 Account Sharing Detection")

sharing_suspects = []

for email, user_data in security_db.items():
    recent_logins = user_data.get('login_history', [])[-20:]
    
    if len(recent_logins) < 5:
        continue
    
    # Check for multiple simultaneous locations
    unique_ips = set([l.get('ip', 'Unknown') for l in recent_logins])
    unique_locations = set([l.get('location', 'Unknown') for l in recent_logins])
    unique_devices = set([l.get('device_fingerprint', 'Unknown') for l in recent_logins])
    
    # Suspicious if multiple IPs/locations/devices in short time
    if len(unique_ips) > 3 or len(unique_locations) > 3 or len(unique_devices) > 2:
        sharing_suspects.append({
            'Email': email,
            'Unique IPs': len(unique_ips),
            'Unique Locations': len(unique_locations),
            'Unique Devices': len(unique_devices),
            'Recent Logins': len(recent_logins),
            'Suspicion Level': '🔴 High' if (len(unique_ips) > 5 or len(unique_devices) > 3) else '🟡 Medium',
            'Action': 'Investigate'
        })

if sharing_suspects:
    df_sharing = pd.DataFrame(sharing_suspects)
    df_sharing = df_sharing.sort_values('Unique IPs', ascending=False)
    
    st.warning(f"⚠️ {len(sharing_suspects)} accounts showing signs of sharing")
    st.dataframe(df_sharing, use_container_width=True, hide_index=True)
    
    # Download button
    csv_sharing = df_sharing.to_csv(index=False)
    st.download_button(
        label="📥 Download Sharing Suspects (CSV)",
        data=csv_sharing,
        file_name=f"account_sharing_suspects_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.success("✅ No account sharing detected!")

st.divider()

# ============================================
# RECENT SECURITY EVENTS
# ============================================

st.header("📋 Recent Security Events")

# Collect all recent security events
all_events = []

for email, user_data in security_db.items():
    for login in user_data.get('login_history', [])[-5:]:
        event_type = "Login"
        if login.get('action'):
            if 'FORCED_LOGOUT' in login.get('action', ''):
                event_type = "🚨 Forced Logout"
            elif 'FAILED' in login.get('action', ''):
                event_type = "❌ Failed Login"
        
        all_events.append({
            'Timestamp': login.get('timestamp', 'Unknown')[:19].replace('T', ' '),
            'User': email,
            'Event': event_type,
            'IP': login.get('ip', 'Unknown'),
            'Location': login.get('location', 'Unknown'),
            'Device': login.get('device_type', 'Unknown'),
            'Risk': login.get('action', 'Normal')
        })

if all_events:
    df_events = pd.DataFrame(all_events)
    # Sort by timestamp descending
    df_events = df_events.sort_values('Timestamp', ascending=False)
    
    st.dataframe(df_events.head(50), use_container_width=True, hide_index=True)
    st.caption(f"Showing last 50 of {len(all_events)} events")
else:
    st.info("No recent security events")

st.divider()

# ============================================
# ADMIN ACTIONS
# ============================================

st.header("🛡️ Admin Security Actions")

col_action1, col_action2, col_action3, col_action4 = st.columns(4)

with col_action1:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with col_action2:
    if st.button("📊 Export Full Report", use_container_width=True):
        # Create comprehensive report
        report_data = []
        for email, user_data in security_db.items():
            try:
                from advanced_security_tracking import AnomalyDetector
                risk_score, risk_reasons = AnomalyDetector.calculate_risk_score(email, {})
            except:
                risk_score = 0
                risk_reasons = []
            
            report_data.append({
                'Email': email,
                'Risk Score': risk_score,
                'Active Sessions': len(user_data.get('sessions', [])),
                'Total Devices': len(user_data.get('devices', [])),
                'Total Logins': len(user_data.get('login_history', [])),
                'Risk Reasons': ', '.join(risk_reasons) if risk_reasons else 'None'
            })
        
        df_report = pd.DataFrame(report_data)
        csv_report = df_report.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Complete Security Report",
            data=csv_report,
            file_name=f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col_action3:
    if st.button("🚫 View Blocked Users", use_container_width=True):
        st.info("Blocked users feature coming soon!")

with col_action4:
    if st.button("📧 Send Security Alert", use_container_width=True):
        st.info("Email alert feature coming soon!")

# Footer
st.markdown("---")
st.caption("🛡️ T21 Services UK - Admin Security Monitoring Dashboard")
st.caption(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
st.caption(f"Monitoring {total_users} users | {total_sessions} active sessions | {high_risk_accounts} high-risk accounts")
