"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Complete NHS Healthcare Administration - Training & Automation Suite
By T21 Services Limited | Company No: 13091053 | Liverpool, England
www.t21services.co.uk | info@t21services.co.uk

7 Integrated Modules:
- RTT & Pathway Intelligence
- Cancer Pathway Management  
- MDT Coordination Suite
- Intelligent Appointment System
- Medical Secretary AI
- Data Quality & Governance
- Professional Training Academy (15+ NHS Roles)

Trusted by NHS Trusts, Training Providers, and Healthcare Professionals
"""

import streamlit as st
import json
from datetime import datetime

# Import with error handling
try:
    from rtt_validator import (validate_pathway, validate_clinic_letter, validate_timeline, 
                              validate_patient_registration, validate_appointments, generate_comment_line)
except Exception as e:
    st.error(f"Error loading rtt_validator: {e}")
    # Provide fallback functions
    def validate_pathway(data): return {"error": "Module not loaded"}
    def validate_clinic_letter(letter, pas): return {"error": "Module not loaded"}
    def validate_timeline(events): return {"error": "Module not loaded"}
    def validate_patient_registration(data): return {"error": "Module not loaded"}
    def validate_appointments(data): return {"error": "Module not loaded"}
    def generate_comment_line(data): return {"Standardised_Comment_Line": "ERROR"}

# NEW IMPORTS - All the powerful features we built!
try:
    from database import (save_validation, get_validation_history, get_dashboard_stats, 
                         get_active_alerts, acknowledge_alert)
except:
    def save_validation(data): pass
    def get_validation_history(): return []
    def get_dashboard_stats(): return {}
    def get_active_alerts(): return []
    def acknowledge_alert(id): pass

try:
    from excel_export import create_validation_excel, create_batch_results_excel
except:
    def create_validation_excel(data): return None
    def create_batch_results_excel(data): return None

try:
    from training_library import get_all_scenarios, check_answer as check_scenario_answer
except:
    def get_all_scenarios(): return []
    def check_scenario_answer(q, a): return False, ""

try:
    from smart_alerts import validate_and_generate_alerts
except:
    def validate_and_generate_alerts(data): return []
# All other imports with error handling
try:
    from interview_prep import (analyze_job_description, generate_smart_questions_to_ask, 
                                generate_red_flags_to_avoid)
except:
    def analyze_job_description(desc): return {}
    def generate_smart_questions_to_ask(role): return []
    def generate_red_flags_to_avoid(role): return []

try:
    from cv_builder import (generate_cv_data, generate_professional_summary, format_cv_html,
                            get_ats_keywords, generate_linkedin_profile, get_t21_qualifications)
except:
    def generate_cv_data(data): return {}
    def generate_professional_summary(data): return ""
    def format_cv_html(data): return ""
    def get_ats_keywords(role): return []
    def generate_linkedin_profile(data): return ""
    def get_t21_qualifications(): return []

try:
    from interactive_learning import (INTERACTIVE_QUIZZES, BADGES, check_answer as check_quiz_answer, 
                                      get_all_categories, get_quiz_by_difficulty,
                                      StudentProgress, get_leaderboard, add_to_leaderboard)
except:
    INTERACTIVE_QUIZZES = {}
    BADGES = []
    def check_quiz_answer(q, a): return False, ""
    def get_all_categories(): return []
    def get_quiz_by_difficulty(d): return []
    class StudentProgress: pass
    def get_leaderboard(): return []
    def add_to_leaderboard(name, score): pass

try:
    from certification_system import (generate_exam, grade_exam, generate_certificate, 
                                      format_certificate_html, verify_certificate)
except:
    def generate_exam(level): return []
    def grade_exam(answers): return 0, []
    def generate_certificate(name, score): return ""
    def format_certificate_html(cert): return ""
    def verify_certificate(id): return False

try:
    from ai_tutor import (answer_question, get_code_info, generate_related_quiz, ChatHistory)
except:
    def answer_question(question): return "AI Tutor unavailable"
    def get_code_info(code): return ""
    def generate_related_quiz(topic): return []
    class ChatHistory: pass

try:
    from access_control import UserLicense, ROLES, check_feature_access
except:
    class UserLicense: pass
    ROLES = {}
    def check_feature_access(role, feature): return True

try:
    from student_auth import (login_student, register_student, hash_password,
                              list_all_students, upgrade_student, extend_student_license,
                              request_password_reset, verify_reset_code, reset_password,
                              get_student_info)
except:
    def login_student(email, pw): return False, "", None
    def register_student(email, pw, name, role="trial"): return False, "", None
    def hash_password(pw): return pw
    def list_all_students(): return []
    def upgrade_student(email, tier): pass
    def extend_student_license(email, days): pass
    def request_password_reset(email): return False, ""
    def verify_reset_code(email, code): return False
    def reset_password(email, pw): pass
    def get_student_info(email): return {}

try:
    from advanced_access_control import UserAccount, USER_TYPES
except:
    class UserAccount: pass
    USER_TYPES = {}

try:
    from admin_management import load_users_db, save_users_db
except:
    def load_users_db(): return {}
    def save_users_db(db): pass

try:
    from admin_panel_ui import render_admin_panel
except:
    def render_admin_panel(email): st.info("Admin panel unavailable")

try:
    from module_access_control import get_accessible_modules, can_access_module
except:
    def get_accessible_modules(role, email=None): return []
    def can_access_module(role, module, email=None): return True

try:
    from admin_module_access_ui import render_module_access_admin
except:
    def render_module_access_admin(): st.info("Module access admin unavailable")

try:
    from admin_bulk_email import render_bulk_email_ui
except:
    def render_bulk_email_ui(): st.info("Bulk email unavailable")

try:
    from admin_trial_automation_ui import render_trial_automation_ui
except:
    def render_trial_automation_ui(): st.info("Trial automation unavailable")

try:
    from admin_personal_message_ui import render_personal_message_ui
except:
    def render_personal_message_ui(): st.info("Personal message unavailable")

try:
    from admin_modular_access_ui import render_modular_access_admin
except:
    def render_modular_access_admin(): st.info("Modular access unavailable")

try:
    from lms_course_manager import render_course_manager_ui
except:
    def render_course_manager_ui(): st.info("LMS course manager unavailable")

try:
    from lms_student_portal import render_student_lms_portal
except:
    def render_student_lms_portal(email, role): st.info("LMS student portal unavailable")

try:
    from lms_enhanced_catalog import render_enhanced_catalog
except:
    def render_enhanced_catalog(email): st.info("LMS catalog unavailable")

try:
    from lms_course_preview import render_course_preview
except:
    def render_course_preview(course_id, email): st.info("Course preview unavailable")

try:
    from user_module_marketplace import render_user_marketplace
except:
    def render_user_marketplace(email, role): st.info("Module marketplace unavailable")

try:
    from admin_school_management_ui import render_school_management_admin
except:
    def render_school_management_admin(): st.info("School management unavailable")

try:
    from student_school_portal import render_student_school_portal
except:
    def render_student_school_portal(email): st.info("School portal unavailable")

try:
    from ai_validator_ui import render_ai_validator
except:
    def render_ai_validator(): st.info("AI validator unavailable")

try:
    from admin_ai_training import render_ai_training_admin
except:
    def render_ai_training_admin(): st.info("AI training admin unavailable")

try:
    from admin_user_tracking_ui import render_user_tracking_dashboard
except:
    def render_user_tracking_dashboard(): st.info("User tracking unavailable")

try:
    from ptl_ui import render_ptl
except:
    def render_ptl(): st.info("PTL unavailable")

try:
    from cancer_pathway_ui import render_cancer_pathways
except:
    def render_cancer_pathways(): st.info("Cancer pathways unavailable")

try:
    from mdt_coordination_ui import render_mdt_coordination
except:
    def render_mdt_coordination(): st.info("MDT coordination unavailable")

try:
    from advanced_booking_ui import render_advanced_booking
except:
    def render_advanced_booking(): st.info("Advanced booking unavailable")

try:
    from medical_secretary_ui import render_medical_secretary
except:
    def render_medical_secretary(): st.info("Medical secretary unavailable")

try:
    from data_quality_ui import render_data_quality
except:
    def render_data_quality(): st.info("Data quality unavailable")

try:
    from interactive_reports import generate_student_progress_report
except:
    def generate_student_progress_report(email): return ""

import hashlib
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="T21 Healthcare Intelligence Platform | T21 Services UK",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM SIDEBAR (Show/Hide based on login)
# ============================================
try:
    from sidebar_manager import render_sidebar
    render_sidebar()
except Exception as e:
    st.sidebar.warning(f"Sidebar manager error: {e}")

# ============================================
# AUTHENTICATION & ACCESS CONTROL
# ============================================

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_license' not in st.session_state:
    st.session_state.user_license = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'session_email' not in st.session_state:
    st.session_state.session_email = None
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = None

# Session timeout check (15 minutes of inactivity)
if st.session_state.logged_in and st.session_state.last_activity:
    from datetime import datetime, timedelta
    time_since_activity = datetime.now() - st.session_state.last_activity
    
    # Auto-logout after 15 minutes of inactivity
    if time_since_activity > timedelta(minutes=15):
        st.session_state.logged_in = False
        st.session_state.user_license = None
        st.session_state.user_email = None
        st.session_state.session_email = None
        st.session_state.last_activity = None
        st.warning("⏱️ Session expired due to inactivity. Please login again.")
        st.rerun()

# Update last activity timestamp
if st.session_state.logged_in:
    from datetime import datetime
    st.session_state.last_activity = datetime.now()

# Session persistence - restore login on refresh
if not st.session_state.logged_in and st.session_state.session_email:
    # Try to restore session
    try:
        import hashlib
        stored_email = st.session_state.session_email
        
        # Try loading from Supabase first
        try:
            from supabase_database import get_user_by_email
            user_data = get_user_by_email(stored_email)
            
            if user_data:
                # Create simple user object
                class SimpleUser:
                    def __init__(self, data):
                        self.email = data.get('email')
                        self.full_name = data.get('full_name')
                        self.role = data.get('role', 'trial')
                        self.user_type = data.get('user_type', 'student')
                
                user_obj = SimpleUser(user_data)
                st.session_state.logged_in = True
                st.session_state.user_license = user_obj
                st.session_state.user_email = stored_email
        except:
            # Fallback to old system
            from student_auth import load_students_db
            students = load_students_db()
            if stored_email in students:
                st.session_state.logged_in = True
                st.session_state.user_license = students[stored_email]['license']
                st.session_state.user_email = stored_email
    except Exception as e:
        pass  # Silent fail, just show login page

# Login/Registration Page
if not st.session_state.logged_in:
    # Import and render clean landing page
    try:
        from landing_page_clean import render_clean_landing_page
        render_clean_landing_page()
    except Exception as e:
        st.error(f"Error loading landing page: {e}")
    
    st.stop()  # Stop here - landing page is complete
    
    with tab1:
        st.subheader("Login")
        st.caption("For Students, Staff, and Administrators")
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            if email and password:
                import json
                import os
                
                # Try Supabase first (all users)
                try:
                    from supabase_database import get_user_by_email, update_user_last_login
                    import hashlib
                    
                    supabase_user = get_user_by_email(email)
                    
                    if supabase_user:
                        # User found in Supabase
                        password_hash = hashlib.sha256(password.encode()).hexdigest()
                        
                        if supabase_user.get('password_hash') == password_hash:
                            # Check if account is active
                            if supabase_user.get('status') == 'active':
                                # Check if 2FA is enabled
                                if supabase_user.get('two_factor_enabled'):
                                    # Store user data temporarily and show 2FA prompt
                                    st.session_state.pending_2fa_user = supabase_user
                                    st.session_state.show_2fa_prompt = True
                                    st.rerun()
                                else:
                                    # No 2FA, proceed with normal login
                                    # Update last login
                                    update_user_last_login(email)
                                    
                                    # Track login
                                    from user_tracking_system import track_user_login
                                    track_user_login(email, success=True)
                                    
                                    # Create a simple user object for session
                                    class SimpleUser:
                                        def __init__(self, data):
                                            self.email = data.get('email')
                                            self.full_name = data.get('full_name')
                                            self.role = data.get('role', 'trial')
                                            self.user_type = data.get('user_type', 'student')
                                            self.status = data.get('status', 'active')
                                    
                                    user_obj = SimpleUser(supabase_user)
                                    
                                    # Set session
                                    st.session_state.logged_in = True
                                    st.session_state.user_license = user_obj
                                    st.session_state.user_email = email
                                    st.session_state.session_email = email  # Persist across refreshes
                                    
                                    # Enhanced Audit Trail
                                    try:
                                        from enhanced_audit_trail import log_audit_event, AuditActions
                                        log_audit_event(
                                            user_email=email,
                                            action=AuditActions.LOGIN,
                                            details={'method': 'supabase', 'user_type': user_obj.user_type, '2fa': False},
                                            reason='User authentication'
                                        )
                                    except:
                                        pass  # Don't break login if audit fails
                                    
                                    st.success(f"✅ Welcome back, {user_obj.full_name}!")
                                    st.rerun()
                            else:
                                st.error(f"❌ Account {supabase_user.get('status')}. Please contact administrator.")
                        else:
                            # Track failed login
                            from user_tracking_system import track_user_login
                            track_user_login(email, success=False)
                            st.error("❌ Incorrect password")
                        # Exit early if found in Supabase
                        st.stop()
                        
                except Exception as e:
                    # If Supabase fails, fall back to old databases
                    st.warning(f"Using backup login system...")
                
                # Fallback: Try advanced users database (old system)
                users_db = load_users_db()
                
                if email in users_db:
                    # Advanced user (admin/staff)
                    user = users_db[email]
                    
                    # Check password
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    
                    if user.password_hash and user.password_hash == password_hash:
                        if user.is_active():
                            # PORTAL VALIDATION
                            user_type = user.user_type
                            
                            if staff_portal and user_type not in ['admin', 'staff', 'super_admin']:
                                st.error("❌ Staff/Partner Portal is restricted to authorized personnel only")
                                st.info("💡 Please uncheck 'Staff/Partner' and use the correct portal")
                            elif nhs_portal and user_type not in ['admin', 'staff', 'nhs_user', 'super_admin']:
                                st.error("❌ NHS Organization Portal requires NHS/Organization account")
                                st.info("💡 Students should use the Student Portal")
                            else:
                                # Record login
                                user.record_login()
                                save_users_db(users_db)
                                
                                # Track user login with geolocation
                                from user_tracking_system import track_user_login
                                track_user_login(email, success=True)
                                
                                # Set session
                                st.session_state.logged_in = True
                                st.session_state.user_license = user
                                st.session_state.user_email = email
                                st.session_state.session_email = email  # Persist across refreshes
                                
                                # Portal-specific welcome
                                if staff_portal:
                                    st.success(f"👥 Staff Portal: Welcome back, {user.full_name}!")
                                elif nhs_portal:
                                    st.success(f"🏥 NHS Portal: Welcome back, {user.full_name}!")
                                else:
                                    st.success(f"Welcome back, {user.full_name}!")
                                
                                st.rerun()
                        else:
                            st.error(f"Account {user.status}. Please contact administrator.")
                    else:
                        # Track failed login
                        from user_tracking_system import track_user_login
                        track_user_login(email, success=False)
                        st.error("Incorrect password")
                else:
                    # Try old student database
                    success, message, user_license = login_student(email, password)
                    if success:
                        # Check if trial expired
                        if user_license.role == "trial" and not user_license.is_active():
                            st.error("❌ Your 48-hour trial has expired!")
                            st.warning("⬆️ Please upgrade to continue using the platform.")
                            st.info("💰 **Upgrade Options:**\n- Basic: £299 / 3 months\n- Professional: £599 / 6 months\n- Premium: £999 / 12 months")
                            if st.button("📧 Contact Admin to Upgrade", key="contact_admin_2"):
                                st.info("📧 Email: admin@t21services.co.uk")
                        else:
                            # PORTAL VALIDATION FOR STUDENTS
                            if staff_portal:
                                st.error("❌ Staff/Partner Portal is restricted to T21 staff only")
                                st.info("💡 Please uncheck 'Staff/Partner' to access student training")
                            elif nhs_portal:
                                st.error("❌ NHS Organization Portal is for NHS trusts only")
                                st.info("💡 Please uncheck 'NHS Organization' to access student training")
                            else:
                                # Track student login
                                from user_tracking_system import track_user_login
                                track_user_login(email, success=True)
                                
                                st.session_state.logged_in = True
                                st.session_state.user_license = user_license
                                st.session_state.user_email = email
                                st.session_state.session_email = email  # Persist across refreshes
                                st.success(f"🎓 Student Portal: {message}")
                                st.rerun()
                    else:
                        # Track failed login
                        from user_tracking_system import track_user_login
                        track_user_login(email, success=False)
                        st.error(message)
            else:
                st.warning("Please enter email and password")
        
        # 2FA Verification Prompt
        if st.session_state.get('show_2fa_prompt'):
            st.markdown("---")
            st.markdown("### 🔐 Two-Factor Authentication Required")
            
            pending_user = st.session_state.get('pending_2fa_user')
            
            if pending_user:
                st.info(f"Please enter the 6-digit code from your authenticator app for **{pending_user.get('email')}**")
                
                two_fa_code = st.text_input("Enter 6-digit code:", max_chars=6, key="2fa_code_input")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Verify & Login", type="primary"):
                        if two_fa_code and len(two_fa_code) == 6:
                            from two_factor_auth import verify_2fa_code
                            
                            secret = pending_user.get('two_factor_secret')
                            
                            if verify_2fa_code(secret, two_fa_code):
                                # 2FA verified! Complete login
                                from user_tracking_system import track_user_login
                                from supabase_database import update_user_last_login
                                
                                email = pending_user.get('email')
                                update_user_last_login(email)
                                track_user_login(email, success=True)
                                
                                # Create user object
                                class SimpleUser:
                                    def __init__(self, data):
                                        self.email = data.get('email')
                                        self.full_name = data.get('full_name')
                                        self.role = data.get('role', 'trial')
                                        self.user_type = data.get('user_type', 'student')
                                        self.status = data.get('status', 'active')
                                
                                user_obj = SimpleUser(pending_user)
                                
                                # Set session
                                st.session_state.logged_in = True
                                st.session_state.user_license = user_obj
                                st.session_state.user_email = email
                                st.session_state.session_email = email
                                
                                # Clear 2FA prompt
                                st.session_state.show_2fa_prompt = False
                                st.session_state.pending_2fa_user = None
                                
                                # Audit log
                                try:
                                    from enhanced_audit_trail import log_audit_event, AuditActions
                                    log_audit_event(
                                        user_email=email,
                                        action=AuditActions.LOGIN,
                                        details={'method': 'supabase', 'user_type': user_obj.user_type, '2fa': True},
                                        reason='User authentication with 2FA'
                                    )
                                except:
                                    pass
                                
                                st.success(f"✅ 2FA Verified! Welcome back, {user_obj.full_name}!")
                                st.rerun()
                            else:
                                st.error("❌ Invalid 2FA code. Please try again.")
                        else:
                            st.error("Please enter a 6-digit code")
                
                with col2:
                    if st.button("🔙 Use Backup Code"):
                        st.session_state.show_backup_code_input = True
                        st.rerun()
                
                # Backup code option
                if st.session_state.get('show_backup_code_input'):
                    st.markdown("---")
                    st.warning("⚠️ Each backup code can only be used once")
                    backup_code = st.text_input("Enter backup code (XXXX-XXXX):", key="backup_code_input")
                    
                    if st.button("✅ Verify Backup Code"):
                        if backup_code:
                            from supabase_database import use_backup_code
                            
                            if use_backup_code(pending_user.get('email'), backup_code):
                                # Login successful
                                email = pending_user.get('email')
                                
                                # Same login process as above
                                from user_tracking_system import track_user_login
                                from supabase_database import update_user_last_login
                                
                                update_user_last_login(email)
                                track_user_login(email, success=True)
                                
                                class SimpleUser:
                                    def __init__(self, data):
                                        self.email = data.get('email')
                                        self.full_name = data.get('full_name')
                                        self.role = data.get('role', 'trial')
                                        self.user_type = data.get('user_type', 'student')
                                        self.status = data.get('status', 'active')
                                
                                user_obj = SimpleUser(pending_user)
                                
                                st.session_state.logged_in = True
                                st.session_state.user_license = user_obj
                                st.session_state.user_email = email
                                st.session_state.session_email = email
                                
                                st.session_state.show_2fa_prompt = False
                                st.session_state.pending_2fa_user = None
                                st.session_state.show_backup_code_input = False
                                
                                st.success(f"✅ Backup code verified! Welcome back, {user_obj.full_name}!")
                                st.warning("⚠️ Consider regenerating backup codes in your account settings")
                                st.rerun()
                            else:
                                st.error("❌ Invalid backup code")
                        else:
                            st.error("Please enter a backup code")
        
        st.markdown("---")
        
        # Password Reset Section
        with st.expander("🔐 Forgot Password?"):
            st.write("**Reset your password in 3 easy steps:**")
            
            reset_email = st.text_input("Enter your email address:", key="reset_email")
            
            if 'reset_step' not in st.session_state:
                st.session_state.reset_step = 1
            
            if st.session_state.reset_step == 1:
                if st.button("📧 Send Reset Code"):
                    if reset_email:
                        success, message = request_password_reset(reset_email)
                        if success:
                            st.success(message)
                            st.session_state.reset_step = 2
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please enter your email")
            
            elif st.session_state.reset_step == 2:
                st.info(f"✅ Reset code sent to {reset_email}")
                reset_code = st.text_input("Enter 6-digit code from email:", max_chars=6, key="reset_code")
                new_password = st.text_input("New Password:", type="password", key="reset_new_password")
                confirm_password = st.text_input("Confirm New Password:", type="password", key="reset_confirm_password")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Reset Password"):
                        if not (reset_code and new_password and confirm_password):
                            st.warning("Please fill all fields")
                        elif new_password != confirm_password:
                            st.error("Passwords don't match")
                        elif len(new_password) < 6:
                            st.error("Password must be at least 6 characters")
                        else:
                            success, message = reset_password(reset_email, reset_code, new_password)
                            if success:
                                st.success(message)
                                st.balloons()
                                st.session_state.reset_step = 1
                                st.rerun()
                            else:
                                st.error(message)
                
                with col2:
                    if st.button("← Start Over"):
                        st.session_state.reset_step = 1
                        st.rerun()
    
    with tab2:
        st.subheader("New Student Registration")
        st.info("🎉 **Start with 48-HOUR FREE TRIAL!** No credit card required.")
        
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email Address", key="reg_email")
        reg_password = st.text_input("Password (min 12 characters)", type="password", key="reg_password", 
                                      help="Must contain: uppercase, lowercase, number, and special character")
        
        # Real-time password strength indicator
        if reg_password:
            from security_utils import validate_password_strength
            strength_check = validate_password_strength(reg_password)
            
            col_strength, col_score = st.columns([3, 1])
            with col_strength:
                st.markdown(f"**Password Strength:** {strength_check['strength']}")
            with col_score:
                st.markdown(f"**Score:** {strength_check['score']}/100")
            
            # Show feedback
            with st.expander("📋 Password Requirements", expanded=not strength_check['valid']):
                for item in strength_check['feedback']:
                    st.markdown(f"- {item}")
        
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        st.checkbox("I agree to Terms & Conditions", key="terms_agreed")
        
        if st.button("Register & Start Free Trial", type="primary"):
            if not st.session_state.terms_agreed:
                st.warning("Please agree to Terms & Conditions")
            elif not (reg_name and reg_email and reg_password):
                st.warning("Please fill all fields")
            elif reg_password != reg_confirm:
                st.error("Passwords don't match")
            else:
                # Validate password strength
                from security_utils import validate_password_strength
                strength_check = validate_password_strength(reg_password)
                
                if not strength_check['valid']:
                    st.error(f"❌ Password is too weak ({strength_check['strength']})")
                    st.error("Please choose a stronger password that meets all requirements.")
                else:
                    # Use Supabase for new registrations
                    try:
                        from supabase_database import create_user
                        import hashlib
                        
                        password_hash = hashlib.sha256(reg_password.encode()).hexdigest()
                        success, message = create_user(reg_email, password_hash, reg_name, role="trial", user_type="student")
                        
                        if success:
                            # Enhanced Audit Trail - Log new registration
                            try:
                                from enhanced_audit_trail import log_audit_event, AuditActions
                                log_audit_event(
                                    user_email=reg_email,
                                    action=AuditActions.CREATE_USER,
                                    details={
                                        'method': 'self_registration',
                                        'role': 'trial',
                                        'user_type': 'student',
                                        'full_name': reg_name
                                    },
                                    reason='New user self-registration'
                                )
                            except:
                                pass
                            
                            st.success("🎉 Registration successful!")
                            st.success("✅ You can now login with your credentials!")
                            st.info("🎁 Your 48-hour FREE TRIAL has started!")
                        else:
                            st.error(message)
                    except Exception as e:
                        # Fallback to old system if Supabase fails
                        st.warning(f"Using backup registration system...")
                        success, message, user_license = register_student(reg_email, reg_password, reg_name, role="trial")
                        if success:
                            st.success(message)
                            st.success("✅ You can now login with your credentials!")
                        else:
                            st.error(message)
    
    # PROFESSIONAL FOOTER WITH COMPANY DETAILS
    st.markdown("---")
    st.markdown("## 🏢 T21 Services Limited")
    st.markdown("*Healthcare Training & Technology Solutions*")
    st.markdown("")
    
    footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)
    
    with footer_col1:
        st.markdown("### 📍 Head Office")
        st.markdown("64 Upper Parliament Street")
        st.markdown("Liverpool, L8 7LF")
        st.markdown("England, United Kingdom")
        st.markdown("")
        st.markdown("**Company No:** 13091053")
        st.markdown("**Status:** Active ✅")
        st.markdown("**Incorporated:** 18 December 2020")
    
    with footer_col2:
        st.markdown("### 📞 Contact Us")
        st.markdown("📧 info@t21services.co.uk")
        st.markdown("📧 support@t21services.co.uk")
        st.markdown("📧 sales@t21services.co.uk")
        st.markdown("🌐 [www.t21services.co.uk](https://www.t21services.co.uk)")
    
    with footer_col3:
        st.markdown("### 🌐 Follow Us")
        st.markdown("💼 [LinkedIn](https://linkedin.com/company/t21services)")
        st.markdown("🐦 [X (Twitter)](https://x.com/t21services)")
        st.markdown("📘 [Facebook](https://facebook.com/t21services)")
        st.markdown("📸 [Instagram](https://instagram.com/t21services)")
        st.markdown("🎵 [TikTok](https://tiktok.com/@t21services)")
    
    with footer_col4:
        st.markdown("### 📄 Legal & Support")
        st.markdown("📄 Privacy Policy")
        st.markdown("(Access from sidebar)")
        st.markdown("")
        st.markdown("📜 Terms of Service")
        st.markdown("(Access from sidebar)")
    
    st.markdown("---")
    st.markdown("© 2020-2025 T21 Services Limited. All rights reserved.")
    st.markdown("*Company registered in England and Wales*")
    
    # Stop here if not logged in
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #005EB8;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #425563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .json-output {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #005EB8;
    }
    .breach-flag {
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
        text-align: center;
    }
    .breach-none {
        background-color: #d4edda;
        color: #155724;
    }
    .breach-18 {
        background-color: #fff3cd;
        color: #856404;
    }
    .breach-26 {
        background-color: #f8d7da;
        color: #721c24;
    }
    .breach-52 {
        background-color: #721c24;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header - Professional Branding
st.markdown('<div class="main-header">🏥 T21 Healthcare Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Complete NHS Healthcare Administration - Training & Automation Suite | T21 Services UK</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 14px; margin-top: -10px;">✨ 7 Integrated Modules | 15+ NHS Roles | AI-Powered Throughout | Trusted by Healthcare Professionals</p>', unsafe_allow_html=True)

# Sidebar - User License Info
st.sidebar.title("👤 User Profile")

if st.session_state.user_license:
    user_license = st.session_state.user_license
    
    # Check if it's an advanced UserAccount or old UserLicense
    if isinstance(user_license, UserAccount):
        # Advanced user (admin, staff, or new students)
        summary = user_license.get_summary()
        
        # Status card
        if summary["status"] == "active":
            st.sidebar.success(f"✅ {summary['role_name']}")
        else:
            st.sidebar.error(f"❌ {summary['role_name']} - {summary['status'].upper()}")
        
        if summary["days_remaining"] > 3000:
            st.sidebar.markdown(f"**Expires:** Never")
        else:
            st.sidebar.markdown(f"**Days Remaining:** {summary['days_remaining']}")
            st.sidebar.markdown(f"**Expires:** {summary['expiry_date']}")
        
        # Show usage for students
        if summary["user_type"] == "student":
            usage_data = user_license.usage
            st.sidebar.markdown("**Today's Usage:**")
            st.sidebar.markdown(f"- Logins: {usage_data.get('logins_today', 0)}")
            if usage_data.get('ai_questions_today', 0) > 0:
                st.sidebar.markdown(f"- AI Questions: {usage_data.get('ai_questions_today', 0)}")
    elif hasattr(user_license, 'email') and hasattr(user_license, 'role'):
        # SimpleUser from Supabase login
        role = getattr(user_license, 'role', 'user')
        user_type = getattr(user_license, 'user_type', 'student')
        full_name = getattr(user_license, 'full_name', 'User')
        
        # Status card
        st.sidebar.success(f"✅ {full_name}")
        st.sidebar.markdown(f"**Role:** {role.replace('_', ' ').title()}")
        
        if user_type in ['admin', 'staff', 'super_admin']:
            st.sidebar.markdown(f"**Type:** {user_type.replace('_', ' ').title()}")
        else:
            st.sidebar.markdown(f"**Type:** Student")
    else:
        # Old UserLicense object
        try:
            usage = user_license.get_usage_summary()
            
            # License status card
            if usage["status"] == "Active":
                st.sidebar.success(f"✅ {usage['role']}")
            else:
                st.sidebar.error(f"❌ {usage['role']} - EXPIRED")
            
            st.sidebar.markdown(f"**Days Remaining:** {usage['days_remaining']}")
            st.sidebar.markdown(f"**Expires:** {usage['expiry_date']}")
            
            # Usage limits (if any)
            if usage["usage_today"]:
                st.sidebar.markdown("**Today's Usage:**")
                for feature, limit in usage["usage_today"].items():
                    st.sidebar.markdown(f"- {feature}: {limit}")
        except AttributeError:
            # Fallback for unknown user object type
            st.sidebar.info("✅ Logged In")
            if hasattr(user_license, 'email'):
                st.sidebar.markdown(f"**Email:** {user_license.email}")
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        # Enhanced Audit Trail - Log logout
        try:
            from enhanced_audit_trail import log_audit_event, AuditActions
            if st.session_state.user_email:
                log_audit_event(
                    user_email=st.session_state.user_email,
                    action=AuditActions.LOGOUT,
                    details={'manual_logout': True},
                    reason='User initiated logout'
                )
        except:
            pass
        
        st.session_state.logged_in = False
        st.session_state.user_license = None
        st.session_state.user_email = None
        st.session_state.session_email = None  # Clear persistent session
        st.rerun()

st.sidebar.markdown("---")

# Enhanced Trial Status Display
user_license = st.session_state.user_license
if hasattr(user_license, 'role') and user_license.role == "trial":
    days_remaining = user_license.days_remaining()
    hours_remaining = days_remaining * 24
    
    if hours_remaining <= 0:
        st.sidebar.error("⏰ **TRIAL EXPIRED!**")
        st.sidebar.warning("Please upgrade to continue")
    elif hours_remaining <= 6:
        st.sidebar.error(f"⏰ **{int(hours_remaining)} HOURS LEFT!**")
        st.sidebar.warning("⚠️ Upgrade NOW!")
    elif hours_remaining <= 24:
        st.sidebar.warning(f"⏰ **{int(hours_remaining)} hours remaining**")
        st.sidebar.info("Consider upgrading soon!")
    else:
        st.sidebar.info(f"⏰ Trial: {int(hours_remaining)} hours left")

st.sidebar.markdown("---")

# Sidebar navigation
st.sidebar.title("🧭 Platform Modules")
# Get user's accessible modules based on their role AND user-specific access
user_role = st.session_state.user_license.role if hasattr(st.session_state.user_license, 'role') else "trial"
user_email = st.session_state.user_email if 'user_email' in st.session_state else None
accessible_modules = get_accessible_modules(user_role, user_email)

# Remove any duplicates (use dict to preserve order while removing duplicates)
accessible_modules = list(dict.fromkeys(accessible_modules))

# If no accessible modules (error), show all
if not accessible_modules:
    accessible_modules = [
        "📋 PTL - Patient Tracking List",
        "🎗️ Cancer Pathways",
        "👥 MDT Coordination",
        "📅 Advanced Booking System",
        "📧 Medical Secretary AI",
        "📊 Data Quality System",
        "🤖 AI Auto-Validator",
        "📊 Pathway Validator",
        "📝 Clinic Letter Interpreter",
        "📅 Timeline Auditor",
        "👤 Patient Registration Validator",
        "📆 Appointment & Booking Checker",
        "💬 Comment Line Generator",
        "✍️ Clinic Letter Creator",
        "🎓 Training Library",
        "🎮 Interactive Learning Center",
        "🎓 Certification Exam",
        "🤖 AI RTT Tutor",
        "💼 Job Interview Prep",
        "📄 CV Builder",
        "📊 Interactive Reports",
        "📈 Dashboard & Analytics",
        "🚨 Smart Alerts",
        "📜 Validation History",
        "⚙️ My Account & Upgrade",
        "🛒 Module Marketplace",
        "📚 LMS - My Courses",
        "🎓 My Academic Portal",
        "👥 Staff Management",
        "🔧 Admin Panel",
        "🏥 PAS Integration Demo (Hands-On)",
        "🔌 Custom PAS Integration",
        "🎓 Practical Training Portal (All Courses)",
        "ℹ️ About RTT Rules",
        "📄 Privacy Policy",
        "📜 Terms of Service",
        "📧 Contact Us"
    ]

tool = st.sidebar.radio(
    "Select Tool:",
    accessible_modules
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏢 **T21 Services Limited**")
st.sidebar.markdown("*Healthcare Training & Technology Solutions*")
st.sidebar.markdown("**Company No:** 13091053")
st.sidebar.markdown("**Address:** 64 Upper Parliament St, Liverpool, L8 7LF")
st.sidebar.markdown("📧 info@t21services.co.uk")
st.sidebar.markdown("📧 support@t21services.co.uk")
st.sidebar.markdown("🌐 [www.t21services.co.uk](https://www.t21services.co.uk)")
st.sidebar.markdown("💼 [LinkedIn](https://linkedin.com/company/t21services) | 🐦 [X](https://x.com/t21services)")
st.sidebar.markdown("📘 [Facebook](https://facebook.com/t21services) | 📸 [Instagram](https://instagram.com/t21services)")
st.sidebar.markdown("🎵 [TikTok](https://tiktok.com/@t21services)")
st.sidebar.markdown("---")
st.sidebar.caption("⚠️ Training & Simulation Environment")
st.sidebar.caption("No real patient data used")


# ============================================
# TOOL 0: PTL - PATIENT TRACKING LIST (CRITICAL NHS TOOL!)
# ============================================
if tool == "📋 PTL - Patient Tracking List":
    render_ptl()


# ============================================
# TOOL 0B: CANCER PATHWAYS (2WW/62-DAY TRACKING!)
# ============================================
elif tool == "🎗️ Cancer Pathways":
    render_cancer_pathways()


# ============================================
# TOOL 0C: MDT COORDINATION
# ============================================
elif tool == "👥 MDT Coordination":
    render_mdt_coordination()


# ============================================
# TOOL 0D: ADVANCED BOOKING SYSTEM
# ============================================
elif tool == "📅 Advanced Booking System":
    render_advanced_booking()


# ============================================
# TOOL 0E: MEDICAL SECRETARY AI
# ============================================
elif tool == "📧 Medical Secretary AI":
    render_medical_secretary()


# ============================================
# TOOL 0F: DATA QUALITY SYSTEM
# ============================================
elif tool == "📊 Data Quality System":
    render_data_quality()


# ============================================
# TOOL 1: AI AUTO-VALIDATOR (REVOLUTIONARY!)
# ============================================
elif tool == "🤖 AI Auto-Validator":
    render_ai_validator()


# ============================================
# TOOL 2: PATHWAY VALIDATOR
# ============================================
elif tool == "📊 Pathway Validator":
    st.header("RTT Pathway Validator")
    st.markdown("Validate a complete RTT pathway from referral to treatment (0-52 weeks)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Pathway Details")
        specialty = st.text_input("Specialty", value="ENT")
        referral_source = st.selectbox("Referral Source", ["GP", "Consultant", "A&E", "Dentist", "Optician", "Other"])
        referral_date = st.date_input("Referral Received Date", value=datetime(2025, 1, 2))
        first_appt_date = st.date_input("First Appointment Date", value=datetime(2025, 1, 10))
        
        st.subheader("📅 Key Dates")
        diagnostics_date = st.date_input("Diagnostics Date (if any)", value=datetime(2025, 1, 25))
        decision_date = st.date_input("Decision To Treat Date (if any)", value=datetime(2025, 2, 1))
        tci_date = st.date_input("Planned Admission/TCI Date (if any)", value=datetime(2025, 2, 12))
        treatment_date = st.date_input("First Treatment Date (if completed)", value=datetime(2025, 2, 20))
    
    with col2:
        st.subheader("⏸️ Delays & Status")
        delays_pauses = st.text_area("Known Delays/Pauses", 
                                      placeholder="e.g., Patient requested 4-week delay for personal reasons")
        
        active_monitoring = st.selectbox("Active Monitoring", 
                                         ["None", "31_patient", "32_clinician"])
        
        am_start_date = st.date_input("AM Start Date (if applicable)", value=None)
        
        transfer_out = st.selectbox("Transfer Out", ["N", "Y"])
        
        cancellations_dna = st.text_area("Cancellations/DNAs", 
                                         placeholder="e.g., Hospital cancelled 1st appointment")
        
        current_rtt_event = st.selectbox("Current RTT Event Code", 
                                         ["10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"])
        
        notes = st.text_area("Additional Notes", placeholder="Any extra context...")
    
    if st.button("🔍 Validate Pathway", type="primary"):
        # Prepare data
        data = {
            'specialty': specialty,
            'referral_source': referral_source,
            'referral_date': referral_date.strftime('%d/%m/%Y'),
            'first_appt_date': first_appt_date.strftime('%d/%m/%Y'),
            'diagnostics_date': diagnostics_date.strftime('%d/%m/%Y') if diagnostics_date else '',
            'decision_date': decision_date.strftime('%d/%m/%Y') if decision_date else '',
            'tci_date': tci_date.strftime('%d/%m/%Y') if tci_date else '',
            'treatment_date': treatment_date.strftime('%d/%m/%Y') if treatment_date else '',
            'delays_pauses': delays_pauses,
            'active_monitoring': active_monitoring,
            'am_start_date': am_start_date.strftime('%d/%m/%Y') if am_start_date else '',
            'transfer_out': transfer_out,
            'cancellations_dna': cancellations_dna,
            'current_rtt_event': current_rtt_event,
            'notes': notes
        }
        
        # Validate
        result = validate_pathway(data)
        
        # Display results
        st.success("✅ Validation Complete")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Clock Status", result['RTT_Clock_Status'])
        with col2:
            st.metric("Weeks Elapsed", result['Weeks_Elapsed'])
        with col3:
            st.metric("RTT Code", result['RTT_Code'])
        with col4:
            st.metric("Confidence", result['Confidence_Level'])
        
        # Breach flag
        breach_class = "breach-none"
        if "52" in result['Breach_Flag']:
            breach_class = "breach-52"
        elif "26" in result['Breach_Flag']:
            breach_class = "breach-26"
        elif "18" in result['Breach_Flag']:
            breach_class = "breach-18"
        
        st.markdown(f'<div class="breach-flag {breach_class}">🚨 {result["Breach_Flag"]}</div>', 
                   unsafe_allow_html=True)
        
        # Explanation
        st.subheader("📖 Explanation")
        st.info(result['Explanation'])
        
        # Recommended action
        st.subheader("✅ Recommended Action")
        st.success(f"**{result['Recommended_Action']}**")
        
        # PAS Updates
        st.subheader("🔧 What To Change In PAS")
        for update in result['What_To_Change_In_PAS']:
            st.markdown(f"- {update}")
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 2: CLINIC LETTER INTERPRETER
# ============================================
elif tool == "📝 Clinic Letter Interpreter":
    st.header("Clinic Letter Interpreter")
    st.markdown("Interpret clinic letters and verify action compliance in PAS")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📨 Clinic Letter / Outcome Text")
        letter_text = st.text_area("Paste clinic letter here:", 
                                    height=300,
                                    placeholder="Example:\n\nENT Review: Patient assessed for deviated septum.\nPlan: Proceed to septoplasty – patient consented.\nPlease book on surgical waiting list (ENT – Septoplasty).\nFollow-up in 6 weeks pre-op clinic to confirm fitness.\nCopy to GP.")
    
    with col2:
        st.subheader("💻 Current PAS Summary")
        st.markdown("**What has already been recorded in PAS:**")
        
        validator_initials = st.text_input("Validator Initials (2-3 letters)", 
                                          value="VLD", 
                                          max_chars=3,
                                          help="Your initials for the comment line (e.g., JDS, AKM)")
        
        # Excel Tracker Fields
        st.markdown("**Excel Tracker Fields:**")
        
        clock_status = st.selectbox("Clock Status (for Excel)", 
                                   ["Previously Stopped", "Hospital to Review", "Unclear", "No", "Yes"],
                                   help="Previously Stopped = Another validator stopped it before | Yes = You're stopping it now")
        
        outcome = st.selectbox("Outcome (for Excel)",
                              ["(Blank)", "Awaiting OPD Appt", "Awaiting results", "Awaiting TC date", 
                               "CL Required", "Discharged", "Further Information Required", "OPD Appt (Booked)"],
                              help="Next action required based on letter")
        
        st.markdown("---")
        st.markdown("**PAS System Checks:**")
        
        followup_booked = st.selectbox("Follow-up appointment booked?", ["N", "Y"])
        followup_date = st.date_input("Follow-up date (if booked)", value=None)
        
        diagnostics_ordered = st.selectbox("Diagnostics ordered?", ["N", "Y"])
        diagnostics_date = st.date_input("Diagnostics date (if ordered)", value=None)
        
        waiting_list = st.selectbox("Added to waiting list?", ["N", "Y"])
        wl_type = st.text_input("Waiting list type", placeholder="e.g., ENT surgical list")
        
        gp_informed = st.selectbox("GP letter sent?", ["N", "Y"])
        
        am_recorded = st.selectbox("Active Monitoring recorded?", ["N", "Y"])
        
        treatment_started = st.selectbox("Treatment started recorded (code 30)?", ["N", "Y"])
        
        other_notes = st.text_area("Other notes", placeholder="Any additional PAS entries...")
    
    if st.button("🔍 Interpret Letter", type="primary"):
        pas_summary = {
            'validator_initials': validator_initials.upper(),
            'clock_status': clock_status,
            'outcome': outcome,
            'followup_booked': followup_booked,
            'followup_date': followup_date.strftime('%d/%m/%Y') if followup_date else '',
            'diagnostics_ordered': diagnostics_ordered,
            'diagnostics_date': diagnostics_date.strftime('%d/%m/%Y') if diagnostics_date else '',
            'waiting_list': waiting_list,
            'wl_type': wl_type,
            'gp_informed': gp_informed,
            'am_recorded': am_recorded,
            'treatment_started': treatment_started,
            'other_notes': other_notes
        }
        
        result = validate_clinic_letter(letter_text, pas_summary)
        
        # VALIDATION STATUS BANNER
        val_summary = result['Validation_Summary']
        if val_summary['Excel_Flag_Color'] == "GREEN":
            st.success(f"✅ {val_summary['Overall_Status']}")
        elif val_summary['Excel_Flag_Color'] == "AMBER":
            st.warning(f"⚠️ {val_summary['Overall_Status']}")
        else:
            st.error(f"❌ {val_summary['Overall_Status']}")
        
        # VALIDATION METRICS (for Excel reporting)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("RTT Code", result['RTT_Code'])
        with col2:
            st.metric("Clock Status", result['Clock_Status'])
        with col3:
            st.metric("Compliance Rate", val_summary['Compliance_Rate'])
        with col4:
            flag_color = val_summary['Excel_Flag_Color']
            st.metric("Excel Flag", flag_color, delta_color="off")
        
        # EXCEL REPORTING SECTION (Matches Excel Tracker Columns)
        st.subheader("📊 Excel Tracker Report")
        excel_data = result['Excel_Report']
        
        excel_output = f"""
