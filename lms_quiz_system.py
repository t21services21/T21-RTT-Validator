"""
T21 LMS - QUIZ SYSTEM
Create and manage quizzes for courses with auto-grading

Features:
- Create quizzes with multiple question types
- Automatic grading
- Immediate feedback
- Quiz attempts tracking
- Score history
- Pass/fail thresholds
"""

import json
import os
from datetime import datetime
from database_schema import generate_id, load_db, save_db


QUIZZES_DB = "lms_quizzes.json"
QUIZ_ATTEMPTS_DB = "lms_quiz_attempts.json"


# ============================================
# QUIZ MANAGEMENT
# ============================================

def create_quiz(course_id, title, description, time_limit_minutes=30, passing_score=70, max_attempts=3):
    """Create a new quiz"""
    quizzes = load_db(QUIZZES_DB)
    
    quiz_id = generate_id("QZ")
    
    quiz = {
        'quiz_id': quiz_id,
        'course_id': course_id,
        'title': title,
        'description': description,
        'time_limit_minutes': time_limit_minutes,
        'passing_score': passing_score,
        'max_attempts': max_attempts,
        'questions': [],
        'created_at': datetime.now().isoformat()
    }
    
    quizzes[quiz_id] = quiz
    save_db(QUIZZES_DB, quizzes)
    
    return quiz_id


def add_question_to_quiz(quiz_id, question_text, question_type, options, correct_answer, explanation, points=1):
    """Add a question to a quiz"""
    quizzes = load_db(QUIZZES_DB)
    
    if quiz_id not in quizzes:
        return False
    
    question = {
        'question_id': generate_id("Q"),
        'question_text': question_text,
        'type': question_type,  # multiple_choice, true_false, fill_blank
        'options': options,
        'correct_answer': correct_answer,
        'explanation': explanation,
        'points': points
    }
    
    quizzes[quiz_id]['questions'].append(question)
    save_db(QUIZZES_DB, quizzes)
    
    return True


def get_quiz(quiz_id):
    """Get quiz by ID"""
    quizzes = load_db(QUIZZES_DB)
    return quizzes.get(quiz_id)


def get_quizzes_for_course(course_id):
    """Get all quizzes for a course"""
    quizzes = load_db(QUIZZES_DB)
    
    course_quizzes = []
    for quiz_id, quiz in quizzes.items():
        if quiz['course_id'] == course_id:
            course_quizzes.append(quiz)
    
    return course_quizzes


# ============================================
# QUIZ ATTEMPTS & GRADING
# ============================================

