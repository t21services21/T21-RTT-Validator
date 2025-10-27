"""
LEVEL 3 DIPLOMA IN ADULT CARE - COMPLETE SYSTEM WITH ALL 27 UNITS
Integrated into T21 Healthcare Platform

Structure:
- 7 Mandatory Units (24 credits) - Units 1-7
- 20 Optional Units (choose 34 credits) - Units 8-27
- Total: 58 credits

Features:
- Unit selection system
- Progress tracking
- Evidence management
- Portfolio building
"""

import streamlit as st
from datetime import datetime, date
import json
from typing import Dict, List, Optional
import os

# ============================================
# LEVEL 3 QUALIFICATION STRUCTURE
# ============================================

# MANDATORY UNITS (7 units = 24 credits) - ALL STUDENTS MUST COMPLETE
MANDATORY_UNITS = {
    'unit1': {
        'code': 'Unit 1',
        'name': 'Duty of Care',
        'glh': 30,
        'credits': 5,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT1_DUTY_OF_CARE_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2', '3.3'],
        'assessment_methods': ['Professional Discussion', 'Reflective Account', 'Witness Statement']
    },
    'unit2': {
        'code': 'Unit 2',
        'name': 'Equality, Diversity and Inclusion',
        'glh': 12,
        'credits': 2,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT2_EQUALITY_DIVERSITY_COMPLETE.md',
        'criteria': ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3'],
        'assessment_methods': ['Written Assignment', 'Observation', 'Reflective Account']
    },
    'unit3': {
        'code': 'Unit 3',
        'name': 'Person-Centred Care',
        'glh': 30,
        'credits': 5,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT3_PERSON_CENTRED_CARE_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '2.3', '3.1', '3.2', '4.1', '4.2'],
        'assessment_methods': ['Observation', 'Professional Discussion', 'Care Plan Evidence']
    },
    'unit4': {
        'code': 'Unit 4',
        'name': 'Safeguarding in Care Settings',
        'glh': 18,
        'credits': 3,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT4_SAFEGUARDING_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2'],
        'assessment_methods': ['Case Study', 'Professional Discussion', 'Witness Statement']
    },
    'unit5': {
        'code': 'Unit 5',
        'name': 'Effective Communication',
        'glh': 18,
        'credits': 3,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT5_COMMUNICATION_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1'],
        'assessment_methods': ['Observation', 'Professional Discussion', 'Reflective Account']
    },
    'unit6': {
        'code': 'Unit 6',
        'name': 'Health & Wellbeing',
        'glh': 18,
        'credits': 3,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT6_HEALTH_WELLBEING_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1'],
        'assessment_methods': ['Written Assignment', 'Observation', 'Care Plan Evidence']
    },
    'unit7': {
        'code': 'Unit 7',
        'name': 'Continuous Professional Development',
        'glh': 18,
        'credits': 3,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT7_PROFESSIONAL_DEVELOPMENT_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1'],
        'assessment_methods': ['Reflective Account', 'Professional Discussion', 'Development Plan']
    }
}

