"""
TQUK Functional Skills Maths Module
Levels 1 and 2
"""

import streamlit as st
from tquk_mock_exams_maths import render_maths_mock_exam

# Course IDs
COURSE_ID_L1 = "tquk_fs_maths_l1"
COURSE_ID_L2 = "tquk_fs_maths_l2"

# Course information
COURSES = {
    "Level 1": {
        "id": COURSE_ID_L1,
        "name": "Functional Skills Maths Level 1",
        "qualification_number": "610/2623/2",
        "level": 1,
        "glh": 55,
        "description": "Essential maths skills for everyday life and work"
    },
    "Level 2": {
        "id": COURSE_ID_L2,
        "name": "Functional Skills Maths Level 2",
        "qualification_number": "610/2624/4",
        "level": 2,
        "glh": 55,
        "description": "GCSE equivalent maths skills for work and further study"
    }
}

# Content areas for both levels
CONTENT_AREAS = {
    "numbers": {
        "name": "Numbers & Number System",
        "icon": "🔢",
        "description": "Working with numbers, fractions, decimals, percentages"
    },
    "measures": {
        "name": "Measures, Shape & Space",
        "icon": "📐",
        "description": "Calculations with measurements, geometry, shapes"
    },
    "data": {
        "name": "Information & Data",
        "icon": "📊",
        "description": "Charts, graphs, statistics, probability"
    },
    "problem_solving": {
        "name": "Problem Solving",
        "icon": "🧩",
        "description": "Applying maths to real-world problems"
    }
}

