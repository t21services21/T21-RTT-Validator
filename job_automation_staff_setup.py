"""
NHS JOB APPLICATION AUTOMATION - STAFF CONTROL CENTER
Staff manages ALL student job automation
Students only VIEW results (no setup access)
"""

import streamlit as st
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
        st.error("⚠️ Encryption key not configured.")
        return None

def job_automation_staff_control():
    """Complete staff control center for job automation"""
    
    st.title("💼 NHS Job Automation - Staff Control Center")
    st.markdown("**Complete control over all student job applications**")
    
    # Check if Supabase is available
    if not SUPABASE_AVAILABLE or supabase is None:
        st.error("⚠️ Job automation system is currently unavailable.")
        return
    
    # Admin info
    user_email = st.session_state.get('user_email', '')
    if 'admin' in user_email.lower() or 'super_admin' in str(st.session_state.get('user_license', '')).lower():
        st.success("👑 **ADMIN ACCESS:** You can manage students, view all applications, monitor staff activity, and control the entire system")
    else:
        st.info("👥 **STAFF ACCESS:** You can manage students and monitor job applications")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "➕ Add Students",
        "👥 Manage Students",
        "📝 Application Queue",
        "🎤 Interviews",
        "📊 Analytics",
        "⚙️ System Settings",
        "🎮 Manual Runner"
    ])
    
    # ============================================================================
    # TAB 1: ADD STUDENTS (Staff adds/imports students)
    # ============================================================================
    with tab1:
        st.header("➕ Add Students to Job Automation")
        
        st.info("💡 **Staff controls everything:** You add students, set preferences, manage credentials")
        
        # Method selection
        method = st.radio("How do you want to add students?", 
                         ["📝 Single Student", "📊 Bulk Upload (Excel)"],
                         horizontal=True)
        
        if method == "📝 Single Student":
            st.subheader("Add Individual Student")
            
            col1, col2 = st.columns(2)
            
            with col1:
                student_email = st.text_input("Student Email", placeholder="student@example.com")
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
            
            with col2:
                trac_email = st.text_input("Student's Trac Email", placeholder="trac@nhs.net")
                trac_password = st.text_input("Student's Trac Password", type="password")
                notification_email = st.text_input("Notification Email (optional)", placeholder="Same as student email")
            
            st.markdown("---")
            st.subheader("🎯 Job Preferences")
            
            col1, col2 = st.columns(2)
            
            with col1:
                requires_sponsorship = st.checkbox("Requires Visa Sponsorship")
                
                preferred_locations = st.multiselect(
                    "Preferred Locations",
                    ["London", "Manchester", "Birmingham", "Leeds", "Liverpool", 
                     "Newcastle", "Sheffield", "Bristol", "Nottingham", "Leicester"],
                    default=["London"]
                )
                
                search_radius = st.slider("Search Radius (miles)", 5, 50, 20)
            
            with col2:
                preferred_bands = st.multiselect(
                    "Preferred NHS Bands",
                    ["Band 2", "Band 3", "Band 4", "Band 5", "Band 6"],
                    default=["Band 3", "Band 4"]
                )
                
                working_patterns = st.multiselect(
                    "Working Patterns",
                    ["Full time", "Part time", "Flexible"],
                    default=["Full time"]
                )
                
                max_applications_per_day = st.number_input("Max Applications Per Day", 1, 100, 50)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                if st.button("✅ ADD STUDENT & ACTIVATE", use_container_width=True, type="primary"):
                    if not student_email or not trac_email or not trac_password:
                        st.error("Please fill in all required fields!")
                    else:
                        try:
                            # 1. Get student from existing users table
                            # Staff enters email of EXISTING student account
                            user_check = supabase.table('users').select('id').eq('email', student_email).execute()
                            
                            if user_check.data:
                                student_id = user_check.data[0]['id']
                                
                                # Check if this student already has automation set up
                                existing_check = supabase.table('student_automation_settings').select('id').eq('student_id', student_id).execute()
                                if existing_check.data:
                                    st.warning(f"⚠️ Automation already exists for {student_email}")
                                    st.info("Go to 'Manage Students' tab to edit existing settings")
                                    return
                            else:
                                st.error(f"❌ Student account not found for {student_email}")
                                st.info("💡 Student must create an account first before you can set up job automation")
                                st.info("Ask student to register at the platform, then come back here to activate automation")
                                return
                            
                            # 2. Encrypt password
                            encrypted_pwd = encrypt_password(trac_password)
                            
                            if not encrypted_pwd:
                                st.error("Failed to encrypt password")
                                return
                            
                            # 3. Create automation settings
                            settings_data = {
                                'student_id': student_id,
                                'trac_email': trac_email,
                                'trac_password_encrypted': encrypted_pwd,
                                'encryption_key_id': 'default',
                                'auto_submit_enabled': True,
                                'max_applications_per_day': max_applications_per_day,
                                'requires_sponsorship': requires_sponsorship,
                                'preferred_locations': preferred_locations,
                                'search_radius_miles': search_radius,
                                'preferred_bands': preferred_bands,
                                'working_patterns': working_patterns,
                                'notification_email': notification_email or student_email,
                                'send_daily_summary': True,
                                'send_interview_alerts': True,
                                'status': 'active',
                                'contract_signed': True,
                                'contract_signed_date': datetime.now().isoformat(),
                                'created_at': datetime.now().isoformat()
                            }
                            
                            supabase.table('student_automation_settings').insert(settings_data).execute()
                            
                            st.success(f"✅ Student added successfully! Automation is now ACTIVE for {first_name} {last_name}")
                            st.balloons()
                            st.info(f"📧 {first_name} will receive email notifications at: {notification_email or student_email}")
                            
                        except Exception as e:
                            st.error(f"Error adding student: {str(e)}")
        
        else:
            # Bulk upload
            st.subheader("📊 Bulk Upload Students (Excel)")
            
            st.markdown("""
            ### 📝 Excel Template Format
            
            Your Excel file should have these columns:
            - **email** - Student email
            - **first_name** - First name
            - **last_name** - Last name
            - **trac_email** - NHS Trac email
            - **trac_password** - NHS Trac password
            - **requires_sponsorship** - TRUE/FALSE
            - **preferred_locations** - Comma-separated (e.g., "London,Manchester")
            - **preferred_bands** - Comma-separated (e.g., "Band 3,Band 4")
            """)
            
            # Download template
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                template_df = pd.DataFrame({
                    'email': ['student1@example.com'],
                    'first_name': ['John'],
                    'last_name': ['Smith'],
                    'trac_email': ['john.smith@nhs.net'],
                    'trac_password': ['password123'],
                    'requires_sponsorship': [False],
                    'preferred_locations': ['London,Manchester'],
                    'preferred_bands': ['Band 3,Band 4']
                })
                
                csv = template_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Template",
                    csv,
                    "job_automation_template.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Upload file
            uploaded_file = st.file_uploader("Upload Student List (Excel/CSV)", type=['xlsx', 'csv'])
            
            if uploaded_file:
                try:
                    # Read file
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.success(f"✅ File loaded: {len(df)} students found")
                    st.dataframe(df.head())
                    
                    if st.button("🚀 IMPORT ALL STUDENTS & ACTIVATE", type="primary", use_container_width=True):
                        success_count = 0
                        error_count = 0
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, row in df.iterrows():
                            try:
                                status_text.text(f"Processing {row['first_name']} {row['last_name']}...")
                                
                                # Check if student account exists
                                user_check = supabase.table('users').select('id').eq('email', row['email']).execute()
                                
                                if user_check.data:
                                    student_id = user_check.data[0]['id']
                                else:
                                    st.warning(f"⚠️ Skipping {row['email']} - account not found. Student must register first.")
                                    error_count += 1
                                    continue
                                
                                # Encrypt password
                                encrypted_pwd = encrypt_password(row['trac_password'])
                                
                                # Parse locations and bands
                                locations = [loc.strip() for loc in str(row['preferred_locations']).split(',')]
                                bands = [band.strip() for band in str(row['preferred_bands']).split(',')]
                                
                                # Create settings
                                settings_data = {
                                    'student_id': student_id,
                                    'trac_email': row['trac_email'],
                                    'trac_password_encrypted': encrypted_pwd,
                                    'encryption_key_id': 'default',
                                    'auto_submit_enabled': True,
                                    'max_applications_per_day': 50,
                                    'requires_sponsorship': bool(row.get('requires_sponsorship', False)),
                                    'preferred_locations': locations,
                                    'search_radius_miles': 20,
                                    'preferred_bands': bands,
                                    'working_patterns': ['Full time'],
                                    'notification_email': row['email'],
                                    'send_daily_summary': True,
                                    'send_interview_alerts': True,
                                    'status': 'active',
                                    'contract_signed': True,
                                    'contract_signed_date': datetime.now().isoformat()
                                }
                                
                                supabase.table('student_automation_settings').insert(settings_data).execute()
                                success_count += 1
                                
                            except Exception as e:
                                st.error(f"Error with {row.get('email', 'unknown')}: {str(e)}")
                                error_count += 1
                            
                            progress_bar.progress((idx + 1) / len(df))
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.success(f"🎉 Import Complete! ✅ {success_count} students added, ❌ {error_count} errors")
                        st.balloons()
                        
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
    
    # ============================================================================
    # TAB 2: MANAGE STUDENTS
    # ============================================================================
    with tab2:
        st.header("👥 Manage Student Automation")
        
        try:
            # Get all students with automation
            students = supabase.table('student_automation_settings').select('*, users(email)').execute()
            
            if not students.data:
                st.info("No students added yet. Go to 'Add Students' tab to get started!")
            else:
                st.success(f"📊 **{len(students.data)}** students with automation active")
                
                for student in students.data:
                    user = student.get('users', {})
                    
                    with st.expander(f"👤 {user.get('email', 'Unknown Student')}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write("**Settings:**")
                            st.write(f"Status: {student.get('status', 'Unknown').upper()}")
                            st.write(f"Trac Email: {student.get('trac_email', 'N/A')}")
                            if student.get('requires_sponsorship'):
                                st.write("✓ Sponsorship Required")
                        
                        with col2:
                            st.write("**Preferences:**")
                            st.write(f"Locations: {', '.join(student.get('preferred_locations', []))}")
                            st.write(f"Bands: {', '.join(student.get('preferred_bands', []))}")
                        
                        with col3:
                            st.write("**Actions:**")
                            
                            if student.get('status') == 'active':
                                if st.button("⏸️ Pause", key=f"pause_{student.get('id')}", use_container_width=True):
                                    supabase.table('student_automation_settings').update({'status': 'paused'}).eq('id', student.get('id')).execute()
                                    st.success("Paused")
                                    st.rerun()
                            else:
                                if st.button("▶️ Resume", key=f"resume_{student.get('id')}", use_container_width=True):
                                    supabase.table('student_automation_settings').update({'status': 'active'}).eq('id', student.get('id')).execute()
                                    st.success("Resumed")
                                    st.rerun()
                            
                            if st.button("✏️ Edit", key=f"edit_{student.get('id')}", use_container_width=True):
                                st.info("Edit functionality coming soon!")
                            
                            if st.button("🗑️ Remove", key=f"remove_{student.get('id')}", use_container_width=True):
                                supabase.table('student_automation_settings').delete().eq('id', student.get('id')).execute()
                                st.success("Removed")
                                st.rerun()
        
        except Exception as e:
            st.error(f"Error loading students: {str(e)}")
    
    # ============================================================================
    # TAB 3: APPLICATION QUEUE
    # ============================================================================
    with tab3:
        st.header("📝 Application Queue")
        
        try:
            # Get all queued and processing applications
            apps = supabase.table('applications').select('*, users(email), discovered_jobs(*)').in_('status', ['queued', 'processing']).order('created_at', desc=True).execute()
            
            if not apps.data:
                st.info("📭 No applications in queue. Applications will appear here once the backend scraper finds jobs!")
                st.markdown("""
                ### How it works:
                1. Backend scraper finds matching NHS jobs (every 6 hours)
                2. AI generates supporting information (every hour)
                3. Applications appear here in "queued" status
                4. Auto-submitter submits them to NHS Trac (every 30 minutes)
                5. Status changes to "submitted"
                
                **Note:** Backend processes are not running yet. See documentation for setup.
                """)
            else:
                st.success(f"📊 **{len(apps.data)}** applications in queue")
                
                for app in apps.data:
                    user = app.get('users', {})
                    job = app.get('discovered_jobs', {})
                    
                    status_emoji = {
                        'queued': '⏳',
                        'processing': '⚙️',
                        'submitted': '✅',
                        'failed': '❌'
                    }.get(app.get('status', 'unknown'), '❓')
                    
                    with st.expander(f"{status_emoji} {user.get('email', 'Unknown')} → {job.get('title', 'Unknown Job')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Student:** {user.get('email', 'Unknown')}")
                            st.write(f"**Job:** {job.get('title', 'Unknown')}")
                            st.write(f"**Trust:** {job.get('trust', 'Unknown')}")
                            st.write(f"**Location:** {job.get('location', 'Unknown')}")
                            st.write(f"**Status:** {app.get('status', 'Unknown').upper()}")
                        
                        with col2:
                            st.write(f"**Created:** {app.get('created_at', 'Unknown')[:10]}")
                            st.write(f"**Priority:** {app.get('priority', 'normal')}")
                            st.write(f"**Attempts:** {app.get('attempts', 0)}")
                            
                            if job.get('closing_date'):
                                st.write(f"**Closes:** {job.get('closing_date')[:10]}")
                        
                        if app.get('ai_supporting_information'):
                            with st.expander("📄 View AI-Generated Content"):
                                st.text_area("Supporting Information", app.get('ai_supporting_information'), height=200, disabled=True)
        
        except Exception as e:
            st.error(f"Error loading application queue: {str(e)}")
    
    # ============================================================================
    # TAB 4: INTERVIEWS
    # ============================================================================
    with tab4:
        st.header("🎤 Interview Calendar")
        
        try:
            # Get all interviews
            interviews = supabase.table('interviews').select('*, users(email), discovered_jobs(*)').order('interview_date', desc=True).execute()
            
            if not interviews.data:
                st.info("📭 No interviews scheduled yet. Once students get interview invitations, they'll appear here!")
            else:
                st.success(f"🎉 **{len(interviews.data)}** interview(s) scheduled!")
                
                # Group by status
                scheduled = [i for i in interviews.data if i.get('status') in ['scheduled', 'confirmed']]
                completed = [i for i in interviews.data if i.get('status') == 'completed']
                
                tab_upcoming, tab_completed = st.tabs([f"📅 Upcoming ({len(scheduled)})", f"✅ Completed ({len(completed)})"])
                
                with tab_upcoming:
                    if scheduled:
                        for interview in scheduled:
                            user = interview.get('users', {})
                            job = interview.get('discovered_jobs', {})
                            
                            with st.expander(f"🎤 {user.get('email', 'Unknown')} - {job.get('title', 'Unknown')}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Student:** {user.get('email', 'Unknown')}")
                                    st.write(f"**Job:** {job.get('title', 'Unknown')}")
                                    st.write(f"**Trust:** {job.get('trust', 'Unknown')}")
                                    st.write(f"**Date:** {interview.get('interview_date', 'TBC')[:10] if interview.get('interview_date') else 'TBC'}")
                                    st.write(f"**Time:** {interview.get('interview_time', 'TBC')}")
                                
                                with col2:
                                    st.write(f"**Format:** {interview.get('interview_format', 'Not specified')}")
                                    st.write(f"**Location:** {interview.get('interview_location', 'TBC')}")
                                    st.write(f"**Status:** {interview.get('status', 'Unknown').upper()}")
                    else:
                        st.info("No upcoming interviews")
                
                with tab_completed:
                    if completed:
                        for interview in completed:
                            user = interview.get('users', {})
                            job = interview.get('discovered_jobs', {})
                            
                            outcome = interview.get('outcome', 'pending')
                            if outcome == 'offered':
                                outcome_emoji = "🎉"
                            elif outcome == 'rejected':
                                outcome_emoji = "❌"
                            else:
                                outcome_emoji = "⏳"
                            
                            with st.expander(f"{outcome_emoji} {user.get('email', 'Unknown')} - {job.get('title', 'Unknown')}"):
                                st.write(f"**Outcome:** {outcome.upper()}")
                                st.write(f"**Date:** {interview.get('interview_date', 'Unknown')[:10] if interview.get('interview_date') else 'Unknown'}")
                    else:
                        st.info("No completed interviews yet")
        
        except Exception as e:
            st.error(f"Error loading interviews: {str(e)}")
    
    # ============================================================================
    # TAB 5: ANALYTICS
    # ============================================================================
    with tab5:
        st.header("📊 Analytics & Reporting")
        
        try:
            # Get overview statistics
            total_students = supabase.table('student_automation_settings').select('id', count='exact').execute()
            total_apps = supabase.table('applications').select('id', count='exact').execute()
            total_interviews = supabase.table('interviews').select('id', count='exact').execute()
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Active Students", total_students.count if total_students else 0)
            
            with col2:
                st.metric("📬 Total Applications", total_apps.count if total_apps else 0)
            
            with col3:
                st.metric("🎤 Total Interviews", total_interviews.count if total_interviews else 0)
            
            with col4:
                if total_apps.count and total_apps.count > 0:
                    success_rate = (total_interviews.count / total_apps.count) * 100 if total_interviews else 0
                    st.metric("📈 Success Rate", f"{success_rate:.1f}%")
                else:
                    st.metric("📈 Success Rate", "0.0%")
            
            st.markdown("---")
            
            st.info("""
            ### 📊 Full Analytics Coming Soon
            
            This section will include:
            - 📈 Application trends over time
            - 🎯 Success rates by location/trust
            - 📊 Student performance rankings
            - 🏥 Most successful job types
            - 📅 Interview conversion rates
            - 💼 Offer acceptance rates
            
            **Note:** Analytics require historical data. Once applications start flowing, charts and insights will appear here!
            """)
        
        except Exception as e:
            st.error(f"Error loading analytics: {str(e)}")
    
    # ============================================================================
    # TAB 6: SYSTEM SETTINGS
    # ============================================================================
    with tab6:
        st.header("⚙️ System Settings")
        
        st.warning("🔐 **Super Admin Only:** These settings affect the entire job automation system")
        
        try:
            # Get current system config
            config = supabase.table('system_config').select('*').execute()
            
            if config.data:
                current_config = config.data[0]
            else:
                current_config = {
                    'scraper_interval_hours': 6,
                    'max_concurrent_applications': 10,
                    'rate_limit_per_hour': 50,
                    'ai_model': 'gpt-4',
                    'enable_auto_submit': True,
                    'enable_interview_detection': True
                }
            
            st.subheader("🤖 Automation Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                scraper_interval = st.number_input(
                    "Scraper Interval (hours)",
                    min_value=1,
                    max_value=24,
                    value=current_config.get('scraper_interval_hours', 6),
                    help="How often to scrape NHS Jobs for new positions"
                )
                
                max_concurrent = st.number_input(
                    "Max Concurrent Applications",
                    min_value=1,
                    max_value=50,
                    value=current_config.get('max_concurrent_applications', 10),
                    help="Maximum applications to process simultaneously"
                )
            
            with col2:
                rate_limit = st.number_input(
                    "Rate Limit (per hour)",
                    min_value=10,
                    max_value=200,
                    value=current_config.get('rate_limit_per_hour', 50),
                    help="Maximum requests to NHS Jobs per hour"
                )
                
                ai_model = st.selectbox(
                    "AI Model",
                    ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
                    index=0 if current_config.get('ai_model') == 'gpt-4' else 2
                )
            
            st.markdown("---")
            
            st.subheader("🔧 Feature Toggles")
            
            col1, col2 = st.columns(2)
            
            with col1:
                enable_auto_submit = st.checkbox(
                    "Enable Auto-Submit",
                    value=current_config.get('enable_auto_submit', True),
                    help="Automatically submit applications to NHS Trac"
                )
            
            with col2:
                enable_interview_detection = st.checkbox(
                    "Enable Interview Detection",
                    value=current_config.get('enable_interview_detection', True),
                    help="Automatically detect interview invitations from emails"
                )
            
            st.markdown("---")
            
            if st.button("💾 Save System Settings", type="primary"):
                new_config = {
                    'scraper_interval_hours': scraper_interval,
                    'max_concurrent_applications': max_concurrent,
                    'rate_limit_per_hour': rate_limit,
                    'ai_model': ai_model,
                    'enable_auto_submit': enable_auto_submit,
                    'enable_interview_detection': enable_interview_detection,
                    'updated_at': datetime.now().isoformat()
                }
                
                if config.data:
                    # Update existing
                    supabase.table('system_config').update(new_config).eq('id', config.data[0]['id']).execute()
                else:
                    # Insert new
                    supabase.table('system_config').insert(new_config).execute()
                
                st.success("✅ System settings saved!")
                st.rerun()
        
        except Exception as e:
            st.error(f"Error loading system settings: {str(e)}")
    
    # ============================================================================
    # TAB 7: MANUAL RUNNER
    # ============================================================================
    with tab7:
        st.header("🎮 Manual Automation Runner")
        st.info("""
        ⚠️ **Installing required packages...**
        
        The manual runner requires:
        - `beautifulsoup4` (for web scraping)
        - `cryptography` (for password encryption)
        
        **Status:** Installing packages via requirements.txt
        
        **ETA:** 2-3 minutes after you push the updated requirements.txt
        
        **To enable:**
        1. Push the updated requirements.txt
        2. Wait for Streamlit to redeploy
        3. Refresh this page
        
        Meanwhile, you can:
        - ✅ Add students
        - ✅ Manage students  
        - ✅ View other tabs
        """)

if __name__ == "__main__":
    job_automation_staff_control()
