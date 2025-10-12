"""
T21 SERVICES - ABOUT PAGE
"""

import streamlit as st
from navigation import render_navigation

st.set_page_config(page_title="About Us | T21 Services", page_icon="🏢", layout="wide")

# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="about")

st.title("About T21 Services")

st.markdown("""
**T21 Services Limited** is a **TQUK Approved Centre** (Centre No: **36257481088**) and leading healthcare training, talent supply, and technology company serving the NHS and healthcare sector.

**Official TQUK Endorsement:**
- ✅ **TQUK Approved Centre Number:** 36257481088
- ✅ **Endorsed Course:** "Proficient Professional Development Learning Course in Understanding RTT and Hospital Administration" (PDLC-01-039)
- ✅ **Status:** APPROVED by Training Qualifications UK
- ✅ **Contact:** Amb. Tosin Michael Owonifari, FCISM (t.owonifari@t21services.co.uk)

**What We Do:**
- 🎓 **Train Individuals** - TQUK-certified RTT & Hospital Administration courses for career starters
- 👥 **Upskill NHS Staff** - Professional development and certification for existing healthcare professionals
- 💼 **Supply Qualified Talent** - Place trained, job-ready staff in NHS organizations
- 🤝 **Job Application Support** - Help our trained graduates secure NHS roles with proven success
- 🤖 **Provide AI Automation** - 50+ intelligent modules saving £2M+ per trust annually
- 🏥 **Support NHS Trusts** - End-to-end workforce training, talent supply, and technology solutions

Established in 2020 and registered with Companies House (No: 13091053), we're a TQUK Approved Centre committed to transforming healthcare workforce development through officially endorsed training programs and cutting-edge technology solutions.
""")

st.markdown("---")

# Mission & Vision
st.markdown("## 🎯 Our Mission & Vision")

col_mv1, col_mv2 = st.columns(2)

with col_mv1:
    st.markdown("""
    ### 🎯 Our Mission
    **"Training • Talent • Technology"**
    
    To be the UK's leading NHS workforce partner by:
    
    1. **Training** individuals seeking NHS careers + Upskilling existing NHS staff with TQUK-certified qualifications
    2. **Supplying** qualified, job-ready talent to healthcare organizations
    3. **Transforming** NHS operations through AI-powered technology
    
    We serve both aspiring healthcare professionals and current NHS staff, bridging training gaps and revolutionizing operations with cutting-edge automation.
    """)

with col_mv2:
    st.markdown("""
    ### 🚀 Our Vision
    **"Empowering Healthcare Through Excellence"**
    
    To become the NHS sector's most trusted partner for:
    - World-class healthcare training (TQUK-certified)
    - Reliable supply of qualified professionals
    - Innovative AI automation solutions
    - Sustainable workforce transformation
    
    **By 2030:** Train 10,000+ healthcare professionals • Place 5,000+ staff in NHS roles • Save NHS £500M+ through automation
    """)

st.markdown("---")

# Three Pillars
st.markdown("## 🏛️ Our Three Pillars")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.markdown("""
    ### 🎓 Training
    **TQUK-Certified Excellence**
    
    - RTT & Hospital Administration
    - Hands-on platform practice
    - Job-ready skills
    - Professional certifications
    - Career development
    
    *Building competent healthcare professionals*
    """)

with col_p2:
    st.markdown("""
    ### 💼 Talent
    **Workforce Supply**
    
    - Supply trained NHS staff
    - Pre-vetted candidates
    - Job application support
    - Interview preparation
    - Placement assistance
    
    *Connecting talent with opportunity*
    """)

with col_p3:
    st.markdown("""
    ### 🤖 Technology
    **AI-Powered Innovation**
    
    - 50+ automation modules
    - £2M+ savings per trust
    - 120x faster validation
    - 99.9% accuracy
    - Zero breaches
    
    *Revolutionizing NHS operations*
    """)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🏢 Company Details
    - **Registered:** Companies House UK
    - **Company No:** 13091053
    - **Location:** Liverpool, England
    - **Founded:** 2020
    - **VAT Registered:** Yes
    """)

with col2:
    st.markdown("""
    ### ✅ Certifications
    - **TQUK Approved Centre**
    - **Centre No:** 36257481088
    - **Course Code:** PDLC-01-039
    - **Cyber Essentials Certified** ✅
    - **NHS Compliant**
    - **GDPR Certified**
    - **Companies House Registered**
    """)

with col3:
    st.markdown("""
    ### 📊 Our Impact
    - **500+** Students Trained
    - **50+** NHS Organizations
    - **£2M+** Annual Savings
    - **98%** Satisfaction Rate
    """)

st.markdown("---")

# Quick Links
st.markdown("## 🔗 Learn More")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👔 Leadership Team", use_container_width=True, type="primary"):
        st.switch_page("pages/leadership.py")

with col2:
    if st.button("⭐ Testimonials", use_container_width=True, type="primary"):
        st.switch_page("pages/testimonials.py")

with col3:
    if st.button("🏆 Why Choose T21?", use_container_width=True, type="primary"):
        st.switch_page("pages/why_t21.py")

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
