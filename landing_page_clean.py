"""
T21 SERVICES - CLEAN LANDING PAGE
ONLY Hero + Login Buttons
"""

import streamlit as st

def render_clean_landing_page():
    """Render clean landing page with hero and login only"""
    
    # Professional CSS - Complete Spacing Control
    st.markdown("""
    <style>
        /* ===== STREAMLIT FRAMEWORK OVERRIDES ===== */
        [data-testid="stSidebar"] {display: none !important;}
        header[data-testid="stHeader"] {display: none !important; height: 0 !important;}
        
        /* Force zero padding/margin on all Streamlit containers */
        .main, .main .block-container, section[data-testid="stAppViewContainer"], .stApp {
            padding: 0 !important;
            margin: 0 !important;
            margin-top: -100px !important;
            max-width: 100% !important;
        }
        
        /* Kill the top white space completely */
        .main > div:first-child {
            margin-top: -100px !important;
        }
        
        /* Remove ALL element gaps */
        .element-container, .stMarkdown, div[data-testid="stVerticalBlock"] > div {
            margin: 0 !important;
            padding: 0 !important;
            gap: 0 !important;
        }
        
        /* ===== TOP NAVIGATION BAR ===== */
        .top-nav {
            background: rgba(26, 26, 26, 0.95);
            padding: 15px 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            width: 100vw;
            margin-left: calc(-50vw + 50%);
        }
        
        .nav-logo-text {
            font-size: 24px;
            font-weight: 800;
            color: #d4af37;
            text-transform: uppercase;
        }
        
        /* ===== NAVIGATION BUTTONS SECTION ===== */
        .nav-buttons-wrapper {
            background: rgba(26, 26, 26, 0.95);
            padding: 10px 60px;
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            margin-top: 0;
            margin-bottom: 0;
        }
        
        /* ===== HERO SECTION ===== */
        .hero {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920') center/cover;
            padding: 40px 60px 60px 60px;
            min-height: 380px;
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            margin-top: 0;
            margin-bottom: 0;
        }
        
        .hero h1 {
            color: white;
            font-size: 64px;
            font-weight: 800;
            margin: 0 0 10px 0;
            line-height: 1.0;
            letter-spacing: -0.5px;
        }
        
        .hero h2 {
            color: #d4af37;
            font-size: 40px;
            font-weight: 700;
            margin: 0 0 18px 0;
            line-height: 1.0;
        }
        
        .hero p {
            color: rgba(255,255,255,0.95);
            font-size: 17px;
            max-width: 800px;
            line-height: 1.55;
            margin: 0;
        }
    </style>
    
    <div class='top-nav'>
        <span class='nav-logo-text'>T21 SERVICES</span>
        <div class='nav-menu' style='gap:0;'></div>
        <div>
            <a href='#login' style='background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border-radius: 25px; font-weight: 800; text-decoration: none; text-transform: uppercase; font-size: 14px;'>LOGIN / REGISTER</a>
        </div>
    </div>
    
    <!-- hero moved below as a separate Streamlit block -->
    """, unsafe_allow_html=True)
    
    # Top navigation buttons (Streamlit for smooth navigation)
    st.markdown("""<div class='nav-buttons-wrapper'>""", unsafe_allow_html=True)
    
    nb1, nb2, nb3, nb4, nb5, nb6 = st.columns(6)
    with nb1:
        if st.button("📋 ABOUT", key="top_about", use_container_width=True):
            st.switch_page("pages/about.py")
    with nb2:
        if st.button("🛠️ SERVICES", key="top_services", use_container_width=True):
            st.switch_page("pages/services.py")
    with nb3:
        if st.button("💰 PRICING", key="top_pricing", use_container_width=True):
            st.switch_page("pages/pricing.py")
    with nb4:
        if st.button("📞 CONTACT", key="top_contact", use_container_width=True):
            st.switch_page("pages/contact_us.py")
    with nb5:
        if st.button("🏠 HOME", key="top_home", use_container_width=True, type="primary"):
            st.switch_page("app.py")
    with nb6:
        if st.button("🏛️ PROCUREMENT", key="top_procurement", use_container_width=True):
            st.switch_page("pages/procurement.py")
    st.markdown("</div>", unsafe_allow_html=True)

    # Hero section (professional, zero-gap)
    st.markdown("""
    <div class='hero'>
        <h1>Your NHS Career & Workforce Partner</h1>
        <h2>Training • Talent • Technology</h2>
        <p>UK Certified Centre serving individuals seeking NHS careers, NHS staff advancing their skills, and NHS trusts 
        transforming operations. TQUK-endorsed training, job application support with proven success, 
        and AI automation saving £2M+ annually. From student to system—we empower everyone.</p>
    </div>
    """, unsafe_allow_html=True)

    # Login buttons section
    st.markdown("<div id='login'></div>", unsafe_allow_html=True)
    st.markdown("## 🔐 Login or Register")
    st.markdown("*Select your portal to access the platform*")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 2])
    
    with col2:
        if st.button("🎓 STUDENT LOGIN / REGISTER", key="student_login_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/student_login.py")
    
    with col3:
        if st.button("👥 STAFF LOGIN / REGISTER", key="staff_login_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/staff_login.py")
    
    with col4:
        if st.button("🏥 NHS LOGIN / REGISTER", key="nhs_login_btn", use_container_width=True, type="primary"):
            st.switch_page("pages/nhs_login.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trust Badges
    st.markdown("""
    <div style='display: flex; gap: 20px; justify-content: center; padding: 60px 0; background: #f8f9fa; margin: 0 -70px; flex-wrap: wrap;'>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700; color: #1a1a1a;'>✅ TQUK APPROVED<br>CENTRE</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700; color: #1a1a1a;'>🔒 CYBER ESSENTIALS<br>CERTIFIED</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700; color: #1a1a1a;'>🏥 NHS<br>COMPLIANT</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700; color: #1a1a1a;'>✅ COMPANIES HOUSE<br>REGISTERED</div>
        <div style='background: white; padding: 25px 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; font-weight: 700; color: #1a1a1a;'>🇬🇧 UK<br>BASED</div>
    </div>
    """, unsafe_allow_html=True)
