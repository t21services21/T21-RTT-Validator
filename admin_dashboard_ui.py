"""
T21 ADMIN DASHBOARD UI
User interface for admin/tutor monitoring
"""

import streamlit as st
from admin_dashboard import render_admin_dashboard, is_admin_or_tutor


def show_admin_dashboard():
    """Main entry point for admin dashboard"""
    
    # Check authentication
    if not st.session_state.get('logged_in', False):
        st.error("🔒 Please login first")
        st.info("Go to the login page to access the admin dashboard")
        return
    
    # Check admin/tutor privileges
    if not is_admin_or_tutor():
        st.error("🔒 Access Denied")
        st.warning("This dashboard requires Admin or Tutor privileges.")
        st.info("""
        **To access this dashboard, you need:**
        - Admin role
        - Tutor role
        - Staff role
        - Or email ending with @t21services.co.uk, @admin, @staff, or @tutor
        """)
        return
    
    # Render dashboard
    render_admin_dashboard()


if __name__ == "__main__":
    show_admin_dashboard()
