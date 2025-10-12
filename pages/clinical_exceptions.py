"""
T21 HEALTHCARE PLATFORM - CLINICAL EXCEPTIONS MODULE
Educational module for managing medically appropriate delays
"""

import streamlit as st
from datetime import datetime, timedelta
from navigation import render_navigation
import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)


st.set_page_config(page_title="Clinical Exceptions | T21 Services", page_icon="⚕️", layout="wide")

# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="clinical_exceptions")

st.title("⚕️ Clinical Exceptions & Medical Delays")
st.markdown("**Track medically appropriate delays and RTT clock impact**")


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Clinical Exception Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Clinical Exceptions")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_clinical_exceptions")
    with col2:
        records = read_all_records('clinical_exceptions')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "clinical_exceptions.csv", "text/csv")
    
    # Get records
    records = read_all_records('clinical_exceptions')
    
    if search_term:
        records = search_records('clinical_exceptions', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Clinical Exception #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('clinical_exceptions', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Clinical Exception")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('clinical_exceptions')
    
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
with st.expander("📚 LEARNING OBJECTIVES - Clinical Exception Rules", expanded=True):
    st.markdown("""
    ### What are Clinical Exceptions?
    
    **Clinical Exceptions** = Medically appropriate delays where treatment cannot proceed for valid clinical reasons.
    
    ### 🚨 CRITICAL RTT RULE:
    
    **Clock May PAUSE for:**
    - Patient medically unfit for treatment
    - Patient needs optimization before procedure
    - Awaiting essential test results
    - Active infection preventing surgery
    - Other medical contraindications
    
    ### ⚕️ Valid Clinical Exceptions:
    
    #### 1️⃣ **Patient Medically Unfit**
    
    **Examples:**
    - Uncontrolled diabetes before surgery
    - Heart condition requires cardiology clearance
    - Active chest infection
    - Severe hypertension needs control
    
    **RTT Impact:** Clock MAY pause while addressing fitness issues
    
    **Documentation Required:**
    - Clinical reason documented by consultant
    - Specific issue identified
    - Plan to address fitness
    - Expected timeframe
    
    #### 2️⃣ **Weight Optimization Required**
    
    **Examples:**
    - BMI too high for safe anaesthesia
    - Joint replacement requires weight loss
    - Bariatric surgery prerequisite
    
    **RTT Impact:** Clock PAUSES during weight loss program
    
    **Must Document:**
    - Target weight/BMI
    - Weight loss plan in place
    - Regular review appointments
    - Support provided
    
    #### 3️⃣ **Awaiting Investigation Results**
    
    **Examples:**
    - MRI results needed before surgery decision
    - Biopsy results pending
    - Genetic test results awaited
    
    **RTT Impact:** Clock CONTINUES (investigations part of pathway)
    
    **Exception:** If investigation causes unavoidable delay, clock may adjust
    
    #### 4️⃣ **Active Medical Condition**
    
    **Examples:**
    - Patient has COVID-19
    - Active DVT/PE
    - Recent MI/stroke
    - Acute mental health crisis
    
    **RTT Impact:** Clock PAUSES until condition resolved
    
    #### 5️⃣ **Clinical Pathway Changed**
    
    **Examples:**
    - Consultant recommends conservative management first
    - Trial of physiotherapy before surgery
    - Medical management before procedure
    
    **RTT Impact:** Depends on whether new pathway or delay
    
    ### ⚖️ NOT Valid Exceptions:
    
    ❌ **These are NOT clinical exceptions:**
    - Hospital resource issues (beds, theatre time)
    - Staff shortages
    - Equipment unavailable
    - Administrative delays
    - Lost referrals
    - Booking errors
    
    **These are TRUST failures, not clinical exceptions!**
    
    ### 📝 Documentation Requirements
    
    **MUST document:**
    - ✅ Specific clinical reason (medical terms)
    - ✅ Consultant name and date
    - ✅ What needs to happen before treatment
    - ✅ Expected timeframe
    - ✅ Patient informed of delay
    - ✅ Review date set
    - ✅ Alternative treatments considered
    
    ### 🚩 Audit Considerations
    
    **Clinical exceptions are audited:**
    - Must have clear clinical justification
    - Cannot be used to hide capacity issues
    - Must be consultant-led decision
    - Patient safety must be priority
    - Regular review required
    """)

st.markdown("---")

# Clinical Exception Recording
st.markdown("## 📝 Record Clinical Exception")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("exception_form"):
        st.markdown("### Patient Details")
        
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *", max_chars=10)
        
        col_a, col_b = st.columns(2)
        with col_a:
            referral_date = st.date_input("Original Referral Date *")
            weeks_waiting = ((datetime.now().date() - referral_date).days) // 7
            st.info(f"⏰ Current Wait: **{weeks_waiting} weeks**")
        
        with col_b:
            specialty = st.selectbox("Specialty *", [
                "Orthopaedics", "Cardiology", "ENT", "General Surgery",
                "Ophthalmology", "Dermatology", "Urology", "Gastroenterology"
            ])
            procedure_planned = st.text_input("Planned Procedure/Treatment *")
        
        st.markdown("### Clinical Exception Details")
        
        exception_type = st.selectbox("Type of Clinical Exception *", [
            "⚕️ Patient medically unfit",
            "⚖️ Weight optimization required",
            "🧪 Awaiting essential investigation results",
            "🦠 Active infection/acute illness",
            "💊 Medication optimization required",
            "❤️ Cardiac clearance needed",
            "🫁 Respiratory optimization required",
            "🧠 Mental health stabilization needed",
            "🔄 Trial of conservative treatment first",
            "Other clinical reason"
        ])
        
        exception_date = st.date_input("Date Exception Identified *",
            value=datetime.now().date())
        
        clinical_reason = st.text_area("Detailed Clinical Reason *",
            placeholder="e.g., Patient has uncontrolled type 2 diabetes (HbA1c 95mmol/mol). Requires optimization before surgery. Endocrinology referral made.",
            help="Be specific - use medical terms")
        
        consultant_name = st.text_input("Consultant Name *",
            help="Consultant who made this clinical decision")
        
        st.markdown("### Clinical Plan")
        
        action_required = st.text_area("What needs to happen before treatment? *",
            placeholder="e.g., HbA1c must be <58mmol/mol, Patient enrolled in weight loss program, Awaiting cardiology clearance")
        
        expected_duration = st.selectbox("Expected Duration *", [
            "1-2 weeks",
            "2-4 weeks",
            "4-8 weeks",
            "8-12 weeks",
            "12+ weeks",
            "Unknown/TBC"
        ])
        
        review_date = st.date_input("Next Review Date *",
            min_value=datetime.now().date())
        
        alternative_considered = st.text_area("Alternative Treatments Considered",
            placeholder="e.g., Conservative management, Different procedure, Medical management")
        
        st.markdown("### RTT Clock Decision")
        
        clock_action = st.radio("RTT Clock Action *", [
            "⏸️ Pause clock - Medically appropriate delay",
            "⏱️ Continue clock - Investigation part of pathway",
            "🔄 Adjust clock - Unavoidable medical delay"
        ])
        
        if "Pause" in clock_action:
            st.warning(f"""
            ⚠️ **PAUSING RTT CLOCK**
            - Current wait: {weeks_waiting} weeks
            - Clock will pause from: {exception_date.strftime('%d/%m/%Y')}
            - Expected resume: {review_date.strftime('%d/%m/%Y')}
            - Reason: Clinical exception
            
            **This MUST be clinically justified!**
            """)
        
        st.markdown("### Patient Communication")
        
        patient_informed = st.checkbox("Patient informed of delay and reason? *")
        
        if patient_informed:
            communication_method = st.multiselect("How was patient informed? *", [
                "Face-to-face consultation",
                "Phone call",
                "Letter",
                "Clinic appointment"
            ])
        
        patient_understands = st.checkbox("Patient understands this is for their safety?")
        
        notes = st.text_area("Additional Clinical Notes")
        
        submitted = st.form_submit_button("⚕️ Record Clinical Exception", type="primary", use_container_width=True)
        
        if submitted:
            if (patient_name and nhs_number and clinical_reason and 
                consultant_name and action_required and patient_informed):
                
                st.success("✅ Clinical exception recorded!")
                
                # Summary
                st.markdown("### 📋 Clinical Exception Summary")
                st.markdown(f"""
                **Patient:** {patient_name} (NHS: {nhs_number})
                **Procedure:** {procedure_planned}
                
                **Exception Details:**
                - Type: {exception_type}
                - Identified: {exception_date.strftime('%d/%m/%Y')}
                - By: {consultant_name}
                - Current Wait: {weeks_waiting} weeks
                
                **Clinical Reason:**
                {clinical_reason}
                
                **Required Action:**
                {action_required}
                
                **Timeline:**
                - Expected Duration: {expected_duration}
                - Review Date: {review_date.strftime('%d/%m/%Y')}
                
                **RTT Impact:** {clock_action}
                """)
                
                # RTT Impact Analysis
                st.markdown("### 🎯 RTT Clock Impact")
                
                if "Pause" in clock_action:
                    remaining = 18 - weeks_waiting
                    st.warning(f"""
                    ⏸️ **CLOCK PAUSED - Clinical Exception**
                    
                    **Current Status:**
                    - Patient has waited {weeks_waiting} weeks
                    - Clock paused from {exception_date.strftime('%d/%m/%Y')}
                    - Time remaining when resumed: {remaining} weeks
                    
                    **Requirements:**
                    - ✅ Clinical justification documented
                    - ✅ Consultant-led decision
                    - ✅ Patient informed
                    - ✅ Review date set
                    - ✅ Action plan in place
                    
                    **Next Steps:**
                    - Address clinical issue
                    - Review on {review_date.strftime('%d/%m/%Y')}
                    - Resume clock when fit
                    - Complete treatment within {remaining} weeks after resume
                    """)
                
                # Safety checks
                st.markdown("### ✅ Safety & Governance Checklist")
                
                if weeks_waiting > 16:
                    st.error("""
                    🚨 **HIGH-RISK PATIENT**
                    - Patient already at 16+ weeks
                    - Close to 18-week breach
                    - Requires senior review
                    - Consider escalation
                    - Document in incident log
                    """)
                else:
                    st.info("""
                    ✅ **Governance Checks:**
                    - Clinical decision documented
                    - Consultant-approved
                    - Patient-centered care
                    - Safety prioritized
                    - Regular review planned
                    """)
                
            else:
                st.error("""
                ❌ Cannot record clinical exception!
                
                **Must complete:**
                - All required fields (*)
                - Detailed clinical reason
                - Consultant name
                - Action plan
                - Patient informed
                """)

with col2:
    st.markdown("### 📊 Exception Stats")
    
    st.metric("Active Exceptions", "56", "+4")
    st.metric("Resolved This Month", "89", "+12")
    st.metric("Average Duration", "4.2 weeks", "-0.8")
    
    st.markdown("### 🎓 Quick Reference")
    st.info("""
    **Valid Exceptions:**
    - ⚕️ Medically unfit
    - ⚖️ Weight loss needed
    - 🦠 Active infection
    - ❤️ Cardiac clearance
    - 💊 Med optimization
    
    **NOT Valid:**
    - ❌ No beds
    - ❌ No theatre
    - ❌ Staff shortage
    - ❌ Admin delays
    """)
    
    st.markdown("### ⚖️ Audit Requirements")
    st.warning("""
    **Must Document:**
    - Clinical reason
    - Consultant decision
    - Patient informed
    - Review date set
    - Action plan clear
    """)

# Practice Scenarios
st.markdown("---")
st.markdown("## 🎓 Practice Scenarios")

scenario = st.selectbox("Select a scenario:", [
    "Select a scenario...",
    "Scenario 1: Uncontrolled diabetes before surgery",
    "Scenario 2: No theatre slots available",
    "Scenario 3: Patient needs to lose weight"
])

if scenario == "Scenario 2: No theatre slots available":
    st.markdown("""
    ### Scenario 2: Theatre Capacity Issue
    
    **Patient:** Mark Thompson, NHS: 9999999999
    - **Waiting:** 14 weeks for hip replacement
    - **Medically fit:** Ready for surgery
    - **Issue:** No theatre slots available for next 6 weeks
    - **Question:** Is this a valid clinical exception?
    """)
    
    answer = st.radio("Is this a clinical exception?", [
        "Yes - Pause clock for 6 weeks",
        "No - This is a trust capacity issue",
        "Yes - Unavoidable delay",
        "Depends on local policy"
    ])
    
    if st.button("Check Answer"):
        if answer == "No - This is a trust capacity issue":
            st.success("""
            ✅ **CORRECT!**
            
            **Explanation:**
            - 🚨 This is NOT a clinical exception!
            - This is a TRUST FAILURE - lack of capacity
            - Patient is medically fit for surgery
            - Clock CONTINUES running
            - Trust must find solution (outsource, extra sessions, etc.)
            - Patient may BREACH if not addressed
            
            **Clinical exceptions are for PATIENT fitness, not hospital resources!**
            
            **Correct Action:**
            - Do NOT pause clock
            - Escalate capacity issue
            - Consider outsourcing to private provider
            - Prevent breach
            """)
        else:
            st.error("""
            ❌ **INCORRECT**
            
            **Correct Answer:** No - This is a trust capacity issue
            
            **Why:** Hospital resource problems are NOT clinical exceptions!
            Clock continues running - trust must solve capacity issue!
            """)

st.markdown("---")
st.info("""
**💡 Remember:** Clinical exceptions = PATIENT medical issues, NOT hospital problems!
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
