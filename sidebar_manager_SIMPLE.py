"""
T21 SERVICES - SIMPLIFIED SIDEBAR MANAGER
Focus on CORE modules only - tested and working
"""

import streamlit as st


def render_sidebar():
    """Render sidebar with CORE modules only"""
    
    # Check if user is logged in
    is_logged_in = st.session_state.get('logged_in', False)
    user_role = st.session_state.get('user_role', 'trial')
    user_type = st.session_state.get('user_type', 'student')
    
    with st.sidebar:
        # Compact header styling
        st.markdown("""
        <style>
            section[data-testid="stSidebar"] > div:first-child {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            .sidebar-header {
                text-align: center;
                padding: 0;
                margin: 0 0 5px 0;
            }
            .sidebar-title {
                font-size: 14px;
                font-weight: 600;
                color: #1f1f1f;
                margin: 2px 0;
            }
            .sidebar-subtitle {
                font-size: 10px;
                color: #666;
                margin: 0 0 5px 0;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Logo - centered, compact
        col1, col2, col3 = st.columns([0.2, 2.6, 0.2])
        with col2:
            try:
                st.image("assets/logo.png", width=90)
            except:
                pass
        
        # Company name - compact
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">T21 Services Limited</div>
            <div class="sidebar-subtitle">Healthcare Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if not is_logged_in:
            # PUBLIC PAGES ONLY (before login)
            st.markdown("### 🔐 Login Options")
            st.caption("Please select your portal:")
            
            if st.button("🎓 Student Login", key="btn_student_login", use_container_width=True, type="primary"):
                st.switch_page("pages/student_login.py")
            
            if st.button("👥 Staff Login", key="btn_staff_login", use_container_width=True):
                st.switch_page("pages/staff_login.py")
            
            if st.button("🏥 NHS Login", key="btn_nhs_login", use_container_width=True):
                st.switch_page("pages/nhs_login.py")
            
            st.markdown("---")
            st.markdown("### ℹ️ Information")
            
            if st.button("📧 Contact Us", key="btn_contact", use_container_width=True):
                st.switch_page("pages/contact_us.py")
            
            if st.button("📜 Terms of Service", key="btn_terms", use_container_width=True):
                st.switch_page("pages/terms_of_service.py")
            
            if st.button("🔒 Privacy Policy", key="btn_privacy", use_container_width=True):
                st.switch_page("pages/privacy_policy.py")
            
            st.markdown("---")
            st.info("👆 Login above to access:\n\n✅ 7 Core Clinical Tools\n✅ Training Platform\n✅ Career Support")
        
        else:
            # ============================================
            # LOGGED IN USERS - CORE MODULES ONLY
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
            
            if st.button("📊 Dashboard", key="btn_dashboard", use_container_width=True, type="primary"):
                st.switch_page("app.py")
            
            # ============================================
            # CORE 7 AUTOMATION MODULES (TESTED & WORKING)
            # ============================================
            st.markdown("---")
            st.markdown("### 🏥 Core Clinical Tools")
            st.caption("7 automation modules - tested & ready")
            
            if st.button("📋 PTL - Patient Tracking", key="btn_ptl", use_container_width=True):
                st.session_state['selected_tool'] = "📋 PTL - Patient Tracking List"
                st.switch_page("app.py")
            
            if st.button("🤖 AI Auto-Validator", key="btn_ai_validator", use_container_width=True):
                st.session_state['selected_tool'] = "🤖 AI Auto-Validator"
                st.switch_page("app.py")
            
            if st.button("🎗️ Cancer Pathways", key="btn_cancer", use_container_width=True):
                st.session_state['selected_tool'] = "🎗️ Cancer Pathways"
                st.switch_page("app.py")
            
            if st.button("👥 MDT Coordination", key="btn_mdt", use_container_width=True):
                st.session_state['selected_tool'] = "👥 MDT Coordination"
                st.switch_page("app.py")
            
            if st.button("📅 Advanced Booking", key="btn_booking", use_container_width=True):
                st.session_state['selected_tool'] = "📅 Advanced Booking System"
                st.switch_page("app.py")
            
            if st.button("📧 Medical Secretary AI", key="btn_secretary", use_container_width=True):
                st.session_state['selected_tool'] = "📧 Medical Secretary AI"
                st.switch_page("app.py")
            
            if st.button("📊 Data Quality System", key="btn_data_quality", use_container_width=True):
                st.session_state['selected_tool'] = "📊 Data Quality System"
                st.switch_page("app.py")
            
            # ============================================
            # CORE TRAINING MODULES (TESTED & WORKING)
            # ============================================
            st.markdown("---")
            st.markdown("### 🎓 Training & Career")
            st.caption("Learn RTT & advance your career")
            
            if st.button("🎓 Training Library", key="btn_training", use_container_width=True):
                st.session_state['selected_tool'] = "🎓 Training Library"
                st.switch_page("app.py")
            
            if st.button("🎮 Interactive Learning", key="btn_interactive", use_container_width=True):
                st.session_state['selected_tool'] = "🎮 Interactive Learning Center"
                st.switch_page("app.py")
            
            if st.button("🤖 AI RTT Tutor", key="btn_ai_tutor", use_container_width=True):
                st.session_state['selected_tool'] = "🤖 AI RTT Tutor"
                st.switch_page("app.py")
            
            if st.button("🎓 Certification Exam", key="btn_certification", use_container_width=True):
                st.session_state['selected_tool'] = "🎓 Certification Exam"
                st.switch_page("app.py")
            
            if st.button("💼 Job Interview Prep", key="btn_interview", use_container_width=True):
                st.session_state['selected_tool'] = "💼 Job Interview Prep"
                st.switch_page("app.py")
            
            if st.button("📄 CV Builder", key="btn_cv", use_container_width=True):
                st.session_state['selected_tool'] = "📄 CV Builder"
                st.switch_page("app.py")
            
            # ============================================
            # SETTINGS & ADMIN
            # ============================================
            st.markdown("---")
            st.markdown("### ⚙️ Settings")
            
            if st.button("🔐 2FA Security", key="btn_2fa", use_container_width=True):
                st.switch_page("pages/security_2fa.py")
            
            if st.button("👤 My Account", key="btn_account", use_container_width=True):
                st.session_state['selected_tool'] = "⚙️ My Account & Upgrade"
                st.switch_page("app.py")
            
            # Admin/Staff only features
            if user_type in ['admin', 'staff']:
                st.markdown("---")
                st.markdown("### 🔧 Administration")
                
                if st.button("🔧 Admin Panel", key="btn_admin", use_container_width=True):
                    st.session_state['selected_tool'] = "🔧 Admin Panel"
                    st.switch_page("app.py")
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", key="btn_logout", use_container_width=True, type="secondary"):
                # Clear session
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("© 2025 T21 Services Limited")
        st.caption("🎯 Core modules only")


def get_page_config():
    """Get recommended page config"""
    return {
        "page_title": "T21 Services",
        "page_icon": "🏥",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
