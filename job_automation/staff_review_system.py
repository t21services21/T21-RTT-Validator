"""
Staff Review & Approval System
Flexible workflow: Staff can choose to review applications OR auto-submit
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from supabase import create_client
import os
import logging

logger = logging.getLogger(__name__)

class StaffReviewSystem:
    """
    Staff interface for reviewing and approving applications
    Three modes:
    1. Review Mode: Staff checks every application before submit
    2. Auto-Submit Mode: Applications submit automatically
    3. Hybrid Mode: Auto-submit some, review others (based on criteria)
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    def render_staff_dashboard(self):
        """
        Main staff review dashboard
        """
        st.title("👨‍💼 Staff Review Dashboard")
        st.markdown("**Review applications before submission or enable auto-submit**")
        
        # Tabs
        tabs = st.tabs([
            "📝 Pending Review",
            "⚙️ Student Settings",
            "📊 Submission History",
            "🔧 Global Settings"
        ])
        
        with tabs[0]:
            self.render_pending_applications()
        
        with tabs[1]:
            self.render_student_settings()
        
        with tabs[2]:
            self.render_submission_history()
        
        with tabs[3]:
            self.render_global_settings()
    
    def render_pending_applications(self):
        """
        Show applications pending staff review
        """
        st.subheader("📝 Applications Pending Review")
        
        # Get applications in 'ready' status (waiting for review)
        apps = self.supabase.table('applications')\
            .select('*, student:student_id(first_name, last_name, email), job:job_id(*)')\
            .eq('status', 'ready')\
            .order('created_at', desc=False)\
            .execute()
        
        if not apps.data:
            st.success("✅ No applications pending review")
            return
        
        st.markdown(f"**{len(apps.data)} applications waiting for your review**")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_student = st.selectbox(
                "Filter by Student",
                ["All"] + list(set([app['student']['email'] for app in apps.data]))
            )
        
        with col2:
            filter_priority = st.multiselect(
                "Priority",
                ["urgent", "high", "normal", "low"],
                default=["urgent", "high"]
            )
        
        with col3:
            filter_sponsorship = st.selectbox(
                "Sponsorship",
                ["All", "Required", "Not Required"]
            )
        
        # Apply filters
        filtered_apps = apps.data
        
        if filter_student != "All":
            filtered_apps = [app for app in filtered_apps if app['student']['email'] == filter_student]
        
        if filter_priority:
            filtered_apps = [app for app in filtered_apps if app['priority'] in filter_priority]
        
        if filter_sponsorship != "All":
            if filter_sponsorship == "Required":
                filtered_apps = [app for app in filtered_apps if app['job'].get('has_sponsorship')]
            else:
                filtered_apps = [app for app in filtered_apps if not app['job'].get('has_sponsorship')]
        
        # Display each application
        for app in filtered_apps:
            self.render_application_review_card(app)
    
    def render_application_review_card(self, app: dict):
        """
        Single application review card with approve/reject buttons
        """
        student = app['student']
        job = app['job']
        
        # Priority color
        priority_colors = {
            'urgent': '🔴',
            'high': '🟠',
            'normal': '🟢',
            'low': '⚪'
        }
        priority_icon = priority_colors.get(app['priority'], '⚪')
        
        with st.expander(
            f"{priority_icon} {student['first_name']} {student['last_name']} → {job['title']} at {job['trust']}",
            expanded=app['priority'] in ['urgent', 'high']
        ):
            # Two columns: Application details | Preview
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 📋 Application Details")
                
                st.write(f"**Student:** {student['first_name']} {student['last_name']}")
                st.write(f"**Email:** {student['email']}")
                st.write(f"**Job Title:** {job['title']}")
                st.write(f"**Trust:** {job['trust']}")
                st.write(f"**Location:** {job['location']}")
                st.write(f"**Band:** {job.get('band', 'N/A')}")
                st.write(f"**Closing Date:** {job['closing_date']}")
                st.write(f"**Sponsorship:** {'✅ Available' if job.get('has_sponsorship') else '❌ Not available'}")
                st.write(f"**Priority:** {app['priority'].upper()}")
                
                # AI Generation Stats
                st.markdown("---")
                st.markdown("### 🤖 AI Generation")
                st.write(f"**Word Count:** {app.get('ai_word_count', 0)} words")
                st.write(f"**Generation Time:** {app.get('ai_generation_time', 0):.2f}s")
                st.write(f"**Quality Score:** {app.get('quality_score', 0)}/100")
                
                # Scheduled submission
                st.markdown("---")
                st.write(f"**Scheduled Submit:** {app.get('scheduled_submit_time', 'Not set')}")
            
            with col2:
                st.markdown("### 📄 Supporting Information Preview")
                
                # Show AI-generated supporting information
                supporting_info = app.get('ai_supporting_information', '')
                
                if supporting_info:
                    # Show first 500 characters
                    preview = supporting_info[:500] + "..." if len(supporting_info) > 500 else supporting_info
                    st.text_area(
                        "AI-Generated Content",
                        value=preview,
                        height=300,
                        disabled=True
                    )
                    
                    # Download full content
                    st.download_button(
                        "📥 Download Full Supporting Information",
                        supporting_info,
                        file_name=f"supporting_info_{app['id']}.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("⚠️ No supporting information generated yet")
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✅ Approve & Submit Now", key=f"approve_{app['id']}"):
                    self.approve_and_submit(app['id'])
                    st.success("✅ Application approved! Submitting now...")
                    st.rerun()
            
            with col2:
                if st.button("📝 Edit & Approve", key=f"edit_{app['id']}"):
                    self.open_edit_modal(app)
            
            with col3:
                if st.button("⏰ Schedule for Later", key=f"schedule_{app['id']}"):
                    self.schedule_for_later(app['id'])
                    st.success("⏰ Application will be submitted at scheduled time")
                    st.rerun()
            
            with col4:
                if st.button("❌ Reject", key=f"reject_{app['id']}"):
                    self.reject_application(app['id'])
                    st.warning("❌ Application rejected")
                    st.rerun()
    
    def render_student_settings(self):
        """
        Configure automation settings per student
        """
        st.subheader("⚙️ Student Automation Settings")
        
        # Get all students
        students = self.supabase.table('student_automation_settings')\
            .select('*, student:student_id(first_name, last_name, email)')\
            .execute()
        
        if not students.data:
            st.info("No students configured yet")
            return
        
        # Select student
        student_options = {
            f"{s['student']['first_name']} {s['student']['last_name']} ({s['student']['email']})": s
            for s in students.data
        }
        
        selected = st.selectbox("Select Student", list(student_options.keys()))
        
        if selected:
            settings = student_options[selected]
            self.render_student_automation_config(settings)
    
    def render_student_automation_config(self, settings: dict):
        """
        Configure automation for individual student
        """
        st.markdown(f"### {settings['student']['first_name']} {settings['student']['last_name']}")
        
        # Three columns: Current Status | Settings | Actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📊 Current Status")
            
            # Get stats
            stats = self.supabase.table('student_application_stats')\
                .select('*')\
                .eq('student_id', settings['student_id'])\
                .single()\
                .execute()
            
            if stats.data:
                st.metric("Total Applications", stats.data.get('total_applications', 0))
                st.metric("Submitted", stats.data.get('applications_submitted', 0))
                st.metric("Interviews", stats.data.get('interviews_invited', 0))
                st.metric("Success Rate", f"{stats.data.get('overall_success_rate', 0):.1f}%")
        
        with col2:
            st.markdown("#### ⚙️ Automation Settings")
            
            # Automation mode
            automation_mode = st.radio(
                "Automation Mode",
                [
                    "🔴 Paused (No automation)",
                    "🟡 Review Mode (Staff approval required)",
                    "🟢 Auto-Submit (Fully automated)"
                ],
                index=self.get_current_mode_index(settings)
            )
            
            # Other settings
            max_apps_per_day = st.slider(
                "Max Applications per Day",
                min_value=1,
                max_value=100,
                value=settings.get('max_applications_per_day', 50)
            )
            
            requires_sponsorship = st.checkbox(
                "Requires Sponsorship",
                value=settings.get('requires_sponsorship', False)
            )
            
            # Job preferences
            st.markdown("**Job Preferences:**")
            
            locations = st.multiselect(
                "Preferred Locations",
                ["London", "Manchester", "Birmingham", "Leeds", "Bristol", "Liverpool", "Sheffield"],
                default=settings.get('preferred_locations', ['London'])
            )
            
            bands = st.multiselect(
                "Preferred Bands",
                ["Band 3", "Band 4", "Band 5", "Band 6"],
                default=settings.get('preferred_bands', ['Band 3', 'Band 4'])
            )
        
        with col3:
            st.markdown("#### 🎯 Actions")
            
            if st.button("💾 Save Settings", key=f"save_{settings['student_id']}"):
                # Parse automation mode
                if "Paused" in automation_mode:
                    status = 'paused'
                    auto_submit = False
                elif "Review Mode" in automation_mode:
                    status = 'active'
                    auto_submit = False
                else:  # Auto-Submit
                    status = 'active'
                    auto_submit = True
                
                # Update settings
                self.supabase.table('student_automation_settings')\
                    .update({
                        'status': status,
                        'auto_submit_enabled': auto_submit,
                        'max_applications_per_day': max_apps_per_day,
                        'requires_sponsorship': requires_sponsorship,
                        'preferred_locations': locations,
                        'preferred_bands': bands,
                        'updated_at': datetime.now().isoformat()
                    })\
                    .eq('student_id', settings['student_id'])\
                    .execute()
                
                st.success("✅ Settings saved!")
            
            # Quick actions
            st.markdown("---")
            
            if st.button("▶️ Start Automation", key=f"start_{settings['student_id']}"):
                self.supabase.table('student_automation_settings')\
                    .update({'status': 'active'})\
                    .eq('student_id', settings['student_id'])\
                    .execute()
                st.success("✅ Automation started!")
            
            if st.button("⏸️ Pause Automation", key=f"pause_{settings['student_id']}"):
                self.supabase.table('student_automation_settings')\
                    .update({'status': 'paused'})\
                    .eq('student_id', settings['student_id'])\
                    .execute()
                st.warning("⏸️ Automation paused")
            
            # Contract status
            st.markdown("---")
            st.markdown("**Contract Status:**")
            
            contract_signed = settings.get('contract_signed', False)
            
            if contract_signed:
                st.success("✅ Contract Signed")
                st.write(f"Signed: {settings.get('contract_signed_date', 'N/A')}")
            else:
                st.error("❌ Contract Not Signed")
                
                uploaded_contract = st.file_uploader(
                    "Upload Signed Contract",
                    type=['pdf', 'jpg', 'png'],
                    key=f"contract_{settings['student_id']}"
                )
                
                if uploaded_contract and st.button("✅ Mark Contract as Signed"):
                    # Upload contract (implement file storage)
                    self.supabase.table('student_automation_settings')\
                        .update({
                            'contract_signed': True,
                            'contract_signed_date': datetime.now().isoformat()
                        })\
                        .eq('student_id', settings['student_id'])\
                        .execute()
                    st.success("✅ Contract marked as signed!")
    
    def render_submission_history(self):
        """
        View all submitted applications
        """
        st.subheader("📊 Submission History")
        
        # Get submitted applications
        apps = self.supabase.table('applications')\
            .select('*, student:student_id(first_name, last_name, email), job:job_id(title, trust)')\
            .eq('status', 'submitted')\
            .order('submitted_at', desc=True)\
            .limit(100)\
            .execute()
        
        if not apps.data:
            st.info("No submitted applications yet")
            return
        
        # Convert to DataFrame
        data = []
        for app in apps.data:
            data.append({
                'Student': f"{app['student']['first_name']} {app['student']['last_name']}",
                'Email': app['student']['email'],
                'Job Title': app['job']['title'],
                'Trust': app['job']['trust'],
                'Submitted': app['submitted_at'],
                'Confirmation': app.get('confirmation_number', 'N/A'),
                'Status': app['status']
            })
        
        df = pd.DataFrame(data)
        
        st.dataframe(df, use_container_width=True)
        
        # Export
        if st.button("📥 Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "submission_history.csv",
                "text/csv"
            )
    
    def render_global_settings(self):
        """
        Global automation settings
        """
        st.subheader("🔧 Global System Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🤖 System Automation")
            
            # Get current settings
            config = self.get_system_config()
            
            enable_auto_submit = st.checkbox(
                "Enable Global Auto-Submit",
                value=config.get('enable_auto_submit', True),
                help="When enabled, applications in auto-submit mode will be submitted automatically"
            )
            
            scraper_interval = st.slider(
                "Job Scraper Interval (hours)",
                min_value=1,
                max_value=24,
                value=config.get('scraper_interval_hours', 6)
            )
            
            max_concurrent = st.slider(
                "Max Concurrent Applications",
                min_value=1,
                max_value=20,
                value=config.get('max_concurrent_applications', 10)
            )
            
            rate_limit = st.slider(
                "Rate Limit (per hour)",
                min_value=10,
                max_value=100,
                value=config.get('rate_limit_per_hour', 50)
            )
        
        with col2:
            st.markdown("### 🎯 Default Settings for New Students")
            
            default_mode = st.selectbox(
                "Default Automation Mode",
                ["Review Mode", "Auto-Submit Mode", "Paused"]
            )
            
            default_max_apps = st.slider(
                "Default Max Apps/Day",
                min_value=1,
                max_value=100,
                value=50
            )
            
            require_contract = st.checkbox(
                "Require Signed Contract",
                value=True,
                help="Students must have signed contract before automation starts"
            )
        
        if st.button("💾 Save Global Settings"):
            # Update system config
            self.update_system_config({
                'enable_auto_submit': enable_auto_submit,
                'scraper_interval_hours': scraper_interval,
                'max_concurrent_applications': max_concurrent,
                'rate_limit_per_hour': rate_limit,
                'default_automation_mode': default_mode,
                'default_max_apps_per_day': default_max_apps,
                'require_contract': require_contract
            })
            st.success("✅ Global settings saved!")
    
    # Helper methods
    def approve_and_submit(self, application_id: str):
        """Mark application as approved and submit immediately"""
        self.supabase.table('applications')\
            .update({
                'status': 'approved',
                'scheduled_submit_time': datetime.now().isoformat()
            })\
            .eq('id', application_id)\
            .execute()
    
    def schedule_for_later(self, application_id: str):
        """Keep scheduled submit time"""
        self.supabase.table('applications')\
            .update({'status': 'approved'})\
            .eq('id', application_id)\
            .execute()
    
    def reject_application(self, application_id: str):
        """Reject application"""
        self.supabase.table('applications')\
            .update({'status': 'rejected'})\
            .eq('id', application_id)\
            .execute()
    
    def open_edit_modal(self, app: dict):
        """Open edit interface for application"""
        st.info("Edit functionality - implement text editor for supporting information")
    
    def get_current_mode_index(self, settings: dict) -> int:
        """Get current automation mode index for radio button"""
        if settings['status'] == 'paused':
            return 0
        elif not settings.get('auto_submit_enabled', False):
            return 1
        else:
            return 2
    
    def get_system_config(self) -> dict:
        """Get system configuration"""
        try:
            config = self.supabase.table('system_config').select('*').execute()
            return {row['key']: row['value'] for row in config.data} if config.data else {}
        except:
            return {}
    
    def update_system_config(self, config: dict):
        """Update system configuration"""
        for key, value in config.items():
            self.supabase.table('system_config')\
                .upsert({'key': key, 'value': value, 'updated_at': datetime.now().isoformat()})\
                .execute()


if __name__ == '__main__':
    system = StaffReviewSystem()
    system.render_staff_dashboard()
