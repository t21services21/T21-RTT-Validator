"""
T21 SERVICES - SERVICES PAGE
"""

import streamlit as st

st.set_page_config(page_title="Our Services | T21 Services", page_icon="🎯", layout="wide")

# Navigation bar
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    
    /* Remove all top spacing */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .main {
        padding-top: 0 !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .top-nav {
        background: rgba(26, 26, 26, 0.95);
        padding: 15px 60px;
        margin: -100px -70px 30px -70px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .nav-logo-text {
        font-size: 24px;
        font-weight: 800;
        color: #d4af37;
        text-transform: uppercase;
        text-decoration: none;
    }
    
    .nav-menu {
        display: flex;
        gap: 40px;
    }
    
    .nav-link {
        color: white !important;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        text-decoration: none;
        padding: 10px 15px;
    }
    
    .nav-link:hover {
        color: #d4af37 !important;
    }
</style>

<div class='top-nav'>
    <img src='assets/t21_logo.png' alt='T21 SERVICES' style='height:34px; vertical-align: middle; border-radius: 50%; margin-right:10px;' onerror="this.style.display='none';">
    <span class='nav-logo-text'>T21 SERVICES</span>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
st.markdown("<div style='background: rgba(26, 26, 26, 0.95); padding: 10px; margin: -30px -70px 20px -70px;'>", unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("🏠 HOME", key="nav_home", use_container_width=True, type="primary"):
        st.switch_page("app.py")
with col2:
    if st.button("📋 ABOUT", key="nav_about", use_container_width=True):
        st.switch_page("pages/about.py")
with col3:
    if st.button("💰 PRICING", key="nav_pricing", use_container_width=True):
        st.switch_page("pages/pricing.py")
with col4:
    if st.button("📞 CONTACT", key="nav_contact", use_container_width=True):
        st.switch_page("pages/contact_us.py")
with col5:
    if st.button("⭐ TESTIMONIALS", key="nav_testimonials", use_container_width=True):
        st.switch_page("pages/testimonials.py")
with col6:
    if st.button("🏛️ PROCUREMENT", key="nav_procurement", use_container_width=True):
        st.switch_page("pages/procurement.py")
st.markdown("</div>", unsafe_allow_html=True)

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
st.markdown("## 💼 Talent Supply Services")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### What We Provide
    - **Certified Healthcare Professionals**
    - **RTT-trained learners and graduates**
    - **Hospital Administration specialists**
    - **Job application & interview support**
    - **Pre-vetted & qualified candidates**
    """)

with col2:
    st.markdown("""
    ### Our Process
    1. Train individuals to NHS standards
    2. TQUK-endorsed certification
    3. Job application support
    4. Interview preparation
    5. NHS employer hiring (we do not directly place; we support your applications)
    6. Ongoing alumni support
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
