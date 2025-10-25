"""
STUDENT PROGRESS TRACKER - COMPETITIVE ADVANTAGE

Real-time progress tracking for students and admins
Shows completion %, time spent, achievements, next steps
Makes platform feel premium and engaging
"""

import streamlit as st
from datetime import datetime, timedelta
from supabase_database import supabase, get_user_modules
import json

def calculate_student_progress(student_email):
    """Calculate comprehensive student progress"""
    
    try:
        # Get student's modules
        modules = get_user_modules(student_email)
        
        # Get usage data
        result = supabase.table('users').select('*').eq('email', student_email).execute()
        if not result.data:
            return None
        
        user = result.data[0]
        
        # Calculate progress metrics
        progress = {
            'overall_completion': 0,
            'modules_accessed': 0,
            'total_modules': len(modules) if modules else 0,
            'time_spent_hours': 0,
            'last_activity': None,
            'achievements': [],
            'next_steps': [],
            'streak_days': 0,
            'completion_by_category': {}
        }
        
        # Get activity logs (if available)
        try:
            activity_result = supabase.table('user_activity').select('*').eq('user_email', student_email).execute()
            activities = activity_result.data if activity_result.data else []
            
            if activities:
                # Calculate time spent
                total_minutes = sum([a.get('duration_minutes', 0) for a in activities])
                progress['time_spent_hours'] = round(total_minutes / 60, 1)
                
                # Last activity
                if activities:
                    latest = max(activities, key=lambda x: x.get('timestamp', ''))
                    progress['last_activity'] = latest.get('timestamp')
                
                # Calculate streak
                progress['streak_days'] = calculate_streak(activities)
        except:
            pass
        
        # Calculate module completion
        if modules:
            # Check which modules have been accessed
            accessed_modules = set([a.get('module_name') for a in activities if a.get('module_name')])
            progress['modules_accessed'] = len(accessed_modules)
            
            # Overall completion
            if progress['total_modules'] > 0:
                progress['overall_completion'] = round((progress['modules_accessed'] / progress['total_modules']) * 100)
        
        # Achievements
        progress['achievements'] = calculate_achievements(progress, activities)
        
        # Next steps
        progress['next_steps'] = generate_next_steps(progress, modules, activities)
        
        return progress
        
    except Exception as e:
        st.error(f"Error calculating progress: {e}")
        return None


def calculate_streak(activities):
    """Calculate consecutive days of activity"""
    if not activities:
        return 0
    
    # Get unique dates
    dates = set()
    for activity in activities:
        try:
            timestamp = activity.get('timestamp', '')
            date = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).date()
            dates.add(date)
        except:
            continue
    
    if not dates:
        return 0
    
    # Sort dates
    sorted_dates = sorted(dates, reverse=True)
    
    # Calculate streak
    streak = 1
    today = datetime.now().date()
    
    # Check if active today or yesterday
    if sorted_dates[0] not in [today, today - timedelta(days=1)]:
        return 0
    
    for i in range(len(sorted_dates) - 1):
        diff = (sorted_dates[i] - sorted_dates[i + 1]).days
        if diff == 1:
            streak += 1
        else:
            break
    
    return streak


def calculate_achievements(progress, activities):
    """Calculate student achievements"""
    achievements = []
    
    # First login
    if activities:
        achievements.append({
            'icon': '🎉',
            'title': 'Welcome!',
            'description': 'Started your learning journey'
        })
    
    # Module milestones
    if progress['modules_accessed'] >= 1:
        achievements.append({
            'icon': '📚',
            'title': 'First Module',
            'description': 'Accessed your first module'
        })
    
    if progress['modules_accessed'] >= 3:
        achievements.append({
            'icon': '🎓',
            'title': 'Getting Started',
            'description': 'Accessed 3 modules'
        })
    
    if progress['modules_accessed'] >= 5:
        achievements.append({
            'icon': '⭐',
            'title': 'Active Learner',
            'description': 'Accessed 5 modules'
        })
    
    # Time spent milestones
    if progress['time_spent_hours'] >= 1:
        achievements.append({
            'icon': '⏰',
            'title': 'First Hour',
            'description': 'Spent 1 hour learning'
        })
    
    if progress['time_spent_hours'] >= 10:
        achievements.append({
            'icon': '💪',
            'title': 'Dedicated',
            'description': 'Spent 10 hours learning'
        })
    
    # Streak achievements
    if progress['streak_days'] >= 3:
        achievements.append({
            'icon': '🔥',
            'title': '3-Day Streak',
            'description': 'Logged in 3 days in a row'
        })
    
    if progress['streak_days'] >= 7:
        achievements.append({
            'icon': '🏆',
            'title': 'Week Warrior',
            'description': '7-day learning streak'
        })
    
    return achievements


