"""
STUDENT ACCESS MANAGEMENT SYSTEM
Add students, manage access to materials, quizzes, and NHS modules

Features:
- Add/Remove students
- Grant module access (NHS workflows)
- Grant material access
- Grant quiz access
- Bulk access management
- Student directory
- Access reports
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List
from supabase_database import supabase, create_user, get_all_users, grant_module_access, get_user_modules
import hashlib


# ============================================
# EMAIL NOTIFICATION SYSTEM (Using existing SendGrid service!)
# ============================================

def send_student_welcome_email(student_email: str, student_name: str, temp_password: str) -> Dict:
    """
    Send welcome email to new student with login details
    Uses the existing email_service.py with SendGrid integration
    """
    
    try:
        # Import existing email service
        from email_service import send_email
        
        subject = "🎉 Welcome to T21 Healthcare Platform - Student Account Created!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
                <h1 style="color: #0066cc;">Welcome to T21 Healthcare Platform! 🎉</h1>
                
                <p>Dear {student_name},</p>
                
                <p>Your student account has been successfully created! Welcome to the T21 Healthcare Intelligence Platform.</p>
                
                <div style="background-color: #f0f8ff; padding: 20px; border-left: 4px solid #0066cc; margin: 20px 0;">
                    <h3 style="margin-top: 0;">🔐 Your Login Details:</h3>
                    <p><strong>Email:</strong> {student_email}<br>
                    <strong>Temporary Password:</strong> <code style="background: #f5f5f5; padding: 2px 6px; border-radius: 3px;">{temp_password}</code></p>
                </div>
                
                <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                    <p><strong>🔒 IMPORTANT SECURITY STEPS:</strong></p>
                    <ol>
                        <li>Login with the credentials above</li>
                        <li>Go to "My Account" in the sidebar</li>
                        <li><strong>Change your password immediately</strong></li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background-color: #0066cc; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                        LOGIN NOW →
                    </a>
                </div>
                
                <p><strong>📚 What's Available to You:</strong></p>
                <ul>
                    <li>✅ Learning Portal (Materials, Videos, Quizzes)</li>
                    <li>✅ NHS Workflow Training</li>
                    <li>✅ RTT Pathway Management</li>
                    <li>✅ Interactive Learning Tools</li>
                    <li>✅ Student Portfolio System</li>
                    <li>✅ Career Development Resources</li>
                </ul>
                
                <p><strong>💡 Getting Started:</strong></p>
                <ol>
                    <li>Login to the platform</li>
                    <li>Change your password</li>
                    <li>Complete your profile</li>
                    <li>Explore the Learning Portal</li>
                    <li>Start with Week 1 materials</li>
                </ol>
                
                <p>Need help? Contact your instructor or email support@t21services.com</p>
                
                <p>Best regards,<br>
                <strong>T21 Services Team</strong><br>
                Your Healthcare Training Experts</p>
                
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    © 2025 T21 Services. All rights reserved.<br>
                    64 Upper Parliament Street, Liverpool, L8 7LF, United Kingdom
                </p>
            </div>
        </body>
        </html>
        """
        
        # Send using existing SendGrid service
        success = send_email(student_email, subject, html_content)
        
        if success:
            return {
                'success': True,
                'message': f'Welcome email sent to {student_email}'
            }
        else:
            return {
                'success': False,
                'error': 'Email sending failed. Please check SendGrid configuration.'
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Email error: {str(e)}'
        }


# ============================================
# NHS WORKFLOW MODULES LIST
# ============================================

