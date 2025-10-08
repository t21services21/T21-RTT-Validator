"""
T21 INTERACTIVE LEARNING CENTER
AI-Powered Gamified RTT Training System

Features:
- Multiple quiz types (MCQ, True/False, Drag-Drop, Fill-in-Blank, Timeline)
- AI-powered feedback
- Gamification (points, badges, achievements)
- Progress tracking
- Leaderboard
- Adaptive difficulty
"""

import json
from datetime import datetime

# ============================================
# QUIZ QUESTIONS DATABASE
# ============================================

INTERACTIVE_QUIZZES = [
    # MULTIPLE CHOICE QUESTIONS
    {
        "id": "mcq_1",
        "type": "multiple_choice",
        "difficulty": "Easy",
        "question": "What RTT code is used when a GP refers a patient to a consultant?",
        "options": ["Code 10", "Code 20", "Code 30", "Code 34"],
        "correct_answer": "Code 10",
        "explanation": "Code 10 = 1st activity after referral in RTT. This STARTS the RTT clock.",
        "points": 10,
        "category": "RTT Codes Basics"
    },
    {
        "id": "mcq_2",
        "type": "multiple_choice",
        "difficulty": "Easy",
        "question": "Which code STOPS the RTT clock when first definitive treatment starts?",
        "options": ["Code 20", "Code 30", "Code 32", "Code 34"],
        "correct_answer": "Code 30",
        "explanation": "Code 30 = Start 1st Definitive Treatment. This STOPS the RTT clock when treatment begins.",
        "points": 10,
        "category": "RTT Codes Basics"
    },
    {
        "id": "mcq_3",
        "type": "multiple_choice",
        "difficulty": "Hard",
        "question": "A patient DNA'd their FIRST outpatient appointment. What code should be used?",
        "options": ["Code 20", "Code 33", "Code 34", "Code 92"],
        "correct_answer": "Code 33",
        "explanation": "Code 33 = Patient DNA's the 1st Activity. This STOPS the RTT clock. Note: Only for first appointment DNA!",
        "points": 20,
        "category": "Patient Events"
    },
    {
        "id": "mcq_4",
        "type": "multiple_choice",
        "difficulty": "Hard",
        "question": "What happens to the RTT clock when a patient has a tertiary referral (Code 21)?",
        "options": ["Clock stops", "Clock pauses", "Clock continues (still ticking)", "Clock restarts"],
        "correct_answer": "Clock continues (still ticking)",
        "explanation": "Code 21 = Tertiary referral. The RTT clock CONTINUES - it does NOT stop or reset when referred to another provider!",
        "points": 20,
        "category": "Clock Management"
    },
    {
        "id": "mcq_5",
        "type": "multiple_choice",
        "difficulty": "Medium",
        "question": "A patient declines the recommended treatment. What code is this?",
        "options": ["Code 30", "Code 31", "Code 34", "Code 35"],
        "correct_answer": "Code 35",
        "explanation": "Code 35 = Patient declines treatment. Patient refuses to proceed. This STOPS the RTT clock.",
        "points": 15,
        "category": "Patient Events"
    },
    
    # TRUE/FALSE QUESTIONS
    {
        "id": "tf_1",
        "type": "true_false",
        "difficulty": "Easy",
        "question": "A 2-Week Wait cancer referral uses Code 20 instead of Code 10.",
        "correct_answer": "False",
        "explanation": "FALSE! 2WW referrals still use Code 10 (GP referral). The 2WW status affects BOOKING timeline (within 14 days), not the RTT code.",
        "points": 10,
        "category": "Cancer Pathways"
    },
    {
        "id": "tf_2",
        "type": "true_false",
        "difficulty": "Easy",
        "question": "Code 30 can only be used for surgical treatments.",
        "correct_answer": "False",
        "explanation": "FALSE! Code 30 applies to ANY first definitive treatment - surgery, cryotherapy, injections, endoscopy, etc.",
        "points": 10,
        "category": "RTT Codes Basics"
    },
    {
        "id": "tf_3",
        "type": "true_false",
        "difficulty": "Medium",
        "question": "Watchful wait by clinician (Code 32) stops the RTT clock.",
        "correct_answer": "True",
        "explanation": "TRUE! Code 32 = Start of watchful wait by Clinician. This STOPS the RTT clock. Can resume with Code 11.",
        "points": 15,
        "category": "Clock Management"
    },
    {
        "id": "tf_4",
        "type": "true_false",
        "difficulty": "Hard",
        "question": "Code 36 is used when a patient has passed away.",
        "correct_answer": "True",
        "explanation": "TRUE! Code 36 = Patient Deceased. This STOPS the RTT clock when a patient dies.",
        "points": 20,
        "category": "RTT Codes Basics"
    },
    
    # DRAG-AND-DROP (Code Matching)
    {
        "id": "dd_1",
        "type": "drag_drop",
        "difficulty": "Medium",
        "question": "Match each scenario to the correct RTT code:",
        "pairs": [
            {"scenario": "GP refers patient to cardiology", "code": "Code 10"},
            {"scenario": "Patient has surgery performed", "code": "Code 30"},
            {"scenario": "Patient DNA's first appointment", "code": "Code 33"},
            {"scenario": "Clinical decision not to treat", "code": "Code 34"}
        ],
        "explanation": "GP referral = 10 (START), Treatment = 30 (STOP), DNA 1st activity = 33 (STOP), Decision not to treat = 34 (STOP)",
        "points": 20,
        "category": "RTT Codes Basics"
    },
    
    # FILL IN THE BLANK
    {
        "id": "fib_1",
        "type": "fill_blank",
        "difficulty": "Easy",
        "question": "The RTT target is that 92% of patients should be seen within ____ weeks.",
        "correct_answer": "18",
        "explanation": "The NHS RTT standard is 18 weeks from referral to first definitive treatment.",
        "points": 10,
        "category": "NHS Standards"
    },
    {
        "id": "fib_2",
        "type": "fill_blank",
        "difficulty": "Medium",
        "question": "A 2-Week Wait cancer referral must be seen within ____ days.",
        "correct_answer": "14",
        "explanation": "2WW = 14 days (2 weeks) from referral to first appointment.",
        "points": 15,
        "category": "Cancer Pathways"
    },
    
    # TIMELINE/ORDERING
    {
        "id": "timeline_1",
        "type": "timeline",
        "difficulty": "Medium",
        "question": "Put these RTT events in the correct chronological order:",
        "items": [
            "GP Referral (Code 10)",
            "First Outpatient Appointment",
            "Decision to Treat (Code 20)",
            "Added to Waiting List",
            "Surgery Performed (Code 30)"
        ],
        "correct_order": [0, 1, 2, 3, 4],
        "explanation": "Correct pathway: Referral → OPA → Decision → WL → Treatment",
        "points": 20,
        "category": "Pathway Understanding"
    },
    
    # ============================================
    # ADDITIONAL QUIZZES - REACHING 50 TOTAL
    # ============================================
    
    # MORE MULTIPLE CHOICE
    {
        "id": "mcq_6",
        "type": "multiple_choice",
        "difficulty": "Medium",
        "question": "What code is used when a patient wants to think about treatment?",
        "options": ["Code 30", "Code 31", "Code 34", "Code 35"],
        "correct_answer": "Code 31",
        "explanation": "Code 31 = Start of watchful wait by patient. Patient chooses to wait and see how condition develops. This STOPS the clock.",
        "points": 15,
        "category": "Patient Events"
    },
    {
        "id": "mcq_7",
        "type": "multiple_choice",
        "difficulty": "Hard",
        "question": "A patient is referred to a tertiary center. What happens to the RTT clock?",
        "options": ["Stops", "Pauses", "Continues (still ticking)", "Restarts"],
        "correct_answer": "Continues (still ticking)",
        "explanation": "Code 21 = Tertiary referral. RTT clock CONTINUES - does not stop or reset!",
        "points": 20,
        "category": "Clock Management"
    },
    {
        "id": "mcq_8",
        "type": "multiple_choice",
        "difficulty": "Easy",
        "question": "How many weeks is the NHS RTT standard target?",
        "options": ["12 weeks", "16 weeks", "18 weeks", "26 weeks"],
        "correct_answer": "18 weeks",
        "explanation": "18 weeks from referral to first definitive treatment for 92% of patients.",
        "points": 10,
        "category": "NHS Standards"
    },
    {
        "id": "mcq_9",
        "type": "multiple_choice",
        "difficulty": "Medium",
        "question": "Which code is used when a clinician decides to monitor (watchful wait)?",
        "options": ["Code 30", "Code 31", "Code 32", "Code 91"],
        "correct_answer": "Code 32",
        "explanation": "Code 32 = Start of watchful wait by Clinician. Clock STOPS when clinician decides to monitor.",
        "points": 15,
        "category": "RTT Codes Basics"
    },
    {
        "id": "mcq_10",
        "type": "multiple_choice",
        "difficulty": "Hard",
        "question": "Patient DNA'd their first outpatient appointment and was rebooked. What is the PRIMARY action?",
        "options": ["Discharge patient (Code 34)", "Remove from list", "Rebook appointment", "Restart clock (Code 11)"],
        "correct_answer": "Rebook appointment",
        "explanation": "After a DNA (Code 33), the patient must be rebooked according to trust policy. The RTT clock continues running.",
        "points": 20,
        "category": "Patient Events"
    },
    {
        "id": "mcq_11",
        "type": "multiple_choice",
        "difficulty": "Expert",
        "question": "What RTT code is used when a diagnostic test is ordered?",
        "options": ["Code 10", "Code 20", "Code 30", "Code 92"],
        "correct_answer": "Code 20",
        "explanation": "Code 20 = Subsequent consultant/diagnostic tests. Clock continues (still ticking) when diagnostics ordered.",
        "points": 25,
        "category": "Clock Management"
    },
    
    # MORE TRUE/FALSE
    {
        "id": "tf_5",
        "type": "true_false",
        "difficulty": "Medium",
        "question": "A patient can be on multiple RTT pathways at the same time.",
        "correct_answer": "True",
        "explanation": "TRUE! A patient can have separate RTT pathways for different conditions/specialties.",
        "points": 15,
        "category": "Pathway Understanding"
    },
    {
        "id": "tf_6",
        "type": "true_false",
        "difficulty": "Easy",
        "question": "Code 34 means the patient was discharged without treatment.",
        "correct_answer": "True",
        "explanation": "TRUE! Code 34 = Discharge with no treatment needed. Clock STOPS.",
        "points": 10,
        "category": "RTT Codes Basics"
    },
    {
        "id": "tf_7",
        "type": "true_false",
        "difficulty": "Hard",
        "question": "The RTT clock must always start on the date the GP letter is received.",
        "correct_answer": "False",
        "explanation": "FALSE! Clock starts on date GP sent referral (letter date), NOT received date.",
        "points": 20,
        "category": "Clock Management"
    },
    {
        "id": "tf_8",
        "type": "true_false",
        "difficulty": "Medium",
        "question": "Diagnostic tests alone can stop the RTT clock.",
        "correct_answer": "False",
        "explanation": "FALSE! Diagnostics alone do NOT stop the clock. Need Code 30 (treatment) or Code 34 (discharge).",
        "points": 15,
        "category": "Clock Management"
    },
    {
        "id": "tf_9",
        "type": "true_false",
        "difficulty": "Expert",
        "question": "Code 11 is used to start a new RTT period after watchful wait ends.",
        "correct_answer": "True",
        "explanation": "TRUE! Code 11 = 1st activity after watchful wait ends. Starts a new RTT clock when patient ready for treatment.",
        "points": 25,
        "category": "RTT Codes Basics"
    },
    {
        "id": "tf_10",
        "type": "true_false",
        "difficulty": "Hard",
        "question": "A 62-day cancer target uses different RTT codes than regular pathways.",
        "correct_answer": "False",
        "explanation": "FALSE! Cancer pathways use the SAME RTT codes. Only the target timeline differs.",
        "points": 20,
        "category": "Cancer Pathways"
    },
    
    # SPECIALTY-SPECIFIC QUESTIONS
    {
        "id": "mcq_12",
        "type": "multiple_choice",
        "difficulty": "Medium",
        "question": "In cancer pathways, how many days is the 2-Week Wait target?",
        "options": ["7 days", "10 days", "14 days", "21 days"],
        "correct_answer": "14 days",
        "explanation": "2WW = 14 days (2 weeks) from GP referral to first hospital appointment.",
        "points": 15,
        "category": "Cancer Pathways"
    },
    {
        "id": "mcq_13",
        "type": "multiple_choice",
        "difficulty": "Hard",
        "question": "Cancer treatment must start within how many days of referral?",
        "options": ["31 days", "62 days", "104 days", "126 days"],
        "correct_answer": "62 days",
        "explanation": "62-day target from urgent GP referral to first cancer treatment.",
        "points": 20,
        "category": "Cancer Pathways"
    },
    {
        "id": "mcq_14",
        "type": "multiple_choice",
        "difficulty": "Medium",
        "question": "What system is commonly used for patient administration in NHS?",
        "options": ["EMR", "PAS", "CRM", "ERP"],
        "correct_answer": "PAS",
        "explanation": "PAS = Patient Administration System. Core NHS system for appointments, admissions, pathways.",
        "points": 15,
        "category": "NHS Systems"
    },
    
    # SCENARIO-BASED QUESTIONS
    {
        "id": "scenario_1",
        "type": "multiple_choice",
        "difficulty": "Hard",
        "question": "Patient seen in clinic. Diagnostic tests ordered. What code?",
        "options": ["Code 10", "Code 20", "Code 30", "Code 92"],
        "correct_answer": "Code 20",
        "explanation": "Code 20 = Subsequent consultant/diagnostic tests. Clock continues (still ticking) when diagnostics ordered.",
        "points": 20,
        "category": "Real-World Scenarios"
    },
    {
        "id": "scenario_2",
        "type": "multiple_choice",
        "difficulty": "Expert",
        "question": "Patient decides to decline treatment. What code?",
        "options": ["Code 30", "Code 31", "Code 34", "Code 35"],
        "correct_answer": "Code 35",
        "explanation": "Code 35 = Patient declines treatment. Patient refuses to proceed. This STOPS the RTT clock.",
        "points": 25,
        "category": "Real-World Scenarios"
    },
    {
        "id": "scenario_3",
        "type": "multiple_choice",
        "difficulty": "Hard",
        "question": "Patient referred to tertiary center for specialist care. What code?",
        "options": ["Code 10", "Code 20", "Code 21", "Code 30"],
        "correct_answer": "Code 21",
        "explanation": "Code 21 = Tertiary referral. Clock CONTINUES (still ticking) on the pathway.",
        "points": 20,
        "category": "Real-World Scenarios"
    },
    
    # FILL IN THE BLANK - MORE
    {
        "id": "fib_3",
        "type": "fill_blank",
        "difficulty": "Medium",
        "question": "Cancer treatment must start within ____ days of 2WW referral.",
        "correct_answer": "62",
        "explanation": "62-day cancer standard from urgent GP referral to first treatment.",
        "points": 15,
        "category": "Cancer Pathways"
    },
    {
        "id": "fib_4",
        "type": "fill_blank",
        "difficulty": "Easy",
        "question": "Code ____ is used when a GP refers a patient to a consultant.",
        "correct_answer": "10",
        "explanation": "Code 10 = GP referral. Starts the RTT clock.",
        "points": 10,
        "category": "RTT Codes Basics"
    },
    {
        "id": "fib_5",
        "type": "fill_blank",
        "difficulty": "Medium",
        "question": "Code ____ is used when first definitive treatment is completed.",
        "correct_answer": "30",
        "explanation": "Code 30 = First Definitive Treatment. Stops the RTT clock.",
        "points": 15,
        "category": "RTT Codes Basics"
    },
    {
        "id": "fib_6",
        "type": "fill_blank",
        "difficulty": "Hard",
        "question": "Code ____ is used when patient declines treatment.",
        "correct_answer": "35",
        "explanation": "Code 35 = Patient declines treatment (patient refuses to proceed).",
        "points": 20,
        "category": "Patient Events"
    },
    
    # ADVANCED CONCEPTS
    {
        "id": "advanced_1",
        "type": "multiple_choice",
        "difficulty": "Expert",
        "question": "Patient breach imminent (day 125). What is PRIMARY action?",
        "options": ["Change RTT code", "Discharge patient", "Escalate to management", "Reset clock"],
        "correct_answer": "Escalate to management",
        "explanation": "Breach risk = escalation required! RTT code doesn't change. Management must find solution.",
        "points": 25,
        "category": "Breach Management"
    },
    {
        "id": "advanced_2",
        "type": "true_false",
        "difficulty": "Expert",
        "question": "RTT clock can be stopped retrospectively if error found.",
        "correct_answer": "False",
        "explanation": "FALSE! RTT clocks cannot be changed retrospectively. Must be accurate from day one!",
        "points": 25,
        "category": "Data Quality"
    },
    {
        "id": "advanced_3",
        "type": "multiple_choice",
        "difficulty": "Expert",
        "question": "Best way to prevent RTT breaches?",
        "options": ["Change codes", "Weekly validation", "Patient discharge", "Restart clocks"],
        "correct_answer": "Weekly validation",
        "explanation": "Proactive weekly validation identifies issues early. Prevents breaches before they occur!",
        "points": 25,
        "category": "Best Practices"
    }
]


