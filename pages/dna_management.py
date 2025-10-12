"""
T21 HEALTHCARE PLATFORM - DNA MANAGEMENT MODULE
Educational module for tracking Did Not Attend (DNA) appointments
"""

import streamlit as st
from datetime import datetime, timedelta
from navigation import render_navigation
import pandas as pd

st.set_page_config(page_title="DNA Management | T21 Services", page_icon="📵", layout="wide")

# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="dna")

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

# Educational scenarios
st.markdown("---")
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
