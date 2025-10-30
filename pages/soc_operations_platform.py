"""
SOC OPERATIONS PLATFORM
24/7 Security Operations Center for client work

Features:
- Real-time monitoring
- Alert management
- Incident response
- Ticket queue
- Client dashboards
- Analyst workspace
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="SOC Operations", page_icon="🛡️", layout="wide")

# Check if analyst/admin
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email
user_role = st.session_state.get('user_license', {})
if hasattr(user_role, 'role'):
    user_role = user_role.role
else:
    user_role = 'student'

is_analyst = user_role in ['super_admin', 'admin', 'staff', 'analyst'] or 'admin@t21services' in user_email.lower()

if not is_analyst:
    st.error("🚫 SOC Analyst Access Only")
    st.stop()

# Header
st.title("🛡️ SOC Operations Platform")
st.markdown(f"**Analyst:** {user_email}")
st.markdown(f"**Shift:** Day Shift | **Status:** 🟢 Active")

st.divider()

# ============================================
# OPERATIONS DASHBOARD
# ============================================

st.header("📊 Operations Dashboard")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🚨 Active Alerts", "23", "+5 last hour")

with col2:
    st.metric("🎯 Open Tickets", "47", "-3 today")

with col3:
    st.metric("👥 Active Clients", "12", "All monitored")

with col4:
    st.metric("⏱️ Avg Response", "4.2 min", "-0.8 min")

with col5:
    st.metric("✅ Resolved Today", "34", "+12 vs yesterday")

st.divider()

# ============================================
# ALERT QUEUE
# ============================================

st.header("🚨 Alert Queue")

tab1, tab2, tab3, tab4 = st.tabs(["🔥 Critical", "⚠️ High", "🟡 Medium", "📋 All Alerts"])

with tab1:
    st.subheader("Critical Alerts - Immediate Action Required")
    
    critical_alerts = [
        {
            "id": "ALT-2025-001",
            "client": "NHS Trust London",
            "type": "Ransomware Detection",
            "severity": "🔴 Critical",
            "time": "2 minutes ago",
            "status": "New"
        },
        {
            "id": "ALT-2025-002",
            "client": "FinTech Solutions",
            "type": "Data Exfiltration Attempt",
            "severity": "🔴 Critical",
            "time": "15 minutes ago",
            "status": "Investigating"
        }
    ]
    
    for alert in critical_alerts:
        with st.expander(f"🔴 {alert['id']} - {alert['type']} - {alert['client']}"):
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                st.markdown(f"**Client:** {alert['client']}")
                st.markdown(f"**Type:** {alert['type']}")
                st.markdown(f"**Severity:** {alert['severity']}")
            
            with col_a2:
                st.markdown(f"**Alert ID:** {alert['id']}")
                st.markdown(f"**Time:** {alert['time']}")
                st.markdown(f"**Status:** {alert['status']}")
            
            st.markdown("**Details:**")
            st.code("""
Source IP: 185.220.101.45 (Russia)
Target: file-server-01.nhslondon.local
Process: suspicious_encrypt.exe
Hash: a3f2e1d4c5b6...
Behavior: Mass file encryption detected
Files Affected: 1,247 files
            """)
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            
            with col_b1:
                if st.button("🔍 Investigate", key=f"inv_{alert['id']}"):
                    st.success("Opening investigation workspace...")
            
            with col_b2:
                if st.button("🚨 Escalate", key=f"esc_{alert['id']}"):
                    st.warning("Escalating to senior analyst...")
            
            with col_b3:
                if st.button("📞 Call Client", key=f"call_{alert['id']}"):
                    st.info("Initiating client call...")
            
            with col_b4:
                if st.button("✅ Resolve", key=f"res_{alert['id']}"):
                    st.success("Marking as resolved...")

with tab2:
    st.subheader("High Priority Alerts")
    
    high_alerts = [
        {"id": "ALT-2025-003", "client": "Global Manufacturing", "type": "Brute Force Attack", "time": "25 min ago"},
        {"id": "ALT-2025-004", "client": "Tech Startup XYZ", "type": "Malware Detection", "time": "45 min ago"},
        {"id": "ALT-2025-005", "client": "Retail Corp", "type": "Suspicious Login", "time": "1 hour ago"}
    ]
    
    for alert in high_alerts:
        col_h1, col_h2, col_h3, col_h4 = st.columns([2, 2, 1, 1])
        with col_h1:
            st.markdown(f"**{alert['id']}** - {alert['type']}")
        with col_h2:
            st.markdown(f"🏢 {alert['client']}")
        with col_h3:
            st.markdown(f"⏱️ {alert['time']}")
        with col_h4:
            if st.button("View", key=f"view_{alert['id']}"):
                st.success("✅ Alert Details:")
                st.code(f"""
Alert ID: {alert['id']}
Type: {alert['type']}
Source: {alert['source']}
Time: {alert['time']}
Status: Active

