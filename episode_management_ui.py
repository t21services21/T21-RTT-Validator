"""
T21 EPISODE MANAGEMENT UI
User interface for managing consultant, treatment, and diagnostic episodes
"""

import streamlit as st
from datetime import datetime, date
from episode_management_system import (
    add_consultant_episode,
    add_treatment_episode,
    add_diagnostic_episode,
    get_patient_episodes,
    get_all_episodes,
    close_consultant_episode,
    get_episode_stats,
    update_episode,
    delete_episode,
    move_episode_to_pathway,
    get_episode_by_id
)
from success_message_component import show_huge_success
from patient_selector_component import render_patient_selector, render_pathway_selector


SPECIALTIES = [
    "Cardiology", "Dermatology", "ENT", "Gastroenterology",
    "General Surgery", "Neurology", "Ophthalmology", "Orthopaedics",
    "Respiratory", "Rheumatology", "Urology", "Other"
]


def render_episode_management():
    """Main episode management interface"""
    
    st.header("📋 Episode Management System")
    st.markdown("**Track Consultant, Treatment & Diagnostic Episodes**")
    
    st.success("""
    📋 **Episode Management Features:**
    - 👨‍⚕️ Consultant Episodes - Track patient under consultant care
    - 💉 Treatment Episodes - Record treatments and procedures
    - 🔬 Diagnostic Episodes - Manage investigations and tests
    - ⏱️ Episode Timeline - View patient journey
    - 📊 Episode Statistics - Track activity
    - 🔗 Link to RTT Pathways
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👨‍⚕️ Add Consultant Episode",
        "💉 Add Treatment Episode",
        "🔬 Add Diagnostic Episode",
        "📋 View All Episodes",
        "✏️ Manage Episodes",
        "📊 Episode Statistics"
    ])
    
    with tab1:
        render_add_consultant_episode()
    
    with tab2:
        render_add_treatment_episode()
    
    with tab3:
        render_add_diagnostic_episode()
    
    with tab4:
        render_view_episodes()
    
    with tab5:
        render_manage_episodes()
    
    with tab6:
        render_episode_stats()


def render_add_consultant_episode():
    """Add new consultant episode"""
    
    st.subheader("👨‍⚕️ Add Consultant Episode")
    
    st.info("""
    **Consultant Episode:** Period when patient is under the care of a consultant.
    
    Key points:
    - Episode starts when patient referred to consultant
    - Episode ends when patient discharged or transferred
    - Used for RTT clock tracking
    - Can have multiple episodes for same patient (different consultants/specialties)
    """)
    
    # Success message - ENHANCED
    if 'consultant_episode_added' in st.session_state:
        episode_id = st.session_state['consultant_episode_added']
        
        show_huge_success(
            title="CONSULTANT EPISODE CREATED!",
            subtitle="Episode saved to database",
            details={"Episode ID": episode_id, "Status": "Active"},
            next_steps="You can now add treatments and diagnostics to this episode."
        )
        del st.session_state['consultant_episode_added']
    
    # SMART PATIENT SELECTOR (with search!)
    st.markdown("---")
    selected_patient = render_patient_selector(key_prefix="consultant_episode")
    
    if not selected_patient:
        st.warning("⚠️ Please search and select a patient first")
        return
    
    patient_id = selected_patient.get('patient_id')
    patient_name = selected_patient.get('full_name')
    
    st.markdown("---")
    
    # OPTIONAL: Link to pathway
    st.markdown("### 🔗 Link to Pathway (Optional)")
    selected_pathway = render_pathway_selector(patient_id=patient_id, key_prefix="consultant_pathway")
    pathway_id = selected_pathway.get('pathway_id') if selected_pathway else None
    
    st.markdown("---")
    
    with st.form("add_consultant_episode"):
        
        st.markdown("### Episode Details")
        col1, col2 = st.columns(2)
        with col1:
            consultant_name = st.text_input("Consultant Name*", placeholder="Dr. Smith")
            specialty = st.selectbox("Specialty*", SPECIALTIES)
            start_date = st.date_input("Episode Start Date*", value=date.today())
            episode_code = st.text_input("Episode Code", placeholder="e.g., 10, AA10, 20C",
                                        help="HRG code, procedure code, or episode identifier")
        
        with col2:
            priority = st.selectbox("Priority", ["Routine", "Urgent", "2WW", "Cancer"])
            referral_source = st.selectbox("Referral Source", ["GP", "Consultant", "A&E", "Dentist", "Optician"])
            expected_duration = st.number_input("Expected Duration (weeks)", min_value=1, max_value=52, value=12)
        
        reason = st.text_area("Reason for Referral*", height=100, 
                             placeholder="Why is patient being referred to consultant?")
        
        notes = st.text_area("Clinical Notes", height=100)
        
        submit = st.form_submit_button("✅ Create Consultant Episode", type="primary")
        
        if submit:
            if not consultant_name or not reason:
                st.error("❌ Please fill all required fields")
            else:
                result = add_consultant_episode(
                    patient_id=patient_id,
                    patient_name=patient_name,
                    consultant_name=consultant_name,
                    specialty=specialty,
                    start_date=str(start_date),
                    reason=reason,
                    expected_duration_weeks=expected_duration,
                    priority=priority,
                    referral_source=referral_source,
                    pathway_id=pathway_id if pathway_id else None,
                    notes=notes,
                    episode_code=episode_code
                )
                
                if result['success']:
                    st.session_state['consultant_episode_added'] = result['episode_id']
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")


def render_add_treatment_episode():
    """Add new treatment episode"""
    
    st.subheader("💉 Add Treatment Episode")
    
    st.info("""
    **Treatment Episode:** Record of a specific treatment, procedure, or surgery.
    
    Examples:
    - Surgery (e.g., Hip replacement)
    - Chemotherapy session
    - Radiotherapy course
    - Minor procedure (e.g., Endoscopy)
    """)
    
    # Success message - ENHANCED
    if 'treatment_episode_added' in st.session_state:
        episode_id = st.session_state['treatment_episode_added']
        
        show_huge_success(
            title="TREATMENT EPISODE CREATED!",
            subtitle="Treatment details recorded permanently",
            details={"Episode ID": episode_id, "Status": "Active"},
            next_steps="Treatment episode has been saved to the database."
        )
        del st.session_state['treatment_episode_added']
    
    with st.form("add_treatment_episode"):
        st.markdown("### Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Patient ID / NHS Number*", placeholder="TEMP_2025... or NHS number")
        with col2:
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
        
        st.markdown("### Treatment Details")
        col1, col2 = st.columns(2)
        with col1:
            treatment_type = st.text_input("Treatment Type*", placeholder="e.g., Hip Replacement Surgery")
            treatment_date = st.date_input("Treatment Date*", value=date.today())
            location = st.text_input("Location*", placeholder="Theatre 2, Main Hospital")
        
        with col2:
            provider = st.text_input("Provider (Surgeon/Consultant)*", placeholder="Mr. Johnson")
            consultant_episode_id = st.text_input("Link to Consultant Episode (Optional)", 
                                                  placeholder="CE_...")
            pathway_id = st.text_input("Link to Pathway (Optional)", placeholder="PATHWAY_...")
        
        outcome = st.text_area("Treatment Outcome", height=100,
                              placeholder="Result of treatment (leave empty if scheduled)")
        
        complications = st.text_area("Complications (if any)", height=80)
        
        notes = st.text_area("Additional Notes", height=80)
        
        submit = st.form_submit_button("✅ Create Treatment Episode", type="primary")
        
        if submit:
            if not patient_id or not patient_name or not treatment_type or not provider:
                st.error("❌ Please fill all required fields")
            else:
                result = add_treatment_episode(
                    patient_id=patient_id,
                    patient_name=patient_name,
                    treatment_type=treatment_type,
                    treatment_date=str(treatment_date),
                    location=location,
                    provider=provider,
                    consultant_episode_id=consultant_episode_id if consultant_episode_id else None,
                    pathway_id=pathway_id if pathway_id else None,
                    outcome=outcome,
                    complications=complications,
                    notes=notes
                )
                
                if result['success']:
                    st.session_state['treatment_episode_added'] = result['episode_id']
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")


def render_add_diagnostic_episode():
    """Add new diagnostic episode"""
    
    st.subheader("🔬 Add Diagnostic Episode")
    
    st.info("""
    **Diagnostic Episode:** Investigation or test ordered for patient.
    
    Examples:
    - Blood tests
    - X-rays, CT, MRI scans
    - Endoscopy
    - Biopsy
    - ECG, Echocardiogram
    """)
    
    # Success message - ENHANCED
    if 'diagnostic_episode_added' in st.session_state:
        episode_id = st.session_state['diagnostic_episode_added']
        
        show_huge_success(
            title="DIAGNOSTIC EPISODE CREATED!",
            subtitle="Diagnostic details recorded permanently",
            details={"Episode ID": episode_id, "Status": "Active"},
            next_steps="Diagnostic episode has been saved to the database."
        )
        del st.session_state['diagnostic_episode_added']
    
    with st.form("add_diagnostic_episode"):
        st.markdown("### Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Patient ID / NHS Number*", placeholder="TEMP_2025... or NHS number")
        with col2:
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
        
        st.markdown("### Investigation Details")
        col1, col2 = st.columns(2)
        with col1:
            investigation_type = st.selectbox("Investigation Type*", [
                "Blood Tests", "X-Ray", "CT Scan", "MRI Scan", "Ultrasound",
                "Endoscopy", "Colonoscopy", "Biopsy", "ECG", "Echocardiogram",
                "Spirometry", "Other"
            ])
            request_date = st.date_input("Request Date*", value=date.today())
            requested_by = st.text_input("Requested By*", placeholder="Dr. Smith")
        
        with col2:
            urgency = st.selectbox("Urgency", ["Routine", "Urgent", "2WW"])
            performed_date = st.date_input("Performed Date (if done)", value=None)
            location = st.text_input("Location", placeholder="Radiology Department")
        
        results = st.text_area("Results (if available)", height=150,
                              placeholder="Investigation findings...")
        
        consultant_episode_id = st.text_input("Link to Consultant Episode (Optional)", placeholder="CE_...")
        pathway_id = st.text_input("Link to Pathway (Optional)", placeholder="PATHWAY_...")
        
        notes = st.text_area("Additional Notes", height=80)
        
        submit = st.form_submit_button("✅ Create Diagnostic Episode", type="primary")
        
        if submit:
            if not patient_id or not patient_name or not requested_by:
                st.error("❌ Please fill all required fields")
            else:
                result = add_diagnostic_episode(
                    patient_id=patient_id,
                    patient_name=patient_name,
                    investigation_type=investigation_type,
                    request_date=str(request_date),
                    requested_by=requested_by,
                    performed_date=str(performed_date) if performed_date else None,
                    results=results,
                    consultant_episode_id=consultant_episode_id if consultant_episode_id else None,
                    pathway_id=pathway_id if pathway_id else None,
                    urgency=urgency,
                    location=location,
                    notes=notes
                )
                
                if result['success']:
                    st.session_state['diagnostic_episode_added'] = result['episode_id']
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")


def render_view_episodes():
    """View all episodes"""
    
    st.subheader("📋 All Episodes")
    
    # Refresh
    if st.button("🔄 Refresh", key="refresh_episodes_btn"):
        st.rerun()
    
    episodes = get_all_episodes()
    
    if not episodes:
        st.info("📋 No episodes recorded yet. Use the tabs above to add episodes.")
        return
    
    st.write(f"**Total Episodes:** {len(episodes)}")
    
    # Filter
    filter_type = st.selectbox("Filter by Type", ["All", "Consultant", "Treatment", "Diagnostic"])
    
    if filter_type != "All":
        episodes = [e for e in episodes if e.get('episode_type', '').lower() == filter_type.lower()]
    
    # Display episodes
    for episode in episodes:
        episode_type = episode.get('episode_type', 'unknown')
        
        icon = {
            'consultant': '👨‍⚕️',
            'treatment': '💉',
            'diagnostic': '🔬'
        }.get(episode_type, '📋')
        
        status_color = {
            'active': '🟢',
            'closed': '⚪',
            'completed': '✅',
            'scheduled': '🕐',
            'requested': '⏰'
        }.get(episode.get('status', ''), '⚫')
        
        with st.expander(f"{icon} {episode.get('episode_id')} - {episode.get('patient_name')} ({episode_type.title()}) {status_color}"):
            if episode_type == 'consultant':
                render_consultant_episode_details(episode)
            elif episode_type == 'treatment':
                render_treatment_episode_details(episode)
            elif episode_type == 'diagnostic':
                render_diagnostic_episode_details(episode)


def render_consultant_episode_details(episode: dict):
    """Display consultant episode details"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Episode ID:** {episode.get('episode_id')}")
        st.write(f"**Patient:** {episode.get('patient_name')}")
        st.write(f"**Consultant:** {episode.get('consultant_name')}")
        st.write(f"**Specialty:** {episode.get('specialty')}")
        st.write(f"**Start Date:** {episode.get('start_date')}")
        st.write(f"**Status:** {episode.get('status')}")
    
    with col2:
        st.write(f"**Priority:** {episode.get('priority')}")
        st.write(f"**Referral Source:** {episode.get('referral_source')}")
        st.write(f"**Expected Duration:** {episode.get('expected_duration_weeks')} weeks")
        if episode.get('end_date'):
            st.write(f"**End Date:** {episode.get('end_date')}")
        if episode.get('pathway_id'):
            st.write(f"**Pathway:** {episode.get('pathway_id')}")
    
    if episode.get('reason'):
        st.markdown(f"**Reason:** {episode.get('reason')}")
    
    if episode.get('notes'):
        st.markdown(f"**Notes:** {episode.get('notes')}")


