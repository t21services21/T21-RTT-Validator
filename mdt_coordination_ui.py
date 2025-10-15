"""
T21 MDT COORDINATION UI
Complete interface for MDT meeting management

Features:
- Create & schedule MDT meetings
- Add patients to MDT
- Record outcomes
- Track actions
- Generate reports
"""

import streamlit as st
from mdt_coordination_system import (
    create_mdt_meeting,
    add_patient_to_mdt,
    record_mdt_outcome,
    complete_mdt_meeting,
    get_all_mdt_meetings,
    get_upcoming_mdt_meetings,
    get_mdt_meeting_by_id,
    get_mdt_stats,
    export_mdt_meeting_report,
    MDT_SPECIALTIES,
    MDT_OUTCOMES
)
from datetime import datetime, timedelta


def render_mdt_coordination():
    """Main MDT coordination interface"""
    
    st.header("👥 MDT Coordination System")
    st.markdown("**AI-Powered Multi-Disciplinary Team Meeting Management**")
    
    st.success("""
    👥 **Complete MDT Coordination**
    - Schedule MDT meetings
    - Manage patient lists
    - Record outcomes & decisions
    - Track actions
    - Automated reporting
    - AI decision recommendations
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 MDT Dashboard",
        "📅 Schedule Meeting",
        "➕ Add Patient to MDT",
        "✅ Record Outcomes",
        "📥 MDT Reports"
    ])
    
    with tab1:
        render_mdt_dashboard()
    
    with tab2:
        render_schedule_mdt()
    
    with tab3:
        render_add_patient_to_mdt()
    
    with tab4:
        render_record_outcomes()
    
    with tab5:
        render_mdt_reports()


def render_mdt_dashboard():
    """MDT dashboard with stats"""
    
    st.subheader("📊 MDT Dashboard")
    
    stats = get_mdt_stats()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total MDT Meetings", stats['total_meetings'])
    
    with col2:
        st.metric("Upcoming Meetings", stats['upcoming_count'])
    
    with col3:
        st.metric("This Week", stats['this_week'])
    
    with col4:
        st.metric("Patients Discussed", stats['total_patients_discussed'])
    
    st.markdown("---")
    
    # Upcoming meetings
    st.markdown("### 📅 Upcoming MDT Meetings")
    
    upcoming = get_upcoming_mdt_meetings()
    
    if upcoming:
        for meeting in upcoming[:5]:  # Show next 5
            with st.expander(f"📅 {meeting['specialty']} MDT - {meeting['meeting_date']} at {meeting['meeting_time']}"):
                st.markdown(f"**Location:** {meeting['location']}")
                st.markdown(f"**Chair:** {meeting.get('chair_person') or meeting.get('chair', 'N/A')}")
                patients = meeting.get('patients_discussed') or meeting.get('patients', [])
                st.markdown(f"**Patients:** {len(patients)}")
                st.markdown(f"**Status:** {meeting['status']}")
                
                if st.button("👁️ View Details", key=f"view_{meeting['meeting_id']}"):
                    st.session_state['viewing_mdt'] = meeting['meeting_id']
    else:
        st.info("No upcoming MDT meetings scheduled")


def render_schedule_mdt():
    """Schedule new MDT meeting"""
    
    st.subheader("📅 Schedule MDT Meeting")
    
    # Show success message if meeting was just scheduled
    if 'mdt_meeting_scheduled' in st.session_state:
        meeting_info = st.session_state['mdt_meeting_scheduled']
        st.success(f"✅ MDT Meeting scheduled! ID: {meeting_info['meeting_id']}")
        st.balloons()
        st.info(f"Meeting scheduled for **{meeting_info['meeting_date']}**. View in 'MDT Dashboard' tab.")
        # Clear the flag
        del st.session_state['mdt_meeting_scheduled']
    
    with st.form("schedule_mdt"):
        col1, col2 = st.columns(2)
        
        with col1:
            meeting_date = st.date_input("Meeting Date", value=datetime.now() + timedelta(days=7))
            meeting_time = st.time_input("Meeting Time", value=datetime.strptime("14:00", "%H:%M").time())
            specialty = st.selectbox("Specialty", MDT_SPECIALTIES)
        
        with col2:
            location = st.text_input("Location/Room", placeholder="e.g., Meeting Room 3")
            chair = st.text_input("Meeting Chair*", placeholder="e.g., Dr. Smith")
            meeting_type = st.selectbox("Meeting Type", ["Regular", "Emergency", "Special"])
        
        st.markdown("**Attendees** (one per line):")
        attendees_text = st.text_area("Attendees", height=100, 
                                      placeholder="Dr. Jones - Oncologist\nDr. Brown - Surgeon\nSarah Wilson - CNS")
        
        notes = st.text_area("Meeting Notes", height=100)
        
        submit = st.form_submit_button("📅 Schedule MDT Meeting", type="primary")
        
        if submit:
            if not chair:
                st.error("❌ Meeting chair is required!")
            else:
                # Parse attendees
                attendees = [line.strip() for line in attendees_text.split('\n') if line.strip()]
                
                meeting_id = create_mdt_meeting(
                    meeting_date=str(meeting_date),
                    meeting_time=meeting_time.strftime("%H:%M"),
                    specialty=specialty,
                    location=location,
                    chair=chair,
                    attendees=attendees,
                    meeting_type=meeting_type,
                    notes=notes
                )
                
                # Store success message in session state
                st.session_state['mdt_meeting_scheduled'] = {
                    'meeting_id': meeting_id,
                    'meeting_date': str(meeting_date)
                }
                
                # Force refresh to show new data
                st.rerun()


def render_add_patient_to_mdt():
    """Add patient to upcoming MDT"""
    
    st.subheader("➕ Add Patient to MDT")
    
    # Select upcoming meeting
    upcoming = get_upcoming_mdt_meetings()
    
    if not upcoming:
        st.warning("⚠️ No upcoming MDT meetings. Schedule a meeting first.")
        return
    
    meeting_options = [f"{m['specialty']} MDT - {m['meeting_date']} ({m['meeting_id']})" for m in upcoming]
    selected_meeting = st.selectbox("Select MDT Meeting", meeting_options, key="select_mdt_add_patient")
    
    if selected_meeting:
        meeting_id = selected_meeting.split('(')[1].strip(')')
        
        with st.form("add_patient_mdt"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_name = st.text_input("Patient Name*", placeholder="John Smith")
                nhs_number = st.text_input("NHS Number*", placeholder="123 456 7890")
                diagnosis = st.text_input("Diagnosis*", placeholder="e.g., Stage II Breast Cancer")
            
            with col2:
                presenting_clinician = st.text_input("Presenting Clinician*", placeholder="Dr. Jones")
                urgency = st.selectbox("Urgency", ["Standard", "Urgent", "Emergency"])
                presentation_order = st.number_input("Presentation Order (optional)", min_value=1, value=None)
            
            discussion_points = st.text_area("Discussion Points*", height=150,
                                            placeholder="Key points for MDT discussion...")
            
            submit = st.form_submit_button("➕ Add Patient to MDT", type="primary")
            
            if submit:
                if not patient_name or not nhs_number or not diagnosis or not presenting_clinician:
                    st.error("❌ Please fill all required fields!")
                else:
                    success = add_patient_to_mdt(
                        meeting_id=meeting_id,
                        patient_name=patient_name,
                        nhs_number=nhs_number,
                        diagnosis=diagnosis,
                        presenting_clinician=presenting_clinician,
                        discussion_points=discussion_points,
                        urgency=urgency,
                        presentation_order=presentation_order
                    )
                    
                    if success:
                        st.success(f"✅ Patient {patient_name} added to MDT!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to add patient. Check meeting ID.")


def render_record_outcomes():
    """Record MDT outcomes"""
    
    st.subheader("✅ Record MDT Outcomes")
    
    # Select meeting
    meetings = get_all_mdt_meetings()
    
    if not meetings:
        st.warning("⚠️ No MDT meetings found.")
        return
    
    meeting_options = [f"{m['specialty']} MDT - {m['meeting_date']} ({m['meeting_id']})" for m in meetings[:10]]
    selected_meeting = st.selectbox("Select MDT Meeting", meeting_options, key="select_mdt_record_outcomes")
    
    if selected_meeting:
        meeting_id = selected_meeting.split('(')[1].strip(')')
        meeting = get_mdt_meeting_by_id(meeting_id)
        
        if meeting:
            # Get patients list (handle both old and new field names)
            patients = meeting.get('patients_discussed') or meeting.get('patients', [])
            st.markdown(f"### Patients in this MDT: {len(patients)}")
            
            # Show each patient
            for idx, patient in enumerate(patients, 1):
                with st.expander(f"{idx}. {patient['patient_name']} (NHS: {patient['nhs_number']})"):
                    st.markdown(f"**Diagnosis:** {patient['diagnosis']}")
                    st.markdown(f"**Presenter:** {patient['presenting_clinician']}")
                    st.markdown(f"**Discussion Points:** {patient['discussion_points']}")
                    
                    if patient.get('discussed'):
                        st.success("✅ Outcome Recorded")
                        st.markdown(f"**Outcome:** {patient.get('outcome', 'N/A')}")
                        st.markdown(f"**Decision:** {patient.get('decision', 'N/A')}")
                    else:
                        st.warning("⚠️ Outcome NOT recorded")
                        
                        with st.form(f"outcome_{patient['nhs_number']}"):
                            outcome = st.selectbox("MDT Outcome", MDT_OUTCOMES, key=f"out_{idx}")
                            decision = st.text_area("Clinical Decision", height=100, key=f"dec_{idx}")
                            
                            actions_text = st.text_area("Actions Required (one per line)", height=100, key=f"act_{idx}",
                                                       placeholder="Book surgery within 4 weeks\nArrange chemotherapy\nRefer to palliative care")
                            
                            next_steps = st.text_area("Next Steps", height=80, key=f"next_{idx}")
                            
                            if st.form_submit_button("✅ Record Outcome", key=f"submit_{idx}"):
                                actions = [a.strip() for a in actions_text.split('\n') if a.strip()]
                                
                                success = record_mdt_outcome(
                                    meeting_id=meeting_id,
                                    nhs_number=patient['nhs_number'],
                                    outcome=outcome,
                                    decision=decision,
                                    actions=actions,
                                    next_steps=next_steps
                                )
                                
                                if success:
                                    st.success("✅ Outcome recorded!")
                                    st.rerun()
            
            # Complete meeting button
            if meeting['status'] != 'COMPLETED':
                st.markdown("---")
                st.markdown("### Complete MDT Meeting")
                
                with st.form("complete_mdt"):
                    summary = st.text_area("Meeting Summary", height=150)
                    
                    if st.form_submit_button("✅ Complete & Close MDT Meeting", type="primary"):
                        success = complete_mdt_meeting(meeting_id, summary)
                        if success:
                            st.success("✅ MDT Meeting completed!")
                            st.balloons()
                            st.rerun()


def render_mdt_reports():
    """MDT reports and exports"""
    
    st.subheader("📥 MDT Reports")
    
    # Select meeting
    meetings = get_all_mdt_meetings()
    
    if not meetings:
        st.warning("⚠️ No MDT meetings found.")
        return
    
    meeting_options = [f"{m['specialty']} MDT - {m['meeting_date']} ({m['meeting_id']})" for m in meetings[:20]]
    selected_meeting = st.selectbox("Select MDT Meeting", meeting_options, key="select_mdt_reports")
    
    if selected_meeting:
        meeting_id = selected_meeting.split('(')[1].strip(')')
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Generate MDT Report", type="primary"):
                report = export_mdt_meeting_report(meeting_id)
                
                if report:
                    st.success("✅ Report generated!")
                    st.text_area("MDT Meeting Report", value=report, height=600)
                    
                    st.download_button(
                        label="💾 Download Report",
                        data=report,
                        file_name=f"MDT_Report_{meeting_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("❌ Failed to generate report")
        
        with col2:
            st.markdown("#### Report Contents:")
            st.markdown("""
            - Meeting details
            - Attendees list
            - All patients discussed
            - Outcomes recorded
            - Actions required
            - Meeting summary
            """)
