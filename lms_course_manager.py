"""
T21 LMS - COURSE MANAGEMENT SYSTEM
Create and manage courses, modules, and lessons

Features:
- Create/edit/delete courses
- Add modules and lessons
- Upload content (videos, PDFs)
- Set prerequisites
- Pricing tiers
- Publish/unpublish courses
"""

import streamlit as st
from database_schema import (
    Course, Lesson, load_db, save_db, generate_id,
    COURSES_DB, LESSONS_DB
)
from datetime import datetime


# ============================================
# COURSE CRUD OPERATIONS
# ============================================

def create_course(title, description, instructor, category, level, duration_hours, price, required_role):
    """Create a new course"""
    courses = load_db(COURSES_DB)
    
    course = Course(
        title=title,
        description=description,
        instructor=instructor,
        category=category,
        level=level,
        duration_hours=duration_hours,
        price=price,
        required_role=required_role
    )
    
    courses[course.course_id] = course.to_dict()
    save_db(COURSES_DB, courses)
    
    return course.course_id


def get_course(course_id):
    """Get course by ID"""
    courses = load_db(COURSES_DB)
    return courses.get(course_id)


def get_all_courses(status=None, category=None):
    """Get all courses with optional filters"""
    courses = load_db(COURSES_DB)
    
    filtered = []
    for course_id, course in courses.items():
        if status and course.get('status') != status:
            continue
        if category and course.get('category') != category:
            continue
        filtered.append(course)
    
    return filtered


def update_course(course_id, updates):
    """Update course details"""
    courses = load_db(COURSES_DB)
    
    if course_id in courses:
        courses[course_id].update(updates)
        courses[course_id]['updated_at'] = datetime.now().isoformat()
        save_db(COURSES_DB, courses)
        return True
    
    return False


def publish_course(course_id):
    """Publish a course"""
    return update_course(course_id, {'status': 'published'})


def unpublish_course(course_id):
    """Unpublish a course"""
    return update_course(course_id, {'status': 'draft'})


def delete_course(course_id):
    """Delete a course"""
    courses = load_db(COURSES_DB)
    
    if course_id in courses:
        del courses[course_id]
        save_db(COURSES_DB, courses)
        
        # Also delete associated lessons
        lessons = load_db(LESSONS_DB)
        lessons = {lid: l for lid, l in lessons.items() if l.get('course_id') != course_id}
        save_db(LESSONS_DB, lessons)
        
        return True
    
    return False


# ============================================
# LESSON CRUD OPERATIONS
# ============================================

def create_lesson(course_id, module_id, title, description, content_type, content='', video_url='', pdf_url='', duration_minutes=0, order=0):
    """Create a new lesson"""
    lessons = load_db(LESSONS_DB)
    
    lesson = Lesson(
        course_id=course_id,
        module_id=module_id,
        title=title,
        description=description,
        content_type=content_type,
        content=content,
        video_url=video_url,
        pdf_url=pdf_url,
        duration_minutes=duration_minutes,
        order=order
    )
    
    lessons[lesson.lesson_id] = lesson.to_dict()
    save_db(LESSONS_DB, lessons)
    
    # Update course total lessons count
    courses = load_db(COURSES_DB)
    if course_id in courses:
        courses[course_id]['total_lessons'] = courses[course_id].get('total_lessons', 0) + 1
        save_db(COURSES_DB, courses)
    
    return lesson.lesson_id


def get_lessons_for_course(course_id):
    """Get all lessons for a course"""
    lessons = load_db(LESSONS_DB)
    
    course_lessons = []
    for lesson_id, lesson in lessons.items():
        if lesson.get('course_id') == course_id:
            course_lessons.append(lesson)
    
    # Sort by order
    course_lessons.sort(key=lambda x: x.get('order', 0))
    
    return course_lessons


