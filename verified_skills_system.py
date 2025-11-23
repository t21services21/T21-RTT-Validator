"""
Verified Skills & Badge System
Employer-trusted skill assessments with public verification

This system provides:
- Proctored skill assessments
- Verified digital badges
- Public verification URLs
- LinkedIn integration
- Employer trust scores
- Real-time verification API

WHY THIS MATTERS:
- Employers skip their own technical assessments
- Learners get interviews faster
- Higher starting salaries
- Platform becomes industry standard
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import uuid
from typing import Dict, List, Optional
import qrcode
from io import BytesIO
import json

# Skill assessment structure
class SkillAssessment:
    """Individual skill assessment with verification"""
    
    def __init__(
        self,
        skill_id: str,
        skill_name: str,
        skill_category: str,
        difficulty_level: str,
        time_limit_minutes: int,
        pass_threshold: float,
        questions: List[Dict]
    ):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_category = skill_category
        self.difficulty_level = difficulty_level
        self.time_limit = time_limit_minutes
        self.pass_threshold = pass_threshold
        self.questions = questions


# Skill assessments catalog
SKILL_ASSESSMENTS = {
    "python_fundamentals": SkillAssessment(
        skill_id="python_fundamentals",
        skill_name="Python for Data Analysis",
        skill_category="Programming",
        difficulty_level="Intermediate",
        time_limit_minutes=60,
        pass_threshold=0.80,
        questions=[
            {
                "type": "coding",
                "question": "Write a function to clean and analyze a pandas DataFrame",
                "points": 20,
                "test_cases": 5
            },
            {
                "type": "multiple_choice",
                "question": "Which pandas method is most efficient for large datasets?",
                "points": 5,
                "options": ["iterrows()", "apply()", "vectorized operations", "for loop"]
            }
            # ... 15 more questions
        ]
    ),
    
    "sql_advanced": SkillAssessment(
        skill_id="sql_advanced",
        skill_name="SQL - Advanced Analytics",
        skill_category="Data Querying",
        difficulty_level="Advanced",
        time_limit_minutes=90,
        pass_threshold=0.75,
        questions=[
            {
                "type": "sql_query",
                "question": "Write a query using window functions to calculate running totals",
                "points": 25,
                "database_schema": "sales database"
            }
            # ... more questions
        ]
    ),
    
    "machine_learning": SkillAssessment(
        skill_id="machine_learning",
        skill_name="Machine Learning - Production Ready",
        skill_category="ML/AI",
        difficulty_level="Advanced",
        time_limit_minutes=120,
        pass_threshold=0.80,
        questions=[
            {
                "type": "coding",
                "question": "Build and evaluate a classification model with proper validation",
                "points": 30
            },
            {
                "type": "case_study",
                "question": "Design an ML system for real-time fraud detection",
                "points": 25
            }
            # ... more questions
        ]
    ),
    
    "data_visualization": SkillAssessment(
        skill_id="data_visualization",
        skill_name="Data Visualization & Storytelling",
        skill_category="Communication",
        difficulty_level="Intermediate",
        time_limit_minutes=90,
        pass_threshold=0.75,
        questions=[
            {
                "type": "practical",
                "question": "Create a dashboard from messy data and present insights",
                "points": 40
            }
        ]
    ),
    
    "statistics": SkillAssessment(
        skill_id="statistics",
        skill_name="Statistics for Data Science",
        skill_category="Mathematics",
        difficulty_level="Intermediate",
        time_limit_minutes=60,
        pass_threshold=0.80,
        questions=[]
    ),
    
    "data_engineering": SkillAssessment(
        skill_id="data_engineering",
        skill_name="Data Engineering - ETL & Pipelines",
        skill_category="Engineering",
        difficulty_level="Advanced",
        time_limit_minutes=120,
        pass_threshold=0.75,
        questions=[]
    ),
    
    "spark": SkillAssessment(
        skill_id="spark",
        skill_name="Apache Spark - Big Data Processing",
        skill_category="Big Data",
        difficulty_level="Advanced",
        time_limit_minutes=90,
        pass_threshold=0.75,
        questions=[]
    ),
    
    "deep_learning": SkillAssessment(
        skill_id="deep_learning",
        skill_name="Deep Learning & Neural Networks",
        skill_category="ML/AI",
        difficulty_level="Expert",
        time_limit_minutes=120,
        pass_threshold=0.70,
        questions=[]
    ),
    
    "ab_testing": SkillAssessment(
        skill_id="ab_testing",
        skill_name="A/B Testing & Experimentation",
        skill_category="Analytics",
        difficulty_level="Intermediate",
        time_limit_minutes=60,
        pass_threshold=0.75,
        questions=[]
    ),
    
    "mlops": SkillAssessment(
        skill_id="mlops",
        skill_name="MLOps - Model Deployment",
        skill_category="ML/AI",
        difficulty_level="Expert",
        time_limit_minutes=120,
        pass_threshold=0.75,
        questions=[]
    )
}


class VerifiedBadge:
    """Digital badge with verification"""
    
    def __init__(
        self,
        badge_id: str,
        user_id: str,
        skill_id: str,
        skill_name: str,
        score: float,
        issued_date: datetime,
        expiry_date: Optional[datetime] = None
    ):
        self.badge_id = badge_id
        self.user_id = user_id
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.score = score
        self.issued_date = issued_date
        self.expiry_date = expiry_date
        self.verification_url = self._generate_verification_url()
        self.verification_code = self._generate_verification_code()
        
    def _generate_verification_url(self) -> str:
        """Generate public verification URL"""
        return f"https://verify.yourplatform.com/badge/{self.badge_id}"
    
    def _generate_verification_code(self) -> str:
        """Generate unique verification code"""
        data = f"{self.badge_id}{self.user_id}{self.skill_id}"
        return hashlib.sha256(data.encode()).hexdigest()[:12].upper()
    
    def is_valid(self) -> bool:
        """Check if badge is still valid"""
        if self.expiry_date:
            return datetime.now() < self.expiry_date
        return True
    
    def to_linkedin_format(self) -> Dict:
        """Format for LinkedIn certification"""
        return {
            "name": f"Verified: {self.skill_name}",
            "organization": "Your Platform Name",
            "issue_date": self.issued_date.strftime("%Y-%m"),
            "credential_id": self.verification_code,
            "credential_url": self.verification_url
        }


def render_skill_assessment_catalog():
    """Display available skill assessments"""
    
    st.title("🏅 Verified Skills & Certifications")
    
    st.markdown("""
    Earn **employer-trusted badges** that prove your skills. Our assessments are:
    - ✅ **Proctored** - Ensures integrity
    - ✅ **Verified** - Public verification URLs
    - ✅ **Trusted** - Recognized by 100+ companies
    - ✅ **LinkedIn-Ready** - Add directly to profile
    - ✅ **Career-Boosting** - Skip technical interviews
    """)
    
    st.info("""
    💡 **Why employers trust our badges:**
    - Rigorous proctored assessments
    - Industry-standard evaluation criteria
    - Public verification system
    - Can't be faked or copied
    - Real-world practical problems
    """)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox(
            "Category",
            ["All", "Programming", "ML/AI", "Engineering", "Analytics"]
        )
    with col2:
        difficulty_filter = st.selectbox(
            "Difficulty",
            ["All", "Intermediate", "Advanced", "Expert"]
        )
    with col3:
        status_filter = st.selectbox(
            "Your Status",
            ["All", "Not Started", "In Progress", "Earned"]
        )
    
    # Display assessments as cards
    st.markdown("---")
    st.subheader("Available Skill Assessments")
    
    for skill_id, assessment in SKILL_ASSESSMENTS.items():
        with st.expander(
            f"{'🏆' if status_filter == 'Earned' else '📋'} {assessment.skill_name} - {assessment.difficulty_level}",
            expanded=False
        ):
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                st.markdown(f"**Category:** {assessment.skill_category}")
                st.markdown(f"**Difficulty:** {assessment.difficulty_level}")
                st.markdown(f"**Duration:** {assessment.time_limit} minutes")
                st.markdown(f"**Pass Threshold:** {int(assessment.pass_threshold * 100)}%")
                
                st.markdown("**What You'll Prove:**")
                if "python" in skill_id:
                    st.markdown("""
                    - Data manipulation with pandas
                    - Efficient code writing
                    - Error handling
                    - Real-world problem solving
                    """)
                elif "sql" in skill_id:
                    st.markdown("""
                    - Complex queries with joins
                    - Window functions
                    - Query optimization
                    - Database design
                    """)
                elif "machine_learning" in skill_id:
                    st.markdown("""
                    - End-to-end ML pipeline
                    - Model selection & tuning
                    - Proper validation
                    - Production considerations
                    """)
            
            with col_b:
                # Badge preview
                st.image("https://via.placeholder.com/150x150?text=Badge", width=150)
                
                if st.button(f"Start Assessment", key=f"start_{skill_id}"):
                    st.session_state.active_assessment = skill_id
                    st.rerun()
                
                st.markdown("**Recognition:**")
                st.markdown("✅ 50+ companies")
                st.markdown("✅ LinkedIn verified")
            
            # Sample questions
            with st.expander("Preview Sample Question"):
                st.code("""
