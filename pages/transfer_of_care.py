"""
T21 HEALTHCARE PLATFORM - TRANSFER OF CARE MODULE
Educational module for managing patient transfers between providers/specialties
"""

import streamlit as st
from datetime import datetime, timedelta
from navigation import render_navigation

st.set_page_config(page_title="Transfer of Care | T21 Services", page_icon="🔄", layout="wide")

# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="transfer")

st.title("🔄 Transfer of Care Management")
st.markdown("**Track patient transfers and RTT clock responsibility**")

# Educational section
with st.expander("📚 LEARNING OBJECTIVES - Transfer Rules", expanded=True):
    st.markdown("""
    ### What is Transfer of Care?
    
    **Transfer of Care** = When a patient moves between providers, specialties, or care settings while on RTT pathway.
    
    ### 🚨 CRITICAL RTT RULES FOR TRANSFERS:
    
    #### 1️⃣ **Inter-Provider Transfer** (Between NHS Trusts)
    
    **Clock TRANSFERS to new provider:**
    - Patient moves from Trust A to Trust B
    - RTT clock continues running
    - New provider inherits the RTT responsibility
    - Original provider no longer responsible for 18-week target
    
    **Example:**
    - Patient at 10 weeks at Hospital A
    - Transfers to Hospital B
    - Hospital B now responsible for seeing patient within remaining 8 weeks
    
    #### 2️⃣ **Inter-Specialty Transfer** (Same Trust)
    
    **NEW clock starts:**
    - Patient moves from Orthopaedics to Rheumatology
    - Original clock STOPS
    - NEW RTT clock starts on transfer date
    - New specialty has fresh 18 weeks
    
    **Example:**
    - Patient referred to Ortho for knee pain
    - At 6 weeks, consultant refers to Rheumatology (suspected arthritis)
    - Ortho clock stops at 6 weeks
    - New Rheumatology clock starts from zero
    
    #### 3️⃣ **Private to NHS Transfer**
    
    **NEW clock starts:**
    - Patient started treatment privately
    - Now transferring to NHS
    - Fresh RTT clock starts on NHS referral date
    - Private waiting time does NOT count
    
    #### 4️⃣ **Emergency to Elective Transfer**
    
    **Clock starts when ready for elective:**
    - Emergency admission
    - Later requires elective procedure
    - RTT clock starts when decision for elective made
    
    ### 📋 Transfer Documentation Requirements
    
    **MUST document:**
    - ✅ Reason for transfer
    - ✅ Transferring provider details
    - ✅ Receiving provider details
    - ✅ Current RTT status
    - ✅ Weeks elapsed on clock
    - ✅ Clinical information transferred
    - ✅ Patient informed of transfer
    - ✅ Consent obtained
    
    ### ⚖️ Responsibility Rules
    
    **Transferring Provider:**
    - Ensure complete clinical information sent
    - Confirm receiving provider accepts
    - Document transfer in PAS
    - Inform patient
    - Remove from own waiting list
    
    **Receiving Provider:**
    - Accept transfer formally
    - Inherit RTT clock (inter-provider)
    - OR start new clock (inter-specialty)
    - Add to waiting list
    - See within appropriate timeframe
    
    ### 🚩 Common Transfer Errors
    
    ❌ **Wrong clock action:**
    - Continued old clock when should start new
    - Started new clock when should transfer
    
    ❌ **Poor communication:**
    - Receiving provider not informed
    - Patient lost in transfer
    - Clinical info not sent
    
    ❌ **Missing documentation:**
    - Transfer not recorded in PAS
    - Consent not obtained
    - RTT status unclear
    """)

st.markdown("---")