**Copy to Excel Tracker (Exact Column Order):**

Validator Name: {excel_data['Validator_Name']}
Clock Status: {excel_data['Clock_Status']}
Outcome: {excel_data['Outcome']}
Validation Date: {excel_data['Validation_Date']}
Validation Comments: {excel_data['Validation_Comments']}
        """
        st.code(excel_output.strip(), language=None)
        
        # Show comment in highlighted box
        st.info(f"**Validation Comment for Excel:**\n\n{excel_data['Validation_Comments']}")
        
        # VALIDATION CHECKLIST
        st.subheader("✅ Validation Checklist")
        compliance = result['Action_Compliance']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📋 Actions Required (from letter):**")
            for action in compliance['Actions_Required']:
                st.markdown(f"- {action}")
        
        with col2:
            st.markdown("**✅ Actions Completed (verified in PAS):**")
            if compliance['Actions_Reported_In_PAS']:
                for action in compliance['Actions_Reported_In_PAS']:
                    st.markdown(f"- ✅ {action}")
            else:
                st.markdown("*No actions completed in PAS*")
        
        # GAPS & FLAGS
        if compliance['Gaps']:
            st.error(f"**🚩 GAPS FOUND - {compliance['Priority']} Priority ({val_summary['Actions_Outstanding']} outstanding)**")
            for i, gap in enumerate(compliance['Gaps'], 1):
                st.markdown(f"{i}. ❌ **{gap}**")
        else:
            st.success("✅ **No gaps found - All actions completed!**")
        
        # COMMENT LINE (for PAS system)
        st.subheader("💬 Standardised Comment Line (Copy to PAS)")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # EXCEL EXPORT BUTTON (NEW!)
        st.markdown("---")
        st.subheader("📥 Download Excel Report")
        
        if st.button("📥 Generate Excel Report", type="primary"):
            excel_file = create_validation_excel(result, excel_data)
            
            # Offer download
            st.download_button(
                label="⬇️ Download 4-Sheet Excel Report",
                data=excel_file,
                file_name=f"RTT_Validation_{result['RTT_Code']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("✅ Excel report generated! Click button above to download.")
        
        # Explanation
        with st.expander("📖 Code Explanation"):
            st.info(result['Explanation'])
        
        # Full JSON
        with st.expander("📄 Full JSON Output (for technical review)"):
            st.json(result)


# ============================================
# TOOL 3: TIMELINE AUDITOR
# ============================================
elif tool == "📅 Timeline Auditor":
    st.header("RTT Timeline Auditor")
    st.markdown("Audit a chronological sequence of RTT events for coding accuracy")
    
    st.subheader("📋 Enter Pathway Timeline")
    st.markdown("Add events in chronological order:")
    
    # Initialize session state for events
    if 'events' not in st.session_state:
        st.session_state.events = [
            {'date': '01/02/2025', 'description': 'Referral received', 'code': '10', 'notes': 'GP to ENT'}
        ]
    
    # Display existing events
    for i, event in enumerate(st.session_state.events):
        col1, col2, col3, col4, col5 = st.columns([2, 3, 1, 3, 1])
        with col1:
            event['date'] = st.text_input(f"Date {i+1}", value=event['date'], key=f"date_{i}")
        with col2:
            event['description'] = st.text_input(f"Description {i+1}", value=event['description'], key=f"desc_{i}")
        with col3:
            event['code'] = st.selectbox(f"Code {i+1}", 
                                        ["10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"],
                                        index=["10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"].index(event['code']),
                                        key=f"code_{i}")
        with col4:
            event['notes'] = st.text_input(f"Notes {i+1}", value=event.get('notes', ''), key=f"notes_{i}")
        with col5:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.events.pop(i)
                st.rerun()
    
    # Add new event
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Add Event"):
            st.session_state.events.append({
                'date': datetime.now().strftime('%d/%m/%Y'),
                'description': 'New event',
                'code': '20',
                'notes': ''
            })
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Timeline"):
            st.session_state.events = [
                {'date': '01/02/2025', 'description': 'Referral received', 'code': '10', 'notes': 'GP to ENT'}
            ]
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🔍 Audit Timeline", type="primary"):
        result = validate_timeline(st.session_state.events)
        
        # Overall status
        status_color = "success" if result['Overall_Status'] == "Pass" else ("warning" if result['Overall_Status'] == "Warning" else "error")
        st.markdown(f"### {result['Overall_Status']}")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Clock Start", result['Clock_Start_Date'])
        with col2:
            st.metric("Clock Stop", result['Clock_Stop_Date'] or "Active")
        with col3:
            st.metric("Total Weeks", result['Weeks_Total'])
        with col4:
            st.metric("Breach Flag", result['Breach_Flag'])
        
        # Issues
        if result['Critical_Issues']:
            st.error("**🚨 Critical Issues:**")
            for issue in result['Critical_Issues']:
                st.markdown(f"- {issue}")
        
        if result['Moderate_Issues']:
            st.warning("**⚠️ Moderate Issues:**")
            for issue in result['Moderate_Issues']:
                st.markdown(f"- {issue}")
        
        if result['Duplicate_Code_Issues']:
            st.error("**🔄 Duplicate Code Issues:**")
            for issue in result['Duplicate_Code_Issues']:
                st.markdown(f"- {issue}")
        
        # Recode suggestions
        if result['Recommended_Recode_Suggestions']:
            st.subheader("🔧 Recode Suggestions")
            for suggestion in result['Recommended_Recode_Suggestions']:
                st.markdown(f"- {suggestion}")
        
        # Training feedback
        st.subheader("🎓 Training Feedback")
        st.info(result['Training_Feedback'])
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 4: PATIENT REGISTRATION VALIDATOR
# ============================================
elif tool == "👤 Patient Registration Validator":
    st.header("Patient Registration Validator")
    st.markdown("Validate patient registration details and document readiness before starting RTT pathway")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Patient Demographics")
        patient_name = st.text_input("Patient Name *", placeholder="SURNAME, Forename")
        nhs_number = st.text_input("NHS Number *", placeholder="1234567890 (10 digits)")
        district_number = st.text_input("District Number", placeholder="Hospital number")
        dob = st.date_input("Date of Birth *", value=None)
        age = st.number_input("Age (optional)", min_value=0, max_value=120, value=0)
        
    with col2:
        st.subheader("📋 Referral Details")
        referral_source = st.selectbox("Referral Source *", ["", "GP", "Consultant", "A&E", "Dentist", "Optician", "Other"])
        referral_date = st.date_input("Referral Date *", value=None)
        specialty = st.text_input("Specialty *", placeholder="e.g., ENT, Orthopaedics")
        referral_type = st.text_input("Referral Type", placeholder="e.g., Consultant-led, Diagnostic-only")
        
    st.subheader("📎 Documents Uploaded")
    documents = st.text_area("Document Names (comma-separated)", 
                            placeholder="SMITH_JOHN_020125_REFERRAL.pdf, SMITH_JOHN_020125_XRAY.dcm")
    
    col1, col2 = st.columns(2)
    with col1:
        referral_accepted = st.selectbox("Referral Accepted?", ["N", "Y"])
        check_duplicate = st.selectbox("Check for Duplicates?", ["N", "Y"])
    
    with col2:
        notes = st.text_area("Additional Notes", placeholder="Any special considerations...")
    
    if st.button("✅ Validate Registration", type="primary"):
        data = {
            'patient_name': patient_name,
            'nhs_number': nhs_number,
            'district_number': district_number,
            'dob': dob.strftime('%d/%m/%Y') if dob else '',
            'age': str(age) if age > 0 else '',
            'referral_source': referral_source,
            'referral_date': referral_date.strftime('%d/%m/%Y') if referral_date else '',
            'specialty': specialty,
            'referral_type': referral_type,
            'documents': documents,
            'referral_accepted': referral_accepted,
            'check_duplicate': check_duplicate,
            'notes': notes
        }
        
        result = validate_patient_registration(data)
        
        # Display result
        if result['Validation_Result'] == "Pass":
            st.success("✅ Registration Validated - PASS")
        elif result['Validation_Result'] == "Warning":
            st.warning("⚠️ Registration Validated - WARNING")
        else:
            st.error("❌ Registration Validated - FAIL")
        
        # Data issues
        if result['Data_Issues']:
            st.subheader("⚠️ Data Issues Found")
            for issue in result['Data_Issues']:
                st.markdown(f"- ❌ {issue}")
        else:
            st.success("✅ No data issues found!")
        
        # PAS updates
        st.subheader("🔧 PAS Updates Required")
        for update in result['PAS_Update']:
            st.markdown(f"- {update}")
        
        # Training feedback
        st.subheader("🎓 Training Feedback")
        st.info(result['Training_Feedback'])
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 5: APPOINTMENT & BOOKING CHECKER
# ============================================
elif tool == "📆 Appointment & Booking Checker":
    st.header("Appointment & Booking Checker")
    st.markdown("Review booking history and verify correct RTT impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Appointment History")
        referral_date = st.date_input("Referral Date", value=datetime(2025, 1, 2))
        first_appt_date = st.date_input("First Appointment Date", value=datetime(2025, 1, 12))
        first_appt_type = st.text_input("First Appointment Type", value="New OP", placeholder="e.g., New OP, Diagnostic")
        
        followup_appointments = st.text_area("Follow-up Appointments", 
                                            placeholder="e.g., 01/02/2025 - Review OP, 15/02/2025 - Pre-op")
    
    with col2:
        st.subheader("⚠️ Issues & Status")
        dnas_cancellations = st.text_area("DNAs / Cancellations", 
                                         placeholder="e.g., Patient cancelled 1st appt - personal reasons\nHospital cancelled 2nd appt - staff shortage")
        
        planned_surgery = st.text_area("Planned Surgery / WL Details", 
                                      placeholder="e.g., Listed for septoplasty, TCI 20/02/2025")
        
        am_status = st.selectbox("Active Monitoring Status", 
                                ["None", "31 (patient-initiated)", "32 (clinician-initiated)", "91 (during AM)"])
        am_start_date = st.date_input("AM Start Date (if applicable)", value=None)
    
    treatment_started = st.selectbox("Treatment Started?", ["N", "Y"])
    notes = st.text_area("Additional Notes", placeholder="e.g., Review in 6 weeks instructed")
    
    if st.button("🔍 Check Appointments", type="primary"):
        data = {
            'referral_date': referral_date.strftime('%d/%m/%Y'),
            'first_appt_date': first_appt_date.strftime('%d/%m/%Y'),
            'first_appt_type': first_appt_type,
            'followup_appointments': followup_appointments,
            'dnas_cancellations': dnas_cancellations,
            'planned_surgery': planned_surgery,
            'am_status': am_status.split()[0] if am_status != "None" else "",
            'am_start_date': am_start_date.strftime('%d/%m/%Y') if am_start_date else '',
            'treatment_started': treatment_started,
            'notes': notes
        }
        
        result = validate_appointments(data)
        
        st.success("✅ Appointment Check Complete")
        
        # RTT Impact
        st.subheader("📊 RTT Impact")
        st.metric("RTT Impact", result['RTT_Impact'])
        
        # Issues
        if result['Issues'] != ["No issues found"]:
            st.subheader("⚠️ Issues Detected")
            for issue in result['Issues']:
                st.markdown(f"- ⚠️ {issue}")
        else:
            st.success("✅ No issues found!")
        
        # PAS updates
        st.subheader("🔧 PAS Updates Required")
        for update in result['PAS_Update']:
            st.markdown(f"- {update}")
        
        # Training feedback
        st.subheader("🎓 Training Feedback")
        st.info(result['Training_Feedback'])
        
        # Comment line
        st.subheader("💬 Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        # Full JSON
        with st.expander("📄 View Full JSON Output"):
            st.json(result)


# ============================================
# TOOL 6: COMMENT LINE GENERATOR
# ============================================
elif tool == "💬 Comment Line Generator":
    st.header("Comment Line Generator")
    st.markdown("Generate standardised T21 PAS comment lines for any RTT event")
    
    st.info("📋 Fill in the event details below to generate a professional PAS comment line")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Event Details")
        event = st.selectbox("Event Type", [
            "First Treatment / FDT",
            "Active Monitoring Start",
            "DNA First Care",
            "Waiting List / TCI",
            "Discharge",
            "Decision to Treat",
            "Other / Custom"
        ])
        
        key_date = st.date_input("Key Date", value=datetime.now())
        
        rtt_code = st.selectbox("RTT Code (if known)", 
                               ["", "10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"])
    
    with col2:
        st.subheader("📝 Additional Information")
        procedure = st.text_input("Procedure / Outcome", 
                                 placeholder="e.g., Septoplasty, Hip Replacement")
        
        next_action = st.text_input("Follow-up / Next Action", 
                                   placeholder="e.g., FU booked 01/03/2025, Review in 12 weeks")
        
        gp_letter = st.selectbox("GP Letter Sent?", ["N", "Y"])
    
    st.markdown("---")
    
    if st.button("✨ Generate Comment Line", type="primary"):
        data = {
            'event': event,
            'key_date': key_date.strftime('%d/%m/%Y'),
            'rtt_code': rtt_code,
            'procedure': procedure,
            'next_action': next_action,
            'gp_letter': gp_letter
        }
        
        result = generate_comment_line(data)
        
        st.success("✅ Comment Line Generated")
        
        st.subheader("💬 Your Standardised Comment Line")
        st.code(result['Standardised_Comment_Line'], language=None)
        
        st.markdown("**Copy and paste this into PAS notes field**")
        
        # Examples
        with st.expander("📚 View Comment Line Examples"):
            st.markdown("""
            ### Example Comment Lines:
            
            **First Definitive Treatment:**
            ```
            CS20/02/2025/30 – FDT STARTED (SEPTOPLASTY). PATHWAY CLOSED. GP LETTER SENT.
            ```
            
            **Active Monitoring:**
            ```
            AM32/10/01/2025 – UNDER REVIEW 12W. FU BOOKED 10/04/2025.
            ```
            
            **DNA First Care:**
            ```
            DNA33/15/01/2025 – FIRST CARE DNA. REBOOK 2W. GP COPY PENDING.
            ```
            
            **Waiting List / TCI:**
            ```
            WL/TCI 20/02/2025 – TCI SET. CONTINUE 20.
            ```
            
            **Discharge:**
            ```
            DISCH15/01/2025/34 – NO TREATMENT REQUIRED. PATHWAY CLOSED. GP LETTER SENT.
            ```
            
            **Decision to Treat:**
            ```
            DTT01/02/2025/20 – LISTED FOR SEPTOPLASTY. WL ENTRY REQUIRED.
            ```
            """)


# ============================================
# TOOL 7: CLINIC LETTER CREATOR (NEW!)
# ============================================
elif tool == "✍️ Clinic Letter Creator":
    st.header("✍️ Clinic Letter Creator")
    st.markdown("Generate realistic NHS clinic letters for training purposes")
    
    # Scenario templates
    st.subheader("📋 Select Scenario or Create Custom")
    
    scenario_type = st.selectbox("Choose Letter Type:", [
        "Custom (Fill in all fields)",
        "GP Referral - Cardiology",
        "GP Referral - Orthopaedics", 
        "GP Referral - ENT",
        "Clinic Outcome - Decision to Treat",
        "Clinic Outcome - Discharge",
        "Results Letter - Normal",
        "Results Letter - Abnormal",
        "Treatment Completed Letter",
        "DNA Letter",
        "Active Monitoring Letter"
    ])
    
    st.markdown("---")
    
    # Letter details
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Patient Details")
        patient_name = st.text_input("Patient Name", value="Mr. John Thompson" if scenario_type != "Custom (Fill in all fields)" else "")
        nhs_number = st.text_input("NHS Number", value="1234567890" if scenario_type != "Custom (Fill in all fields)" else "")
        dob = st.date_input("Date of Birth", value=datetime(1980, 5, 15) if scenario_type != "Custom (Fill in all fields)" else None)
        address = st.text_area("Address", value="23 High Street\nLondon\nSW1A 1AA" if scenario_type != "Custom (Fill in all fields)" else "", height=100)
    
    with col2:
        st.subheader("📅 Letter Details")
        letter_date = st.date_input("Letter Date", value=datetime.now())
        specialty = st.selectbox("Specialty", [
            "Cardiology", "Orthopaedics", "ENT", "General Surgery", 
            "Urology", "Gastroenterology", "Neurology", "Dermatology"
        ])
        consultant_name = st.text_input("Consultant/GP Name", value="Dr. Sarah Williams" if scenario_type != "Custom (Fill in all fields)" else "")
        practice_hospital = st.text_input("Practice/Hospital", value="Grove Medical Centre" if scenario_type != "Custom (Fill in all fields)" else "")
    
    st.markdown("---")
    st.subheader("📝 Clinical Content")
    
    col1, col2 = st.columns(2)
    
    with col1:
        clinical_history = st.text_area("Clinical History/Symptoms", 
                                       value="Chest pain on exertion for past 3 months" if scenario_type == "GP Referral - Cardiology" else "",
                                       height=150,
                                       placeholder="Describe the patient's condition, symptoms, duration...")
        
        current_meds = st.text_area("Current Medications", 
                                   value="",
                                   height=100,
                                   placeholder="List any current medications...")
    
    with col2:
        investigations = st.text_area("Investigations/Tests Requested or Done", 
                                     value="ECG required\nEchocardiogram required" if scenario_type == "GP Referral - Cardiology" else "",
                                     height=150,
                                     placeholder="e.g., MRI scan, Blood tests, X-ray...")
        
        plan_action = st.text_area("Plan/Action Required", 
                                  value="Urgent cardiology assessment\nBook within 2 weeks" if scenario_type == "GP Referral - Cardiology" else "",
                                  height=100,
                                  placeholder="What should happen next?")
    
    # Additional options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        is_urgent = st.checkbox("Urgent/2WW Referral", value=False)
    
    with col2:
        copy_to_gp = st.checkbox("Copy to GP", value=True)
    
    with col3:
        followup_required = st.checkbox("Follow-up Required", value=False)
    
    if followup_required:
        followup_time = st.text_input("Follow-up timeframe", value="6 weeks", placeholder="e.g., 6 weeks, 3 months")
    else:
        followup_time = ""
    
    st.markdown("---")
    
    if st.button("✨ Generate Clinic Letter", type="primary"):
        
        # Generate the letter
        urgency_text = "URGENT - 2 WEEK WAIT" if is_urgent else ""
        
        letter = f"""
{"=" * 70}
{practice_hospital}
{"=" * 70}

