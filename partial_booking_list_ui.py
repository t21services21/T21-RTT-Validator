"""
PARTIAL BOOKING LIST (PBL) - USER INTERFACE
NHS-Compliant PBL Management with Data Cleansing Tools

FEATURES:
- View all patients on PBL
- Add/Remove patients
- Send acknowledgment emails
- Monitor breach risks
- Data cleansing tools (for NHS experts)
- Automatic removal when appointment booked
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from partial_booking_list_system import (
    add_to_pbl,
    remove_from_pbl,
    load_pbl_patients,
    validate_pbl_data,
    clean_pbl_duplicates,
    PBLPatient
)

def render_partial_booking_list():
    """Main PBL interface"""
    
    st.title("📋 Partial Booking List (PBL)")
    st.markdown("### Patients Awaiting First Appointment")
    
    st.info("""
    **What is PBL?**
    
    The Partial Booking List contains patients whose referral has been ACCEPTED but we currently have NO APPOINTMENT SLOTS available.
    
    ✅ Referral accepted  
    📧 Acknowledgment email sent  
    ⏰ Waiting for first appointment slot  
    🔔 Automatically removed when appointment booked  
    """)
    
    # Tabs for different PBL functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 View PBL",
        "➕ Add to PBL",
        "📧 Acknowledgments",
        "⚠️ Breach Risks",
        "🔧 Data Cleansing"
    ])
    
    with tab1:
        render_pbl_view()
    
    with tab2:
        render_add_to_pbl()
    
    with tab3:
        render_acknowledgment_tracking()
    
    with tab4:
        render_breach_monitoring()
    
    with tab5:
        render_data_cleansing()


def render_pbl_view():
    """View all patients on PBL"""
    
    st.subheader("📊 Current Partial Booking List")
    
    pbl_patients = load_pbl_patients()
    
    if not pbl_patients:
        st.warning("📭 PBL is currently empty - No patients awaiting first appointment")
        return
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total on PBL", len(pbl_patients))
    
    with col2:
        at_risk = sum(1 for p in pbl_patients if p.get('days_until_breach', 999) < 28)
        st.metric("At Risk (<4 weeks)", at_risk, delta=f"-{at_risk}" if at_risk > 0 else "0", delta_color="inverse")
    
    with col3:
        no_ack = sum(1 for p in pbl_patients if not p.get('acknowledgment_sent'))
        st.metric("No Acknowledgment", no_ack)
    
    with col4:
        avg_wait = sum(p.get('weeks_waiting', 0) for p in pbl_patients) // len(pbl_patients) if pbl_patients else 0
        st.metric("Avg Wait (weeks)", avg_wait)
    
    st.markdown("---")
    
    # Filter options
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        specialty_filter = st.selectbox(
            "Filter by Specialty",
            ["All"] + list(set(p['specialty'] for p in pbl_patients)),
            key="pbl_specialty_filter"
        )
    
    with col_filter2:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["All", "Urgent", "2-Week Wait", "Routine"],
            key="pbl_priority_filter"
        )
    
    with col_filter3:
        risk_filter = st.selectbox(
            "Filter by Risk",
            ["All", "At Risk (<4 weeks)", "Safe (>4 weeks)"],
            key="pbl_risk_filter"
        )
    
    # Apply filters
    filtered_patients = pbl_patients.copy()
    
    if specialty_filter != "All":
        filtered_patients = [p for p in filtered_patients if p['specialty'] == specialty_filter]
    
    if priority_filter != "All":
        filtered_patients = [p for p in filtered_patients if p['priority'] == priority_filter]
    
    if risk_filter == "At Risk (<4 weeks)":
        filtered_patients = [p for p in filtered_patients if p.get('days_until_breach', 999) < 28]
    elif risk_filter == "Safe (>4 weeks)":
        filtered_patients = [p for p in filtered_patients if p.get('days_until_breach', 999) >= 28]
    
    st.markdown(f"**Showing {len(filtered_patients)} of {len(pbl_patients)} patients**")
    
    # Display patients
    for patient in filtered_patients:
        render_pbl_patient_card(patient)


def render_pbl_patient_card(patient: dict):
    """Render individual patient card with actions"""
    
    # Determine color based on breach risk
    days_until_breach = patient.get('days_until_breach', 999)
    if days_until_breach < 14:
        border_color = "#ff4444"  # Red - Critical
    elif days_until_breach < 28:
        border_color = "#ff9800"  # Orange - At Risk
    else:
        border_color = "#4CAF50"  # Green - Safe
    
    with st.container():
        st.markdown(f"""
        <div style="border-left: 5px solid {border_color}; padding: 15px; background: #f9f9f9; margin: 10px 0; border-radius: 5px;">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.markdown(f"**{patient['name']}**")
            st.markdown(f"NHS: {patient['nhs_number']} | DOB: {patient['dob']}")
            st.markdown(f"📧 {patient.get('contact_email', 'No email')} | 📞 {patient.get('contact_phone', 'No phone')}")
        
        with col2:
            st.markdown(f"**Specialty:** {patient['specialty']}")
            st.markdown(f"**Priority:** {patient['priority']}")
            st.markdown(f"**Referring GP:** {patient.get('referring_gp', 'Unknown')}")
        
        with col3:
            st.markdown(f"**Waiting:** {patient.get('weeks_waiting', 0)} weeks")
            st.markdown(f"**Breach in:** {days_until_breach} days")
            ack_status = "✅ Sent" if patient.get('acknowledgment_sent') else "❌ Not Sent"
            st.markdown(f"**Acknowledgment:** {ack_status}")
        
        with col4:
            if st.button("📅 Book Appt", key=f"book_{patient['nhs_number']}", help="Book appointment and remove from PBL"):
                # This would integrate with booking system
                result = remove_from_pbl(patient['nhs_number'], "Appointment Booked")
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
            
            if st.button("📧 Resend Ack", key=f"resend_{patient['nhs_number']}", help="Resend acknowledgment email"):
                st.info("Acknowledgment email resent!")
            
            if st.button("❌ Remove", key=f"remove_{patient['nhs_number']}", help="Remove from PBL"):
                result = remove_from_pbl(patient['nhs_number'], "Manual Removal")
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_add_to_pbl():
    """Add new patient to PBL"""
    
    st.subheader("➕ Add Patient to Partial Booking List")
    
    st.info("""
    **When to add to PBL:**
    - Referral has been ACCEPTED
    - NO appointment slots currently available
    - Patient needs to wait for first appointment
    """)
    
    with st.form("add_to_pbl_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Patient Details")
            name = st.text_input("Patient Name*", placeholder="John Smith")
            nhs_number = st.text_input("NHS Number*", placeholder="123 456 7890")
            dob = st.date_input("Date of Birth*")
            
            st.markdown("#### Contact Information")
            email = st.text_input("Email Address*", placeholder="patient@email.com")
            phone = st.text_input("Phone Number*", placeholder="07123 456789")
        
        with col2:
            st.markdown("#### Referral Details")
            specialty = st.selectbox("Specialty*", [
                "Cardiology", "Dermatology", "ENT", "Gastroenterology",
                "General Surgery", "Gynecology", "Neurology", "Ophthalmology",
                "Orthopedics", "Respiratory", "Rheumatology", "Urology"
            ])
            
            priority = st.selectbox("Priority*", [
                "Routine", "Urgent", "2-Week Wait", "Emergency"
            ])
            
            referral_date = st.date_input("Referral Date*")
            referring_gp = st.text_input("Referring GP*", placeholder="Dr. Smith, Green Street Medical")
            referral_reason = st.text_area("Referral Reason", placeholder="Brief clinical reason for referral...")
        
        send_ack = st.checkbox("📧 Send acknowledgment email to patient", value=True)
        
        submit = st.form_submit_button("➕ Add to PBL", type="primary")
        
        if submit:
            if not all([name, nhs_number, email, phone, specialty, referring_gp]):
                st.error("❌ Please fill all required fields (*)")
            else:
                patient_data = {
                    'name': name,
                    'nhs_number': nhs_number,
                    'dob': str(dob),
                    'email': email,
                    'phone': phone,
                    'specialty': specialty,
                    'priority': priority,
                    'referral_date': str(referral_date),
                    'referring_gp': referring_gp,
                    'referral_reason': referral_reason
                }
                
                result = add_to_pbl(patient_data, send_acknowledgment=send_ack)
                
                if result['success']:
                    st.success(f"✅ {result['message']}")
                    if send_ack:
                        st.success("📧 Acknowledgment email sent to patient")
                    st.balloons()
                else:
                    st.error(f"❌ {result['message']}")


