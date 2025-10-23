"""
LEVEL 3 DIPLOMA IN ADULT CARE - COMPLETE SYSTEM MODULE
Integrated into T21 Healthcare Platform

Features:
- Unit progress tracking
- Observation recording
- Evidence management
- Assessment planning
- Portfolio building
- IQA sampling
"""

import streamlit as st
from datetime import datetime, date
import json
from typing import Dict, List, Optional

# ============================================
# LEVEL 3 QUALIFICATION STRUCTURE
# ============================================

LEVEL3_UNITS = {
    'unit1': {
        'code': 'Unit 1',
        'name': 'Duty of Care',
        'glh': 20,
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2', '3.3'],
        'assessment_methods': ['Professional Discussion', 'Reflective Account', 'Witness Statement']
    },
    'unit2': {
        'code': 'Unit 2',
        'name': 'Equality, Diversity and Inclusion',
        'glh': 30,
        'criteria': ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3'],
        'assessment_methods': ['Written Assignment', 'Observation', 'Reflective Account']
    },
    'unit3': {
        'code': 'Unit 3',
        'name': 'Person-Centred Care',
        'glh': 40,
        'criteria': ['1.1', '1.2', '2.1', '2.2', '2.3', '3.1', '3.2', '4.1', '4.2'],
        'assessment_methods': ['Observation', 'Professional Discussion', 'Care Plan Evidence']
    },
    'unit4': {
        'code': 'Unit 4',
        'name': 'Communication in Health and Social Care',
        'glh': 30,
        'criteria': ['1.1', '1.2', '2.1', '2.2', '2.3', '3.1', '3.2', '4.1', '4.2'],
        'assessment_methods': ['Observation', 'Witness Statement', 'Reflective Account']
    },
    'unit5': {
        'code': 'Unit 5',
        'name': 'Health and Safety',
        'glh': 35,
        'criteria': ['1.1', '1.2', '1.3', '2.1', '2.2', '3.1', '3.2', '4.1', '4.2', '5.1'],
        'assessment_methods': ['Observation', 'Risk Assessment', 'Health & Safety Certificates']
    },
    'unit6': {
        'code': 'Unit 6',
        'name': 'Safeguarding and Protection',
        'glh': 35,
        'criteria': ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '4.1', '4.2'],
        'assessment_methods': ['Written Assignment', 'Professional Discussion', 'Case Study']
    },
    'unit7': {
        'code': 'Unit 7',
        'name': 'Personal Development',
        'glh': 25,
        'criteria': ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2', '4.1'],
        'assessment_methods': ['Personal Development Plan', 'Reflective Journal', 'Supervision Records']
    }
}


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
    """Learner dashboard and portfolio"""
    
    st.info("**Welcome to your Level 3 Diploma!** Track your progress, submit evidence, and build your portfolio.")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 My Progress",
        "📚 Course Materials",
        "📝 Submit Evidence",
        "📁 My Portfolio",
        "📅 Assessment Schedule"
    ])
    
    with tab1:
        render_learner_progress()
    
    with tab2:
        render_course_materials()
    
    with tab3:
        render_evidence_submission()
    
    with tab4:
        render_learner_portfolio()
    
    with tab5:
        render_assessment_schedule()


def render_learner_progress():
    """Show learner's progress across all units"""
    
    st.subheader("📊 Your Progress")
    
    # Overall progress
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Units Completed", "2 / 7", "28%")
    
    with col2:
        st.metric("Evidence Submitted", "15 items", "+3 this week")
    
    with col3:
        st.metric("Target Completion", "December 2025", "8 weeks left")
    
    st.markdown("---")
    
    # Unit-by-unit progress
    st.subheader("📚 Unit Progress")
    
    for unit_id, unit in LEVEL3_UNITS.items():
        with st.expander(f"{unit['code']}: {unit['name']}"):
            
            # Progress bar
            progress = 0  # Get from database
            st.progress(progress / 100)
            st.write(f"**{progress}% Complete**")
            
            # Status
            status = "Not Started"  # Get from database
            status_colors = {
                'Not Started': '⚪',
                'In Progress': '🟡',
                'Completed': '🟢'
            }
            st.write(f"Status: {status_colors.get(status, '⚪')} {status}")
            
            # Criteria checklist
            st.write("**Assessment Criteria:**")
            for criteria in unit['criteria']:
                # Check if met (get from database)
                is_met = False
                if is_met:
                    st.write(f"✅ {criteria}")
                else:
                    st.write(f"⬜ {criteria}")
            
            # Evidence count
            evidence_count = 0  # Get from database
            st.write(f"**Evidence Collected:** {evidence_count} items")
            
            # Next steps
            st.info(f"**Next Steps:** Complete observation for criteria {unit['criteria'][0]}")


