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

# Custom CSS
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
                    st.switch_page("landing_page.py")
            
            if login_btn:
                if email and password:
                    # Load admin/staff users database
                    users_db = load_users_db()
                    
                    if email in users_db:
                        user_data = users_db[email]
                        password_hash = hashlib.sha256(password.encode()).hexdigest()
                        
                        if user_data.get('password_hash') == password_hash:
                            # Check if user is staff/admin
                            user_type = user_data.get('user_type', 'student')
                            
                            if user_type in ['admin', 'staff', 'partner']:
                                user_account = UserAccount(
                                    email=email,
                                    user_type=user_data.get('user_type'),
                                    role=user_data.get('role'),
                                    modules_access=user_data.get('modules_access', [])
                                )
                                
                                st.session_state.logged_in = True
                                st.session_state.user_license = user_account
                                st.session_state.user_email = email
                                
                                st.success(f"✅ Welcome to Staff Portal!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Unauthorized access. This portal is for staff/partners only.")
                        else:
                            st.error("❌ Incorrect password")
                    else:
                        st.error("❌ Staff/Partner account not found. Please contact IT support.")
                else:
                    st.error("❌ Please enter both email and password")
        
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
