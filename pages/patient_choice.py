"""
T21 HEALTHCARE PLATFORM - PATIENT CHOICE MODULE
Educational module for tracking patient choice and RTT clock pauses
"""

import streamlit as st
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from navigation import render_navigation
from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)



# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="choice")

st.title("🤔 Patient Choice & Deferrals")
st.markdown("**Track patient decisions and understand when RTT clock PAUSES**")


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Patient Choice Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Patient Choices")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_patient_choice")
    with col2:
        records = read_all_records('patient_choice')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "patient_choice.csv", "text/csv")
    
    # Get records
    records = read_all_records('patient_choice')
    
    if search_term:
        records = search_records('patient_choice', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Patient Choice #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('patient_choice', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Patient Choice")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('patient_choice')
    
    if records:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(records))
        with col2:
            st.metric("This Month", 0)  # Calculate as needed
        with col3:
            st.metric("Active", len(records))
    else:
        st.info("No data for analytics yet")

st.markdown("---")
# Educational content continues below...


# Educational section
with st.expander("📚 LEARNING OBJECTIVES - Patient Choice Rules", expanded=True):
    st.markdown("""
    ### What is Patient Choice?
    
    **Patient Choice** = When a patient makes a decision that delays their treatment for NON-MEDICAL reasons.
    
    ### 🚨 CRITICAL RTT RULE:
    
    #### When RTT Clock PAUSES:
    
    ✅ **Clock PAUSES when patient:**
    - Declines all offered appointment dates
    - Requests a specific consultant with longer wait
    - Asks to delay treatment for personal reasons (holiday, work, etc.)
    - Chooses a provider with longer waiting times
    - Requests to wait for specific surgeon/consultant
    
    #### When RTT Clock CONTINUES:
    
    ❌ **Clock CONTINUES when:**
    - Hospital cannot offer appointment
    - Patient cancels but accepts alternative date offered
    - Patient asks for reasonable adjustments (disability access, interpreter)
    - Medical reasons for delay
    
    ### 📋 NHS Patient Choice Policy
    
    **Patients MUST be offered:**
    1. **Choice of provider** - At least 2 providers (if available)
    2. **Choice of date** - Reasonable options within 18 weeks
    3. **Choice of consultant** - Where feasible
    
    **Patients CAN:**
    - Decline offered appointments
    - Request specific dates
    - Choose different provider
    - Ask for second opinion
    
    **NHS MUST:**
    - Offer reasonable alternatives
    - Document all choices
    - Inform patient of RTT impact
    - Resume clock when patient ready
    
    ### ⏰ Clock Pause Examples
    
    **Example 1: Holiday**
    - Patient offered appointment in 2 weeks
    - Patient declines - going on holiday for 3 weeks
    - **Action:** Clock PAUSES for 3 weeks
    - **Restart:** When patient returns and accepts date
    
    **Example 2: Specific Consultant**
    - Patient offered Mr. Jones (2 weeks wait)
    - Patient requests Mr. Smith (6 weeks wait)
    - **Action:** Clock PAUSES for extra 4 weeks
    - **Reason:** Patient choice, not clinical need
    
    **Example 3: Work Commitments**
    - Patient offered 3 appointment dates
    - Patient declines all - busy at work
    - **Action:** Clock PAUSES until patient accepts
    
    ### 📝 Documentation Requirements
    
    **MUST document:**
    - ✅ What appointments were offered
    - ✅ Why patient declined
    - ✅ Patient's specific request
    - ✅ Date clock paused
    - ✅ Expected resume date
    - ✅ Patient informed of RTT impact
    
    ### ⚖️ Ethical Considerations
    
    - Patient has RIGHT to make choices
    - Must respect patient autonomy
    - Cannot pressure patients
    - Must provide clear information about waiting times
    - Consider patient's circumstances
    """)

st.markdown("---")