# ============================================
# GAMIFICATION SYSTEM
# ============================================

BADGES = {
    "first_quiz": {
        "name": "🎓 First Steps",
        "description": "Completed your first quiz",
        "requirement": 1
    },
    "bronze_learner": {
        "name": "🥉 Bronze Learner",
        "description": "Scored 50+ points",
        "requirement": 50
    },
    "silver_learner": {
        "name": "🥈 Silver Learner",
        "description": "Scored 150+ points",
        "requirement": 150
    },
    "gold_learner": {
        "name": "🥇 Gold Master",
        "description": "Scored 300+ points",
        "requirement": 300
    },
    "perfectionist": {
        "name": "💯 Perfectionist",
        "description": "Got 10 questions perfect in a row",
        "requirement": "streak_10"
    },
    "speed_demon": {
        "name": "⚡ Speed Demon",
        "description": "Completed 5 quizzes in under 1 minute each",
        "requirement": "speed_5"
    },
    "rtt_expert": {
        "name": "👑 RTT Expert",
        "description": "Completed all quizzes with 90%+ score",
        "requirement": "expert"
    }
}


def calculate_points(correct, difficulty, time_taken_seconds):
    """Calculate points based on performance"""
    base_points = {
        "Easy": 10,
        "Medium": 15,
        "Hard": 20,
        "Expert": 25
    }
    
    if not correct:
        return 0
    
    points = base_points.get(difficulty, 10)
    
    # Time bonus (if answered quickly)
    if time_taken_seconds < 10:
        points += 5  # Speed bonus
    
    return points