def generate_next_steps(progress, modules, activities):
    """Generate personalized next steps"""
    next_steps = []
    
    # If no activity yet
    if not activities:
        next_steps.append({
            'icon': '🚀',
            'title': 'Start Learning',
            'description': 'Access your first module',
            'action': 'Go to Learning Portal'
        })
        return next_steps
    
    # If not all modules accessed
    if progress['modules_accessed'] < progress['total_modules']:
        unaccessed = progress['total_modules'] - progress['modules_accessed']
        next_steps.append({
            'icon': '📖',
            'title': 'Explore More',
            'description': f'You have {unaccessed} modules to explore',
            'action': 'Browse available modules'
        })
    
    # If low activity
    if progress['time_spent_hours'] < 5:
        next_steps.append({
            'icon': '💡',
            'title': 'Keep Learning',
            'description': 'Spend more time with the materials',
            'action': 'Continue your course'
        })
    
    # If streak broken
    if progress['streak_days'] == 0 and activities:
        next_steps.append({
            'icon': '🔄',
            'title': 'Get Back On Track',
            'description': 'Start a new learning streak',
            'action': 'Login daily'
        })
    
    # Career development
    if 'CV Builder' in modules and 'CV Builder' not in [a.get('module_name', '') for a in activities]:
        next_steps.append({
            'icon': '📄',
            'title': 'Build Your CV',
            'description': 'Create a professional CV',
            'action': 'Go to CV Builder'
        })
    
    return next_steps


def render_student_progress_dashboard(student_email=None):
    """Render progress dashboard for student or admin"""
    
    # If no email provided, use current user
    if not student_email:
        student_email = st.session_state.get('user_email')
    
    if not student_email:
        st.error("No student email provided")
        return
    
    st.markdown("# 📊 Progress Dashboard")
    
    # Calculate progress
    with st.spinner("Loading progress..."):
        progress = calculate_student_progress(student_email)
    
    if not progress:
        st.warning("No progress data available yet")
        return
    
    # Overall progress card
    st.markdown("## 🎯 Overall Progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Completion",
            f"{progress['overall_completion']}%",
            help="Percentage of modules accessed"
        )
    
    with col2:
        st.metric(
            "Modules Accessed",
            f"{progress['modules_accessed']}/{progress['total_modules']}",
            help="Number of modules you've explored"
        )
    
    with col3:
        st.metric(
            "Time Spent",
            f"{progress['time_spent_hours']}h",
            help="Total hours spent learning"
        )
    
    with col4:
        streak_label = f"{progress['streak_days']} days" if progress['streak_days'] > 0 else "Start today!"
        st.metric(
            "Streak 🔥",
            streak_label,
            help="Consecutive days of activity"
        )
    
    # Progress bar
    st.progress(progress['overall_completion'] / 100)
    
    st.markdown("---")
    
    # Achievements
    if progress['achievements']:
        st.markdown("## 🏆 Achievements")
        
        cols = st.columns(3)
        for idx, achievement in enumerate(progress['achievements']):
            with cols[idx % 3]:
                st.info(f"""
                {achievement['icon']} **{achievement['title']}**
                
                {achievement['description']}
                """)
    
    st.markdown("---")
    
    # Next steps
    if progress['next_steps']:
        st.markdown("## 🎯 Next Steps")
        
        for step in progress['next_steps']:
            with st.expander(f"{step['icon']} {step['title']}"):
                st.write(step['description'])
                st.info(f"**Action:** {step['action']}")
    
    st.markdown("---")
    
    # Activity timeline
    st.markdown("## 📅 Recent Activity")
    
    if progress['last_activity']:
        try:
            last_activity_date = datetime.fromisoformat(progress['last_activity'].replace('Z', '+00:00'))
            st.success(f"Last active: {last_activity_date.strftime('%B %d, %Y at %I:%M %p')}")
        except:
            st.info("Activity tracking enabled")
    else:
        st.info("No recent activity recorded")


