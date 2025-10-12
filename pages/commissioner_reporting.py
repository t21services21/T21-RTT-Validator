"""
T21 HEALTHCARE PLATFORM - COMMISSIONER REPORTING
Auto-generate monthly NHS England RTT submissions
"""

import streamlit as st
from datetime import datetime
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



st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="commissioner")

st.title("📊 Commissioner Reporting - NHS England Submissions")
st.markdown("**Auto-generate monthly RTT reports for NHS England**")

with st.expander("📚 What is Commissioner Reporting?", expanded=True):
    st.markdown("""
    ### Monthly NHS England Submissions
    
    **Required Reports:**
    - RTT Incomplete Pathways (waiting list)
    - RTT Completed Pathways (treated patients)
    - 52-Week Waiters (critical breaches)
    - Cancer 2-Week Wait
    - Diagnostic 6-Week Wait
    
    **Deadline:** 2nd Thursday after month end
    
    **Published:** Publicly on NHS England website
    """)


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Report Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Reports")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_commissioner_reports")
    with col2:
        records = read_all_records('commissioner_reports')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "commissioner_reports.csv", "text/csv")
    
    # Get records
    records = read_all_records('commissioner_reports')
    
    if search_term:
        records = search_records('commissioner_reports', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Report #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('commissioner_reports', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Report")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('commissioner_reports')
    
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

# Quick report generator
col1, col2 = st.columns(2)
with col1:
    report_month = st.selectbox("Report Month", ["January 2025", "February 2025", "March 2025"])
with col2:
    report_type = st.selectbox("Report Type", [
        "RTT Incomplete Pathways",
        "52-Week Waiter Report",
        "Full Monthly Submission"
    ])

if st.button("📊 Generate Report", type="primary", use_container_width=True):
    st.success("✅ Report generated!")
    
    # Demo data
    demo_data = pd.DataFrame({
        "Specialty": ["Orthopaedics", "Cardiology", "ENT", "General Surgery"],
        "Total Waiting": [450, 320, 280, 510],
        "Within 18 Weeks": [410, 298, 265, 475],
        ">18 Weeks": [40, 22, 15, 35],
        "% Within Target": ["91.1%", "93.1%", "94.6%", "93.1%"]
    })
    
    st.dataframe(demo_data, use_container_width=True)
    
    st.info("""
    **Trust Performance:**
    - Overall: **92.8%** within 18 weeks ✅
    - Target: 92%
    - 52-week waiters: 0
    - Status: COMPLIANT
    """)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("📥 Download CSV", use_container_width=True)
    with col_b:
        st.button("📧 Submit to NHS England", use_container_width=True)

st.markdown("---")
st.info("💡 **For Students:** Practice generating reports with demo data. For NHS: Use real data from PAS system.")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
