"""
TEACHER DASHBOARD
For TQUK assessors and trainers to view and mark student work

Features:
- View all students
- See each student's portfolio
- Mark competencies
- Export TQUK evidence
- Track progress
- Generate reports
"""

import streamlit as st
from datetime import datetime
from patient_registration_system import get_all_patients
from pathway_management_system import get_all_pathways
from episode_management_system import get_all_episodes
from typing import List, Dict
import json


def get_all_students() -> List[str]:
    """Get list of all unique student emails"""
    # Get all data
    patients = get_all_patients()
    pathways = get_all_pathways()
    episodes = get_all_episodes()
    
    # Extract unique user emails
    emails = set()
    
    for p in patients:
        if p.get('user_email'):
            emails.add(p.get('user_email'))
    
    for p in pathways:
        if p.get('user_email'):
            emails.add(p.get('user_email'))
    
    for e in episodes:
        if e.get('user_email'):
            emails.add(e.get('user_email'))
    
    return sorted(list(emails))


def get_student_work(student_email: str) -> Dict:
    """Get all work for specific student"""
    all_patients = get_all_patients()
    all_pathways = get_all_pathways()
    all_episodes = get_all_episodes()
    
    # Filter by student
    student_patients = [p for p in all_patients if p.get('user_email') == student_email]
    student_pathways = [p for p in all_pathways if p.get('user_email') == student_email]
    student_episodes = [e for e in all_episodes if e.get('user_email') == student_email]
    
    return {
        'email': student_email,
        'patients': student_patients,
        'pathways': student_pathways,
        'episodes': student_episodes,
        'total_patients': len(student_patients),
        'total_pathways': len(student_pathways),
        'total_episodes': len(student_episodes)
    }


def calculate_competencies(student_work: Dict) -> Dict:
    """Calculate TQUK competency completion"""
    
    competencies = {
        'patient_registration': {
            'required': 5,
            'completed': min(student_work['total_patients'], 5),
            'status': 'complete' if student_work['total_patients'] >= 5 else 'incomplete'
        },
        'pathway_creation': {
            'required': 3,
            'completed': min(student_work['total_pathways'], 3),
            'status': 'complete' if student_work['total_pathways'] >= 3 else 'incomplete'
        },
        'episode_management': {
            'required': 5,
            'completed': min(student_work['total_episodes'], 5),
            'status': 'complete' if student_work['total_episodes'] >= 5 else 'incomplete'
        },
        'rtt_clock_management': {
            'required': 1,
            'completed': len([p for p in student_work['pathways'] if p.get('total_pause_days', 0) > 0]),
            'status': 'complete' if any(p.get('total_pause_days', 0) > 0 for p in student_work['pathways']) else 'incomplete'
        },
        'milestone_recording': {
            'required': 3,
            'completed': len([p for p in student_work['pathways'] if p.get('first_appointment_date')]),
            'status': 'complete' if len([p for p in student_work['pathways'] if p.get('first_appointment_date')]) >= 3 else 'incomplete'
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


def render_teacher_dashboard():
    """Main teacher dashboard interface"""
    
    st.header("👨‍🏫 Teacher Dashboard")
    st.markdown("**View and assess all student work for TQUK certification**")
    
    st.success("""
    **Teacher Dashboard Features:**
    - 📊 View all students
    - 📋 See each student's portfolio
    - ✅ Mark competencies
    - 📄 Export TQUK evidence
    - 📈 Track progress
    - 🎓 Generate reports
    """)
    
    # Get all students
    students = get_all_students()
    
    if not students:
        st.warning("📚 No student work found yet. Students need to register patients and create pathways.")
        return
    
    st.write(f"**Total Students:** {len(students)}")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 All Students Overview",
        "📋 Student Portfolio",
        "📄 Export Evidence"
    ])
    
    with tab1:
        render_all_students_overview(students)
    
    with tab2:
        render_student_portfolio(students)
    
    with tab3:
        render_export_evidence(students)


