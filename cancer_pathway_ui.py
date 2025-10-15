"""
T21 CANCER PATHWAY UI
User interface for cancer pathway management

Features:
- Cancer PTL dashboard
- 2WW and 62-day pathway tracking
- AI breach prediction
- Milestone tracking
- Cancer data reporting
"""

import streamlit as st
from cancer_pathway_system import (
    get_all_cancer_patients,
    get_cancer_patient_by_id,
    add_cancer_patient,
    add_cancer_milestone,
    search_cancer_patients,
    get_cancer_ptl_stats,
    export_cancer_ptl_to_csv,
    calculate_cancer_days_waiting,
    get_cancer_breach_status,
    ai_predict_cancer_breach,
    CANCER_TYPES,
    CANCER_MILESTONES
)
from datetime import datetime, timedelta


def render_cancer_pathways():
    """Main cancer pathway interface"""
    
    st.header("🎗️ Cancer Pathway Management")
    st.markdown("**AI-Powered 2WW & 62-Day Cancer Pathway Tracking**")
    
    st.success("""
    🎗️ **Cancer Pathway Excellence**
    - 2-Week Wait (2WW) tracking
    - 62-Day cancer pathway management
    - 31-Day decision-to-treat tracking
    - AI breach prediction (cancer-specific!)
    - Milestone tracking
    - Automated cancer reporting
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Cancer PTL Dashboard",
        "📋 Cancer Patient List",
        "➕ Add Cancer Patient",
        "🚨 Cancer Breach Alerts",
        "📥 Cancer Reports"
    ])
    
    with tab1:
        render_cancer_dashboard()
    
    with tab2:
        render_cancer_patient_list()
    
    with tab3:
        render_add_cancer_patient()
    
    with tab4:
        render_cancer_breach_alerts()
    
    with tab5:
        render_cancer_reports()


def render_cancer_dashboard():
    """Cancer PTL dashboard"""
    
    st.subheader("📊 Cancer PTL Dashboard")
    
    # UNIVERSAL DEBUG PANEL
    try:
        from universal_debug_panel import show_universal_debug_info
        show_universal_debug_info()
    except:
        pass
    
    stats = get_cancer_ptl_stats()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cancer Patients", stats['total_patients'])
    
    with col2:
        st.metric("Active Pathways", stats['active_pathways'])
    
    with col3:
        st.metric("2WW Breaches", stats['2ww_breaches'],
                 delta=None if stats['2ww_breaches'] == 0 else f"-{stats['2ww_breaches']}",
                 delta_color="inverse")
    
    with col4:
        st.metric("62-Day Breaches", stats['62day_breaches'],
                 delta=None if stats['62day_breaches'] == 0 else f"-{stats['62day_breaches']}",
                 delta_color="inverse")
    
    st.markdown("---")
    
    # Breach risk breakdown
    st.markdown("### 🚨 Cancer Breach Risk Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 CRITICAL", stats['breach_risks']['CRITICAL'])
    
    with col2:
        st.metric("🟠 HIGH", stats['breach_risks']['HIGH'])
    
    with col3:
        st.metric("🟡 MEDIUM", stats['breach_risks']['MEDIUM'])
    
    with col4:
        st.metric("🟢 LOW", stats['breach_risks']['LOW'])
    
    st.markdown("---")
    
    # Cancer types breakdown
    if stats['cancer_types']:
        st.markdown("### 🎗️ Patients by Cancer Type")
        col1, col2 = st.columns(2)
        
        with col1:
            for cancer_type, count in list(stats['cancer_types'].items())[:5]:
                st.markdown(f"**{cancer_type}:** {count} patients")
        
        with col2:
            for cancer_type, count in list(stats['cancer_types'].items())[5:10]:
                st.markdown(f"**{cancer_type}:** {count} patients")
    
    # Pathway types
    if stats['pathway_types']:
        st.markdown("---")
        st.markdown("### ⏱️ Patients by Pathway Type")
        cols = st.columns(len(stats['pathway_types']))
        for i, (pathway, count) in enumerate(stats['pathway_types'].items()):
            with cols[i]:
                st.metric(pathway.upper(), count)


def render_cancer_patient_list():
    """Cancer patient list with filters"""
    
    st.subheader("📋 Cancer Patient List")
    
    # Filters
    st.markdown("### 🔍 Filters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_query = st.text_input("🔍 Search", placeholder="Name or NHS number")
    
    with col2:
        cancer_type_filter = st.selectbox("Cancer Type", ["All"] + CANCER_TYPES)
    
    with col3:
        pathway_filter = st.selectbox("Pathway Type", ["All", "2WW", "62-Day", "31-Day"])
    
    with col4:
        risk_filter = st.selectbox("Breach Risk", ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    
    # Get filtered patients
    patients = search_cancer_patients(
        query=search_query if search_query else "",
        cancer_type=None if cancer_type_filter == "All" else cancer_type_filter,
        pathway_type=None if pathway_filter == "All" else pathway_filter.lower().replace('-', ''),
        breach_risk=None if risk_filter == "All" else risk_filter
    )
    
    st.markdown(f"**Showing {len(patients)} cancer patients**")
    
    if not patients:
        st.info("No cancer patients on PTL. Add patients using the 'Add Cancer Patient' tab.")
        return
    
    # Display patients
    for patient in patients:
        render_cancer_patient_card(patient)


def render_cancer_patient_card(patient: dict):
    """Render individual cancer patient card"""
    
    # Calculate breach info - use helper function for field compatibility
    from cancer_pathway_system import get_pathway_start_date
    days = calculate_cancer_days_waiting(get_pathway_start_date(patient))
    breach_info = get_cancer_breach_status(days, patient['pathway_type'])
    
    # Color based on breach risk
    if breach_info['color'] == 'red':
        border_color = "#ff4444"
        bg_color = "#ffe6e6"
    elif breach_info['color'] == 'orange':
        border_color = "#ff8800"
        bg_color = "#fff4e6"
    elif breach_info['color'] == 'yellow':
        border_color = "#ffcc00"
        bg_color = "#fffaeb"
    else:
        border_color = "#44ff44"
        bg_color = "#e6ffe6"
    
    with st.container():
        st.markdown(f"""
        <div style="border-left: 5px solid {border_color}; background-color: {bg_color}; padding: 15px; margin-bottom: 10px; border-radius: 5px;">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            st.markdown(f"**👤 {patient['patient_name']}**")
            st.markdown(f"NHS: {patient['nhs_number']}")
            st.markdown(f"🎗️ {patient['cancer_type']}")
        
        with col2:
            st.markdown(f"**Pathway: {patient['pathway_type'].upper()}**")
            st.markdown(f"Referral: {patient['referral_date']}")
            st.markdown(f"Status: {patient['current_status']}")
        
        with col3:
            st.markdown(f"**⏱️ {days} days waiting**")
            st.markdown(f"Breach Risk: **{breach_info['status']}**")
            if breach_info['days_to_breach'] > 0:
                st.markdown(f"Days to breach: {breach_info['days_to_breach']}")
            else:
                st.markdown(f"⚠️ BREACHED by {abs(breach_info['days_to_breach'])} days")
        
        with col4:
            # Get patient ID (compatible with both field names)
            patient_id = patient.get('pathway_id') or patient.get('patient_id')
            st.markdown(f"**Milestones: {len(patient.get('milestones', []))}**")
            if st.button("👁️ View", key=f"view_{patient_id}"):
                st.session_state[f"viewing_{patient_id}"] = True
            
            if st.button("➕ Add Milestone", key=f"milestone_{patient_id}"):
                st.session_state[f"adding_milestone_{patient_id}"] = True
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_add_cancer_patient():
    """Add new cancer patient"""
    
    st.subheader("➕ Add Cancer Patient to PTL")
    
    # Show success message if patient was just added
    if 'cancer_patient_added' in st.session_state:
        patient_info = st.session_state['cancer_patient_added']
        st.success(f"✅ Cancer patient added to PTL! ID: {patient_info['patient_id']}")
        st.balloons()
        st.info(f"**{patient_info['patient_name']}** is now being tracked. View in 'Cancer Patient List' tab.")
        # Clear the flag
        del st.session_state['cancer_patient_added']
    
    with st.form("add_cancer_patient"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
            nhs_number = st.text_input("NHS Number*", placeholder="123 456 7890")
            cancer_type = st.selectbox("Cancer Type*", CANCER_TYPES)
            pathway_type = st.selectbox("Pathway Type*", ["2ww", "62day", "31day"])
            referral_date = st.date_input("Referral Date*", value=datetime.now())
        
        with col2:
            referring_clinician = st.text_input("Referring Clinician*", placeholder="Dr. Jones")
            primary_site = st.text_input("Primary Site", placeholder="e.g., Right Breast")
            suspected_diagnosis = st.text_area("Suspected Diagnosis", height=100)
            urgency = st.selectbox("Urgency", ["Standard", "Urgent", "Emergency"])
            contact_number = st.text_input("Contact Number", placeholder="07123456789")
        
        notes = st.text_area("Clinical Notes", height=100)
        
        submit = st.form_submit_button("➕ Add to Cancer PTL", type="primary")
        
        if submit:
            if not patient_name or not nhs_number or not referring_clinician:
                st.error("❌ Please provide required fields!")
            else:
                patient_id = add_cancer_patient(
                    patient_name=patient_name,
                    nhs_number=nhs_number,
                    cancer_type=cancer_type,
                    pathway_type=pathway_type,
                    referral_date=str(referral_date),
                    referring_clinician=referring_clinician,
                    primary_site=primary_site,
                    suspected_diagnosis=suspected_diagnosis,
                    urgency=urgency,
                    contact_number=contact_number,
                    notes=notes
                )
                
                # Store success message in session state
                st.session_state['cancer_patient_added'] = {
                    'patient_id': patient_id,
                    'patient_name': patient_name
                }
                
                # Force refresh to show new data
                st.rerun()


def render_cancer_breach_alerts():
    """Cancer breach alerts"""
    
    st.subheader("🚨 Cancer Breach Alerts")
    
    # Get critical and high-risk patients
    critical_patients = search_cancer_patients(breach_risk="CRITICAL")
    high_risk_patients = search_cancer_patients(breach_risk="HIGH")
    
    st.markdown(f"### 🔴 CRITICAL - {len(critical_patients)} Patients")
    
    if critical_patients:
        from cancer_pathway_system import get_pathway_start_date
        for patient in critical_patients:
            days = calculate_cancer_days_waiting(get_pathway_start_date(patient))
            breach_info = get_cancer_breach_status(days, patient['pathway_type'])
            
            st.error(f"""
            **{patient['patient_name']}** ({patient['nhs_number']})  
            Cancer: {patient['cancer_type']} | Pathway: {patient['pathway_type'].upper()}  
            Days waiting: {days} | Days to breach: {breach_info['days_to_breach']}  
            Status: {breach_info['status']} | {breach_info['action']}  
            **IMMEDIATE ACTION REQUIRED!**
            """)
    else:
        st.success("✅ No critical cancer patients!")
    
    st.markdown("---")
    st.markdown(f"### 🟠 HIGH RISK - {len(high_risk_patients)} Patients")
    
    if high_risk_patients:
        from cancer_pathway_system import get_pathway_start_date
        for patient in high_risk_patients:
            days = calculate_cancer_days_waiting(get_pathway_start_date(patient))
            breach_info = get_cancer_breach_status(days, patient['pathway_type'])
            
            st.warning(f"""
            **{patient['patient_name']}** ({patient['nhs_number']})  
            Cancer: {patient['cancer_type']} | Pathway: {patient['pathway_type'].upper()}  
            Days waiting: {days} | Days to breach: {breach_info['days_to_breach']}  
            **Urgent action needed within {breach_info['days_to_breach']} days**
            """)
    else:
        st.success("✅ No high-risk cancer patients!")


def render_cancer_reports():
    """Cancer pathway reports"""
    
    st.subheader("📥 Cancer Pathway Reports")
    
    st.markdown("### 📊 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Export to CSV")
        if st.button("📥 Download Cancer PTL CSV", type="primary"):
            csv_data = export_cancer_ptl_to_csv()
            if csv_data:
                st.download_button(
                    label="💾 Save Cancer_PTL.csv",
                    data=csv_data,
                    file_name=f"Cancer_PTL_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                st.success("✅ CSV ready for download!")
            else:
                st.warning("No cancer patients to export")
    
    with col2:
        st.markdown("#### 📊 Cancer Performance Report")
        if st.button("📥 Generate Report"):
            stats = get_cancer_ptl_stats()
            
            report = f"""
# CANCER PATHWAY PERFORMANCE REPORT

**Generated:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

## OVERVIEW
- Total Cancer Patients: {stats['total_patients']}
- Active Pathways: {stats['active_pathways']}
- Completed Pathways: {stats['completed_pathways']}

## BREACH PERFORMANCE
- 2WW Breaches: {stats['2ww_breaches']}
- 62-Day Breaches: {stats['62day_breaches']}
- Total Breaches: {stats['breaches']}

## BREACH RISK
- 🔴 Critical: {stats['breach_risks']['CRITICAL']}
- 🟠 High: {stats['breach_risks']['HIGH']}
- 🟡 Medium: {stats['breach_risks']['MEDIUM']}
- 🟢 Low: {stats['breach_risks']['LOW']}

## ACTIONS REQUIRED
- {stats['breach_risks']['CRITICAL'] + stats['breach_risks']['HIGH']} patients need urgent attention
- {stats['breaches']} breach(es) to report to Cancer Alliance
            """
            
            st.markdown(report)
            
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"Cancer_Report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