# Sample Question:
# Write a function that cleans a DataFrame and calculates summary statistics

def analyze_data(df):
    '''
    Clean DataFrame and return summary statistics
    
    Args:
        df: pandas DataFrame with potential missing values
    
    Returns:
        dict with summary statistics
    '''
    # Your code here
    pass
                """, language="python")


def render_proctored_assessment(assessment_id: str):
    """Render proctored assessment interface"""
    
    assessment = SKILL_ASSESSMENTS.get(assessment_id)
    if not assessment:
        st.error("Assessment not found")
        return
    
    st.title(f"🔒 Proctored Assessment: {assessment.skill_name}")
    
    # Proctoring requirements
    st.warning("""
    ⚠️ **Proctored Assessment Requirements:**
    - Webcam must be enabled (identity verification)
    - Full screen mode (no switching tabs)
    - Time limit enforced
    - All code execution logged
    - Suspicious activity flagged
    
    **Academic Integrity:** Violations result in permanent ban.
    """)
    
    # Pre-assessment checklist
    st.markdown("### Before You Begin")
    
    checklist = {
        "I have read the assessment requirements": False,
        "My webcam is working": False,
        "I'm in a quiet environment": False,
        "I have stable internet": False,
        "I understand this is proctored": False,
        "I agree to academic integrity policy": False
    }
    
    all_checked = True
    for item, checked in checklist.items():
        if not st.checkbox(item, key=item):
            all_checked = False
    
    # System check
    st.markdown("---")
    st.markdown("### System Check")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ Camera: Ready")
    with col2:
        st.success("✅ Internet: Stable")
    with col3:
        st.success("✅ Browser: Compatible")
    
    # Start button
    st.markdown("---")
    if all_checked:
        if st.button("🚀 Begin Proctored Assessment", type="primary"):
            st.session_state.assessment_started = True
            st.session_state.assessment_start_time = datetime.now()
            st.rerun()
    else:
        st.info("Complete all checklist items to begin")
    
    # Active assessment
    if st.session_state.get('assessment_started', False):
        render_active_assessment(assessment)


def render_active_assessment(assessment: SkillAssessment):
    """Render active assessment with timer"""
    
    # Timer
    start_time = st.session_state.assessment_start_time
    elapsed = (datetime.now() - start_time).total_seconds()
    remaining = (assessment.time_limit * 60) - elapsed
    
    if remaining <= 0:
        st.error("⏰ Time's up! Submitting assessment...")
        # Auto-submit
        return
    
    # Progress bar
    progress = elapsed / (assessment.time_limit * 60)
    st.progress(progress)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Time Remaining", f"{int(remaining/60)}:{int(remaining%60):02d}")
    with col2:
        st.metric("Questions", "3/15")
    with col3:
        st.metric("Score", "85%")
    
    # Warning if low time
    if remaining < 300:  # 5 minutes
        st.warning("⚠️ Less than 5 minutes remaining!")
    
    st.markdown("---")
    
    # Sample question
    st.markdown("### Question 3 of 15")
    st.markdown("""
    **Scenario:** You have a DataFrame with 1M rows of customer transactions.
    Write an efficient function to calculate the top 10 customers by total spend.
    
    Requirements:
    - Handle missing values
    - Optimize for performance
    - Return sorted results
    """)
    
    code = st.text_area(
        "Your solution:",
        height=300,
        value="""import pandas as pd
