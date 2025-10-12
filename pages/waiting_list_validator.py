"""
T21 HEALTHCARE PLATFORM - WAITING LIST VALIDATOR
Educational module for validating waiting lists and priority categorization
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


st.set_page_config(page_title="Waiting List Validator | T21 Services", page_icon="📋", layout="wide")

# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="waiting_list")

st.title("📋 Waiting List Validator")
st.markdown("**Verify patients are on correct waiting lists with appropriate priority**")


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Waiting List Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Waiting Lists")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_waiting_list")
    with col2:
        records = read_all_records('waiting_list')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "waiting_list.csv", "text/csv")
    
    # Get records
    records = read_all_records('waiting_list')
    
    if search_term:
        records = search_records('waiting_list', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Waiting List #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('waiting_list', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Waiting List")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('waiting_list')
    
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
with st.expander("📚 LEARNING OBJECTIVES - Waiting List Rules", expanded=True):
    st.markdown("""
    ### What are Waiting Lists?
    
    **Waiting Lists** = Organized lists of patients awaiting treatment, categorized by specialty, urgency, and RTT status.
    
    ### 🚨 Types of NHS Waiting Lists:
    
    #### 1️⃣ **RTT (Referral to Treatment) Waiting Lists**
    
    **Routine RTT:**
    - 18-week target applies
    - Elective procedures
    - Non-urgent referrals
    - Most common type
    
    **Urgent RTT:**
    - Shorter timeframe required
    - Clinically urgent (not emergency)
    - May be <18 weeks target
    - Example: Suspected cancer pathway
    
    **Cancer 2-Week Wait:**
    - MUST be seen within 14 days
    - Suspected cancer referrals
    - Highest priority for appointments
    - Separate tracking required
    
    #### 2️⃣ **Non-RTT Waiting Lists**
    
    **Follow-up Appointments:**
    - NOT part of RTT pathway
    - Ongoing care/monitoring
    - No 18-week target
    - Example: Diabetic eye screening
    
    **Diagnostic Tests:**
    - May or may not be RTT
    - Depends if part of treatment pathway
    - 6-week diagnostic target
    
    ### 📊 Priority Categories
    
    **Priority 1 - URGENT (0-4 weeks)**
    - Cancer 2-week wait
    - Clinical urgent
    - High risk of deterioration
    
    **Priority 2 - SOON (4-8 weeks)**
    - Clinically recommended
    - Moderately urgent
    - Significant symptoms
    
    **Priority 3 - ROUTINE (8-18 weeks)**
    - Standard referrals
    - 18-week target
    - Elective procedures
    
    **Priority 4 - PLANNED (>18 weeks)**
    - Staged procedures
    - Patient choice delay
    - Clinical reasons for delay
    
    ### ✅ Validation Checks
    
    **Patient on CORRECT list?**
    - Specialty matches referral?
    - RTT vs Non-RTT correct?
    - Priority appropriate?
    
    **Priority JUSTIFIED?**
    - Clinical evidence for urgency?
    - Cancer pathway documented?
    - Consultant review required?
    
    **Clock STATUS correct?**
    - Active/Paused status correct?
    - Reason for pause documented?
    - Resume date set?
    
    ### 🚩 Common Errors
    
    ❌ **Wrong Specialty:**
    - Referred to ENT, on Ortho list
    - Must be moved immediately
    
    ❌ **Wrong Priority:**
    - Cancer patient on routine list
    - Urgent case marked as routine
    
    ❌ **Wrong RTT Status:**
    - Follow-up on RTT list
    - Non-RTT marked as RTT
    
    ❌ **Clock Error:**
    - Active clock marked as paused
    - Pause not documented
    """)

st.markdown("---")

# Waiting List Validation
st.markdown("## 🔍 Validate Patient on Waiting List")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("validation_form"):
        st.markdown("### Patient Details")
        
        patient_name = st.text_input("Patient Name *")
        nhs_number = st.text_input("NHS Number *", max_chars=10)
        
        col_a, col_b = st.columns(2)
        with col_a:
            referral_date = st.date_input("Referral Date *")
            weeks_waiting = ((datetime.now().date() - referral_date).days) // 7
            st.info(f"⏰ Current Wait: **{weeks_waiting} weeks**")
        
        with col_b:
            specialty = st.selectbox("Specialty *", [
                "Orthopaedics", "Cardiology", "ENT", "General Surgery",
                "Ophthalmology", "Dermatology", "Urology", "Gastroenterology",
                "Gynaecology", "Neurology", "Respiratory", "Rheumatology"
            ])
        
        st.markdown("### Current Waiting List Status")
        
        current_list = st.selectbox("Which list is patient on? *", [
            "RTT - Routine Waiting List",
            "RTT - Urgent Waiting List",
            "Cancer 2-Week Wait List",
            "Follow-up Appointment List",
            "Diagnostic Test List",
            "Suspended/Paused List",
            "Unknown/Not on any list"
        ])
        
        current_priority = st.selectbox("Current Priority *", [
            "Priority 1 - URGENT (0-4 weeks)",
            "Priority 2 - SOON (4-8 weeks)",
            "Priority 3 - ROUTINE (8-18 weeks)",
            "Priority 4 - PLANNED (>18 weeks)",
            "No priority assigned"
        ])
        
        clock_status = st.selectbox("RTT Clock Status *", [
            "Active - Clock running",
            "Paused - Patient choice",
            "Paused - Clinical reason",
            "Paused - Admin reason",
            "Stopped - Treatment complete",
            "Unknown"
        ])
        
        st.markdown("### Clinical Information")
        
        referral_reason = st.text_area("Reason for Referral *",
            placeholder="e.g., Chronic knee pain, Suspected cancer, Routine cataract")
        
        clinical_urgency = st.radio("Clinical Urgency Assessment *", [
            "🔴 Cancer suspected (2-week wait)",
            "🟠 Clinically urgent",
            "🟡 Moderately urgent",
            "🟢 Routine/Elective"
        ])
        
        is_first_appointment = st.radio("Is this for first appointment? *", [
            "Yes - First outpatient",
            "No - Follow-up appointment",
            "No - Treatment appointment"
        ])
        
        submitted = st.form_submit_button("🔍 Validate Waiting List", type="primary", use_container_width=True)
        
        if submitted:
            if patient_name and nhs_number and referral_reason:
                st.success("✅ Validation Complete!")
                
                # Validation Logic
                validation_issues = []
                recommendations = []
                
                # Check 1: Cancer pathway
                if "Cancer" in clinical_urgency:
                    if "Cancer 2-Week Wait" not in current_list:
                        validation_issues.append("❌ **CRITICAL:** Cancer suspected but NOT on 2-week wait list!")
                        recommendations.append("🚨 **URGENT:** Move to Cancer 2-week wait list immediately")
                    if "Priority 1" not in current_priority:
                        validation_issues.append("❌ Cancer patient must be Priority 1")
                        recommendations.append("Change priority to Priority 1 - URGENT")
                
                # Check 2: Priority vs waiting time
                if weeks_waiting > 16:
                    if "Priority 1" not in current_priority and "Priority 2" not in current_priority:
                        validation_issues.append("⚠️ Patient at 16+ weeks should be Priority 1 or 2")
                        recommendations.append("Escalate priority to prevent breach")
                
                # Check 3: Follow-up vs first appointment
                if "No - Follow" in is_first_appointment:
                    if "RTT" in current_list and "Follow-up" not in current_list:
                        validation_issues.append("⚠️ Follow-up appointment on RTT list")
                        recommendations.append("Move to Follow-up Appointment List (Non-RTT)")
                
                # Check 4: Clock status
                if weeks_waiting > 18 and "Active" in clock_status:
                    validation_issues.append("🚨 **BREACH:** Patient over 18 weeks with active clock!")
                    recommendations.append("Urgent clinical review and escalation required")
                
                # Check 5: Urgency vs list
                if "urgent" in clinical_urgency.lower():
                    if "Routine" in current_list:
                        validation_issues.append("❌ Urgent patient on routine waiting list")
                        recommendations.append("Move to Urgent Waiting List")
                
                # Display results
                st.markdown("### 🎯 Validation Results")
                
                if not validation_issues:
                    st.success("""
                    ✅ **ALL CHECKS PASSED**
                    
                    Patient is on the correct waiting list with appropriate priority.
                    - List assignment: Correct
                    - Priority level: Appropriate
                    - RTT status: Valid
                    - No action required
                    """)
                else:
                    st.error(f"""
                    ⚠️ **{len(validation_issues)} ISSUES FOUND**
                    
                    Immediate action required:
                    """)
                    
                    for issue in validation_issues:
                        st.markdown(issue)
                    
                    st.markdown("### 📋 Recommended Actions")
                    for rec in recommendations:
                        st.markdown(f"- {rec}")
                
                # Summary
                st.markdown("### 📊 Validation Summary")
                st.markdown(f"""
                **Patient:** {patient_name} (NHS: {nhs_number})
                **Current Status:**
                - Waiting List: {current_list}
                - Priority: {current_priority}
                - Wait Time: {weeks_waiting} weeks
                - Clock Status: {clock_status}
                - Urgency: {clinical_urgency}
                
                **Issues Found:** {len(validation_issues)}
                **Status:** {'✅ VALID' if not validation_issues else '❌ REQUIRES ACTION'}
                """)
                
            else:
                st.error("❌ Please complete all required fields marked with *")

with col2:
    st.markdown("### 📊 Validation Stats")
    
    st.metric("Patients Validated", "1,234", "+56")
    st.metric("Issues Found", "89", "-12")
    st.metric("Critical Issues", "7", "-3")
    
    st.markdown("### 🎓 Quick Checks")
    st.info("""
    **Validate:**
    - ✅ Right specialty?
    - ✅ Right priority?
    - ✅ RTT vs Non-RTT?
    - ✅ Clock status correct?
    """)
    
    st.markdown("### 🚨 Red Flags")
    st.warning("""
    **Immediate Action:**
    - Cancer not on 2WW
    - >16 weeks low priority
    - Follow-up on RTT list
    - >18 weeks active clock
    """)
    
    st.markdown("### 📚 Priority Guide")
    st.success("""
    **P1:** Cancer, Urgent (0-4w)
    **P2:** Soon (4-8w)
    **P3:** Routine (8-18w)
    **P4:** Planned (>18w)
    """)

# Practice scenarios
st.markdown("---")
st.markdown("## 🎓 Practice Scenarios")

scenario = st.selectbox("Select a scenario:", [
    "Select a scenario...",
    "Scenario 1: Cancer patient on routine list",
    "Scenario 2: Follow-up on RTT list",
    "Scenario 3: 17-week patient on low priority"
])

if scenario == "Scenario 1: Cancer patient on routine list":
    st.markdown("""
    ### Scenario 1: Cancer Patient Misplaced
    
    **Patient:** John Williams, NHS: 7777777777
    - **Referral:** Suspected bowel cancer
    - **Current List:** RTT - Routine Waiting List
    - **Priority:** Priority 3 - ROUTINE
    - **Wait Time:** 6 weeks
    
    **What is wrong and what action is needed?**
    """)
    
    answer = st.radio("Select correct action:", [
        "No issues - patient within 18 weeks",
        "Move to Cancer 2-Week Wait list immediately - Priority 1",
        "Keep on routine list but increase priority",
        "Wait until 14 weeks then escalate"
    ])
    
    if st.button("Check Answer"):
        if answer == "Move to Cancer 2-Week Wait list immediately - Priority 1":
            st.success("""
            ✅ **CORRECT!**
            
            **Explanation:**
            - 🚨 CRITICAL ERROR: Cancer patient on wrong list!
            - Cancer 2-week wait target = MUST be seen within 14 days
            - Patient already at 6 weeks = BREACH of 2WW
            - MUST move to Cancer 2-Week Wait list
            - MUST be Priority 1 - URGENT
            - Escalate to consultant immediately
            - Incident report required
            
            **This is a SERIOUS patient safety issue!**
            """)
        else:
            st.error("""
            ❌ **INCORRECT**
            
            **Correct Answer:** Move to Cancer 2-Week Wait list immediately
            
            **Why:** Cancer suspected = 2-week wait, not 18 weeks! This is critical!
            """)

st.markdown("---")
st.info("""
**💡 Remember:** Right list + Right priority = Patient safety + RTT compliance!
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
