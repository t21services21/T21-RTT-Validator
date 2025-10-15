"""
DATA VALIDATION & ALERTS SYSTEM
Automated data quality checks and alerts

Features:
- Validate pathway data completeness
- Identify missing information
- Breach risk alerts
- Data quality scoring
- Automated warnings
"""

import streamlit as st
from datetime import datetime, timedelta, date
from typing import Dict, List, Tuple
from patient_registration_system import get_all_patients
from pathway_management_system import get_all_pathways
from episode_management_system import get_all_episodes


def validate_patient_data(patient: Dict) -> Tuple[bool, List[str], int]:
    """
    Validate patient data completeness
    Returns: (is_complete, missing_fields, quality_score)
    """
    missing_fields = []
    required_fields = [
        ('nhs_number', 'NHS Number'),
        ('full_name', 'Full Name'),
        ('date_of_birth', 'Date of Birth'),
        ('gender', 'Gender'),
        ('address', 'Address'),
        ('postcode', 'Postcode'),
        ('phone', 'Phone Number'),
        ('email', 'Email'),
        ('gp_name', 'GP Name'),
        ('gp_practice', 'GP Practice'),
        ('next_of_kin_name', 'Next of Kin Name'),
        ('next_of_kin_relationship', 'Next of Kin Relationship'),
        ('next_of_kin_phone', 'Next of Kin Phone')
    ]
    
    for field_key, field_name in required_fields:
        if not patient.get(field_key):
            missing_fields.append(field_name)
    
    total_fields = len(required_fields)
    completed_fields = total_fields - len(missing_fields)
    quality_score = int((completed_fields / total_fields) * 100)
    
    is_complete = len(missing_fields) == 0
    
    return is_complete, missing_fields, quality_score


def validate_pathway_data(pathway: Dict) -> Tuple[bool, List[str], int]:
    """
    Validate pathway data completeness
    Returns: (is_complete, missing_fields, quality_score)
    """
    missing_fields = []
    required_fields = [
        ('patient_id', 'Patient ID'),
        ('patient_name', 'Patient Name'),
        ('pathway_type', 'Pathway Type'),
        ('specialty', 'Specialty'),
        ('consultant', 'Consultant'),
        ('referral_source', 'Referral Source'),
        ('priority', 'Priority'),
        ('clock_start_date', 'Clock Start Date'),
        ('breach_date', 'Breach Date'),
        ('referral_received_date', 'Referral Received Date'),
        ('gp_name', 'GP Name'),
        ('presenting_complaint', 'Presenting Complaint')
    ]
    
    for field_key, field_name in required_fields:
        if not pathway.get(field_key):
            missing_fields.append(field_name)
    
    total_fields = len(required_fields)
    completed_fields = total_fields - len(missing_fields)
    quality_score = int((completed_fields / total_fields) * 100)
    
    is_complete = len(missing_fields) == 0
    
    return is_complete, missing_fields, quality_score


def check_breach_risk(pathway: Dict) -> Dict:
    """
    Check if pathway is at risk of breaching
    Returns alert level and details
    """
    if pathway.get('status') in ['closed', 'completed']:
        return {'alert_level': 'none', 'message': 'Pathway closed'}
    
    breach_date_str = pathway.get('breach_date')
    if not breach_date_str:
        return {'alert_level': 'warning', 'message': 'No breach date set'}
    
    try:
        if isinstance(breach_date_str, str):
            breach_date = datetime.fromisoformat(breach_date_str.replace('Z', '+00:00')).date()
        elif isinstance(breach_date_str, date):
            breach_date = breach_date_str
        else:
            return {'alert_level': 'warning', 'message': 'Invalid breach date format'}
        
        today = datetime.now().date()
        days_remaining = (breach_date - today).days
        
        if days_remaining < 0:
            return {
                'alert_level': 'critical',
                'message': f'BREACHED! {abs(days_remaining)} days overdue',
                'days_remaining': days_remaining
            }
        elif days_remaining <= 7:
            return {
                'alert_level': 'critical',
                'message': f'Critical risk: {days_remaining} days remaining',
                'days_remaining': days_remaining
            }
        elif days_remaining <= 14:
            return {
                'alert_level': 'high',
                'message': f'High risk: {days_remaining} days remaining',
                'days_remaining': days_remaining
            }
        elif days_remaining <= 28:
            return {
                'alert_level': 'medium',
                'message': f'Medium risk: {days_remaining} days remaining',
                'days_remaining': days_remaining
            }
        else:
            return {
                'alert_level': 'low',
                'message': f'Low risk: {days_remaining} days remaining',
                'days_remaining': days_remaining
            }
    
    except Exception as e:
        return {'alert_level': 'warning', 'message': f'Error checking breach: {str(e)}'}


