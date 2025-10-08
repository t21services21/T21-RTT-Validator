"""
T21 LMS - COURSE REVIEWS & RATINGS SYSTEM
Allow students to rate and review courses

Features:
- 5-star rating system
- Written reviews
- Verified completion badges
- Helpful/not helpful votes
- Review moderation
- Average rating calculation
"""

import json
import os
from datetime import datetime
from database_schema import generate_id, load_db, save_db


REVIEWS_DB = "lms_reviews.json"


def add_review(user_email, user_name, course_id, rating, review_text, verified_completion=False):
    """Add a course review"""
    
    reviews = load_db(REVIEWS_DB)
    
    # Check if user already reviewed this course
    for review_id, review in reviews.items():
        if review['user_email'] == user_email and review['course_id'] == course_id:
            # Update existing review
            review['rating'] = rating
            review['review_text'] = review_text
            review['updated_at'] = datetime.now().isoformat()
            save_db(REVIEWS_DB, reviews)
            return review_id
    
    # Create new review
    review_id = generate_id("REV")
    
    review = {
        'review_id': review_id,
        'user_email': user_email,
        'user_name': user_name,
        'course_id': course_id,
        'rating': rating,
        'review_text': review_text,
        'verified_completion': verified_completion,
        'helpful_votes': 0,
        'not_helpful_votes': 0,
        'approved': True,  # Auto-approve for now
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    reviews[review_id] = review
    save_db(REVIEWS_DB, reviews)
    
    # Update course average rating
    update_course_rating(course_id)
    
    return review_id


def get_course_reviews(course_id, approved_only=True):
    """Get all reviews for a course"""
    
    reviews = load_db(REVIEWS_DB)
    
    course_reviews = []
    for review_id, review in reviews.items():
        if review['course_id'] == course_id:
            if not approved_only or review.get('approved', True):
                course_reviews.append(review)
    
    # Sort by date (newest first)
    course_reviews.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return course_reviews


def get_user_review(user_email, course_id):
    """Get a user's review for a specific course"""
    
    reviews = load_db(REVIEWS_DB)
    
    for review_id, review in reviews.items():
        if review['user_email'] == user_email and review['course_id'] == course_id:
            return review
    
    return None


def vote_helpful(review_id, helpful=True):
    """Vote on whether a review was helpful"""
    
    reviews = load_db(REVIEWS_DB)
    
    if review_id in reviews:
        if helpful:
            reviews[review_id]['helpful_votes'] += 1
        else:
            reviews[review_id]['not_helpful_votes'] += 1
        
        save_db(REVIEWS_DB, reviews)
        return True
    
    return False


def update_course_rating(course_id):
    """Update course average rating and total reviews"""
    
    from lms_course_manager import update_course
    
    reviews = get_course_reviews(course_id)
    
    if reviews:
        total_rating = sum(r['rating'] for r in reviews)
        average_rating = total_rating / len(reviews)
        
        update_course(course_id, {
            'average_rating': round(average_rating, 1),
            'total_reviews': len(reviews)
        })
    else:
        update_course(course_id, {
            'average_rating': 0,
            'total_reviews': 0
        })


def get_rating_distribution(course_id):
    """Get rating distribution for a course"""
    
    reviews = get_course_reviews(course_id)
    
    distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    
    for review in reviews:
        rating = review['rating']
        distribution[rating] += 1
    
    # Convert to percentages
    total = len(reviews)
    if total > 0:
        for rating in distribution:
            distribution[rating] = int((distribution[rating] / total) * 100)
    
    return distribution


def moderate_review(review_id, approved):
    """Approve or reject a review (admin function)"""
    
    reviews = load_db(REVIEWS_DB)
    
    if review_id in reviews:
        reviews[review_id]['approved'] = approved
        save_db(REVIEWS_DB, reviews)
        
        # Update course rating
        course_id = reviews[review_id]['course_id']
        update_course_rating(course_id)
        
        return True
    
    return False


def delete_review(review_id):
    """Delete a review"""
    
    reviews = load_db(REVIEWS_DB)
    
    if review_id in reviews:
        course_id = reviews[review_id]['course_id']
        del reviews[review_id]
        save_db(REVIEWS_DB, reviews)
        
        # Update course rating
        update_course_rating(course_id)
        
        return True
    
    return False
