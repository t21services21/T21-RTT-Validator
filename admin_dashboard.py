"""
T21 ADMIN DASHBOARD - TUTOR & STAFF MONITORING
View all students' work, progress, and training sessions

Features:
- View all students' PTL patients
- View all students' MDT meetings
- View all students' appointments
- Monitor student progress
- Assessment and grading
- Export student portfolios
- Training session monitoring
- Performance analytics
"""

import streamlit as st
from datetime import datetime
import pandas as pd

# Import Supabase functions
try:
    from supabase_database import supabase
    SUPABASE_ENABLED = True
except:
    SUPABASE_ENABLED = False


def is_admin_or_tutor():
    """Check if current user is admin or tutor"""
    user_email = st.session_state.get('user_email', '')
    user_role = st.session_state.get('user_role', '')
    
    # Check role
    if user_role in ['admin', 'tutor', 'staff', 'instructor']:
        return True
    
    # Check email domain for staff
    if any(domain in user_email.lower() for domain in ['@t21services.co.uk', '@admin', '@staff', '@tutor']):
        return True
    
    return False


def get_all_students():
    """Get list of all students"""
    if not SUPABASE_ENABLED:
        return []
    
    try:
        result = supabase.table('users').select('email, full_name, user_type, created_at, last_login').eq('user_type', 'student').execute()
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Error loading students: {e}")
        return []


def get_student_ptl_data(student_email):
    """Get all PTL patients for a specific student"""
    if not SUPABASE_ENABLED:
        return []
    
    try:
        result = supabase.table('ptl_patients').select('*').eq('user_email', student_email).execute()
        return result.data if result.data else []
    except Exception as e:
        return []


def get_student_mdt_data(student_email):
    """Get all MDT meetings for a specific student"""
    if not SUPABASE_ENABLED:
        return []
    
    try:
        result = supabase.table('mdt_meetings').select('*').eq('user_email', student_email).execute()
        return result.data if result.data else []
    except Exception as e:
        return []


def get_student_appointments(student_email):
    """Get all appointments for a specific student"""
    if not SUPABASE_ENABLED:
        return []
    
    try:
        result = supabase.table('appointments').select('*').eq('user_email', student_email).execute()
        return result.data if result.data else []
    except Exception as e:
        return []


def get_all_ptl_data():
    """Get ALL PTL patients from ALL students"""
    if not SUPABASE_ENABLED:
        return []
    
    try:
        result = supabase.table('ptl_patients').select('*').execute()
        return result.data if result.data else []
    except Exception as e:
        return []


def get_all_mdt_data():
    """Get ALL MDT meetings from ALL students"""
    if not SUPABASE_ENABLED:
        return []
    
    try:
        result = supabase.table('mdt_meetings').select('*').execute()
        return result.data if result.data else []
    except Exception as e:
        return []


def get_all_appointments():
    """Get ALL appointments from ALL students"""
    if not SUPABASE_ENABLED:
        return []
    
    try:
        result = supabase.table('appointments').select('*').execute()
        return result.data if result.data else []
    except Exception as e:
        return []


def render_admin_dashboard():
    """Main admin dashboard"""
    
    # Check if user is admin/tutor
    if not is_admin_or_tutor():
        st.error("🔒 Access Denied - Admin/Tutor privileges required")
        st.info("This dashboard is only accessible to tutors, staff, and administrators.")
        return
    
    st.title("👨‍🏫 Admin Dashboard - Student Monitoring")
    st.markdown("**Monitor all students' training progress and work**")
    
    st.success(f"✅ Logged in as: {st.session_state.get('user_email', 'Unknown')} (Admin/Tutor)")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "👥 Students",
        "🏥 All PTL Data",
        "👔 All MDT Data",
        "📅 All Appointments"
    ])
    
    with tab1:
        render_overview()
    
    with tab2:
        render_students_view()
    
    with tab3:
        render_all_ptl()
    
    with tab4:
        render_all_mdt()
    
    with tab5:
        render_all_appointments()