# Transfer Recording
st.markdown("## 📝 Record Transfer of Care")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("transfer_form"):
        st.markdown("### Patient Details")
        
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *", max_chars=10)
        
        col_a, col_b = st.columns(2)
        with col_a:
            referral_date = st.date_input("Original Referral Date *")
            weeks_elapsed = ((datetime.now().date() - referral_date).days) // 7
            st.info(f"⏰ Time Elapsed: **{weeks_elapsed} weeks**")
        
        with col_b:
            transfer_date = st.date_input("Transfer Date *",
                value=datetime.now().date())
        
        st.markdown("### Transfer Details")
        
        transfer_type = st.selectbox("Type of Transfer *", [
            "🏥 Inter-Provider (Between NHS Trusts)",
            "🔄 Inter-Specialty (Same Trust)",
            "💰 Private to NHS",
            "🚑 Emergency to Elective",
            "🌍 Out of Area Transfer",
            "Other"
        ])
        
        col_from, col_to = st.columns(2)
        
        with col_from:
            st.markdown("#### FROM:")
            from_provider = st.text_input("Provider/Trust *",
                value="Current Trust")
            from_specialty = st.selectbox("Specialty *", [
                "Orthopaedics", "Cardiology", "ENT", "General Surgery",
                "Ophthalmology", "Dermatology", "Urology", "Gastroenterology",
                "Gynaecology", "Rheumatology", "Neurology", "Other"
            ])
        
        with col_to:
            st.markdown("#### TO:")
            to_provider = st.text_input("Provider/Trust *",
                value="New Trust")
            to_specialty = st.selectbox("New Specialty *", [
                "Orthopaedics", "Cardiology", "ENT", "General Surgery",
                "Ophthalmology", "Dermatology", "Urology", "Gastroenterology",
                "Gynaecology", "Rheumatology", "Neurology", "Other"
            ], key="to_spec")
        
        st.markdown("### Clinical Information")
        
        reason_transfer = st.text_area("Reason for Transfer *",
            placeholder="e.g., Specialist expertise required, Patient choice, Out of catchment area")
        
        clinical_summary = st.text_area("Clinical Summary *",
            placeholder="Brief clinical history and current status")
        
        urgent_transfer = st.radio("Is this an urgent transfer? *", [
            "No - Routine transfer",
            "Yes - Clinically urgent"
        ])
        
        st.markdown("### RTT Clock Management")
        
        current_rtt_status = st.radio("Current RTT Status *", [
            "Active RTT pathway",
            "Paused RTT pathway",
            "Non-RTT pathway"
        ])
        
        # Determine clock action based on transfer type
        if "Inter-Provider" in transfer_type:
            st.warning("""
            ⏰ **RTT CLOCK ACTION:** Clock TRANSFERS to receiving provider
            - Current wait time: {weeks_elapsed} weeks
            - Receiving provider inherits clock
            - Must see within {18 - weeks_elapsed} weeks
            """.format(weeks_elapsed=weeks_elapsed))
            clock_action = "Transfer existing clock"
            
        elif "Inter-Specialty" in transfer_type:
            st.info("""
            🔄 **RTT CLOCK ACTION:** NEW clock starts
            - Current clock STOPS
            - New clock starts from zero
            - New specialty has fresh 18 weeks
            """)
            clock_action = "Start new clock"
        
        elif "Private" in transfer_type:
            st.info("""
            💰 **RTT CLOCK ACTION:** NEW clock starts
            - Private time does NOT count
            - Fresh RTT clock from NHS acceptance
            - 18 weeks from transfer date
            """)
            clock_action = "Start new clock (private transfer)"
        
        else:
            clock_action = st.selectbox("Clock Action Required *", [
                "Transfer existing clock",
                "Start new clock",
                "No RTT implications"
            ])
        
        st.markdown("### Communication & Consent")
        
        patient_informed = st.checkbox("Patient informed and consents to transfer? *")
        
        receiving_accepted = st.checkbox("Receiving provider has accepted transfer? *")
        
        clinical_info_sent = st.checkbox("Complete clinical information sent? *")
        
        notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("📤 Process Transfer", type="primary", use_container_width=True)
        
        if submitted:
            if (patient_name and nhs_number and reason_transfer and 
                patient_informed and receiving_accepted and clinical_info_sent):
                
                st.success("✅ Transfer processed successfully!")
                st.balloons()
                
                # Transfer Summary
                st.markdown("### 📋 Transfer Summary")
                st.markdown(f"""
                **Patient:** {patient_name} (NHS: {nhs_number})
                
                **Transfer Details:**
                - Type: {transfer_type}
                - From: {from_provider} - {from_specialty}
                - To: {to_provider} - {to_specialty}
                - Date: {transfer_date.strftime('%d/%m/%Y')}
                - Reason: {reason_transfer}
                
                **RTT Status:**
                - Time Elapsed: {weeks_elapsed} weeks
                - Clock Action: {clock_action}
                - Urgent: {urgent_transfer}
                """)
                
                # RTT Impact Analysis
                st.markdown("### 🎯 RTT Clock Impact")
                
                if clock_action == "Transfer existing clock":
                    remaining = 18 - weeks_elapsed
                    st.warning(f"""
                    ⏰ **CLOCK TRANSFERRED**
                    
                    **Receiving Provider ({to_provider}):**
                    - Inherits RTT clock at {weeks_elapsed} weeks
                    - Must see patient within **{remaining} weeks**
                    - 18-week deadline: {(transfer_date + timedelta(weeks=remaining)).strftime('%d/%m/%Y')}
                    - Responsibility now with receiving provider
                    
                    **Original Provider ({from_provider}):**
                    - No longer responsible for 18-week target
                    - Must send complete information
                    - Update PAS system
                    """)
                
                elif "new clock" in clock_action.lower():
                    st.info("""
                    🆕 **NEW CLOCK STARTS**
                    
                    **Receiving Provider ({to_provider}):**
                    - Fresh 18-week RTT clock starts
                    - Clock start date: {transfer_date.strftime('%d/%m/%Y')}
                    - 18-week deadline: {(transfer_date + timedelta(weeks=18)).strftime('%d/%m/%Y')}
                    - Previous wait time does NOT count
                    
                    **Original Provider ({from_provider}):**
                    - Original clock STOPS
                    - Discharge patient from specialty
                    - Update PAS system
                    """.format(to_provider=to_provider, transfer_date=transfer_date,
                              from_provider=from_provider))
                
                # Action checklist
                st.markdown("### ✅ Action Checklist")
                st.success("""
                **Completed:**
                - ✅ Patient informed and consents
                - ✅ Receiving provider accepted
                - ✅ Clinical information sent
                - ✅ RTT clock action determined
                
                **Next Steps:**
                - 📝 Update PAS system
                - 📧 Send formal transfer letter
                - 📋 Update waiting list
                - 🔔 Set follow-up reminder
                - 📊 Inform commissioners (if out of area)
                """)
                
            else:
                st.error("""
                ❌ Cannot process transfer!
                
                **Must complete:**
                - All required fields (*)
                - Patient consent obtained
                - Receiving provider accepted
                - Clinical information sent
                """)

