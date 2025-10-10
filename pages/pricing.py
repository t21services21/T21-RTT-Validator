"""
T21 SERVICES - PRICING PAGE
"""

import streamlit as st
from navigation import render_navigation

st.set_page_config(page_title="Pricing | T21 Services", page_icon="💰", layout="wide")

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
    <img src='assets/t21_logo.png' alt='T21 SERVICES' style='height:34px; vertical-align: middle; border-radius: 50%; margin-right:10px;' onerror="this.style.display='none';">
    <span class='nav-logo-text'>T21 SERVICES</span>
</div>
""", unsafe_allow_html=True)

# Reusable navigation
render_navigation(current_page="pricing")

st.title("Pricing Plans")
st.markdown("*Certified NHS Training Courses - UK Certified Centre with TQUK Endorsement*")

st.markdown("---")

# Student Pricing
st.markdown("## 🎓 Student Pricing Plans")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;'>
        <h3 style='color: #d4af37;'>🆓 Taster</h3>
        <p style='font-size: 42px; font-weight: 800; color: #1a1a1a; margin: 15px 0;'>£99</p>
        <p style='color: #666;'>1 Month</p>
        <ul style='text-align: left; color: #555; line-height: 1.8; font-size: 14px;'>
            <li>✅ Try the platform</li>
            <li>✅ Limited AI tutor (10 Q/day)</li>
            <li>✅ Basic training modules</li>
            <li>❌ No certification</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;'>
        <h3 style='color: #d4af37;'>📚 Tier 1 Practice</h3>
        <p style='font-size: 42px; font-weight: 800; color: #1a1a1a; margin: 15px 0;'>£499</p>
        <p style='color: #666;'>6 Months</p>
        <ul style='text-align: left; color: #555; line-height: 1.8; font-size: 14px;'>
            <li>✅ Full platform access</li>
            <li>✅ Unlimited AI tutor</li>
            <li>✅ All training scenarios</li>
            <li>✅ CV & interview prep</li>
            <li>❌ No certification</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d4af37, #f4d03f); padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); text-align: center;'>
        <h3 style='color: #1a1a1a;'>🎓 Tier 2 Certified</h3>
        <p style='font-size: 42px; font-weight: 800; color: #1a1a1a; margin: 15px 0;'>£1,299</p>
        <p style='color: #1a1a1a;'>12 Months</p>
        <ul style='text-align: left; color: #1a1a1a; line-height: 1.8; font-size: 14px;'>
            <li>✅ Everything in Tier 1</li>
            <li>✅ Certified qualification (TQUK-endorsed)</li>
            <li>✅ Job application support</li>
            <li>✅ Alumni network (lifetime)</li>
            <li>✅ 10 months post-cert access</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;'>
        <h3 style='color: #d4af37;'>💼 Tier 3 Premium</h3>
        <p style='font-size: 42px; font-weight: 800; color: #1a1a1a; margin: 15px 0;'>£1,799</p>
        <p style='color: #666;'>12 Months</p>
        <ul style='text-align: left; color: #555; line-height: 1.8; font-size: 14px;'>
            <li>✅ Everything in Tier 2</li>
            <li>✅ <strong>Job application support</strong> (CV, forms, monitoring)</li>
            <li>✅ Dedicated career coach</li>
            <li>✅ Interview preparation & scheduling</li>
            <li>✅ Ongoing support (no employment guarantee)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# NHS Organization Pricing
st.markdown("## 🏥 NHS Organization Pricing")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);'>
        <h3 style='color: #d4af37; text-align: center;'>🏥 NHS Trust Package</h3>
        <p style='font-size: 42px; font-weight: 800; color: #1a1a1a; margin: 20px 0; text-align: center;'>Custom</p>
        <p style='color: #666; text-align: center;'>Tailored to your trust</p>
        <ul style='color: #555; line-height: 2;'>
            <li>✅ Trust-wide deployment (unlimited users)</li>
            <li>✅ NHS framework compliant</li>
            <li>✅ Data Processing Agreement included</li>
            <li>✅ On-site training & implementation</li>
            <li>✅ Integration with EPR systems (SystmOne, EMIS, etc.)</li>
            <li>✅ AI-powered automation (188 scenarios)</li>
            <li>✅ Dedicated account manager</li>
            <li>✅ 24/7 priority support</li>
            <li>✅ Custom reporting & analytics</li>
            <li>✅ Annual cost savings: £2M+ proven</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); color: white;'>
        <h3 style='text-align: center; margin-bottom: 20px;'>💡 Why NHS Trusts Choose Us</h3>
        <p style='font-size: 16px; line-height: 1.8;'>
        <strong>Transform your workforce training and reduce administrative burden with our proven NHS-compliant platform.</strong>
        </p>
        <ul style='line-height: 2; margin-top: 20px;'>
            <li><strong>Reduce RTT breaches</strong> by up to 40%</li>
            <li><strong>Save £2M+ annually</strong> through automation</li>
            <li><strong>Train staff 3x faster</strong> with AI-powered learning</li>
            <li><strong>GDPR & NHS compliant</strong> - fully audited</li>
            <li><strong>Integrate seamlessly</strong> with existing systems</li>
            <li><strong>Proven results</strong> across 50+ NHS organizations</li>
        </ul>
        <div style='text-align: center; margin-top: 30px;'>
            <p style='font-size: 18px; font-weight: 700;'>📞 Book a demo: +44 20 3375 2061</p>
            <p style='font-size: 14px;'>📧 info@t21services.co.uk</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Call to Action
st.markdown("## 🚀 Ready to Get Started?")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎓 Student Registration", use_container_width=True, type="primary"):
        st.switch_page("pages/student_login.py")

with col2:
    if st.button("👥 Staff Portal", use_container_width=True, type="primary"):
        st.switch_page("pages/staff_login.py")

with col3:
    if st.button("🏥 Contact Sales", use_container_width=True, type="primary"):
        st.switch_page("pages/contact_us.py")

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
