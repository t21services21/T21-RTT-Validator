"""
T21 SERVICES - SCHOOL MANAGEMENT ADMIN UI
Complete training institution management interface

Features:
- Department management
- Program/course management
- Class/batch creation
- Student enrollment
- Exam creation & grading
- Attendance tracking
- Materials upload
- Timetable scheduling
- Reports & analytics
"""

import streamlit as st
from school_management_system import (
    create_department, create_program, create_class,
    enroll_student_in_class, create_exam, record_grade,
    mark_attendance, upload_material, create_event,
    calculate_attendance_percentage, calculate_final_grade,
    DEPARTMENTS_DB, PROGRAMS_DB, CLASSES_DB, ENROLLMENTS_DB,
    EXAMS_DB, GRADES_DB, ATTENDANCE_DB, MATERIALS_DB
)
from database_schema import load_db, save_db
from student_auth import list_all_students
from datetime import datetime, timedelta


def render_school_management_admin():
    """Main school management admin interface"""
    
    st.header("🏫 School Management System")
    st.markdown("**Complete training institution management**")
    
    # Tabs for different management areas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🏛️ Departments",
        "📚 Programs",
        "👥 Classes",
        "📝 Enrollments",
        "📋 Exams",
        "✅ Attendance",
        "📄 Materials",
        "📊 Reports"
    ])
    
    with tab1:
        render_department_management()
    
    with tab2:
        render_program_management()
    
    with tab3:
        render_class_management()
    
    with tab4:
        render_enrollment_management()
    
    with tab5:
        render_exam_management()
    
    with tab6:
        render_attendance_management()
    
    with tab7:
        render_materials_management()
    
    with tab8:
        render_reports_analytics()


def render_department_management():
    """Manage departments/faculties"""
    
    st.subheader("🏛️ Department Management")
    
    departments = load_db(DEPARTMENTS_DB)
    
    # Display existing departments
    st.markdown("### Existing Departments")
    
    if departments:
        for dept_id, dept in departments.items():
            with st.expander(f"📂 {dept['name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Head:** {dept['head_of_department']}")
                    st.markdown(f"**Email:** {dept['email']}")
                    st.markdown(f"**Phone:** {dept['phone']}")
                
                with col2:
                    st.metric("Programs", len(dept['programs']))
                    st.metric("Staff", dept['staff_count'])
                    st.metric("Students", dept['student_count'])
                
                st.markdown(f"**Description:** {dept['description']}")
    else:
        st.info("No departments yet. Create your first department!")
    
    st.markdown("---")
    
    # Create new department
    st.markdown("### ➕ Create New Department")
    
    with st.form("create_department"):
        col1, col2 = st.columns(2)
        
        with col1:
            dept_name = st.text_input("Department Name*", placeholder="e.g., Healthcare Training")
            head_name = st.text_input("Head of Department*", placeholder="e.g., Dr. Sarah Johnson")
            email = st.text_input("Contact Email*", placeholder="department@email.com")
        
        with col2:
            description = st.text_area("Description*", placeholder="Brief description of department", height=100)
            phone = st.text_input("Contact Phone", placeholder="+44 123 456 7890")
        
        submit = st.form_submit_button("➕ Create Department", type="primary")
        
        if submit:
            if not dept_name or not description or not head_name or not email:
                st.error("Please fill all required fields")
            else:
                dept_id = create_department(dept_name, description, head_name, email, phone)
                st.success(f"✅ Department created! ID: {dept_id}")
                st.balloons()
                st.rerun()


