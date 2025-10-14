"""
T21 Training AI - Complete Training Automation
"""

import streamlit as st

st.set_page_config(page_title="Training AI", page_icon="🎓", layout="wide")

st.title("🎓 Training AI")
st.markdown("### AI training modules, VR simulations, competency tracking - Save £1.68 BILLION/year!")

tab1, tab2 = st.tabs(["🎓 Features", "ℹ️ About"])

with tab1:
    st.header("🎓 Training AI Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ AI Training Modules")
        st.info("Personalized AI-powered training")
        
        st.subheader("✅ Virtual Training")
        st.info("VR/AR training simulations")
        
        st.subheader("✅ Competency Tracking")
        st.info("Track staff competencies")
        
        st.subheader("✅ Certification Management")
        st.info("Manage all certifications")
        
        st.subheader("✅ Compliance Tracking")
        st.info("Ensure mandatory training complete")
    
    with col2:
        st.subheader("✅ Assessment Automation")
        st.info("Automated testing and grading")
        
        st.subheader("✅ Learning Paths")
        st.info("Personalized learning journeys")
        
        st.subheader("✅ Performance Analytics")
        st.info("Track training effectiveness")
        
        st.subheader("✅ Content Management")
        st.info("Manage all training content")
        
        st.subheader("✅ Integration")
        st.info("Connect with HR systems")

with tab2:
    st.header("ℹ️ About Training AI")
    st.markdown("""
    ### 💰 Business Impact:
    - Market: 60,000 training staff
    - Cost: £28,000/year per staff
    - Total: £1.68 BILLION/year
    - Automation: 80%
    - Savings: £1.34 BILLION/year
    
    ### 🚀 10 Features:
    1. AI training modules
    2. Virtual reality training
    3. Competency tracking
    4. Certification management
    5. Compliance tracking
    6. Assessment automation
    7. Personalized learning paths
    8. Performance analytics
    9. Content management
    10. System integration
    
    ### 📞 Support:
    
    Email: info@t21services.co.uk  
    Website: www.t21services.co.uk  
    Company: T21 Services Limited (No: 13091053)
    """)

st.markdown("---")
st.caption("© 2025 T21 Services Limited | Training AI v1.0")
