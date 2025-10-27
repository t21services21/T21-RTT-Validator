"""
TQUK Interactive Quizzes
Self-assessment quizzes with instant feedback for all courses
"""

import streamlit as st
import random

# Quiz database for Functional Skills English
ENGLISH_QUIZZES = {
    "Level 1": {
        "Reading": [
            {
                "question": "What is the purpose of a formal letter?",
                "options": ["To chat with friends", "To make official requests or complaints", "To tell jokes", "To share photos"],
                "correct": 1,
                "explanation": "Formal letters are used for official communication like job applications, complaints, or requests."
            },
            {
                "question": "Which of these is a fact?",
                "options": ["Pizza is the best food", "London is the capital of England", "Summer is better than winter", "Red is a nice color"],
                "correct": 1,
                "explanation": "A fact is something that can be proven true. London being the capital of England is a fact."
            },
            {
                "question": "What does 'skim reading' mean?",
                "options": ["Reading every word carefully", "Reading quickly to get the main idea", "Reading out loud", "Reading backwards"],
                "correct": 1,
                "explanation": "Skim reading means reading quickly to understand the main points without reading every word."
            }
        ],
        "Writing": [
            {
                "question": "Which sentence uses correct punctuation?",
                "options": ["its a lovely day", "Its a lovely day.", "Its a lovely day", "it's a lovely day."],
                "correct": 3,
                "explanation": "The correct sentence needs a capital letter at the start, an apostrophe in 'it's', and a full stop at the end."
            },
            {
                "question": "What should you include in a formal email?",
                "options": ["Emojis and slang", "A clear subject line and polite language", "Text speak like 'u' and 'r'", "Lots of exclamation marks!!!"],
                "correct": 1,
                "explanation": "Formal emails need a clear subject, polite language, and proper spelling - no slang or text speak."
            }
        ]
    },
    "Level 2": {
        "Reading": [
            {
                "question": "What is the difference between fact and opinion?",
                "options": ["There is no difference", "Facts can be proven, opinions are personal views", "Opinions are always wrong", "Facts are boring"],
                "correct": 1,
                "explanation": "Facts are statements that can be proven true or false. Opinions are personal beliefs that may vary."
            },
            {
                "question": "What is bias in a text?",
                "options": ["Perfect balance", "Favoring one side over another", "Using difficult words", "Writing in paragraphs"],
                "correct": 1,
                "explanation": "Bias means the text favors one viewpoint and may not present all sides fairly."
            }
        ],
        "Writing": [
            {
                "question": "Which sentence uses a semicolon correctly?",
                "options": ["I like tea; but not coffee", "I like tea; I don't like coffee", "I like; tea and coffee", "I like tea and; coffee"],
                "correct": 1,
                "explanation": "A semicolon joins two related independent clauses. 'I like tea; I don't like coffee' is correct."
            }
        ]
    }
}

# Quiz database for Functional Skills Maths
MATHS_QUIZZES = {
    "Level 1": {
        "Numbers": [
            {
                "question": "What is 10% of £50?",
                "options": ["£5", "£10", "£15", "£50"],
                "correct": 0,
                "explanation": "10% = 10/100 = 0.1. So 10% of £50 = £50 × 0.1 = £5"
            },
            {
                "question": "What is 1/2 + 1/4?",
                "options": ["1/6", "2/6", "3/4", "2/4"],
                "correct": 2,
                "explanation": "1/2 = 2/4, so 2/4 + 1/4 = 3/4"
            },
            {
                "question": "Round 47 to the nearest 10",
                "options": ["40", "45", "50", "47"],
                "correct": 2,
                "explanation": "47 is closer to 50 than to 40, so we round up to 50"
            }
        ],
        "Measures": [
            {
                "question": "How many centimeters in 2.5 meters?",
                "options": ["25 cm", "250 cm", "2500 cm", "0.25 cm"],
                "correct": 1,
                "explanation": "1 meter = 100 cm, so 2.5 meters = 2.5 × 100 = 250 cm"
            },
            {
                "question": "What is the area of a rectangle 5cm × 3cm?",
                "options": ["8 cm²", "15 cm²", "16 cm²", "30 cm²"],
                "correct": 1,
                "explanation": "Area = length × width = 5 × 3 = 15 cm²"
            }
        ]
    },
    "Level 2": {
        "Numbers": [
            {
                "question": "What is 15% of £200?",
                "options": ["£15", "£20", "£30", "£35"],
                "correct": 2,
                "explanation": "15% of £200 = £200 × 0.15 = £30"
            },
            {
                "question": "Simplify the ratio 12:18",
                "options": ["6:9", "2:3", "4:6", "1:2"],
                "correct": 1,
                "explanation": "Divide both numbers by 6: 12÷6 = 2, 18÷6 = 3, so 2:3"
            }
        ],
        "Measures": [
            {
                "question": "What is the area of a circle with radius 5cm? (π ≈ 3.14)",
                "options": ["15.7 cm²", "31.4 cm²", "78.5 cm²", "157 cm²"],
                "correct": 2,
                "explanation": "Area = πr² = 3.14 × 5² = 3.14 × 25 = 78.5 cm²"
            }
        ]
    }
}

