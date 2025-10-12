"""
T21 SERVICES - COMPLIANCE & GOVERNANCE
"""

import streamlit as st
from navigation import render_navigation


# Reusable nav
render_navigation(current_page="compliance")

st.title("🛡️ Compliance & Governance")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Security & Privacy
    - **Cyber Essentials**: Certified ✅
    - **UK GDPR**: Compliant processes and contracts
    - **Data Processing Agreement (DPA)**: Available on request
    - **DPIA Support**: Templates and guidance provided
    - **Access Control**: Role-based access with audit logging
    """)

with col2:
    st.markdown("""
    ### NHS DSPT (Data Security & Protection Toolkit)
    - We **support Trust submissions** by providing an evidence pack
    - Technical/organisational measures documented for IG review
    - Onboarding assistance for information governance
    - Contacts for IG queries provided below
    """)

st.markdown("---")

st.markdown("""
### Documentation Pack
- Statement of Work (SoW)
- Data Processing Agreement (DPA)
- DPIA templates (on request)
- Implementation & onboarding checklist
""")

st.markdown("---")

st.markdown("""
### Contact (Information Governance)
- **Email:** info@t21services.co.uk  
- **Legal:** legal@t21services.co.uk  
- **Phone:** +44 20 3375 2061
""")

if st.button("← Back to Procurement", type="secondary"):
    st.switch_page("pages/procurement.py")
