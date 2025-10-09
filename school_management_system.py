"""
T21 SERVICES - COMPLETE SCHOOL MANAGEMENT SYSTEM
Comprehensive training institution management platform

Features:
- Multi-department course management
- Student enrollment & records
- Staff/Instructor management
- Exam & assessment system
- Grade management & transcripts
- Attendance tracking
- Class/batch management
- Academic calendar
- Materials & resources
- Report cards & certificates
- Parent/Guardian portal
- Fee management
- Timetable scheduling
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database_schema import generate_id, load_db, save_db


# ============================================
# DATABASE FILES
# ============================================

DEPARTMENTS_DB = "school_departments.json"
PROGRAMS_DB = "school_programs.json"
CLASSES_DB = "school_classes.json"
ENROLLMENTS_DB = "school_enrollments.json"
EXAMS_DB = "school_exams.json"
GRADES_DB = "school_grades.json"
ATTENDANCE_DB = "school_attendance.json"
MATERIALS_DB = "school_materials.json"
TIMETABLE_DB = "school_timetable.json"
ANNOUNCEMENTS_DB = "school_announcements.json"
STUDENT_RECORDS_DB = "school_student_records.json"


# ============================================
# DEPARTMENTS & PROGRAMS
# ============================================

def create_department(name, description, head_of_department, email, phone):
    """Create a training department"""
    departments = load_db(DEPARTMENTS_DB)
    
    dept_id = generate_id("DEPT")
    
    department = {
        'department_id': dept_id,
        'name': name,
        'description': description,
        'head_of_department': head_of_department,
        'email': email,
        'phone': phone,
        'programs': [],
        'staff_count': 0,
        'student_count': 0,
        'created_at': datetime.now().isoformat()
    }
    
    departments[dept_id] = department
    save_db(DEPARTMENTS_DB, departments)
    
    return dept_id


def create_program(department_id, name, description, duration_months, level, qualification, prerequisites):
    """Create a training program"""
    programs = load_db(PROGRAMS_DB)
    
    program_id = generate_id("PROG")
    
    program = {
        'program_id': program_id,
        'department_id': department_id,
        'name': name,
        'description': description,
        'duration_months': duration_months,
        'level': level,  # Certificate, Diploma, Degree, Masters, etc.
        'qualification': qualification,
        'prerequisites': prerequisites,
        'courses': [],
        'total_credits': 0,
        'status': 'active',
        'created_at': datetime.now().isoformat()
    }
    
    programs[program_id] = program
    save_db(PROGRAMS_DB, programs)
    
    return program_id


# ============================================
# CLASS/BATCH MANAGEMENT
# ============================================

def create_class(program_id, name, semester, academic_year, instructor_email, max_students, schedule):
    """Create a class/batch"""
    classes = load_db(CLASSES_DB)
    
    class_id = generate_id("CLS")
    
    class_data = {
        'class_id': class_id,
        'program_id': program_id,
        'name': name,
        'semester': semester,
        'academic_year': academic_year,
        'instructor_email': instructor_email,
        'max_students': max_students,
        'enrolled_students': [],
        'schedule': schedule,  # {"Monday": "09:00-11:00", ...}
        'room': '',
        'status': 'active',
        'start_date': datetime.now().isoformat(),
        'end_date': None
    }
    
    classes[class_id] = class_data
    save_db(CLASSES_DB, classes)
    
    return class_id


def enroll_student_in_class(student_email, class_id):
    """Enroll student in a class"""
    classes = load_db(CLASSES_DB)
    enrollments = load_db(ENROLLMENTS_DB)
    
    if class_id not in classes:
        return False, "Class not found"
    
    class_data = classes[class_id]
    
    # Check if full
    if len(class_data['enrolled_students']) >= class_data['max_students']:
        return False, "Class is full"
    
    # Check if already enrolled
    if student_email in class_data['enrolled_students']:
        return False, "Already enrolled"
    
    # Add to class
    class_data['enrolled_students'].append(student_email)
    save_db(CLASSES_DB, classes)
    
    # Create enrollment record
    enrollment_id = generate_id("ENR")
    
    enrollment = {
        'enrollment_id': enrollment_id,
        'student_email': student_email,
        'class_id': class_id,
        'enrollment_date': datetime.now().isoformat(),
        'status': 'active',  # active, dropped, completed
        'attendance_percentage': 0,
        'grade': None,
        'credits_earned': 0
    }
    
    enrollments[enrollment_id] = enrollment
    save_db(ENROLLMENTS_DB, enrollments)
    
    return True, "Enrolled successfully"


# ============================================
# EXAM & ASSESSMENT SYSTEM
# ============================================

def create_exam(class_id, name, exam_type, total_marks, passing_marks, exam_date, duration_minutes):
    """Create an exam/assessment"""
    exams = load_db(EXAMS_DB)
    
    exam_id = generate_id("EXM")
    
    exam = {
        'exam_id': exam_id,
        'class_id': class_id,
        'name': name,
        'exam_type': exam_type,  # quiz, midterm, final, assignment, practical
        'total_marks': total_marks,
        'passing_marks': passing_marks,
        'exam_date': exam_date,
        'duration_minutes': duration_minutes,
        'weightage': 0,  # Percentage contribution to final grade
        'instructions': '',
        'questions': [],
        'created_at': datetime.now().isoformat()
    }
    
    exams[exam_id] = exam
    save_db(EXAMS_DB, exams)
    
    return exam_id


def record_grade(student_email, exam_id, marks_obtained, feedback=''):
    """Record student grade for an exam"""
    grades = load_db(GRADES_DB)
    
    grade_id = generate_id("GRD")
    
    grade = {
        'grade_id': grade_id,
        'student_email': student_email,
        'exam_id': exam_id,
        'marks_obtained': marks_obtained,
        'feedback': feedback,
        'graded_by': '',
        'graded_at': datetime.now().isoformat()
    }
    
    grades[grade_id] = grade
    save_db(GRADES_DB, grades)
    
    return grade_id


def calculate_final_grade(student_email, class_id):
    """Calculate final grade for a student in a class"""
    exams = load_db(EXAMS_DB)
    grades = load_db(GRADES_DB)
    
    # Get all exams for this class
    class_exams = {eid: e for eid, e in exams.items() if e['class_id'] == class_id}
    
    # Get student's grades
    student_grades = {gid: g for gid, g in grades.items() if g['student_email'] == student_email}
    
    # Calculate weighted average
    total_weighted_score = 0
    total_weightage = 0
    
    for exam_id, exam in class_exams.items():
        weightage = exam.get('weightage', 0)
        
        # Find student's grade for this exam
        for grade_id, grade in student_grades.items():
            if grade['exam_id'] == exam_id:
                percentage = (grade['marks_obtained'] / exam['total_marks']) * 100
                total_weighted_score += percentage * (weightage / 100)
                total_weightage += weightage
                break
    
    if total_weightage == 0:
        return 0, 'F'
    
    final_percentage = total_weighted_score
    
    # Grade conversion
    if final_percentage >= 90:
        letter_grade = 'A+'
    elif final_percentage >= 85:
        letter_grade = 'A'
    elif final_percentage >= 80:
        letter_grade = 'A-'
    elif final_percentage >= 75:
        letter_grade = 'B+'
    elif final_percentage >= 70:
        letter_grade = 'B'
    elif final_percentage >= 65:
        letter_grade = 'B-'
    elif final_percentage >= 60:
        letter_grade = 'C+'
    elif final_percentage >= 55:
        letter_grade = 'C'
    elif final_percentage >= 50:
        letter_grade = 'D'
    else:
        letter_grade = 'F'
    
    return final_percentage, letter_grade


# ============================================
# ATTENDANCE SYSTEM
# ============================================

def mark_attendance(class_id, date, student_email, status, remarks=''):
    """Mark student attendance"""
    attendance = load_db(ATTENDANCE_DB)
    
    attendance_id = generate_id("ATT")
    
    record = {
        'attendance_id': attendance_id,
        'class_id': class_id,
        'date': date,
        'student_email': student_email,
        'status': status,  # present, absent, late, excused
        'remarks': remarks,
        'marked_by': '',
        'marked_at': datetime.now().isoformat()
    }
    
    attendance[attendance_id] = record
    save_db(ATTENDANCE_DB, attendance)
    
    return attendance_id


def calculate_attendance_percentage(student_email, class_id):
    """Calculate attendance percentage"""
    attendance = load_db(ATTENDANCE_DB)
    
    # Get all attendance records for this student in this class
    records = [a for a in attendance.values() 
               if a['student_email'] == student_email and a['class_id'] == class_id]
    
    if not records:
        return 0
    
    present_count = len([r for r in records if r['status'] in ['present', 'late']])
    total_count = len(records)
    
    return int((present_count / total_count) * 100)


# ============================================
# MATERIALS & RESOURCES
# ============================================

def upload_material(class_id, title, description, file_type, file_url, uploaded_by):
    """Upload learning material"""
    materials = load_db(MATERIALS_DB)
    
    material_id = generate_id("MAT")
    
    material = {
        'material_id': material_id,
        'class_id': class_id,
        'title': title,
        'description': description,
        'file_type': file_type,  # pdf, video, document, presentation, etc.
        'file_url': file_url,
        'file_size': 0,
        'uploaded_by': uploaded_by,
        'uploaded_at': datetime.now().isoformat(),
        'downloads': 0
    }
    
    materials[material_id] = material
    save_db(MATERIALS_DB, materials)
    
    return material_id


# ============================================
# ACADEMIC CALENDAR
# ============================================

def create_event(title, description, event_type, start_date, end_date, applies_to):
    """Create academic calendar event"""
    announcements = load_db(ANNOUNCEMENTS_DB)
    
    event_id = generate_id("EVT")
    
    event = {
        'event_id': event_id,
        'title': title,
        'description': description,
        'event_type': event_type,  # holiday, exam, registration, orientation, etc.
        'start_date': start_date,
        'end_date': end_date,
        'applies_to': applies_to,  # all, specific department, specific program
        'created_at': datetime.now().isoformat()
    }
    
    announcements[event_id] = event
    save_db(ANNOUNCEMENTS_DB, announcements)
    
    return event_id


# ============================================
# STUDENT RECORDS & TRANSCRIPTS
# ============================================

def create_student_record(student_email, student_name, student_id, program_id, admission_date):
    """Create comprehensive student record"""
    records = load_db(STUDENT_RECORDS_DB)
    
    record_id = generate_id("REC")
    
    record = {
        'record_id': record_id,
        'student_email': student_email,
        'student_name': student_name,
        'student_id': student_id,
        'program_id': program_id,
        'admission_date': admission_date,
        'status': 'active',  # active, graduated, dropped, suspended
        'gpa': 0.0,
        'total_credits': 0,
        'enrollments': [],
        'grades': {},
        'attendance_overall': 0,
        'achievements': [],
        'disciplinary_records': [],
        'graduation_date': None
    }
    
    records[record_id] = record
    save_db(STUDENT_RECORDS_DB, records)
    
    return record_id


def generate_transcript(student_email):
    """Generate official academic transcript"""
    records = load_db(STUDENT_RECORDS_DB)
    grades = load_db(GRADES_DB)
    classes = load_db(CLASSES_DB)
    exams = load_db(EXAMS_DB)
    
    # Find student record
    student_record = None
    for rec in records.values():
        if rec['student_email'] == student_email:
            student_record = rec
            break
    
    if not student_record:
        return None
    
    # Compile transcript
    transcript = {
        'student_name': student_record['student_name'],
        'student_id': student_record['student_id'],
        'program': student_record['program_id'],
        'admission_date': student_record['admission_date'],
        'gpa': student_record['gpa'],
        'total_credits': student_record['total_credits'],
        'courses': [],
        'generated_at': datetime.now().isoformat()
    }
    
    # Get all courses and grades
    for enrollment_id in student_record['enrollments']:
        # Get class details
        # Calculate final grade
        # Add to transcript
        pass
    
    return transcript