def render_course_materials():
    """Display all course materials by unit"""
    
    st.subheader("📚 Course Materials")
    
    st.info("Access all learning resources, reading materials, and assessment guidance for each unit.")
    
    for unit_id, unit in LEVEL3_UNITS.items():
        with st.expander(f"{unit['code']}: {unit['name']} ({unit['glh']} GLH)"):
            
            st.markdown(f"**Assessment Methods:** {', '.join(unit['assessment_methods'])}")
            
            # Materials
            st.markdown("### 📖 Learning Resources")
            st.download_button(
                f"📄 Download Unit {unit['code']} Handbook",
                data="Unit content here",  # Load from files
                file_name=f"Unit_{unit['code']}_Handbook.pdf",
                mime="application/pdf"
            )
            
            st.download_button(
                f"📋 Download Assessment Guidance",
                data="Assessment guidance here",
                file_name=f"Unit_{unit['code']}_Assessment.pdf",
                mime="application/pdf"
            )
            
            # Activities
            st.markdown("### ✏️ Activities & Exercises")
            st.write("- Activity 1: Reflective practice exercise")
            st.write("- Activity 2: Case study analysis")
            st.write("- Activity 3: Workplace observation")


def render_evidence_submission():
    """Allow learners to submit evidence"""
    
    st.subheader("📝 Submit Evidence")
    
    st.info("Upload your evidence here. Your assessor will review and provide feedback.")
    
    with st.form("evidence_submission"):
        
        # Evidence type
        evidence_type = st.selectbox(
            "Evidence Type",
            ["Reflective Account", "Witness Statement", "Work Product", "Written Assignment", "Other"]
        )
        
        # Unit selection
        unit_options = [f"{u['code']}: {u['name']}" for u in LEVEL3_UNITS.values()]
        selected_units = st.multiselect("Which unit(s) does this evidence cover?", unit_options)
        
        # Criteria selection
        st.write("**Which assessment criteria does this evidence cover?**")
        selected_criteria = st.text_input("Enter criteria codes (e.g., 1.1, 1.2, 2.1)", placeholder="1.1, 1.2")
        
        # Description
        description = st.text_area(
            "Description of Evidence",
            height=150,
            placeholder="Describe what this evidence demonstrates..."
        )
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Evidence File",
            type=['pdf', 'docx', 'jpg', 'png'],
            help="Accepted formats: PDF, Word, Images"
        )
        
        # Submit
        submitted = st.form_submit_button("📤 Submit Evidence")
        
        if submitted:
            if uploaded_file and description and selected_units:
                # Save to database
                st.success("✅ Evidence submitted successfully!")
                st.balloons()
                st.info("Your assessor will review this within 5 working days.")
            else:
                st.error("❌ Please complete all required fields")


