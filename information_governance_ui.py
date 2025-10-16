"""
INFORMATION GOVERNANCE TRAINING UI
Mandatory NHS Data Protection & Confidentiality Training

Required for ALL NHS staff annually
Must achieve 100% to complete
"""

import streamlit as st
from datetime import datetime
from information_governance_module import IG_TRAINING_MODULES, IG_ASSESSMENT, DATA_BREACH_PROCEDURE

def render_information_governance():
    """Main Information Governance training page"""
    
    st.title("🔒 Information Governance Training")
    st.markdown("### Mandatory Annual Training for All NHS Staff")
    
    # Warning banner
    st.warning("""
    ⚠️ **MANDATORY REQUIREMENT**
    
    All NHS staff must complete Information Governance training annually.
    You must achieve **100% on the final assessment** to receive your certificate.
    
    This training covers:
    - GDPR & Data Protection Act 2018
    - NHS Caldicott Principles
    - Patient Confidentiality
    - Cyber Security
    - Data Breach Procedures
    """)
    
    # Progress tracking
    if 'ig_progress' not in st.session_state:
        st.session_state.ig_progress = {
            'modules_completed': [],
            'assessment_score': 0,
            'certificate_issued': False
        }
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Training Modules",
        "🎯 Practice Scenarios",
        "📝 Final Assessment",
        "🚨 Data Breach Guide",
        "📜 My Certificate"
    ])
    
    with tab1:
        render_training_modules()
    
    with tab2:
        render_practice_scenarios()
    
    with tab3:
        render_final_assessment()
    
    with tab4:
        render_breach_procedure()
    
    with tab5:
        render_certificate()


