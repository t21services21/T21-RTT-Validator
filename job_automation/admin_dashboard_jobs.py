"""
T21 JOB AUTOMATION - ADMIN DASHBOARD
Staff oversight of all student job applications
NO MANUAL UPDATES REQUIRED - Everything is automatic!
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
import os

class JobAutomationAdminDashboard:
    """
    Admin dashboard for monitoring job automation system
    Staff can see ALL students and their applications
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    def render(self):
        """Main dashboard"""
        st.set_page_config(page_title="Job Automation Admin", layout="wide")
        
        st.title("🎯 Job Automation - Admin Dashboard")
        st.markdown("**Monitor all student job applications and automation status**")
        
        # Top metrics
        self.render_top_metrics()
        
        st.markdown("---")
        
        # Tabs
        tabs = st.tabs([
            "📊 Overview",
            "👥 Students",
            "📝 Application Queue",
            "🗓️ Interview Calendar",
            "⚙️ System Status",
            "📧 Notifications",
            "📈 Analytics"
        ])
        
        with tabs[0]:
            self.render_overview()
        
        with tabs[1]:
            self.render_students()
        
        with tabs[2]:
            self.render_application_queue()
        
        with tabs[3]:
            self.render_interview_calendar()
        
        with tabs[4]:
            self.render_system_status()
        
        with tabs[5]:
            self.render_notifications()
        
        with tabs[6]:
            self.render_analytics()
    
    def render_top_metrics(self):
        """Top-level metrics"""
        
        # Get counts
        active_students = self.get_active_student_count()
        total_applications = self.get_total_application_count()
        applications_today = self.get_applications_today_count()
        interviews_scheduled = self.get_interviews_scheduled_count()
        offers_received = self.get_offers_count()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Active Students", active_students, help="Students with automation enabled")
        
        with col2:
            st.metric("Total Applications", total_applications)
        
        with col3:
            st.metric("Applications Today", applications_today, 
                     delta=f"+{applications_today}")
        
        with col4:
            st.metric("Interviews Scheduled", interviews_scheduled)
        
        with col5:
            st.metric("Offers Received", offers_received,
                     delta=f"+{self.get_offers_this_week_count()}")
    
    def render_overview(self):
        """Overview dashboard"""
        
        st.subheader("📊 System Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Application status breakdown
            st.markdown("### Application Status")
            status_data = self.get_application_status_breakdown()
            if status_data:
                fig = px.pie(
                    values=list(status_data.values()),
                    names=list(status_data.keys()),
                    title="Applications by Status"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Student performance
            st.markdown("### Top Performing Students")
            top_students = self.get_top_students()
            if top_students:
                df = pd.DataFrame(top_students)
                st.dataframe(df, use_container_width=True)
        
        # Recent activity
        st.markdown("### 📈 Recent Activity (Last 24 Hours)")
        recent = self.get_recent_activity()
        if recent:
            for activity in recent[:10]:
                icon = self.get_activity_icon(activity['type'])
                st.info(f"{icon} **{activity['student_name']}**: {activity['description']} - {activity['time_ago']}")
    
    def render_students(self):
        """Students view with detailed stats"""
        
        st.subheader("👥 All Students")
        
        # Get student data from view
        students = self.supabase.from_('admin_student_overview').select('*').execute()
        
        if not students.data:
            st.info("No students found")
            return
        
        df = pd.DataFrame(students.data)
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            automation_filter = st.selectbox(
                "Automation Status",
                ["All", "Active", "Paused", "Suspended"]
            )
        
        with col2:
            sponsorship_filter = st.selectbox(
                "Requires Sponsorship",
                ["All", "Yes", "No"]
            )
        
        with col3:
            sort_by = st.selectbox(
                "Sort By",
                ["Last Application", "Total Applications", "Success Rate", "Name"]
            )
        
        # Apply filters
        if automation_filter != "All":
            df = df[df['automation_status'] == automation_filter.lower()]
        
        if sponsorship_filter != "All":
            df = df[df['requires_sponsorship'] == (sponsorship_filter == "Yes")]
        
        # Display table
        st.dataframe(df, use_container_width=True)
        
        # Student detail view
        st.markdown("---")
        st.subheader("🔍 Student Details")
        
        student_emails = df['email'].tolist()
        selected_student = st.selectbox("Select Student", student_emails)
        
        if selected_student:
            self.render_student_detail(selected_student)
    
    def render_student_detail(self, student_email: str):
        """Detailed view of single student"""
        
        # Get student stats
        stats = self.supabase.table('student_application_stats')\
            .select('*')\
            .eq('student_id', self.get_student_id(student_email))\
            .single()\
            .execute()
        
        if not stats.data:
            st.warning("No stats available")
            return
        
        stats_data = stats.data
        
        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric("Submitted", stats_data.get('applications_submitted', 0))
        col2.metric("Queued", stats_data.get('applications_queued', 0))
        col3.metric("Interviews", stats_data.get('interviews_invited', 0))
        col4.metric("Offers", stats_data.get('offers_received', 0))
        col5.metric("Success Rate", f"{stats_data.get('overall_success_rate', 0):.1f}%")
        
        # Recent applications
        st.markdown("### Recent Applications")
        apps = self.supabase.from_('admin_application_queue')\
            .select('*')\
            .eq('student_name', student_email)\
            .limit(20)\
            .execute()
        
        if apps.data:
            df = pd.DataFrame(apps.data)
            st.dataframe(df, use_container_width=True)
    
    def render_application_queue(self):
        """View all applications in queue"""
        
        st.subheader("📝 Application Queue")
        
        # Get queue from view
        queue = self.supabase.from_('admin_application_queue')\
            .select('*')\
            .execute()
        
        if not queue.data:
            st.info("No applications in queue")
            return
        
        df = pd.DataFrame(queue.data)
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_filter = st.multiselect(
                "Status",
                ["queued", "processing", "ready", "auto_submitting", "submitted", "failed"],
                default=["queued", "processing", "ready"]
            )
        
        with col2:
            priority_filter = st.multiselect(
                "Priority",
                ["urgent", "high", "normal", "low"],
                default=["urgent", "high"]
            )
        
        with col3:
            days_filter = st.slider("Days Until Closing", 0, 14, (0, 7))
        
        with col4:
            search = st.text_input("Search (Job Title/Trust)")
        
        # Apply filters
        if status_filter:
            df = df[df['status'].isin(status_filter)]
        
        if priority_filter:
            df = df[df['priority'].isin(priority_filter)]
        
        if search:
            df = df[
                df['job_title'].str.contains(search, case=False) |
                df['trust'].str.contains(search, case=False)
            ]
        
        # Display
        st.markdown(f"**Showing {len(df)} applications**")
        
        # Color code by priority
        def highlight_priority(row):
            if row['priority'] == 'urgent':
                return ['background-color: #ffcccc'] * len(row)
            elif row['priority'] == 'high':
                return ['background-color: #ffffcc'] * len(row)
            return [''] * len(row)
        
        styled_df = df.style.apply(highlight_priority, axis=1)
        st.dataframe(styled_df, use_container_width=True)
    
    def render_interview_calendar(self):
        """Interview calendar view"""
        
        st.subheader("🗓️ Interview Calendar")
        
        # Get interviews from view
        interviews = self.supabase.from_('admin_interview_calendar')\
            .select('*')\
            .execute()
        
        if not interviews.data:
            st.info("No upcoming interviews")
            return
        
        df = pd.DataFrame(interviews.data)
        
        # Calendar view
        df['interview_date'] = pd.to_datetime(df['interview_date'])
        df['date_only'] = df['interview_date'].dt.date
        
        # Group by date
        for date in sorted(df['date_only'].unique()):
            st.markdown(f"### 📅 {date}")
            
            day_interviews = df[df['date_only'] == date]
            
            for _, interview in day_interviews.iterrows():
                with st.expander(f"⏰ {interview['interview_date'].strftime('%H:%M')} - {interview['student_name']} - {interview['job_title']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Trust:** {interview['trust']}")
                        st.write(f"**Location:** {interview['interview_location']}")
                        st.write(f"**Format:** {interview['interview_format']}")
                    
                    with col2:
                        st.write(f"**Student Email:** {interview['student_email']}")
                        st.write(f"**Status:** {interview['status']}")
                        if interview['outcome']:
                            st.write(f"**Outcome:** {interview['outcome']}")
    
    def render_system_status(self):
        """System health and status"""
        
        st.subheader("⚙️ System Status")
        
        # System health checks
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🤖 Background Workers")
            
            # Check if workers are running
            scraper_status = self.check_scraper_status()
            queue_status = self.check_queue_processor_status()
            interview_status = self.check_interview_detector_status()
            
            status_icon = "✅" if scraper_status else "❌"
            st.write(f"{status_icon} Job Scraper: {'Running' if scraper_status else 'Stopped'}")
            
            status_icon = "✅" if queue_status else "❌"
            st.write(f"{status_icon} Queue Processor: {'Running' if queue_status else 'Stopped'}")
            
            status_icon = "✅" if interview_status else "❌"
            st.write(f"{status_icon} Interview Detector: {'Running' if interview_status else 'Stopped'}")
        
        with col2:
            st.markdown("### 📊 Processing Stats")
            
            # Get processing stats
            stats = self.get_system_stats()
            
            st.metric("Jobs Discovered (24h)", stats.get('jobs_discovered_24h', 0))
            st.metric("Applications Submitted (24h)", stats.get('apps_submitted_24h', 0))
            st.metric("Interviews Detected (24h)", stats.get('interviews_detected_24h', 0))
        
        with col3:
            st.markdown("### ⚠️ System Alerts")
            
            alerts = self.get_system_alerts()
            
            if alerts:
                for alert in alerts:
                    st.warning(f"⚠️ {alert}")
            else:
                st.success("✅ No alerts")
        
        # Recent errors
        st.markdown("### 🐛 Recent Errors")
        errors = self.get_recent_errors()
        
        if errors:
            df = pd.DataFrame(errors)
            st.dataframe(df, use_container_width=True)
        else:
            st.success("✅ No errors in last 24 hours")
    
    def render_notifications(self):
        """View sent notifications"""
        
        st.subheader("📧 Email Notifications")
        
        # Get recent notifications
        notifications = self.supabase.table('email_notifications')\
            .select('*')\
            .order('sent_at', desc=True)\
            .limit(100)\
            .execute()
        
        if not notifications.data:
            st.info("No notifications sent yet")
            return
        
        df = pd.DataFrame(notifications.data)
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            notif_type_filter = st.multiselect(
                "Notification Type",
                df['notification_type'].unique() if 'notification_type' in df.columns else []
            )
        
        with col2:
            date_filter = st.date_input(
                "Date Range",
                value=(datetime.now().date() - timedelta(days=7), datetime.now().date())
            )
        
        # Apply filters
        if notif_type_filter:
            df = df[df['notification_type'].isin(notif_type_filter)]
        
        # Display
        st.dataframe(df, use_container_width=True)
        
        # Stats
        st.markdown("### 📊 Notification Stats")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total Sent", len(df))
        col2.metric("Delivered", df['delivered_at'].notna().sum() if 'delivered_at' in df.columns else 0)
        col3.metric("Opened", df['opened_at'].notna().sum() if 'opened_at' in df.columns else 0)
        col4.metric("Clicked", df['clicked_at'].notna().sum() if 'clicked_at' in df.columns else 0)
    
    def render_analytics(self):
        """Analytics and insights"""
        
        st.subheader("📈 Analytics & Insights")
        
        # Time period selector
        period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
        
        # Applications over time
        st.markdown("### Applications Over Time")
        apps_timeline = self.get_applications_timeline(period)
        
        if apps_timeline:
            fig = px.line(
                apps_timeline,
                x='date',
                y='count',
                title='Applications Submitted Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Success rates
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Success Rates by Student")
            success_data = self.get_success_rates_by_student()
            
            if success_data:
                fig = px.bar(
                    success_data,
                    x='student',
                    y='success_rate',
                    title='Application Success Rates'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Top Hiring Trusts")
            trust_data = self.get_top_hiring_trusts()
            
            if trust_data:
                fig = px.bar(
                    trust_data,
                    x='trust',
                    y='interviews',
                    title='Trusts with Most Interviews'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Helper methods
    def get_active_student_count(self) -> int:
        result = self.supabase.table('student_automation_settings')\
            .select('id', count='exact')\
            .eq('status', 'active')\
            .execute()
        return result.count or 0
    
    def get_total_application_count(self) -> int:
        result = self.supabase.table('applications')\
            .select('id', count='exact')\
            .execute()
        return result.count or 0
    
    def get_applications_today_count(self) -> int:
        today = datetime.now().date().isoformat()
        result = self.supabase.table('applications')\
            .select('id', count='exact')\
            .gte('created_at', today)\
            .execute()
        return result.count or 0
    
    def get_interviews_scheduled_count(self) -> int:
        result = self.supabase.table('interviews')\
            .select('id', count='exact')\
            .in_('status', ['scheduled', 'confirmed'])\
            .execute()
        return result.count or 0
    
    def get_offers_count(self) -> int:
        result = self.supabase.table('interviews')\
            .select('id', count='exact')\
            .eq('outcome', 'offered')\
            .execute()
        return result.count or 0
    
    def get_offers_this_week_count(self) -> int:
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        result = self.supabase.table('interviews')\
            .select('id', count='exact')\
            .eq('outcome', 'offered')\
            .gte('outcome_date', week_ago)\
            .execute()
        return result.count or 0
    
    def get_application_status_breakdown(self) -> dict:
        apps = self.supabase.table('applications')\
            .select('status')\
            .execute()
        
        if not apps.data:
            return {}
        
        from collections import Counter
        return dict(Counter([app['status'] for app in apps.data]))
    
    def get_top_students(self) -> list:
        # Get from stats table
        stats = self.supabase.table('student_application_stats')\
            .select('*')\
            .order('overall_success_rate', desc=True)\
            .limit(10)\
            .execute()
        
        return stats.data if stats.data else []
    
    def get_recent_activity(self) -> list:
        # Combine recent applications and interviews
        # Simplified for now
        return []
    
    def get_activity_icon(self, activity_type: str) -> str:
        icons = {
            'application_submitted': '📝',
            'interview_detected': '🎉',
            'offer_received': '🎊',
            'application_queued': '⏳'
        }
        return icons.get(activity_type, '📌')
    
    def get_student_id(self, email: str) -> str:
        student = self.supabase.table('students')\
            .select('id')\
            .eq('email', email)\
            .single()\
            .execute()
        return student.data['id'] if student.data else None
    
    def check_scraper_status(self) -> bool:
        # Check if scraper ran recently (within last 7 hours)
        # Implementation depends on how you track worker status
        return True  # Placeholder
    
    def check_queue_processor_status(self) -> bool:
        return True  # Placeholder
    
    def check_interview_detector_status(self) -> bool:
        return True  # Placeholder
    
    def get_system_stats(self) -> dict:
        return {
            'jobs_discovered_24h': 0,
            'apps_submitted_24h': 0,
            'interviews_detected_24h': 0
        }
    
    def get_system_alerts(self) -> list:
        return []
    
    def get_recent_errors(self) -> list:
        # Get failed applications
        errors = self.supabase.table('applications')\
            .select('*')\
            .eq('status', 'failed')\
            .gte('created_at', (datetime.now() - timedelta(days=1)).isoformat())\
            .execute()
        
        return errors.data if errors.data else []
    
    def get_applications_timeline(self, period: str) -> pd.DataFrame:
        # Get applications grouped by date
        # Simplified for now
        return pd.DataFrame()
    
    def get_success_rates_by_student(self) -> pd.DataFrame:
        return pd.DataFrame()
    
    def get_top_hiring_trusts(self) -> pd.DataFrame:
        return pd.DataFrame()


if __name__ == '__main__':
    dashboard = JobAutomationAdminDashboard()
    dashboard.render()
