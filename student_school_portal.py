"""
T21 SERVICES - STUDENT SCHOOL PORTAL
Student interface for school management system

Features:
- View enrolled classes
- Access course materials
- View timetable
- Check grades & transcripts
- View attendance
- Submit assignments
- Access exam results
- Academic calendar
- Announcements
"""

import streamlit as st
from school_management_system import (
    calculate_attendance_percentage, calculate_final_grade,
    CLASSES_DB, ENROLLMENTS_DB, EXAMS_DB, GRADES_DB,
    ATTENDANCE_DB, MATERIALS_DB, ANNOUNCEMENTS_DB
)
from database_schema import load_db
from datetime import datetime


def render_student_school_portal(student_email):
    """Main student school portal interface"""
    
    st.header("🎓 My Academic Portal")
    st.markdown("**Your complete academic dashboard**")
    
    # Get student's enrollments
    enrollments = load_db(ENROLLMENTS_DB)
    student_enrollments = [e for e in enrollments.values() if e['student_email'] == student_email]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_classes = len([e for e in student_enrollments if e['status'] == 'active'])
        st.metric("📚 Active Classes", active_classes)
    
    with col2:
        completed = len([e for e in student_enrollments if e['status'] == 'completed'])
        st.metric("✅ Completed", completed)
    
    with col3:
        # Calculate average attendance
        if student_enrollments:
            avg_attendance = sum([e.get('attendance_percentage', 0) for e in student_enrollments]) / len(student_enrollments)
            st.metric("📊 Attendance", f"{int(avg_attendance)}%")
        else:
            st.metric("📊 Attendance", "N/A")
    
    with col4:
        # Calculate GPA (placeholder)
        st.metric("🎯 GPA", "N/A")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📚 My Classes",
        "📋 Exams & Grades",
        "✅ Attendance",
        "📄 Materials",
        "📅 Calendar",
        "📜 Transcript"
    ])
    
    with tab1:
        render_student_classes(student_email, student_enrollments)
    
    with tab2:
        render_student_grades(student_email, student_enrollments)
    
    with tab3:
        render_student_attendance(student_email, student_enrollments)
    
    with tab4:
        render_student_materials(student_email, student_enrollments)
    
    with tab5:
        render_student_calendar(student_email)
    
    with tab6:
        render_student_transcript(student_email)


def render_student_classes(student_email, enrollments):
    """Display student's enrolled classes"""
    
    st.subheader("📚 My Classes")
    
    if not enrollments:
        st.info("You are not enrolled in any classes yet. Contact your advisor for enrollment.")
        return
    
    classes = load_db(CLASSES_DB)
    
    # Show active classes
    active = [e for e in enrollments if e['status'] == 'active']
    
    if active:
        st.markdown(f"**Active Classes: {len(active)}**")
        
        for enrollment in active:
            class_id = enrollment['class_id']
            
            if class_id not in classes:
                continue
            
            class_data = classes[class_id]
            
            with st.expander(f"📖 {class_data['name']} - {class_data['semester']}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Instructor:** {class_data['instructor_email']}")
                    st.markdown(f"**Academic Year:** {class_data['academic_year']}")
                    st.markdown(f"**Room:** {class_data.get('room', 'TBA')}")
                
                with col2:
                    attendance_pct = calculate_attendance_percentage(student_email, class_id)
                    if attendance_pct >= 75:
                        st.success(f"📊 Attendance: {attendance_pct}%")
                    else:
                        st.warning(f"📊 Attendance: {attendance_pct}%")
                    
                    # Get current grade
                    grade_pct, letter_grade = calculate_final_grade(student_email, class_id)
                    if grade_pct > 0:
                        st.info(f"🎯 Current Grade: {letter_grade} ({grade_pct:.1f}%)")
                
                # Schedule
                if class_data['schedule']:
                    st.markdown("**Class Schedule:**")
                    for day, time in class_data['schedule'].items():
                        st.markdown(f"- {day}: {time}")
    else:
        st.info("No active classes this semester")


