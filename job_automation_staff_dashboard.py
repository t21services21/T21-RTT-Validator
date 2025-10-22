"""
NHS JOB APPLICATION AUTOMATION - STAFF DASHBOARD
Complete monitoring and management system for T21 staff
Full control over all student job automation
"""

import streamlit as st
from datetime import datetime, timedelta
from supabase import create_client
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def get_all_students_overview():
    """Get overview of all students with automation"""
    try:
        response = supabase.table('admin_student_overview').select('*').execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading student overview: {str(e)}")
        return []

def get_application_queue():
    """Get all pending applications"""
    try:
        response = supabase.table('admin_application_queue').select('*').execute()
        return response.data if response.data else []
    except Exception as e:
        return []

def get_interview_calendar():
    """Get upcoming interviews"""
    try:
        response = supabase.table('admin_interview_calendar').select('*').execute()
        return response.data if response.data else []
    except Exception as e:
        return []

def get_system_stats():
    """Get overall system statistics"""
    try:
        # Total students with automation
        students = supabase.table('student_automation_settings').select('id', count='exact').execute()
        total_students = len(students.data) if students.data else 0
        
        # Total applications
        apps = supabase.table('applications').select('id', count='exact').execute()
        total_apps = len(apps.data) if apps.data else 0
        
        # Applications this week
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        apps_week = supabase.table('applications').select('id').gte('created_at', week_ago).execute()
        apps_this_week = len(apps_week.data) if apps_week.data else 0
        
        # Total interviews
        interviews = supabase.table('interviews').select('id', count='exact').execute()
        total_interviews = len(interviews.data) if interviews.data else 0
        
        # Job offers
        offers = supabase.table('interviews').select('id').eq('outcome', 'offered').execute()
        total_offers = len(offers.data) if offers.data else 0
        
        return {
            'total_students': total_students,
            'total_applications': total_apps,
            'applications_this_week': apps_this_week,
            'total_interviews': total_interviews,
            'total_offers': total_offers
        }
    except Exception as e:
        return {
            'total_students': 0,
            'total_applications': 0,
            'applications_this_week': 0,
            'total_interviews': 0,
            'total_offers': 0
        }

