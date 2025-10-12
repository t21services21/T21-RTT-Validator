"""
T21 HEALTHCARE PLATFORM - CONSENT MANAGER
Track patient consent for procedures and treatments
"""

import streamlit as st
from datetime import datetime, timedelta
from navigation import render_navigation

st.set_page_config(page_title="Consent Manager | T21 Services", page_icon="✍️", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="consent")

st.title("✍️ Consent Management")
st.markdown("**Track patient consent for procedures - RTT cannot proceed without valid consent**")

with st.expander("📚 Why Consent Matters for RTT", expanded=True):
    st.markdown("""
    ### Legal & Ethical Requirement
    
    **Cannot treat without consent!**
    - Treatment CANNOT proceed without valid consent
    - RTT clock may PAUSE if consent issues
    - Patient has right to refuse
    - Consent must be informed and voluntary
    
    ### Types of Consent:
    
    **Written Consent (Formal):**
    - Surgical procedures
    - Invasive investigations
    - General anaesthetic
    - Significant risk procedures
    
    **Verbal Consent:**
    - Minor procedures
    - Routine investigations
    - Low-risk treatments
    
    **Implied Consent:**
    - Venepuncture
    - Blood pressure check
    - Routine examinations
    
    ### Consent Must Be:
    - ✅ Voluntary (not coerced)
    - ✅ Informed (risks explained)
    - ✅ Capacity confirmed (patient understands)
    - ✅ Documented
    - ✅ Current (not expired)
    
    ### RTT Impact:
    
    **If patient withdraws consent:**
    - RTT clock STOPS
    - Patient discharged from pathway
    - Can re-refer if changes mind
    
    **If consent not yet obtained:**
    - Clock CONTINUES
    - Must obtain before procedure
    - Part of normal pathway
    """)

st.markdown("---")

# Record consent
st.markdown("## 📝 Record Consent")

with st.form("consent_form"):
    st.markdown("### Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *")
    with col2:
        dob = st.date_input("Date of Birth *")
        specialty = st.selectbox("Specialty *", [
            "Orthopaedics", "General Surgery", "ENT", "Ophthalmology",
            "Urology", "Gynaecology", "Cardiology"
        ])
    
    st.markdown("### Procedure/Treatment")
    
    procedure = st.text_input("Procedure Name *",
        placeholder="e.g., Total Hip Replacement, Cataract Surgery")
    
    procedure_details = st.text_area("Procedure Details",
        placeholder="Brief description of what will be done")
    
    st.markdown("### Consent Details")
    
    consent_type = st.radio("Type of Consent *", [
        "Written Consent (Formal consent form signed)",
        "Verbal Consent (Documented in notes)",
        "Implied Consent (Routine procedure)"
    ])
    
    consent_date = st.date_input("Date Consent Obtained *")
    
    obtained_by = st.text_input("Consent Obtained By *",
        placeholder="e.g., Dr. Smith, Consultant")
    
    st.markdown("### Risk Discussion")
    
    risks_explained = st.checkbox("Risks and benefits explained to patient? *")
    
    if risks_explained:
        risks_list = st.text_area("Risks Discussed",
            placeholder="e.g., Infection, bleeding, anaesthetic risks, implant failure")
    
    alternatives_discussed = st.checkbox("Alternative treatments discussed?")
    
    patient_questions = st.text_area("Patient Questions/Concerns",
        placeholder="Any questions the patient asked")
    
    st.markdown("### Capacity & Understanding")
    
    capacity_confirmed = st.radio("Patient has capacity to consent? *", [
        "Yes - Patient understands and can make decision",
        "No - Lacks capacity (best interests decision needed)",
        "Uncertain - Needs assessment"
    ])
    
    patient_understands = st.checkbox("Patient demonstrates understanding of procedure?")
    
    interpreter_used = st.checkbox("Interpreter used?")
    
    st.markdown("### Consent Status")
    
    consent_valid_until = st.date_input("Consent Valid Until",
        value=datetime.now().date() + timedelta(days=180),
        help="Typically 6 months for elective surgery")
    
    consent_withdrawn = st.checkbox("Patient has withdrawn consent?")
    
    if consent_withdrawn:
        st.warning("⚠️ If consent withdrawn, RTT pathway must be closed!")
        withdrawal_reason = st.text_area("Reason for Withdrawal")
    
    notes = st.text_area("Additional Notes")
    
    submitted = st.form_submit_button("✍️ Record Consent", type="primary", use_container_width=True)
    
    if submitted:
        if patient_name and nhs_number and procedure and risks_explained:
            st.success("✅ Consent recorded successfully!")
            st.balloons()
            
            st.info(f"""
            **Consent Summary:**
            - Patient: {patient_name}
            - Procedure: {procedure}
            - Date: {consent_date.strftime('%d/%m/%Y')}
            - Valid until: {consent_valid_until.strftime('%d/%m/%Y')}
            - Obtained by: {obtained_by}
            - Type: {consent_type}
            - Capacity: {capacity_confirmed}
            """)
            
            if consent_withdrawn:
                st.error("""
                🚨 **CONSENT WITHDRAWN**
                - RTT pathway must be CLOSED
                - Inform consultant immediately
                - Remove from waiting list
                - Document in clinical notes
                - Inform patient of right to re-refer if changes mind
                """)
            
        else:
            st.error("❌ Please complete all required fields marked with *")

# Consent register
st.markdown("---")
st.markdown("## 📋 Consent Register")

st.info("**Search consent records** (Demo data)")

import pandas as pd

consent_register = pd.DataFrame({
    "Patient": ["John Smith", "Mary Jones", "David Brown", "Lisa Wilson"],
    "Procedure": ["Hip Replacement", "Cataract Surgery", "Knee Arthroscopy", "Hernia Repair"],
    "Consent Date": ["05/01/2025", "08/01/2025", "10/01/2025", "12/01/2025"],
    "Valid Until": ["05/07/2025", "08/07/2025", "10/07/2025", "12/07/2025"],
    "Status": ["✅ Valid", "✅ Valid", "✅ Valid", "✅ Valid"],
    "Obtained By": ["Dr. Smith", "Dr. Jones", "Dr. Brown", "Dr. Wilson"]
})

st.dataframe(consent_register, use_container_width=True)

# Statistics
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Valid Consents", "156", "+12")
with col2:
    st.metric("Expiring Soon (<30d)", "8", "+2")
with col3:
    st.metric("Withdrawn", "3", "+1")
with col4:
    st.metric("Pending", "12", "+4")

st.markdown("---")
st.warning("""
⚠️ **Legal Requirement:** Valid consent MUST be in place before any procedure!
- Check expiry dates regularly
- Re-consent if circumstances change
- Document everything
""")