def render_all_students_overview(students: List[str]):
    """Overview of all students"""
    
    st.subheader("📊 All Students Overview")
    
    # Get work for all students
    all_student_data = []
    for student in students:
        work = get_student_work(student)
        competencies = calculate_competencies(work)
        all_student_data.append({
            'email': student,
            'work': work,
            'competencies': competencies
        })
    
    # Display summary table
    st.markdown("### 📋 Student Progress Summary")
    
    for student_data in all_student_data:
        email = student_data['email']
        work = student_data['work']
        comp = student_data['competencies']
        
        with st.expander(f"👤 {email} - {comp['overall_percentage']:.0f}% Complete"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Patients Registered", work['total_patients'])
                st.metric("Pathways Created", work['total_pathways'])
            
            with col2:
                st.metric("Episodes Added", work['total_episodes'])
                st.metric("Overall Progress", f"{comp['overall_percentage']:.0f}%")
            
            with col3:
                st.markdown("**Competencies:**")
                for comp_name, comp_data in comp['competencies'].items():
                    status_icon = "✅" if comp_data['status'] == 'complete' else "⏳"
                    st.write(f"{status_icon} {comp_name.replace('_', ' ').title()}: {comp_data['completed']}/{comp_data['required']}")
            
            with col4:
                if comp['overall_percentage'] >= 100:
                    st.success("✅ **READY FOR ASSESSMENT**")
                elif comp['overall_percentage'] >= 75:
                    st.info("🔵 **NEARLY COMPLETE**")
                elif comp['overall_percentage'] >= 50:
                    st.warning("🟡 **IN PROGRESS**")
                else:
                    st.error("🔴 **JUST STARTED**")


def render_student_portfolio(students: List[str]):
    """Detailed view of individual student portfolio"""
    
    st.subheader("📋 Student Portfolio")
    
    # Select student
    selected_student = st.selectbox("Select Student:", ["-- Select Student --"] + students)
    
    if selected_student == "-- Select Student --":
        return
    
    # Get student work
    work = get_student_work(selected_student)
    comp_data = calculate_competencies(work)
    
    st.markdown(f"### 👤 {selected_student}")
    
    # Overall progress
    st.progress(comp_data['overall_percentage'] / 100)
    st.write(f"**Overall Progress:** {comp_data['overall_percentage']:.0f}%")
    
    st.markdown("---")
    
    # Competency breakdown
    st.markdown("### ✅ Competency Checklist")
    
    for comp_name, comp_details in comp_data['competencies'].items():
        status_icon = "✅" if comp_details['status'] == 'complete' else "⏳"
        st.write(f"{status_icon} **{comp_name.replace('_', ' ').title()}:** {comp_details['completed']}/{comp_details['required']}")
    
    st.markdown("---")
    
    # Detailed work
    detail_tab1, detail_tab2, detail_tab3 = st.tabs([
        f"👤 Patients ({work['total_patients']})",
        f"📁 Pathways ({work['total_pathways']})",
        f"📋 Episodes ({work['total_episodes']})"
    ])
    
    with detail_tab1:
        st.markdown("### 👤 Registered Patients")
        for patient in work['patients']:
            st.write(f"- **{patient.get('full_name')}** ({patient.get('patient_id')}) - {patient.get('registration_date', 'N/A')}")
    
    with detail_tab2:
        st.markdown("### 📁 Created Pathways")
        for pathway in work['pathways']:
            st.write(f"- **{pathway.get('pathway_id')}** - {pathway.get('patient_name')} ({pathway.get('specialty')}) - Status: {pathway.get('status')}")
    
    with detail_tab3:
        st.markdown("### 📋 Managed Episodes")
        for episode in work['episodes']:
            st.write(f"- **{episode.get('episode_id')}** ({episode.get('episode_type')}) - {episode.get('patient_name')}")


def render_export_evidence(students: List[str]):
    """Export TQUK evidence"""
    
    st.subheader("📄 Export TQUK Evidence")
    
    st.info("""
    **Export Options:**
    - Individual student evidence pack
    - Class summary report
    - Competency matrix
    - Portfolio screenshots
    """)
    
    # Select student for export
    selected_student = st.selectbox("Select Student for Export:", ["-- Select Student --", "All Students"] + students)
    
    if selected_student == "-- Select Student --":
        return
    
    export_format = st.radio("Export Format:", ["JSON", "Text Summary", "CSV"])
    
    if st.button("📥 Generate Evidence Pack", type="primary"):
        if selected_student == "All Students":
            # Export all students
            all_data = []
            for student in students:
                work = get_student_work(student)
                comp = calculate_competencies(work)
                all_data.append({
                    'student': student,
                    'work': work,
                    'competencies': comp
                })
            
            if export_format == "JSON":
                st.download_button(
                    "📥 Download All Students Evidence (JSON)",
                    data=json.dumps(all_data, indent=2, default=str),
                    file_name=f"tquk_evidence_all_students_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            else:
                summary = generate_text_summary(all_data)
                st.download_button(
                    "📥 Download All Students Summary (TXT)",
                    data=summary,
                    file_name=f"tquk_summary_all_students_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        else:
            # Export single student
            work = get_student_work(selected_student)
            comp = calculate_competencies(work)
            
            if export_format == "JSON":
                evidence_pack = {
                    'student': selected_student,
                    'generated_date': datetime.now().isoformat(),
                    'work_summary': work,
                    'competencies': comp
                }
                st.download_button(
                    f"📥 Download {selected_student} Evidence (JSON)",
                    data=json.dumps(evidence_pack, indent=2, default=str),
                    file_name=f"tquk_evidence_{selected_student.replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            else:
                summary = generate_student_summary(selected_student, work, comp)
                st.download_button(
                    f"📥 Download {selected_student} Summary (TXT)",
                    data=summary,
                    file_name=f"tquk_summary_{selected_student.replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        
        st.success("✅ Evidence pack generated successfully!")


def generate_text_summary(all_data: List[Dict]) -> str:
    """Generate text summary for all students"""
    summary = "TQUK EVIDENCE SUMMARY - ALL STUDENTS\n"
    summary += "=" * 60 + "\n"
    summary += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for student_data in all_data:
        student = student_data['student']
        work = student_data['work']
        comp = student_data['competencies']
        
        summary += f"\nSTUDENT: {student}\n"
        summary += "-" * 60 + "\n"
        summary += f"Overall Progress: {comp['overall_percentage']:.0f}%\n"
        summary += f"Patients Registered: {work['total_patients']}\n"
        summary += f"Pathways Created: {work['total_pathways']}\n"
        summary += f"Episodes Managed: {work['total_episodes']}\n"
        summary += "\nCompetencies:\n"
        for comp_name, comp_details in comp['competencies'].items():
            status = "✓" if comp_details['status'] == 'complete' else "✗"
            summary += f"  {status} {comp_name.replace('_', ' ').title()}: {comp_details['completed']}/{comp_details['required']}\n"
        summary += "\n"
    
    return summary


def generate_student_summary(student_email: str, work: Dict, comp: Dict) -> str:
    """Generate text summary for single student"""
    summary = f"TQUK EVIDENCE PACK - {student_email}\n"
    summary += "=" * 60 + "\n"
    summary += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    summary += f"OVERALL PROGRESS: {comp['overall_percentage']:.0f}%\n"
    summary += f"Status: {'READY FOR ASSESSMENT' if comp['overall_percentage'] >= 100 else 'IN PROGRESS'}\n\n"
    
    summary += "WORK SUMMARY:\n"
    summary += f"- Patients Registered: {work['total_patients']}\n"
    summary += f"- Pathways Created: {work['total_pathways']}\n"
    summary += f"- Episodes Managed: {work['total_episodes']}\n\n"
    
    summary += "COMPETENCY CHECKLIST:\n"
    for comp_name, comp_details in comp['competencies'].items():
        status = "✓ COMPLETE" if comp_details['status'] == 'complete' else "✗ INCOMPLETE"
        summary += f"  {status} - {comp_name.replace('_', ' ').title()}: {comp_details['completed']}/{comp_details['required']}\n"
    
    summary += "\nDETAILED WORK:\n"
    summary += "\nPatients:\n"
    for patient in work['patients']:
        summary += f"  - {patient.get('full_name')} ({patient.get('patient_id')})\n"
    
    summary += "\nPathways:\n"
    for pathway in work['pathways']:
        summary += f"  - {pathway.get('pathway_id')}: {pathway.get('patient_name')} - {pathway.get('specialty')}\n"
    
    summary += "\nEpisodes:\n"
    for episode in work['episodes']:
        summary += f"  - {episode.get('episode_id')} ({episode.get('episode_type')}): {episode.get('patient_name')}\n"
    
    return summary
