"""
USER ROLE HELPER
Centralized function to check if user has teacher/staff/admin privileges
USE THIS EVERYWHERE to ensure consistent access control
"""

import streamlit as st

def is_privileged_user():
    """
    Check if user has teacher/staff/tester/admin privileges
    
    Returns True if user is:
    - Admin
    - Super Admin
    - Teacher
    - Staff
    - Tester
    - Partner
    
    Returns False if user is:
    - Student (any tier)
    - Trial
    - Unknown
    
    Usage:
        from user_role_helper import is_privileged_user
        
        if is_privileged_user():
            # Show teacher/admin view
            render_teacher_view()
        else:
            # Show student view
            render_student_view()
    """
    
    # Get user information from session state
    user_email = st.session_state.get('user_email', '').lower()
    user_type = st.session_state.get('user_type', 'student')
    user_license = st.session_state.get('user_license')
    user_role = getattr(user_license, 'role', 'student') if user_license else 'student'
    
    # List of privileged roles
    privileged_roles = ['admin', 'super_admin', 'teacher', 'staff', 'tester', 'partner', 'instructor', 'trainer']
    
    # Check if user is privileged
    is_privileged = (
        user_type in privileged_roles or
        user_role in privileged_roles or
        'admin' in user_email or
        'teacher' in user_email or
        'staff' in user_email
    )
    
    return is_privileged


def get_user_role_display():
    """
    Get user role for display purposes
    
    Returns: String representation of user role
    """
    user_type = st.session_state.get('user_type', 'student')
    user_license = st.session_state.get('user_license')
    user_role = getattr(user_license, 'role', 'student') if user_license else 'student'
    
    # Prefer user_type over user_role
    role = user_type if user_type != 'student' else user_role
    
    return role.replace('_', ' ').title()


def is_super_admin():
    """
    Check if user is super admin
    
    Returns True only for super admin
    """
    user_email = st.session_state.get('user_email', '').lower()
    user_type = st.session_state.get('user_type', 'student')
    user_license = st.session_state.get('user_license')
    user_role = getattr(user_license, 'role', 'student') if user_license else 'student'
    
    return (
        user_type == 'super_admin' or
        user_role == 'super_admin' or
        'admin@t21services' in user_email
    )