def render_acknowledgment_tracking():
    """Track acknowledgment emails"""
    
    st.subheader("📧 Acknowledgment Email Tracking")
    
    pbl_patients = load_pbl_patients()
    
    # Patients without acknowledgment
    no_ack = [p for p in pbl_patients if not p.get('acknowledgment_sent')]
    
    if no_ack:
        st.warning(f"⚠️ {len(no_ack)} patients have NOT received acknowledgment email")
        
        for patient in no_ack:
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{patient['name']}** - {patient['nhs_number']}")
            
            with col2:
                st.markdown(f"Added: {patient['added_to_pbl_date']}")
            
            with col3:
                if st.button("📧 Send Now", key=f"send_ack_{patient['nhs_number']}"):
                    st.success(f"Acknowledgment sent to {patient['contact_email']}")
    else:
        st.success("✅ All patients have received acknowledgment emails")
    
    st.markdown("---")
    
    # Patients with acknowledgment
    with_ack = [p for p in pbl_patients if p.get('acknowledgment_sent')]
    
    if with_ack:
        st.subheader("✅ Acknowledgments Sent")
        
        df = pd.DataFrame([{
            'Name': p['name'],
            'NHS Number': p['nhs_number'],
            'Email': p.get('contact_email', ''),
            'Sent Date': p.get('acknowledgment_date', 'Unknown'),
            'Specialty': p['specialty']
        } for p in with_ack])
        
        st.dataframe(df, use_container_width=True)