def update_lesson(lesson_id, updates):
    """Update lesson details"""
    lessons = load_db(LESSONS_DB)
    
    if lesson_id in lessons:
        lessons[lesson_id].update(updates)
        save_db(LESSONS_DB, lessons)
        return True
    
    return False


def delete_lesson(lesson_id):
    """Delete a lesson"""
    lessons = load_db(LESSONS_DB)
    
    if lesson_id in lessons:
        course_id = lessons[lesson_id].get('course_id')
        del lessons[lesson_id]
        save_db(LESSONS_DB, lessons)
        
        # Update course total lessons count
        courses = load_db(COURSES_DB)
        if course_id in courses:
            courses[course_id]['total_lessons'] = max(0, courses[course_id].get('total_lessons', 1) - 1)
            save_db(COURSES_DB, courses)
        
        return True
    
    return False


# ============================================
# ADMIN UI FOR COURSE MANAGEMENT
# ============================================

def render_course_manager_ui():
    """Render the course management interface for instructors/admins"""
    
    st.header("📚 Course Management System")
    st.markdown("**Create and manage your LMS courses**")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 My Courses", "➕ Create Course", "📝 Manage Lessons"])
    
    with tab1:
        render_courses_list()
    
    with tab2:
        render_create_course()
    
    with tab3:
        render_lesson_manager()


def render_courses_list():
    """Display list of all courses"""
    st.subheader("All Courses")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status:",
            ["All", "Published", "Draft", "Archived"]
        )
    
    with col2:
        category_filter = st.selectbox(
            "Filter by Category:",
            ["All", "RTT Training", "Clinical Skills", "Admin", "Leadership", "Compliance"]
        )
    
    # Get courses
    status = None if status_filter == "All" else status_filter.lower()
    category = None if category_filter == "All" else category_filter
    
    courses = get_all_courses(status=status, category=category)
    
    if not courses:
        st.info("No courses found. Create your first course!")
    else:
        st.markdown(f"**Total courses:** {len(courses)}")
        
        # Display courses
        for course in courses:
            with st.expander(f"📚 {course['title']} ({course['status'].upper()})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Category:** {course['category']}")
                    st.markdown(f"**Level:** {course['level']}")
                    st.markdown(f"**Duration:** {course['duration_hours']} hours")
                    st.markdown(f"**Lessons:** {course['total_lessons']}")
                    st.markdown(f"**Description:** {course['description']}")
                
                with col2:
                    if course['status'] == 'draft':
                        if st.button("✅ Publish", key=f"pub_{course['course_id']}"):
                            publish_course(course['course_id'])
                            st.success("Published!")
                            st.rerun()
                    else:
                        if st.button("📝 Unpublish", key=f"unpub_{course['course_id']}"):
                            unpublish_course(course['course_id'])
                            st.success("Unpublished!")
                            st.rerun()
                    
                    if st.button("🗑️ Delete", key=f"del_{course['course_id']}"):
                        delete_course(course['course_id'])
                        st.success("Deleted!")
                        st.rerun()


