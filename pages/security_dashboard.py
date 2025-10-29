"""
REAL-TIME SECURITY DASHBOARD
Enterprise-grade security monitoring and analytics

Features:
- Live security metrics
- Risk score monitoring
- Device tracking
- Location analytics
- Anomaly detection alerts
- Session management
- Threat intelligence
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="Security Dashboard", page_icon="🔒", layout="wide")

# Check if user is logged in
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access the Security Dashboard")
    st.stop()

user_email = st.session_state.user_email

# Header
st.title("🔒 Security Dashboard")
st.markdown(f"**Account:** {user_email}")
st.markdown(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

st.divider()

# Get security data
try:
    from advanced_security_tracking import get_security_dashboard_data, get_user_ip_advanced, get_real_ip_geolocation
    security_data = get_security_dashboard_data(user_email)
    
    if not security_data:
        st.warning("No security data available yet. Data will appear after your first login.")
        st.stop()
    
except Exception as e:
    st.error(f"Error loading security data: {str(e)}")
    st.stop()

# ============================================
# KEY METRICS
# ============================================

st.header("📊 Security Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🔐 Total Logins",
        value=security_data.get('total_logins', 0),
        delta=f"{security_data.get('success_rate', 0)}% success rate"
    )

with col2:
    risk_score = security_data.get('risk_score', 0)
    risk_color = "🟢" if risk_score < 30 else "🟡" if risk_score < 60 else "🔴"
    st.metric(
        label=f"{risk_color} Risk Score",
        value=f"{risk_score}/100",
        delta="Low" if risk_score < 30 else "Medium" if risk_score < 60 else "High",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="🌍 Unique Locations",
        value=security_data.get('unique_locations', 0),
        delta=f"{security_data.get('unique_ips', 0)} IPs"
    )

with col4:
    st.metric(
        label="📅 Account Age",
        value=f"{security_data.get('account_age_days', 0)} days",
        delta=f"Last login: {security_data.get('last_login', 'Never')[:10]}"
    )

st.divider()

# ============================================
# RISK ANALYSIS
# ============================================

if security_data.get('risk_score', 0) > 0:
    st.header("⚠️ Risk Analysis")
    
    col_risk1, col_risk2 = st.columns([2, 1])
    
    with col_risk1:
        # Risk reasons
        st.subheader("Risk Factors Detected")
        risk_reasons = security_data.get('risk_reasons', [])
        
        if risk_reasons:
            for reason in risk_reasons:
                st.warning(f"⚠️ {reason}")
        else:
            st.success("✅ No risk factors detected")
    
    with col_risk2:
        # Risk score gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=security_data.get('risk_score', 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkred" if security_data.get('risk_score', 0) > 60 else "orange" if security_data.get('risk_score', 0) > 30 else "green"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 60], 'color': "lightyellow"},
                    {'range': [60, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig_gauge.update_layout(height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.divider()

# ============================================
# RECENT ACTIVITY
# ============================================

st.header("📋 Recent Login Activity")

recent_logins = security_data.get('recent_logins', [])

if recent_logins:
    # Create dataframe
    login_data = []
    for login in recent_logins:
        details = login.get('details', {})
        if isinstance(details, str):
            try:
                details = json.loads(details)
            except:
                details = {}
        
        login_data.append({
            'Timestamp': login.get('timestamp', 'Unknown')[:19].replace('T', ' '),
            'IP Address': login.get('ip_address', 'Unknown'),
            'Location': details.get('location', 'Unknown'),
            'Device': details.get('device_type', 'Unknown'),
            'Browser': details.get('browser', 'Unknown'),
            'OS': details.get('os', 'Unknown'),
            'Status': '✅ Success' if login.get('user_action') == 'LOGIN' else '❌ Failed'
        })
    
    df_logins = pd.DataFrame(login_data)
    st.dataframe(df_logins, use_container_width=True, hide_index=True)
    
    # Download button
    csv = df_logins.to_csv(index=False)
    st.download_button(
        label="📥 Download Login History (CSV)",
        data=csv,
        file_name=f"login_history_{user_email}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.info("No recent login activity to display")

st.divider()

# ============================================
# LOCATION MAP
# ============================================

st.header("🗺️ Login Locations")

try:
    # Extract location data
    locations = []
    for login in recent_logins:
        details = login.get('details', {})
        if isinstance(details, str):
            try:
                details = json.loads(details)
            except:
                details = {}
        
        geo = details.get('geolocation', {})
        if isinstance(geo, dict) and geo.get('latitude') and geo.get('longitude'):
            locations.append({
                'lat': geo.get('latitude'),
                'lon': geo.get('longitude'),
                'city': geo.get('city', 'Unknown'),
                'country': geo.get('country', 'Unknown'),
                'timestamp': login.get('timestamp', 'Unknown')[:19]
            })
    
    if locations:
        df_map = pd.DataFrame(locations)
        
        # Create map
        fig_map = px.scatter_mapbox(
            df_map,
            lat='lat',
            lon='lon',
            hover_name='city',
            hover_data={'country': True, 'timestamp': True, 'lat': False, 'lon': False},
            zoom=2,
            height=400
        )
        
        fig_map.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No location data available for mapping")
except Exception as e:
    st.warning(f"Unable to display location map: {str(e)}")

st.divider()

# ============================================
# DEVICE ANALYTICS
# ============================================

st.header("💻 Device Analytics")

col_dev1, col_dev2, col_dev3 = st.columns(3)

# Count devices, browsers, OS
devices = {}
browsers = {}
oses = {}

for login in recent_logins:
    details = login.get('details', {})
    if isinstance(details, str):
        try:
            details = json.loads(details)
        except:
            details = {}
    
    device = details.get('device_type', 'Unknown')
    browser = details.get('browser', 'Unknown')
    os = details.get('os', 'Unknown')
    
    devices[device] = devices.get(device, 0) + 1
    browsers[browser] = browsers.get(browser, 0) + 1
    oses[os] = oses.get(os, 0) + 1

with col_dev1:
    st.subheader("Device Types")
    if devices:
        fig_devices = px.pie(
            values=list(devices.values()),
            names=list(devices.keys()),
            hole=0.4
        )
        fig_devices.update_layout(height=250, showlegend=True)
        st.plotly_chart(fig_devices, use_container_width=True)
    else:
        st.info("No device data")

with col_dev2:
    st.subheader("Browsers")
    if browsers:
        fig_browsers = px.pie(
            values=list(browsers.values()),
            names=list(browsers.keys()),
            hole=0.4
        )
        fig_browsers.update_layout(height=250, showlegend=True)
        st.plotly_chart(fig_browsers, use_container_width=True)
    else:
        st.info("No browser data")

with col_dev3:
    st.subheader("Operating Systems")
    if oses:
        fig_os = px.pie(
            values=list(oses.values()),
            names=list(oses.keys()),
            hole=0.4
        )
        fig_os.update_layout(height=250, showlegend=True)
        st.plotly_chart(fig_os, use_container_width=True)
    else:
        st.info("No OS data")

st.divider()

# ============================================
# ACTIVE SESSIONS
# ============================================

st.header("🔐 Active Sessions")

try:
    from account_security_system import load_security_db
    db = load_security_db()
    
    if user_email in db:
        sessions = db[user_email].get('sessions', [])
        
        if sessions:
            st.success(f"✅ {len(sessions)} active session(s)")
            
            for i, session in enumerate(sessions, 1):
                with st.expander(f"Session {i} - {session.get('device_fingerprint', 'Unknown')[:8]}"):
                    col_s1, col_s2 = st.columns(2)
                    
                    with col_s1:
                        st.markdown(f"**Session ID:** `{session.get('session_id', 'Unknown')[:16]}...`")
                        st.markdown(f"**Created:** {session.get('created', 'Unknown')[:19]}")
                        st.markdown(f"**Last Activity:** {session.get('last_activity', 'Unknown')[:19]}")
                    
                    with col_s2:
                        st.markdown(f"**IP:** {session.get('ip', 'Unknown')}")
                        st.markdown(f"**Location:** {session.get('location', 'Unknown')}")
                        st.markdown(f"**Device:** {session.get('device_fingerprint', 'Unknown')[:16]}...")
                    
                    if st.button(f"🚫 End Session {i}", key=f"end_session_{i}"):
                        from account_security_system import end_session
                        end_session(user_email, session['session_id'])
                        st.success("Session ended!")
                        st.rerun()
        else:
            st.info("No active sessions")
    else:
        st.info("No session data available")
except Exception as e:
    st.warning(f"Unable to load session data: {str(e)}")

st.divider()

# ============================================
# SECURITY RECOMMENDATIONS
# ============================================

st.header("💡 Security Recommendations")

recommendations = []

# Check risk score
if security_data.get('risk_score', 0) > 60:
    recommendations.append("🔴 **HIGH RISK**: Change your password immediately and enable 2FA")
elif security_data.get('risk_score', 0) > 30:
    recommendations.append("🟡 **MEDIUM RISK**: Consider enabling 2FA for additional security")

# Check multiple locations
if security_data.get('unique_locations', 0) > 5:
    recommendations.append("⚠️ Multiple locations detected - verify all login locations are legitimate")

# Check failed logins
if security_data.get('failed_logins', 0) > 3:
    recommendations.append("⚠️ Multiple failed login attempts detected - change your password if you didn't make these attempts")

# General recommendations
recommendations.extend([
    "✅ Use a strong, unique password (12+ characters, mixed case, numbers, symbols)",
    "✅ Enable two-factor authentication (2FA) for maximum security",
    "✅ Don't share your login credentials with anyone",
    "✅ Log out when using shared or public computers",
    "✅ Review your login activity regularly"
])

for rec in recommendations:
    st.markdown(f"- {rec}")

st.divider()

# ============================================
# SECURITY ACTIONS
# ============================================

st.header("🛡️ Security Actions")

col_act1, col_act2, col_act3 = st.columns(3)

with col_act1:
    if st.button("🔄 Change Password", use_container_width=True):
        st.info("Password change feature coming soon!")

with col_act2:
    if st.button("🔐 Enable 2FA", use_container_width=True):
        st.info("2FA setup coming soon!")

with col_act3:
    if st.button("🚫 End All Sessions", use_container_width=True):
        try:
            from account_security_system import end_all_sessions
            end_all_sessions(user_email)
            st.success("All sessions ended! You will be logged out.")
            st.session_state.logged_in = False
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.caption("🔒 T21 Services UK - Enterprise Security Dashboard")
st.caption(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