Date: {letter_date.strftime('%d/%m/%Y')}
{"URGENT - 2 WEEK WAIT REFERRAL" if is_urgent else ""}

Dear {"Consultant" if "Referral" in scenario_type else "Patient"},

RE: {patient_name}
NHS Number: {nhs_number}
DOB: {dob.strftime('%d/%m/%Y') if dob else ""}
Address: {address}

{"I am writing to refer this patient for " + specialty.lower() + " assessment." if "Referral" in scenario_type else "Thank you for attending clinic."}

Clinical History:
{clinical_history}

{"Current Medications:" if current_meds else ""}
{current_meds if current_meds else "No regular medications"}

{"Investigations Requested:" if "Referral" in scenario_type and investigations else ""}
{"Investigations Performed:" if "Results" in scenario_type or "Outcome" in scenario_type else ""}
{investigations if investigations else ""}

Plan:
{plan_action}

{f"Follow-up: Review in {followup_time}" if followup_required else ""}

{"Copy to GP" if copy_to_gp and "Referral" not in scenario_type else ""}

Yours sincerely,

{consultant_name}
{specialty + " Department" if "Referral" not in scenario_type else "GP Partner"}
{practice_hospital}
{"=" * 70}
        """
        
        st.success("✅ Clinic Letter Generated Successfully!")
        
        st.subheader("📄 Your Clinic Letter")
        st.text_area("Generated Letter (Copy this)", letter.strip(), height=500)
        
        # Copy button helper
        st.info("💡 **Next Steps:**\n1. Copy the letter above\n2. Upload to your PAS simulation (Patient Documents)\n3. Practice registering the patient and booking appointments!")
        
        # What RTT code should this be?
        st.markdown("---")
        st.subheader("🎯 Training Question")
        
        expected_code = ""
        if "Referral" in scenario_type:
            expected_code = "10"
            hint = "This is a referral letter - starts a new RTT pathway"
        elif "Decision to Treat" in scenario_type:
            expected_code = "20"
            hint = "Decision to treat has been made - pathway continues"
        elif "Discharge" in scenario_type:
            expected_code = "34"
            hint = "Patient discharged with no treatment - clock stops"
        elif "Treatment Completed" in scenario_type:
            expected_code = "30"
            hint = "First definitive treatment completed - clock stops"
        elif "DNA" in scenario_type:
            expected_code = "33"
            hint = "Patient did not attend - special handling required"
        elif "Active Monitoring" in scenario_type:
            expected_code = "32"
            hint = "Active monitoring started - clock pauses"
        else:
            expected_code = "20"
            hint = "Review the letter content carefully"
        
        with st.expander("🎓 What RTT code should this letter get?"):
            student_answer = st.selectbox("Your answer:", 
                                         ["Select...", "10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36"],
                                         key="student_code")
            
            if st.button("Check Answer"):
                if student_answer == expected_code:
                    st.success(f"✅ CORRECT! This should be Code {expected_code}")
                    st.info(f"💡 {hint}")
                elif student_answer != "Select...":
                    st.error(f"❌ Not quite. The correct answer is Code {expected_code}")
                    st.info(f"💡 {hint}")
        
        # Download option
        st.markdown("---")
        if st.button("💾 Download Letter as Text File"):
            st.download_button(
                label="⬇️ Download Letter",
                data=letter.strip(),
                file_name=f"Clinic_Letter_{patient_name.replace(' ', '_')}_{letter_date.strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )


# ============================================
# TOOL 8: TRAINING LIBRARY (NEW!)
# ============================================
elif tool == "🎓 Training Library":
    st.header("🎓 RTT Training Library")
    st.markdown("Practice RTT validation with real scenarios and instant feedback!")
    
    # Import modular access
    from modular_access_system import user_has_module_access
    
    scenarios = get_all_scenarios()
    
    # Get user's accessible scenarios
    user_email = st.session_state.user_email
    
    # Check if user has full training library access
    has_full_access = user_has_module_access(user_email, "training_library")
    
    # Count accessible scenarios
    accessible_count = 0
    for scenario in scenarios:
        scenario_id = f"scenario_{scenario['id']:02d}"
        if has_full_access or user_has_module_access(user_email, scenario_id):
            accessible_count += 1
    
    st.markdown(f"### 📚 Scenarios Available: {accessible_count}/{len(scenarios)}")
    
    if accessible_count < len(scenarios):
        st.info(f"🔒 You have access to {accessible_count} scenarios. Upgrade to unlock all {len(scenarios)} scenarios!")
    
    for scenario in scenarios:
        scenario_id = f"scenario_{scenario['id']:02d}"
        has_access = has_full_access or user_has_module_access(user_email, scenario_id)
        
        # Icon based on access
        icon = "✅" if has_access else "🔒"
        
        with st.expander(f"{icon} Scenario {scenario['id']}: {scenario['title']} - {scenario['difficulty']}", expanded=False):
            st.markdown(f"**Difficulty:** {scenario['difficulty']}")
            
            if has_access:
                # User has access - show full content
                st.markdown("**Letter:**")
                st.text_area("Clinic Letter", scenario['letter'], height=200, key=f"letter_{scenario['id']}", disabled=True)
                
                st.markdown("---")
                st.markdown("**Your Answer:**")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    user_answer = st.selectbox(
                        "What RTT code should this letter get?",
                        ["Select...", "10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92", "98"],
                        key=f"answer_{scenario['id']}"
                    )
                
                with col2:
                    check_btn = st.button("Check Answer", key=f"check_{scenario['id']}")
                
                if check_btn and user_answer != "Select...":
                    result = check_scenario_answer(scenario['id'], user_answer)
                    
                    if result['correct']:
                        st.success(f"✅ CORRECT! Well done!")
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: Code {result['correct_answer']}")
                    
                    st.info(f"**Explanation:** {result['explanation']}")
                    
                    st.markdown("**Key Points:**")
                    for point in result['key_points']:
                        st.markdown(f"- {point}")
                    
                    st.markdown("**Expected Actions:**")
                    for action in result['expected_actions']:
                        st.markdown(f"- ✅ {action}")
            
            else:
                # User doesn't have access - show preview
                st.warning("🔒 **This scenario is locked**")
                st.markdown("**Preview:**")
                st.markdown(scenario['letter'][:200] + "... [Locked]")
                st.markdown("---")
                st.info("""
                **Unlock this scenario:**
                - Purchase individual scenario (£29)
                - Get 5 scenarios bundle (£99)
                - Get full Training Library access (£299)
                
                Contact admin to upgrade!
                """)
                
                if st.button("📧 Request Access", key=f"request_{scenario['id']}"):
                    st.success("✅ Access request sent to admin!")


# ============================================
# TOOL 9: INTERACTIVE LEARNING CENTER (NEW!) 🎮
# ============================================
elif tool == "🎮 Interactive Learning Center":
    st.header("🎮 Interactive RTT Learning Center")
    st.markdown("**Gamified AI-Powered Learning System** - Learn faster with interactive quizzes!")
    
    # Initialize session state for progress tracking
    if 'student_progress' not in st.session_state:
        st.session_state.student_progress = StudentProgress("Student")
    if 'current_quiz_index' not in st.session_state:
        st.session_state.current_quiz_index = 0
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = datetime.now()
    
    progress = st.session_state.student_progress
    
    # Top stats dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏆 Total Points", progress.total_points)
    with col2:
        st.metric("✅ Accuracy", f"{progress.get_accuracy()}%")
    with col3:
        st.metric("🔥 Current Streak", progress.current_streak)
    with col4:
        st.metric("📊 Completed", progress.quizzes_completed)
    
    # Badges earned
    if progress.badges_earned:
        st.markdown("---")
        st.subheader("🏅 Your Badges")
        badge_cols = st.columns(len(progress.badges_earned))
        for idx, badge_id in enumerate(progress.badges_earned):
            with badge_cols[idx]:
                badge_info = BADGES.get(badge_id, {})
                st.markdown(f"**{badge_info.get('name', badge_id)}**")
                st.caption(badge_info.get('description', ''))
    
    st.markdown("---")
    
    # Learning mode selection
    st.subheader("🎯 Choose Your Learning Mode")
    
    mode = st.radio("Select Mode:", [
        "📚 Practice Mode (Learn at your own pace)",
        "⚡ Challenge Mode (60 seconds per question!)",
        "🎲 Random Quiz (Surprise me!)",
        "📊 Progress Dashboard"
    ], horizontal=False)
    
    # Initialize timer for challenge mode
    if 'challenge_time_left' not in st.session_state:
        st.session_state.challenge_time_left = 60
    if 'challenge_active' not in st.session_state:
        st.session_state.challenge_active = False
    
    if mode == "📊 Progress Dashboard":
        st.markdown("---")
        st.subheader("📊 Your Learning Progress")
        
        summary = progress.get_summary()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📈 Statistics:**")
            st.markdown(f"- Total Points: **{summary['total_points']}**")
            st.markdown(f"- Quizzes Completed: **{summary['quizzes_completed']}**")
            st.markdown(f"- Accuracy: **{summary['accuracy']}%**")
            st.markdown(f"- Best Streak: **{summary['best_streak']}**")
            
        with col2:
            st.markdown("**🏅 Achievements:**")
            if summary['badges']:
                for badge_id in summary['badges']:
                    badge_info = BADGES.get(badge_id, {})
                    st.markdown(f"- {badge_info.get('name', badge_id)}")
            else:
                st.markdown("_No badges yet - keep learning!_")
        
        # Progress bar
        total_quizzes = len(INTERACTIVE_QUIZZES)
        progress_pct = (summary['quizzes_completed'] / total_quizzes) * 100 if total_quizzes > 0 else 0
        st.progress(progress_pct / 100)
        st.caption(f"Completed {summary['quizzes_completed']} of {total_quizzes} quizzes ({progress_pct:.1f}%)")
        
        # Leaderboard
        st.markdown("---")
        st.subheader("🏆 Global Leaderboard - Top 10")
        
        leaderboard = get_leaderboard()
        if leaderboard:
            leaderboard_data = []
            for idx, entry in enumerate(leaderboard, 1):
                rank_emoji = ["🥇", "🥈", "🥉"][idx-1] if idx <= 3 else f"{idx}."
                leaderboard_data.append({
                    "Rank": rank_emoji,
                    "Name": entry['name'],
                    "Points": entry['points'],
                    "Accuracy": f"{entry['accuracy']}%"
                })
            
            st.table(pd.DataFrame(leaderboard_data))
        else:
            st.info("Be the first on the leaderboard! Complete some quizzes to get started.")
        
        # Add to leaderboard button
        if st.button("📤 Submit My Score to Leaderboard"):
            student_name = st.text_input("Enter your name (or nickname):", "Anonymous")
            if student_name:
                add_to_leaderboard(student_name, summary['total_points'], summary['accuracy'])
                st.success(f"✅ Added {student_name} to leaderboard!")
                st.balloons()
    
    else:
        # Quiz mode
        st.markdown("---")
        
        # Filter options
        difficulty_filter = st.selectbox("Filter by Difficulty:", ["All", "Easy", "Medium", "Hard", "Expert"])
        
        # Get available quizzes
        if difficulty_filter == "All":
            available_quizzes = INTERACTIVE_QUIZZES
        else:
            available_quizzes = get_quiz_by_difficulty(difficulty_filter)
        
        if not available_quizzes:
            st.warning("No quizzes available for this difficulty level yet!")
        else:
            # Current quiz
            quiz_index = st.session_state.current_quiz_index % len(available_quizzes)
            current_quiz = available_quizzes[quiz_index]
            
            st.subheader(f"Question {quiz_index + 1} of {len(available_quizzes)}")
            st.markdown(f"**Difficulty:** {current_quiz['difficulty']} | **Category:** {current_quiz['category']} | **Points:** {current_quiz['points']}")
            
            # Challenge Mode Timer
            if mode == "⚡ Challenge Mode (60 seconds per question!)":
                st.warning(f"⏱️ **TIME REMAINING: {st.session_state.challenge_time_left} seconds**")
                if st.session_state.challenge_time_left <= 10:
                    st.error("⚠️ HURRY! Time running out!")
            
            st.markdown("---")
            st.markdown(f"### {current_quiz['question']}")
            
            # Question type handling
            if current_quiz['type'] == 'multiple_choice':
                user_answer = st.radio("Select your answer:", current_quiz['options'], key=f"mcq_{quiz_index}")
            
            elif current_quiz['type'] == 'true_false':
                user_answer = st.radio("Select your answer:", ["True", "False"], key=f"tf_{quiz_index}")
            
            elif current_quiz['type'] == 'fill_blank':
                user_answer = st.text_input("Enter your answer:", key=f"fib_{quiz_index}")
            
            elif current_quiz['type'] == 'drag_drop':
                st.info("💡 Match each scenario to the correct code:")
                user_answer = {}
                for pair in current_quiz['pairs']:
                    user_answer[pair['scenario']] = st.selectbox(
                        pair['scenario'], 
                        [p['code'] for p in current_quiz['pairs']],
                        key=f"dd_{pair['scenario']}"
                    )
            
            elif current_quiz['type'] == 'timeline':
                st.info("💡 Drag to reorder (use selectboxes for now):")
                user_answer = []
                for idx, item in enumerate(current_quiz['items']):
                    position = st.selectbox(f"{item}", list(range(1, len(current_quiz['items'])+1)), key=f"tl_{idx}")
                    user_answer.append(position - 1)
            
            # Submit button
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Submit Answer", type="primary"):
                    # Calculate time taken
                    time_taken = (datetime.now() - st.session_state.quiz_start_time).total_seconds()
                    
                    # Check answer
                    result = check_quiz_answer(current_quiz['id'], user_answer)
                    
                    if result:
                        if result['correct']:
                            st.success(f"🎉 **CORRECT!** +{result['points_earned']} points")
                            st.balloons()
                        else:
                            st.error(f"❌ Incorrect. The correct answer is: **{result['correct_answer']}**")
                        
                        # Show explanation
                        st.info(f"💡 **Explanation:** {result['explanation']}")
                        
                        # Show video if available
                        if 'video_url' in current_quiz and current_quiz['video_url']:
                            st.markdown("---")
                            st.markdown("📹 **Watch Video Explanation:**")
                            st.video(current_quiz['video_url'])
                        
                        # Update progress
                        progress.add_quiz_result(
                            current_quiz['id'], 
                            result['correct'], 
                            result['points_earned'],
                            time_taken
                        )
                        
                        # Check for new badges
                        new_badges = [b for b in progress.badges_earned if b not in st.session_state.get('shown_badges', [])]
                        if new_badges:
                            st.success(f"🏅 **NEW BADGE UNLOCKED:** {BADGES[new_badges[-1]]['name']}")
                            if 'shown_badges' not in st.session_state:
                                st.session_state.shown_badges = []
                            st.session_state.shown_badges.extend(new_badges)
                    
                    # Reset timer for next question
                    st.session_state.quiz_start_time = datetime.now()
            
            with col2:
                if st.button("➡️ Next Question"):
                    st.session_state.current_quiz_index += 1
                    st.session_state.quiz_start_time = datetime.now()
                    st.rerun()
            
            # Quick navigation
            st.markdown("---")
            st.markdown("**📍 Quick Jump:**")
            jump_to = st.selectbox("Go to question:", list(range(1, len(available_quizzes)+1)), index=quiz_index)
            if st.button("🚀 Jump"):
                st.session_state.current_quiz_index = jump_to - 1
                st.rerun()


# ============================================
# TOOL 10: CERTIFICATION EXAM (NEW!) 🎓
# ============================================
elif tool == "🎓 Certification Exam":
    st.header("🎓 RTT Certification Exam")
    st.markdown("**Become a Certified RTT Professional!**")
    
    st.info("""📜 **Official T21 RTT Certification:**
    - 50 comprehensive questions
    - 90-minute time limit
    - 80% pass mark required
    - Downloadable PDF certificate
    - Unique verification code
    - Valid for 2 years
    - Recognized by NHS employers
    """)
    
    # Initialize exam state
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'exam_data' not in st.session_state:
        st.session_state.exam_data = None
    if 'exam_answers' not in st.session_state:
        st.session_state.exam_answers = {}
    
    if not st.session_state.exam_started:
        st.markdown("---")
        st.subheader("📋 Exam Requirements")
        
        st.markdown("""
        **Before starting the exam:**
        - ✅ Complete at least 20 practice quizzes
        - ✅ Achieve 70%+ accuracy in practice mode
        - ✅ Review all RTT codes (10-39)
        - ✅ Understand cancer pathways
        - ✅ Know clock management rules
        
        **Exam Rules:**
        - 🕐 90 minutes to complete
        - 📝 50 multiple-choice questions
        - 🎯 80% score required to pass
        - ❌ No retakes for 7 days if you fail
        - ✅ Certificate issued immediately upon passing
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            student_name = st.text_input("Enter your full name (for certificate):", placeholder="John David Smith")
        
        with col2:
            student_email = st.text_input("Email address:", placeholder="your.email@example.com")
        
        agree = st.checkbox("I understand the exam rules and I'm ready to begin")
        
        if st.button("🚀 Start Certification Exam", type="primary", disabled=not agree or not student_name):
            if student_name and agree:
                st.session_state.exam_data = generate_exam(randomize=True)
                st.session_state.exam_started = True
                st.session_state.student_name = student_name
                st.session_state.student_email = student_email
                st.success("✅ Exam started! Good luck!")
                st.rerun()
    
    else:
        # Exam in progress
        exam_data = st.session_state.exam_data
        
        st.warning(f"⏱️ **EXAM IN PROGRESS** - Time limit: 90 minutes")
        st.markdown(f"**Student:** {st.session_state.student_name}")
        
        # Progress bar
        answered = len(st.session_state.exam_answers)
        total = len(exam_data['questions'])
        progress_pct = answered / total if total > 0 else 0
        
        st.progress(progress_pct)
        st.caption(f"Answered: {answered}/{total} questions")
        
        st.markdown("---")
        
        # Display questions
        for idx, question in enumerate(exam_data['questions'], 1):
            with st.expander(f"Question {idx}", expanded=(idx == 1)):
                st.markdown(f"**{question['question']}**")
                
                answer = st.radio(
                    "Select your answer:",
                    question['options'],
                    key=f"exam_q_{question['id']}",
                    index=None
                )
                
                if answer:
                    st.session_state.exam_answers[question['id']] = answer
        
        st.markdown("---")
        
        # Submit exam
        if answered == total:
            st.success("✅ All questions answered! Ready to submit.")
            
            if st.button("📤 Submit Exam for Grading", type="primary"):
                with st.spinner("Grading your exam..."):
                    result = grade_exam(exam_data, st.session_state.exam_answers)
                    
                    st.markdown("---")
                    st.header("📊 Exam Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Score", f"{result['score_percentage']}%")
                    with col2:
                        st.metric("Correct Answers", f"{result['correct_answers']}/{result['total_questions']}")
                    with col3:
                        st.metric("Pass Mark", f"{result['pass_mark']}%")
                    
                    if result['passed']:
                        st.success("🎉 **CONGRATULATIONS! YOU PASSED!**")
                        st.balloons()
                        
                        # Generate certificate
                        certificate = generate_certificate(st.session_state.student_name, result)
                        
                        if certificate:
                            st.markdown("---")
                            st.subheader("📜 Your Official Certificate")
                            
                            st.info(f"""
                            **Certificate Details:**
                            - Certificate Number: {certificate['certificate_number']}
                            - Verification Code: {certificate['verification_code']}
                            - Valid Until: {certificate['valid_until']}
                            - Score: {certificate['score']}%
                            """)
                            
                            # Certificate download
                            cert_html = format_certificate_html(certificate)
                            
                            st.download_button(
                                label="⬇️ Download Certificate (HTML)",
                                data=cert_html,
                                file_name=f"T21_RTT_Certificate_{st.session_state.student_name.replace(' ', '_')}.html",
                                mime="text/html"
                            )
                            
                            st.info("💡 Open the HTML file in your browser and print to PDF (Ctrl+P → Save as PDF)")
                    
                    else:
                        st.error(f"❌ **YOU SCORED {result['score_percentage']}% - DID NOT PASS**")
                        st.warning("You need 80% to pass. Review the material and try again in 7 days.")
                        
                        # Show incorrect answers
                        st.markdown("---")
                        st.subheader("📝 Review Your Mistakes")
                        
                        incorrect = [r for r in result['results'] if not r['correct']]
                        
                        for mistake in incorrect[:10]:  # Show first 10 mistakes
                            st.error(f"**{mistake['question']}**")
                            st.markdown(f"Your answer: {mistake['user_answer']}")
                            st.markdown(f"Correct answer: {mistake['correct_answer']}")
                    
                    # Reset exam
                    if st.button("🔄 Close Results"):
                        st.session_state.exam_started = False
                        st.session_state.exam_data = None
                        st.session_state.exam_answers = {}
                        st.rerun()
        
        else:
            st.warning(f"⚠️ Please answer all questions before submitting ({total - answered} remaining)")


