"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Welcome / Landing Page
"""

import streamlit as st
import sys
import os

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Custom sidebar
try:
    from sidebar_manager import render_sidebar
    render_sidebar()
except:
    pass

# Hero Section
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 60px 20px; 
            border-radius: 15px; 
            text-align: center; 
            color: white; 
            margin-bottom: 40px;'>
    <h1 style='font-size: 48px; margin: 0;'>🏥 T21 Healthcare Intelligence Platform</h1>
    <p style='font-size: 24px; margin: 20px 0 0 0;'>Complete NHS Healthcare Administration Training & Operations Suite</p>
    <p style='font-size: 18px; margin: 10px 0 0 0; opacity: 0.9;'>Training + Automation | AI-Powered | 188 Scenarios</p>
</div>
""", unsafe_allow_html=True)

# Check if logged in
is_logged_in = st.session_state.get('logged_in', False)

if not is_logged_in:
    # NOT LOGGED IN - Show marketing content
    st.markdown("## 🎯 Transform Your NHS Career")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎓 TQUK Certified
        **Official Qualification**
        - Ofqual-regulated
        - NHS-recognized
        - 8-week program
        - Industry standard
        """)
    
    with col2:
        st.markdown("""
        ### 🏥 Hands-On Practice
        **Real Clinical Tools**
        - RTT Clinical Validator
        - Pathway Management
        - Appointment Systems
        - Live scenarios
        """)
    
    with col3:
        st.markdown("""
        ### 🤖 AI-Powered
        **24/7 Learning**
        - Unlimited AI tutor
        - Interactive scenarios
        - Instant feedback
        - Modern platform
        """)
    
    st.markdown("---")
    
    # Pricing Teasers
    st.markdown("## 💰 Choose Your Plan")
    
    pricing_col1, pricing_col2, pricing_col3 = st.columns(3)
    
    with pricing_col1:
        st.info("""
        ### 💰 Taster
        **£99 / 1 Month**
        
        ✅ Try the platform
        ✅ AI tutor (limited)
        ✅ Sample scenarios
        
        Perfect for testing!
        """)
    
    with pricing_col2:
        st.success("""
        ### ⭐ Full Access
        **£499 / 6 Months**
        
        ✅ Unlimited AI tutor
        ✅ All hands-on tools
        ✅ Full scenarios
        
        Best for practice!
        """)
    
    with pricing_col3:
        st.warning("""
        ### 🏆 Certified
        **£1,299 / 12 Months**
        
        ✅ TQUK Certification
        ✅ Live tutors
        ✅ Job support
        
        Get qualified!
        """)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("""
    <div style='background: #f0f2f6; padding: 30px; border-radius: 10px; text-align: center;'>
        <h2>🚀 Ready to Start Your NHS Career?</h2>
        <p style='font-size: 18px;'>Login to access the platform or contact us for more information</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Login buttons (centered)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col2:
        if st.button("🎓 Student Login", use_container_width=True, type="primary"):
            st.switch_page("pages/student_login.py")
    
    with col3:
        if st.button("👥 Staff Login", use_container_width=True):
            st.switch_page("pages/staff_login.py")
    
    with col4:
        if st.button("🏥 NHS Login", use_container_width=True):
            st.switch_page("pages/nhs_login.py")

else:
    # LOGGED IN - Redirect to dashboard
    st.info("Redirecting to dashboard...")
    st.switch_page("app.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>T21 Services Limited</strong> | Company No: 13091053 | Liverpool, England</p>
    <p>🌐 www.t21services.co.uk | 📧 info@t21services.co.uk</p>
    <p>Trusted by NHS Trusts, Training Providers, and Healthcare Professionals</p>
</div>
""", unsafe_allow_html=True)
