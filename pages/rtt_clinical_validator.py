"""
T21 SERVICES - RTT CLINICAL VALIDATOR
Full NHS RTT Training System Embedded
Access ALL patient registration, pathway validation, and clinical tools
"""

import streamlit as st

st.set_page_config(
    page_title="RTT Clinical Validator | T21 Services",
    page_icon="🏥",
    layout="wide"
)

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>🏥 RTT Clinical Validator</h1>
    <p style='color: white; margin: 0;'>NHS Referral to Treatment - Full Training System</p>
</div>
""", unsafe_allow_html=True)

# Info banner
st.info("""
**🎓 Welcome to the RTT Clinical Validator!**

This system provides complete NHS RTT training including:
- ✅ Patient Registration & Demographics
- ✅ Appointment Management & Booking
- ✅ RTT Pathway Validation & Tracking
- ✅ Timeline Auditing & Compliance
- ✅ Diagnostic Information Management
- ✅ Referral Information Processing
- ✅ Complete NHS Clinical Training Environment

**Note:** You may need to login to access the clinical tools below.
""")

# Instructions expander
with st.expander("📖 How to Use This System"):
    st.markdown("""
    ### Getting Started:
    1. The full RTT Clinical Validator is embedded below
    2. If prompted, login with your RTT Trainer credentials
    3. Access all patient registration, appointments, and validation tools
    4. Your session will remain active as you navigate
    
    ### Available Features:
    - **Patient Registration** - Register and manage patient demographics
    - **Appointments** - Book, manage, and track appointments
    - **Pathway Validation** - Validate RTT pathways and ensure compliance
    - **Timeline Auditor** - Audit patient timelines and milestones
    - **Diagnostic Information** - Manage diagnostic test results
    - **Referral Information** - Process and track referrals
    - **Ad-hoc Events** - Record non-standard pathway events
    
    ### Tips:
    - Use Chrome or Edge for best experience
    - Enable popups if needed
    - Session stays active while you work
    - All data is for training purposes only
    """)

st.markdown("---")

# Embedded RTT Trainer
st.markdown("### 🖥️ RTT Clinical Training System")

# Full-width iframe embed
st.markdown("""
<div style='width: 100%; height: 800px; border: 2px solid #e0e0e0; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
    <iframe 
        src="https://t21servicestraining.co.uk" 
        width="100%" 
        height="100%" 
        frameborder="0"
        style="border: none;"
        allowfullscreen>
    </iframe>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Footer info
st.markdown("### 💡 Need Help?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Technical Support:**
    - Email: support@t21services.co.uk
    - Available: Mon-Fri 9am-5pm
    - Response time: 24 hours
    """)

with col2:
    st.markdown("""
    **Training Resources:**
    - User guides in Training Library
    - Video tutorials available
    - AI Tutor for instant help
    """)

with col3:
    st.markdown("""
    **System Status:**
    - ✅ RTT Validator: Online
    - ✅ Patient Data: Active
    - ✅ All features: Available
    """)

st.markdown("---")

# Security notice
st.info("""
**🔒 Security & Privacy:**
- All patient data is simulated for training purposes
- No real patient information is used
- Your session is secure and encrypted
- All access is logged for security compliance
""")

st.caption("T21 Services Limited | NHS RTT Clinical Validator | Training Environment")