# ============================================
# TOOL 11: AI RTT TUTOR (NEW!) 🤖
# ============================================
elif tool == "🤖 AI RTT Tutor":
    st.header("🤖 AI RTT Tutor - Your 24/7 Learning Assistant")
    st.markdown("**Ask me ANYTHING about RTT!** I'm here to help you learn faster! 🚀")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ChatHistory()
    
    chat = st.session_state.chat_history
    
    # Info box
    st.info("""💡 **What can the AI Tutor help with?**
    - Explain any RTT code (10-39)
    - When does the clock start/stop/pause?
    - NHS targets (18-week, 2WW, 62-day)
    - Breach prevention
    - PAS systems
    - Real-world scenarios
    - And much more!
    
    **Just type your question below!** 👇
    """)
    
    # Quick question buttons
    st.markdown("### 🔥 Quick Questions:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("❓ What code for DNA?"):
            user_question = "What code when patient DNA?"
            st.session_state.quick_question = user_question
    
    with col2:
        if st.button("⏰ When does clock stop?"):
            user_question = "When does the RTT clock stop?"
            st.session_state.quick_question = user_question
    
    with col3:
        if st.button("🎯 What's 18-week target?"):
            user_question = "What's the 18-week target?"
            st.session_state.quick_question = user_question
    
    st.markdown("---")
    
    # Chat interface
    st.subheader("💬 Chat with AI Tutor")
    
    # Display chat history
    if chat.messages:
        st.markdown("### 📜 Conversation History:")
        for msg in chat.get_history(limit=20):
            if msg['role'] == 'user':
                st.markdown(f"**🧑 You:** {msg['content']}")
            else:
                st.markdown(f"**🤖 AI Tutor:** {msg['content']}")
                st.markdown("---")
    
    # User input
    user_question = st.text_area(
        "💬 Ask your question:",
        placeholder="e.g., What code should I use when a patient DNA'd?",
        help="Be as specific as possible for the best answer!",
        key="user_question_input"
    )
    
    # Handle quick question
    if 'quick_question' in st.session_state:
        user_question = st.session_state.quick_question
        del st.session_state.quick_question
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        ask_button = st.button("🚀 Ask AI Tutor", type="primary")
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            chat.clear()
            st.success("Chat cleared!")
            st.rerun()
    
    with col3:
        if chat.messages:
            chat_export = chat.export()
            st.download_button(
                label="📥 Export Chat",
                data=chat_export,
                file_name=f"ai_tutor_chat_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # Process question
    if ask_button and user_question:
        with st.spinner("🤔 AI Tutor is thinking..."):
            # Add user message to history
            chat.add_message('user', user_question)
            
            # Get AI response
            ai_response = answer_question(user_question)
            
            # Add related quiz suggestion
            ai_response += generate_related_quiz(user_question)
            
            # Add AI response to history
            chat.add_message('assistant', ai_response)
            
            # Display response
            st.markdown("---")
            st.markdown("### 🤖 AI Tutor's Answer:")
            st.markdown(ai_response)
            
            # Success message
            st.success("✅ Answer provided! Ask another question or try the suggested quiz!")
    
    elif ask_button and not user_question:
        st.warning("⚠️ Please enter a question first!")
    
    # Code lookup section
    st.markdown("---")
    st.subheader("📋 Quick Code Lookup")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        code_number = st.selectbox(
            "Select RTT Code:",
            ["10", "11", "12", "20", "21", "30", "31", "32", "33", "34", "35", "36", "90", "91", "92"]
        )
    
    with col2:
        if st.button("📖 Show Code Info"):
            code_info = get_code_info(code_number)
            if code_info:
                st.markdown(code_info)
    
    # Premium upgrade CTA
    st.markdown("---")
    st.info("""
    🌟 **Upgrade to AI Tutor Premium** for:
    - ✅ Unlimited questions (no daily limit)
    - ✅ Priority response
    - ✅ Advanced explanations
    - ✅ Custom scenarios
    - ✅ 24/7 availability
    
    **Only £19.99/month!**
    
    [Contact us to upgrade →]
    """)


# ============================================
# TOOL 12: INTERACTIVE REPORTS (NEW!) 📊
# ============================================
elif tool == "📊 Interactive Reports":
    st.header("📊 Interactive Reports & Analytics")
    st.markdown("**Replace Excel with built-in dashboards!**")
    
    st.info("""✨ **Why this is better than Excel:**
    - ✅ Real-time interactive charts
    - ✅ No manual data entry
    - ✅ Automated insights
    - ✅ Beautiful visualizations
    - ✅ Download as CSV or PDF
    - ✅ Works on any device
    """)
    
    report_type = st.selectbox("Select Report Type:", [
        "📈 Student Progress Report",
        "🎯 Quiz Performance Analysis",
        "🏆 Leaderboard Export",
        "📋 Validation History Report",
        "📊 Overall Statistics"
    ])
    
    st.markdown("---")
    
    if report_type == "📈 Student Progress Report":
        st.subheader("📈 Your Learning Progress")
        
        if 'student_progress' in st.session_state:
            progress = st.session_state.student_progress
            summary = progress.get_summary()
            
            # Generate report
            report = generate_student_progress_report(summary)
            
            # Display key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Points", report['summary']['total_points'])
                st.metric("Accuracy", f"{report['summary']['accuracy']}%")
            
            with col2:
                st.metric("Quizzes Completed", report['summary']['quizzes_completed'])
                st.metric("Best Streak", report['summary']['best_streak'])
            
            with col3:
                st.metric("Badges Earned", report['summary']['badges_earned'])
                st.metric("Hours Spent", report['summary']['time_spent_hours'])
            
            # Strengths & Weaknesses
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💪 Strengths")
                for strength in report['strengths']:
                    st.success(f"✅ {strength}")
            
            with col2:
                st.subheader("🎯 Areas to Improve")
                for weakness in report['areas_for_improvement']:
                    st.warning(f"→ {weakness}")
            
            # Recommendations
            st.markdown("---")
            st.subheader("📚 Personalized Recommendations")
            
            for rec in report['recommendations']:
                st.info(rec)
            
            # Download options
            st.markdown("---")
            st.subheader("📥 Download Report")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV export
                csv_data = generate_csv_export(report, 'student_progress')
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv_data,
                    file_name=f"Progress_Report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Text export
                text_report = format_report_for_print(report)
                st.download_button(
                    label="⬇️ Download as TXT",
                    data=text_report,
                    file_name=f"Progress_Report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        
        else:
            st.warning("No progress data available. Complete some quizzes first!")
    
    elif report_type == "📊 Overall Statistics":
        st.subheader("📊 System-Wide Statistics")
        
        st.markdown(f"""
        **Platform Metrics:**
        - Total Interactive Quizzes: {len(INTERACTIVE_QUIZZES)}
        - Total Training Scenarios: 20
        - Total RTT Codes Covered: 16
        - Difficulty Levels: 4 (Easy, Medium, Hard, Expert)
        - Categories: 10+
        """)
        
        # Quiz distribution
        easy_count = len([q for q in INTERACTIVE_QUIZZES if q['difficulty'] == 'Easy'])
        medium_count = len([q for q in INTERACTIVE_QUIZZES if q['difficulty'] == 'Medium'])
        hard_count = len([q for q in INTERACTIVE_QUIZZES if q['difficulty'] == 'Hard'])
        expert_count = len([q for q in INTERACTIVE_QUIZZES if q['difficulty'] == 'Expert'])
        
        st.markdown("**Quiz Difficulty Distribution:**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Easy", easy_count)
        with col2:
            st.metric("Medium", medium_count)
        with col3:
            st.metric("Hard", hard_count)
        with col4:
            st.metric("Expert", expert_count)


# ============================================
# TOOL 13: JOB INTERVIEW PREP (NEW!)
# ============================================
elif tool == "💼 Job Interview Prep":
    st.header("💼 Job Interview Preparation Assistant")
    st.markdown("**Career support for ALL T21 students!** Prepare for ANY job interview with AI-powered question generator!")
    
    st.info("""📋 **Supports ALL career paths:**
    ✅ Healthcare Assistant / Care Worker
    ✅ Adult Social Care
    ✅ Teaching Assistant
    ✅ Customer Service
    ✅ Business Administration
    ✅ IT Support
    ✅ RTT Validation & NHS Admin
    ✅ And ANY other role!
    
    **You'll get:**
    - 40-50+ likely interview questions
    - FULL answers to ALL questions (STAR method)
    - Organization research (mission, vision, values)
    - Preparation checklists
    - Questions to ask them
    - Common mistakes to avoid
    """)
    
    # Job Details
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title", placeholder="e.g., RTT Validation Officer")
        company_name = st.text_input("Organization/Trust Name", placeholder="e.g., Royal London Hospital NHS Trust")
    
    with col2:
        interview_date = st.date_input("Interview Date (if known)", value=None)
        interview_format = st.selectbox("Interview Format", ["Not sure", "Face-to-face", "Video call (Teams/Zoom)", "Phone", "Panel interview"])
    
    st.markdown("---")
    st.subheader("📄 Job Description")
    
    # File upload option
    upload_method = st.radio("How do you want to provide the job description?", 
                            ["📝 Type/Paste Text", "📎 Upload Document (PDF/Word)"],
                            horizontal=True)
    
    job_description = ""
    
    if upload_method == "📎 Upload Document (PDF/Word)":
        uploaded_file = st.file_uploader("Upload Job Description (PDF or Word)", 
                                        type=['pdf', 'docx', 'doc'],
                                        help="Upload the job description document")
        
        if uploaded_file is not None:
            try:
                # Extract text from uploaded file
                if uploaded_file.name.endswith('.pdf'):
                    try:
                        import PyPDF2
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        job_description = ""
                        for page in pdf_reader.pages:
                            job_description += page.extract_text()
                        st.success(f"✅ PDF uploaded! Extracted {len(job_description)} characters")
                    except ImportError:
                        st.error("PDF support not available. Please install PyPDF2: pip install PyPDF2")
                        st.info("Or paste the job description text below instead.")
                
                elif uploaded_file.name.endswith(('.docx', '.doc')):
                    try:
                        from docx import Document
                        doc = Document(uploaded_file)
                        job_description = "\n".join([para.text for para in doc.paragraphs])
                        st.success(f"✅ Word document uploaded! Extracted {len(job_description)} characters")
                    except ImportError:
                        st.error("Word support not available. Please install python-docx: pip install python-docx")
                        st.info("Or paste the job description text below instead.")
                
                # Show extracted text
                if job_description:
                    with st.expander("📄 View Extracted Text", expanded=False):
                        st.text_area("Extracted Job Description", job_description, height=200, disabled=True)
            
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                st.info("Please try pasting the text manually below.")
    
    else:
        # Manual text input
        job_description = st.text_area(
            "Paste the full job description here:",
            height=300,
            placeholder="""EXAMPLES (Any role works!):

Healthcare Assistant:
"We are seeking a caring Healthcare Assistant to join our team. You will provide personal care, monitor vital signs, support patients with daily living activities..."

Teaching Assistant:
"Primary school seeks Teaching Assistant to support children with SEN. Experience with behavior management and differentiation required..."

Customer Service:
"Join our busy reception team. Handle patient queries, book appointments, manage phone calls..."

Adult Social Care:
"Care Worker needed for domiciliary care. Provide personal care in service users' homes, medication support, meal preparation..."

Business Admin:
"Administrative Assistant for busy NHS department. Data entry, filing, meeting coordination..."

RTT Validation:
"Validate RTT pathways, ensure 18-week compliance, work with PAS systems..."

Just paste ANY job description here!"""
        )
    
    if st.button("🎯 Generate Interview Preparation Pack", type="primary"):
        if not job_title or not job_description:
            st.error("Please enter job title and job description!")
        else:
            with st.spinner("⚡ Analyzing job description and generating interview prep pack..."):
                result = analyze_job_description(job_title, job_description, company_name)
                
                st.success("✅ Interview Prep Pack Generated!")
                
                # ===== LIKELY INTERVIEW QUESTIONS =====
                st.markdown("---")
                st.subheader("🎯 Likely Interview Questions")
                
                st.markdown(f"**Based on this job description, you're likely to be asked {len(result['interview_questions'])} types of questions:**")
                
                # Group by category
                categories = {}
                for q in result['interview_questions']:
                    cat = q['category']
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append(q)
                
                # Display by category
                for category, questions in categories.items():
                    with st.expander(f"📌 {category} Questions ({len(questions)})", expanded=True):
                        for i, q in enumerate(questions, 1):
                            st.markdown(f"**Q{i}. {q['question']}**")
                            st.markdown(f"*Why they ask this:* {q['why_asked']}")
                            st.markdown(f"*Likelihood:* {q['likelihood']}")
                            st.markdown("")
                
                # ===== EXAMPLE ANSWERS =====
                st.markdown("---")
                st.subheader("💡 Example Answers (STAR Method)")
                st.info("📝 **Professional example answers** - Use these as templates for your responses!")
                
                if result['example_answers']:
                    for i, answer in enumerate(result['example_answers'], 1):
                        with st.expander(f"📝 Answer #{i}: {answer['question']}", expanded=(i==1)):
                            # GPT-4 generated answers have 'answer' field, old ones have 'example_answer'
                            answer_text = answer.get('answer', answer.get('example_answer', ''))
                            st.markdown(answer_text)
                            
                            # Old format tips
                            if answer.get('tips'):
                                st.markdown("---")
                                st.markdown("**Additional Tips:**")
                                for tip in answer['tips']:
                                    st.markdown(f"- ✅ {tip}")
                else:
                    st.warning("⚠️ No example answers generated. Please try regenerating the prep pack.")
                
                # ===== PREPARATION TIPS =====
                st.markdown("---")
                st.subheader("📚 Preparation Checklist")
                
                prep_tips = result['preparation_tips']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Before the Interview:**")
                    for tip in prep_tips['before_interview']:
                        st.markdown(f"- [ ] {tip}")
                    
                    if prep_tips['technical_prep']:
                        st.markdown("**Technical Preparation:**")
                        for tip in prep_tips['technical_prep']:
                            st.markdown(f"- [ ] {tip}")
                
                with col2:
                    st.markdown("**On the Day:**")
                    for tip in prep_tips['on_the_day']:
                        st.markdown(f"- [ ] {tip}")
                    
                    st.markdown("**Documents to Bring:**")
                    for doc in prep_tips['key_documents']:
                        st.markdown(f"- [ ] {doc}")
                
                # ===== RESEARCH AREAS =====
                st.markdown("---")
                st.subheader("🔍 Research Areas")
                
                for area in result['research_areas']:
                    with st.expander(f"📖 {area['area']}", expanded=False):
                        st.markdown("**What to find out:**")
                        for item in area['what_to_find']:
                            st.markdown(f"- {item}")
                
                # ===== QUESTIONS TO ASK =====
                st.markdown("---")
                st.subheader("❓ Smart Questions to Ask Them")
                
                smart_questions = generate_smart_questions_to_ask(job_title)
                
                st.markdown("**You MUST have questions prepared! Here are some good ones:**")
                
                for i, q in enumerate(smart_questions, 1):
                    st.markdown(f"**{i}. {q['question']}**")
                    st.markdown(f"   *Why this is good:* {q['why_good']}")
                    st.markdown("")
                
                # ===== RED FLAGS TO AVOID =====
                st.markdown("---")
                st.subheader("🚫 Common Mistakes to AVOID")
                
                red_flags = generate_red_flags_to_avoid()
                
                for flag in red_flags:
                    st.error(f"❌ **{flag['mistake']}**")
                    st.markdown(f"   *Why it's bad:* {flag['why_bad']}")
                    st.success(f"   ✅ *Instead:* {flag['instead']}")
                    st.markdown("")
                
                # ===== DOWNLOAD OPTION =====
                st.markdown("---")
                st.subheader("📥 Download Your Prep Pack")
                
                # Create downloadable text summary
                prep_pack_text = f"""
JOB INTERVIEW PREPARATION PACK
================================
Generated by T21 Services Interview Prep Tool
Date: {datetime.now().strftime('%d/%m/%Y')}

Job Title: {job_title}
Company: {company_name}
Interview Date: {interview_date if interview_date else 'TBD'}

LIKELY INTERVIEW QUESTIONS ({len(result['interview_questions'])} questions)
{'=' * 50}

"""
                for i, q in enumerate(result['interview_questions'], 1):
                    prep_pack_text += f"{i}. {q['question']}\n"
                    prep_pack_text += f"   Category: {q['category']}\n"
                    prep_pack_text += f"   Likelihood: {q['likelihood']}\n"
                    prep_pack_text += f"   Why asked: {q['why_asked']}\n\n"
                
                prep_pack_text += "\n\nPREPARATION CHECKLIST\n"
                prep_pack_text += "=" * 50 + "\n\n"
                
                prep_pack_text += "BEFORE INTERVIEW:\n"
                for tip in prep_tips['before_interview']:
                    prep_pack_text += f"[ ] {tip}\n"
                
                prep_pack_text += "\n\nON THE DAY:\n"
                for tip in prep_tips['on_the_day']:
                    prep_pack_text += f"[ ] {tip}\n"
                
                prep_pack_text += "\n\nQUESTIONS TO ASK:\n"
                for q in smart_questions:
                    prep_pack_text += f"- {q['question']}\n"
                
                st.download_button(
                    label="⬇️ Download Full Prep Pack (Text File)",
                    data=prep_pack_text,
                    file_name=f"Interview_Prep_{job_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                
                st.success("💪 **You've got this! Good luck with your interview!**")


# ============================================
# TOOL 10: CV BUILDER (NEW!) 💰 REVENUE GENERATOR
# ============================================
elif tool == "📄 CV Builder":
    st.header("📄 Professional CV Builder")
    st.markdown("**Create an ATS-optimized, professional CV in minutes!**")
    
    st.info("""✨ **Features:**
    - ✅ Professional templates for all careers
    - ✅ ATS-optimized (beats applicant tracking systems)
    - ✅ Auto-includes your T21 qualifications
    - ✅ Career-specific keywords
    - ✅ Download as HTML (convert to PDF)
    - ✅ BONUS: LinkedIn profile optimizer!
    
    💡 **Perfect for ALL T21 graduates:**
    Healthcare Assistant | Care Worker | Teaching Assistant | Customer Service | Business Admin | RTT Validation
    """)
    
    # Career Path Selection
    st.subheader("Step 1: Select Your Career Path")
    
    st.markdown("**👥 Select the job role you're applying for:**")
    
    career_category = st.radio("Career Category:", [
        "🏥 NHS Pathway & Admin Jobs (RTT, Cancer, Waiting List)",
        "💼 Healthcare & Care Jobs",
        "🎓 Education & Teaching Jobs",
        "💻 Tech & IT Jobs",
        "📊 Business & Professional Jobs"
    ], horizontal=False)
    
    if career_category == "🏥 NHS Pathway & Admin Jobs (RTT, Cancer, Waiting List)":
        career_path = st.selectbox("Select NHS Role:", [
            "RTT Validation Officer / Validator",
            "RTT Navigator / Patient Pathway Navigator",
            "Patient Pathway Coordinator",
            "Pathway Assistant / Coordinator",
            "Cancer Pathway Tracker / Data Officer",
            "Waiting List Coordinator / Administrator",
            "Booking Officer / Administrator",
            "Appointment Administrator",
            "MDT Administrator / Coordinator",
            "Medical Secretary",
            "Data Officer / Information Quality Officer",
            "Clerical Officer (NHS)",
            "Other NHS Admin Role"
        ])
    elif career_category == "💼 Healthcare & Care Jobs":
        career_path = st.selectbox("Select Healthcare Role:", [
            "Healthcare Assistant / HCA",
            "Care Worker / Support Worker",
            "Adult Social Care Worker",
            "Customer Service / Reception"
        ])
    elif career_category == "🎓 Education & Teaching Jobs":
        career_path = st.selectbox("Select Education Role:", [
            "Teaching Assistant",
            "Learning Support Assistant",
            "SEN Teaching Assistant"
        ])
    elif career_category == "💻 Tech & IT Jobs":
        career_path = st.selectbox("Select Tech Role:", [
            "Data Analyst",
            "Data Scientist",
            "Software Tester / QA",
            "Business Analyst",
            "Project Manager",
            "IT Support",
            "Web Developer",
            "Python Developer"
        ])
    else:  # Business & Professional
        career_path = st.selectbox("Select Business Role:", [
            "Business Administrator",
            "Digital Marketing Specialist",
            "HR Officer",
            "Bookkeeper / Accountant",
            "Team Leader / Manager"
        ])
    
    # Map to internal career codes
    career_map = {
        # NHS Pathway & Admin
        "RTT Validation Officer / Validator": "rtt_validation",
        "RTT Navigator / Patient Pathway Navigator": "pathway_navigator",
        "Patient Pathway Coordinator": "pathway_coordinator",
        "Pathway Assistant / Coordinator": "pathway_coordinator",
        "Cancer Pathway Tracker / Data Officer": "cancer_tracker",
        "Waiting List Coordinator / Administrator": "waiting_list_admin",
        "Booking Officer / Administrator": "booking_officer",
        "Appointment Administrator": "appointment_admin",
        "MDT Administrator / Coordinator": "mdt_admin",
        "Medical Secretary": "medical_secretary",
        "Data Officer / Information Quality Officer": "data_officer",
        "Clerical Officer (NHS)": "nhs_clerical",
        "Other NHS Admin Role": "rtt_validation",
        
        # Healthcare
        "Healthcare Assistant / HCA": "healthcare_assistant",
        "Care Worker / Support Worker": "care_worker",
        "Adult Social Care Worker": "care_worker",
        "Customer Service / Reception": "customer_service",
        
        # Education
        "Teaching Assistant": "teaching_assistant",
        "Learning Support Assistant": "teaching_assistant",
        "SEN Teaching Assistant": "teaching_assistant",
        
        # Tech
        "Data Analyst": "data_analyst",
        "Data Scientist": "data_scientist",
        "Software Tester / QA": "software_tester",
        "Business Analyst": "business_analyst",
        "Project Manager": "project_manager",
        "IT Support": "it_support",
        "Web Developer": "web_developer",
        "Python Developer": "python_developer",
        
        # Business
        "Business Administrator": "business_admin",
        "Digital Marketing Specialist": "digital_marketing",
        "HR Officer": "hr_officer",
        "Bookkeeper / Accountant": "bookkeeper",
        "Team Leader / Manager": "team_leader"
    }
    career_code = career_map.get(career_path, "healthcare_assistant")
    
    st.markdown("---")
    
    # Personal Information
    st.subheader("Step 2: Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name*", placeholder="John David Smith")
        email = st.text_input("Email Address*", placeholder="john.smith@email.com")
        phone = st.text_input("Phone Number*", placeholder="07700 900123")
    
    with col2:
        location = st.text_input("Location*", placeholder="London, UK")
        linkedin = st.text_input("LinkedIn Profile (optional)", placeholder="linkedin.com/in/yourname")
        years_exp = st.number_input("Years of Experience", min_value=0, max_value=50, value=2)
    
    st.markdown("---")
    
    # Work Experience
    st.subheader("Step 3: Work Experience")
    st.markdown("Add your most recent jobs (most recent first)")
    
    num_jobs = st.number_input("How many jobs to add?", min_value=1, max_value=5, value=2)
    
    work_history = []
    for i in range(num_jobs):
        with st.expander(f"Job #{i+1}", expanded=(i==0)):
            job_title = st.text_input(f"Job Title", key=f"job_title_{i}", placeholder="Healthcare Assistant")
            job_company = st.text_input(f"Company/Organization", key=f"job_company_{i}", placeholder="Royal London Hospital NHS Trust")
            job_dates = st.text_input(f"Dates", key=f"job_dates_{i}", placeholder="Jan 2022 - Present")
            
            st.markdown("**Key Responsibilities (one per line):**")
            responsibilities_text = st.text_area(
                "Responsibilities",
                key=f"responsibilities_{i}",
                height=150,
                placeholder="""Example for Healthcare Assistant:
Provided compassionate personal care to patients on medical ward
Monitored and recorded vital signs (BP, pulse, temperature, oxygen saturation)
Assisted patients with mobility, eating, drinking, and personal hygiene
Maintained patient dignity and respect at all times
Reported changes in patient condition to registered nurses
Followed strict infection control and safeguarding procedures"""
            )
            
            if job_title and job_company and job_dates and responsibilities_text:
                responsibilities = [r.strip() for r in responsibilities_text.split('\n') if r.strip()]
                work_history.append({
                    'title': job_title,
                    'company': job_company,
                    'dates': job_dates,
                    'responsibilities': responsibilities
                })
    
    st.markdown("---")
    
    # Qualifications
    st.subheader("Step 4: Qualifications")
    st.markdown("✨ **Your T21 qualifications will be auto-added!**")
    
    # Get T21 qualifications
    t21_quals = get_t21_qualifications()
    
    st.markdown("**Select your T21 qualifications:**")
    selected_quals = []
    
    for qual in t21_quals:
        if st.checkbox(qual['title'], key=f"qual_{qual['title']}"):
            year = st.text_input(f"Year completed:", key=f"year_{qual['title']}", placeholder="2024")
            selected_quals.append({
                'title': qual['title'],
                'institution': qual['institution'],
                'date': year if year else "2024"
            })
    
    # Additional qualifications
    st.markdown("**Add other qualifications (optional):**")
    additional_qual = st.text_input("Additional Qualification", placeholder="e.g., GCSE English & Maths")
    additional_inst = st.text_input("Institution", placeholder="e.g., Local College")
    additional_year = st.text_input("Year", placeholder="2020")
    
    if additional_qual and additional_inst and additional_year:
        selected_quals.append({
            'title': additional_qual,
            'institution': additional_inst,
            'date': additional_year
        })
    
    st.markdown("---")
    
    # Skills
    st.subheader("Step 5: Key Skills")
    
    # Get career-specific ATS keywords
    suggested_skills = get_ats_keywords(career_code)
    
    st.markdown(f"**Suggested skills for {career_path}:**")
    st.markdown("*(Select at least 8-10 for best results)*")
    
    selected_skills = []
    
    # Display in 3 columns
    cols = st.columns(3)
    for idx, skill in enumerate(suggested_skills):
        with cols[idx % 3]:
            if st.checkbox(skill, key=f"skill_{skill}", value=(idx < 10)):
                selected_skills.append(skill)
    
    # Additional skills
    st.markdown("**Add custom skills:**")
    custom_skills = st.text_input("Custom skills (comma-separated)", placeholder="e.g., First Aid, Manual Handling, Fire Safety")
    
    if custom_skills:
        custom_list = [s.strip() for s in custom_skills.split(',') if s.strip()]
        selected_skills.extend(custom_list)
    
    st.markdown("---")
    
    # Generate CV Button
    if st.button("🎯 Generate Professional CV", type="primary"):
        # Better validation with specific messages
        errors = []
        
        if not full_name or full_name.strip() == "":
            errors.append("❌ Full Name is required (scroll to Step 2)")
        if not email or email.strip() == "":
            errors.append("❌ Email Address is required (scroll to Step 2)")
        if not phone or phone.strip() == "":
            errors.append("❌ Phone Number is required (scroll to Step 2)")
        if not location or location.strip() == "":
            errors.append("❌ Location is required (scroll to Step 2)")
        if not work_history:
            errors.append("❌ Please add at least one work experience (scroll to Step 3)")
        if not selected_quals:
            errors.append("❌ Please select at least one qualification (scroll to Step 4)")
        if len(selected_skills) < 5:
            errors.append(f"❌ Please select at least 5 skills (you have {len(selected_skills)} - scroll to Step 5)")
        
        if errors:
            st.error("**Please fix the following issues:**")
            for error in errors:
                st.error(error)
        else:
            with st.spinner("✨ Generating your professional CV..."):
                
                # Generate professional summary
                summary = generate_professional_summary(career_code, years_exp, selected_skills)
                
                # Create student info
                student_info = {
                    'name': full_name,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'linkedin': linkedin,
                    'summary': summary
                }
                
                # Generate CV data
                cv_data = generate_cv_data(student_info, work_history, selected_quals, selected_skills, career_code)
                
                # Generate HTML CV
                cv_html = format_cv_html(cv_data)
                
                # Generate LinkedIn profile
                linkedin_profile = generate_linkedin_profile(cv_data)
                
                st.success("✅ **Your Professional CV is Ready!**")
                
                # Display CV preview
                st.markdown("---")
                st.subheader("📄 Your CV Preview")
                
                # Show HTML preview in expandable section
                with st.expander("👁️ View CV Preview", expanded=True):
                    st.markdown(cv_html, unsafe_allow_html=True)
                
                # Download button
                st.markdown("---")
                st.subheader("📥 Download Your CV")
                
                st.download_button(
                    label="⬇️ Download CV (HTML)",
                    data=cv_html,
                    file_name=f"CV_{full_name.replace(' ', '_')}.html",
                    mime="text/html"
                )
                
                st.info("""💡 **How to convert to PDF:**
                1. Download the HTML file
                2. Open it in your web browser
                3. Press Ctrl+P (Print)
                4. Select "Save as PDF"
                5. Done! You now have a PDF CV!
                
                Or use an online converter: html-to-pdf.net""")
                
                # LinkedIn Profile
                st.markdown("---")
                st.subheader("💼 BONUS: LinkedIn Profile Optimizer")
                
                st.markdown("**Your Optimized LinkedIn Headline:**")
                st.code(linkedin_profile['headline'])
                
                st.markdown("**Your About Section:**")
                st.text_area("LinkedIn About Section (copy this!)", linkedin_profile['about'], height=300)
                
                st.markdown("**Skills to Add to LinkedIn:**")
                skills_text = ", ".join(linkedin_profile['skills_to_add'][:20])
                st.text_area("Copy these skills", skills_text, height=100)
                
                st.markdown("**LinkedIn Success Tips:**")
                for tip in linkedin_profile['tips']:
                    st.markdown(f"- ✅ {tip}")
                
                # Upgrade prompt
                st.markdown("---")
                st.success("""🎉 **Want MORE?**
                
                **PREMIUM CV PACKAGE (£39):**
                - ✅ Professional CV review by career expert
                - ✅ ATS score analysis
                - ✅ Keyword optimization
                - ✅ Multiple template designs
                - ✅ Cover letter template
                - ✅ Email application templates
                - ✅ LinkedIn profile makeover
                
                Contact T21 Services to upgrade! 📧""")


# ============================================
# TOOL 11: DASHBOARD & ANALYTICS (NEW!)
# ============================================
elif tool == "📈 Dashboard & Analytics":
    st.header("📈 Your Dashboard")
    
    user_license = st.session_state.user_license
    user_info = get_student_info(st.session_state.user_email)
    
    # Trial Countdown (if trial user)
    if hasattr(user_license, 'role') and user_license.role == "trial":
        days_remaining = user_license.days_remaining()
        hours_remaining = days_remaining * 24
        
        st.markdown("### ⏰ Trial Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if hours_remaining <= 0:
                st.error("### ❌ EXPIRED")
                st.markdown("**Your trial has ended**")
            elif hours_remaining <= 6:
                st.error(f"### ⏰ {int(hours_remaining)}h")
                st.markdown("**URGENT: Expires soon!**")
            elif hours_remaining <= 24:
                st.warning(f"### ⏰ {int(hours_remaining)}h")
                st.markdown("**Less than 1 day left**")
            else:
                st.info(f"### ⏰ {int(hours_remaining)}h")
                st.markdown(f"**{days_remaining:.1f} days remaining**")
        
        with col2:
            st.metric("Plan", "48-Hour Trial")
            st.caption("Free access to explore")
        
        with col3:
            if hours_remaining <= 6:
                st.error("### ⚠️ UPGRADE NOW!")
                if st.button("⬆️ View Upgrade Options", type="primary"):
                    st.session_state.show_upgrade = True
                    st.rerun()
            else:
                st.info("### 💡 Enjoying it?")
                st.caption("Upgrade for unlimited access")
        
        # Progress bar
        total_hours = 48
        progress = max(0, min(1, hours_remaining / total_hours))
        st.progress(progress)
        
        if hours_remaining > 0:
            st.caption(f"⏱️ Trial expires in {int(hours_remaining)} hours ({int(hours_remaining * 60)} minutes)")
        else:
            st.caption("❌ Trial expired - Please upgrade to continue")
        
        st.markdown("---")
    
    # Account Overview
    st.subheader("👤 Account Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        role = user_license.role.title() if user_license else "Admin"
        st.metric("Role", role)
    
    with col2:
        if user_license and hasattr(user_license, 'is_active'):
            status = "Active" if user_license.is_active() else "Expired"
        else:
            status = "Active"
        st.metric("Status", status)
    
    with col3:
        if user_info:
            from datetime import datetime
            created = datetime.fromisoformat(user_info['created_at'])
            days_member = (datetime.now() - created).days
            st.metric("Member", f"{days_member} days")
    
    with col4:
        if user_license and hasattr(user_license, 'usage'):
            total_logins = user_license.usage.get('total_logins', 0)
        else:
            total_logins = 0
        st.metric("Total Logins", total_logins)
    
    st.markdown("---")
    
    # Usage Today
    st.subheader("📊 Today's Activity")
    
    if user_license and hasattr(user_license, 'usage'):
        usage = user_license.usage if not callable(user_license.usage) else {}
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            validations_today = usage.get('validations_today', 0) if isinstance(usage, dict) else 0
            st.metric("Validations Today", validations_today)
        
        with col2:
            quiz_completed = usage.get('quizzes_completed_today', 0) if isinstance(usage, dict) else 0
            st.metric("Quizzes Completed", quiz_completed)
        
        with col3:
            ai_questions = usage.get('ai_questions_today', 0) if isinstance(usage, dict) else 0
            st.metric("AI Tutor Questions", ai_questions)
    else:
        st.info("Usage tracking not available for this account type")
    
    st.markdown("---")
    
    # Performance Stats
    validator_initials = st.text_input("Your Initials (to filter validation stats):", value="", max_chars=3)
    
    if validator_initials:
        stats = get_dashboard_stats(validator_initials=validator_initials.upper())
    else:
        stats = get_dashboard_stats()
    
    st.subheader("📈 Validation Performance")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Validations", stats.get('total_validations', 0))
    
    with col2:
        pass_rate = stats.get('pass_rate', 0)
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    
    with col3:
        avg_comp = stats.get('avg_compliance', 0)
        st.metric("Avg Compliance", f"{avg_comp:.1f}%")
    
    with col4:
        flag_dist = stats.get('flag_distribution', {})
        green_count = flag_dist.get('GREEN', 0)
        st.metric("Green Flags", green_count)
    
    st.markdown("---")
    
    # Flag Distribution
    st.subheader("📊 Flag Distribution")
    flag_data = stats.get('flag_distribution', {})
    if flag_data:
        df_flags = pd.DataFrame(list(flag_data.items()), columns=['Flag', 'Count'])
        st.bar_chart(df_flags.set_index('Flag'))
    else:
        st.info("No validation data yet. Start validating letters to see analytics!")
    
    # Common Gaps
    st.markdown("---")
    st.subheader("🔍 Most Common Gaps")
    common_gaps = stats.get('common_gaps', [])
    if common_gaps:
        for i, gap in enumerate(common_gaps[:10], 1):
            st.markdown(f"{i}. **{gap['gap_description']}** - {gap['count']} occurrences")
    else:
        st.info("No gaps data available yet.")


# ============================================
# TOOL 9: SMART ALERTS (NEW!)
# ============================================
elif tool == "🚨 Smart Alerts":
    st.header("🚨 Smart Alerts & Warnings")
    
    active_alerts = get_active_alerts()
    
    if active_alerts:
        st.markdown(f"### ⚠️ You have {len(active_alerts)} active alert(s)")
        
        for alert in active_alerts:
            alert_level = alert.get('alert_level', 'MEDIUM')
            
            if alert_level == 'CRITICAL':
                alert_type = "error"
            elif alert_level == 'HIGH':
                alert_type = "warning"
            else:
                alert_type = "info"
            
            with st.container():
                if alert_type == "error":
                    st.error(f"🚨 **{alert.get('alert_type')}**: {alert.get('message')}")
                elif alert_type == "warning":
                    st.warning(f"⚠️ **{alert.get('alert_type')}**: {alert.get('message')}")
                else:
                    st.info(f"ℹ️ **{alert.get('alert_type')}**: {alert.get('message')}")
                
                if st.button(f"Acknowledge Alert #{alert.get('id')}", key=f"ack_{alert.get('id')}"):
                    acknowledge_alert(alert.get('id'))
                    st.success("Alert acknowledged!")
                    st.rerun()
        
    else:
        st.success("✅ No active alerts! All systems normal.")
    
    st.markdown("---")
    st.markdown("### 📋 Alert Types")
    st.markdown("""
    - **🚨 CRITICAL**: 52-week breaches, urgent referrals not flagged
    - **⚠️ HIGH**: 26-week breaches, high gap counts (5+)
    - **ℹ️ MEDIUM**: 18-week warnings, PBL timeouts
    """)


# ============================================
# TOOL 10: VALIDATION HISTORY (NEW!)
# ============================================
elif tool == "📜 Validation History":
    st.header("📜 Validation History")
    
    validator_filter = st.text_input("Filter by validator initials:", value="", max_chars=3)
    
    if validator_filter:
        history = get_validation_history(validator_initials=validator_filter.upper(), limit=50)
    else:
        history = get_validation_history(limit=50)
    
    if history:
        st.markdown(f"### Showing last {len(history)} validations")
        
        for val in history:
            with st.expander(f"{val.get('validation_date')} - {val.get('validator_initials')} - Code {val.get('rtt_code')}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**RTT Code:** {val.get('rtt_code')}")
                    st.markdown(f"**Clock Status:** {val.get('clock_status')}")
                    st.markdown(f"**Outcome:** {val.get('outcome')}")
                
                with col2:
                    st.markdown(f"**Actions Required:** {val.get('actions_required')}")
                    st.markdown(f"**Completed:** {val.get('actions_completed')}")
                    st.markdown(f"**Gaps:** {val.get('gaps_found')}")
                    st.markdown(f"**Compliance:** {val.get('compliance_rate')}")
                
                st.markdown("**Validation Comments:**")
                st.code(val.get('validation_comments', ''))
    
    else:
        st.info("No validation history yet. Start validating letters!")


# ============================================
# MY ACCOUNT & UPGRADE
# ============================================
elif tool == "⚙️ My Account & Upgrade":
    st.header("⚙️ My Account & License Management")
    
    user_license = st.session_state.user_license
    user_info = get_student_info(st.session_state.user_email)
    
    if user_info:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Profile Information")
            st.markdown(f"**Name:** {user_info['full_name']}")
            st.markdown(f"**Email:** {user_info['email']}")
            st.markdown(f"**Member Since:** {datetime.fromisoformat(user_info['created_at']).strftime('%d/%m/%Y')}")
            st.markdown(f"**Last Login:** {user_info['last_login']}")
        
        with col2:
            st.subheader("📜 License Details")
            
            # Check if user_license exists and has the method
            if user_license and hasattr(user_license, 'get_usage_summary'):
                try:
                    usage = user_license.get_usage_summary()
                    
                    if usage["status"] == "Active":
                        st.success(f"✅ **Status:** {usage['status']}")
                    else:
                        st.error(f"❌ **Status:** {usage['status']}")
                    
                    st.markdown(f"**Plan:** {usage['role']}")
                    st.markdown(f"**Days Remaining:** {usage['days_remaining']}")
                    st.markdown(f"**Expires:** {usage['expiry_date']}")
                except Exception as e:
                    st.info("**Status:** Active")
                    st.markdown(f"**Plan:** {user_license.role if user_license else 'Unknown'}")
            else:
                st.info("**Status:** Active")
                st.markdown("**Plan:** Administrator")
            
            st.markdown(f"**License Key:** `{user_info.get('license_key', 'N/A')}`")
        
        st.markdown("---")
        
        # Usage Statistics
        st.subheader("📊 Today's Usage")
        if user_license and hasattr(user_license, 'get_usage_summary'):
            try:
                usage = user_license.get_usage_summary()
                if usage.get("usage_today"):
                    cols = st.columns(len(usage["usage_today"]))
                    for idx, (feature, limit) in enumerate(usage["usage_today"].items()):
                        with cols[idx]:
                            st.metric(feature, limit)
                else:
                    st.info("No usage data available for today")
            except:
                st.info("No usage data available for today")
        else:
            st.info("✨ Unlimited usage on your plan!")
        
        st.markdown("---")
        
        # Upgrade Options
        st.subheader("⬆️ Upgrade Your Plan")
        
        current_role = user_license.role if user_license else 'trial'
        
        # Show upgrade options (NEW 4-TIER PRICING)
        st.info("💰 **Special Offer:** Pay in full and save £50-£100!")
        
        upgrade_cols = st.columns(4)
        
        with upgrade_cols[0]:
            st.markdown("### 🆓 Taster")
            st.markdown("**£99** / 1 month")
            st.markdown("✅ AI Tutor (10 Q/day)")
            st.markdown("✅ Sample scenarios")
            st.markdown("✅ Demo tools")
            st.markdown("❌ Full platform")
            st.markdown("❌ Certification")
            
            if current_role == "trial":
                if st.button("Try Taster", key="upgrade_taster"):
                    st.info("💳 Contact admin@t21services.co.uk")
        
        with upgrade_cols[1]:
            st.markdown("### 💪 Tier 1")
            st.markdown("**£499** / 6 months")
            st.markdown("*£449 if paid in full*")
            st.markdown("✅ **Full platform access**")
            st.markdown("✅ **Unlimited AI Tutor**")
            st.markdown("✅ All clinical tools")
            st.markdown("✅ Complete scenarios")
            st.markdown("❌ Certification")
            
            if current_role in ["trial", "taster"]:
                if st.button("Upgrade to Tier 1", key="upgrade_tier1"):
                    st.info("💳 Contact admin@t21services.co.uk")
        
        with upgrade_cols[2]:
            st.markdown("### ⭐ Tier 2")
            st.markdown("**£1,299** / 12 months")
            st.markdown("*£1,199 if paid in full*")
            st.markdown("✅ Everything in Tier 1")
            st.markdown("✅ **TQUK Certification**")
            st.markdown("✅ **8-week program**")
            st.markdown("✅ Live tutor sessions")
            st.markdown("✅ Alumni network")
            
            if current_role in ["trial", "taster", "tier1"]:
                if st.button("Upgrade to Tier 2", key="upgrade_tier2"):
                    st.info("💳 Contact admin@t21services.co.uk")
        
        with upgrade_cols[3]:
            st.markdown("### 🏆 Tier 3")
            st.markdown("**£1,799** / 12 months")
            st.markdown("*£1,699 if paid in full*")
            st.markdown("✅ Everything in Tier 2")
            st.markdown("✅ **Job Placement**")
            st.markdown("✅ **3-5 interviews guaranteed**")
            st.markdown("✅ Staff applies for you")
            st.markdown("✅ Support until hired")
            
            if current_role != "tier3":
                if st.button("Upgrade to Tier 3", key="upgrade_tier3"):
                    st.info("💳 Contact admin@t21services.co.uk")
        
        st.markdown("---")
        
        # Activate License Key
        st.subheader("🔑 Activate License Key")
        st.markdown("Already purchased? Enter your license key below:")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            license_key_input = st.text_input("License Key", placeholder="XXXX-XXXX-XXXX-XXXX")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Activate"):
                if license_key_input:
                    success, message = activate_license(st.session_state.user_email, license_key_input)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter a license key")


# ============================================
# ADMIN PANEL
# ============================================
elif tool == "🔧 Admin Panel":
    # Check if user is admin
    if st.session_state.user_license:
        # Check if it's UserAccount (new system) or UserLicense (old system)
        is_admin = False
        if isinstance(st.session_state.user_license, UserAccount):
            user_type = st.session_state.user_license.role
            if "admin" in user_type or "staff" in user_type:
                is_admin = True
        else:
            # Old UserLicense system - check role
            user_role = st.session_state.user_license.role
            if user_role == "admin":
                is_admin = True
        
        if is_admin:
            st.header("🔧 Admin Panel")
            
            # Create tabs for different admin functions
            admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5, admin_tab6, admin_tab7, admin_tab8, admin_tab9, admin_tab10 = st.tabs([
                "👥 User Management", 
                "🔐 Module Access Control",
                "🎯 Modular Access",
                "📧 Bulk Email",
                "💬 Personal Message",
                "⏰ Trial Automation",
                "📚 LMS Courses",
                "🏫 School Management",
                "🤖 AI Training",
                "🗺️ User Tracking"
            ])
            
            with admin_tab1:
                try:
                    render_admin_panel(st.session_state.user_email)
                except Exception as e:
                    st.error(f"Error loading User Management: {str(e)}")
                    import traceback
                    with st.expander("🔍 Show Full Error Details"):
                        st.code(traceback.format_exc())
                    st.info("💡 If you see this error, please report it with the details above.")
            
            with admin_tab2:
                try:
                    render_module_access_admin()
                except Exception as e:
                    st.error(f"Error loading Module Access Control: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab3:
                try:
                    render_modular_access_admin()
                except Exception as e:
                    st.error(f"Error loading Modular Access: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab4:
                try:
                    render_bulk_email_ui()
                except Exception as e:
                    st.error(f"Error loading Bulk Email: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab5:
                try:
                    render_personal_message_ui()
                except Exception as e:
                    st.error(f"Error loading Personal Message: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab6:
                try:
                    render_trial_automation_ui()
                except Exception as e:
                    st.error(f"Error loading Trial Automation: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab7:
                try:
                    render_course_manager_ui()
                except Exception as e:
                    st.error(f"Error loading LMS Courses: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab8:
                try:
                    render_school_management_admin()
                except Exception as e:
                    st.error(f"Error loading School Management: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab9:
                try:
                    render_ai_training_admin()
                except Exception as e:
                    st.error(f"Error loading AI Training: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
            
            with admin_tab10:
                try:
                    render_user_tracking_dashboard()
                except Exception as e:
                    st.error(f"Error loading User Tracking: {str(e)}")
                    st.info("💡 This feature is being updated. Please try again later.")
        else:
            st.error("⛔ Access Denied - Admin or Staff privileges required")
    else:
        st.error("⛔ Access Denied - Admin or Staff privileges required")


# ============================================
# MODULE MARKETPLACE
# ============================================
elif tool == "🛒 Module Marketplace":
    render_user_marketplace(st.session_state.user_email)


# ============================================
# ACADEMIC PORTAL (STUDENT)
# ============================================
elif tool == "🎓 My Academic Portal":
    render_student_school_portal(st.session_state.user_email)


# ============================================
# LMS - MY COURSES (STUDENT VIEW)
# ============================================
elif tool == "📚 LMS - My Courses":
    user_role = st.session_state.user_license.role if hasattr(st.session_state.user_license, 'role') else "trial"
    
    # Check if viewing a specific course
    if 'viewing_course' in st.session_state:
        # Show the course player
        render_student_lms_portal(st.session_state.user_email, user_role)
    
    # Check if previewing a course
    elif 'preview_course' in st.session_state:
        # Show course preview
        render_course_preview(st.session_state.preview_course, st.session_state.user_email)
    
    # Otherwise show enhanced catalog
    else:
        # Enhanced course catalog
        render_enhanced_catalog(st.session_state.user_email, user_role)


# ============================================
# STAFF MANAGEMENT
# ============================================
elif tool == "👥 Staff Management":
    st.header("👥 Staff Management System")
    st.info("🚧 Staff Management System - Coming in next phase!")
    st.markdown("""
    **Planned Features:**
    - 👤 Staff directory
    - 📅 Shift scheduling
    - ✅ Task management
    - 📊 Performance tracking
    - ⏰ Time & attendance
    - 💬 Team communication
    
    This comprehensive staff management system will help you manage your team efficiently!
    """)


# ============================================
# PAS INTEGRATION DEMO (HANDS-ON)
# ============================================
elif tool == "🏥 PAS Integration Demo (Hands-On)":
    st.switch_page("pages/pas_integration_demo.py")


# ============================================
# CUSTOM PAS INTEGRATION (NHS TRUSTS)
# ============================================
elif tool == "🔌 Custom PAS Integration":
    st.switch_page("pages/pas_custom_integration.py")


# ============================================
# PRACTICAL TRAINING PORTAL - ALL COURSES
# ============================================
elif tool == "🎓 Practical Training Portal (All Courses)":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 40px; border-radius: 10px; margin-bottom: 30px; text-align: center;'>
        <h1 style='color: white; margin: 0;'>🎓 T21 Practical Training Portal</h1>
        <p style='color: white; margin: 10px 0 0 0; font-size: 18px;'>Access ALL Your Hands-On Training Courses</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    **🎓 Practical Training Portal** is your dedicated hands-on training environment with MULTIPLE courses and practical exercises across ALL NHS specialties.
    
    **You will need to login separately** to access the Training Portal.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📚 What's in the Training Portal?
        
        ✅ **RTT Training** - Referral to Treatment pathways & validation  
        ✅ **Hospital Administration** - Complete admin training  
        ✅ **Cancer Pathways** - 2WW & 62-day pathway management  
        ✅ **MDT Coordination** - Multi-disciplinary team training  
        ✅ **Medical Secretary** - Complete secretary skills  
        ✅ **Appointment Systems** - Booking & scheduling  
        ✅ **Data Quality** - NHS data standards & validation  
        ✅ **Clinical Coding** - Introduction to coding  
        ✅ **Patient Pathways** - End-to-end pathway management  
        ✅ **Practical Scenarios** - Real-world case studies  
        ✅ **Assessment Tools** - Test your knowledge  
        ✅ **Progress Tracking** - Monitor your learning  
        
        ### 🔐 Separate Login Required
        
        The Training Portal is a separate system with its own login:
        - If you have Training Portal access, use your portal username and password
        - If you don't have access yet, contact admin@t21services.co.uk
        
        ### 💡 How It Works
        
        1. Click "Launch Training Portal" button below
        2. New window opens to Training Portal login
        3. Login with your Training Portal credentials
        4. Access ALL your practical training courses
        5. Return here anytime for theory, AI tools, and validators
        """)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;'>
            <img src='https://via.placeholder.com/150x150/1e3a8a/ffffff?text=TRAINING+PORTAL' style='border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: #1e3a8a; margin-bottom: 10px;'>External Platform</h3>
            <p style='color: #666; margin-bottom: 20px;'>Multiple courses available</p>
            <p style='color: #666; font-size: 12px;'>RTT • Admin • Cancer • MDT<br>Secretary • Coding • More!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Launch button
    st.markdown("### 🚀 Ready to Start Training?")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    
    with col_b:
        st.markdown("""
        <div style='text-align: center; margin: 30px 0;'>
            <a href='https://t21servicestraining.co.uk/account/login' target='_blank' style='text-decoration: none;'>
                <button style='
                    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    padding: 20px 40px;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
                    width: 100%;
                '>
                    🎓 Launch Training Portal (New Window)
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("Opens in new window: https://t21servicestraining.co.uk")
    
    st.markdown("---")
    
    st.markdown("""
    ### ❓ Need Help?
    
    **Don't have Training Portal access?**  
    📧 Email: admin@t21services.co.uk  
    ☎️ Phone: +44 20 3375 2061
    
    **Forgot your Training Portal password?**  
    Use the "Forgot Password?" link on the Training Portal login page
    
    **Technical issues?**  
    Contact our support team: support@t21services.co.uk
    """)


# ============================================
# TOOL 11: ABOUT RTT RULES
# ============================================
elif tool == "ℹ️ About RTT Rules":
    st.header("NHS RTT Rules Summary")
    
    st.markdown("""
    ## 🕒 RTT Clock Fundamentals
    
    - The RTT clock **starts** when a referral for consultant-led care is received
    - It also starts when a **decision to treat** is made without a referral
    - The clock **continues** through all stages until formally stopped
    - The standard NHS target is **18 weeks**
    
    ## ⏸️ Clock Pauses
    
    - **Patient-initiated delays (PIDs)** can pause a clock
    - **Provider-initiated cancellations** do NOT pause the clock
    - Clock pauses are temporary and resume when patient is available
    
    ## 🛑 Clock Stops
    
    The RTT clock **stops** when:
    1. First definitive treatment starts (surgery, active medication, therapeutic procedure)
    2. Clinical decision made that treatment is not required
    3. Patient declines or fails to respond to reasonable offer
    4. Patient transferred to another provider
    5. Patient dies or DNA after reasonable offer
    
    ## 🧾 RTT Event Codes
    
    | Code | Description | Impact |
    |------|-------------|--------|
    | **10** | First activity in pathway | Clock start |
    | **11** | First activity after Active Monitoring/Watchful Wait ends | Clock restart |
    | **12** | First activity following Consultant/AHP referral for NEW condition | Clock start |
    | **20** | Subsequent activity | Clock continues |
    | **21** | Tertiary referral | Transfer responsibility |
    | **30** | First definitive treatment | Clock stop |
    | **31** | Active monitoring (patient-initiated) | Clock pause |
    | **32** | Active monitoring (provider-initiated) | Clock pause |
    | **33** | DNA – first care activity | Special handling |
    | **34** | Decision not to treat | Clock stop |
    | **35** | Patient declined treatment | Clock stop |
    | **36** | Patient died | Clock stop |
    | **90** | FDT occurred previously | Post-treatment (non-RTT) |
    | **91** | Activity during active monitoring | During AM only |
    | **92** | Diagnostics only | Non-RTT |
    | **98** | Not applicable to RTT | Non-RTT |
    
    ## ⏱️ Breach Thresholds
    
    - **18 weeks**: Standard RTT target
    - **26 weeks**: Serious wait breach
    - **52 weeks**: Critical breach (requires escalation)
    
    ## 📚 Policy Reference
    
    **NHS England RTT Rules and Guidance v17.0**
    
    ---
    
    ### 🎓 Training Environment
    
    This is a **simulation and training tool** for T21 Services UK.  
    **No real patient data should be entered.**
    
    Use this tool to:
    - Practice RTT pathway validation
    - Learn correct coding sequences
    - Understand breach thresholds
    - Improve data quality
    
    """)


# ============================================
# LEGAL PAGES
# ============================================
elif tool == "📄 Privacy Policy":
    st.header("🔒 Privacy Policy")
    st.markdown("**Last Updated:** October 9, 2025")
    st.markdown("**Company:** T21 Services Limited (Company No: 13091053)")
    
    st.markdown("""
    ## 1. Introduction
    
    Welcome to T21 Services Limited. We are committed to protecting your personal data and respecting your privacy.
    
    **Contact Information:**
    - **Company:** T21 Services Limited
    - **Company Number:** 13091053
    - **Address:** 64 Upper Parliament Street, Liverpool, L8 7LF, England
    - **Email:** privacy@t21services.co.uk
    - **Website:** www.t21services.co.uk
    
    ## 2. Information We Collect
    
    **Personal Information:**
    - Name, email address, password (encrypted)
    - Professional information (job title, organization)
    - Payment information (via secure third-party processors)
    
    **Usage Information:**
    - Login data (IP address, login times, device information)
    - Geolocation (approximate location for security)
    - Platform usage (pages visited, features used)
    - Training progress (scenarios completed, scores)
    
    ## 3. How We Use Your Information
    
    - Providing platform access and services
    - Processing training and generating insights
    - Security and fraud prevention
    - Platform improvement and analytics
    - Legal compliance
    
    ## 4. Legal Basis (GDPR)
    
    - **Contract Performance:** To provide services
    - **Legitimate Interests:** Platform improvement, security
    - **Consent:** Where explicitly given
    - **Legal Obligation:** UK/EU law compliance
    
    ## 5. Data Sharing
    
    **We DO NOT sell your data.**
    
    We share data with:
    - Service providers (cloud hosting, payment processors)
    - Legal authorities (when required by law)
    - NHS organizations (for organizational accounts only)
    
    ## 6. Data Security
    
    - 256-bit SSL/TLS encryption
    - Encrypted password storage (SHA-256)
    - Regular security audits
    - Real-time security monitoring
    
    ## 7. Your Rights (GDPR)
    
    You have the right to:
    - Access your data
    - Rectify inaccurate data
    - Erasure ("right to be forgotten")
    - Restrict processing
    - Data portability
    - Object to processing
    - Withdraw consent
    - Complain to ICO (UK regulator)
    
    **To exercise your rights:** privacy@t21services.co.uk
    
    ## 8. Data Retention
    
    - Active accounts: Duration of subscription + 6 months
    - Training records: Up to 7 years (NHS requirements)
    - Financial records: 7 years (UK tax law)
    
    ## 9. Contact Us
    
    **Privacy Team:**
    - Email: privacy@t21services.co.uk
    - Mail: T21 Services Limited, Privacy Team, 64 Upper Parliament Street, Liverpool, L8 7LF
    
    **UK Regulator (ICO):**
    - Website: ico.org.uk
    - Helpline: 0303 123 1113
    
    ---
    
    **T21 Services Limited** | Company No: 13091053  
    © 2020-2025 T21 Services Limited. All rights reserved.
    """)

elif tool == "📜 Terms of Service":
    st.header("📄 Terms of Service")
    st.markdown("**Effective Date:** October 9, 2025")
    st.markdown("**Company:** T21 Services Limited (Company No: 13091053)")
    
    st.markdown("""
    ## 1. Agreement to Terms
    
    By using the T21 Healthcare Intelligence Platform, you agree to these Terms of Service.
    
    **IF YOU DO NOT AGREE, DO NOT USE THE PLATFORM.**
    
    **Platform Provider:**
    - **Company:** T21 Services Limited
    - **Company Number:** 13091053
    - **Address:** 64 Upper Parliament Street, Liverpool, L8 7LF, England
    - **Website:** www.t21services.co.uk
    
    ## 2. Eligibility
    
    - Must be 18+ years old
    - Designed for healthcare professionals, students, NHS organizations
    - Provide accurate information during registration
    
    ## 3. User Accounts
    
    **Account Types:**
    - **Free Trial:** 48-hour trial (limited features)
    - **Paid Subscriptions:** Basic (£299/3mo), Professional (£599/6mo), Premium (£999/12mo)
    - **NHS Organizations:** Custom pricing
    
    **Account Security:**
    - Keep password confidential
    - Responsible for all account activity
    - Notify us of unauthorized access
    
    ## 4. Subscription & Payment
    
    - All fees in GBP (£), excluding VAT
    - Payment via secure third-party processors
    - Non-refundable after 7-day cooling-off period
    - Auto-renewal unless cancelled 7 days before expiry
    
    ## 5. Permitted Use
    
    **You MAY:**
    - Complete training scenarios
    - Access NHS administration tools
    - Generate reports and analytics
    
    **You may NOT:**
    - Share account credentials
    - Use automated tools (bots, scrapers)
    - Reverse engineer the platform
    - Copy or distribute content
    - Use for illegal purposes
    - Bypass security measures
    
    ## 6. Intellectual Property
    
    **We own:**
    - Platform software and code
    - Training scenarios and content
    - AI models and algorithms
    - Trademarks and branding
    
    **You own:**
    - Data you upload (we license to process it)
    
    ## 7. Training & Certification
    
    - Training is for educational purposes only
    - Certifications confirm completion of modules
    - NOT official NHS qualifications
    - Supplement with workplace experience
    
    ## 8. Data Protection
    
    See our Privacy Policy for details on data handling.
    
    ## 9. Service Availability
    
    - We strive for 99.5% uptime (no guarantee)
    - Scheduled maintenance with advance notice
    - Not liable for interruptions beyond our control
    
    ## 10. Limitation of Liability
    
    **Platform provided "AS IS" without warranties.**
    
    **Liability limited to:**
    - Students: Amount paid in last 12 months
    - NHS Organizations: As per contract
    
    **NOT liable for:**
    - Indirect, consequential damages
    - Loss of profits, data, goodwill
    - Clinical decisions made using platform data
    
    ## 11. Termination
    
    **By You:** Cancel subscription anytime
    
    **By Us:** Immediate termination if you:
    - Breach these Terms
    - Engage in fraudulent activity
    - Pose security risk
    
    ## 12. Governing Law
    
    These Terms governed by laws of England and Wales.
    
    ## 13. Contact
    
    **General:** info@t21services.co.uk  
    **Legal:** legal@t21services.co.uk  
    **Support:** support@t21services.co.uk
    
    ---
    
    **T21 Services Limited** | Company No: 13091053  
    © 2020-2025 T21 Services Limited. All rights reserved.
    """)

elif tool == "📧 Contact Us":
    st.header("📧 Contact Us")
    st.markdown("We'd love to hear from you!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💬 Send Us a Message")
        
        with st.form("contact_form_main"):
            contact_type = st.selectbox(
                "I am contacting as:",
                [
                    "NHS Organization (Book Demo)",
                    "Student (Training Inquiry)",
                    "Training Provider (Partnership)",
                    "Existing Customer (Support)",
                    "General Inquiry"
                ]
            )
            
            full_name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            organization = st.text_input("Organization (optional)")
            subject = st.text_input("Subject *")
            message = st.text_area("Message *", height=150)
            
            privacy_consent = st.checkbox("I agree to the Privacy Policy *")
            
            submitted = st.form_submit_button("📨 Send Message", type="primary")
            
            if submitted:
                if not full_name or not email or not subject or not message:
                    st.error("❌ Please fill in all required fields (*)")
                elif not privacy_consent:
                    st.error("❌ You must agree to the Privacy Policy")
                elif "@" not in email:
                    st.error("❌ Please enter a valid email address")
                else:
                    import json
                    import os
                    from datetime import datetime
                    
                    # Save submission
                    try:
                        os.makedirs("data/contact_submissions", exist_ok=True)
                        
                        submission = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "contact_type": contact_type,
                            "full_name": full_name,
                            "email": email,
                            "organization": organization,
                            "subject": subject,
                            "message": message,
                            "privacy_consent": privacy_consent
                        }
                        
                        filename = f"data/contact_submissions/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{email.replace('@', '_at_')}.json"
                        with open(filename, 'w') as f:
                            json.dump(submission, f, indent=2)
                        
                        st.success("✅ Message Sent Successfully!")
                        st.balloons()
                        st.info(f"Thank you, {full_name}! We'll respond within 24 hours (Mon-Fri).")
                        
                    except Exception as e:
                        st.error(f"Error submitting form. Please email us directly at info@t21services.co.uk")
    
    with col2:
        st.markdown("### 📍 Contact Information")
        
        st.markdown("""
        **🏢 T21 Services Limited**  
        Company No: 13091053  
        Status: Active ✅
        
        **📍 Head Office**  
        64 Upper Parliament Street  
        Liverpool, L8 7LF  
        England, United Kingdom 🇬🇧
        
        **📧 Email Us**  
        General: info@t21services.co.uk  
        Support: support@t21services.co.uk  
        Sales: sales@t21services.co.uk
        
        **🌐 Website**  
        www.t21services.co.uk
        
        **🔗 Social Media**  
        💼 [LinkedIn](https://linkedin.com/company/t21services)  
        🐦 [X (Twitter)](https://x.com/t21services)  
        📘 [Facebook](https://facebook.com/t21services)  
        📸 [Instagram](https://instagram.com/t21services)  
        🎵 [TikTok](https://tiktok.com/@t21services)
        
        **🕐 Office Hours**  
        Monday - Friday: 9:00 AM - 5:00 PM GMT  
        Saturday - Sunday: Closed  
        *24/7 platform support available*
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <strong>T21 RTT Pathway Intelligence v1.2</strong><br>
    T21 Services UK | NHS Training & Simulation Environment<br>
    <em>No real patient data | For training purposes only</em>
</div>
""", unsafe_allow_html=True)
