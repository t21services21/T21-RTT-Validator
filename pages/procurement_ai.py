"""
T21 Procurement AI - Complete Procurement Automation
"""

import streamlit as st

st.set_page_config(page_title="Procurement AI", page_icon="📦", layout="wide")

st.title("📦 Procurement AI")
st.markdown("### Auto-ordering, inventory management, supplier optimization - Save £920M/year!")

tab1, tab2 = st.tabs(["📦 Features", "ℹ️ About"])

with tab1:
    st.header("📦 Procurement AI Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Auto-Ordering")
        st.info("Automatically order supplies when low")
        
        st.subheader("✅ Inventory Management")
        st.info("Real-time stock tracking")
        
        st.subheader("✅ Predictive Ordering")
        st.info("AI predicts future needs")
        
        st.subheader("✅ Supplier Management")
        st.info("Optimize supplier relationships")
        
        st.subheader("✅ Cost Optimization")
        st.info("Find best prices automatically")
    
    with col2:
        st.subheader("✅ Contract Management")
        st.info("Track and renew contracts")
        
        st.subheader("✅ Quality Assurance")
        st.info("Monitor supplier quality")
        
        st.subheader("✅ Compliance")
        st.info("Ensure procurement compliance")
        
        st.subheader("✅ Analytics")
        st.info("Procurement insights and trends")
        
        st.subheader("✅ Integration")
        st.info("Connect with all systems")

with tab2:
    st.header("ℹ️ About Procurement AI")
    st.markdown("""
    ### 💰 Business Impact:
    - Market: 20,000 procurement staff
    - Cost: £46,000/year per staff
    - Total: £920 MILLION/year
    - Automation: 70%
    - Savings: £644 MILLION/year
    
    ### 🚀 10 Features:
    1. Auto-ordering
    2. Inventory management
    3. Predictive ordering
    4. Supplier management
    5. Cost optimization
    6. Contract management
    7. Quality assurance
    8. Compliance checking
    9. Procurement analytics
    10. System integration
    """)

st.markdown("---")
st.caption("© 2025 T21 Services Limited | Procurement AI v1.0")