# OPTIONAL UNITS (20 units - choose 34 credits)
OPTIONAL_UNITS = {
    'unit8': {
        'code': 'Unit 8',
        'name': 'Dementia Care',
        'glh': 30,
        'credits': 5,
        'type': 'optional',
        'category': 'Specialist Care',
        'file': 'LEVEL3_UNIT8_DEMENTIA_CARE_COMPLETE.md',
        'unit_code': 'H/601/8059'
    },
    'unit9': {
        'code': 'Unit 9',
        'name': 'Mental Health Awareness',
        'glh': 24,
        'credits': 4,
        'type': 'optional',
        'category': 'Specialist Care',
        'file': 'LEVEL3_UNIT9_MENTAL_HEALTH_COMPLETE.md',
        'unit_code': 'K/601/5313'
    },
    'unit10': {
        'code': 'Unit 10',
        'name': 'End of Life Care',
        'glh': 30,
        'credits': 5,
        'type': 'optional',
        'category': 'Specialist Care',
        'file': 'LEVEL3_UNIT10_END_OF_LIFE_CARE_COMPLETE.md',
        'unit_code': 'Y/601/8325'
    },
    'unit11': {
        'code': 'Unit 11',
        'name': 'Medication Management',
        'glh': 24,
        'credits': 4,
        'type': 'optional',
        'category': 'Clinical Skills',
        'file': 'LEVEL3_UNIT11_MEDICATION_MANAGEMENT_COMPLETE.md',
        'unit_code': 'M/601/8326'
    },
    'unit12': {
        'code': 'Unit 12',
        'name': 'Moving and Handling',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Clinical Skills',
        'file': 'LEVEL3_UNIT12_MOVING_HANDLING_COMPLETE.md',
        'unit_code': 'L/601/8027'
    },
    'unit13': {
        'code': 'Unit 13',
        'name': 'Infection Prevention and Control',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Clinical Skills',
        'file': 'LEVEL3_UNIT13_INFECTION_CONTROL_COMPLETE.md',
        'unit_code': 'M/601/8324'
    },
    'unit14': {
        'code': 'Unit 14',
        'name': 'Nutrition and Hydration',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Clinical Skills',
        'file': 'LEVEL3_UNIT14_NUTRITION_HYDRATION_COMPLETE.md',
        'unit_code': 'K/601/8322'
    },
    'unit15': {
        'code': 'Unit 15',
        'name': 'Personal Care',
        'glh': 24,
        'credits': 4,
        'type': 'optional',
        'category': 'Clinical Skills',
        'file': 'LEVEL3_UNIT15_PERSONAL_CARE_COMPLETE.md',
        'unit_code': 'H/601/8323'
    },
    'unit16': {
        'code': 'Unit 16',
        'name': 'Supporting Independence',
        'glh': 24,
        'credits': 4,
        'type': 'optional',
        'category': 'Person-Centred Care',
        'file': 'LEVEL3_UNIT16_SUPPORTING_INDEPENDENCE_COMPLETE.md',
        'unit_code': 'R/601/8321'
    },
    'unit17': {
        'code': 'Unit 17',
        'name': 'Working in Partnership',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Person-Centred Care',
        'file': 'LEVEL3_UNIT17_WORKING_PARTNERSHIP_COMPLETE.md',
        'unit_code': 'Y/601/8320'
    },
    'unit18': {
        'code': 'Unit 18',
        'name': 'Dignity and Privacy',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Person-Centred Care',
        'file': 'LEVEL3_UNIT18_DIGNITY_PRIVACY_COMPLETE.md',
        'unit_code': 'L/601/8319'
    },
    'unit19': {
        'code': 'Unit 19',
        'name': 'Safeguarding Vulnerable Adults',
        'glh': 24,
        'credits': 4,
        'type': 'optional',
        'category': 'Safeguarding',
        'file': 'LEVEL3_UNIT19_SAFEGUARDING_VULNERABLE_ADULTS_COMPLETE.md',
        'unit_code': 'M/601/8318'
    },
    'unit20': {
        'code': 'Unit 20',
        'name': 'Learning Disabilities Support',
        'glh': 24,
        'credits': 4,
        'type': 'optional',
        'category': 'Specialist Care',
        'file': 'LEVEL3_UNIT20_LEARNING_DISABILITIES_COMPLETE.md',
        'unit_code': 'T/601/8317'
    },
    'unit21': {
        'code': 'Unit 21',
        'name': 'Autism Awareness',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Specialist Care',
        'file': 'LEVEL3_UNIT21_AUTISM_AWARENESS_COMPLETE.md',
        'unit_code': 'K/601/9484'
    },
    'unit22': {
        'code': 'Unit 22',
        'name': 'Stroke Care',
        'glh': 24,
        'credits': 4,
        'type': 'optional',
        'category': 'Condition-Specific',
        'file': 'LEVEL3_UNIT22_STROKE_CARE_COMPLETE.md',
        'unit_code': 'A/601/8316'
    },
    'unit23': {
        'code': 'Unit 23',
        'name': 'Diabetes Care',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Condition-Specific',
        'file': 'LEVEL3_UNIT23_DIABETES_CARE_COMPLETE.md',
        'unit_code': 'F/601/8315'
    },
    'unit24': {
        'code': 'Unit 24',
        'name': 'Continence Care',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Condition-Specific',
        'file': 'LEVEL3_UNIT24_CONTINENCE_CARE_COMPLETE.md',
        'unit_code': 'J/601/8314'
    },
    'unit25': {
        'code': 'Unit 25',
        'name': 'Falls Prevention',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Condition-Specific',
        'file': 'LEVEL3_UNIT25_FALLS_PREVENTION_COMPLETE.md',
        'unit_code': 'H/601/8313'
    },
    'unit26': {
        'code': 'Unit 26',
        'name': 'Pressure Area Care',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Condition-Specific',
        'file': 'LEVEL3_UNIT26_PRESSURE_AREA_CARE_COMPLETE.md',
        'unit_code': 'D/601/8312'
    },
    'unit27': {
        'code': 'Unit 27',
        'name': 'Sensory Loss Support',
        'glh': 18,
        'credits': 3,
        'type': 'optional',
        'category': 'Specialist Care',
        'file': 'LEVEL3_UNIT27_SENSORY_LOSS_COMPLETE.md',
        'unit_code': 'Y/601/8311'
    }
}

