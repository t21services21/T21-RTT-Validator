"""
T21 SERVICES - PROFESSIONAL LANDING PAGE
"""

import streamlit as st

def render_clean_landing_page():
    """Professional landing page with hero image"""
    
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        header[data-testid="stHeader"] {display: none;}
        .main .block-container {padding: 0; margin-top: -80px; max-width: 100%;}
        
        .top-nav {
            background: #1a1a1a;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: -5rem -5rem 0 -5rem;
        }
        .logo {font-size: 24px; font-weight: 800; color: #d4af37; text-transform: uppercase;}
        
        .hero-section {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920') center/cover;
            padding: 45px 40px 50px;
            margin: 0 -5rem;
            color: white;
        }
        .hero-section h1 {
            color: white; 
            font-size: 56px; 
            font-weight: 800; 
            margin: 0 0 12px 0; 
            line-height: 1.1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .hero-section h2 {
            color: #d4af37; 
            font-size: 36px; 
            font-weight: 700; 
            margin: 0 0 20px 0; 
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .hero-section p {
            font-size: 16px; 
            max-width: 850px; 
            margin: 0;
            line-height: 1.6;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
        }
    </style>
    
    <div class="top-nav">
        <span class="logo">T21 SERVICES</span>
        <a href="#login" style="background: linear-gradient(135deg, #d4af37, #f4d03f); color: #1a1a1a; padding: 10px 30px; border-radius: 25px; font-weight: 800; text-decoration: none; text-transform: uppercase; font-size: 14px; cursor: pointer;" onclick="document.getElementById('login').scrollIntoView({behavior: 'smooth'});">LOGIN / REGISTER</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown('<div style="background: #1a1a1a; padding: 10px 40px; margin: 0 -5rem;">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        if st.button("📋 ABOUT", key="nav_about", use_container_width=True):
            st.switch_page("pages/about.py")
    with c2:
        if st.button("🛠️ SERVICES", key="nav_services", use_container_width=True):
            st.switch_page("pages/services.py")
    with c3:
        if st.button("💰 PRICING", key="nav_pricing", use_container_width=True):
            st.switch_page("pages/pricing.py")
    with c4:
        if st.button("📞 CONTACT", key="nav_contact", use_container_width=True):
            st.switch_page("pages/contact_us.py")
    with c5:
        if st.button("🏠 HOME", key="nav_home", use_container_width=True, type="primary"):
            st.switch_page("app.py")
    with c6:
        if st.button("🏛️ PROCUREMENT", key="nav_procurement", use_container_width=True):
            st.switch_page("pages/procurement.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <h1>Your NHS Career & Workforce Partner</h1>
        <h2>Training • Talent • Technology</h2>
        <p><strong>COMPLETE NHS SOLUTION:</strong> Train individuals seeking NHS careers + Upskill existing NHS staff with TQUK-endorsed professional development • Supply qualified talent to NHS trusts • AI automation saving £2M+ per trust. 120x faster validation • 99.9% accuracy • Zero breaches. Training, talent supply, and technology transformation - your one-stop NHS workforce solution.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div id="login"></div>', unsafe_allow_html=True)
    st.markdown("### 🔐 Login or Register")
    st.markdown("*Select your portal to access the platform*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎓 STUDENT LOGIN / REGISTER", use_container_width=True, type="primary"):
            st.switch_page("pages/student_login.py")
    with col2:
        if st.button("👥 STAFF LOGIN / REGISTER", use_container_width=True, type="primary"):
            st.switch_page("pages/staff_login.py")
    with col3:
        if st.button("🏥 NHS LOGIN / REGISTER", use_container_width=True, type="primary"):
            st.switch_page("pages/nhs_login.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Revolutionary capabilities
    st.markdown("""
    <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-top: 3rem;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">🤖 AI-POWERED<br>AUTOMATION</div>
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">⚡ 120x FASTER<br>THAN MANUAL</div>
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">💰 £2M+ SAVINGS<br>PER TRUST</div>
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">✅ 99.9%<br>ACCURACY</div>
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">🏆 TQUK-ENDORSED<br>COURSE (PDLC-01-039)</div>
        <div style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; font-weight: 700; font-size: 0.9rem; color: white;">🚀 FUTURE-PROOF<br>100 YEARS</div>
    </div>
    """, unsafe_allow_html=True)
    
    # COMPREHENSIVE FEATURES SECTION
    st.markdown("---")
    st.markdown("## 🚀 Complete NHS Platform - 35+ Integrated Modules")
    st.markdown("*Everything you need for NHS operations, training, and workforce management*")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎓 Training & Professional Development
        - **TQUK-Endorsed Course** (PDLC-01-039)
        - 500+ RTT Training Scenarios
        - Interactive Learning Center
        - AI RTT Tutor with Trust-specific context ⭐ NEW!
        - Information Governance Training
        - Career Development Tools
        - CV Builder & Interview Prep
        - TQUK-Recognized Certificates
        
        ### 🏥 Patient Management
        - Patient Registration System
        - NHS Number Auto-Generation
        - Pathway Management (RTT, Cancer, Custom)
        - Episode Management & Tracking
        - DNA (Did Not Attend) Management
        - Transfer of Care System
        - Patient Choice Module
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Operational Systems
        - Patient Tracking List (PTL)
        - Partial Booking List (PBL) with Data Cleansing
        - Advanced Booking System
        - Waiting List Management
        - Cancer Pathway Tracker (62-day, 31-day, 2WW)
        - MDT Coordination & Meeting Management
        - Breach Risk Monitoring
        - Consent Manager
        - Funding/IFR Management
        
        ### 🤖 AI & Automation
        - AI Auto-Validator (500,000x faster)
        - Medical Secretary AI
        - Clinical Letter Generation
        - Clinic Letter Interpreter
        - Policy/SOP Generator ⭐ NEW!
        - Handwriting OCR
        - Document Management
        """)
    
    with col3:
        st.markdown("""
        ### 📈 Analytics & Reporting
        - Executive Dashboard
        - Pathway Statistics
        - AI Query Analytics Dashboard ⭐ NEW!
        - Data Quality System
        - Interactive Reports
        - Breach Analytics
        - Performance Metrics
        
        ### ⚙️ Administration & Settings
        - Trust AI Customization ⭐ NEW!
        - Multi-User Management
        - Role-Based Access Control
        - 2FA Security
        - Trial Management
        - Module Access Control
        - Admin Panel
        
        ### 🔒 Compliance & Security
        - Information Governance Module
        - GDPR Compliance
        - NHS Caldicott Principles
        - Data Breach Reporting
        - Audit Trail Logging
        """)
    
    st.markdown("---")
    st.markdown("### ⭐ NEW COMPETITIVE FEATURES (Added October 2025)")
    
    feature_cols = st.columns(3)
    with feature_cols[0]:
        st.success("""
        **🏥 Trust AI Customization**
        
        Upload your Trust's policies and train AI on your specific workflows - just like Sigma!
        
        ✅ Trust-specific responses
        ✅ Policy document upload
        ✅ Custom AI training
        """)
    
    with feature_cols[1]:
        st.success("""
        **📊 AI Analytics Dashboard**
        
        Track AI performance, user satisfaction, and system improvements.
        
        ✅ Query tracking
        ✅ Response metrics
        ✅ User feedback analysis
        """)
    
    with feature_cols[2]:
        st.success("""
        **📋 Policy/SOP Generator**
        
        Automatically generate RTT policies, SOPs, and procedures.
        
        ✅ NHS-compliant templates
        ✅ Trust-customizable
        ✅ Downloadable documents
        """)
    
    st.markdown("---")
    
    # ============================================
    # PUBLIC AI CHATBOT - LEAD GENERATION
    # ============================================
    st.markdown("## 💬 Questions? Ask Our AI Assistant!")
    st.info("🚀 Get instant answers about our training, pricing, features, and career opportunities!")
    
    # Initialize chat history
    if "public_ai_chat" not in st.session_state:
        st.session_state.public_ai_chat = [
            {
                "role": "assistant",
                "content": "👋 **Welcome to T21 Healthcare Platform!**\n\n"
                          "I can help you with:\n"
                          "💰 **Pricing** - 4 tiers from £99 to £1,799\n"
                          "📚 **Courses** - 8-week TQUK-endorsed training\n"
                          "🎓 **Certification** - Industry-recognized qualifications\n"
                          "💼 **Careers** - 20+ NHS roles (£25k-£55k)\n"
                          "🏥 **NHS Solutions** - Trust-wide deployments\n\n"
                          "**What would you like to know?**"
            }
        ]
    
    # Display messages
    for msg in st.session_state.public_ai_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if user_q := st.chat_input("Type your question here..."):
        st.session_state.public_ai_chat.append({"role": "user", "content": user_q})
        
        with st.chat_message("user"):
            st.markdown(user_q)
        
        with st.chat_message("assistant"):
            with st.spinner("✨ Thinking..."):
                try:
                    from openai import OpenAI
                    from COMPLETE_PLATFORM_KNOWLEDGE import COMPLETE_PLATFORM_KNOWLEDGE
                    import json
                    
                    client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
                    
                    sys_prompt = f"""You are an enthusiastic sales AI for T21 Healthcare Platform.

COMPLETE INFO:
{json.dumps(COMPLETE_PLATFORM_KNOWLEDGE, indent=2)}

SALES TACTICS:
1. Highlight value: "£5,000+ value for £1,299"
2. Create urgency: "Limited 30 spots/month", "Price increase April 2026 (+£200)"
3. Add bonuses: "£300 FREE bonuses now!"
4. Social proof: "Sarah: secretary £24k → coordinator £34k (8 weeks)"
5. ROI: "92% get jobs within 3 months"
6. Show 20+ career paths (not just secretary!)
7. End with CTA

PRICING:
- Taster: £99/1 month
- Tier 1: £499/6 months (full access, no cert)
- Tier 2: £1,299/12 months (TQUK cert) ⭐ MOST POPULAR
- Tier 3: £1,799/12 months (cert + career coach)
- NHS Trust: Custom

Direct them to click LOGIN/REGISTER button above to enroll!
Keep under 200 words unless detailed explanation needed."""
                    
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": sys_prompt},
                            *st.session_state.public_ai_chat[-6:]
                        ],
                        max_tokens=400,
                        temperature=0.7
                    )
                    
                    ai_answer = resp.choices[0].message.content
                    st.markdown(ai_answer)
                    st.session_state.public_ai_chat.append({"role": "assistant", "content": ai_answer})
                    
                except Exception as e:
                    err = "AI temporarily unavailable. Email: admin@t21services.co.uk or click LOGIN/REGISTER above!"
                    st.error(err)
                    st.session_state.public_ai_chat.append({"role": "assistant", "content": err})
    
    # Quick buttons
    st.markdown("**Quick Questions:**")
    q1, q2, q3 = st.columns(3)
    
    with q1:
        if st.button("💰 Pricing", key="q_price"):
            st.session_state.public_ai_chat.append({"role": "user", "content": "How much does it cost?"})
            st.rerun()
    
    with q2:
        if st.button("🎓 Careers", key="q_career"):
            st.session_state.public_ai_chat.append({"role": "user", "content": "What career paths are available?"})
            st.rerun()
    
    with q3:
        if st.button("⏱️ Duration", key="q_time"):
            st.session_state.public_ai_chat.append({"role": "user", "content": "How long does training take?"})
            st.rerun()
    
    st.markdown("---")
