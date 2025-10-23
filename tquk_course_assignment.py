"""
TQUK COURSE ASSIGNMENT SYSTEM
Allows teachers to assign TQUK qualifications to learners and track enrollments
"""

import streamlit as st
import json
from datetime import datetime

# Import Supabase client
try:
    from supabase_client import get_supabase_client
except ImportError:
    def get_supabase_client():
        try:
            from supabase_database import supabase
            return supabase
        except:
            return None

# Available TQUK Qualifications
TQUK_QUALIFICATIONS = {
    "level3_adult_care": {
        "name": "Level 3 Diploma in Adult Care",
        "code": "610/0103/6",
        "duration": "12-18 weeks",
        "price": "£1,500",
        "credits": 58,
        "units": 7
    },
    "level2_it_skills": {
        "name": "Level 2 Certificate in IT User Skills",
        "code": "603/0646/8",
        "duration": "10-12 weeks",
        "price": "£700",
        "credits": 20,
        "units": 5
    },
    "level2_customer_service": {
        "name": "Level 2 Certificate in Customer Service",
        "code": "603/3896/7",
        "duration": "10-12 weeks",
        "price": "£700",
        "credits": 18,
        "units": 6
    },
    "level2_business_admin": {
        "name": "Level 2 Certificate in Business Administration",
        "code": "603/2949/X",
        "duration": "10-12 weeks",
        "price": "£700",
        "credits": 20,
        "units": 7
    }
}


def assign_course_to_learner(learner_email, course_id, assigned_by):
    """Assign a TQUK course to a learner"""
    try:
        supabase = get_supabase_client()
        
        # Check if already enrolled
        existing = supabase.table('tquk_enrollments').select('*').eq('learner_email', learner_email).eq('course_id', course_id).execute()
        
        if existing.data:
            return False, "Learner already enrolled in this course"
        
        # Create enrollment
        enrollment_data = {
            'learner_email': learner_email,
            'course_id': course_id,
            'course_name': TQUK_QUALIFICATIONS[course_id]['name'],
            'assigned_by': assigned_by,
            'assigned_date': datetime.now().isoformat(),
            'status': 'enrolled',
            'progress': 0,
            'units_completed': 0,
            'total_units': TQUK_QUALIFICATIONS[course_id]['units']
        }
        
        result = supabase.table('tquk_enrollments').insert(enrollment_data).execute()
        return True, "Course assigned successfully!"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_learner_enrollments(learner_email):
    """Get all courses a learner is enrolled in"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('tquk_enrollments').select('*').eq('learner_email', learner_email).execute()
        return result.data if result.data else []
    except:
        return []


def get_all_enrollments():
    """Get all course enrollments (for teachers)"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('tquk_enrollments').select('*').order('assigned_date', desc=True).execute()
        return result.data if result.data else []
    except:
        return []


def update_learner_progress(learner_email, course_id, progress, units_completed):
    """Update learner's progress in a course"""
    try:
        supabase = get_supabase_client()
        
        update_data = {
            'progress': progress,
            'units_completed': units_completed,
            'last_updated': datetime.now().isoformat()
        }
        
        # Update status based on progress
        if progress >= 100:
            update_data['status'] = 'completed'
            update_data['completion_date'] = datetime.now().isoformat()
        elif progress > 0:
            update_data['status'] = 'in_progress'
        
        result = supabase.table('tquk_enrollments').update(update_data).eq('learner_email', learner_email).eq('course_id', course_id).execute()
        return True
        
    except Exception as e:
        st.error(f"Error updating progress: {str(e)}")
        return False


def render_course_assignment_ui():
    """Teacher interface for assigning courses"""
    st.subheader("📚 Assign TQUK Qualifications to Learners")
    
    # Get list of students
    try:
        supabase = get_supabase_client()
        students = supabase.table('users').select('email, full_name, role').eq('role', 'student').execute()
        student_list = students.data if students.data else []
    except:
        student_list = []
    
    if not student_list:
        st.warning("No students found. Add students first in Student Management.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Select Learner")
        selected_student = st.selectbox(
            "Choose student",
            options=[s['email'] for s in student_list],
            format_func=lambda x: f"{next((s['full_name'] for s in student_list if s['email'] == x), x)} ({x})"
        )
    
    with col2:
        st.markdown("### Select Course")
        selected_course = st.selectbox(
            "Choose qualification",
            options=list(TQUK_QUALIFICATIONS.keys()),
            format_func=lambda x: TQUK_QUALIFICATIONS[x]['name']
        )
    
    # Show course details
    if selected_course:
        course = TQUK_QUALIFICATIONS[selected_course]
        st.info(f"""
        **{course['name']}**
        - Code: {course['code']}
        - Duration: {course['duration']}
        - Price: {course['price']}
        - Credits: {course['credits']}
        - Units: {course['units']}
        """)
    
    if st.button("✅ Assign Course", type="primary"):
        success, message = assign_course_to_learner(
            selected_student,
            selected_course,
            st.session_state.get('user_email', 'admin')
        )
        
        if success:
            st.success(message)
            st.balloons()
        else:
            st.error(message)
    
    # Show current enrollments
    st.markdown("---")
    st.subheader("📊 Current Enrollments")
    
    enrollments = get_all_enrollments()
    
    if enrollments:
        for enrollment in enrollments:
            with st.expander(f"{enrollment['learner_email']} - {enrollment['course_name']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Progress", f"{enrollment['progress']}%")
                
                with col2:
                    st.metric("Units Completed", f"{enrollment['units_completed']}/{enrollment['total_units']}")
                
                with col3:
                    status_color = {
                        'enrolled': '🟡',
                        'in_progress': '🔵',
                        'completed': '🟢'
                    }
                    st.metric("Status", f"{status_color.get(enrollment['status'], '⚪')} {enrollment['status'].title()}")
                
                st.caption(f"Assigned: {enrollment['assigned_date'][:10]} by {enrollment['assigned_by']}")
    else:
        st.info("No enrollments yet. Assign courses to learners above.")


def render_learner_courses_ui(learner_email):
    """Learner interface showing their enrolled courses"""
    st.subheader("🎓 My TQUK Qualifications")
    
    enrollments = get_learner_enrollments(learner_email)
    
    if not enrollments:
        st.info("You are not enrolled in any TQUK qualifications yet. Contact your teacher.")
        return enrollments
    
    # Show enrolled courses
    for enrollment in enrollments:
        status_emoji = {
            'enrolled': '🟡',
            'in_progress': '🔵',
            'completed': '🟢'
        }
        
        with st.container():
            st.markdown(f"### {status_emoji.get(enrollment['status'], '⚪')} {enrollment['course_name']}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Progress", f"{enrollment['progress']}%")
                st.progress(enrollment['progress'] / 100)
            
            with col2:
                st.metric("Units Completed", f"{enrollment['units_completed']}/{enrollment['total_units']}")
            
            with col3:
                st.metric("Status", enrollment['status'].title())
            
            if enrollment['status'] == 'completed':
                st.success(f"✅ Completed on {enrollment.get('completion_date', 'N/A')[:10]}")
                st.info("🎓 Your TQUK certificate will be issued after internal and external verification (6-8 weeks)")
            
            st.markdown("---")
    
    return enrollments
