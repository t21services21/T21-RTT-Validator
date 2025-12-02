"""
AI-Powered Mock Interview System
Practice technical and behavioral interviews with automated feedback

Features:
- Timed coding challenges
- Behavioral question practice
- System design interviews
- Performance scoring
- Detailed feedback
- Session recording and review
"""

import streamlit as st
from datetime import datetime, timedelta
import json
from typing import List, Dict
import pandas as pd

class InterviewSession:
    """Mock interview session manager"""
    
    def __init__(self, session_type: str, difficulty: str):
        self.session_type = session_type  # coding, behavioral, system_design
        self.difficulty = difficulty  # junior, mid, senior
        self.start_time = datetime.now()
        self.questions = []
        self.responses = []
        self.scores = {}
        
    def get_duration(self) -> int:
        """Get session duration in minutes"""
        return int((datetime.now() - self.start_time).total_seconds() / 60)


# Interview Question Banks
CODING_INTERVIEW_QUESTIONS = {
    "junior_data_analyst": [
        {
            "id": "ca_001",
            "question": "Write a SQL query to find the top 5 selling products by revenue.",
            "type": "sql",
            "time_limit": 15,
            "difficulty": "Easy",
            "test_cases": [
                "Should use GROUP BY and ORDER BY",
                "Should include SUM() for revenue",
                "Should LIMIT to 5 results"
            ],
            "ideal_answer": """
SELECT 
    product_name,
    SUM(quantity * unit_price) as total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 5;
            """,
            "scoring_rubric": {
                "correctness": 40,
                "efficiency": 20,
                "code_quality": 20,
                "explanation": 20
            }
        },
        {
            "id": "ca_002",
            "question": "You have a DataFrame with customer purchases. Calculate the average order value by customer segment.",
            "type": "python",
            "time_limit": 15,
            "difficulty": "Easy",
            "starter_code": """
import pandas as pd

def calculate_avg_by_segment(df):
    # df has columns: customer_id, segment, order_value
    # Return: DataFrame with segment and avg_order_value
    pass
            """,
            "test_cases": [
                "Group by segment",
                "Calculate mean of order_value",
                "Return properly formatted DataFrame"
            ],
            "ideal_answer": """
import pandas as pd

def calculate_avg_by_segment(df):
    return df.groupby('segment')['order_value'].mean().reset_index(
        name='avg_order_value'
    )
            """
        }
    ],
    
    "mid_data_scientist": [
        {
            "id": "cs_001",
            "question": "Implement a function to perform k-fold cross-validation and return average metrics.",
            "type": "python",
            "time_limit": 25,
            "difficulty": "Medium",
            "starter_code": """
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import numpy as np

def cross_validate(model, X, y, k=5):
    '''
    Perform k-fold cross validation.
    Return dict with mean and std of scores.
    '''
    pass
            """,
            "ideal_answer": """
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import numpy as np

def cross_validate(model, X, y, k=5):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    scores = []
    
    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        scores.append(accuracy_score(y_val, y_pred))
    
    return {
        'mean_score': np.mean(scores),
        'std_score': np.std(scores),
        'scores': scores
    }
            """
        }
    ],
    
    "senior_data_engineer": [
        {
            "id": "de_001",
            "question": "Design a data pipeline to process 1TB of daily event data with fault tolerance.",
            "type": "system_design",
            "time_limit": 30,
            "difficulty": "Hard",
            "evaluation_criteria": [
                "Scalability considerations",
                "Fault tolerance mechanisms",
                "Data quality checks",
                "Monitoring strategy",
                "Cost optimization"
            ]
        }
    ]
}


BEHAVIORAL_QUESTIONS = {
    "leadership": [
        "Tell me about a time you had to convince stakeholders to change direction on a data project.",
        "Describe a situation where you had to deliver bad news about project timelines.",
        "How did you handle a conflict with a team member over technical approach?"
    ],
    "problem_solving": [
        "Walk me through your approach to a data problem you've never seen before.",
        "Tell me about the most complex analysis you've done. What made it challenging?",
        "Describe a time when your initial analysis was wrong. What did you learn?"
    ],
    "communication": [
        "Explain a complex technical concept to a non-technical stakeholder. (I'll be the stakeholder)",
        "Tell me about a time you had to present findings to executives.",
        "How do you balance technical accuracy with making insights accessible?"
    ],
    "failure_learning": [
        "Tell me about a project that failed. What went wrong?",
        "Describe your biggest mistake and what you learned.",
        "Tell me about a time you missed a deadline. How did you handle it?"
    ]
}


