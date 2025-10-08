"""
T21 LMS - STUDENT PORTAL
Student-facing interface for browsing courses, learning, and tracking progress

Features:
- Browse available courses
- Enroll in courses
- View lessons and content
- Track progress
- Earn certificates
- Resume learning
"""

import streamlit as st
from database_schema import (
    StudentProgress, load_db, save_db, generate_id,
    COURSES_DB, LESSONS_DB, STUDENT_PROGRESS_DB
)
from datetime import datetime, timedelta
from lms_course_manager import get_all_courses, get_lessons_for_course, get_course
from lms_quiz_ui import render_quiz_interface, render_quiz_list_for_course
from lms_reviews_ui import render_review_section
from lms_certificates_ui import render_certificates_gallery, render_certificate_viewer
from lms_certificates import generate_certificate


# ============================================
# STUDENT PROGRESS TRACKING
# ============================================

def enroll_student(user_email, course_id):
    """Enroll a student in a course"""
    progress_db = load_db(STUDENT_PROGRESS_DB)
    
    # Check if already enrolled
    for prog_id, prog in progress_db.items():
        if prog['user_email'] == user_email and prog['course_id'] == course_id:
            return False, "Already enrolled in this course"
    
    # Create progress record
    progress = StudentProgress(
        user_email=user_email,
        course_id=course_id
    )
    
    progress_db[progress.progress_id] = progress.to_dict()
    save_db(STUDENT_PROGRESS_DB, progress_db)
    
    return True, "Enrolled successfully!"


def get_student_progress(user_email, course_id):
    """Get student's progress for a specific course"""
    progress_db = load_db(STUDENT_PROGRESS_DB)
    
    for prog_id, prog in progress_db.items():
        if prog['user_email'] == user_email and prog['course_id'] == course_id:
            return prog
    
    return None


def get_all_student_progress(user_email):
    """Get all courses a student is enrolled in"""
    progress_db = load_db(STUDENT_PROGRESS_DB)
    
    student_courses = []
    for prog_id, prog in progress_db.items():
        if prog['user_email'] == user_email:
            student_courses.append(prog)
    
    return student_courses


def mark_lesson_complete(user_email, course_id, lesson_id):
    """Mark a lesson as completed"""
    progress_db = load_db(STUDENT_PROGRESS_DB)
    
    for prog_id, prog in progress_db.items():
        if prog['user_email'] == user_email and prog['course_id'] == course_id:
            if lesson_id not in prog['completed_lessons']:
                prog['completed_lessons'].append(lesson_id)
                prog['last_lesson'] = lesson_id
                prog['last_accessed'] = datetime.now().isoformat()
                
                # Update completion percentage
                lessons = get_lessons_for_course(course_id)
                total_lessons = len(lessons)
                completed = len(prog['completed_lessons'])
                prog['completion_percentage'] = int((completed / total_lessons * 100)) if total_lessons > 0 else 0
                
                # Check if course completed
                if prog['completion_percentage'] >= 100:
                    prog['status'] = 'completed'
                    prog['certificate_issued'] = True
                    prog['certificate_date'] = datetime.now().isoformat()
                
                save_db(STUDENT_PROGRESS_DB, progress_db)
                return True
    
    return False


def update_time_spent(user_email, course_id, minutes):
    """Update time spent on a course"""
    progress_db = load_db(STUDENT_PROGRESS_DB)
    
    for prog_id, prog in progress_db.items():
        if prog['user_email'] == user_email and prog['course_id'] == course_id:
            prog['time_spent_minutes'] += minutes
            prog['last_accessed'] = datetime.now().isoformat()
            save_db(STUDENT_PROGRESS_DB, progress_db)
            return True
    
    return False


# ============================================
# STUDENT UI
# ============================================

