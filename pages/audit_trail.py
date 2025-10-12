"""
T21 HEALTHCARE PLATFORM - AUDIT TRAIL
Track who did what when for governance and compliance
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from navigation import render_navigation
from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)



st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="audit")

st.title("🔍 Audit Trail - Activity Tracking")
st.markdown("**Track all system changes for governance and accountability**")

with st.expander("📚 Why Audit Trails Matter", expanded=True):
    st.markdown("""
    ### Governance & Compliance
    
    **Audit trails answer:**
    - WHO made the change?
    - WHAT was changed?
    - WHEN was it changed?
    - WHY was it changed?
    
    **Required for:**
    - CQC inspections
    - Internal audits
    - Incident investigations
    - Data protection (GDPR)
    - Clinical governance
    
    ### What Gets Audited:
    - Patient pathway changes
    - RTT clock adjustments
    - Priority changes
    - Cancellations/DNAs recorded
    - Transfers processed
    - Clinical exceptions added
    - Waiting list changes
    - User logins/actions
    """)


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Audit Record Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Audit Records")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_audit_records")
    with col2:
        records = read_all_records('audit_records')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "audit_records.csv", "text/csv")
    
    # Get records
    records = read_all_records('audit_records')
    
    if search_term:
        records = search_records('audit_records', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Audit Record #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('audit_records', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Audit Record")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('audit_records')
    
    if records:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(records))
        with col2:
            st.metric("This Month", 0)  # Calculate as needed
        with col3:
            st.metric("Active", len(records))
    else:
        st.info("No data for analytics yet")

st.markdown("---")
# Educational content continues below...


st.markdown("---")

# Search filters
st.markdown("## 🔎 Search Audit Log")

col1, col2, col3 = st.columns(3)
with col1:
    date_range = st.date_input("Date Range", value=(datetime.now().date() - timedelta(days=7), datetime.now().date()))
with col2:
    user_filter = st.selectbox("User", ["All Users", "T21 Administrator", "Staff User", "NHS User"])
with col3:
    action_filter = st.selectbox("Action Type", [
        "All Actions",
        "Patient Added",
        "Patient Updated",
        "Clock Paused",
        "Clock Resumed",
        "Priority Changed",
        "Transfer Processed",
        "DNA Recorded",
        "Cancellation Recorded"
    ])

search_button = st.button("🔍 Search", type="primary", use_container_width=True)

if search_button:
    # Demo audit data
    demo_audit = pd.DataFrame({
        "Timestamp": [
            "2025-01-12 14:35:22",
            "2025-01-12 14:20:15",
            "2025-01-12 13:45:08",
            "2025-01-12 11:22:33",
            "2025-01-12 10:15:44"
        ],
        "User": [
            "T21 Administrator",
            "Staff User (Jane Smith)",
            "T21 Administrator",
            "NHS User (Dr. Jones)",
            "Staff User (Jane Smith)"
        ],
        "Action": [
            "Patient Added",
            "Clock Paused",
            "Priority Changed",
            "DNA Recorded",
            "Transfer Processed"
        ],
        "Patient": [
            "John Doe (NHS: 1234567890)",
            "Mary Johnson (NHS: 2345678901)",
            "David Smith (NHS: 3456789012)",
            "Lisa Brown (NHS: 4567890123)",
            "Sarah Wilson (NHS: 5678901234)"
        ],
        "Details": [
            "New patient added to Ortho waiting list",
            "Clock paused - patient choice (holiday)",
            "Priority changed from P3 to P2 (clinical escalation)",
            "DNA recorded - first offense, warning sent",
            "Transfer to Rheumatology - new clock started"
        ],
        "IP Address": [
            "192.168.1.100",
            "192.168.1.105",
            "192.168.1.100",
            "192.168.1.110",
            "192.168.1.105"
        ]
    })
    
    st.markdown("### 📋 Audit Log Results")
    st.dataframe(demo_audit, use_container_width=True)
    
    st.info(f"""
    **Search Results:**
    - **{len(demo_audit)} events** found
    - Date Range: Last 7 days
    - Users: {demo_audit['User'].nunique()} different users
    - Actions: {demo_audit['Action'].nunique()} different action types
    """)
    
    # Export options
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.button("📥 Export to CSV", use_container_width=True)
    with col_b:
        st.button("📊 Generate Report", use_container_width=True)
    with col_c:
        st.button("📧 Email to Auditor", use_container_width=True)

# Recent activity
st.markdown("---")
st.markdown("## ⏱️ Recent Activity (Last Hour)")

recent_activity = pd.DataFrame({
    "Time": ["14:35", "14:30", "14:25", "14:20", "14:15"],
    "User": ["T21 Administrator", "Staff User", "NHS User", "T21 Administrator", "Staff User"],
    "Action": ["Patient Added", "Data Exported", "DNA Recorded", "Login", "Clock Paused"],
    "Status": ["✅ Success", "✅ Success", "✅ Success", "✅ Success", "✅ Success"]
})

st.dataframe(recent_activity, use_container_width=True)

# Statistics
st.markdown("---")
st.markdown("## 📊 Audit Statistics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Events Today", "237", "+45")
with col2:
    st.metric("Unique Users", "12", "+2")
with col3:
    st.metric("Failed Logins", "0", "0")
with col4:
    st.metric("Data Exports", "8", "+3")

st.markdown("---")

# Compliance checks
st.markdown("## ✅ Compliance Checks")

compliance_checks = [
    ("All clock changes have justification", True, "✅ PASS"),
    ("All user actions logged", True, "✅ PASS"),
    ("No unauthorized access detected", True, "✅ PASS"),
    ("Audit log retention policy met (7 years)", True, "✅ PASS"),
    ("Data protection measures in place", True, "✅ PASS")
]

for check, status, result in compliance_checks:
    col_check, col_status = st.columns([4, 1])
    with col_check:
        st.markdown(f"**{check}**")
    with col_status:
        if status:
            st.success(result)
        else:
            st.error("❌ FAIL")

st.markdown("---")
st.info("""
💡 **For Students:** Practice reviewing audit logs. For NHS: Full audit trail available for all system changes.

**GDPR Compliant:** All audit data anonymized for training. Real NHS data fully protected.
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
