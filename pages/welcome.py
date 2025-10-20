"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Welcome / Landing Page
"""

import streamlit as st
import sys
import os

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Custom sidebar
try:
    from sidebar_manager import render_sidebar
    render_sidebar()
except:
    pass

# Hero Section
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 60px 20px; 
            border-radius: 15px; 
            text-align: center; 
            color: white; 
            margin-bottom: 40px;'>
    <h1 style='font-size: 48px; margin: 0;'>🏥 T21 Healthcare Intelligence Platform</h1>
    <p style='font-size: 24px; margin: 20px 0 0 0;'>Complete NHS Healthcare Administration Training & Operations Suite</p>
    <p style='font-size: 18px; margin: 10px 0 0 0; opacity: 0.9;'>Training + Automation | AI-Powered | 188 Scenarios</p>
</div>
""", unsafe_allow_html=True)

# Check if logged in
is_logged_in = st.session_state.get('logged_in', False)

if not is_logged_in:
    # NOT LOGGED IN - Show marketing content
    st.markdown("## 🎯 Transform Your NHS Career")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎓 TQUK Certified
        **Official Qualification**
        - Ofqual-regulated
        - NHS-recognized
        - 8-week program
        - Industry standard
        """)
    
    with col2:
        st.markdown("""
        ### 🏥 Hands-On Practice
        **Real Clinical Tools**
        - RTT Clinical Validator
        - Pathway Management
        - Appointment Systems
        - Live scenarios
        """)
    
    with col3:
        st.markdown("""
        ### 🤖 AI-Powered
        **24/7 Learning**
        - Unlimited AI tutor
        - Interactive scenarios
        - Instant feedback
        - Modern platform
        """)
    
    st.markdown("---")
    
    # Pricing Teasers
    st.markdown("## 💰 Choose Your Plan")
    
    pricing_col1, pricing_col2, pricing_col3, pricing_col4 = st.columns(4)
    
    with pricing_col1:
        st.info("""
        ### 💰 Taster
        **£99 / 1 Month**
        
        ✅ Try platform
        ✅ AI tutor (10/day)
        ✅ Sample scenarios
        ❌ No certification
        
        **Perfect for testing!**
        """)
    
    with pricing_col2:
        st.success("""
        ### ⭐ Full Access
        **£499 / 6 Months**
        
        ✅ Unlimited AI tutor
        ✅ All hands-on tools
        ✅ Full scenarios
        ❌ No certification
        
        **Best for practice!**
        """)
    
    with pricing_col3:
        st.warning("""
        ### 🏆 Certified
        **£1,299 / 12 Months**
        
        ✅ TQUK Certification
        ✅ Live tutors
        ✅ Alumni network
        ✅ Basic job support
        
        **Get qualified!**
        """)
    
    with pricing_col4:
        st.error("""
        ### 💎 Premium
        **£1,799 / 12 Months**
        
        ✅ Everything in Tier 3
        ✅ **Staff applies for jobs FOR you**
        ✅ **We get you interviews**
        ✅ Job application support
        
        **Get hired faster!**
        """)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("""
    <div style='background: #f0f2f6; padding: 30px; border-radius: 10px; text-align: center;'>
        <h2>🚀 Ready to Start Your NHS Career?</h2>
        <p style='font-size: 18px;'>Login to access the platform or contact us for more information</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Login buttons (centered)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col2:
        if st.button("🎓 Student Login", use_container_width=True, type="primary"):
            st.switch_page("pages/student_login.py")
    
    with col3:
        if st.button("👥 Staff Login", use_container_width=True):
            st.switch_page("pages/staff_login.py")
    
    with col4:
        if st.button("🏥 NHS Login", use_container_width=True):
            st.switch_page("pages/nhs_login.py")

else:
    # LOGGED IN - Redirect to dashboard
    st.info("Redirecting to dashboard...")
    st.switch_page("app.py")