Recommended Action: Investigate and contain
                """)
                st.info("🔍 Click 'Investigate' to start analysis")

with tab3:
    st.subheader("Medium Priority Alerts")
    st.info("15 medium priority alerts - Review when critical/high are handled")

with tab4:
    st.subheader("All Alerts")
    
    # Filter options
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        client_filter = st.selectbox("Filter by Client", ["All Clients", "NHS Trust London", "FinTech Solutions", "Global Manufacturing"])
    with col_f2:
        severity_filter = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"])
    with col_f3:
        status_filter = st.selectbox("Filter by Status", ["All", "New", "Investigating", "Resolved", "False Positive"])
    
    st.info(f"Showing 47 alerts matching filters")

st.divider()

# ============================================
# TICKET QUEUE
# ============================================

st.header("🎫 Ticket Queue")

col_tq1, col_tq2 = st.columns([2, 1])

with col_tq1:
    st.subheader("My Assigned Tickets")
    
    tickets = [
        {
            "id": "TKT-2025-101",
            "client": "NHS Trust London",
            "title": "Investigate ransomware alert",
            "priority": "🔴 Critical",
            "assigned": "You",
            "status": "In Progress",
            "sla": "15 min remaining"
        },
        {
            "id": "TKT-2025-102",
            "client": "FinTech Solutions",
            "title": "Review suspicious login patterns",
            "priority": "🟠 High",
            "assigned": "You",
            "status": "New",
            "sla": "2 hours remaining"
        },
        {
            "id": "TKT-2025-103",
            "client": "Global Manufacturing",
            "title": "Monthly security report",
            "priority": "🟢 Low",
            "assigned": "You",
            "status": "New",
            "sla": "2 days remaining"
        }
    ]
    
    for ticket in tickets:
        with st.expander(f"{ticket['priority']} {ticket['id']} - {ticket['title']}"):
            col_t1, col_t2 = st.columns(2)
            
            with col_t1:
                st.markdown(f"**Client:** {ticket['client']}")
                st.markdown(f"**Priority:** {ticket['priority']}")
                st.markdown(f"**Status:** {ticket['status']}")
            
            with col_t2:
                st.markdown(f"**Ticket ID:** {ticket['id']}")
                st.markdown(f"**Assigned:** {ticket['assigned']}")
                st.markdown(f"**SLA:** {ticket['sla']}")
            
            col_tb1, col_tb2, col_tb3 = st.columns(3)
            with col_tb1:
                if st.button("🔍 Work On", key=f"work_{ticket['id']}"):
                    st.success("Opening ticket workspace...")
            with col_tb2:
                if st.button("💬 Add Note", key=f"note_{ticket['id']}"):
                    st.info("Adding note...")
            with col_tb3:
                if st.button("✅ Close", key=f"close_{ticket['id']}"):
                    st.success("Closing ticket...")

with col_tq2:
    st.subheader("Ticket Statistics")
    
    st.metric("My Open Tickets", "3")
    st.metric("Resolved Today", "7")
    st.metric("Avg Resolution Time", "42 min")
    
    st.markdown("---")
    
    st.subheader("SLA Compliance")
    st.progress(0.94)
    st.caption("94% SLA compliance this month")

st.divider()

# ============================================
# INVESTIGATION WORKSPACE
# ============================================

st.header("🔍 Investigation Workspace")

col_inv1, col_inv2 = st.columns([2, 1])

with col_inv1:
    st.subheader("Active Investigation: ALT-2025-001")
    
    # Investigation tabs
    inv_tabs = st.tabs(["📊 Timeline", "🔍 Evidence", "📝 Notes", "🎯 Actions"])
    
    with inv_tabs[0]:
        st.markdown("### Event Timeline")
        
        timeline = [
            {"time": "14:32:15", "event": "Initial alert triggered", "severity": "🔴"},
            {"time": "14:32:18", "event": "Suspicious process detected: suspicious_encrypt.exe", "severity": "🔴"},
            {"time": "14:32:25", "event": "Mass file encryption started", "severity": "🔴"},
            {"time": "14:32:45", "event": "Network connection to C2 server detected", "severity": "🔴"},
            {"time": "14:33:00", "event": "Analyst assigned to investigation", "severity": "🟢"},
            {"time": "14:33:30", "event": "Process terminated", "severity": "🟢"}
        ]
        
        for event in timeline:
            st.markdown(f"{event['severity']} **{event['time']}** - {event['event']}")
    
    with inv_tabs[1]:
        st.markdown("### Collected Evidence")
        
        st.markdown("**Files:**")
        st.markdown("- suspicious_encrypt.exe (SHA256: a3f2e1d4c5b6...)")
        st.markdown("- ransom_note.txt")
        st.markdown("- network_capture.pcap")
        
        st.markdown("**Network:**")
        st.markdown("- C2 Server: 185.220.101.45:443")
        st.markdown("- Data transferred: 2.3 MB")
        
        if st.button("📥 Download Evidence Package"):
            st.success("Downloading evidence...")
    
    with inv_tabs[2]:
        st.markdown("### Investigation Notes")
        
        notes = st.text_area("Add notes:", height=150, placeholder="Document your findings...")
        
        if st.button("💾 Save Notes"):
            st.success("Notes saved!")
    
    with inv_tabs[3]:
        st.markdown("### Recommended Actions")
        
        actions = [
            "✅ Isolate affected system from network",
            "✅ Terminate malicious process",
            "⏳ Run full malware scan",
            "⏳ Restore files from backup",
            "⏳ Block C2 server IP",
            "⏳ Notify client CISO"
        ]
        
        for action in actions:
            st.markdown(f"- {action}")

with col_inv2:
    st.subheader("Quick Actions")
    
    if st.button("🚨 Declare Incident", use_container_width=True):
        st.warning("Incident declared!")
    
    if st.button("🔒 Isolate System", use_container_width=True):
        st.success("System isolated!")
    
    if st.button("📧 Notify Client", use_container_width=True):
        st.info("Client notified!")
    
    if st.button("📊 Generate Report", use_container_width=True):
        st.success("Report generated!")
    
    st.markdown("---")
    
    st.subheader("Playbooks")
    
    playbooks = [
        "Ransomware Response",
        "Data Breach",
        "Malware Infection",
        "DDoS Attack",
        "Insider Threat"
    ]
    
    selected_playbook = st.selectbox("Select Playbook:", playbooks)
    
    if st.button("📖 Load Playbook", use_container_width=True):
        st.info(f"Loading {selected_playbook} playbook...")

st.divider()

# ============================================
# CLIENT DASHBOARDS
# ============================================

st.header("👥 Client Dashboards")

clients = [
    {"name": "NHS Trust London", "status": "🔴 Incident Active", "alerts": 3, "health": 65},
    {"name": "FinTech Solutions", "status": "🟡 Monitoring", "alerts": 2, "health": 85},
    {"name": "Global Manufacturing", "status": "🟢 Secure", "alerts": 1, "health": 95},
    {"name": "Tech Startup XYZ", "status": "🟢 Secure", "alerts": 0, "health": 98}
]

for client in clients:
    col_c1, col_c2, col_c3, col_c4, col_c5 = st.columns([2, 1, 1, 1, 1])
    
    with col_c1:
        st.markdown(f"**{client['name']}**")
    with col_c2:
        st.markdown(client['status'])
    with col_c3:
        st.markdown(f"🚨 {client['alerts']} alerts")
    with col_c4:
        st.progress(client['health'] / 100)
        st.caption(f"{client['health']}% health")
    with col_c5:
        if st.button("View", key=f"view_client_{client['name']}"):
            st.info(f"Loading {client['name']} dashboard...")

st.divider()

# ============================================
# SHIFT HANDOVER
# ============================================

st.header("🔄 Shift Handover")

col_sh1, col_sh2 = st.columns(2)

with col_sh1:
    st.subheader("Current Shift Summary")
    
    st.markdown("""
    **Shift:** Day Shift (08:00 - 16:00)  
    **Analyst:** {user_email}  
    **Duration:** 6 hours 45 minutes
    
    **Activity Summary:**
    - Alerts handled: 34
    - Incidents resolved: 7
    - Tickets closed: 7
    - Escalations: 2
    
    **Outstanding Items:**
    - 3 open tickets (see above)
    - 1 critical incident (ransomware)
    - 2 pending client calls
    """)

with col_sh2:
    st.subheader("Handover Notes")
    
    handover_notes = st.text_area(
        "Notes for next shift:",
        height=200,
        placeholder="Document important information for the next analyst..."
    )
    
    if st.button("📝 Submit Handover", use_container_width=True):
        st.success("Handover notes submitted!")
        st.info("Next shift analyst will be notified")

st.divider()

# ============================================
# PERFORMANCE METRICS
# ============================================

st.header("📈 Your Performance")

col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    st.metric("Tickets Resolved", "127", "+15 this week")

with col_p2:
    st.metric("Avg Response Time", "4.2 min", "-0.8 min")

with col_p3:
    st.metric("SLA Compliance", "94%", "+2%")

with col_p4:
    st.metric("Client Satisfaction", "4.8/5", "+0.2")

# Performance chart
st.subheader("Weekly Performance Trend")

dates = pd.date_range(start='2025-10-23', end='2025-10-29', freq='D')
tickets_resolved = [15, 18, 22, 19, 25, 21, 27]

fig_perf = px.line(x=dates, y=tickets_resolved, labels={'x': 'Date', 'y': 'Tickets Resolved'})
fig_perf.update_layout(height=300)
st.plotly_chart(fig_perf, use_container_width=True)

# Footer
st.markdown("---")
st.caption("🛡️ T21 SOC Operations Platform - Protecting Clients 24/7")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
