"""
TQUK LEVEL 2 IT USER SKILLS - COMPLETE LEARNER MODULE
Integrated with RTT/PAS system for practical assessment
"""

import streamlit as st
from tquk_course_assignment import get_learner_enrollments

COURSE_ID = "level2_it_skills"
COURSE_NAME = "Level 2 Certificate in IT User Skills"

UNITS = {
    1: {
        "name": "Using IT to increase productivity",
        "ref": "J/617/2480",
        "credits": 4,
        "glh": 30,
        "level": 2,
        "file": "LEVEL2_IT_USER_SKILLS_COMPLETE.md",
        "learning_outcomes": 5,
        "activities": 10
    },
    2: {
        "name": "IT software fundamentals",
        "ref": "F/617/2428",
        "credits": 3,
        "glh": 20,
        "level": 2,
        "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    3: {
        "name": "IT security for users",
        "ref": "H/617/2423",
        "credits": 1,
        "glh": 10,
        "level": 1,
        "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md",
        "learning_outcomes": 1,
        "activities": 5
    },
    4: {
        "name": "Presentation software",
        "ref": "J/617/2429",
        "credits": 4,
        "glh": 30,
        "level": 2,
        "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md",
        "learning_outcomes": 3,
        "activities": 8
    },
    5: {
        "name": "Spreadsheet software",
        "ref": "A/617/2430",
        "credits": 4,
        "glh": 30,
        "level": 2,
        "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md",
        "learning_outcomes": 3,
        "activities": 8
    }
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
    
    # 8 tabs like Level 3 and Level 2 Business Admin
    tabs = st.tabs([
        "📚 Course Overview",
        "📖 Learning Materials", 
        "📝 Assessments",
        "📋 Evidence Tracking",
        "📥 TQUK Documents",
        "📊 My Progress",
        "🎓 Certificate",
        "🖥️ RTT Practice"
    ])
    
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
        # Assessments tab (EXACTLY like Level 3)
        from tquk_evidence_tracking import render_evidence_submission_form
        
        st.subheader("📝 Assessment & Evidence Submission")
        
        st.success("""
        **📚 Welcome to Assessments!**
        
        Submit evidence for each unit to demonstrate you've met the learning outcomes.
        """)
        
        st.info("""
        **💡 Types of Evidence You Can Submit:**
        
        - 📸 **Observation** - Your assessor watches you work
        - 📝 **Witness Statement** - Colleagues confirm your competence
        - 💭 **Reflective Account** - You reflect on your practice
        - 📄 **Product Evidence** - Documents you've created (reports, spreadsheets, etc.)
        - 💬 **Professional Discussion** - Discussion with your assessor
        - 📋 **Case Study** - Analysis of a real situation
        """)
        
        st.markdown("---")
        
        # Unit selector for assessment
        selected_unit = st.selectbox(
            "Select Unit for Assessment",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}",
            key="assessment_unit"
        )
        
        if selected_unit:
            # Use the proper evidence submission form
            render_evidence_submission_form(learner_email, COURSE_ID, selected_unit)
    
    with tabs[3]:
        # Evidence Tracking tab (EXACTLY like Level 3)
        from tquk_evidence_tracking import render_evidence_tracking
        render_evidence_tracking(learner_email, COURSE_ID)
    
    with tabs[4]:
        # TQUK Documents tab
        render_tquk_documents_tab()
    
    with tabs[5]:
        # My Progress tab
        st.subheader("📊 My Progress")
        if enrollment:
            st.markdown("### Overall Progress")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Completion", f"{enrollment['progress']}%")
                st.progress(enrollment['progress'] / 100)
            with col2:
                st.metric("Units Completed", f"{enrollment['units_completed']}/5")
            
            st.markdown("---")
            st.markdown("### Unit-by-Unit Progress")
            
            for unit_num, unit_data in UNITS.items():
                with st.expander(f"Unit {unit_num}: {unit_data['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Progress", "0%")
                        st.progress(0)
                    with col2:
                        st.metric("Status", "Not Started")
        else:
            st.info("Enrollment data not available.")
    
    with tabs[6]:
        # Certificate tab
        render_certificate(enrollment)
    
    with tabs[7]:
        # RTT Practice tab (moved from tab 2)
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