def render_student_grades(student_email, enrollments):
    """Display student's exam grades"""
    
    st.subheader("📋 Exams & Grades")
    
    if not enrollments:
        st.info("No grades to display")
        return
    
    exams = load_db(EXAMS_DB)
    grades = load_db(GRADES_DB)
    classes = load_db(CLASSES_DB)
    
    # Get student's grades
    student_grades = {gid: g for gid, g in grades.items() if g['student_email'] == student_email}
    
    if not student_grades:
        st.info("No grades recorded yet")
        return
    
    # Group by class
    for enrollment in enrollments:
        class_id = enrollment['class_id']
        
        if class_id not in classes:
            continue
        
        class_data = classes[class_id]
        
        # Get exams for this class
        class_exams = {eid: e for eid, e in exams.items() if e['class_id'] == class_id}
        
        if not class_exams:
            continue
        
        with st.expander(f"📖 {class_data['name']}", expanded=True):
            # Calculate final grade
            grade_pct, letter_grade = calculate_final_grade(student_email, class_id)
            
            if grade_pct > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### Current Grade: {letter_grade}")
                
                with col2:
                    st.markdown(f"### Percentage: {grade_pct:.1f}%")
                
                st.progress(grade_pct / 100)
            
            st.markdown("---")
            st.markdown("**Individual Assessments:**")
            
            # Show individual exam grades
            for exam_id, exam in class_exams.items():
                # Find student's grade for this exam
                exam_grade = None
                for grade_id, grade in student_grades.items():
                    if grade['exam_id'] == exam_id:
                        exam_grade = grade
                        break
                
                col_a, col_b, col_c = st.columns([2, 1, 1])
                
                with col_a:
                    st.markdown(f"**{exam['name']}** ({exam['exam_type'].title()})")
                
                with col_b:
                    if exam_grade:
                        marks = exam_grade['marks_obtained']
                        total = exam['total_marks']
                        percentage = (marks / total) * 100
                        
                        if percentage >= 50:
                            st.success(f"{marks}/{total} ({percentage:.0f}%)")
                        else:
                            st.error(f"{marks}/{total} ({percentage:.0f}%)")
                    else:
                        st.info("Not graded yet")
                
                with col_c:
                    st.caption(f"Weight: {exam.get('weightage', 0)}%")
                
                if exam_grade and exam_grade['feedback']:
                    st.info(f"💬 Feedback: {exam_grade['feedback']}")


def render_student_attendance(student_email, enrollments):
    """Display attendance records"""
    
    st.subheader("✅ My Attendance")
    
    if not enrollments:
        st.info("No attendance records")
        return
    
    attendance = load_db(ATTENDANCE_DB)
    classes = load_db(CLASSES_DB)
    
    # Group by class
    for enrollment in enrollments:
        class_id = enrollment['class_id']
        
        if class_id not in classes:
            continue
        
        class_data = classes[class_id]
        
        # Get attendance for this class
        class_attendance = [a for a in attendance.values() 
                           if a['student_email'] == student_email and a['class_id'] == class_id]
        
        if not class_attendance:
            continue
        
        with st.expander(f"📖 {class_data['name']}", expanded=False):
            # Calculate percentage
            percentage = calculate_attendance_percentage(student_email, class_id)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Attendance Rate", f"{percentage}%")
            
            with col2:
                total = len(class_attendance)
                present = len([a for a in class_attendance if a['status'] in ['present', 'late']])
                st.metric("Days Present", f"{present}/{total}")
            
            if percentage < 75:
                st.warning("⚠️ Your attendance is below 75%. This may affect your eligibility for exams.")
            
            st.markdown("---")
            st.markdown("**Recent Attendance:**")
            
            # Sort by date (newest first)
            sorted_attendance = sorted(class_attendance, key=lambda x: x['date'], reverse=True)
            
            for record in sorted_attendance[:10]:  # Show last 10
                status_icon = {
                    'present': '✅',
                    'absent': '❌',
                    'late': '⏰',
                    'excused': '📝'
                }.get(record['status'], '❓')
                
                st.markdown(f"{status_icon} {record['date']} - {record['status'].title()}")
                if record['remarks']:
                    st.caption(f"   Note: {record['remarks']}")


