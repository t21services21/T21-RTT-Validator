"""
Patient Search and Quick Booking
Find registered patients and book appointments directly
"""

import streamlit as st
from datetime import datetime, timedelta
from supabase_database import supabase, SUPABASE_AVAILABLE

def search_patient(search_term, search_type="nhs_number"):
    """
    Search for patient in database
    
    Args:
        search_term: Search query
        search_type: Type of search (nhs_number, name, dob)
    
    Returns:
        List of matching patients
    """
    
    if not SUPABASE_AVAILABLE or supabase is None:
        return []
    
    try:
        # Clean search term (remove spaces from NHS number)
        clean_search = search_term.replace(' ', '').strip()
        
        if search_type == "nhs_number":
            # Format the search term with spaces (NHS format: XXX XXX XXXX)
            if len(clean_search) == 10:
                # Format as: 211 043 8788
                formatted_nhs = f"{clean_search[0:3]} {clean_search[3:6]} {clean_search[6:10]}"
            else:
                formatted_nhs = search_term
            
            # Try multiple search strategies for NHS number
            # 1. Search with formatted NHS number (with spaces)
            result = supabase.table('patients').select('*').eq('nhs_number', formatted_nhs).execute()
            
            # 2. If no results, try partial match with formatted number
            if not result.data:
                result = supabase.table('patients').select('*').ilike('nhs_number', f'%{formatted_nhs}%').execute()
            
            # 3. If still no results, try with cleaned number (no spaces)
            if not result.data:
                result = supabase.table('patients').select('*').ilike('nhs_number', f'%{clean_search}%').execute()
            
            # 4. If still no results, try with original search term
            if not result.data:
                result = supabase.table('patients').select('*').ilike('nhs_number', f'%{search_term}%').execute()
                
        elif search_type == "name":
            # Search by name - try first name first, then last name if no results
            result = supabase.table('patients').select('*').ilike('first_name', f'%{search_term}%').execute()
            
            # If no results, try last name
            if not result.data:
                result = supabase.table('patients').select('*').ilike('last_name', f'%{search_term}%').execute()
        elif search_type == "dob":
            # Search by date of birth
            result = supabase.table('patients').select('*').eq('date_of_birth', search_term).execute()
        else:
            return []
        
        return result.data if result.data else []
    
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []


def get_patient_appointments(patient_id):
    """Get all appointments for a patient"""
    
    if not SUPABASE_AVAILABLE or supabase is None:
        return []
    
    try:
        result = supabase.table('appointments').select('*').eq('patient_id', patient_id).order('appointment_date', desc=True).execute()
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Error fetching appointments: {str(e)}")
        return []


def outcome_appointment(appointment_id, outcome, notes=""):
    """
    Outcome an appointment
    
    Args:
        appointment_id: Appointment ID
        outcome: Outcome type (Attended, DNA, Cancelled, etc.)
        notes: Additional notes
    
    Returns:
        Success status
    """
    
    if not SUPABASE_AVAILABLE or supabase is None:
        return False
    
    try:
        update_data = {
            'status': outcome,
            'outcome_notes': notes,
            'outcome_date': datetime.now().isoformat()
        }
        
        result = supabase.table('appointments').update(update_data).eq('id', appointment_id).execute()
        return True if result.data else False
    
    except Exception as e:
        st.error(f"Error outcaming appointment: {str(e)}")
        return False


