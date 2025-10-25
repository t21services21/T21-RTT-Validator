"""
SIMPLE COURSE & MODULE ASSIGNMENT
One page to assign everything to students

Flow:
1. Select student
2. Tick what they need
3. Click assign
4. Done!
"""

import streamlit as st
from typing import Dict, List
from supabase_database import supabase, grant_module_access, get_user_modules
from tquk_course_assignment import assign_course_to_learner, get_learner_enrollments

# ============================================
# AVAILABLE COURSES & MODULES
# ============================================

TQUK_COURSES = {
    "level3_adult_care": {
        "name": "Level 3 Diploma in Adult Care",
        "code": "610/0103/6",
        "module": "📚 Level 3 Adult Care"
    },
    "it_user_skills": {
        "name": "IT User Skills",
        "code": "TBD",
        "module": "💻 IT User Skills"
    },
    "customer_service": {
        "name": "Customer Service",
        "code": "TBD",
        "module": "🤝 Customer Service"
    },
    "business_admin": {
        "name": "Business Administration",
        "code": "TBD",
        "module": "📊 Business Administration"
    }
}

RTT_TRAINING = {
    "rtt_hospital_admin": {
        "name": "RTT & Hospital Administration Training",
        "modules": [
            "🎓 Learning Portal",
            "🎓 Training & Certification",
            "🏥 Patient Administration Hub",
            "🏥 Clinical Workflows",
            "✅ Task Management",
            "📊 Reports & Analytics"
        ]
    }
}

CAREER_TOOLS = {
    "cv_builder": {
        "name": "CV Builder",
        "module": "📄 CV Builder"
    },
    "interview_prep": {
        "name": "Job Interview Preparation",
        "module": "💼 Job Interview Prep"
    },
    "career_dev": {
        "name": "Career Development",
        "module": "💼 Career Development"
    }
}

BASIC_ACCESS = {
    "learning_portal": "🎓 Learning Portal",
    "help": "ℹ️ Help & Information"
}


# ============================================
# MAIN UI
# ============================================

