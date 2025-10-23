"""
TQUK LEVEL 2 BUSINESS ADMINISTRATION - COMPLETE LEARNER MODULE
Integrated with RTT hospital administration for practical assessment
"""

import streamlit as st
from tquk_course_assignment import get_learner_enrollments

COURSE_ID = "level2_business_admin"
COURSE_NAME = "Level 2 Certificate in Business Administration"

UNITS = {
    1: {"name": "Principles of Business Administration", "credits": 3},
    2: {"name": "Communication in Business", "credits": 3},
    3: {"name": "Business Document Production", "credits": 3},
    4: {"name": "Using IT Systems", "credits": 3},
    5: {"name": "Team Working", "credits": 3},
    6: {"name": "Personal Development", "credits": 2},
    7: {"name": "Health & Safety", "credits": 3}
}

def render_business_admin_module():
    """Main module for Business Administration"""
    
    learner_email = st.session_state.get('user_email', '')
    
    st.title("📊 Level 2 Certificate in Business Administration")
    st.success("✅ **TQUK Approved** - Learn Using Real Hospital Administration (RTT)")
    
    # Get user role
    user_role = 'student'
    if hasattr(st.session_state, 'user_license') and hasattr(st.session_state.user_license, 'role'):
        user_role = st.session_state.user_license.role
    elif 'user_role' in st.session_state:
        user_role = st.session_state.user_role
    elif 'user_type' in st.session_state:
        user_role = st.session_state.user_type
    if learner_email and 'admin@t21services' in learner_email.lower():
        user_role = 'super_admin'
    
    # Check enrollment (bypass for admins, teachers, testers, staff)
    admin_roles = ['super_admin', 'admin', 'teacher', 'tester', 'staff', 'instructor', 'trainer']
    
    enrollments = get_learner_enrollments(learner_email)
    is_enrolled = any(e['course_id'] == COURSE_ID for e in enrollments)
    enrollment = next((e for e in enrollments if e['course_id'] == COURSE_ID), None) if is_enrolled else None
    
    # Only students need to be enrolled
    if not is_enrolled and user_role not in admin_roles:
        st.warning("⚠️ You are not enrolled in this course yet.")
        st.info("Contact your teacher to be assigned to this qualification.")
        return
    
    # For admins/staff viewing without enrollment
    if not is_enrolled and user_role in admin_roles:
        st.info("👨‍💼 **Admin/Staff View** - Full access to preview. Students must be enrolled.")
    
    if enrollment:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Progress", f"{enrollment['progress']}%")
            st.progress(enrollment['progress'] / 100)
        with col2:
            st.metric("Units Completed", f"{enrollment['units_completed']}/7")
        with col3:
            st.metric("Status", enrollment['status'].title())
    
    st.markdown("---")
    
    tabs = st.tabs(["📚 Overview", "📖 Materials", "🏥 RTT Practice", "📝 Assessments", "📊 Progress"])
    
    with tabs[0]:
        st.subheader("📚 Course Overview")
        
        # Welcome banner
        st.success("""
        # 📊 Welcome to Level 2 Business Administration!
        
        **Congratulations on starting your journey to becoming a qualified business administrator!**
        """)
        
        # Quick start guide
        st.info("""
        ## 🚀 Quick Start Guide - Your Journey to Qualification:
        
        **Step 1:** 📖 Study the 7 units (Materials tab)
        
        **Step 2:** 🏥 Practice with real hospital admin tasks (RTT Practice tab)
        
        **Step 3:** 📝 Submit evidence for all units (Assessments tab)
        
        **Step 4:** 📊 Track your progress (Progress tab)
        
        **Step 5:** 🎓 Get your certificate when complete!
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🏥 Learn Business Administration in Healthcare!
        
        **Practice with real hospital administration tasks using RTT system**
        
        ### 📋 Course Structure:
        """)
        
        for unit_num, unit_data in UNITS.items():
            with st.expander(f"Unit {unit_num}: {unit_data['name']} ({unit_data['credits']} credits)"):
                st.write(f"**Credits:** {unit_data['credits']}")
                st.write("**Assessment:** Hospital administration tasks in RTT")
    
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        
        st.success("""
        **📚 Welcome to Your Learning Materials!**
        
        Study all 7 units to complete your qualification.
        """)
        
        st.info("""
        **💡 Quick Guide:**
        - 📖 **Read** the content for each unit
        - ✏️ **Complete** the activities
        - 🏥 **Practice** in RTT system
        - 📝 **Submit** evidence in Assessments tab
        """)
        
        st.write("Materials available in TQUK_ALL_QUALIFICATIONS_SUMMARY.md")
    
    with tabs[2]:
        st.subheader("🏥 Practice with Hospital Administration")
        st.success("🚀 Practice business admin with real RTT workflows!")
        
        st.markdown("""
        ### Practical Tasks:
        
        - Create patient pathway documents
        - Generate RTT reports and statistics
        - Manage appointment schedules
        - Communicate with departments
        - Work with clinical teams
        - Maintain health & safety records
        """)
        
        if st.button("🚀 Go to RTT System", type="primary"):
            st.info("Navigate to 'Clinical Workflows' to practice!")
    
    with tabs[3]:
        st.subheader("📝 Assessment Submission")
        st.info("Submit evidence of business administration skills")
    
    with tabs[4]:
        st.subheader("📊 My Progress")
        st.info("Progress tracking coming soon!")
