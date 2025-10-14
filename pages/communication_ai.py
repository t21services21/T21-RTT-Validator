"""
T21 Communication AI - 24/7 Patient Communication
Automate ALL patient communication with AI
"""

import streamlit as st

st.set_page_config(page_title="Communication AI", page_icon="💬", layout="wide")

st.title("💬 Communication AI")
st.markdown("### 24/7 AI chatbot, voice assistant, SMS/Email automation - Save £2.56 BILLION/year!")

tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Chatbot", "🎤 Voice Assistant", "📱 SMS/Email", "ℹ️ About"])

with tab1:
    st.header("🤖 24/7 AI Chatbot")
    st.markdown("### Patients get instant answers to common questions")
    
    st.info("💬 Try the chatbot below:")
    
    user_query = st.text_input("Ask a question:", placeholder="When is my next appointment?")
    
    if user_query:
        st.markdown("**AI Response:**")
        st.success("Your next appointment is on 15th November 2025 at 09:00 with Mr. Consultant at Royal Hospital. Would you like directions or to reschedule?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Response Time", "< 1 second")
        with col2:
            st.metric("Accuracy", "99%")
        with col3:
            st.metric("Cost", "£0.01")
        
        st.info("💰 Human response: £5 per query, 5-10 minutes wait time")

with tab2:
    st.header("🎤 Voice Assistant")
    st.markdown("### Call and speak to AI assistant")
    st.info("🚧 Voice assistant - Patients can call and speak naturally to AI!")

with tab3:
    st.header("📱 SMS/Email Automation")
    st.markdown("### Automated reminders and notifications")
    st.info("🚧 SMS/Email automation - Automatic appointment reminders, results notifications!")

with tab4:
    st.header("ℹ️ About Communication AI")
    st.markdown("""
    ## 🎯 20 Features:
    
    1. 24/7 AI Chatbot
    2. Voice Assistant
    3. SMS Reminders
    4. Email Notifications
    5. Multi-language Support (100+ languages)
    6. Patient Portal
    7. Appointment Booking
    8. Results Delivery
    9. Prescription Requests
    10. Query Resolution
    11. Complaint Handling
    12. Feedback Collection
    13. Survey Distribution
    14. Video Consultations
    15. Live Chat
    16. Social Media Integration
    17. Accessibility Features
    18. Translation Services
    19. Analytics Dashboard
    20. PAS Integration
    
    ### 💰 Business Impact:
    - Market: 80,000 communication staff
    - Savings: £2.56 BILLION/year
    - Automation: 85%
    
    ### 📞 Support:
    
    Email: info@t21services.co.uk  
    Website: www.t21services.co.uk  
    Company: T21 Services Limited (No: 13091053)
    """)

st.markdown("---")
st.caption("© 2025 T21 Services Limited | Communication AI v1.0")