def render_treatment_episode_details(episode: dict):
    """Display treatment episode details"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Episode ID:** {episode.get('episode_id')}")
        st.write(f"**Patient:** {episode.get('patient_name')}")
        st.write(f"**Treatment:** {episode.get('treatment_type')}")
        st.write(f"**Date:** {episode.get('treatment_date')}")
        st.write(f"**Provider:** {episode.get('provider')}")
    
    with col2:
        st.write(f"**Location:** {episode.get('location')}")
        st.write(f"**Status:** {episode.get('status')}")
        if episode.get('consultant_episode_id'):
            st.write(f"**Consultant Episode:** {episode.get('consultant_episode_id')}")
    
    if episode.get('outcome'):
        st.markdown(f"**Outcome:** {episode.get('outcome')}")
    
    if episode.get('complications'):
        st.warning(f"**Complications:** {episode.get('complications')}")


def render_diagnostic_episode_details(episode: dict):
    """Display diagnostic episode details"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Episode ID:** {episode.get('episode_id')}")
        st.write(f"**Patient:** {episode.get('patient_name')}")
        st.write(f"**Investigation:** {episode.get('investigation_type')}")
        st.write(f"**Request Date:** {episode.get('request_date')}")
        st.write(f"**Requested By:** {episode.get('requested_by')}")
    
    with col2:
        st.write(f"**Urgency:** {episode.get('urgency')}")
        st.write(f"**Status:** {episode.get('status')}")
        if episode.get('performed_date'):
            st.write(f"**Performed:** {episode.get('performed_date')}")
        if episode.get('location'):
            st.write(f"**Location:** {episode.get('location')}")
    
    if episode.get('results'):
        st.markdown(f"**Results:** {episode.get('results')}")