# ============================================
# FLOATING AI CHATBOT (For public homepage)
# ============================================
if not is_logged_in:
    st.markdown("---")
    st.markdown("## 💬 Questions? Ask Our AI Assistant!")
    st.info("Get instant answers about our training, pricing, features, and more!")
    
    # Initialize chat history for public AI
    if "public_ai_messages" not in st.session_state:
        st.session_state.public_ai_messages = [
            {
                "role": "assistant",
                "content": "👋 **Welcome to T21!** I'm your AI assistant.\n\n"
                          "Ask me about:\n"
                          "💰 Pricing and payment options\n"
                          "📚 Courses and training content\n"
                          "🎓 Certification and qualifications\n"
                          "💼 Career opportunities (20+ NHS roles!)\n"
                          "🏥 NHS Trust solutions\n\n"
                          "What would you like to know?"
            }
        ]
    
    # Display chat messages
    for message in st.session_state.public_ai_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask anything about T21..."):
        # Add user message
        st.session_state.public_ai_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("✨ Thinking..."):
                try:
                    from openai import OpenAI
                    from COMPLETE_PLATFORM_KNOWLEDGE import COMPLETE_PLATFORM_KNOWLEDGE
                    import json
                    
                    client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
                    
                    system_prompt = f"""You are an enthusiastic sales AI for T21 Healthcare Platform.
                    
COMPLETE PLATFORM INFO:
{json.dumps(COMPLETE_PLATFORM_KNOWLEDGE, indent=2)}

INSTRUCTIONS:
1. Be enthusiastic and helpful
2. Use the COMPLETE_PLATFORM_KNOWLEDGE for accurate answers
3. Highlight value: "£5,000+ value for £1,299" for Tier 2
4. Mention urgency: "Limited spots (30/month for Tier 2)", "Price increase April 2026"
5. Add bonuses: "£300 in FREE bonuses right now!"
6. Use social proof: "Sarah (secretary £24k → coordinator £34k in 8 weeks)"
7. Show ROI: "92% get jobs within 3 months"
8. Mention 20+ career paths (not just secretary!)
9. End with CTA: "Ready to start?" or "Want to enroll?"
10. Keep under 200 words unless detailed explanation needed

PRICING (ACCURATE):
- Taster: £99 / 1 month
- Tier 1: £499 / 6 months (full access, no cert)
- Tier 2: £1,299 / 12 months (TQUK cert) - MOST POPULAR
- Tier 3: £1,799 / 12 months (cert + career coach)
- NHS Trust: Custom pricing

If user wants to enroll, guide them to click "Student Login" button above to register!"""
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.public_ai_messages[-6:]
                        ],
                        max_tokens=400,
                        temperature=0.7
                    )
                    
                    answer = response.choices[0].message.content
                    st.markdown(answer)
                    st.session_state.public_ai_messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    error_msg = f"AI temporarily unavailable. Please email admin@t21services.co.uk or click Student Login to register!"
                    st.error(error_msg)
                    st.session_state.public_ai_messages.append({"role": "assistant", "content": error_msg})
    
    # Quick action buttons
    st.markdown("---")
    st.markdown("**Quick Questions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 How much?", key="quick_price"):
            st.session_state.public_ai_messages.append({"role": "user", "content": "How much does it cost?"})
            st.rerun()
    
    with col2:
        if st.button("🎓 What careers?", key="quick_career"):
            st.session_state.public_ai_messages.append({"role": "user", "content": "What career paths are available?"})
            st.rerun()
    
    with col3:
        if st.button("⏱️ How long?", key="quick_time"):
            st.session_state.public_ai_messages.append({"role": "user", "content": "How long does it take?"})
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>T21 Services Limited</strong> | Company No: 13091053 | Liverpool, England</p>
    <p>🌐 www.t21services.co.uk | 📧 info@t21services.co.uk</p>
    <p>Trusted by NHS Trusts, Training Providers, and Healthcare Professionals</p>
</div>
""", unsafe_allow_html=True)