def render_simple_course_assignment():
    """Simple one-page course and module assignment"""
    
    st.markdown("# 🎓 Assign Courses & Modules")
    
    st.info("""
    **Simple 3-step process:**
    1. Select a student
    2. Tick the courses/modules they need
    3. Click "Assign Selected"
    """)
    
    # Get all students
    try:
        result = supabase.table('users').select('*').eq('user_type', 'student').execute()
        students = result.data if result.data else []
    except Exception as e:
        st.error(f"Error loading students: {e}")
        return
    
    if not students:
        st.warning("No students found. Please register students first.")
        return
    
    # Select student
    student_options = {f"{s.get('full_name')} ({s.get('email')})": s for s in students}
    selected = st.selectbox(
        "📌 Select Student:",
        ["-- Select Student --"] + list(student_options.keys())
    )
    
    if selected == "-- Select Student --":
        st.info("👆 Please select a student to assign courses and modules")
        return
    
    student = student_options[selected]
    student_email = student.get('email')
    
    st.markdown(f"### Assigning to: **{student.get('full_name')}**")
    
    # Get current access
    try:
        current_modules = get_user_modules(student_email)
        current_enrollments = get_learner_enrollments(student_email)
    except:
        current_modules = []
        current_enrollments = []
    
    # Show current access
    with st.expander("📋 Current Access", expanded=False):
        if current_modules or current_enrollments:
            if current_enrollments:
                st.markdown("**TQUK Courses:**")
                for enrollment in current_enrollments:
                    st.write(f"✓ {enrollment.get('course_name')}")
            if current_modules:
                st.markdown("**Modules:**")
                for module in current_modules:
                    st.write(f"✓ {module}")
        else:
            st.info("No courses or modules assigned yet")
    
    st.markdown("---")
    
    # ============================================
    # TQUK QUALIFICATIONS
    # ============================================
    
    st.markdown("## 📚 TQUK Qualifications")
    st.caption("Select which TQUK courses to enroll this student in")
    
    selected_tquk = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        for course_id, course_info in list(TQUK_COURSES.items())[:2]:
            # Check if already enrolled
            already_enrolled = any(e.get('course_id') == course_id for e in current_enrollments)
            
            if st.checkbox(
                course_info['name'],
                value=already_enrolled,
                disabled=already_enrolled,
                key=f"tquk_{course_id}",
                help=f"Code: {course_info['code']}"
            ):
                if not already_enrolled:
                    selected_tquk.append(course_id)
    
    with col2:
        for course_id, course_info in list(TQUK_COURSES.items())[2:]:
            already_enrolled = any(e.get('course_id') == course_id for e in current_enrollments)
            
            if st.checkbox(
                course_info['name'],
                value=already_enrolled,
                disabled=already_enrolled,
                key=f"tquk_{course_id}",
                help=f"Code: {course_info['code']}"
            ):
                if not already_enrolled:
                    selected_tquk.append(course_id)
    
    # Add new TQUK course button
    if st.button("➕ Add New TQUK Course", help="Add more TQUK courses to the system"):
        st.info("Contact administrator to add new TQUK courses")
    
    st.markdown("---")
    
    # ============================================
    # RTT & NHS TRAINING
    # ============================================
    
    st.markdown("## 🏥 RTT & Hospital Administration Training")
    st.caption("Complete training program for NHS RTT pathways")
    
    selected_rtt = False
    
    # Check if already has RTT modules
    has_rtt = any(m in current_modules for m in RTT_TRAINING['rtt_hospital_admin']['modules'])
    
    selected_rtt = st.checkbox(
        "RTT & Hospital Administration Training",
        value=has_rtt,
        disabled=has_rtt,
        key="rtt_training",
        help="Includes: Learning Portal, Training & Certification, Patient Admin, Clinical Workflows, Task Management, Reports"
    )
    
    st.markdown("---")
    
    # ============================================
    # CAREER DEVELOPMENT
    # ============================================
    
    st.markdown("## 💼 Career Development Tools")
    st.caption("Optional career support tools")
    
    selected_career = []
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tool_id = "cv_builder"
        tool_info = CAREER_TOOLS[tool_id]
        has_tool = tool_info['module'] in current_modules
        
        if st.checkbox(
            tool_info['name'],
            value=has_tool,
            disabled=has_tool,
            key=f"career_{tool_id}"
        ):
            if not has_tool:
                selected_career.append(tool_id)
    
    with col2:
        tool_id = "interview_prep"
        tool_info = CAREER_TOOLS[tool_id]
        has_tool = tool_info['module'] in current_modules
        
        if st.checkbox(
            tool_info['name'],
            value=has_tool,
            disabled=has_tool,
            key=f"career_{tool_id}"
        ):
            if not has_tool:
                selected_career.append(tool_id)
    
    with col3:
        tool_id = "career_dev"
        tool_info = CAREER_TOOLS[tool_id]
        has_tool = tool_info['module'] in current_modules
        
        if st.checkbox(
            tool_info['name'],
            value=has_tool,
            disabled=has_tool,
            key=f"career_{tool_id}"
        ):
            if not has_tool:
                selected_career.append(tool_id)
    
    st.markdown("---")
    
    # ============================================
    # ASSIGN BUTTON
    # ============================================
    
    # Count selections
    total_selected = len(selected_tquk) + (1 if selected_rtt and not has_rtt else 0) + len(selected_career)
    
    if total_selected > 0:
        st.success(f"📌 {total_selected} new items selected for assignment")
        
        if st.button("✅ Assign Selected Courses & Modules", type="primary", use_container_width=True):
            admin_email = st.session_state.get('user_email', 'admin@example.com')
            
            success_count = 0
            error_count = 0
            
            with st.spinner("Assigning courses and modules..."):
                
                # Assign TQUK courses
                for course_id in selected_tquk:
                    try:
                        success, message = assign_course_to_learner(student_email, course_id, admin_email)
                        if success:
                            success_count += 1
                            # Also grant the module access
                            course_info = TQUK_COURSES[course_id]
                            grant_module_access(student_email, course_info['module'], admin_email)
                        else:
                            error_count += 1
                            st.warning(f"⚠️ {message}")
                    except Exception as e:
                        error_count += 1
                        st.error(f"❌ Error assigning {TQUK_COURSES[course_id]['name']}: {e}")
                
                # Assign RTT training
                if selected_rtt and not has_rtt:
                    try:
                        for module in RTT_TRAINING['rtt_hospital_admin']['modules']:
                            grant_module_access(student_email, module, admin_email)
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        st.error(f"❌ Error assigning RTT training: {e}")
                
                # Assign career tools
                for tool_id in selected_career:
                    try:
                        tool_info = CAREER_TOOLS[tool_id]
                        grant_module_access(student_email, tool_info['module'], admin_email)
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        st.error(f"❌ Error assigning {tool_info['name']}: {e}")
                
                # Always grant basic access
                try:
                    for module in BASIC_ACCESS.values():
                        if module not in current_modules:
                            grant_module_access(student_email, module, admin_email)
                except:
                    pass
            
            # Show results
            if success_count > 0:
                st.success(f"✅ Successfully assigned {success_count} courses/modules!")
                st.balloons()
            
            if error_count > 0:
                st.warning(f"⚠️ {error_count} assignments failed")
            
            if success_count > 0:
                st.info("🔄 Refreshing page...")
                st.rerun()
    
    else:
        st.info("👆 Select courses and modules above, then click assign")


# ============================================
# MANAGE EXISTING ASSIGNMENTS
# ============================================

def render_manage_assignments():
    """View and manage existing course assignments"""
    
    st.markdown("## 📋 Manage Existing Assignments")
    
    # Get all students with assignments
    try:
        result = supabase.table('users').select('*').eq('user_type', 'student').execute()
        students = result.data if result.data else []
    except Exception as e:
        st.error(f"Error loading students: {e}")
        return
    
    if not students:
        st.info("No students found")
        return
    
    # Show students with their assignments
    for student in students:
        with st.expander(f"👤 {student.get('full_name')} ({student.get('email')})"):
            try:
                modules = get_user_modules(student.get('email'))
                enrollments = get_learner_enrollments(student.get('email'))
                
                if enrollments:
                    st.markdown("**TQUK Courses:**")
                    for enrollment in enrollments:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"✓ {enrollment.get('course_name')}")
                        with col2:
                            if st.button("🗑️", key=f"remove_course_{student.get('email')}_{enrollment.get('id')}"):
                                # Remove enrollment
                                st.info("Unenrollment feature coming soon")
                
                if modules:
                    st.markdown("**Modules:**")
                    for module in modules:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"✓ {module}")
                        with col2:
                            if st.button("🗑️", key=f"remove_module_{student.get('email')}_{module}"):
                                try:
                                    supabase.table('module_access').delete().eq('user_email', student.get('email')).eq('module_name', module).execute()
                                    st.success("Removed!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                
                if not enrollments and not modules:
                    st.info("No assignments yet")
            
            except Exception as e:
                st.error(f"Error: {e}")
