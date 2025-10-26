"""
TQUK LEVEL 2 CUSTOMER SERVICE - COMPLETE LEARNER MODULE
Integrated with PAS patient reception for practical assessment
"""

import streamlit as st
from tquk_course_assignment import get_learner_enrollments

COURSE_ID = "level2_customer_service"
COURSE_NAME = "Level 2 Certificate in Customer Service"

UNITS = {
    1: {
        "name": "Customer Service Delivery",
        "ref": "TBD",
        "credits": 3,
        "glh": 20,
        "level": 2,
        "file": "CUSTOMER_SERVICE_ALL_UNITS_COMPLETE.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    2: {
        "name": "Communication with Customers",
        "ref": "TBD",
        "credits": 3,
        "glh": 20,
        "level": 2,
        "file": "CUSTOMER_SERVICE_ALL_UNITS_COMPLETE.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    3: {
        "name": "Understanding the Organization",
        "ref": "TBD",
        "credits": 3,
        "glh": 20,
        "level": 2,
        "file": "CUSTOMER_SERVICE_ALL_UNITS_COMPLETE.md",
        "learning_outcomes": 3,
        "activities": 6
    },
    4: {
        "name": "Handling Customer Problems",
        "ref": "TBD",
        "credits": 3,
        "glh": 20,
        "level": 2,
        "file": "CUSTOMER_SERVICE_ALL_UNITS_COMPLETE.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    5: {
        "name": "Working in a Team",
        "ref": "TBD",
        "credits": 3,
        "glh": 20,
        "level": 2,
        "file": "CUSTOMER_SERVICE_ALL_UNITS_COMPLETE.md",
        "learning_outcomes": 3,
        "activities": 6
    },
    6: {
        "name": "Personal Development",
        "ref": "TBD",
        "credits": 3,
        "glh": 20,
        "level": 2,
        "file": "CUSTOMER_SERVICE_ALL_UNITS_COMPLETE.md",
        "learning_outcomes": 3,
        "activities": 6
    }
}