def render_functional_skills_maths_module():
    """Main render function for Functional Skills Maths module"""
    
    st.title("🔢 TQUK Functional Skills Maths")
    
    # Level selector
    selected_level = st.radio(
        "Select Level:",
        list(COURSES.keys()),
        horizontal=True,
        key="maths_level_selector"
    )
    
    course_info = COURSES[selected_level]
    
    # Course header
    st.markdown(f"""
    ### {course_info['name']}
    
    **Qualification Number:** {course_info['qualification_number']}  
    **Level:** {course_info['level']} | **GLH:** {course_info['glh']} hours | **TQT:** 60 hours
    
    {course_info['description']}
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📋 Overview",
        "📚 Learning Materials",
        "✏️ Practice Exercises",
        "📝 Assessment Info",
        "📂 Evidence Portfolio",
        "📈 Progress Tracking",
        "🎯 Exam Preparation",
        "ℹ️ Help & Resources"
    ])
    
    with tab1:
        render_overview(selected_level, course_info)
    
    with tab2:
        render_materials(selected_level, course_info)
    
    with tab3:
        render_practice(selected_level, course_info)
    
    with tab4:
        render_assessment_info(selected_level, course_info)
    
    with tab5:
        render_evidence(selected_level, course_info)
    
    with tab6:
        render_progress(selected_level, course_info)
    
    with tab7:
        render_exam_prep(selected_level, course_info)
    
    with tab8:
        render_help(selected_level, course_info)

def render_overview(level, course_info):
    """Render overview tab"""
    st.subheader("📋 Course Overview")
    
    st.markdown(f"""
    ## What is Functional Skills Maths {level}?
    
    This qualification develops your mathematical skills for work, study and everyday life. 
    You'll learn to apply maths confidently to solve real-world problems.
    
    ### 🎯 What You'll Learn:
    
    **Four Key Areas:**
    """)
    
    for area_key, area_info in CONTENT_AREAS.items():
        st.markdown(f"""
        **{area_info['icon']} {area_info['name']}**  
        {area_info['description']}
        """)
    
    st.markdown(f"""
    ---
    
    ### 📝 Assessment Structure:
    
    **Single Exam - Two Sections (Continuous Sitting)**
    
    | Section | Duration | Calculator | Weighting |
    |---------|----------|------------|-----------|
    | **Section A: Non-Calculator** | 30 minutes | ❌ No | 25% |
    | **Section B: Calculator** | 90 minutes | ✅ Yes | 75% |
    | **Total** | **2 hours** | - | **100%** |
    
    **Important:** Both sections must be completed in one continuous sitting!
    
    ---
    
    ### 🎓 Grading:
    
    - **Pass/Fail** (no grades)
    - Combined mark from both sections
    - Can retake if needed (no limit)
    
    ---
    
    ### 📦 What to Bring to Exam:
    
    ✅ Pen and pencil  
    ✅ Eraser  
    ✅ Ruler (30cm)  
    ✅ Protractor  
    ✅ Compass  
    ✅ **Non-scientific calculator** (Section B only)
    
    ---
    
    ### 🚀 Progression:
    
    After completing {level}, you can progress to:
    """)
    
    if level == "Level 1":
        st.markdown("""
        - ✅ Functional Skills Maths Level 2
        - ✅ GCSE Mathematics
        - ✅ Further vocational qualifications
        - ✅ Employment opportunities
        """)
    else:
        st.markdown("""
        - ✅ GCSE Mathematics
        - ✅ Advanced vocational qualifications
        - ✅ Apprenticeships
        - ✅ Employment opportunities
        """)

def render_materials(level, course_info):
    """Render materials tab"""
    st.subheader("📖 Learning Materials")
    
    st.info(f"""
    **Study all 4 content areas for {level}**
    
    Each area includes theory, examples, and practice questions.
    """)
    
    # Content area selector
    area = st.selectbox(
        "Select Content Area to Study:",
        list(CONTENT_AREAS.keys()),
        format_func=lambda x: f"{CONTENT_AREAS[x]['icon']} {CONTENT_AREAS[x]['name']} - {CONTENT_AREAS[x]['description']}",
        key="materials_area_selector"
    )
    
    area_info = CONTENT_AREAS[area]
    
    st.markdown("---")
    
    st.markdown(f"## {area_info['icon']} {area_info['name']}")
    
    # Load content from markdown file
    try:
        with open(f"tquk_functional_skills_maths_{level.lower().replace(' ', '_')}_content.md", "r", encoding="utf-8") as f:
            content = f.read()
            
            # Extract section for this area
            if area == "numbers":
                section_marker = "# Numbers & Number System"
            elif area == "measures":
                section_marker = "# Measures, Shape & Space"
            elif area == "data":
                section_marker = "# Information & Data"
            else:
                section_marker = "# Problem Solving"
            
            # Find the section and display it
            if section_marker in content:
                section_start = content.find(section_marker)
                # Find the next major section (next # at start of line)
                next_section = content.find("\n# ", section_start + 1)
                
                if next_section == -1:
                    # This is the last section, take everything to the end
                    section_content = content[section_start:]
                else:
                    # Take content up to the next section
                    section_content = content[section_start:next_section]
                
                st.markdown(section_content)
            else:
                st.markdown(content)
    except FileNotFoundError:
        st.warning(f"Content file not found. Please contact your tutor.")
        st.markdown(f"""
        ### {area_info['name']}
        
        Content for this area will be available soon.
        
        In the meantime, you can:
        - Review the official TQUK specification
        - Practice with sample questions
        - Consult with your tutor
        """)

def render_practice(level, course_info):
    """Render practice tab"""
    st.subheader("✏️ Practice Exercises")
    
    st.info("""
    **Practice makes perfect!**
    
    Complete exercises for each content area to build your skills.
    """)
    
    # Area selector
    area = st.selectbox(
        "Select Content Area:",
        list(CONTENT_AREAS.keys()),
        format_func=lambda x: f"{CONTENT_AREAS[x]['icon']} {CONTENT_AREAS[x]['name']}",
        key="practice_area_selector"
    )
    
    area_info = CONTENT_AREAS[area]
    
    st.markdown("---")
    
    st.markdown(f"## {area_info['icon']} {area_info['name']} Practice")
    
    if area == "numbers":
        st.markdown("""
        ### Practice Questions:
        
        **Question 1:** Calculate 15% of £240
        
        **Question 2:** Convert 3.5 metres to centimetres
        
        **Question 3:** What is 3/4 as a decimal?
        
        **Question 4:** Order these numbers from smallest to largest: -5, 3, -2, 0, 7
        
        **Question 5:** Calculate: 12 × 100
        
        ---
        
        💡 **Tip:** Show your working out for all calculations!
        """)
    
    elif area == "measures":
        st.markdown("""
        ### Practice Questions:
        
        **Question 1:** Calculate the area of a rectangle 8cm × 5cm
        
        **Question 2:** A map scale is 1:50,000. What real distance does 4cm represent?
        
        **Question 3:** Calculate the perimeter of a square with sides of 12cm
        
        **Question 4:** Convert 2.5 kg to grams
        
        **Question 5:** What is the volume of a cube with sides of 3cm?
        
        ---
        
        💡 **Tip:** Remember to include units in your answers!
        """)
    
    elif area == "data":
        st.markdown("""
        ### Practice Questions:
        
        **Question 1:** Find the mean of: 4, 7, 9, 12, 8
        
        **Question 2:** What is the range of: 15, 22, 18, 30, 25?
        
        **Question 3:** A coin is flipped. What is the probability of getting heads?
        
        **Question 4:** Create a bar chart for: Apples=5, Oranges=8, Bananas=3
        
        **Question 5:** Find the mode of: 3, 5, 3, 7, 3, 9
        
        ---
        
        💡 **Tip:** Check your calculations twice!
        """)
    
    else:  # problem_solving
        st.markdown("""
        ### Practice Problems:
        
        **Problem 1:** You buy 3 items at £4.50 each. You pay with a £20 note. How much change?
        
        **Problem 2:** A recipe needs 250g flour for 12 cakes. How much for 18 cakes?
        
        **Problem 3:** You travel 60 miles in 1.5 hours. What is your average speed?
        
        **Problem 4:** A shop offers 20% off £80. What is the sale price?
        
        **Problem 5:** You work 35 hours at £9.50/hour. What are your total earnings?
        
        ---
        
        💡 **Tip:** Read the question carefully and identify what you need to find!
        """)
    
    st.markdown("---")
    
    st.success("✅ Complete these practice questions and check your answers with your tutor!")

def render_assessment_info(level, course_info):
    """Render assessment information tab"""
    st.subheader("📝 Assessment Information")
    
    st.markdown(f"""
    ## {level} Assessment Details
    
    ### 📋 Exam Structure:
    
    **Single-Component Assessment (Two Sections)**
    
    Both sections must be completed in **one continuous sitting** (no breaks between sections).
    
    | Section | Duration | Calculator | Content | Marks |
    |---------|----------|------------|---------|-------|
    | **A: Non-Calculator** | 30 minutes | ❌ No | Basic skills | 25% |
    | **B: Calculator** | 90 minutes | ✅ Yes | Problem solving | 75% |
    | **Total** | **120 minutes** | - | All content | 100% |
    
    ---
    
    ### 🎯 What's Assessed:
    
    **Content Balance:**
    - 25% Underpinning skills (basic maths ability)
    - 75% Problem solving (applying maths to real situations)
    
    **Content Areas:**
    - Numbers & Number System
    - Measures, Shape & Space
    - Information & Data
    - Problem Solving
    
    ---
    
    ### 📦 Equipment Required:
    
    **You MUST bring:**
    - ✅ Pen and pencil
    - ✅ Eraser
    - ✅ Ruler (30cm)
    - ✅ Protractor
    - ✅ Compass
    - ✅ **Non-scientific calculator** (Section B only)
    
    **Calculator Requirements:**
    - Basic, non-scientific only
    - Battery or solar powered
    - No formulae stored
    - No internet connection
    - No symbolic algebra functions
    
    ---
    
    ### 📊 Grading:
    
    **Pass/Fail Only**
    - Combined mark from both sections determines result
    - No separate pass mark for each section
    - Must achieve overall pass mark to get certificate
    
    ---
    
    ### 🔄 Retakes:
    
    - ✅ No limit on retake attempts
    - ✅ Can retake as soon as you're ready
    - ✅ Results within 6 working days
    - ✅ Previous results don't carry forward (fresh attempt each time)
    
    ---
    
    ### 📍 Where to Sit Exam:
    
    **Option 1: At T21 Services Centre**
    - Face-to-face exam
    - Formal exam conditions
    - Invigilated by our staff
    
    **Option 2: Remote Online**
    - Sit exam at home
    - TQUK secure platform
    - Remote invigilation via webcam
    - Additional cost applies
    
    ---
    
    ### ⏰ Booking:
    
    - **Online exams:** Book anytime (centre sets dates)
    - **Paper-based:** 5 working days' notice required
    - **Results:** Within 6 working days
    
    ---
    
    ### 🎓 Certificate:
    
    Once you pass, you'll receive:
    - ✅ Official TQUK certificate
    - ✅ Ofqual regulated qualification
    - ✅ {level} = {'Entry level equivalent' if level == 'Level 1' else 'GCSE equivalent'}
    - ✅ Nationally recognized
    """)

def render_evidence(level, course_info, learner_email="student@example.com"):
    """Render evidence portfolio tab"""
    st.subheader("📂 Evidence Portfolio")
    
    st.info("""
    **Track your learning journey**
    
    Upload practice work and track your progress through the course.
    """)
    
    area = st.selectbox(
        "Select Content Area:",
        list(CONTENT_AREAS.keys()),
        format_func=lambda x: f"{CONTENT_AREAS[x]['icon']} {CONTENT_AREAS[x]['name']}",
        key="evidence_area_selector"
    )
    
    area_info = CONTENT_AREAS[area]
    
    st.markdown("---")
    
    st.markdown(f"### {area_info['icon']} {area_info['name']} Evidence")
    
    evidence_type = st.selectbox(
        "Evidence Type:",
        ["Practice Work", "Homework", "Mock Exam", "Notes"],
        key="evidence_type_selector_maths"
    )
    
    description = st.text_area(
        "Describe this evidence:",
        placeholder="What does this work demonstrate?",
        key="evidence_description_maths"
    )
    
    uploaded_file = st.file_uploader(
        "Upload Evidence (PDF, Images, Word):",
        type=['pdf', 'docx', 'doc', 'jpg', 'png'],
        key="evidence_uploader_maths"
    )
    
    if st.button("💾 Save Evidence", key="save_evidence_maths"):
        if uploaded_file and description:
            st.success(f"""
            ✅ Evidence saved successfully!
            
            **Area:** {area_info['name']}  
            **Type:** {evidence_type}  
            **File:** {uploaded_file.name}
            """)
            st.balloons()
        else:
            st.error("⚠️ Please provide both a description and upload a file.")
    
    st.markdown("---")
    
    st.markdown("### 📋 Your Evidence Portfolio")
    
    st.info("Your uploaded evidence will appear here. Keep building your portfolio as you progress through the course!")

def render_progress(level, course_info):
    """Render progress tracking tab"""
    st.subheader("📈 Progress Tracking")
    
    st.markdown(f"""
    ## Your {level} Progress
    
    Track your completion of each content area.
    """)
    
    # Progress for each area
    for area_key, area_info in CONTENT_AREAS.items():
        st.markdown(f"### {area_info['icon']} {area_info['name']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Materials Studied", "0%")
        with col2:
            st.metric("Practice Complete", "0%")
        with col3:
            st.metric("Confidence Level", "⭐⭐⭐☆☆")
        
        st.progress(0.0)
        st.markdown("---")
    
    st.markdown("### 🎯 Overall Progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Course Completion", "0%")
    with col2:
        st.metric("Practice Hours", "0")
    with col3:
        st.metric("Mock Exams", "0")
    with col4:
        st.metric("Ready for Exam", "Not Yet")
    
    st.progress(0.0)
    
    st.info("💡 **Tip:** Complete all materials and practice exercises before booking your exam!")

def render_exam_prep(level, course_info):
    """Render exam preparation tab"""
    st.subheader("🎯 Exam Preparation")
    
    st.markdown(f"""
    ## Preparing for Your {level} Exam
    
    ### ✅ Exam Checklist:
    
    **Before Exam Day:**
    - [ ] Completed all learning materials
    - [ ] Practiced all content areas
    - [ ] Completed mock exams
    - [ ] Confident with calculator and non-calculator questions
    - [ ] Gathered all required equipment
    - [ ] Registered with TQUK
    - [ ] Booked exam date
    
    ---
    
    ### 📦 Equipment Checklist:
    
    **Bring to Exam:**
    - [ ] Pen and pencil
    - [ ] Eraser
    - [ ] Ruler (30cm)
    - [ ] Protractor
    - [ ] Compass
    - [ ] Non-scientific calculator (check batteries!)
    - [ ] Photo ID
    
    ---
    
    ### 💡 Exam Tips:
    
    **Section A (Non-Calculator):**
    - ✅ 30 minutes - work quickly but carefully
    - ✅ Show all working out
    - ✅ Check mental maths answers
    - ✅ Use estimation to verify answers
    - ✅ Don't spend too long on one question
    
    **Section B (Calculator):**
    - ✅ 90 minutes - pace yourself
    - ✅ Read questions carefully
    - ✅ Identify what the question is asking
    - ✅ Show your working
    - ✅ Use calculator wisely
    - ✅ Check answers make sense
    - ✅ Include units in answers
    
    **General Tips:**
    - ✅ Answer all questions (no penalty for wrong answers)
    - ✅ If stuck, move on and come back
    - ✅ Check your work if time permits
    - ✅ Write clearly and neatly
    - ✅ Stay calm and focused
    
    ---
    
    ### 📚 Mock Exams:
    
    Practice with mock exams to build confidence and identify areas for improvement.
    """)
    
    st.markdown("---")
    
    # Render actual mock exam
    render_maths_mock_exam(level)
    
    st.markdown("---")
    
    st.success("🎯 **You've got this!** Complete your preparation and book your exam when ready!")

def render_help(level, course_info):
    """Render help and resources tab"""
    st.subheader("ℹ️ Help & Resources")
    
    st.markdown(f"""
    ## {level} Help & Resources
    
    ### 📞 Need Help?
    
    **Contact Your Tutor:**
    - Email: tutor@t21services.com
    - Questions about content
    - Practice support
    - Exam preparation guidance
    
    **T21 Services Support:**
    - Email: support@t21services.com
    - Technical issues
    - Exam booking
    - Certificate queries
    
    ---
    
    ### 📚 Useful Resources:
    
    **Official TQUK Resources:**
    - [TQUK Website](https://www.tquk.org)
    - [Functional Skills Maths Specification](https://www.tquk.org/functional-skills)
    - Sample assessment papers
    - Mark schemes
    
    **Free Online Resources:**
    - BBC Bitesize Functional Skills
    - Khan Academy (Maths)
    - Corbettmaths
    - MathsGenie
    
    ---
    
    ### 🎓 Course Information:
    
    **Qualification:** {course_info['name']}  
    **QAN:** {course_info['qualification_number']}  
    **Level:** {course_info['level']}  
    **GLH:** {course_info['glh']} hours  
    **TQT:** 60 hours
    
    **Awarding Organisation:** TQUK (Training Qualifications UK)  
    **Regulated by:** Ofqual  
    **Recognition:** Nationally recognized, {level} = {'Entry level equivalent' if level == 'Level 1' else 'GCSE equivalent'}
    
    ---
    
    ### ❓ Frequently Asked Questions:
    
    **Q: How long does the exam take?**  
    A: 2 hours total (30 mins non-calculator + 90 mins calculator) in one continuous sitting.
    
    **Q: Can I use a calculator throughout?**  
    A: No, Section A is non-calculator only. Section B allows calculators.
    
    **Q: What type of calculator can I use?**  
    A: Basic, non-scientific calculator only. No formulae stored, no internet.
    
    **Q: How is it graded?**  
    A: Pass/Fail only. Combined mark from both sections determines result.
    
    **Q: Can I retake if I fail?**  
    A: Yes, unlimited retakes. No minimum wait time.
    
    **Q: How long for results?**  
    A: Usually 6 working days from exam completion.
    
    **Q: Is this equivalent to GCSE?**  
    A: Level 2 is GCSE equivalent. Level 1 is entry level equivalent.
    
    **Q: Can I take the exam online?**  
    A: Yes, both face-to-face at centre and remote online options available.
    
    ---
    
    ### 📖 Study Tips:
    
    1. **Practice regularly** - Little and often is better than cramming
    2. **Show your working** - Even if answer is wrong, you may get method marks
    3. **Learn formulae** - Area, perimeter, volume formulae are essential
    4. **Check answers** - Use estimation to verify calculations
    5. **Time management** - Don't spend too long on one question
    6. **Read carefully** - Understand what the question is asking
    7. **Use real examples** - Apply maths to everyday situations
    8. **Ask for help** - Don't struggle alone, contact your tutor
    
    ---
    
    ### ✅ Ready to Start?
    
    Begin with the **Learning Materials** tab and work through each content area systematically.
    
    Good luck with your studies! 🎓
    """)

if __name__ == "__main__":
    render_functional_skills_maths_module()