with col2:
    st.markdown("### 📊 Transfer Stats")
    
    st.metric("Transfers This Month", "67", "+12")
    st.metric("Inter-Provider", "34", "+5")
    st.metric("Inter-Specialty", "28", "+6")
    st.metric("Pending Acceptance", "5", "-2")
    
    st.markdown("### 🎓 Quick Reference")
    st.info("""
    **Clock Actions:**
    - 🏥 Inter-Provider = TRANSFER clock
    - 🔄 Inter-Specialty = NEW clock
    - 💰 Private→NHS = NEW clock
    - 🚑 Emergency→Elective = NEW clock
    """)
    
    st.markdown("### ✅ Transfer Checklist")
    st.success("""
    **Always:**
    - Get patient consent
    - Send clinical info
    - Confirm acceptance
    - Document in PAS
    - Update waiting list
    - Inform patient
    """)

# Practice Scenarios
st.markdown("---")
st.markdown("## 🎓 Practice Scenarios")

scenario = st.selectbox("Select a scenario:", [
    "Select a scenario...",
    "Scenario 1: Transfer between two hospitals",
    "Scenario 2: Ortho to Rheumatology transfer",
    "Scenario 3: Private to NHS transfer"
])

if scenario == "Scenario 2: Ortho to Rheumatology transfer":
    st.markdown("""
    ### Scenario 2: Inter-Specialty Transfer
    
    **Patient:** Lisa Johnson, NHS: 8888888888
    - **Original Referral:** Orthopaedics for knee pain (12 weeks ago)
    - **Now:** Ortho consultant suspects inflammatory arthritis
    - **Action:** Referring to Rheumatology
    - **Question:** What happens to the RTT clock?
    """)
    
    answer = st.radio("Select correct RTT clock action:", [
        "Keep existing clock - patient at 12 weeks",
        "Start NEW clock - Rheumatology gets fresh 18 weeks",
        "Clock stops - no longer RTT",
        "Clock pauses until Rheumatology appointment"
    ])
    
    if st.button("Check Answer"):
        if answer == "Start NEW clock - Rheumatology gets fresh 18 weeks":
            st.success("""
            ✅ **CORRECT!**
            
            **Explanation:**
            - Inter-specialty transfer = NEW clock
            - Orthopaedics clock STOPS at 12 weeks
            - Rheumatology gets fresh 18-week clock
            - Clock starts from transfer/referral date
            - Patient is NOT at 12 weeks for Rheumatology
            - This is a NEW RTT pathway
            
            **Why:** Different specialty = different condition = new pathway!
            """)
        else:
            st.error("""
            ❌ **INCORRECT**
            
            **Correct Answer:** Start NEW clock - Rheumatology gets fresh 18 weeks
            
            **Why:** Inter-specialty transfers start fresh clocks!
            """)

st.markdown("---")
st.info("""
**💡 Remember:** Inter-PROVIDER = Transfer clock | Inter-SPECIALTY = New clock
""")
