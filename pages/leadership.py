"""
T21 SERVICES - LEADERSHIP PAGE
"""

import streamlit as st

st.set_page_config(page_title="Leadership | T21 Services", page_icon="👔", layout="wide")

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
        <a href='/contact_us' class='nav-link'>CONTACT</a>
    </div>
    <a href='/' style='background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border-radius: 25px; font-weight: 800; text-decoration: none; text-transform: uppercase; font-size: 14px;'>HOME</a>
</div>
""", unsafe_allow_html=True)

st.title("Leadership Team")

st.markdown("---")

# CEO Profile
st.markdown("## 👔 Founder & Chief Executive Officer")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d4af37, #f4d03f); padding: 40px; border-radius: 15px; text-align: center;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>👨‍💼</div>
        <h2 style='color: #1a1a1a; margin: 0;'>H.E. Ambassador</h2>
        <h3 style='color: #1a1a1a; margin: 10px 0;'>Tosin Michael Owonifari</h3>
        <p style='color: #1a1a1a; font-weight: 600;'>Founder & CEO</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### Professional Background
    
    **H.E. Ambassador Tosin Michael Owonifari** is the Founder and Chief Executive Officer of T21 Services Limited, bringing over **10 years of specialized experience** in NHS healthcare administration, training, and digital transformation.
    
    ### Key Roles & Achievements
    
    - 🌍 **African Union Agenda 2063 Ambassador**
    - 🏥 **10+ Years NHS Experience** - Healthcare administration, RTT pathways, and workforce development
    - 🎓 **TQUK Approved Centre Director** - Centre No: 36257481088
    - 🤖 **Healthcare Innovation Leader** - AI automation and digital transformation
    - 💼 **Workforce Development Expert** - Training and talent supply for NHS organizations
    
    ### Vision & Mission
    
    Ambassador Owonifari founded T21 Services with a clear vision: to transform NHS workforce development through innovative training programs and cutting-edge technology solutions. His deep understanding of NHS challenges, combined with expertise in AI automation, has positioned T21 Services as a leading provider of healthcare training and technology solutions.
    
    ### Areas of Expertise
    
    - NHS Referral to Treatment (RTT) Pathways
    - Hospital Administration & Management
    - Healthcare Workforce Training & Development
    - AI-Powered Healthcare Automation
    - NHS Digital Transformation
    - TQUK-Endorsed Training Programs
    - Healthcare Talent Supply & Recruitment
    
    ### Education & Certifications
    
    - TQUK Approved Centre Director
    - African Union Agenda 2063 Ambassador
    - NHS Healthcare Administration Specialist
    - Digital Transformation & AI Implementation
    
    ### Contact
    
    📧 **Email:** info@t21services.co.uk  
    📞 **Phone:** +44 20 3375 2061  
    🌐 **LinkedIn:** [Connect with Ambassador Owonifari](https://linkedin.com/in/tosinowonifari)
    """)

st.markdown("---")

# Company Philosophy
st.markdown("## 🎯 Our Leadership Philosophy")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🌟 Innovation
    We continuously innovate to provide cutting-edge solutions that address real NHS challenges. Our AI-powered automation and training programs are designed with deep NHS expertise.
    """)

with col2:
    st.markdown("""
    ### 🤝 Partnership
    We believe in true partnership with NHS organizations, working collaboratively to understand unique challenges and deliver tailored solutions that drive real results.
    """)

with col3:
    st.markdown("""
    ### 📈 Excellence
    We maintain the highest standards in everything we do, from TQUK-endorsed training programs to AI automation systems, ensuring quality and compliance at every level.
    """)

st.markdown("---")

# Call to Action
st.markdown("## 📞 Connect With Our Leadership")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📧 Contact CEO", use_container_width=True, type="primary"):
        st.switch_page("pages/contact_us.py")

with col2:
    if st.button("🏢 About T21 Services", use_container_width=True, type="primary"):
        st.switch_page("pages/about.py")

with col3:
    if st.button("🤝 Book a Meeting", use_container_width=True, type="primary"):
        st.switch_page("pages/contact_us.py")

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
