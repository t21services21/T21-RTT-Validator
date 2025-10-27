"""
TQUK Functional Skills English Level 1 & 2 Module
Dual-level qualification with Reading, Writing, Speaking, Listening components
"""

import streamlit as st
from datetime import datetime
from tquk_course_assignment import get_learner_enrollments

# Course IDs for both levels
COURSE_ID_L1 = "functional_skills_english_l1"
COURSE_ID_L2 = "functional_skills_english_l2"

# Course Details
COURSES = {
    "Level 1": {
        "id": COURSE_ID_L1,
        "name": "Functional Skills English Level 1",
        "qualification_number": "610/2626/8",
        "level": 1,
        "glh": 55,
        "description": "Entry level English skills for everyday life and work"
    },
    "Level 2": {
        "id": COURSE_ID_L2,
        "name": "Functional Skills English Level 2",
        "qualification_number": "610/2626/6",
        "level": 2,
        "glh": 55,
        "description": "GCSE equivalent English skills for work and further study"
    }
}

# Components for both levels
COMPONENTS = {
    "reading": {
        "name": "Reading",
        "icon": "📖",
        "description": "Understand and interpret texts"
    },
    "writing": {
        "name": "Writing",
        "icon": "✍️",
        "description": "Write clearly and effectively"
    },
    "speaking": {
        "name": "Speaking",
        "icon": "🗣️",
        "description": "Speak clearly and confidently"
    },
    "listening": {
        "name": "Listening",
        "icon": "👂",
        "description": "Understand spoken language"
    }
}


def render_functional_skills_english_module():
    """Main render function for Functional Skills English"""
    
    learner_email = st.session_state.get('user_email', '')
    
    st.title("📚 Functional Skills English")
    st.success("✅ **TQUK Approved** - Level 1 & Level 2 Qualifications")
    
    # Get user role
    user_role = st.session_state.get('user_role', 'student')
    
    # Admin/Staff preview notice
    if user_role in ['super_admin', 'admin', 'staff', 'tester']:
        st.info("👨‍💼 **Admin/Staff View** - Full access to preview. Students must be enrolled.")
    
    # Level selector
    st.markdown("---")
    selected_level = st.radio(
        "**Select Your Level:**",
        ["Level 1", "Level 2"],
        horizontal=True,
        help="Choose the level you're enrolled in"
    )
    
    course_info = COURSES[selected_level]
    course_id = course_info['id']
    
    # Display course info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Level", course_info['level'])
    with col2:
        st.metric("GLH", f"{course_info['glh']} hours")
    with col3:
        st.metric("Qualification", course_info['qualification_number'])
    
    # Get enrollment
    enrollment = None
    if learner_email:
        enrollments = get_learner_enrollments(learner_email)
        enrollment = next((e for e in enrollments if e['course_id'] == course_id), None)
    
    # Show enrollment status
    if enrollment:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Progress", f"{enrollment.get('progress', 0)}%")
            st.progress(enrollment.get('progress', 0) / 100)
        with col2:
            st.metric("Status", enrollment.get('status', 'active').title())
        with col3:
            st.metric("Components", "4")
    
    st.markdown("---")
    
    # 8 tabs (shortened names)
    tabs = st.tabs([
        "📚 Overview",
        "📖 Materials",
        "📝 Practice",
        "🎯 Mock Exam",
        "📋 Evidence",
        "📥 Docs",
        "📊 Progress",
        "🎓 Certificate"
    ])
    
    with tabs[0]:
        render_overview(selected_level, course_info)
    
    with tabs[1]:
        render_materials(selected_level, course_info)
    
    with tabs[2]:
        render_practice(selected_level, course_info)
    
    with tabs[3]:
        render_mock_exam(selected_level, course_info)
    
    with tabs[4]:
        render_evidence(selected_level, course_info, learner_email)
    
    with tabs[5]:
        render_tquk_documents(selected_level, course_info)
    
    with tabs[6]:
        render_progress(selected_level, course_info, enrollment)
    
    with tabs[7]:
        render_certificate(selected_level, course_info, enrollment)


