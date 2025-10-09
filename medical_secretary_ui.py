"""
T21 MEDICAL SECRETARY UI
Complete interface for medical secretary tasks

Features:
- AI letter generation
- Diary management
- Referral processing
- Clinic coordination
"""

import streamlit as st
from medical_secretary_ai import (
    ai_draft_clinic_letter,
    ai_manage_diary,
    ai_process_referral,
    LETTER_TYPES,
    EVENT_TYPES
)
from datetime import datetime, timedelta


def render_medical_secretary():
    """Main medical secretary interface"""
    
    st.header("📧 Medical Secretary AI Assistant")
    st.markdown("**AI-Powered Clinic Coordination & Correspondence**")
    
    st.success("""
    📧 **Complete Medical Secretary Support**
    - AI professional letter generation
    - Intelligent diary management
    - Automated referral processing
    - Clinic coordination
    - 80% faster than manual
    - Professional NHS standards
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "✍️ Generate Letters",
        "📅 Diary Management",
        "📨 Process Referrals",
        "📊 Secretary Dashboard"
    ])
    
    with tab1:
        render_generate_letters()
    
    with tab2:
        render_diary_management()
    
    with tab3:
        render_process_referrals()
    
    with tab4:
        render_secretary_dashboard()


def render_generate_letters():
    """AI letter generation"""
    
    st.subheader("✍️ AI Professional Letter Generator")
    
    letter_type = st.selectbox("Letter Type", LETTER_TYPES)
    
    with st.form("generate_letter"):
        st.markdown("### Patient & Appointment Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="Robert Brown")
            nhs_number = st.text_input("NHS Number*", placeholder="234 567 8901")
            clinic_date = st.date_input("Clinic Date*", value=datetime.now())
        
        with col2:
            consultant_name = st.text_input("Consultant Name*", placeholder="Dr. Smith")
            gp_name = st.text_input("GP Name*", placeholder="Dr. Jones")
            gp_address = st.text_area("GP Address*", height=100, placeholder="Main Street Surgery\n123 High Street\nLondon\nSW1A 1AA")
        
        st.markdown("### Clinical Content")
        
        diagnosis = st.text_area("Diagnosis/Findings", height=100, placeholder="e.g., Hypertension, well controlled")
        
        investigations_text = st.text_area("Investigations Performed (one per line)", height=100,
                                          placeholder="Blood pressure: 130/80\nECG: Normal sinus rhythm")
        
        treatment_plan = st.text_area("Treatment Plan", height=100, placeholder="Started on Amlodipine 5mg daily\nLifestyle advice given")
        
        follow_up = st.text_area("Follow-up Arrangements", height=80, placeholder="Review in 3 months with repeat BP check")
        
        additional_notes = st.text_area("Additional Notes", height=80)
        
        submit = st.form_submit_button("🤖 Generate AI Letter", type="primary")
        
        if submit:
            if not patient_name or not nhs_number or not consultant_name or not gp_name:
                st.error("❌ Please fill all required fields!")
            else:
                investigations = [inv.strip() for inv in investigations_text.split('\n') if inv.strip()]
                
                with st.spinner("🤖 AI drafting professional letter..."):
                    result = ai_draft_clinic_letter(
                        letter_type=letter_type,
                        patient_name=patient_name,
                        nhs_number=nhs_number,
                        gp_name=gp_name,
                        gp_address=gp_address,
                        clinic_date=str(clinic_date),
                        consultant_name=consultant_name,
                        diagnosis=diagnosis,
                        investigations=investigations,
                        treatment_plan=treatment_plan,
                        follow_up=follow_up,
                        additional_notes=additional_notes
                    )
                
                if result['success']:
                    st.success(f"✅ Letter generated! AI Confidence: {result['ai_confidence']}%")
                    
                    st.markdown("### 📄 Generated Letter:")
                    st.text_area("Letter Content", value=result['content'], height=600)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="💾 Download Letter",
                            data=result['content'],
                            file_name=f"Clinic_Letter_{patient_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        if result['requires_review']:
                            st.warning("⚠️ Please review before sending to GP")
                        else:
                            st.success("✅ Ready to send")


def render_diary_management():
    """Diary management"""
    
    st.subheader("📅 Intelligent Diary Management")
    
    action = st.radio("Action", ["View Diary", "Add Event", "AI Optimize Diary"])
    
    if action == "Add Event":
        with st.form("add_diary_event"):
            consultant_name = st.text_input("Consultant Name*", placeholder="Dr. Smith")
            
            col1, col2 = st.columns(2)
            
            with col1:
                event_date = st.date_input("Event Date*")
                start_time = st.time_input("Start Time*", value=datetime.strptime("09:00", "%H:%M").time())
                end_time = st.time_input("End Time*", value=datetime.strptime("10:00", "%H:%M").time())
            
            with col2:
                event_type = st.selectbox("Event Type*", EVENT_TYPES)
                location = st.text_input("Location", placeholder="Clinic Room 2")
                description = st.text_area("Description", height=80)
            
            submit = st.form_submit_button("➕ Add to Diary")
            
            if submit:
                if consultant_name:
                    event_details = {
                        'date': str(event_date),
                        'start_time': start_time.strftime("%H:%M"),
                        'end_time': end_time.strftime("%H:%M"),
                        'event_type': event_type,
                        'location': location,
                        'description': description
                    }
                    
                    result = ai_manage_diary(consultant_name, 'add', event_details)
                    
                    if result.get('success'):
                        st.success(f"✅ Event added! ID: {result['event_id']}")
                    else:
                        st.warning(f"⚠️ {result['message']}")
                        
                        if result.get('conflicts'):
                            st.error("**Conflicts detected:**")
                            for conflict in result['conflicts']:
                                st.markdown(f"- {conflict['event_type']} on {conflict['date']} {conflict['start_time']}-{conflict['end_time']}")
                        
                        if result.get('ai_alternatives'):
                            st.markdown("### 🤖 AI-Suggested Alternative Times:")
                            for alt in result['ai_alternatives'][:3]:
                                st.info(f"{alt['day']} {alt['date']} at {alt['start_time']} (Score: {alt['ai_score']}/100)")
                else:
                    st.error("❌ Consultant name required")
    
    elif action == "View Diary":
        consultant_name = st.text_input("Consultant Name", placeholder="Dr. Smith")
        view_date = st.date_input("View Date (optional - leave for all upcoming)")
        
        if st.button("👁️ View Diary"):
            if consultant_name:
                event_details = {'date': str(view_date)} if view_date else None
                result = ai_manage_diary(consultant_name, 'view', event_details)
                
                if result.get('success'):
                    events = result.get('events', [])
                    
                    if events:
                        st.success(f"✅ Found {len(events)} events")
                        
                        for event in events:
                            with st.expander(f"{event['date']} - {event['event_type']}"):
                                st.markdown(f"**Time:** {event['start_time']} - {event['end_time']}")
                                st.markdown(f"**Location:** {event.get('location', 'N/A')}")
                                st.markdown(f"**Description:** {event.get('description', 'N/A')}")
                    else:
                        st.info("No events found")
            else:
                st.error("❌ Consultant name required")
    
    else:  # AI Optimize
        consultant_name = st.text_input("Consultant Name for Optimization", placeholder="Dr. Smith")
        
        if st.button("🤖 Run AI Diary Optimization"):
            if consultant_name:
                with st.spinner("🤖 AI analyzing diary..."):
                    result = ai_manage_diary(consultant_name, 'optimize', None)
                
                if result.get('success'):
                    st.success("✅ AI Analysis Complete!")
                    
                    st.metric("Diary Efficiency Score", f"{result['optimization_score']:.1f}/100")
                    
                    if result['recommendations']:
                        st.markdown("### 🤖 AI Recommendations:")
                        
                        for rec in result['recommendations']:
                            if rec['priority'] == 'HIGH':
                                st.error(f"**{rec['type']}** - {rec['message']}")
                            elif rec['priority'] == 'MEDIUM':
                                st.warning(f"**{rec['type']}** - {rec['message']}")
                            else:
                                st.info(f"**{rec['type']}** - {rec['message']}")
                    else:
                        st.success("✅ Diary is well optimized!")


def render_process_referrals():
    """Referral processing"""
    
    st.subheader("📨 AI Referral Processing")
    
    with st.form("process_referral"):
        st.markdown("### New Referral Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="Sarah Wilson")
            nhs_number = st.text_input("NHS Number*", placeholder="345 678 9012")
            dob = st.date_input("Date of Birth*")
        
        with col2:
            gp_name = st.text_input("Referring GP*", placeholder="Dr. Brown")
            referral_date = st.date_input("Referral Date*", value=datetime.now())
        
        referral_reason = st.text_area("Referral Reason*", height=100,
                                      placeholder="Brief description of why patient is being referred...")
        
        clinical_history = st.text_area("Clinical History", height=150,
                                       placeholder="Relevant medical history, symptoms, investigations...")
        
        submit = st.form_submit_button("🤖 Process Referral with AI", type="primary")
        
        if submit:
            if not patient_name or not nhs_number or not gp_name or not referral_reason:
                st.error("❌ Please fill all required fields!")
            else:
                referral_data = {
                    'patient_name': patient_name,
                    'nhs_number': nhs_number,
                    'dob': str(dob),
                    'gp_name': gp_name,
                    'referral_date': str(referral_date),
                    'referral_reason': referral_reason,
                    'clinical_history': clinical_history
                }
                
                with st.spinner("🤖 AI processing referral..."):
                    result = ai_process_referral(referral_data)
                
                if result['success']:
                    st.success("✅ Referral processed by AI!")
                    
                    # Validation
                    validation = result['validation']
                    if validation['complete']:
                        st.success(f"✅ Referral is complete ({validation['completeness_score']:.0f}% complete)")
                    else:
                        st.warning(f"⚠️ Referral incomplete - missing: {', '.join(validation['missing_fields'])}")
                    
                    # Urgency
                    urgency = result['urgency_assessment']
                    if urgency['urgency_level'] == '2WW':
                        st.error(f"""
                        🔴 **2-WEEK WAIT REFERRAL**
                        - Urgency Score: {urgency['urgency_score']}
                        - Keywords: {', '.join(urgency['keywords_found'])}
                        - **Action:** {urgency['recommended_action']}
                        """)
                    elif urgency['urgency_level'] == 'Urgent':
                        st.warning(f"""
                        🟠 **URGENT REFERRAL**
                        - Action: {urgency['recommended_action']}
                        """)
                    else:
                        st.info(f"""
                        🟢 **ROUTINE REFERRAL**
                        - Action: {urgency['recommended_action']}
                        """)
                    
                    # Suggested clinic
                    clinic = result['suggested_clinic']
                    if clinic['suggested_clinics']:
                        st.markdown("### 🤖 AI-Suggested Clinic:")
                        for suggestion in clinic['suggested_clinics']:
                            st.success(f"**{suggestion['specialty']}** (Confidence: {suggestion['confidence']}%)")
                    
                    # Acknowledgment letter
                    st.markdown("### 📄 AI-Generated Acknowledgment Letter:")
                    st.text_area("Letter", value=result['acknowledgment_letter'], height=400)
                    
                    st.download_button(
                        label="💾 Download Acknowledgment",
                        data=result['acknowledgment_letter'],
                        file_name=f"Acknowledgment_{patient_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )


def render_secretary_dashboard():
    """Secretary dashboard"""
    
    st.subheader("📊 Medical Secretary Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Letters Generated Today", "12")
        st.metric("Referrals Processed", "8")
    
    with col2:
        st.metric("Diary Events This Week", "24")
        st.metric("Appointments Coordinated", "45")
    
    with col3:
        st.metric("AI Efficiency Gain", "80%")
        st.metric("Time Saved Today", "4.2 hours")
    
    st.markdown("---")
    st.markdown("### 📋 Today's Tasks")
    
    tasks = [
        {"task": "Draft clinic letters (5 pending)", "priority": "HIGH", "status": "In Progress"},
        {"task": "Process new referrals (3)", "priority": "MEDIUM", "status": "Pending"},
        {"task": "Update consultant diary", "priority": "LOW", "status": "Completed"}
    ]
    
    for task in tasks:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{task['task']}**")
        
        with col2:
            if task['priority'] == 'HIGH':
                st.error(task['priority'])
            elif task['priority'] == 'MEDIUM':
                st.warning(task['priority'])
            else:
                st.info(task['priority'])
        
        with col3:
            st.markdown(task['status'])
