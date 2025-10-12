"""
T21 HEALTHCARE PLATFORM - COMMISSIONER REPORTING
Auto-generate monthly NHS England RTT submissions
"""

import streamlit as st
from datetime import datetime
from navigation import render_navigation
import pandas as pd

st.set_page_config(page_title="Commissioner Reporting | T21 Services", page_icon="📊", layout="wide")

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
