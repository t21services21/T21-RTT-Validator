"""
T21 HEALTHCARE PLATFORM - DNA MANAGEMENT MODULE  
Simplified version that definitely works
"""

import streamlit as st
from datetime import datetime
from navigation import render_navigation

st.set_page_config(page_title="DNA Management | T21 Services", page_icon="📵", layout="wide")

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

# Try to import CRUD, but don't crash if it fails
try:
    import os
    import sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    from universal_crud import (
        create_record, read_all_records, read_record_by_id,
        update_record, delete_record, search_records, export_to_csv
    )
    CRUD_AVAILABLE = True
    st.success("✅ CRUD System Loaded Successfully")
except Exception as e:
    CRUD_AVAILABLE = False
    st.error(f"⚠️ CRUD System Not Available: {e}")
    st.info("Showing educational content only. Database features temporarily disabled.")

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
    """)

# Show CRUD interface only if available
if CRUD_AVAILABLE:
    st.markdown("---")
    st.markdown("## 💼 DNA Case Management")
    
    tab1, tab2 = st.tabs(["📋 View All Cases", "➕ Add New DNA"])
    
    with tab1:
        st.subheader("📋 All DNA Cases")
        records = read_all_records('dna_cases')
        
        if records:
            st.info(f"Total DNA Cases: {len(records)}")
            for idx, record in enumerate(records):
                st.json(record)
        else:
            st.info("No DNA cases recorded yet.")
    
    with tab2:
        st.subheader("➕ Record New DNA Case")
        
        patient_name = st.text_input("Patient Name")
        nhs_number = st.text_input("NHS Number")
        
        if st.button("💾 Save"):
            if patient_name and nhs_number:
                data = {
                    'patient_name': patient_name,
                    'nhs_number': nhs_number,
                    'date': str(datetime.now())
                }
                if create_record('dna_cases', data):
                    st.success("Saved!")
else:
    st.warning("Database features are temporarily unavailable. Contact support if this persists.")

# Back button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
