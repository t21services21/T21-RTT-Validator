"""
UNIFIED PATIENT RECORD UI
Search and view patient data across ALL modules
"""

import streamlit as st
from datetime import datetime
from unified_patient_system import find_patient_by_nhs, search_patients, get_patient_summary


def render_unified_patient_search():
    """Main unified patient search interface"""
    
    st.header("🔍 Unified Patient Search")
    st.markdown("**Search for any patient across ALL modules**")
    
    st.success("""
    📋 **Unified Patient Record Features:**
    - Search across PTL, Cancer, MDT, and Appointments
    - Complete patient timeline
    - All clinical events in one view
    - Quick access to all module data
    """)
    
    # Search bar
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search Patient", placeholder="Enter NHS number or patient name", key="unified_search")
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if search_query or search_button:
        if len(search_query) >= 3:
            # Perform search
            results = search_patients(search_query)
            
            if results:
                st.markdown(f"### Found {len(results)} patient(s)")
                
                for result in results[:20]:  # Limit to 20 results
                    with st.expander(f"👤 {result['patient_name']} (NHS: {result['nhs_number']})"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown(f"**Name:** {result['patient_name']}")
                            st.markdown(f"**NHS Number:** {result['nhs_number']}")
                            st.markdown(f"**Status:** {result.get('status', 'Unknown')}")
                        
                        with col_b:
                            modules_badges = ' '.join([f"🏷️ {m}" for m in result['modules']])
                            st.markdown(f"**Found in:** {modules_badges}")
                            st.markdown(f"**Latest Activity:** {result.get('latest_activity', 'N/A')}")
                        
                        if st.button("👁️ View Full Record", key=f"view_{result['nhs_number']}", use_container_width=True):
                            st.session_state['viewing_patient_nhs'] = result['nhs_number']
                            st.rerun()
            else:
                st.warning(f"⚠️ No patients found matching '{search_query}'")
        else:
            st.info("💡 Enter at least 3 characters to search")
    
    # View full patient record if selected
    if st.session_state.get('viewing_patient_nhs'):
        st.markdown("---")
        render_patient_full_record(st.session_state['viewing_patient_nhs'])


def render_patient_full_record(nhs_number: str):
    """Display complete patient record from all modules"""
    
    # Back button
    if st.button("⬅️ Back to Search"):
        del st.session_state['viewing_patient_nhs']
        st.rerun()
    
    # Load unified record
    with st.spinner("Loading complete patient record..."):
        unified = find_patient_by_nhs(nhs_number)
    
    if not unified:
        st.error("❌ Patient not found")
        return
    
    # Header
    st.markdown(f"## 👤 {unified['patient_name']}")
    st.markdown(f"**NHS Number:** {unified['nhs_number']}")
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Modules", len(unified['found_in']))
    with col2:
        st.metric("Total Events", len(unified['timeline']))
    with col3:
        st.metric("MDT Discussions", len(unified['mdt_appearances']))
    with col4:
        st.metric("Appointments", len(unified['appointments']))
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📅 Timeline",
        "📋 PTL Record",
        "🎗️ Cancer Record",
        "👥 MDT History",
        "🗓️ Appointments",
        "📁 Documents"
    ])
    
    with tab1:
        render_patient_timeline(unified)
    
    with tab2:
        render_ptl_record(unified)
    
    with tab3:
        render_cancer_record(unified)
    
    with tab4:
        render_mdt_history(unified)
    
    with tab5:
        render_appointments_history(unified)
    
    with tab6:
        render_patient_documents(unified)


