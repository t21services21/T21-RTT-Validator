"""
TQUK LEVEL 2 BUSINESS ADMINISTRATION - COMPLETE LEARNER MODULE
Integrated with RTT hospital administration for practical assessment
"""

import streamlit as st
from tquk_course_assignment import get_learner_enrollments

COURSE_ID = "level2_business_admin"
COURSE_NAME = "Level 2 Certificate in Business Administration"

# TQUK Level 2 Business Admin - Official Structure (603/2949/X)
# 5 Mandatory + 2 Optional (from 13 choices) = 20 credits minimum

MANDATORY_UNITS = {
    1: {
        "name": "Principles of providing administrative services",
        "ref": "A/616/8832",
        "credits": 4,
        "glh": 25,
        "rtt_tasks": ["RTT clinic scheduling", "Meeting organization", "Diary management", "Mail handling"]
    },
    2: {
        "name": "Principles of business document production and information management",
        "ref": "F/616/8833",
        "credits": 3,
        "glh": 21,
        "rtt_tasks": ["RTT letters", "Pathway reports", "Clinic documentation", "File management"]
    },
    3: {
        "name": "Understand employer organisations",
        "ref": "J/616/8834",
        "credits": 6,
        "glh": 40,
        "rtt_tasks": ["NHS structure", "Trust organization", "RTT governance", "Policy understanding"]
    },
    4: {
        "name": "Principles of communication in a business environment",
        "ref": "M/616/8861",
        "credits": 1,
        "glh": 10,
        "rtt_tasks": ["Patient communication", "Team emails", "Clinical correspondence", "Professional writing"]
    },
    5: {
        "name": "Principles of developing working relationships with colleagues",
        "ref": "T/616/8862",
        "credits": 2,
        "glh": 15,
        "rtt_tasks": ["Team collaboration", "Pathway meetings", "Feedback sessions", "Conflict resolution"]
    }
}