def check_missing_milestones(pathway: Dict) -> List[str]:
    """Check for missing milestone dates"""
    missing_milestones = []
    
    # Check if pathway has been running for a while
    clock_start = pathway.get('clock_start_date')
    if not clock_start:
        return ['Clock Start Date']
    
    try:
        if isinstance(clock_start, str):
            start_date = datetime.fromisoformat(clock_start.replace('Z', '+00:00')).date()
        else:
            start_date = clock_start
        
        days_running = (datetime.now().date() - start_date).days
        
        # Check first appointment (should be within 30 days)
        if days_running > 30 and not pathway.get('first_appointment_date'):
            missing_milestones.append('First Appointment Date (overdue)')
        
        # Check decision to treat (should be within 60 days if first appt done)
        if pathway.get('first_appointment_date') and days_running > 60 and not pathway.get('decision_to_treat_date'):
            missing_milestones.append('Decision to Treat Date')
        
        # Check treatment start (should be within 90 days if DTT done)
        if pathway.get('decision_to_treat_date') and days_running > 90 and not pathway.get('treatment_start_date'):
            missing_milestones.append('Treatment Start Date')
    
    except Exception:
        pass
    
    return missing_milestones


def generate_all_alerts() -> Dict:
    """Generate all data quality alerts"""
    
    patients = get_all_patients()
    pathways = get_all_pathways()
    
    alerts = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': [],
        'data_quality': []
    }
    
    # Check pathways for breach risk
    for pathway in pathways:
        if pathway.get('status') not in ['closed', 'completed']:
            breach_check = check_breach_risk(pathway)
            alert_level = breach_check.get('alert_level')
            
            if alert_level in ['critical', 'high', 'medium']:
                alerts[alert_level].append({
                    'type': 'breach_risk',
                    'pathway_id': pathway.get('pathway_id'),
                    'patient_name': pathway.get('patient_name'),
                    'message': breach_check.get('message'),
                    'days_remaining': breach_check.get('days_remaining')
                })
    
    # Check for incomplete pathway data
    for pathway in pathways:
        if pathway.get('status') not in ['closed', 'completed']:
            is_complete, missing_fields, quality_score = validate_pathway_data(pathway)
            
            if quality_score < 80:
                alerts['data_quality'].append({
                    'type': 'incomplete_pathway',
                    'pathway_id': pathway.get('pathway_id'),
                    'patient_name': pathway.get('patient_name'),
                    'quality_score': quality_score,
                    'missing_fields': missing_fields
                })
    
    # Check for missing milestones
    for pathway in pathways:
        if pathway.get('status') not in ['closed', 'completed']:
            missing_milestones = check_missing_milestones(pathway)
            
            if missing_milestones:
                alerts['medium'].append({
                    'type': 'missing_milestones',
                    'pathway_id': pathway.get('pathway_id'),
                    'patient_name': pathway.get('patient_name'),
                    'missing_milestones': missing_milestones
                })
    
    # Check for incomplete patient data
    for patient in patients:
        is_complete, missing_fields, quality_score = validate_patient_data(patient)
        
        if quality_score < 70:
            alerts['data_quality'].append({
                'type': 'incomplete_patient',
                'patient_id': patient.get('patient_id'),
                'patient_name': patient.get('full_name'),
                'quality_score': quality_score,
                'missing_fields': missing_fields
            })
    
    return alerts


