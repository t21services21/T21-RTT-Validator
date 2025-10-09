"""
T21 SERVICES - SIDEBAR MANAGER
Dynamic sidebar that shows pages based on login status and user role
"""

import streamlit as st


def render_sidebar():
    """Render sidebar with appropriate pages based on login status"""
    
    # Check if user is logged in
    is_logged_in = st.session_state.get('logged_in', False)
    user_role = st.session_state.get('user_role', 'trial')
    user_type = st.session_state.get('user_type', 'student')
    
    with st.sidebar:
        # Logo and branding
        st.markdown("# 🏥 T21 Services")
        st.markdown("Healthcare Intelligence Platform")
        st.markdown("---")
        
        if not is_logged_in:
            # PUBLIC PAGES ONLY (before login)
            st.markdown("### 🔐 Login Options")
            st.caption("Please select your portal:")
            
            if st.button("🎓 Student Login", use_container_width=True, type="primary"):
                st.switch_page("pages/student_login.py")
            
            if st.button("👥 Staff Login", use_container_width=True):
                st.switch_page("pages/staff_login.py")
            
            if st.button("🏥 NHS Login", use_container_width=True):
                st.switch_page("pages/nhs_login.py")
            
            st.markdown("---")
            st.markdown("### ℹ️ Information")
            
            if st.button("📧 Contact Us", use_container_width=True):
                try:
                    st.switch_page("pages/contact_us.py")
                except:
                    st.info("Contact: info@t21services.co.uk")
            
            if st.button("📜 Terms of Service", use_container_width=True):
                try:
                    st.switch_page("pages/terms_of_service.py")
                except:
                    pass
            
            if st.button("🔒 Privacy Policy", use_container_width=True):
                try:
                    st.switch_page("pages/privacy_policy.py")
                except:
                    pass
            
            # Helpful message
            st.markdown("---")
            st.info("👆 Login above to access:\n\n✅ Training Platform\n✅ Clinical Tools\n✅ Certification Programs")
        
        else:
            # ============================================
            # LOGGED IN USERS ONLY
            # ============================================
            
            # Show user info
            user_email = st.session_state.get('user_email', 'User')
            user_name = st.session_state.get('user_license')
            if user_name and hasattr(user_name, 'full_name'):
                display_name = user_name.full_name
            else:
                display_name = user_email.split('@')[0]
            
            st.success(f"👤 {display_name}")
            
            st.markdown("---")
            st.markdown("### 🏠 Main")
            
            if st.button("📊 Dashboard", use_container_width=True, type="primary"):
                st.switch_page("app.py")
            
            st.markdown("---")
            st.markdown("### 🏥 Clinical Tools")
            
            if st.button("🏥 RTT Clinical Validator", use_container_width=True):
                st.switch_page("pages/rtt_clinical_validator.py")
            
            if st.button("📊 Pathway Validator", use_container_width=True):
                st.switch_page("pages/pathway_validator.py")
            
            if st.button("📅 Appointment System", use_container_width=True):
                st.switch_page("pages/appointment_system.py")
            
            st.markdown("---")
            st.markdown("### ⚙️ Settings")
            
            if st.button("🔐 2FA Security", use_container_width=True):
                st.switch_page("pages/2fa_setup.py")
            
            if st.button("👤 My Account", use_container_width=True):
                st.switch_page("app.py")
            
            # Admin/Staff only features
            if user_type in ['admin', 'staff']:
                st.markdown("---")
                st.markdown("### 🔧 Administration")
                
                if st.button("🏥 PAS Integration", use_container_width=True):
                    st.switch_page("pages/pas_integration_demo.py")
                
                if st.button("📊 Analytics", use_container_width=True):
                    st.switch_page("app.py")
                
                if st.button("👥 Users", use_container_width=True):
                    st.switch_page("app.py")
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                # Clear session
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("Logged out successfully!")
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("© 2025 T21 Services Limited")


def get_page_config():
    """Get recommended page config"""
    return {
        "page_title": "T21 Services",
        "page_icon": "🏥",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
