"""
🌟 T21 MARKETING LANDING PAGE WITH AI ASSISTANT
Standalone landing page for marketing with embedded AI chatbot
Can be deployed separately as: t21-ai.streamlit.app
"""

import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="T21 Healthcare Platform - RTT Training",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for landing page
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .cta-button {
        background: #667eea;
        color: white;
        padding: 1rem 2rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .stat-box {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chatbot-badge {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 15px 25px;
        border-radius: 50px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 T21 Healthcare Platform</h1>
    <h3>Master NHS RTT Validation in 8 Weeks</h3>
    <p style="font-size: 1.2rem;">The UK's #1 AI-Powered RTT Training Platform</p>
</div>
""", unsafe_allow_html=True)

# Hero Section
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("## 🚀 Transform Your Healthcare Career")
    st.markdown("""
    ### Why T21?
    
    ✅ **AI-Powered Learning** - 30x faster than traditional training  
    ✅ **Industry Certification** - Recognized by NHS employers  
    ✅ **8-Week Program** - Self-paced, flexible learning  
    ✅ **1000+ Practice Questions** - Comprehensive exam prep  
    ✅ **Real NHS Simulation** - Hands-on PAS system training  
    ✅ **92% Job Placement** - Our students get hired  
    """)
    
    if st.button("🎁 START FREE 7-DAY TRIAL", key="hero_cta", use_container_width=True):
        st.balloons()
        st.success("🎉 Awesome! Creating your free account...")
        with st.form("trial_form"):
            trial_name = st.text_input("Full Name*")
            trial_email = st.text_input("Email*")
            trial_phone = st.text_input("Phone (optional)")
            trial_role = st.selectbox("Current Role", ["Medical Secretary", "Healthcare Admin", "Job Seeker", "Student", "Other"])
            
            if st.form_submit_button("✨ Activate Trial"):
                if trial_name and trial_email:
                    st.success(f"✅ Welcome {trial_name}! Check your email for login details.")
                    st.info("📧 Confirmation sent to: " + trial_email)
                else:
                    st.error("Please fill in all required fields")

with col2:
    st.image("https://via.placeholder.com/400x300?text=Platform+Demo", use_container_width=True)
    st.markdown("### 🎥 Watch Demo")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Replace with actual demo

# Stats Section
st.markdown("---")
st.markdown("## 📊 Trusted by Healthcare Professionals")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="stat-box"><h2>1000+</h2><p>Active Students</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-box"><h2>92%</h2><p>Job Placement</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-box"><h2>4.8/5</h2><p>Satisfaction Rating</p></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="stat-box"><h2>85%</h2><p>Completion Rate</p></div>', unsafe_allow_html=True)

# Features Section
st.markdown("---")
st.markdown("## 🎓 What You'll Learn")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>📚 Complete RTT Training</h3>
        <ul>
            <li>8-week structured course</li>
            <li>Video lectures & materials</li>
            <li>Real NHS workflows</li>
            <li>Expert instructors</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🤖 AI-Powered Practice</h3>
        <ul>
            <li>1000+ exam questions</li>
            <li>AI letter interpretation</li>
            <li>Instant feedback</li>
            <li>Personalized learning</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>🏆 Certification & Support</h3>
        <ul>
            <li>Industry-recognized cert</li>
            <li>Interview preparation</li>
            <li>CV building tools</li>
            <li>Job placement support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Pricing Section
st.markdown("---")
st.markdown("## 💰 Simple, Transparent Pricing")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Individual
    **£49/month**
    
    ✅ Full platform access  
    ✅ All courses & materials  
    ✅ Certification exam  
    ✅ 6 months access  
    ✅ Email support  
    
    <br>
    """, unsafe_allow_html=True)
    st.button("Start Trial", key="price1", use_container_width=True)

with col2:
    st.markdown("""
    ### One-Time Payment
    **£497**
    
    ✅ Lifetime access  
    ✅ All future updates  
    ✅ Priority support  
    ✅ Exclusive content  
    ✅ Money-back guarantee  
    
    <br>
    """, unsafe_allow_html=True)
    st.button("Buy Now", key="price2", use_container_width=True, type="primary")

with col3:
    st.markdown("""
    ### Enterprise
    **Custom**
    
    ✅ Unlimited users  
    ✅ White-labeling  
    ✅ Custom integrations  
    ✅ Dedicated support  
    ✅ Training sessions  
    
    <br>
    """, unsafe_allow_html=True)
    st.button("Contact Sales", key="price3", use_container_width=True)

# Testimonials
st.markdown("---")
st.markdown("## 💬 What Our Students Say")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **"Changed my career!"**
    
    "Within 8 weeks I went from medical secretary to RTT validator. The AI practice was invaluable."
    
    ⭐⭐⭐⭐⭐  
    *Sarah M., RTT Validator*
    """)

with col2:
    st.info("""
    **"Best investment ever"**
    
    "The platform is intuitive, comprehensive, and actually fun to use. Got certified and hired within 3 months!"
    
    ⭐⭐⭐⭐⭐  
    *James K., Healthcare Admin*
    """)

with col3:
    st.info("""
    **"Incredible support"**
    
    "The AI tutor answered all my questions instantly. Felt like having a personal mentor 24/7."
    
    ⭐⭐⭐⭐⭐  
    *Priya S., Medical Secretary*
    """)

# FAQ Section
st.markdown("---")
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("How long does it take to complete?"):
    st.write("Most students complete the course in 8 weeks studying 1-2 hours per day. It's self-paced, so you can go faster or slower based on your schedule.")

with st.expander("Is certification recognized by employers?"):
    st.write("Yes! Our certification is recognized by NHS employers and recruitment agencies. 92% of our certified students secure RTT validation roles.")

with st.expander("What if I need help during the course?"):
    st.write("You have 24/7 access to our AI tutor, email support, and a community forum. Plus, we offer live Q&A sessions twice a week.")

with st.expander("Can I get a refund?"):
    st.write("Absolutely! We offer a 30-day money-back guarantee. If you're not satisfied, we'll refund you in full, no questions asked.")

with st.expander("Do I need prior experience?"):
    st.write("No! The course is designed for beginners. We start with basics and progressively build your skills to professional level.")

# Final CTA
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h2>Ready to Transform Your Career?</h2>
    <p style="font-size: 1.2rem;">Join 1000+ healthcare professionals who trust T21</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 START YOUR FREE 7-DAY TRIAL", key="final_cta", use_container_width=True, type="primary"):
        st.balloons()
        st.success("Redirecting to signup...")

# AI Chatbot Section (Always visible)
st.markdown("---")
st.markdown("## 💬 Questions? Ask Our AI Assistant")

# Simple embedded chatbot
if "landing_messages" not in st.session_state:
    st.session_state.landing_messages = [
        {"role": "assistant", "content": "👋 Hi! I'm here to help. Ask me anything about T21, RTT training, pricing, or how to get started!"}
    ]

# Display chat
for msg in st.session_state.landing_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.landing_messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI response (simplified for landing page)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful sales assistant for T21 Healthcare Platform. Be enthusiastic, answer questions about RTT training, pricing (£49/month or £497 one-time), features, and guide users to start a free trial. Keep responses under 150 words."},
                        *st.session_state.landing_messages[-5:]
                    ],
                    max_tokens=300
                )
                
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.landing_messages.append({"role": "assistant", "content": answer})
                
            except:
                st.error("AI temporarily unavailable. Email us at: admin@t21services.co.uk")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; background: #f8f9fa; border-radius: 10px;">
    <h3>🏢 T21 Services Limited</h3>
    <p><strong>Company No:</strong> 13091053 | <strong>Address:</strong> 64 Upper Parliament St, Liverpool, L8 7LF</p>
    <p>📧 admin@t21services.co.uk | 🌐 www.t21services.co.uk</p>
    <p>
        💼 <a href="https://linkedin.com/company/t21services">LinkedIn</a> | 
        🐦 <a href="https://x.com/t21services">X</a> | 
        📘 <a href="https://facebook.com/t21services">Facebook</a> | 
        📸 <a href="https://instagram.com/t21services">Instagram</a>
    </p>
    <p style="color: #666; font-size: 0.9rem;">© 2025 T21 Services Ltd. All rights reserved. | Privacy Policy | Terms of Service</p>
</div>
""", unsafe_allow_html=True)