SYSTEM_DESIGN_QUESTIONS = [
    {
        "question": "Design a recommendation system for 10M users with <100ms latency",
        "focus_areas": [
            "Architecture (batch vs real-time)",
            "Data storage strategy",
            "Caching approach",
            "Scalability",
            "A/B testing infrastructure"
        ],
        "time_limit": 45,
        "difficulty": "Senior"
    },
    {
        "question": "Design a real-time fraud detection system processing 10K transactions/second",
        "focus_areas": [
            "Stream processing architecture",
            "Feature computation at scale",
            "Model serving infrastructure",
            "Monitoring and alerting",
            "Handling false positives"
        ],
        "time_limit": 45,
        "difficulty": "Senior"
    }
]


def render_mock_interview_page():
    """Main interface for mock interviews"""
    st.title("🎤 Mock Interview Practice")
    
    st.markdown("""
    Practice interviews in a realistic environment with:
    - ✅ Timed questions like real interviews
    - 🤖 AI-powered feedback on your answers
    - 📊 Performance tracking and improvement areas
    - 🎥 Session recording for self-review
    - 🏆 Score and benchmark against others
    """)
    
    # Interview type selection
    st.markdown("---")
    st.subheader("Choose Interview Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        interview_type = st.selectbox(
            "Interview Format",
            [
                "Coding Interview (Technical)",
                "Behavioral Interview",
                "System Design Interview",
                "Full Mock Interview (Mixed)"
            ]
        )
    
    with col2:
        role_level = st.selectbox(
            "Role Level",
            [
                "Junior (0-2 years)",
                "Mid-Level (2-5 years)",
                "Senior (5+ years)"
            ]
        )
    
    specific_role = st.selectbox(
        "Specific Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Data Engineer",
            "ML Engineer",
            "Analytics Engineer"
        ]
    )
    
    # Interview settings
    st.markdown("---")
    st.subheader("Interview Settings")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        duration = st.slider("Duration (minutes)", 15, 60, 30)
    with col_b:
        difficulty = st.select_slider(
            "Difficulty",
            options=["Easy", "Medium", "Hard", "Expert"]
        )
    with col_c:
        enable_hints = st.checkbox("Enable hints", value=True)
    
    # Start interview button
    st.markdown("---")
    if st.button("🎬 Start Interview", type="primary"):
        st.session_state.interview_active = True
        st.session_state.interview_start = datetime.now()
        st.success("Interview started! Good luck!")
        st.rerun()
    
    # Active interview session
    if st.session_state.get('interview_active', False):
        render_interview_session(interview_type, role_level, difficulty)


def render_interview_session(interview_type: str, role_level: str, difficulty: str):
    """Render active interview session"""
    
    # Timer display
    start_time = st.session_state.interview_start
    elapsed = (datetime.now() - start_time).total_seconds()
    time_limit = 30 * 60  # 30 minutes
    remaining = time_limit - elapsed
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.metric("Time Remaining", f"{int(remaining/60)}:{int(remaining%60):02d}")
    with col2:
        st.metric("Questions", f"1/5")
    with col3:
        if st.button("End Interview"):
            st.session_state.interview_active = False
            render_interview_results()
            return
    
    st.markdown("---")
    
    # Sample coding question
    if "Coding" in interview_type:
        render_coding_question()
    elif "Behavioral" in interview_type:
        render_behavioral_question()
    elif "System Design" in interview_type:
        render_system_design_question()


