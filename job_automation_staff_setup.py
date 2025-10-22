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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "➕ Add Students",
        "👥 Manage Students",
        "📝 Application Queue",
        "🎤 Interviews",
        "📊 Analytics",
        "⚙️ System Settings"
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
                            # 1. Find or create student in users table
                            user_check = supabase.table('users').select('id').eq('email', student_email).execute()
                            
                            if user_check.data:
                                student_id = user_check.data[0]['id']
                            else:
                                # Create student account
                                new_user = {
                                    'email': student_email,
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'role': 'student',
                                    'created_at': datetime.now().isoformat()
                                }
                                result = supabase.table('users').insert(new_user).execute()
                                student_id = result.data[0]['id']
                            
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
                                
                                # Create user
                                user_check = supabase.table('users').select('id').eq('email', row['email']).execute()
                                
                                if user_check.data:
                                    student_id = user_check.data[0]['id']
                                else:
                                    new_user = {
                                        'email': row['email'],
                                        'first_name': row['first_name'],
                                        'last_name': row['last_name'],
                                        'role': 'student',
                                        'created_at': datetime.now().isoformat()
                                    }
                                    result = supabase.table('users').insert(new_user).execute()
                                    student_id = result.data[0]['id']
                                
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
            students = supabase.table('student_automation_settings').select('*, users(email, first_name, last_name)').execute()
            
            if not students.data:
                st.info("No students added yet. Go to 'Add Students' tab to get started!")
            else:
                st.success(f"📊 **{len(students.data)}** students with automation active")
                
                for student in students.data:
                    user = student.get('users', {})
                    
                    with st.expander(f"👤 {user.get('first_name', '')} {user.get('last_name', '')} - {user.get('email', '')}"):
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
    # TAB 3-6: Use existing staff dashboard functionality
    # ============================================================================
    with tab3:
        st.header("📝 Application Queue")
        st.info("Application monitoring - Coming from main staff dashboard")
    
    with tab4:
        st.header("🎤 Interviews")
        st.info("Interview calendar - Coming from main staff dashboard")
    
    with tab5:
        st.header("📊 Analytics")
        st.info("Analytics and reporting - Coming from main staff dashboard")
    
    with tab6:
        st.header("⚙️ System Settings")
        st.info("Global system configuration - Coming from main staff dashboard")

if __name__ == "__main__":
    job_automation_staff_control()
