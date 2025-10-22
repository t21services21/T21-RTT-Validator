"""
SIMPLE TEST - Create jobs and applications directly
No complex imports, no scraping, just direct database operations
"""

import streamlit as st
from datetime import datetime, timedelta
from supabase_database import supabase, SUPABASE_AVAILABLE

def simple_automation_test():
    """Simple test that definitely works"""
    
    st.title("🧪 Simple Automation Test")
    st.info("This bypasses all complex code and does it simply")
    
    if not SUPABASE_AVAILABLE or supabase is None:
        st.error("❌ Database not connected")
        st.info("Check SUPABASE_URL and SUPABASE_KEY in secrets")
        return
    
    st.success("✅ Database connected!")
    
    # Show current state
    st.subheader("📊 Current State")
    
    try:
        students = supabase.table('student_automation_settings').select('*').execute()
        jobs = supabase.table('discovered_jobs').select('*').execute()
        apps = supabase.table('applications').select('*').execute()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Students", len(students.data) if students.data else 0)
        with col2:
            st.metric("Jobs", len(jobs.data) if jobs.data else 0)
        with col3:
            st.metric("Applications", len(apps.data) if apps.data else 0)
    
    except Exception as e:
        st.error(f"❌ Error reading database: {str(e)}")
        return
    
    st.markdown("---")
    
    # Step 1: Add a test job
    st.subheader("1️⃣ Add Test Job")
    
    if st.button("➕ Add One Test Job"):
        try:
            job_data = {
                'title': 'Test RTT Administrator',
                'trust': 'Test Hospital',
                'location': 'London', 
                'band': 'Band 3',
                'salary_min': 25000,
                'salary_max': 30000,
                'closing_date': (datetime.now() + timedelta(days=14)).isoformat(),
                'nhs_jobs_url': 'https://test.com/job1',
                'job_reference': f'SIMPLE-TEST-{int(datetime.now().timestamp())}',
                'discovered_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            result = supabase.table('discovered_jobs').insert(job_data).execute()
            
            if result.data:
                st.success(f"✅ Added job: {result.data[0]['title']}")
                st.json(result.data[0])
                st.rerun()
            else:
                st.error("❌ Failed to add job - no data returned")
                
        except Exception as e:
            st.error(f"❌ Error adding job: {str(e)}")
            st.code(str(e))
    
    # Step 2: Create application
    if jobs.data and len(jobs.data) > 0:
        st.subheader("2️⃣ Create Application")
        
        # Get student
        if students.data and len(students.data) > 0:
            student = students.data[0]
            job = jobs.data[0]
            
            st.info(f"Will create application for: {student.get('users', {}).get('email', 'Unknown')} → {job['title']}")
            
            if st.button("➕ Create One Application"):
                try:
                    app_data = {
                        'student_id': student['student_id'],
                        'job_id': job['id'],
                        'status': 'queued',
                        'ai_supporting_information': 'This is a test application created directly. I am interested in this RTT position and have completed T21 training.',
                        'ai_word_count': 20,
                        'ai_generation_time': 0.1,
                        'priority': 'normal',
                        'attempts': 0,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    result = supabase.table('applications').insert(app_data).execute()
                    
                    if result.data:
                        st.success(f"✅ Created application!")
                        st.json(result.data[0])
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to create application")
                        
                except Exception as e:
                    st.error(f"❌ Error creating application: {str(e)}")
                    st.code(str(e))
        else:
            st.warning("⚠️ No students found - add a student first")
    
    else:
        st.info("ℹ️ Add a job first to create applications")
    
    # Step 3: Show results
    st.subheader("3️⃣ Results")
    
    if apps.data and len(apps.data) > 0:
        st.success(f"🎉 SUCCESS! {len(apps.data)} applications created")
        
        for app in apps.data:
            with st.expander(f"📝 Application #{app['id'][:8]}"):
                st.write(f"**Student ID:** {app['student_id']}")
                st.write(f"**Job ID:** {app['job_id']}")
                st.write(f"**Status:** {app['status']}")
                st.write(f"**Supporting Info:** {app['ai_supporting_information']}")
                st.write(f"**Created:** {app['created_at']}")
    else:
        st.info("No applications yet")
    
    # Debug info
    with st.expander("🔍 Debug Info"):
        st.write("**Students data:**")
        st.json(students.data if students.data else [])
        st.write("**Jobs data:**")
        st.json(jobs.data if jobs.data else [])
        st.write("**Applications data:**") 
        st.json(apps.data if apps.data else [])

if __name__ == "__main__":
    simple_automation_test()
