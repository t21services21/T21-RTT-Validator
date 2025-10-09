"""
T21 HEALTHCARE INTELLIGENCE PLATFORM - MAIN LANDING PAGE
Professional landing page with portal routing

By T21 Services Limited
Company No: 13091053
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="T21 Healthcare Intelligence Platform | T21 Services Limited",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional landing page
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
    }
    
    .hero h1 {
        font-size: 48px;
        margin-bottom: 20px;
        font-weight: 700;
    }
    
    .hero p {
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    .hero .subtitle {
        font-size: 18px;
        color: #e0e0e0;
    }
    
    /* Portal cards */
    .portal-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .portal-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    
    .portal-card h3 {
        color: #667eea;
        font-size: 24px;
        margin-bottom: 15px;
    }
    
    .portal-card p {
        color: #666;
        font-size: 16px;
        margin-bottom: 20px;
    }
    
    /* Feature section */
    .feature-box {
        background: #f8f9fa;
        padding: 30px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    /* Stats section */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    
    .stat-box h2 {
        font-size: 48px;
        margin: 0;
    }
    
    .stat-box p {
        font-size: 16px;
        margin: 5px 0 0 0;
    }
    
    /* Footer */
    .footer {
        background: #2c3e50;
        color: white;
        padding: 40px 20px;
        border-radius: 10px;
        margin-top: 60px;
    }
    
    .footer a {
        color: #3498db;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>🏥 T21 Healthcare Intelligence Platform</h1>
    <p>Complete NHS Healthcare Administration Suite</p>
    <p class="subtitle">Training & Automation in One Platform</p>
    <p class="subtitle">✨ 7 Integrated Modules | 15+ NHS Roles | AI-Powered Throughout</p>
</div>
""", unsafe_allow_html=True)

# Quick Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <h2>7</h2>
        <p>Integrated Modules</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h2>15+</h2>
        <p>NHS Roles Trained</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <h2>£2M+</h2>
        <p>Annual Savings</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <h2>500x</h2>
        <p>Faster Processing</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Portal Selection
