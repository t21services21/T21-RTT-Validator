"""
STUDENT PORTFOLIO VIEW
For students to view their own work and progress

Features:
- See personal portfolio
- View competency checklist
- Track progress
- Self-assessment
- Export personal evidence
"""

import streamlit as st
from datetime import datetime
from patient_registration_system import get_all_patients
from pathway_management_system import get_all_pathways
from episode_management_system import get_all_episodes
from typing import Dict
import json


def get_my_work(user_email: str) -> Dict:
    """Get all work for current student"""
    all_patients = get_all_patients()
    all_pathways = get_all_pathways()
    all_episodes = get_all_episodes()
    
    # Filter by current user
    my_patients = [p for p in all_patients if p.get('user_email') == user_email]
    my_pathways = [p for p in all_pathways if p.get('user_email') == user_email]
    my_episodes = [e for e in all_episodes if e.get('user_email') == user_email]
    
    return {
        'email': user_email,
        'patients': my_patients,
        'pathways': my_pathways,
        'episodes': my_episodes,
        'total_patients': len(my_patients),
        'total_pathways': len(my_pathways),
        'total_episodes': len(my_episodes)
    }


def calculate_my_competencies(my_work: Dict) -> Dict:
    """Calculate competency completion for current student"""
    
    competencies = {
        'patient_registration': {
            'name': 'Patient Registration',
            'description': 'Register patients with complete demographics',
            'required': 5,
            'completed': min(my_work['total_patients'], 5),
            'status': 'complete' if my_work['total_patients'] >= 5 else 'incomplete',
            'tasks': [
                'Register patient with NHS number',
                'Complete all mandatory fields',
                'Add GP details',
                'Add next of kin',
                'Verify data accuracy'
            ]
        },
        'pathway_creation': {
            'name': 'Pathway Creation',
            'description': 'Create and manage RTT pathways',
            'required': 3,
            'completed': min(my_work['total_pathways'], 3),
            'status': 'complete' if my_work['total_pathways'] >= 3 else 'incomplete',
            'tasks': [
                'Create RTT pathway',
                'Select correct specialty',
                'Set referral details',
                'Calculate breach date',
                'Monitor pathway progress'
            ]
        },
        'episode_management': {
            'name': 'Episode Management',
            'description': 'Add and manage clinical episodes',
            'required': 5,
            'completed': min(my_work['total_episodes'], 5),
            'status': 'complete' if my_work['total_episodes'] >= 5 else 'incomplete',
            'tasks': [
                'Add consultant episode',
                'Add treatment episode',
                'Add diagnostic episode',
                'Link episodes to pathways',
                'Use episode codes correctly'
            ]
        },
        'rtt_clock_management': {
            'name': 'RTT Clock Management',
            'description': 'Pause and resume RTT clock',
            'required': 1,
            'completed': len([p for p in my_work['pathways'] if p.get('total_pause_days', 0) > 0]),
            'status': 'complete' if any(p.get('total_pause_days', 0) > 0 for p in my_work['pathways']) else 'incomplete',
            'tasks': [
                'Understand clock pause reasons',
                'Pause RTT clock correctly',
                'Resume RTT clock',
                'Understand breach date extension',
                'Document pause reasons'
            ]
        },
        'milestone_recording': {
            'name': 'Milestone Recording',
            'description': 'Record key NHS milestone dates',
            'required': 3,
            'completed': len([p for p in my_work['pathways'] if p.get('first_appointment_date')]),
            'status': 'complete' if len([p for p in my_work['pathways'] if p.get('first_appointment_date')]) >= 3 else 'incomplete',
            'tasks': [
                'Record first appointment',
                'Record decision to treat',
                'Record treatment start',
                'Calculate milestone timings',
                'Understand milestone significance'
            ]
        }
    }
    
    total_required = sum([c['required'] for c in competencies.values()])
    total_completed = sum([c['completed'] for c in competencies.values()])
    overall_percentage = (total_completed / total_required * 100) if total_required > 0 else 0
    
    return {
        'competencies': competencies,
        'overall_percentage': overall_percentage,
        'total_required': total_required,
        'total_completed': total_completed
    }


