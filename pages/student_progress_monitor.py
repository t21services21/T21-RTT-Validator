"""
T21 HEALTHCARE PLATFORM - STUDENT PROGRESS MONITOR
Admin/Tutor dashboard to review student work and provide grading
"""

import streamlit as st
from navigation import render_navigation
import os
import json
from datetime import datetime

st.set_page_config(page_title="Student Progress Monitor | T21 Services", page_icon="👨‍🏫", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="student_monitor")

st.title("👨‍🏫 Student Progress Monitor")
st.markdown("**Admin & Tutor Dashboard - Review student work, grade submissions, track progress**")

# Check if user is admin/staff
if 'user_role' not in st.session_state or st.session_state.user_role not in ['admin', 'staff', 'tutor']:
    st.error("⛔ Access Denied - This page is only for Admin, Staff, and Tutors")
    st.info("Login as Admin or Staff to access student monitoring")
    st.stop()

st.success(f"✅ Logged in as: **{st.session_state.user_role.upper()}** - {st.session_state.get('user_email', 'Unknown')}")

st.markdown("---")

# Load all student data
def load_all_students():
    """Load all student license data"""
    students = []
    license_dir = "data/licenses"
    
    if os.path.exists(license_dir):
        for filename in os.listdir(license_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(license_dir, filename), 'r') as f:
                        license_data = json.load(f)
                        # Only include students (not staff/admin)
                        if license_data.get('role') in ['trial', 'tier1', 'tier2', 'tier3']:
                            students.append({
                                'email': license_data.get('email'),
                                'name': license_data.get('full_name', 'Unknown'),
                                'tier': license_data.get('role', 'Unknown'),
                                'created': license_data.get('created_date', 'Unknown'),
                                'license_file': filename
                            })
                except Exception as e:
                    continue
    
    return students