def render_alerts_dashboard():
    """Render data validation and alerts dashboard"""
    
    st.subheader("⚠️ Data Validation & Alerts")
    
    st.info("""
    **Automated Data Quality Monitoring:**
    - Breach risk alerts
    - Missing milestone warnings
    - Incomplete data notifications
    - Data quality scoring
    """)
    
    # Generate alerts
    with st.spinner("Analyzing data quality..."):
        alerts = generate_all_alerts()
    
    # Summary metrics
    st.markdown("### 📊 Alert Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        critical_count = len(alerts['critical'])
        if critical_count > 0:
            st.error(f"🔴 Critical\n\n{critical_count}")
        else:
            st.success(f"🔴 Critical\n\n{critical_count}")
    
    with col2:
        high_count = len(alerts['high'])
        if high_count > 0:
            st.warning(f"🟠 High\n\n{high_count}")
        else:
            st.success(f"🟠 High\n\n{high_count}")
    
    with col3:
        medium_count = len(alerts['medium'])
        if medium_count > 0:
            st.info(f"🟡 Medium\n\n{medium_count}")
        else:
            st.success(f"🟡 Medium\n\n{medium_count}")
    
    with col4:
        quality_count = len(alerts['data_quality'])
        if quality_count > 0:
            st.warning(f"📊 Quality\n\n{quality_count}")
        else:
            st.success(f"📊 Quality\n\n{quality_count}")
    
    with col5:
        total_alerts = sum([len(v) for v in alerts.values()])
        if total_alerts > 0:
            st.metric("Total Alerts", total_alerts)
        else:
            st.success(f"✅ All Clear\n\n{total_alerts}")
    
    st.markdown("---")
    
    # Tabs for different alert types
    tab1, tab2, tab3, tab4 = st.tabs([
        f"🔴 Critical ({critical_count})",
        f"🟠 High Risk ({high_count})",
        f"🟡 Medium Risk ({medium_count})",
        f"📊 Data Quality ({quality_count})"
    ])
    
    with tab1:
        render_alert_list(alerts['critical'], "Critical")
    
    with tab2:
        render_alert_list(alerts['high'], "High")
    
    with tab3:
        render_alert_list(alerts['medium'], "Medium")
    
    with tab4:
        render_data_quality_alerts(alerts['data_quality'])


def render_alert_list(alert_list: List[Dict], level: str):
    """Render list of alerts"""
    
    if not alert_list:
        st.success(f"✅ No {level.lower()} risk alerts!")
        return
    
    for alert in alert_list:
        alert_type = alert.get('type')
        
        if alert_type == 'breach_risk':
            icon = "🔴" if alert.get('days_remaining', 0) < 0 else "⚠️"
            with st.expander(f"{icon} {alert['pathway_id']} - {alert['patient_name']}"):
                st.error(alert['message'])
                st.write(f"**Pathway ID:** {alert['pathway_id']}")
                st.write(f"**Patient:** {alert['patient_name']}")
                if alert.get('days_remaining') is not None:
                    st.write(f"**Days Remaining:** {alert['days_remaining']}")
                st.button("🔍 View Pathway", key=f"view_{alert['pathway_id']}")
        
        elif alert_type == 'missing_milestones':
            with st.expander(f"📅 {alert['pathway_id']} - {alert['patient_name']}"):
                st.warning("Missing milestone dates")
                st.write(f"**Pathway ID:** {alert['pathway_id']}")
                st.write(f"**Patient:** {alert['patient_name']}")
                st.write("**Missing Milestones:**")
                for milestone in alert.get('missing_milestones', []):
                    st.write(f"- {milestone}")
                st.button("📝 Record Milestones", key=f"milestone_{alert['pathway_id']}")


def render_data_quality_alerts(quality_alerts: List[Dict]):
    """Render data quality alerts"""
    
    if not quality_alerts:
        st.success("✅ All data meets quality standards!")
        return
    
    for alert in quality_alerts:
        alert_type = alert.get('type')
        quality_score = alert.get('quality_score', 0)
        
        if quality_score < 50:
            color = "🔴"
            status = "Poor"
        elif quality_score < 70:
            color = "🟠"
            status = "Fair"
        else:
            color = "🟡"
            status = "Good"
        
        if alert_type == 'incomplete_pathway':
            with st.expander(f"{color} {alert['pathway_id']} - {status} Quality ({quality_score}%)"):
                st.progress(quality_score / 100)
                st.write(f"**Pathway ID:** {alert['pathway_id']}")
                st.write(f"**Patient:** {alert['patient_name']}")
                st.write(f"**Quality Score:** {quality_score}%")
                st.write("**Missing Fields:**")
                for field in alert.get('missing_fields', []):
                    st.write(f"- {field}")
                st.button("✏️ Complete Data", key=f"complete_pathway_{alert['pathway_id']}")
        
        elif alert_type == 'incomplete_patient':
            with st.expander(f"{color} {alert['patient_id']} - {status} Quality ({quality_score}%)"):
                st.progress(quality_score / 100)
                st.write(f"**Patient ID:** {alert['patient_id']}")
                st.write(f"**Patient:** {alert['patient_name']}")
                st.write(f"**Quality Score:** {quality_score}%")
                st.write("**Missing Fields:**")
                for field in alert.get('missing_fields', []):
                    st.write(f"- {field}")
                st.button("✏️ Update Patient", key=f"update_patient_{alert['patient_id']}")


def get_data_quality_summary() -> Dict:
    """Get overall data quality summary"""
    
    patients = get_all_patients()
    pathways = get_all_pathways()
    
    patient_scores = []
    pathway_scores = []
    
    for patient in patients:
        _, _, score = validate_patient_data(patient)
        patient_scores.append(score)
    
    for pathway in pathways:
        if pathway.get('status') not in ['closed', 'completed']:
            _, _, score = validate_pathway_data(pathway)
            pathway_scores.append(score)
    
    avg_patient_quality = sum(patient_scores) / len(patient_scores) if patient_scores else 0
    avg_pathway_quality = sum(pathway_scores) / len(pathway_scores) if pathway_scores else 0
    overall_quality = (avg_patient_quality + avg_pathway_quality) / 2 if (patient_scores or pathway_scores) else 0
    
    return {
        'avg_patient_quality': round(avg_patient_quality, 1),
        'avg_pathway_quality': round(avg_pathway_quality, 1),
        'overall_quality': round(overall_quality, 1),
        'total_patients': len(patients),
        'total_pathways': len([p for p in pathways if p.get('status') not in ['closed', 'completed']])
    }
