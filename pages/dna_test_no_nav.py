"""
DNA MANAGEMENT - TEST WITHOUT NAVIGATION
Testing if navigation.py is causing the crash
"""

import streamlit as st
from datetime import datetime

# NO navigation.py import!
# from navigation import render_navigation

st.title("📵 DNA Management - Test Version")
st.success("✅ If you see this, navigation.py was the problem!")

st.markdown("## Quick Test")

st.info("""
This version DOES NOT use render_navigation()

If this loads but the regular version doesn't, then navigation.py is crashing all the pages!
""")

# Simple form
st.markdown("### Add DNA Case")

patient_name = st.text_input("Patient Name")
nhs_number = st.text_input("NHS Number")

if st.button("Save"):
    st.success(f"Would save: {patient_name} - {nhs_number}")

st.markdown("---")

# Educational content
with st.expander("📚 What is DNA?"):
    st.markdown("""
    **DNA = Did Not Attend**
    
    When a patient fails to attend a scheduled appointment.
    
    **RTT Impact:** Clock CONTINUES running!
    """)

if st.button("← Back to Main App"):
    st.switch_page("app.py")
