"""
T21 SERVICES - NHS PROCUREMENT BROCHURE (PRINTABLE)
"""

import streamlit as st
from navigation import render_navigation

st.set_page_config(page_title="Brochure | T21 Services", page_icon="📄", layout="wide")

# Reusable navigation
render_navigation(current_page="brochure")

st.markdown("""
<style>
    @media print {
        .element-container, .stButton { page-break-inside: avoid; }
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 T21 Services – NHS Procurement Overview")

st.markdown("""
**T21 Services Limited** (Company No: 13091053) is a UK Certified Centre delivering TQUK-endorsed training in NHS RTT & Hospital Administration, with AI-enabled tools for operational efficiency.
""")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Credentials
    - TQUK Approved Centre (No: **36257481088**)
    - TQUK-endorsed RTT & Hospital Administration training
    - Cyber Essentials Certified ✅
    - UK GDPR compliant (DPA available)
    """)
with col2:
    st.markdown("""
    ### NHS-Ready Delivery
    - Trust onboarding & staff training
    - Documentation: SoW, DPA, DPIA templates
    - Integration workflows (SystmOne/EMIS), CSV/API where applicable
    - Account management & SLAs
    """)

st.markdown("---")

st.markdown("""
### What We Deliver
- Accredited training programmes (RTT & Hospital Administration)
- AI-enabled admin efficiency (188 scenarios)
- Reporting dashboards and skills transfer
- Quarterly optimisation reviews
""")

st.markdown("---")

st.markdown("""
### Contact
- **Email:** info@t21services.co.uk  
- **Phone:** +44 20 3375 2061  
- **Website:** www.t21services.co.uk

To proceed, please contact us for a DPA and implementation discussion.
""")

st.info("Tip: Use your browser's Print dialog to save this page as PDF.")

if st.button("← Back to Procurement", type="secondary"):
    st.switch_page("pages/procurement.py")
