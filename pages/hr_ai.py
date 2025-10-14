"""
T21 HR AI - Complete HR Automation
"""

import streamlit as st

st.set_page_config(page_title="HR AI", page_icon="👥", layout="wide")

st.title("👥 HR AI")
st.markdown("### Payroll, recruitment, performance tracking - Save £1.4 BILLION/year!")

tab1, tab2 = st.tabs(["👥 Features", "ℹ️ About"])

with tab1:
    st.header("👥 HR AI Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Payroll Automation")
        st.info("Automated salary calculations and payments")
        
        st.subheader("✅ Recruitment")
        st.info("AI-powered candidate screening")
        
        st.subheader("✅ Onboarding")
        st.info("Automated new starter processes")
        
        st.subheader("✅ Leave Management")
        st.info("Automated leave requests and approvals")
        
        st.subheader("✅ Performance Tracking")
        st.info("Monitor staff performance metrics")
    
    with col2:
        st.subheader("✅ Training Management")
        st.info("Track mandatory training compliance")
        
        st.subheader("✅ Rota Management")
        st.info("Intelligent staff scheduling")
        
        st.subheader("✅ Compliance")
        st.info("Ensure HR policy compliance")
        
        st.subheader("✅ Analytics")
        st.info("Workforce analytics and insights")
        
        st.subheader("✅ Employee Portal")
        st.info("Self-service for staff")

with tab2:
    st.header("ℹ️ About HR AI")
    st.markdown("""
    ### 💰 Business Impact:
    - Market: 30,000 HR staff
    - Cost: £46,667/year per staff
    - Total: £1.4 BILLION/year
    - Automation: 75%
    - Savings: £1.05 BILLION/year
    
    ### 🚀 10 Features:
    1. Payroll automation
    2. Recruitment automation
    3. Onboarding automation
    4. Leave management
    5. Performance tracking
    6. Training management
    7. Rota management
    8. Compliance checking
    9. Workforce analytics
    10. Employee self-service
    """)

st.markdown("---")
st.caption("© 2025 T21 Services Limited | HR AI v1.0")
