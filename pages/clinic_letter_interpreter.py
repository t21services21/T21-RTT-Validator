"""
T21 Professional Clinic Letter Interpreter - Streamlit Page
For NHS Staff, Graduates, and Healthcare Professionals
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clinic_letter_interpreter_pro import render_clinic_letter_interpreter

# Page config
st.set_page_config(
    page_title="Clinic Letter Interpreter - T21",
    page_icon="📝",
    layout="wide"
)

# Render the interpreter
render_clinic_letter_interpreter()
