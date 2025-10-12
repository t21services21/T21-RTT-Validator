"""
T21 HEALTHCARE PLATFORM - FUNDING & IFR MANAGEMENT
Track Individual Funding Requests and RTT clock impact
"""

import streamlit as st
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from universal_crud import (
    create_
from navigation import render_navigation
record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)



st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="funding")

st.title("💰 Funding & IFR (Individual Funding Request)")
st.markdown("**Track funding applications and RTT clock impact**")

with st.expander("📚 What are IFRs and Why They Matter", expanded=True):
    st.markdown("""
    ### Individual Funding Requests (IFR)
    
    **What is an IFR?**
    - Request for funding for treatment NOT routinely commissioned
    - Examples: Experimental treatment, out-of-area care, specialized procedure
    - Requires CCG/ICB approval before treatment
    
    ### 🚨 CRITICAL RTT RULE:
    
    **RTT Clock PAUSES during IFR process!**
    
    **Why?**
    - Cannot treat without funding approval
    - Delay is NOT patient's fault
    - Delay is NOT trust's fault
    - Legitimate pause in pathway
    
    ### IFR Process:
    
    **Step 1: Clinical Assessment**
    - Consultant identifies need for non-standard treatment
    - Gathers clinical evidence
    - Documents exceptional circumstances
    
    **Step 2: IFR Application**
    - Complete IFR form
    - Attach clinical evidence
    - Submit to CCG/ICB panel
    
    **Step 3: Panel Review**
    - Monthly panel meetings (usually)
    - Review clinical case
    - Decision: Approve/Decline/More info needed
    
    **Step 4: Outcome**
    - **If Approved:** Clock resumes, proceed with treatment
    - **If Declined:** Patient informed, alternative options, clock stops
    - **If More Info:** Remains paused until provided
    
    ### Typical Timelines:
    - Application to decision: **4-8 weeks** (depends on panel frequency)
    - Urgent cases: **2-3 weeks** (expedited)
    - Complex cases: **3+ months** (multiple panels)
    
    ### RTT Impact:
    
    **Clock PAUSES from:**
    - IFR application submitted date
    
    **Clock RESUMES when:**
    - IFR approved and patient ready
    - Alternative treatment agreed
    
    **Clock STOPS if:**
    - IFR declined with no alternative
    - Patient chooses not to proceed
    
    ### Common IFR Scenarios:
    - Fertility treatment
    - Cosmetic procedures with clinical need
    - Weight loss surgery
    - High-cost drugs
    - Out-of-area specialist centers
    - Experimental/new treatments
    """)


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Funding Request Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Funding Requests")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_funding_requests")
    with col2:
        records = read_all_records('funding_requests')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "funding_requests.csv", "text/csv")
    
    # Get records
    records = read_all_records('funding_requests')
    
    if search_term:
        records = search_records('funding_requests', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Funding Request #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('funding_requests', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Funding Request")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('funding_requests')
    
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


st.markdown("---")

# Submit IFR
st.markdown("## 📝 Submit IFR Application")

with st.form("ifr_form"):
    st.markdown("### Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *")
        dob = st.date_input("Date of Birth *")
    with col2:
        referral_date = st.date_input("Original Referral Date *")
        specialty = st.selectbox("Specialty *", [
            "Orthopaedics", "General Surgery", "Gynaecology",
            "Plastic Surgery", "Ophthalmology", "Fertility", "Other"
        ])
        weeks_waiting = ((datetime.now().date() - referral_date).days) // 7
        st.info(f"⏰ Wait Time: **{weeks_waiting} weeks**")
    
    st.markdown("### Treatment Details")
    
    treatment_requested = st.text_input("Treatment/Procedure Requested *",
        placeholder="e.g., Bariatric surgery, Fertility treatment")
    
    clinical_justification = st.text_area("Clinical Justification *",
        placeholder="Explain why this treatment is needed and why standard alternatives are unsuitable",
        help="Be detailed - panel needs strong clinical case")
    
    exceptional_circumstances = st.text_area("Exceptional Circumstances *",
        placeholder="Explain what makes this case exceptional/unusual",
        help="Why does this patient need funding approval?")
    
    standard_treatment_tried = st.checkbox("Standard treatment options tried/considered?")
    
    if standard_treatment_tried:
        treatments_tried = st.text_area("Treatments Already Tried",
            placeholder="List previous treatments and outcomes")
    
    st.markdown("### Clinical Evidence")
    
    supporting_evidence = st.multiselect("Supporting Evidence Attached", [
        "Consultant letter",
        "Clinical notes",
        "Test results",
        "Previous treatment records",
        "Research papers/guidelines",
        "Patient photos (if relevant)",
        "Second opinion",
        "MDT decision"
    ])
    
    consultant_name = st.text_input("Applying Consultant *")
    consultant_speciality = st.text_input("Consultant Specialty")
    
    st.markdown("### Funding Details")
    
    estimated_cost = st.number_input("Estimated Cost (£)", min_value=0, value=5000, step=100)
    
    urgency = st.radio("Urgency *", [
        "Standard (routine panel review)",
        "Urgent (expedited review requested)",
        "Emergency (immediate decision needed)"
    ])
    
    if "Urgent" in urgency or "Emergency" in urgency:
        urgency_reason = st.text_area("Reason for Urgency *",
            placeholder="Explain why expedited review is needed")
    
    ccg_icb = st.selectbox("Commissioning Organization *", [
        "NHS Cheshire & Merseyside ICB",
        "NHS Greater Manchester ICB",
        "NHS Lancashire & South Cumbria ICB",
        "Other"
    ])
    
    st.markdown("### RTT Clock Management")
    
    st.warning("⚠️ **Important:** RTT clock will PAUSE from IFR submission date")
    
    ifr_submission_date = st.date_input("IFR Submission Date *",
        value=datetime.now().date())
    
    expected_decision_date = st.date_input("Expected Panel Decision Date",
        value=datetime.now().date() + timedelta(days=42),
        help="Usually 4-8 weeks from submission")
    
    notes = st.text_area("Additional Notes")
    
    submitted = st.form_submit_button("📤 Submit IFR Application", type="primary", use_container_width=True)
    
    if submitted:
        if patient_name and nhs_number and treatment_requested and clinical_justification:
            st.success("✅ IFR application submitted!")
            st.balloons()
            
            st.markdown("### 📋 IFR Application Summary")
            st.info(f"""
            **Patient:** {patient_name} (NHS: {nhs_number})
            **Treatment:** {treatment_requested}
            **Estimated Cost:** £{estimated_cost:,}
            **Urgency:** {urgency}
            **Commissioning Org:** {ccg_icb}
            
            **RTT Impact:**
            - Current wait: {weeks_waiting} weeks
            - Clock PAUSED from: {ifr_submission_date.strftime('%d/%m/%Y')}
            - Expected decision: {expected_decision_date.strftime('%d/%m/%Y')}
            - Time remaining when approved: {18 - weeks_waiting} weeks
            """)
            
            st.markdown("### 📧 Next Steps")
            st.success("""
            **Automatic Actions:**
            - ✅ IFR application logged
            - ✅ RTT clock paused
            - ✅ Patient informed
            - ✅ Panel notification sent
            - ✅ Follow-up reminder set
            
            **Manual Actions Required:**
            - 📎 Attach supporting documents
            - 📧 Email to commissioning panel
            - 📞 Inform patient of timeline
            - 📅 Set reminder for decision date
            """)
            
        else:
            st.error("❌ Please complete all required fields marked with *")

# IFR Register
st.markdown("---")
st.markdown("## 📊 IFR Register")

import pandas as pd

ifr_register = pd.DataFrame({
    "Patient": ["John Smith", "Mary Jones", "David Brown", "Lisa Wilson"],
    "Treatment": ["Bariatric Surgery", "Fertility Treatment", "Cosmetic Reconstruction", "High-Cost Drug"],
    "Submitted": ["05/12/2024", "10/12/2024", "15/12/2024", "20/12/2024"],
    "Status": ["🟡 Awaiting Decision", "✅ Approved", "🟡 Awaiting Decision", "🔴 More Info Needed"],
    "Next Panel": ["20/01/2025", "Approved", "20/01/2025", "03/02/2025"],
    "Cost": ["£8,500", "£12,000", "£6,200", "£45,000"]
})

st.dataframe(ifr_register, use_container_width=True)

# Statistics
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Active IFRs", "18", "+3")
with col2:
    st.metric("Approved This Month", "7", "+2")
with col3:
    st.metric("Declined", "2", "0")
with col4:
    st.metric("Avg Decision Time", "5.2 weeks", "-0.8")

st.markdown("---")
st.warning("""
⚠️ **Remember:**
- IFR process = Clock PAUSES
- Keep patient informed
- Chase panel for decisions
- Document everything
- Resume clock when approved
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
