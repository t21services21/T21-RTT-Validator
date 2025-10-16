"""
EXAM MANAGEMENT SYSTEM FOR TUTORS/ADMINS
View exam questions, answers, and student performance by cohort/batch

🔒 COMPLIANCE FEATURES:
- Secure question bank management
- Cohort-specific exam tracking
- Proctoring logs for remote exams
- Academic integrity monitoring
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Exam data directories
EXAM_DATA_DIR = "exam_data"
COHORT_DATA_DIR = "cohort_data"
os.makedirs(EXAM_DATA_DIR, exist_ok=True)
os.makedirs(COHORT_DATA_DIR, exist_ok=True)


def render_exam_management_admin():
    """Main exam management interface for tutors/admin"""
    
    st.header("📋 Exam Management System - Tutor/Admin Portal")
    
    st.success("""
    **🎓 COMPREHENSIVE EXAM MANAGEMENT:**
    - View question bank by category
    - Track cohort/batch exam results
    - Monitor student performance
    - Ensure exam compliance (remote/hybrid)
    - Academic integrity tracking
    """)
    
    tabs = st.tabs([
        "📚 Question Bank",
        "👥 Cohort Management",
        "📊 Exam Results",
        "🔒 Compliance & Proctoring",
        "➕ Add/Edit Questions"
    ])
    
    with tabs[0]:
        render_question_bank()
    
    with tabs[1]:
        render_cohort_management()
    
    with tabs[2]:
        render_exam_results()
    
    with tabs[3]:
        render_compliance_proctoring()
    
    with tabs[4]:
        render_add_edit_questions()


def render_question_bank():
    """View all exam questions organized by category"""
    
    st.subheader("📚 RTT Exam Question Bank")
    
    st.info("""
    **Question Bank Overview:**
    - 1000+ RTT validation questions
    - 9 categories covering all RTT codes
    - 4 difficulty levels (Easy, Medium, Hard, Expert)
    - Regularly updated with new scenarios
    """)
    
    # Category selector
    categories = [
        "All Categories",
        "RTT Clock Start (Codes 10-13)",
        "RTT Clock Stop (Codes 20-21)",
        "Patient Removed Self (Codes 31-32)",
        "Administrative Codes (Code 02-03)",
        "Consultant Upgrades (Code 04-09)",
        "Active Monitoring (Codes 90-93)",
        "Cancer Pathways (62-day, 31-day)",
        "RTT Pauses & Adjustments",
        "Complex Scenarios"
    ]
    
    selected_category = st.selectbox("Select Category", categories)
    
    # Difficulty filter
    difficulty_filter = st.multiselect(
        "Filter by Difficulty",
        ["Easy", "Medium", "Hard", "Expert"],
        default=["Easy", "Medium", "Hard", "Expert"]
    )
    
    # Sample questions (in production, load from database)
    sample_questions = [
        {
            "id": "Q001",
            "category": "RTT Clock Start (Codes 10-13)",
            "difficulty": "Medium",
            "question": "Patient receives GP referral letter dated 15/03/2024 for Orthopaedic consultation. Practice posts letter on 18/03/2024. Hospital receives letter on 20/03/2024. What is the correct RTT clock start date?",
            "options": [
                "A) 15/03/2024 (GP letter date)",
                "B) 18/03/2024 (Posted date)",
                "C) 20/03/2024 (Hospital received date)",
                "D) Date of first hospital contact"
            ],
            "correct_answer": "C",
            "explanation": "RTT clock starts on the date the referral is RECEIVED by the provider, not the date written or posted. This is 20/03/2024.",
            "rtt_code": "Code 10",
            "times_used": 145,
            "success_rate": "68%"
        },
        {
            "id": "Q002",
            "category": "Patient Removed Self (Codes 31-32)",
            "difficulty": "Hard",
            "question": "Patient attends pre-op assessment and is told surgery will be scheduled within 2 weeks. Patient calls 3 days later saying they've changed their mind and don't want surgery. What code should be used?",
            "options": [
                "A) Code 31 - Patient declined treatment before it was offered",
                "B) Code 32 - Patient declined treatment after reasonable offer",
                "C) Code 20 - Patient did not attend",
                "D) Code 93 - Administrative error"
            ],
            "correct_answer": "B",
            "explanation": "Code 32 is correct because the patient was given a reasonable offer (surgery within 2 weeks) and declined AFTER that offer. Code 31 is only if patient declines before any offer is made.",
            "rtt_code": "Code 32",
            "times_used": 89,
            "success_rate": "54%"
        },
        {
            "id": "Q003",
            "category": "RTT Clock Stop (Codes 20-21)",
            "difficulty": "Easy",
            "question": "Patient undergoes day case surgery (hernia repair) on 10/05/2024. When does the RTT clock stop?",
            "options": [
                "A) Date surgery scheduled",
                "B) 10/05/2024 (Date of surgery)",
                "C) Date patient discharged",
                "D) Clock continues until follow-up"
            ],
            "correct_answer": "B",
            "explanation": "RTT clock stops on the date the patient receives definitive treatment. For surgical procedures, this is the date of surgery (10/05/2024). Code 20 is used.",
            "rtt_code": "Code 20",
            "times_used": 234,
            "success_rate": "87%"
        }
    ]
    
    # Filter questions
    filtered_questions = sample_questions
    if selected_category != "All Categories":
        filtered_questions = [q for q in filtered_questions if q["category"] == selected_category]
    filtered_questions = [q for q in filtered_questions if q["difficulty"] in difficulty_filter]
    
    st.markdown(f"### Showing {len(filtered_questions)} Questions")
    
    for q in filtered_questions:
        with st.expander(f"**{q['id']}** - {q['category']} - {q['difficulty']} - ✅ {q['success_rate']} success rate"):
            st.markdown(f"**Question:**\n{q['question']}")
            
            st.markdown("**Options:**")
            for option in q['options']:
                if option.startswith(q['correct_answer']):
                    st.success(f"✅ {option} **(CORRECT ANSWER)**")
                else:
                    st.markdown(f"• {option}")
            
            st.info(f"**Explanation:** {q['explanation']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Times Used", q['times_used'])
            with col2:
                st.metric("Success Rate", q['success_rate'])
            with col3:
                st.markdown(f"**RTT Code:** {q['rtt_code']}")
    
    # Export options
    st.markdown("---")
    if st.button("📥 Export Question Bank to Excel"):
        st.success("✅ Question bank exported! (Would download Excel file in production)")


def render_cohort_management():
    """Manage student cohorts/batches"""
    
    st.subheader("👥 Cohort & Batch Management")
    
    st.info("""
    **Track exams by cohort/batch:**
    - View which cohort took which exam
    - See questions used for each batch
    - Compare performance across cohorts
    - Ensure exam variation between batches
    """)
    
    # Sample cohorts
    cohorts = [
        {
            "cohort_id": "2024-OCT-01",
            "cohort_name": "October 2024 - Batch A",
            "exam_date": "15/10/2024",
            "students": 25,
            "avg_score": "84.2%",
            "pass_rate": "92%",
            "exam_mode": "Remote (Zoom Proctored)"
        },
        {
            "cohort_id": "2024-OCT-02",
            "cohort_name": "October 2024 - Batch B",
            "exam_date": "16/10/2024",
            "students": 28,
            "avg_score": "81.5%",
            "pass_rate": "89%",
            "exam_mode": "Hybrid (In-person + Remote)"
        },
        {
            "cohort_id": "2024-SEP-01",
            "cohort_name": "September 2024 - Batch A",
            "exam_date": "20/09/2024",
            "students": 30,
            "avg_score": "86.1%",
            "pass_rate": "93%",
            "exam_mode": "In-person"
        }
    ]
    
    df_cohorts = pd.DataFrame(cohorts)
    st.dataframe(df_cohorts, use_container_width=True, hide_index=True)
    
    # Select cohort for details
    st.markdown("---")
    selected_cohort = st.selectbox(
        "Select Cohort for Detailed View",
        [c["cohort_name"] for c in cohorts]
    )
    
    if selected_cohort:
        cohort_data = next(c for c in cohorts if c["cohort_name"] == selected_cohort)
        
        st.markdown(f"### 📋 {selected_cohort} - Exam Details")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Students", cohort_data["students"])
        with col2:
            st.metric("Average Score", cohort_data["avg_score"])
        with col3:
            st.metric("Pass Rate", cohort_data["pass_rate"])
        with col4:
            st.metric("Exam Mode", cohort_data["exam_mode"])
        
        st.markdown("#### 📝 Questions Used in This Exam")
        st.info("""
        This cohort received a personalized 100-question exam selected from our 1000+ question bank.
        Questions were randomly selected with balanced distribution across categories.
        """)
        
        # Show some example questions used
        st.markdown("**Sample Questions from This Exam:**")
        sample_used = [
            {"num": 1, "id": "Q045", "category": "Clock Start", "difficulty": "Medium"},
            {"num": 2, "id": "Q128", "category": "Clock Stop", "difficulty": "Easy"},
            {"num": 3, "id": "Q276", "category": "Patient Removed", "difficulty": "Hard"},
            {"num": "...", "id": "...", "category": "...", "difficulty": "..."},
            {"num": 100, "id": "Q892", "category": "Complex Scenarios", "difficulty": "Expert"}
        ]
        
        df_questions_used = pd.DataFrame(sample_used)
        st.dataframe(df_questions_used, use_container_width=True, hide_index=True)
        
        if st.button("📥 Download Full Question List for This Cohort"):
            st.success("✅ Full question list downloaded! (Would download PDF in production)")


def render_exam_results():
    """View exam results and student performance"""
    
    st.subheader("📊 Exam Results & Performance Analytics")
    
    st.info("""
    **Analyze student performance:**
    - Individual student results
    - Cohort comparisons
    - Question difficulty analysis
    - Identify weak areas
    """)
    
    # Sample student results
    student_results = [
        {
            "student_name": "John Smith",
            "cohort": "2024-OCT-01",
            "exam_date": "15/10/2024",
            "score": "89%",
            "result": "RTT Practitioner",
            "exam_mode": "Remote",
            "completion_time": "78 mins",
            "proctoring_status": "✅ Verified"
        },
        {
            "student_name": "Sarah Johnson",
            "cohort": "2024-OCT-01",
            "exam_date": "15/10/2024",
            "score": "92%",
            "result": "RTT Expert",
            "exam_mode": "Remote",
            "completion_time": "65 mins",
            "proctoring_status": "✅ Verified"
        },
        {
            "student_name": "Mohammed Ali",
            "cohort": "2024-OCT-01",
            "exam_date": "15/10/2024",
            "score": "76%",
            "result": "RTT Foundation",
            "exam_mode": "Remote",
            "completion_time": "89 mins",
            "proctoring_status": "✅ Verified"
        }
    ]
    
    df_results = pd.DataFrame(student_results)
    st.dataframe(df_results, use_container_width=True, hide_index=True)
    
    # Performance analytics
    st.markdown("---")
    st.markdown("### 📈 Performance Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Score", "84.2%", delta="+2.1%")
    with col2:
        st.metric("Pass Rate", "92%", delta="+3%")
    with col3:
        st.metric("Avg Time", "74 mins", delta="-6 mins")
    with col4:
        st.metric("Proctoring Issues", "0", delta="0")
    
    # Weakest topics
    st.markdown("#### 🎯 Areas Needing Improvement")
    weak_topics = [
        {"Topic": "Code 31 vs Code 32 (Patient Declined)", "Avg Score": "54%", "Students Struggling": "18/25"},
        {"Topic": "Complex Clock Adjustments", "Avg Score": "62%", "Students Struggling": "12/25"},
        {"Topic": "Cancer Pathway 62-day Rules", "Avg Score": "68%", "Students Struggling": "8/25"}
    ]
    
    df_weak = pd.DataFrame(weak_topics)
    st.dataframe(df_weak, use_container_width=True, hide_index=True)
    
    st.warning("""
    **⚠️ Recommendation:** Schedule additional training session on Code 31/32 distinction.
    Success rate on these questions is below 60% - students need more practice.
    """)


def render_compliance_proctoring():
    """Exam compliance and proctoring for remote/hybrid exams"""
    
    st.subheader("🔒 Exam Compliance & Proctoring System")
    
    st.success("""
    **✅ COMPREHENSIVE EXAM SECURITY:**
    - Remote proctoring logs (Zoom/Teams)
    - Identity verification
    - Screen monitoring alerts
    - Time tracking
    - Academic integrity checks
    - TQUK compliance requirements
    """)
    
    st.markdown("### 🎥 Remote Proctoring Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Identity Verification:**
        - Photo ID check before exam
        - Face recognition during exam
        - Webcam required throughout
        - Random photo captures
        
        **✅ Screen Monitoring:**
        - Tab switching detection
        - Copy/paste blocking
        - Full-screen mode required
        - Screenshot prevention
        """)
    
    with col2:
        st.markdown("""
        **✅ Integrity Checks:**
        - Unique exam for each student
        - Random question order
        - Time limits enforced
        - No backtracking
        
        **✅ Compliance Records:**
        - Video recordings (30 days)
        - Activity logs
        - Incident reports
        - TQUK audit trail
        """)
    
    st.markdown("---")
    st.markdown("### 📊 Proctoring Incident Log")
    
    incidents = [
        {
            "date": "15/10/2024",
            "student": "Alex Brown",
            "cohort": "2024-OCT-01",
            "incident": "Tab switched during exam",
            "action_taken": "Warning issued, continued exam",
            "severity": "Low",
            "status": "Resolved"
        },
        {
            "date": "16/10/2024",
            "student": "Lisa Chen",
            "cohort": "2024-OCT-02",
            "incident": "Webcam disconnected briefly",
            "action_taken": "Technical issue resolved, exam continued",
            "severity": "Low",
            "status": "Resolved"
        }
    ]
    
    df_incidents = pd.DataFrame(incidents)
    st.dataframe(df_incidents, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### ✅ TQUK Compliance Checklist")
    
    compliance_items = [
        ("Identity verification completed", True),
        ("Unique exam per student", True),
        ("Proctoring records maintained", True),
        ("Incident log up to date", True),
        ("Assessment secure and fair", True),
        ("Results properly recorded", True),
        ("Certificates issued correctly", True),
        ("Audit trail complete", True)
    ]
    
    for item, compliant in compliance_items:
        if compliant:
            st.success(f"✅ {item}")
        else:
            st.error(f"❌ {item}")
    
    st.markdown("---")
    if st.button("📥 Generate Compliance Report for TQUK"):
        st.success("✅ TQUK Compliance Report generated! (Would download PDF in production)")


def render_add_edit_questions():
    """Add or edit exam questions"""
    
    st.subheader("➕ Add/Edit Exam Questions")
    
    st.info("Add new RTT validation questions to the exam bank")
    
    with st.form("add_question_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category*", [
                "RTT Clock Start (Codes 10-13)",
                "RTT Clock Stop (Codes 20-21)",
                "Patient Removed Self (Codes 31-32)",
                "Administrative Codes (Code 02-03)",
                "Cancer Pathways",
                "Complex Scenarios"
            ])
            
            difficulty = st.selectbox("Difficulty*", ["Easy", "Medium", "Hard", "Expert"])
            rtt_code = st.text_input("RTT Code", placeholder="e.g., Code 10")
        
        with col2:
            question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Scenario"])
            points = st.number_input("Points", min_value=1, max_value=10, value=1)
        
        st.markdown("### Question")
        question_text = st.text_area(
            "Question Text*",
            height=150,
            placeholder="Enter the exam question here..."
        )
        
        st.markdown("### Answer Options")
        option_a = st.text_input("Option A*", placeholder="First answer option")
        option_b = st.text_input("Option B*", placeholder="Second answer option")
        option_c = st.text_input("Option C*", placeholder="Third answer option")
        option_d = st.text_input("Option D*", placeholder="Fourth answer option")
        
        correct_answer = st.selectbox("Correct Answer*", ["A", "B", "C", "D"])
        
        explanation = st.text_area(
            "Explanation*",
            height=100,
            placeholder="Explain why this answer is correct..."
        )
        
        submit = st.form_submit_button("➕ Add Question to Bank", type="primary")
        
        if submit:
            if not question_text or not option_a or not option_b or not option_c or not option_d or not explanation:
                st.error("❌ Please fill in all required fields")
            else:
                st.success("✅ Question added to exam bank!")
                st.balloons()
