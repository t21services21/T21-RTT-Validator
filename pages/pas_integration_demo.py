"""
T21 SERVICES - PAS INTEGRATION DEMO
Live demonstration of NHS PAS connectivity via HL7 FHIR
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fhir_integration import FHIRClient, FHIR_CONFIGS
import pandas as pd


# ⚠️ AUTHENTICATION CHECK - MUST BE LOGGED IN
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 **Access Denied - Login Required**")
    st.warning("You must be logged in to access the PAS Integration Demo.")
    st.info("This feature is available to enrolled students and NHS organizations.")
    
    st.markdown("### Please Login:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎓 Student Login", use_container_width=True):
            st.switch_page("pages/student_login.py")
    with col2:
        if st.button("👥 Staff Login", use_container_width=True):
            st.switch_page("pages/staff_login.py")
    with col3:
        if st.button("🏥 NHS Login", use_container_width=True):
            st.switch_page("pages/nhs_login.py")
    
    st.stop()  # Stop execution here

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; margin: 0;'>🏥 NHS PAS Integration Demo</h1>
    <p style='color: white; margin: 0;'>Live HL7 FHIR Connection to Patient Administration Systems</p>
</div>
""", unsafe_allow_html=True)

# Info banner
st.info("""
**🔗 What This Demonstrates:**
- Real-time connection to HL7 FHIR servers (NHS standard)
- Pull live patient demographics
- Retrieve appointment data
- Ready for NHS Trust deployment

**Currently Connected To:** Public FHIR test server (demo data)  
**For NHS Trusts:** Connect to YOUR PAS by providing API endpoint
""")

st.markdown("---")

# Server selection
st.subheader("🔧 FHIR Server Configuration")

col1, col2 = st.columns(2)

with col1:
    server_choice = st.selectbox(
        "Select FHIR Server:",
        options=list(FHIR_CONFIGS.keys()),
        format_func=lambda x: FHIR_CONFIGS[x]["name"]
    )
    
    server_config = FHIR_CONFIGS[server_choice]
    
    st.markdown(f"""
    **Server:** {server_config['name']}  
    **Endpoint:** `{server_config['base_url']}`  
    **Auth Required:** {'Yes' if server_config['auth_required'] else 'No'}  
    **Description:** {server_config['description']}
    """)

with col2:
    st.markdown("### 🏥 For NHS Trusts")
    st.markdown("""
    **To connect to YOUR PAS:**
    1. Provide FHIR API endpoint
    2. Provide authentication credentials
    3. We configure in 1 hour
    4. **GO LIVE!** ✅
    
    **Compatible with:**
    - Lorenzo (DXC)
    - Cerner Millennium
    - Epic
    - System C
    - Any FHIR-compliant PAS
    """)

st.markdown("---")

# Test connection button
if st.button("🔌 Test FHIR Connection", type="primary"):
    with st.spinner("Connecting to FHIR server..."):
        try:
            client = FHIRClient(server_choice)
            success, message = client.test_connection()
            
            if success:
                st.success(message)
                st.session_state.fhir_connected = True
                st.session_state.fhir_client = client
            else:
                st.error(message)
                st.session_state.fhir_connected = False
        
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")
            st.session_state.fhir_connected = False

st.markdown("---")