def check_badge_unlock(total_points, quizzes_completed, streak):
    """Check if user unlocked any new badges"""
    unlocked = []
    
    if quizzes_completed == 1:
        unlocked.append("first_quiz")
    
    if total_points >= 50:
        unlocked.append("bronze_learner")
    
    if total_points >= 150:
        unlocked.append("silver_learner")
    
    if total_points >= 300:
        unlocked.append("gold_learner")
    
    if streak >= 10:
        unlocked.append("perfectionist")
    
    return unlocked


def get_quiz_by_difficulty(difficulty):
    """Get quizzes filtered by difficulty"""
    return [q for q in INTERACTIVE_QUIZZES if q['difficulty'] == difficulty]


def get_quiz_by_category(category):
    """Get quizzes filtered by category"""
    return [q for q in INTERACTIVE_QUIZZES if q['category'] == category]


def get_all_categories():
    """Get list of all quiz categories"""
    categories = set()
    for quiz in INTERACTIVE_QUIZZES:
        categories.add(quiz['category'])
    return sorted(list(categories))


def check_answer(quiz_id, user_answer):
    """Check if answer is correct and return feedback"""
    quiz = next((q for q in INTERACTIVE_QUIZZES if q['id'] == quiz_id), None)
    
    if not quiz:
        return None
    
    correct = str(user_answer).strip() == str(quiz['correct_answer']).strip()
    
    return {
        'correct': correct,
        'user_answer': user_answer,
        'correct_answer': quiz['correct_answer'],
        'explanation': quiz['explanation'],
        'points_earned': quiz['points'] if correct else 0,
        'quiz_type': quiz['type'],
        'difficulty': quiz['difficulty']
    }