def render_create_course():
    """Form to create a new course"""
    st.subheader("Create New Course")
    
    with st.form("create_course_form"):
        title = st.text_input("Course Title*", placeholder="e.g., RTT Pathway Mastery")
        
        description = st.text_area(
            "Course Description*",
            placeholder="Describe what students will learn...",
            height=150
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            instructor = st.text_input("Instructor Name*", placeholder="Your name")
            
            category = st.selectbox(
                "Category*",
                ["RTT Training", "Clinical Skills", "Admin", "Leadership", "Compliance", "IT Skills"]
            )
            
            level = st.selectbox(
                "Level*",
                ["Beginner", "Intermediate", "Advanced", "Expert"]
            )
        
        with col2:
            duration_hours = st.number_input("Duration (hours)*", min_value=0, value=10)
            
            price = st.number_input("Price (£)*", min_value=0, value=0)
            
            required_role = st.selectbox(
                "Required Role*",
                ["trial", "basic", "professional", "ultimate"]
            )
        
        submitted = st.form_submit_button("📚 Create Course", type="primary")
        
        if submitted:
            if not title or not description or not instructor:
                st.error("Please fill all required fields (*)")
            else:
                course_id = create_course(
                    title=title,
                    description=description,
                    instructor=instructor,
                    category=category,
                    level=level,
                    duration_hours=duration_hours,
                    price=price,
                    required_role=required_role
                )
                
                st.success(f"✅ Course created successfully! ID: {course_id}")
                st.balloons()
                st.info("Now add lessons to your course in the 'Manage Lessons' tab!")


def render_lesson_manager():
    """Manage lessons for courses"""
    st.subheader("Manage Lessons")
    
    # Select course
    courses = get_all_courses()
    
    if not courses:
        st.warning("Create a course first before adding lessons!")
        return
    
    course_options = {c['title']: c['course_id'] for c in courses}
    selected_course_title = st.selectbox("Select Course:", list(course_options.keys()))
    selected_course_id = course_options[selected_course_title]
    
    # Display existing lessons
    st.markdown("---")
    st.markdown("### 📝 Existing Lessons")
    
    lessons = get_lessons_for_course(selected_course_id)
    
    if lessons:
        for idx, lesson in enumerate(lessons, 1):
            with st.expander(f"Lesson {idx}: {lesson['title']}"):
                st.markdown(f"**Type:** {lesson['content_type']}")
                st.markdown(f"**Duration:** {lesson['duration_minutes']} minutes")
                st.markdown(f"**Description:** {lesson['description']}")
                
                if st.button("🗑️ Delete Lesson", key=f"del_lesson_{lesson['lesson_id']}"):
                    delete_lesson(lesson['lesson_id'])
                    st.success("Lesson deleted!")
                    st.rerun()
    else:
        st.info("No lessons yet. Add your first lesson below!")
    
    # Add new lesson
    st.markdown("---")
    st.markdown("### ➕ Add New Lesson")
    
    with st.form("add_lesson_form"):
        lesson_title = st.text_input("Lesson Title*", placeholder="e.g., Introduction to RTT")
        
        lesson_description = st.text_area(
            "Lesson Description",
            placeholder="Brief description of this lesson...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            content_type = st.selectbox(
                "Content Type*",
                ["text", "video", "pdf", "quiz", "interactive"]
            )
            
            duration = st.number_input("Duration (minutes)*", min_value=1, value=15)
        
        with col2:
            module_name = st.text_input("Module Name", placeholder="e.g., Week 1")
            
            order = st.number_input("Lesson Order", min_value=1, value=len(lessons) + 1)
        
        # Content based on type
        if content_type == "text":
            content = st.text_area("Lesson Content (Markdown supported)*", height=200)
        elif content_type == "video":
            video_url = st.text_input("Video URL (YouTube, Vimeo)*", placeholder="https://youtube.com/watch?v=...")
            content = st.text_area("Additional Notes", height=100)
        elif content_type == "pdf":
            pdf_url = st.text_input("PDF URL*", placeholder="https://...")
            content = st.text_area("PDF Description", height=100)
        else:
            content = st.text_area("Lesson Content*", height=200)
        
        submit_lesson = st.form_submit_button("📝 Add Lesson", type="primary")
        
        if submit_lesson:
            if not lesson_title:
                st.error("Please enter a lesson title")
            else:
                lesson_id = create_lesson(
                    course_id=selected_course_id,
                    module_id=module_name or "default",
                    title=lesson_title,
                    description=lesson_description,
                    content_type=content_type,
                    content=content if content_type != "video" else "",
                    video_url=video_url if content_type == "video" else "",
                    pdf_url=pdf_url if content_type == "pdf" else "",
                    duration_minutes=duration,
                    order=order
                )
                
                st.success(f"✅ Lesson added successfully!")
                st.rerun()
