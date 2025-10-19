"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Staff & Partner Portal Login

For T21 Services Staff, Training Providers, and Authorized Partners
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin_management import load_users_db
from advanced_access_control import UserAccount
from auth_persistence import initialize_auth_session, save_auth_cookie
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
    <div style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                color: white; 
                padding: 6px 16px; 
                border-radius: 15px; 
                display: inline-block; 
                font-size: 14px;
                margin: 5px 0;'>
        👥 STAFF & PARTNER PORTAL
    </div>
    <h2 style='color: #e74c3c; margin: 8px 0;'>T21 Healthcare Intelligence Platform</h2>
    <p style='color: #666; font-size: 14px; margin: 0 0 10px 0;'>Authorized Personnel Only</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .login-header {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    .portal-badge {
        background: #d35400;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="login-header">
    <div class="portal-badge">👥 STAFF & PARTNER PORTAL</div>
    <h1>T21 Healthcare Intelligence Platform</h1>
    <p>Internal Staff & Authorized Partner Access</p>
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
        # CHECK IF 2FA PROMPT SHOULD SHOW (ONLY AFTER PASSWORD VERIFIED)
        if st.session_state.get('show_2fa_prompt'):
            # SHOW 2FA VERIFICATION INSTEAD OF LOGIN FORM
            st.markdown("### 🔐 Two-Factor Authentication Required")
            
            pending_user = st.session_state.get('pending_2fa_user')
            
            if pending_user:
                st.info(f"Please enter the 6-digit code from your authenticator app for **{pending_user.get('email')}**")
                
                two_fa_code = st.text_input("Enter 6-digit code:", max_chars=6, key="staff_2fa_code")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("✅ Verify & Login", type="primary", key="staff_verify_2fa", use_container_width=True):
                        if two_fa_code and len(two_fa_code) == 6:
                            from two_factor_auth import verify_2fa_code
                            
                            secret = pending_user.get('two_factor_secret')
                            
                            if verify_2fa_code(secret, two_fa_code):
                                # 2FA verified! Complete login
                                from supabase_database import update_user_last_login
                                
                                email = pending_user.get('email')
                                update_user_last_login(email)
                                
                                class SimpleUser:
                                    def __init__(self, data):
                                        self.email = data.get('email')
                                        self.full_name = data.get('full_name')
                                        self.role = data.get('role', 'staff')
                                        self.user_type = data.get('user_type', 'staff')
                                
                                user_obj = SimpleUser(pending_user)
                                
                                st.session_state.logged_in = True
                                st.session_state.user_license = user_obj
                                st.session_state.user_email = email
                                st.session_state.session_email = email
                                
                                # Save to cookie for persistent login (non-blocking)
                                try:
                                    save_auth_cookie(email, pending_user.get('password_hash'), pending_user)
                                except:
                                    pass  # Continue even if cookies fail
                                
                                # Clear 2FA prompt
                                st.session_state.show_2fa_prompt = False
                                st.session_state.pending_2fa_user = None
                                
                                st.success(f"✅ 2FA Verified! Welcome, {user_obj.full_name}!")
                                st.switch_page("app.py")
                            else:
                                st.error("❌ Invalid 2FA code. Please try again.")
                        else:
                            st.error("Please enter a 6-digit code")
                
                with col_b:
                    if st.button("🔙 Cancel", key="staff_cancel_2fa", use_container_width=True):
                        st.session_state.show_2fa_prompt = False
                        st.session_state.pending_2fa_user = None
                        st.rerun()
        
        else:
            # SHOW NORMAL LOGIN FORM (ONLY IF NOT IN 2FA MODE)
            st.markdown("### 🔐 Staff/Partner Login")
            st.warning("⚠️ This portal is restricted to authorized T21 Services staff, training providers, and approved partners only.")
            
            with st.form("staff_login"):
                email = st.text_input("Staff/Partner Email", placeholder="your.name@t21services.co.uk")
                password = st.text_input("Password", type="password")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    login_btn = st.form_submit_button("👥 Staff/Partner Login", type="primary", use_container_width=True)
                
                with col_b:
                    if st.form_submit_button("← Back to Main Page", use_container_width=True):
                        st.switch_page("app.py")
                
                if login_btn:
                    if email and password:
                        password_hash = hashlib.sha256(password.encode()).hexdigest()
                        require_supabase = str(st.secrets.get("REQUIRE_SUPABASE_LOGIN", "false")).lower() == "true"
                        login_source = None
                        
                        # Try Supabase first, but gracefully fall back if not available
                        supabase_user = None
                        try:
                            from supabase_database import get_user_by_email, update_user_last_login
                            try:
                                supabase_user = get_user_by_email(email)
                            except Exception:
                                supabase_user = None
                            
                            if supabase_user and supabase_user.get('password_hash') == password_hash:
                                user_type = supabase_user.get('user_type', 'student')
                                
                                if user_type in ['admin', 'staff', 'partner']:
                                    # Check if 2FA is enabled
                                    if supabase_user.get('two_factor_enabled'):
                                        # Store for 2FA verification
                                        st.session_state.pending_2fa_user = supabase_user
                                        st.session_state.show_2fa_prompt = True
                                        st.rerun()
                                    else:
                                        # No 2FA, proceed with login
                                        try:
                                            update_user_last_login(email)
                                        except Exception:
                                            pass
                                        
                                        class SimpleUser:
                                            def __init__(self, data):
                                                self.email = data.get('email')
                                                self.full_name = data.get('full_name')
                                                self.role = data.get('role', 'staff')
                                                self.user_type = data.get('user_type', 'staff')
                                        
                                        user_account = SimpleUser(supabase_user)
                                        
                                        st.session_state.logged_in = True
                                        st.session_state.user_license = user_account
                                        st.session_state.user_email = email
                                        st.session_state.session_email = email
                                        st.session_state.auth_source = "supabase"
                                        
                                        # Save to cookie for persistent login (non-blocking)
                                        try:
                                            save_auth_cookie(email, password_hash, supabase_user)
                                        except:
                                            pass  # Continue even if cookies fail
                                        
                                        st.switch_page("app.py")
                                else:
                                    st.error("❌ This portal is for staff/partners only")
                            elif supabase_user:
                                st.error("❌ Incorrect password")
                        except Exception:
                            supabase_user = None
                        
                        if not supabase_user:
                            if require_supabase:
                                st.error("❌ Supabase login is required. Please check Supabase credentials and user record.")
                            else:
                                users_db = load_users_db()
                                
                                if email in users_db:
                                    user_data = users_db[email]
                                    # Handle UserAccount object vs dict
                                    if hasattr(user_data, 'password_hash'):
                                        stored_hash = user_data.password_hash
                                    elif isinstance(user_data, dict):
                                        stored_hash = user_data.get('password_hash')
                                    else:
                                        stored_hash = None

                                    if stored_hash and stored_hash == password_hash:
                                        # Get user type from user_data
                                        if hasattr(user_data, 'user_type'):
                                            local_user_type = user_data.user_type
                                        elif isinstance(user_data, dict):
                                            local_user_type = user_data.get('user_type', 'student')
                                        else:
                                            local_user_type = 'student'
                                        
                                        # Check if user is staff/admin
                                        if local_user_type in ['admin', 'staff', 'partner']:
                                            st.session_state.logged_in = True
                                            st.session_state.user_license = user_data
                                            st.session_state.user_email = email
                                            st.session_state.auth_source = "local_json"
                                            
                                            # Save to cookie for persistent login
                                            user_dict = user_data if isinstance(user_data, dict) else {
                                                'email': email,
                                                'full_name': getattr(user_data, 'full_name', email),
                                                'role': getattr(user_data, 'role', 'staff'),
                                                'user_type': getattr(user_data, 'user_type', 'staff')
                                            }
                                            try:
                                                save_auth_cookie(email, password_hash, user_dict)
                                            except:
                                                pass  # Continue even if cookies fail
                                            
                                            st.success(f"✅ Welcome to Staff Portal!")
                                            st.switch_page("app.py")
                                        else:
                                            st.error("❌ Unauthorized access. This portal is for staff/partners only.")
                                    else:
                                        st.error("❌ Incorrect password")
                                else:
                                    st.error("❌ Account not found")
                else:
                    st.error("❌ Please enter both email and password")
        
        # Forgot Password Button
        st.markdown("---")
        if st.button("🔒 Forgot Password? Click Here to Reset", use_container_width=True, key="staff_forgot_btn"):
            st.session_state.show_staff_password_reset = True
            st.rerun()
        
        # Password Reset Form
        if st.session_state.get('show_staff_password_reset'):
            st.markdown("---")
            st.markdown("### 🔒 Reset Your Password")
            
            reset_email = st.text_input("Enter your staff email:", key="staff_reset_email")
            
            if 'staff_reset_step' not in st.session_state:
                st.session_state.staff_reset_step = 1
            
            if st.session_state.staff_reset_step == 1:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📧 Send Reset Code", type="primary", use_container_width=True, key="staff_send_code"):
                        if reset_email:
                            try:
                                from student_auth import request_password_reset
                                success, message = request_password_reset(reset_email)
                                if success:
                                    st.success(message)
                                    st.session_state.staff_reset_step = 2
                                    st.rerun()
                                else:
                                    st.error(message)
                            except:
                                st.error("Password reset not available. Contact admin@t21services.co.uk")
                        else:
                            st.warning("Please enter your email")
                with col2:
                    if st.button("← Cancel", use_container_width=True, key="staff_cancel_reset"):
                        st.session_state.show_staff_password_reset = False
                        st.session_state.staff_reset_step = 1
                        st.rerun()
            
            elif st.session_state.staff_reset_step == 2:
                st.info(f"✅ Reset code sent to {reset_email}")
                reset_code = st.text_input("6-digit code:", max_chars=6, key="staff_reset_code")
                new_password = st.text_input("New Password (min 8 chars):", type="password", key="staff_new_pass")
                confirm_password = st.text_input("Confirm Password:", type="password", key="staff_confirm_pass")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✅ Reset Password", type="primary", key="staff_do_reset"):
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
                                    st.session_state.staff_reset_step = 1
                                    st.session_state.show_staff_password_reset = False
                                    st.rerun()
                                else:
                                    st.error(message)
                            except:
                                st.error("Reset failed. Contact admin@t21services.co.uk")
                with col2:
                    if st.button("← Start Over", key="staff_reset_restart"):
                        st.session_state.staff_reset_step = 1
                        st.rerun()
                with col3:
                    if st.button("Cancel", key="staff_reset_cancel"):
                        st.session_state.show_staff_password_reset = False
                        st.session_state.staff_reset_step = 1
                        st.rerun()
            
            st.markdown("---")
        
        # Information section
        st.markdown("### 👥 Staff & Partner Access Includes:")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            **Administrative Tools:**
            - ✅ User Management
            - ✅ Course Management
            - ✅ School Administration
            - ✅ Module Access Control
            """)
        
        with col_b:
            st.markdown("""
            **Business Tools:**
            - ✅ Revenue & Analytics
            - ✅ Bulk Operations
            - ✅ Trial Automation
            - ✅ System Configuration
            """)
        
        st.markdown("---")
        
        # Access request info
        st.info("""
        **Need Staff/Partner Access?**
        
        **For T21 Services Staff:**
        Contact IT Department for account provisioning
        
        **For Training Providers/Partners:**
        📧 Email: partnerships@t21services.com  
        📞 Phone: [Your Phone]  
        
        Partnership applications reviewed within 3 business days
        """)
        
        # Security notice
        st.error("""
        **🔒 Security Notice**
        
        - All access attempts are logged and monitored
        - Unauthorized access attempts will be reported
        - Staff accounts must use company email addresses
        - 2FA may be required for sensitive operations
        """)
        
        # Footer
        st.caption("T21 Services Limited | Company No: 13091053 | 64 Upper Parliament Street, Liverpool, L8 7LF")
        st.caption("⚠️ Authorized Personnel Only | For support: it-support@t21services.com")
