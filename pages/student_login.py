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

st.set_page_config(
    page_title="Student Training Portal | T21 Healthcare Intelligence",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .login-header {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    .portal-badge {
        background: #1abc9c;
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
    <div class="portal-badge">🎓 STUDENT TRAINING PORTAL</div>
    <h1>T21 Healthcare Intelligence Platform</h1>
    <p>Professional NHS Administration Training</p>
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
                        st.switch_page("landing_page.py")
                
                if login_btn:
                    if email and password:
                        import hashlib
                        
                        # Try Supabase first
                        try:
                            from supabase_database import get_user_by_email, update_user_last_login
                            supabase_user = get_user_by_email(email)
                            
                            if supabase_user:
                                password_hash = hashlib.sha256(password.encode()).hexdigest()
                                
                                if supabase_user.get('password_hash') == password_hash:
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
                                    
                                    st.success(f"✅ Welcome back {user_obj.full_name}!")
                                    st.switch_page("app.py")
                                else:
                                    st.error("❌ Incorrect password")
                            else:
                                # Fall back to old student system
                                result = login_student(email, password)
                                
                                if result["success"]:
                                    st.session_state.logged_in = True
                                    st.session_state.user_license = result["license"]
                                    st.session_state.user_email = email
                                    
                                    st.success(f"✅ Welcome back {result['student_name']}!")
                                    st.switch_page("app.py")
                                else:
                                    st.error(f"❌ {result['message']}")
                        except Exception as e:
                            # Fall back to old system
                            result = login_student(email, password)
                            
                            if result["success"]:
                                st.session_state.logged_in = True
                                st.session_state.user_license = result["license"]
                                st.session_state.user_email = email
                                
                                st.success(f"✅ Welcome back {result['student_name']}!")
                                st.switch_page("app.py")
                            else:
                                st.error(f"❌ {result['message']}")
                    else:
                        st.error("❌ Please enter both email and password")
        
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
