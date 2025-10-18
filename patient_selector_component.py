"""
SMART PATIENT SELECTOR COMPONENT
Search and select patients with autocomplete/filter

Features:
- Search by name, NHS number, or patient ID
- Real-time filtering
- Display patient details
- Works with 1000s of patients
- Returns selected patient data

For: All modules that need patient selection
"""

import streamlit as st
from patient_registration_system import search_patients, get_all_patients


def render_patient_selector(key_prefix: str = "patient_selector") -> dict:
    """
    Render smart patient selector with search
    
    Args:
        key_prefix: Unique prefix for session state keys
    
    Returns:
        Selected patient dict or None
    """
    
    st.markdown("### 🔍 Select Patient")
    
    # Option to show all patients
    col1, col2 = st.columns([3, 1])
    with col1:
        # Search input
        search_query = st.text_input(
            "Search Patient (Name, NHS Number, or Patient ID)",
            placeholder="Type to search...",
            key=f"{key_prefix}_search",
            help="Search by patient name, NHS number, or patient ID"
        )
    with col2:
        show_all = st.checkbox("Show All", key=f"{key_prefix}_show_all")
    
    selected_patient = None
    results = []
    
    # Show all patients if checkbox is ticked
    if show_all:
        st.info("📋 Showing all registered patients...")
        results = get_all_patients()
    elif search_query:
        # Search patients
        st.write(f"🔍 Searching for: **{search_query}**")
        with st.spinner("Searching database..."):
            results = search_patients(search_query)
        st.write(f"📊 Database returned: **{len(results)}** results")
        
        # If no results from search, try getting ALL patients and filter locally
        if not results:
            st.warning(f"⚠️ Search returned 0 results. Trying alternate search...")
            all_patients = get_all_patients()
            query_lower = search_query.lower()
            results = [
                p for p in all_patients 
                if query_lower in p.get('full_name', '').lower() or
                   query_lower in p.get('nhs_number', '').lower() or
                   query_lower in p.get('patient_id', '').lower() or
                   query_lower in p.get('first_name', '').lower() or
                   query_lower in p.get('surname', '').lower()
            ]
    
    # Display results
    if results:
        st.success(f"✅ Found {len(results)} patient(s)")
        
        # Display results
        for idx, patient in enumerate(results):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.write(f"**{patient.get('full_name', 'Unknown')}**")
            
            with col2:
                st.write(f"NHS: {patient.get('nhs_number', patient.get('patient_id', 'N/A'))}")
            
            with col3:
                st.write(f"DOB: {patient.get('date_of_birth', 'N/A')}")
            
            with col4:
                if st.button("Select", key=f"{key_prefix}_select_{idx}"):
                    selected_patient = patient
                    st.session_state[f'{key_prefix}_selected'] = patient
                    st.rerun()
            
            st.markdown("---")
    
    elif search_query and not show_all:
        st.warning("⚠️ No patients found. Try different search terms or click 'Show All'.")
    
    else:
        st.info("💡 Type patient name, NHS number, or ID to search. Or click 'Show All' to see everyone.")
    
    # Show selected patient
    if f'{key_prefix}_selected' in st.session_state:
        selected_patient = st.session_state[f'{key_prefix}_selected']
        
        st.success("✅ **Selected Patient:**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Name:** {selected_patient.get('full_name', 'Unknown')}")
            st.write(f"**Patient ID:** {selected_patient.get('patient_id', 'N/A')}")
        
        with col2:
            st.write(f"**NHS Number:** {selected_patient.get('nhs_number', 'Pending')}")
            st.write(f"**DOB:** {selected_patient.get('date_of_birth', 'N/A')}")
        
        if st.button("🔄 Change Patient", key=f"{key_prefix}_change"):
            del st.session_state[f'{key_prefix}_selected']
            st.rerun()
    
    return selected_patient


