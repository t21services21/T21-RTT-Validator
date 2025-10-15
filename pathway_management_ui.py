"""
T21 PATHWAY MANAGEMENT UI
User interface for complete pathway management
"""

import streamlit as st
from datetime import datetime, date
from pathway_management_system import (
    create_pathway,
    get_all_pathways,
    get_patient_pathways,
    get_pathway_by_id,
    update_pathway_progress,
    close_pathway,
    get_pathway_stats,
    pause_pathway_clock,
    resume_pathway_clock,
    record_milestone,
    update_rtt_status
)
from patient_selector_component import render_patient_selector, render_patient_quick_select
from episode_management_system import get_patient_episodes


SPECIALTIES = [
    "Cardiology", "Dermatology", "ENT", "Gastroenterology",
    "General Surgery", "Neurology", "Ophthalmology", "Orthopaedics",
    "Respiratory", "Rheumatology", "Urology", "Oncology", "Other"
]


def render_pathway_management():
    """Main pathway management interface"""
    
    st.header("📁 Pathway Management System")
    st.markdown("**Create & Track RTT and Cancer Pathways**")
    
    st.success("""
    📁 **Pathway Management Features:**
    - 📋 Create RTT Pathways (18-week)
    - 🎗️ Create Cancer Pathways (2WW, 62-day, 31-day)
    - ⏱️ Automatic breach date calculation
    - 🔗 Link episodes to pathways
    - 📊 Timeline view of patient journey
    - 🚨 Breach risk monitoring
    - 📈 Pathway statistics
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Create Pathway",
        "📋 All Pathways",
        "⏸️ Manage Pathway",
        "📊 Pathway Timeline",
        "📈 Statistics"
    ])
    
    with tab1:
        render_create_pathway()
    
    with tab2:
        render_all_pathways()
    
    with tab3:
        render_manage_pathway()
    
    with tab4:
        render_pathway_timeline()
    
    with tab5:
        render_pathway_stats()


def render_create_pathway():
    """Create new pathway"""
    
    st.subheader("➕ Create New Pathway")
    
    st.info("""
    **Pathway Creation:**
    1. Search and select patient
    2. Choose pathway type (RTT or Cancer)
    3. Pathway automatically starts RTT clock
    4. Add episodes to track progress
    """)
    
    # Success message
    if 'pathway_created' in st.session_state:
        pathway_info = st.session_state['pathway_created']
        st.success(f"✅ Pathway created: {pathway_info['pathway_id']}")
        st.info(f"**Breach Date:** {pathway_info['breach_date']}")
        st.balloons()
        del st.session_state['pathway_created']
    
    # Patient selector with SEARCH
    st.markdown("---")
    selected_patient = render_patient_selector(key_prefix="create_pathway")
    
    if not selected_patient:
        st.warning("⚠️ Please search and select a patient first")
        return
    
    st.markdown("---")
    
    # Pathway creation form
    with st.form("create_pathway_form"):
        st.markdown("### 📁 Pathway Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pathway_type = st.selectbox("Pathway Type*", [
                "rtt",
                "cancer_2ww",
                "cancer_62day",
                "cancer_31day",
                "other"
            ], format_func=lambda x: {
                'rtt': '📋 RTT 18-Week Pathway',
                'cancer_2ww': '🎗️ Cancer 2-Week Wait',
                'cancer_62day': '🎗️ Cancer 62-Day Pathway',
                'cancer_31day': '🎗️ Cancer 31-Day Pathway',
                'other': '📁 Other Pathway'
            }[x])
            
            specialty = st.selectbox("Specialty*", SPECIALTIES,
                                    help="Which specialty is treating this patient?")
            
            consultant = st.text_input("Consultant*", placeholder="Dr. Smith",
                                       help="Lead consultant for this pathway")
        
        with col2:
            referral_source = st.selectbox("Referral Source*", [
                "GP", "Consultant to Consultant", "A&E", "Dentist", "Optician", 
                "Self Referral", "Screening Programme", "Other Healthcare Professional"
            ])
            
            priority = st.selectbox("Priority*", [
                "Routine", "Urgent", "2WW (Two Week Wait)", "Emergency"
            ])
            
            referral_method = st.selectbox("Referral Method", [
                "e-Referral (Choose & Book)", "Letter", "Phone", "Email", "Fax", "Other"
            ])
        
        st.markdown("### 📅 Key Dates")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            referral_received_date = st.date_input("Referral Received Date*", value=date.today(),
                                                   help="Date referral was received by hospital")
        
        with col2:
            clock_start_date = st.date_input("Clock Start Date*", value=date.today(),
                                             help="Date RTT clock starts (usually referral date)")
        
        with col3:
            earliest_reasonable_offer = st.date_input("Earliest Reasonable Offer Date", 
                                                      value=None,
                                                      help="Earliest date patient can attend (Optional)")
        
        st.markdown("### 📋 Clinical Information")
        
        presenting_complaint = st.text_area("Presenting Complaint*", height=80,
                                           placeholder="Main symptoms/condition patient is presenting with...")
        
        suspected_diagnosis = st.text_area("Suspected Diagnosis", height=60,
                                          placeholder="Initial suspected diagnosis (if known)...")
        
        reason = st.text_area("Detailed Reason for Referral*", height=100,
                             placeholder="Full clinical reason for this referral...")
        
        st.markdown("### 📞 Contact & Communication")
        col1, col2 = st.columns(2)
        
        with col1:
            gp_name = st.text_input("Referring GP Name", placeholder="Dr. Jones",
                                   help="Name of referring GP (if applicable)")
            gp_practice = st.text_input("GP Practice", placeholder="High Street Surgery")
        
        with col2:
            patient_informed = st.checkbox("Patient Informed of Referral", value=True)
            interpreter_required = st.checkbox("Interpreter Required")
            if interpreter_required:
                language_needed = st.text_input("Language Required", placeholder="e.g., Polish, Urdu")
        
        additional_needs = st.text_area("Additional Patient Needs", height=60,
                                       placeholder="e.g., Wheelchair access, hearing loop, etc...")
        
        notes = st.text_area("Additional Clinical Notes", height=80,
                            placeholder="Any other relevant clinical information...")
        
        submit = st.form_submit_button("✅ Create Pathway & Start Clock", type="primary")
        
        if submit:
            if not reason or not presenting_complaint or not consultant:
                st.error("❌ Please fill all required fields (marked with *)")
            else:
                with st.spinner("📁 Creating pathway..."):
                    result = create_pathway(
                        patient_id=selected_patient.get('patient_id'),
                        patient_name=selected_patient.get('full_name'),
                        pathway_type=pathway_type,
                        start_date=str(clock_start_date),
                        specialty=specialty,
                        consultant=consultant,
                        referral_source=referral_source,
                        priority=priority,
                        reason=reason,
                        notes=notes,
                        # NEW NHS Workflow fields
                        referral_method=referral_method,
                        referral_received_date=str(referral_received_date),
                        clock_start_date=str(clock_start_date),
                        earliest_reasonable_offer_date=str(earliest_reasonable_offer) if earliest_reasonable_offer else "",
                        presenting_complaint=presenting_complaint,
                        suspected_diagnosis=suspected_diagnosis,
                        gp_name=gp_name,
                        gp_practice=gp_practice,
                        patient_informed=patient_informed,
                        interpreter_required=interpreter_required,
                        language_needed=language_needed if interpreter_required else "",
                        additional_needs=additional_needs
                    )
                
                if result['success']:
                    st.session_state['pathway_created'] = {
                        'pathway_id': result['pathway_id'],
                        'breach_date': result['breach_date']
                    }
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")


def render_all_pathways():
    """Display all pathways"""
    
    st.subheader("📋 All Pathways")
    
    # Refresh
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Get all pathways
    pathways = get_all_pathways()
    
    if not pathways:
        st.info("📁 No pathways created yet. Use 'Create Pathway' tab to start.")
        return
    
    st.write(f"**Total Pathways:** {len(pathways)}")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Active", "Closed"])
    with col2:
        type_filter = st.selectbox("Type", ["All", "RTT", "Cancer 2WW", "Cancer 62-day", "Cancer 31-day"])
    with col3:
        risk_filter = st.selectbox("Risk Level", ["All", "Breached", "Critical", "High", "Medium", "Low"])
    
    # Apply filters
    filtered = pathways
    
    if status_filter != "All":
        filtered = [p for p in filtered if p.get('status', '').lower() == status_filter.lower()]
    
    if type_filter != "All":
        type_map = {
            "RTT": "rtt",
            "Cancer 2WW": "cancer_2ww",
            "Cancer 62-day": "cancer_62day",
            "Cancer 31-day": "cancer_31day"
        }
        filtered = [p for p in filtered if p.get('pathway_type') == type_map.get(type_filter)]
    
    if risk_filter != "All":
        filtered = [p for p in filtered if p.get('risk_level', '').lower() == risk_filter.lower()]
    
    st.write(f"**Showing:** {len(filtered)} pathways")
    
    # Display pathways
    for pathway in filtered:
        render_pathway_card(pathway)


def render_pathway_card(pathway: dict):
    """Render individual pathway card"""
    
    # Risk status icon
    risk_icons = {
        'breached': '🔴',
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }
    
    risk_icon = risk_icons.get(pathway.get('risk_level', 'low'), '⚪')
    status_icon = '🟢' if pathway.get('status') == 'active' else '⚪'
    
    # Show specialty in title if available
    specialty_text = f" - {pathway.get('specialty')}" if pathway.get('specialty') else ""
    
    with st.expander(f"{risk_icon} {status_icon} {pathway.get('pathway_id')} - {pathway.get('patient_name')} ({pathway.get('pathway_name')}{specialty_text})"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Patient & Pathway:**")
            st.write(f"**Pathway ID:** {pathway.get('pathway_id')}")
            st.write(f"**Patient:** {pathway.get('patient_name')}")
            st.write(f"**Patient ID:** {pathway.get('patient_id')}")
            st.write(f"**Type:** {pathway.get('pathway_name')}")
            if pathway.get('specialty'):
                st.write(f"**🏥 Specialty:** {pathway.get('specialty')}")
            if pathway.get('consultant'):
                st.write(f"**👨‍⚕️ Consultant:** {pathway.get('consultant')}")
        
        with col2:
            st.markdown("**Timeline:**")
            st.write(f"**Start Date:** {pathway.get('start_date')}")
            st.write(f"**Breach Date:** {pathway.get('breach_date')}")
            st.write(f"**Days Elapsed:** {pathway.get('days_elapsed', 0)}")
            st.write(f"**Days Remaining:** {pathway.get('days_remaining', 0)}")
            if pathway.get('referral_source'):
                st.write(f"**📨 Referral From:** {pathway.get('referral_source')}")
        
        with col3:
            st.markdown("**Status:**")
            st.write(f"**Status:** {pathway.get('status', 'N/A').title()}")
            st.write(f"**Risk Level:** {pathway.get('risk_level', 'N/A').title()}")
            st.write(f"**Clock:** {pathway.get('clock_status', 'N/A').title()}")
            st.write(f"**Priority:** {pathway.get('priority', 'N/A')}")
        
        if pathway.get('reason'):
            st.markdown("---")
            st.markdown("**📝 Reason for Referral:**")
            st.write(pathway.get('reason'))
        
        if pathway.get('notes'):
            st.markdown("**📄 Clinical Notes:**")
            st.write(pathway.get('notes'))
        
        # Show episodes count
        episodes = get_patient_episodes(pathway.get('patient_id', ''))
        st.info(f"📋 **Episodes Linked:** {episodes.get('total_count', 0)}")


def render_manage_pathway():
    """Manage pathway - Pause/Resume, Milestones, Status"""
    
    st.subheader("⏸️ Manage Pathway")
    
    st.success("""
    **NHS Pathway Management:**
    - ⏸️ **Pause/Resume RTT Clock** - Patient unavailable, clinical reasons
    - 📅 **Record Milestones** - First appointment, DTT, treatment, discharge
    - 🔄 **Update Status** - Active, suspended, completed, removed
    """)
    
    # Get all active pathways
    all_pathways = get_all_pathways()
    active_pathways = [p for p in all_pathways if p.get('status') != 'closed']
    
    if not active_pathways:
        st.warning("📁 No active pathways found. Create a pathway first.")
        return
    
    # Select pathway to manage
    pathway_options = {
        f"{p.get('pathway_id')} - {p.get('patient_name')} ({p.get('specialty')})": p
        for p in active_pathways
    }
    
    selected_option = st.selectbox(
        "Select Pathway to Manage:",
        options=["-- Select Pathway --"] + list(pathway_options.keys())
    )
    
    if selected_option == "-- Select Pathway --":
        return
    
    selected_pathway = pathway_options[selected_option]
    
    st.markdown("---")
    st.markdown(f"### Managing: {selected_pathway.get('pathway_id')}")
    
    # Show current pathway status
    with st.expander("📋 Current Pathway Status", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"**Patient:** {selected_pathway.get('patient_name')}")
            st.write(f"**Specialty:** {selected_pathway.get('specialty')}")
        
        with col2:
            st.write(f"**Clock Status:** {selected_pathway.get('clock_status', 'N/A').title()}")
            st.write(f"**RTT Status:** {selected_pathway.get('rtt_status', 'active').title()}")
        
        with col3:
            st.write(f"**Days Elapsed:** {selected_pathway.get('days_elapsed', 0)}")
            st.write(f"**Days Remaining:** {selected_pathway.get('days_remaining', 0)}")
        
        with col4:
            st.write(f"**Breach Date:** {selected_pathway.get('breach_date')}")
            if selected_pathway.get('total_pause_days', 0) > 0:
                st.write(f"**Total Paused:** {selected_pathway.get('total_pause_days')} days")
    
    st.markdown("---")
    
    # Management tabs
    mgmt_tab1, mgmt_tab2, mgmt_tab3 = st.tabs([
        "⏸️ Clock Pause/Resume",
        "📅 Record Milestones",
        "🔄 Update Status"
    ])
    
    with mgmt_tab1:
        render_clock_management(selected_pathway)
    
    with mgmt_tab2:
        render_milestone_recording(selected_pathway)
    
    with mgmt_tab3:
        render_status_management(selected_pathway)


def render_clock_management(pathway: dict):
    """Pause or resume RTT clock"""
    
    st.markdown("### ⏸️ RTT Clock Management")
    
    is_paused = pathway.get('clock_paused', False)
    
    if is_paused:
        st.warning(f"⏸️ **Clock is PAUSED**")
        st.write(f"**Paused on:** {pathway.get('pause_start_date')}")
        st.write(f"**Reason:** {pathway.get('pause_reason')}")
        
        st.markdown("---")
        st.markdown("### ▶️ Resume Clock")
        
        with st.form("resume_clock_form"):
            resume_date = st.date_input("Resume Date*", value=date.today(),
                                       help="Date when patient becomes available again")
            
            submit = st.form_submit_button("▶️ Resume RTT Clock", type="primary")
            
            if submit:
                result = resume_pathway_clock(pathway.get('pathway_id'), str(resume_date))
                
                if result['success']:
                    st.success(f"✅ {result['message']}")
                    st.info(f"🆕 New Breach Date: **{result['new_breach_date']}**")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")
    
    else:
        st.success("▶️ **Clock is RUNNING**")
        
        st.markdown("---")
        st.markdown("### ⏸️ Pause Clock")
        
        st.info("""
        **Pause RTT clock when:**
        - Patient unavailable (holiday, personal reasons)
        - Clinical reasons (e.g., patient must lose weight first)
        - Patient declined interim appointment
        - Social/non-clinical reasons
        
        **Clock automatically extends breach date!**
        """)
        
        with st.form("pause_clock_form"):
            pause_date = st.date_input("Pause Start Date*", value=date.today())
            
            pause_reason = st.selectbox("Pause Reason*", [
                "Patient unavailable - Holiday",
                "Patient unavailable - Personal reasons",
                "Patient declined appointment",
                "Clinical - Must lose weight",
                "Clinical - Must stop smoking",
                "Clinical - Improve fitness",
                "Social reasons",
                "Other - See notes"
            ])
            
            pause_notes = st.text_area("Additional Notes", height=80)
            
            submit = st.form_submit_button("⏸️ Pause RTT Clock", type="primary")
            
            if submit:
                result = pause_pathway_clock(
                    pathway.get('pathway_id'),
                    pause_reason,
                    str(pause_date)
                )
                
                if result['success']:
                    st.success("✅ RTT clock paused successfully!")
                    st.warning("⚠️ Remember to resume clock when patient is available!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")


def render_milestone_recording(pathway: dict):
    """Record key NHS milestone dates"""
    
    st.markdown("### 📅 Record NHS Milestones")
    
    st.info("""
    **Key NHS Milestones:**
    - 📅 First Appointment
    - 🩺 Decision to Treat (DTT)
    - 💉 Treatment Start
    - 🏥 Admission
    - ⚕️ Surgery
    - 🚪 Discharge
    """)
    
    # Show recorded milestones
    with st.expander("✅ Recorded Milestones", expanded=False):
        if pathway.get('first_appointment_date'):
            st.write(f"📅 First Appointment: **{pathway.get('first_appointment_date')}** ({pathway.get('days_to_first_appointment')} days)")
        if pathway.get('decision_to_treat_date'):
            st.write(f"🩺 Decision to Treat: **{pathway.get('decision_to_treat_date')}** ({pathway.get('days_to_decision_to_treat')} days)")
        if pathway.get('treatment_start_date'):
            st.write(f"💉 Treatment: **{pathway.get('treatment_start_date')}** ({pathway.get('days_to_treatment')} days)")
        if pathway.get('admission_date'):
            st.write(f"🏥 Admission: **{pathway.get('admission_date')}**")
        if pathway.get('surgery_date'):
            st.write(f"⚕️ Surgery: **{pathway.get('surgery_date')}**")
        if pathway.get('discharge_date'):
            st.write(f"🚪 Discharge: **{pathway.get('discharge_date')}** ({pathway.get('days_to_discharge')} days)")
    
    st.markdown("---")
    
    # Record new milestone
    milestone_type = st.selectbox("Select Milestone to Record:", [
        "-- Select Milestone --",
        "first_appointment",
        "decision_to_treat",
        "treatment",
        "admission",
        "surgery",
        "discharge"
    ], format_func=lambda x: {
        "-- Select Milestone --": "-- Select Milestone --",
        "first_appointment": "📅 First Appointment",
        "decision_to_treat": "🩺 Decision to Treat (DTT)",
        "treatment": "💉 Treatment Start",
        "admission": "🏥 Admission",
        "surgery": "⚕️ Surgery",
        "discharge": "🚪 Discharge"
    }[x])
    
    if milestone_type != "-- Select Milestone --":
        with st.form(f"milestone_{milestone_type}_form"):
            milestone_date = st.date_input(f"{milestone_type.replace('_', ' ').title()} Date*", value=date.today())
            
            # Additional fields for specific milestones
            if milestone_type == 'first_appointment':
                attended = st.checkbox("Patient Attended", value=True)
            
            elif milestone_type == 'discharge':
                discharge_reason = st.selectbox("Discharge Reason", [
                    "Treatment completed",
                    "Discharged to GP",
                    "No further treatment needed",
                    "Patient declined treatment",
                    "Transferred to another provider",
                    "Other"
                ])
                
                discharge_destination = st.text_input("Discharge Destination", placeholder="e.g., GP, Community Care")
                
                outcome = st.selectbox("Treatment Outcome", [
                    "Successful", "Partially successful", "No improvement", "Declined treatment"
                ])
                
                follow_up_required = st.checkbox("Follow-up Required")
                follow_up_date = None
                if follow_up_required:
                    follow_up_date = st.date_input("Follow-up Date")
            
            submit = st.form_submit_button(f"✅ Record {milestone_type.replace('_', ' ').title()}", type="primary")
            
            if submit:
                kwargs = {}
                if milestone_type == 'first_appointment':
                    kwargs['attended'] = attended
                elif milestone_type == 'discharge':
                    kwargs['reason'] = discharge_reason
                    kwargs['destination'] = discharge_destination
                    kwargs['outcome'] = outcome
                    kwargs['follow_up_required'] = follow_up_required
                    if follow_up_required:
                        kwargs['follow_up_date'] = str(follow_up_date)
                
                result = record_milestone(
                    pathway.get('pathway_id'),
                    milestone_type,
                    str(milestone_date),
                    **kwargs
                )
                
                if result['success']:
                    st.success(f"✅ {result['message']}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")


def render_status_management(pathway: dict):
    """Update RTT pathway status"""
    
    st.markdown("### 🔄 Update RTT Status")
    
    current_status = pathway.get('rtt_status', 'active')
    st.write(f"**Current Status:** {current_status.title()}")
    
    st.info("""
    **RTT Status Codes:**
    - **Active**: Pathway in progress
    - **Paused**: Clock temporarily stopped
    - **Active Monitoring**: Patient being monitored
    - **Suspended**: Temporarily suspended
    - **Completed**: Treatment completed
    - **Removed - Died**: Patient deceased
    - **Removed - Moved**: Patient moved area
    - **Removed - Declined**: Patient declined treatment
    - **Cancelled**: Pathway cancelled
    """)
    
    new_status = st.selectbox("New Status:", [
        "active",
        "paused",
        "active_monitoring",
        "suspended",
        "completed",
        "removed_died",
        "removed_moved",
        "removed_declined",
        "cancelled"
    ], format_func=lambda x: x.replace('_', ' ').title())
    
    if st.button(f"🔄 Update Status to: {new_status.title()}", type="primary"):
        result = update_rtt_status(pathway.get('pathway_id'), new_status)
        
        if result['success']:
            st.success(f"✅ {result['message']}")
            st.rerun()
        else:
            st.error(f"❌ Failed: {result.get('error')}")


def render_pathway_timeline():
    """Render pathway timeline view"""
    
    st.subheader("📊 Pathway Timeline View")
    
    st.info("🔍 Select a patient to view their complete pathway timeline with all episodes")
    
    # Patient selector
    selected_patient = render_patient_quick_select(key_prefix="timeline")
    
    if not selected_patient:
        return
    
    patient_id = selected_patient.get('patient_id')
    
    # Get patient's pathways
    pathways = get_patient_pathways(patient_id)
    
    if not pathways:
        st.warning(f"⚠️ No pathways found for {selected_patient.get('full_name')}")
        return
    
    st.success(f"✅ Found {len(pathways)} pathway(s) for {selected_patient.get('full_name')}")
    
    # Display each pathway
    for pathway in pathways:
        st.markdown("---")
        st.markdown(f"### 📁 {pathway.get('pathway_id')} - {pathway.get('pathway_name')}")
        
        # Pathway overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Start Date", pathway.get('start_date'))
        with col2:
            st.metric("Days Elapsed", pathway.get('days_elapsed', 0))
        with col3:
            st.metric("Days Remaining", pathway.get('days_remaining', 0))
        with col4:
            risk = pathway.get('risk_level', 'low').title()
            st.metric("Risk", risk)
        
        # Get episodes for this pathway
        all_episodes = get_patient_episodes(patient_id)
        episodes = all_episodes.get('all_episodes', [])
        
        if episodes:
            st.markdown("#### 📋 Episodes Timeline:")
            
            for episode in episodes:
                episode_type = episode.get('episode_type', 'unknown')
                icon = {
                    'consultant': '👨‍⚕️',
                    'treatment': '💉',
                    'diagnostic': '🔬'
                }.get(episode_type, '📋')
                
                st.markdown(f"{icon} **{episode.get('episode_id')}** - {episode_type.title()}")
                
                if episode_type == 'consultant':
                    st.write(f"  └─ {episode.get('start_date')} - {episode.get('consultant_name')} ({episode.get('specialty')})")
                elif episode_type == 'treatment':
                    st.write(f"  └─ {episode.get('treatment_date')} - {episode.get('treatment_type')}")
                elif episode_type == 'diagnostic':
                    st.write(f"  └─ {episode.get('request_date')} - {episode.get('investigation_type')}")
        else:
            st.info("📋 No episodes added to this pathway yet")


def render_pathway_stats():
    """Display pathway statistics"""
    
    st.subheader("📈 Pathway Statistics")
    
    stats = get_pathway_stats()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pathways", stats['total_pathways'])
    
    with col2:
        st.metric("🟢 Active", stats['active_pathways'])
    
    with col3:
        st.metric("⚪ Closed", stats['closed_pathways'])
    
    with col4:
        breached = stats['breached'] + stats['critical_risk']
        st.metric("🔴 At Risk", breached)
    
    # By type
    st.markdown("---")
    st.markdown("### 📊 By Pathway Type")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📋 RTT Pathways", stats['rtt_pathways'])
    
    with col2:
        st.metric("🎗️ Cancer Pathways", stats['cancer_pathways'])
    
    # Risk breakdown
    st.markdown("---")
    st.markdown("### 🚨 Risk Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 Breached", stats['breached'])
    
    with col2:
        st.metric("🔴 Critical Risk", stats['critical_risk'])
    
    with col3:
        st.metric("🟠 High Risk", stats['high_risk'])
