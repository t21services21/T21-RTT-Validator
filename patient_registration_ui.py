"""
T21 PATIENT REGISTRATION UI
User interface for complete patient registration

Features:
- Register new patients
- Search existing patients
- View patient demographics
- NHS number validation
- Patient list management
"""

import streamlit as st
from datetime import datetime, date
from patient_registration_system import (
    register_patient,
    validate_nhs_number,
    generate_temporary_id,
    get_patient_by_id,
    search_patients,
    get_all_patients,
    get_registration_stats
)


def render_patient_registration():
    """Main patient registration interface"""
    
    st.header("👤 Patient Registration System")
    st.markdown("**Complete Patient Demographics & Registration Management**")
    
    st.success("""
    👤 **Patient Registration Features:**
    - 📝 Register new patients with complete demographics
    - 🔍 NHS number validation (Modulus 11 algorithm)
    - 🆔 Automatic temporary ID generation
    - 🔎 Search existing patients
    - 📊 Registration statistics
    - 🏥 GP and next of kin management
    - 🌍 Interpreter requirements tracking
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Register New Patient",
        "📋 Patient List",
        "🔍 Search Patients",
        "📊 Registration Stats"
    ])
    
    with tab1:
        render_register_patient()
    
    with tab2:
        render_patient_list()
    
    with tab3:
        render_search_patients()
    
    with tab4:
        render_registration_stats()


def render_register_patient():
    """Register new patient form"""
    
    st.subheader("➕ Register New Patient")
    
    # Show success message if patient was just registered - ENHANCED
    if 'patient_registered' in st.session_state:
        patient_info = st.session_state['patient_registered']
        st.balloons()
        st.success(f"""
        ✅ **PATIENT REGISTERED SUCCESSFULLY!**
        
        **Patient ID:** {patient_info['patient_id']}  
        **NHS Number:** {patient_info.get('nhs_number', 'Not provided')}  
        **NHS Status:** {patient_info['nhs_status']}  
        **Name:** {patient_info['name']}  
        
        ✔️ Patient has been saved to the database!  
        📊 All demographic information recorded permanently!
        """)
        st.info("💡 **Next Steps:** You can now create pathways, book appointments, or register episodes for this patient.")
        del st.session_state['patient_registered']
    
    with st.form("register_patient"):
        st.markdown("### 📋 Patient Demographics")
        
        # Basic Information
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            title = st.selectbox("Title*", ["Mr", "Mrs", "Miss", "Ms", "Dr", "Master", "Mx"])
        with col2:
            first_name = st.text_input("First Name*", placeholder="John")
        with col3:
            surname = st.text_input("Surname*", placeholder="Smith")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dob = st.date_input("Date of Birth*", min_value=date(1900, 1, 1), max_value=date.today())
        with col2:
            gender = st.selectbox("Gender*", ["Male", "Female", "Other", "Prefer not to say"])
        with col3:
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed", "Civil Partnership", "Unknown"])
        
        # NHS Number
        st.markdown("### 🆔 NHS Number")
        col1, col2 = st.columns([3, 1])
        with col1:
            nhs_number = st.text_input(
                "NHS Number (10 digits)",
                placeholder="123 456 7890",
                help="Leave empty to generate temporary ID"
            )
        with col2:
            if st.form_submit_button("✓ Validate", use_container_width=True):
                if nhs_number:
                    validation = validate_nhs_number(nhs_number)
                    if validation['valid']:
                        st.success(f"✅ Valid: {validation['formatted']}")
                    else:
                        st.error(f"❌ {validation['error']}")
        
        # Address
        st.markdown("### 🏠 Address")
        address_line1 = st.text_input("Address Line 1*", placeholder="123 High Street")
        address_line2 = st.text_input("Address Line 2", placeholder="Apartment 4B")
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("City*", placeholder="London")
        with col2:
            postcode = st.text_input("Postcode*", placeholder="SW1A 1AA")
        
        # Contact Information
        st.markdown("### 📞 Contact Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            phone_home = st.text_input("Home Phone", placeholder="020 1234 5678")
        with col2:
            phone_mobile = st.text_input("Mobile Phone*", placeholder="07123 456789")
        with col3:
            email = st.text_input("Email", placeholder="patient@example.com")
        
        # GP Information
        st.markdown("### 🏥 GP Information")
        col1, col2 = st.columns(2)
        with col1:
            gp_name = st.text_input("GP Name*", placeholder="Dr. Jones")
            gp_practice = st.text_input("GP Practice*", placeholder="High Street Surgery")
        with col2:
            gp_address = st.text_area("GP Address", height=100, placeholder="123 High Street, London, SW1A 1AA")
        
        # Next of Kin
        st.markdown("### 👥 Next of Kin")
        col1, col2, col3 = st.columns(3)
        with col1:
            nok_name = st.text_input("Next of Kin Name*", placeholder="Jane Smith")
        with col2:
            nok_relationship = st.selectbox("Relationship*", [
                "Spouse", "Parent", "Child", "Sibling", "Partner", "Friend", "Other"
            ])
        with col3:
            nok_phone = st.text_input("Next of Kin Phone*", placeholder="07123 456789")
        
        # Emergency Contact (if different)
        st.markdown("### 🚨 Emergency Contact")
        col1, col2 = st.columns(2)
        with col1:
            emergency_name = st.text_input("Emergency Contact Name", placeholder="Leave empty if same as Next of Kin")
        with col2:
            emergency_phone = st.text_input("Emergency Contact Phone")
        
        # Additional Information
        st.markdown("### ℹ️ Additional Information")
        col1, col2 = st.columns(2)
        with col1:
            ethnicity = st.selectbox("Ethnicity", [
                "White British", "White Irish", "White Other",
                "Asian/Asian British - Indian", "Asian/Asian British - Pakistani", "Asian/Asian British - Bangladeshi",
                "Black/Black British - Caribbean", "Black/Black British - African",
                "Mixed - White and Black Caribbean", "Mixed - White and Black African",
                "Chinese", "Other", "Prefer not to say"
            ])
            language = st.text_input("Preferred Language", value="English")
        with col2:
            interpreter_required = st.checkbox("Interpreter Required")
            religion = st.text_input("Religion", placeholder="Optional")
            occupation = st.text_input("Occupation", placeholder="Optional")
        
        # Notes
        notes = st.text_area("Clinical Notes", height=100, placeholder="Any relevant notes...")
        
        # Submit
        st.markdown("---")
        submit = st.form_submit_button("✅ Register Patient", type="primary", use_container_width=True)
        
        if submit:
            # Validation
            if not first_name or not surname or not phone_mobile or not city or not postcode:
                st.error("❌ Please fill all required fields marked with *")
            elif not gp_name or not gp_practice:
                st.error("❌ GP information is required")
            elif not nok_name or not nok_phone:
                st.error("❌ Next of Kin information is required")
            else:
                # Register patient
                with st.spinner("📝 Registering patient..."):
                    result = register_patient(
                        title=title,
                        first_name=first_name,
                        surname=surname,
                        date_of_birth=str(dob),
                        gender=gender,
                        nhs_number=nhs_number if nhs_number else None,
                        address_line1=address_line1,
                        address_line2=address_line2,
                        city=city,
                        postcode=postcode,
                        phone_home=phone_home,
                        phone_mobile=phone_mobile,
                        email=email,
                        gp_name=gp_name,
                        gp_practice=gp_practice,
                        gp_address=gp_address,
                        next_of_kin_name=nok_name,
                        next_of_kin_relationship=nok_relationship,
                        next_of_kin_phone=nok_phone,
                        emergency_contact_name=emergency_name,
                        emergency_contact_phone=emergency_phone,
                        ethnicity=ethnicity,
                        language=language,
                        interpreter_required=interpreter_required,
                        religion=religion,
                        marital_status=marital_status,
                        occupation=occupation,
                        notes=notes
                    )
                
                if result['success']:
                    # Store success info
                    st.session_state['patient_registered'] = {
                        'patient_id': result['patient_id'],
                        'nhs_status': result['nhs_status'],
                        'name': f"{title} {first_name} {surname}"
                    }
                    st.rerun()
                else:
                    st.error(f"❌ Registration failed: {result.get('error', 'Unknown error')}")


def render_patient_list():
    """Display list of all registered patients"""
    
    st.subheader("📋 Registered Patients")
    
    # Refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Get all patients
    patients = get_all_patients()
    
    if not patients:
        st.info("📝 No patients registered yet. Use 'Register New Patient' tab to add patients.")
        return
    
    st.write(f"**Total Patients:** {len(patients)}")
    
    # Display patients in cards
    for patient in patients:
        with st.expander(f"👤 {patient.get('full_name', 'Unknown')} - {patient.get('patient_id', 'N/A')}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Demographics:**")
                st.write(f"**DOB:** {patient.get('date_of_birth', 'N/A')}")
                st.write(f"**Gender:** {patient.get('gender', 'N/A')}")
                st.write(f"**NHS Number:** {patient.get('nhs_number', 'Pending')}")
                st.write(f"**NHS Status:** {patient.get('nhs_status', 'N/A')}")
            
            with col2:
                st.markdown("**Contact:**")
                st.write(f"**Mobile:** {patient.get('phone_mobile', 'N/A')}")
                st.write(f"**Email:** {patient.get('email', 'N/A')}")
                st.write(f"**Address:** {patient.get('address_line1', '')}, {patient.get('city', '')}")
                st.write(f"**Postcode:** {patient.get('postcode', 'N/A')}")
            
            with col3:
                st.markdown("**GP & NOK:**")
                st.write(f"**GP:** {patient.get('gp_name', 'N/A')}")
                st.write(f"**Practice:** {patient.get('gp_practice', 'N/A')}")
                st.write(f"**Next of Kin:** {patient.get('next_of_kin_name', 'N/A')}")
                st.write(f"**NOK Phone:** {patient.get('next_of_kin_phone', 'N/A')}")
            
            if patient.get('interpreter_required'):
                st.warning(f"🌍 **Interpreter Required:** {patient.get('language', 'Unknown')}")


def render_search_patients():
    """Search for patients"""
    
    st.subheader("🔍 Search Patients")
    
    search_query = st.text_input(
        "Search by Name, NHS Number, or Patient ID",
        placeholder="Enter name, NHS number, or ID...",
        key="patient_search"
    )
    
    if search_query:
        with st.spinner("Searching..."):
            results = search_patients(search_query)
        
        if results:
            st.success(f"✅ Found {len(results)} patient(s)")
            
            for patient in results:
                with st.expander(f"👤 {patient.get('full_name', 'Unknown')} - {patient.get('patient_id', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Patient ID:** {patient.get('patient_id', 'N/A')}")
                        st.write(f"**NHS Number:** {patient.get('nhs_number', 'Pending')}")
                        st.write(f"**DOB:** {patient.get('date_of_birth', 'N/A')}")
                        st.write(f"**Gender:** {patient.get('gender', 'N/A')}")
                        st.write(f"**Mobile:** {patient.get('phone_mobile', 'N/A')}")
                    
                    with col2:
                        st.write(f"**GP:** {patient.get('gp_name', 'N/A')}")
                        st.write(f"**Address:** {patient.get('city', 'N/A')}, {patient.get('postcode', 'N/A')}")
                        st.write(f"**Registered:** {patient.get('registration_date', 'N/A')[:10]}")
                        st.write(f"**Status:** {patient.get('status', 'N/A')}")
        else:
            st.warning("⚠️ No patients found matching your search")
    else:
        st.info("💡 Enter a search term to find patients")


def render_registration_stats():
    """Display registration statistics"""
    
    st.subheader("📊 Patient Registration Statistics")
    
    stats = get_registration_stats()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", stats['total_patients'])
    
    with col2:
        st.metric("With NHS Number", stats['with_nhs_number'], 
                 delta=f"{stats['nhs_verified_rate']:.0f}% verified")
    
    with col3:
        st.metric("Pending NHS Number", stats['pending_nhs_number'])
    
    with col4:
        st.metric("Registered Today", stats['registered_today'])
    
    # Additional info
    st.markdown("---")
    st.info(f"""
    📊 **Registration Summary:**
    - **Total Registered:** {stats['total_patients']} patients
    - **NHS Verified:** {stats['with_nhs_number']} ({stats['nhs_verified_rate']:.1f}%)
    - **Temporary IDs:** {stats['temporary_ids']}
    - **Registered Today:** {stats['registered_today']}
    """)
    
    if stats['pending_nhs_number'] > 0:
        st.warning(f"⚠️ {stats['pending_nhs_number']} patients awaiting NHS number assignment")