def render_student_lms_portal(user_email, user_role):
    """Render the student LMS portal"""
    
    # Check if viewing a certificate
    if 'viewing_certificate' in st.session_state:
        render_certificate_viewer(st.session_state.viewing_certificate)
        return
    
    # Check if taking a quiz
    if 'active_quiz' in st.session_state:
        render_quiz_interface(st.session_state.active_quiz, user_email)
        
        if st.button("⬅️ Back to Course"):
            del st.session_state.active_quiz
            st.rerun()
        return
    
    st.header("📚 My Learning Portal")
    st.markdown("**Explore courses and continue your learning journey**")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "🏠 My Courses",
        "📖 Continue Learning",
        "🏆 Certificates"
    ])
    
    with tab1:
        render_my_courses(user_email)
    
    with tab2:
        render_continue_learning(user_email)
    
    with tab3:
        render_certificates_gallery(user_email)


def render_my_courses(user_email):
    """Display student's enrolled courses"""
    st.subheader("📚 My Enrolled Courses")
    
    enrolled = get_all_student_progress(user_email)
    
    if not enrolled:
        st.info("You haven't enrolled in any courses yet. Browse courses to get started!")
        return
    
    st.markdown(f"**Total courses:** {len(enrolled)}")
    
    # Display enrolled courses
    for progress in enrolled:
        course = get_course(progress['course_id'])
        
        if not course:
            continue
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"### 📚 {course['title']}")
                st.caption(f"{course['category']} • {course['level']}")
            
            with col2:
                completion = progress['completion_percentage']
                if completion >= 100:
                    st.success(f"✅ {completion}%")
                elif completion >= 50:
                    st.info(f"🔵 {completion}%")
                else:
                    st.warning(f"⚠️ {completion}%")
            
            with col3:
                if st.button("▶️ Continue", key=f"continue_{progress['course_id']}"):
                    st.session_state.viewing_course = progress['course_id']
                    st.rerun()
            
            # Progress bar
            st.progress(completion / 100)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"⏱️ {progress['time_spent_minutes']} minutes spent")
            with col2:
                st.caption(f"📝 {len(progress['completed_lessons'])} lessons completed")
            with col3:
                last_accessed = datetime.fromisoformat(progress['last_accessed'])
                days_ago = (datetime.now() - last_accessed).days
                st.caption(f"🕒 Last accessed {days_ago} days ago")
            
            st.markdown("---")


def render_browse_courses(user_email, user_role):
    """Browse and enroll in available courses"""
    st.subheader("🔍 Browse Available Courses")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.selectbox(
            "Category:",
            ["All", "RTT Training", "Clinical Skills", "Admin", "Leadership", "Compliance"]
        )
    
    with col2:
        level_filter = st.selectbox(
            "Level:",
            ["All", "Beginner", "Intermediate", "Advanced", "Expert"]
        )
    
    # Get published courses
    courses = get_all_courses(status='published')
    
    # Apply filters
    if category_filter != "All":
        courses = [c for c in courses if c['category'] == category_filter]
    
    if level_filter != "All":
        courses = [c for c in courses if c['level'] == level_filter]
    
    if not courses:
        st.info("No courses available matching your criteria.")
        return
    
    st.markdown(f"**{len(courses)} courses found**")
    
    # Display courses
    for course in courses:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"### 📚 {course['title']}")
                st.markdown(f"**Instructor:** {course['instructor']}")
                st.caption(f"{course['category']} • {course['level']} • {course['duration_hours']} hours")
                st.markdown(f"{course['description'][:200]}...")
                
                # Show lessons count
                lessons = get_lessons_for_course(course['course_id'])
                st.caption(f"📝 {len(lessons)} lessons")
            
            with col2:
                if course['price'] > 0:
                    st.markdown(f"**£{course['price']}**")
                else:
                    st.success("**FREE**")
                
                # Check if enrolled
                progress = get_student_progress(user_email, course['course_id'])
                
                if progress:
                    st.success("✅ Enrolled")
                    if st.button("▶️ Start", key=f"start_{course['course_id']}"):
                        st.session_state.viewing_course = course['course_id']
                        st.rerun()
                else:
                    if st.button("📚 Enroll", key=f"enroll_{course['course_id']}", type="primary"):
                        success, message = enroll_student(user_email, course['course_id'])
                        if success:
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)
            
            st.markdown("---")


