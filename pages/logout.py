"""
T21 Platform - Logout Page
"""

import streamlit as st

st.set_page_config(page_title="Logout", page_icon="🚪")

st.title("🚪 Logout")

if st.session_state.get('logged_in'):
    user_email = st.session_state.get('user_email', 'User')
    
    st.info(f"Currently logged in as: **{user_email}**")
    
    if st.button("🚪 Logout", type="primary"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.success("✅ Logged out successfully!")
        st.info("You can now close this tab or login again.")
        st.balloons()
        
        # Redirect to login after 2 seconds
        import time
        time.sleep(2)
        st.switch_page("pages/student_login.py")
else:
    st.info("You are not logged in.")
    
    if st.button("← Go to Login"):
        st.switch_page("pages/student_login.py")
