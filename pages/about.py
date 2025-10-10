"""
T21 SERVICES - ABOUT PAGE
"""

import streamlit as st

st.set_page_config(page_title="About Us | T21 Services", page_icon="🏢", layout="wide")

# Navigation bar
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    
    /* Remove all top spacing */
    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .main {
        padding-top: 0 !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .top-nav {
        background: rgba(26, 26, 26, 0.95);
        padding: 15px 60px;
        margin: -100px -70px 30px -70px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .nav-logo-text {
        font-size: 24px;
        font-weight: 800;
        color: #d4af37;
        text-transform: uppercase;
        text-decoration: none;
    }
    
    .nav-menu {
        display: flex;
        gap: 40px;
    }
    
    .nav-link {
        color: white !important;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        text-decoration: none;
        padding: 10px 15px;
    }
    
    .nav-link:hover {
        color: #d4af37 !important;
    }
</style>

<div class='top-nav'>
    <a href='/' style='text-decoration: none;'>
        <span class='nav-logo-text'>T21 SERVICES</span>
    </a>
    <div class='nav-menu'>
        <a href='/about' class='nav-link'>ABOUT</a>
        <a href='/services' class='nav-link'>SERVICES</a>
        <a href='/pricing' class='nav-link'>PRICING</a>
        <a href='/contact' class='nav-link'>CONTACT</a>
    </div>
    <a href='/' style='background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border-radius: 25px; font-weight: 800; text-decoration: none; text-transform: uppercase; font-size: 14px;'>HOME</a>
</div>
""", unsafe_allow_html=True)

st.title("About T21 Services")

st.markdown("""
**T21 Services Limited** is a UK Certified Centre and leading healthcare training, talent supply, and technology company serving the NHS and healthcare sector.

**What We Do:**
- 🎓 **Train Individuals** - Certified NHS administration courses (TQUK-endorsed RTT & Hospital Administration)
- 👥 **Upskill NHS Staff** - Professional development for existing healthcare professionals
- 💼 **Supply Qualified Talent** - Place our trained graduates into NHS roles
- 🤖 **Provide AI Automation** - 7 intelligent systems with 188 scenarios to transform NHS operations
- 🏥 **Support NHS Trusts** - End-to-end workforce and technology solutions

Established in 2020 and registered with Companies House (No: 13091053), we're a UK Certified Centre committed to transforming healthcare workforce development through certified training programs (with TQUK endorsement for RTT and Hospital Administration) and cutting-edge technology solutions.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🏢 Company Details
    - **Registered:** Companies House UK
    - **Company No:** 13091053
    - **Location:** Liverpool, England
    - **Founded:** 2020
    - **VAT Registered:** Yes
    """)

with col2:
    st.markdown("""
    ### ✅ Certifications
    - **UK Certified Centre**
    - **TQUK Endorsement** (RTT & Hospital Admin)
    - **NHS Compliant**
    - **GDPR Certified**
    - **ISO 9001 Standards**
    - **Cyber Essentials**
    """)

with col3:
    st.markdown("""
    ### 📊 Our Impact
    - **500+** Students Trained
    - **50+** NHS Organizations
    - **£2M+** Annual Savings
    - **98%** Satisfaction Rate
    """)

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