def submit_quiz_attempt(user_email, quiz_id, answers):
    """Submit and grade a quiz attempt"""
    quiz = get_quiz(quiz_id)
    
    if not quiz:
        return None
    
    # Grade the quiz
    total_points = 0
    earned_points = 0
    results = []
    
    for question in quiz['questions']:
        question_id = question['question_id']
        correct_answer = question['correct_answer']
        user_answer = answers.get(question_id, '')
        
        is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        
        total_points += question['points']
        if is_correct:
            earned_points += question['points']
        
        results.append({
            'question_id': question_id,
            'question_text': question['question_text'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'explanation': question.get('explanation', '')
        })
    
    # Calculate score percentage
    score = int((earned_points / total_points * 100)) if total_points > 0 else 0
    passed = score >= quiz['passing_score']
    
    # Save attempt
    attempts = load_db(QUIZ_ATTEMPTS_DB)
    
    attempt_id = generate_id("ATT")
    
    attempt = {
        'attempt_id': attempt_id,
        'user_email': user_email,
        'quiz_id': quiz_id,
        'score': score,
        'earned_points': earned_points,
        'total_points': total_points,
        'passed': passed,
        'answers': answers,
        'results': results,
        'completed_at': datetime.now().isoformat()
    }
    
    if attempt_id not in attempts:
        attempts[attempt_id] = attempt
        save_db(QUIZ_ATTEMPTS_DB, attempts)
    
    return attempt


def get_user_quiz_attempts(user_email, quiz_id):
    """Get all attempts for a user on a specific quiz"""
    attempts = load_db(QUIZ_ATTEMPTS_DB)
    
    user_attempts = []
    for attempt_id, attempt in attempts.items():
        if attempt['user_email'] == user_email and attempt['quiz_id'] == quiz_id:
            user_attempts.append(attempt)
    
    # Sort by date (newest first)
    user_attempts.sort(key=lambda x: x['completed_at'], reverse=True)
    
    return user_attempts


def get_best_quiz_score(user_email, quiz_id):
    """Get user's best score for a quiz"""
    attempts = get_user_quiz_attempts(user_email, quiz_id)
    
    if not attempts:
        return None
    
    best_attempt = max(attempts, key=lambda x: x['score'])
    return best_attempt['score']


def can_retake_quiz(user_email, quiz_id):
    """Check if user can retake a quiz"""
    quiz = get_quiz(quiz_id)
    
    if not quiz:
        return False
    
    attempts = get_user_quiz_attempts(user_email, quiz_id)
    
    max_attempts = quiz.get('max_attempts', 3)
    
    if max_attempts == 0:  # Unlimited attempts
        return True
    
    return len(attempts) < max_attempts


# ============================================
# SAMPLE QUIZZES
# ============================================

def create_sample_rtt_quiz(course_id):
    """Create a sample RTT quiz"""
    
    quiz_id = create_quiz(
        course_id=course_id,
        title="RTT Pathway Fundamentals Quiz",
        description="Test your knowledge of RTT pathway basics",
        time_limit_minutes=20,
        passing_score=70,
        max_attempts=3
    )
    
    # Question 1
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="What does RTT stand for?",
        question_type="multiple_choice",
        options=["Referral To Treatment", "Return To Therapy", "Rapid Treatment Time", "Regional Treatment Trust"],
        correct_answer="Referral To Treatment",
        explanation="RTT stands for Referral To Treatment - it's the pathway from when a patient is referred until they receive treatment.",
        points=1
    )
    
    # Question 2
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="What is the maximum waiting time for non-urgent RTT pathways?",
        question_type="multiple_choice",
        options=["12 weeks", "18 weeks", "26 weeks", "52 weeks"],
        correct_answer="18 weeks",
        explanation="The RTT standard is that 92% of patients should wait no longer than 18 weeks from referral to treatment.",
        points=1
    )
    
    # Question 3
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="Does a DNA (Did Not Attend) stop the RTT clock?",
        question_type="true_false",
        options=["True", "False"],
        correct_answer="False",
        explanation="DNA does NOT stop the RTT clock. The clock continues to run until the patient receives treatment or is discharged.",
        points=1
    )
    
    # Question 4
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="What event STARTS the RTT clock?",
        question_type="multiple_choice",
        options=[
            "When patient calls to book appointment",
            "When referral is received",
            "When first appointment happens",
            "When treatment is given"
        ],
        correct_answer="When referral is received",
        explanation="The RTT clock starts when a referral for consultant-led care is received, or when a decision to treat is made.",
        points=1
    )
    
    # Question 5
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="What STOPS the RTT clock?",
        question_type="multiple_choice",
        options=[
            "First outpatient appointment",
            "Diagnostic test",
            "Start of treatment",
            "Patient discharge"
        ],
        correct_answer="Start of treatment",
        explanation="The RTT clock stops when treatment starts, or when the patient is discharged from the pathway.",
        points=1
    )
    
    return quiz_id


def create_sample_admin_quiz(course_id):
    """Create a sample Hospital Admin quiz"""
    
    quiz_id = create_quiz(
        course_id=course_id,
        title="Hospital Administration Basics",
        description="Test your knowledge of hospital administration",
        time_limit_minutes=15,
        passing_score=70,
        max_attempts=3
    )
    
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="What is the primary role of hospital administration?",
        question_type="multiple_choice",
        options=[
            "Direct patient care",
            "Managing hospital operations and resources",
            "Performing surgeries",
            "Conducting research"
        ],
        correct_answer="Managing hospital operations and resources",
        explanation="Hospital administration focuses on managing operations, resources, staff, and ensuring efficient healthcare delivery.",
        points=1
    )
    
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="GDPR applies to patient data in healthcare settings?",
        question_type="true_false",
        options=["True", "False"],
        correct_answer="True",
        explanation="GDPR (General Data Protection Regulation) strictly applies to all patient data and must be followed in healthcare.",
        points=1
    )
    
    add_question_to_quiz(
        quiz_id=quiz_id,
        question_text="What does CQC stand for?",
        question_type="multiple_choice",
        options=[
            "Care Quality Commission",
            "Clinical Quality Control",
            "Central Quality Centre",
            "Clinical Quality Commission"
        ],
        correct_answer="Care Quality Commission",
        explanation="The CQC (Care Quality Commission) is the independent regulator of health and social care in England.",
        points=1
    )
    
    return quiz_id
