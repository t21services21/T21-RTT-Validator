"""
T21 SERVICES - PROFESSIONAL LANDING PAGE
"""

import streamlit as st

def render_clean_landing_page():
    """Professional landing page"""
    
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        header[data-testid="stHeader"] {display: none;}
        .main .block-container {padding: 2rem 1rem; margin-top: -80px;}
        
        .hero-section {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            padding: 3rem 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }
        .hero-section h1 {color: white; margin-bottom: 0.5rem;}
        .hero-section h2 {color: #d4af37; margin-bottom: 1rem;}
    </style>
    
    <div class="hero-section">
        <h1>T21 Healthcare Intelligence Platform</h1>
        <h2>Your NHS Career & Workforce Partner</h2>
        <p style="font-size: 1.1rem; margin: 0;"><strong>Training • Talent • Technology</strong></p>
        <p style="margin-top: 1rem;">UK Certified Centre serving individuals seeking NHS careers, NHS staff advancing their skills, and NHS trusts transforming operations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Login or Register")
    st.markdown("*Select your portal to access the platform*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎓 STUDENT LOGIN / REGISTER", use_container_width=True, type="primary"):
            st.switch_page("pages/student_login.py")
    with col2:
        if st.button("👥 STAFF LOGIN / REGISTER", use_container_width=True, type="primary"):
            st.switch_page("pages/staff_login.py")
    with col3:
        if st.button("🏥 NHS LOGIN / REGISTER", use_container_width=True, type="primary"):
            st.switch_page("pages/nhs_login.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trust badges
    st.markdown("""
    <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-top: 3rem;">
        <div style="background: white; padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; font-weight: 700; font-size: 0.9rem;">✅ TQUK APPROVED<br>CENTRE</div>
        <div style="background: white; padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; font-weight: 700; font-size: 0.9rem;">🔒 CYBER ESSENTIALS<br>CERTIFIED</div>
        <div style="background: white; padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; font-weight: 700; font-size: 0.9rem;">🏥 NHS<br>COMPLIANT</div>
        <div style="background: white; padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; font-weight: 700; font-size: 0.9rem;">✅ COMPANIES HOUSE<br>REGISTERED</div>
        <div style="background: white; padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; font-weight: 700; font-size: 0.9rem;">🇬🇧 UK<br>BASED</div>
    </div>
    """, unsafe_allow_html=True)