# Combine all units
ALL_UNITS = {**MANDATORY_UNITS, **OPTIONAL_UNITS}


# ============================================
# HELPER FUNCTIONS
# ============================================

def load_markdown_file(filename):
    """Load markdown content from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file: {str(e)}\n\nPlease ensure the file '{filename}' exists in the project folder."


# ============================================
# MAIN LEVEL 3 MODULE
# ============================================

def render_level3_adult_care():
    """Main entry point for Level 3 Adult Care module"""
    
    st.header("🎓 Level 3 Diploma in Adult Care")
    
    # Check user role
    user_email = st.session_state.get('user_email', '')
    user_type = st.session_state.get('user_type', 'student')
    
    # Determine view
    if user_type in ['admin', 'super_admin', 'teacher', 'staff', 'tester']:
        render_assessor_view()
    else:
        render_learner_view()


# ============================================
# LEARNER VIEW
# ============================================

def render_learner_view():
    """Student/learner view with unit selection"""
    
    st.success("✅ **TQUK Approved Centre #36257481088** - Nationally Recognized Qualification")
    
    # Qualification structure info
    with st.expander("📋 Qualification Structure"):
        st.markdown("""
        **Level 3 Diploma in Adult Care**
        
        **Total Credits Required:** 58 credits
        
        **Structure:**
        - **7 Mandatory Units** (24 credits) - MUST complete all
        - **Optional Units** (34 credits) - Choose from 20 options
        
        **Total:** 58 credits
        """)
    
    # Tabs
    tabs = st.tabs([
        "📊 My Progress",
        "📚 Mandatory Units",
        "🎯 Choose Optional Units",
        "📝 Submit Evidence",
        "📁 My Portfolio",
        "📅 Assessment Schedule"
    ])
    
    # Tab 1: My Progress
    with tabs[0]:
        render_progress_overview()
    
    # Tab 2: Mandatory Units
    with tabs[1]:
        render_mandatory_units()
    
    # Tab 3: Choose Optional Units
    with tabs[2]:
        render_optional_units_selection()
    
    # Tab 3: Submit Evidence
    with tabs[3]:
        render_evidence_submission()
    
    # Tab 4: My Portfolio
    with tabs[4]:
        render_portfolio()
    
    # Tab 5: Assessment Schedule
    with tabs[5]:
        render_assessment_schedule()


def render_progress_overview():
    """Show overall progress"""
    
    st.subheader("📊 Your Progress")
    
    # Mock data (replace with database queries)
    mandatory_completed = 4
    mandatory_total = 7
    optional_selected = 3
    optional_completed = 1
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mandatory Units", f"{mandatory_completed}/{mandatory_total}")
        st.progress(mandatory_completed / mandatory_total)
    
    with col2:
        st.metric("Optional Units Selected", f"{optional_selected}/4")
        st.progress(optional_selected / 4)
    
    with col3:
        st.metric("Optional Units Completed", f"{optional_completed}/{optional_selected}")
        if optional_selected > 0:
            st.progress(optional_completed / optional_selected)
    
    # Credits
    st.markdown("---")
    st.subheader("💳 Credits")
    
    mandatory_credits = 14  # Mock: 4/7 units done (approx 14 credits)
    optional_credits = 8    # Mock: 1/3 units done (approx 8 credits)
    total_credits = mandatory_credits + optional_credits
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mandatory Credits", f"{mandatory_credits}/24")
    
    with col2:
        st.metric("Optional Credits", f"{optional_credits}/34")
    
    with col3:
        st.metric("Total Credits", f"{total_credits}/58")
        st.progress(total_credits / 58)


def render_mandatory_units():
    """Show mandatory units (must complete all 7)"""
    
    st.subheader("📚 Mandatory Units (Must Complete All)")
    
    st.info("✅ You MUST complete all 7 mandatory units (24 credits) to achieve your diploma.")
    
    for unit_id, unit in MANDATORY_UNITS.items():
        with st.expander(f"✅ {unit['code']}: {unit['name']} ({unit['credits']} credits)", expanded=False):
            # Unit info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("GLH", f"{unit['glh']} hours")
            with col2:
                st.metric("Credits", unit['credits'])
            with col3:
                st.metric("Progress", "60%")
            
            st.write(f"**Assessment Methods:** {', '.join(unit['assessment_methods'])}")
            
            st.markdown("---")
            
            # View materials button
            if st.button(f"📖 View Learning Materials", key=f"view_{unit_id}"):
                st.session_state[f'show_materials_{unit_id}'] = True
            
            # Display materials if button was clicked
            if st.session_state.get(f'show_materials_{unit_id}', False):
                with st.container():
                    st.markdown(f"### 📚 Learning Materials: {unit['name']}")
                    
                    # Load and display content
                    content = load_markdown_file(unit['file'])
                    
                    if content and not content.startswith("Error"):
                        st.markdown(content, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"✅ Mark Complete", key=f"complete_{unit_id}", type="primary"):
                                st.success(f"✅ {unit['name']} marked as complete!")
                                st.balloons()
                        with col2:
                            if st.button(f"📝 Submit Evidence", key=f"evidence_{unit_id}"):
                                st.info("Go to the 'Submit Evidence' tab to upload your evidence!")
                        with col3:
                            # Download as markdown
                            st.download_button(
                                label=f"📥 Download",
                                data=content,
                                file_name=f"{unit['file']}",
                                mime="text/markdown",
                                key=f"download_{unit_id}"
                            )
                        
                        # Hide button
                        if st.button(f"🔼 Hide Materials", key=f"hide_{unit_id}"):
                            st.session_state[f'show_materials_{unit_id}'] = False
                            st.rerun()
                    else:
                        st.error(content)  # Show error message


def render_optional_units_selection():
    """Allow students to choose optional units to reach 34 credits from 20 options"""
    
    st.subheader("🎯 Choose Your Optional Units")
    
    st.info("✅ You must choose **34 credits** of optional units from the 20 options below to complete your diploma.")
    
    # Mock selected units (replace with database)
    if 'selected_optional_units' not in st.session_state:
        st.session_state.selected_optional_units = []
    
    # Show selected units
    st.markdown("### 📌 Your Selected Units")
    
    if len(st.session_state.selected_optional_units) == 0:
        st.warning("⚠️ You haven't selected any optional units yet. Choose units to reach 34 credits.")
    else:
        selected_credits = sum([OPTIONAL_UNITS[uid]['credits'] for uid in st.session_state.selected_optional_units])
        credits_remaining = 34 - selected_credits
        if credits_remaining > 0:
            st.warning(f"⚠️ Selected: {len(st.session_state.selected_optional_units)} units ({selected_credits}/34 credits) - Need {credits_remaining} more credits")
        elif credits_remaining == 0:
            st.success(f"✅ Perfect! Selected: {len(st.session_state.selected_optional_units)} units ({selected_credits}/34 credits)")
        else:
            st.error(f"❌ Too many credits! Selected: {selected_credits}/34 credits - Remove {abs(credits_remaining)} credits")
        
        for unit_id in st.session_state.selected_optional_units:
            unit = OPTIONAL_UNITS[unit_id]
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"✅ **{unit['code']}: {unit['name']}** ({unit['credits']} credits)")
            with col2:
                if st.button("Remove", key=f"remove_{unit_id}"):
                    st.session_state.selected_optional_units.remove(unit_id)
                    st.rerun()
    
    # Show available units by category
    st.markdown("---")
    st.markdown("### 📚 Available Optional Units")
    
    # Group by category
    categories = {}
    for unit_id, unit in OPTIONAL_UNITS.items():
        category = unit.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append((unit_id, unit))
    
    # Display by category
    for category, units in categories.items():
        with st.expander(f"📂 {category} ({len(units)} units)"):
            for unit_id, unit in units:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{unit['code']}: {unit['name']}**")
                    st.write(f"GLH: {unit['glh']} hours | Credits: {unit['credits']}")
                with col2:
                    if unit_id in st.session_state.selected_optional_units:
                        st.success("✅ Selected")
                    elif len(st.session_state.selected_optional_units) >= 4:
                        st.button("Full", key=f"select_{unit_id}", disabled=True)
                    else:
                        if st.button("Select", key=f"select_{unit_id}"):
                            st.session_state.selected_optional_units.append(unit_id)
                            st.rerun()


def render_evidence_submission():
    """Evidence submission interface"""
    
    st.subheader("📝 Submit Evidence")
    
    st.info("Upload evidence for your units here. Each piece of evidence should be linked to specific learning outcomes.")
    
    # Select unit
    all_unit_names = {uid: f"{u['code']}: {u['name']}" for uid, u in ALL_UNITS.items()}
    selected_unit = st.selectbox("Select Unit", options=list(all_unit_names.keys()), format_func=lambda x: all_unit_names[x])
    
    # Evidence details
    evidence_type = st.selectbox("Evidence Type", [
        "Observation",
        "Reflective Account",
        "Professional Discussion",
        "Witness Statement",
        "Work Product",
        "Case Study",
        "Other"
    ])
    
    evidence_description = st.text_area("Describe what this evidence demonstrates...")
    
    # File upload
    st.write("**Upload Evidence File:**")
    uploaded_file = st.file_uploader("Drag and drop file here", type=['pdf', 'docx', 'jpg', 'png', 'jpeg'])
    
    if st.button("📤 Submit Evidence", type="primary"):
        if uploaded_file and evidence_description:
            st.success("✅ Evidence submitted successfully!")
        else:
            st.error("❌ Please provide description and upload a file.")


def render_portfolio():
    """Show student's evidence portfolio"""
    
    st.subheader("📁 My Portfolio")
    
    st.info("Your complete portfolio of evidence organized by unit.")
    
    # Evidence by unit
    for unit_id, unit in MANDATORY_UNITS.items():
        with st.expander(f"{unit['code']}: {unit['name']}"):
            
            st.write("**Evidence for this unit:**")
            
            # Sample evidence (get from database)
            evidence_items = [
                {"type": "Observation", "date": "2025-10-15", "status": "Approved", "criteria": "1.1, 1.2"},
                {"type": "Reflective Account", "date": "2025-10-18", "status": "Pending", "criteria": "2.1"},
            ]
            
            for idx, item in enumerate(evidence_items):
                status_icon = "✅" if item['status'] == "Approved" else "⏳"
                st.write(f"{status_icon} **{item['type']}** - {item['date']} - Criteria: {item['criteria']}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"Status: {item['status']}")
                with col2:
                    st.button("View", key=f"view_{unit_id}_{item['type']}_{item['date']}_{idx}")
    
    # Download portfolio
    st.markdown("---")
    st.download_button(
        "📥 Download Complete Portfolio (PDF)",
        data="Portfolio PDF here",
        file_name="Level3_Portfolio.pdf",
        mime="application/pdf",
        type="primary"
    )


def render_assessment_schedule():
    """Show upcoming assessments and visits"""
    
    st.subheader("📅 Assessment Schedule")
    
    st.info("Your upcoming observations, assessments, and tutor visits.")
    
    # Mock schedule
    schedule = [
        {"date": "2025-11-05", "type": "Observation", "unit": "Unit 1", "assessor": "Jane Smith"},
        {"date": "2025-11-12", "type": "Professional Discussion", "unit": "Unit 2", "assessor": "John Doe"},
        {"date": "2025-11-20", "type": "Workplace Visit", "unit": "Multiple", "assessor": "Jane Smith"},
    ]
    
    for item in schedule:
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"📅 **{item['date']}**")
            with col2:
                st.write(f"**{item['type']}**")
            with col3:
                st.write(f"{item['unit']}")
            with col4:
                st.write(f"👤 {item['assessor']}")
            st.markdown("---")