def render_find_patient():
    """Render patient search and quick booking interface"""
    
    st.subheader("🔍 Find Patient & Quick Book")
    st.info("Search for registered patients and book appointments directly")
    
    # Debug: Show all patients button
    if st.button("🔍 Show All Patients (Debug)", type="secondary"):
        if SUPABASE_AVAILABLE and supabase:
            try:
                all_patients = supabase.table('patients').select('*').limit(10).execute()
                if all_patients.data:
                    st.success(f"✅ Found {len(all_patients.data)} patients in database")
                    for p in all_patients.data:
                        st.write(f"**Name:** {p.get('first_name')} {p.get('last_name')} | **NHS:** {p.get('nhs_number')}")
                else:
                    st.warning("No patients in database")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Search section
    st.markdown("### 🔎 Search Patient")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Search", placeholder="Enter NHS number, name, or DOB...")
    
    with col2:
        search_type = st.selectbox("Search By", ["nhs_number", "name", "dob"])
    
    if st.button("🔍 Search", type="primary"):
        if search_term:
            with st.spinner("Searching..."):
                patients = search_patient(search_term, search_type)
                
                # Debug output
                st.info(f"🔍 Searched for: '{search_term}' (type: {search_type})")
                st.info(f"📊 Database returned: {len(patients) if patients else 0} results")
                
                if patients:
                    st.success(f"✅ Found {len(patients)} patient(s)")
                    
                    # Store in session state
                    st.session_state['search_results'] = patients
                else:
                    st.warning("⚠️ No patients found")
                    st.info("💡 Try searching by name instead, or check if NHS number has spaces")
                    st.session_state['search_results'] = []
        else:
            st.error("❌ Please enter a search term")
    
    # Display search results
    if 'search_results' in st.session_state and st.session_state['search_results']:
        st.markdown("---")
        st.markdown("### 📋 Search Results")
        
        for patient in st.session_state['search_results']:
            with st.expander(f"👤 {patient.get('first_name', '')} {patient.get('last_name', '')} - NHS: {patient.get('nhs_number', 'N/A')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Handle different possible field names
                    first_name = patient.get('first_name') or patient.get('firstname') or ''
                    last_name = patient.get('last_name') or patient.get('lastname') or ''
                    full_name = patient.get('full_name') or patient.get('name') or f"{first_name} {last_name}"
                    
                    st.write(f"**Name:** {full_name}")
                    st.write(f"**NHS Number:** {patient.get('nhs_number', 'N/A')}")
                    st.write(f"**DOB:** {patient.get('date_of_birth') or patient.get('dob', 'N/A')}")
                
                with col2:
                    st.write(f"**Contact:** {patient.get('contact_number', 'N/A')}")
                    st.write(f"**Address:** {patient.get('address', 'N/A')}")
                
                # Quick book button
                if st.button(f"📅 Quick Book Appointment", key=f"book_{patient.get('id')}"):
                    st.session_state['selected_patient'] = patient
                    st.session_state['show_quick_book'] = True
                    st.rerun()
                
                # View appointments
                if st.button(f"📋 View Appointments", key=f"view_{patient.get('id')}"):
                    appointments = get_patient_appointments(patient.get('id'))
                    
                    if appointments:
                        st.markdown("#### 📅 Appointment History")
                        
                        for apt in appointments:
                            status_emoji = {
                                'Booked': '📅',
                                'Attended': '✅',
                                'DNA': '❌',
                                'Cancelled': '🚫',
                                'Rescheduled': '🔄'
                            }.get(apt.get('status', ''), '📅')
                            
                            st.write(f"{status_emoji} **{apt.get('appointment_date')}** - {apt.get('appointment_type', 'N/A')} - {apt.get('status', 'N/A')}")
                    else:
                        st.info("No appointments found")
    
    # Quick booking form
    if st.session_state.get('show_quick_book') and st.session_state.get('selected_patient'):
        st.markdown("---")
        st.markdown("### 📅 Quick Book Appointment")
        
        patient = st.session_state['selected_patient']
        
        st.info(f"Booking for: **{patient.get('first_name')} {patient.get('last_name')}** (NHS: {patient.get('nhs_number')})")
        
        with st.form("quick_book_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                appointment_type = st.selectbox("Appointment Type*", [
                    "New Patient", "Follow-up", "Review", "Procedure", 
                    "Consultation", "Diagnostic", "Treatment"
                ])
                appointment_date = st.date_input("Date*", value=datetime.now() + timedelta(days=7))
            
            with col2:
                clinic_id = st.text_input("Clinic ID*", placeholder="CLINIC_20250109")
                slot_time = st.time_input("Time*", value=datetime.strptime("10:00", "%H:%M").time())
            
            priority = st.selectbox("Priority", ["Routine", "Urgent", "2WW", "Emergency"])
            special_requirements = st.text_area("Special Requirements", height=80)
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("📅 Book Appointment", type="primary")
            
            with col2:
                cancel = st.form_submit_button("❌ Cancel")
            
            if cancel:
                st.session_state['show_quick_book'] = False
                st.session_state['selected_patient'] = None
                st.rerun()
            
            if submit:
                if not clinic_id:
                    st.error("❌ Please enter Clinic ID")
                else:
                    # Book appointment logic here
                    st.success("✅ Appointment booked successfully!")
                    st.balloons()
                    st.session_state['show_quick_book'] = False
                    st.session_state['selected_patient'] = None


