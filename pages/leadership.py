"""
T21 SERVICES - LEADERSHIP PAGE
"""

import streamlit as st
from navigation import render_navigation


render_navigation(current_page="leadership")

st.title("Leadership Team")

st.markdown("---")
st.markdown("## 👔 Founder & Chief Executive Officer")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d4af37, #f4d03f); padding: 40px; border-radius: 15px; text-align: center;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>👨‍💼</div>
        <h2 style='color: #1a1a1a; margin: 0;'>Amb. Tosin Michael Owonifari</h2>
        <h3 style='color: #1a1a1a; margin: 10px 0; font-size: 18px;'>FCISM, BCS</h3>
        <p style='color: #1a1a1a; font-weight: 600; font-size: 16px;'>Founder & CEO | AU Agenda 2063 Ambassador</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### Professional Background
    
    **Amb. Tosin Michael Owonifari, FCISM** is the Founder and Chief Executive Officer of T21 Services (UK & Nigeria) and Executive Director of AU Gateway Global CIC. A visionary leader, technocrat, and training expert with extensive experience in digital transformation, skills development, and cross-continental program delivery.
    
    ### Key Roles & Achievements
    
    - 🌍 **African Union Agenda 2063 Ambassador** (UK – North West Region)
    - 🎓 **Fellow, Chartered Institute of Strategic Management (FCISM)**
    - 💻 **Member, British Computer Society (BCS)**
    - 🏥 **TQUK Approved Centre Director** - Centre No: 36257481088
    - 📋 **CPD Certification Approval** - RTT Validator & Hospital Administrative Training
    - 🏢 **Certiport Authorized Testing Centre Manager**
    - 🤝 **Former Consultant** - Leadership Training Partner, Liverpool Hope University
    
    ### Professional Qualifications
    
    - **Level 4 Award** - Internal Quality Assurance of Assessment Processes (RQF) – IAO
    - **Level 3 Certificate** - Assessing Vocational Achievement (RQF) – IAO
    - **Level 3 Award** - Education and Training (RQF) – IAO
    - **B.Sc. (Hons)** - Oil and Gas Management, University of Plymouth (2:1)
    - **Fellow (FCISM)** - Chartered Institute of Strategic Management
    - **Member (BCS)** - British Computer Society
    
    ### Vision & Mission
    
    Ambassador Owonifari founded T21 Services with a clear vision: to transform NHS workforce development through innovative training programs and cutting-edge technology solutions. His deep understanding of NHS challenges, combined with expertise in curriculum development and quality assurance, has positioned T21 Services as a leading provider of accredited healthcare training.
    
    ### Areas of Expertise
    
    **Training & Assessment:**
    - NHS Administrative Careers & RTT Validation
    - Internal Quality Assurance (IQA)
    - Curriculum Design & Assessment
    - Vocational Assessment & Portfolio Review
    - CPD-Approved Training Programs
    
    **Healthcare & Technology:**
    - Hospital Administration & Management
    - EPR/PAS Systems Training
    - AI-Powered Healthcare Automation
    - Cybersecurity Awareness
    - Data Protection & Compliance
    
    **Leadership & Development:**
    - Centre Management & Policy Implementation
    - Strategic Partnerships & International Relations
    - Diaspora & Civic Engagement
    - Youth Empowerment & Leadership Coaching
    - Remote Work Enablement
    
    ### Global Impact
    
    - Facilitated diaspora-led civic partnerships across UK councils under AU Agenda 2063
    - Led youth empowerment projects and leadership bootcamps with universities
    - Advancing access to international remote job markets for trained African talent
    - Developing multi-purpose training & remote work hub in Liverpool
    
    ### Contact
    
    📧 **Email:** t.owonifari@t21services.co.uk  
    📞 **Direct:** +44 7447 459420  
    📞 **Office:** +44 20 3375 2061  
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