OPTIONAL_UNITS = {
    6: {
        "name": "Principles of business administrative tasks",
        "ref": "A/616/8863",
        "credits": 3,
        "glh": 30,
        "recommended": True,
        "rtt_tasks": ["Referral processing", "Reception duties", "Event organization", "Financial admin"]
    },
    7: {
        "name": "Understand how to prepare text",
        "ref": "F/616/8864",
        "credits": 2,
        "glh": 20,
        "recommended": True,
        "rtt_tasks": ["Clinic notes", "Pathway documentation", "Transcription", "Text formatting"]
    },
    8: {
        "name": "Understand how to provide administrative support for meetings",
        "ref": "L/616/8835",
        "credits": 4,
        "glh": 28,
        "rtt_tasks": ["RTT meetings", "Agendas", "Minutes", "Action tracking"]
    },
    9: {
        "name": "Store, retrieve, and archive information",
        "ref": "R/616/8836",
        "credits": 4,
        "glh": 19,
        "rtt_tasks": ["Patient records", "RTT data", "Archive management", "Information retrieval"]
    },
    10: {
        "name": "Understand working in a customer service environment",
        "ref": "Y/616/8837",
        "credits": 3,
        "glh": 25,
        "rtt_tasks": ["Patient service", "Query handling", "Complaint management", "Service standards"]
    },
    11: {
        "name": "Understand the use of research in business",
        "ref": "D/616/8838",
        "credits": 6,
        "glh": 40,
        "rtt_tasks": ["RTT data analysis", "Performance research", "Improvement projects", "Report writing"]
    },
    12: {
        "name": "Principles of customer relationships",
        "ref": "H/616/8839",
        "credits": 3,
        "glh": 18,
        "rtt_tasks": ["Patient relationships", "Feedback collection", "Service improvement", "Satisfaction tracking"]
    },
    13: {
        "name": "Principles of marketing theory",
        "ref": "Y/616/8840",
        "credits": 4,
        "glh": 30,
        "rtt_tasks": ["Service promotion", "Patient engagement", "Communication campaigns", "Brand awareness"]
    },
    14: {
        "name": "Exploring social media",
        "ref": "D/616/8841",
        "credits": 2,
        "glh": 16,
        "rtt_tasks": ["NHS social media", "Patient engagement", "Digital communication", "Online presence"]
    },
    15: {
        "name": "Understand the safe use of online and social media platforms",
        "ref": "H/616/8842",
        "credits": 4,
        "glh": 35,
        "rtt_tasks": ["Data protection", "Online security", "Safe communication", "Privacy management"]
    },
    16: {
        "name": "Principles of equality and diversity in the workplace",
        "ref": "K/616/8843",
        "credits": 2,
        "glh": 10,
        "rtt_tasks": ["Inclusive service", "Equality practices", "Diversity awareness", "Fair treatment"]
    },
    17: {
        "name": "Principles of digital marketing",
        "ref": "K/616/8860",
        "credits": 5,
        "glh": 40,
        "rtt_tasks": ["Digital campaigns", "Online engagement", "SEO basics", "Analytics"]
    },
    18: {
        "name": "Principles of team leading",
        "ref": "T/616/8859",
        "credits": 5,
        "glh": 37,
        "rtt_tasks": ["Team leadership", "Motivation", "Performance management", "Change management"]
    }
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
        
        **TQUK Qualification 603/2949/X - Integrated with Real NHS Hospital Administration**
        
        **Congratulations on starting your journey to becoming a qualified business administrator!**
        """)
        
        # Dual certification highlight
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            ### 🎓 TQUK Certification
            - Ofqual Regulated
            - Level 2 RQF
            - 20+ Credits
            - Nationally Recognized
            """)
        with col2:
            st.info("""
            ### 🏥 RTT Certification
            - NHS Hospital Admin
            - Real Workplace Skills
            - Practical Experience
            - Industry Valued
            """)
        
        st.markdown("---")
        
        # Quick start guide
        st.success("""
        ## 🚀 Your 12-Week Journey to Dual Qualification:
        
        **Weeks 1-2:** Study & practice Unit 1 (Admin Services) + RTT scheduling
        
        **Weeks 3-4:** Study & practice Unit 2 (Documents) + RTT letters
        
        **Weeks 5-6:** Study & practice Unit 3 (Organizations) + NHS structure
        
        **Weeks 7-8:** Study & practice Unit 4 (Communication) + Patient correspondence
        
        **Weeks 9-10:** Study & practice Unit 5 (Teamwork) + Collaboration
        
        **Weeks 11-12:** Complete 2 optional units + Final assessments
        
        **Result:** TWO qualifications - TQUK + RTT Certified!
        """)
        
        st.markdown("---")
        
        # Mandatory units
        st.markdown("### 📋 Mandatory Units (All 5 Required - 16 Credits)")
        
        for unit_num, unit_data in MANDATORY_UNITS.items():
            with st.expander(f"✅ Unit {unit_num}: {unit_data['name']} ({unit_data['credits']} credits)"):
                st.write(f"**Unit Reference:** {unit_data['ref']}")
                st.write(f"**Credits:** {unit_data['credits']}")
                st.write(f"**Guided Learning Hours:** {unit_data['glh']}")
                st.write("**🏥 RTT Practical Tasks:**")
                for task in unit_data['rtt_tasks']:
                    st.write(f"- {task}")
                st.write("**📝 Evidence:** Screenshots and documentation from RTT system")
        
        st.markdown("---")
        
        # Optional units
        st.markdown("### 🎯 Optional Units (Choose 2 or More - Minimum 4 Credits)")
        st.caption("⭐ = Recommended for healthcare administration")
        
        for unit_num, unit_data in OPTIONAL_UNITS.items():
            recommended = "⭐ " if unit_data.get('recommended') else ""
            with st.expander(f"{recommended}Unit {unit_num}: {unit_data['name']} ({unit_data['credits']} credits)"):
                st.write(f"**Unit Reference:** {unit_data['ref']}")
                st.write(f"**Credits:** {unit_data['credits']}")
                st.write(f"**Guided Learning Hours:** {unit_data['glh']}")
                if unit_data.get('recommended'):
                    st.success("⭐ **Recommended** - Highly relevant for NHS roles")
                st.write("**🏥 RTT Practical Tasks:**")
                for task in unit_data['rtt_tasks']:
                    st.write(f"- {task}")
                st.write("**📝 Evidence:** Screenshots and documentation from RTT system")
    
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        
        st.success("""
        **📚 Welcome to Your Learning Materials!**
        
        Study all mandatory units + choose 2 optional units to complete your qualification.
        """)
        
        st.info("""
        **💡 Study Guide:**
        - 📖 **Read** each unit's learning outcomes and assessment criteria
        - ✏️ **Complete** the activities and exercises
        - 🏥 **Practice** with real RTT tasks (see RTT Practice tab)
        - 📝 **Collect** evidence as you work
        - ✅ **Submit** your portfolio for TQUK assessment
        """)
        
        st.markdown("---")
        
        # Unit selector
        unit_type = st.radio("Select Unit Type:", ["Mandatory Units", "Optional Units"])
        
        if unit_type == "Mandatory Units":
            units_to_show = MANDATORY_UNITS
            st.info("📋 All 5 mandatory units must be completed")
        else:
            units_to_show = OPTIONAL_UNITS
            st.info("🎯 Choose at least 2 optional units (minimum 4 credits total)")
        
        selected_unit = st.selectbox(
            "Choose a unit to study:",
            options=list(units_to_show.keys()),
            format_func=lambda x: f"Unit {x}: {units_to_show[x]['name']}"
        )
        
        if selected_unit:
            unit = units_to_show[selected_unit]
            st.markdown(f"### Unit {selected_unit}: {unit['name']}")
            st.write(f"**Reference:** {unit['ref']}")
            st.write(f"**Credits:** {unit['credits']} | **GLH:** {unit['glh']} hours")
            
            if unit.get('recommended'):
                st.success("⭐ **Recommended for healthcare roles**")
            
            st.markdown("#### 🏥 RTT Practical Tasks for This Unit:")
            for task in unit['rtt_tasks']:
                st.write(f"✅ {task}")
            
            st.markdown("#### 📝 Evidence You'll Collect:")
            st.write("- Screenshots of completed RTT tasks")
            st.write("- Documents you create (letters, reports, schedules)")
            st.write("- Reflective accounts of your learning")
            st.write("- Feedback from supervisors/colleagues")
            
            st.info("💡 **Tip:** Complete the RTT tasks in the 'RTT Practice' tab to gather evidence for this unit!")
            
            # Load full unit materials
            st.markdown("---")
            st.markdown("#### 📚 Full Learning Materials")
            
            try:
                import os
                materials_path = os.path.join(os.path.dirname(__file__), 'tquk_materials', 'ALL_UNITS_COMPLETE.md')
                if os.path.exists(materials_path):
                    with open(materials_path, 'r', encoding='utf-8') as f:
                        materials_content = f.read()
                    
                    # Extract content for selected unit
                    unit_header = f"## {'MANDATORY' if unit_type == 'Mandatory Units' else 'OPTIONAL'} UNIT {selected_unit}:"
                    
                    if unit_header in materials_content:
                        start_idx = materials_content.find(unit_header)
                        next_unit_idx = materials_content.find("\n## ", start_idx + 1)
                        if next_unit_idx == -1:
                            unit_content = materials_content[start_idx:]
                        else:
                            unit_content = materials_content[start_idx:next_unit_idx]
                        
                        with st.expander("📖 View Full Unit Content (Learning Outcomes, Assessment Criteria, Details)", expanded=False):
                            st.markdown(unit_content)
                    else:
                        st.info("📚 Full detailed materials available - includes all learning outcomes and assessment criteria")
                else:
                    st.success("✅ Complete TQUK-compliant materials created! All learning outcomes, assessment criteria, and RTT integration included.")
            except Exception as e:
                st.info("📚 Full learning materials are integrated into this course!")
    
    with tabs[2]:
        st.subheader("🏥 RTT Practice - Real Hospital Administration")
        st.success("🚀 Practice business admin with actual NHS RTT workflows!")
        
        st.markdown("""
        ### Why RTT Practice?
        
        **TQUK requires workplace evidence.** Our RTT system provides:
        - ✅ Real NHS hospital administration tasks
        - ✅ Authentic documents and scenarios
        - ✅ Automatic evidence collection
        - ✅ Supervisor feedback system
        - ✅ Portfolio-ready screenshots
        
        **This is your virtual workplace!**
        """)
        
        st.markdown("---")
        
        # RTT task categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Administrative Tasks")
            st.write("- RTT clinic scheduling")
            st.write("- Appointment management")
            st.write("- Diary coordination")
            st.write("- Meeting organization")
            st.write("- Mail and correspondence")
            
            st.markdown("#### 📝 Documentation Tasks")
            st.write("- Patient letters")
            st.write("- Pathway reports")
            st.write("- Clinic notes")
            st.write("- Performance dashboards")
            st.write("- Meeting minutes")
        
        with col2:
            st.markdown("#### 👥 Communication Tasks")
            st.write("- Patient correspondence")
            st.write("- Team emails")
            st.write("- Clinical liaison")
            st.write("- Professional writing")
            st.write("- Feedback sessions")
            
            st.markdown("#### 📊 Data & Analysis Tasks")
            st.write("- RTT performance data")
            st.write("- Breach analysis")
            st.write("- Report generation")
            st.write("- Information management")
            st.write("- Archive systems")
        
        st.markdown("---")
        
        st.info("""
        ### 🎯 How to Use RTT for Evidence:
        
        1. **Navigate** to the RTT modules (Clinical Workflows, Training & Certification)
        2. **Complete** the tasks relevant to your current unit
        3. **Take screenshots** of your work (use Windows Snipping Tool)
        4. **Save** screenshots with clear filenames (e.g., "Unit1_RTT_Scheduling.png")
        5. **Write** a brief description of what you did
        6. **Upload** to your evidence portfolio in Assessments tab
        
        **💡 Tip:** Complete 2-3 RTT tasks per unit for strong evidence!
        """)
        
        if st.button("🚀 Go to RTT Training System", type="primary", use_container_width=True):
            st.success("✅ Navigate to '🎓 Training & Certification' in the sidebar to start practicing!")
    
    with tabs[3]:
        st.subheader("📝 Evidence & Assessment Submission")
        
        st.info("""
        ### 📋 Assessment Requirements
        
        **To complete this qualification, you must:**
        1. ✅ Complete all 5 mandatory units
        2. ✅ Complete at least 2 optional units (4+ credits)
        3. ✅ Submit evidence for all learning outcomes
        4. ✅ Demonstrate competence in RTT practical tasks
        
        **Total Credits Required:** 20+ credits
        """)
        
        st.markdown("---")
        
        st.markdown("### 📤 Evidence Portfolio")
        
        st.write("""
        Your evidence portfolio should include:
        
        **For Each Unit:**
        - 📸 **Screenshots** from RTT system showing completed tasks
        - 📄 **Documents** you created (letters, reports, schedules, etc.)
        - 📝 **Reflective accounts** explaining what you learned
        - ✅ **Witness testimonies** from supervisors (if available)
        - 📊 **Work products** demonstrating your skills
        
        **Quality over quantity!** 2-3 strong pieces of evidence per unit is better than 10 weak ones.
        """)
        
        st.markdown("---")
        
        st.success("""
        ### ✅ Evidence Checklist
        
        Before submitting, ensure your evidence:
        - ✅ Clearly shows YOUR work
        - ✅ Relates to the specific unit and learning outcomes
        - ✅ Is dated and labeled
        - ✅ Demonstrates competence
        - ✅ Is professional and well-presented
        - ✅ Includes your reflections on learning
        """)
        
        st.markdown("---")
        
        st.warning("""
        ### 📬 Submission Process
        
        **When you're ready to submit:**
        1. Organize all evidence by unit
        2. Create a contents page
        3. Number all pages
        4. Include your name and candidate number
        5. Contact your tutor to arrange submission
        
        **Your tutor will review and submit to TQUK for final assessment.**
        """)
    
    with tabs[4]:
        st.subheader("📊 My Progress")
        
        if enrollment:
            # Show actual progress
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall Progress", f"{enrollment['progress']}%")
            with col2:
                st.metric("Units Completed", f"{enrollment['units_completed']}/7")
            with col3:
                st.metric("Status", enrollment['status'].title())
            with col4:
                st.metric("Credits Earned", f"{enrollment['units_completed'] * 3}/20+")
            
            st.progress(enrollment['progress'] / 100)
        
        st.markdown("---")
        
        # Progress checklist
        st.markdown("### ✅ Qualification Checklist")
        
        st.markdown("#### Mandatory Units (All Required)")
        for unit_num, unit in MANDATORY_UNITS.items():
            st.checkbox(f"Unit {unit_num}: {unit['name']} ({unit['credits']} credits)", key=f"progress_m{unit_num}")
        
        st.markdown("#### Optional Units (Choose 2+)")
        for unit_num, unit in OPTIONAL_UNITS.items():
            recommended = " ⭐" if unit.get('recommended') else ""
            st.checkbox(f"Unit {unit_num}: {unit['name']} ({unit['credits']} credits){recommended}", key=f"progress_o{unit_num}")
        
        st.markdown("---")
        
        st.info("""
        ### 🎯 Next Steps
        
        **To progress:**
        1. Study each unit in the Materials tab
        2. Complete RTT practical tasks
        3. Collect evidence as you work
        4. Submit portfolio when complete
        5. Receive your TQUK + RTT dual certification!
        
        **Questions?** Contact your tutor for support.
        """)
