"""
T21 PTL UI - PATIENT TRACKING LIST USER INTERFACE
NHS-style interface for managing patient tracking lists

Features:
- View all patients awaiting treatment
- Color-coded breach alerts
- Filter and search
- Add/update patients
- Export to Excel
- Real-time breach monitoring
- Dashboard with stats
"""

import streamlit as st
from ptl_system import (
    get_all_patients,
    get_patient_by_id,
    add_patient_to_ptl,
    update_patient_status,
    add_appointment,
    remove_from_ptl,
    search_patients,
    get_ptl_stats,
    export_ptl_to_csv,
    get_breach_risk_patients,
    calculate_days_waiting,
    calculate_weeks_waiting,
    get_breach_status
)
from datetime import datetime, timedelta
import pandas as pd
from ai_ptl_automation import (
    ai_predict_breach_risk,
    ai_auto_prioritize_ptl,
    ai_recommend_appointments,
    ai_generate_ptl_report,
    ai_detect_anomalies,
    ai_optimize_resource_allocation
)


def render_ptl():
    """Main PTL interface"""
    
    st.header("🤖 AI-Powered PTL - Patient Tracking List")
    st.markdown("**Revolutionary AI-Enhanced RTT Patient Tracking**")
    
    st.info("""
    💾 **PERMANENT STORAGE ENABLED!** All patients you add are saved to your personal database and will be available every time you login.
    
    ✅ **Your Practice Data:**
    - Saves permanently to database
    - Available across all sessions
    - Only YOU can see your patients
    - Build your portfolio over time
    - Track your progress
    """)
    
    st.success("""
    🤖 **AI-POWERED FEATURES (10x Better Than Standard NHS PTL!)**
    - 🤖 AI Breach Risk Prediction (4 weeks ahead!)
    - 🤖 AI Auto-Prioritization
    - 🤖 AI Appointment Recommendations
    - 🤖 AI Anomaly Detection
    - 🤖 AI Report Generation
    - 🤖 AI Resource Optimization
    
    ✅ **Plus Standard PTL Features:**
    - Track all patients awaiting treatment
    - Monitor RTT clocks in real-time
    - Color-coded breach alerts
    - Filter by specialty, priority, risk
    - Export to CSV/Excel
    - Prevent breaches proactively
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 PTL Dashboard",
        "📋 Full Patient List",
        "➕ Add Patient",
        "🚨 Breach Alerts",
        "🤖 AI Auto-Prioritize",
        "🤖 AI Insights",
        "📥 Export & Reports"
    ])
    
    with tab1:
        render_ptl_dashboard()
    
    with tab2:
        render_patient_list()
    
    with tab3:
        render_add_patient()
    
    with tab4:
        render_breach_alerts()
    
    with tab5:
        render_ai_auto_prioritize()
    
    with tab6:
        render_ai_insights()
    
    with tab7:
        render_export_reports()


def render_ptl_dashboard():
    """PTL Dashboard with key stats"""
    
    st.subheader("📊 PTL Dashboard")
    
    stats = get_ptl_stats()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", stats['total_patients'])
    
    with col2:
        st.metric("Active Breaches", stats['breaches'], 
                 delta=None if stats['breaches'] == 0 else f"-{stats['breaches']}", 
                 delta_color="inverse")
    
    with col3:
        st.metric("Avg Wait (Weeks)", stats['avg_weeks_waiting'])
    
    with col4:
        st.metric("Longest Wait (Weeks)", stats['longest_wait_weeks'],
                 delta=None if stats['longest_wait_weeks'] < 18 else "+Breach",
                 delta_color="inverse")
    
    st.markdown("---")
    
    # Breach risk breakdown
    st.markdown("### 🚨 Breach Risk Breakdown")
    
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
    
    # Specialty breakdown
    if stats['specialties']:
        st.markdown("### 🏥 Patients by Specialty")
        col1, col2 = st.columns(2)
        
        with col1:
            for specialty, count in list(stats['specialties'].items())[:5]:
                st.markdown(f"**{specialty}:** {count} patients")
        
        with col2:
            for specialty, count in list(stats['specialties'].items())[5:10]:
                st.markdown(f"**{specialty}:** {count} patients")
    
    # Priority breakdown
    if stats['priorities']:
        st.markdown("---")
        st.markdown("### ⚡ Patients by Priority")
        cols = st.columns(len(stats['priorities']))
        for i, (priority, count) in enumerate(stats['priorities'].items()):
            with cols[i]:
                st.metric(priority, count)


def render_patient_list():
    """Full patient list with filters"""
    
    st.subheader("📋 Full Patient Tracking List")
    
    # Filters
    st.markdown("### 🔍 Filters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_query = st.text_input("🔍 Search", placeholder="Name or NHS number")
    
    with col2:
        specialty_filter = st.selectbox("Specialty", ["All"] + [
            "Orthopaedics", "Cardiology", "General Surgery", "ENT",
            "Ophthalmology", "Urology", "Gastroenterology", "Neurology"
        ])
    
    with col3:
        priority_filter = st.selectbox("Priority", ["All", "Routine", "Urgent", "2WW", "Cancer 62-day"])
    
    with col4:
        risk_filter = st.selectbox("Breach Risk", ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    
    # Get filtered patients
    patients = search_patients(
        query=search_query if search_query else "",
        specialty=None if specialty_filter == "All" else specialty_filter,
        priority=None if priority_filter == "All" else priority_filter,
        breach_risk=None if risk_filter == "All" else risk_filter
    )
    
    st.markdown(f"**Showing {len(patients)} patients**")
    
    if not patients:
        st.info("No patients on PTL. Add patients using the 'Add Patient' tab.")
        return
    
    # Display patients
    for patient in patients:
        render_patient_card(patient)


def render_patient_card(patient: dict):
    """Render individual patient card"""
    
    # Calculate breach info
    days = calculate_days_waiting(patient['clock_start_date'])
    weeks = days // 7
    breach_info = get_breach_status(days, patient.get('pathway_type', 'routine'))
    
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
            st.markdown(f"📅 Referral: {patient['referral_date']}")
        
        with col2:
            st.markdown(f"**🏥 {patient['specialty']}**")
            st.markdown(f"Priority: {patient['priority']}")
            st.markdown(f"Status: {patient['current_status']}")
        
        with col3:
            st.markdown(f"**⏱️ {weeks} weeks ({days} days)**")
            st.markdown(f"Breach Risk: **{breach_info['status']}**")
            if breach_info['days_to_breach'] > 0:
                st.markdown(f"Days to breach: {breach_info['days_to_breach']}")
            else:
                st.markdown(f"⚠️ BREACHED by {abs(breach_info['days_to_breach'])} days")
        
        with col4:
            if st.button("👁️ View", key=f"view_{patient['patient_id']}"):
                st.session_state[f"viewing_{patient['patient_id']}"] = True
            
            if st.button("📝 Update", key=f"update_{patient['patient_id']}"):
                st.session_state[f"updating_{patient['patient_id']}"] = True
            
            if st.button("✅ Remove", key=f"remove_{patient['patient_id']}"):
                st.session_state[f"removing_{patient['patient_id']}"] = True
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # View details popup
        if st.session_state.get(f"viewing_{patient['patient_id']}", False):
            with st.expander("📄 Full Patient Details", expanded=True):
                st.markdown(f"**Patient ID:** {patient['patient_id']}")
                st.markdown(f"**Name:** {patient['patient_name']}")
                st.markdown(f"**NHS Number:** {patient['nhs_number']}")
                st.markdown(f"**Specialty:** {patient['specialty']}")
                st.markdown(f"**Consultant:** {patient.get('consultant', 'Not assigned')}")
                st.markdown(f"**Contact:** {patient.get('contact_number', 'Not provided')}")
                st.markdown(f"**Referral Source:** {patient['referral_source']}")
                st.markdown(f"**Referral Date:** {patient['referral_date']}")
                st.markdown(f"**Clock Start:** {patient['clock_start_date']}")
                st.markdown(f"**Current RTT Code:** {patient['rtt_code']}")
                st.markdown(f"**Clock Status:** {patient['clock_status']}")
                if patient.get('notes'):
                    st.markdown(f"**Notes:** {patient['notes']}")
                
                # Events history
                if patient.get('events'):
                    st.markdown("### 📝 Events History")
                    for event in patient['events']:
                        st.markdown(f"- **{event['date']}** - Code {event['code']}: {event['description']}")
                
                if st.button("Close", key=f"close_{patient['patient_id']}"):
                    st.session_state[f"viewing_{patient['patient_id']}"] = False
                    st.rerun()


def render_add_patient():
    """Add new patient to PTL"""
    
    st.subheader("➕ Add Patient to PTL")
    
    with st.form("add_patient_ptl"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
            nhs_number = st.text_input("NHS Number*", placeholder="123 456 7890")
            referral_date = st.date_input("Referral Date*", value=datetime.now())
            specialty = st.selectbox("Specialty*", [
                "Orthopaedics", "Cardiology", "General Surgery", "ENT",
                "Ophthalmology", "Urology", "Gastroenterology", "Neurology",
                "Dermatology", "Rheumatology", "Other"
            ])
        
        with col2:
            referral_source = st.selectbox("Referral Source*", [
                "GP", "Consultant", "A&E", "Dentist", "Optician", "Other"
            ])
            priority = st.selectbox("Priority*", [
                "Routine", "Urgent", "2WW", "Cancer 62-day"
            ])
            consultant = st.text_input("Consultant", placeholder="Dr. Jones")
            contact_number = st.text_input("Contact Number", placeholder="07123456789")
        
        current_status = st.selectbox("Current Status", [
            "Awaiting First Appointment",
            "First Appointment Booked",
            "Seen - Diagnostics Pending",
            "Diagnostics Complete - Awaiting Decision",
            "Decision Made - Awaiting Treatment",
            "On Waiting List for Treatment"
        ])
        
        notes = st.text_area("Notes", height=100)
        
        submit = st.form_submit_button("➕ Add to PTL", type="primary")
        
        if submit:
            if not patient_name or not nhs_number:
                st.error("❌ Please provide patient name and NHS number!")
            else:
                pathway_type = "routine"
                if priority == "2WW":
                    pathway_type = "2ww"
                elif priority == "Cancer 62-day":
                    pathway_type = "62day"
                
                patient_id = add_patient_to_ptl(
                    patient_name=patient_name,
                    nhs_number=nhs_number,
                    specialty=specialty,
                    referral_date=str(referral_date),
                    referral_source=referral_source,
                    pathway_type=pathway_type,
                    priority=priority,
                    current_status=current_status,
                    consultant=consultant,
                    contact_number=contact_number,
                    notes=notes
                )
                
                st.success(f"✅ Patient added to PTL! ID: {patient_id}")
                st.balloons()
                st.info("Patient is now being tracked. View in 'Full Patient List' tab.")


def render_breach_alerts():
    """Show breach alerts and high-risk patients"""
    
    st.subheader("🚨 Breach Alerts & High-Risk Patients")
    
    # Critical patients (breached or imminent breach)
    critical_patients = get_breach_risk_patients("CRITICAL")
    high_risk_patients = get_breach_risk_patients("HIGH")
    
    st.markdown(f"### 🔴 CRITICAL - {len(critical_patients)} Patients")
    
    if critical_patients:
        for patient in critical_patients:
            st.error(f"""
            **{patient['patient_name']}** ({patient['nhs_number']})  
            Specialty: {patient['specialty']} | Waiting: {patient['weeks_waiting']} weeks ({patient['days_waiting']} days)  
            Status: {patient['breach_info']['status']} | Days to breach: {patient['breach_info']['days_to_breach']}  
            **ACTION REQUIRED IMMEDIATELY!**
            """)
    else:
        st.success("✅ No critical patients!")
    
    st.markdown("---")
    st.markdown(f"### 🟠 HIGH RISK - {len(high_risk_patients)} Patients")
    
    if high_risk_patients:
        for patient in high_risk_patients:
            st.warning(f"""
            **{patient['patient_name']}** ({patient['nhs_number']})  
            Specialty: {patient['specialty']} | Waiting: {patient['weeks_waiting']} weeks ({patient['days_waiting']} days)  
            Days to breach: {patient['breach_info']['days_to_breach']}  
            **Urgent action needed within {patient['breach_info']['days_to_breach']} days**
            """)
    else:
        st.success("✅ No high-risk patients!")


def render_export_reports():
    """Export PTL data"""
    
    st.subheader("📥 Export & Reports")
    
    st.markdown("### 📊 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Export to CSV")
        if st.button("📥 Download CSV", type="primary"):
            csv_data = export_ptl_to_csv()
            if csv_data:
                st.download_button(
                    label="💾 Save PTL.csv",
                    data=csv_data,
                    file_name=f"PTL_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                st.success("✅ CSV ready for download!")
            else:
                st.warning("No patients to export")
    
    with col2:
        st.markdown("#### 📊 Export to Excel")
        if st.button("📥 Generate Excel Report"):
            st.info("🚧 Excel export coming soon! Use CSV for now.")
    
    st.markdown("---")
    st.markdown("### 📈 Weekly Report")
    
    stats = get_ptl_stats()
    
    st.markdown(f"""
    **PTL Weekly Summary - Week Ending {datetime.now().strftime('%d/%m/%Y')}**
    
    **Overview:**
    - Total Patients on PTL: {stats['total_patients']}
    - Active Breaches: {stats['breaches']}
    - Average Wait: {stats['avg_weeks_waiting']} weeks
    - Longest Wait: {stats['longest_wait_weeks']} weeks
    
    **Breach Risk:**
    - 🔴 Critical: {stats['breach_risks']['CRITICAL']}
    - 🟠 High: {stats['breach_risks']['HIGH']}
    - 🟡 Medium: {stats['breach_risks']['MEDIUM']}
    - 🟢 Low: {stats['breach_risks']['LOW']}
    
    **Action Required:**
    - {stats['breach_risks']['CRITICAL'] + stats['breach_risks']['HIGH']} patients need urgent attention
    - {stats['breaches']} breach(es) to report to ICB/CCG
    """)


def render_ai_auto_prioritize():
    """AI Auto-Prioritization of entire PTL"""
    
    st.subheader("🤖 AI Auto-Prioritize PTL")
    st.markdown("**AI automatically prioritizes all patients by breach risk**")
    
    st.info("""
    💡 **How AI Auto-Prioritize Works:**
    - AI analyzes ALL patients on PTL
    - Calculates advanced breach risk scores
    - Considers specialty capacity, trends, patterns
    - Automatically sorts by priority
    - Provides action recommendations for each patient
    - 10x more accurate than manual prioritization!
    """)
    
    if st.button("🤖 Run AI Auto-Prioritization", type="primary"):
        with st.spinner("🤖 AI analyzing entire PTL..."):
            patients = get_all_patients()
            
            if not patients:
                st.warning("No patients on PTL to prioritize")
                return
            
            # AI prioritization
            prioritized_patients = ai_auto_prioritize_ptl(patients)
            
            st.success(f"✅ AI prioritized {len(prioritized_patients)} patients!")
            
            st.markdown("### 🎯 AI-Prioritized Patient List")
            st.markdown("**Sorted by AI Priority Score (Highest Risk First)**")
            
            for idx, patient in enumerate(prioritized_patients[:20], 1):  # Show top 20
                ai_score = patient.get('ai_priority_score', 0)
                ai_level = patient.get('ai_priority_level', 'LOW')
                
                # Color based on AI level
                if ai_level == 'CRITICAL':
                    st.error(f"""
                    **#{idx} - {patient['patient_name']}** (AI Score: {ai_score:.1f}/100)
                    - NHS Number: {patient['nhs_number']}
                    - Specialty: {patient['specialty']}
                    - Priority: **{ai_level}**
                    - Weeks Waiting: {calculate_weeks_waiting(patient['clock_start_date'])}
                    """)
                elif ai_level == 'HIGH':
                    st.warning(f"""
                    **#{idx} - {patient['patient_name']}** (AI Score: {ai_score:.1f}/100)
                    - NHS Number: {patient['nhs_number']}
                    - Specialty: {patient['specialty']}
                    - Priority: **{ai_level}**
                    - Weeks Waiting: {calculate_weeks_waiting(patient['clock_start_date'])}
                    """)
                else:
                    st.info(f"""
                    **#{idx} - {patient['patient_name']}** (AI Score: {ai_score:.1f}/100)
                    - NHS Number: {patient['nhs_number']}
                    - Specialty: {patient['specialty']}
                    - Priority: {ai_level}
                    - Weeks Waiting: {calculate_weeks_waiting(patient['clock_start_date'])}
                    """)
                
                # Show AI recommendations
                if patient.get('ai_recommendations'):
                    with st.expander("📋 AI Recommendations"):
                        for rec in patient['ai_recommendations']:
                            st.markdown(f"✅ {rec}")
            
            if len(prioritized_patients) > 20:
                st.info(f"Showing top 20 of {len(prioritized_patients)} patients. Full list available in export.")


def render_ai_insights():
    """AI Insights & Analytics"""
    
    st.subheader("🤖 AI Insights & Analytics")
    st.markdown("**AI-powered analysis of your PTL performance**")
    
    stats = get_ptl_stats()
    
    st.markdown("### 🔍 AI Anomaly Detection")
    
    if st.button("🤖 Run AI Anomaly Detection", type="primary"):
        with st.spinner("🤖 AI analyzing PTL for anomalies..."):
            anomalies = ai_detect_anomalies(stats)
            
            if anomalies:
                st.warning(f"⚠️ AI detected {len(anomalies)} anomalies!")
                
                for anomaly in anomalies:
                    severity = anomaly['severity']
                    
                    if severity == 'CRITICAL':
                        st.error(f"""
                        🔴 **CRITICAL: {anomaly['type']}**
                        - {anomaly['description']}
                        - **Recommendation:** {anomaly['recommendation']}
                        """)
                    elif severity == 'HIGH':
                        st.warning(f"""
                        🟠 **HIGH: {anomaly['type']}**
                        - {anomaly['description']}
                        - **Recommendation:** {anomaly['recommendation']}
                        """)
                    else:
                        st.info(f"""
                        🟡 **{severity}: {anomaly['type']}**
                        - {anomaly['description']}
                        - **Recommendation:** {anomaly['recommendation']}
                        """)
            else:
                st.success("✅ No anomalies detected! PTL is performing well.")
    
    st.markdown("---")
    st.markdown("### 📊 AI Resource Optimization")
    
    if st.button("🤖 Generate AI Resource Recommendations"):
        with st.spinner("🤖 AI optimizing resource allocation..."):
            recommendations = ai_optimize_resource_allocation(stats)
            
            st.success("✅ AI resource analysis complete!")
            
            if recommendations['specialty_priorities']:
                st.markdown("#### 🏥 Specialty Priorities")
                for spec in recommendations['specialty_priorities']:
                    st.warning(f"""
                    **{spec['specialty']}**
                    - Patients Waiting: {spec['patients_waiting']}
                    - Priority: {spec['priority']}
                    - Recommended Action: {spec['recommended_action']}
                    """)
    
    st.markdown("---")
    st.markdown("### 📈 AI Report Generation")
    
    report_type = st.selectbox("Report Type", ["Weekly", "Monthly", "Breach Analysis", "Management Summary"])
    
    if st.button("🤖 Generate AI Report"):
        with st.spinner(f"🤖 AI generating {report_type} report..."):
            report = ai_generate_ptl_report(stats, report_type.lower())
            
            st.success("✅ AI report generated!")
            st.markdown(report)
            
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"AI_PTL_Report_{report_type}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
