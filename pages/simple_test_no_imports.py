"""
SIMPLEST POSSIBLE TEST PAGE
No imports except streamlit - if this doesn't work, nothing will
"""

import streamlit as st

st.title("🧪 Simple Test Page - No Imports")
st.success("✅ This page loaded successfully!")

st.markdown("## This proves:")
st.markdown("- ✅ Streamlit is working")
st.markdown("- ✅ Pages can load via st.switch_page()")
st.markdown("- ✅ Basic rendering works")

st.info("If you see this, the problem is with module imports or navigation.py")

if st.button("← Back to Main App"):
    st.switch_page("app.py")
