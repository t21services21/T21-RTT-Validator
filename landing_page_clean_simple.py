"""
T21 SERVICES - SIMPLE WORKING LANDING PAGE
"""

import streamlit as st

def render_clean_landing_page():
    """Simple working landing page"""
    
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        header[data-testid="stHeader"] {display: none;}
        .main .block-container {padding-top: 0; margin-top: -80px;}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# T21 Healthcare Intelligence Platform")
    st.markdown("## Your NHS Career & Workforce Partner")
    st.markdown("**Training • Talent • Technology**")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎓 STUDENT LOGIN", use_container_width=True, type="primary"):
            st.switch_page("pages/student_login.py")
    with col2:
        if st.button("👥 STAFF LOGIN", use_container_width=True, type="primary"):
            st.switch_page("pages/staff_login.py")
    with col3:
        if st.button("🏥 NHS LOGIN", use_container_width=True, type="primary"):
            st.switch_page("pages/nhs_login.py")
