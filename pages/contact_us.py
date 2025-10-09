"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Contact Us Page

By T21 Services Limited
Company No: 13091053
"""

import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Contact Us | T21 Services Limited",
    page_icon="📧",
    layout="wide"
)

# Custom sidebar
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from sidebar_manager import render_sidebar
    render_sidebar()
except:
    pass

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 10px; margin-bottom: 30px; text-align: center;'>
    <h1 style='color: white; margin: 0;'>📧 Contact Us</h1>
    <p style='color: white; margin: 10px 0 0 0; font-size: 18px;'>We'd love to hear from you!</p>
</div>
""", unsafe_allow_html=True)

# Two column layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 💬 Send Us a Message")
    st.markdown("Fill out the form below and we'll get back to you within 24 hours (Monday-Friday)")
    
    with st.form("contact_form"):
        # Contact type
        contact_type = st.selectbox(
            "I am contacting as a:",
            [
                "NHS Organization (Book Demo)",
                "Student (Training Inquiry)",
                "Training Provider (Partnership)",
                "Existing Customer (Support)",
                "Media/Press Inquiry",
                "General Inquiry"
            ]
        )
        
        # Name
        full_name = st.text_input("Full Name *", placeholder="John Smith")
        
        # Email
        email = st.text_input("Email Address *", placeholder="john.smith@example.com")
        
        # Organization (optional)
        organization = st.text_input("Organization / NHS Trust (optional)", placeholder="Liverpool University Hospitals NHS Foundation Trust")
        
        # Phone (optional)
        phone = st.text_input("Phone Number (optional)", placeholder="+44 7XXX XXXXXX")
        
        # Subject
        subject = st.text_input("Subject *", placeholder="Interested in NHS Demo")
        
        # Message
        message = st.text_area(
            "Message *",
            placeholder="Tell us about your needs, questions, or feedback...",
            height=150
        )
        
        # How did you hear about us
        hear_about = st.selectbox(
            "How did you hear about us?",
            [
                "Select...",
                "Google Search",
                "LinkedIn",
                "Facebook",
                "NHS Colleague Recommendation",
                "Training Provider",
                "Conference/Event",
                "Other"
            ]
        )
        
        # Marketing consent
        marketing_consent = st.checkbox(
            "I would like to receive updates about T21 Services products and offers"
        )
        
        # Privacy consent
        privacy_consent = st.checkbox(
            "I agree to the Privacy Policy and Terms of Service *"
        )
        
        # Submit button
        submitted = st.form_submit_button("📨 Send Message", type="primary", use_container_width=True)
        
        if submitted:
            if not full_name or not email or not subject or not message:
                st.error("❌ Please fill in all required fields (*)")
            elif not privacy_consent:
                st.error("❌ You must agree to the Privacy Policy and Terms of Service")
            elif "@" not in email:
                st.error("❌ Please enter a valid email address")
            else:
                # Save contact form submission
                try:
                    # Create data directory if it doesn't exist
                    os.makedirs("data/contact_submissions", exist_ok=True)
                    
                    # Create submission record
                    submission = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "contact_type": contact_type,
                        "full_name": full_name,
                        "email": email,
                        "organization": organization,
                        "phone": phone,
                        "subject": subject,
                        "message": message,
                        "hear_about": hear_about,
                        "marketing_consent": marketing_consent,
                        "privacy_consent": privacy_consent
                    }
                    
                    # Save to JSON file
                    filename = f"data/contact_submissions/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{email.replace('@', '_at_')}.json"
                    with open(filename, 'w') as f:
                        json.dump(submission, f, indent=2)
                    
                    # Success message
                    st.success("✅ **Message Sent Successfully!**")
                    st.balloons()
                    st.info(f"""
                    Thank you for contacting T21 Services, {full_name}!
                    
                    We've received your message and will respond within 24 hours (Monday-Friday).
                    
                    **What happens next:**
                    - You'll receive a confirmation email at {email}
                    - Our team will review your inquiry
                    - We'll get back to you with next steps
                    
                    **For urgent matters:** Call [Your Phone Number] or email support@t21services.co.uk
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Error submitting form. Please email us directly at info@t21services.co.uk")

with col2:
    st.markdown("## 📍 Contact Information")
    
    # Company Info
    st.markdown("""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>🏢 T21 Services Limited</h4>
        <p style='margin: 5px 0; color: #666;'>
        <strong>Company No:</strong> 13091053<br>
        <strong>Status:</strong> Active ✅<br>
        <strong>Incorporated:</strong> 18 Dec 2020
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Head Office
    st.markdown("""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>📍 Head Office</h4>
        <p style='margin: 5px 0; color: #666;'>
        64 Upper Parliament Street<br>
        Liverpool, L8 7LF<br>
        England, United Kingdom 🇬🇧
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Email
    st.markdown("""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>📧 Email Us</h4>
        <p style='margin: 5px 0;'>
        <strong>General:</strong><br>
        <a href='mailto:info@t21services.co.uk'>info@t21services.co.uk</a><br><br>
        
        <strong>Support:</strong><br>
        <a href='mailto:support@t21services.co.uk'>support@t21services.co.uk</a><br><br>
        
        <strong>Sales (NHS):</strong><br>
        <a href='mailto:sales@t21services.co.uk'>sales@t21services.co.uk</a><br><br>
        
        <strong>Student Support:</strong><br>
        <a href='mailto:student-support@t21services.co.uk'>student-support@t21services.co.uk</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Social Media
    st.markdown("""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>🌐 Follow Us</h4>
        <p style='margin: 5px 0;'>
        💼 <a href='https://linkedin.com/company/t21services' target='_blank'>LinkedIn</a><br>
        🐦 <a href='https://x.com/t21services' target='_blank'>X (Twitter)</a><br>
        📘 <a href='https://facebook.com/t21services' target='_blank'>Facebook</a><br>
        📸 <a href='https://instagram.com/t21services' target='_blank'>Instagram</a><br>
        🎵 <a href='https://tiktok.com/@t21services' target='_blank'>TikTok</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Website
    st.markdown("""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4 style='margin-top: 0;'>🌐 Website</h4>
        <p style='margin: 5px 0;'>
        <a href='https://www.t21services.co.uk' target='_blank'>www.t21services.co.uk</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Office Hours
    st.markdown("""
    <div style='background: #e3f2fd; padding: 20px; border-radius: 10px;'>
        <h4 style='margin-top: 0;'>🕐 Office Hours</h4>
        <p style='margin: 5px 0; color: #666;'>
        <strong>Monday - Friday:</strong><br>
        9:00 AM - 5:00 PM GMT<br><br>
        
        <strong>Saturday - Sunday:</strong><br>
        Closed<br><br>
        
        <em>24/7 platform support available</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# FAQ Section
st.markdown("## ❓ Frequently Asked Questions")

faq_col1, faq_col2 = st.columns(2)

with faq_col1:
    with st.expander("🏥 How do I book an NHS demo?"):
        st.markdown("""
        **For NHS Organizations:**
        1. Select "NHS Organization" in the contact form
        2. Tell us about your trust and needs
        3. We'll schedule a personalized demo
        4. See the platform in action (30-60 minutes)
        5. Discuss pricing and implementation
        
        **Or email:** sales@t21services.co.uk
        """)
    
    with st.expander("🎓 How do I sign up as a student?"):
        st.markdown("""
        **For Students:**
        1. Click "Student Portal" on the home page
        2. Register for free 48-hour trial
        3. Explore 188 training scenarios
        4. Upgrade to full access (£299-999)
        
        **Need help?** Email student-support@t21services.co.uk
        """)
    
    with st.expander("💰 What are your pricing options?"):
        st.markdown("""
        **For Students:**
        - Free 48-hour trial
        - Basic: £299 / 3 months
        - Professional: £599 / 6 months
        - Premium: £999 / 12 months
        
        **For NHS Organizations:**
        - Custom pricing based on trust size
        - Typical: £100k-300k per year
        - Contact us for quote
        """)

with faq_col2:
    with st.expander("🤝 How do I become a training partner?"):
        st.markdown("""
        **For Training Providers:**
        1. Select "Training Provider" in contact form
        2. Tell us about your organization
        3. We'll discuss partnership opportunities
        4. White-label options available
        5. Revenue share models
        
        **Or email:** sales@t21services.co.uk
        """)
    
    with st.expander("🔒 Is my data secure?"):
        st.markdown("""
        **Yes! We are:**
        - 🇬🇧 UK GDPR compliant
        - 🏥 NHS Data Security Toolkit compliant
        - 🔒 256-bit SSL/TLS encryption
        - ✅ Regular security audits
        
        Read our **Privacy Policy** for details.
        """)
    
    with st.expander("🚀 How quickly can we get started?"):
        st.markdown("""
        **Timeline:**
        - **Students:** Instant (register now!)
        - **NHS Organizations:** 2-4 weeks
          - Week 1: Demo & contract
          - Week 2: Setup & integration
          - Week 3: Training
          - Week 4: Go live!
        
        **Fast-track available for urgent needs**
        """)

st.markdown("---")

# Back button
if st.button("← Back to Home"):
    st.switch_page("landing_page.py")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>T21 Services Limited</strong> | Company No: 13091053 | Liverpool, England</p>
    <p>📧 info@t21services.co.uk | 🌐 www.t21services.co.uk</p>
    <p style='font-size: 12px; margin-top: 10px;'>© 2020-2025 T21 Services Limited. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
