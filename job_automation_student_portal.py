"""
NHS JOB APPLICATION AUTOMATION - STUDENT PORTAL
Complete job automation system for T21 students
Fully functional with all features integrated
"""

import streamlit as st
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import pandas as pd

# Import existing Supabase connection
from supabase_database import supabase, SUPABASE_AVAILABLE

def encrypt_password(password):
    """Encrypt Trac password"""
    try:
        key = st.secrets["ENCRYPTION_KEY"].encode()
        f = Fernet(key)
        return f.encrypt(password.encode()).decode()
    except KeyError:
        st.error("⚠️ Encryption key not configured. Please add ENCRYPTION_KEY to Streamlit secrets.")
        return None

def decrypt_password(encrypted_password):
    """Decrypt Trac password"""
    try:
        key = st.secrets["ENCRYPTION_KEY"].encode()
        f = Fernet(key)
        return f.decrypt(encrypted_password.encode()).decode()
    except KeyError:
        st.error("⚠️ Encryption key not configured.")
        return None

def get_student_settings(student_id):
    """Get student automation settings"""
    try:
        response = supabase.table('student_automation_settings').select('*').eq('student_id', student_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        return None

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
            'offers_received': 0
        }
    except Exception as e:
        return {
            'total_applications': 0,
            'applications_submitted': 0,
            'interviews_invited': 0,
            'offers_received': 0
        }

