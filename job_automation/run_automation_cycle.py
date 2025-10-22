"""
JOB AUTOMATION CYCLE RUNNER
Runs the complete automation cycle:
1. Scrape NHS Jobs
2. Generate AI applications
3. Submit to Trac

Can be run manually or scheduled
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_automation.nhs_jobs_scraper import scrape_jobs_for_all_students
from job_automation.ai_application_generator import generate_applications_for_all_students
from supabase_database import supabase, SUPABASE_AVAILABLE

def run_full_automation_cycle():
    """
    Run complete automation cycle for all active students
    """
    
    print("=" * 70)
    print("🤖 NHS JOB AUTOMATION - FULL CYCLE")
    print("=" * 70)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ FATAL: Supabase not available!")
        print("Please check your environment variables:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_KEY")
        return False
    
    try:
        # Get active students count
        students = supabase.table('student_automation_settings').select('id', count='exact').eq('status', 'active').execute()
        student_count = students.count if students else 0
        
        print(f"👥 Active students: {student_count}")
        
        if student_count == 0:
            print("ℹ️ No active students found. Add students via the admin dashboard first.")
            return True
        
        print()
        
        # STEP 1: Scrape NHS Jobs
        print("-" * 70)
        print("STEP 1: 🔍 SCRAPING NHS JOBS")
        print("-" * 70)
        
        scrape_jobs_for_all_students()
        
        print()
        
        # STEP 2: Generate AI Applications
        print("-" * 70)
        print("STEP 2: 🤖 GENERATING AI APPLICATIONS")
        print("-" * 70)
        
        generate_applications_for_all_students()
        
        print()
        
        # STEP 3: Auto-Submit (if enabled)
        print("-" * 70)
        print("STEP 3: 📤 AUTO-SUBMISSION")
        print("-" * 70)
        
        # Check system config
        config = supabase.table('system_config').select('*').limit(1).execute()
        
        if config.data and config.data[0].get('enable_auto_submit', True):
            print("✅ Auto-submit is ENABLED")
            
            # Get queued applications
            queued = supabase.table('applications').select('id', count='exact').eq('status', 'queued').execute()
            queued_count = queued.count if queued else 0
            
            print(f"📝 {queued_count} applications queued for submission")
            
            if queued_count > 0:
                print()
                print("⚠️ AUTO-SUBMISSION REQUIRES:")
                print("  1. Playwright installed: pip install playwright")
                print("  2. Browser installed: playwright install chromium")
                print("  3. Student Trac credentials in database")
                print("  4. Contract approval from students")
                print()
                print("To submit applications manually:")
                print("  python -m job_automation.trac_auto_submitter")
            else:
                print("ℹ️ No applications to submit")
        else:
            print("⏸️ Auto-submit is DISABLED in system settings")
            print("Applications will remain in 'queued' status")
            print("Enable in Admin → Job Automation → System Settings")
        
        print()
        print("=" * 70)
        print("✅ AUTOMATION CYCLE COMPLETE")
        print("=" * 70)
        
        # Summary
        jobs = supabase.table('discovered_jobs').select('id', count='exact').execute()
        apps = supabase.table('applications').select('id', count='exact').execute()
        submitted = supabase.table('applications').select('id', count='exact').eq('status', 'submitted').execute()
        
        print()
        print("📊 SUMMARY:")
        print(f"  Jobs in database: {jobs.count if jobs else 0}")
        print(f"  Total applications: {apps.count if apps else 0}")
        print(f"  Successfully submitted: {submitted.count if submitted else 0}")
        print()
        print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        return True
    
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR IN AUTOMATION CYCLE")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False

def quick_test():
    """Quick test to verify system is working"""
    
    print("🧪 QUICK SYSTEM TEST")
    print("=" * 70)
    
    # Test 1: Database connection
    print("\n1️⃣ Testing database connection...")
    if SUPABASE_AVAILABLE and supabase:
        print("   ✅ Supabase connected")
    else:
        print("   ❌ Supabase NOT connected")
        return False
    
    # Test 2: Check for active students
    print("\n2️⃣ Checking for active students...")
    students = supabase.table('student_automation_settings').select('id', count='exact').eq('status', 'active').execute()
    print(f"   ✅ Found {students.count if students else 0} active students")
    
    # Test 3: Check for jobs
    print("\n3️⃣ Checking discovered jobs...")
    jobs = supabase.table('discovered_jobs').select('id', count='exact').execute()
    print(f"   ✅ {jobs.count if jobs else 0} jobs in database")
    
    # Test 4: Check OpenAI key
    print("\n4️⃣ Checking OpenAI API key...")
    try:
        import streamlit as st
        api_key = st.secrets.get("OPENAI_API_KEY")
        if api_key:
            print("   ✅ OpenAI API key found")
        else:
            print("   ⚠️ OpenAI API key not found (AI generation will fail)")
    except:
        print("   ⚠️ Cannot check OpenAI key (not in Streamlit context)")
    
    print("\n" + "=" * 70)
    print("✅ System test complete!")
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run quick test
        quick_test()
    else:
        # Run full cycle
        success = run_full_automation_cycle()
        sys.exit(0 if success else 1)
