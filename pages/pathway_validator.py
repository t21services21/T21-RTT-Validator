"""
T21 SERVICES - RTT PATHWAY VALIDATOR
Validate RTT Pathways for Compliance
"""

import streamlit as st

st.set_page_config(
    page_title="Pathway Validator | T21 Services",
    page_icon="📊",
    layout="wide"
)

# ⚠️ AUTHENTICATION CHECK - MUST BE LOGGED IN
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 **Access Denied - Login Required**")
    st.warning("You must be logged in to access the Pathway Validator.")
    st.info("This feature is available to all enrolled students. Please login to continue.")
    
    st.markdown("### Please Login:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎓 Student Login", use_container_width=True):
            st.switch_page("pages/student_login.py")
    with col2:
        if st.button("👥 Staff Login", use_container_width=True):
            st.switch_page("pages/staff_login.py")
    with col3:
        if st.button("🏥 NHS Login", use_container_width=True):
            st.switch_page("pages/nhs_login.py")
    
    st.stop()  # Stop execution here

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>📊 RTT Pathway Validator</h1>
    <p style='color: white; margin: 0;'>Validate NHS Referral to Treatment Pathways</p>
</div>
""", unsafe_allow_html=True)

st.info("""
**📋 RTT Pathway Validation System**

Validate patient RTT pathways against NHS standards:
- ✅ Check pathway compliance with 18-week target
- ✅ Validate clock start and stop rules
- ✅ Identify pathway errors and issues
- ✅ Generate validation reports
- ✅ Track pathway milestones
""")

# Embedded pathway validator
st.markdown("""
<div style='width: 100%; height: 800px; border: 2px solid #e0e0e0; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
    <iframe 
        src="https://t21servicestraining.co.uk/nhs/pathway" 
        width="100%" 
        height="100%" 
        frameborder="0"
        style="border: none;"
        allowfullscreen>
    </iframe>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("T21 Services | RTT Pathway Validator | Training Environment")
