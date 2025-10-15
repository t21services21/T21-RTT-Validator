"""
UNIVERSAL DEBUG PANEL
Shows what's happening across ALL data modules
Helps diagnose "data not showing" issues
"""

import streamlit as st

def show_universal_debug_info():
    """Display comprehensive debug information"""
    
    st.markdown("### 🔧 Universal Debug Panel")
    
    with st.expander("🔍 Click to see debug information"):
        
        # SESSION STATE
        st.markdown("#### 📊 Session State")
        st.write(f"**Logged in:** {st.session_state.get('logged_in', False)}")
        st.write(f"**User email:** `{st.session_state.get('user_email', 'NOT SET')}`")
        st.write(f"**Session email:** `{st.session_state.get('session_email', 'NOT SET')}`")
        
        st.markdown("---")
        
        # PTL PATIENTS
        st.markdown("#### 📋 PTL Patients Module")
        try:
            from supabase_database import get_ptl_patients_for_user, supabase
            user_email = st.session_state.get('user_email', 'demo@t21services.co.uk')
            
            # Check if Supabase is working
            try:
                ptl_patients = get_ptl_patients_for_user(user_email)
                st.success(f"✅ Supabase connected - Found {len(ptl_patients)} PTL patients for `{user_email}`")
                
                # Check all users in database
                all_result = supabase.table('ptl_patients').select('user_email, patient_name').execute()
                if all_result.data:
                    unique_emails = set(p['user_email'] for p in all_result.data)
                    st.info(f"**PTL patients in database by user:**")
                    for email in unique_emails:
                        count = sum(1 for p in all_result.data if p['user_email'] == email)
                        match = "✅ MATCH!" if email == user_email else ""
                        st.write(f"- `{email}`: {count} patients {match}")
                else:
                    st.warning("No PTL patients in database at all")
            except Exception as e:
                st.error(f"❌ Supabase error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Could not load PTL module: {str(e)}")
        
        st.markdown("---")
        
        # CANCER PATIENTS
        st.markdown("#### 🎗️ Cancer Pathways Module")
        try:
            from supabase_database import get_cancer_patients_for_user, supabase
            user_email = st.session_state.get('user_email', 'demo@t21services.co.uk')
            
            try:
                cancer_patients = get_cancer_patients_for_user(user_email)
                st.success(f"✅ Supabase connected - Found {len(cancer_patients)} cancer patients for `{user_email}`")
                
                # Check all users in database
                all_result = supabase.table('cancer_pathways').select('user_email, patient_name').execute()
                if all_result.data:
                    unique_emails = set(p['user_email'] for p in all_result.data)
                    st.info(f"**Cancer patients in database by user:**")
                    for email in unique_emails:
                        count = sum(1 for p in all_result.data if p['user_email'] == email)
                        match = "✅ MATCH!" if email == user_email else ""
                        st.write(f"- `{email}`: {count} patients {match}")
                else:
                    st.warning("No cancer patients in database at all")
            except Exception as e:
                st.error(f"❌ Supabase error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Could not load Cancer module: {str(e)}")
        
        st.markdown("---")
        
        # MDT MEETINGS
        st.markdown("#### 👥 MDT Meetings Module")
        try:
            from supabase_database import get_mdt_meetings_for_user, supabase
            user_email = st.session_state.get('user_email', 'demo@t21services.co.uk')
            
            try:
                mdt_meetings = get_mdt_meetings_for_user(user_email)
                st.success(f"✅ Supabase connected - Found {len(mdt_meetings)} MDT meetings for `{user_email}`")
            except Exception as e:
                st.error(f"❌ Supabase error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Could not load MDT module: {str(e)}")
        
        st.markdown("---")
        
        # SUPABASE CONNECTION
        st.markdown("#### 🔗 Supabase Connection Status")
        try:
            from supabase_database import supabase
            # Try a simple query
            result = supabase.table('users').select('email').limit(1).execute()
            st.success("✅ Supabase connected successfully!")
            st.write(f"**API URL:** {supabase.url}")
        except Exception as e:
            st.error(f"❌ Supabase connection error: {str(e)}")
            st.warning("Check your Supabase credentials in Streamlit secrets!")
        
        st.markdown("---")
        
        # DIAGNOSIS
        st.markdown("#### 💡 Diagnosis")
        
        user_email = st.session_state.get('user_email')
        if not user_email:
            st.error("❌ **Problem:** user_email is NOT SET in session state!")
            st.info("**Solution:** Make sure you're logged in properly")
        else:
            st.success(f"✅ user_email is set: `{user_email}`")
            
            # Check if data exists but under different email
            try:
                from supabase_database import supabase
                ptl_check = supabase.table('ptl_patients').select('user_email').execute()
                if ptl_check.data:
                    emails_in_db = set(p['user_email'] for p in ptl_check.data)
                    if user_email not in emails_in_db:
                        st.warning(f"⚠️ **Problem:** You're logged in as `{user_email}` but data exists for: {emails_in_db}")
                        st.info("**Solution:** Login with one of the emails listed above, OR add new data")
            except:
                pass


def show_quick_debug():
    """Quick debug info at top of page"""
    user_email = st.session_state.get('user_email', 'NOT SET')
    if user_email == 'NOT SET':
        st.warning(f"⚠️ Debug: user_email = `{user_email}` - You may not see any data!")
    else:
        st.info(f"📧 Logged in as: `{user_email}`")