def render_customer_service_module():
    """Main module for Customer Service"""
    
    learner_email = st.session_state.get('user_email', '')
    
    st.title("🤝 Level 2 Certificate in Customer Service")
    st.success("✅ **TQUK Approved** - Learn Using Real Patient Reception System (PAS)")
    
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
            st.metric("Units Completed", f"{enrollment['units_completed']}/6")
        with col3:
            st.metric("Status", enrollment['status'].title())
    
    st.markdown("---")
    
    # 8 tabs like Level 3, Business Admin, and IT User Skills
    tabs = st.tabs([
        "📚 Course Overview",
        "📖 Learning Materials",
        "📝 Assessments",
        "📋 Evidence Tracking",
        "📥 TQUK Documents",
        "📊 My Progress",
        "🎓 Certificate",
        "👥 PAS Practice"
    ])
    
    with tabs[0]:
        st.subheader("📚 Course Overview")
        
        # Welcome banner
        st.success("""
        # 🤝 Welcome to Level 2 Customer Service!
        
        **Congratulations on starting your journey to becoming a qualified customer service professional!**
        """)
        
        # Qualification details
        st.info("""
        ## 📋 Qualification Details:
        
        - **Code:** 603/3896/7
        - **Level:** 2
        - **Total Credits:** 18 (6 mandatory units)
        - **Duration:** 180 hours TQT / 120 hours GLH
        - **Assessment:** Portfolio of evidence
        """)
        
        # Quick start guide
        st.success("""
        ## 🚀 Quick Start Guide - Your Journey to Qualification:
        
        **Step 1:** 📖 Study all 6 mandatory units (Materials tab)
        
        **Step 2:** 👥 Practice with patient reception scenarios (Practice tab)
        
        **Step 3:** 📝 Submit evidence for all units (Assessments tab)
        
        **Step 4:** 📊 Track your progress (Progress tab)
        
        **Step 5:** 🎓 TQUK will issue your certificate after verification!
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🏥 Learn Customer Service in Healthcare!
        
        **Practice with real patient reception scenarios**
        
        🚀 **Learn by doing!** You'll use our **real PAS patient reception system** to practice customer service:
        
        - **Patient Interactions:** Greet and assist patients professionally
        - **Communication:** Handle inquiries and provide information
        - **Problem Solving:** Resolve patient concerns and complaints
        - **Teamwork:** Collaborate with medical staff
        - **Professional Development:** Track your growth and skills
        
        ### Course Structure:
        """)
        
        # Display all units with credits
        st.markdown("### 📚 6 Mandatory Units (18 Credits Total):")
        
        for unit_num, unit_data in UNITS.items():
            with st.expander(f"Unit {unit_num}: {unit_data['name']} ({unit_data['credits']} credits)"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Credits:** {unit_data['credits']}")
                with col2:
                    st.write(f"**GLH:** {unit_data['glh']} hours")
                with col3:
                    st.write(f"**Level:** {unit_data['level']}")
                st.write(f"**Learning Outcomes:** {unit_data['learning_outcomes']}")
                st.write("**Assessment:** Portfolio of evidence using PAS patient reception")
        
        # Credits summary
        total_credits = sum(unit['credits'] for unit in UNITS.values())
        st.success(f"""
        ### ✅ Total Qualification:
        - **6 mandatory units**
        - **{total_credits} credits total**
        - **All units must be completed**
        """)
    
    with tabs[1]:
        # Learning Materials tab (EXACTLY like Level 3)
        from tquk_pdf_converter import create_unit_pdf
        
        st.subheader("📖 Learning Materials")
        
        st.success("""
        **📚 Welcome to Your Learning Materials!**
        
        Study all 6 mandatory units to complete your qualification.
        """)
        
        st.info("""
        **💡 Study Guide:**
        - 📖 Read each unit's learning outcomes and assessment criteria
        - ✏️ Complete the activities and exercises
        - 🏥 Practice with real PAS patient reception scenarios
        - 📝 Collect evidence as you work
        - ✅ Submit your portfolio for TQUK assessment
        """)
        
        st.markdown("---")
        
        # Unit selector
        selected_unit = st.selectbox(
            "Select Unit to Study:",
            options=list(UNITS.keys()),
            format_func=lambda x: f"Unit {x}: {UNITS[x]['name']} ({UNITS[x]['credits']} credits)",
            key="learning_materials_unit"
        )
        
        if selected_unit:
            unit_data = UNITS[selected_unit]
            
            # Unit header
            st.markdown(f"## 🎯 Unit {selected_unit}: {unit_data['name']}")
            st.caption(f"Mandatory Unit • {unit_data['credits']} Credits • {unit_data['glh']} GLH • Level {unit_data['level']}")
            
            # Unit info cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Learning Outcomes", unit_data['learning_outcomes'])
            with col2:
                st.metric("Activities", unit_data['activities'])
            with col3:
                st.metric("Credits", unit_data['credits'])
            
            st.markdown("---")
            
            # Load and display content
            try:
                def load_markdown_file(filename):
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            return f.read()
                    except Exception as e:
                        return f"Error loading file: {str(e)}"
                
                content = load_markdown_file(unit_data['file'])
                
                if content and not content.startswith("Error"):
                    with st.container():
                        st.markdown(content, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Interactive elements
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"✅ Mark Unit {selected_unit} Complete", key=f"complete_{selected_unit}", type="primary"):
                            st.success(f"✅ Unit {selected_unit} marked as complete!")
                    
                    with col2:
                        if st.button(f"📝 Go to Assessment", key=f"assess_{selected_unit}"):
                            st.info("Switch to the 'Assessments' tab to submit your evidence!")
                    
                    # Download option
                    try:
                        pdf_buffer = create_unit_pdf(selected_unit, unit_data['name'], content)
                        st.download_button(
                            label=f"📥 Download Unit {selected_unit} as PDF",
                            data=pdf_buffer,
                            file_name=f"Level2_Customer_Service_Unit{selected_unit}_{unit_data['name'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            help="Download professional PDF document",
                            key=f"download_{selected_unit}",
                            type="primary"
                        )
                    except Exception as e:
                        st.error(f"PDF generation error: {str(e)}")
                        st.download_button(
                            label=f"📥 Download Unit {selected_unit} (Markdown)",
                            data=content,
                            file_name=f"Level2_Customer_Service_Unit{selected_unit}_{unit_data['name'].replace(' ', '_')}.md",
                            mime="text/markdown",
                            key=f"download_md_{selected_unit}"
                        )
                else:
                    st.warning(f"⚠️ Materials for Unit {selected_unit} are being prepared.")
                    st.info("Use the PAS Practice tab to start collecting evidence!")
                    
            except Exception as e:
                st.error(f"Error loading materials: {str(e)}")
    
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
        
        - 📸 **Observation** - Your assessor watches you work with patients
        - 📝 **Witness Statement** - Colleagues confirm your customer service skills
        - 💭 **Reflective Account** - You reflect on your customer service practice
        - 📄 **Product Evidence** - Documents you've created (emails, reports, etc.)
        - 💬 **Professional Discussion** - Discussion with your assessor
        - 📋 **Case Study** - Analysis of a real customer service situation
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
                st.metric("Progress", f"{enrollment['progress']}%")
                st.progress(enrollment['progress'] / 100)
            with col2:
                st.metric("Units Completed", f"{enrollment['units_completed']}/6")
            
            st.markdown("---")
            st.markdown("### Unit Progress")
            
            for unit_num, unit_data in UNITS.items():
                with st.expander(f"Unit {unit_num}: {unit_data['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Status", "In Progress")
                    with col2:
                        st.metric("Evidence Submitted", "0")
        else:
            st.info("Enrollment data not available.")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Progress", "0%")
                st.progress(0)
            with col2:
                st.metric("Status", "Not Started")
    
    with tabs[6]:
        # Certificate tab
        render_certificate(enrollment)
    
    with tabs[7]:
        # PAS Practice tab
        st.subheader("👥 Practice with PAS Patient Reception")
        st.success("🚀 **UNIQUE FEATURE:** Practice customer service using real patient reception system!")
        
        st.markdown("""
        ### Practical Exercises:
        
        **Unit 1: Customer Service Delivery**
        - Greet patients professionally
        - Assess patient needs
        - Provide excellent service
        - Handle different patient types
        
        **Unit 2: Communication with Customers**
        - Practice verbal communication
        - Use appropriate body language
        - Write professional emails
        - Listen actively to patients
        
        **Unit 3: Understanding the Organization**
        - Learn hospital structure
        - Understand NHS services
        - Follow hospital procedures
        - Know your role and responsibilities
        
        **Unit 4: Handling Customer Problems**
        - Identify patient concerns
        - Resolve complaints professionally
        - Escalate when necessary
        - Document issues properly
        
        **Unit 5: Working in a Team**
        - Collaborate with medical staff
        - Support colleagues
        - Communicate effectively in teams
        - Contribute to team goals
        
        **Unit 6: Personal Development**
        - Identify your development needs
        - Set personal goals
        - Track your learning
        - Review your progress
        """)
        
        if st.button("🚀 Go to PAS System", type="primary"):
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
    
    1. **TQUK Level 2 Certificate in Customer Service (RQF)**
       - Qualification Number: 603/3896/7
       - Ofqual regulated
       - Nationally recognized
       - 18 credits at Level 2
    
    2. **T21 PAS Customer Service Certificate**
       - Industry-recognized certification
       - NHS customer service expertise
       - Practical skills in patient reception
       - Job-ready competencies
    """)
    
    st.markdown("---")
    
    st.markdown("### 📋 Requirements for Certification")
    
    st.write("""
    **To receive your TQUK certificate, you must:**
    
    ✅ Complete all 6 mandatory units  
    ✅ Submit evidence for all learning outcomes  
    ✅ Demonstrate competence in PAS patient reception tasks  
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
            st.metric("Units Completed", f"{units_completed}/6")
        
        if progress >= 100 and units_completed >= 6:
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
    
    - 🏥 Hospital Receptionist
    - 💼 NHS Customer Service Advisor
    - 📞 Patient Services Coordinator
    - 🤝 Patient Liaison Officer
    - 📋 Healthcare Administrator
    - 💻 Medical Secretary
    
    **Your advantage:** Real NHS system experience + TQUK qualification!
    """)
