"""
T21 Finance AI - Complete Financial Automation
"""

import streamlit as st

st.set_page_config(page_title="Finance AI", page_icon="💰", layout="wide")

st.title("💰 Finance AI")
st.markdown("### Auto-invoicing, payment processing, fraud detection - Save £1.96 BILLION/year!")

tab1, tab2 = st.tabs(["💰 Features", "ℹ️ About"])

with tab1:
    st.header("💰 Finance AI Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Invoicing")
        st.info("Auto-generate invoices from treatment records")
        
        st.subheader("✅ Payment Processing")
        st.info("Automated payment collection and reconciliation")
        
        st.subheader("✅ Fraud Detection")
        st.info("AI detects suspicious transactions")
        
        st.subheader("✅ Budget Tracking")
        st.info("Real-time budget monitoring")
        
        st.subheader("✅ Financial Reporting")
        st.info("Auto-generate financial reports")
    
    with col2:
        st.subheader("✅ Cost Analysis")
        st.info("Analyze costs by department/service")
        
        st.subheader("✅ Revenue Optimization")
        st.info("Identify revenue opportunities")
        
        st.subheader("✅ Compliance Checking")
        st.info("Ensure financial compliance")
        
        st.subheader("✅ Forecasting")
        st.info("Predict future financial performance")
        
        st.subheader("✅ Integration")
        st.info("Connect with all financial systems")

with tab2:
    st.header("ℹ️ About Finance AI")
    st.markdown("""
    ### 💰 Business Impact:
    - Market: 40,000 finance staff
    - Cost: £49,000/year per staff
    - Total: £1.96 BILLION/year
    - Automation: 80%
    - Savings: £1.57 BILLION/year
    
    ### 🚀 10 Features:
    1. Auto-invoicing
    2. Payment processing
    3. Fraud detection
    4. Budget tracking
    5. Financial reporting
    6. Cost analysis
    7. Revenue optimization
    8. Compliance checking
    9. Forecasting
    10. System integration
    
    ### 📞 Support:
    
    Email: info@t21services.co.uk  
    Website: www.t21services.co.uk  
    Company: T21 Services Limited (No: 13091053)
    """)

st.markdown("---")
st.caption("© 2025 T21 Services Limited | Finance AI v1.0")