def render_learner_portfolio():
    """Show learner's complete portfolio"""
    
    st.subheader("📁 My Portfolio")
    
    st.info("Your complete portfolio of evidence organized by unit.")
    
    # Portfolio summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Evidence", "15 items")
    
    with col2:
        st.metric("Pending Review", "3 items")
    
    with col3:
        st.metric("Approved", "12 items")
    
    st.markdown("---")
    
    # Evidence by unit
    for unit_id, unit in LEVEL3_UNITS.items():
        with st.expander(f"{unit['code']}: {unit['name']}"):
            
            st.write("**Evidence for this unit:**")
            
            # Sample evidence (get from database)
            evidence_items = [
                {"type": "Observation", "date": "2025-10-15", "status": "Approved", "criteria": "1.1, 1.2"},
                {"type": "Reflective Account", "date": "2025-10-18", "status": "Pending", "criteria": "2.1"},
            ]
            
            for item in evidence_items:
                status_icon = "✅" if item['status'] == "Approved" else "⏳"
                st.write(f"{status_icon} **{item['type']}** - {item['date']} - Criteria: {item['criteria']}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"Status: {item['status']}")
                with col2:
                    st.button("View", key=f"view_{item['type']}_{item['date']}")
    
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
    
    st.info("Your upcoming assessor visits and assessment deadlines.")
    
    # Upcoming visits
    st.markdown("### 🗓️ Upcoming Assessor Visits")
    
    visits = [
        {"date": "2025-11-05", "time": "10:00 AM", "focus": "Units 3 & 4 Observations", "location": "Your Workplace"},
        {"date": "2025-11-19", "time": "2:00 PM", "focus": "Professional Discussion - Unit 6", "location": "Your Workplace"},
        {"date": "2025-12-03", "time": "10:00 AM", "focus": "Final Portfolio Review", "location": "Your Workplace"},
    ]
    
    for visit in visits:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                st.write(f"📅 **{visit['date']}**")
            with col2:
                st.write(f"🕐 {visit['time']}")
            with col3:
                st.write(f"📍 {visit['location']}")
            st.write(f"**Focus:** {visit['focus']}")
            st.markdown("---")
    
    # Pending submissions
    st.markdown("### ⏰ Pending Submissions")
    
    deadlines = [
        {"task": "Reflective Account - Unit 2", "due": "2025-11-01", "status": "Due Soon"},
        {"task": "Written Assignment - Unit 6", "due": "2025-11-10", "status": "Upcoming"},
    ]
    
    for deadline in deadlines:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"📝 {deadline['task']}")
        with col2:
            st.write(f"Due: {deadline['due']}")
        with col3:
            if deadline['status'] == "Due Soon":
                st.warning(deadline['status'])
            else:
                st.info(deadline['status'])


# ============================================
# ASSESSOR VIEW
# ============================================

def render_assessor_view():
    """Assessor dashboard and tools"""
    
    st.info("**Assessor Tools:** Manage learners, record observations, track progress, and conduct IQA.")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 My Learners",
        "📝 Record Observation",
        "📊 Progress Tracking",
        "✅ IQA Sampling",
        "📈 Reports"
    ])
    
    with tab1:
        render_assessor_learners()
    
    with tab2:
        render_observation_recording()
    
    with tab3:
        render_assessor_progress_tracking()
    
    with tab4:
        render_iqa_sampling()
    
    with tab5:
        render_assessor_reports()


def render_assessor_learners():
    """List all learners and their status"""
    
    st.subheader("👥 My Learners")
    
    # Sample learners (get from database)
    learners = [
        {
            "name": "Current Learner",
            "start_date": "2025-10-01",
            "target_completion": "2025-12-31",
            "progress": 35,
            "units_completed": 2,
            "total_units": 7,
            "status": "On Track"
        }
    ]
    
    for learner in learners:
        with st.expander(f"📋 {learner['name']} - {learner['progress']}% Complete"):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Progress", f"{learner['progress']}%")
                st.progress(learner['progress'] / 100)
            
            with col2:
                st.metric("Units", f"{learner['units_completed']} / {learner['total_units']}")
            
            with col3:
                st.metric("Status", learner['status'])
            
            # Actions
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.button("📊 View Progress", key=f"progress_{learner['name']}")
            
            with col2:
                st.button("📝 Record Observation", key=f"obs_{learner['name']}")
            
            with col3:
                st.button("📁 View Portfolio", key=f"portfolio_{learner['name']}")
            
            with col4:
                st.button("📅 Schedule Visit", key=f"schedule_{learner['name']}")