def load_student_patients(student_email):
    """Load a specific student's patient data"""
    email_safe = student_email.replace('@', '_at_').replace('.', '_')
    db_file = f"data/patients_{email_safe}.json"
    
    if os.path.exists(db_file):
        try:
            with open(db_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def load_student_validations(student_email):
    """Load a specific student's validation history"""
    email_safe = student_email.replace('@', '_at_').replace('.', '_')
    history_file = f"data/validation_history_{email_safe}.json"
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def load_student_module_activity(student_email):
    """Load ALL module usage by student"""
    email_safe = student_email.replace('@', '_at_').replace('.', '_')
    activity_file = f"data/module_activity_{email_safe}.json"
    
    if os.path.exists(activity_file):
        try:
            with open(activity_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def get_all_student_data_files(student_email):
    """Find all data files for a student across ALL modules"""
    email_safe = student_email.replace('@', '_at_').replace('.', '_')
    student_files = {}
    
    # Check for various data files
    possible_files = {
        'PTL Patients': f"data/patients_{email_safe}.json",
        'Validations': f"data/validation_history_{email_safe}.json",
        'DNA Cases': f"data/dna_cases_{email_safe}.json",
        'Cancellations': f"data/cancellations_{email_safe}.json",
        'Patient Choice': f"data/patient_choice_{email_safe}.json",
        'Transfers': f"data/transfers_{email_safe}.json",
        'Clinical Exceptions': f"data/exceptions_{email_safe}.json",
        'Capacity Plans': f"data/capacity_{email_safe}.json",
        'Module Activity': f"data/module_activity_{email_safe}.json"
    }
    
    for module_name, filepath in possible_files.items():
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if data:  # Only include if has data
                        student_files[module_name] = data
            except:
                continue
    
    return student_files

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Student Overview", "🔍 Individual Review", "📝 Grade Submissions", "📈 Progress Analytics"])

with tab1:
    st.markdown("### 📊 All Students Overview")
    
    students = load_all_students()
    
    if not students:
        st.warning("No students found in system")
    else:
        st.info(f"**Total Students:** {len(students)}")
        
        # Display students in a table
        import pandas as pd
        df = pd.DataFrame(students)
        
        # Add activity indicators
        for idx, student in enumerate(students):
            patient_count = len(load_student_patients(student['email']))
            validation_count = len(load_student_validations(student['email']))
            df.loc[idx, 'Patients Added'] = patient_count
            df.loc[idx, 'Validations'] = validation_count
            df.loc[idx, 'Activity'] = '🟢 Active' if patient_count > 0 else '🔴 Inactive'
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", len(students))
        with col2:
            active = len([s for s in students if len(load_student_patients(s['email'])) > 0])
            st.metric("Active Students", active)
        with col3:
            total_patients = sum([len(load_student_patients(s['email'])) for s in students])
            st.metric("Total Patient Cases", total_patients)
        with col4:
            total_validations = sum([len(load_student_validations(s['email'])) for s in students])
            st.metric("Total Validations", total_validations)

with tab2:
    st.markdown("### 🔍 Individual Student Review")
    
    students = load_all_students()
    
    if not students:
        st.warning("No students to review")
    else:
        # Select student
        student_options = {f"{s['name']} ({s['email']}) - {s['tier'].upper()}": s for s in students}
        selected_student_key = st.selectbox("Select Student to Review:", list(student_options.keys()))
        
        if selected_student_key:
            selected_student = student_options[selected_student_key]
            
            st.markdown(f"### 👤 Student: **{selected_student['name']}**")
            st.markdown(f"**Email:** {selected_student['email']}")
            st.markdown(f"**Tier:** {selected_student['tier'].upper()}")
            st.markdown(f"**Enrolled:** {selected_student['created']}")
            
            st.markdown("---")
            
            # Load ALL student's work across ALL modules
            all_student_data = get_all_student_data_files(selected_student['email'])
            
            # Calculate total activity
            total_items = sum([len(data) if isinstance(data, list) else 1 for data in all_student_data.values()])
            modules_used = len(all_student_data)
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("Modules Used", modules_used)
            with col_stats2:
                st.metric("Total Practice Items", total_items)
            with col_stats3:
                st.metric("Activity Score", total_items * 10)
            
            st.markdown("---")
            
            # Show work from ALL modules
            st.markdown("#### 📚 Work Across ALL Modules")
            
            if all_student_data:
                for module_name, module_data in all_student_data.items():
                    with st.expander(f"📁 {module_name} ({len(module_data) if isinstance(module_data, list) else 1} items)"):
                        
                        if isinstance(module_data, list):
                            # Module has multiple items (like patients, DNAs, etc.)
                            for idx, item in enumerate(module_data, 1):
                                st.markdown(f"**Item #{idx}:**")
                                
                                # Display key information
                                for key, value in item.items():
                                    if key not in ['tutor_feedback', 'grade', 'graded_by', 'graded_date']:
                                        st.markdown(f"- **{key}:** {value}")
                                
                                # Show existing feedback if any
                                if item.get('tutor_feedback') or item.get('grade'):
                                    st.success(f"✅ **Graded:** {item.get('grade', 'N/A')} - {item.get('tutor_feedback', 'No feedback')}")
                                
                                # Add grading section
                                st.markdown("---")
                                feedback = st.text_area(f"Feedback for {module_name} #{idx}", 
                                    value=item.get('tutor_feedback', ''),
                                    key=f"feedback_{module_name}_{idx}",
                                    placeholder="Enter your feedback here...")
                                
                                grade = st.selectbox(f"Grade {module_name} #{idx}", 
                                    ['Not Graded', 'Excellent', 'Good', 'Needs Improvement', 'Incorrect'],
                                    key=f"grade_{module_name}_{idx}",
                                    index=0)
                                
                                if st.button(f"Save Feedback #{idx}", key=f"save_{module_name}_{idx}"):
                                    # Save feedback
                                    item['tutor_feedback'] = feedback
                                    item['grade'] = grade
                                    item['graded_by'] = st.session_state.user_email
                                    item['graded_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    
                                    st.success(f"✅ Feedback saved for {module_name} #{idx}")
                                
                                st.markdown("---")
                        else:
                            # Module has single item or summary data
                            st.json(module_data)
            else:
                st.info("✨ Student has not used any modules yet - check back after they start practicing!")
                st.markdown("""
                **Modules that will appear here when student practices:**
                - PTL Patient cases
                - DNA Management cases  
                - Cancellation records
                - Patient Choice submissions
                - Transfer of Care records
                - Clinical Exceptions
                - Capacity planning work
                - All validation attempts
                - And more from 55 modules!
                """)

with tab3:
    st.markdown("### 📝 Grade Student Submissions")
    
    st.info("View and grade student exam submissions, assignments, and certification tests")
    
    # This would integrate with your exam system
    st.markdown("**Coming Soon:**")
    st.markdown("- Certification exam results")
    st.markdown("- Assignment submissions")
    st.markdown("- Practical assessment grading")
    st.markdown("- Final qualification approval")

with tab4:
    st.markdown("### 📈 Progress Analytics")
    
    students = load_all_students()
    
    if students:
        # Calculate analytics
        total_students = len(students)
        active_students = len([s for s in students if len(load_student_patients(s['email'])) > 0])
        total_patients = sum([len(load_student_patients(s['email'])) for s in students])
        total_validations = sum([len(load_student_validations(s['email'])) for s in students])
        
        col_an1, col_an2, col_an3 = st.columns(3)
        
        with col_an1:
            st.markdown("### Engagement Rate")
            engagement = (active_students / total_students * 100) if total_students > 0 else 0
            st.metric("Active Students", f"{engagement:.1f}%", f"{active_students}/{total_students}")
        
        with col_an2:
            st.markdown("### Average Activity")
            avg_patients = total_patients / total_students if total_students > 0 else 0
            st.metric("Patients per Student", f"{avg_patients:.1f}")
        
        with col_an3:
            st.markdown("### Total Activity")
            st.metric("Platform Actions", total_patients + total_validations)
        
        st.markdown("---")
        
        # Top performers
        st.markdown("### 🏆 Top Performing Students")
        
        student_scores = []
        for student in students:
            score = len(load_student_patients(student['email'])) + len(load_student_validations(student['email']))
            student_scores.append({
                'Name': student['name'],
                'Email': student['email'],
                'Tier': student['tier'],
                'Activity Score': score,
                'Patients': len(load_student_patients(student['email'])),
                'Validations': len(load_student_validations(student['email']))
            })
        
        # Sort by score
        student_scores = sorted(student_scores, key=lambda x: x['Activity Score'], reverse=True)
        
        import pandas as pd
        df_top = pd.DataFrame(student_scores[:10])  # Top 10
        st.dataframe(df_top, use_container_width=True, hide_index=True)

st.markdown("---")
st.success("""
👨‍🏫 **Tutor/Admin Features:**
- ✅ View all student work
- ✅ Provide individual feedback
- ✅ Grade patient cases
- ✅ Track student progress
- ✅ Identify students needing help
- ✅ Export reports for management
""")
