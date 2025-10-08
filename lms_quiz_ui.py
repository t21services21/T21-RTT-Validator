"""
T21 LMS - QUIZ UI
Student interface for taking quizzes

Features:
- Take quizzes
- Immediate feedback
- Score display
- Review answers
- Attempt history
"""

import streamlit as st
from lms_quiz_system import (
    get_quiz, submit_quiz_attempt, get_user_quiz_attempts,
    can_retake_quiz, get_best_quiz_score
)
from datetime import datetime


def render_quiz_interface(quiz_id, user_email):
    """Render the quiz taking interface"""
    
    quiz = get_quiz(quiz_id)
    
    if not quiz:
        st.error("Quiz not found")
        return
    
    # Check if user can take quiz
    can_retake = can_retake_quiz(user_email, quiz_id)
    attempts = get_user_quiz_attempts(user_email, quiz_id)
    best_score = get_best_quiz_score(user_email, quiz_id)
    
    # Quiz header
    st.title(f"📝 {quiz['title']}")
    st.markdown(quiz['description'])
    
    # Quiz info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Questions", len(quiz['questions']))
    
    with col2:
        st.metric("Time Limit", f"{quiz['time_limit_minutes']} min")
    
    with col3:
        st.metric("Passing Score", f"{quiz['passing_score']}%")
    
    with col4:
        if best_score is not None:
            st.metric("Best Score", f"{best_score}%")
        else:
            st.metric("Attempts", f"{len(attempts)}/{quiz['max_attempts']}")
    
    st.markdown("---")
    
    # Check if quiz already submitted in this session
    if 'quiz_result' in st.session_state and st.session_state.get('quiz_result_id') == quiz_id:
        render_quiz_results(st.session_state.quiz_result)
        
        if st.button("🔄 Take Again"):
            del st.session_state.quiz_result
            del st.session_state.quiz_result_id
            st.rerun()
        return
    
    # Check if can retake
    if not can_retake:
        st.error(f"❌ You've used all {quiz['max_attempts']} attempts for this quiz.")
        
        if attempts:
            st.markdown("### 📊 Your Attempts:")
            for idx, attempt in enumerate(attempts, 1):
                status = "✅ PASSED" if attempt['passed'] else "❌ FAILED"
                st.markdown(f"**Attempt {idx}:** {attempt['score']}% - {status}")
        
        return
    
    # Show previous attempts
    if attempts:
        with st.expander(f"📊 Previous Attempts ({len(attempts)})"):
            for idx, attempt in enumerate(attempts, 1):
                status = "✅ PASSED" if attempt['passed'] else "❌ FAILED"
                completed = datetime.fromisoformat(attempt['completed_at']).strftime('%Y-%m-%d %H:%M')
                st.markdown(f"**Attempt {idx}:** {attempt['score']}% - {status} (on {completed})")
    
    st.markdown("---")
    
    # Quiz instructions
    st.info(f"""
    **Instructions:**
    - Answer all questions
    - You have {quiz['time_limit_minutes']} minutes to complete
    - Passing score: {quiz['passing_score']}%
    - You can attempt this quiz {quiz['max_attempts']} times
    - Click 'Submit Quiz' when done
    """)
    
    st.markdown("---")
    
    # Quiz questions
    answers = {}
    
    for idx, question in enumerate(quiz['questions'], 1):
        st.markdown(f"### Question {idx}")
        st.markdown(f"**{question['question_text']}**")
        
        question_id = question['question_id']
        
        if question['type'] == 'multiple_choice':
            answer = st.radio(
                "Select your answer:",
                options=question['options'],
                key=f"q_{question_id}",
                index=None
            )
            if answer:
                answers[question_id] = answer
        
        elif question['type'] == 'true_false':
            answer = st.radio(
                "Select your answer:",
                options=["True", "False"],
                key=f"q_{question_id}",
                index=None
            )
            if answer:
                answers[question_id] = answer
        
        elif question['type'] == 'fill_blank':
            answer = st.text_input(
                "Your answer:",
                key=f"q_{question_id}"
            )
            if answer:
                answers[question_id] = answer
        
        st.markdown("---")
    
    # Submit button
    if st.button("📤 Submit Quiz", type="primary", use_container_width=True):
        # Check all questions answered
        if len(answers) < len(quiz['questions']):
            st.error("❌ Please answer all questions before submitting!")
        else:
            # Submit and grade
            result = submit_quiz_attempt(user_email, quiz_id, answers)
            
            if result:
                st.session_state.quiz_result = result
                st.session_state.quiz_result_id = quiz_id
                st.rerun()


def render_quiz_results(result):
    """Display quiz results with feedback"""
    
    st.markdown("---")
    
    # Score display
    score = result['score']
    passed = result['passed']
    
    if passed:
        st.success(f"# 🎉 CONGRATULATIONS! YOU PASSED!")
        st.balloons()
    else:
        st.error(f"# ❌ QUIZ FAILED")
    
    # Score metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Your Score", f"{score}%")
    
    with col2:
        st.metric("Points", f"{result['earned_points']}/{result['total_points']}")
    
    with col3:
        status = "PASSED ✅" if passed else "FAILED ❌"
        st.metric("Status", status)
    
    st.markdown("---")
    
    # Results breakdown
    st.subheader("📊 Answer Review")
    
    correct_count = sum(1 for r in result['results'] if r['is_correct'])
    total_count = len(result['results'])
    
    st.markdown(f"**Correct Answers:** {correct_count}/{total_count}")
    
    st.markdown("---")
    
    # Show each question result
    for idx, question_result in enumerate(result['results'], 1):
        is_correct = question_result['is_correct']
        
        if is_correct:
            st.success(f"### ✅ Question {idx}")
        else:
            st.error(f"### ❌ Question {idx}")
        
        st.markdown(f"**{question_result['question_text']}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Your Answer:**")
            if is_correct:
                st.success(question_result['user_answer'])
            else:
                st.error(question_result['user_answer'])
        
        with col2:
            st.markdown(f"**Correct Answer:**")
            st.info(question_result['correct_answer'])
        
        if question_result.get('explanation'):
            st.info(f"💡 **Explanation:** {question_result['explanation']}")
        
        st.markdown("---")


def render_quiz_list_for_course(course_id, user_email):
    """Render list of quizzes for a course"""
    
    from lms_quiz_system import get_quizzes_for_course
    
    quizzes = get_quizzes_for_course(course_id)
    
    if not quizzes:
        st.info("No quizzes available for this course yet.")
        return
    
    st.subheader(f"📝 Course Quizzes ({len(quizzes)})")
    
    for quiz in quizzes:
        with st.expander(f"📝 {quiz['title']}", expanded=False):
            st.markdown(quiz['description'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.caption(f"⏱️ {quiz['time_limit_minutes']} minutes")
            
            with col2:
                st.caption(f"📊 Passing: {quiz['passing_score']}%")
            
            with col3:
                best_score = get_best_quiz_score(user_email, quiz['quiz_id'])
                if best_score is not None:
                    if best_score >= quiz['passing_score']:
                        st.success(f"✅ Best: {best_score}%")
                    else:
                        st.warning(f"Best: {best_score}%")
            
            if st.button("📝 Take Quiz", key=f"quiz_{quiz['quiz_id']}"):
                st.session_state.active_quiz = quiz['quiz_id']
                st.rerun()