def render_overview():
    """Overview dashboard"""
    
    st.subheader("📊 Platform Overview")
    
    # Get all data
    students = get_all_students()
    all_ptl = get_all_ptl_data()
    all_mdt = get_all_mdt_data()
    all_appointments = get_all_appointments()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(students))
    
    with col2:
        st.metric("Total PTL Patients", len(all_ptl))
    
    with col3:
        st.metric("Total MDT Meetings", len(all_mdt))
    
    with col4:
        st.metric("Total Appointments", len(all_appointments))
    
    st.markdown("---")
    
    # Student activity
    st.subheader("👥 Student Activity")
    
    if students:
        student_data = []
        for student in students:
            email = student.get('email')
            ptl_count = len(get_student_ptl_data(email))
            mdt_count = len(get_student_mdt_data(email))
            appt_count = len(get_student_appointments(email))
            
            student_data.append({
                'Student': student.get('full_name', email),
                'Email': email,
                'PTL Patients': ptl_count,
                'MDT Meetings': mdt_count,
                'Appointments': appt_count,
                'Total Activity': ptl_count + mdt_count + appt_count,
                'Last Login': student.get('last_login', 'Never')
            })
        
        df = pd.DataFrame(student_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No students found")


def render_students_view():
    """View individual student data"""
    
    st.subheader("👥 Student Details")
    
    students = get_all_students()
    
    if not students:
        st.info("No students found")
        return
    
    # Select student
    student_options = {f"{s.get('full_name', s.get('email'))} ({s.get('email')})": s.get('email') for s in students}
    selected = st.selectbox("Select Student", list(student_options.keys()))
    
    if selected:
        student_email = student_options[selected]
        
        st.markdown(f"### 📧 {student_email}")
        
        # Get student data
        ptl_data = get_student_ptl_data(student_email)
        mdt_data = get_student_mdt_data(student_email)
        appt_data = get_student_appointments(student_email)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("PTL Patients", len(ptl_data))
        
        with col2:
            st.metric("MDT Meetings", len(mdt_data))
        
        with col3:
            st.metric("Appointments", len(appt_data))
        
        st.markdown("---")
        
        # Show data
        tab1, tab2, tab3 = st.tabs(["PTL Patients", "MDT Meetings", "Appointments"])
        
        with tab1:
            if ptl_data:
                st.dataframe(pd.DataFrame(ptl_data), use_container_width=True)
            else:
                st.info("No PTL patients")
        
        with tab2:
            if mdt_data:
                st.dataframe(pd.DataFrame(mdt_data), use_container_width=True)
            else:
                st.info("No MDT meetings")
        
        with tab3:
            if appt_data:
                st.dataframe(pd.DataFrame(appt_data), use_container_width=True)
            else:
                st.info("No appointments")


def render_all_ptl():
    """View all PTL data from all students"""
    
    st.subheader("🏥 All PTL Patients (All Students)")
    
    all_ptl = get_all_ptl_data()
    
    if all_ptl:
        st.markdown(f"**Total: {len(all_ptl)} patients across all students**")
        
        df = pd.DataFrame(all_ptl)
        
        # Add filters
        col1, col2 = st.columns(2)
        
        with col1:
            if 'user_email' in df.columns:
                selected_student = st.selectbox("Filter by Student", ["All"] + list(df['user_email'].unique()))
                if selected_student != "All":
                    df = df[df['user_email'] == selected_student]
        
        with col2:
            if 'specialty' in df.columns:
                selected_specialty = st.selectbox("Filter by Specialty", ["All"] + list(df['specialty'].unique()))
                if selected_specialty != "All":
                    df = df[df['specialty'] == selected_specialty]
        
        st.dataframe(df, use_container_width=True)
        
        # Export
        if st.button("📥 Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "all_ptl_data.csv", "text/csv")
    else:
        st.info("No PTL data found")


def render_all_mdt():
    """View all MDT data from all students"""
    
    st.subheader("👔 All MDT Meetings (All Students)")
    
    all_mdt = get_all_mdt_data()
    
    if all_mdt:
        st.markdown(f"**Total: {len(all_mdt)} MDT meetings across all students**")
        
        df = pd.DataFrame(all_mdt)
        
        # Add filters
        if 'user_email' in df.columns:
            selected_student = st.selectbox("Filter by Student", ["All"] + list(df['user_email'].unique()))
            if selected_student != "All":
                df = df[df['user_email'] == selected_student]
        
        st.dataframe(df, use_container_width=True)
        
        # Export
        if st.button("📥 Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "all_mdt_data.csv", "text/csv")
    else:
        st.info("No MDT data found")


def render_all_appointments():
    """View all appointments from all students"""
    
    st.subheader("📅 All Appointments (All Students)")
    
    all_appts = get_all_appointments()
    
    if all_appts:
        st.markdown(f"**Total: {len(all_appts)} appointments across all students**")
        
        df = pd.DataFrame(all_appts)
        
        # Add filters
        if 'user_email' in df.columns:
            selected_student = st.selectbox("Filter by Student", ["All"] + list(df['user_email'].unique()))
            if selected_student != "All":
                df = df[df['user_email'] == selected_student]
        
        st.dataframe(df, use_container_width=True)
        
        # Export
        if st.button("📥 Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "all_appointments_data.csv", "text/csv")
    else:
        st.info("No appointment data found")
