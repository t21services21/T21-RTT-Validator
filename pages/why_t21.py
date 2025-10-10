"""
T21 SERVICES - WHY CHOOSE T21
"""

import streamlit as st

st.set_page_config(page_title="Why T21 | T21 Services", page_icon="🏆", layout="wide")

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
col1, col2, col3, col4, col5, col6 = st.columns(6)
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
    if st.button("📞 CONTACT", use_container_width=True):
        st.switch_page("pages/contact_us.py")
with col6:
    if st.button("🏛️ PROCUREMENT", use_container_width=True):
        st.switch_page("pages/procurement.py")
st.markdown("</div>", unsafe_allow_html=True)

st.title("🏆 Why Choose T21 Services?")

Unlike recruitment agencies or consultancies, we provide end-to-end solutions from training to technology.
""")

st.markdown("---")

# Comparison Table
st.markdown("## 📊 T21 vs Traditional Providers")

st.markdown("""
<div style='overflow-x: auto;'>
<table style='width: 100%; border-collapse: collapse; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
    <thead>
        <tr style='background: linear-gradient(135deg, #d4af37, #f4d03f);'>
            <th style='padding: 20px; text-align: left; color: #1a1a1a; font-size: 16px;'>Feature</th>
            <th style='padding: 20px; text-align: center; color: #1a1a1a; font-size: 16px;'>T21 Services</th>
            <th style='padding: 20px; text-align: center; color: #666; font-size: 16px;'>Recruitment Agencies</th>
            <th style='padding: 20px; text-align: center; color: #666; font-size: 16px;'>Consultancies</th>
        </tr>
    </thead>
    <tbody>
        <tr style='border-bottom: 1px solid #eee;'>
            <td style='padding: 15px; font-weight: 600;'>TQUK-Endorsed Training</td>
            <td style='padding: 15px; text-align: center; color: green; font-size: 24px;'>✅</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee; background: #f8f9fa;'>
            <td style='padding: 15px; font-weight: 600;'>Official Certification</td>
            <td style='padding: 15px; text-align: center; color: green; font-size: 24px;'>✅</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
            <td style='padding: 15px; font-weight: 600;'>Job Application Support</td>
            <td style='padding: 15px; text-align: center; color: green; font-size: 24px;'>✅</td>
            <td style='padding: 15px; text-align: center; color: orange; font-size: 20px;'>⚠️ (Fee-based)</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee; background: #f8f9fa;'>
            <td style='padding: 15px; font-weight: 600;'>AI Automation Tools</td>
            <td style='padding: 15px; text-align: center; color: green; font-size: 24px;'>✅</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
            <td style='padding: 15px; text-align: center; color: orange; font-size: 20px;'>⚠️ (Project-based)</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
            <td style='padding: 15px; font-weight: 600;'>Fixed Pricing</td>
            <td style='padding: 15px; text-align: center; color: green; font-size: 24px;'>✅</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌ (15-25% salary)</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌ (£500-2000/day)</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee; background: #f8f9fa;'>
            <td style='padding: 15px; font-weight: 600;'>Ongoing Support</td>
            <td style='padding: 15px; text-align: center; color: green; font-size: 24px;'>✅</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
            <td style='padding: 15px; text-align: center; color: orange; font-size: 20px;'>⚠️ (Extra cost)</td>
        </tr>
        <tr style='border-bottom: 1px solid #eee;'>
            <td style='padding: 15px; font-weight: 600;'>Alumni Network</td>
            <td style='padding: 15px; text-align: center; color: green; font-size: 24px;'>✅</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
            <td style='padding: 15px; text-align: center; color: red; font-size: 24px;'>❌</td>
        </tr>
    </tbody>
</table>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Unique Advantages
st.markdown("## 🌟 Our Unique Advantages")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎓 Complete Ecosystem
    **Train → Certify → Support → Employ**
    
    We don't just train or recruit - we provide the complete journey from beginner to employed NHS professional.
    
    **Others:** Only do one part
    **T21:** Complete solution
    """)

with col2:
    st.markdown("""
    ### 👔 Ambassador-Led
    **H.E. Ambassador Tosin Michael Owonifari**
    
    Led by an African Union Agenda 2063 Ambassador with 10+ years NHS experience and international credibility.
    
    **Others:** Standard management
    **T21:** Diplomatic-level leadership
    """)

with col3:
    st.markdown("""
    ### 💰 Cost-Effective
    **Fixed Pricing, Maximum Value**
    
    £99-£1,799 for complete training vs £10,000+ for recruitment fees or consultancy projects.
    
    **Others:** 15-25% salary or £500-2000/day
    **T21:** Fixed, affordable pricing
    """)

st.markdown("---")

# ROI Comparison
st.markdown("## 💰 Cost Comparison Example")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d4af37, #f4d03f); padding: 30px; border-radius: 15px;'>
        <h3 style='color: #1a1a1a; margin-top: 0;'>🏆 T21 Services</h3>
        <p style='color: #1a1a1a; font-size: 18px; line-height: 1.8;'>
        <strong>For Individuals:</strong><br>
        £1,299 - Complete TQUK certification + job support<br><br>
        <strong>For NHS Trusts:</strong><br>
        Custom pricing - AI automation + training<br>
        £2M+ annual savings proven
        </p>
        <p style='color: #1a1a1a; font-weight: 800; font-size: 24px; margin-bottom: 0;'>✅ Fixed Cost, Maximum ROI</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 30px; border-radius: 15px; border: 2px solid #ddd;'>
        <h3 style='color: #666; margin-top: 0;'>Traditional Providers</h3>
        <p style='color: #666; font-size: 18px; line-height: 1.8;'>
        <strong>Recruitment Agencies:</strong><br>
        15-25% of annual salary (£6,000-£10,000+ per hire)<br><br>
        <strong>Consultancies:</strong><br>
        £500-£2,000 per day<br>
        Projects cost £50,000-£500,000+
        </p>
        <p style='color: #666; font-weight: 800; font-size: 24px; margin-bottom: 0;'>❌ Variable, High Cost</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Success Metrics
st.markdown("## 📈 Proven Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Students Trained", "500+", "+150 this year")

with col2:
    st.metric("Job Success Rate", "85%", "+10% vs industry")

with col3:
    st.metric("NHS Organizations", "50+", "Growing monthly")

with col4:
    st.metric("Satisfaction Rate", "98%", "5-star reviews")

st.markdown("---")

# Call to Action
st.markdown("## 🚀 Ready to Experience the T21 Difference?")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎓 View Courses", use_container_width=True, type="primary"):
        st.switch_page("pages/pricing.py")

with col2:
    if st.button("⭐ Read Testimonials", use_container_width=True, type="primary"):
        st.switch_page("pages/testimonials.py")

with col3:
    if st.button("📞 Contact Sales", use_container_width=True, type="primary"):
        st.switch_page("pages/contact_us.py")

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