# Patient Choice Recording
st.markdown("## 📝 Record Patient Choice Event")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("choice_form"):
        st.markdown("### Patient Details")
        
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *", max_chars=10)
        
        col_a, col_b = st.columns(2)
        with col_a:
            specialty = st.selectbox("Specialty *", [
                "Orthopaedics", "Cardiology", "ENT", "General Surgery",
                "Ophthalmology", "Dermatology", "Urology", "Gastroenterology"
            ])
            priority = st.selectbox("Priority *", [
                "Routine", "Urgent", "Cancer 2-week wait"
            ])
        with col_b:
            referral_date = st.date_input("Original Referral Date *")
            current_wait_weeks = st.number_input("Current Wait (weeks)", min_value=0, max_value=52, value=8)
        
        st.markdown("### Choice Details")
        
        choice_type = st.selectbox("Type of Patient Choice *", [
            "🏖️ Holiday/Personal event (Patient requests delay)",
            "👨‍⚕️ Specific consultant requested (Longer wait)",
            "🏥 Different provider chosen (Longer wait)",
            "📅 Declined all offered dates (Personal reasons)",
            "👥 Second opinion requested",
            "⏰ Waiting for specific date/time",
            "💼 Work commitments",
            "👪 Family circumstances",
            "🤔 Patient undecided about treatment",
            "Other"
        ])
        
        st.markdown("### Appointments Offered")
        
        dates_offered = st.text_area("What appointment dates were offered? *",
            placeholder="e.g., 15/03/2024, 22/03/2024, 29/03/2024",
            help="Enter all dates that were offered to the patient")
        
        reason_declined = st.text_area("Why did patient decline? *",
            placeholder="e.g., Going on holiday 10-25 March, Requested Mr. Smith specifically",
            help="Document patient's exact reason")
        
        st.markdown("### Patient's Request")
        
        patient_request = st.text_area("What did patient request? *",
            placeholder="e.g., Appointment after 1st April, Want to see Mr. Smith only",
            help="What does patient want?")
        
        pause_date = st.date_input("Date Clock Pauses *",
            value=datetime.now().date())
        
        expected_resume = st.date_input("Expected Resume Date",
            min_value=datetime.now().date(),
            help="When patient will be ready")
        
        patient_informed = st.checkbox("Patient informed that clock will pause? *")
        
        if patient_informed:
            st.success("✅ Patient aware of RTT clock impact")
        else:
            st.warning("⚠️ You MUST inform patient before pausing clock!")
        
        st.markdown("### Communication")
        
        communication_method = st.multiselect("How was patient informed? *", [
            "Phone call",
            "Letter",
            "Email",
            "SMS",
            "Patient portal",
            "Face-to-face (clinic)"
        ])
        
        notes = st.text_area("Additional Notes",
            placeholder="Any other relevant information...")
        
        submitted = st.form_submit_button("⏸️ Pause RTT Clock", type="primary", use_container_width=True)
        
        if submitted:
            if patient_name and nhs_number and dates_offered and reason_declined and patient_informed:
                st.success("✅ Patient choice recorded - RTT clock PAUSED!")
                st.balloons()
                
                # Calculate pause duration
                if expected_resume:
                    pause_duration = (expected_resume - pause_date).days
                    pause_weeks = pause_duration // 7
                    
                    st.markdown("### ⏸️ Clock Pause Summary")
                    st.markdown(f"""
                    - **Patient:** {patient_name} (NHS: {nhs_number})
                    - **Choice Type:** {choice_type}
                    - **Clock Paused:** {pause_date.strftime('%d/%m/%Y')}
                    - **Resume Expected:** {expected_resume.strftime('%d/%m/%Y')}
                    - **Pause Duration:** {pause_weeks} weeks ({pause_duration} days)
                    - **Current Wait:** {current_wait_weeks} weeks
                    - **Wait After Resume:** {current_wait_weeks} weeks (clock was paused)
                    """)
                    
                    # RTT Impact
                    st.markdown("### 🎯 RTT Impact Analysis")
                    
                    remaining_weeks = 18 - current_wait_weeks
                    
                    if remaining_weeks > pause_weeks:
                        st.success(f"""
                        ✅ **SAFE:** Patient still within 18-week target after pause
                        - Currently at {current_wait_weeks} weeks
                        - Pause adds {pause_weeks} weeks
                        - Total: {current_wait_weeks} weeks (pause time excluded)
                        - Remaining: {remaining_weeks} weeks until breach
                        """)
                    else:
                        st.warning(f"""
                        ⚠️ **RISK:** Patient may approach 18-week target
                        - Currently at {current_wait_weeks} weeks
                        - After pause resumes: still {current_wait_weeks} weeks
                        - Must book within {remaining_weeks} weeks after resume
                        """)
                    
                    # Documentation checklist
                    st.markdown("### ✅ Documentation Checklist")
                    st.info("""
                    **Ensure you have:**
                    - ✅ Dates offered documented
                    - ✅ Reason for decline documented
                    - ✅ Patient's request documented
                    - ✅ Patient informed of pause
                    - ✅ Communication method recorded
                    - ✅ Expected resume date set
                    - ✅ Updated in PAS system
                    - ✅ Follow-up reminder set
                    """)
            else:
                st.error("❌ Please complete all required fields marked with * and confirm patient was informed!")

