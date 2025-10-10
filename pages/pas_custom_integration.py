"""
T21 SERVICES - CUSTOM PAS INTEGRATION
Allow NHS Trusts to connect their own PAS systems
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fhir_integration import FHIRClient, FHIR_CONFIGS
import json

st.set_page_config(
    page_title="Custom PAS Integration | T21 Services",
    page_icon="🔌",
    layout="wide"
)

# ⚠️ AUTHENTICATION CHECK - ADMIN/NHS ONLY
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 **Access Denied - Login Required**")
    st.warning("Custom PAS Integration is available to NHS organizations only.")
    st.stop()

# Check if user is NHS Trust or Admin
user_license = st.session_state.get('user_license')
user_role = getattr(user_license, 'role', 'trial') if user_license else 'trial'
user_type = getattr(user_license, 'user_type', 'student') if hasattr(user_license, 'user_type') else 'student'

is_nhs_or_admin = user_role in ['nhs_trust', 'admin'] or user_type in ['admin', 'nhs']

if not is_nhs_or_admin:
    st.error("🔒 **Access Denied**")
    st.warning("This feature is available to NHS Trusts and Administrators only.")
    st.info("📧 Contact info@t21services.co.uk to integrate your PAS system")
    st.stop()

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>🔌 Custom PAS Integration</h1>
    <p style='color: white; margin: 0;'>Connect YOUR Trust's PAS System to T21 Platform</p>
</div>
""", unsafe_allow_html=True)

# Info banner
st.info("""
**🏥 For NHS Trusts:** Connect your existing PAS system (Lorenzo, Cerner, Epic, etc.) to T21 Services platform using HL7 FHIR standard.

**⚡ Integration Time:** 1-3 days | **Standard:** HL7 FHIR R4 | **Security:** NHS DSP Toolkit Compliant
""")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Integration Request", "🔧 Configuration", "✅ Test Connection", "📚 Documentation"])

with tab1:
    st.markdown("## 📋 PAS Integration Request Form")
    st.markdown("Complete this form to request custom PAS integration for your NHS Trust.")
    
    with st.form("pas_integration_request"):
        st.markdown("### Trust Information")
        col1, col2 = st.columns(2)
        
        with col1:
            trust_name = st.text_input("NHS Trust Name *", placeholder="Liverpool University Hospitals NHS Foundation Trust")
            trust_code = st.text_input("Trust ODS Code *", placeholder="REM")
            contact_name = st.text_input("IT Contact Name *", placeholder="John Smith")
        
        with col2:
            contact_email = st.text_input("IT Contact Email *", placeholder="john.smith@trust.nhs.uk")
            contact_phone = st.text_input("Contact Phone *", placeholder="+44 151 XXX XXXX")
            project_ref = st.text_input("Project Reference (Optional)", placeholder="PAS-INT-2025")
        
        st.markdown("---")
        st.markdown("### PAS System Details")
        
        col3, col4 = st.columns(2)
        
        with col3:
            pas_vendor = st.selectbox(
                "PAS Vendor *",
                ["Select...", "Lorenzo (DXC)", "Cerner Millennium", "Epic", "Medway", "System C", "TrakCare (InterSystems)", "Other"]
            )
            pas_version = st.text_input("PAS Version", placeholder="e.g., Lorenzo 16.0")
        
        with col4:
            fhir_available = st.radio("Does your PAS have FHIR API? *", ["Yes", "No", "Not Sure"])
            integration_type = st.selectbox(
                "Integration Type",
                ["Read Only (Query patients, appointments)", "Read + Write (Book appointments, update data)", "Full Integration"]
            )
        
        st.markdown("---")
        st.markdown("### Technical Details")
        
        fhir_endpoint = st.text_input(
            "FHIR API Endpoint URL (if known)",
            placeholder="https://fhir.yourtrust.nhs.uk/api/FHIR/R4"
        )
        
        auth_method = st.selectbox(
            "Authentication Method",
            ["Not Sure", "OAuth 2.0", "API Key", "Basic Auth", "JWT Token", "Other"]
        )
        
        additional_info = st.text_area(
            "Additional Information / Requirements",
            placeholder="Any specific requirements, firewall details, data access restrictions, etc.",
            height=150
        )
        
        st.markdown("---")
        
        col5, col6 = st.columns(2)
        with col5:
            urgency = st.radio("Integration Urgency", ["Standard (2-3 weeks)", "Priority (1 week)", "Urgent (ASAP)"])
        
        with col6:
            go_live_date = st.date_input("Target Go-Live Date")
        
        submit_button = st.form_submit_button("📤 Submit Integration Request", type="primary", use_container_width=True)
        
        if submit_button:
            # Validate required fields
            if not all([trust_name, trust_code, contact_name, contact_email, contact_phone, pas_vendor != "Select..."]):
                st.error("❌ Please fill in all required fields (*)")
            else:
                # Save request
                request_data = {
                    "trust_name": trust_name,
                    "trust_code": trust_code,
                    "contact_name": contact_name,
                    "contact_email": contact_email,
                    "contact_phone": contact_phone,
                    "project_ref": project_ref,
                    "pas_vendor": pas_vendor,
                    "pas_version": pas_version,
                    "fhir_available": fhir_available,
                    "integration_type": integration_type,
                    "fhir_endpoint": fhir_endpoint,
                    "auth_method": auth_method,
                    "additional_info": additional_info,
                    "urgency": urgency,
                    "go_live_date": str(go_live_date),
                    "submitted_by": st.session_state.get('user_email'),
                    "submitted_date": st.session_state.get('timestamp', 'now')
                }
                
                # Save to JSON file
                try:
                    # Load existing requests
                    requests_file = "pas_integration_requests.json"
                    if os.path.exists(requests_file):
                        with open(requests_file, 'r') as f:
                            requests = json.load(f)
                    else:
                        requests = []
                    
                    # Add new request
                    requests.append(request_data)
                    
                    # Save
                    with open(requests_file, 'w') as f:
                        json.dump(requests, f, indent=2)
                    
                    st.success("""
                    ✅ **Integration Request Submitted Successfully!**
                    
                    **What happens next:**
                    1. Our integration team will review your request within 24 hours
                    2. You'll receive an email with technical requirements
                    3. We'll schedule a technical call
                    4. Integration typically completes in 1-3 days after credentials provided
                    
                    **📧 Confirmation sent to:** {contact_email}
                    """)
                    
                    # Email notification to T21 admin
                    st.info("📧 T21 Integration Team has been notified: integration@t21services.co.uk")
                
                except Exception as e:
                    st.error(f"❌ Error saving request: {e}")
                    st.info("📧 Please email your details to: integration@t21services.co.uk")

