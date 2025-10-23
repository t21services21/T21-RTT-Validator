"""
TQUK LEVEL 3 DIPLOMA IN ADULT CARE - COMPLETE LEARNER MODULE
Standalone module for learners to access materials, track progress, and submit evidence
VERSION: 2.0 - ALL 27 UNITS WITH FULL MATERIALS
"""

import streamlit as st
import os
from tquk_course_assignment import get_learner_enrollments, update_learner_progress
from tquk_pdf_converter import create_unit_pdf
from tquk_optional_units import render_optional_units_selector, calculate_total_credits
from tquk_evidence_tracking import render_evidence_tracking, render_evidence_submission_form
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
        "file": "LEVEL3_UNIT4_SAFEGUARDING_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 4
    },
    5: {
        "name": "Effective Communication",
        "file": "LEVEL3_UNIT5_COMMUNICATION_COMPLETE.md",
        "activities": 7,
        "learning_outcomes": 4
    },
    6: {
        "name": "Health & Wellbeing",
        "file": "LEVEL3_UNIT6_HEALTH_WELLBEING_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 5
    },
    7: {
        "name": "Continuous Professional Development",
        "file": "LEVEL3_UNIT7_PROFESSIONAL_DEVELOPMENT_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 3
    },
    # Optional Units (8-27)
    8: {
        "name": "Dementia Care",
        "file": "LEVEL3_UNIT8_DEMENTIA_CARE_COMPLETE.md",
        "activities": 10,
        "learning_outcomes": 6,
        "optional": True,
        "credits": 5
    },
    9: {
        "name": "Mental Health Awareness",
        "file": "LEVEL3_UNIT9_MENTAL_HEALTH_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 5,
        "optional": True,
        "credits": 4
    },
    10: {
        "name": "End of Life Care",
        "file": "LEVEL3_UNIT10_END_OF_LIFE_CARE_COMPLETE.md",
        "activities": 9,
        "learning_outcomes": 6,
        "optional": True,
        "credits": 5
    },
    11: {
        "name": "Medication Management",
        "file": "LEVEL3_UNIT11_MEDICATION_MANAGEMENT_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 5,
        "optional": True,
        "credits": 4
    },
    12: {
        "name": "Moving and Handling",
        "file": "LEVEL3_UNIT12_MOVING_HANDLING_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    13: {
        "name": "Infection Prevention and Control",
        "file": "LEVEL3_UNIT13_INFECTION_CONTROL_COMPLETE.md",
        "activities": 7,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    14: {
        "name": "Nutrition and Hydration",
        "file": "LEVEL3_UNIT14_NUTRITION_HYDRATION_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    15: {
        "name": "Personal Care",
        "file": "LEVEL3_UNIT15_PERSONAL_CARE_COMPLETE.md",
        "activities": 9,
        "learning_outcomes": 5,
        "optional": True,
        "credits": 4
    },
    16: {
        "name": "Supporting Independence",
        "file": "LEVEL3_UNIT16_SUPPORTING_INDEPENDENCE_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 5,
        "optional": True,
        "credits": 4
    },
    17: {
        "name": "Working in Partnership",
        "file": "LEVEL3_UNIT17_WORKING_PARTNERSHIP_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    18: {
        "name": "Dignity and Privacy",
        "file": "LEVEL3_UNIT18_DIGNITY_PRIVACY_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    19: {
        "name": "Safeguarding Vulnerable Adults",
        "file": "LEVEL3_UNIT19_SAFEGUARDING_VULNERABLE_ADULTS_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 5,
        "optional": True,
        "credits": 4
    },
    20: {
        "name": "Learning Disabilities Support",
        "file": "LEVEL3_UNIT20_LEARNING_DISABILITIES_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 5,
        "optional": True,
        "credits": 4
    },
    21: {
        "name": "Autism Awareness",
        "file": "LEVEL3_UNIT21_AUTISM_AWARENESS_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    22: {
        "name": "Stroke Care",
        "file": "LEVEL3_UNIT22_STROKE_CARE_COMPLETE.md",
        "activities": 8,
        "learning_outcomes": 5,
        "optional": True,
        "credits": 4
    },
    23: {
        "name": "Diabetes Care",
        "file": "LEVEL3_UNIT23_DIABETES_CARE_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    24: {
        "name": "Continence Care",
        "file": "LEVEL3_UNIT24_CONTINENCE_CARE_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    25: {
        "name": "Falls Prevention",
        "file": "LEVEL3_UNIT25_FALLS_PREVENTION_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    26: {
        "name": "Pressure Area Care",
        "file": "LEVEL3_UNIT26_PRESSURE_AREA_CARE_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
    },
    27: {
        "name": "Sensory Loss Support",
        "file": "LEVEL3_UNIT27_SENSORY_LOSS_COMPLETE.md",
        "activities": 6,
        "learning_outcomes": 4,
        "optional": True,
        "credits": 3
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
    
    # Get user role - check multiple possible locations
    user_role = 'student'  # Default
    if hasattr(st.session_state, 'user_license') and hasattr(st.session_state.user_license, 'role'):
        user_role = st.session_state.user_license.role
    elif 'user_role' in st.session_state:
        user_role = st.session_state.user_role
    elif 'user_type' in st.session_state:
        user_role = st.session_state.user_type
    
    # Check if admin email
    if learner_email and 'admin@t21services' in learner_email.lower():
        user_role = 'super_admin'
    
    st.title("🎓 Level 3 Diploma in Adult Care")
    st.success("✅ **TQUK Approved Centre #36257481088** - Nationally Recognized Qualification")
    
    # Check enrollment (bypass for admins, teachers, testers, staff)
    admin_roles = ['super_admin', 'admin', 'teacher', 'tester', 'staff', 'instructor', 'trainer']
    
    enrollments = get_learner_enrollments(learner_email)
    is_enrolled = any(e['course_id'] == COURSE_ID for e in enrollments)
    
    # Only students need to be enrolled
    if not is_enrolled and user_role not in admin_roles:
        st.warning("⚠️ You are not enrolled in this course yet.")
        st.info("Please contact your teacher to be assigned to this qualification.")
        return
    
    # For admins/staff viewing without enrollment, show info message
    if not is_enrolled and user_role in admin_roles:
        st.info("👨‍💼 **Admin/Staff View** - You have full access to preview this course. Students must be enrolled to access.")
    
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
        "🎯 Optional Units",
        "📝 Assessments",
        "📋 Evidence Tracking",
        "📊 My Progress",
        "🎓 Certificate"
    ])
    
    with tabs[0]:
        render_course_overview()
    
    with tabs[1]:
        render_learning_materials(enrollment)
    
    with tabs[2]:
        # Optional Units Selection and Content
        render_optional_units_selector(learner_email, COURSE_ID, required_credits=58, mandatory_credits=24)
        
        st.markdown("---")
        st.markdown("---")
        
        # Show learning materials for selected optional units
        from tquk_optional_units import render_optional_units_content
        render_optional_units_content(learner_email, COURSE_ID, UNITS)
    
    with tabs[3]:
        render_assessments(learner_email)
    
    with tabs[4]:
        # Evidence Tracking
        render_evidence_tracking(learner_email, COURSE_ID)
    
    with tabs[5]:
        render_progress_tracker(enrollment)
    
    with tabs[6]:
        render_certificate(enrollment)