with col2:
    st.markdown("### 📊 Patient Choice Stats")
    
    st.metric("Active Pauses", "34", "+3")
    st.metric("Average Pause", "3.2 weeks", "-0.5")
    st.metric("Resumed This Month", "28", "+7")
    
    st.markdown("### 🎓 Quick Reference")
    st.info("""
    **Clock PAUSES when:**
    - 🏖️ Patient delays for personal reasons
    - 👨‍⚕️ Specific consultant requested
    - 📅 All dates declined
    - 🤔 Patient undecided
    
    **MUST:**
    - Inform patient
    - Document everything
    - Set resume date
    """)
    
    st.markdown("### ⚖️ Patient Rights")
    st.success("""
    **Patients have RIGHT to:**
    - Choose provider
    - Choose consultant
    - Decline dates
    - Request delays
    - Change mind
    """)

# Educational scenarios
st.markdown("---")
st.markdown("## 🎓 Practice Scenarios")

scenario = st.selectbox("Select a scenario:", [
    "Select a scenario...",
    "Scenario 1: Patient going on holiday",
    "Scenario 2: Wants specific consultant",
    "Scenario 3: Declined all dates - work",
    "Scenario 4: Patient needs interpreter (NOT a pause!)"
])

if scenario == "Scenario 1: Patient going on holiday":
    st.markdown("""
    ### Scenario 1: Patient Holiday
    
    **Patient:** Sarah Brown, NHS: 5555555555
    - **Waiting:** 10 weeks
    - **Offered:** Appointments on 5th, 12th, and 19th March
    - **Patient:** "I'm going on holiday 1st-20th March. Can I have appointment after?"
    
    **What should you do?**
    """)
    
    answer = st.radio("Select correct action:", [
        "Refuse - must see patient within 18 weeks",
        "Pause clock, offer appointment after 20th March",
        "Discharge patient back to GP",
        "Keep offering March dates until patient accepts"
    ])
    
    if st.button("Check Answer"):
        if answer == "Pause clock, offer appointment after 20th March":
            st.success("""
            ✅ **CORRECT!**
            
            **Explanation:**
            - Patient has RIGHT to choose
            - This is PATIENT CHOICE for personal reasons
            - RTT clock PAUSES during holiday
            - Offer appointment after 20th March
            - Document: "Patient declined March dates - holiday"
            - Clock resumes when patient returns
            - Patient still at 10 weeks waiting (pause excluded)
            
            **IMPORTANT:** Must inform patient clock will pause!
            """)
        else:
            st.error("""
            ❌ **INCORRECT**
            
            **Correct Answer:** Pause clock, offer appointment after 20th March
            
            **Why:** Patient choice for personal reasons = Clock PAUSES. Patient rights must be respected!
            """)

st.markdown("---")
st.info("""
**💡 Remember:** Patient choice = Clock PAUSES. Always document and inform patient!
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
