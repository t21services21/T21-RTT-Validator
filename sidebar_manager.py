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
        # Aggressive spacing removal
        st.markdown("""
        <style>
            /* Remove ALL top padding */
            section[data-testid="stSidebar"] > div:first-child {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            section[data-testid="stSidebar"] .block-container {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            /* Compact header */
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
            
            if st.button("📊 Dashboard", key="btn_dashboard", use_container_width=True, type="primary"):
                st.switch_page("app.py")
            
            st.markdown("---")
            st.markdown("### 🏥 Clinical Tools")
            
            if st.button("🏥 RTT Clinical Validator", key="btn_rtt_validator", use_container_width=True):
                st.switch_page("pages/rtt_clinical_validator.py")
            
            if st.button("📊 Pathway Validator", key="btn_pathway_validator", use_container_width=True):
                st.switch_page("pages/pathway_validator.py")
            
            if st.button("📅 Appointment System", key="btn_appointments", use_container_width=True):
                st.switch_page("pages/appointment_system.py")
            
            # NEW CLINICAL MODULES WITH CRUD
            st.markdown("---")
            st.markdown("### 📋 Patient Management")
            
            if st.button("📵 DNA Management", key="btn_dna", use_container_width=True):
                st.switch_page("pages/dna_management.py")
            
            if st.button("❌ Cancellation Management", key="btn_cancellation", use_container_width=True):
                st.switch_page("pages/cancellation_management.py")
            
            if st.button("🎯 Patient Choice & Deferrals", key="btn_patient_choice", use_container_width=True):
                st.switch_page("pages/patient_choice.py")
            
            if st.button("📋 Waiting List Validator", key="btn_waiting_list", use_container_width=True):
                st.switch_page("pages/waiting_list_validator.py")
            
            if st.button("🔄 Transfer of Care", key="btn_transfer", use_container_width=True):
                st.switch_page("pages/transfer_of_care.py")
            
            if st.button("⚕️ Clinical Exceptions", key="btn_clinical_exceptions", use_container_width=True):
                st.switch_page("pages/clinical_exceptions.py")
            
            if st.button("📊 Capacity Planner", key="btn_capacity", use_container_width=True):
                st.switch_page("pages/capacity_planner.py")
            
            if st.button("✍️ Consent Manager", key="btn_consent", use_container_width=True):
                st.switch_page("pages/consent_manager.py")
            
            st.markdown("---")
            st.markdown("### 📊 Reporting & Admin")
            
            if st.button("📈 Commissioner Reporting", key="btn_commissioner", use_container_width=True):
                st.switch_page("pages/commissioner_reporting.py")
            
            if st.button("📜 Audit Trail", key="btn_audit", use_container_width=True):
                st.switch_page("pages/audit_trail.py")
            
            if st.button("💬 Communications Tracker", key="btn_communications", use_container_width=True):
                st.switch_page("pages/communications_tracker.py")
            
            if st.button("💰 Funding & IFR", key="btn_funding", use_container_width=True):
                st.switch_page("pages/funding_ifr.py")
            
            st.markdown("---")
            st.markdown("### 🚀 Advanced Features")
            
            if st.button("📱 Mobile App Preview", key="btn_mobile", use_container_width=True):
                st.switch_page("pages/mobile_app_preview.py")
            
            if st.button("📊 Executive Dashboard", key="btn_executive", use_container_width=True):
                st.switch_page("pages/executive_dashboard.py")
            
            if st.button("🎤 Voice AI Interface", key="btn_voice", use_container_width=True):
                st.switch_page("pages/voice_ai_interface.py")
            
            if st.button("🔗 PAS Integration", key="btn_pas_integration", use_container_width=True):
                st.switch_page("pages/pas_integration.py")
            
            if st.button("👤 Patient Portal", key="btn_patient_portal", use_container_width=True):
                st.switch_page("pages/patient_portal.py")
            
            if st.button("📝 AI Documentation", key="btn_ai_docs", use_container_width=True):
                st.switch_page("pages/ai_documentation.py")
            
            if st.button("🔐 Blockchain Audit", key="btn_blockchain", use_container_width=True):
                st.switch_page("pages/blockchain_audit.py")
            
            if st.button("🤖 Predictive AI", key="btn_predictive", use_container_width=True):
                st.switch_page("pages/predictive_ai.py")
            
            if st.button("🌍 National Benchmarking", key="btn_benchmarking", use_container_width=True):
                st.switch_page("pages/national_benchmarking.py")
            
            if st.button("🎓 Student Progress Monitor", key="btn_student_progress", use_container_width=True):
                st.switch_page("pages/student_progress_monitor.py")
            
            st.markdown("---")
            st.markdown("### 🎓 Training & Learning")
            
            if st.button("💼 Job Interview Prep", key="btn_interview", use_container_width=True):
                st.session_state['selected_tool'] = "💼 Job Interview Prep"
                st.switch_page("app.py")
            
            if st.button("📄 CV Builder", key="btn_cv", use_container_width=True):
                st.session_state['selected_tool'] = "📄 CV Builder"
                st.switch_page("app.py")
            
            if st.button("🎓 Training Library", key="btn_training", use_container_width=True):
                st.session_state['selected_tool'] = "🎓 Training Library"
                st.switch_page("app.py")
            
            if st.button("🎮 Interactive Learning Center", key="btn_interactive", use_container_width=True):
                st.session_state['selected_tool'] = "🎮 Interactive Learning Center"
                st.switch_page("app.py")
            
            if st.button("🤖 AI RTT Tutor", key="btn_ai_tutor", use_container_width=True):
                st.session_state['selected_tool'] = "🤖 AI RTT Tutor"
                st.switch_page("app.py")
            
            if st.button("🎓 Certification Exam", key="btn_certification", use_container_width=True):
                st.session_state['selected_tool'] = "🎓 Certification Exam"
                st.switch_page("app.py")
            
            if st.button("📚 LMS - My Courses", key="btn_lms", use_container_width=True):
                st.session_state['selected_tool'] = "📚 LMS - My Courses"
                st.switch_page("app.py")
            
            st.markdown("---")
            st.markdown("### ⚙️ Settings")
            
            if st.button("🔐 2FA Security", key="btn_2fa", use_container_width=True):
                st.switch_page("pages/security_2fa.py")
            
            if st.button("👤 My Account", key="btn_account", use_container_width=True):
                st.switch_page("app.py")
            
            # Admin/Staff only features
            if user_type in ['admin', 'staff']:
                st.markdown("---")
                st.markdown("### 🔧 Administration")
                
                if st.button("🏥 PAS Integration", key="btn_pas_demo", use_container_width=True):
                    st.switch_page("pages/pas_integration_demo.py")
                
                if st.button("📊 Analytics", key="btn_analytics", use_container_width=True):
                    st.switch_page("app.py")
                
                if st.button("👥 Users", key="btn_users", use_container_width=True):
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


def get_page_config():
    """Get recommended page config"""
    return {
        "page_title": "T21 Services",
        "page_icon": "🏥",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
