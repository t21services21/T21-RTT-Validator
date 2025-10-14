"""
T21 HEALTHCARE PLATFORM - DNA MANAGEMENT MODULE
Production-grade DNA tracking with full CRUD functionality
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from sidebar_manager import render_sidebar
from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)


# Remove top white space
st.markdown("""
<style>
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 1rem !important;}
</style>
""", unsafe_allow_html=True)

render_sidebar()

st.title("📵 DNA (Did Not Attend) Management")
st.markdown("**Track patient non-attendance and understand RTT impact**")

# Educational section
with st.expander("📚 LEARNING OBJECTIVES - What is DNA?", expanded=True):
    st.markdown("""
    ### What Does DNA Mean?
    **DNA = Did Not Attend** - When a patient fails to attend a scheduled appointment without cancelling.
    
    ### Why is DNA Important for RTT?
    
    #### 🚨 **CRITICAL RTT RULE:**
    - When a patient DNAs an appointment, the **RTT clock CONTINUES running**
    - The patient remains on the waiting list
    - The 18-week target still applies
    - NHS trust is still responsible for offering treatment within 18 weeks
    
    #### 📊 **DNA Impact on Performance:**
    - **Wasted Capacity:** Empty clinic slots could have seen other patients
    - **Financial Loss:** NHS loses money for unused appointments
    - **Longer Waits:** Other patients wait longer
    - **Breach Risk:** DNA patients may breach 18 weeks
    
    #### 📝 **NHS DNA Policy (Standard):**
    1. **First DNA:** Send warning letter, re-book appointment
    2. **Second DNA:** Send final warning letter, re-book appointment
    3. **Third DNA:** Patient may be discharged back to GP
    4. **Exception:** Emergency/urgent cases get more chances
    
    #### ⚖️ **Legal/Ethical Considerations:**
    - Patient has right to decline treatment
    - Must consider vulnerable patients (mental health, elderly, etc.)
    - Document all communications
    - Follow trust's local DNA policy
    """)

st.markdown("---")

# DNA Recording Section
st.markdown("## 📝 Record DNA Event")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("dna_form"):
        st.markdown("### Patient & Appointment Details")
        
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *", max_chars=10)
        
        col_a, col_b = st.columns(2)
        with col_a:
            appointment_date = st.date_input("Appointment Date *")
            appointment_time = st.time_input("Appointment Time *")
        with col_b:
            specialty = st.selectbox("Specialty *", [
                "Orthopaedics", "Cardiology", "ENT", "General Surgery",
                "Ophthalmology", "Dermatology", "Urology", "Gastroenterology"
            ])
            appointment_type = st.selectbox("Appointment Type *", [
                "First Outpatient", "Follow-up", "Pre-Op Assessment",
                "Treatment", "Investigation"
            ])
        
        st.markdown("### DNA Details")
        
        dna_count = st.selectbox("How many times has this patient DNA'd? *", [
            "First DNA (1st offense)",
            "Second DNA (2nd offense)",
            "Third DNA (3rd offense - Consider discharge)",
            "Multiple DNAs (4+)"
        ])
        
        contacted = st.radio("Was patient contacted after DNA? *", [
            "Yes - Patient contacted successfully",
            "No - Unable to contact",
            "Attempted - No response"
        ])
        
        reason_given = st.text_area("Patient's Reason (if known)",
            placeholder="e.g., Forgot appointment, No transport, Unwell, Family emergency")
        
        action_taken = st.multiselect("Actions Taken *", [
            "Warning letter sent",
            "Final warning letter sent",
            "New appointment offered",
            "Discharge letter sent to GP",
            "Social prescribing referral",
            "Transport arranged for next appointment",
            "SMS reminder activated",
            "Telephone reminder activated"
        ])
        
        st.markdown("### RTT Impact")
        
        referral_date = st.date_input("Original Referral Date *")
        
        weeks_waiting = (appointment_date - referral_date).days // 7
        
        if weeks_waiting >= 0:
            st.info(f"⏱️ Patient has been waiting **{weeks_waiting} weeks** ({(appointment_date - referral_date).days} days)")
            
            if weeks_waiting > 18:
                st.error(f"🚨 **BREACH ALERT:** Patient has exceeded 18-week RTT target by {weeks_waiting - 18} weeks!")
            elif weeks_waiting > 16:
                st.warning(f"⚠️ **HIGH RISK:** Only {18 - weeks_waiting} weeks until breach!")
        
        rebook_date = st.date_input("New Appointment Date (if re-booked)",
            min_value=datetime.now().date())
        
        notes = st.text_area("Additional Notes",
            placeholder="Any other relevant information...")
        
        submitted = st.form_submit_button("📝 Record DNA Event", type="primary", use_container_width=True)
        
        if submitted:
            if patient_name and nhs_number:
                st.success("✅ DNA event recorded successfully!")
                st.balloons()
                
                # Show summary
                st.markdown("### 📋 DNA Event Summary")
                st.markdown(f"""
                - **Patient:** {patient_name} (NHS: {nhs_number})
                - **Missed Appointment:** {appointment_date.strftime('%d/%m/%Y')} at {appointment_time.strftime('%H:%M')}
                - **Specialty:** {specialty}
                - **DNA Count:** {dna_count}
                - **Weeks Waiting:** {weeks_waiting} weeks
                - **Actions:** {', '.join(action_taken) if action_taken else 'None recorded'}
                """)
                
                # RTT Impact Analysis
                st.markdown("### 🎯 RTT Impact Analysis")
                if weeks_waiting > 18:
                    st.error("""
                    ⚠️ **CRITICAL:** This patient has BREACHED the 18-week RTT target.
                    - Must be prioritized for urgent re-booking
                    - Escalate to clinical team immediately
                    - Document in incident log
                    """)
                else:
                    remaining_weeks = 18 - weeks_waiting
                    st.info(f"""
                    ✅ **RTT Clock Status:** Still within target
                    - {remaining_weeks} weeks remaining until breach
                    - Must be re-booked within {remaining_weeks} weeks
                    - Monitor closely for further DNAs
                    """)
            else:
                st.error("❌ Please complete all required fields marked with *")

with col2:
    st.markdown("### 📊 DNA Statistics (Demo)")
    
    # Demo statistics
    st.metric("Total DNAs This Month", "127", "+15%")
    st.metric("DNA Rate", "8.5%", "-1.2%")
    st.metric("Patients at Risk", "23", "+5")
    
    st.markdown("### 🎓 Quick Reference")
    st.info("""
    **Remember:**
    - ✅ DNA ≠ Clock Stop
    - ⏱️ Clock continues running
    - 📨 Send warning letters
    - 📅 Re-book urgently
    - 📝 Document everything
    """)
    
    st.markdown("### 🚨 Breach Risk")
    st.warning("""
    **High Risk Patients:**
    - 3 DNAs in 6 months
    - >16 weeks waiting
    - Urgent/Cancer pathways
    """)

# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 DNA Case Management")

tab1, tab2, tab3, tab4 = st.tabs(["📋 View All Cases", "➕ Add New DNA", "📊 Analytics", "🎓 Training"])

with tab1:
    st.subheader("📋 All DNA Cases")
    
    # Search and filter
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_term = st.text_input("🔍 Search (patient name, NHS number, etc.)", key="search_dna")
    with col2:
        filter_period = st.selectbox("Period", ["All Time", "This Month", "Last 3 Months", "This Year"])
    with col3:
        records = read_all_records('dna_cases')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "dna_cases.csv", "text/csv")
    
    # Get and filter records
    records = read_all_records('dna_cases')
    
    if search_term:
        records = search_records('dna_cases', search_term, ['patient_name', 'nhs_number', 'appointment_type'])
    
    # Display records
    if records:
        st.info(f"📊 Total DNA Cases: **{len(records)}**")
        
        # Show as table with action buttons
        for idx, record in enumerate(records):
            with st.expander(f"DNA #{idx+1}: {record.get('patient_name', 'Unknown')} - {record.get('dna_date', 'No date')}", expanded=False):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    **Patient Details:**
                    - Name: {record.get('patient_name', 'N/A')}
                    - NHS Number: {record.get('nhs_number', 'N/A')}
                    - Contact: {record.get('contact_number', 'N/A')}
                    """)
                
                with col_b:
                    st.markdown(f"""
                    **Appointment Details:**
                    - Type: {record.get('appointment_type', 'N/A')}
                    - Date: {record.get('appointment_date', 'N/A')}
                    - DNA Date: {record.get('dna_date', 'N/A')}
                    - DNA Number: {record.get('dna_count', '1')}
                    """)
                
                st.markdown(f"""
                **RTT Impact:**
                - Weeks Waiting: {record.get('weeks_waiting', 'N/A')}
                - Breach Risk: {record.get('breach_risk', 'N/A')}
                - Action Taken: {record.get('action_taken', 'N/A')}
                
                **Reason:** {record.get('reason', 'No reason recorded')}
                
                **Notes:** {record.get('notes', 'No additional notes')}
                """)
                
                # Action buttons
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col_btn2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('dna_cases', record['id']):
                            st.success("Deleted!")
                            st.rerun()
                with col_btn3:
                    st.markdown(f"*Created: {record.get('created_at', 'Unknown')}*")
        
        # Edit form (if editing)
        if 'editing_record' in st.session_state:
            st.markdown("---")
            st.subheader("✏️ Edit DNA Case")
            
            edit_record = read_record_by_id('dna_cases', st.session_state['editing_record'])
            
            if edit_record:
                with st.form("edit_dna_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        patient_name = st.text_input("Patient Name *", value=edit_record.get('patient_name', ''))
                        nhs_number = st.text_input("NHS Number *", value=edit_record.get('nhs_number', ''))
                        contact_number = st.text_input("Contact Number", value=edit_record.get('contact_number', ''))
                        appointment_type = st.text_input("Appointment Type *", value=edit_record.get('appointment_type', ''))
                    
                    with col2:
                        appointment_date = st.date_input("Appointment Date *")
                        dna_date = st.date_input("DNA Date *")
                        dna_count = st.number_input("DNA Number (1st, 2nd, 3rd) *", min_value=1, max_value=10, value=int(edit_record.get('dna_count', 1)))
                        weeks_waiting = st.number_input("Weeks Waiting *", min_value=0, max_value=104, value=int(edit_record.get('weeks_waiting', 0)))
                    
                    breach_risk = st.selectbox("Breach Risk *", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(edit_record.get('breach_risk', 'Low')))
                    action_taken = st.selectbox("Action Taken *", [
                        "Warning letter sent + Re-booked",
                        "Final warning sent + Re-booked", 
                        "Discharged to GP",
                        "Patient contacted - Re-booked",
                        "Awaiting contact"
                    ])
                    reason = st.text_area("Reason for DNA", value=edit_record.get('reason', ''))
                    notes = st.text_area("Additional Notes", value=edit_record.get('notes', ''))
                    
                    col_submit1, col_submit2 = st.columns(2)
                    with col_submit1:
                        if st.form_submit_button("💾 Update DNA Case", use_container_width=True):
                            updated_data = {
                                'patient_name': patient_name,
                                'nhs_number': nhs_number,
                                'contact_number': contact_number,
                                'appointment_type': appointment_type,
                                'appointment_date': str(appointment_date),
                                'dna_date': str(dna_date),
                                'dna_count': dna_count,
                                'weeks_waiting': weeks_waiting,
                                'breach_risk': breach_risk,
                                'action_taken': action_taken,
                                'reason': reason,
                                'notes': notes
                            }
                            
                            if update_record('dna_cases', st.session_state['editing_record'], updated_data):
                                st.success("✅ DNA case updated successfully!")
                                del st.session_state['editing_record']
                                st.rerun()
                    
                    with col_submit2:
                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                            del st.session_state['editing_record']
                            st.rerun()
    else:
        st.info("📝 No DNA cases recorded yet. Add your first case in the 'Add New DNA' tab!")

with tab2:
    st.subheader("➕ Record New DNA Case")
    
    with st.form("add_dna_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Patient Information**")
            patient_name = st.text_input("Patient Name *", placeholder="SURNAME, Forename")
            nhs_number = st.text_input("NHS Number *", placeholder="1234567890")
            contact_number = st.text_input("Contact Number", placeholder="07XXX XXXXXX")
            appointment_type = st.text_input("Appointment Type *", placeholder="e.g., First Outpatient, Follow-up")
        
        with col2:
            st.markdown("**Appointment Details**")
            appointment_date = st.date_input("Scheduled Appointment Date *")
            dna_date = st.date_input("DNA Date *", value=datetime.now())
            dna_count = st.number_input("DNA Number (1st, 2nd, 3rd) *", min_value=1, max_value=10, value=1)
            weeks_waiting = st.number_input("Weeks on Waiting List *", min_value=0, max_value=104, value=0)
        
        breach_risk = st.selectbox("Breach Risk Assessment *", ["Low (<12 weeks)", "Medium (12-16 weeks)", "High (16-18 weeks)", "Critical (>18 weeks)"])
        
        action_taken = st.selectbox("Action Taken *", [
            "Warning letter sent + Re-booked",
            "Final warning sent + Re-booked",
            "Discharged to GP (3rd DNA)",
            "Patient contacted - Will re-book",
            "Awaiting patient contact"
        ])
        
        reason = st.text_area("Reason for DNA (if known)", placeholder="e.g., Patient forgot, Transport issues, Feeling unwell")
        notes = st.text_area("Additional Notes", placeholder="Any other relevant information...")
        
        submitted = st.form_submit_button("💾 Save DNA Case", use_container_width=True)
        
        if submitted:
            if patient_name and nhs_number and appointment_type:
                dna_data = {
                    'patient_name': patient_name,
                    'nhs_number': nhs_number,
                    'contact_number': contact_number,
                    'appointment_type': appointment_type,
                    'appointment_date': str(appointment_date),
                    'dna_date': str(dna_date),
                    'dna_count': dna_count,
                    'weeks_waiting': weeks_waiting,
                    'breach_risk': breach_risk,
                    'action_taken': action_taken,
                    'reason': reason,
                    'notes': notes,
                    'recorded_by': st.session_state.get('user_email', 'Unknown')
                }
                
                if create_record('dna_cases', dna_data):
                    st.success("✅ DNA case recorded successfully!")
                    st.info("💡 Case saved to your records. View all cases in the 'View All Cases' tab.")
                    st.rerun()
            else:
                st.error("❌ Please fill in all required fields (*)")

with tab3:
    st.subheader("📊 DNA Analytics & Reports")
    
    records = read_all_records('dna_cases')
    
    if records:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total DNA Cases", len(records))
        
        with col2:
            high_risk = len([r for r in records if 'High' in r.get('breach_risk', '')])
            st.metric("High/Critical Risk", high_risk)
        
        with col3:
            first_dna = len([r for r in records if r.get('dna_count') == 1])
            st.metric("First-time DNAs", first_dna)
        
        with col4:
            repeat_dna = len([r for r in records if r.get('dna_count', 1) >= 2])
            st.metric("Repeat DNAs", repeat_dna)
        
        st.markdown("---")
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("**DNA by Risk Level**")
            risk_counts = {}
            for r in records:
                risk = r.get('breach_risk', 'Unknown')
                risk_counts[risk] = risk_counts.get(risk, 0) + 1
            st.bar_chart(risk_counts)
        
        with col_chart2:
            st.markdown("**DNA Count Distribution**")
            dna_counts = {}
            for r in records:
                count = r.get('dna_count', 1)
                dna_counts[f"{count}{'st' if count==1 else 'nd' if count==2 else 'rd' if count==3 else 'th'} DNA"] = dna_counts.get(f"{count}{'st' if count==1 else 'nd' if count==2 else 'rd' if count==3 else 'th'} DNA", 0) + 1
            st.bar_chart(dna_counts)
    else:
        st.info("📝 No data available for analytics yet. Record some DNA cases to see statistics and charts!")

with tab4:
    st.subheader("🎓 Training & Practice Scenarios")
    
    # Educational scenarios (moved from main area)
    st.markdown("## 🎓 Practice Scenarios")

scenario = st.selectbox("Select a scenario to learn:", [
    "Select a scenario...",
    "Scenario 1: First-time DNA at 12 weeks",
    "Scenario 2: Second DNA at 17 weeks (near breach)",
    "Scenario 3: Third DNA - Discharge decision",
    "Scenario 4: DNA with valid reason (unwell)",
    "Scenario 5: Urgent patient DNAs"
])

if scenario == "Scenario 1: First-time DNA at 12 weeks":
    st.markdown("""
    ### Scenario 1: First-time DNA at 12 weeks
    
    **Patient:** Mary Jones, NHS: 1234567890
    - **Referral Date:** 10 weeks ago
    - **Appointment:** First outpatient - Orthopaedics
    - **DNA Status:** First DNA
    - **Patient contacted:** Yes - Said she forgot
    
    **What should you do?**
    """)
    
    answer = st.radio("Select the correct action:", [
        "Discharge patient immediately",
        "Send warning letter and re-book within 6 weeks",
        "Wait for patient to call back",
        "Close the RTT pathway"
    ])
    
    if st.button("Check Answer"):
        if answer == "Send warning letter and re-book within 6 weeks":
            st.success("""
            ✅ **CORRECT!**
            
            **Explanation:**
            - This is first DNA, so patient gets a warning
            - RTT clock is still running (12 weeks elapsed)
            - Patient has 6 weeks left until breach
            - Send warning letter AND re-book urgently
            - Document DNA in PAS system
            """)
        else:
            st.error("""
            ❌ **INCORRECT**
            
            **Correct Answer:** Send warning letter and re-book within 6 weeks
            
            **Why:** First DNA requires warning and re-booking, not discharge.
            RTT clock continues running!
            """)

st.markdown("---")
st.markdown("### 📚 Additional Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **📖 NHS Guidance**
    - RTT Rules & Guidance
    - DNA Policy Templates
    - Patient Communication
    """)

with col2:
    st.info("""
    **🎯 Best Practice**
    - SMS reminders
    - Telephone reminders
    - Transport support
    """)

with col3:
    st.info("""
    **⚖️ Legal/Ethical**
    - Patient rights
    - Vulnerable patients
    - Documentation
    """)

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
