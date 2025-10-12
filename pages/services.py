"""
T21 SERVICES - SERVICES PAGE
"""

import streamlit as st
from navigation import render_navigation

st.set_page_config(page_title="Our Services | T21 Services", page_icon="🎯", layout="wide")

# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

# Reusable navigation
render_navigation(current_page="services")

st.title("Our Complete Services")

st.markdown("---")

# Training & Education
st.markdown("## 🎓 Training & Education")
st.markdown("*UK Certified Centre with TQUK Endorsement*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### NHS Administration Training
    - **RTT (Referral to Treatment) Training** - TQUK-endorsed
    - **Hospital Administration** - TQUK-endorsed
    - **Cancer Pathway Management**
    - **MDT Coordination Training**
    - **Medical Secretary AI Training**
    - **Data Quality & Governance**
    - **NHS Appointment System Training**
    - **Patient Pathway Validation**
    """)

with col2:
    st.markdown("""
    ### Professional Development
    - **Advanced Excel for Healthcare**
    - **NHS Data Analytics**
    - **Clinical Coding Introduction**
    - **GDPR for Healthcare**
    - **Leadership & Management**
    - **Customer Service Excellence**
    - **Conflict Resolution**
    - **Time Management for Healthcare**
    """)

st.markdown("---")

# AI & Automation
st.markdown("## 🤖 AI & Automation Solutions")
st.markdown("*7 Intelligent Systems • 188 Pre-Built Scenarios*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Automation Tools
    - **AI-Powered RTT Validation**
    - **Automated Appointment Scheduling**
    - **Intelligent Data Quality Checks**
    - **Pathway Automation (188 Scenarios)**
    - **Predictive Analytics**
    - **Automated Reporting**
    """)

with col2:
    st.markdown("""
    ### Benefits
    - ✅ Save £2M+ annually
    - ✅ Reduce RTT breaches by 40%
    - ✅ Automate routine tasks
    - ✅ Reduce administrative burden
    - ✅ Improve data accuracy
    - ✅ Free staff for patient care
    """)

st.markdown("---")

# Talent Supply
st.markdown("## 💼 Talent Supply & Placement Services")
st.markdown("*Supply NHS-Ready Certified Staff to Healthcare Organizations*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### What We Supply
    - **TQUK-Certified Healthcare Professionals**
    - **RTT-trained coordinators & specialists**
    - **Hospital Administration experts**
    - **Medical secretaries & data quality staff**
    - **Pre-vetted & qualified candidates**
    - **Job-ready from day one**
    """)

with col2:
    st.markdown("""
    ### Our Process
    1. Train individuals to NHS standards (TQUK-certified)
    2. Hands-on practice with our AI platform
    3. Job application support & CV building
    4. Interview preparation & coaching
    5. **Place qualified staff in NHS trusts**
    6. Ongoing support & alumni network
    
    **We supply trained, qualified staff ready for NHS employment.**
    """)

st.markdown("---")

# Consulting & Support
st.markdown("## 🏥 NHS Trust Solutions")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Consulting Services
    - **NHS Digital Transformation**
    - **Process Optimization**
    - **Change Management**
    - **Training Needs Analysis**
    - **Workforce Planning**
    - **System Integration**
    """)

with col2:
    st.markdown("""
    ### Support Services
    - **24/7 Technical Support** (Enterprise clients)
    - **Dedicated Account Management**
    - **Custom Training Development**
    - **White-Label Solutions**
    - **On-site Implementation**
    - **Data Processing Agreements**
    """)

st.markdown("---")

# Call to Action
st.markdown("## 📞 Get Started")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎓 For Individuals
    Start your NHS career with certified training
    """)
    if st.button("View Training Courses", use_container_width=True, type="primary"):
        st.switch_page("pages/student_login.py")

with col2:
    st.markdown("""
    ### 👥 For NHS Staff
    Upskill with professional development
    """)
    if st.button("Staff Training", use_container_width=True, type="primary"):
        st.switch_page("pages/staff_login.py")

with col3:
    st.markdown("""
    ### 🏥 For NHS Trusts
    Transform your workforce & operations
    """)
    if st.button("Book a Demo", use_container_width=True, type="primary"):
        st.switch_page("pages/contact_us.py")

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
