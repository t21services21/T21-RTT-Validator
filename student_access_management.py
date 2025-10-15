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
# NHS WORKFLOW MODULES LIST
# ============================================

NHS_MODULES = [
    "Patient Registration",
    "Pathway Management",
    "Episode Management",
    "RTT Clock Management",
    "Waiting List Management",
    "DNA & Cancellation Tracking",
    "Data Quality Alerts",
    "Appointment Booking",
    "PTL - Patient Tracking List",
    "Cancer Pathways",
    "MDT Coordination",
    "Task Management"
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name*", placeholder="e.g., John Smith")
        email = st.text_input("Email*", placeholder="e.g., john.smith@example.com")
        password = st.text_input("Temporary Password*", type="password", placeholder="Student will change this")
    
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
    
    if st.button("➕ Add Student", type="primary"):
        if not full_name or not email or not password:
            st.error("Please fill in all required fields")
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
            
            st.balloons()
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
    
    st.markdown("### 👥 All Students")
    
    students = get_all_students()
    
    if not students:
        st.info("No students added yet.")
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
                    st.session_state['manage_access_student'] = student.get('email')
                    st.rerun()
            
            with col2:
                if st.button(f"📊 View Progress", key=f"progress_{student.get('email')}"):
                    st.info("Progress tracking coming soon!")
            
            with col3:
                if st.button(f"✏️ Edit", key=f"edit_{student.get('email')}"):
                    st.info("Edit functionality coming soon!")


def render_manage_access():
    """Manage student access to modules"""
    
    st.markdown("### 🔐 Manage Module Access")
    
    students = get_all_students()
    
    if not students:
        st.info("No students added yet.")
        return
    
    # Select student
    student_options = {f"{s.get('full_name')} ({s.get('email')})": s for s in students}
    selected = st.selectbox("Select Student:", ["-- Select Student --"] + list(student_options.keys()))
    
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