st.markdown("## 🚪 Choose Your Portal")
st.markdown("Select the portal that matches your role:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="portal-card">
        <h3>🏥 NHS Organizations</h3>
        <p>For NHS Trusts, Hospitals, and Healthcare Organizations using our operational systems</p>
        <p><strong>Access:</strong></p>
        <ul style="text-align: left; color: #666;">
            <li>RTT & Pathway Management</li>
            <li>Cancer Pathway Tracking</li>
            <li>MDT Coordination</li>
            <li>Appointment Systems</li>
            <li>Medical Secretary AI</li>
            <li>Data Quality Tools</li>
            <li>Full Admin Dashboard</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏥 NHS/Organization Login", type="primary", use_container_width=True):
        st.switch_page("pages/nhs_login.py")

with col2:
    st.markdown("""
    <div class="portal-card">
        <h3>🎓 Students & Learners</h3>
        <p>For individuals training for NHS administration roles</p>
        <p><strong>Access:</strong></p>
        <ul style="text-align: left; color: #666;">
            <li>188 Hands-On Scenarios</li>
            <li>15+ NHS Role Training</li>
            <li>AI Tutor 24/7</li>
            <li>Interactive Learning</li>
            <li>Certification Exams</li>
            <li>Progress Tracking</li>
            <li>Career Resources</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎓 Student Training Portal", type="primary", use_container_width=True):
        st.switch_page("pages/student_login.py")

with col3:
    st.markdown("""
    <div class="portal-card">
        <h3>👥 Staff & Partners</h3>
        <p>For T21 Services staff, training providers, and authorized partners</p>
        <p><strong>Access:</strong></p>
        <ul style="text-align: left; color: #666;">
            <li>Admin Control Panel</li>
            <li>User Management</li>
            <li>Course Management</li>
            <li>School Administration</li>
            <li>Revenue & Analytics</li>
            <li>Bulk Operations</li>
            <li>System Configuration</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👥 Staff/Partner Portal", type="primary", use_container_width=True):
        st.switch_page("pages/staff_login.py")

st.markdown("---")

# Features Section
st.markdown("## ⭐ Why Choose T21 Healthcare Intelligence Platform?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 AI-Powered Throughout</h3>
        <p>13 intelligent AI systems automate complex tasks, predict breaches 4 weeks ahead, and provide decision support.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
        <h3>💰 Proven ROI</h3>
        <p>NHS trusts save £2M+ annually through automation, breach prevention, and staff efficiency gains.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
        <h3>🎓 Dual-Purpose Platform</h3>
        <p>Train staff on the platform, then use it for operations. Zero learning curve. Immediate productivity.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>⚡ 100-500x Faster</h3>
        <p>Automate tasks that take hours manually in seconds with AI. RTT validation: 30 mins → 15 seconds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
        <h3>🔧 Complete Integration</h3>
        <p>7 modules work seamlessly together. One platform for all NHS admin needs - no disconnected systems.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
        <h3>💡 Cost Effective</h3>
        <p>£350k/year for complete suite vs £10M+ for Epic/Cerner. 1/40th the cost with superior admin capabilities.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 7 Modules Overview
st.markdown("## 📦 7 Integrated Modules")

modules = [
    {"icon": "🔍", "name": "RTT & Pathway Intelligence", "desc": "AI-powered RTT validation, breach prediction, pathway coordination"},
    {"icon": "🎗️", "name": "Cancer Pathway Management", "desc": "2WW/62-day tracking, cancer data management, MDT integration"},
    {"icon": "👥", "name": "MDT Coordination Suite", "desc": "Meeting scheduling, outcome recording, decision support"},
    {"icon": "📅", "name": "Intelligent Appointment System", "desc": "AI booking optimization, capacity planning, DNA prevention"},
    {"icon": "📧", "name": "Medical Secretary AI", "desc": "Letter generation, diary management, referral processing"},
    {"icon": "📊", "name": "Data Quality & Governance", "desc": "AI validation, audit trails, compliance monitoring"},
    {"icon": "🎓", "name": "Professional Training Academy", "desc": "188 scenarios, 15+ roles, AI tutoring, certification"}
]

cols = st.columns(2)
for idx, module in enumerate(modules):
    with cols[idx % 2]:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h4>{module['icon']} {module['name']}</h4>
            <p style="color: #666;">{module['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Company Information Footer
st.markdown("""
<div class="footer">
    <div style="text-align: center; margin-bottom: 30px;">
        <h2>🏢 T21 Services Limited</h2>
        <p style="font-size: 18px;">Healthcare Training & Technology Solutions</p>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;">
        <div>
            <h3>📍 Head Office</h3>
            <p>64 Upper Parliament Street<br>
            Liverpool, L8 7lf<br>
            England, L8 7LF</p>
            <p><strong>Company No:</strong> 13091053<br>
            <strong>Status:</strong> Active ✅<br>
            <strong>Incorporated:</strong> 18 December 2020</p>
        </div>
        
        <div>
            <h3>📞 Contact Us</h3>
            <p>
            📧 Email: <a href="mailto:info@t21services.com">info@t21services.com</a><br>
            📧 Support: <a href="mailto:support@t21services.com">support@t21services.com</a><br>
            📧 Sales: <a href="mailto:sales@t21services.com">sales@t21services.com</a><br>
            📞 Phone: [Your Phone Number]
            </p>
        </div>
        
        <div>
            <h3>🌐 Follow Us</h3>
            <p>
            💼 <a href="https://linkedin.com/company/t21-services" target="_blank">LinkedIn</a><br>
            🐦 <a href="https://twitter.com/t21services" target="_blank">Twitter/X</a><br>
            📘 <a href="https://facebook.com/t21services" target="_blank">Facebook</a><br>
            🌐 <a href="https://www.t21services.com" target="_blank">www.t21services.com</a>
            </p>
        </div>
        
        <div>
            <h3>📄 Legal</h3>
            <p>
            <a href="#">Privacy Policy</a><br>
            <a href="#">Terms of Service</a><br>
            <a href="#">Data Protection</a><br>
            <a href="#">GDPR Compliance</a>
            </p>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 30px; padding-top: 30px; border-top: 1px solid #555;">
        <p>© 2020-2025 T21 Services Limited. All rights reserved. Company registered in England and Wales.</p>
        <p style="font-size: 12px; color: #999;">T21 Healthcare Intelligence Platform is a registered product of T21 Services Limited.</p>
    </div>
</div>
""", unsafe_allow_html=True)