def render_continue_learning(user_email):
    """Show current lesson and allow student to continue"""
    st.subheader("📖 Continue Learning")
    
    # Check if viewing a specific course
    if 'viewing_course' not in st.session_state:
        st.info("Select a course from 'My Courses' to continue learning!")
        return
    
    course_id = st.session_state.viewing_course
    course = get_course(course_id)
    progress = get_student_progress(user_email, course_id)
    
    if not course or not progress:
        st.error("Course not found or not enrolled")
        return
    
    # Course header
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"## 📚 {course['title']}")
        st.caption(f"Progress: {progress['completion_percentage']}%")
    
    with col2:
        if st.button("⬅️ Back to Courses"):
            del st.session_state.viewing_course
            st.rerun()
    
    st.progress(progress['completion_percentage'] / 100)
    
    # Tabs for course content
    lesson_tab, quiz_tab, review_tab = st.tabs(["📝 Lessons", "❓ Quizzes", "⭐ Reviews"])
    
    with lesson_tab:
        # Get lessons
        lessons = get_lessons_for_course(course_id)
        
        if not lessons:
            st.warning("This course doesn't have any lessons yet.")
        else:
            st.markdown("### 📝 Course Lessons")
            
            for idx, lesson in enumerate(lessons, 1):
                lesson_id = lesson['lesson_id']
                is_completed = lesson_id in progress['completed_lessons']
                
                with st.expander(
                    f"{'✅' if is_completed else '⭕'} Lesson {idx}: {lesson['title']}", 
                    expanded=(not is_completed and idx == 1)
                ):
                    st.markdown(f"**Duration:** {lesson['duration_minutes']} minutes")
                    st.markdown(f"**Description:** {lesson['description']}")
                    
                    # Show content based on type
                    if lesson['content_type'] == 'video':
                        if lesson['video_url']:
                            st.video(lesson['video_url'])
                        st.markdown(lesson['content'])
                    
                    elif lesson['content_type'] == 'pdf':
                        if lesson['pdf_url']:
                            st.markdown(f"📄 [Download PDF]({lesson['pdf_url']})")
                        st.markdown(lesson['content'])
                    
                    elif lesson['content_type'] == 'text':
                        st.markdown(lesson['content'])
                    
                    else:
                        st.markdown(lesson['content'])
                    
                    # Mark complete button
                    if not is_completed:
                        if st.button(f"✅ Mark as Complete", key=f"complete_{lesson_id}"):
                            mark_lesson_complete(user_email, course_id, lesson_id)
                            update_time_spent(user_email, course_id, lesson['duration_minutes'])
                            
                            # Check if course completed and generate certificate
                            updated_progress = get_student_progress(user_email, course_id)
                            if updated_progress['status'] == 'completed' and not updated_progress['certificate_issued']:
                                generate_certificate(
                                    user_email=user_email,
                                    user_name=updated_progress.get('user_name', 'Student'),
                                    course_id=course_id,
                                    course_title=course['title']
                                )
                            
                            st.success("Lesson completed!")
                            st.balloons()
                            st.rerun()
                    else:
                        st.success("✅ Completed")
    
    with quiz_tab:
        render_quiz_list_for_course(course_id, user_email)
    
    with review_tab:
        # Get user info for reviews
        from student_auth import get_student_info
        user_info = get_student_info(user_email)
        user_name = user_info['full_name'] if user_info else "Student"
        
        render_review_section(course_id, course['title'], user_email, user_name)


def render_certificates(user_email):
    """Display earned certificates"""
    st.subheader("🏆 My Certificates")
    
    enrolled = get_all_student_progress(user_email)
    completed = [p for p in enrolled if p['certificate_issued']]
    
    if not completed:
        st.info("Complete courses to earn certificates!")
        return
    
    st.markdown(f"**Certificates earned:** {len(completed)}")
    
    for progress in completed:
        course = get_course(progress['course_id'])
        
        if not course:
            continue
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### 🏆 {course['title']}")
                cert_date = datetime.fromisoformat(progress['certificate_date'])
                st.caption(f"Completed on: {cert_date.strftime('%B %d, %Y')}")
                st.caption(f"Time spent: {progress['time_spent_minutes']} minutes")
            
            with col2:
                if st.button("📄 Download", key=f"cert_{progress['progress_id']}"):
                    st.info("Certificate download feature coming soon!")
            
            st.markdown("---")