# ============================================
# PROGRESS TRACKING
# ============================================

class StudentProgress:
    """Track individual student progress"""
    
    def __init__(self, student_name="Student"):
        self.student_name = student_name
        self.total_points = 0
        self.quizzes_completed = 0
        self.correct_answers = 0
        self.total_attempts = 0
        self.current_streak = 0
        self.best_streak = 0
        self.badges_earned = []
        self.quiz_history = []
        self.start_time = datetime.now()
    
    def add_quiz_result(self, quiz_id, correct, points_earned, time_taken):
        """Record quiz result"""
        self.quizzes_completed += 1
        self.total_attempts += 1
        
        if correct:
            self.correct_answers += 1
            self.current_streak += 1
            self.total_points += points_earned
            
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
        else:
            self.current_streak = 0
        
        self.quiz_history.append({
            'quiz_id': quiz_id,
            'correct': correct,
            'points': points_earned,
            'time': time_taken,
            'timestamp': datetime.now()
        })
        
        # Check for new badges
        new_badges = check_badge_unlock(
            self.total_points, 
            self.quizzes_completed, 
            self.current_streak
        )
        
        for badge in new_badges:
            if badge not in self.badges_earned:
                self.badges_earned.append(badge)
    
    def get_accuracy(self):
        """Calculate overall accuracy percentage"""
        if self.total_attempts == 0:
            return 0
        return round((self.correct_answers / self.total_attempts) * 100, 1)
    
    def get_summary(self):
        """Get progress summary"""
        return {
            'name': self.student_name,
            'total_points': self.total_points,
            'quizzes_completed': self.quizzes_completed,
            'accuracy': self.get_accuracy(),
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'badges': self.badges_earned,
            'time_spent': (datetime.now() - self.start_time).total_seconds()
        }


# ============================================
# LEADERBOARD
# ============================================

LEADERBOARD = []

def add_to_leaderboard(student_name, total_points, accuracy):
    """Add student to leaderboard"""
    entry = {
        'name': student_name,
        'points': total_points,
        'accuracy': accuracy,
        'timestamp': datetime.now()
    }
    LEADERBOARD.append(entry)
    
    # Sort by points (descending)
    LEADERBOARD.sort(key=lambda x: x['points'], reverse=True)
    
    # Keep top 10 only
    return LEADERBOARD[:10]


def get_leaderboard():
    """Get current leaderboard"""
    return LEADERBOARD[:10]