def render_manage_episodes():
    """Manage episodes - Edit, Delete, Move"""
    
    st.subheader("✏️ Manage Episodes")
    
    st.info("""
    **Episode Management:**
    - ✏️ **Edit Episode** - Update episode code, details, or fix mistakes
    - 🗑️ **Delete Episode** - Remove incorrect episodes
    - 🔀 **Move Episode** - Transfer episode to different pathway
    """)
    
    # Get all episodes
    all_episodes = get_all_episodes()
    
    if not all_episodes:
        st.warning("📋 No episodes found. Create episodes first.")
        return
    
    # Filter out deleted episodes
    active_episodes = [e for e in all_episodes if e.get('status') != 'deleted']
    
    if not active_episodes:
        st.warning("📋 No active episodes found.")
        return
    
    st.write(f"**Total Active Episodes:** {len(active_episodes)}")
    
    # Check if episode was pre-selected from Pathway Management
    if 'edit_episode' in st.session_state:
        preselected_ep = st.session_state['edit_episode']
        st.success(f"✅ Episode pre-selected: **{preselected_ep.get('episode_id')}** from Pathway Management")
        st.info("💡 This episode was selected from Pathway view. Change selection below if needed.")
    
    # Select episode to manage
    episode_options = {
        f"{e.get('episode_id')} - {e.get('patient_name')} ({e.get('episode_type').title()})": e
        for e in active_episodes
    }
    
    # Determine default selection
    default_index = 0
    if 'edit_episode' in st.session_state:
        preselected_id = st.session_state['edit_episode'].get('episode_id')
        for idx, (option_text, episode) in enumerate(episode_options.items(), start=1):
            if episode.get('episode_id') == preselected_id:
                default_index = idx
                break
    
    selected_option = st.selectbox(
        "Select Episode to Manage:",
        options=["-- Select Episode --"] + list(episode_options.keys()),
        index=default_index
    )
    
    if selected_option == "-- Select Episode --":
        return
    
    selected_episode = episode_options[selected_option]
    
    # Clear the pre-selection after first load
    if 'edit_episode' in st.session_state:
        del st.session_state['edit_episode']
    
    st.markdown("---")
    st.markdown(f"### Managing: {selected_episode.get('episode_id')}")
    
    # Show current episode details
    with st.expander("📋 Current Episode Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Episode ID:** {selected_episode.get('episode_id')}")
            st.write(f"**Type:** {selected_episode.get('episode_type').title()}")
            st.write(f"**Patient:** {selected_episode.get('patient_name')}")
        
        with col2:
            st.write(f"**Status:** {selected_episode.get('status')}")
            if selected_episode.get('episode_code'):
                st.write(f"**Episode Code:** {selected_episode.get('episode_code')}")
            # SHOW EPISODE CODE (HRG Code)
            episode_code = selected_episode.get('episode_code', 'N/A')
            if episode_code and episode_code != 'N/A':
                st.write(f"**📋 Episode/HRG Code:** {episode_code}")
            else:
                st.write(f"**📋 Episode/HRG Code:** Not set")
            if selected_episode.get('pathway_id'):
                st.write(f"**Pathway:** {selected_episode.get('pathway_id')}")
        
        with col3:
            if selected_episode.get('specialty'):
                st.write(f"**Specialty:** {selected_episode.get('specialty')}")
            if selected_episode.get('consultant_name'):
                st.write(f"**Consultant:** {selected_episode.get('consultant_name')}")
    
    st.markdown("---")
    
    # Management actions
    action_tab1, action_tab2, action_tab3 = st.tabs([
        "✏️ Edit Episode",
        "🔀 Move to Pathway",
        "🗑️ Delete Episode"
    ])
    
    with action_tab1:
        st.markdown("### ✏️ Edit Episode Details")
        
        with st.form("edit_episode_form"):
            st.info("Update episode code, dates, or other details. Fix any mistakes here!")
            
            col_edit1, col_edit2 = st.columns(2)
            
            with col_edit1:
                new_episode_code = st.text_input(
                    "Episode Code",
                    value=selected_episode.get('episode_code', ''),
                    placeholder="e.g., 10, AA10, 20C"
                )
                
                # Note: RTT codes are set on RTT PATHWAYS, not episodes
                # Episodes use episode_code (HRG codes) instead
            
            with col_edit2:
                # DATE EDIT
                from datetime import datetime
                try:
                    current_date = datetime.strptime(selected_episode.get('start_date'), '%Y-%m-%d').date()
                except:
                    current_date = datetime.now().date()
                
                new_date = st.date_input(
                    "Episode Date",
                    value=current_date,
                    help="Fix date if incorrect"
                )
                
                # END DATE EDIT (if applicable)
                if selected_episode.get('end_date'):
                    try:
                        current_end_date = datetime.strptime(selected_episode.get('end_date'), '%Y-%m-%d').date()
                        new_end_date = st.date_input(
                            "End Date",
                            value=current_end_date,
                            help="Update end date if needed"
                        )
                    except:
                        new_end_date = None
                else:
                    new_end_date = None
            
            new_notes = st.text_area(
                "Clinical Notes",
                value=selected_episode.get('notes', ''),
                height=100
            )
            
            if selected_episode.get('episode_type') == 'consultant':
                new_consultant = st.text_input(
                    "Consultant Name",
                    value=selected_episode.get('consultant_name', '')
                )
                new_specialty = st.selectbox(
                    "Specialty",
                    options=SPECIALTIES,
                    index=SPECIALTIES.index(selected_episode.get('specialty', 'Other')) if selected_episode.get('specialty') in SPECIALTIES else 0
                )
            
            submit_edit = st.form_submit_button("💾 Save Changes", type="primary")
            
            if submit_edit:
                update_data = {
                    'episode_code': new_episode_code,
                    'notes': new_notes,
                    'start_date': str(new_date)
                }
                
                if new_end_date:
                    update_data['end_date'] = str(new_end_date)
                
                if selected_episode.get('episode_type') == 'consultant':
                    update_data['consultant_name'] = new_consultant
                    update_data['specialty'] = new_specialty
                
                result = update_episode(selected_episode.get('episode_id'), update_data)
                
                if result['success']:
                    st.balloons()
                    st.success("""
                    ✅ **EPISODE UPDATED SUCCESSFULLY!**
                    
                    ✔️ All changes have been saved!  
                    📊 Episode information updated in database!
                    """)
                    st.rerun()
                else:
                    st.error(f"❌ Update failed: {result.get('error')}")
    
    with action_tab2:
        st.markdown("### 🔀 Move Episode to Different Pathway")
        
        st.warning("⚠️ Moving episode will unlink it from current pathway and link to new pathway.")
        
        # Show current pathway
        if selected_episode.get('pathway_id'):
            st.info(f"**Current Pathway:** {selected_episode.get('pathway_id')}")
        else:
            st.info("**Current Pathway:** Not linked to any pathway")
        
        # Select new pathway
        new_pathway = render_pathway_selector(
            patient_id=selected_episode.get('patient_id'),
            key_prefix=f"move_episode_{selected_episode.get('episode_id')}"
        )
        
        if new_pathway:
            st.success(f"✅ Selected New Pathway: **{new_pathway.get('pathway_id')}**")
            
            if st.button("🔀 Move Episode to This Pathway", type="primary"):
                result = move_episode_to_pathway(
                    selected_episode.get('episode_id'),
                    new_pathway.get('pathway_id')
                )
                
                if result['success']:
                    st.balloons()
                    st.success("""
                    ✅ **EPISODE MOVED SUCCESSFULLY!**
                    
                    ✔️ Episode has been moved to new pathway!  
                    🔀 Pathway link updated!
                    """)
                    st.rerun()
                else:
                    st.error(f"❌ Move failed: {result.get('error')}")
    
    with action_tab3:
        st.markdown("### 🗑️ Delete Episode")
        
        st.error("""
        ⚠️ **WARNING: This will delete the episode!**
        
        The episode will be marked as deleted and removed from all views.
        This action cannot be undone easily.
        """)
        
        st.write(f"**Episode to Delete:** {selected_episode.get('episode_id')}")
        st.write(f"**Patient:** {selected_episode.get('patient_name')}")
        st.write(f"**Type:** {selected_episode.get('episode_type').title()}")
        
        confirm = st.text_input(
            'Type "DELETE" to confirm:',
            key=f"delete_confirm_{selected_episode.get('episode_id')}"
        )
        
        if st.button("🗑️ DELETE EPISODE", type="primary", disabled=(confirm != "DELETE")):
            result = delete_episode(selected_episode.get('episode_id'))
            
            if result['success']:
                show_huge_success(
                    title="EPISODE DELETED!",
                    subtitle="Episode removed from database",
                    next_steps="The episode has been permanently deleted."
                )
                st.rerun()
            else:
                st.error(f"❌ Delete failed: {result.get('error')}")


def render_episode_stats():
    """Display episode statistics"""
    
    st.subheader("📊 Episode Statistics")
    
    stats = get_episode_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Episodes", stats['total_episodes'])
        st.metric("👨‍⚕️ Consultant", stats['consultant_episodes'])
    
    with col2:
        st.metric("💉 Treatment", stats['treatment_episodes'])
        st.metric("🔬 Diagnostic", stats['diagnostic_episodes'])
    
    with col3:
        st.metric("🟢 Active", stats['active_episodes'])
        st.metric("⚪ Closed", stats['closed_episodes'])
