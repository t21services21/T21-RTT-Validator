"""
T21 SERVICES - PROFESSIONAL LANDING PAGE
"""

import streamlit as st

def render_clean_landing_page():
    """Professional landing page with hero image"""
    
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        header[data-testid="stHeader"] {display: none;}
        .main .block-container {padding: 0; margin-top: -80px; max-width: 100%;}
        
        .top-nav {
            background: #1a1a1a;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: -5rem -5rem 0 -5rem;
        }
        .logo {font-size: 24px; font-weight: 800; color: #d4af37; text-transform: uppercase;}
        
        .hero-section {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920') center/cover;
            padding: 45px 40px 50px;
            margin: 0 -5rem;
            color: white;
        }
        .hero-section h1 {
            color: white; 
            font-size: 56px; 
            font-weight: 800; 
            margin: 0 0 12px 0; 
            line-height: 1.1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .hero-section h2 {
            color: #d4af37; 
            font-size: 36px; 
            font-weight: 700; 
            margin: 0 0 20px 0; 
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .hero-section p {
            font-size: 16px; 
            max-width: 850px; 
            margin: 0;
            line-height: 1.6;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
        }
    </style>
    
    <div class="top-nav">
        <span class="logo">T21 SERVICES</span>
        <a href="#login" style="background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border-radius: 25px; font-weight: 800; text-decoration: none; text-transform: uppercase; font-size: 14px; cursor: pointer;" onclick="document.getElementById('login').scrollIntoView({behavior: 'smooth'});">LOGIN / REGISTER</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown('<div style="background: #1a1a1a; padding: 10px 40px; margin: 0 -5rem;">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <h1>Your NHS Career & Workforce Partner</h1>
        <h2>Training • Talent • Technology</h2>
        <p><strong>COMPLETE NHS SOLUTION:</strong> Train individuals seeking NHS careers + Upskill existing NHS staff with TQUK certification • Supply qualified talent to NHS trusts • AI automation saving £2M+ per trust. 120x faster validation • 99.9% accuracy • Zero breaches. Training, talent supply, and technology transformation - your one-stop NHS workforce solution.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div id="login"></div>', unsafe_allow_html=True)
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
    
    # Forgot Password Button
    st.markdown("<br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if st.button("🔒 Forgot Password? Click Here to Reset", use_container_width=True):
            st.session_state.show_password_reset = True
            st.rerun()
    
    # Password Reset Form
    if st.session_state.get('show_password_reset'):
        st.markdown("---")
        st.markdown("### 🔒 Password Reset")
        st.caption("Enter your email address to receive a password reset code")
        
        reset_email = st.text_input("Email Address", key="landing_reset_email")
        
        if 'reset_step' not in st.session_state:
            st.session_state.reset_step = 1
        
        if st.session_state.reset_step == 1:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📧 Send Reset Code", type="primary", use_container_width=True):
                    if reset_email:
                        try:
                            from student_auth import request_password_reset
                            success, message = request_password_reset(reset_email)
                            if success:
                                st.success(message)
                                st.session_state.reset_step = 2
                                st.rerun()
                            else:
                                st.error(message)
                        except:
                            st.error("Password reset functionality not available. Please contact admin@t21services.co.uk")
                    else:
                        st.warning("Please enter your email address")
            with col2:
                if st.button("← Cancel", use_container_width=True):
                    st.session_state.show_password_reset = False
                    st.session_state.reset_step = 1
                    st.rerun()
        
        elif st.session_state.reset_step == 2:
            st.info(f"✅ Reset code sent to {reset_email}")
            reset_code = st.text_input("Enter 6-digit code:", max_chars=6, key="landing_reset_code")
            new_password = st.text_input("New Password (min 8 characters):", type="password", key="landing_new_pass")
            confirm_password = st.text_input("Confirm New Password:", type="password", key="landing_confirm_pass")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Reset Password", type="primary"):
                    if not (reset_code and new_password and confirm_password):
                        st.warning("Please fill all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(new_password) < 8:
                        st.error("Password must be at least 8 characters")
                    else:
                        try:
                            from student_auth import reset_password
                            success, message = reset_password(reset_email, reset_code, new_password)
                            if success:
                                st.success(message)
                                st.balloons()
                                st.session_state.reset_step = 1
                                st.session_state.show_password_reset = False
                                st.rerun()
                            else:
                                st.error(message)
                        except:
                            st.error("Password reset failed. Please contact admin@t21services.co.uk")
            with col2:
                if st.button("← Start Over"):
                    st.session_state.reset_step = 1
                    st.rerun()
            with col3:
                if st.button("Cancel"):
                    st.session_state.show_password_reset = False
                    st.session_state.reset_step = 1
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Revolutionary capabilities
    st.markdown("""
    <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-top: 3rem;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">🤖 AI-POWERED<br>AUTOMATION</div>
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">⚡ 120x FASTER<br>THAN MANUAL</div>
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">💰 £2M+ SAVINGS<br>PER TRUST</div>
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">✅ 99.9%<br>ACCURACY</div>
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">🏆 TQUK APPROVED<br>CENTRE #36257481088</div>
        <div style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">🚀 FUTURE-PROOF<br>100 YEARS</div>
    </div>
    """, unsafe_allow_html=True)
