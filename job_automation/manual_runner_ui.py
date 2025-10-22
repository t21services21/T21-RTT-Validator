"""
MANUAL AUTOMATION RUNNER UI
Allows admins to manually trigger the automation cycle from Streamlit
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_automation.nhs_jobs_scraper import scrape_jobs_for_all_students
from job_automation.ai_application_generator import generate_applications_for_all_students
from supabase_database import supabase, SUPABASE_AVAILABLE

def render_manual_runner():
    """Render the manual automation runner interface"""
    
    st.title("🎮 Manual Automation Runner")
    st.markdown("**Manually trigger the job automation cycle**")
    
    if not SUPABASE_AVAILABLE or supabase is None:
        st.error("❌ Database not available")
        return
    
    # Get system status
    students = supabase.table('student_automation_settings').select('id', count='exact').eq('status', 'active').execute()
    jobs = supabase.table('discovered_jobs').select('id', count='exact').execute()
    apps = supabase.table('applications').select('id', count='exact').execute()
    queued = supabase.table('applications').select('id', count='exact').eq('status', 'queued').execute()
    submitted = supabase.table('applications').select('id', count='exact').eq('status', 'submitted').execute()
    
    # Status cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Active Students", students.count if students else 0)
    
    with col2:
        # Refresh job count
        jobs = supabase.table('discovered_jobs').select('id', count='exact').execute()
        st.metric("💼 Discovered Jobs", jobs.count if jobs else 0)
    
    with col3:
        # Refresh app count
        apps = supabase.table('applications').select('id', count='exact').execute()
        st.metric("📝 Total Applications", apps.count if apps else 0)
    
    with col4:
        # Refresh submitted count
        submitted = supabase.table('applications').select('id', count='exact').eq('status', 'submitted').execute()
        st.metric("✅ Submitted", submitted.count if submitted else 0)
    
    st.markdown("---")
    
    # Manual controls
    st.subheader("🎮 Manual Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1️⃣ Scrape Jobs")
        st.info("Find new NHS jobs matching student preferences")
        
        if st.button("🔍 RUN SCRAPER", use_container_width=True, type="primary"):
            with st.spinner("Scraping NHS Jobs..."):
                progress_container = st.empty()
                
                with progress_container.container():
                    st.write("🔍 Searching NHS Jobs website...")
                    
                    try:
                        # Run scraper
                        scrape_jobs_for_all_students()
                        
                        # Refresh counts
                        jobs_after = supabase.table('discovered_jobs').select('id', count='exact').execute()
                        new_jobs = (jobs_after.count if jobs_after else 0) - (jobs.count if jobs else 0)
                        
                        st.success(f"✅ Scraping complete! Found {new_jobs} new jobs")
                        st.balloons()
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Scraping failed: {str(e)}")
    
    with col2:
        st.markdown("### 2️⃣ Generate Applications")
        st.info("Use AI to create supporting information")
        
        # Check if there are jobs to apply for
        jobs_count = supabase.table('discovered_jobs').select('id', count='exact').execute()
        if jobs_count.count == 0:
            st.warning("⚠️ No jobs in database. Add test jobs first!")
        
        if st.button("🤖 RUN AI GENERATOR", use_container_width=True, type="primary"):
            if jobs_count.count == 0:
                st.error("❌ No jobs to apply for! Click 'ADD TEST JOBS' first.")
            else:
                with st.spinner("Generating AI applications..."):
                    progress_container = st.empty()
                    
                    with progress_container.container():
                        st.write("🤖 Generating applications with GPT-4...")
                        
                        try:
                            # Check OpenAI key
                            api_key = st.secrets.get("OPENAI_API_KEY")
                            if not api_key:
                                st.error("❌ OpenAI API key not configured!")
                                st.info("Add OPENAI_API_KEY to Streamlit secrets")
                                return
                            
                            # Run generator
                            generate_applications_for_all_students()
                            
                            # Refresh counts
                            apps_after = supabase.table('applications').select('id', count='exact').execute()
                            new_apps = (apps_after.count if apps_after else 0) - (apps.count if apps else 0)
                            
                            st.success(f"✅ Generation complete! Created {new_apps} applications")
                            st.balloons()
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Generation failed: {str(e)}")
    
    with col3:
        st.markdown("### 3️⃣ Submit to Trac")
        st.info("Submit queued applications to NHS Trac")
        
        st.warning("⚠️ Requires Playwright")
        
        if queued.count and queued.count > 0:
            st.info(f"📝 {queued.count} applications queued")
        
        if st.button("📤 RUN SUBMITTER", use_container_width=True, disabled=True):
            st.info("Auto-submission coming soon! Requires Playwright setup.")
    
    st.markdown("---")
    
    # Test data section
    st.subheader("🧪 Test Data (For Demo/Testing)")
    st.info("Add fake NHS jobs to test the system without scraping")
    
    # Show current job count
    current_jobs = supabase.table('discovered_jobs').select('id', count='exact').execute()
    st.info(f"Current jobs in database: {current_jobs.count if current_jobs else 0}")
    
    if st.button("📦 ADD TEST JOBS", use_container_width=True):
        with st.spinner("Adding test NHS jobs..."):
            # Clear existing jobs first
            try:
                supabase.table('discovered_jobs').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            except:
                pass
            
            # Add fresh jobs
            from datetime import datetime, timedelta
            import random
            
            timestamp = str(int(datetime.now().timestamp()))
            random_id = str(random.randint(1000, 9999))
            
            job_data = {
                'title': 'RTT Validation Officer',
                'trust': 'Royal London Hospital',
                'location': 'London',
                'band': 'Band 3',
                'salary_min': 24000,
                'salary_max': 28000,
                'closing_date': (datetime.now() + timedelta(days=14)).isoformat(),
                'nhs_jobs_url': f'https://www.jobs.nhs.uk/test-{random_id}',
                'job_reference': f'TEST-{timestamp}-{random_id}',
                'discovered_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            try:
                result = supabase.table('discovered_jobs').insert(job_data).execute()
                if result.data:
                    st.success("✅ Added 1 test job! Now click 'RUN AI GENERATOR'")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to add job")
            except Exception as e:
                st.error(f"❌ Database error: {str(e)}")
                st.code(str(e))
    
    st.markdown("---")
    
    # Full cycle
    st.subheader("🚀 Run Full Cycle")
    st.info("Run all 3 steps in sequence: Scrape → Generate → Submit")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🚀 RUN FULL AUTOMATION CYCLE", use_container_width=True, type="primary"):
            with st.spinner("Running full automation cycle..."):
                progress = st.progress(0)
                status = st.empty()
                
                try:
                    # Step 1: Scrape
                    status.write("🔍 Step 1/2: Scraping NHS Jobs...")
                    progress.progress(0.25)
                    scrape_jobs_for_all_students()
                    progress.progress(0.5)
                    
                    # Step 2: Generate
                    status.write("🤖 Step 2/2: Generating applications...")
                    generate_applications_for_all_students()
                    progress.progress(1.0)
                    
                    status.success("✅ Full cycle complete!")
                    st.balloons()
                    st.rerun()
                
                except Exception as e:
                    status.error(f"❌ Cycle failed: {str(e)}")
    
    st.markdown("---")
    
    # Logs
    st.subheader("📋 Recent Activity")
    
    recent_apps = supabase.table('applications').select('*, users(email), discovered_jobs(title, trust)').order('created_at', desc=True).limit(10).execute()
    
    if recent_apps.data:
        for app in recent_apps.data:
            user = app.get('users', {})
            job = app.get('discovered_jobs', {})
            
            status_emoji = {'queued': '⏳', 'processing': '⚙️', 'submitted': '✅', 'failed': '❌'}.get(app.get('status'), '❓')
            
            with st.expander(f"{status_emoji} {user.get('email', 'Unknown')} → {job.get('title', 'Unknown')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Job:** {job.get('title', 'Unknown')}")
                    st.write(f"**Trust:** {job.get('trust', 'Unknown')}")
                    st.write(f"**Status:** {app.get('status', 'Unknown').upper()}")
                
                with col2:
                    st.write(f"**Created:** {app.get('created_at', 'Unknown')[:16]}")
                    if app.get('ai_word_count'):
                        st.write(f"**AI Words:** {app.get('ai_word_count')}")
    else:
        st.info("No applications yet. Run the automation cycle to get started!")

if __name__ == "__main__":
    render_manual_runner()
