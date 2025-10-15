"""
CLINICAL LETTER GENERATOR UI
Interface for creating and managing clinical letters
"""

import streamlit as st
from datetime import datetime
from clinical_letters import (
    LETTER_TEMPLATES,
    generate_mdt_gp_letter,
    generate_mdt_patient_letter,
    generate_appointment_confirmation_letter,
    generate_referral_letter,
    generate_discharge_summary,
    format_letter_for_print
)


def render_clinical_letters():
    """Main clinical letters interface"""
    
    st.header("📄 Clinical Letter Generator")
    st.markdown("**Professional Clinical Letters & Communications**")
    
    st.success("""
    📝 **Automated Letter Generation**
    - MDT outcome letters (GP & Patient)
    - Appointment confirmations
    - Referral letters
    - Discharge summaries
    - Print-ready formatting
    """)
    
    # Tabs for different letter types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✉️ MDT Letters",
        "📅 Appointment Letters",
        "📨 Referrals",
        "📋 Discharge",
        "📚 Templates"
    ])
    
    with tab1:
        render_mdt_letters()
    
    with tab2:
        render_appointment_letters()
    
    with tab3:
        render_referral_letters()
    
    with tab4:
        render_discharge_letters()
    
    with tab5:
        render_letter_templates()


def render_mdt_letters():
    """MDT outcome letters"""
    st.markdown("### ✉️ MDT Outcome Letters")
    
    letter_type = st.radio("Letter Type", ["To GP", "To Patient"], horizontal=True)
    
    if letter_type == "To GP":
        render_mdt_gp_letter_form()
    else:
        render_mdt_patient_letter_form()


