"""
QUIZ & ASSESSMENT ENGINE
Interactive quizzes and assessments for courses

Features:
- Multiple choice questions
- True/False questions
- Practical scenarios
- Instant feedback
- Progress tracking
- Adaptive difficulty
"""

import random
import json
from datetime import datetime
from soc_training_database import db

class QuizEngine:
    """
    Quiz and assessment system
    """
    
    def __init__(self):
        self.question_bank = self.initialize_questions()
    
    def initialize_questions(self):
        """Initialize question bank"""
        
        return {
            "cybersecurity_basics": [
                {
                    "id": 1,
                    "question": "What does the 'C' in CIA Triad stand for?",
                    "options": ["Confidentiality", "Cryptography", "Certification", "Compliance"],
                    "correct": 0,
                    "explanation": "The CIA Triad stands for Confidentiality, Integrity, and Availability."
                },
                {
                    "id": 2,
                    "question": "Which of the following is NOT a common attack vector?",
                    "options": ["Phishing", "Malware", "Firewall", "SQL Injection"],
                    "correct": 2,
                    "explanation": "A firewall is a security control, not an attack vector."
                },
                {
                    "id": 3,
                    "question": "What is the primary purpose of encryption?",
                    "options": [
                        "To speed up data transmission",
                        "To protect data confidentiality",
                        "To compress data",
                        "To authenticate users"
                    ],
                    "correct": 1,
                    "explanation": "Encryption protects data confidentiality by making it unreadable without the key."
                },
                {
                    "id": 4,
                    "question": "Which protocol is used for secure web browsing?",
                    "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
                    "correct": 2,
                    "explanation": "HTTPS (HTTP Secure) encrypts web traffic using SSL/TLS."
                },
                {
                    "id": 5,
                    "question": "What is a zero-day vulnerability?",
                    "options": [
                        "A vulnerability that takes zero days to exploit",
                        "A vulnerability with no known fix",
                        "A vulnerability discovered on day zero",
                        "A vulnerability that expires in zero days"
                    ],
                    "correct": 1,
                    "explanation": "A zero-day vulnerability is one for which no patch or fix exists yet."
                }
            ],
            "network_security": [
                {
                    "id": 6,
                    "question": "What port does SSH typically use?",
                    "options": ["21", "22", "23", "25"],
                    "correct": 1,
                    "explanation": "SSH (Secure Shell) uses port 22 by default."
                },
                {
                    "id": 7,
                    "question": "What does IDS stand for?",
                    "options": [
                        "Internet Detection System",
                        "Intrusion Detection System",
                        "Internal Defense System",
                        "Integrated Data Security"
                    ],
                    "correct": 1,
                    "explanation": "IDS stands for Intrusion Detection System."
                }
            ],
            "soc_operations": [
                {
                    "id": 8,
                    "question": "What is the first step in incident response?",
                    "options": ["Containment", "Identification", "Eradication", "Recovery"],
                    "correct": 1,
                    "explanation": "Identification is the first step - you must identify that an incident occurred."
                },
                {
                    "id": 9,
                    "question": "What does SIEM stand for?",
                    "options": [
                        "Security Information and Event Management",
                        "System Integration and Event Monitoring",
                        "Security Incident and Event Monitoring",
                        "System Information and Error Management"
                    ],
                    "correct": 0,
                    "explanation": "SIEM stands for Security Information and Event Management."
                }
            ]
        }
    
    def generate_quiz(self, category, num_questions=5):
        """Generate a quiz from question bank"""
        
        questions = self.question_bank.get(category, [])
        
        if len(questions) < num_questions:
            num_questions = len(questions)
        
        selected = random.sample(questions, num_questions)
        
        # Shuffle options for each question
        quiz = []
        for q in selected:
            shuffled_q = q.copy()
            correct_answer = shuffled_q['options'][shuffled_q['correct']]
            
            # Shuffle options
            random.shuffle(shuffled_q['options'])
            
            # Update correct index
            shuffled_q['correct'] = shuffled_q['options'].index(correct_answer)
            
            quiz.append(shuffled_q)
        
        return quiz
    
    def check_answer(self, question, selected_option):
        """Check if answer is correct"""
        
        return selected_option == question['correct']
    
    def calculate_score(self, answers, questions):
        """Calculate quiz score"""
        
        correct = sum(1 for i, ans in enumerate(answers) if ans == questions[i]['correct'])
        total = len(questions)
        percentage = (correct / total) * 100 if total > 0 else 0
        
        return {
            "correct": correct,
            "total": total,
            "percentage": round(percentage, 1),
            "passed": percentage >= 70
        }
    
    def save_quiz_result(self, student_id, module_id, score):
        """Save quiz result to database"""
        
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE module_progress 
        SET quiz_score = ?
        WHERE student_id = ? AND module_id = ?
        """, (score['percentage'], student_id, module_id))
        
        conn.commit()
        conn.close()
        
        # Award points
        if score['passed']:
            db.update_student_points(student_id, score['correct'] * 5)

# Quiz engine instance
quiz_engine = QuizEngine()

def render_quiz_interface(student_id, module_id, category):
    """Render interactive quiz interface"""
    
    import streamlit as st
    
    st.markdown("### 📝 Module Quiz")
    
    # Initialize quiz if not exists
    if 'quiz' not in st.session_state:
        st.session_state.quiz = quiz_engine.generate_quiz(category, 5)
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.quiz_complete = False
    
    quiz = st.session_state.quiz
    current_q = st.session_state.current_question
    
    if not st.session_state.quiz_complete:
        # Show current question
        if current_q < len(quiz):
            question = quiz[current_q]
            
            st.markdown(f"**Question {current_q + 1} of {len(quiz)}**")
            st.markdown(f"### {question['question']}")
            
            # Progress bar
            st.progress((current_q) / len(quiz))
            
            # Options
            selected = st.radio(
                "Select your answer:",
                options=range(len(question['options'])),
                format_func=lambda x: question['options'][x],
                key=f"q_{current_q}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if current_q > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state.current_question -= 1
                        st.rerun()
            
            with col2:
                if st.button("Next ➡️" if current_q < len(quiz) - 1 else "Submit ✅"):
                    # Save answer
                    if len(st.session_state.answers) <= current_q:
                        st.session_state.answers.append(selected)
                    else:
                        st.session_state.answers[current_q] = selected
                    
                    if current_q < len(quiz) - 1:
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.session_state.quiz_complete = True
                        st.rerun()
    
    else:
        # Show results
        st.markdown("### 🎉 Quiz Complete!")
        
        score = quiz_engine.calculate_score(st.session_state.answers, quiz)
        
        # Save result
        quiz_engine.save_quiz_result(student_id, module_id, score)
        
        # Display score
        col_score1, col_score2, col_score3 = st.columns(3)
        
        with col_score1:
            st.metric("Score", f"{score['percentage']}%")
        
        with col_score2:
            st.metric("Correct", f"{score['correct']}/{score['total']}")
        
        with col_score3:
            if score['passed']:
                st.success("✅ Passed!")
            else:
                st.error("❌ Failed")
        
        # Show answers
        st.markdown("---")
        st.markdown("### 📊 Review Your Answers")
        
        for i, question in enumerate(quiz):
            user_answer = st.session_state.answers[i]
            correct_answer = question['correct']
            is_correct = user_answer == correct_answer
            
            with st.expander(f"Question {i+1}: {'✅' if is_correct else '❌'}"):
                st.markdown(f"**{question['question']}**")
                
                st.markdown(f"**Your answer:** {question['options'][user_answer]}")
                st.markdown(f"**Correct answer:** {question['options'][correct_answer]}")
                
                if is_correct:
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect")
                
                st.info(f"💡 **Explanation:** {question['explanation']}")
        
        # Retry button
        if st.button("🔄 Retake Quiz"):
            del st.session_state.quiz
            del st.session_state.current_question
            del st.session_state.answers
            del st.session_state.quiz_complete
            st.rerun()