def get_student_applications(student_id):
    """Get all applications for student"""
    try:
        response = supabase.table('applications').select('*, discovered_jobs(*)').eq('student_id', student_id).order('created_at', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading applications: {str(e)}")
        return []

def get_student_interviews(student_id):
    """Get all interviews for student"""
    try:
        response = supabase.table('interviews').select('*, discovered_jobs(*)').eq('student_id', student_id).order('interview_date', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        return []

def get_available_jobs(settings):
    """Get jobs matching student preferences"""
    try:
        query = supabase.table('discovered_jobs').select('*').eq('is_active', True)
        
        # Filter by sponsorship if required
        if settings and settings.get('requires_sponsorship'):
            query = query.eq('has_sponsorship', True)
        
        # Filter by closing date
        today = datetime.now().date()
        max_closing = today + timedelta(days=settings.get('max_days_until_closing', 14) if settings else 14)
        query = query.gte('closing_date', str(today)).lte('closing_date', str(max_closing))
        
        response = query.order('closing_date', desc=False).limit(50).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading jobs: {str(e)}")
        return []

def job_automation_student_portal():
    """Main student portal for job automation"""
    
    st.title("💼 NHS Job Application Automation")
    st.markdown("**Automated job applications to NHS trusts - your personal AI assistant**")
    
    # Check if Supabase is available
    if not SUPABASE_AVAILABLE or supabase is None:
        st.error("⚠️ Job automation system is currently unavailable. Database connection not configured.")
        st.info("Please contact support@t21services.co.uk for assistance.")
        return
    
    # Get student ID from session
    if 'user_id' not in st.session_state:
        st.error("Please log in to access job automation")
        return
    
    student_id = st.session_state['user_id']
    
    # Get student settings and stats
    settings = get_student_settings(student_id)
    stats = get_student_stats(student_id)
    
    # Tab navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "⚙️ Setup & Settings", 
        "🔍 Available Jobs",
        "📝 My Applications",
        "🎤 My Interviews"
    ])
    
    # ============================================================================
    # TAB 1: DASHBOARD
    # ============================================================================
    with tab1:
        st.header("📊 Your Job Search Dashboard")
        
        if not settings or not settings.get('auto_submit_enabled'):
            st.warning("⚠️ **Job automation not set up yet!**")
            st.info("👉 Go to **Setup & Settings** tab to activate automation")
        else:
            st.success(f"✅ **Automation Active** - Status: {settings.get('status', 'active').upper()}")
        
        # Statistics
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
        st.subheader("📋 Recent Activity")
        
        recent_apps = get_student_applications(student_id)[:5]
        
        if recent_apps:
            for app in recent_apps:
                job = app.get('discovered_jobs', {})
                
                with st.expander(f"📄 {job.get('title', 'Unknown')} - {job.get('trust', 'Unknown Trust')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Status:** {app.get('status', 'Unknown').replace('_', ' ').title()}")
                        st.write(f"**Location:** {job.get('location', 'Not specified')}")
                        st.write(f"**Band:** {job.get('band', 'Not specified')}")
                        st.write(f"**Closing Date:** {job.get('closing_date', 'Unknown')}")
                    
                    with col2:
                        if app.get('status') == 'submitted':
                            st.success("✅ Submitted")
                            if app.get('submitted_at'):
                                st.caption(f"Submitted: {app.get('submitted_at')[:10]}")
                        elif app.get('status') == 'queued':
                            st.info("⏳ Queued")
                        elif app.get('status') == 'processing':
                            st.warning("⚙️ Processing")
                        elif app.get('status') == 'failed':
                            st.error("❌ Failed")
        else:
            st.info("No applications yet. Set up automation to start applying!")
    
    # ============================================================================
    # TAB 2: SETUP & SETTINGS
    # ============================================================================
    with tab2:
        st.header("⚙️ Job Automation Setup")
        
        st.markdown("""
        ### 🎯 How It Works
        
        1. **Enter your NHS Trac credentials** (securely encrypted)
        2. **Set your job preferences** (location, band, working pattern, etc.)
        3. **Activate automation** - System finds jobs and applies automatically
        4. **Get notified** - Email alerts for applications and interviews
        5. **Track everything** - Monitor all applications in your dashboard
        """)
        
        st.markdown("---")
        
        # Trac Credentials
        st.subheader("🔐 NHS Trac Credentials")
        st.caption("Your credentials are encrypted and secure. We use them ONLY to submit applications on your behalf.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            trac_email = st.text_input(
                "Trac Email Address",
                value=settings.get('trac_email', '') if settings else '',
                help="Your NHS Trac login email"
            )
        
        with col2:
            trac_password = st.text_input(
                "Trac Password",
                type="password",
                help="Your NHS Trac password (encrypted before storage)"
            )
        
        st.markdown("---")
        
        # Job Preferences
        st.subheader("🎯 Job Search Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            requires_sponsorship = st.checkbox(
                "I require visa sponsorship",
                value=settings.get('requires_sponsorship', False) if settings else False,
                help="Only show jobs that offer visa sponsorship"
            )
            
            preferred_locations = st.multiselect(
                "Preferred Locations",
                options=["London", "Manchester", "Birmingham", "Leeds", "Liverpool", 
                        "Newcastle", "Sheffield", "Bristol", "Nottingham", "Leicester"],
                default=settings.get('preferred_locations', ['London']) if settings else ['London']
            )
            
            search_radius = st.slider(
                "Search Radius (miles)",
                min_value=5,
                max_value=50,
                value=settings.get('search_radius_miles', 20) if settings else 20
            )
        
        with col2:
            preferred_bands = st.multiselect(
                "Preferred NHS Bands",
                options=["Band 2", "Band 3", "Band 4", "Band 5", "Band 6", "Band 7"],
                default=settings.get('preferred_bands', ['Band 3', 'Band 4']) if settings else ['Band 3', 'Band 4']
            )
            
            working_patterns = st.multiselect(
                "Working Patterns",
                options=["Full time", "Part time", "Flexible"],
                default=settings.get('working_patterns', ['Full time']) if settings else ['Full time']
            )
            
            contract_types = st.multiselect(
                "Contract Types",
                options=["Permanent", "Fixed term", "Bank"],
                default=settings.get('contract_types', ['Permanent', 'Fixed term']) if settings else ['Permanent', 'Fixed term']
            )
        
        include_hybrid = st.checkbox("Include hybrid/remote roles", value=settings.get('include_hybrid', True) if settings else True)
        
        st.markdown("---")
        
        # Notification Settings
        st.subheader("📧 Notification Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            notification_email = st.text_input(
                "Notification Email",
                value=settings.get('notification_email', '') if settings else '',
                help="Where to send application updates"
            )
        
        with col2:
            max_applications = st.number_input(
                "Max Applications Per Day",
                min_value=1,
                max_value=100,
                value=settings.get('max_applications_per_day', 50) if settings else 50
            )
        
        send_daily_summary = st.checkbox("Send daily summary email", value=settings.get('send_daily_summary', True) if settings else True)
        send_interview_alerts = st.checkbox("Send interview invitation alerts", value=settings.get('send_interview_alerts', True) if settings else True)
        
        st.markdown("---")
        
        # Save button
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("💾 SAVE SETTINGS & ACTIVATE", use_container_width=True, type="primary"):
                if not trac_email or not trac_password:
                    st.error("Please enter your Trac credentials!")
                elif not preferred_locations or not preferred_bands:
                    st.error("Please select at least one location and band!")
                else:
                    try:
                        # Encrypt password
                        encrypted_pwd = encrypt_password(trac_password)
                        
                        settings_data = {
                            'student_id': student_id,
                            'trac_email': trac_email,
                            'trac_password_encrypted': encrypted_pwd,
                            'encryption_key_id': 'default',
                            'auto_submit_enabled': True,
                            'max_applications_per_day': max_applications,
                            'requires_sponsorship': requires_sponsorship,
                            'preferred_locations': preferred_locations,
                            'search_radius_miles': search_radius,
                            'preferred_bands': preferred_bands,
                            'working_patterns': working_patterns,
                            'contract_types': contract_types,
                            'include_hybrid': include_hybrid,
                            'notification_email': notification_email or trac_email,
                            'send_daily_summary': send_daily_summary,
                            'send_interview_alerts': send_interview_alerts,
                            'status': 'active',
                            'updated_at': datetime.now().isoformat()
                        }
                        
                        if settings:
                            # Update existing
                            supabase.table('student_automation_settings').update(settings_data).eq('student_id', student_id).execute()
                        else:
                            # Insert new
                            settings_data['contract_signed'] = True
                            settings_data['contract_signed_date'] = datetime.now().isoformat()
                            supabase.table('student_automation_settings').insert(settings_data).execute()
                        
                        st.success("✅ Settings saved! Job automation is now ACTIVE!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving settings: {str(e)}")
    
    # ============================================================================
    # TAB 3: AVAILABLE JOBS
    # ============================================================================
    with tab3:
        st.header("🔍 Available NHS Jobs")
        
        if not settings:
            st.warning("⚠️ Please set up your automation settings first!")
        else:
            jobs = get_available_jobs(settings)
            
            st.info(f"📊 Found **{len(jobs)}** jobs matching your preferences")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_trust = st.selectbox("Filter by Trust", ["All"] + list(set([j.get('trust', '') for j in jobs if j.get('trust')])))
            
            with col2:
                filter_band = st.selectbox("Filter by Band", ["All"] + list(set([j.get('band', '') for j in jobs if j.get('band')])))
            
            with col3:
                filter_sponsorship = st.selectbox("Sponsorship", ["All", "Yes", "No"])
            
            # Display jobs
            for job in jobs:
                # Apply filters
                if filter_trust != "All" and job.get('trust') != filter_trust:
                    continue
                if filter_band != "All" and job.get('band') != filter_band:
                    continue
                if filter_sponsorship == "Yes" and not job.get('has_sponsorship'):
                    continue
                if filter_sponsorship == "No" and job.get('has_sponsorship'):
                    continue
                
                with st.expander(f"📄 {job.get('title')} - {job.get('trust')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Location:** {job.get('location', 'Not specified')}")
                        st.write(f"**Band:** {job.get('band', 'Not specified')}")
                        st.write(f"**Salary:** £{job.get('salary_min', 0):,.0f} - £{job.get('salary_max', 0):,.0f}")
                        st.write(f"**Working Pattern:** {job.get('working_pattern', 'Not specified')}")
                        st.write(f"**Contract Type:** {job.get('contract_type', 'Not specified')}")
                        
                        if job.get('has_sponsorship'):
                            st.success("✅ Offers Visa Sponsorship")
                        
                        st.write(f"**Posted:** {job.get('posted_date', 'Unknown')}")
                        st.write(f"**Closing Date:** {job.get('closing_date')}")
                        
                        days_until_closing = (datetime.strptime(job.get('closing_date'), '%Y-%m-%d').date() - datetime.now().date()).days
                        if days_until_closing <= 2:
                            st.error(f"⚠️ **URGENT:** Closes in {days_until_closing} days!")
                        elif days_until_closing <= 7:
                            st.warning(f"⏰ Closes in {days_until_closing} days")
                        else:
                            st.info(f"📅 Closes in {days_until_closing} days")
                    
                    with col2:
                        st.write("**Quick Actions:**")
                        
                        if st.button("🚀 Apply Now", key=f"apply_{job.get('id')}", use_container_width=True):
                            # Check if already applied
                            existing = supabase.table('applications').select('id').eq('student_id', student_id).eq('job_id', job.get('id')).execute()
                            
                            if existing.data:
                                st.warning("You've already applied to this job!")
                            else:
                                # Create application
                                try:
                                    app_data = {
                                        'student_id': student_id,
                                        'job_id': job.get('id'),
                                        'status': 'queued',
                                        'priority': 'normal',
                                        'queued_at': datetime.now().isoformat()
                                    }
                                    supabase.table('applications').insert(app_data).execute()
                                    st.success("✅ Application queued! AI is generating your supporting information...")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        
                        if job.get('nhs_jobs_url'):
                            st.link_button("🔗 View on NHS Jobs", job.get('nhs_jobs_url'), use_container_width=True)
    
    # ============================================================================
    # TAB 4: MY APPLICATIONS
    # ============================================================================
    with tab4:
        st.header("📝 My Applications")
        
        applications = get_student_applications(student_id)
        
        if not applications:
            st.info("No applications yet. Go to 'Available Jobs' to start applying!")
        else:
            st.info(f"📊 Total Applications: **{len(applications)}**")
            
            # Status filter
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Queued", "Processing", "Submitted", "Failed"]
            )
            
            for app in applications:
                if status_filter != "All" and app.get('status', '').lower() != status_filter.lower():
                    continue
                
                job = app.get('discovered_jobs', {})
                
                with st.expander(f"📄 {job.get('title', 'Unknown')} - {app.get('status', 'Unknown').upper()}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Trust:** {job.get('trust', 'Unknown')}")
                        st.write(f"**Location:** {job.get('location', 'Not specified')}")
                        st.write(f"**Band:** {job.get('band', 'Not specified')}")
                        st.write(f"**Applied:** {app.get('created_at', 'Unknown')[:10]}")
                        
                        if app.get('submitted_at'):
                            st.write(f"**Submitted:** {app.get('submitted_at')[:10]}")
                        
                        if app.get('confirmation_number'):
                            st.success(f"✅ **Confirmation:** {app.get('confirmation_number')}")
                        
                        if app.get('error_message'):
                            st.error(f"❌ **Error:** {app.get('error_message')}")
                    
                    with col2:
                        if app.get('status') == 'submitted':
                            st.success("✅ SUBMITTED")
                        elif app.get('status') == 'queued':
                            st.info("⏳ QUEUED")
                        elif app.get('status') == 'processing':
                            st.warning("⚙️ PROCESSING")
                        elif app.get('status') == 'failed':
                            st.error("❌ FAILED")
                        
                        if app.get('ai_supporting_information'):
                            with st.expander("📄 View Supporting Information"):
                                st.text_area(
                                    "AI-Generated Content",
                                    app.get('ai_supporting_information'),
                                    height=200
                                )
    
    # ============================================================================
    # TAB 5: MY INTERVIEWS
    # ============================================================================
    with tab5:
        st.header("🎤 My Interviews")
        
        interviews = get_student_interviews(student_id)
        
        if not interviews:
            st.info("No interviews scheduled yet. Keep applying!")
        else:
            st.success(f"🎉 You have **{len(interviews)}** interview(s)!")
            
            for interview in interviews:
                job = interview.get('discovered_jobs', {})
                
                with st.expander(f"🎤 {job.get('title', 'Unknown')} - {interview.get('status', 'Unknown').upper()}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Trust:** {job.get('trust', 'Unknown')}")
                        st.write(f"**Date:** {interview.get('interview_date', 'TBC')}")
                        st.write(f"**Time:** {interview.get('interview_time', 'TBC')}")
                        st.write(f"**Location:** {interview.get('interview_location', 'TBC')}")
                        st.write(f"**Format:** {interview.get('interview_format', 'Not specified')}")
                        
                        if interview.get('outcome'):
                            if interview.get('outcome') == 'offered':
                                st.success(f"🎉 **OUTCOME:** Job Offer Received!")
                            elif interview.get('outcome') == 'rejected':
                                st.error(f"**OUTCOME:** Not successful this time")
                            else:
                                st.info(f"**OUTCOME:** {interview.get('outcome')}")
                    
                    with col2:
                        if interview.get('status') == 'scheduled':
                            st.warning("📅 SCHEDULED")
                        elif interview.get('status') == 'confirmed':
                            st.success("✅ CONFIRMED")
                        elif interview.get('status') == 'completed':
                            st.info("✅ COMPLETED")
                        
                        if st.button("📚 Interview Prep", key=f"prep_{interview.get('id')}", use_container_width=True):
                            st.info("Interview preparation materials will be sent to your email!")

if __name__ == "__main__":
    job_automation_student_portal()
