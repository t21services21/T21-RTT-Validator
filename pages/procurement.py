"""
T21 SERVICES - PROCUREMENT (NHS BUYERS)
"""

import streamlit as st

st.set_page_config(page_title="Procurement | T21 Services", page_icon="🏛️", layout="wide")

# Basic chrome
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    .main .block-container { padding-top: 0 !important; margin-top: 0 !important; }
    header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Simple top bar (text + buttons)
st.markdown("<div style='background: rgba(26,26,26,0.95); padding: 15px 60px; margin: -100px -70px 20px -70px; box-shadow: 0 2px 10px rgba(0,0,0,0.3); color: #d4af37; font-weight: 800; text-transform: uppercase;'>T21 SERVICES</div>", unsafe_allow_html=True)

nav = st.columns(6)
with nav[0]:
    if st.button("🏠 HOME", use_container_width=True, type="primary"):
        st.switch_page("app.py")
with nav[1]:
    if st.button("📋 ABOUT", use_container_width=True):
        st.switch_page("pages/about.py")
with nav[2]:
    if st.button("🛠️ SERVICES", use_container_width=True):
        st.switch_page("pages/services.py")
with nav[3]:
    if st.button("💰 PRICING", use_container_width=True):
        st.switch_page("pages/pricing.py")
with nav[4]:
    if st.button("📞 CONTACT", use_container_width=True):
        st.switch_page("pages/contact_us.py")
with nav[5]:
    if st.button("⭐ TESTIMONIALS", use_container_width=True):
        st.switch_page("pages/testimonials.py")

st.title("🏛️ Procurement for NHS Buyers")

st.markdown("""
Our solutions can be procured directly by NHS organizations. We provide full documentation and contracts to support
information governance, data protection, and deployment planning.
""")

st.markdown("---")

# Credentials & Compliance
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    ### ✅ Credentials
    - TQUK Approved Centre (No: **36257481088**)
    - TQUK-endorsed RTT & Hospital Administration training
    - Companies House Registered (No: **13091053**)
    """)
with col2:
    st.markdown("""
    ### 🔒 Security
    - Cyber Essentials Certified
    - UK GDPR compliant
    - Data Processing Agreement (DPA) available
    - Role-based access & audit logs
    """)
with col3:
    st.markdown("""
    ### 🏥 NHS-Ready
    - NHS-compliant processes and documentation
    - Integration support (SystmOne/EMIS workflows, CSV, API where applicable)
    - Onboarding & training for staff
    - Account management & support
    """)

st.markdown("---")

# What you get
st.markdown("## 📦 What We Deliver")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - TQUK-endorsed training programmes (RTT & Hospital Administration)
    - AI-powered tools for admin efficiency (188 scenarios)
    - Reporting & oversight dashboards
    - Implementation & skills transfer
    """)
with col2:
    st.markdown("""
    - Flexible licensing (trust-wide or department)
    - SLAs & support options
    - Documentation pack (SoW, DPA, DPIA templates)
    - Quarterly review & optimisation
    """)

st.markdown("---")

# Compliance & Governance
st.markdown("## 🛡️ Compliance & Governance")
colc1, colc2 = st.columns(2)
with colc1:
    st.markdown("""
    - **Cyber Essentials**: Certified ✅
    - **UK GDPR**: Compliant processes and contracts
    - **Data Processing Agreement (DPA)**: Available
    - **DPIA support**: Templates and guidance provided
    """)
with colc2:
    st.markdown("""
    - **NHS DSPT**: We support Trust submissions and provide evidence pack
    - **Audit & Logging**: Role-based access and audit trails
    - **Onboarding**: IG reviews, documentation, and training
    """)

st.markdown("---")

# Actions
cta = st.columns(3)
with cta[0]:
    if st.button("📞 Book a Demo", use_container_width=True, type="primary"):
        st.switch_page("pages/contact_us.py")
with cta[1]:
    if st.button("📄 Request DPA Pack", use_container_width=True):
        st.switch_page("pages/contact_us.py")
with cta[2]:
    if st.button("🏗️ Implementation Planning", use_container_width=True):
        st.switch_page("pages/contact_us.py")

st.markdown("---")

st.caption("T21 Services Limited | Company No: 13091053 | Liverpool, England | info@t21services.co.uk | +44 20 3375 2061")
