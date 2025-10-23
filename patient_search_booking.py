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


def get_patient_appointments(patient_id_or_nhs):
    """Get all appointments for a patient by patient_id or NHS number"""
    
    if not SUPABASE_AVAILABLE or supabase is None:
        return []
    
    try:
        # Try searching by patient_id first
        result = supabase.table('appointments').select('*').eq('patient_id', patient_id_or_nhs).order('appointment_date', desc=True).execute()
        
        # If no results, try searching by NHS number
        if not result.data:
            result = supabase.table('appointments').select('*').eq('nhs_number', patient_id_or_nhs).order('appointment_date', desc=True).execute()
        
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
            # Get full name properly
            first_name = patient.get('first_name') or patient.get('firstname') or ''
            last_name = patient.get('last_name') or patient.get('lastname') or ''
            title = patient.get('title') or ''
            full_name = f"{title} {first_name} {last_name}".strip() or patient.get('full_name') or patient.get('name') or 'Unknown'
            
            with st.expander(f"👤 {full_name} - NHS: {patient.get('nhs_number', 'N/A')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Full Name:** {full_name}")
                    st.write(f"**NHS Number:** {patient.get('nhs_number', 'N/A')}")
                    st.write(f"**DOB:** {patient.get('date_of_birth') or patient.get('dob', 'N/A')}")
                    st.write(f"**Gender:** {patient.get('gender', 'N/A')}")
                
                with col2:
                    st.write(f"**Mobile:** {patient.get('mobile_number') or patient.get('contact_number', 'N/A')}")
                    st.write(f"**Email:** {patient.get('email', 'N/A')}")
                    st.write(f"**Address:** {patient.get('address', 'N/A')}")
                    st.write(f"**GP:** {patient.get('gp_name', 'N/A')}")
                
                st.markdown("---")
                
                # Action buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"📅 Quick Book Appointment", key=f"book_{patient.get('id')}", use_container_width=True, type="primary"):
                        st.session_state['selected_patient'] = patient
                        st.session_state['show_quick_book'] = True
                        st.rerun()
                
                with col2:
                    if st.button(f"📋 View Appointments", key=f"view_{patient.get('id')}", use_container_width=True):
                        # Pass NHS number to find appointments
                        appointments = get_patient_appointments(patient.get('nhs_number'))
                        
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
                                
                                # Show full appointment details
                                with st.expander(f"{status_emoji} {apt.get('appointment_date')} at {apt.get('appointment_time', 'N/A')} - {apt.get('specialty', 'N/A')} - {apt.get('status', 'N/A')}"):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.write(f"**Date:** {apt.get('appointment_date', 'N/A')}")
                                        st.write(f"**Time:** {apt.get('appointment_time', 'N/A')}")
                                        st.write(f"**Specialty:** {apt.get('specialty', 'N/A')}")
                                        st.write(f"**Type:** {apt.get('appointment_type', 'N/A')}")
                                    
                                    with col2:
                                        st.write(f"**Clinic:** {apt.get('clinic_location', 'N/A')}")
                                        st.write(f"**Consultant:** {apt.get('consultant', 'N/A')}")
                                        st.write(f"**Status:** {apt.get('status', 'N/A')}")
                                        st.write(f"**Appointment ID:** {apt.get('appointment_id', 'N/A')}")
                                    
                                    if apt.get('notes'):
                                        st.write(f"**Notes:** {apt.get('notes')}")
                        else:
                            st.info("No appointments found")
    
    # Quick booking form
    if st.session_state.get('show_quick_book') and st.session_state.get('selected_patient'):
        st.markdown("---")
        st.markdown("### 📅 Quick Book Appointment")
        
        patient = st.session_state['selected_patient']
        
        # Get full name
        first_name = patient.get('first_name') or patient.get('firstname') or ''
        last_name = patient.get('last_name') or patient.get('lastname') or ''
        title = patient.get('title') or ''
        full_name = f"{title} {first_name} {last_name}".strip()
        
        st.info(f"📋 Booking for: **{full_name}** (NHS: {patient.get('nhs_number')})")
        
        with st.form("quick_book_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Specialty - CRITICAL for NHS pathways
                specialty = st.selectbox("Specialty*", [
                    "Cardiology",
                    "Orthopaedics", 
                    "Gastroenterology",
                    "ENT (Ear, Nose & Throat)",
                    "Dermatology",
                    "Ophthalmology",
                    "Urology",
                    "Gynaecology",
                    "Respiratory Medicine",
                    "Neurology",
                    "Rheumatology",
                    "Endocrinology",
                    "General Surgery",
                    "Trauma & Orthopaedics",
                    "Paediatrics",
                    "Geriatrics",
                    "Pain Management",
                    "Diabetes",
                    "Other"
                ])
                
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
                    # Book appointment using the advanced booking system
                    from advanced_booking_system import book_appointment
                    
                    result = book_appointment(
                        patient_name=full_name,
                        nhs_number=patient.get('nhs_number'),
                        clinic_id=clinic_id,
                        appointment_date=str(appointment_date),
                        slot_time=slot_time.strftime("%H:%M"),
                        appointment_type=appointment_type,
                        specialty=specialty,  # Add specialty for NHS pathway tracking
                        priority=priority,
                        special_requirements=special_requirements,
                        contact_number=patient.get('mobile_number') or patient.get('contact_number', ''),
                        transport_required=False
                    )
                    
                    if result.get('success'):
                        storage_type = result.get('storage', 'unknown')
                        storage_emoji = {
                            'supabase': '☁️',
                            'session': '💾',
                            'file': '📁'
                        }.get(storage_type, '💾')
                        
                        # HUGE SUCCESS MESSAGE
                        from success_message_component import show_huge_success
                        
                        show_huge_success(
                            title="APPOINTMENT BOOKED!",
                            subtitle=f"{storage_emoji} Saved to {storage_type}",
                            details={
                                "Appointment ID": result['appointment_id'],
                                "Patient": full_name,
                                "Specialty": specialty,
                                "Date": appointment_date,
                                "Time": slot_time.strftime("%H:%M"),
                                "Type": appointment_type,
                                "Priority": priority,
                                "Clinic": clinic_id
                            },
                            next_steps="Go to '⚙️ Manage Appointments' tab → 'View All Appointments' to see this appointment." if storage_type == 'supabase' else None
                        )
                        
                        # Show warning if not saved to Supabase
                        if storage_type != 'supabase':
                            st.warning(f"⚠️ **Saved to {storage_type} storage** - May not persist after page refresh.")
                            st.error("""
                            **Supabase is not working!**
                            
                            Possible causes:
                            1. Supabase credentials not configured
                            2. Database table schema mismatch
                            3. Network/connection issue
                            
                            Check the server logs for detailed error messages.
                            """)
                        
                        # Store appointment ID for easy access
                        st.session_state['last_booked_appointment'] = result['appointment_id']
                    else:
                        st.error(f"❌ Failed to book appointment: {result.get('message', 'Unknown error')}")
                    
                    st.session_state['show_quick_book'] = False
                    st.session_state['selected_patient'] = None


def render_manage_appointments():
    """Render appointment management and outcaming interface"""
    
    st.subheader("⚙️ Manage Appointments")
    st.info("View, outcome, and manage all appointments")
    
    # Quick view all button
    if st.button("📋 VIEW ALL APPOINTMENTS", type="primary", use_container_width=True):
        st.session_state['load_all_appointments'] = True
    
    st.markdown("---")
    st.markdown("### 🔍 Filter Appointments (Optional)")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_date = st.date_input("Filter by Date (optional)", value=datetime.now())
    
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Booked", "Attended", "DNA", "Cancelled"])
    
    with col3:
        filter_clinic = st.text_input("Filter by Clinic ID (optional)")
    
    if st.button("🔍 Load Filtered Appointments", type="secondary") or st.session_state.get('load_all_appointments'):
        with st.spinner("Loading appointments..."):
            # Fetch appointments from database
            if SUPABASE_AVAILABLE and supabase:
                try:
                    # Load all appointments or filtered
                    query = supabase.table('appointments').select('*')
                    
                    # Apply filters only if specified
                    if filter_status != "All":
                        query = query.eq('status', filter_status)
                    
                    if filter_clinic:
                        query = query.eq('clinic_id', filter_clinic)
                    
                    # Order by most recent first
                    result = query.order('created_at', desc=True).limit(50).execute()
                    appointments = result.data if result.data else []
                    
                    # Clear the load flag
                    if 'load_all_appointments' in st.session_state:
                        del st.session_state['load_all_appointments']
                    
                    if appointments:
                        st.success(f"✅ Found {len(appointments)} appointment(s)")
                        
                        # Display appointments
                        for apt in appointments:
                            # Get specialty for display
                            specialty = apt.get('specialty', 'N/A')
                            status = apt.get('status', 'N/A')
                            
                            # Status emoji
                            status_emoji = {
                                'Booked': '📅',
                                'Attended': '✅',
                                'DNA': '❌',
                                'Cancelled': '🚫',
                                'Rescheduled': '🔄'
                            }.get(status, '📅')
                            
                            with st.expander(f"{status_emoji} {apt.get('appointment_date')} - {apt.get('patient_name', 'N/A')} - {specialty} - {status}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Patient:** {apt.get('patient_name', 'N/A')}")
                                    st.write(f"**NHS Number:** {apt.get('nhs_number', 'N/A')}")
                                    st.write(f"**Specialty:** {specialty}")
                                    st.write(f"**Date:** {apt.get('appointment_date', 'N/A')}")
                                    st.write(f"**Time:** {apt.get('slot_time', 'N/A')}")
                                
                                with col2:
                                    st.write(f"**Type:** {apt.get('appointment_type', 'N/A')}")
                                    st.write(f"**Clinic:** {apt.get('clinic_id', 'N/A')}")
                                    st.write(f"**Status:** {status}")
                                    st.write(f"**Priority:** {apt.get('priority', 'N/A')}")
                                    st.write(f"**Appointment ID:** {apt.get('id', 'N/A')}")
                                
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
