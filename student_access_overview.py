"""
STUDENT ACCESS OVERVIEW - ADMIN DASHBOARD

Shows all students and their module access in one view
Quick actions: View, Edit, Remove, Add access
"""

import streamlit as st
from supabase_database import supabase, get_user_modules
from tquk_course_assignment import get_learner_enrollments

def render_student_access_overview():
    """Admin dashboard showing all student access"""
    
    st.markdown("# 👁️ Student Access Overview")
    
    st.info("""
    **Quick view of all students and their access**
    - See what each student can access
    - Identify students with too much/too little access
    - Quick actions to fix access issues
    """)
    
    # Get all students
    try:
        result = supabase.table('users').select('*').eq('user_type', 'student').execute()
        students = result.data if result.data else []
    except Exception as e:
        st.error(f"Error loading students: {e}")
        return
    
    if not students:
        st.warning("No students found")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_role = st.selectbox(
            "Filter by Role:",
            ["All", "student_basic", "student_professional", "student_ultimate", "trial"]
        )
    
    with col2:
        filter_status = st.selectbox(
            "Filter by Status:",
            ["All", "active", "suspended", "expired"]
        )
    
    with col3:
        filter_access = st.selectbox(
            "Filter by Access:",
            ["All", "Has Access", "No Access", "Too Much Access (10+)"]
        )
    
    st.markdown("---")
    
    # Summary stats
    total_students = len(students)
    active_students = len([s for s in students if s.get('status') == 'active'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Active", active_students)
    col3.metric("Suspended", len([s for s in students if s.get('status') == 'suspended']))
    col4.metric("Expired", len([s for s in students if s.get('status') == 'expired']))
    
    st.markdown("---")
    
    # Process each student
    student_data = []
    
    for student in students:
        email = student.get('email')
        name = student.get('full_name')
        role = student.get('role', 'student_basic')
        status = student.get('status', 'active')
        
        # Get modules
        try:
            modules = get_user_modules(email)
            module_count = len(modules) if modules else 0
        except:
            modules = []
            module_count = 0
        
        # Get TQUK courses
        try:
            enrollments = get_learner_enrollments(email)
            course_count = len(enrollments) if enrollments else 0
        except:
            enrollments = []
            course_count = 0
        
        student_data.append({
            'email': email,
            'name': name,
            'role': role,
            'status': status,
            'modules': modules,
            'module_count': module_count,
            'enrollments': enrollments,
            'course_count': course_count
        })
    
    # Apply filters
    filtered_data = student_data
    
    if filter_role != "All":
        filtered_data = [s for s in filtered_data if s['role'] == filter_role]
    
    if filter_status != "All":
        filtered_data = [s for s in filtered_data if s['status'] == filter_status]
    
    if filter_access == "Has Access":
        filtered_data = [s for s in filtered_data if s['module_count'] > 0]
    elif filter_access == "No Access":
        filtered_data = [s for s in filtered_data if s['module_count'] == 0]
    elif filter_access == "Too Much Access (10+)":
        filtered_data = [s for s in filtered_data if s['module_count'] >= 10]
    
    st.markdown(f"### Showing {len(filtered_data)} students")
    
    # Display students
    for student in filtered_data:
        with st.expander(f"👤 {student['name']} ({student['email']}) - {student['module_count']} modules"):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Student info
                st.markdown(f"**Role:** {student['role'].replace('_', ' ').title()}")
                
                # Status with color
                if student['status'] == 'active':
                    st.success(f"**Status:** Active ✅")
                elif student['status'] == 'suspended':
                    st.warning(f"**Status:** Suspended ⚠️")
                else:
                    st.error(f"**Status:** Expired ❌")
                
                # Access summary
                if student['module_count'] == 0:
                    st.error("⚠️ **No module access!**")
                elif student['module_count'] >= 10:
                    st.warning(f"⚠️ **{student['module_count']} modules - May be too many!**")
                else:
                    st.info(f"✅ **{student['module_count']} modules**")
            
            with col2:
                # Quick actions
                st.markdown("**Quick Actions:**")
                
                if st.button("✏️ Edit Access", key=f"edit_{student['email']}", use_container_width=True):
                    st.session_state['edit_student_email'] = student['email']
                    st.session_state['selected_tool'] = "👨‍🏫 Teaching & Assessment"
                    st.rerun()
                
                if st.button("🗑️ Remove All", key=f"remove_{student['email']}", use_container_width=True):
                    st.session_state['remove_all_student'] = student['email']
                    st.rerun()
            
            # Show TQUK courses
            if student['course_count'] > 0:
                st.markdown("**📚 TQUK Courses:**")
                for enrollment in student['enrollments']:
                    st.write(f"✓ {enrollment.get('course_name')}")
            else:
                st.info("No TQUK courses enrolled")
            
            # Show modules
            if student['module_count'] > 0:
                st.markdown("**🎓 Modules:**")
                
                # Organize by category
                tquk_modules = []
                nhs_modules = []
                career_modules = []
                basic_modules = []
                
                for module in student['modules']:
                    if any(x in module for x in ['Level 3', 'IT User', 'Customer Service', 'Business']):
                        tquk_modules.append(module)
                    elif any(x in module for x in ['Patient', 'Clinical', 'Task', 'Reports', 'Training & Certification']):
                        nhs_modules.append(module)
                    elif any(x in module for x in ['Career', 'CV Builder', 'Interview']):
                        career_modules.append(module)
                    else:
                        basic_modules.append(module)
                
                if tquk_modules:
                    st.markdown("**TQUK Qualifications:**")
                    for m in tquk_modules:
                        st.write(f"  ✓ {m}")
                
                if nhs_modules:
                    st.markdown("**NHS/RTT Training:**")
                    for m in nhs_modules:
                        st.write(f"  ✓ {m}")
                
                if career_modules:
                    st.markdown("**Career Tools:**")
                    for m in career_modules:
                        st.write(f"  ✓ {m}")
                
                if basic_modules:
                    st.markdown("**Basic Access:**")
                    for m in basic_modules:
                        st.write(f"  ✓ {m}")
            else:
                st.warning("No modules assigned")
            
            # Recommendations
            st.markdown("---")
            st.markdown("**💡 Recommendations:**")
            
            if student['module_count'] == 0:
                st.error("⚠️ Student has no access! Assign modules in 'TQUK Course Assignment' tab")
            elif student['module_count'] >= 10:
                st.warning("⚠️ Student has many modules. Consider if they need all of them.")
            elif student['course_count'] == 0 and any('Level 3' in m or 'IT User' in m or 'Customer Service' in m or 'Business' in m for m in student['modules']):
                st.warning("⚠️ Student has TQUK module access but no course enrollment. Enroll them in 'TQUK Course Assignment' tab")
            else:
                st.success("✅ Access looks good!")
    
    # Handle remove all action
    if 'remove_all_student' in st.session_state:
        student_email = st.session_state['remove_all_student']
        
        st.warning(f"⚠️ Remove ALL access for {student_email}?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Yes, Remove All", type="primary", use_container_width=True):
                try:
                    # Remove all module access
                    supabase.table('module_access').delete().eq('user_email', student_email).execute()
                    
                    st.success("✅ All access removed!")
                    del st.session_state['remove_all_student']
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                del st.session_state['remove_all_student']
                st.rerun()


# ============================================
# EXPORT REPORT
# ============================================

def export_access_report():
    """Export student access report to CSV"""
    
    st.markdown("## 📊 Export Access Report")
    
    if st.button("📥 Download CSV Report"):
        try:
            result = supabase.table('users').select('*').eq('user_type', 'student').execute()
            students = result.data if result.data else []
            
            # Create CSV data
            csv_data = "Name,Email,Role,Status,Module Count,Modules\n"
            
            for student in students:
                email = student.get('email')
                name = student.get('full_name')
                role = student.get('role', 'student_basic')
                status = student.get('status', 'active')
                
                try:
                    modules = get_user_modules(email)
                    module_count = len(modules) if modules else 0
                    module_list = "; ".join(modules) if modules else "None"
                except:
                    module_count = 0
                    module_list = "None"
                
                csv_data += f'"{name}","{email}","{role}","{status}",{module_count},"{module_list}"\n'
            
            st.download_button(
                label="📥 Download Report",
                data=csv_data,
                file_name="student_access_report.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"Error generating report: {e}")