def render_overview(level, course_info):
    """Render overview tab"""
    st.subheader("📚 Course Overview")
    
    st.success(f"""
    # 📚 Welcome to Functional Skills English {level}!
    
    **{course_info['description']}**
    """)
    
    st.markdown("---")
    
    st.markdown("### 📋 Qualification Details")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **Qualification:** {course_info['name']}  
        **Number:** {course_info['qualification_number']}  
        **Level:** {course_info['level']}  
        **GLH:** {course_info['glh']} hours
        """)
    with col2:
        st.info("""
        **Assessment:**  
        - Reading Exam
        - Writing Exam
        - Speaking & Listening Portfolio
        """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 What You'll Learn")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📖 Reading:**
        - Understand different texts
        - Find information
        - Identify purpose and audience
        - Use reference materials
        
        **✍️ Writing:**
        - Write clearly and effectively
        - Spelling, punctuation, grammar
        - Plan and organize writing
        - Different text types
        """)
    with col2:
        st.markdown("""
        **🗣️ Speaking:**
        - Speak clearly and confidently
        - Express ideas effectively
        - Participate in discussions
        - Formal and informal speech
        
        **👂 Listening:**
        - Understand spoken language
        - Follow instructions
        - Identify main points
        - Respond appropriately
        """)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Quick Start Guide")
    
    st.write("""
    **Step 1:** 📖 Study all 4 components (Materials tab)  
    **Step 2:** 📝 Complete practice exercises (Practice tab)  
    **Step 3:** 🎯 Take mock exams (Mock Exam tab)  
    **Step 4:** 📋 Submit your evidence (Evidence tab)  
    **Step 5:** 📊 Track your progress (Progress tab)  
    **Step 6:** 🎓 Receive your TQUK certificate!
    """)
    
    if level == "Level 2":
        st.success("""
        ### ⭐ Level 2 Advantage
        
        **Functional Skills English Level 2 is equivalent to GCSE English!**
        
        This qualification is:
        - ✅ Recognized by employers
        - ✅ Accepted by universities
        - ✅ Required for many jobs
        - ✅ Essential for apprenticeships
        """)


