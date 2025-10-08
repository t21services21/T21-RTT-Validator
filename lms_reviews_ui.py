"""
T21 LMS - COURSE REVIEWS UI
Student interface for submitting and viewing reviews

Features:
- Submit reviews with ratings
- View all course reviews
- Rating distribution
- Helpful votes
"""

import streamlit as st
from lms_reviews import (
    add_review, get_course_reviews, get_user_review,
    get_rating_distribution, vote_helpful
)
from datetime import datetime


def render_review_section(course_id, course_title, user_email, user_name):
    """Render the review section for a course"""
    
    st.subheader("⭐ Course Reviews")
    
    # Import here to avoid circular import
    from lms_student_portal import get_student_progress
    
    # Check if user completed the course
    progress = get_student_progress(user_email, course_id)
    is_enrolled = progress is not None
    is_completed = progress and progress.get('status') == 'completed'
    
    # Get user's existing review
    user_review = get_user_review(user_email, course_id)
    
    # Submit/Edit Review Form
    if is_enrolled:
        with st.expander("✍️ Write a Review" if not user_review else "✏️ Edit Your Review", expanded=not user_review):
            
            if user_review:
                st.info("You've already reviewed this course. You can update your review below.")
                default_rating = user_review['rating']
                default_text = user_review['review_text']
            else:
                default_rating = 5
                default_text = ""
            
            # Rating
            rating = st.select_slider(
                "Rating:",
                options=[1, 2, 3, 4, 5],
                value=default_rating,
                format_func=lambda x: "⭐" * x
            )
            
            # Review text
            review_text = st.text_area(
                "Your Review:",
                value=default_text,
                placeholder="Share your experience with this course...",
                height=150
            )
            
            # Submit button
            if st.button("📝 Submit Review" if not user_review else "💾 Update Review", type="primary"):
                if not review_text.strip():
                    st.error("Please write a review")
                else:
                    review_id = add_review(
                        user_email=user_email,
                        user_name=user_name,
                        course_id=course_id,
                        rating=rating,
                        review_text=review_text,
                        verified_completion=is_completed
                    )
                    
                    if user_review:
                        st.success("✅ Review updated successfully!")
                    else:
                        st.success("✅ Review submitted successfully!")
                        st.balloons()
                    
                    st.rerun()
    else:
        st.info("📚 Enroll in this course to leave a review!")
    
    st.markdown("---")
    
    # Get all reviews
    reviews = get_course_reviews(course_id)
    
    if not reviews:
        st.info("No reviews yet. Be the first to review this course!")
        return
    
    # Rating Summary
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Average rating
        total_rating = sum(r['rating'] for r in reviews)
        avg_rating = total_rating / len(reviews)
        
        st.markdown(f"### {avg_rating:.1f} ⭐")
        st.caption(f"{len(reviews)} reviews")
    
    with col2:
        # Rating distribution
        st.markdown("**Rating Distribution:**")
        distribution = get_rating_distribution(course_id)
        
        for stars in range(5, 0, -1):
            percentage = distribution.get(stars, 0)
            stars_display = "⭐" * stars
            
            col_a, col_b = st.columns([1, 4])
            with col_a:
                st.caption(stars_display)
            with col_b:
                st.progress(percentage / 100)
                st.caption(f"{percentage}%")
    
    st.markdown("---")
    
    # Display reviews
    for review in reviews:
        render_single_review(review)


def render_single_review(review):
    """Render a single review"""
    
    with st.container():
        # Reviewer info
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"**{review['user_name']}**")
            if review.get('verified_completion'):
                st.caption("✅ Completed")
        
        with col2:
            # Rating
            stars = "⭐" * review['rating']
            st.markdown(stars)
            
            # Date
            created = datetime.fromisoformat(review['created_at'])
            days_ago = (datetime.now() - created).days
            
            if days_ago == 0:
                time_str = "Today"
            elif days_ago == 1:
                time_str = "Yesterday"
            elif days_ago < 7:
                time_str = f"{days_ago} days ago"
            elif days_ago < 30:
                weeks = days_ago // 7
                time_str = f"{weeks} week{'s' if weeks > 1 else ''} ago"
            else:
                months = days_ago // 30
                time_str = f"{months} month{'s' if months > 1 else ''} ago"
            
            st.caption(time_str)
        
        # Review text
        st.markdown(review['review_text'])
        
        # Helpful votes
        helpful = review.get('helpful_votes', 0)
        not_helpful = review.get('not_helpful_votes', 0)
        
        col_a, col_b = st.columns([1, 4])
        
        with col_a:
            if helpful > 0:
                st.caption(f"👍 {helpful} helpful")
        
        st.markdown("---")


def render_compact_reviews(course_id, limit=3):
    """Render compact review preview for course preview page"""
    
    reviews = get_course_reviews(course_id)
    
    if not reviews:
        st.info("No reviews yet")
        return
    
    # Show top reviews
    for review in reviews[:limit]:
        col1, col2 = st.columns([1, 5])
        
        with col1:
            st.markdown(f"**{review['user_name'][:1]}***")
        
        with col2:
            stars = "⭐" * review['rating']
            st.markdown(stars)
            
            # Truncate long reviews
            text = review['review_text']
            if len(text) > 200:
                text = text[:200] + "..."
            
            st.caption(text)
        
        st.markdown("---")
    
    if len(reviews) > limit:
        st.caption(f"+ {len(reviews) - limit} more reviews")
