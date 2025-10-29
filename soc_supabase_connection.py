"""
SOC TRAINING PLATFORM - SUPABASE CONNECTION
Connect to the SOC training database tables
"""

import streamlit as st
from supabase import create_client, Client
from datetime import datetime

def get_soc_supabase_client():
    """Get Supabase client for SOC training tables"""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# ============================================
# STUDENT FUNCTIONS
# ============================================

def get_or_create_student(email, name=None):
    """Get existing student or create new one"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return None
    
    try:
        # Check if student exists
        result = supabase.table('soc_students').select('*').eq('email', email).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            # Create new student
            new_student = {
                'email': email,
                'name': name or email.split('@')[0],
                'total_points': 0,
                'level': 'Beginner',
                'active': True
            }
            result = supabase.table('soc_students').insert(new_student).execute()
            return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error getting/creating student: {e}")
        return None

def get_student_progress(student_id):
    """Get student's complete progress"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return {}
    
    try:
        # Get enrollments
        enrollments = supabase.table('soc_enrollments').select('*, soc_courses(*)').eq('student_id', student_id).execute()
        
        # Get lab attempts
        labs = supabase.table('soc_lab_attempts').select('*, soc_labs(*)').eq('student_id', student_id).execute()
        
        # Get certifications
        certs = supabase.table('soc_cert_exams').select('*, soc_certifications(*)').eq('student_id', student_id).eq('passed', True).execute()
        
        # Get achievements
        achievements = supabase.table('soc_student_achievements').select('*, soc_achievements(*)').eq('student_id', student_id).execute()
        
        return {
            'enrollments': enrollments.data if enrollments.data else [],
            'labs': labs.data if labs.data else [],
            'certifications': certs.data if certs.data else [],
            'achievements': achievements.data if achievements.data else []
        }
    except Exception as e:
        print(f"Error getting student progress: {e}")
        return {}

# ============================================
# COURSE FUNCTIONS
# ============================================

def get_all_courses():
    """Get all available courses"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return []
    
    try:
        result = supabase.table('soc_courses').select('*').eq('active', True).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting courses: {e}")
        return []

def enroll_student(student_id, course_id):
    """Enroll student in a course"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return False
    
    try:
        enrollment = {
            'student_id': student_id,
            'course_id': course_id,
            'progress_percentage': 0,
            'status': 'active'
        }
        result = supabase.table('soc_enrollments').insert(enrollment).execute()
        return True if result.data else False
    except Exception as e:
        print(f"Error enrolling student: {e}")
        return False

# ============================================
# LAB FUNCTIONS
# ============================================

def get_all_labs(category=None):
    """Get all labs, optionally filtered by category"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return []
    
    try:
        query = supabase.table('soc_labs').select('*').eq('active', True)
        if category:
            query = query.eq('category', category)
        result = query.execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting labs: {e}")
        return []

def start_lab(student_id, lab_id):
    """Start a lab attempt"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return None
    
    try:
        attempt = {
            'student_id': student_id,
            'lab_id': lab_id,
            'completed': False,
            'hints_used': 0
        }
        result = supabase.table('soc_lab_attempts').insert(attempt).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error starting lab: {e}")
        return None

def submit_lab_flag(attempt_id, flag_submitted, correct_flag):
    """Submit lab flag"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return False
    
    try:
        completed = (flag_submitted == correct_flag)
        score = 100 if completed else 0
        
        update_data = {
            'end_time': datetime.now().isoformat(),
            'completed': completed,
            'score': score,
            'flag_submitted': flag_submitted
        }
        
        result = supabase.table('soc_lab_attempts').update(update_data).eq('attempt_id', attempt_id).execute()
        return completed
    except Exception as e:
        print(f"Error submitting flag: {e}")
        return False

# ============================================
# CERTIFICATION FUNCTIONS
# ============================================

def get_all_certifications():
    """Get all certifications"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return []
    
    try:
        result = supabase.table('soc_certifications').select('*').eq('active', True).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting certifications: {e}")
        return []

def record_exam_result(student_id, cert_id, score, passed, time_taken, verification_code):
    """Record certification exam result"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return False
    
    try:
        exam_result = {
            'student_id': student_id,
            'cert_id': cert_id,
            'score': score,
            'passed': passed,
            'time_taken_minutes': time_taken,
            'verification_code': verification_code
        }
        result = supabase.table('soc_cert_exams').insert(exam_result).execute()
        return True if result.data else False
    except Exception as e:
        print(f"Error recording exam: {e}")
        return False

# ============================================
# ACHIEVEMENT FUNCTIONS
# ============================================

def get_all_achievements():
    """Get all achievements"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return []
    
    try:
        result = supabase.table('soc_achievements').select('*').execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting achievements: {e}")
        return []

def award_achievement(student_id, achievement_id):
    """Award achievement to student"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return False
    
    try:
        award = {
            'student_id': student_id,
            'achievement_id': achievement_id
        }
        result = supabase.table('soc_student_achievements').insert(award).execute()
        return True if result.data else False
    except Exception as e:
        print(f"Error awarding achievement: {e}")
        return False

# ============================================
# LEADERBOARD FUNCTIONS
# ============================================

def get_leaderboard(limit=10):
    """Get top students by points"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return []
    
    try:
        result = supabase.table('soc_students').select('name, email, total_points, rank, level').eq('active', True).order('total_points', desc=True).limit(limit).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting leaderboard: {e}")
        return []

# ============================================
# HELPER FUNCTIONS
# ============================================

def update_student_points(student_id, points_to_add):
    """Add points to student's total"""
    supabase = get_soc_supabase_client()
    if not supabase:
        return False
    
    try:
        # Get current points
        result = supabase.table('soc_students').select('total_points').eq('student_id', student_id).execute()
        if result.data:
            current_points = result.data[0]['total_points']
            new_points = current_points + points_to_add
            
            # Update points
            supabase.table('soc_students').update({'total_points': new_points}).eq('student_id', student_id).execute()
            return True
        return False
    except Exception as e:
        print(f"Error updating points: {e}")
        return False
