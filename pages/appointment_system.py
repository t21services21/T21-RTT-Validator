"""
T21 SERVICES - APPOINTMENT MANAGEMENT SYSTEM
Book, Manage, and Track NHS Appointments
"""

import streamlit as st

st.set_page_config(
    page_title="Appointment System | T21 Services",
    page_icon="📅",
    layout="wide"
)

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>📅 NHS Appointment System</h1>
    <p style='color: white; margin: 0;'>Book, Manage, and Track Patient Appointments</p>
</div>
""", unsafe_allow_html=True)

st.info("""
**📅 Appointment Management Features**

Complete appointment management system:
- ✅ Book patient appointments
- ✅ Manage partial and booked appointments  
- ✅ Track waiting lists
- ✅ Monitor appointment compliance
- ✅ Generate appointment reports
""")

# Embedded appointment system
st.markdown("""
<div style='width: 100%; height: 800px; border: 2px solid #e0e0e0; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
    <iframe 
        src="https://t21servicestraining.co.uk/nhs/appointment" 
        width="100%" 
        height="100%" 
        frameborder="0"
        style="border: none;"
        allowfullscreen>
    </iframe>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("T21 Services | NHS Appointment System | Training Environment")
