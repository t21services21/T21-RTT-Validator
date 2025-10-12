"""
T21 SERVICES - PROFESSIONAL LANDING PAGE
Clean, gap-free design for NHS platform
"""

import streamlit as st

def render_clean_landing_page():
    """Render professional landing page - zero gaps"""
    
    st.markdown("""
    <style>
        /* Remove ALL Streamlit defaults */
        [data-testid="stSidebar"] {display: none !important;}
        header[data-testid="stHeader"] {display: none !important;}
        .main, .main .block-container, .stApp {padding: 0 !important; margin: 0 !important; margin-top: -100px !important; max-width: 100% !important; overflow-x: hidden !important;}
        body {overflow-x: hidden !important;}
        .element-container, .stMarkdown, div[data-testid="stVerticalBlock"] > div {margin: 0 !important; padding: 0 !important; gap: 0 !important;}
        
        /* Full-width sections */
        .top-bar {background: #1a1a1a; padding: 15px 60px; display: flex; justify-content: space-between; align-items: center; width: 100vw; margin-left: calc(-50vw + 50%);}
        .logo {font-size: 24px; font-weight: 800; color: #d4af37; text-transform: uppercase;}
        .nav-buttons {background: #1a1a1a; padding: 10px 60px; width: 100vw; margin-left: calc(-50vw + 50%);}
        .hero {background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920') center/cover; padding: 50px 60px 80px; color: white; width: 100vw; margin-left: calc(-50vw + 50%);}
        .hero h1 {font-size: 64px; font-weight: 800; margin: 0 0 10px 0; line-height: 1;}
        .hero h2 {font-size: 40px; font-weight: 700; color: #d4af37; margin: 0 0 20px 0;}
        .hero p {font-size: 17px; max-width: 800px; line-height: 1.6;}
    </style>
    
    <div class='top-bar'>
        <span class='logo'>T21 SERVICES</span>
        <a href='#login' style='background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border-radius: 25px; font-weight: 800; text-decoration: none; text-transform: uppercase; font-size: 14px;'>LOGIN / REGISTER</a>
    </div>
    <div class='nav-buttons'>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        if st.button("📋 ABOUT", key="nav_about", use_container_width=True):
            st.switch_page("pages/about.py")
    with c2:
        if st.button("🛠️ SERVICES", key="nav_services", use_container_width=True):
            st.switch_page("pages/services.py")
    with c3:
        if st.button("💰 PRICING", key="nav_pricing", use_container_width=True):
            st.switch_page("pages/pricing.py")
    with c4:
        if st.button("📞 CONTACT", key="nav_contact", use_container_width=True):
            st.switch_page("pages/contact_us.py")
    with c5:
        if st.button("🏠 HOME", key="nav_home", use_container_width=True, type="primary"):
            st.switch_page("app.py")
    with c6:
        if st.button("🏛️ PROCUREMENT", key="nav_procurement", use_container_width=True):
            st.switch_page("pages/procurement.py")
    
    st.markdown("""
    </div>
    <div class='hero'>
        <h1>Your NHS Career & Workforce Partner</h1>
        <h2>Training • Talent • Technology</h2>
        <p>UK Certified Centre serving individuals seeking NHS careers, NHS staff advancing their skills, and NHS trusts transforming operations. TQUK-endorsed training, job application support with proven success, and AI automation saving £2M+ annually. From student to system—we empower everyone.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login section
    st.markdown("<div id='login' style='padding: 40px 60px; background: white;'><h2 style='text-align: center;'>🔐 Login or Register</h2><p style='text-align: center; color: #666;'>Select your portal to access the platform</p></div>", unsafe_allow_html=True)
    
    _, c1, c2, c3, _ = st.columns([2, 1.5, 1.5, 1.5, 2])
    with c1:
        if st.button("🎓 STUDENT LOGIN / REGISTER", key="student_login", use_container_width=True, type="primary"):
            st.switch_page("pages/student_login.py")
    with c2:
        if st.button("👥 STAFF LOGIN / REGISTER", key="staff_login", use_container_width=True, type="primary"):
            st.switch_page("pages/staff_login.py")
    with c3:
        if st.button("🏥 NHS LOGIN / REGISTER", key="nhs_login", use_container_width=True, type="primary"):
            st.switch_page("pages/nhs_login.py")
    
    # Trust badges
    st.markdown("""
    <div style='display: flex; gap: 20px; justify-content: center; padding: 60px; background: #f8f9fa; flex-wrap: wrap;'>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700;'>✅ TQUK APPROVED<br>CENTRE</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700;'>🔒 CYBER ESSENTIALS<br>CERTIFIED</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700;'>🏥 NHS<br>COMPLIANT</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700;'>✅ COMPANIES HOUSE<br>REGISTERED</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700;'>🇬🇧 UK<br>BASED</div>
    </div>
    """, unsafe_allow_html=True)
