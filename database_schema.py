"""
T21 UNIFIED PLATFORM - DATABASE SCHEMA
Complete database architecture for all-in-one management system

Modules:
1. User Management (Students, Staff, Admins)
2. LMS (Courses, Lessons, Progress)
3. Staff Management (Scheduling, Tasks, Performance)
4. HR Management (Recruitment, Payroll, Leave)
5. Communications (Messages, Notifications)
6. Analytics & Reporting
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


# ============================================
# DATABASE FILE PATHS
# ============================================

COURSES_DB = "lms_courses.json"
LESSONS_DB = "lms_lessons.json"
STUDENT_PROGRESS_DB = "lms_student_progress.json"
STAFF_DB = "staff_database.json"
STAFF_SCHEDULES_DB = "staff_schedules.json"
STAFF_TASKS_DB = "staff_tasks.json"
STAFF_PERFORMANCE_DB = "staff_performance.json"
HR_RECRUITMENT_DB = "hr_recruitment.json"
HR_LEAVE_DB = "hr_leave.json"
HR_PAYROLL_DB = "hr_payroll.json"
MESSAGES_DB = "messages_database.json"
NOTIFICATIONS_DB = "notifications_database.json"


# ============================================
# UTILITY FUNCTIONS
# ============================================

def load_db(file_path: str) -> Dict:
    """Load database from JSON file"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    return {}