# Updated module list matching current sidebar structure
NHS_MODULES = [
    # Core Hubs
    "🏥 Patient Administration Hub",
    "🎓 Learning Portal",
    "👨‍🏫 Teaching & Assessment",
    
    # Clinical & Workflow
    "🏥 Clinical Workflows",
    "📋 PTL - Patient Tracking List",
    "🎗️ Cancer Pathways",
    "👥 MDT Coordination",
    "📅 Advanced Booking System",
    "✅ Task Management",
    
    # Patient Management (individual modules)
    "Patient Registration",
    "Pathway Management",
    "Episode Management",
    "RTT Clock Management",
    "Waiting List Management",
    "DNA & Cancellation Tracking",
    "Data Quality Alerts",
    "Appointment Booking",
    
    # AI & Tools
    "🤖 AI & Automation",
    "🤖 AI Auto-Validator",
    "📧 Medical Secretary AI",
    "📄 Clinical Letters",
    
    # Reports & Analytics
    "📊 Reports & Analytics",
    "📊 Executive Dashboard",
    "📊 Interactive Reports",
    "📊 Data Quality",
    "📊 Data Quality System",
    
    # Training & Career
    "🎓 Training & Certification",
    "🎓 Training Library",
    "🎮 Interactive Learning Center",
    "🤖 AI RTT Tutor",
    "🎓 Certification Exam",
    "💼 Career Development",
    "💼 Job Interview Prep",
    "📄 CV Builder",
    
    # Admin
    "⚙️ Administration",
    "⚙️ My Account & Upgrade",
    "🔧 Admin Panel"
]

LEARNING_MODULES = [
    "Learning Materials",
    "Video Library",
    "Announcements",
    "Assignments",
    "Quizzes",
    "Student Portfolio"
]


# ============================================
# STUDENT MANAGEMENT FUNCTIONS
# ============================================

def add_student(
    email: str,
    full_name: str,
    password: str,
    role: str = "student_basic",
    user_type: str = "student"
) -> Dict:
    """Add a new student"""
    
    try:
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user
        success, message = create_user(email, password_hash, full_name, role, user_type)
        
        if success:
            return {
                'success': True,
                'message': f'Student {full_name} added successfully!',
                'email': email
            }
        else:
            return {'success': False, 'error': message}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_all_students() -> List[Dict]:
    """Get all students"""
    
    try:
        all_users = get_all_users()
        # Filter for students only
        students = [u for u in all_users if u.get('user_type') == 'student']
        return students
    
    except Exception as e:
        st.error(f"Error getting students: {e}")
        return []


def grant_access_to_student(student_email: str, module_name: str, granted_by: str) -> Dict:
    """Grant module access to student"""
    
    try:
        success, message = grant_module_access(student_email, module_name, granted_by)
        
        if success:
            return {'success': True, 'message': f'Access to {module_name} granted'}
        else:
            return {'success': False, 'error': message}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_student_access(student_email: str) -> List[str]:
    """Get all modules student has access to"""
    
    try:
        modules = get_user_modules(student_email)
        return modules
    
    except Exception as e:
        st.error(f"Error getting student access: {e}")
        return []


