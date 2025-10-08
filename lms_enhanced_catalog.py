"""
T21 LMS - ENHANCED COURSE CATALOG
Professional course browsing with categories, search, and filters

Features:
- Beautiful course cards with thumbnails
- Advanced search and filters
- Category browsing
- Sort options (popular, newest, rating, price)
- Course preview
- Instructor profiles
"""

import streamlit as st
from lms_course_manager import get_all_courses, get_course
from lms_student_portal import enroll_student, get_student_progress
from datetime import datetime


# Course categories with icons
COURSE_CATEGORIES = {
    "All": "📚",
    "RTT Training": "🏥",
    "Hospital Administration": "🏢",
    "Clinical Skills": "⚕️",
    "Leadership & Management": "👔",
    "Compliance & Legal": "⚖️",
    "IT & Technology": "💻"
}

# Difficulty levels with colors
DIFFICULTY_LEVELS = {
    "All": "",
    "Beginner": "🟢",
    "Intermediate": "🟡",
    "Advanced": "🟠",
    "Expert": "🔴"
}


def render_enhanced_catalog(user_email, user_role):
    """Render the enhanced course catalog"""
    
    st.header("📚 Course Catalog")
    st.markdown("**Explore our comprehensive training courses**")
    
    # Search bar
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search courses",
            placeholder="Search by title, description, or instructor...",
            label_visibility="collapsed"
        )
    
    with col2:
        view_type = st.selectbox(
            "View",
            ["Grid View 📱", "List View 📋"],
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_category = st.selectbox(
            "Category",
            list(COURSE_CATEGORIES.keys())
        )
    
    with col2:
        selected_level = st.selectbox(
            "Level",
            list(DIFFICULTY_LEVELS.keys())
        )
    
    with col3:
        price_filter = st.selectbox(
            "Price",
            ["All", "Free", "Paid"]
        )
    
    with col4:
        sort_by = st.selectbox(
            "Sort By",
            ["Newest", "Popular", "Highest Rated", "Price: Low to High", "Price: High to Low"]
        )
    
    st.markdown("---")
    
    # Get all published courses
    courses = get_all_courses(status='published')
    
    # Apply filters
    filtered_courses = filter_courses(
        courses, 
        search_query, 
        selected_category, 
        selected_level, 
        price_filter
    )
    
    # Sort courses
    sorted_courses = sort_courses(filtered_courses, sort_by)
    
    # Display results count
    st.markdown(f"**{len(sorted_courses)} courses found**")
    
    if not sorted_courses:
        st.info("No courses match your criteria. Try adjusting your filters!")
        return
    
    # Display courses
    if "Grid" in view_type:
        render_grid_view(sorted_courses, user_email)
    else:
        render_list_view(sorted_courses, user_email)


def filter_courses(courses, query, category, level, price):
    """Apply filters to course list"""
    filtered = []
    
    for course in courses:
        # Search filter
        if query:
            query_lower = query.lower()
            if not (
                query_lower in course['title'].lower() or
                query_lower in course['description'].lower() or
                query_lower in course['instructor'].lower()
            ):
                continue
        
        # Category filter
        if category != "All" and course['category'] != category:
            continue
        
        # Level filter
        if level != "All" and course['level'] != level:
            continue
        
        # Price filter
        if price == "Free" and course['price'] > 0:
            continue
        if price == "Paid" and course['price'] == 0:
            continue
        
        filtered.append(course)
    
    return filtered


def sort_courses(courses, sort_by):
    """Sort courses based on criteria"""
    if sort_by == "Newest":
        return sorted(courses, key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_by == "Popular":
        return sorted(courses, key=lambda x: x.get('total_enrollments', 0), reverse=True)
    elif sort_by == "Highest Rated":
        return sorted(courses, key=lambda x: x.get('average_rating', 0), reverse=True)
    elif sort_by == "Price: Low to High":
        return sorted(courses, key=lambda x: x.get('price', 0))
    elif sort_by == "Price: High to Low":
        return sorted(courses, key=lambda x: x.get('price', 0), reverse=True)
    
    return courses


def render_grid_view(courses, user_email):
    """Render courses in grid layout"""
    
    # Display in rows of 3
    for i in range(0, len(courses), 3):
        cols = st.columns(3)
        
        for j in range(3):
            if i + j < len(courses):
                course = courses[i + j]
                
                with cols[j]:
                    render_course_card(course, user_email)


def render_list_view(courses, user_email):
    """Render courses in list layout"""
    
    for course in courses:
        render_course_list_item(course, user_email)
        st.markdown("---")


def render_course_card(course, user_email):
    """Render a single course card"""
    
    with st.container():
        # Course thumbnail
        if course.get('thumbnail'):
            st.image(course['thumbnail'], use_container_width=True)
        else:
            # Placeholder with category icon
            category_icon = COURSE_CATEGORIES.get(course['category'], "📚")
            st.markdown(
                f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 60px; text-align: center; border-radius: 8px; color: white; font-size: 48px;'>
                {category_icon}
                </div>""",
                unsafe_allow_html=True
            )
        
        # Course title
        st.markdown(f"### {course['title']}")
        
        # Instructor
        st.caption(f"👤 {course['instructor']}")
        
        # Rating (if available)
        rating = course.get('average_rating', 0)
        if rating > 0:
            stars = "⭐" * int(rating)
            st.caption(f"{stars} {rating:.1f}")
        
        # Level badge
        level_icon = DIFFICULTY_LEVELS.get(course['level'], "")
        st.caption(f"{level_icon} {course['level']}")
        
        # Price
        if course['price'] > 0:
            st.markdown(f"**£{course['price']}**")
        else:
            st.success("**FREE**")
        
        # Enroll button
        progress = get_student_progress(user_email, course['course_id'])
        
        if progress:
            st.success("✅ Enrolled")
            if st.button("▶️ Continue", key=f"card_continue_{course['course_id']}"):
                st.session_state.viewing_course = course['course_id']
                st.rerun()
        else:
            if st.button("📚 Enroll Now", key=f"card_enroll_{course['course_id']}", type="primary"):
                success, message = enroll_student(user_email, course['course_id'])
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # Preview button
        if st.button("👁️ Preview", key=f"card_preview_{course['course_id']}"):
            st.session_state.preview_course = course['course_id']
            st.rerun()


def render_course_list_item(course, user_email):
    """Render a single course in list view"""
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # Thumbnail
        if course.get('thumbnail'):
            st.image(course['thumbnail'], use_container_width=True)
        else:
            category_icon = COURSE_CATEGORIES.get(course['category'], "📚")
            st.markdown(
                f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 40px; text-align: center; border-radius: 8px; color: white; font-size: 36px;'>
                {category_icon}
                </div>""",
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown(f"### {course['title']}")
        st.caption(f"👤 {course['instructor']} | 📚 {course['category']} | {DIFFICULTY_LEVELS.get(course['level'], '')} {course['level']}")
        
        # Rating
        rating = course.get('average_rating', 0)
        if rating > 0:
            stars = "⭐" * int(rating)
            st.caption(f"{stars} {rating:.1f} ({course.get('total_reviews', 0)} reviews)")
        
        # Description (truncated)
        description = course['description'][:150] + "..." if len(course['description']) > 150 else course['description']
        st.markdown(description)
        
        # Course info
        st.caption(f"⏱️ {course['duration_hours']} hours | 📝 {course['total_lessons']} lessons")
    
    with col3:
        # Price
        if course['price'] > 0:
            st.markdown(f"### £{course['price']}")
        else:
            st.success("### FREE")
        
        # Enroll button
        progress = get_student_progress(user_email, course['course_id'])
        
        if progress:
            st.success("✅ Enrolled")
            completion = progress.get('completion_percentage', 0)
            st.progress(completion / 100)
            st.caption(f"{completion}% complete")
            
            if st.button("▶️ Continue", key=f"list_continue_{course['course_id']}"):
                st.session_state.viewing_course = course['course_id']
                st.rerun()
        else:
            if st.button("📚 Enroll", key=f"list_enroll_{course['course_id']}", type="primary"):
                success, message = enroll_student(user_email, course['course_id'])
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        if st.button("👁️ Preview", key=f"list_preview_{course['course_id']}"):
            st.session_state.preview_course = course['course_id']
            st.rerun()


def render_category_browser():
    """Render category browser"""
    
    st.subheader("📚 Browse by Category")
    
    cols = st.columns(3)
    
    for idx, (category, icon) in enumerate(COURSE_CATEGORIES.items()):
        if category == "All":
            continue
        
        with cols[idx % 3]:
            courses = get_all_courses(status='published', category=category)
            
            if st.button(
                f"{icon} {category}\n{len(courses)} courses",
                key=f"cat_{category}",
                use_container_width=True
            ):
                st.session_state.selected_category = category
                st.rerun()