def render_training_modules():
    """Display training content"""
    
    st.subheader("📚 Core Training Modules")
    
    st.info("""
    **Instructions:**
    - Read each module carefully
    - Complete the quiz at the end
    - All modules must be completed before final assessment
    """)
    
    # Module 1: GDPR Basics
    with st.expander("📖 Module 1: GDPR & Data Protection Fundamentals", expanded=False):
        module = IG_TRAINING_MODULES['gdpr_basics']
        st.markdown(module['content'])
        
        st.markdown("---")
        st.markdown("### 📝 Quick Quiz")
        
        for i, q in enumerate(module['quiz']):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            answer = st.radio(
                "Select your answer:",
                q['options'],
                key=f"gdpr_q{i}"
            )
            
            if st.button(f"Check Answer", key=f"gdpr_check{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success(f"✅ Correct! {q['explanation']}")
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
        
        if st.button("✅ Mark Module 1 Complete", key="complete_mod1"):
            if 'gdpr_basics' not in st.session_state.ig_progress['modules_completed']:
                st.session_state.ig_progress['modules_completed'].append('gdpr_basics')
            st.success("Module 1 completed!")
            st.rerun()
    
    # Module 2: Caldicott Principles
    with st.expander("📖 Module 2: NHS Caldicott Principles", expanded=False):
        module = IG_TRAINING_MODULES['caldicott_principles']
        st.markdown(module['content'])
        
        st.markdown("---")
        st.markdown("### 📝 Quick Quiz")
        
        for i, q in enumerate(module['quiz']):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            answer = st.radio(
                "Select your answer:",
                q['options'],
                key=f"caldicott_q{i}"
            )
            
            if st.button(f"Check Answer", key=f"caldicott_check{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success(f"✅ Correct! {q['explanation']}")
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
        
        if st.button("✅ Mark Module 2 Complete", key="complete_mod2"):
            if 'caldicott_principles' not in st.session_state.ig_progress['modules_completed']:
                st.session_state.ig_progress['modules_completed'].append('caldicott_principles')
            st.success("Module 2 completed!")
            st.rerun()
    
    # Progress indicator
    st.markdown("---")
    completed = len(st.session_state.ig_progress['modules_completed'])
    total = len(IG_TRAINING_MODULES)
    st.progress(completed / total)
    st.markdown(f"**Progress:** {completed}/{total} modules completed")


def render_practice_scenarios():
    """Interactive confidentiality scenarios"""
    
    st.subheader("🎯 Practice Scenarios - What Would You Do?")
    
    st.info("""
    Test your knowledge with realistic workplace scenarios.
    These are common situations NHS staff face daily.
    """)
    
    scenarios = IG_TRAINING_MODULES['confidentiality_scenarios']['scenarios']
    
    for i, scenario in enumerate(scenarios):
        with st.expander(f"Scenario {i+1}", expanded=(i==0)):
            st.markdown(scenario['scenario'])
            
            st.markdown("---")
            answer = st.radio(
                "What should you do?",
                scenario['options'],
                key=f"scenario_{i}"
            )
            
            if st.button("Check Answer", key=f"scenario_check_{i}"):
                if scenario['options'].index(answer) == scenario['correct']:
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect")
                
                st.info(scenario['explanation'])


def render_final_assessment():
    """Final assessment - must score 100%"""
    
    st.subheader("📝 Final Assessment")
    
    # Check if modules completed
    if len(st.session_state.ig_progress['modules_completed']) < 2:
        st.warning("⚠️ Please complete all training modules before taking the assessment.")
        return
    
    st.warning("""
    **ASSESSMENT REQUIREMENTS:**
    - You must score **100%** to pass
    - You can retake as many times as needed
    - Certificate issued immediately upon passing
    """)
    
    if st.button("🚀 Start Assessment", type="primary"):
        st.session_state.taking_assessment = True
        st.rerun()
    
    if st.session_state.get('taking_assessment', False):
        st.markdown("---")
        st.markdown("### Answer all questions:")
        
        answers = []
        
        for i, q in enumerate(IG_ASSESSMENT):
            st.markdown(f"**Question {i+1}:** {q['q']}")
            answer = st.radio(
                "Select your answer:",
                q['opts'],
                key=f"assessment_q{i}"
            )
            answers.append(q['opts'].index(answer))
        
        if st.button("📋 Submit Assessment", type="primary"):
            # Check answers
            correct = 0
            for i, q in enumerate(IG_ASSESSMENT):
                if answers[i] == q['ans']:
                    correct += 1
            
            score = (correct / len(IG_ASSESSMENT)) * 100
            st.session_state.ig_progress['assessment_score'] = score
            
            if score == 100:
                st.success("🎉 **CONGRATULATIONS! You scored 100%!**")
                st.session_state.ig_progress['certificate_issued'] = True
                st.session_state.ig_progress['completion_date'] = datetime.now().strftime("%d %B %Y")
                st.balloons()
            else:
                st.error(f"❌ You scored {score:.0f}%. You need 100% to pass.")
                st.warning("Review the incorrect answers below and try again:")
                
                for i, q in enumerate(IG_ASSESSMENT):
                    if answers[i] != q['ans']:
                        st.markdown(f"**Question {i+1}:** {q['q']}")
                        st.markdown(f"**Your answer:** {q['opts'][answers[i]]}")
                        st.markdown(f"**Correct answer:** {q['opts'][q['ans']]}")
                        st.info(q['exp'])
            
            st.session_state.taking_assessment = False
            st.rerun()


def render_breach_procedure():
    """Data breach reporting procedure"""
    
    st.subheader("🚨 Data Breach Reporting Procedure")
    
    st.markdown(DATA_BREACH_PROCEDURE)
    
    st.markdown("---")
    st.error("""
    **REMEMBER:**
    
    🚨 Report ALL suspected breaches immediately
    📞 Contact your line manager and IG team
    ⏰ ICO must be notified within 72 hours if serious
    📝 Document everything
    
    **Better to report and be wrong than not report a real breach!**
    """)
    
    # Quick breach checker
    st.markdown("---")
    st.subheader("🔍 Is This a Data Breach?")
    
    st.markdown("**Check if the following situations are data breaches:**")
    
    breach_quiz = [
        {"scenario": "Emailed patient list to wrong GP practice", "is_breach": True},
        {"scenario": "Discussed patient in corridor where others could hear", "is_breach": True},
        {"scenario": "Looked up a celebrity's medical record out of curiosity", "is_breach": True},
        {"scenario": "Shredded confidential documents", "is_breach": False},
        {"scenario": "Left patient notes in unlocked car overnight", "is_breach": True},
        {"scenario": "Used NHSmail to send patient info to another NHS trust", "is_breach": False}
    ]
    
    for i, item in enumerate(breach_quiz):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{i+1}.** {item['scenario']}")
        with col2:
            if st.button("Check", key=f"breach_q{i}"):
                if item['is_breach']:
                    st.error("YES - Data Breach!")
                else:
                    st.success("NO - Not a breach")


def render_certificate():
    """Display IG certificate if earned"""
    
    st.subheader("📜 Information Governance Certificate")
    
    if st.session_state.ig_progress.get('certificate_issued', False):
        completion_date = st.session_state.ig_progress.get('completion_date', 'Unknown')
        user_name = st.session_state.get('user_name', 'NHS Staff Member')
        
        st.success("✅ **You have successfully completed Information Governance training!**")
        
        # Certificate display
        st.markdown(f"""
        <div style="border: 5px solid gold; padding: 30px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin: 20px 0;">
            <h1>🏆 CERTIFICATE OF COMPLETION 🏆</h1>
            <h2 style="margin-top: 20px;">Information Governance Training</h2>
            <p style="font-size: 20px; margin-top: 20px;">This certifies that</p>
            <h2 style="margin: 10px 0; font-size: 32px;">{user_name}</h2>
            <p style="font-size: 20px; margin-top: 20px;">has successfully completed mandatory Information Governance training</p>
            <p style="font-size: 18px; margin-top: 20px;">covering GDPR, Data Protection, NHS Caldicott Principles, and Confidentiality</p>
            <p style="font-size: 20px; margin-top: 30px;">Assessment Score: <strong>100%</strong></p>
            <p style="font-size: 16px; margin-top: 20px;">Completion Date: {completion_date}</p>
            <p style="font-size: 14px; margin-top: 30px;">Valid for 12 months from date of completion</p>
            <p style="font-size: 12px; margin-top: 20px;">T21 Services Limited | NHS Training Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("""
        **Next Steps:**
        - Save or print this certificate for your records
        - You must retake this training in 12 months
        - Keep up to date with your Trust's IG policies
        """)
        
        if st.button("📥 Download Certificate (PDF)"):
            st.info("PDF download feature coming soon!")
    
    else:
        st.warning("""
        ⚠️ **Certificate not yet earned**
        
        To receive your Information Governance certificate:
        1. Complete all training modules
        2. Pass the final assessment with 100%
        
        Once completed, your certificate will appear here.
        """)


# Main render function
if __name__ == "__main__":
    render_information_governance()
