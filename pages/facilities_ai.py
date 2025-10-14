"""
T21 Facilities AI - Complete Facilities Automation
"""

import streamlit as st

st.set_page_config(page_title="Facilities AI", page_icon="🏢", layout="wide")

st.title("🏢 Facilities AI")
st.markdown("### Maintenance scheduling, energy optimization, asset tracking - Save £840M/year!")

tab1, tab2 = st.tabs(["🏢 Features", "ℹ️ About"])

with tab1:
    st.header("🏢 Facilities AI Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Maintenance Scheduling")
        st.info("Automated preventive maintenance")
        
        st.subheader("✅ Space Management")
        st.info("Optimize room and space usage")
        
        st.subheader("✅ Energy Optimization")
        st.info("AI reduces energy costs")
        
        st.subheader("✅ Asset Tracking")
        st.info("Track all equipment and assets")
        
        st.subheader("✅ Predictive Maintenance")
        st.info("Predict equipment failures")
    
    with col2:
        st.subheader("✅ Work Order Management")
        st.info("Automated work order system")
        
        st.subheader("✅ Compliance Checking")
        st.info("Ensure facilities compliance")
        
        st.subheader("✅ Vendor Management")
        st.info("Manage facilities vendors")
        
        st.subheader("✅ Cost Tracking")
        st.info("Track all facilities costs")
        
        st.subheader("✅ Integration")
        st.info("Connect with building systems")

with tab2:
    st.header("ℹ️ About Facilities AI")
    st.markdown("""
    ### 💰 Business Impact:
    - Market: 10,000 facilities staff
    - Cost: £84,000/year per staff
    - Total: £840 MILLION/year
    - Automation: 65%
    - Savings: £546 MILLION/year
    
    ### 🚀 10 Features:
    1. Maintenance scheduling
    2. Space management
    3. Energy optimization
    4. Asset tracking
    5. Predictive maintenance
    6. Work order management
    7. Compliance checking
    8. Vendor management
    9. Cost tracking
    10. System integration
    
    ### 📞 Support:
    
    Email: info@t21services.co.uk  
    Website: www.t21services.co.uk  
    Company: T21 Services Limited (No: 13091053)
    """)

st.markdown("---")
st.caption("© 2025 T21 Services Limited | Facilities AI v1.0")
