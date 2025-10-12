"""
UNIVERSAL PAGE FOOTER
Add navigation back to main platform
"""

import streamlit as st

def render_back_button(button_text="← Back to Platform Dashboard"):
    """Render a centered back button to return to main platform"""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(button_text, use_container_width=True, type="primary", key="back_to_platform"):
            st.switch_page("app.py")

def render_page_footer_with_info(info_text=None):
    """Render footer with optional info message and back button"""
    if info_text:
        st.markdown("---")
        st.info(info_text)
    
    render_back_button()