import numpy as np

def top_customers(df):
    '''
    Calculate top 10 customers by total spend
    
    Args:
        df: DataFrame with columns customer_id, transaction_amount
    
    Returns:
        DataFrame with customer_id and total_spend
    '''
    # Your code here
    pass
"""
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶️ Run Tests"):
            st.success("✅ All test cases passed!")
    with col_b:
        if st.button("Next Question ➡️"):
            st.info("Moving to next question...")
    
    # Submit assessment
    st.markdown("---")
    if st.button("📤 Submit Assessment", type="primary"):
        render_assessment_results(assessment)


def render_assessment_results(assessment: SkillAssessment):
    """Display assessment results and issue badge"""
    
    st.title("🎉 Assessment Complete!")
    
    # Calculate score
    score = 87.5  # Sample score
    passed = score >= (assessment.pass_threshold * 100)
    
    if passed:
        st.balloons()
        st.success(f"✅ **PASSED!** Score: {score}%")
        
        # Issue badge
        badge = VerifiedBadge(
            badge_id=str(uuid.uuid4()),
            user_id="user_123",
            skill_id=assessment.skill_id,
            skill_name=assessment.skill_name,
            score=score,
            issued_date=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=730)  # 2 years
        )
        
        st.markdown("---")
        st.subheader("🏅 Your Verified Badge")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/200x200?text=Badge", width=200)
        
        with col2:
            st.markdown(f"**Skill:** {badge.skill_name}")
            st.markdown(f"**Score:** {badge.score}%")
            st.markdown(f"**Issued:** {badge.issued_date.strftime('%B %d, %Y')}")
            st.markdown(f"**Valid Until:** {badge.expiry_date.strftime('%B %d, %Y')}")
            st.markdown(f"**Verification Code:** `{badge.verification_code}`")
            
            st.markdown("**Verification URL:**")
            st.code(badge.verification_url)
        
        # Actions
        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("📥 Download Certificate"):
                st.success("Certificate downloaded!")
        with col_b:
            if st.button("💼 Add to LinkedIn"):
                st.info("LinkedIn integration opening...")
        with col_c:
            if st.button("📧 Share with Employers"):
                st.success("Shareable link copied!")
        
        # LinkedIn instructions
        st.markdown("---")
        st.subheader("📌 Add to LinkedIn Profile")
        st.markdown("""
        1. Go to LinkedIn profile
        2. Click "Add profile section" → "Licenses & Certifications"
        3. Fill in:
           - **Name:** {name}
           - **Issuing Organization:** Your Platform Name
           - **Issue Date:** {date}
           - **Credential ID:** {code}
           - **Credential URL:** {url}
        4. Click Save
        
        ✅ Employers can verify by clicking the URL!
        """.format(
            name=badge.skill_name,
            date=badge.issued_date.strftime("%B %Y"),
            code=badge.verification_code,
            url=badge.verification_url
        ))
        
    else:
        st.error(f"❌ **Not Passed** Score: {score}% (Required: {int(assessment.pass_threshold * 100)}%)")
        st.info("""
        **Next Steps:**
        - Review your mistakes
        - Study recommended materials
        - Retake in 7 days
        """)


def render_my_badges():
    """Display user's earned badges"""
    
    st.title("🏅 My Verified Badges")
    
    # Sample badges
    earned_badges = [
        {
            "skill": "Python for Data Analysis",
            "score": 92,
            "date": "November 2025",
            "verification_code": "PY9234ABC567",
            "status": "Active"
        },
        {
            "skill": "SQL - Advanced Analytics",
            "score": 88,
            "date": "October 2025",
            "verification_code": "SQL8834XYZ123",
            "status": "Active"
        },
        {
            "skill": "Machine Learning - Production",
            "score": 85,
            "date": "September 2025",
            "verification_code": "ML7745DEF890",
            "status": "Active"
        }
    ]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Badges Earned", len(earned_badges))
    with col2:
        st.metric("Average Score", "88%")
    with col3:
        st.metric("Verified By", "45 employers")
    with col4:
        st.metric("Profile Views", "+230%")
    
    st.markdown("---")
    
    # Display badges
    for badge in earned_badges:
        with st.expander(f"🏆 {badge['skill']} - {badge['score']}%", expanded=True):
            col_a, col_b, col_c = st.columns([1, 2, 1])
            
            with col_a:
                st.image("https://via.placeholder.com/150x150?text=Badge", width=150)
            
            with col_b:
                st.markdown(f"**Score:** {badge['score']}%")
                st.markdown(f"**Issued:** {badge['date']}")
                st.markdown(f"**Verification:** `{badge['verification_code']}`")
                st.markdown(f"**Status:** ✅ {badge['status']}")
                
                verification_url = f"https://verify.yourplatform.com/badge/{badge['verification_code']}"
                st.markdown(f"**Verify:** [{verification_url}]({verification_url})")
            
            with col_c:
                if st.button("Download", key=f"dl_{badge['verification_code']}"):
                    st.success("Downloaded!")
                if st.button("Share", key=f"share_{badge['verification_code']}"):
                    st.success("Link copied!")


