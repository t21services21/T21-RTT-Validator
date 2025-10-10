"""
T21 SERVICES - TESTIMONIALS & SUCCESS STORIES
"""

import streamlit as st

st.set_page_config(page_title="Testimonials | T21 Services", page_icon="⭐", layout="wide")

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
    <span class='nav-logo-text'>T21 SERVICES</span>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
st.markdown("<div style='background: rgba(26, 26, 26, 0.95); padding: 10px; margin: -30px -70px 20px -70px;'>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 HOME", key="nav_home", use_container_width=True, type="primary"):
        st.switch_page("app.py")
with col2:
    if st.button("📋 ABOUT", key="nav_about", use_container_width=True):
        st.switch_page("pages/about.py")
with col3:
    if st.button("🛠️ SERVICES", key="nav_services", use_container_width=True):
        st.switch_page("pages/services.py")
with col4:
    if st.button("💰 PRICING", key="nav_pricing", use_container_width=True):
        st.switch_page("pages/pricing.py")
with col5:
    if st.button("📞 CONTACT", key="nav_contact", use_container_width=True):
        st.switch_page("pages/contact_us.py")
st.markdown("</div>", unsafe_allow_html=True)

st.title("⭐ Student Success Stories & Testimonials")

st.markdown("""
**Real stories from real students who transformed their careers with T21 Services**

Our TQUK-endorsed training programs have helped hundreds of individuals secure NHS roles. 
Here's what they have to say about their journey with us.
""")

st.markdown("---")

# YouTube Channel Link
st.markdown("## 📺 Watch Our Student Testimonials")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; color: white;'>
    <h3 style='margin: 0 0 15px 0;'>🎥 Full Video Testimonials on YouTube</h3>
    <p style='font-size: 18px; margin-bottom: 20px;'>Watch dozens of success stories from our graduates</p>
    <a href='https://www.youtube.com/channel/UCVzalMNDgFgJptD3Brnfktg' target='_blank' style='background: white; color: #764ba2; padding: 15px 40px; border-radius: 25px; text-decoration: none; font-weight: 800; font-size: 16px; display: inline-block;'>
        ▶️ VISIT OUR YOUTUBE CHANNEL
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Success Stats
st.markdown("## 📊 Our Impact in Numbers")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center;'>
        <h2 style='color: #d4af37; font-size: 48px; margin: 0;'>500+</h2>
        <p style='color: #666; font-weight: 600;'>Students Trained</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center;'>
        <h2 style='color: #d4af37; font-size: 48px; margin: 0;'>85%</h2>
        <p style='color: #666; font-weight: 600;'>Job Success Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center;'>
        <h2 style='color: #d4af37; font-size: 48px; margin: 0;'>98%</h2>
        <p style='color: #666; font-weight: 600;'>Satisfaction Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center;'>
        <h2 style='color: #d4af37; font-size: 48px; margin: 0;'>50+</h2>
        <p style='color: #666; font-weight: 600;'>NHS Organizations</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sample Testimonials
st.markdown("## 💬 What Our Students Say")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;'>
        <p style='font-size: 16px; color: #555; line-height: 1.8; font-style: italic;'>
        "T21 Services transformed my career. The RTT training was comprehensive and the job application support helped me secure my dream NHS role within 3 months of completing the course!"
        </p>
        <p style='margin-top: 15px; font-weight: 700; color: #d4af37;'>⭐⭐⭐⭐⭐</p>
        <p style='color: #666; font-weight: 600;'>— Sarah M., RTT Coordinator</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;'>
        <p style='font-size: 16px; color: #555; line-height: 1.8; font-style: italic;'>
        "The TQUK certification gave me the credibility I needed. The AI tutor was amazing and helped me understand complex NHS pathways. Now working at a major NHS trust!"
        </p>
        <p style='margin-top: 15px; font-weight: 700; color: #d4af37;'>⭐⭐⭐⭐⭐</p>
        <p style='color: #666; font-weight: 600;'>— James K., Hospital Administrator</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;'>
        <p style='font-size: 16px; color: #555; line-height: 1.8; font-style: italic;'>
        "Best investment I ever made! The Tier 3 package with job application support was worth every penny. They helped me with my CV, applications, and interview prep. Got 3 job offers!"
        </p>
        <p style='margin-top: 15px; font-weight: 700; color: #d4af37;'>⭐⭐⭐⭐⭐</p>
        <p style='color: #666; font-weight: 600;'>— Amina T., Cancer Pathway Coordinator</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;'>
        <p style='font-size: 16px; color: #555; line-height: 1.8; font-style: italic;'>
        "Coming from a non-NHS background, I was nervous. But T21's training was so thorough and the support was incredible. Now I'm a confident NHS professional!"
        </p>
        <p style='margin-top: 15px; font-weight: 700; color: #d4af37;'>⭐⭐⭐⭐⭐</p>
        <p style='color: #666; font-weight: 600;'>— David L., RTT Validator</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# NHS Organizations
st.markdown("## 🏥 Our Graduates Work At")
st.markdown("*Our trained students have successfully secured roles at NHS trusts including:*")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    - **Manchester NHS Trust**
    - **Liverpool NHS Trust**
    - **Leeds NHS Trust**
    - **Birmingham NHS Trusts**
    """)

with col2:
    st.markdown("""
    - **Wolverhampton NHS Trust**
    - **Various London NHS Trusts**
    - **Royal Liverpool University Hospital**
    - **University Hospitals Birmingham**
    """)

with col3:
    st.markdown("""
    - **Leeds Teaching Hospitals**
    - **Manchester University NHS FT**
    - **Multiple NHS Trusts Nationwide**
    - **50+ NHS Organizations**
    """)

st.markdown("---")

# Call to Action
st.markdown("## 🚀 Start Your NHS Career Journey")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 View Courses", use_container_width=True, type="primary"):
        st.switch_page("pages/pricing.py")

with col2:
    if st.button("🎓 Register Now", use_container_width=True, type="primary"):
        st.switch_page("pages/student_login.py")

with col3:
    if st.button("📞 Contact Us", use_container_width=True, type="primary"):
        st.switch_page("pages/contact_us.py")

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