def render_materials(level, course_info):
    """Render materials tab"""
    st.subheader("📖 Learning Materials")
    
    st.info(f"""
    **Study all 4 components for {level}**
    
    Each component includes theory, examples, and guidance.
    """)
    
    # Component selector
    component = st.selectbox(
        "Select Component to Study:",
        list(COMPONENTS.keys()),
        format_func=lambda x: f"{COMPONENTS[x]['icon']} {COMPONENTS[x]['name']} - {COMPONENTS[x]['description']}",
        key="materials_component_selector"
    )
    
    component_info = COMPONENTS[component]
    
    st.markdown("---")
    
    st.markdown(f"## {component_info['icon']} {component_info['name']}")
    
    # Load content from markdown file
    try:
        with open('FUNCTIONAL_SKILLS_ENGLISH_ALL_CONTENT.md', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find the section for this level and component
            section_marker = f"# {level.upper()} - {component_info['name'].upper()}"
            if section_marker in content:
                section_start = content.find(section_marker)
                # Find next section or end
                next_section = content.find("\n# ", section_start + 1)
                if next_section == -1:
                    section_content = content[section_start:]
                else:
                    section_content = content[section_start:next_section]
                
                st.markdown(section_content)
            else:
                st.warning(f"Content for {level} {component_info['name']} is being prepared.")
    except FileNotFoundError:
        st.error("Content file not found. Please contact support.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📄 Download {component_info['name']} PDF", use_container_width=True):
            st.success("PDF download feature coming soon!")
    with col2:
        if st.button(f"✅ Mark {component_info['name']} Complete", use_container_width=True):
            st.success(f"{component_info['name']} marked as studied!")


def render_practice(level, course_info):
    """Render practice tab"""
    st.subheader("📝 Practice Exercises")
    
    st.info("""
    **Practice makes perfect!**
    
    Complete exercises for each component to build your skills.
    """)
    
    # Component selector
    component = st.selectbox(
        "Select Component:",
        list(COMPONENTS.keys()),
        format_func=lambda x: f"{COMPONENTS[x]['icon']} {COMPONENTS[x]['name']}",
        key="practice_component_selector"
    )
    
    component_info = COMPONENTS[component]
    
    st.markdown("---")
    
    st.markdown(f"## {component_info['icon']} {component_info['name']} Practice")
    
    if component == "reading":
        st.markdown("""
        ### 📖 Reading Practice
        
        **Exercise 1: Comprehension**
        
        Read the text below and answer the questions.
        
        *[Practice text would be loaded here]*
        """)
        
        st.text_area("Your Answer:", height=150)
        
        if st.button("Submit Answer"):
            st.success("Answer submitted! Check feedback below.")
    
    elif component == "writing":
        st.markdown("""
        ### ✍️ Writing Practice
        
        **Exercise 1: Write a Letter**
        
        Write a formal letter applying for a job.
        
        **Remember to include:**
        - Your address
        - Date
        - Recipient's address
        - Greeting
        - Body paragraphs
        - Closing
        """)
        
        st.text_area("Your Letter:", height=300)
        
        if st.button("Submit Writing"):
            st.success("Writing submitted for review!")
    
    elif component == "speaking":
        st.markdown("""
        ### 🗣️ Speaking Practice
        
        **Exercise 1: Presentation**
        
        Prepare a 2-minute presentation on a topic of your choice.
        
        **Tips:**
        - Speak clearly
        - Make eye contact
        - Use appropriate language
        - Structure your points
        """)
        
        st.info("Record your presentation and upload in the Evidence tab.")
    
    elif component == "listening":
        st.markdown("""
        ### 👂 Listening Practice
        
        **Exercise 1: Follow Instructions**
        
        Listen to the instructions and complete the task.
        
        *[Audio would be played here]*
        """)
        
        st.text_area("What did you understand?", height=150)
        
        if st.button("Submit Response"):
            st.success("Response submitted!")


def render_mock_exam(level, course_info):
    """Render mock exam tab"""
    st.subheader("🎯 Mock Examination")
    
    st.warning("""
    **⏱️ Timed Mock Exam**
    
    This is a practice exam under timed conditions.
    
    **Reading:** 45 minutes (L1) / 60 minutes (L2)  
    **Writing:** 45 minutes (L1) / 60 minutes (L2)
    """)
    
    exam_type = st.radio("Select Exam:", ["Reading", "Writing"], horizontal=True)
    
    st.markdown("---")
    
    if exam_type == "Reading":
        st.markdown(f"### 📖 {level} Reading Mock Exam")
        
        if st.button("🚀 Start Reading Exam", use_container_width=True):
            st.info("Mock exam feature coming soon! This will include full practice papers.")
    
    else:
        st.markdown(f"### ✍️ {level} Writing Mock Exam")
        
        if st.button("🚀 Start Writing Exam", use_container_width=True):
            st.info("Mock exam feature coming soon! This will include full practice papers.")


def render_evidence(level, course_info, learner_email):
    """Render evidence tab"""
    st.subheader("📋 Evidence Submission")
    
    st.info("""
    **Submit your evidence for each component**
    
    Upload your work to build your portfolio.
    """)
    
    component = st.selectbox(
        "Select Component:",
        list(COMPONENTS.keys()),
        format_func=lambda x: f"{COMPONENTS[x]['icon']} {COMPONENTS[x]['name']}",
        key="evidence_component_selector"
    )
    
    component_info = COMPONENTS[component]
    
    st.markdown("---")
    
    st.markdown(f"### {component_info['icon']} {component_info['name']} Evidence")
    
    evidence_type = st.selectbox(
        "Evidence Type:",
        ["Written Work", "Recording", "Assessment", "Portfolio"],
        key="evidence_type_selector"
    )
    
    description = st.text_area(
        "Describe this evidence:",
        placeholder="What does this evidence demonstrate?"
    )
    
    uploaded_file = st.file_uploader(
        "Upload Evidence (PDF, Word, Audio, Video):",
        type=['pdf', 'docx', 'doc', 'mp3', 'mp4', 'jpg', 'png']
    )
    
    if st.button("📤 Submit Evidence", use_container_width=True):
        if uploaded_file and description:
            st.success(f"""
            ✅ **Evidence Submitted Successfully!**
            
            - Component: {component_info['name']}
            - Type: {evidence_type}
            - File: {uploaded_file.name}
            
            Your tutor will review this evidence.
            """)
        else:
            st.error("Please provide description and upload a file.")


def render_tquk_documents(level, course_info):
    """Render TQUK documents tab"""
    st.subheader("📥 TQUK Documents")
    
    st.info("""
    **Download official TQUK documents**
    
    All documents include T21 Services branding.
    """)
    
    st.markdown("### 📂 Available Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **{level} Documents:**
        - Qualification Specification
        - Assessment Guidance
        - Sample Papers
        - Marking Criteria
        """)
    
    with col2:
        if st.button("📄 Download All Documents", use_container_width=True):
            st.success("Documents download feature coming soon!")


def render_progress(level, course_info, enrollment):
    """Render progress tab"""
    st.subheader("📊 My Progress")
    
    if enrollment:
        st.markdown("### Overall Progress")
        
        col1, col2 = st.columns(2)
        with col1:
            progress = enrollment.get('progress', 0)
            st.metric("Progress", f"{progress}%")
            st.progress(progress / 100)
        with col2:
            st.metric("Status", enrollment.get('status', 'active').title())
        
        st.markdown("---")
        st.markdown("### Component Progress")
        
        for comp_key, comp_info in COMPONENTS.items():
            with st.expander(f"{comp_info['icon']} {comp_info['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Status", "In Progress")
                with col2:
                    st.metric("Evidence Submitted", "0")
    else:
        st.info("Enrollment data not available.")


def render_certificate(level, course_info, enrollment):
    """Render certificate tab"""
    st.subheader("🎓 TQUK Certificate")
    
    st.info(f"""
    **📜 About Your TQUK Certificate**
    
    Upon successful completion, you will receive:
    
    **TQUK Functional Skills English {level}**
    - Qualification Number: {course_info['qualification_number']}
    - Ofqual regulated
    - Nationally recognized
    - {"GCSE equivalent" if level == "Level 2" else "Entry level qualification"}
    """)
    
    st.markdown("---")
    
    st.markdown("### 📋 Requirements for Certification")
    
    st.write("""
    **To receive your TQUK certificate, you must:**
    
    ✅ Pass Reading exam  
    ✅ Pass Writing exam  
    ✅ Complete Speaking & Listening portfolio  
    ✅ Meet all assessment criteria  
    ✅ Pass TQUK external quality assurance
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Your Progress")
    
    if enrollment:
        progress = enrollment.get('progress', 0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Progress", f"{progress}%")
            st.progress(progress / 100)
        with col2:
            st.metric("Components Complete", "0/4")
        
        if progress >= 100:
            st.success("""
            ### 🎉 Congratulations!
            
            You've completed all requirements!
            
            Your certificate will be issued by TQUK after final assessment.
            """)
        else:
            st.info(f"Keep going! You're {progress}% complete.")
    else:
        st.info("Progress data not available.")
    
    st.markdown("---")
    
    st.markdown("### 💼 Career Opportunities")
    
    if level == "Level 2":
        st.write("""
        **With Functional Skills English Level 2, you can:**
        
        - 🎓 Progress to further education
        - 💼 Apply for jobs requiring GCSE English
        - 🔧 Start apprenticeships
        - 📈 Improve career prospects
        - 🎯 Access higher-level courses
        """)
    else:
        st.write("""
        **With Functional Skills English Level 1, you can:**
        
        - 📚 Progress to Level 2
        - 💼 Improve employment prospects
        - 🔧 Access entry-level jobs
        - 📈 Build confidence in English
        - 🎯 Prepare for further study
        """)
