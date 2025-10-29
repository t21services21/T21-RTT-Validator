"""
CONTENT GENERATOR
AI-powered content generation for courses, labs, and questions

Features:
- Generate video scripts
- Create lab scenarios
- Generate exam questions
- Create course outlines
"""

import streamlit as st
from datetime import datetime

class ContentGenerator:
    """
    AI-powered content generation system
    """
    
    def generate_video_script(self, topic, duration_minutes=15):
        """Generate video script for a topic"""
        
        script_template = f"""
# VIDEO SCRIPT: {topic}
Duration: {duration_minutes} minutes

## INTRODUCTION (2 minutes)
- Welcome students
- Overview of what they'll learn
- Why this topic matters

## MAIN CONTENT ({duration_minutes-4} minutes)
- Key concept 1
- Key concept 2
- Key concept 3
- Real-world examples
- Demonstrations

## CONCLUSION (2 minutes)
- Summary of key points
- What's next
- Call to action

## TALKING POINTS:

[00:00-02:00] Introduction
"Welcome to this lesson on {topic}. In the next {duration_minutes} minutes, 
you'll learn..."

[02:00-{duration_minutes-2}:00] Main Content
"Let's start with the fundamentals..."

[{duration_minutes-2}:00-{duration_minutes}:00] Conclusion
"To summarize what we've covered today..."

## VISUAL AIDS NEEDED:
- Slide 1: Title slide
- Slide 2: Key concepts overview
- Slide 3-5: Detailed explanations
- Slide 6: Summary

## RESOURCES TO MENTION:
- Documentation links
- Practice labs
- Additional reading

## QUIZ QUESTIONS (for end of video):
1. What is {topic}?
2. Why is {topic} important?
3. How do you implement {topic}?
"""
        
        return script_template
    
    def generate_lab_scenario(self, lab_name, difficulty, category):
        """Generate lab scenario"""
        
        scenario_template = f"""
# LAB: {lab_name}
Category: {category}
Difficulty: {difficulty}

## LEARNING OBJECTIVES:
- Objective 1
- Objective 2
- Objective 3

## SCENARIO:
You are a SOC analyst investigating...

## ENVIRONMENT:
- VM: Ubuntu 22.04
- Tools available: [list tools]
- Network: 10.0.0.0/24

## TASKS:
1. Task 1 description
2. Task 2 description
3. Task 3 description

## HINTS:
- Hint 1: Try using [tool]
- Hint 2: Check [location]
- Hint 3: Look for [pattern]

## FLAG:
flag{{{lab_name.lower().replace(' ', '_')}_completed}}

## SOLUTION:
Step 1: [command]
Step 2: [command]
Step 3: [command]

## LEARNING POINTS:
- Point 1
- Point 2
- Point 3
"""
        
        return scenario_template
    
    def generate_exam_questions(self, topic, num_questions=10):
        """Generate exam questions"""
        
        questions_template = f"""
# EXAM QUESTIONS: {topic}
Generated: {datetime.now().strftime('%Y-%m-%d')}

## Question 1
**Question:** What is {topic}?
**Options:**
A) Option 1
B) Option 2
C) Option 3
D) Option 4
**Correct:** A
**Explanation:** Explanation here

## Question 2
**Question:** Why is {topic} important?
**Options:**
A) Option 1
B) Option 2
C) Option 3
D) Option 4
**Correct:** B
**Explanation:** Explanation here

[Generate {num_questions-2} more questions...]

## Question {num_questions}
**Question:** How do you implement {topic}?
**Options:**
A) Option 1
B) Option 2
C) Option 3
D) Option 4
**Correct:** C
**Explanation:** Explanation here
"""
        
        return questions_template
    
    def generate_course_outline(self, course_name, level, weeks):
        """Generate complete course outline"""
        
        outline_template = f"""
# COURSE OUTLINE: {course_name}
Level: {level}
Duration: {weeks} weeks

## WEEK 1: Introduction
### Module 1.1: Course Overview
- Video: Welcome & Introduction (15 min)
- Reading: Course syllabus
- Quiz: Pre-assessment

### Module 1.2: Fundamentals
- Video: Core concepts (20 min)
- Lab: Hands-on introduction
- Quiz: Fundamentals check

## WEEK 2: Deep Dive
### Module 2.1: Advanced Concepts
- Video: Advanced topics (25 min)
- Reading: Best practices
- Lab: Practical application

### Module 2.2: Real-World Applications
- Video: Case studies (20 min)
- Lab: Complex scenario
- Quiz: Week 2 assessment

[Continue for {weeks} weeks...]

## FINAL WEEK: Certification
### Module {weeks}.1: Review
- Video: Course recap (30 min)
- Practice exam
- Study materials

### Module {weeks}.2: Certification Exam
- Final exam (2 hours)
- Certificate generation
- Next steps

## TOTAL CONTENT:
- Videos: {weeks * 4} videos
- Labs: {weeks * 2} labs
- Quizzes: {weeks * 2} quizzes
- Final exam: 1
"""
        
        return outline_template

# Content generator instance
content_gen = ContentGenerator()

def render_content_generator_ui():
    """Render content generator interface"""
    
    st.title("🎬 Content Generator")
    
    st.markdown("""
    Use AI to help generate course content, lab scenarios, and exam questions.
    
    **What you can generate:**
    - 📹 Video scripts
    - 🔬 Lab scenarios
    - 📝 Exam questions
    - 📚 Course outlines
    """)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📹 Video Scripts",
        "🔬 Lab Scenarios",
        "📝 Exam Questions",
        "📚 Course Outlines"
    ])
    
    with tab1:
        st.subheader("Generate Video Script")
        
        topic = st.text_input("Topic", "Introduction to Cybersecurity")
        duration = st.slider("Duration (minutes)", 5, 60, 15)
        
        if st.button("🎬 Generate Script"):
            script = content_gen.generate_video_script(topic, duration)
            st.code(script, language="markdown")
            
            st.download_button(
                "📥 Download Script",
                script,
                file_name=f"script_{topic.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
    
    with tab2:
        st.subheader("Generate Lab Scenario")
        
        lab_name = st.text_input("Lab Name", "Linux Privilege Escalation")
        category = st.selectbox("Category", ["Linux", "Network", "Web", "Malware", "Forensics"])
        difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced", "Expert"])
        
        if st.button("🔬 Generate Lab"):
            scenario = content_gen.generate_lab_scenario(lab_name, difficulty, category)
            st.code(scenario, language="markdown")
            
            st.download_button(
                "📥 Download Scenario",
                scenario,
                file_name=f"lab_{lab_name.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
    
    with tab3:
        st.subheader("Generate Exam Questions")
        
        exam_topic = st.text_input("Topic", "Network Security")
        num_questions = st.number_input("Number of Questions", 5, 50, 10)
        
        if st.button("📝 Generate Questions"):
            questions = content_gen.generate_exam_questions(exam_topic, num_questions)
            st.code(questions, language="markdown")
            
            st.download_button(
                "📥 Download Questions",
                questions,
                file_name=f"questions_{exam_topic.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
    
    with tab4:
        st.subheader("Generate Course Outline")
        
        course_name = st.text_input("Course Name", "SOC Analyst Foundation")
        level = st.selectbox("Level", ["Foundation", "Professional", "Expert"])
        weeks = st.number_input("Duration (weeks)", 4, 20, 8)
        
        if st.button("📚 Generate Outline"):
            outline = content_gen.generate_course_outline(course_name, level, weeks)
            st.code(outline, language="markdown")
            
            st.download_button(
                "📥 Download Outline",
                outline,
                file_name=f"outline_{course_name.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    render_content_generator_ui()