def render_tquk_documents_tab():
    """Render TQUK Documents tab with downloadable submission materials"""
    st.subheader("📥 TQUK Submission Documents")
    
    st.success("""
    **📄 Download Official Documents for TQUK Submission**
    
    All documents include T21 Services branding and your registered office details.
    """)
    
    st.info("""
    **How to use:**
    
    1. Click "📄 PDF" button to download documents
    2. Files download as **PDF format** with full company branding
    3. **Ready to send immediately** - No conversion needed!
    4. Email PDFs directly to TQUK for approval
    
    ✅ Professional PDF format with headers and footers!
    """)
    
    st.markdown("---")
    
    # Company details
    st.success("""
    **📌 Your Documents Include:**
    
    **Company:** T21 SERVICES LIMITED  
    **Company Number:** 13091053  
    **Centre Number:** 36257481088  
    **Address:** 64 Upper Parliament Street, Liverpool, L8 7LF
    """)
    
    st.markdown("---")
    
    st.markdown("## 📂 TQUK Submission Documents")
    
    with st.expander("📁 TQUK Submission Documents", expanded=True):
        st.caption("Documents to submit to TQUK for CDA approval")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**CDA Submission Package** 🔴 REQUIRED")
            st.caption("Complete submission with mapping matrix")
        with col2:
            if st.button("📄 PDF", key="cda_pdf", help="Download as PDF"):
                st.success("✅ Available")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Email Template to TQUK** 🔴 REQUIRED")
            st.caption("Copy-paste email for TQUK submission")
        with col2:
            if st.button("📄 PDF", key="email_pdf", help="Download as PDF"):
                st.success("✅ Available")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Assessment Pack Templates** 🔴 REQUIRED")
            st.caption("All assessment forms and templates")
        with col2:
            if st.button("📄 PDF", key="assessment_pdf", help="Download as PDF"):
                st.success("✅ Available")


def render_certificate(enrollment):
    """Render certificate tab"""
    st.subheader("🎓 TQUK Certificate")
    
    st.info("""
    **📜 About Your TQUK Certificate**
    
    Upon successful completion of this qualification, you will receive:
    
    1. **TQUK Level 2 Certificate in IT User Skills (RQF)**
       - Qualification Number: 603/3646/8
       - Ofqual regulated
       - Nationally recognized
       - 16 credits at Level 2
    
    2. **T21 RTT Hospital IT Certificate**
       - Industry-recognized certification
       - NHS IT expertise
       - Practical skills in hospital systems
       - Job-ready competencies
    """)
    
    st.markdown("---")
    
    st.markdown("### 📋 Requirements for Certification")
    
    st.write("""
    **To receive your TQUK certificate, you must:**
    
    ✅ Complete all 5 mandatory units  
    ✅ Submit evidence for all learning outcomes  
    ✅ Demonstrate competence in RTT/PAS practical tasks  
    ✅ Meet all assessment criteria  
    ✅ Pass internal quality assurance  
    ✅ Pass TQUK external quality assurance
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Your Progress")
    
    if enrollment:
        progress = enrollment.get('progress', 0)
        units_completed = enrollment.get('units_completed', 0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Progress", f"{progress}%")
            st.progress(progress / 100)
        with col2:
            st.metric("Units Completed", f"{units_completed}/5")
        
        if progress >= 100 and units_completed >= 5:
            st.success("""
            ### 🎉 Congratulations!
            
            You've completed all requirements!
            
            **Next Steps:**
            1. Your tutor will conduct final internal quality assurance
            2. Your portfolio will be submitted to TQUK
            3. TQUK will conduct external quality assurance
            4. Upon approval, your certificate will be issued
            5. You'll receive both TQUK and T21 certificates
            
            **Expected timeline:** 2-3 weeks after submission
            """)
        else:
            st.info(f"""
            **Keep going!**
            
            You're {progress}% complete. Complete all units and submit your evidence to qualify for certification.
            """)
    else:
        st.info("Progress data not available. Complete your enrollment to track progress.")
    
    st.markdown("---")
    
    st.markdown("### 💼 Career Opportunities")
    
    st.write("""
    **With this dual certification, you'll be qualified for:**
    
    - 🏥 Hospital IT Administrator
    - 💻 NHS IT Support Specialist
    - 📊 Healthcare Data Administrator
    - 🖥️ Medical Secretary with IT Skills
    - 📈 RTT/PAS System Administrator
    - 💼 Healthcare Office Manager
    
    **Your advantage:** Real NHS system experience + TQUK qualification!
    """)
