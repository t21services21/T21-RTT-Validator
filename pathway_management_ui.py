"""
T21 PATHWAY MANAGEMENT UI
User interface for complete pathway management
"""

import streamlit as st
from datetime import datetime, date
from pathway_management_system import (
    create_pathway,
    get_all_pathways,
    get_patient_pathways,
    get_pathway_by_id,
    update_pathway_progress,
    close_pathway,
    get_pathway_stats
)
from patient_selector_component import render_patient_selector, render_patient_quick_select
from episode_management_system import get_patient_episodes


SPECIALTIES = [
    "Cardiology", "Dermatology", "ENT", "Gastroenterology",
    "General Surgery", "Neurology", "Ophthalmology", "Orthopaedics",
    "Respiratory", "Rheumatology", "Urology", "Oncology", "Other"
]


def render_pathway_management():
    """Main pathway management interface"""
    
    st.header("📁 Pathway Management System")
    st.markdown("**Create & Track RTT and Cancer Pathways**")
    
    st.success("""
    📁 **Pathway Management Features:**
    - 📋 Create RTT Pathways (18-week)
    - 🎗️ Create Cancer Pathways (2WW, 62-day, 31-day)
    - ⏱️ Automatic breach date calculation
    - 🔗 Link episodes to pathways
    - 📊 Timeline view of patient journey
    - 🚨 Breach risk monitoring
    - 📈 Pathway statistics
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Create Pathway",
        "📋 All Pathways",
        "📊 Pathway Timeline",
        "📈 Statistics"
    ])
    
    with tab1:
        render_create_pathway()
    
    with tab2:
        render_all_pathways()
    
    with tab3:
        render_pathway_timeline()
    
    with tab4:
        render_pathway_stats()


def render_create_pathway():
    """Create new pathway"""
    
    st.subheader("➕ Create New Pathway")
    
    st.info("""
    **Pathway Creation:**
    1. Search and select patient
    2. Choose pathway type (RTT or Cancer)
    3. Pathway automatically starts RTT clock
    4. Add episodes to track progress
    """)
    
    # Success message
    if 'pathway_created' in st.session_state:
        pathway_info = st.session_state['pathway_created']
        st.success(f"✅ Pathway created: {pathway_info['pathway_id']}")
        st.info(f"**Breach Date:** {pathway_info['breach_date']}")
        st.balloons()
        del st.session_state['pathway_created']
    
    # Patient selector with SEARCH
    st.markdown("---")
    selected_patient = render_patient_selector(key_prefix="create_pathway")
    
    if not selected_patient:
        st.warning("⚠️ Please search and select a patient first")
        return
    
    st.markdown("---")
    
    # Pathway creation form
    with st.form("create_pathway_form"):
        st.markdown("### 📁 Pathway Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pathway_type = st.selectbox("Pathway Type*", [
                "rtt",
                "cancer_2ww",
                "cancer_62day",
                "cancer_31day",
                "other"
            ], format_func=lambda x: {
                'rtt': '📋 RTT 18-Week Pathway',
                'cancer_2ww': '🎗️ Cancer 2-Week Wait',
                'cancer_62day': '🎗️ Cancer 62-Day Pathway',
                'cancer_31day': '🎗️ Cancer 31-Day Pathway',
                'other': '📁 Other Pathway'
            }[x])
            
            start_date = st.date_input("Pathway Start Date*", value=date.today(),
                                      help="This is when RTT clock starts!")
            
            specialty = st.selectbox("Specialty*", SPECIALTIES)
        
        with col2:
            consultant = st.text_input("Consultant", placeholder="Dr. Smith")
            
            referral_source = st.selectbox("Referral Source*", [
                "GP", "Consultant", "A&E", "Dentist", "Optician", "Other"
            ])
            
            priority = st.selectbox("Priority", [
                "Routine", "Urgent", "2WW", "Cancer"
            ])
        
        reason = st.text_area("Reason for Referral*", height=100,
                             placeholder="Why is patient on this pathway?")
        
        notes = st.text_area("Clinical Notes", height=100)
        
        submit = st.form_submit_button("✅ Create Pathway & Start Clock", type="primary")
        
        if submit:
            if not reason:
                st.error("❌ Please provide reason for referral")
            else:
                with st.spinner("📁 Creating pathway..."):
                    result = create_pathway(
                        patient_id=selected_patient.get('patient_id'),
                        patient_name=selected_patient.get('full_name'),
                        pathway_type=pathway_type,
                        start_date=str(start_date),
                        specialty=specialty,
                        consultant=consultant,
                        referral_source=referral_source,
                        priority=priority,
                        reason=reason,
                        notes=notes
                    )
                
                if result['success']:
                    st.session_state['pathway_created'] = {
                        'pathway_id': result['pathway_id'],
                        'breach_date': result['breach_date']
                    }
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {result.get('error')}")


def render_all_pathways():
    """Display all pathways"""
    
    st.subheader("📋 All Pathways")
    
    # Refresh
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Get all pathways
    pathways = get_all_pathways()
    
    if not pathways:
        st.info("📁 No pathways created yet. Use 'Create Pathway' tab to start.")
        return
    
    st.write(f"**Total Pathways:** {len(pathways)}")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Active", "Closed"])
    with col2:
        type_filter = st.selectbox("Type", ["All", "RTT", "Cancer 2WW", "Cancer 62-day", "Cancer 31-day"])
    with col3:
        risk_filter = st.selectbox("Risk Level", ["All", "Breached", "Critical", "High", "Medium", "Low"])
    
    # Apply filters
    filtered = pathways
    
    if status_filter != "All":
        filtered = [p for p in filtered if p.get('status', '').lower() == status_filter.lower()]
    
    if type_filter != "All":
        type_map = {
            "RTT": "rtt",
            "Cancer 2WW": "cancer_2ww",
            "Cancer 62-day": "cancer_62day",
            "Cancer 31-day": "cancer_31day"
        }
        filtered = [p for p in filtered if p.get('pathway_type') == type_map.get(type_filter)]
    
    if risk_filter != "All":
        filtered = [p for p in filtered if p.get('risk_level', '').lower() == risk_filter.lower()]
    
    st.write(f"**Showing:** {len(filtered)} pathways")
    
    # Display pathways
    for pathway in filtered:
        render_pathway_card(pathway)


def render_pathway_card(pathway: dict):
    """Render individual pathway card"""
    
    # Risk status icon
    risk_icons = {
        'breached': '🔴',
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }
    
    risk_icon = risk_icons.get(pathway.get('risk_level', 'low'), '⚪')
    status_icon = '🟢' if pathway.get('status') == 'active' else '⚪'
    
    with st.expander(f"{risk_icon} {status_icon} {pathway.get('pathway_id')} - {pathway.get('patient_name')} ({pathway.get('pathway_name')})"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Patient & Pathway:**")
            st.write(f"**Pathway ID:** {pathway.get('pathway_id')}")
            st.write(f"**Patient:** {pathway.get('patient_name')}")
            st.write(f"**Patient ID:** {pathway.get('patient_id')}")
            st.write(f"**Type:** {pathway.get('pathway_name')}")
        
        with col2:
            st.markdown("**Timeline:**")
            st.write(f"**Start Date:** {pathway.get('start_date')}")
            st.write(f"**Breach Date:** {pathway.get('breach_date')}")
            st.write(f"**Days Elapsed:** {pathway.get('days_elapsed', 0)}")
            st.write(f"**Days Remaining:** {pathway.get('days_remaining', 0)}")
        
        with col3:
            st.markdown("**Status:**")
            st.write(f"**Status:** {pathway.get('status', 'N/A').title()}")
            st.write(f"**Risk Level:** {pathway.get('risk_level', 'N/A').title()}")
            st.write(f"**Clock:** {pathway.get('clock_status', 'N/A').title()}")
            st.write(f"**Priority:** {pathway.get('priority', 'N/A')}")
        
        if pathway.get('reason'):
            st.markdown(f"**Reason:** {pathway.get('reason')}")
        
        # Show episodes count
        episodes = get_patient_episodes(pathway.get('patient_id', ''))
        st.info(f"📋 **Episodes Linked:** {episodes.get('total_count', 0)}")


def render_pathway_timeline():
    """Render pathway timeline view"""
    
    st.subheader("📊 Pathway Timeline View")
    
    st.info("🔍 Select a patient to view their complete pathway timeline with all episodes")
    
    # Patient selector
    selected_patient = render_patient_quick_select(key_prefix="timeline")
    
    if not selected_patient:
        return
    
    patient_id = selected_patient.get('patient_id')
    
    # Get patient's pathways
    pathways = get_patient_pathways(patient_id)
    
    if not pathways:
        st.warning(f"⚠️ No pathways found for {selected_patient.get('full_name')}")
        return
    
    st.success(f"✅ Found {len(pathways)} pathway(s) for {selected_patient.get('full_name')}")
    
    # Display each pathway
    for pathway in pathways:
        st.markdown("---")
        st.markdown(f"### 📁 {pathway.get('pathway_id')} - {pathway.get('pathway_name')}")
        
        # Pathway overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Start Date", pathway.get('start_date'))
        with col2:
            st.metric("Days Elapsed", pathway.get('days_elapsed', 0))
        with col3:
            st.metric("Days Remaining", pathway.get('days_remaining', 0))
        with col4:
            risk = pathway.get('risk_level', 'low').title()
            st.metric("Risk", risk)
        
        # Get episodes for this pathway
        all_episodes = get_patient_episodes(patient_id)
        episodes = all_episodes.get('all_episodes', [])
        
        if episodes:
            st.markdown("#### 📋 Episodes Timeline:")
            
            for episode in episodes:
                episode_type = episode.get('episode_type', 'unknown')
                icon = {
                    'consultant': '👨‍⚕️',
                    'treatment': '💉',
                    'diagnostic': '🔬'
                }.get(episode_type, '📋')
                
                st.markdown(f"{icon} **{episode.get('episode_id')}** - {episode_type.title()}")
                
                if episode_type == 'consultant':
                    st.write(f"  └─ {episode.get('start_date')} - {episode.get('consultant_name')} ({episode.get('specialty')})")
                elif episode_type == 'treatment':
                    st.write(f"  └─ {episode.get('treatment_date')} - {episode.get('treatment_type')}")
                elif episode_type == 'diagnostic':
                    st.write(f"  └─ {episode.get('request_date')} - {episode.get('investigation_type')}")
        else:
            st.info("📋 No episodes added to this pathway yet")


def render_pathway_stats():
    """Display pathway statistics"""
    
    st.subheader("📈 Pathway Statistics")
    
    stats = get_pathway_stats()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pathways", stats['total_pathways'])
    
    with col2:
        st.metric("🟢 Active", stats['active_pathways'])
    
    with col3:
        st.metric("⚪ Closed", stats['closed_pathways'])
    
    with col4:
        breached = stats['breached'] + stats['critical_risk']
        st.metric("🔴 At Risk", breached)
    
    # By type
    st.markdown("---")
    st.markdown("### 📊 By Pathway Type")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📋 RTT Pathways", stats['rtt_pathways'])
    
    with col2:
        st.metric("🎗️ Cancer Pathways", stats['cancer_pathways'])
    
    # Risk breakdown
    st.markdown("---")
    st.markdown("### 🚨 Risk Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 Breached", stats['breached'])
    
    with col2:
        st.metric("🔴 Critical Risk", stats['critical_risk'])
    
    with col3:
        st.metric("🟠 High Risk", stats['high_risk'])