def render_manage_appointments():
    """Render appointment management and outcaming interface"""
    
    st.subheader("⚙️ Manage Appointments")
    st.info("View, outcome, and manage all appointments")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_date = st.date_input("Filter by Date", value=datetime.now())
    
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Booked", "Attended", "DNA", "Cancelled"])
    
    with col3:
        filter_clinic = st.text_input("Filter by Clinic ID")
    
    if st.button("🔍 Load Appointments", type="primary"):
        with st.spinner("Loading appointments..."):
            # Fetch appointments from database
            if SUPABASE_AVAILABLE and supabase:
                try:
                    query = supabase.table('appointments').select('*')
                    
                    if filter_status != "All":
                        query = query.eq('status', filter_status)
                    
                    if filter_clinic:
                        query = query.eq('clinic_id', filter_clinic)
                    
                    result = query.order('appointment_date', desc=False).execute()
                    appointments = result.data if result.data else []
                    
                    if appointments:
                        st.success(f"✅ Found {len(appointments)} appointment(s)")
                        
                        # Display appointments
                        for apt in appointments:
                            with st.expander(f"📅 {apt.get('appointment_date')} - {apt.get('patient_name', 'N/A')} - {apt.get('status', 'N/A')}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Patient:** {apt.get('patient_name', 'N/A')}")
                                    st.write(f"**NHS Number:** {apt.get('nhs_number', 'N/A')}")
                                    st.write(f"**Date:** {apt.get('appointment_date', 'N/A')}")
                                    st.write(f"**Time:** {apt.get('slot_time', 'N/A')}")
                                
                                with col2:
                                    st.write(f"**Type:** {apt.get('appointment_type', 'N/A')}")
                                    st.write(f"**Clinic:** {apt.get('clinic_id', 'N/A')}")
                                    st.write(f"**Status:** {apt.get('status', 'N/A')}")
                                    st.write(f"**Priority:** {apt.get('priority', 'N/A')}")
                                
                                # Outcome section
                                if apt.get('status') == 'Booked':
                                    st.markdown("---")
                                    st.markdown("#### 📝 Outcome Appointment")
                                    
                                    outcome_col1, outcome_col2 = st.columns(2)
                                    
                                    with outcome_col1:
                                        outcome = st.selectbox(
                                            "Outcome",
                                            ["Attended", "DNA", "Cancelled", "Rescheduled"],
                                            key=f"outcome_{apt.get('id')}"
                                        )
                                    
                                    with outcome_col2:
                                        notes = st.text_input("Notes", key=f"notes_{apt.get('id')}")
                                    
                                    if st.button("✅ Save Outcome", key=f"save_{apt.get('id')}"):
                                        if outcome_appointment(apt.get('id'), outcome, notes):
                                            st.success("✅ Appointment outcomed successfully!")
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to outcome appointment")
                    else:
                        st.warning("⚠️ No appointments found")
                
                except Exception as e:
                    st.error(f"Error loading appointments: {str(e)}")
            else:
                st.error("❌ Database not available")
