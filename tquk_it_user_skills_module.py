"""
TQUK LEVEL 2 IT USER SKILLS - COMPLETE LEARNER MODULE
Integrated with RTT/PAS system for practical assessment
"""

import streamlit as st
from tquk_course_assignment import get_learner_enrollments

COURSE_ID = "level2_it_skills"
COURSE_NAME = "Level 2 Certificate in IT User Skills"

UNITS = {
    1: {"name": "Using IT Systems", "credits": 5, "file": "LEVEL2_IT_USER_SKILLS_COMPLETE.md"},
    2: {"name": "IT Communication Fundamentals", "credits": 4, "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md"},
    3: {"name": "IT Software Fundamentals", "credits": 4, "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md"},
    4: {"name": "Using Collaborative Technologies", "credits": 3, "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md"},
    5: {"name": "Using Databases", "credits": 4, "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md"}
}


def render_it_user_skills_module():
    """Main module for IT User Skills"""
    
    learner_email = st.session_state.get('user_email', '')
    
    st.title("💻 Level 2 Certificate in IT User Skills")
    st.success("✅ **TQUK Approved** - Learn Using Real NHS Systems (RTT/PAS)")
    
    # Get user role - check multiple possible locations
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
    
    # Progress overview
    if enrollment:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Progress", f"{enrollment['progress']}%")
            st.progress(enrollment['progress'] / 100)
        with col2:
            st.metric("Units Completed", f"{enrollment['units_completed']}/5")
        with col3:
            st.metric("Status", enrollment['status'].title())
    
    st.markdown("---")
    
    tabs = st.tabs(["📚 Overview", "📖 Materials", "🖥️ RTT/PAS Practice", "📝 Assessments", "📊 Progress"])
    
    with tabs[0]:
        st.subheader("📚 Course Overview")
        
        # Welcome banner
        st.success("""
        # 💻 Welcome to Level 2 IT User Skills!
        
        **Congratulations on starting your journey to becoming IT proficient!**
        """)
        
        # Quick start guide
        st.info("""
        ## 🚀 Quick Start Guide - Your Journey to Qualification:
        
        **Step 1:** 📖 Study the 6 units (Materials tab)
        
        **Step 2:** 💻 Practice with hospital IT systems (Practice tab)
        
        **Step 3:** 📝 Submit evidence for all units (Assessments tab)
        
        **Step 4:** 📊 Track your progress (Progress tab)
        
        **Step 5:** 🎓 TQUK will issue your certificate after verification!
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🏥 Learn IT Skills in Healthcare!
        
        **Practice with real hospital IT systems**
        
        ### 📋 Course Structure:
        """)
        
        st.markdown("""
        ### What Makes This Course Unique?
        
        🚀 **Learn by doing!** You'll use our **real RTT/PAS hospital system** to practice IT skills:
        
        - **Word Processing:** Create patient letters and medical documents
        - **Spreadsheets:** Generate waiting list reports and RTT statistics
        - **Databases:** Search patient records and query waiting lists
        - **Email:** Send appointment notifications and department communications
        - **Collaboration:** Use shared calendars and team documents
        
        ### Course Structure:
        """)
        
        for unit_num, unit_data in UNITS.items():
            with st.expander(f"Unit {unit_num}: {unit_data['name']} ({unit_data['credits']} credits)"):
                st.write(f"**Credits:** {unit_data['credits']}")
                st.write("**Assessment:** Practical tasks using RTT/PAS system")
    
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        
        st.success("""
        **📚 Welcome to Your Learning Materials!**
        
        Study all 6 units to complete your qualification.
        """)
        
        st.info("""
        **💡 Quick Guide:**
        - 📖 **Read** the content for each unit
        - ✏️ **Complete** the activities
        - 💻 **Practice** with hospital IT systems
        - 📝 **Submit** evidence in Assessments tab
        """)
        
        st.write("Materials available in TQUK_ALL_QUALIFICATIONS_SUMMARY.md")
        
        selected_unit = st.selectbox(
            "Select Unit",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}"
        )
        
        if selected_unit:
            unit = UNITS[selected_unit]
            st.markdown(f"### Unit {selected_unit}: {unit['name']}")
            
            try:
                with open(unit['file'], 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Show relevant section
                    if selected_unit == 1:
                        st.markdown(content)
                    else:
                        st.info(f"📘 Unit {selected_unit} materials - Summary format")
                        # Extract unit summary from TQUK_ALL_QUALIFICATIONS_SUMMARY.md
                        if f"UNIT {selected_unit}:" in content:
                            start = content.find(f"UNIT {selected_unit}:")
                            end = content.find(f"UNIT {selected_unit + 1}:") if selected_unit < 5 else len(content)
                            st.markdown(content[start:end])
                        else:
                            st.markdown("Full materials coming soon!")
            except:
                st.error("Error loading materials. Please contact your teacher.")
    
    with tabs[2]:
        st.subheader("🖥️ Practice with RTT/PAS System")
        st.success("🚀 **UNIQUE FEATURE:** Practice IT skills using real hospital software!")
        
        st.markdown("""
        ### Practical Exercises:
        
        Use the RTT/PAS system to complete these tasks:
        
        **Unit 1: Using IT Systems**
        - Navigate the RTT/PAS interface
        - Manage files and folders
        - Use help features
        - Apply security best practices
        
        **Unit 2: IT Communication**
        - Send patient appointment emails
        - Research NHS guidelines online
        - Share documents securely
        - Follow email protocols
        
        **Unit 3: IT Software**
        - Create patient letter templates (Word)
        - Generate waiting list reports (Excel)
        - Format medical documents
        - Print appointment schedules
        
        **Unit 4: Collaboration**
        - Use shared appointment calendars
        - Collaborate on patient lists
        - Work with multi-disciplinary teams
        
        **Unit 5: Databases**
        - Search patient database
        - Query waiting lists
        - Generate RTT reports
        - Maintain data quality
        """)
        
        if st.button("🚀 Go to RTT/PAS System", type="primary"):
            st.info("Navigate to 'Patient Administration Hub' in the sidebar to practice!")
    
    with tabs[3]:
        st.subheader("📝 Assessment Submission")
        st.info("Submit evidence of your IT skills using the RTT/PAS system")
        
        selected_unit = st.selectbox(
            "Unit",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="assess_unit"
        )
        
        evidence_type = st.selectbox(
            "Evidence Type",
            ["Screenshot", "Document Created", "Report Generated", "Email Sent", "Database Query"]
        )
        
        description = st.text_area("Description", placeholder="Describe what you did...")
        uploaded_file = st.file_uploader("Upload Evidence", type=['pdf', 'docx', 'png', 'jpg'])
        
        if st.button("📤 Submit Evidence"):
            if description and uploaded_file:
                st.success("✅ Evidence submitted!")
                st.balloons()
            else:
                st.warning("Please provide description and file")
    
    with tabs[4]:
        st.subheader("📊 My Progress")
        if enrollment:
            for unit_num, unit_data in UNITS.items():
                with st.expander(f"Unit {unit_num}: {unit_data['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Progress", "0%")
                        st.progress(0)
                    with col2:
                        st.metric("Status", "Not Started")