def render_patient_quick_select(key_prefix: str = "quick_select") -> dict:
    """
    Render quick patient selector with recent patients
    
    Returns:
        Selected patient dict or None
    """
    
    st.markdown("### 👤 Quick Select Patient")
    
    # Get recent patients (last 20)
    all_patients = get_all_patients()
    recent_patients = all_patients[:20] if len(all_patients) > 20 else all_patients
    
    if not recent_patients:
        st.info("📝 No patients registered yet. Register a patient first.")
        return None
    
    # Create dropdown options
    patient_options = {
        f"{p.get('full_name', 'Unknown')} - {p.get('nhs_number', p.get('patient_id', 'N/A'))}": p
        for p in recent_patients
    }
    
    selected_option = st.selectbox(
        "Select from recent patients:",
        options=["-- Select Patient --"] + list(patient_options.keys()),
        key=f"{key_prefix}_dropdown"
    )
    
    if selected_option != "-- Select Patient --":
        selected_patient = patient_options[selected_option]
        
        # Show details
        with st.expander("Patient Details", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {selected_patient.get('full_name', 'Unknown')}")
                st.write(f"**Patient ID:** {selected_patient.get('patient_id', 'N/A')}")
                st.write(f"**DOB:** {selected_patient.get('date_of_birth', 'N/A')}")
            
            with col2:
                st.write(f"**NHS Number:** {selected_patient.get('nhs_number', 'Pending')}")
                st.write(f"**Gender:** {selected_patient.get('gender', 'N/A')}")
                st.write(f"**Mobile:** {selected_patient.get('phone_mobile', 'N/A')}")
        
        return selected_patient
    
    return None


def render_pathway_selector(patient_id: str = None, key_prefix: str = "pathway_selector") -> dict:
    """
    Render pathway selector
    
    Args:
        patient_id: If provided, only show pathways for this patient
        key_prefix: Unique prefix for session state keys
    
    Returns:
        Selected pathway dict or None
    """
    from pathway_management_system import get_patient_pathways, get_all_pathways
    
    st.markdown("### 📁 Select Pathway")
    
    # Check if pathway was selected from Pathway Management
    if 'selected_pathway_for_episode' in st.session_state:
        saved_pathway = st.session_state['selected_pathway_for_episode']
        st.success(f"✅ Pathway pre-selected: **{saved_pathway.get('pathway_id')}** - {saved_pathway.get('patient_name')}")
        st.info("💡 This pathway was selected from Pathway Management. Change it below if needed.")
    
    # Get pathways
    if patient_id:
        pathways = get_patient_pathways(patient_id)
        if not pathways:
            st.info("📁 No pathways for this patient yet. Create a pathway first.")
            return None
    else:
        pathways = get_all_pathways()
        if not pathways:
            st.info("📁 No pathways created yet.")
            return None
    
    # Filter active pathways only (optional)
    show_closed = st.checkbox("Show closed pathways", value=False, key=f"{key_prefix}_show_closed")
    
    if not show_closed:
        pathways = [p for p in pathways if p.get('status') == 'active']
    
    if not pathways:
        st.warning("⚠️ No active pathways found.")
        return None
    
    # Create dropdown options
    pathway_options = {
        f"{p.get('pathway_id', 'N/A')} - {p.get('patient_name', 'Unknown')} ({p.get('pathway_name', 'Unknown')})": p
        for p in pathways
    }
    
    # Determine default selection
    default_index = 0  # "-- Select Pathway --"
    if 'selected_pathway_for_episode' in st.session_state:
        saved_pathway = st.session_state['selected_pathway_for_episode']
        saved_pathway_id = saved_pathway.get('pathway_id')
        # Find matching pathway in options
        for idx, (option_text, pathway) in enumerate(pathway_options.items(), start=1):
            if pathway.get('pathway_id') == saved_pathway_id:
                default_index = idx
                break
    
    selected_option = st.selectbox(
        "Select pathway:",
        options=["-- Select Pathway --"] + list(pathway_options.keys()),
        index=default_index,
        key=f"{key_prefix}_dropdown"
    )
    
    if selected_option != "-- Select Pathway --":
        selected_pathway = pathway_options[selected_option]
        
        # Show details
        with st.expander("Pathway Details", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Pathway ID:** {selected_pathway.get('pathway_id', 'N/A')}")
                st.write(f"**Patient:** {selected_pathway.get('patient_name', 'Unknown')}")
                st.write(f"**Type:** {selected_pathway.get('pathway_name', 'Unknown')}")
                st.write(f"**Start Date:** {selected_pathway.get('start_date', 'N/A')}")
            
            with col2:
                st.write(f"**Status:** {selected_pathway.get('status', 'N/A')}")
                st.write(f"**Days Elapsed:** {selected_pathway.get('days_elapsed', 0)}")
                st.write(f"**Days Remaining:** {selected_pathway.get('days_remaining', 0)}")
                st.write(f"**Risk:** {selected_pathway.get('risk_level', 'N/A')}")
        
        return selected_pathway
    
    return None
