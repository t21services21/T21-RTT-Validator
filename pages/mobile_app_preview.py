"""
T21 HEALTHCARE PLATFORM - MOBILE APP PREVIEW
Demonstration of mobile capabilities coming soon
"""

import streamlit as st
from navigation import render_navigation
from datetime import datetime

st.set_page_config(page_title="Mobile App | T21 Services", page_icon="📱", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="mobile")

st.title("📱 T21 Mobile App - Coming Soon!")
st.markdown("**RTT management on-the-go - iOS & Android**")

# Mobile mockup
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 30px; color: white; text-align: center;">
        <h1 style="color: white; margin: 0;">📱</h1>
        <h2 style="color: white;">T21 Mobile App</h2>
        <p style="font-size: 18px;">Manage RTT pathways from your phone</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features showcase
    st.markdown("### 🌟 Mobile App Features")
    
    features = [
        ("⚡ **Instant Validation**", "Validate pathways in 5 seconds from phone"),
        ("🔔 **Push Notifications**", "Real-time breach alerts wherever you are"),
        ("📊 **Live Dashboard**", "Monitor performance on mobile device"),
        ("📸 **Photo Upload**", "Scan clinic letters with camera"),
        ("🎤 **Voice Commands**", "Say 'Validate NHS 1234567890' - done!"),
        ("📍 **Location Alerts**", "Notify on-call staff automatically"),
        ("💬 **Team Chat**", "Instant messaging with RTT team"),
        ("🔐 **Biometric Login**", "Face ID / Fingerprint security")
    ]
    
    for title, desc in features:
        st.markdown(f"""
        <div style="background: white; padding: 20px; margin: 10px 0; border-radius: 10px; border-left: 5px solid #667eea;">
            <strong style="font-size: 18px;">{title}</strong>
            <p style="margin: 5px 0 0 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Demo simulation
    st.markdown("### 📲 Try the Mobile Experience (Demo)")
    
    if st.button("🚀 Launch Mobile Demo", type="primary", use_container_width=True):
        st.success("📱 Mobile app launched!")
        st.balloons()
        
        # Simulated mobile interface
        st.markdown("""
        <div style="background: #f0f2f6; padding: 30px; border-radius: 20px; max-width: 400px; margin: 20px auto;">
            <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin: 0 0 15px 0;">📊 Today's Overview</h3>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <div style="text-align: center;">
                        <div style="font-size: 32px; font-weight: bold; color: #667eea;">245</div>
                        <div style="font-size: 12px; color: #666;">Active Patients</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 32px; font-weight: bold; color: #f5576c;">12</div>
                        <div style="font-size: 12px; color: #666;">At Risk</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 32px; font-weight: bold; color: #43e97b;">92%</div>
                        <div style="font-size: 12px; color: #666;">Compliant</div>
                    </div>
                </div>
                <hr>
                <div style="margin-top: 15px;">
                    <div style="background: #fff3cd; padding: 10px; border-radius: 8px; margin: 5px 0;">
                        <strong>🔔 Alert:</strong> 3 patients approaching 18 weeks
                    </div>
                    <div style="background: #d4edda; padding: 10px; border-radius: 8px; margin: 5px 0;">
                        <strong>✅ Success:</strong> 15 pathways validated today
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Download section
st.markdown("---")
st.markdown("### 📥 Get Early Access")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    <div style="background: #000; color: white; padding: 30px; border-radius: 15px; text-align: center;">
        <h2 style="color: white; margin: 0;">🍎 iOS App</h2>
        <p>iPhone & iPad</p>
        <button style="background: white; color: black; padding: 15px 40px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer;">
            Coming to App Store
        </button>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; text-align: center;">
        <h2 style="color: white; margin: 0;">🤖 Android App</h2>
        <p>All Android devices</p>
        <button style="background: white; color: #764ba2; padding: 15px 40px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer;">
            Coming to Google Play
        </button>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Beta signup
st.markdown("### 🎯 Join Beta Testing Program")

with st.form("beta_signup"):
    name = st.text_input("Your Name")
    email = st.text_input("Email Address")
    organization = st.text_input("NHS Trust/Organization")
    device = st.radio("Preferred Device", ["iOS (iPhone/iPad)", "Android", "Both"])
    
    if st.form_submit_button("🚀 Sign Up for Beta", type="primary", use_container_width=True):
        st.success("✅ You're on the list! We'll notify you when mobile app launches.")
        st.balloons()

st.markdown("---")
st.info("""
💡 **Beta Launch:** Q2 2025  
📱 **Platforms:** iOS 14+, Android 10+  
🔐 **Security:** Biometric authentication, end-to-end encryption  
⚡ **Performance:** Optimized for 5G networks
""")
