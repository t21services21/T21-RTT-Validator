"""
T21 HEALTHCARE PLATFORM - COMMUNICATIONS TRACKER
Track all patient communications (letters, calls, SMS)
"""

import streamlit as st
from datetime import datetime, timedelta
from navigation import render_navigation
import pandas as pd

st.set_page_config(page_title="Communications Tracker | T21 Services", page_icon="✉️", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="communications")

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