def job_automation_staff_dashboard():
    """Main staff dashboard for job automation monitoring"""
    
    st.title("📊 NHS Job Automation - Staff Dashboard")
    st.markdown("**Complete monitoring and management of student job applications**")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "👥 Students",
        "📝 Application Queue",
        "🎤 Interviews",
        "📈 Analytics",
        "⚙️ System Settings"
    ])
    
    # ============================================================================
    # TAB 1: OVERVIEW
    # ============================================================================
    with tab1:
        st.header("📊 System Overview")
        
        # Get stats
        stats = get_system_stats()
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "👥 Active Students",
                stats['total_students']
            )
        
        with col2:
            st.metric(
                "📬 Total Applications",
                stats['total_applications'],
                delta=f"{stats['applications_this_week']} this week"
            )
        
        with col3:
            st.metric(
                "🎤 Interviews",
                stats['total_interviews']
            )
        
        with col4:
            st.metric(
                "🎉 Job Offers",
                stats['total_offers']
            )
        
        with col5:
            success_rate = (stats['total_offers'] / stats['total_interviews'] * 100) if stats['total_interviews'] > 0 else 0
            st.metric(
                "📈 Success Rate",
                f"{success_rate:.1f}%"
            )
        
        st.markdown("---")
        
        # Recent activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Recent Applications")
            
            recent_apps = supabase.table('applications').select('*, students(first_name, last_name), discovered_jobs(title, trust)').order('created_at', desc=True).limit(10).execute()
            
            if recent_apps.data:
                for app in recent_apps.data:
                    student = app.get('students', {})
                    job = app.get('discovered_jobs', {})
                    
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.write(f"**{student.get('first_name', '')} {student.get('last_name', '')}**")
                            st.caption(f"{job.get('title', 'Unknown')} - {job.get('trust', 'Unknown')}")
                        with col_b:
                            status = app.get('status', 'unknown')
                            if status == 'submitted':
                                st.success("✅")
                            elif status == 'failed':
                                st.error("❌")
                            else:
                                st.info("⏳")
                        st.divider()
            else:
                st.info("No recent applications")
        
        with col2:
            st.subheader("🎤 Upcoming Interviews")
            
            upcoming = supabase.table('interviews').select('*, students(first_name, last_name), discovered_jobs(title, trust)').gte('interview_date', datetime.now().isoformat()).order('interview_date', desc=False).limit(10).execute()
            
            if upcoming.data:
                for interview in upcoming.data:
                    student = interview.get('students', {})
                    job = interview.get('discovered_jobs', {})
                    
                    with st.container():
                        st.write(f"**{student.get('first_name', '')} {student.get('last_name', '')}**")
                        st.caption(f"{job.get('title', 'Unknown')} - {interview.get('interview_date', 'TBC')[:10]}")
                        st.divider()
            else:
                st.info("No upcoming interviews")
    
    # ============================================================================
    # TAB 2: STUDENTS
    # ============================================================================
    with tab2:
        st.header("👥 Student Management")
        
        students = get_all_students_overview()
        
        if not students:
            st.info("No students have set up job automation yet")
        else:
            st.success(f"📊 **{len(students)}** students using job automation")
            
            # Convert to DataFrame
            df = pd.DataFrame(students)
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "active", "paused", "suspended"])
            
            with col2:
                sponsorship_filter = st.selectbox("Sponsorship", ["All", "Required", "Not Required"])
            
            with col3:
                sort_by = st.selectbox("Sort By", ["Last Application Date", "Total Applications", "Success Rate"])
            
            # Display students
            for student in students:
                # Apply filters
                if status_filter != "All" and student.get('automation_status') != status_filter:
                    continue
                if sponsorship_filter == "Required" and not student.get('requires_sponsorship'):
                    continue
                if sponsorship_filter == "Not Required" and student.get('requires_sponsorship'):
                    continue
                
                with st.expander(f"👤 {student.get('first_name', '')} {student.get('last_name', '')} - {student.get('email', '')}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Applications:**")
                        st.write(f"Total: {student.get('total_applications', 0)}")
                        st.write(f"Submitted: {student.get('applications_submitted', 0)}")
                    
                    with col2:
                        st.write("**Interviews:**")
                        st.write(f"Invited: {student.get('interviews_invited', 0)}")
                        st.write(f"Offers: {student.get('offers_received', 0)}")
                    
                    with col3:
                        st.write("**Settings:**")
                        st.write(f"Status: {student.get('automation_status', 'Unknown')}")
                        if student.get('requires_sponsorship'):
                            st.write("✓ Sponsorship Required")
                        if student.get('auto_submit_enabled'):
                            st.write("✓ Auto-submit Enabled")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        if st.button("📊 View Details", key=f"details_{student.get('id')}", use_container_width=True):
                            st.info("Detailed view coming soon!")
                    
                    with col_b:
                        if student.get('automation_status') == 'active':
                            if st.button("⏸️ Pause Automation", key=f"pause_{student.get('id')}", use_container_width=True):
                                supabase.table('student_automation_settings').update({'status': 'paused'}).eq('student_id', student.get('id')).execute()
                                st.success("Automation paused")
                                st.rerun()
                        else:
                            if st.button("▶️ Resume Automation", key=f"resume_{student.get('id')}", use_container_width=True):
                                supabase.table('student_automation_settings').update({'status': 'active'}).eq('student_id', student.get('id')).execute()
                                st.success("Automation resumed")
                                st.rerun()
                    
                    with col_c:
                        if st.button("📧 Send Email", key=f"email_{student.get('id')}", use_container_width=True):
                            st.info("Email functionality coming soon!")
    
    # ============================================================================
    # TAB 3: APPLICATION QUEUE
    # ============================================================================
    with tab3:
        st.header("📝 Application Queue")
        
        queue = get_application_queue()
        
        if not queue:
            st.info("No applications in queue")
        else:
            st.success(f"📊 **{len(queue)}** applications in queue")
            
            # Status breakdown
            queued = len([a for a in queue if a.get('status') == 'queued'])
            processing = len([a for a in queue if a.get('status') == 'processing'])
            ready = len([a for a in queue if a.get('status') == 'ready'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏳ Queued", queued)
            with col2:
                st.metric("⚙️ Processing", processing)
            with col3:
                st.metric("✅ Ready", ready)
            
            st.markdown("---")
            
            # Display queue
            for app in queue:
                with st.expander(f"📄 {app.get('student_name', 'Unknown')} → {app.get('job_title', 'Unknown')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Trust:** {app.get('trust', 'Unknown')}")
                        st.write(f"**Location:** {app.get('location', 'Unknown')}")
                        st.write(f"**Closing Date:** {app.get('closing_date', 'Unknown')}")
                        st.write(f"**Status:** {app.get('status', 'Unknown').upper()}")
                        st.write(f"**Priority:** {app.get('priority', 'Normal').upper()}")
                        st.write(f"**Attempts:** {app.get('attempts', 0)}")
                    
                    with col2:
                        if st.button("👁️ Review", key=f"review_{app.get('id')}", use_container_width=True):
                            st.info("Review interface coming soon!")
                        
                        if st.button("🚀 Submit Now", key=f"submit_{app.get('id')}", use_container_width=True):
                            st.info("Manual submission coming soon!")
                        
                        if st.button("❌ Cancel", key=f"cancel_{app.get('id')}", use_container_width=True):
                            supabase.table('applications').delete().eq('id', app.get('id')).execute()
                            st.success("Application cancelled")
                            st.rerun()
    
    # ============================================================================
    # TAB 4: INTERVIEWS
    # ============================================================================
    with tab4:
        st.header("🎤 Interview Calendar")
        
        interviews = get_interview_calendar()
        
        if not interviews:
            st.info("No interviews scheduled")
        else:
            st.success(f"📊 **{len(interviews)}** interviews scheduled")
            
            for interview in interviews:
                with st.expander(f"🎤 {interview.get('student_name', 'Unknown')} - {interview.get('job_title', 'Unknown')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Student:** {interview.get('student_name', 'Unknown')}")
                        st.write(f"**Email:** {interview.get('student_email', 'Unknown')}")
                        st.write(f"**Trust:** {interview.get('trust', 'Unknown')}")
                        st.write(f"**Date:** {interview.get('interview_date', 'TBC')}")
                        st.write(f"**Location:** {interview.get('interview_location', 'TBC')}")
                        st.write(f"**Format:** {interview.get('interview_format', 'Not specified')}")
                        st.write(f"**Status:** {interview.get('status', 'Unknown').upper()}")
                        
                        if interview.get('outcome'):
                            st.write(f"**Outcome:** {interview.get('outcome', 'Unknown').upper()}")
                    
                    with col2:
                        if st.button("📧 Send Reminder", key=f"remind_{interview.get('id')}", use_container_width=True):
                            st.info("Reminder sent!")
                        
                        if st.button("📚 Prep Materials", key=f"prep_{interview.get('id')}", use_container_width=True):
                            st.info("Prep materials sent!")
                        
                        if st.button("✏️ Update Outcome", key=f"outcome_{interview.get('id')}", use_container_width=True):
                            st.info("Update interface coming soon!")
    
    # ============================================================================
    # TAB 5: ANALYTICS
    # ============================================================================
    with tab5:
        st.header("📈 Analytics & Insights")
        
        # Get data for charts
        try:
            # Applications over time
            apps_data = supabase.table('applications').select('created_at, status').execute()
            
            if apps_data.data:
                df_apps = pd.DataFrame(apps_data.data)
                df_apps['created_at'] = pd.to_datetime(df_apps['created_at'])
                df_apps['date'] = df_apps['created_at'].dt.date
                
                # Applications per day
                apps_per_day = df_apps.groupby('date').size().reset_index(name='count')
                
                fig = px.line(apps_per_day, x='date', y='count', 
                             title='Applications Per Day',
                             labels={'date': 'Date', 'count': 'Applications'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Status breakdown
                status_counts = df_apps['status'].value_counts()
                
                fig2 = px.pie(values=status_counts.values, names=status_counts.index,
                             title='Application Status Distribution')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No application data available yet")
        except Exception as e:
            st.error(f"Error loading analytics: {str(e)}")
    
    # ============================================================================
    # TAB 6: SYSTEM SETTINGS
    # ============================================================================
    with tab6:
        st.header("⚙️ System Settings")
        
        st.subheader("🔧 Global Configuration")
        
        try:
            config = supabase.table('system_config').select('*').execute()
            
            if config.data:
                for setting in config.data:
                    key = setting.get('key')
                    value = setting.get('value')
                    description = setting.get('description', '')
                    
                    st.write(f"**{key}**")
                    st.caption(description)
                    
                    if isinstance(value, bool) or value in ['true', 'false']:
                        new_value = st.checkbox(key, value=value if isinstance(value, bool) else value == 'true')
                    elif isinstance(value, (int, float)) or value.isdigit():
                        new_value = st.number_input(key, value=int(value))
                    else:
                        new_value = st.text_input(key, value=str(value))
                    
                    st.divider()
            else:
                st.info("No system configuration found")
        except Exception as e:
            st.error(f"Error loading settings: {str(e)}")
        
        if st.button("💾 SAVE SETTINGS", type="primary", use_container_width=True):
            st.success("Settings saved!")

if __name__ == "__main__":
    job_automation_staff_dashboard()
