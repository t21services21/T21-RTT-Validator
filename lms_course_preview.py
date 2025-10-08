"""
T21 LMS - COURSE PREVIEW SYSTEM
Allow students to preview courses before enrolling

Features:
- Course overview
- Preview video
- Course outline
- Instructor bio
- Reviews preview
- What you'll learn
- Course requirements
"""

import streamlit as st
from lms_course_manager import get_course, get_lessons_for_course
from lms_student_portal import enroll_student, get_student_progress
from lms_reviews_ui import render_compact_reviews


def render_course_preview(course_id, user_email):
    """Render course preview modal/page"""
    
    course = get_course(course_id)
    
    if not course:
        st.error("Course not found")
        return
    
    # Back button
    if st.button("⬅️ Back to Catalog"):
        if 'preview_course' in st.session_state:
            del st.session_state.preview_course
        st.rerun()
    
    st.markdown("---")
    
    # Course header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title(course['title'])
        st.markdown(f"**{course['description']}**")
        
        # Course meta
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Duration", f"{course['duration_hours']} hours")
        
        with col_b:
            st.metric("Lessons", course['total_lessons'])
        
        with col_c:
            level_icons = {
                "Beginner": "🟢",
                "Intermediate": "🟡",
                "Advanced": "🟠",
                "Expert": "🔴"
            }
            icon = level_icons.get(course['level'], "")
            st.metric("Level", f"{icon} {course['level']}")
        
        # Rating
        rating = course.get('average_rating', 0)
        if rating > 0:
            stars = "⭐" * int(rating)
            reviews = course.get('total_reviews', 0)
            st.markdown(f"### {stars} {rating:.1f} ({reviews} reviews)")
    
    with col2:
        # Price & Enroll
        st.markdown("### Price")
        if course['price'] > 0:
            st.markdown(f"# £{course['price']}")
        else:
            st.success("# FREE")
        
        # Check if enrolled
        progress = get_student_progress(user_email, course_id)
        
        if progress:
            st.success("✅ Already Enrolled")
            completion = progress.get('completion_percentage', 0)
            st.progress(completion / 100)
            st.caption(f"{completion}% complete")
            
            if st.button("▶️ Go to Course", type="primary", use_container_width=True):
                st.session_state.viewing_course = course_id
                del st.session_state.preview_course
                st.rerun()
        else:
            if st.button("📚 Enroll Now", type="primary", use_container_width=True):
                success, message = enroll_student(user_email, course_id)
                if success:
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)
        
        # Course info
        st.markdown("---")
        st.markdown("**This course includes:**")
        st.markdown(f"- ⏱️ {course['duration_hours']} hours of content")
        st.markdown(f"- 📝 {course['total_lessons']} lessons")
        st.markdown(f"- 📋 {course['total_quizzes']} quizzes")
        if course.get('certificate_enabled'):
            st.markdown("- 🏆 Certificate of completion")
        st.markdown("- 📱 Access on mobile and desktop")
        st.markdown("- ♾️ Lifetime access")
    
    st.markdown("---")
    
    # Preview video (if available)
    if course.get('preview_video_url'):
        st.subheader("📹 Course Preview")
        st.video(course['preview_video_url'])
        st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Course Content",
        "👤 Instructor",
        "⭐ Reviews",
        "ℹ️ About"
    ])
    
    with tab1:
        render_course_outline(course_id)
    
    with tab2:
        render_instructor_bio(course)
    
    with tab3:
        render_course_reviews(course_id)
    
    with tab4:
        render_course_about(course)


def render_course_outline(course_id):
    """Render course content outline"""
    
    st.subheader("📚 Course Content")
    
    lessons = get_lessons_for_course(course_id)
    
    if not lessons:
        st.info("Course content will be available soon")
        return
    
    # Group lessons by module
    modules = {}
    for lesson in lessons:
        module = lesson.get('module_id', 'default')
        if module not in modules:
            modules[module] = []
        modules[module].append(lesson)
    
    # Display modules
    for module_name, module_lessons in modules.items():
        with st.expander(f"📂 {module_name.title()} ({len(module_lessons)} lessons)", expanded=True):
            for idx, lesson in enumerate(module_lessons, 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    # Lesson icon based on type
                    icons = {
                        'video': '🎥',
                        'text': '📄',
                        'pdf': '📑',
                        'quiz': '❓',
                        'interactive': '🎮'
                    }
                    icon = icons.get(lesson['content_type'], '📝')
                    
                    # Free preview indicator
                    free_tag = " 🆓" if lesson.get('is_free', False) else ""
                    
                    st.markdown(f"{idx}. {icon} {lesson['title']}{free_tag}")
                
                with col2:
                    st.caption(f"⏱️ {lesson['duration_minutes']} min")
                
                with col3:
                    if lesson.get('is_free', False):
                        if st.button("▶️", key=f"preview_lesson_{lesson['lesson_id']}"):
                            st.session_state.preview_lesson = lesson['lesson_id']
                            st.rerun()


def render_instructor_bio(course):
    """Render instructor information"""
    
    st.subheader("👤 About the Instructor")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Instructor photo placeholder
        st.markdown(
            """<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 60px; text-align: center; border-radius: 50%; color: white; font-size: 48px;'>
            👤
            </div>""",
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(f"### {course['instructor']}")
        st.caption(f"Instructor | {course['category']}")
        
        # Instructor stats
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Courses", "1")  # TODO: Count actual courses
        
        with col_b:
            st.metric("Students", "0")  # TODO: Count actual students
        
        with col_c:
            st.metric("Rating", "4.8 ⭐")  # TODO: Calculate actual rating
    
    st.markdown("---")
    
    # Instructor bio
    st.markdown("""
    **Bio:**
    
    Experienced healthcare professional with expertise in RTT validation, 
    hospital administration, and clinical training.
    
    **Qualifications:**
    - MSc in Healthcare Management
    - Certified RTT Specialist
    - 10+ years NHS experience
    
    **Specializations:**
    - RTT Pathway Management
    - Hospital Operations
    - Staff Training & Development
    """)


def render_course_reviews(course_id):
    """Render course reviews"""
    
    st.subheader("⭐ Student Reviews")
    
    # Use the actual review system
    render_compact_reviews(course_id, limit=5)


def render_course_about(course):
    """Render course about/details"""
    
    st.subheader("ℹ️ Course Details")
    
    # What you'll learn
    st.markdown("### 📚 What You'll Learn")
    st.markdown(f"""
    {course['description']}
    
    **By the end of this course, you will be able to:**
    - Understand RTT pathway requirements
    - Validate patient pathways effectively
    - Identify and resolve common issues
    - Use validation tools confidently
    - Apply RTT rules correctly
    """)
    
    st.markdown("---")
    
    # Requirements
    st.markdown("### 📋 Requirements")
    st.markdown("""
    - Basic understanding of NHS processes
    - Access to a computer or tablet
    - Internet connection
    - Willingness to learn!
    """)
    
    st.markdown("---")
    
    # Who this course is for
    st.markdown("### 👥 Who This Course Is For")
    st.markdown("""
    - NHS Staff working with RTT
    - Healthcare Administrators
    - RTT Coordinators
    - Validation Officers
    - Anyone interested in RTT training
    """)