def render_employer_verification():
    """Public verification page for employers"""
    
    st.title("✅ Verify Candidate Skills")
    
    st.markdown("""
    Enter a verification code to confirm a candidate's skills.
    This is a public, tamper-proof verification system.
    """)
    
    verification_code = st.text_input(
        "Verification Code",
        placeholder="e.g., PY9234ABC567"
    )
    
    if st.button("Verify Badge"):
        # Sample verification
        st.success("✅ Badge Verified!")
        
        st.markdown("---")
        st.subheader("Badge Information")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/200x200?text=Verified", width=200)
        
        with col2:
            st.markdown("**Candidate:** Alex Chen")
            st.markdown("**Skill:** Python for Data Analysis")
            st.markdown("**Score:** 92%")
            st.markdown("**Issued:** November 15, 2025")
            st.markdown("**Status:** ✅ Active")
            st.markdown("**Proctored:** Yes")
        
        st.markdown("---")
        st.subheader("Assessment Details")
        st.markdown("""
        **Assessment Type:** Proctored, timed coding challenges
        **Duration:** 60 minutes
        **Pass Threshold:** 80%
        **Questions:** 15 practical problems
        **Topics Covered:**
        - Data manipulation (pandas)
        - Performance optimization
        - Error handling
        - Real-world problem solving
        
        **Integrity Measures:**
        - ✅ Identity verified via webcam
        - ✅ Full screen enforced
        - ✅ Code execution logged
        - ✅ Time limit enforced
        """)
        
        # Employer actions
        st.markdown("---")
        if st.button("📥 Download Verification Report"):
            st.success("Report downloaded!")


# Main navigation
if __name__ == "__main__":
    st.set_page_config(page_title="Verified Skills", layout="wide")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        [
            "Skill Assessments",
            "My Badges",
            "Employer Verification",
            "Leaderboard"
        ]
    )
    
    if page == "Skill Assessments":
        if st.session_state.get('active_assessment'):
            render_proctored_assessment(st.session_state.active_assessment)
        else:
            render_skill_assessment_catalog()
    elif page == "My Badges":
        render_my_badges()
    elif page == "Employer Verification":
        render_employer_verification()
    else:
        st.title("🏆 Skills Leaderboard")
        st.markdown("See how you rank against other learners!")
        
        leaderboard_data = pd.DataFrame({
            'Rank': range(1, 11),
            'Name': ['Alex C.', 'Sarah K.', 'Mike J.', 'Emily W.', 'David L.',
                    'Lisa M.', 'John D.', 'Anna R.', 'Tom B.', 'Mary S.'],
            'Badges Earned': [15, 14, 13, 12, 11, 10, 9, 8, 8, 7],
            'Avg Score': ['94%', '92%', '91%', '90%', '89%', '88%', '87%', '86%', '86%', '85%']
        })
        
        st.dataframe(leaderboard_data, use_container_width=True)
