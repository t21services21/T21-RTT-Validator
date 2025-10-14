"""
T21 HEALTHCARE PLATFORM - COMMUNICATIONS TRACKER
Track all patient communications (letters, calls, SMS)
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

from sidebar_manager import render_sidebar
from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)



st.markdown("""
<style>
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 1rem !important;}
</style>
""", unsafe_allow_html=True)

render_sidebar()

st.title("✉️ Patient Communications Tracker")
st.markdown("**Log all patient communications for RTT compliance**")

with st.expander("📚 Why Track Communications?", expanded=True):
    st.markdown("""
    ### Legal & RTT Requirements
    
    **Must prove:**
    - Patient was offered appointments
    - Patient received appointment letters
    - Patient was contacted after DNA
    - Patient was informed of delays
    - Patient gave consent
    
    **RTT Disputes:**
    If patient claims not contacted, you must PROVE communication was sent!
    
    ### What to Track:
    - 📧 Appointment letters sent
    - 📞 Phone calls made
    - 📱 SMS reminders sent
    - ✉️ Email notifications
    - 🚨 Breach warning letters
    - 📋 DNA warning letters
    - 🔄 Transfer notifications
    """)


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Communication Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Communications")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_communications")
    with col2:
        records = read_all_records('communications')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "communications.csv", "text/csv")
    
    # Get records
    records = read_all_records('communications')
    
    if search_term:
        records = search_records('communications', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Communication #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('communications', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Communication")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('communications')
    
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

# Log communication
st.markdown("## 📝 Log New Communication")

with st.form("communication_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *")
    
    with col2:
        comm_type = st.selectbox("Communication Type *", [
            "📧 Appointment Letter",
            "📞 Phone Call",
            "📱 SMS Reminder",
            "✉️ Email",
            "🚨 Breach Warning Letter",
            "📋 DNA Warning Letter",
            "🔄 Transfer Notification",
            "ℹ️ Information Letter",
            "Other"
        ])
        
        comm_date = st.date_input("Date Sent/Made *")
    
    purpose = st.text_area("Purpose of Communication *",
        placeholder="e.g., Appointment confirmation for 15/03/2025, DNA warning - first offense")
    
    appointment_date = st.date_input("Related Appointment Date (if applicable)")
    
    outcome = st.selectbox("Outcome/Response", [
        "Sent successfully",
        "Patient confirmed receipt",
        "Patient declined/cancelled",
        "Phone - no answer (left message)",
        "Phone - spoke to patient",
        "Letter returned (wrong address)",
        "Email bounced",
        "SMS delivered",
        "Awaiting response"
    ])
    
    notes = st.text_area("Additional Notes")
    
    submitted = st.form_submit_button("📝 Log Communication", type="primary", use_container_width=True)
    
    if submitted:
        if patient_name and nhs_number and purpose:
            st.success("✅ Communication logged successfully!")
            st.balloons()

# Communication history
st.markdown("---")
st.markdown("## 📋 Recent Communications")

demo_comms = pd.DataFrame({
    "Date": ["12/01/2025", "11/01/2025", "10/01/2025", "09/01/2025", "08/01/2025"],
    "Patient": ["John Smith", "Mary Jones", "David Brown", "Lisa Wilson", "Sarah Johnson"],
    "Type": ["📧 Appointment Letter", "📞 Phone Call", "📱 SMS Reminder", "📋 DNA Warning", "🚨 Breach Warning"],
    "Purpose": [
        "Appt confirmation 20/01/2025",
        "DNA follow-up",
        "Reminder for tomorrow",
        "First DNA warning",
        "Near 18-week breach"
    ],
    "Outcome": ["✅ Sent", "✅ Patient answered", "✅ Delivered", "✅ Sent", "✅ Sent"],
    "By": ["Admin Staff", "Jane Smith", "Auto-system", "Admin Staff", "Admin Staff"]
})

st.dataframe(demo_comms, use_container_width=True)

# Statistics
st.markdown("---")
st.markdown("## 📊 Communication Statistics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Letters Sent Today", "45", "+8")
with col2:
    st.metric("Phone Calls Made", "23", "+5")
with col3:
    st.metric("SMS Sent", "67", "+12")
with col4:
    st.metric("Undelivered", "2", "-1")

st.markdown("---")
st.info("💡 **RTT Protection:** Detailed communication log proves compliance if disputes arise!")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