def render_program_management():
    """Manage training programs"""
    
    st.subheader("📚 Program Management")
    
    departments = load_db(DEPARTMENTS_DB)
    programs = load_db(PROGRAMS_DB)
    
    if not departments:
        st.warning("Create departments first before adding programs!")
        return
    
    # Display existing programs
    st.markdown("### Existing Programs")
    
    if programs:
        for prog_id, prog in programs.items():
            with st.expander(f"📖 {prog['name']} - {prog['level']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Level:** {prog['level']}")
                    st.markdown(f"**Duration:** {prog['duration_months']} months")
                
                with col2:
                    st.markdown(f"**Qualification:** {prog['qualification']}")
                    st.markdown(f"**Status:** {prog['status']}")
                
                with col3:
                    st.metric("Courses", len(prog['courses']))
                    st.metric("Credits", prog['total_credits'])
                
                st.markdown(f"**Description:** {prog['description']}")
                
                if prog['prerequisites']:
                    st.markdown(f"**Prerequisites:** {prog['prerequisites']}")
    else:
        st.info("No programs yet. Create your first program!")
    
    st.markdown("---")
    
    # Create new program
    st.markdown("### ➕ Create New Program")
    
    with st.form("create_program"):
        dept_options = {dept['name']: dept_id for dept_id, dept in departments.items()}
        selected_dept = st.selectbox("Department*", list(dept_options.keys()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            prog_name = st.text_input("Program Name*", placeholder="e.g., RTT Specialist Certificate")
            level = st.selectbox("Level*", [
                "Certificate",
                "Diploma", 
                "Advanced Diploma",
                "Bachelor's Degree",
                "Master's Degree",
                "Professional Certificate"
            ])
            duration = st.number_input("Duration (months)*", min_value=1, value=6)
        
        with col2:
            qualification = st.text_input("Qualification Awarded*", placeholder="e.g., Certified RTT Professional")
            description = st.text_area("Description*", height=100)
            prerequisites = st.text_input("Prerequisites", placeholder="e.g., Healthcare background")
        
        submit = st.form_submit_button("➕ Create Program", type="primary")
        
        if submit:
            if not prog_name or not qualification or not description:
                st.error("Please fill all required fields")
            else:
                dept_id = dept_options[selected_dept]
                prog_id = create_program(dept_id, prog_name, description, duration, level, qualification, prerequisites)
                st.success(f"✅ Program created! ID: {prog_id}")
                st.balloons()
                st.rerun()


def render_class_management():
    """Manage classes/batches"""
    
    st.subheader("👥 Class/Batch Management")
    
    programs = load_db(PROGRAMS_DB)
    classes = load_db(CLASSES_DB)
    
    if not programs:
        st.warning("Create programs first before adding classes!")
        return
    
    # Display existing classes
    st.markdown("### Active Classes")
    
    if classes:
        for class_id, class_data in classes.items():
            status_icon = "🟢" if class_data['status'] == 'active' else "🔴"
            
            with st.expander(f"{status_icon} {class_data['name']} - {class_data['academic_year']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Semester:** {class_data['semester']}")
                    st.markdown(f"**Instructor:** {class_data['instructor_email']}")
                
                with col2:
                    st.markdown(f"**Students:** {len(class_data['enrolled_students'])}/{class_data['max_students']}")
                    st.markdown(f"**Room:** {class_data.get('room', 'TBA')}")
                
                with col3:
                    st.markdown(f"**Status:** {class_data['status']}")
                
                if class_data['schedule']:
                    st.markdown("**Schedule:**")
                    for day, time in class_data['schedule'].items():
                        st.markdown(f"- {day}: {time}")
    else:
        st.info("No classes yet. Create your first class!")
    
    st.markdown("---")
    
    # Create new class
    st.markdown("### ➕ Create New Class")
    
    with st.form("create_class"):
        prog_options = {prog['name']: prog_id for prog_id, prog in programs.items()}
        selected_prog = st.selectbox("Program*", list(prog_options.keys()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            class_name = st.text_input("Class Name*", placeholder="e.g., RTT-2025-A")
            semester = st.selectbox("Semester*", ["Semester 1", "Semester 2", "Summer"])
            academic_year = st.text_input("Academic Year*", placeholder="2025")
        
        with col2:
            instructor = st.text_input("Instructor Email*", placeholder="instructor@email.com")
            max_students = st.number_input("Max Students*", min_value=1, value=30)
        
        st.markdown("**Schedule:**")
        schedule_cols = st.columns(3)
        schedule = {}
        
        with schedule_cols[0]:
            mon = st.text_input("Monday", placeholder="09:00-11:00")
            if mon: schedule["Monday"] = mon
            tue = st.text_input("Tuesday", placeholder="09:00-11:00")
            if tue: schedule["Tuesday"] = tue
        
        with schedule_cols[1]:
            wed = st.text_input("Wednesday", placeholder="09:00-11:00")
            if wed: schedule["Wednesday"] = wed
            thu = st.text_input("Thursday", placeholder="09:00-11:00")
            if thu: schedule["Thursday"] = thu
        
        with schedule_cols[2]:
            fri = st.text_input("Friday", placeholder="09:00-11:00")
            if fri: schedule["Friday"] = fri
        
        submit = st.form_submit_button("➕ Create Class", type="primary")
        
        if submit:
            if not class_name or not instructor:
                st.error("Please fill all required fields")
            else:
                prog_id = prog_options[selected_prog]
                class_id = create_class(prog_id, class_name, semester, academic_year, instructor, max_students, schedule)
                st.success(f"✅ Class created! ID: {class_id}")
                st.balloons()
                st.rerun()


def render_enrollment_management():
    """Manage student enrollments"""
    
    st.subheader("📝 Student Enrollment Management")
    
    classes = load_db(CLASSES_DB)
    all_students = list_all_students()
    
    if not classes:
        st.warning("Create classes first!")
        return
    
    if not all_students:
        st.warning("No students in system!")
        return
    
    st.markdown("### Enroll Student in Class")
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_options = {f"{s['full_name']} ({s['email']})": s['email'] for s in all_students}
        selected_student = st.selectbox("Select Student", list(student_options.keys()))
        student_email = student_options[selected_student]
    
    with col2:
        class_options = {f"{c['name']} - {c['academic_year']}": cid for cid, c in classes.items()}
        selected_class = st.selectbox("Select Class", list(class_options.keys()))
        class_id = class_options[selected_class]
    
    if st.button("📝 Enroll Student", type="primary"):
        success, message = enroll_student_in_class(student_email, class_id)
        if success:
            st.success(message)
            st.balloons()
        else:
            st.error(message)
    
    st.markdown("---")
    
    # View enrollments by class
    st.markdown("### View Class Enrollments")
    
    view_class = st.selectbox("Select Class to View", list(class_options.keys()), key="view_class")
    view_class_id = class_options[view_class]
    
    class_data = classes[view_class_id]
    enrolled = class_data['enrolled_students']
    
    if enrolled:
        st.markdown(f"**Enrolled Students: {len(enrolled)}/{class_data['max_students']}**")
        
        for email in enrolled:
            st.markdown(f"- {email}")
    else:
        st.info("No students enrolled yet")


def render_exam_management():
    """Manage exams and grading"""
    
    st.subheader("📋 Exam & Assessment Management")
    
    classes = load_db(CLASSES_DB)
    exams = load_db(EXAMS_DB)
    
    if not classes:
        st.warning("Create classes first!")
        return
    
    # Display existing exams
    st.markdown("### Scheduled Exams")
    
    if exams:
        for exam_id, exam in exams.items():
            with st.expander(f"📝 {exam['name']} ({exam['exam_type'].title()})", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Date:** {exam['exam_date']}")
                    st.markdown(f"**Duration:** {exam['duration_minutes']} min")
                
                with col2:
                    st.markdown(f"**Total Marks:** {exam['total_marks']}")
                    st.markdown(f"**Passing Marks:** {exam['passing_marks']}")
                
                with col3:
                    st.markdown(f"**Weightage:** {exam.get('weightage', 0)}%")
                
                # Quick grading
                st.markdown("**Quick Grade Entry:**")
                grade_student = st.text_input("Student Email", key=f"grade_{exam_id}")
                marks = st.number_input("Marks", min_value=0, max_value=exam['total_marks'], key=f"marks_{exam_id}")
                
                if st.button("💾 Save Grade", key=f"save_{exam_id}"):
                    if grade_student:
                        record_grade(grade_student, exam_id, marks)
                        st.success("Grade saved!")
    else:
        st.info("No exams scheduled")
    
    st.markdown("---")
    
    # Create new exam
    st.markdown("### ➕ Create New Exam")
    
    with st.form("create_exam"):
        class_options = {f"{c['name']}": cid for cid, c in classes.items()}
        selected_class = st.selectbox("Class*", list(class_options.keys()))
        
        col1, col2 = st.columns(2)
        
        with col1:
            exam_name = st.text_input("Exam Name*", placeholder="e.g., Midterm Exam")
            exam_type = st.selectbox("Type*", ["quiz", "midterm", "final", "assignment", "practical", "project"])
            exam_date = st.date_input("Exam Date*")
        
        with col2:
            total_marks = st.number_input("Total Marks*", min_value=1, value=100)
            passing_marks = st.number_input("Passing Marks*", min_value=1, value=50)
            duration = st.number_input("Duration (minutes)*", min_value=1, value=120)
        
        weightage = st.slider("Weightage (%)", 0, 100, 30, help="Contribution to final grade")
        
        submit = st.form_submit_button("➕ Create Exam", type="primary")
        
        if submit:
            if not exam_name:
                st.error("Please fill required fields")
            else:
                class_id = class_options[selected_class]
                exam_id = create_exam(class_id, exam_name, exam_type, total_marks, passing_marks, exam_date.isoformat(), duration)
                
                # Update weightage
                exams = load_db(EXAMS_DB)
                exams[exam_id]['weightage'] = weightage
                save_db(EXAMS_DB, exams)
                
                st.success(f"✅ Exam created! ID: {exam_id}")
                st.rerun()


def render_attendance_management():
    """Manage attendance tracking"""
    
    st.subheader("✅ Attendance Management")
    
    classes = load_db(CLASSES_DB)
    
    if not classes:
        st.warning("Create classes first!")
        return
    
    st.markdown("### Mark Attendance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        class_options = {f"{c['name']}": cid for cid, c in classes.items()}
        selected_class = st.selectbox("Select Class", list(class_options.keys()))
        class_id = class_options[selected_class]
    
    with col2:
        attendance_date = st.date_input("Date", value=datetime.now())
    
    class_data = classes[class_id]
    enrolled_students = class_data['enrolled_students']
    
    if not enrolled_students:
        st.info("No students enrolled in this class")
        return
    
    st.markdown(f"**Mark attendance for {len(enrolled_students)} students:**")
    
    attendance_data = {}
    
    for email in enrolled_students:
        col_a, col_b, col_c = st.columns([2, 1, 2])
        
        with col_a:
            st.markdown(f"**{email}**")
        
        with col_b:
            status = st.selectbox(
                "Status",
                ["present", "absent", "late", "excused"],
                key=f"status_{email}",
                label_visibility="collapsed"
            )
            attendance_data[email] = status
        
        with col_c:
            # Show attendance percentage
            percentage = calculate_attendance_percentage(email, class_id)
            if percentage >= 75:
                st.success(f"📊 {percentage}%")
            elif percentage >= 50:
                st.warning(f"📊 {percentage}%")
            else:
                st.error(f"📊 {percentage}%")
    
    if st.button("💾 Save Attendance", type="primary"):
        date_str = attendance_date.isoformat()
        for email, status in attendance_data.items():
            mark_attendance(class_id, date_str, email, status)
        st.success(f"✅ Attendance marked for {len(attendance_data)} students!")
        st.balloons()


def render_materials_management():
    """Manage learning materials"""
    
    st.subheader("📄 Learning Materials")
    
    st.info("💡 Upload materials feature - Coming soon! For now, materials can be added to LMS courses.")


def render_reports_analytics():
    """Generate reports and analytics"""
    
    st.subheader("📊 Reports & Analytics")
    
    departments = load_db(DEPARTMENTS_DB)
    programs = load_db(PROGRAMS_DB)
    classes = load_db(CLASSES_DB)
    enrollments = load_db(ENROLLMENTS_DB)
    exams = load_db(EXAMS_DB)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Departments", len(departments))
    
    with col2:
        st.metric("Programs", len(programs))
    
    with col3:
        st.metric("Active Classes", len([c for c in classes.values() if c['status'] == 'active']))
    
    with col4:
        st.metric("Total Enrollments", len(enrollments))
    
    st.markdown("---")
    
    st.info("📊 Detailed reports and analytics - Coming soon!")
