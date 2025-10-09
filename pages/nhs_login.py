"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
NHS/Organization Portal Login

For NHS Trusts, Hospitals, and Healthcare Organizations
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from student_auth import login_student
from admin_management import load_users_db
from advanced_access_control import UserAccount
import hashlib

st.set_page_config(
    page_title="NHS Organization Portal | T21 Healthcare Intelligence",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .login-header {
        background: linear-gradient(135deg, #2980b9 0%, #2c3e50 100%);
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    .portal-badge {
        background: #3498db;
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
    <div class="portal-badge">🏥 NHS ORGANIZATION PORTAL</div>
    <h1>T21 Healthcare Intelligence Platform</h1>
    <p>NHS Trust & Healthcare Organization Access</p>
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
        st.markdown("### 🔐 Organization Login")
        st.info("This portal is for NHS trusts and healthcare organizations using our operational systems.")
        
        with st.form("nhs_login"):
            email = st.text_input("Organization Email", placeholder="your.name@trust.nhs.uk")
            password = st.text_input("Password", type="password")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                login_btn = st.form_submit_button("🏥 Login to Organization Portal", type="primary", use_container_width=True)
            
            with col_b:
                if st.form_submit_button("← Back to Main Page", use_container_width=True):
                    st.switch_page("landing_page.py")
            
            if login_btn:
                if email and password:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    
                    # Try Supabase first
                    try:
                        from supabase_database import get_user_by_email, update_user_last_login
                        supabase_user = get_user_by_email(email)
                        
                        if supabase_user and supabase_user.get('password_hash') == password_hash:
                            user_type = supabase_user.get('user_type', 'student')
                            
                            if user_type in ['admin', 'staff', 'nhs_user']:
                                update_user_last_login(email)
                                
                                class SimpleUser:
                                    def __init__(self, data):
                                        self.email = data.get('email')
                                        self.full_name = data.get('full_name')
                                        self.role = data.get('role', 'nhs_user')
                                        self.user_type = data.get('user_type', 'nhs_user')
                                
                                user_account = SimpleUser(supabase_user)
                                
                                st.session_state.logged_in = True
                                st.session_state.user_license = user_account
                                st.session_state.user_email = email
                                
                                st.success(f"✅ Welcome to NHS Organization Portal, {user_account.full_name}!")
                                st.switch_page("app.py")
                            else:
                                st.error("❌ This portal is for NHS organizations only. Students should use the Training Portal.")
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
                                    user_type = user_data.get('user_type', 'student') if isinstance(user_data, dict) else getattr(user_data, 'user_type', 'student')
                                    
                                    if user_type in ['admin', 'staff', 'nhs_user']:
                                        st.session_state.logged_in = True
                                        st.session_state.user_license = user_data
                                        st.session_state.user_email = email
                                        
                                        st.success(f"✅ Welcome to NHS Organization Portal!")
                                        st.switch_page("app.py")
                                    else:
                                        st.error("❌ This portal is for NHS organizations only. Students should use the Training Portal.")
                                else:
                                    st.error("❌ Incorrect password")
                            else:
                                st.error("❌ Organization account not found")
                    except Exception as e:
                        st.error(f"❌ Login error. Please try the main app login page.")
                else:
                    st.error("❌ Please enter both email and password")
        
        st.markdown("---")
        
        # Information section
        st.markdown("### 🏥 NHS Organization Access Includes:")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            **Operational Systems:**
            - ✅ RTT & Pathway Management
            - ✅ Cancer Pathway Tracking
            - ✅ MDT Coordination
            - ✅ Appointment Systems
            """)
        
        with col_b:
            st.markdown("""
            **Additional Features:**
            - ✅ Medical Secretary AI
            - ✅ Data Quality Tools
            - ✅ Admin Dashboards
            - ✅ Reporting & Analytics
            """)
        
        st.markdown("---")
        
        # Contact info
        st.info("""
        **Need NHS Organization Access?**
        
        📧 Email: sales@t21services.com  
        📞 Phone: [Your Phone]  
        🌐 Website: www.t21services.com
        
        We offer FREE 90-day pilots for NHS trusts!
        """)
        
        # Footer
        st.caption("T21 Services Limited | Company No: 13091053 | 64 Upper Parliament Street, Liverpool, L8 7LF")