def save_db(file_path: str, data: Dict):
    """Save database to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")


def generate_id(prefix: str = "ID") -> str:
    """Generate unique ID"""
    import hashlib
    import time
    timestamp = str(time.time())
    return f"{prefix}_{hashlib.md5(timestamp.encode()).hexdigest()[:12]}"


# ============================================
# LMS DATABASE SCHEMA
# ============================================

class Course:
    """Course entity for LMS"""
    def __init__(self, course_id: str = None, **kwargs):
        self.course_id = course_id or generate_id("CRS")
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.instructor = kwargs.get('instructor', '')
        self.category = kwargs.get('category', 'General')  # RTT, Admin, Clinical, etc.
        self.level = kwargs.get('level', 'Beginner')  # Beginner, Intermediate, Advanced
        self.duration_hours = kwargs.get('duration_hours', 0)
        self.thumbnail = kwargs.get('thumbnail', '')
        self.price = kwargs.get('price', 0)
        self.required_role = kwargs.get('required_role', 'trial')  # trial, basic, professional, etc.
        self.status = kwargs.get('status', 'draft')  # draft, published, archived
        self.modules = kwargs.get('modules', [])  # List of module IDs
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())
        self.updated_at = kwargs.get('updated_at', datetime.now().isoformat())
        self.total_lessons = kwargs.get('total_lessons', 0)
        self.total_quizzes = kwargs.get('total_quizzes', 0)
        self.certificate_enabled = kwargs.get('certificate_enabled', True)
    
    def to_dict(self) -> Dict:
        return {
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'instructor': self.instructor,
            'category': self.category,
            'level': self.level,
            'duration_hours': self.duration_hours,
            'thumbnail': self.thumbnail,
            'price': self.price,
            'required_role': self.required_role,
            'status': self.status,
            'modules': self.modules,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'total_lessons': self.total_lessons,
            'total_quizzes': self.total_quizzes,
            'certificate_enabled': self.certificate_enabled
        }


class Lesson:
    """Lesson entity for LMS"""
    def __init__(self, lesson_id: str = None, **kwargs):
        self.lesson_id = lesson_id or generate_id("LSN")
        self.course_id = kwargs.get('course_id', '')
        self.module_id = kwargs.get('module_id', '')
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.content_type = kwargs.get('content_type', 'text')  # text, video, pdf, quiz, interactive
        self.content = kwargs.get('content', '')
        self.video_url = kwargs.get('video_url', '')
        self.pdf_url = kwargs.get('pdf_url', '')
        self.duration_minutes = kwargs.get('duration_minutes', 0)
        self.order = kwargs.get('order', 0)
        self.is_free = kwargs.get('is_free', False)
        self.quiz_id = kwargs.get('quiz_id', '')
        self.resources = kwargs.get('resources', [])  # Downloadable files
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'lesson_id': self.lesson_id,
            'course_id': self.course_id,
            'module_id': self.module_id,
            'title': self.title,
            'description': self.description,
            'content_type': self.content_type,
            'content': self.content,
            'video_url': self.video_url,
            'pdf_url': self.pdf_url,
            'duration_minutes': self.duration_minutes,
            'order': self.order,
            'is_free': self.is_free,
            'quiz_id': self.quiz_id,
            'resources': self.resources,
            'created_at': self.created_at
        }


class StudentProgress:
    """Track student progress through courses"""
    def __init__(self, progress_id: str = None, **kwargs):
        self.progress_id = progress_id or generate_id("PRG")
        self.user_email = kwargs.get('user_email', '')
        self.course_id = kwargs.get('course_id', '')
        self.enrolled_at = kwargs.get('enrolled_at', datetime.now().isoformat())
        self.completed_lessons = kwargs.get('completed_lessons', [])  # List of lesson IDs
        self.completed_quizzes = kwargs.get('completed_quizzes', {})  # {quiz_id: score}
        self.last_accessed = kwargs.get('last_accessed', datetime.now().isoformat())
        self.last_lesson = kwargs.get('last_lesson', '')
        self.time_spent_minutes = kwargs.get('time_spent_minutes', 0)
        self.completion_percentage = kwargs.get('completion_percentage', 0)
        self.status = kwargs.get('status', 'in_progress')  # in_progress, completed, paused
        self.certificate_issued = kwargs.get('certificate_issued', False)
        self.certificate_date = kwargs.get('certificate_date', None)
    
    def to_dict(self) -> Dict:
        return {
            'progress_id': self.progress_id,
            'user_email': self.user_email,
            'course_id': self.course_id,
            'enrolled_at': self.enrolled_at,
            'completed_lessons': self.completed_lessons,
            'completed_quizzes': self.completed_quizzes,
            'last_accessed': self.last_accessed,
            'last_lesson': self.last_lesson,
            'time_spent_minutes': self.time_spent_minutes,
            'completion_percentage': self.completion_percentage,
            'status': self.status,
            'certificate_issued': self.certificate_issued,
            'certificate_date': self.certificate_date
        }


# ============================================
# STAFF MANAGEMENT SCHEMA
# ============================================

class StaffMember:
    """Staff member entity"""
    def __init__(self, staff_id: str = None, **kwargs):
        self.staff_id = staff_id or generate_id("STF")
        self.email = kwargs.get('email', '')
        self.full_name = kwargs.get('full_name', '')
        self.job_title = kwargs.get('job_title', '')
        self.department = kwargs.get('department', '')
        self.manager_id = kwargs.get('manager_id', '')
        self.photo_url = kwargs.get('photo_url', '')
        self.phone = kwargs.get('phone', '')
        self.skills = kwargs.get('skills', [])
        self.certifications = kwargs.get('certifications', [])
        self.start_date = kwargs.get('start_date', datetime.now().isoformat())
        self.employment_type = kwargs.get('employment_type', 'full_time')  # full_time, part_time, contract
        self.status = kwargs.get('status', 'active')  # active, on_leave, terminated
    
    def to_dict(self) -> Dict:
        return {
            'staff_id': self.staff_id,
            'email': self.email,
            'full_name': self.full_name,
            'job_title': self.job_title,
            'department': self.department,
            'manager_id': self.manager_id,
            'photo_url': self.photo_url,
            'phone': self.phone,
            'skills': self.skills,
            'certifications': self.certifications,
            'start_date': self.start_date,
            'employment_type': self.employment_type,
            'status': self.status
        }


class Task:
    """Task entity for staff management"""
    def __init__(self, task_id: str = None, **kwargs):
        self.task_id = task_id or generate_id("TSK")
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.assigned_to = kwargs.get('assigned_to', '')  # staff_id
        self.assigned_by = kwargs.get('assigned_by', '')
        self.priority = kwargs.get('priority', 'medium')  # low, medium, high, urgent
        self.status = kwargs.get('status', 'todo')  # todo, in_progress, review, done
        self.due_date = kwargs.get('due_date', '')
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())
        self.completed_at = kwargs.get('completed_at', None)
        self.tags = kwargs.get('tags', [])
    
    def to_dict(self) -> Dict:
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'assigned_to': self.assigned_to,
            'assigned_by': self.assigned_by,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'tags': self.tags
        }


# ============================================
# HR MANAGEMENT SCHEMA
# ============================================

class LeaveRequest:
    """Leave request entity"""
    def __init__(self, request_id: str = None, **kwargs):
        self.request_id = request_id or generate_id("LVE")
        self.staff_id = kwargs.get('staff_id', '')
        self.leave_type = kwargs.get('leave_type', 'annual')  # annual, sick, unpaid, maternity, etc.
        self.start_date = kwargs.get('start_date', '')
        self.end_date = kwargs.get('end_date', '')
        self.days_count = kwargs.get('days_count', 0)
        self.reason = kwargs.get('reason', '')
        self.status = kwargs.get('status', 'pending')  # pending, approved, rejected
        self.approved_by = kwargs.get('approved_by', '')
        self.submitted_at = kwargs.get('submitted_at', datetime.now().isoformat())
        self.reviewed_at = kwargs.get('reviewed_at', None)
    
    def to_dict(self) -> Dict:
        return {
            'request_id': self.request_id,
            'staff_id': self.staff_id,
            'leave_type': self.leave_type,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'days_count': self.days_count,
            'reason': self.reason,
            'status': self.status,
            'approved_by': self.approved_by,
            'submitted_at': self.submitted_at,
            'reviewed_at': self.reviewed_at
        }


# ============================================
# INITIALIZATION
# ============================================

def initialize_databases():
    """Initialize all database files if they don't exist"""
    databases = [
        COURSES_DB, LESSONS_DB, STUDENT_PROGRESS_DB,
        STAFF_DB, STAFF_SCHEDULES_DB, STAFF_TASKS_DB,
        STAFF_PERFORMANCE_DB, HR_RECRUITMENT_DB,
        HR_LEAVE_DB, HR_PAYROLL_DB,
        MESSAGES_DB, NOTIFICATIONS_DB
    ]
    
    for db in databases:
        if not os.path.exists(db):
            save_db(db, {})