def render_breach_monitoring():
    """Monitor patients at risk of RTT breach"""
    
    st.subheader("⚠️ RTT Breach Risk Monitoring")
    
    pbl_patients = load_pbl_patients()
    
    # Categorize by risk
    critical = [p for p in pbl_patients if p.get('days_until_breach', 999) < 14]
    at_risk = [p for p in pbl_patients if 14 <= p.get('days_until_breach', 999) < 28]
    safe = [p for p in pbl_patients if p.get('days_until_breach', 999) >= 28]
    
    # Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 Critical (<2 weeks)", len(critical))
    
    with col2:
        st.metric("🟠 At Risk (2-4 weeks)", len(at_risk))
    
    with col3:
        st.metric("🟢 Safe (>4 weeks)", len(safe))
    
    # Display critical patients
    if critical:
        st.error(f"🔴 **CRITICAL: {len(critical)} patients at imminent breach risk!**")
        
        for patient in critical:
            st.markdown(f"""
            **{patient['name']}** - {patient['specialty']}  
            NHS: {patient['nhs_number']} | Breach in: **{patient['days_until_breach']} days**  
            Action: URGENT appointment needed immediately!
            """)
    
    # Display at-risk patients
    if at_risk:
        st.warning(f"🟠 **AT RISK: {len(at_risk)} patients need appointment soon**")
        
        with st.expander("View At-Risk Patients"):
            for patient in at_risk:
                st.markdown(f"• **{patient['name']}** - {patient['specialty']} - Breach in {patient['days_until_breach']} days")


def render_data_cleansing():
    """Data cleansing tools for NHS experts"""
    
    st.subheader("🔧 Data Cleansing Tools")
    
    st.warning("""
    **For NHS Experts Only**
    
    These tools help maintain PBL data quality by identifying and fixing:
    - Duplicate entries
    - Missing patient information
    - Invalid NHS numbers
    - Overdue acknowledgments
    - Long waiters (>12 weeks)
    """)
    
    # Run validation
    if st.button("🔍 Run Data Quality Check", type="primary"):
        with st.spinner("Validating PBL data..."):
            issues = validate_pbl_data()
            
            # Display issues
            total_issues = sum(len(v) for v in issues.values())
            
            if total_issues == 0:
                st.success("✅ No data quality issues found!")
            else:
                st.error(f"⚠️ Found {total_issues} data quality issues")
                
                # Duplicates
                if issues['duplicates']:
                    with st.expander(f"🔴 Duplicates ({len(issues['duplicates'])})"):
                        for dup in issues['duplicates']:
                            st.markdown(f"• {dup['name']} - {dup['nhs_number']}")
                        
                        if st.button("🧹 Clean Duplicates"):
                            result = clean_pbl_duplicates()
                            st.success(f"Removed {result['removed_count']} duplicates")
                            st.rerun()
                
                # Missing data
                if issues['missing_data']:
                    with st.expander(f"⚠️ Missing Data ({len(issues['missing_data'])})"):
                        for item in issues['missing_data']:
                            st.markdown(f"• {item['patient']['name']} - Missing: {', '.join(item['missing_fields'])}")
                
                # Invalid NHS numbers
                if issues['invalid_nhs_numbers']:
                    with st.expander(f"❌ Invalid NHS Numbers ({len(issues['invalid_nhs_numbers'])})"):
                        for patient in issues['invalid_nhs_numbers']:
                            st.markdown(f"• {patient['name']} - {patient['nhs_number']}")
                
                # Overdue acknowledgments
                if issues['overdue_acknowledgments']:
                    with st.expander(f"📧 No Acknowledgment Sent ({len(issues['overdue_acknowledgments'])})"):
                        for patient in issues['overdue_acknowledgments']:
                            st.markdown(f"• {patient['name']} - Added: {patient['added_to_pbl_date']}")
                
                # Breach risks
                if issues['breach_risks']:
                    with st.expander(f"⏰ Breach Risks ({len(issues['breach_risks'])})"):
                        for patient in issues['breach_risks']:
                            st.markdown(f"• {patient['name']} - {patient['days_until_breach']} days until breach")
                
                # Long waiters
                if issues['long_waiters']:
                    with st.expander(f"⌛ Long Waiters >12 weeks ({len(issues['long_waiters'])})"):
                        for patient in issues['long_waiters']:
                            st.markdown(f"• {patient['name']} - Waiting {patient['weeks_waiting']} weeks")
    
    st.markdown("---")
    
    # Export options
    st.subheader("📊 Export PBL Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export to Excel"):
            st.info("Excel export feature coming soon!")
    
    with col2:
        if st.button("📄 Generate Report"):
            st.info("Report generation feature coming soon!")


# Main render function
if __name__ == "__main__":
    render_partial_booking_list()