def render_student_materials(student_email, enrollments):
    """Display course materials"""
    
    st.subheader("📄 Course Materials")
    
    if not enrollments:
        st.info("No materials available")
        return
    
    materials = load_db(MATERIALS_DB)
    classes = load_db(CLASSES_DB)
    
    # Get materials for enrolled classes
    for enrollment in enrollments:
        class_id = enrollment['class_id']
        
        if class_id not in classes:
            continue
        
        class_data = classes[class_id]
        
        # Get materials for this class
        class_materials = [m for m in materials.values() if m['class_id'] == class_id]
        
        if not class_materials:
            continue
        
        with st.expander(f"📖 {class_data['name']}", expanded=False):
            st.markdown(f"**{len(class_materials)} materials available**")
            
            for material in class_materials:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    file_icon = {
                        'pdf': '📄',
                        'video': '🎥',
                        'document': '📝',
                        'presentation': '📊'
                    }.get(material['file_type'], '📎')
                    
                    st.markdown(f"{file_icon} **{material['title']}**")
                    st.caption(material['description'])
                
                with col2:
                    if material['file_url']:
                        st.link_button("📥 Download", material['file_url'])
                    else:
                        st.button("📥 View", key=material['material_id'])
                
                st.markdown("---")


def render_student_calendar(student_email):
    """Display academic calendar"""
    
    st.subheader("📅 Academic Calendar")
    
    announcements = load_db(ANNOUNCEMENTS_DB)
    
    if not announcements:
        st.info("No upcoming events")
        return
    
    # Sort by start date
    sorted_events = sorted(announcements.values(), key=lambda x: x['start_date'])
    
    st.markdown("**Upcoming Events:**")
    
    for event in sorted_events:
        event_icon = {
            'holiday': '🎉',
            'exam': '📝',
            'registration': '📋',
            'orientation': '🎓'
        }.get(event['event_type'], '📅')
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"{event_icon} **{event['title']}**")
                st.caption(event['description'])
            
            with col2:
                st.markdown(f"**{event['start_date']}**")
                if event['end_date'] != event['start_date']:
                    st.caption(f"to {event['end_date']}")
            
            st.markdown("---")


def render_student_transcript(student_email):
    """Display academic transcript"""
    
    st.subheader("📜 Academic Transcript")
    
    enrollments = load_db(ENROLLMENTS_DB)
    classes = load_db(CLASSES_DB)
    
    student_enrollments = [e for e in enrollments.values() if e['student_email'] == student_email]
    
    if not student_enrollments:
        st.info("No transcript data available")
        return
    
    st.markdown("### Official Transcript")
    st.markdown(f"**Student:** {student_email}")
    st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    
    # Group by status
    completed = [e for e in student_enrollments if e['status'] == 'completed']
    in_progress = [e for e in student_enrollments if e['status'] == 'active']
    
    if completed:
        st.markdown("### ✅ Completed Courses")
        
        for enrollment in completed:
            class_id = enrollment['class_id']
            
            if class_id not in classes:
                continue
            
            class_data = classes[class_id]
            grade_pct, letter_grade = calculate_final_grade(student_email, class_id)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{class_data['name']}**")
                st.caption(f"{class_data['semester']} {class_data['academic_year']}")
            
            with col2:
                if grade_pct > 0:
                    st.markdown(f"**{letter_grade}**")
                else:
                    st.markdown("**N/A**")
            
            with col3:
                st.markdown(f"**{enrollment.get('credits_earned', 0)} Credits**")
    
    if in_progress:
        st.markdown("---")
        st.markdown("### 📚 In Progress")
        
        for enrollment in in_progress:
            class_id = enrollment['class_id']
            
            if class_id not in classes:
                continue
            
            class_data = classes[class_id]
            
            st.markdown(f"- {class_data['name']} ({class_data['semester']} {class_data['academic_year']})")
    
    st.markdown("---")
    
    # Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_credits = sum([e.get('credits_earned', 0) for e in completed])
        st.metric("Total Credits", total_credits)
    
    with col2:
        st.metric("Completed Courses", len(completed))
    
    with col3:
        st.metric("GPA", "N/A")  # Calculate properly
    
    st.markdown("---")
    
    if st.button("📥 Download Transcript (PDF)", type="primary"):
        st.info("PDF download feature coming soon!")