def render_mdt_gp_letter_form():
    """Form for MDT GP letter"""
    st.markdown("#### Letter to GP - MDT Outcome")
    
    with st.form("mdt_gp_letter"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
            nhs_number = st.text_input("NHS Number*", placeholder="123 456 7890")
            meeting_date = st.date_input("MDT Date*", value=datetime.now())
            specialty = st.text_input("Specialty*", placeholder="Oncology")
            diagnosis = st.text_area("Diagnosis*", placeholder="Clinical diagnosis...")
        
        with col2:
            gp_name = st.text_input("GP Name*", placeholder="Dr Jones")
            gp_practice = st.text_input("GP Practice*", placeholder="City Medical Centre")
            consultant_name = st.text_input("Consultant Name", value="Consultant")
            mdt_outcome = st.selectbox("MDT Outcome*", [
                "Radiotherapy recommended",
                "Surgery recommended",
                "Chemotherapy recommended",
                "Palliative care",
                "Continue monitoring",
                "Discharge back to GP"
            ])
        
        mdt_decision = st.text_area("Management Plan*", height=100, 
                                    placeholder="Detailed management plan from MDT...")
        
        actions = st.text_area("Actions Required (one per line)*", height=100,
                              placeholder="Book surgery within 4 weeks\nArrange chemotherapy\nFollow-up in 6 weeks")
        
        next_steps = st.text_area("Next Steps*", height=80,
                                  placeholder="Patient to be seen in clinic in 2 weeks...")
        
        if st.form_submit_button("📄 Generate Letter", type="primary"):
            if all([patient_name, nhs_number, gp_name, gp_practice, diagnosis, mdt_decision, actions, next_steps]):
                actions_list = [a.strip() for a in actions.split('\n') if a.strip()]
                
                letter = generate_mdt_gp_letter(
                    patient_name=patient_name,
                    nhs_number=nhs_number,
                    gp_name=gp_name,
                    gp_practice=gp_practice,
                    meeting_date=str(meeting_date),
                    specialty=specialty,
                    diagnosis=diagnosis,
                    mdt_outcome=mdt_outcome,
                    mdt_decision=mdt_decision,
                    actions=actions_list,
                    next_steps=next_steps,
                    consultant_name=consultant_name
                )
                
                st.session_state['generated_letter'] = letter
                st.session_state['letter_type'] = 'MDT_GP'
                st.success("✅ Letter generated!")
                st.rerun()
            else:
                st.error("❌ Please fill all required fields")
    
    # Display generated letter
    if st.session_state.get('generated_letter') and st.session_state.get('letter_type') == 'MDT_GP':
        st.markdown("---")
        st.markdown("### 📄 Generated Letter")
        st.text_area("Letter Content", value=st.session_state['generated_letter'], height=400)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "💾 Download as Text",
                data=st.session_state['generated_letter'],
                file_name=f"MDT_GP_Letter_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        with col2:
            if st.button("🖨️ Print Version"):
                html_letter = format_letter_for_print(st.session_state['generated_letter'])
                st.components.v1.html(html_letter, height=600, scrolling=True)
        with col3:
            if st.button("🗑️ Clear"):
                del st.session_state['generated_letter']
                del st.session_state['letter_type']
                st.rerun()


def render_mdt_patient_letter_form():
    """Form for MDT patient letter"""
    st.markdown("#### Letter to Patient - MDT Outcome")
    
    with st.form("mdt_patient_letter"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
            patient_address = st.text_area("Patient Address*", height=80, 
                                          placeholder="123 Main Street\nCity\nPostcode")
            meeting_date = st.date_input("MDT Date*", value=datetime.now())
            specialty = st.text_input("Specialty*", placeholder="Oncology")
        
        with col2:
            diagnosis = st.text_input("Diagnosis*", placeholder="Clinical diagnosis...")
            mdt_outcome = st.text_input("Recommended Treatment*", placeholder="Surgery and chemotherapy")
            consultant_name = st.text_input("Consultant Name", value="Consultant")
            contact_number = st.text_input("Contact Number", value="01234 567890")
        
        treatment_plan = st.text_area("Treatment Plan (Plain English)*", height=100,
                                      placeholder="You will have surgery to remove the tumor, followed by chemotherapy...")
        
        next_appointment = st.text_area("What Happens Next*", height=80,
                                       placeholder="You will receive an appointment for surgery within 2 weeks...")
        
        if st.form_submit_button("📄 Generate Letter", type="primary"):
            if all([patient_name, patient_address, diagnosis, treatment_plan, next_appointment]):
                letter = generate_mdt_patient_letter(
                    patient_name=patient_name,
                    patient_address=patient_address,
                    meeting_date=str(meeting_date),
                    specialty=specialty,
                    diagnosis=diagnosis,
                    mdt_outcome=mdt_outcome,
                    treatment_plan=treatment_plan,
                    next_appointment=next_appointment,
                    contact_number=contact_number,
                    consultant_name=consultant_name
                )
                
                st.session_state['generated_letter'] = letter
                st.session_state['letter_type'] = 'MDT_PATIENT'
                st.success("✅ Letter generated!")
                st.rerun()
            else:
                st.error("❌ Please fill all required fields")
    
    # Display generated letter
    if st.session_state.get('generated_letter') and st.session_state.get('letter_type') == 'MDT_PATIENT':
        st.markdown("---")
        st.markdown("### 📄 Generated Letter")
        st.text_area("Letter Content", value=st.session_state['generated_letter'], height=400)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "💾 Download as Text",
                data=st.session_state['generated_letter'],
                file_name=f"MDT_Patient_Letter_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        with col2:
            if st.button("🖨️ Print Version"):
                html_letter = format_letter_for_print(st.session_state['generated_letter'])
                st.components.v1.html(html_letter, height=600, scrolling=True)
        with col3:
            if st.button("🗑️ Clear"):
                del st.session_state['generated_letter']
                del st.session_state['letter_type']
                st.rerun()


def render_appointment_letters():
    """Appointment confirmation letters"""
    st.markdown("### 📅 Appointment Confirmation Letters")
    
    with st.form("appointment_letter"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*")
            patient_address = st.text_area("Patient Address*", height=80)
            nhs_number = st.text_input("NHS Number*")
            appointment_date = st.date_input("Appointment Date*")
            appointment_time = st.time_input("Appointment Time*")
        
        with col2:
            appointment_type = st.text_input("Appointment Type*", value="Outpatient Consultation")
            location = st.text_input("Location*", value="Clinic Room 2")
            consultant_name = st.text_input("Consultant*", value="Dr Smith")
            specialty = st.text_input("Specialty*", value="Cardiology")
            contact_number = st.text_input("Contact Number", value="01234 567890")
        
        special_instructions = st.text_area("Special Instructions (optional)", height=80,
                                           placeholder="Please fast for 12 hours before appointment...")
        
        if st.form_submit_button("📄 Generate Letter", type="primary"):
            if all([patient_name, patient_address, nhs_number]):
                letter = generate_appointment_confirmation_letter(
                    patient_name=patient_name,
                    patient_address=patient_address,
                    nhs_number=nhs_number,
                    appointment_date=str(appointment_date),
                    appointment_time=appointment_time.strftime("%H:%M"),
                    appointment_type=appointment_type,
                    location=location,
                    consultant_name=consultant_name,
                    specialty=specialty,
                    special_instructions=special_instructions,
                    contact_number=contact_number
                )
                
                st.session_state['generated_letter'] = letter
                st.success("✅ Letter generated!")
                st.rerun()
            else:
                st.error("❌ Please fill all required fields")
    
    if st.session_state.get('generated_letter'):
        display_generated_letter()


def render_referral_letters():
    """Referral letter generator"""
    st.markdown("### 📨 Referral Letters")
    
    st.info("Generate professional referral letters to other specialties")
    
    with st.form("referral_letter"):
        st.markdown("#### Patient Details")
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*")
            nhs_number = st.text_input("NHS Number*")
            date_of_birth = st.date_input("Date of Birth*")
        
        with col2:
            priority = st.selectbox("Priority*", ["Routine", "Urgent", "2-Week Wait"])
        
        st.markdown("#### Referral Information")
        col1, col2 = st.columns(2)
        
        with col1:
            referring_clinician = st.text_input("Your Name*", value="Dr Smith")
            referring_specialty = st.text_input("Your Specialty*", value="General Surgery")
        
        with col2:
            receiving_clinician = st.text_input("Receiving Clinician*", value="Dr Jones")
            receiving_specialty = st.text_input("Receiving Specialty*", value="Cardiology")
        
        referral_reason = st.text_area("Reason for Referral*", height=80)
        clinical_history = st.text_area("Clinical History*", height=100)
        current_medications = st.text_area("Current Medications*", height=80)
        investigations = st.text_area("Investigations Performed*", height=80)
        
        if st.form_submit_button("📄 Generate Letter", type="primary"):
            if all([patient_name, nhs_number, referral_reason, clinical_history]):
                letter = generate_referral_letter(
                    patient_name=patient_name,
                    nhs_number=nhs_number,
                    date_of_birth=str(date_of_birth),
                    referring_clinician=referring_clinician,
                    referring_specialty=referring_specialty,
                    receiving_clinician=receiving_clinician,
                    receiving_specialty=receiving_specialty,
                    referral_reason=referral_reason,
                    clinical_history=clinical_history,
                    current_medications=current_medications,
                    investigations=investigations,
                    priority=priority
                )
                
                st.session_state['generated_letter'] = letter
                st.success("✅ Letter generated!")
                st.rerun()
            else:
                st.error("❌ Please fill all required fields")
    
    if st.session_state.get('generated_letter'):
        display_generated_letter()


def render_discharge_letters():
    """Discharge summary generator"""
    st.markdown("### 📋 Discharge Summaries")
    
    st.info("Generate comprehensive discharge summaries for GPs")
    
    # Implementation similar to above
    st.markdown("**Coming soon:** Full discharge summary generator")


def render_letter_templates():
    """View and manage letter templates"""
    st.markdown("### 📚 Letter Templates")
    
    for template_id, template_info in LETTER_TEMPLATES.items():
        with st.expander(f"📄 {template_info['name']}"):
            st.markdown(f"**Description:** {template_info['description']}")
            st.markdown(f"**Template ID:** {template_id}")


def display_generated_letter():
    """Display generated letter with actions"""
    st.markdown("---")
    st.markdown("### 📄 Generated Letter")
    st.text_area("Letter Content", value=st.session_state['generated_letter'], height=400, key="letter_display")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "💾 Download as Text",
            data=st.session_state['generated_letter'],
            file_name=f"Clinical_Letter_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            key="download_letter"
        )
    with col2:
        if st.button("🖨️ Print Version", key="print_letter"):
            html_letter = format_letter_for_print(st.session_state['generated_letter'])
            st.components.v1.html(html_letter, height=600, scrolling=True)
    with col3:
        if st.button("🗑️ Clear", key="clear_letter"):
            del st.session_state['generated_letter']
            st.rerun()
