"""
T21 HEALTHCARE PLATFORM - PATIENT PORTAL
Patient-facing interface for RTT journey tracking
"""

import streamlit as st
from navigation import render_navigation
from datetime import datetime, timedelta

st.set_page_config(page_title="Patient Portal | T21 Services", page_icon="👤", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="patient_portal")

st.title("👤 Patient Portal - Track Your RTT Journey")
st.markdown("**Empowering patients with transparency and control**")

# Patient login demo
st.markdown("""
<div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 40px; border-radius: 20px; color: white; text-align: center;">
    <h1 style="color: white;">👤 Welcome, John Smith</h1>
    <p style="font-size: 18px;">Track your NHS treatment journey in real-time</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Patient journey tracker
st.markdown("### 📊 Your Treatment Journey")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #e3f2fd; padding: 25px; border-radius: 15px; text-align: center;">
        <h3>⏰ Waiting Time</h3>
        <div style="font-size: 48px; font-weight: bold; color: #2196F3;">10 weeks</div>
        <p>of 18 weeks target</p>
        <div style="width: 100%; background: #e0e0e0; border-radius: 10px; height: 20px; margin-top: 15px;">
            <div style="width: 55%; background: #4CAF50; height: 20px; border-radius: 10px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #f3e5f5; padding: 25px; border-radius: 15px; text-align: center;">
        <h3>📅 Next Appointment</h3>
        <div style="font-size: 32px; font-weight: bold; color: #9C27B0;">15 March 2025</div>
        <p>First Outpatient - Orthopaedics</p>
        <button style="background: #9C27B0; color: white; padding: 10px 20px; border: none; border-radius: 8px; margin-top: 10px; cursor: pointer;">
            Confirm Attendance
        </button>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #e8f5e9; padding: 25px; border-radius: 15px; text-align: center;">
        <h3>✅ Status</h3>
        <div style="font-size: 32px; font-weight: bold; color: #4CAF50;">On Track</div>
        <p>Within 18-week target</p>
        <p style="margin-top: 15px;">🎯 8 weeks remaining</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Journey timeline
st.markdown("### 🛤️ Your Journey Timeline")

timeline_events = [
    ("✅", "GP Referral Received", "1 November 2024", "Referred to Orthopaedics for knee pain"),
    ("✅", "Added to Waiting List", "3 November 2024", "Priority: Routine | Clock started"),
    ("✅", "First Appointment Booked", "10 December 2024", "Appointment: 15 March 2025"),
    ("🔵", "First Outpatient Appointment", "15 March 2025", "Upcoming - Please confirm"),
    ("⏳", "Treatment Decision", "Awaiting", "After consultant assessment"),
    ("⏳", "Treatment/Procedure", "TBC", "Estimated: April/May 2025")
]

for status, event, date, details in timeline_events:
    color = "green" if status == "✅" else "blue" if status == "🔵" else "gray"
    st.markdown(f"""
    <div style="border-left: 4px solid {color}; padding: 15px; margin: 10px 0; background: #f9f9f9; border-radius: 8px;">
        <div style="display: flex; justify-content: space-between;">
            <strong style="font-size: 18px;">{status} {event}</strong>
            <span style="color: #666;">{date}</span>
        </div>
        <p style="margin: 5px 0 0 0; color: #555;">{details}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick actions
st.markdown("### ⚡ Quick Actions")

col_a1, col_a2, col_a3, col_a4 = st.columns(4)

with col_a1:
    if st.button("📅 Change Appointment", use_container_width=True):
        st.info("Opening self-booking calendar...")

with col_a2:
    if st.button("❌ Cancel Appointment", use_container_width=True):
        st.warning("Are you sure? This may delay your treatment.")

with col_a3:
    if st.button("📞 Contact Team", use_container_width=True):
        st.success("Message sent to RTT coordinator!")

with col_a4:
    if st.button("📋 My Documents", use_container_width=True):
        st.info("Opening your documents folder...")

st.markdown("---")

# FAQs and support
st.markdown("### ❓ Frequently Asked Questions")

with st.expander("What does 'RTT' mean?"):
    st.markdown("""
    **RTT = Referral to Treatment**
    
    It's the time from when your GP refers you until you receive treatment. 
    NHS aims to treat you within **18 weeks**.
    """)

with st.expander("Why is there a waiting time?"):
    st.markdown("""
    The NHS prioritizes patients by:
    - **Clinical urgency** (urgent cases seen first)
    - **Waiting time** (longer waits prioritized)
    - **Available capacity** (theatre/clinic availability)
    
    Your consultant will see you as soon as safely possible.
    """)

with st.expander("Can I choose a different date?"):
    st.markdown("""
    **Yes!** You can:
    - Use the "Change Appointment" button
    - Select from available slots
    - Note: Declining dates may extend your wait
    """)

with st.expander("What if I can't attend?"):
    st.markdown("""
    **Please let us know ASAP:**
    - Click "Cancel Appointment" button
    - We'll offer you a new date
    - Reduces DNA (Did Not Attend) rates
    - Helps other patients get seen sooner
    """)

st.markdown("---")

# Notifications
st.markdown("### 🔔 Your Notifications")

notifications = [
    ("🟢", "Appointment confirmed for 15 March 2025", "2 days ago"),
    ("🔵", "Please complete pre-assessment questionnaire", "5 days ago"),
    ("🟢", "Added to waiting list", "10 weeks ago")
]

for color, message, time in notifications:
    st.markdown(f"""
    <div style="background: white; padding: 15px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {color.replace('🟢', 'green').replace('🔵', 'blue')};">
        <strong>{message}</strong>
        <br><small style="color: #666;">{time}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Benefits showcase
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.metric("DNA Reduction", "40%", "Patients more engaged")

with col_b2:
    st.metric("Admin Calls Saved", "70%", "Self-service portal")

with col_b3:
    st.metric("Patient Satisfaction", "95%", "+25% improvement")

st.markdown("---")

st.success("""
📱 **Mobile Access:** Download T21 Patient App (iOS & Android)  
🔐 **Secure Login:** NHS Login or email verification  
🔔 **Notifications:** SMS, Email & Push alerts  
💬 **Support:** 24/7 chatbot + human support during office hours
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
