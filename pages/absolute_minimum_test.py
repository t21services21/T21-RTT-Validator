import streamlit as st

st.title("✅ ABSOLUTE MINIMUM TEST")
st.success("If you see this, basic Streamlit pages work!")
st.error("If you DON'T see this, there's a deployment issue")
st.info("This page has ZERO imports, ZERO dependencies")

if st.button("Back"):
    st.switch_page("app.py")
