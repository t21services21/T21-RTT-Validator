"""
T21 Admin Dashboard Page
Access point for tutors and administrators
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin_dashboard_ui import show_admin_dashboard

# Page config
st.set_page_config(
    page_title="Admin Dashboard - T21 RTT",
    page_icon="👨‍🏫",
    layout="wide"
)

# Show dashboard
show_admin_dashboard()