def render_coding_question():
    """Render coding interview question"""
    
    question = {
        "question": "Write a function to find the second largest number in a list.",
        "time_limit": 15,
        "difficulty": "Medium"
    }
    
    st.markdown("### Coding Challenge")
    st.info(f"**Difficulty:** {question['difficulty']} | **Time:** {question['time_limit']} minutes")
    st.markdown(question['question'])
    
    st.markdown("#### Your Solution")
    code = st.text_area(
        "Write your code here:",
        height=300,
        value="""def second_largest(numbers):
    # Your code here
    pass

# Test cases
test1 = [3, 1, 4, 1, 5, 9, 2, 6]
test2 = [10, 5, 8, 12, 3]
"""
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Run Tests"):
            st.success("✅ 3/3 test cases passed!")
    with col2:
        if st.button("💡 Get Hint"):
            st.info("Try sorting the list or tracking the two largest values as you iterate")
    with col3:
        if st.button("Next Question ➡️"):
            st.info("Moving to next question...")
    
    # Code feedback
    st.markdown("---")
    st.markdown("### AI Feedback (After submission)")
    st.markdown("""
    **Correctness:** ✅ Your solution handles all test cases correctly.
    
    **Time Complexity:** ⚠️ Your solution is O(n log n) due to sorting. 
    Can be optimized to O(n) with single pass approach.
    
    **Code Quality:** ✅ Good variable naming and structure.
    
    **Suggestions:**
    - Consider edge cases (empty list, single element)
    - Add input validation
    - More efficient approach: Track two largest values in single pass
    """)


def render_behavioral_question():
    """Render behavioral interview question"""
    
    st.markdown("### Behavioral Question")
    
    question = "Tell me about a time you had to deliver bad news about a project delay to stakeholders."
    st.info(question)
    
    st.markdown("""
    **STAR Framework Reminder:**
    - **S**ituation: Set the context
    - **T**ask: Describe your responsibility
    - **A**ction: Explain what you did
    - **R**esult: Share the outcome
    """)
    
    response = st.text_area(
        "Your answer (aim for 2-3 minutes when speaking):",
        height=200,
        placeholder="Type your answer here..."
    )
    
    # Timer for answer
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏱️ Start Timer"):
            st.info("Timer started! Aim for 2-3 minutes.")
    with col2:
        if st.button("Submit Answer"):
            st.success("Answer recorded!")
    
    # Feedback
    if response:
        st.markdown("---")
        st.markdown("### AI Feedback")
        st.markdown("""
        **STAR Structure:** ✅ Well organized with clear situation and result
        
        **Communication:** ✅ Clear and concise
        
        **Authenticity:** Good - shows accountability
        
        **Suggestions:**
        - Add more details about stakeholder reactions
        - Mention what you learned for future situations
        - Quantify the impact if possible
        
        **Score:** 8/10
        """)


def render_system_design_question():
    """Render system design question"""
    
    st.markdown("### System Design Challenge")
    st.info("Design a real-time recommendation system for 10M users with <100ms latency")
    
    st.markdown("""
    **Consider:**
    - Architecture (batch vs real-time components)
    - Data storage strategy
    - Caching approach
    - Scalability
    - Monitoring
    
    **Time:** 45 minutes for complete design
    """)
    
    # Whiteboard area
    st.markdown("#### Your Design")
    design_notes = st.text_area(
        "Describe your architecture (draw diagram separately):",
        height=300,
        placeholder="Describe components, data flow, technologies..."
    )
    
    # Discussion points
    st.markdown("#### Key Questions to Address")
    
    questions_checklist = {
        "How will you handle cold start problem?": False,
        "What's your caching strategy?": False,
        "How do you ensure <100ms latency?": False,
        "How will you A/B test new models?": False,
        "What's your monitoring approach?": False
    }
    
    for question, checked in questions_checklist.items():
        st.checkbox(question, value=checked)
    
    if st.button("Submit Design"):
        st.success("Design recorded! Feedback will be provided after review.")


def render_interview_results():
    """Show interview performance results"""
    
    st.title("📊 Interview Performance Report")
    
    # Overall score
    overall_score = 78
    st.markdown(f"## Overall Score: {overall_score}/100")
    
    if overall_score >= 80:
        st.success("🎉 Excellent! You're ready for real interviews!")
    elif overall_score >= 60:
        st.info("👍 Good performance. Focus on improvement areas below.")
    else:
        st.warning("⚠️ Keep practicing. Review feedback carefully.")
    
    # Score breakdown
    st.markdown("---")
    st.subheader("Score Breakdown")
    
    scores = {
        "Technical Correctness": 85,
        "Code Quality": 75,
        "Communication": 80,
        "Problem Solving": 70,
        "Time Management": 75
    }
    
    for category, score in scores.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(score / 100)
        with col2:
            st.metric(category, f"{score}%")
    
    # Strengths and improvements
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💪 Strengths")
        st.markdown("""
        - Strong technical knowledge
        - Clear communication
        - Good use of STAR framework
        - Handled follow-up questions well
        """)
    
    with col2:
        st.subheader("📈 Areas to Improve")
        st.markdown("""
        - Practice time management
        - More edge case consideration
        - System design scalability thinking
        - Quantify business impact more
        """)
    
    # Detailed feedback
    st.markdown("---")
    st.subheader("Detailed Question Feedback")
    
    with st.expander("Question 1: SQL Query - Top 5 Products"):
        st.markdown("""
        **Your Answer:** 8/10
        - ✅ Correct logic and syntax
        - ✅ Proper use of GROUP BY and ORDER BY
        - ⚠️ Could optimize with index suggestion
        - ⚠️ Missing NULL handling consideration
        
        **Time:** 12 minutes (Good)
        """)
    
    # Recommendations
    st.markdown("---")
    st.subheader("📚 Recommended Practice")
    st.markdown("""
    1. **Code Challenges:** Complete 10 more medium-level SQL challenges
    2. **System Design:** Practice 3 more end-to-end designs
    3. **Behavioral:** Prepare 2 more failure/learning stories
    4. **Next Interview:** Try "Senior Data Scientist" level
    """)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Retake Interview"):
            st.session_state.interview_active = False
            st.rerun()
    with col2:
        if st.button("📥 Download Report"):
            st.info("Report downloaded!")
    with col3:
        if st.button("📧 Share with Mentor"):
            st.info("Report shared!")


def render_practice_stats():
    """Show interview practice statistics"""
    
    st.title("📊 Your Interview Practice Stats")
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Interviews Completed", "12")
    with col2:
        st.metric("Average Score", "76%", "+5%")
    with col3:
        st.metric("Practice Hours", "8.5")
    with col4:
        st.metric("Improvement Rate", "+18%")
    
    # Progress over time
    st.markdown("---")
    st.subheader("Score Progression")
    
    progress_data = pd.DataFrame({
        'Interview': range(1, 13),
        'Score': [55, 58, 62, 65, 68, 72, 70, 74, 76, 78, 79, 81]
    })
    
    st.line_chart(progress_data.set_index('Interview'))
    
    # Strengths by category
    st.markdown("---")
    st.subheader("Performance by Category")
    
    category_scores = pd.DataFrame({
        'Category': ['SQL', 'Python', 'ML', 'System Design', 'Behavioral'],
        'Average Score': [85, 78, 72, 65, 80]
    })
    
    st.bar_chart(category_scores.set_index('Category'))


# Main app navigation
if __name__ == "__main__":
    st.set_page_config(page_title="Mock Interviews", layout="wide")
    
    page = st.sidebar.radio(
        "Navigate",
        ["Start Interview", "Practice Stats", "Interview Tips"]
    )
    
    if page == "Start Interview":
        render_mock_interview_page()
    elif page == "Practice Stats":
        render_practice_stats()
    else:
        st.title("💡 Interview Tips & Strategies")
        st.markdown("""
        ### Technical Interview Tips
        - Always clarify the problem before coding
        - Think out loud to show your thought process
        - Test your code with edge cases
        - Discuss time/space complexity
        - Ask clarifying questions
        
        ### Behavioral Interview Tips
        - Use STAR framework consistently
        - Prepare 5-7 stories covering different situations
        - Show learning from failures
        - Quantify impact when possible
        - Be honest and authentic
        
        ### System Design Tips
        - Start with requirements clarification
        - Discuss trade-offs explicitly
        - Consider scalability from the start
        - Don't jump to implementation details too quickly
        - Discuss monitoring and operational concerns
        """)
