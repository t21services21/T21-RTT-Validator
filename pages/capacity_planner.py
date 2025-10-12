"""
T21 HEALTHCARE PLATFORM - CAPACITY PLANNER
Educational module for theatre/bed availability and resource planning
"""

import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
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



# Remove top white space
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="capacity")

st.title("🏥 Capacity Planning & Resource Management")
st.markdown("**Plan theatre sessions, beds, and consultant availability to prevent RTT breaches**")


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Capacity Plan Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Capacity Plans")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_capacity_plans")
    with col2:
        records = read_all_records('capacity_plans')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "capacity_plans.csv", "text/csv")
    
    # Get records
    records = read_all_records('capacity_plans')
    
    if search_term:
        records = search_records('capacity_plans', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Capacity Plan #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('capacity_plans', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Capacity Plan")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('capacity_plans')
    
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
with st.expander("📚 LEARNING OBJECTIVES - Capacity Planning", expanded=True):
    st.markdown("""
    ### Why Capacity Planning Matters for RTT
    
    **Capacity Planning** = Ensuring sufficient resources (theatres, beds, consultants) to treat patients within 18 weeks.
    
    ### 🚨 CRITICAL RTT IMPACT:
    
    **Insufficient capacity = RTT BREACHES!**
    
    If hospital cannot offer treatment due to lack of:
    - Theatre time
    - Bed availability
    - Consultant availability
    - Equipment availability
    
    **Result:** This is a TRUST FAILURE, NOT patient fault. Clock continues, patient may breach.
    
    ### 📊 Key Capacity Metrics:
    
    #### 1️⃣ **Theatre Utilization**
    - **Target:** 85-90% utilization
    - **Too Low:** Wasted resource
    - **Too High:** No flexibility for urgent cases
    
    #### 2️⃣ **Bed Occupancy**
    - **Safe Level:** 85-92%
    - **Critical Level:** >95% (unsafe, cancellations likely)
    - **Emergency Threshold:** <10% free beds
    
    #### 3️⃣ **Waiting List Size**
    - Track by specialty
    - Monitor breach risk
    - Balance with capacity
    
    #### 4️⃣ **Consultant Availability**
    - Clinic sessions per week
    - Theatre sessions per week
    - Annual leave coverage
    
    ### 📅 Planning Timeframes:
    
    **Short-term (0-4 weeks):**
    - Daily theatre schedules
    - Bed management
    - Urgent case placement
    
    **Medium-term (1-3 months):**
    - Waiting list management
    - Breach prevention
    - Resource optimization
    
    **Long-term (3-12 months):**
    - Strategic planning
    - Service development
    - Demand forecasting
    
    ### ⚖️ Balancing Act:
    
    **Must balance:**
    - Elective (planned) procedures
    - Emergency admissions
    - Day case procedures
    - Outpatient appointments
    - RTT 18-week targets
    
    ### 🚩 Capacity Issues = RTT Breaches:
    
    **If patient breaches due to:**
    - No theatre slots = Trust failure
    - No beds available = Trust failure  
    - Consultant on leave = Trust failure
    - Equipment broken = Trust failure
    
    **Trust MUST find solutions:** Outsource, extra sessions, locums, etc.
    """)

st.markdown("---")

# Capacity Dashboard
st.markdown("## 📊 Capacity Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["🎭 Theatre Capacity", "🛏️ Bed Capacity", "👨‍⚕️ Consultant Availability", "📈 Demand Forecasting"])

with tab1:
    st.markdown("### 🎭 Theatre Capacity Planning")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Theatres", "8", "")
    with col2:
        st.metric("Available This Week", "6", "-1 (maintenance)")
    with col3:
        st.metric("Utilization Rate", "87%", "+3%")
    with col4:
        st.metric("Cancelled Cases", "3", "-2")
    
    st.markdown("---")
    
    # Theatre schedule input
    st.markdown("### 📅 Weekly Theatre Schedule")
    
    specialty_select = st.selectbox("Select Specialty", [
        "General Surgery", "Orthopaedics", "ENT", "Ophthalmology",
        "Urology", "Gynaecology", "Vascular", "Plastics"
    ])
    
    col_a, col_b = st.columns(2)
    with col_a:
        sessions_per_week = st.number_input("Theatre Sessions per Week", min_value=0, max_value=50, value=8)
        hours_per_session = st.number_input("Hours per Session", min_value=1, max_value=12, value=4)
    
    with col_b:
        cases_per_session = st.number_input("Average Cases per Session", min_value=1, max_value=20, value=4)
        waiting_list_size = st.number_input("Current Waiting List Size", min_value=0, value=120)
    
    # Calculate capacity
    weekly_capacity = sessions_per_week * cases_per_session
    weeks_to_clear = waiting_list_size / weekly_capacity if weekly_capacity > 0 else 0
    
    st.info(f"""
    **Capacity Analysis:**
    - Weekly Theatre Capacity: **{weekly_capacity} cases**
    - Total Theatre Hours: **{sessions_per_week * hours_per_session} hours/week**
    - Waiting List: **{waiting_list_size} patients**
    - Time to Clear List: **{weeks_to_clear:.1f} weeks**
    """)
    
    if weeks_to_clear > 18:
        st.error(f"""
        🚨 **BREACH RISK!**
        - Current capacity insufficient to meet 18-week target
        - Need to add {((waiting_list_size / 18) - weekly_capacity):.0f} more cases per week
        - Options: Additional sessions, outsourcing, efficiency improvements
        """)
    elif weeks_to_clear > 14:
        st.warning(f"""
        ⚠️ **TIGHT CAPACITY**
        - Limited flexibility for new referrals or urgent cases
        - Consider additional capacity planning
        """)
    else:
        st.success(f"""
        ✅ **ADEQUATE CAPACITY**
        - Sufficient to meet 18-week target
        - Room for new referrals and urgent cases
        """)
    
    # Theatre efficiency tips
    with st.expander("💡 Improve Theatre Efficiency"):
        st.markdown("""
        **Strategies to Increase Capacity:**
        
        1. **Extended Hours:**
           - Evening sessions
           - Weekend sessions
           - +20-30% capacity
        
        2. **Reduce Turnaround Time:**
           - Faster room cleaning
           - Better scheduling
           - +10-15% capacity
        
        3. **Case Mix Optimization:**
           - Batch similar cases
           - Right patient, right theatre
           - +5-10% capacity
        
        4. **Cancellation Reduction:**
           - Pre-assessment clinics
           - Patient optimization
           - Reduced waste
        
        5. **Outsourcing:**
           - Private sector capacity
           - Neighboring trusts
           - Immediate relief
        """)

with tab2:
    st.markdown("### 🛏️ Bed Capacity Management")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Beds", "450", "")
    with col2:
        st.metric("Occupied", "405", "+12")
    with col3:
        st.metric("Occupancy Rate", "90%", "+3%")
    with col4:
        st.metric("Available", "45", "-12")
    
    st.markdown("---")
    
    # Bed planning
    st.markdown("### 📊 Bed Availability Forecast")
    
    col_x, col_y = st.columns(2)
    with col_x:
        current_occupancy = st.slider("Current Bed Occupancy %", 0, 100, 90)
        total_beds = st.number_input("Total Beds", min_value=1, value=450)
    
    with col_y:
        elective_surgeries_week = st.number_input("Planned Elective Surgeries This Week", min_value=0, value=50)
        avg_length_stay = st.number_input("Average Length of Stay (days)", min_value=1, value=5)
    
    # Calculate bed pressure
    occupied_beds = int(total_beds * (current_occupancy / 100))
    available_beds = total_beds - occupied_beds
    beds_needed = elective_surgeries_week * (avg_length_stay / 7)
    
    st.info(f"""
    **Bed Capacity Analysis:**
    - Currently Occupied: **{occupied_beds} beds** ({current_occupancy}%)
    - Available: **{available_beds} beds**
    - Needed for Electives: **{beds_needed:.0f} beds**
    - Remaining Capacity: **{available_beds - beds_needed:.0f} beds**
    """)
    
    if current_occupancy > 95:
        st.error("""
        🚨 **CRITICAL BED PRESSURE!**
        - Unsafe occupancy level
        - High risk of cancellations
        - Emergency admissions will cause breaches
        - **Action:** Cancel non-urgent electives, discharge planning, escalate
        """)
    elif current_occupancy > 92:
        st.warning("""
        ⚠️ **HIGH BED PRESSURE**
        - Limited capacity for electives
        - Risk of cancellations
        - **Action:** Active discharge planning, monitor closely
        """)
    else:
        st.success("""
        ✅ **SAFE OCCUPANCY LEVEL**
        - Adequate capacity for planned procedures
        - Room for emergency admissions
        """)
    
    # Bed management strategies
    with st.expander("💡 Bed Management Strategies"):
        st.markdown("""
        **Reduce Bed Pressure:**
        
        1. **Discharge Planning:**
           - Early planning from admission
           - Multi-disciplinary approach
           - Reduce length of stay by 10-20%
        
        2. **Day Case Conversion:**
           - Move suitable cases to day surgery
           - Frees up inpatient beds
           - Reduces costs
        
        3. **Enhanced Recovery:**
           - ERAS protocols
           - Faster patient recovery
           - Earlier discharge
        
        4. **Flow Management:**
           - Admission avoidance
           - Virtual wards
           - Community support
        """)

with tab3:
    st.markdown("### 👨‍⚕️ Consultant Availability")
    
    st.markdown("#### Plan Consultant Time")
    
    consultant_name = st.text_input("Consultant Name", value="Mr. Smith")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        clinic_sessions = st.number_input("Clinic Sessions/Week", min_value=0, max_value=20, value=3)
        patients_per_clinic = st.number_input("Patients per Clinic", min_value=0, max_value=50, value=16)
    
    with col2:
        theatre_sessions = st.number_input("Theatre Sessions/Week", min_value=0, max_value=10, value=2)
        cases_per_theatre = st.number_input("Cases per Theatre", min_value=0, max_value=20, value=4)
    
    with col3:
        weeks_available = st.number_input("Weeks Available (next 3 months)", min_value=0, max_value=13, value=10, 
                                          help="Exclude annual leave, study leave, etc.")
    
    # Calculate capacity
    total_new_patients = clinic_sessions * patients_per_clinic * weeks_available
    total_surgeries = theatre_sessions * cases_per_theatre * weeks_available
    
    st.success(f"""
    **{consultant_name}'s Capacity (Next 3 Months):**
    - Can see **{total_new_patients} new patients** in clinic
    - Can perform **{total_surgeries} surgical procedures**
    - Clinic capacity: **{clinic_sessions * patients_per_clinic} patients/week**
    - Theatre capacity: **{theatre_sessions * cases_per_theatre} cases/week**
    """)
    
    # Leave planning
    st.markdown("#### Annual Leave Coverage")
    
    leave_dates = st.date_input("Select Leave Dates (range)", value=(date.today(), date.today() + timedelta(days=7)))
    
    if isinstance(leave_dates, tuple) and len(leave_dates) == 2:
        leave_days = (leave_dates[1] - leave_dates[0]).days
        st.warning(f"""
        ⚠️ **Leave Impact:**
        - **{leave_days} days** of leave planned
        - **{(leave_days / 7) * (clinic_sessions * patients_per_clinic):.0f} patients** affected
        - **{(leave_days / 7) * (theatre_sessions * cases_per_theatre):.0f} surgical slots** lost
        
        **Coverage Required:**
        - Locum consultant needed?
        - Redistribute to colleagues?
        - Reschedule non-urgent cases?
        """)

with tab4:
    st.markdown("### 📈 Demand Forecasting & Planning")
    
    st.markdown("#### Predict Future Demand")
    
    col1, col2 = st.columns(2)
    with col1:
        current_referrals_month = st.number_input("Average Referrals per Month", min_value=0, value=100)
        current_waiting_list = st.number_input("Current Waiting List", min_value=0, value=250)
    
    with col2:
        treatment_rate_month = st.number_input("Treatment Rate per Month", min_value=0, value=90)
        forecast_months = st.slider("Forecast Months Ahead", 1, 12, 6)
    
    # Simple forecast
    forecast_data = []
    running_list = current_waiting_list
    
    for month in range(1, forecast_months + 1):
        running_list = running_list + current_referrals_month - treatment_rate_month
        forecast_data.append({
            "Month": month,
            "Referrals": current_referrals_month,
            "Treated": treatment_rate_month,
            "Waiting List": running_list
        })
    
    df = pd.DataFrame(forecast_data)
    
    st.markdown("#### Waiting List Forecast")
    st.line_chart(df.set_index("Month")["Waiting List"])
    
    st.dataframe(df, use_container_width=True)
    
    # Analysis
    final_list = running_list
    if final_list > current_waiting_list * 1.2:
        st.error(f"""
        🚨 **GROWING WAITING LIST!**
        - List will grow to **{final_list:.0f} patients** in {forecast_months} months
        - Increase of **{final_list - current_waiting_list:.0f} patients** ({((final_list - current_waiting_list) / current_waiting_list * 100):.0f}%)
        - **Action Required:** Increase treatment capacity by {current_referrals_month - treatment_rate_month} patients/month
        """)
    elif final_list < current_waiting_list * 0.8:
        st.success(f"""
        ✅ **REDUCING WAITING LIST!**
        - List will reduce to **{final_list:.0f} patients**
        - Reduction of **{current_waiting_list - final_list:.0f} patients**
        - On track to improve RTT performance
        """)
    else:
        st.info(f"""
        ℹ️ **STABLE WAITING LIST**
        - List will remain around **{final_list:.0f} patients**
        - Supply and demand balanced
        """)

# Quick actions
st.markdown("---")
st.markdown("## ⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Generate Capacity Report", use_container_width=True):
        st.success("Capacity report generated! (Demo)")

with col2:
    if st.button("🚨 Breach Risk Analysis", use_container_width=True):
        st.warning("23 patients at risk of breach within 4 weeks (Demo)")

with col3:
    if st.button("📧 Alert Management Team", use_container_width=True):
        st.info("Alert sent to capacity managers (Demo)")

st.markdown("---")
st.info("""
**💡 Remember:** Poor capacity planning = RTT breaches. Plan ahead, monitor closely, act early!
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