def render_student_portfolio():
    """Main student portfolio interface"""
    
    st.header("📚 My Portfolio")
    st.markdown("**Track your learning progress and TQUK competencies**")
    
    # Get current user email
    user_email = st.session_state.get('user_email', 'guest@example.com')
    
    # Get my work
    my_work = get_my_work(user_email)
    my_comp = calculate_my_competencies(my_work)
    
    # Overall progress card
    st.markdown("---")
    st.markdown(f"### 👤 {user_email}")
    
    # Progress bar
    progress = my_comp['overall_percentage']
    st.progress(progress / 100)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Progress", f"{progress:.0f}%")
    with col2:
        st.metric("Patients Registered", my_work['total_patients'])
    with col3:
        st.metric("Pathways Created", my_work['total_pathways'])
    with col4:
        st.metric("Episodes Managed", my_work['total_episodes'])
    
    # Status
    if progress >= 100:
        st.success("🎉 **EXCELLENT!** All competencies complete! You're ready for assessment!")
    elif progress >= 75:
        st.info("🔵 **NEARLY THERE!** Just a few more tasks to complete!")
    elif progress >= 50:
        st.warning("🟡 **GOOD PROGRESS!** Keep going!")
    elif progress >= 25:
        st.info("🔵 **GETTING STARTED!** You're on the right track!")
    else:
        st.info("📚 **WELCOME!** Start by registering some patients!")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✅ Competency Checklist",
        "📊 My Work Summary",
        "📚 Learning Resources",
        "📄 Export Portfolio",
        "🎯 Learning Tips"
    ])
    
    with tab1:
        render_competency_checklist(my_comp)
    
    with tab2:
        render_work_summary(my_work)
    
    with tab3:
        render_learning_resources()
    
    with tab4:
        render_export_portfolio(user_email, my_work, my_comp)
    
    with tab5:
        render_learning_tips(my_comp)


def render_competency_checklist(comp_data: Dict):
    """Show detailed competency checklist"""
    
    st.subheader("✅ TQUK Competency Checklist")
    
    st.info("""
    **TQUK Level 2/3 Business Administration - Patient Administration**
    
    Complete all competencies to receive certification.
    Each competency has specific tasks you must demonstrate.
    """)
    
    for comp_key, comp in comp_data['competencies'].items():
        # Competency header
        status_icon = "✅" if comp['status'] == 'complete' else "⏳"
        progress_pct = (comp['completed'] / comp['required'] * 100) if comp['required'] > 0 else 0
        
        with st.expander(f"{status_icon} {comp['name']} - {comp['completed']}/{comp['required']} ({progress_pct:.0f}%)", 
                        expanded=(comp['status'] == 'incomplete')):
            
            st.write(f"**Description:** {comp['description']}")
            st.write(f"**Required:** {comp['required']} | **Completed:** {comp['completed']}")
            
            # Progress bar
            st.progress(progress_pct / 100)
            
            # Task list
            st.markdown("**Tasks to demonstrate:**")
            for i, task in enumerate(comp['tasks'], 1):
                task_icon = "✓" if i <= comp['completed'] else "○"
                st.write(f"{task_icon} {task}")
            
            # Next steps
            if comp['status'] == 'incomplete':
                remaining = comp['required'] - comp['completed']
                st.warning(f"⚠️ **Need {remaining} more to complete this competency**")
            else:
                st.success("✅ **Competency Complete!**")


def render_work_summary(my_work: Dict):
    """Show summary of all work"""
    
    st.subheader("📊 My Work Summary")
    
    # Patients
    st.markdown("### 👤 Patients I've Registered")
    if my_work['patients']:
        for patient in my_work['patients']:
            st.write(f"- **{patient.get('full_name')}** ({patient.get('patient_id')}) - NHS: {patient.get('nhs_number')} - Registered: {patient.get('registration_date', 'N/A')}")
    else:
        st.info("📚 No patients registered yet. Start by registering your first patient!")
    
    st.markdown("---")
    
    # Pathways
    st.markdown("### 📁 Pathways I've Created")
    if my_work['pathways']:
        for pathway in my_work['pathways']:
            specialty = pathway.get('specialty', 'N/A')
            status = pathway.get('status', 'N/A')
            paused = pathway.get('clock_paused', False)
            pause_icon = "⏸️" if paused else ""
            st.write(f"- **{pathway.get('pathway_id')}** - {pathway.get('patient_name')} ({specialty}) - Status: {status} {pause_icon}")
    else:
        st.info("📚 No pathways created yet. Create your first RTT pathway!")
    
    st.markdown("---")
    
    # Episodes
    st.markdown("### 📋 Episodes I've Managed")
    if my_work['episodes']:
        for episode in my_work['episodes']:
            episode_type = episode.get('episode_type', 'N/A')
            code = episode.get('episode_code', '')
            code_text = f"[{code}]" if code else ""
            st.write(f"- **{episode.get('episode_id')}** ({episode_type}) - {episode.get('patient_name')} {code_text}")
    else:
        st.info("📚 No episodes added yet. Start adding consultant episodes!")


