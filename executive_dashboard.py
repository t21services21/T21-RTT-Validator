"""
EXECUTIVE DASHBOARD
Unified view of ALL system metrics and KPIs

Features:
- Cross-module statistics
- Real-time KPIs
- Performance metrics
- Breach alerts
- Resource utilization
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict

# Import from all modules
from ptl_system import get_ptl_stats
from cancer_pathway_system import get_cancer_ptl_stats
from mdt_coordination_system import get_mdt_stats
from task_management_system import get_task_stats
from advanced_booking_system import get_dna_rate, load_appointments


def render_executive_dashboard():
    """Main executive dashboard"""
    
    st.header("📊 Executive Dashboard")
    st.markdown("**Unified System Overview - All Modules**")
    
    # Time period selector
    col1, col2 = st.columns([4, 1])
    with col2:
        time_period = st.selectbox("Period", [7, 30, 60, 90], index=1, key="exec_period")
    
    # Load all stats
    with st.spinner("Loading system metrics..."):
        ptl_stats = get_ptl_stats()
        cancer_stats = get_cancer_ptl_stats()
        mdt_stats = get_mdt_stats()
        task_stats = get_task_stats()
        dna_stats = get_dna_rate(days=time_period)
    
    # Top-level KPIs
    render_top_kpis(ptl_stats, cancer_stats, mdt_stats, task_stats, dna_stats)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏥 Clinical Operations",
        "⚠️ Breach Alerts",
        "📈 Performance Metrics",
        "👥 Resource Utilization",
        "🎯 Strategic View"
    ])
    
    with tab1:
        render_clinical_operations(ptl_stats, cancer_stats, mdt_stats)
    
    with tab2:
        render_breach_alerts(ptl_stats, cancer_stats)
    
    with tab3:
        render_performance_metrics(task_stats, dna_stats, mdt_stats)
    
    with tab4:
        render_resource_utilization(mdt_stats, dna_stats)
    
    with tab5:
        render_strategic_view(ptl_stats, cancer_stats, mdt_stats, task_stats)


def render_top_kpis(ptl_stats, cancer_stats, mdt_stats, task_stats, dna_stats):
    """Top-level KPI cards"""
    
    st.markdown("### 🎯 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_patients = ptl_stats.get('total_patients', 0) + cancer_stats.get('total_patients', 0)
        st.metric("Total Active Patients", total_patients)
    
    with col2:
        breach_risk = ptl_stats.get('high_risk', 0) + cancer_stats.get('breach_risk', 0)
        st.metric("⚠️ Breach Risk", breach_risk, 
                 delta="Action Required" if breach_risk > 0 else None,
                 delta_color="inverse")
    
    with col3:
        st.metric("MDT Meetings", mdt_stats.get('total_meetings', 0),
                 delta=f"{mdt_stats.get('upcoming_count', 0)} upcoming")
    
    with col4:
        task_completion = 0
        if task_stats['total'] > 0:
            task_completion = round((task_stats['completed'] / task_stats['total']) * 100, 1)
        st.metric("Task Completion", f"{task_completion}%",
                 delta="Good" if task_completion >= 70 else "Needs Improvement",
                 delta_color="normal" if task_completion >= 70 else "inverse")
    
    with col5:
        st.metric("DNA Rate", f"{dna_stats['dna_rate']}%",
                 delta="Excellent" if dna_stats['dna_rate'] < 5 else "Review",
                 delta_color="normal" if dna_stats['dna_rate'] < 5 else "inverse")


def render_clinical_operations(ptl_stats, cancer_stats, mdt_stats):
    """Clinical operations overview"""
    
    st.markdown("### 🏥 Clinical Operations Overview")
    
    # PTL Overview
    st.markdown("#### 📋 RTT Patient Tracking List")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", ptl_stats.get('total_patients', 0))
    with col2:
        st.metric("High Risk", ptl_stats.get('high_risk', 0))
    with col3:
        st.metric("Medium Risk", ptl_stats.get('medium_risk', 0))
    with col4:
        st.metric("Low Risk", ptl_stats.get('low_risk', 0))
    
    # Specialty breakdown
    if ptl_stats.get('by_specialty'):
        st.markdown("**By Specialty:**")
        specialty_cols = st.columns(min(4, len(ptl_stats['by_specialty'])))
        for idx, (specialty, count) in enumerate(list(ptl_stats['by_specialty'].items())[:4]):
            with specialty_cols[idx]:
                st.metric(specialty, count)
    
    st.markdown("---")
    
    # Cancer Pathways Overview
    st.markdown("#### 🎗️ Cancer Pathways")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Pathways", cancer_stats.get('total_patients', 0))
    with col2:
        st.metric("2WW Pathways", cancer_stats.get('2ww_count', 0))
    with col3:
        st.metric("62-Day Pathways", cancer_stats.get('62day_count', 0))
    with col4:
        st.metric("Breach Risk", cancer_stats.get('breach_risk', 0))
    
    st.markdown("---")
    
    # MDT Overview
    st.markdown("#### 👥 MDT Coordination")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Meetings", mdt_stats.get('total_meetings', 0))
    with col2:
        st.metric("This Week", mdt_stats.get('this_week', 0))
    with col3:
        st.metric("Upcoming", mdt_stats.get('upcoming_count', 0))
    with col4:
        st.metric("Patients Discussed", mdt_stats.get('total_patients_discussed', 0))


def render_breach_alerts(ptl_stats, cancer_stats):
    """Breach risk alerts"""
    
    st.markdown("### ⚠️ Breach Risk Alerts")
    
    total_breach_risk = ptl_stats.get('high_risk', 0) + cancer_stats.get('breach_risk', 0)
    
    if total_breach_risk == 0:
        st.success("✅ No patients at immediate breach risk!")
    else:
        st.error(f"⚠️ **{total_breach_risk} patients at breach risk** - Immediate action required!")
    
    # PTL Breach Risks
    if ptl_stats.get('high_risk', 0) > 0:
        st.markdown("#### 📋 RTT Breach Risks")
        st.warning(f"**{ptl_stats['high_risk']} RTT patients** at high risk of breaching 18-week target")
        st.markdown("**Recommended Actions:**")
        st.markdown("- Review patient waiting times")
        st.markdown("- Prioritize appointments for high-risk patients")
        st.markdown("- Check for booking delays")
        st.markdown("- Escalate to management if capacity issues")
    
    # Cancer Breach Risks
    if cancer_stats.get('breach_risk', 0) > 0:
        st.markdown("#### 🎗️ Cancer Pathway Breach Risks")
        st.error(f"**{cancer_stats['breach_risk']} cancer patients** at risk of breaching targets")
        st.markdown("**Recommended Actions:**")
        st.markdown("- Fast-track diagnostic tests")
        st.markdown("- Expedite MDT discussion")
        st.markdown("- Book urgent treatment slots")
        st.markdown("- Review pathway delays")
    
    # Weekly forecast
    st.markdown("---")
    st.markdown("#### 📅 7-Day Forecast")
    st.info("""
    **Expected Breaches in Next 7 Days:**
    - Monitor daily for changes
    - Prepare mitigation plans
    - Communicate with clinical teams
    - Update senior management
    """)


def render_performance_metrics(task_stats, dna_stats, mdt_stats):
    """Performance metrics"""
    
    st.markdown("### 📈 Performance Metrics")
    
    # Task Performance
    st.markdown("#### ✅ Task Management Performance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        completion_rate = 0
        if task_stats['total'] > 0:
            completion_rate = round((task_stats['completed'] / task_stats['total']) * 100, 1)
        st.metric("Task Completion Rate", f"{completion_rate}%")
        
        if completion_rate >= 80:
            st.success("✅ Excellent performance")
        elif completion_rate >= 60:
            st.info("ℹ️ Good performance")
        else:
            st.warning("⚠️ Needs improvement")
    
    with col2:
        st.metric("Overdue Tasks", task_stats['overdue'],
                 delta="Action Required" if task_stats['overdue'] > 0 else None,
                 delta_color="inverse")
    
    with col3:
        st.metric("Pending Tasks", task_stats['pending'])
    
    st.markdown("---")
    
    # Appointment Performance
    st.markdown("#### 🗓️ Appointment Attendance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Attendance Rate", f"{dna_stats['attendance_rate']}%",
                 delta="Excellent" if dna_stats['attendance_rate'] > 90 else "Review")
    
    with col2:
        st.metric("DNA Rate", f"{dna_stats['dna_rate']}%",
                 delta="Target: <5%" if dna_stats['dna_rate'] < 5 else "Above Target",
                 delta_color="normal" if dna_stats['dna_rate'] < 5 else "inverse")
    
    with col3:
        st.metric("Total Appointments", dna_stats['total_appointments'])
    
    st.markdown("---")
    
    # MDT Performance
    st.markdown("#### 👥 MDT Effectiveness")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Completed Meetings", mdt_stats.get('completed', 0))
    
    with col2:
        st.metric("Patients Discussed", mdt_stats.get('total_patients_discussed', 0))


def render_resource_utilization(mdt_stats, dna_stats):
    """Resource utilization metrics"""
    
    st.markdown("### 👥 Resource Utilization")
    
    # Clinic Utilization
    st.markdown("#### 🏥 Clinic Utilization")
    
    if dna_stats['total_appointments'] > 0:
        utilized_slots = dna_stats['attended']
        wasted_slots = dna_stats['dna']
        cancelled_slots = dna_stats['cancelled']
        
        utilization_rate = (utilized_slots / dna_stats['total_appointments']) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Utilization Rate", f"{utilization_rate:.1f}%")
        with col2:
            st.metric("Wasted Slots (DNA)", wasted_slots,
                     delta=f"{dna_stats['dna_rate']}% of total")
        with col3:
            st.metric("Cancelled Slots", cancelled_slots)
        
        # Recommendations
        if dna_stats['dna_rate'] > 5:
            st.warning("""
            **⚠️ High DNA Rate Impacting Utilization**
            - Implement reminder system
            - Review booking practices
            - Consider overbooking strategy
            """)
    else:
        st.info("No appointment data available for selected period")
    
    st.markdown("---")
    
    # MDT Resource Usage
    st.markdown("#### 👥 MDT Resource Usage")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Specialties Covered", len(mdt_stats.get('specialties', {})))
    with col2:
        st.metric("Active Meetings", mdt_stats.get('scheduled', 0))


def render_strategic_view(ptl_stats, cancer_stats, mdt_stats, task_stats):
    """Strategic overview for senior management"""
    
    st.markdown("### 🎯 Strategic Overview")
    
    # Overall System Health
    st.markdown("#### 🏥 System Health Score")
    
    # Calculate health score (0-100)
    health_score = 100
    
    # Deduct for breach risks
    breach_risk = ptl_stats.get('high_risk', 0) + cancer_stats.get('breach_risk', 0)
    health_score -= min(breach_risk * 2, 30)  # Max -30 points
    
    # Deduct for overdue tasks
    health_score -= min(task_stats['overdue'] * 1, 20)  # Max -20 points
    
    # Deduct for low task completion
    if task_stats['total'] > 0:
        completion_rate = (task_stats['completed'] / task_stats['total']) * 100
        if completion_rate < 70:
            health_score -= (70 - completion_rate) * 0.5
    
    health_score = max(0, round(health_score))
    
    # Display health score
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if health_score >= 80:
            st.success(f"## ✅ System Health: {health_score}/100")
            st.success("System operating optimally")
        elif health_score >= 60:
            st.info(f"## ℹ️ System Health: {health_score}/100")
            st.info("System operating normally with minor issues")
        else:
            st.error(f"## ⚠️ System Health: {health_score}/100")
            st.error("System requires immediate attention")
    
    st.markdown("---")
    
    # Key Priorities
    st.markdown("#### 🎯 Key Priorities")
    
    priorities = []
    
    if breach_risk > 0:
        priorities.append(f"🔴 **URGENT:** {breach_risk} patients at breach risk - Immediate action required")
    
    if task_stats['overdue'] > 5:
        priorities.append(f"🟠 **HIGH:** {task_stats['overdue']} overdue tasks - Review and prioritize")
    
    if mdt_stats.get('this_week', 0) > 0:
        priorities.append(f"🟡 **MEDIUM:** {mdt_stats['this_week']} MDT meetings this week - Ensure preparation")
    
    if not priorities:
        st.success("✅ No critical priorities - System running smoothly")
    else:
        for priority in priorities:
            st.markdown(priority)
    
    st.markdown("---")
    
    # Strategic Recommendations
    st.markdown("#### 💡 Strategic Recommendations")
    
    st.info("""
    **System Optimization Opportunities:**
    - Implement automated patient reminders to reduce DNA rate
    - Expand MDT capacity to discuss more patients
    - Review specialty-specific bottlenecks
    - Enhance cross-module patient tracking
    - Invest in staff training on system features
    - Consider additional clinic slots for high-demand specialties
    """)
