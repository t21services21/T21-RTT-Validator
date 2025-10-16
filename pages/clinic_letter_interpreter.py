"""
T21 Professional Clinic Letter Interpreter - Streamlit Page
For NHS Staff, Graduates, and Healthcare Professionals
"""

import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Page config
st.set_page_config(
    page_title="Clinic Letter Interpreter - T21",
    page_icon="📝",
    layout="wide"
)

# Try to import and render
try:
    from clinic_letter_interpreter_pro import render_clinic_letter_interpreter
    render_clinic_letter_interpreter()
except Exception as e:
    st.error(f"""
    ⚠️ **Clinic Letter Interpreter Temporarily Unavailable**
    
    This module is being updated. Please try again later or contact support.
    
    **Error:** {str(e)}
    """)
    st.info("💡 **Alternative:** Use the main app's RTT Validator for clinic letter processing.")
