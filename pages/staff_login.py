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
import hashlib

st.set_page_config(
    page_title="Staff & Partner Portal | T21 Healthcare Intelligence",
    page_icon="👥",
    layout="wide"
)

# Hide default sidebar navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Compact Header with Logo
st.markdown("""
<div style='text-align: center; padding: 20px 0 10px 0;'>
    <img src="app/static/logo.png" width="100" style="margin-bottom: 10px;" onerror="this.style.display='none'">
    <div style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                color: white; 
                padding: 6px 16px; 
                border-radius: 15px; 
                display: inline-block; 
                font-size: 14px;
                margin-bottom: 8px;'>
        👥 STAFF & PARTNER PORTAL
    </div>
    <h2 style='color: #e74c3c; margin: 8px 0;'>T21 Healthcare Intelligence Platform</h2>
    <p style='color: #666; font-size: 14px; margin: 0;'>Authorized Personnel Only</p>
</div>
""", unsafe_allow_html=True)
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

# Check if already logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    # Redirect to main app
    st.switch_page("app.py")
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Staff/Partner Login")
        st.warning("⚠️ This portal is restricted to authorized T21 Services staff, training providers, and approved partners only.")
        
        with st.form("staff_login"):
            email = st.text_input("Staff/Partner Email", placeholder="your.name@t21services.com")
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
                    
                    # Try Supabase first
                    try:
                        from supabase_database import get_user_by_email, update_user_last_login
                        supabase_user = get_user_by_email(email)
                        
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
                                    update_user_last_login(email)
                                    
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
                                    
                                    st.success(f"✅ Welcome to Staff Portal, {user_account.full_name}!")
                                    st.switch_page("app.py")
                            else:
                                st.error("❌ This portal is for staff/partners only")
                        elif supabase_user:
                            st.error("❌ Incorrect password")
                        else:
                            # Fall back to old system
                            users_db = load_users_db()
                            
                            if email in users_db:
                                user_data = users_db[email]
                                
                                # Handle UserAccount object
                                if hasattr(user_data, 'password_hash'):
                                    stored_hash = user_data.password_hash
                                else:
                                    stored_hash = user_data.get('password_hash') if isinstance(user_data, dict) else None
                                
                                if stored_hash == password_hash:
                                    # Check if user is staff/admin
                                    user_type = user_data.get('user_type', 'student') if isinstance(user_data, dict) else getattr(user_data, 'user_type', 'student')
                                    
                                    if user_type in ['admin', 'staff', 'partner']:
                                        st.session_state.logged_in = True
                                        st.session_state.user_license = user_data
                                        st.session_state.user_email = email
                                        
                                        st.success(f"✅ Welcome to Staff Portal!")
                                        st.switch_page("app.py")
                                    else:
                                        st.error("❌ Unauthorized access. This portal is for staff/partners only.")
                                else:
                                    st.error("❌ Incorrect password")
                            else:
                                st.error("❌ Staff/Partner account not found. Please contact IT support.")
                    except Exception as e:
                        st.error(f"❌ Login error. Please try the main app login page.")
                else:
                    st.error("❌ Please enter both email and password")
        
        # 2FA Verification Prompt (same as main app)
        if st.session_state.get('show_2fa_prompt'):
            st.markdown("---")
            st.markdown("### 🔐 Two-Factor Authentication Required")
            
            pending_user = st.session_state.get('pending_2fa_user')
            
            if pending_user:
                st.info(f"Please enter the 6-digit code from your authenticator app for **{pending_user.get('email')}**")
                
                two_fa_code = st.text_input("Enter 6-digit code:", max_chars=6, key="staff_2fa_code")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Verify & Login", type="primary", key="staff_verify_2fa"):
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
                                
                                # Clear 2FA prompt
                                st.session_state.show_2fa_prompt = False
                                st.session_state.pending_2fa_user = None
                                
                                st.success(f"✅ 2FA Verified! Welcome, {user_obj.full_name}!")
                                st.switch_page("app.py")
                            else:
                                st.error("❌ Invalid 2FA code. Please try again.")
                        else:
                            st.error("Please enter a 6-digit code")
                
                with col2:
                    if st.button("🔙 Use Backup Code", key="staff_use_backup"):
                        st.session_state.show_backup_code_input = True
                        st.rerun()
                
                # Backup code option
                if st.session_state.get('show_backup_code_input'):
                    st.markdown("---")
                    st.warning("⚠️ Each backup code can only be used once")
                    backup_code = st.text_input("Enter backup code (XXXX-XXXX):", key="staff_backup_code")
                    
                    if st.button("✅ Verify Backup Code", key="staff_verify_backup"):
                        if backup_code:
                            from supabase_database import use_backup_code
                            
                            if use_backup_code(pending_user.get('email'), backup_code):
                                email = pending_user.get('email')
                                
                                from supabase_database import update_user_last_login
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
                                
                                st.session_state.show_2fa_prompt = False
                                st.session_state.pending_2fa_user = None
                                st.session_state.show_backup_code_input = False
                                
                                st.success(f"✅ Backup code verified! Welcome, {user_obj.full_name}!")
                                st.warning("⚠️ Consider regenerating backup codes in your account settings")
                                st.switch_page("app.py")
                            else:
                                st.error("❌ Invalid backup code")
                        else:
                            st.error("Please enter a backup code")
        
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
