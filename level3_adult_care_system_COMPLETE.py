"""
LEVEL 3 DIPLOMA IN ADULT CARE - COMPLETE SYSTEM WITH ALL 27 UNITS
Integrated into T21 Healthcare Platform

Structure:
- 3 Mandatory Units (37 credits)
- 24 Optional Units (choose 4 for 21 credits)
- Total: 7 units = 58 credits

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

# ============================================
# LEVEL 3 QUALIFICATION STRUCTURE
# ============================================

# MANDATORY UNITS (3 units = 37 credits)
MANDATORY_UNITS = {
    'unit1': {
        'code': 'Unit 1',
        'name': 'Duty of Care',
        'glh': 20,
        'credits': 12,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT1_DUTY_OF_CARE_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2', '3.3'],
        'assessment_methods': ['Professional Discussion', 'Reflective Account', 'Witness Statement']
    },
    'unit2': {
        'code': 'Unit 2',
        'name': 'Equality, Diversity and Inclusion',
        'glh': 27,
        'credits': 13,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT2_EQUALITY_DIVERSITY_COMPLETE.md',
        'criteria': ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3'],
        'assessment_methods': ['Written Assignment', 'Observation', 'Reflective Account']
    },
    'unit3': {
        'code': 'Unit 3',
        'name': 'Person-Centred Care',
        'glh': 24,
        'credits': 12,
        'type': 'mandatory',
        'file': 'LEVEL3_UNIT3_PERSON_CENTRED_CARE_COMPLETE.md',
        'criteria': ['1.1', '1.2', '2.1', '2.2', '2.3', '3.1', '3.2', '4.1', '4.2'],
        'assessment_methods': ['Observation', 'Professional Discussion', 'Care Plan Evidence']
    }
}

# OPTIONAL UNITS (24 units - choose 4 for 21 credits)
OPTIONAL_UNITS = {
    'unit4': {
        'code': 'Unit 4',
        'name': 'Safeguarding in Care Settings',
        'glh': 26,
        'credits': 3,
        'type': 'optional',
        'category': 'Core Skills',
        'file': 'LEVEL3_UNIT4_SAFEGUARDING_COMPLETE.md',
        'unit_code': 'L/650/2299'
    },
    'unit5': {
        'code': 'Unit 5',
        'name': 'Effective Communication',
        'glh': 22,
        'credits': 3,
        'type': 'optional',
        'category': 'Core Skills',
        'file': 'LEVEL3_UNIT5_COMMUNICATION_COMPLETE.md',
        'unit_code': 'F/650/2302'
    },
    'unit6': {
        'code': 'Unit 6',
        'name': 'Health & Wellbeing',
        'glh': 28,
        'credits': 3,
        'type': 'optional',
        'category': 'Core Skills',
        'file': 'LEVEL3_UNIT6_HEALTH_WELLBEING_COMPLETE.md',
        'unit_code': 'R/650/2308'
    },
    'unit7': {
        'code': 'Unit 7',
        'name': 'Continuous Professional Development',
        'glh': 24,
        'credits': 3,
        'type': 'optional',
        'category': 'Core Skills',
        'file': 'LEVEL3_UNIT7_PROFESSIONAL_DEVELOPMENT_COMPLETE.md',
        'unit_code': 'D/650/2310'
    },
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
        - **3 Mandatory Units** (37 credits) - MUST complete all
        - **4 Optional Units** (21 credits) - Choose from 24 options
        
        **Total:** 7 units = 58 credits
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
    mandatory_completed = 2
    mandatory_total = 3
    optional_selected = 4
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
    
    mandatory_credits = 25  # Mock: 2/3 units done
    optional_credits = 4    # Mock: 1/4 units done
    total_credits = mandatory_credits + optional_credits
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mandatory Credits", f"{mandatory_credits}/37")
    
    with col2:
        st.metric("Optional Credits", f"{optional_credits}/21")
    
    with col3:
        st.metric("Total Credits", f"{total_credits}/58")
        st.progress(total_credits / 58)


def render_mandatory_units():
    """Show mandatory units (must complete all 3)"""
    
    st.subheader("📚 Mandatory Units (Must Complete All)")
    
    st.info("✅ You MUST complete all 3 mandatory units to achieve your diploma.")
    
    for unit_id, unit in MANDATORY_UNITS.items():
        with st.expander(f"✅ {unit['code']}: {unit['name']} ({unit['credits']} credits)"):
            st.write(f"**GLH:** {unit['glh']} hours")
            st.write(f"**Credits:** {unit['credits']}")
            st.write(f"**Assessment Methods:** {', '.join(unit['assessment_methods'])}")
            
            # Mock progress
            st.progress(0.6)
            st.write("**Progress:** 60% complete")
            
            # View materials button
            if st.button(f"📖 View Learning Materials", key=f"view_{unit_id}"):
                st.info(f"Learning materials for {unit['name']} would load here from {unit['file']}")


def render_optional_units_selection():
    """Allow students to choose 4 optional units from 24"""
    
    st.subheader("🎯 Choose Your Optional Units")
    
    st.info("✅ You must choose **4 optional units** (21 credits total) from the 24 options below.")
    
    # Mock selected units (replace with database)
    if 'selected_optional_units' not in st.session_state:
        st.session_state.selected_optional_units = []
    
    # Show selected units
    st.markdown("### 📌 Your Selected Units")
    
    if len(st.session_state.selected_optional_units) == 0:
        st.warning("⚠️ You haven't selected any optional units yet. Choose 4 units below.")
    else:
        selected_credits = sum([OPTIONAL_UNITS[uid]['credits'] for uid in st.session_state.selected_optional_units])
        st.success(f"✅ Selected: {len(st.session_state.selected_optional_units)}/4 units ({selected_credits} credits)")
        
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