def render_observation_recording():
    """Digital observation recording form"""
    
    st.subheader("📝 Record Observation")
    
    st.info("Complete this form during or immediately after observing the learner in practice.")
    
    with st.form("observation_form"):
        
        # Learner selection
        learner = st.selectbox("Select Learner", ["Current Learner"])
        
        # Basic details
        col1, col2 = st.columns(2)
        
        with col1:
            obs_date = st.date_input("Date of Observation", value=date.today())
            obs_time = st.time_input("Time")
        
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=15, max_value=120, value=30)
            location = st.text_input("Location", placeholder="e.g., Care Home, Service User's Room")
        
        # Activity
        activity = st.text_area(
            "Activity Observed",
            height=100,
            placeholder="e.g., Supporting service user with personal care, Assisting with meals, etc."
        )
        
        # Observation narrative
        narrative = st.text_area(
            "Observation Narrative",
            height=300,
            placeholder="""Describe in detail:
- What the learner did
- How they did it
- Communication used
- Skills demonstrated
- Outcome achieved

Be specific and provide examples."""
        )
        
        # Unit and criteria selection
        st.markdown("### 📋 Assessment Criteria Met")
        
        selected_criteria = {}
        
        for unit_id, unit in LEVEL3_UNITS.items():
            with st.expander(f"{unit['code']}: {unit['name']}"):
                unit_criteria = []
                for criteria in unit['criteria']:
                    if st.checkbox(f"Criteria {criteria}", key=f"obs_criteria_{unit_id}_{criteria}"):
                        unit_criteria.append(criteria)
                if unit_criteria:
                    selected_criteria[unit['code']] = unit_criteria
        
        # Feedback
        st.markdown("### 💬 Feedback to Learner")
        
        strengths = st.text_area(
            "Strengths Demonstrated",
            height=100,
            placeholder="What did the learner do well?"
        )
        
        development = st.text_area(
            "Areas for Development",
            height=100,
            placeholder="What could the learner improve?"
        )
        
        # Assessment decision
        decision = st.radio(
            "Assessment Decision",
            ["Competent - All criteria met", "Not Yet Competent - Further evidence required"]
        )
        
        # Photo upload
        photos = st.file_uploader(
            "Upload Photos (optional)",
            accept_multiple_files=True,
            type=['jpg', 'jpeg', 'png'],
            help="Photos of activities, work products, or environment (ensure consent)"
        )
        
        # Submit
        submitted = st.form_submit_button("💾 Save Observation", type="primary")
        
        if submitted:
            if narrative and activity and selected_criteria:
                # Save to database
                observation_data = {
                    'learner': learner,
                    'date': obs_date,
                    'time': obs_time,
                    'duration': duration,
                    'location': location,
                    'activity': activity,
                    'narrative': narrative,
                    'criteria_met': selected_criteria,
                    'strengths': strengths,
                    'development': development,
                    'decision': decision,
                    'assessor': st.session_state.get('user_email', ''),
                    'timestamp': datetime.now()
                }
                
                # Save observation
                # save_observation(observation_data)
                
                st.success("✅ Observation recorded successfully!")
                st.balloons()
                
                # Generate PDF
                st.download_button(
                    "📄 Download Observation Record (PDF)",
                    data="Observation PDF here",
                    file_name=f"Observation_{learner}_{obs_date}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("❌ Please complete all required fields")


def render_assessor_progress_tracking():
    """Track progress for all learners"""
    
    st.subheader("📊 Progress Tracking")
    
    st.info("Monitor learner progress across all units and identify any gaps.")
    
    # Select learner
    learner = st.selectbox("Select Learner", ["Current Learner"])
    
    # Progress summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Progress", "35%")
    
    with col2:
        st.metric("Units Completed", "2 / 7")
    
    with col3:
        st.metric("Evidence Items", "15")
    
    with col4:
        st.metric("Days to Completion", "58")
    
    st.markdown("---")
    
    # Unit-by-unit tracking
    st.subheader("📚 Unit Progress")
    
    for unit_id, unit in LEVEL3_UNITS.items():
        with st.expander(f"{unit['code']}: {unit['name']}"):
            
            # Progress bar
            progress = 0  # Get from database
            st.progress(progress / 100)
            
            # Criteria coverage
            st.markdown("**Criteria Coverage:**")
            
            for criteria in unit['criteria']:
                # Check if met
                is_met = False  # Get from database
                
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    if is_met:
                        st.write("✅")
                    else:
                        st.write("⬜")
                
                with col2:
                    st.write(f"Criteria {criteria}")
            
            # Evidence summary
            st.markdown("**Evidence Collected:**")
            st.write("- 2 Observations")
            st.write("- 1 Witness Statement")
            st.write("- 1 Reflective Account")
            
            # Gaps
            if progress < 100:
                st.warning(f"**Missing:** Professional Discussion, Written Assignment")


def render_iqa_sampling():
    """IQA sampling and quality assurance"""
    
    st.subheader("✅ IQA Sampling")
    
    st.info("Internal Quality Assurance - Sample 10% of all assessments to ensure standards.")
    
    # Sampling plan
    st.markdown("### 📋 Sampling Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assessments", "15")
    
    with col2:
        st.metric("Required Samples", "2")
    
    with col3:
        st.metric("Completed", "1")
    
    st.markdown("---")
    
    # Sample selection
    st.markdown("### 🎲 Select Sample")
    
    if st.button("🎲 Random Sample Selection"):
        st.success("Selected: Observation - Unit 3 - Date: 2025-10-15")
    
    # IQA form
    with st.form("iqa_form"):
        
        st.markdown("### 📝 IQA Feedback")
        
        # Assessment details
        assessment_type = st.selectbox("Assessment Type", ["Observation", "Witness Statement", "Professional Discussion"])
        unit = st.selectbox("Unit", [f"{u['code']}: {u['name']}" for u in LEVEL3_UNITS.values()])
        
        # IQA checks
        st.markdown("**Quality Checks:**")
        
        valid = st.checkbox("✅ Assessment decision is correct")
        authentic = st.checkbox("✅ Evidence is valid, authentic, current, sufficient")
        criteria = st.checkbox("✅ Assessment criteria clearly identified")
        feedback = st.checkbox("✅ Feedback is constructive and developmental")
        documentation = st.checkbox("✅ Documentation is complete and accurate")
        standards = st.checkbox("✅ TQUK standards are met")
        
        # Comments
        strengths = st.text_area("Strengths", height=100)
        development = st.text_area("Areas for Development", height=100)
        
        # Decision
        iqa_decision = st.radio(
            "IQA Decision",
            ["Approved - Assessment decision upheld", "Action Required - See comments"]
        )
        
        # Submit
        submitted = st.form_submit_button("💾 Save IQA Record")
        
        if submitted:
            st.success("✅ IQA record saved successfully!")


def render_assessor_reports():
    """Generate reports for management and TQUK"""
    
    st.subheader("📈 Reports")
    
    st.info("Generate reports for internal monitoring and TQUK compliance.")
    
    # Report types
    report_type = st.selectbox(
        "Select Report Type",
        [
            "Learner Progress Report",
            "Achievement Rates",
            "Assessor Activity Log",
            "IQA Sampling Report",
            "TQUK Compliance Report"
        ]
    )
    
    # Date range
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("From Date")
    
    with col2:
        end_date = st.date_input("To Date")
    
    # Generate
    if st.button("📊 Generate Report", type="primary"):
        st.success("✅ Report generated!")
        
        # Sample data
        st.markdown("### 📊 Report Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Learners", "1")
        
        with col2:
            st.metric("Assessments Conducted", "15")
        
        with col3:
            st.metric("Achievement Rate", "100%")
        
        # Download
        st.download_button(
            "📥 Download Report (PDF)",
            data="Report PDF here",
            file_name=f"Report_{report_type}_{start_date}.pdf",
            mime="application/pdf"
        )


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_learner_progress(learner_id: str) -> Dict:
    """Get learner's progress data"""
    # TODO: Implement database query
    return {
        'overall_progress': 35,
        'units_completed': 2,
        'total_units': 7,
        'evidence_count': 15,
        'status': 'On Track'
    }


def save_observation(observation_data: Dict) -> bool:
    """Save observation to database"""
    # TODO: Implement database save
    return True


def save_evidence(evidence_data: Dict) -> bool:
    """Save evidence submission to database"""
    # TODO: Implement database save
    return True


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    render_level3_adult_care()