def render_interactive_quiz(subject, level, topic):
    """Render an interactive quiz with instant feedback"""
    
    st.subheader(f"🎯 {topic} Quiz - {level}")
    
    # Get quiz questions
    if subject == "English":
        quizzes = ENGLISH_QUIZZES.get(level, {}).get(topic, [])
    else:  # Maths
        quizzes = MATHS_QUIZZES.get(level, {}).get(topic, [])
    
    if not quizzes:
        st.info(f"Quiz for {topic} coming soon!")
        return
    
    # Initialize session state for quiz
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    
    # Display quiz
    st.info(f"**{len(quizzes)} questions** - Select your answer for each question")
    
    for i, q in enumerate(quizzes):
        st.markdown(f"### Question {i+1}")
        st.markdown(q["question"])
        
        # Radio buttons for options
        answer = st.radio(
            "Select your answer:",
            options=q["options"],
            key=f"quiz_{subject}_{level}_{topic}_q{i}",
            index=None
        )
        
        # Store answer
        if answer:
            st.session_state.quiz_answers[i] = q["options"].index(answer)
        
        # Show feedback if submitted
        if st.session_state.quiz_submitted and i in st.session_state.quiz_answers:
            if st.session_state.quiz_answers[i] == q["correct"]:
                st.success(f"✅ Correct! {q['explanation']}")
            else:
                st.error(f"❌ Incorrect. The correct answer is: **{q['options'][q['correct']]}**")
                st.info(f"💡 {q['explanation']}")
        
        st.markdown("---")
    
    # Submit button
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Submit Quiz", use_container_width=True, disabled=st.session_state.quiz_submitted):
            if len(st.session_state.quiz_answers) < len(quizzes):
                st.warning("⚠️ Please answer all questions before submitting!")
            else:
                # Calculate score
                correct = sum(1 for i, ans in st.session_state.quiz_answers.items() 
                             if ans == quizzes[i]["correct"])
                st.session_state.quiz_score = correct
                st.session_state.quiz_submitted = True
                st.rerun()
    
    with col2:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.rerun()
    
    # Show score if submitted
    if st.session_state.quiz_submitted:
        score = st.session_state.quiz_score
        total = len(quizzes)
        percentage = (score / total) * 100
        
        st.markdown("---")
        st.markdown("### 📊 Your Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{score}/{total}")
        with col2:
            st.metric("Percentage", f"{percentage:.0f}%")
        with col3:
            if percentage >= 80:
                st.metric("Grade", "⭐ Excellent!")
            elif percentage >= 60:
                st.metric("Grade", "✅ Good")
            else:
                st.metric("Grade", "📚 Keep practicing")
        
        st.progress(percentage / 100)
        
        if percentage >= 80:
            st.success("🎉 Great work! You've mastered this topic!")
        elif percentage >= 60:
            st.info("👍 Good effort! Review the questions you got wrong and try again.")
        else:
            st.warning("📖 Keep studying! Review the learning materials and try the quiz again.")

def render_quiz_selector(subject, level):
    """Render quiz topic selector"""
    
    st.markdown("### 🎯 Interactive Quizzes")
    
    st.info("""
    **Test your knowledge with instant feedback!**
    
    - Multiple choice questions
    - Immediate explanations
    - Track your progress
    - Unlimited attempts
    """)
    
    # Topic selector
    if subject == "English":
        topics = list(ENGLISH_QUIZZES.get(level, {}).keys())
    else:
        topics = list(MATHS_QUIZZES.get(level, {}).keys())
    
    if not topics:
        st.warning("Quizzes coming soon for this level!")
        return
    
    selected_topic = st.selectbox(
        "Select Topic:",
        topics,
        key=f"quiz_topic_{subject}_{level}"
    )
    
    st.markdown("---")
    
    if selected_topic:
        render_interactive_quiz(subject, level, selected_topic)

if __name__ == "__main__":
    st.title("🎯 Interactive Quizzes")
    
    subject = st.radio("Select Subject:", ["English", "Maths"], horizontal=True)
    level = st.radio("Select Level:", ["Level 1", "Level 2"], horizontal=True)
    
    st.markdown("---")
    
    render_quiz_selector(subject, level)
