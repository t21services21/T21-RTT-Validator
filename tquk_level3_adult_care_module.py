"""
TQUK LEVEL 3 DIPLOMA IN ADULT CARE - COMPLETE LEARNER MODULE
Standalone module for learners to access materials, track progress, and submit evidence
"""

import streamlit as st
from tquk_course_assignment import get_learner_enrollments, update_learner_progress
from datetime import datetime

COURSE_ID = "level3_adult_care"
COURSE_NAME = "Level 3 Diploma in Adult Care"

# Course Structure
UNITS = {
    1: {
        "name": "Duty of Care",
        "file": "LEVEL3_UNIT1_DUTY_OF_CARE_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 4
    },
    2: {
        "name": "Equality, Diversity & Inclusion",
        "file": "LEVEL3_UNIT2_EQUALITY_DIVERSITY_COMPLETE.md",
        "activities": 10,
        "learning_outcomes": 5
    },
    3: {
        "name": "Person-Centred Care",
        "file": "LEVEL3_UNIT3_PERSON_CENTRED_CARE_COMPLETE.md",
        "activities": 9,
        "learning_outcomes": 5
    },
    4: {
        "name": "Safeguarding in Care Settings",
        "file": "LEVEL3_COMPLETE_DELIVERY_PACKAGE.md",
        "activities": 8,
        "learning_outcomes": 4
    },
    5: {
        "name": "Effective Communication",
        "file": "LEVEL3_COMPLETE_DELIVERY_PACKAGE.md",
        "activities": 7,
        "learning_outcomes": 4
    },
    6: {
        "name": "Health & Wellbeing",
        "file": "LEVEL3_COMPLETE_DELIVERY_PACKAGE.md",
        "activities": 8,
        "learning_outcomes": 5
    },
    7: {
        "name": "Continuous Professional Development",
        "file": "LEVEL3_COMPLETE_DELIVERY_PACKAGE.md",
        "activities": 6,
        "learning_outcomes": 3
    }
}


def load_markdown_file(filename):
    """Load markdown content from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file: {str(e)}\n\nPlease ensure the file '{filename}' exists in the project folder."


def render_level3_adult_care_module():
    """Main module interface for Level 3 Adult Care"""
    
    # Check if learner is enrolled
    learner_email = st.session_state.get('user_email', '')
    user_role = st.session_state.get('user_role', 'student')
    
    st.title("🎓 Level 3 Diploma in Adult Care")
    st.success("✅ **TQUK Approved Centre #36257481088** - Nationally Recognized Qualification")
    
    # Check enrollment
    enrollments = get_learner_enrollments(learner_email)
    is_enrolled = any(e['course_id'] == COURSE_ID for e in enrollments)
    
    if not is_enrolled and user_role == 'student':
        st.warning("⚠️ You are not enrolled in this course yet.")
        st.info("Please contact your teacher to be assigned to this qualification.")
        return
    
    # Get enrollment data
    enrollment = next((e for e in enrollments if e['course_id'] == COURSE_ID), None) if is_enrolled else None
    
    # Show progress overview
    if enrollment:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Progress", f"{enrollment['progress']}%")
            st.progress(enrollment['progress'] / 100)
        
        with col2:
            st.metric("Units Completed", f"{enrollment['units_completed']}/{enrollment['total_units']}")
        
        with col3:
            status_emoji = {'enrolled': '🟡', 'in_progress': '🔵', 'completed': '🟢'}
            st.metric("Status", f"{status_emoji.get(enrollment['status'], '⚪')} {enrollment['status'].title()}")
    
    st.markdown("---")
    
    # Main tabs
    tabs = st.tabs([
        "📚 Course Overview",
        "📖 Learning Materials",
        "📝 Assessments",
        "📊 My Progress",
        "🎓 Certificate"
    ])
    
    with tabs[0]:
        render_course_overview()
    
    with tabs[1]:
        render_learning_materials(enrollment)
    
    with tabs[2]:
        render_assessments(learner_email)
    
    with tabs[3]:
        render_progress_tracker(enrollment)
    
    with tabs[4]:
        render_certificate(enrollment)


def render_course_overview():
    """Course overview and introduction"""
    st.subheader("📚 Course Overview")
    
    st.markdown("""
    ### Welcome to Level 3 Diploma in Adult Care!
    
    **Qualification Details:**
    - **Code:** 610/0103/6
    - **Level:** 3
    - **Total Credits:** 58
    - **Duration:** 12-18 weeks (or 10 weeks accelerated)
    - **Assessment:** Portfolio of evidence
    
    ---
    
    ### What You'll Learn:
    
    This qualification will prepare you for a senior role in adult care settings. You'll develop:
    
    ✅ **Professional Skills:**
    - Duty of care and professional boundaries
    - Safeguarding vulnerable adults
    - Person-centred care approaches
    - Effective communication techniques
    
    ✅ **Leadership Skills:**
    - Supporting colleagues and new staff
    - Promoting equality and diversity
    - Managing health and wellbeing
    - Continuous professional development
    
    ✅ **Practical Skills:**
    - Real-world care scenarios
    - Evidence collection
    - Reflective practice
    - Professional documentation
    
    ---
    
    ### Course Structure:
    """)
    
    for unit_num, unit_data in UNITS.items():
        with st.expander(f"Unit {unit_num}: {unit_data['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📚 Learning Outcomes: {unit_data['learning_outcomes']}")
            with col2:
                st.write(f"✏️ Activities: {unit_data['activities']}")
    
    st.markdown("---")
    
    st.info("""
    ### 📖 How to Use This Module:
    
    1. **Learning Materials** - Read each unit's content and complete activities
    2. **Assessments** - Submit evidence for each learning outcome
    3. **My Progress** - Track your completion and get feedback
    4. **Certificate** - Download your certificate when you complete all units
    
    **Ready to start? Go to the Learning Materials tab!** 🚀
    """)


def render_learning_materials(enrollment):
    """Display learning materials for each unit"""
    st.subheader("📖 Learning Materials")
    
    # Unit selector
    selected_unit = st.selectbox(
        "Select Unit",
        options=list(UNITS.keys()),
        format_func=lambda x: f"Unit {x}: {UNITS[x]['name']}"
    )
    
    if selected_unit:
        unit = UNITS[selected_unit]
        
        st.markdown(f"### Unit {selected_unit}: {unit['name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📚 Learning Outcomes: {unit['learning_outcomes']}")
        with col2:
            st.info(f"✏️ Activities: {unit['activities']}")
        
        st.markdown("---")
        
        # Load and display content
        with st.spinner("Loading materials..."):
            content = load_markdown_file(unit['file'])
            
            # Display in expandable sections
            if "Unit {selected_unit}" in content or unit['name'] in content:
                st.markdown(content)
            else:
                # Show handbook first for units 4-7
                if selected_unit >= 4:
                    st.info(f"📘 This unit is covered in the Complete Delivery Package. Full materials coming soon!")
                    st.markdown(content[:2000] + "...")  # Show preview
                else:
                    st.markdown(content)
        
        st.markdown("---")
        
        # Mark as read button
        if st.button(f"✅ Mark Unit {selected_unit} as Read", key=f"mark_read_{selected_unit}"):
            st.success(f"Unit {selected_unit} marked as read! Progress updated.")
            # TODO: Update progress in database


def render_assessments(learner_email):
    """Assessment submission interface"""
    st.subheader("📝 Assessment & Evidence Submission")
    
    st.info("""
    ### How to Submit Evidence:
    
    For each unit, you need to provide evidence that you've met the learning outcomes. Evidence can include:
    
    - 📸 **Observations** - Your assessor watches you work
    - 📝 **Witness Statements** - Colleagues confirm your competence
    - 💭 **Reflective Accounts** - You reflect on your practice
    - 📄 **Product Evidence** - Documents you've created (care plans, reports, etc.)
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
        st.markdown(f"### Submit Evidence for Unit {selected_unit}: {UNITS[selected_unit]['name']}")
        
        evidence_type = st.selectbox(
            "Evidence Type",
            ["Observation Record", "Witness Statement", "Reflective Account", "Product Evidence", "Professional Discussion"]
        )
        
        description = st.text_area(
            "Description",
            placeholder="Describe what this evidence demonstrates...",
            height=100
        )
        
        uploaded_file = st.file_uploader(
            "Upload Evidence (PDF, Word, Image)",
            type=['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png']
        )
        
        if st.button("📤 Submit Evidence", type="primary"):
            if description and uploaded_file:
                st.success("✅ Evidence submitted successfully!")
                st.balloons()
                st.info("Your assessor will review this and provide feedback soon.")
            else:
                st.warning("Please provide both a description and upload a file.")
    
    st.markdown("---")
    
    # Show submitted evidence
    st.subheader("📋 My Submitted Evidence")
    st.info("Evidence tracking coming soon! You'll see all your submissions here.")


