"""
T21 SERVICES - PROFESSIONAL LANDING PAGE
"""

import streamlit as st

def render_clean_landing_page():
    """Professional landing page with hero image"""
    
    st.markdown("""
    <style>
        /* Complete reset - force edge-to-edge */
        html, body {overflow-x: hidden; margin: 0; padding: 0;}
        [data-testid="stSidebar"] {display: none !important;}
        header[data-testid="stHeader"] {display: none !important;}
        .main, .main .block-container, .stApp {
            padding: 0 !important;
            margin: 0 !important;
            margin-top: -80px !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        
        /* True full-width navigation */
        .top-nav {
            background: #1a1a1a;
            padding: 15px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            box-sizing: border-box;
            position: relative;
            margin: 0;
        }
        .logo {font-size: 24px; font-weight: 800; color: #d4af37; text-transform: uppercase; letter-spacing: 1px;}
        
        /* Professional hero with proper centering */
        .hero-section {
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                        url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920') center/cover;
            padding: 60px 5% 70px;
            width: 100%;
            box-sizing: border-box;
            color: white;
            margin: 0;
        }
        .hero-content {
            max-width: 1200px;
            margin: 0;
        }
        .hero-section h1 {
            color: white;
            font-size: 52px;
            font-weight: 800;
            margin: 0 0 15px 0;
            line-height: 1.1;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            letter-spacing: -0.5px;
        }
        .hero-section h2 {
            color: #f4d03f;
            font-size: 34px;
            font-weight: 700;
            margin: 0 0 25px 0;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        .hero-section p {
            font-size: 17px;
            max-width: 900px;
            margin: 0;
            line-height: 1.7;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            font-weight: 400;
        }
    </style>
    
    <div class="top-nav">
        <span class="logo">T21 SERVICES</span>
        <a href="#login" style="background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border-radius: 25px; font-weight: 800; text-decoration: none; text-transform: uppercase; font-size: 14px;">LOGIN / REGISTER</a>
    </div>
    
    <div class="hero-section">
        <div class="hero-content">
            <h1>Your NHS Career & Workforce Partner</h1>
            <h2>Training • Talent • Technology</h2>
            <p>UK Certified Centre serving individuals seeking NHS careers, NHS staff advancing their skills, and NHS trusts transforming operations. TQUK-endorsed training, job application support with proven success, and AI automation saving £2M+ annually.</p>
        </div>
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