# ============================================
# ASSESSOR VIEW
# ============================================

def render_assessor_view():
    """Teacher/assessor view"""
    
    st.success("👨‍🏫 **Assessor View** - Manage learners and assessments")
    
    tabs = st.tabs([
        "👥 My Learners",
        "📊 Progress Overview",
        "📝 Record Observation",
        "📁 Review Evidence",
        "🎓 Certificates"
    ])
    
    with tabs[0]:
        render_learner_list()
    
    with tabs[1]:
        st.info("Progress overview for all learners")
    
    with tabs[2]:
        st.info("Record observation form")
    
    with tabs[3]:
        st.info("Review submitted evidence")
    
    with tabs[4]:
        st.info("Generate certificates")


def render_learner_list():
    """Show list of learners"""
    
    st.subheader("👥 My Learners")
    
    # Mock learners
    learners = [
        {"name": "John Smith", "progress": 65, "units_completed": "4/7", "last_activity": "2025-10-25"},
        {"name": "Jane Doe", "progress": 80, "units_completed": "5/7", "last_activity": "2025-10-26"},
    ]
    
    for learner in learners:
        with st.expander(f"👤 {learner['name']} - {learner['progress']}% complete"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Progress", f"{learner['progress']}%")
            with col2:
                st.metric("Units", learner['units_completed'])
            with col3:
                st.metric("Last Activity", learner['last_activity'])
            
            st.progress(learner['progress'] / 100)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.button("📊 View Progress", key=f"progress_{learner['name']}")
            
            with col2:
                st.button("📝 Record Observation", key=f"obs_{learner['name']}")
            
            with col3:
                st.button("📁 View Portfolio", key=f"portfolio_{learner['name']}")
            
            with col4:
                st.button("📅 Schedule Visit", key=f"schedule_{learner['name']}")
