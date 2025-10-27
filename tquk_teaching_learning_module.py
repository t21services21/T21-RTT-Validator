"""
TQUK LEVEL 3 CERTIFICATE IN SUPPORTING TEACHING AND LEARNING IN SCHOOLS
Integrated with school administration systems for practical assessment
"""

import streamlit as st
from tquk_course_assignment import get_learner_enrollments

COURSE_ID = "level3_teaching_learning"
COURSE_NAME = "Level 3 Certificate in Supporting Teaching and Learning in Schools"

# Mandatory Units
MANDATORY_UNITS = {
    1: {
        "name": "Communication and professional relationships with children, young people and adults",
        "ref": "J/601/1434",
        "credits": 3,
        "glh": 25,
        "level": 3,
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    2: {
        "name": "Schools as organisations",
        "ref": "M/601/1436",
        "credits": 2,
        "glh": 15,
        "level": 3,
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 3,
        "activities": 6
    },
    3: {
        "name": "Promote equality, diversity and inclusion in work with children and young people",
        "ref": "T/601/1437",
        "credits": 2,
        "glh": 15,
        "level": 3,
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 3,
        "activities": 6
    }
}

# Optional Units (will be added to database)
OPTIONAL_UNITS = {
    4: {
        "name": "Support children and young people's health and safety",
        "ref": "Y/601/1693",
        "credits": 3,
        "glh": 20,
        "level": 3,
        "category": "Health & Safety",
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    5: {
        "name": "Understand child and young person development",
        "ref": "K/601/1694",
        "credits": 4,
        "glh": 30,
        "level": 3,
        "category": "Child Development",
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 5,
        "activities": 10
    },
    6: {
        "name": "Support assessment for learning",
        "ref": "A/601/1695",
        "credits": 3,
        "glh": 25,
        "level": 3,
        "category": "Teaching Support",
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    7: {
        "name": "Support literacy and numeracy activities",
        "ref": "F/601/1696",
        "credits": 4,
        "glh": 30,
        "level": 3,
        "category": "Teaching Support",
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 5,
        "activities": 10
    },
    8: {
        "name": "Support children and young people's positive behaviour",
        "ref": "J/601/1697",
        "credits": 3,
        "glh": 25,
        "level": 3,
        "category": "Behaviour Management",
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 4,
        "activities": 8
    },
    9: {
        "name": "Safeguarding and protection of children and young people",
        "ref": "L/601/1698",
        "credits": 3,
        "glh": 25,
        "level": 3,
        "category": "Safeguarding",
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 5,
        "activities": 10
    },
    10: {
        "name": "Support children and young people with disabilities and special educational needs",
        "ref": "R/601/1699",
        "credits": 4,
        "glh": 30,
        "level": 3,
        "category": "SEND Support",
        "file": "TEACHING_LEARNING_ALL_UNITS.md",
        "learning_outcomes": 5,
        "activities": 10
    }
}

def render_teaching_learning_module():
    """Main module for Teaching and Learning"""
    
    learner_email = st.session_state.get('user_email', '')
    
    st.title("👨‍🏫 Level 3 Certificate in Supporting Teaching and Learning in Schools")
    st.success("✅ **TQUK Approved** - Learn Using Real School Administration Systems")
    
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
    
    # Check enrollment
    admin_roles = ['super_admin', 'admin', 'teacher', 'tester', 'staff', 'instructor', 'trainer']
    
    enrollments = get_learner_enrollments(learner_email)
    is_enrolled = any(e['course_id'] == COURSE_ID for e in enrollments)
    enrollment = next((e for e in enrollments if e['course_id'] == COURSE_ID), None) if is_enrolled else None
    
    if not is_enrolled and user_role not in admin_roles:
        st.warning("⚠️ You are not enrolled in this course yet.")
        st.info("Contact your teacher to be assigned to this qualification.")
        return
    
    if not is_enrolled and user_role in admin_roles:
        st.info("👨‍💼 **Admin/Staff View** - Full access to preview. Students must be enrolled.")
    
    # Progress overview
    if enrollment:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Progress", f"{enrollment['progress']}%")
            st.progress(enrollment['progress'] / 100)
        with col2:
            total_units = len(MANDATORY_UNITS) + enrollment.get('optional_units_selected', 0)
            st.metric("Units Completed", f"{enrollment['units_completed']}/{total_units}")
        with col3:
            st.metric("Status", enrollment['status'].title())
    
    st.markdown("---")
    
    # 8 tabs (shortened names to ensure all visible on screen)
    tabs = st.tabs([
        "📚 Overview",
        "📖 Materials",
        "🎯 Optional",
        "📝 Assess",
        "📋 Evidence",
        "📥 Docs",
        "📊 Progress",
        "🎓 Certificate"
    ])
    
    with tabs[0]:
        st.subheader("📚 Course Overview")
        
        st.success("""
        # 👨‍🏫 Welcome to Level 3 Supporting Teaching and Learning!
        
        **Congratulations on starting your journey to becoming a qualified teaching assistant!**
        """)
        
        st.info("""
        ## 📋 Qualification Details:
        
        - **Code:** 601/2731/4
        - **Level:** 3
        - **Total Credits:** 30 minimum (3 mandatory + optional units)
        - **Duration:** 300+ hours TQT
        - **Assessment:** Portfolio of evidence
        """)
        
        st.success("""
        ## 🚀 Quick Start Guide:
        
        **Step 1:** 📖 Study all 3 mandatory units (Materials tab)
        
        **Step 2:** 🎯 Choose optional units to reach 30 credits minimum (Optional Units tab)
        
        **Step 3:** 🏫 Practice with school administration scenarios
        
        **Step 4:** 📝 Submit evidence for all units (Assessments tab)
        
        **Step 5:** 📊 Track your progress (Progress tab)
        
        **Step 6:** 🎓 TQUK will issue your certificate after verification!
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🏫 Learn Teaching Support Using Real Systems!
        
        **Practice with real school scenarios**
        
        🚀 **Learn by doing!** You'll practice teaching support skills:
        
        - **Communication:** Professional relationships with children, staff, parents
        - **School Organization:** Understanding school structures and procedures
        - **Equality & Diversity:** Promoting inclusion in schools
        - **Assessment Support:** Supporting learning and assessment
        - **Behaviour Management:** Supporting positive behaviour
        - **Safeguarding:** Protecting children and young people
        
        ### Course Structure:
        """)
        
        # Mandatory units
        st.markdown("### 📚 3 Mandatory Units (7 Credits):")
        
        for unit_num, unit_data in MANDATORY_UNITS.items():
            with st.expander(f"Unit {unit_num}: {unit_data['name']} ({unit_data['credits']} credits)"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Credits:** {unit_data['credits']}")
                with col2:
                    st.write(f"**GLH:** {unit_data['glh']} hours")
                with col3:
                    st.write(f"**Level:** {unit_data['level']}")
                st.write(f"**Reference:** {unit_data['ref']}")
                st.write(f"**Learning Outcomes:** {unit_data['learning_outcomes']}")
                st.write("**Assessment:** Portfolio of evidence from school practice")
        
        # Optional units info
        st.markdown("### 🎯 Optional Units:")
        st.info(f"""
        **Choose optional units to reach minimum 30 credits total:**
        - ✅ You've completed 3 mandatory units (7 credits)
        - 🎯 Choose at least 23 more credits from optional units
        - 📚 {len(OPTIONAL_UNITS)} optional units available
        
        **Go to Optional Units tab to select your units!**
        """)
        
        # Credits summary
        mandatory_credits = sum(unit['credits'] for unit in MANDATORY_UNITS.values())
        st.success(f"""
        ### ✅ Total Qualification:
        - **3 mandatory units** ({mandatory_credits} credits)
        - **Optional units** (minimum 23 credits needed)
        - **Minimum total: 30 credits**
        """)
    
    with tabs[1]:
        # Learning Materials tab
        from tquk_pdf_converter import create_unit_pdf
        
        st.subheader("📖 Learning Materials")
        
        st.success("""
        **📚 Welcome to Your Learning Materials!**
        
        Study all 3 mandatory units plus your chosen optional units.
        """)
        
        st.info("""
        **💡 Study Guide:**
        - 📖 Read each unit's learning outcomes and assessment criteria
        - ✏️ Complete the activities and exercises
        - 🏫 Practice with real school scenarios
        - 📝 Collect evidence as you work
        - ✅ Submit your portfolio for TQUK assessment
        """)
        
        st.markdown("---")
        
        # Unit selector
        all_units = {**MANDATORY_UNITS, **OPTIONAL_UNITS}
        selected_unit = st.selectbox(
            "Select Unit to Study:",
            options=list(all_units.keys()),
            format_func=lambda x: f"Unit {x}: {all_units[x]['name']} ({all_units[x]['credits']} credits)",
            key="learning_materials_unit"
        )
        
        if selected_unit:
            unit_data = all_units[selected_unit]
            
            # Unit header
            unit_type = "Mandatory" if selected_unit in MANDATORY_UNITS else "Optional"
            st.markdown(f"## 🎯 Unit {selected_unit}: {unit_data['name']}")
            st.caption(f"{unit_type} Unit • {unit_data['credits']} Credits • {unit_data['glh']} GLH • Level {unit_data['level']}")
            
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
                            file_name=f"Level3_Teaching_Learning_Unit{selected_unit}_{unit_data['name'].replace(' ', '_')}.pdf",
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
                            file_name=f"Level3_Teaching_Learning_Unit{selected_unit}_{unit_data['name'].replace(' ', '_')}.md",
                            mime="text/markdown",
                            key=f"download_md_{selected_unit}"
                        )
                else:
                    st.warning(f"⚠️ Materials for Unit {selected_unit} are being prepared.")
                    st.info("Use the school practice scenarios to start collecting evidence!")
                    
            except Exception as e:
                st.error(f"Error loading materials: {str(e)}")
    
    with tabs[2]:
        # Optional Units tab
        from tquk_optional_units import render_optional_units_selector, render_optional_units_content
        
        mandatory_credits = sum(unit['credits'] for unit in MANDATORY_UNITS.values())
        render_optional_units_selector(learner_email, COURSE_ID, required_credits=30, mandatory_credits=mandatory_credits)
        
        st.markdown("---")
        
        render_optional_units_content(learner_email, COURSE_ID, OPTIONAL_UNITS)
    
    with tabs[3]:
        # Assessments tab
        from tquk_evidence_tracking import render_evidence_submission_form
        
        st.subheader("📝 Assessment & Evidence Submission")
        
        st.success("""
        **📚 Welcome to Assessments!**
        
        Submit evidence for each unit to demonstrate you've met the learning outcomes.
        """)
        
        st.info("""
        **💡 Types of Evidence You Can Submit:**
        
        - 📸 **Observation** - Your assessor watches you work with children
        - 📝 **Witness Statement** - Teachers/colleagues confirm your competence
        - 💭 **Reflective Account** - You reflect on your teaching support practice
        - 📄 **Product Evidence** - Lesson plans, resources, assessments
        - 💬 **Professional Discussion** - Discussion with your assessor
        - 📋 **Case Study** - Analysis of a real teaching situation
        """)
        
        st.markdown("---")
        
        # Unit selector
        all_units = {**MANDATORY_UNITS, **OPTIONAL_UNITS}
        selected_unit = st.selectbox(
            "Select Unit for Assessment",
            options=list(all_units.keys()),
            format_func=lambda x: f"Unit {x}: {all_units[x]['name']}",
            key="assessment_unit"
        )
        
        if selected_unit:
            render_evidence_submission_form(learner_email, COURSE_ID, selected_unit)
    
    with tabs[4]:
        # Evidence Tracking tab
        from tquk_evidence_tracking import render_evidence_tracking
        render_evidence_tracking(learner_email, COURSE_ID)
    
    with tabs[5]:
        # TQUK Documents tab
        render_tquk_documents_tab()
    
    with tabs[6]:
        # My Progress tab
        st.subheader("📊 My Progress")
        if enrollment:
            st.markdown("### Overall Progress")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Progress", f"{enrollment['progress']}%")
                st.progress(enrollment['progress'] / 100)
            with col2:
                total_units = len(MANDATORY_UNITS) + enrollment.get('optional_units_selected', 0)
                st.metric("Units Completed", f"{enrollment['units_completed']}/{total_units}")
            
            st.markdown("---")
            st.markdown("### Mandatory Units Progress")
            
            for unit_num, unit_data in MANDATORY_UNITS.items():
                with st.expander(f"Unit {unit_num}: {unit_data['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Status", "In Progress")
                    with col2:
                        st.metric("Evidence Submitted", "0")
        else:
            st.info("Enrollment data not available.")
    
    with tabs[7]:
        # Certificate tab
        render_certificate(enrollment)


def render_tquk_documents_tab():
    """Render TQUK Documents tab"""
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
            if st.button("📄 PDF", key="cda_pdf"):
                st.success("✅ Available")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Email Template to TQUK** 🔴 REQUIRED")
            st.caption("Copy-paste email for TQUK submission")
        with col2:
            if st.button("📄 PDF", key="email_pdf"):
                st.success("✅ Available")


def render_certificate(enrollment):
    """Render certificate tab"""
    st.subheader("🎓 TQUK Certificate")
    
    st.info("""
    **📜 About Your TQUK Certificate**
    
    Upon successful completion, you will receive:
    
    1. **TQUK Level 3 Certificate in Supporting Teaching and Learning in Schools (RQF)**
       - Qualification Number: 601/2731/4
       - Ofqual regulated
       - Nationally recognized
       - Minimum 30 credits at Level 3
    
    2. **T21 Teaching Support Certificate**
       - Industry-recognized certification
       - School teaching support expertise
       - Practical skills in education settings
       - Job-ready competencies
    """)
    
    st.markdown("---")
    
    st.markdown("### 📋 Requirements for Certification")
    
    st.write("""
    **To receive your TQUK certificate, you must:**
    
    ✅ Complete all 3 mandatory units (7 credits)  
    ✅ Complete optional units to reach minimum 30 credits  
    ✅ Submit evidence for all learning outcomes  
    ✅ Demonstrate competence in teaching support tasks  
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
            total_units = len(MANDATORY_UNITS) + enrollment.get('optional_units_selected', 0)
            st.metric("Units Completed", f"{units_completed}/{total_units}")
        
        if progress >= 100:
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
    
    - 🏫 Teaching Assistant
    - 💼 Learning Support Assistant
    - 👶 Early Years Educator
    - 🤝 Special Educational Needs Assistant
    - 📋 Classroom Support Worker
    - 💻 Higher Level Teaching Assistant (HLTA)
    
    **Your advantage:** Real school experience + TQUK qualification!
    """)