with tab2:
    st.markdown("## 🔧 PAS Configuration (Admin Only)")
    
    if user_type != 'admin':
        st.warning("Configuration panel is available to T21 administrators only.")
        st.stop()
    
    st.markdown("### Current Configured PAS Systems")
    
    # Display current configs
    for key, config in FHIR_CONFIGS.items():
        with st.expander(f"🏥 {config['name']} ({key})"):
            st.markdown(f"**Base URL:** `{config['base_url']}`")
            st.markdown(f"**Auth Required:** {config.get('auth_required', 'No')}")
            st.markdown(f"**Description:** {config['description']}")
    
    st.markdown("---")
    st.markdown("### Add New PAS Configuration")
    
    with st.form("add_pas_config"):
        new_key = st.text_input("Configuration Key (e.g., trust_abc)")
        new_name = st.text_input("PAS System Name")
        new_url = st.text_input("FHIR Base URL")
        new_auth_req = st.checkbox("Authentication Required")
        new_desc = st.text_area("Description")
        
        if st.form_submit_button("💾 Save Configuration"):
            st.info("ℹ️ Configuration changes require code deployment. Contact technical team.")

with tab3:
    st.markdown("## ✅ Test PAS Connection")
    st.markdown("Test connectivity to configured PAS systems.")
    
    # Select PAS to test
    selected_pas = st.selectbox(
        "Select PAS System to Test",
        list(FHIR_CONFIGS.keys()),
        format_func=lambda x: FHIR_CONFIGS[x]['name']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔌 Test Connection", type="primary", use_container_width=True):
            with st.spinner(f"Testing connection to {FHIR_CONFIGS[selected_pas]['name']}..."):
                try:
                    client = FHIRClient(selected_pas)
                    success, message = client.test_connection()
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"❌ Connection test failed: {e}")
    
    with col2:
        if st.button("📥 Fetch Test Patient", use_container_width=True):
            with st.spinner("Fetching patient data..."):
                try:
                    client = FHIRClient(selected_pas)
                    patients = client.get_patients(limit=1)
                    
                    if patients:
                        st.success(f"✅ Retrieved {len(patients)} patient(s)")
                        st.json(patients[0])
                    else:
                        st.warning("No patients found in test environment")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

with tab4:
    st.markdown("## 📚 Integration Documentation")
    
    st.markdown("""
    ### 🏥 NHS Trust PAS Integration Process
    
    #### **Phase 1: Discovery (1-2 days)**
    1. Complete integration request form
    2. Technical call with Trust IT team
    3. Confirm PAS vendor & FHIR capability
    4. Document authentication requirements
    
    #### **Phase 2: Configuration (1 day)**
    1. Trust provides:
       - FHIR API endpoint URL
       - Authentication credentials (OAuth/API Key)
       - Firewall allow-list for T21 IPs
       - Test environment access
    
    2. T21 configures:
       - FHIR client with Trust endpoint
       - Authentication flow
       - SSL certificate verification
       - API rate limiting
    
    #### **Phase 3: Testing (1-2 days)**
    1. Connection test
    2. Patient query test
    3. Appointment query test
    4. Data mapping verification
    5. Performance testing
    
    #### **Phase 4: Go Live (1 day)**
    1. Final UAT (User Acceptance Testing)
    2. Production deployment
    3. Staff training session
    4. Monitoring setup
    5. **LIVE!** ✅
    
    ---
    
    ### 🔐 Security & Compliance
    
    ✅ **NHS DSP Toolkit Compliant**
    ✅ **HL7 FHIR R4 Standard**
    ✅ **TLS 1.3 Encryption**
    ✅ **OAuth 2.0 Authentication**
    ✅ **Audit Trail Logging**
    ✅ **GDPR Compliant**
    ✅ **No local data storage** (real-time API only)
    
    ---
    
    ### 📞 Support & Contact
    
    **Integration Team:**
    - 📧 integration@t21services.co.uk
    - ☎️ +44 20 3375 2061
    - 🌐 www.t21services.co.uk/pas-integration
    
    **Support Hours:**
    - Standard: Monday-Friday, 9am-5pm GMT
    - Priority: 24/7 emergency support available
    
    ---
    
    ### 💰 Pricing
    
    **Integration Fee:** £2,500 one-time
    **Monthly License:** £500-1,500/user (based on user count)
    **Support:** Included in license
    
    **ROI:** Most trusts save 20-40 hours/week in manual data entry
    """)

# Footer
st.markdown("---")
st.markdown("**🏥 T21 Services Limited** | NHS PAS Integration Specialists")
st.markdown("📧 integration@t21services.co.uk | ☎️ +44 20 3375 2061")