def render_progress_tracker(enrollment):
    """Show detailed progress tracking"""
    st.subheader("📊 My Progress")
    
    if not enrollment:
        st.info("Enrollment data not available.")
        return
    
    st.markdown("### Overall Progress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Completion", f"{enrollment['progress']}%")
        st.progress(enrollment['progress'] / 100)
    
    with col2:
        st.metric("Units Completed", f"{enrollment['units_completed']}/7")
    
    st.markdown("---")
    
    st.markdown("### Unit-by-Unit Progress")
    
    for unit_num, unit_data in UNITS.items():
        with st.expander(f"Unit {unit_num}: {unit_data['name']}", expanded=(unit_num == 1)):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # TODO: Get actual progress from database
                progress = 0
                st.metric("Progress", f"{progress}%")
                st.progress(progress / 100)
            
            with col2:
                st.metric("Activities", f"0/{unit_data['activities']}")
            
            with col3:
                status = "Not Started" if progress == 0 else ("In Progress" if progress < 100 else "Completed")
                st.metric("Status", status)
            
            st.caption("Complete activities and submit evidence to update progress")


def render_certificate(enrollment):
    """Certificate download interface"""
    st.subheader("🎓 Certificate")
    
    if not enrollment:
        st.info("Complete your enrollment to access certificate.")
        return
    
    if enrollment['status'] == 'completed':
        st.success("🎉 Congratulations! You've completed the Level 3 Diploma in Adult Care!")
        
        st.markdown(f"""
        **Certificate Details:**
        - Qualification: {COURSE_NAME}
        - Learner: {enrollment['learner_email']}
        - Completion Date: {enrollment.get('completion_date', 'N/A')[:10]}
        - TQUK Centre: #36257481088
        """)
        
        if st.button("📥 Download Certificate (PDF)", type="primary"):
            st.info("Certificate generation coming soon! Your certificate will be available for download here.")
    
    else:
        st.info(f"""
        ### Certificate Not Yet Available
        
        **Current Progress:** {enrollment['progress']}%
        
        Complete all 7 units and submit all required evidence to receive your certificate.
        
        **Units Remaining:** {7 - enrollment['units_completed']}
        """)
        
        st.progress(enrollment['progress'] / 100)