# Only show data if connected
if st.session_state.get('fhir_connected'):
    client = st.session_state.get('fhir_client')
    
    tab1, tab2, tab3 = st.tabs(["👥 Patient List", "📅 Appointments", "📊 Analytics"])
    
    with tab1:
        st.subheader("👥 Patient Demographics from PAS")
        
        col_fetch1, col_fetch2 = st.columns([1, 3])
        
        with col_fetch1:
            patient_limit = st.number_input("Number of patients:", min_value=1, max_value=50, value=10)
        
        with col_fetch2:
            if st.button("🔄 Fetch Patients from PAS", type="primary"):
                with st.spinner("Fetching patient data via FHIR..."):
                    try:
                        patients = client.get_patients(limit=patient_limit)
                        st.session_state.patients = patients
                        st.success(f"✅ Retrieved {len(patients)} patients from PAS")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Display patients
        if st.session_state.get('patients'):
            patients = st.session_state.patients
            
            st.markdown(f"### Showing {len(patients)} patients")
            
            # Convert to DataFrame
            patient_df = pd.DataFrame(patients)
            
            # Select columns to display
            display_cols = ['nhs_number', 'full_name', 'birth_date', 'gender', 'address', 'phone', 'active']
            display_df = patient_df[display_cols]
            
            st.dataframe(
                display_df,
                use_container_width=True,
                column_config={
                    "nhs_number": "NHS Number",
                    "full_name": "Patient Name",
                    "birth_date": "Date of Birth",
                    "gender": "Gender",
                    "address": "Address",
                    "phone": "Contact",
                    "active": st.column_config.CheckboxColumn("Active")
                }
            )
            
            # Export options
            st.markdown("---")
            st.markdown("### 📥 Export Patient Data")
            
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                csv_data = display_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Download as CSV",
                    data=csv_data,
                    file_name=f"pas_patients_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col_exp2:
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    display_df.to_excel(writer, index=False, sheet_name='Patients')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📊 Download as Excel",
                    data=excel_data,
                    file_name=f"pas_patients_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with tab2:
        st.subheader("📅 Appointments from PAS")
        
        if st.button("🔄 Fetch Appointments", type="primary"):
            with st.spinner("Fetching appointments via FHIR..."):
                try:
                    appointments = client.get_appointments(limit=20)
                    st.session_state.appointments = appointments
                    
                    if appointments:
                        st.success(f"✅ Retrieved {len(appointments)} appointments from PAS")
                    else:
                        st.info("No appointments found in test server")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Display appointments
        if st.session_state.get('appointments'):
            appointments = st.session_state.appointments
            
            if appointments:
                appt_df = pd.DataFrame(appointments)
                
                display_appt_cols = ['id', 'status', 'start', 'end', 'description']
                display_appt_df = appt_df[display_appt_cols]
                
                st.dataframe(
                    display_appt_df,
                    use_container_width=True,
                    column_config={
                        "id": "Appointment ID",
                        "status": "Status",
                        "start": "Start Time",
                        "end": "End Time",
                        "description": "Description"
                    }
                )
            else:
                st.info("No appointments in test database")
    
    with tab3:
        st.subheader("📊 Integration Analytics")
        
        if st.session_state.get('patients'):
            patients = st.session_state.patients
            
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                st.metric("Total Patients", len(patients))
            
            with col_stat2:
                active_patients = sum(1 for p in patients if p.get('active'))
                st.metric("Active Patients", active_patients)
            
            with col_stat3:
                male_count = sum(1 for p in patients if p.get('gender', '').lower() == 'male')
                st.metric("Male Patients", male_count)
            
            with col_stat4:
                female_count = sum(1 for p in patients if p.get('gender', '').lower() == 'female')
                st.metric("Female Patients", female_count)
            
            st.markdown("---")
            
            # Gender distribution chart
            import plotly.express as px
            
            gender_data = pd.DataFrame([
                {'Gender': 'Male', 'Count': male_count},
                {'Gender': 'Female', 'Count': female_count},
                {'Gender': 'Other/Unknown', 'Count': len(patients) - male_count - female_count}
            ])
            
            fig = px.pie(gender_data, values='Count', names='Gender', title='Patient Gender Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("Fetch patient data to see analytics")

else:
    st.warning("⚠️ Click 'Test FHIR Connection' above to connect to the PAS")

st.markdown("---")

# Footer info
st.markdown("### 💼 Business Value")

col_bus1, col_bus2, col_bus3 = st.columns(3)

with col_bus1:
    st.markdown("""
    **For NHS Trusts:**
    - Real-time data access
    - No manual data entry
    - Integrated workflows
    - Reduced errors
    """)

with col_bus2:
    st.markdown("""
    **Integration Benefits:**
    - Standard HL7 FHIR
    - Works with any PAS
    - Secure authentication
    - 1-day deployment
    """)

with col_bus3:
    st.markdown("""
    **Pricing:**
    - Integration module: £5,000
    - Per user: £500-1,500/month
    - Includes support
    - Updates included
    """)

st.markdown("---")
st.caption("T21 Services Limited | NHS PAS Integration | HL7 FHIR Compliant")
