"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Student Training Portal Login

For Students & Individual Learners
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from student_auth import login_student, register_student
from advanced_access_control import UserAccount
from auth_persistence import initialize_auth_session, save_auth_cookie
from supabase_database import update_user_last_login, get_user_by_email
from two_factor_auth import verify_2fa_code, use_backup_code
import hashlib


# Remove ALL spacing and center logo
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
    .block-container {padding-top: 1rem !important;}
    .main .block-container {padding-top: 1rem !important;}
</style>
""", unsafe_allow_html=True)

# Centered Logo at top
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image("assets/logo.png", width=100)
    except:
        st.markdown("### 🏥")

st.markdown("""
<div style='text-align: center; padding: 5px 0;'>
    <div style='background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); 
                color: white; 
                padding: 6px 16px; 
                border-radius: 15px; 
                display: inline-block; 
                font-size: 14px;
                margin: 5px 0;'>
        🎓 STUDENT TRAINING PORTAL
    </div>
    <h2 style='color: #27ae60; margin: 8px 0;'>T21 Healthcare Intelligence Platform</h2>
    <p style='color: #666; font-size: 14px; margin: 0 0 10px 0;'>Professional NHS Administration Training</p>
</div>
""", unsafe_allow_html=True)

# Initialize authentication (restore from cookie if available)
initialize_auth_session()

# Check if already logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    # Redirect to main app
    st.switch_page("app.py")
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Student Login", "📝 Register"])
        
        with tab1:
            st.markdown("### 🔐 Login to Training Portal")
            st.info("Access your training, scenarios, AI tutor, and certification exams")
            
            with st.form("student_login"):
                email = st.text_input("Email Address", placeholder="your.email@example.com")
                password = st.text_input("Password", type="password")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    login_btn = st.form_submit_button("🎓 Login to Training", type="primary", use_container_width=True)
                
                with col_b:
                    if st.form_submit_button("← Back to Main Page", use_container_width=True):
                        st.switch_page("app.py")
                
                if login_btn:
                    if email and password:
                        # Try Supabase first
                        try:
                            supabase_user = get_user_by_email(email)
                            
                            if supabase_user:
                                password_hash = hashlib.sha256(password.encode()).hexdigest()
                                
                                if supabase_user.get('password_hash') == password_hash:
                                    # Check if 2FA is enabled
                                    if supabase_user.get('two_factor_enabled'):
                                        # Store for 2FA verification
                                        st.session_state.pending_2fa_user = supabase_user
                                        st.session_state.show_2fa_prompt = True
                                        st.rerun()
                                    else:
                                        # No 2FA, proceed with login
                                        update_user_last_login(email)
                                        
                                        class SimpleUser:
                                            def __init__(self, data):
                                                self.email = data.get('email')
                                                self.full_name = data.get('full_name')
                                                self.role = data.get('role', 'trial')
                                                self.user_type = data.get('user_type', 'student')
                                        
                                        user_obj = SimpleUser(supabase_user)
                                        
                                        st.session_state.logged_in = True
                                        st.session_state.user_license = user_obj
                                        st.session_state.user_email = email
                                        st.session_state.session_email = email
                                        
                                        # Save to cookie for persistent login (non-blocking)
                                        try:
                                            save_auth_cookie(email, password_hash, supabase_user)
                                        except:
                                            pass  # Continue even if cookies fail
                                        
                                        st.success(f" Welcome back {user_obj.full_name}!")
                                        st.switch_page("app.py")
                                else:
                                    st.error(" Incorrect password")
                            else:
                                # Fall back to old student system
                                result = login_student(email, password)
                                
                                if result["success"]:
                                    st.session_state.logged_in = True
                                    st.session_state.user_license = result["license"]
                                    st.session_state.user_email = email
                                    
                                    # Save to cookie for persistent login (non-blocking)
                                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                                    user_dict = {'email': email, 'full_name': email, 'user_type': 'student', 'role': 'student'}
                                    try:
                                        save_auth_cookie(email, password_hash, user_dict)
                                    except:
                                        pass  # Continue even if cookies fail
                                    
                                    st.success(" Login successful! Welcome back!")
                                    st.switch_page("app.py")
                                else:
                                    st.error(f" {result['message']}")
                        except Exception as e:
                            # Fall back to old system
                            result = login_student(email, password)
                            
                            if result["success"]:
                                st.session_state.logged_in = True
                                st.session_state.user_license = result["license"]
                                st.session_state.user_email = email
                                
                                # Save to cookie for persistent login (non-blocking)
                                password_hash = hashlib.sha256(password.encode()).hexdigest()
                                user_dict = {'email': email, 'full_name': email, 'user_type': 'student', 'role': 'student'}
                                try:
                                    save_auth_cookie(email, password_hash, user_dict)
                                except:
                                    pass  # Continue even if cookies fail
                                
                                st.success(" Login successful! Welcome to T21 Healthcare Platform!")
                                st.switch_page("app.py")
                            else:
                                st.error(f" {result['message']}")
                    else:
                        st.error(" Please enter both email and password")
            
            # Forgot Password Button
            st.markdown("---")
            if st.button(" Forgot Password? Click Here to Reset", use_container_width=True):
                st.session_state.show_student_password_reset = True
                st.rerun()
            
            # Password Reset Form
            if st.session_state.get('show_student_password_reset'):
                st.markdown("---")
                st.markdown("### Reset Your Password")
                
                reset_email = st.text_input("Enter your email address:", key="student_reset_email")
                
                if 'student_reset_step' not in st.session_state:
                    st.session_state.student_reset_step = 1
                
                if st.session_state.student_reset_step == 1:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(" Send Reset Code", type="primary", use_container_width=True, key="student_send_code"):
                            if reset_email:
                                try:
                                    from student_auth import request_password_reset
                                    success, message = request_password_reset(reset_email)
                                    if success:
                                        st.success(message)
                                        st.session_state.student_reset_step = 2
                                        st.rerun()
                                    else:
                                        st.error(message)
                                except Exception as e:
                                    st.error(f"Password reset error: {str(e)}")
                                    st.error("Please contact admin@t21services.co.uk")
                            else:
                                st.warning("Please enter your email")
                    with col2:
                        if st.button(" Cancel", use_container_width=True, key="student_cancel_reset"):
                            st.session_state.show_student_password_reset = False
                            st.session_state.student_reset_step = 1
                            st.rerun()
                
                elif st.session_state.student_reset_step == 2:
                    st.info(f" Reset code sent to {reset_email}")
                    reset_code = st.text_input("6-digit code:", max_chars=6, key="student_reset_code")
                    new_password = st.text_input("New Password (min 8 chars):", type="password", key="student_new_pass")
                    confirm_password = st.text_input("Confirm Password:", type="password", key="student_confirm_pass")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(" Reset Password", type="primary", key="student_do_reset"):
                            if not (reset_code and new_password and confirm_password):
                                st.warning("Fill all fields")
                            elif new_password != confirm_password:
                                st.error("Passwords don't match")
                            elif len(new_password) < 8:
                                st.error("Password must be 8+ characters")
                            else:
                                try:
                                    from student_auth import reset_password
                                    success, message = reset_password(reset_email, reset_code, new_password)
                                    if success:
                                        st.success(message)
                                        st.balloons()
                                        st.session_state.student_reset_step = 1
                                        st.session_state.show_student_password_reset = False
                                        st.rerun()
                                    else:
                                        st.error(message)
                                except:
                                    st.error("Reset failed. Contact admin@t21services.co.uk")
                    with col2:
                        if st.button(" Start Over", key="student_reset_restart"):
                            st.session_state.student_reset_step = 1
                            st.rerun()
                    with col3:
                        if st.button("Cancel", key="student_reset_cancel"):
                            st.session_state.show_student_password_reset = False
                            st.session_state.student_reset_step = 1
                            st.rerun()
            
            # 2FA Verification Prompt
            if st.session_state.get('show_2fa_prompt'):
                st.markdown("---")
                st.markdown("### Two-Factor Authentication Required")
                
                pending_user = st.session_state.get('pending_2fa_user')
                
                if pending_user:
                    st.info(f"Please enter the 6-digit code from your authenticator app for **{pending_user.get('email')}**")
                    
                    two_fa_code = st.text_input("Enter 6-digit code:", max_chars=6, key="student_2fa_code")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(" Verify & Login", type="primary", key="student_verify_2fa"):
                            if two_fa_code and len(two_fa_code) == 6:
                                secret = pending_user.get('two_factor_secret')
                                user_email = pending_user.get('email')
                                
                                if verify_2fa_code(secret, two_fa_code):
                                    update_user_last_login(user_email)
                                    
                                    class SimpleUser:
                                        def __init__(self, data):
                                            self.email = data.get('email')
                                            self.full_name = data.get('full_name')
                                            self.role = data.get('role', 'trial')
                                            self.user_type = data.get('user_type', 'student')
                                    
                                    user_obj = SimpleUser(pending_user)
                                    
                                    st.session_state.logged_in = True
                                    st.session_state.user_license = user_obj
                                    st.session_state.user_email = user_email
                                    st.session_state.session_email = user_email
                                    
                                    # Save to cookie for persistent login (non-blocking)
                                    try:
                                        save_auth_cookie(user_email, pending_user.get('password_hash'), pending_user)
                                    except:
                                        pass  # Continue even if cookies fail
                                    
                                    # Clear 2FA prompt
                                    st.session_state.show_2fa_prompt = False
                                    st.session_state.pending_2fa_user = None
                                    
                                    st.success(f" 2FA Verified! Welcome back!")
                                    st.switch_page("app.py")
                                else:
                                    st.error(" Invalid 2FA code. Please try again.")
                            else:
                                st.error("Please enter a 6-digit code")
                    
                    with col2:
                        if st.button("🔙 Use Backup Code", key="student_use_backup"):
                            st.session_state.show_backup_code_input = True
                            st.rerun()
                    
                    if st.session_state.get('show_backup_code_input'):
                        st.markdown("---")
                        st.warning("⚠️ Each backup code can only be used once")
                        backup_code = st.text_input("Enter backup code (XXXX-XXXX):", key="student_backup_code")
                        
                        if st.button("✅ Verify Backup Code", key="student_verify_backup"):
                            if backup_code:
                                user_email = pending_user.get('email')
                                if use_backup_code(user_email, backup_code):
                                    update_user_last_login(user_email)
                                    
                                    class SimpleUser:
                                        def __init__(self, data):
                                            self.email = data.get('email')
                                            self.full_name = data.get('full_name')
                                            self.role = data.get('role', 'trial')
                                            self.user_type = data.get('user_type', 'student')
                                    
                                    user_obj = SimpleUser(pending_user)
                                    
                                    st.session_state.logged_in = True
                                    st.session_state.user_license = user_obj
                                    st.session_state.user_email = user_email
                                    st.session_state.session_email = user_email
                                    
                                    st.session_state.show_2fa_prompt = False
                                    st.session_state.pending_2fa_user = None
                                    st.session_state.show_backup_code_input = False
                                    
                                    st.success(f"✅ Backup code verified! Welcome, {user_obj.full_name}!")
                                    st.switch_page("app.py")
                                else:
                                    st.error("❌ Invalid backup code")
                            else:
                                st.error("Please enter a backup code")
        
        with tab2:
            st.markdown("### 📝 Create Student Account")
            st.success("Start your NHS administration career training today!")
            
            with st.form("student_register"):
                st.markdown("**Personal Information:**")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    first_name = st.text_input("First Name*", placeholder="John")
                    last_name = st.text_input("Last Name*", placeholder="Smith")
                
                with col_b:
                    email_reg = st.text_input("Email Address*", placeholder="john.smith@example.com")
                    phone = st.text_input("Phone Number", placeholder="07123456789")
                
                st.markdown("**Account Security:**")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    password_reg = st.text_input("Password*", type="password", help="Minimum 8 characters")
                
                with col_b:
                    password_confirm = st.text_input("Confirm Password*", type="password")
                
                st.markdown("**Training Details:**")
                
                role_interested = st.selectbox("Which NHS role are you interested in?", [
                    "RTT Validation Officer",
                    "Patient Pathway Navigator",
                    "Cancer Data Officer",
                    "Waiting List Coordinator",
                    "Appointment Administrator",
                    "Medical Secretary",
                    "Data Quality Officer",
                    "MDT Coordinator",
                    "Other/Undecided"
                ])
                
                license_type = st.selectbox("Choose Your Plan", [
                    "trial - 7-Day Free Trial",
                    "monthly - Monthly Subscription (£59/month)",
                    "annual - Annual Subscription (£599/year - Save 15%)"
                ])
                
                agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                
                register_btn = st.form_submit_button("📝 Create Account", type="primary", use_container_width=True)
                
                if register_btn:
                    if not agree_terms:
                        st.error("❌ Please agree to Terms of Service")
                    elif not first_name or not last_name or not email_reg or not password_reg:
                        st.error("❌ Please fill all required fields")
                    elif password_reg != password_confirm:
                        st.error("❌ Passwords do not match")
                    elif len(password_reg) < 8:
                        st.error("❌ Password must be at least 8 characters")
                    else:
                        role = license_type.split(" - ")[0]
                        student_name = f"{first_name} {last_name}"
                        
                        result = register_student(
                            email=email_reg,
                            password=password_reg,
                            student_name=student_name,
                            role=role
                        )
                        
                        if result["success"]:
                            st.success("✅ Account created successfully!")
                            st.success("Please login using the Login tab")
                            st.balloons()
                        else:
                            st.error(f"❌ {result['message']}")
        
        st.markdown("---")
        
        # Features section
        st.markdown("### 🎓 Student Training Includes:")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            **Hands-On Training:**
            - ✅ 188 Real-World Scenarios
            - ✅ 15+ NHS Role Training
            - ✅ AI Tutor 24/7
            - ✅ Interactive Learning
            """)
        
        with col_b:
            st.markdown("""
            **Career Support:**
            - ✅ Professional Certification
            - ✅ Job Interview Prep
            - ✅ CV Builder
            - ✅ Progress Tracking
            """)
        
        st.markdown("---")
        
        # Pricing info
        st.success("""
        **💰 Student Pricing:**
        
        - **Free 7-Day Trial** - Full access, no credit card required
        - **Monthly:** £59/month - Cancel anytime
        - **Annual:** £599/year - Save 15% (£100 off!)
        
        🎉 **Launch Offer:** First 100 students get 50% off! Use code LAUNCH50
        """)
        
        # Contact info
        st.info("""
        **Questions? We're here to help!**
        
        📧 Email: student-support@t21services.com  
        💬 Live Chat: Available on website  
        📞 Phone: [Your Phone]
        """)
        
        # Footer
        st.caption("T21 Services Limited | Company No: 13091053 | 64 Upper Parliament Street, Liverpool, L8 7LF")
