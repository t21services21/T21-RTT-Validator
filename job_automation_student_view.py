"""
NHS JOB APPLICATION AUTOMATION - STUDENT VIEW
Complete dashboard for students to track their applications
READ-ONLY: Students can view everything but cannot change settings
Settings are managed by staff only
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Import existing Supabase connection
from supabase_database import supabase, SUPABASE_AVAILABLE

def get_student_stats(student_id):
    """Get student application statistics"""
    try:
        response = supabase.table('student_application_stats').select('*').eq('student_id', student_id).execute()
        if response.data:
            return response.data[0]
        return {
            'total_applications': 0,
            'applications_submitted': 0,
            'interviews_invited': 0,
            'offers_received': 0,
            'overall_success_rate': 0
        }
    except Exception as e:
        return {
            'total_applications': 0,
            'applications_submitted': 0,
            'interviews_invited': 0,
            'offers_received': 0,
            'overall_success_rate': 0
        }

def get_student_applications(student_id):
    """Get all applications for student"""
    try:
        response = supabase.table('applications').select('*, discovered_jobs(*)').eq('student_id', student_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        return []

def get_student_interviews(student_id):
    """Get all interviews for student"""
    try:
        response = supabase.table('interviews').select('*, discovered_jobs(*)').eq('student_id', student_id).order('interview_date', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        return []

def get_student_settings(student_id):
    """Get student automation settings (view only)"""
    try:
        response = supabase.table('student_automation_settings').select('*').eq('student_id', student_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        return None

def job_automation_student_view():
    """Student dashboard - view all their job automation data"""
    
    st.title("💼 My NHS Job Applications")
    st.markdown("**Track all your automated job applications and interviews**")
    
    # Check if Supabase is available
    if not SUPABASE_AVAILABLE or supabase is None:
        st.error("⚠️ Job automation system is currently unavailable.")
        return
    
    # Get student ID from session
    if 'user_id' not in st.session_state:
        st.warning("Please log in to view your job applications")
        return
    
    student_id = st.session_state['user_id']
    
    # Check if student has automation set up by staff
    settings = get_student_settings(student_id)
    
    if not settings:
        st.info("🔒 **Job automation not set up yet**")
        st.markdown("""
        ### Your training provider will set up job automation for you
        
        Once set up, you'll see here:
        - 📊 Your application statistics
        - 📝 All your job applications
        - 🎤 Your interview invitations
        - 🎉 Job offers
        
        **Contact your training provider to get started!**
        """)
        return
    
    # Get student stats
    stats = get_student_stats(student_id)
    
    # Show automation status
    status = settings.get('status', 'unknown')
    if status == 'active':
        st.success("✅ **Job Automation is ACTIVE** - Applications are being submitted automatically!")
    elif status == 'paused':
        st.warning("⏸️ **Job Automation is PAUSED** - Contact your training provider to resume")
    else:
        st.info(f"Status: {status.upper()}")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",
        "📝 My Applications",
        "🎤 My Interviews",
        "⚙️ My Settings"
    ])
    
    # ============================================================================
    # TAB 1: DASHBOARD
    # ============================================================================
    with tab1:
        st.header("📊 Your Job Search Statistics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📬 Applications Submitted",
                stats.get('applications_submitted', 0),
                delta=f"{stats.get('applications_this_week', 0)} this week"
            )
        
        with col2:
            st.metric(
                "🎤 Interview Invitations",
                stats.get('interviews_invited', 0)
            )
        
        with col3:
            st.metric(
                "🎉 Job Offers",
                stats.get('offers_received', 0)
            )
        
        with col4:
            success_rate = stats.get('overall_success_rate', 0) or 0
            st.metric(
                "📈 Success Rate",
                f"{success_rate:.1f}%"
            )
        
        st.markdown("---")
        
        # Recent activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Recent Applications")
            
            recent_apps = get_student_applications(student_id)[:5]
            
            if recent_apps:
                for app in recent_apps:
                    job = app.get('discovered_jobs', {})
                    
                    with st.container():
                        status_emoji = {
                            'submitted': '✅',
                            'queued': '⏳',
                            'processing': '⚙️',
                            'failed': '❌'
                        }.get(app.get('status', 'unknown'), '❓')
                        
                        st.write(f"{status_emoji} **{job.get('title', 'Unknown')}**")
                        st.caption(f"{job.get('trust', 'Unknown')} - {app.get('created_at', 'Unknown')[:10]}")
                        st.divider()
            else:
                st.info("No applications yet. Your training provider will activate automation soon!")
        
        with col2:
            st.subheader("🎤 Upcoming Interviews")
            
            interviews = get_student_interviews(student_id)
            upcoming = [i for i in interviews if i.get('status') in ['scheduled', 'confirmed']][:5]
            
            if upcoming:
                for interview in upcoming:
                    job = interview.get('discovered_jobs', {})
                    
                    with st.container():
                        st.write(f"📅 **{job.get('title', 'Unknown')}**")
                        st.caption(f"{job.get('trust', 'Unknown')} - {interview.get('interview_date', 'TBC')[:10]}")
                        st.divider()
            else:
                st.info("No upcoming interviews yet. Keep applying!")
        
        st.markdown("---")
        
        # Helpful info
        st.info("""
        💡 **What happens automatically:**
        - ✅ System finds matching NHS jobs every 6 hours
        - ✅ AI generates unique supporting information for each job
        - ✅ Applications are submitted to NHS Trac
        - ✅ You receive email notifications
        - ✅ Interview invitations are detected automatically
        
        **You don't need to do anything - just wait for the emails!** 📧
        """)
    
    # ============================================================================
    # TAB 2: MY APPLICATIONS
    # ============================================================================
    with tab2:
        st.header("📝 All My Applications")
        
        applications = get_student_applications(student_id)
        
        if not applications:
            st.info("No applications yet. Your training provider is setting up automation for you!")
        else:
            st.success(f"📊 **{len(applications)}** applications submitted on your behalf!")
            
            # Status filter
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Submitted", "Queued", "Processing", "Failed"]
            )
            
            # Display applications
            for app in applications:
                if status_filter != "All" and app.get('status', '').lower() != status_filter.lower():
                    continue
                
                job = app.get('discovered_jobs', {})
                
                # Status badge
                status = app.get('status', 'unknown')
                if status == 'submitted':
                    status_badge = "✅ SUBMITTED"
                    status_color = "green"
                elif status == 'queued':
                    status_badge = "⏳ QUEUED"
                    status_color = "blue"
                elif status == 'processing':
                    status_badge = "⚙️ PROCESSING"
                    status_color = "orange"
                elif status == 'failed':
                    status_badge = "❌ FAILED"
                    status_color = "red"
                else:
                    status_badge = "❓ UNKNOWN"
                    status_color = "gray"
                
                with st.expander(f"📄 {job.get('title', 'Unknown')} - {status_badge}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Trust:** {job.get('trust', 'Unknown')}")
                        st.write(f"**Location:** {job.get('location', 'Not specified')}")
                        st.write(f"**Band:** {job.get('band', 'Not specified')}")
                        st.write(f"**Salary:** £{job.get('salary_min', 0):,.0f} - £{job.get('salary_max', 0):,.0f}")
                        st.write(f"**Applied:** {app.get('created_at', 'Unknown')[:10]}")
                        
                        if app.get('submitted_at'):
                            st.write(f"**Submitted:** {app.get('submitted_at')[:10]}")
                        
                        if app.get('confirmation_number'):
                            st.success(f"✅ **Confirmation:** {app.get('confirmation_number')}")
                    
                    with col2:
                        st.markdown(f"**Status:**")
                        if status == 'submitted':
                            st.success(status_badge)
                        elif status == 'failed':
                            st.error(status_badge)
                        else:
                            st.info(status_badge)
                        
                        if job.get('nhs_jobs_url'):
                            st.link_button("🔗 View Job", job.get('nhs_jobs_url'), use_container_width=True)
                    
                    # Show AI-generated supporting information
                    if app.get('ai_supporting_information'):
                        st.markdown("---")
                        with st.expander("📄 View Supporting Information"):
                            st.text_area(
                                "AI-Generated Content (submitted on your behalf)",
                                app.get('ai_supporting_information'),
                                height=200,
                                disabled=True
                            )
                            st.caption(f"Generated in {app.get('ai_generation_time', 0):.1f} seconds | {app.get('ai_word_count', 0)} words")
    
    # ============================================================================
    # TAB 3: MY INTERVIEWS
    # ============================================================================
    with tab3:
        st.header("🎤 My Interviews")
        
        interviews = get_student_interviews(student_id)
        
        if not interviews:
            st.info("No interviews yet. Keep applying - they're coming! 🚀")
        else:
            st.success(f"🎉 **{len(interviews)}** interview invitation(s)!")
            
            for interview in interviews:
                job = interview.get('discovered_jobs', {})
                
                # Status badge
                status = interview.get('status', 'unknown')
                if status == 'scheduled':
                    status_badge = "📅 SCHEDULED"
                elif status == 'confirmed':
                    status_badge = "✅ CONFIRMED"
                elif status == 'completed':
                    status_badge = "✅ COMPLETED"
                else:
                    status_badge = f"📍 {status.upper()}"
                
                with st.expander(f"🎤 {job.get('title', 'Unknown')} - {status_badge}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Trust:** {job.get('trust', 'Unknown')}")
                        st.write(f"**Date:** {interview.get('interview_date', 'TBC')[:10] if interview.get('interview_date') else 'TBC'}")
                        st.write(f"**Time:** {interview.get('interview_time', 'TBC')}")
                        st.write(f"**Location:** {interview.get('interview_location', 'TBC')}")
                        st.write(f"**Address:** {interview.get('interview_address', 'TBC')}")
                        st.write(f"**Format:** {interview.get('interview_format', 'Not specified')}")
                        
                        if interview.get('outcome'):
                            if interview.get('outcome') == 'offered':
                                st.success(f"🎉 **OUTCOME:** Job Offer Received!")
                            elif interview.get('outcome') == 'rejected':
                                st.info(f"**OUTCOME:** Not successful this time")
                            else:
                                st.info(f"**OUTCOME:** {interview.get('outcome')}")
                    
                    with col2:
                        if status == 'scheduled':
                            st.warning(status_badge)
                        elif status == 'confirmed':
                            st.success(status_badge)
                        else:
                            st.info(status_badge)
                        
                        st.markdown("**Resources:**")
                        st.button("📚 Interview Prep", key=f"prep_{interview.get('id')}", use_container_width=True, help="Go to Interview Prep tab")
                        
                        if interview.get('student_notes'):
                            st.markdown("---")
                            st.caption("**Your Notes:**")
                            st.write(interview.get('student_notes'))
    
    # ============================================================================
    # TAB 4: MY SETTINGS (VIEW ONLY)
    # ============================================================================
    with tab4:
        st.header("⚙️ My Automation Settings")
        
        st.info("🔒 **Settings are managed by your training provider**")
        st.markdown("Contact them to make changes to your preferences")
        
        st.markdown("---")
        
        st.subheader("Current Settings:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Job Preferences:**")
            st.write(f"📍 Locations: {', '.join(settings.get('preferred_locations', []))}")
            st.write(f"🏥 Bands: {', '.join(settings.get('preferred_bands', []))}")
            st.write(f"⏰ Working Patterns: {', '.join(settings.get('working_patterns', []))}")
            st.write(f"📊 Search Radius: {settings.get('search_radius_miles', 'N/A')} miles")
        
        with col2:
            st.write("**Application Settings:**")
            st.write(f"📬 Max Per Day: {settings.get('max_applications_per_day', 'N/A')}")
            st.write(f"✉️ Notification Email: {settings.get('notification_email', 'N/A')}")
            
            if settings.get('requires_sponsorship'):
                st.write("✅ Visa sponsorship required")
            else:
                st.write("No visa sponsorship needed")
        
        st.markdown("---")
        
        st.info("""
        💡 **Want to change settings?**
        
        Contact your training provider to:
        - Change preferred locations
        - Adjust NHS bands
        - Update working patterns
        - Modify application limits
        - Pause/resume automation
        """)

if __name__ == "__main__":
    job_automation_student_view()