def render_admin_progress_overview():
    """Admin view of all student progress"""
    
    st.markdown("# 📊 Student Progress Overview")
    
    st.info("See how all students are progressing")
    
    # Get all students
    try:
        result = supabase.table('users').select('*').eq('user_type', 'student').execute()
        students = result.data if result.data else []
    except Exception as e:
        st.error(f"Error loading students: {e}")
        return
    
    if not students:
        st.warning("No students found")
        return
    
    # Calculate progress for all
    student_progress = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, student in enumerate(students):
        status_text.text(f"Loading progress... {idx + 1}/{len(students)}")
        progress_bar.progress((idx + 1) / len(students))
        
        email = student.get('email')
        name = student.get('full_name')
        
        progress = calculate_student_progress(email)
        
        if progress:
            student_progress.append({
                'name': name,
                'email': email,
                'completion': progress['overall_completion'],
                'modules_accessed': progress['modules_accessed'],
                'total_modules': progress['total_modules'],
                'time_spent': progress['time_spent_hours'],
                'streak': progress['streak_days'],
                'last_activity': progress['last_activity']
            })
    
    progress_bar.empty()
    status_text.empty()
    
    # Summary stats
    if student_progress:
        avg_completion = sum([s['completion'] for s in student_progress]) / len(student_progress)
        total_time = sum([s['time_spent'] for s in student_progress])
        active_students = len([s for s in student_progress if s['streak'] > 0])
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Avg Completion", f"{round(avg_completion)}%")
        col2.metric("Total Learning Time", f"{round(total_time)}h")
        col3.metric("Active Students", f"{active_students}/{len(student_progress)}")
        col4.metric("Total Students", len(student_progress))
    
    st.markdown("---")
    
    # Student list
    st.markdown("### Student Progress")
    
    # Sort options
    sort_by = st.selectbox(
        "Sort by:",
        ["Completion %", "Time Spent", "Streak", "Name"]
    )
    
    if sort_by == "Completion %":
        student_progress.sort(key=lambda x: x['completion'], reverse=True)
    elif sort_by == "Time Spent":
        student_progress.sort(key=lambda x: x['time_spent'], reverse=True)
    elif sort_by == "Streak":
        student_progress.sort(key=lambda x: x['streak'], reverse=True)
    else:
        student_progress.sort(key=lambda x: x['name'])
    
    # Display students
    for student in student_progress:
        with st.expander(f"👤 {student['name']} - {student['completion']}% complete"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.progress(student['completion'] / 100)
                st.write(f"**Modules:** {student['modules_accessed']}/{student['total_modules']}")
                st.write(f"**Time Spent:** {student['time_spent']} hours")
                st.write(f"**Streak:** {student['streak']} days {'🔥' if student['streak'] > 0 else ''}")
                
                if student['last_activity']:
                    try:
                        last_active = datetime.fromisoformat(student['last_activity'].replace('Z', '+00:00'))
                        st.write(f"**Last Active:** {last_active.strftime('%B %d, %Y')}")
                    except:
                        pass
            
            with col2:
                if st.button("View Details", key=f"view_{student['email']}"):
                    st.session_state['view_progress_student'] = student['email']
                    st.rerun()