def render_patient_timeline(unified: dict):
    """Render patient timeline"""
    st.markdown("### 📅 Complete Patient Timeline")
    
    if not unified['timeline']:
        st.info("📅 No timeline events found")
        return
    
    st.markdown(f"**{len(unified['timeline'])} events recorded**")
    
    for event in unified['timeline']:
        date = event.get('date', 'Unknown date')
        event_name = event.get('event', 'Unknown event')
        module = event.get('module', 'Unknown')
        details = event.get('details', '')
        
        # Color code by module
        if module == 'PTL':
            icon = "📋"
            color = "#4CAF50"
        elif module == 'Cancer':
            icon = "🎗️"
            color = "#FF5722"
        elif module == 'MDT':
            icon = "👥"
            color = "#2196F3"
        elif module == 'Appointments':
            icon = "🗓️"
            color = "#9C27B0"
        else:
            icon = "📌"
            color = "#607D8B"
        
        with st.container():
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding-left: 15px; margin-bottom: 15px;">
                <strong>{icon} {date}</strong> - {event_name}<br>
                <small style="color: gray;">Module: {module}</small><br>
                {details}
            </div>
            """, unsafe_allow_html=True)


def render_ptl_record(unified: dict):
    """Render PTL record details"""
    st.markdown("### 📋 PTL Record")
    
    ptl = unified.get('ptl_record')
    
    if not ptl:
        st.info("ℹ️ Patient not on PTL")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Patient ID:** {ptl.get('patient_id', 'N/A')}")
        st.markdown(f"**Specialty:** {ptl.get('specialty', 'N/A')}")
        st.markdown(f"**Priority:** {ptl.get('priority', 'N/A')}")
        st.markdown(f"**Referral Date:** {ptl.get('referral_date', 'N/A')}")
        st.markdown(f"**Referral Source:** {ptl.get('referral_source', 'N/A')}")
    
    with col2:
        st.markdown(f"**Current Status:** {ptl.get('current_status', 'N/A')}")
        st.markdown(f"**Consultant:** {ptl.get('consultant', 'N/A')}")
        st.markdown(f"**Contact:** {ptl.get('contact_number', 'N/A')}")
        st.markdown(f"**Clock Status:** {ptl.get('clock_status', 'N/A')}")
        st.markdown(f"**RTT Code:** {ptl.get('rtt_code', 'N/A')}")
    
    if ptl.get('notes'):
        st.markdown("**Notes:**")
        st.info(ptl.get('notes'))


def render_cancer_record(unified: dict):
    """Render cancer pathway record"""
    st.markdown("### 🎗️ Cancer Pathway Record")
    
    cancer = unified.get('cancer_record')
    
    if not cancer:
        st.info("ℹ️ Patient not on cancer pathway")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Pathway ID:** {cancer.get('pathway_id', 'N/A')}")
        st.markdown(f"**Cancer Type:** {cancer.get('cancer_type', 'N/A')}")
        st.markdown(f"**Pathway Type:** {cancer.get('pathway_type', 'N/A')}")
        st.markdown(f"**Referral Date:** {cancer.get('referral_date', 'N/A')}")
        st.markdown(f"**Target Date:** {cancer.get('target_date', 'N/A')}")
    
    with col2:
        st.markdown(f"**Current Status:** {cancer.get('current_status', 'N/A')}")
        st.markdown(f"**Milestones:** {len(cancer.get('milestones', []))}")
        st.markdown(f"**Treatments:** {len(cancer.get('treatments', []))}")
    
    # Milestones
    milestones = cancer.get('milestones', [])
    if milestones:
        st.markdown("**Milestones:**")
        for milestone in milestones:
            st.markdown(f"- **{milestone.get('date')}:** {milestone.get('milestone')} - {milestone.get('description')}")
    
    if cancer.get('notes'):
        st.markdown("**Notes:**")
        st.info(cancer.get('notes'))


def render_mdt_history(unified: dict):
    """Render MDT discussion history"""
    st.markdown("### 👥 MDT Discussion History")
    
    mdt_list = unified.get('mdt_appearances', [])
    
    if not mdt_list:
        st.info("ℹ️ Patient not discussed in any MDT")
        return
    
    st.markdown(f"**Patient discussed in {len(mdt_list)} MDT meeting(s)**")
    
    for mdt in mdt_list:
        discussed = mdt.get('discussed', False)
        status_icon = "✅" if discussed else "⏳"
        
        with st.expander(f"{status_icon} {mdt.get('specialty', 'Unknown')} MDT - {mdt.get('meeting_date', 'Unknown date')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Meeting ID:** {mdt.get('meeting_id', 'N/A')}")
                st.markdown(f"**Date:** {mdt.get('meeting_date', 'N/A')}")
                st.markdown(f"**Specialty:** {mdt.get('specialty', 'N/A')}")
                st.markdown(f"**Diagnosis:** {mdt.get('diagnosis', 'N/A')}")
            
            with col2:
                if discussed:
                    st.markdown(f"**Outcome:** {mdt.get('outcome', 'N/A')}")
                    st.markdown(f"**Decision:** {mdt.get('decision', 'N/A')}")
                    st.success("✅ Outcome Recorded")
                else:
                    st.warning("⏳ Outcome Not Recorded")


def render_appointments_history(unified: dict):
    """Render appointment history"""
    st.markdown("### 🗓️ Appointment History")
    
    appointments = unified.get('appointments', [])
    
    if not appointments:
        st.info("ℹ️ No appointments found")
        return
    
    st.markdown(f"**{len(appointments)} appointment(s) found**")
    
    for appt in appointments:
        status = appt.get('status', 'Unknown')
        
        if status.lower() == 'confirmed':
            status_icon = "🟢"
        elif status.lower() == 'completed':
            status_icon = "✅"
        elif status.lower() == 'cancelled':
            status_icon = "🔴"
        else:
            status_icon = "⚪"
        
        with st.expander(f"{status_icon} {appt.get('appointment_date', 'Unknown')} - {appt.get('appointment_type', 'Unknown')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Date:** {appt.get('appointment_date', 'N/A')}")
                st.markdown(f"**Time:** {appt.get('appointment_time', 'N/A')}")
                st.markdown(f"**Type:** {appt.get('appointment_type', 'N/A')}")
                st.markdown(f"**Status:** {status_icon} {status}")
            
            with col2:
                st.markdown(f"**Specialty:** {appt.get('specialty', 'N/A')}")
                st.markdown(f"**Consultant:** {appt.get('consultant', 'N/A')}")
                st.markdown(f"**Location:** {appt.get('clinic_location', 'N/A')}")
                st.markdown(f"**Clinic ID:** {appt.get('clinic_id', 'N/A')}")
            
            if appt.get('notes'):
                st.markdown(f"**Notes:** {appt.get('notes')}")


def render_patient_documents(unified: dict):
    """Render patient documents"""
    from document_management_ui import render_patient_documents_view
    
    st.markdown("### 📁 Patient Documents")
    
    # Call the document management UI function
    render_patient_documents_view(
        patient_nhs=unified['nhs_number'],
        patient_name=unified['patient_name']
    )