def render_course_overview():
    """Display course overview and structure"""
    st.subheader("📚 Course Overview")
    
    # Welcome banner
    st.success("""
    # 🎓 Welcome to Level 3 Diploma in Adult Care!
    
    **Congratulations on starting your journey to becoming a qualified adult care professional!**
    """)
    
    # Quick start guide
    st.info("""
    ## 🚀 Quick Start Guide - Your Journey to Qualification:
    
    **Step 1:** 📖 Study the 7 mandatory units (Learning Materials tab)
    
    **Step 2:** 🎯 Choose 34 credits from 20 optional units (Optional Units tab)
    
    **Step 3:** 📝 Submit evidence for all units (Assessments tab)
    
    **Step 4:** 📊 Track your progress (My Progress tab)
    
    **Step 5:** 🎓 Download your certificate when complete!
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 📋 Qualification Details:
    - **Code:** 610/0103/6
    - **Level:** 3
    - **Total Credits:** 58 (24 mandatory + 34 optional)
    - **Duration:** 12-18 months
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
    st.subheader("📖 Learning Materials - Mandatory Units")
    
    st.success("""
    **📚 Welcome to Your Learning Materials!**
    
    This tab contains the **7 mandatory units** that all students must complete.
    Click through the tabs below to study each unit.
    """)
    
    st.info("""
    **💡 Quick Guide:**
    - 📖 **Read** the full content for each unit
    - ✏️ **Complete** the activities and case studies
    - 📥 **Download** as PDF to study offline
    - 📝 **Submit** evidence in the Assessments tab
    
    **For optional units:** Go to the "🎯 Optional Units" tab!
    """)
    
    # Progress indicator
    if enrollment:
        progress_text = f"Overall Progress: {enrollment['progress']}% | Units: {enrollment['units_completed']}/27"
        st.progress(enrollment['progress'] / 100, text=progress_text)
        st.markdown("---")
    
    # Separate mandatory and optional units
    mandatory_units = {k: v for k, v in UNITS.items() if k <= 7}
    optional_units = {k: v for k, v in UNITS.items() if k > 7}
    
    # Create two sections
    st.markdown("### 📚 Mandatory Units (1-7)")
    st.info("These units are required for all students.")
    
    # Mandatory unit tabs
    mandatory_tabs = st.tabs([f"Unit {i}: {UNITS[i]['name']}" for i in mandatory_units.keys()])
    
    for idx, (unit_num, unit_data) in enumerate(mandatory_units.items()):
        with mandatory_tabs[idx]:
            # Unit header
            st.markdown(f"## 📚 Unit {unit_num}: {unit_data['name']}")
            
            # Unit info cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Learning Outcomes", unit_data['learning_outcomes'])
            with col2:
                st.metric("Activities", unit_data['activities'])
            with col3:
                # Check if unit is completed
                status = "✅ Complete" if enrollment and enrollment['units_completed'] >= unit_num else "📖 In Progress"
                st.metric("Status", status)
            
            st.markdown("---")
            
            # Load and display content beautifully
            try:
                content = load_markdown_file(unit_data['file'])
                
                if content and not content.startswith("Error"):
                    # Create a container for better formatting
                    with st.container():
                        # Display content with proper markdown rendering
                        st.markdown(content, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Interactive elements
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"✅ Mark Unit {unit_num} Complete", key=f"complete_{unit_num}", type="primary"):
                            st.success(f"✅ Unit {unit_num} marked as complete!")
                            st.balloons()
                            # TODO: Update database
                    
                    with col2:
                        if st.button(f"📝 Go to Assessment", key=f"assess_{unit_num}"):
                            st.info("Switch to the 'Assessments' tab to submit your evidence!")
                    
                    # Download option - Convert to PDF
                    try:
                        pdf_buffer = create_unit_pdf(unit_num, unit_data['name'], content)
                        st.download_button(
                            label=f"📥 Download Unit {unit_num} as PDF",
                            data=pdf_buffer,
                            file_name=f"Level3_Unit{unit_num}_{unit_data['name'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            help="Download professional PDF document",
                            key=f"download_{unit_num}",
                            type="primary"
                        )
                    except Exception as e:
                        st.error(f"PDF generation error: {str(e)}")
                        # Fallback to markdown
                        st.download_button(
                            label=f"📥 Download Unit {unit_num} (Markdown)",
                            data=content,
                            file_name=f"Level3_Unit{unit_num}_{unit_data['name'].replace(' ', '_')}.md",
                            mime="text/markdown",
                            key=f"download_md_{unit_num}"
                        )
                    
                else:
                    st.warning(f"⚠️ Materials for Unit {unit_num} are being prepared.")
                    st.info("""
                    **What's included in this unit:**
                    - Learning outcomes and assessment criteria
                    - Real-world scenarios and case studies
                    - Activities and reflective exercises
                    - Assessment guidance
                    
                    Full materials will be available soon!
                    """)
                    
            except Exception as e:
                st.error(f"Error loading materials: {str(e)}")
                st.info("Please contact your teacher if this persists.")
    


def render_assessments(learner_email):
    """Assessment submission interface"""
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
    - 📄 **Product Evidence** - Documents you've created (care plans, reports, etc.)
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