def render_export_portfolio(user_email: str, my_work: Dict, comp_data: Dict):
    """Export personal portfolio"""
    
    st.subheader("📄 Export My Portfolio")
    
    st.info("""
    **Export your portfolio for:**
    - Job applications
    - Personal records
    - Progress tracking
    - TQUK evidence
    """)
    
    export_format = st.radio("Export Format:", ["JSON (Complete Data)", "Text Summary", "Competency Report"])
    
    if st.button("📥 Download My Portfolio", type="primary"):
        if export_format == "JSON (Complete Data)":
            portfolio_data = {
                'student': user_email,
                'generated_date': datetime.now().isoformat(),
                'progress': comp_data['overall_percentage'],
                'work_summary': {
                    'total_patients': my_work['total_patients'],
                    'total_pathways': my_work['total_pathways'],
                    'total_episodes': my_work['total_episodes']
                },
                'competencies': comp_data['competencies'],
                'detailed_work': my_work
            }
            st.download_button(
                "📥 Download Portfolio (JSON)",
                data=json.dumps(portfolio_data, indent=2, default=str),
                file_name=f"portfolio_{user_email.replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        elif export_format == "Text Summary":
            summary = generate_portfolio_summary(user_email, my_work, comp_data)
            st.download_button(
                "📥 Download Portfolio Summary (TXT)",
                data=summary,
                file_name=f"portfolio_summary_{user_email.replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:  # Competency Report
            report = generate_competency_report(user_email, comp_data)
            st.download_button(
                "📥 Download Competency Report (TXT)",
                data=report,
                file_name=f"competency_report_{user_email.replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        st.success("✅ Portfolio downloaded successfully!")


def render_learning_tips(comp_data: Dict):
    """Show learning tips and next steps"""
    
    st.subheader("🎯 Learning Tips & Next Steps")
    
    # Identify incomplete competencies
    incomplete = [comp for comp in comp_data['competencies'].values() if comp['status'] == 'incomplete']
    
    if not incomplete:
        st.success("""
        🎉 **CONGRATULATIONS!**
        
        You've completed all competencies! Next steps:
        1. Review your work for quality
        2. Export your portfolio
        3. Request teacher assessment
        4. Prepare for TQUK certification
        
        **Well done!** 🎓
        """)
    else:
        st.info("**Focus on completing these competencies:**")
        
        for comp in incomplete:
            remaining = comp['required'] - comp['completed']
            st.markdown(f"### {comp['name']}")
            st.write(f"**Need:** {remaining} more")
            st.write(f"**Tip:** {get_competency_tip(comp['name'])}")
            st.markdown("---")
    
    # General tips
    st.markdown("### 💡 General Tips")
    st.write("""
    - **Take your time:** Quality is more important than speed
    - **Ask questions:** Your teacher is here to help
    - **Practice regularly:** Consistent practice builds confidence
    - **Check your work:** Always verify data accuracy
    - **Use real scenarios:** Think about real NHS situations
    - **Keep notes:** Document what you learn
    """)


def get_competency_tip(comp_name: str) -> str:
    """Get specific tip for competency"""
    tips = {
        'Patient Registration': "Start with Patient Registration tool. Register 5 different patients with complete details including NHS number, GP, and next of kin.",
        'Pathway Creation': "Use Pathway Management tool. Create 3 pathways for different patients. Try different specialties (Orthopaedics, Cardiology, etc.)",
        'Episode Management': "Use Episode Management tool. Add 5 episodes across your pathways. Include consultant, treatment, and diagnostic episodes.",
        'RTT Clock Management': "In Pathway Management, use the 'Manage Pathway' tab. Practice pausing and resuming the RTT clock with proper reasons.",
        'Milestone Recording': "In Pathway Management, use the 'Record Milestones' tab. Record first appointment, decision to treat, and treatment start dates."
    }
    return tips.get(comp_name, "Check with your teacher for guidance.")


def generate_portfolio_summary(user_email: str, my_work: Dict, comp_data: Dict) -> str:
    """Generate text summary of portfolio"""
    summary = f"MY LEARNING PORTFOLIO - {user_email}\n"
    summary += "=" * 60 + "\n"
    summary += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    summary += f"OVERALL PROGRESS: {comp_data['overall_percentage']:.0f}%\n"
    summary += f"Status: {'READY FOR ASSESSMENT' if comp_data['overall_percentage'] >= 100 else 'IN PROGRESS'}\n\n"
    
    summary += "WORK SUMMARY:\n"
    summary += f"- Patients Registered: {my_work['total_patients']}\n"
    summary += f"- Pathways Created: {my_work['total_pathways']}\n"
    summary += f"- Episodes Managed: {my_work['total_episodes']}\n\n"
    
    summary += "COMPETENCY PROGRESS:\n"
    for comp_name, comp in comp_data['competencies'].items():
        status = "✓ COMPLETE" if comp['status'] == 'complete' else "✗ INCOMPLETE"
        summary += f"  {status} - {comp['name']}: {comp['completed']}/{comp['required']}\n"
    
    summary += "\nDETAILED WORK:\n"
    summary += "\nPatients:\n"
    for patient in my_work['patients']:
        summary += f"  - {patient.get('full_name')} ({patient.get('patient_id')})\n"
    
    summary += "\nPathways:\n"
    for pathway in my_work['pathways']:
        summary += f"  - {pathway.get('pathway_id')}: {pathway.get('patient_name')} - {pathway.get('specialty')}\n"
    
    summary += "\nEpisodes:\n"
    for episode in my_work['episodes']:
        summary += f"  - {episode.get('episode_id')} ({episode.get('episode_type')}): {episode.get('patient_name')}\n"
    
    return summary


def generate_competency_report(user_email: str, comp_data: Dict) -> str:
    """Generate competency-focused report"""
    report = f"TQUK COMPETENCY REPORT - {user_email}\n"
    report += "=" * 60 + "\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    report += f"OVERALL: {comp_data['overall_percentage']:.0f}% Complete\n"
    report += f"Progress: {comp_data['total_completed']}/{comp_data['total_required']} tasks\n\n"
    
    for comp_name, comp in comp_data['competencies'].items():
        report += f"\n{comp['name'].upper()}\n"
        report += "-" * 60 + "\n"
        report += f"Description: {comp['description']}\n"
        report += f"Progress: {comp['completed']}/{comp['required']}\n"
        report += f"Status: {comp['status'].upper()}\n"
        report += "\nTasks:\n"
        for i, task in enumerate(comp['tasks'], 1):
            status = "✓" if i <= comp['completed'] else "○"
            report += f"  {status} {task}\n"
    
    return report


def render_learning_resources():
    """Show quick access to learning resources"""
    
    st.subheader("📚 Learning Resources")
    
    st.info("Quick access to all your learning materials")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📄 Materials")
        st.write("Access lecture notes, handouts, and documents")
        if st.button("📚 Go to Learning Materials", key="goto_materials"):
            st.info("Navigate to '📚 Learning Materials' in the sidebar")
    
    with col2:
        st.markdown("### 🎥 Videos")
        st.write("Watch recorded lectures and tutorials")
        if st.button("🎥 Go to Video Library", key="goto_videos"):
            st.info("Navigate to '🎥 Video Library' in the sidebar")
    
    with col3:
        st.markdown("### 📢 News")
        st.write("View announcements and updates")
        if st.button("📢 Go to Announcements", key="goto_announcements"):
            st.info("Navigate to '📢 Announcements' in the sidebar")
    
    st.markdown("---")
    
    # Show recent materials preview
    st.markdown("### 📋 Recent Materials")
    
    from learning_materials import get_all_materials
    materials = get_all_materials()
    
    if materials:
        for material in materials[:3]:
            st.write(f"📄 **{material['title']}** - {material.get('category')} (Week {material.get('week', 0)})")
    else:
        st.info("No materials available yet.")
    
    st.markdown("---")
    
    # Show recent videos preview
    st.markdown("### 🎬 Recent Videos")
    
    from video_library import get_all_videos
    videos = get_all_videos()
    
    if videos:
        for video in videos[:3]:
            duration = video.get('duration_minutes', 0)
            st.write(f"🎥 **{video['title']}** - {duration} min (Week {video.get('week', 0)})")
    else:
        st.info("No videos available yet.")
