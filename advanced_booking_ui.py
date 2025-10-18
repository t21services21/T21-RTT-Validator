"""
T21 ADVANCED BOOKING SYSTEM UI
Complete interface for AI-powered appointment scheduling

Features:
- AI appointment optimization
- Clinic management
- Slot availability
- Conflict detection
- DNA prevention
- Capacity planning
"""

import streamlit as st
from advanced_booking_system import (
    create_clinic_template,
    book_appointment,
    get_available_slots,
    cancel_appointment,
    reschedule_appointment,
    ai_optimize_clinic_capacity,
    APPOINTMENT_TYPES,
    SPECIALTIES
)
from datetime import datetime, timedelta


def render_advanced_booking():
    """Main booking system interface"""
    
    st.header("📅 Advanced Booking System")
    st.markdown("**AI-Powered Appointment Scheduling & Optimization**")
    
    st.success("""
    📅 **Intelligent Appointment Management**
    - AI appointment optimization
    - Conflict detection & resolution
    - Capacity planning
    - DNA prediction & prevention
    - Multi-clinic coordination
    - 120x faster than manual booking
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 Book Appointment",
        "📋 Partial Booking List",
        "📅 Clinic Management",
        "🔍 Check Availability",
        "📊 Capacity Analysis",
        "⚙️ Manage Appointments",
        "📉 DNA Analytics"
    ])
    
    with tab1:
        render_book_appointment()
    
    with tab2:
        # PARTIAL BOOKING LIST - NHS-Critical Workflow
        try:
            from partial_booking_list_ui import render_partial_booking_list
            render_partial_booking_list()
        except Exception as e:
            st.error(f"Error loading Partial Booking List: {e}")
            st.info("""
            **Partial Booking List (PBL)**
            
            NHS workflow for patients whose referral is accepted but no appointment slot available.
            
            Features:
            - Track patients awaiting first appointment
            - Send acknowledgment emails
            - Monitor RTT breach risks
            - Automatically remove when appointment booked
            - Data cleansing tools for NHS experts
            
            Module temporarily unavailable.
            """)
    
    with tab3:
        render_clinic_management()
    
    with tab4:
        render_check_availability()
    
    with tab5:
        render_capacity_analysis()
    
    with tab6:
        render_manage_appointments()
    
    with tab7:
        render_dna_analytics()


def render_book_appointment():
    """Book new appointment with AI optimization"""
    
    st.subheader("📋 Book Appointment")
    
    with st.form("book_appointment"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
            nhs_number = st.text_input("NHS Number*", placeholder="123 456 7890")
            appointment_type = st.selectbox("Appointment Type*", APPOINTMENT_TYPES)
            priority = st.selectbox("Priority", ["Routine", "Urgent", "2WW", "Emergency"])
        
        with col2:
            clinic_id = st.text_input("Clinic ID*", placeholder="CLINIC_20250109")
            appointment_date = st.date_input("Preferred Date*", value=datetime.now() + timedelta(days=7))
            slot_time = st.time_input("Preferred Time", value=datetime.strptime("10:00", "%H:%M").time())
            contact_number = st.text_input("Contact Number", placeholder="07123456789")
        
        special_requirements = st.text_area("Special Requirements", height=80,
                                           placeholder="e.g., Wheelchair access, Interpreter needed")
        
        transport_required = st.checkbox("Transport Required")
        
        submit = st.form_submit_button("📅 Book Appointment", type="primary")
        
        if submit:
            if not patient_name or not nhs_number or not clinic_id:
                st.error("❌ Please fill all required fields!")
            else:
                with st.spinner("🤖 AI finding optimal slot..."):
                    result = book_appointment(
                        patient_name=patient_name,
                        nhs_number=nhs_number,
                        clinic_id=clinic_id,
                        appointment_date=str(appointment_date),
                        slot_time=slot_time.strftime("%H:%M"),
                        appointment_type=appointment_type,
                        priority=priority,
                        special_requirements=special_requirements,
                        contact_number=contact_number,
                        transport_required=transport_required
                    )
                
                if result['success']:
                    st.balloons()
                    st.success(f"""
                    ✅ **APPOINTMENT BOOKED SUCCESSFULLY!**
                    
                    **Appointment ID:** {result['appointment_id']}  
                    **Date:** {apt_date}  
                    **Time:** {apt_time}  
                    **Specialty:** {specialty}  
                    
                    ✔️ {result['confirmation']}  
                    📧 Patient can be notified of appointment!
                    """)
                    st.info("💡 **Next Steps:** Send appointment confirmation to patient or add to PBL if needed.")
                    
                    # Store success info in session state
                    st.session_state['last_booked_appointment_id'] = result['appointment_id']
                    st.session_state['last_booking_time'] = datetime.now().isoformat()
                    
                    st.info("""
                    📋 **Next Steps:**
                    - Your appointment has been saved
                    - Go to "Manage Appointments" tab to view all bookings
                    - Or click the refresh button there to see your new appointment
                    """)
                else:
                    st.warning(f"⚠️ {result['message']}")
                    
                    # NHS WORKFLOW: Add to Partial Booking List if no slots available
                    st.markdown("---")
                    st.error("❌ **No appointment slots available**")
                    st.info("""
                    📋 **NHS Partial Booking List (PBL) Workflow**
                    
                    When no appointment is available, the patient should be added to the Partial Booking List:
                    - ✅ Send acknowledgment email to patient
                    - 📊 Monitor RTT breach risk
                    - 🔔 Alert when slots become available
                    - 📧 Automatically notify patient when booked
                    """)
                    
                    # Add to PBL button
                    col_pbl1, col_pbl2, col_pbl3 = st.columns([2, 1, 2])
                    with col_pbl2:
                        if st.button("➕ Add to Partial Booking List", type="primary", key="add_to_pbl_btn"):
                            st.session_state['add_to_pbl_pending'] = {
                                'patient_name': patient_name,
                                'nhs_number': nhs_number,
                                'appointment_type': appointment_type,
                                'priority': priority,
                                'contact_number': contact_number,
                                'special_requirements': special_requirements
                            }
                            st.success("✅ Patient info saved! Scroll down to complete PBL form.")
                            st.rerun()
                    
                    st.markdown("---")
                    
                    if result.get('alternatives'):
                        st.markdown("### 🤖 AI-Suggested Alternative Slots:")
                        
                        for alt in result['alternatives'][:5]:
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown(f"**Date:** {alt['date']}")
                                st.markdown(f"**Time:** {alt['time']}")
                            
                            with col2:
                                st.markdown(f"**Clinic:** {alt['clinic_name']}")
                                st.markdown(f"**Consultant:** {alt['consultant']}")
                            
                            with col3:
                                st.markdown(f"**AI Score:** {alt['ai_score']:.1f}/100")
                                st.markdown(f"**Rating:** {alt['recommendation']}")
                            
                            st.markdown("---")
    
    # PBL FORM - Shows when user clicks "Add to PBL" button
    if 'add_to_pbl_pending' in st.session_state:
        st.markdown("---")
        st.markdown("## 📋 Add to Partial Booking List")
        st.success("✅ Patient details saved. Complete additional information below:")
        
        pending_data = st.session_state['add_to_pbl_pending']
        
        with st.form("pbl_form"):
            st.markdown("### Complete PBL Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Patient:** {pending_data['patient_name']}")
                st.write(f"**NHS Number:** {pending_data['nhs_number']}")
                st.write(f"**Priority:** {pending_data['priority']}")
                
                dob = st.date_input("Date of Birth*", value=datetime.now() - timedelta(days=365*40))
                referral_date = st.date_input("Referral Date*", value=datetime.now())
                specialty = st.selectbox("Specialty*", SPECIALTIES)
            
            with col2:
                email = st.text_input("Patient Email*", placeholder="patient@email.com")
                phone = st.text_input("Patient Phone", value=pending_data.get('contact_number', ''))
                referring_gp = st.text_input("Referring GP", placeholder="Dr. Jones")
                referral_reason = st.text_area("Referral Reason", 
                                              value=pending_data.get('special_requirements', ''),
                                              height=100)
            
            send_acknowledgment = st.checkbox("📧 Send Acknowledgment Email to Patient", value=True)
            
            notes = st.text_area("Additional Notes", height=80)
            
            submit_pbl = st.form_submit_button("✅ Add to Partial Booking List", type="primary")
            
            if submit_pbl:
                if not email or not specialty:
                    st.error("❌ Please fill all required fields (Email and Specialty)!")
                else:
                    try:
                        from partial_booking_list_system import add_to_pbl
                        
                        pbl_data = {
                            'nhs_number': pending_data['nhs_number'],
                            'name': pending_data['patient_name'],
                            'dob': str(dob),
                            'referral_date': str(referral_date),
                            'specialty': specialty,
                            'priority': pending_data['priority'],
                            'email': email,
                            'phone': phone,
                            'referring_gp': referring_gp,
                            'referral_reason': referral_reason,
                            'notes': notes
                        }
                        
                        result = add_to_pbl(pbl_data, send_acknowledgment=send_acknowledgment)
                        
                        if result['success']:
                            st.balloons()
                            st.success(f"""
                            ✅ **PATIENT ADDED TO PARTIAL BOOKING LIST!**
                            
                            **Patient:** {pending_data['patient_name']}  
                            **NHS Number:** {pending_data['nhs_number']}  
                            **Specialty:** {specialty}  
                            **Priority:** {pending_data['priority']}  
                            
                            {'✅ Acknowledgment email sent!' if send_acknowledgment and email else ''}
                            
                            📋 **Next Steps:**
                            - Patient is now on PBL and monitored for RTT breach risk
                            - Go to "Partial Booking List" tab to view and manage
                            - System will alert when appointments become available
                            - Patient will be automatically notified when booked
                            """)
                            
                            # Clear pending state
                            del st.session_state['add_to_pbl_pending']
                            
                        else:
                            st.error(f"❌ {result['message']}")
                    
                    except Exception as e:
                        st.error(f"❌ Error adding to PBL: {e}")
                        st.info("💡 The Partial Booking List module may not be fully configured. Contact system administrator.")


def render_clinic_management():
    """Manage clinic templates"""
    
    st.subheader("📅 Clinic Management")
    
    with st.form("create_clinic"):
        st.markdown("### Create New Clinic Template")
        
        col1, col2 = st.columns(2)
        
        with col1:
            clinic_name = st.text_input("Clinic Name*", placeholder="Cardiology Outpatients")
            specialty = st.selectbox("Specialty*", SPECIALTIES)
            location = st.text_input("Location*", placeholder="Clinic Room 2")
            consultant = st.text_input("Consultant*", placeholder="Dr. Smith")
        
        with col2:
            day_of_week = st.selectbox("Day of Week*", 
                                       ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            start_time = st.time_input("Start Time", value=datetime.strptime("09:00", "%H:%M").time())
            end_time = st.time_input("End Time", value=datetime.strptime("17:00", "%H:%M").time())
            slot_duration = st.number_input("Slot Duration (minutes)", min_value=5, max_value=60, value=15)
        
        capacity = st.number_input("Total Capacity (slots)", min_value=1, max_value=100, value=20)
        clinic_type = st.selectbox("Clinic Type", ["Outpatient", "New Patient", "Follow-up", "Procedure"])
        
        submit = st.form_submit_button("➕ Create Clinic Template", type="primary")
        
        if submit:
            if not clinic_name or not consultant:
                st.error("❌ Please fill all required fields!")
            else:
                clinic_id = create_clinic_template(
                    clinic_name=clinic_name,
                    specialty=specialty,
                    location=location,
                    consultant=consultant,
                    day_of_week=day_of_week,
                    start_time=start_time.strftime("%H:%M"),
                    end_time=end_time.strftime("%H:%M"),
                    slot_duration=slot_duration,
                    capacity=capacity,
                    clinic_type=clinic_type
                )
                
                st.balloons()
                st.success(f"""
                ✅ **CLINIC TEMPLATE CREATED SUCCESSFULLY!**
                
                **Template ID:** {clinic_id}  
                **Specialty:** {clinic_specialty}  
                **Slots Per Day:** {slots_per_day}  
                
                ✔️ Template has been saved!  
                📅 Ready to use for booking appointments!
                """)
                st.info("💡 **Next Steps:** Use this template to book multiple appointments efficiently.")


def render_check_availability():
    """Check appointment availability"""
    
    st.subheader("🔍 Check Slot Availability")
    
    col1, col2 = st.columns(2)
    
    with col1:
        clinic_id = st.text_input("Clinic ID", placeholder="CLINIC_20250109", key="check_clinic_id")
    
    with col2:
        check_date = st.date_input("Date", value=datetime.now() + timedelta(days=7), key="check_clinic_date")
    
    if st.button("🔍 Check Availability", type="primary"):
        if clinic_id:
            with st.spinner("Checking availability..."):
                slots = get_available_slots(clinic_id, str(check_date))
            
            if slots:
                st.success(f"✅ {len(slots)} slots available on {check_date}")
                
                for slot in slots:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"⏰ **{slot['time']}**")
                    
                    with col2:
                        st.markdown(f"Duration: {slot['duration']} mins")
                    
                    with col3:
                        st.markdown(f"Clinic: {slot['clinic_name']}")
                    
                    st.markdown("---")
            else:
                st.warning("⚠️ No slots available or clinic not found")
        else:
            st.error("❌ Please enter clinic ID")


def render_capacity_analysis():
    """AI capacity analysis"""
    
    st.subheader("📊 AI Capacity Analysis & Optimization")
    
    clinic_id = st.text_input("Clinic ID for Analysis", placeholder="CLINIC_20250109", key="ai_analysis_clinic_id")
    weeks_ahead = st.slider("Analyze Next X Weeks", 1, 12, 4)
    
    if st.button("🤖 Run AI Capacity Analysis", type="primary"):
        if clinic_id:
            with st.spinner("🤖 AI analyzing capacity..."):
                analysis = ai_optimize_clinic_capacity(clinic_id, weeks_ahead)
            
            if analysis:
                st.success("✅ AI Analysis Complete!")
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Capacity", analysis['total_capacity'])
                
                with col2:
                    st.metric("Bookings", analysis['bookings'])
                
                with col3:
                    st.metric("Utilization", f"{analysis['utilization']:.1f}%")
                
                with col4:
                    st.metric("AI Score", f"{analysis['ai_optimization_score']:.1f}/100")
                
                # Recommendations
                if analysis['recommendations']:
                    st.markdown("### 🤖 AI Recommendations:")
                    
                    for rec in analysis['recommendations']:
                        if rec['type'] == 'CRITICAL' or rec['type'] == 'UNDERUTILIZED':
                            st.error(f"""
                            **{rec['type']}**
                            - {rec['message']}
                            - **Action:** {rec['action']}
                            """)
                        elif rec['type'] == 'OVERBOOKED' or rec['type'] == 'HIGH_CANCELLATIONS':
                            st.warning(f"""
                            **{rec['type']}**
                            - {rec['message']}
                            - **Action:** {rec['action']}
                            """)
                        else:
                            st.info(f"""
                            **{rec['type']}**
                            - {rec['message']}
                            - **Action:** {rec['action']}
                            """)
                else:
                    st.success("✅ Clinic is well optimized - no issues detected!")
            else:
                st.error("❌ Clinic not found or analysis failed")
        else:
            st.error("❌ Please enter clinic ID")


def render_appointments_list():
    """View all booked appointments"""
    from advanced_booking_system import load_appointments, get_current_user_email, SUPABASE_ENABLED
    
    st.markdown("### 📋 All Booked Appointments")
    
    # Add refresh button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Loading appointments...**")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Check if appointment was just booked
    if 'last_booked_appointment_id' in st.session_state:
        st.success(f"✅ **Recently Booked:** {st.session_state['last_booked_appointment_id']}")
        st.info("👇 Your new appointment should appear below. If not, click Refresh.")
    
    # Debug info
    user_email = get_current_user_email()
    with st.expander("🔍 Debug Info - Click to see technical details"):
        st.write(f"**User Email:** {user_email}")
        st.write(f"**Supabase Enabled:** {SUPABASE_ENABLED}")
        st.write(f"**Checking appointments for this user...**")
        if 'last_booked_appointment_id' in st.session_state:
            st.write(f"**Last Booked:** {st.session_state['last_booked_appointment_id']}")
            st.write(f"**Booking Time:** {st.session_state.get('last_booking_time', 'Unknown')}")
    
    # Get all appointments
    appointments_data = load_appointments()
    appointments = appointments_data.get('appointments', [])
    
    st.write(f"**Found {len(appointments)} appointments**")
    
    if not appointments:
        st.info("📅 No appointments booked yet")
        st.warning("""
        **If you just booked an appointment:**
        1. Click the "🔄 Refresh" button above
        2. Or go back to "Book Appointment" tab
        3. Check that Supabase is configured
        """)
        return
    
    # Quick Stats Dashboard
    st.markdown("#### 📊 Appointments Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(appointments)
    confirmed = len([a for a in appointments if a.get('status', '').lower() == 'confirmed'])
    cancelled = len([a for a in appointments if a.get('status', '').lower() == 'cancelled'])
    completed = len([a for a in appointments if a.get('status', '').lower() == 'completed'])
    
    with col1:
        st.metric("Total Appointments", total)
    with col2:
        st.metric("🟢 Confirmed", confirmed)
    with col3:
        st.metric("✅ Completed", completed)
    with col4:
        st.metric("🔴 Cancelled", cancelled)
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Confirmed", "Cancelled", "Completed", "No-Show"], key="booking_status_filter")
    with col2:
        date_filter = st.date_input("Filter from Date", value=datetime.now().date(), key="booking_date_filter")
    with col3:
        search = st.text_input("🔍 Search", placeholder="Patient name or NHS number", key="booking_search_filter")
    
    # Filter appointments
    filtered = appointments
    
    if status_filter != "All":
        filtered = [a for a in filtered if a.get('status', '').lower() == status_filter.lower()]
    
    if search:
        filtered = [a for a in filtered if 
                   search.lower() in a.get('patient_name', '').lower() or 
                   search.lower() in a.get('nhs_number', '').lower()]
    
    # Sort by date
    filtered.sort(key=lambda x: (x.get('appointment_date', ''), x.get('appointment_time', '')), reverse=True)
    
    # Display count
    st.markdown(f"**Total Appointments:** {len(filtered)} (of {len(appointments)})")
    
    # Display appointments
    for appt in filtered[:50]:  # Show max 50
        status = appt.get('status', 'Unknown')
        
        # Color code by status
        if status.lower() == 'confirmed':
            status_color = "🟢"
        elif status.lower() == 'cancelled':
            status_color = "🔴"
        elif status.lower() == 'completed':
            status_color = "✅"
        elif status.lower() == 'no-show':
            status_color = "⚠️"
        else:
            status_color = "⚪"
        
        with st.expander(f"{status_color} {appt.get('patient_name', 'Unknown')} - {appt.get('appointment_date', 'N/A')} at {appt.get('appointment_time', 'N/A')}"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(f"**Appointment ID:** {appt.get('appointment_id', 'N/A')}")
                st.markdown(f"**Patient Name:** {appt.get('patient_name', 'N/A')}")
                st.markdown(f"**NHS Number:** {appt.get('nhs_number', 'N/A')}")
                st.markdown(f"**Status:** {status_color} {status}")
            
            with col_b:
                st.markdown(f"**Date:** {appt.get('appointment_date', 'N/A')}")
                st.markdown(f"**Time:** {appt.get('appointment_time', 'N/A')}")
                st.markdown(f"**Specialty:** {appt.get('specialty', 'N/A')}")
                st.markdown(f"**Consultant:** {appt.get('consultant', 'N/A')}")
            
            st.markdown(f"**Clinic:** {appt.get('clinic_id', 'N/A')} - {appt.get('clinic_location', 'N/A')}")
            st.markdown(f"**Type:** {appt.get('appointment_type', 'N/A')}")
            
            if appt.get('notes'):
                st.markdown(f"**Notes:** {appt.get('notes')}")
            
            # Quick actions
            col1, col2, col3, col4 = st.columns(4)
            
            # Only show attendance buttons for confirmed appointments
            if status.lower() == 'confirmed':
                with col1:
                    if st.button("✅ Attended", key=f"attended_{appt.get('appointment_id')}", use_container_width=True):
                        from advanced_booking_system import mark_appointment_attended
                        if mark_appointment_attended(appt.get('appointment_id')):
                            st.success("✅ Marked as attended")
                            st.rerun()
                        else:
                            st.error("❌ Failed to update")
                with col2:
                    if st.button("⚠️ DNA", key=f"dna_{appt.get('appointment_id')}", use_container_width=True):
                        st.session_state[f"marking_dna_{appt.get('appointment_id')}"] = True
            
            with col3:
                if st.button("❌ Cancel", key=f"cancel_{appt.get('appointment_id')}", use_container_width=True):
                    st.session_state[f"cancelling_{appt.get('appointment_id')}"] = True
            with col4:
                if st.button("🔄 Reschedule", key=f"reschedule_{appt.get('appointment_id')}", use_container_width=True):
                    st.session_state[f"rescheduling_{appt.get('appointment_id')}"] = True
            
            # DNA reason form
            if st.session_state.get(f"marking_dna_{appt.get('appointment_id')}"):
                with st.form(f"dna_form_{appt.get('appointment_id')}"):
                    st.warning("⚠️ Mark as DNA (Did Not Attend)")
                    dna_reason = st.text_area("Reason (optional)", placeholder="Patient didn't arrive, no call...")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.form_submit_button("Confirm DNA", type="primary", use_container_width=True):
                            from advanced_booking_system import mark_appointment_dna
                            if mark_appointment_dna(appt.get('appointment_id'), dna_reason):
                                st.success("⚠️ Marked as DNA")
                                del st.session_state[f"marking_dna_{appt.get('appointment_id')}"]
                                st.rerun()
                            else:
                                st.error("❌ Failed to update")
                    with col_b:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            del st.session_state[f"marking_dna_{appt.get('appointment_id')}"]
                            st.rerun()


def render_manage_appointments():
    """Manage existing appointments"""
    
    st.subheader("⚙️ Manage Appointments")
    
    action = st.radio("Action", ["View All Appointments", "Cancel Appointment", "Reschedule Appointment"])
    
    if action == "View All Appointments":
        render_appointments_list()
    
    if action == "Cancel Appointment":
        with st.form("cancel_appt"):
            appointment_id = st.text_input("Appointment ID*", placeholder="APPT_20250109...")
            reason = st.text_area("Cancellation Reason*", height=100)
            cancelled_by = st.selectbox("Cancelled By", ["Patient", "Clinician", "Admin", "System"])
            
            if st.form_submit_button("❌ Cancel Appointment"):
                if appointment_id and reason:
                    success = cancel_appointment(appointment_id, reason, cancelled_by)
                    if success:
                        st.success("✅ Appointment cancelled successfully")
                    else:
                        st.error("❌ Appointment not found")
                else:
                    st.error("❌ Please fill all fields")
    
    else:  # Reschedule
        with st.form("reschedule_appt"):
            appointment_id = st.text_input("Appointment ID*", placeholder="APPT_20250109...")
            new_clinic_id = st.text_input("New Clinic ID*", placeholder="CLINIC_...")
            new_date = st.date_input("New Date*")
            new_time = st.time_input("New Time*")
            
            if st.form_submit_button("🔄 Reschedule Appointment"):
                if appointment_id and new_clinic_id:
                    result = reschedule_appointment(
                        appointment_id=appointment_id,
                        new_clinic_id=new_clinic_id,
                        new_date=str(new_date),
                        new_time=new_time.strftime("%H:%M")
                    )
                    
                    if result.get('success'):
                        st.success(f"✅ Appointment rescheduled! New ID: {result['appointment_id']}")
                    else:
                        st.error(f"❌ {result.get('message', 'Failed to reschedule')}")
                else:
                    st.error("❌ Please fill all fields")


def render_dna_analytics():
    """DNA (Did Not Attend) Analytics and Tracking"""
    from advanced_booking_system import get_dna_rate, load_appointments
    
    st.subheader("📉 DNA (Did Not Attend) Analytics")
    
    # Time period selection
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Overall DNA Statistics")
    with col2:
        days = st.selectbox("Time Period", [7, 14, 30, 60, 90, 180, 365], index=2)
    
    # Get DNA statistics
    stats = get_dna_rate(days=days)
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Appointments", stats['total_appointments'])
    with col2:
        st.metric("✅ Attended", stats['attended'], 
                 delta=f"{stats['attendance_rate']}% rate", 
                 delta_color="normal")
    with col3:
        st.metric("⚠️ DNA", stats['dna'], 
                 delta=f"{stats['dna_rate']}% rate",
                 delta_color="inverse")
    with col4:
        st.metric("🔴 Cancelled", stats['cancelled'])
    
    # DNA Rate Analysis
    st.markdown("---")
    st.markdown("### DNA Rate Analysis")
    
    if stats['dna_rate'] < 5:
        st.success(f"✅ Excellent! DNA rate is {stats['dna_rate']}% (Target: <5%)")
    elif stats['dna_rate'] < 10:
        st.info(f"ℹ️ Good. DNA rate is {stats['dna_rate']}% (Target: <5%)")
    elif stats['dna_rate'] < 15:
        st.warning(f"⚠️ DNA rate is {stats['dna_rate']}% - Needs improvement (Target: <5%)")
    else:
        st.error(f"❌ CRITICAL: DNA rate is {stats['dna_rate']}% - Urgent action required!")
    
    # Recent DNA List
    st.markdown("---")
    st.markdown("### Recent DNA Appointments")
    
    appointments_data = load_appointments()
    all_appointments = appointments_data.get('appointments', [])
    
    # Filter DNAs
    dna_appointments = [a for a in all_appointments if a.get('status', '').lower() == 'no-show']
    dna_appointments.sort(key=lambda x: x.get('appointment_date', ''), reverse=True)
    
    if dna_appointments:
        st.markdown(f"**{len(dna_appointments)} DNA appointments found**")
        
        for dna in dna_appointments[:20]:  # Show latest 20
            with st.expander(f"⚠️ {dna.get('patient_name', 'Unknown')} - {dna.get('appointment_date', 'N/A')}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"**Patient:** {dna.get('patient_name', 'Unknown')}")
                    st.markdown(f"**NHS Number:** {dna.get('nhs_number', 'N/A')}")
                    st.markdown(f"**Date:** {dna.get('appointment_date', 'N/A')}")
                    st.markdown(f"**Time:** {dna.get('appointment_time', 'N/A')}")
                
                with col_b:
                    st.markdown(f"**Specialty:** {dna.get('specialty', 'N/A')}")
                    st.markdown(f"**Type:** {dna.get('appointment_type', 'N/A')}")
                    st.markdown(f"**Consultant:** {dna.get('consultant', 'N/A')}")
                    st.markdown(f"**Clinic:** {dna.get('clinic_id', 'N/A')}")
                
                if dna.get('dna_reason'):
                    st.markdown(f"**Reason:** {dna.get('dna_reason')}")
                
                # DNA recorded info
                if dna.get('dna_recorded_at'):
                    st.caption(f"Recorded at: {dna.get('dna_recorded_at')}")
    else:
        st.success("✅ No DNA appointments in selected period!")
    
    # DNA Prevention Recommendations
    st.markdown("---")
    st.markdown("### 💡 DNA Prevention Recommendations")
    
    if stats['dna_rate'] > 5:
        st.info("""
        **Suggested Actions to Reduce DNA Rate:**
        - Send SMS reminders 48h and 24h before appointment
        - Call patients with history of DNAs
        - Offer more convenient appointment times
        - Implement patient transport support
        - Review appointment booking process
        - Consider telephone consultations as alternative
        - Analyze DNA patterns by specialty/day/time
        """)
    else:
        st.success("""
        **Excellent DNA Rate! Keep up the good work:**
        - Continue current reminder system
        - Maintain flexible appointment times
        - Keep monitoring DNA patterns
        """)