def grant_bulk_access(student_emails: List[str], module_names: List[str], granted_by: str) -> Dict:
    """Grant multiple modules to multiple students"""
    
    try:
        successful = 0
        failed = 0
        
        for email in student_emails:
            for module in module_names:
                result = grant_access_to_student(email, module, granted_by)
                if result.get('success'):
                    successful += 1
                else:
                    failed += 1
        
        return {
            'success': True,
            'successful': successful,
            'failed': failed,
            'message': f'Granted {successful} access permissions'
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def grant_all_access(student_email: str, granted_by: str) -> Dict:
    """Grant access to ALL modules"""
    
    try:
        all_modules = NHS_MODULES + LEARNING_MODULES
        
        successful = 0
        for module in all_modules:
            result = grant_access_to_student(student_email, module, granted_by)
            if result.get('success'):
                successful += 1
        
        return {
            'success': True,
            'message': f'Granted full access to {successful} modules'
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ============================================
# UI FUNCTIONS
# ============================================

def render_student_access_management():
    """Main UI for student access management"""
    
    st.subheader("👥 Student Access Management")
    
    st.info("""
    **Manage Students & Access:**
    - Add new students
    - Grant access to NHS workflow modules
    - Grant access to learning materials
    - Control what students can practice
    - Bulk access management
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add Student",
        "👥 All Students",
        "🔐 Manage Access",
        "📊 Access Report",
        "⚙️ Bulk Operations"
    ])
    
    with tab1:
        render_add_student()
    
    with tab2:
        render_all_students()
    
    with tab3:
        render_manage_access()
    
    with tab4:
        render_access_report()
    
    with tab5:
        render_bulk_operations()


def render_add_student():
    """Add new student"""
    
    st.markdown("### ➕ Add New Student")
    
    # Auto-generate password option
    st.info("🔐 **Password will be auto-generated** and sent to student via email")
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name*", placeholder="e.g., John Smith")
        email = st.text_input("Email*", placeholder="e.g., john.smith@example.com")
        
        # Option to manually set password or auto-generate
        password_option = st.radio(
            "Password Setup:",
            ["🔄 Auto-Generate (Recommended)", "🔧 Set Manually"],
            key="password_option",
            horizontal=True
        )
        
        if password_option == "🔧 Set Manually":
            password = st.text_input("Temporary Password*", type="password", placeholder="Student will change this")
            show_password = st.checkbox("Show password", key="show_temp_pass")
            if show_password and password:
                st.code(password)
        else:
            # Auto-generate secure password
            import secrets
            import string
            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
            st.success(f"✅ Password will be auto-generated: `{password}`")
    
    with col2:
        role = st.selectbox("Account Type", [
            "student_basic",
            "student_professional",
            "student_ultimate",
            "teacher",
            "admin"
        ], help="""
        - Basic: 90 days access
        - Professional: 180 days access
        - Ultimate: 365 days access
        - Teacher: Full access for assessors
        - Admin: Full system access
        """)
        
        grant_all = st.checkbox("Grant access to ALL modules", value=True, help="Recommended for most students")
        send_email = st.checkbox("📧 Send welcome email with login details", value=True, help="Highly recommended!")
    
    if st.button("➕ Add Student", type="primary"):
        if not full_name or not email:
            st.error("Please fill in all required fields")
            return
        
        if password_option == "🔧 Set Manually" and not password:
            st.error("Please enter a password")
            return
        
        # Add student
        result = add_student(email, full_name, password, role)
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            
            # Grant access if requested
            if grant_all:
                admin_email = st.session_state.get('user_email', 'admin@example.com')
                access_result = grant_all_access(email, admin_email)
                
                if access_result.get('success'):
                    st.success(f"✅ {access_result.get('message')}")
                else:
                    st.warning(f"Student added but access grant failed: {access_result.get('error')}")
            
            # Send welcome email if requested
            if send_email:
                email_result = send_student_welcome_email(email, full_name, password)
                if email_result.get('success'):
                    st.success(f"📧 Welcome email sent to {email}")
                else:
                    st.warning(f"⚠️ Student added but email not sent: {email_result.get('error')}")
                    st.info(f"""
                    **Please manually share these login details:**
                    - Email: {email}
                    - Password: {password}
                    - Login URL: https://t21-healthcare-platform.streamlit.app
                    """)
            
            st.balloons()
            
            # Show login details
            with st.expander("📋 Student Login Details", expanded=not send_email):
                st.info(f"""
                **Student Login Details:**
                - Email: {email}
                - Password: {password}
            - They can change password after first login
            """)
            
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_all_students():
    """View all students"""
    
    st.markdown("### 👥 All Students Overview")
    
    # Check if editing a student
    if 'edit_student_email' in st.session_state:
        render_edit_student_form()
        return
    
    students = get_all_students()
    
    if not students:
        st.info("No students found. Add your first student!")
        return
    
    st.write(f"**Total Students: {len(students)}**")
    
    # Search/filter
    search = st.text_input("🔍 Search students", placeholder="Search by name or email...")
    
    if search:
        students = [s for s in students if search.lower() in s.get('full_name', '').lower() or search.lower() in s.get('email', '').lower()]
    
    # Display students
    for student in students:
        with st.expander(f"👤 {student.get('full_name')} - {student.get('email')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {student.get('full_name')}")
                st.write(f"**Email:** {student.get('email')}")
                st.write(f"**Role:** {student.get('role')}")
                st.write(f"**Status:** {student.get('status')}")
            
            with col2:
                created_at = student.get('created_at', '')
                st.write(f"**Created:** {created_at[:10] if created_at else 'N/A'}")
                
                last_login = student.get('last_login')
                if last_login:
                    st.write(f"**Last Login:** {last_login[:10]}")
                else:
                    st.write(f"**Last Login:** Never")
                
                expiry_date = student.get('expiry_date', '')
                st.write(f"**Expires:** {expiry_date[:10] if expiry_date else 'N/A'}")
            
            # Show access
            access_modules = get_student_access(student.get('email'))
            
            if access_modules:
                st.markdown("**Has Access To:**")
                st.write(", ".join(access_modules))
            else:
                st.warning("⚠️ No module access granted yet")
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"🔐 Manage Access", key=f"access_{student.get('email')}"):
                    # Toggle access management display
                    if st.session_state.get(f'show_access_{student.get("email")}'):
                        st.session_state[f'show_access_{student.get("email")}'] = False
                    else:
                        st.session_state[f'show_access_{student.get("email")}'] = True
                    st.rerun()
            
            # Show access management if toggled
            if st.session_state.get(f'show_access_{student.get("email")}'):
                st.markdown("---")
                st.markdown("### 🔐 Grant Module Access")
                
                col_a, col_b = st.columns([2, 1])
                
                with col_a:
                    if st.button("✅ Grant ALL Module Access", key=f"grant_all_inline_{student.get('email')}", type="primary"):
                        admin_email = st.session_state.get('user_email', 'admin@example.com')
                        result = grant_all_access(student.get('email'), admin_email)
                        if result.get('success'):
                            st.success(f"✅ {result.get('message')}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('error')}")
                
                with col_b:
                    if st.button("❌ Close", key=f"close_access_{student.get('email')}"):
                        st.session_state[f'show_access_{student.get("email")}'] = False
                        st.rerun()
                
                st.markdown("**Or select individual modules:**")
                
                # Module selection
                col_nhs, col_learning = st.columns(2)
                
                with col_nhs:
                    st.markdown("**NHS Workflow Modules:**")
                    nhs_selected = st.multiselect(
                        "NHS Modules",
                        NHS_MODULES,
                        key=f"nhs_modules_{student.get('email')}",
                        label_visibility="collapsed"
                    )
                
                with col_learning:
                    st.markdown("**Learning Portal Modules:**")
                    learning_selected = st.multiselect(
                        "Learning Modules",
                        LEARNING_MODULES,
                        key=f"learning_modules_{student.get('email')}",
                        label_visibility="collapsed"
                    )
                
                if st.button("💾 Grant Selected Modules", key=f"grant_selected_inline_{student.get('email')}"):
                    selected_modules = nhs_selected + learning_selected
                    if selected_modules:
                        admin_email = st.session_state.get('user_email', 'admin@example.com')
                        success_count = 0
                        for module in selected_modules:
                            result = grant_module_access(student.get('email'), module, admin_email)
                            if result.get('success'):
                                success_count += 1
                        st.success(f"✅ Granted access to {success_count} modules!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.warning("⚠️ Please select at least one module")
                
                st.markdown("---")
            
            with col2:
                if st.button(f"📊 View Progress", key=f"progress_{student.get('email')}"):
                    # Show student progress
                    st.markdown("### 📊 Student Progress")
                    
                    # Get materials downloaded
                    try:
                        materials_result = supabase.table('material_downloads').select('*').eq('student_email', student.get('email')).execute()
                        materials_count = len(materials_result.data) if materials_result.data else 0
                    except:
                        materials_count = 0
                    
                    # Get videos watched
                    try:
                        videos_result = supabase.table('video_views').select('*').eq('student_email', student.get('email')).execute()
                        videos_count = len(videos_result.data) if videos_result.data else 0
                    except:
                        videos_count = 0
                    
                    # Get quizzes completed
                    try:
                        quizzes_result = supabase.table('quiz_attempts').select('*').eq('student_email', student.get('email')).execute()
                        quizzes_count = len(quizzes_result.data) if quizzes_result.data else 0
                    except:
                        quizzes_count = 0
                    
                    # Display progress
                    pcol1, pcol2, pcol3 = st.columns(3)
                    with pcol1:
                        st.metric("📄 Materials Downloaded", materials_count)
                    with pcol2:
                        st.metric("🎥 Videos Watched", videos_count)
                    with pcol3:
                        st.metric("✅ Quizzes Completed", quizzes_count)
                    
                    # Show access
                    st.markdown("**Module Access:**")
                    if access_modules:
                        st.success(f"Has access to {len(access_modules)} modules")
                    else:
                        st.warning("No module access granted yet")
            
            with col3:
                if st.button(f"✏️ Edit", key=f"edit_{student.get('email')}"):
                    # Set student to edit in session state
                    st.session_state['edit_student_email'] = student.get('email')
                    st.rerun()


def render_edit_student_form():
    """Render form to edit student details"""
    
    student_email = st.session_state.get('edit_student_email')
    
    # Get student details
    try:
        result = supabase.table('users').select('*').eq('email', student_email).execute()
        if not result.data:
            st.error("Student not found")
            if st.button("← Back to Students"):
                del st.session_state['edit_student_email']
                st.rerun()
            return
        
        student = result.data[0]
    except Exception as e:
        st.error(f"Error loading student: {e}")
        if st.button("← Back to Students"):
            del st.session_state['edit_student_email']
            st.rerun()
        return
    
    st.markdown(f"### ✏️ Edit Student: {student.get('full_name')}")
    
    if st.button("← Back to All Students"):
        del st.session_state['edit_student_email']
        st.rerun()
    
    st.markdown("---")
    
    with st.form("edit_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Full Name*", value=student.get('full_name', ''))
            new_role = st.selectbox("Account Type", [
                "student_basic",
                "student_professional",
                "student_ultimate",
                "teacher",
                "admin"
            ], index=["student_basic", "student_professional", "student_ultimate", "teacher", "admin"].index(student.get('role', 'student_basic')))
        
        with col2:
            new_status = st.selectbox("Status", ["active", "suspended", "expired"], 
                                     index=["active", "suspended", "expired"].index(student.get('status', 'active')))
            
            reset_password = st.checkbox("🔐 Reset Password", help="Generate new password and send to student")
        
        send_email_check = False
        new_password = ""
        
        if reset_password:
            import secrets
            import string
            new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
            st.info(f"✅ New password will be: `{new_password}`")
            send_email_check = st.checkbox("📧 Send password reset email to student", value=True)
        
        submitted = st.form_submit_button("💾 Save Changes", type="primary")
        
        if submitted:
            try:
                # Update student in database
                update_data = {
                    'full_name': new_name,
                    'role': new_role,
                    'status': new_status
                }
                
                if reset_password and new_password:
                    import hashlib
                    update_data['password'] = hashlib.sha256(new_password.encode()).hexdigest()
                
                supabase.table('users').update(update_data).eq('email', student_email).execute()
                st.success("✅ Student updated successfully!")
                
                # Send password reset email if requested
                if reset_password and new_password and send_email_check:
                    email_result = send_student_welcome_email(student_email, new_name, new_password)
                    if email_result.get('success'):
                        st.success(f"📧 Password reset email sent to {student_email}!")
                    else:
                        st.warning(f"⚠️ Student updated but email not sent: {email_result.get('error')}")
                        st.info(f"""
                        **Please manually share new password:**
                        - Email: {student_email}
                        - Password: {new_password}
                        """)
                elif reset_password and new_password:
                    st.info(f"""
                    **Student updated! Share new password:**
                    - Email: {student_email}
                    - Password: {new_password}
                    """)
                
                # Clear edit state
                del st.session_state['edit_student_email']
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error updating student: {e}")


def render_manage_access():
    """Manage student access to modules"""
    
    st.markdown("### 🔐 Manage Module Access")
    
    students = get_all_students()
    
    if not students:
        st.info("No students added yet.")
        return
    
    # Check if coming from student list
    preselected_email = st.session_state.get('manage_access_student')
    
    # Select student
    student_options = {f"{s.get('full_name')} ({s.get('email')})": s for s in students}
    
    # Find default index if preselected
    default_index = 0
    if preselected_email:
        for idx, (key, stud) in enumerate(student_options.items(), 1):
            if stud.get('email') == preselected_email:
                default_index = idx
                break
        # Clear the session state
        if 'manage_access_student' in st.session_state:
            del st.session_state['manage_access_student']
    
    selected = st.selectbox("Select Student:", 
                           ["-- Select Student --"] + list(student_options.keys()),
                           index=default_index)
    
    if selected == "-- Select Student --":
        return
    
    student = student_options[selected]
    student_email = student.get('email')
    
    st.markdown(f"**Managing access for: {student.get('full_name')}**")
    
    # Get current access
    current_access = get_student_access(student_email)
    
    # Display current access
    st.markdown("#### Current Access")
    if current_access:
        st.success(f"✅ Has access to {len(current_access)} modules")
        with st.expander("View current access"):
            for module in current_access:
                st.write(f"✓ {module}")
    else:
        st.warning("⚠️ No access granted yet")
    
    st.markdown("---")
    
    # Grant new access
    st.markdown("#### Grant New Access")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**NHS Workflow Modules:**")
        nhs_selected = []
        for module in NHS_MODULES:
            has_access = module in current_access
            if st.checkbox(module, value=has_access, key=f"nhs_{module}_{student_email}"):
                if not has_access:
                    nhs_selected.append(module)
    
    with col2:
        st.markdown("**Learning Modules:**")
        learning_selected = []
        for module in LEARNING_MODULES:
            has_access = module in current_access
            if st.checkbox(module, value=has_access, key=f"learning_{module}_{student_email}"):
                if not has_access:
                    learning_selected.append(module)
    
    # Quick actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Grant All NHS Modules"):
            admin_email = st.session_state.get('user_email', 'admin@example.com')
            for module in NHS_MODULES:
                if module not in current_access:
                    grant_access_to_student(student_email, module, admin_email)
            st.success("✅ Granted access to all NHS modules!")
            st.rerun()
    
    with col2:
        if st.button("✅ Grant All Learning Modules"):
            admin_email = st.session_state.get('user_email', 'admin@example.com')
            for module in LEARNING_MODULES:
                if module not in current_access:
                    grant_access_to_student(student_email, module, admin_email)
            st.success("✅ Granted access to all learning modules!")
            st.rerun()
    
    with col3:
        if st.button("✅ Grant ALL Access"):
            admin_email = st.session_state.get('user_email', 'admin@example.com')
            result = grant_all_access(student_email, admin_email)
            if result.get('success'):
                st.success(f"✅ {result.get('message')}")
                st.rerun()
    
    # Apply selected access
    st.markdown("---")
    
    all_selected = nhs_selected + learning_selected
    
    if all_selected:
        st.info(f"📌 {len(all_selected)} new modules selected")
        
        if st.button(f"🔐 Grant Access to Selected Modules", type="primary"):
            admin_email = st.session_state.get('user_email', 'admin@example.com')
            
            successful = 0
            for module in all_selected:
                result = grant_access_to_student(student_email, module, admin_email)
                if result.get('success'):
                    successful += 1
            
            st.success(f"✅ Granted access to {successful} modules!")
            st.balloons()
            st.rerun()


def render_access_report():
    """Show access report for all students"""
    
    st.markdown("### 📊 Access Report")
    
    students = get_all_students()
    
    if not students:
        st.info("No students added yet.")
        return
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Students", len(students))
    
    with col2:
        with_access = sum(1 for s in students if len(get_student_access(s.get('email'))) > 0)
        st.metric("With Access", with_access)
    
    with col3:
        without_access = len(students) - with_access
        st.metric("No Access", without_access)
    
    st.markdown("---")
    
    # Detailed report
    st.markdown("### Student Access Details")
    
    for student in students:
        student_email = student.get('email')
        access_modules = get_student_access(student_email)
        
        access_count = len(access_modules)
        total_modules = len(NHS_MODULES) + len(LEARNING_MODULES)
        percentage = (access_count / total_modules * 100) if total_modules > 0 else 0
        
        with st.expander(f"👤 {student.get('full_name')} - {access_count}/{total_modules} modules ({percentage:.0f}%)"):
            st.progress(percentage / 100)
            
            if access_modules:
                col1, col2 = st.columns(2)
                
                with col1:
                    nhs_access = [m for m in access_modules if m in NHS_MODULES]
                    if nhs_access:
                        st.markdown("**NHS Modules:**")
                        for module in nhs_access:
                            st.write(f"✓ {module}")
                
                with col2:
                    learning_access = [m for m in access_modules if m in LEARNING_MODULES]
                    if learning_access:
                        st.markdown("**Learning Modules:**")
                        for module in learning_access:
                            st.write(f"✓ {module}")
            else:
                st.warning("⚠️ No access granted")


def render_bulk_operations():
    """Bulk operations for multiple students"""
    
    st.markdown("### ⚙️ Bulk Operations")
    
    students = get_all_students()
    
    if not students:
        st.info("No students added yet.")
        return
    
    st.info("Select multiple students and grant access to multiple modules at once")
    
    # Select students
    st.markdown("#### Select Students")
    
    student_selections = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        select_all = st.checkbox("Select All Students")
    
    with col2:
        if select_all:
            st.info(f"All {len(students)} students selected")
    
    if not select_all:
        for student in students:
            student_selections[student.get('email')] = st.checkbox(
                f"{student.get('full_name')} ({student.get('email')})",
                key=f"bulk_select_{student.get('email')}"
            )
    else:
        student_selections = {s.get('email'): True for s in students}
    
    selected_emails = [email for email, selected in student_selections.items() if selected]
    
    if not selected_emails:
        st.warning("No students selected")
        return
    
    st.success(f"✅ {len(selected_emails)} students selected")
    
    st.markdown("---")
    
    # Select modules
    st.markdown("#### Select Modules to Grant")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**NHS Modules:**")
        nhs_bulk = []
        for module in NHS_MODULES:
            if st.checkbox(module, key=f"bulk_nhs_{module}"):
                nhs_bulk.append(module)
    
    with col2:
        st.markdown("**Learning Modules:**")
        learning_bulk = []
        for module in LEARNING_MODULES:
            if st.checkbox(module, key=f"bulk_learning_{module}"):
                learning_bulk.append(module)
    
    all_bulk_modules = nhs_bulk + learning_bulk
    
    if not all_bulk_modules:
        st.warning("No modules selected")
        return
    
    st.info(f"📌 Will grant access to {len(all_bulk_modules)} modules for {len(selected_emails)} students")
    
    # Bulk actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Grant All NHS Modules to Selected", type="primary"):
            admin_email = st.session_state.get('user_email', 'admin@example.com')
            result = grant_bulk_access(selected_emails, NHS_MODULES, admin_email)
            
            if result.get('success'):
                st.success(f"✅ {result.get('message')}")
                st.balloons()
                st.rerun()
    
    with col2:
        if st.button("✅ Grant ALL Modules to Selected", type="primary"):
            admin_email = st.session_state.get('user_email', 'admin@example.com')
            all_modules = NHS_MODULES + LEARNING_MODULES
            result = grant_bulk_access(selected_emails, all_modules, admin_email)
            
            if result.get('success'):
                st.success(f"✅ {result.get('message')}")
                st.balloons()
                st.rerun()
    
    st.markdown("---")
    
    # Apply selected
    if st.button(f"🔐 Grant Selected Modules to Selected Students", type="primary"):
        admin_email = st.session_state.get('user_email', 'admin@example.com')
        result = grant_bulk_access(selected_emails, all_bulk_modules, admin_email)
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            st.info(f"Details: {result.get('successful')} successful, {result.get('failed')} failed")
            st.balloons()
            st.rerun()
