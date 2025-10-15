"""
ASSIGNMENTS & SUBMISSIONS SYSTEM
Create assignments, collect submissions, and grade student work

Features:
- Create assignments with due dates
- Student submissions
- File uploads (via URL)
- Grading and feedback
- Late submission tracking
- Progress monitoring
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, List, Optional
from supabase_client import get_supabase_client
import json
import os


def create_assignment(
    title: str,
    description: str,
    instructions: str,
    week: int,
    module_name: str,
    competency: str,
    due_date: str,
    total_marks: int = 100,
    pass_mark: int = 50,
    required: bool = True,
    allow_late_submission: bool = False
) -> Dict:
    """Create a new assignment"""
    
    try:
        supabase = get_supabase_client()
        
        assignment_data = {
            'title': title,
            'description': description,
            'instructions': instructions,
            'week': week,
            'module_name': module_name,
            'competency': competency,
            'due_date': due_date,
            'total_marks': total_marks,
            'pass_mark': pass_mark,
            'required': required,
            'allow_late_submission': allow_late_submission,
            'created_by': st.session_state.get('user_email', 'admin@example.com'),
            'created_date': datetime.now().date().isoformat(),
            'status': 'active'
        }
        
        if supabase:
            result = supabase.table('assignments').insert(assignment_data).execute()
            return {
                'success': True,
                'message': 'Assignment created successfully',
                'assignment_id': result.data[0].get('id') if result.data else None
            }
        else:
            # Local storage
            assignments_file = 'data/assignments.json'
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(assignments_file):
                with open(assignments_file, 'r') as f:
                    assignments = json.load(f)
            else:
                assignments = []
            
            assignment_data['id'] = f"ASN-{len(assignments) + 1:05d}"
            assignments.append(assignment_data)
            
            with open(assignments_file, 'w') as f:
                json.dump(assignments, f, indent=2)
            
            return {
                'success': True,
                'message': 'Assignment created successfully',
                'assignment_id': assignment_data['id']
            }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_all_assignments(week: int = None, module: str = None, status: str = 'active') -> List[Dict]:
    """Get all assignments"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('assignments').select('*').eq('status', status)
            
            if week is not None:
                query = query.eq('week', week)
            if module:
                query = query.eq('module_name', module)
            
            result = query.order('due_date').execute()
            return result.data if result.data else []
        else:
            assignments_file = 'data/assignments.json'
            if os.path.exists(assignments_file):
                with open(assignments_file, 'r') as f:
                    assignments = json.load(f)
                
                # Filter
                if week is not None:
                    assignments = [a for a in assignments if a.get('week') == week]
                if module:
                    assignments = [a for a in assignments if a.get('module_name') == module]
                if status:
                    assignments = [a for a in assignments if a.get('status') == status]
                
                return sorted(assignments, key=lambda x: x.get('due_date', ''))
            return []
    
    except Exception as e:
        st.error(f"Error getting assignments: {e}")
        return []


def submit_assignment(
    assignment_id: str,
    student_email: str,
    student_name: str,
    submission_text: str,
    file_url: str = "",
    file_name: str = ""
) -> Dict:
    """Submit an assignment"""
    
    try:
        supabase = get_supabase_client()
        
        # Check if assignment exists and get due date
        assignments = get_all_assignments()
        assignment = next((a for a in assignments if str(a.get('id')) == str(assignment_id)), None)
        
        if not assignment:
            return {'success': False, 'error': 'Assignment not found'}
        
        # Check if late
        due_date = datetime.fromisoformat(assignment['due_date']).date() if isinstance(assignment['due_date'], str) else assignment['due_date']
        is_late = datetime.now().date() > due_date
        
        if is_late and not assignment.get('allow_late_submission'):
            return {'success': False, 'error': 'Late submissions not allowed for this assignment'}
        
        submission_data = {
            'assignment_id': assignment_id,
            'student_email': student_email,
            'student_name': student_name,
            'submission_text': submission_text,
            'file_url': file_url,
            'file_name': file_name,
            'submitted_date': datetime.now().isoformat(),
            'is_late': is_late,
            'status': 'submitted'
        }
        
        if supabase:
            result = supabase.table('assignment_submissions').insert(submission_data).execute()
            return {
                'success': True,
                'message': 'Assignment submitted successfully' + (' (Late submission)' if is_late else ''),
                'submission_id': result.data[0].get('id') if result.data else None
            }
        else:
            # Local storage
            submissions_file = 'data/assignment_submissions.json'
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(submissions_file):
                with open(submissions_file, 'r') as f:
                    submissions = json.load(f)
            else:
                submissions = []
            
            submission_data['id'] = f"SUB-{len(submissions) + 1:05d}"
            submissions.append(submission_data)
            
            with open(submissions_file, 'w') as f:
                json.dump(submissions, f, indent=2)
            
            return {
                'success': True,
                'message': 'Assignment submitted successfully' + (' (Late submission)' if is_late else ''),
                'submission_id': submission_data['id']
            }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_submissions(assignment_id: str = None, student_email: str = None) -> List[Dict]:
    """Get submissions"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('assignment_submissions').select('*')
            
            if assignment_id:
                query = query.eq('assignment_id', assignment_id)
            if student_email:
                query = query.eq('student_email', student_email)
            
            result = query.order('submitted_date', desc=True).execute()
            return result.data if result.data else []
        else:
            submissions_file = 'data/assignment_submissions.json'
            if os.path.exists(submissions_file):
                with open(submissions_file, 'r') as f:
                    submissions = json.load(f)
                
                # Filter
                if assignment_id:
                    submissions = [s for s in submissions if str(s.get('assignment_id')) == str(assignment_id)]
                if student_email:
                    submissions = [s for s in submissions if s.get('student_email') == student_email]
                
                return sorted(submissions, key=lambda x: x.get('submitted_date', ''), reverse=True)
            return []
    
    except Exception as e:
        st.error(f"Error getting submissions: {e}")
        return []


def grade_submission(
    submission_id: str,
    marks_awarded: int,
    feedback: str,
    graded_by: str
) -> Dict:
    """Grade a submission"""
    
    try:
        supabase = get_supabase_client()
        
        grade_data = {
            'marks_awarded': marks_awarded,
            'feedback': feedback,
            'graded_by': graded_by,
            'graded_date': datetime.now().isoformat(),
            'status': 'graded'
        }
        
        if supabase:
            result = supabase.table('assignment_submissions').update(grade_data).eq('id', submission_id).execute()
            return {'success': True, 'message': 'Submission graded successfully'}
        else:
            submissions_file = 'data/assignment_submissions.json'
            if os.path.exists(submissions_file):
                with open(submissions_file, 'r') as f:
                    submissions = json.load(f)
                
                for submission in submissions:
                    if str(submission.get('id')) == str(submission_id):
                        submission.update(grade_data)
                
                with open(submissions_file, 'w') as f:
                    json.dump(submissions, f, indent=2)
            
            return {'success': True, 'message': 'Submission graded successfully'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_assignments_system():
    """Main assignments UI"""
    
    st.subheader("📝 Assignments System")
    
    # Check user role
    user_email = st.session_state.get('user_email', '')
    is_teacher = 'admin' in user_email or 'teacher' in user_email
    
    if is_teacher:
        render_teacher_assignments()
    else:
        render_student_assignments()


def render_teacher_assignments():
    """Teacher view for assignments"""
    
    st.info("**Teacher View:** Create assignments, view submissions, and grade student work")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Create Assignment",
        "📋 All Assignments",
        "📥 Submissions",
        "📊 Statistics"
    ])
    
    with tab1:
        render_create_assignment()
    
    with tab2:
        render_view_assignments_teacher()
    
    with tab3:
        render_grade_submissions()
    
    with tab4:
        render_assignment_stats()


def render_create_assignment():
    """Create new assignment"""
    
    st.markdown("### ➕ Create New Assignment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Assignment Title*", placeholder="e.g., Week 1 Practice Exercise")
        week = st.number_input("Week Number", min_value=1, max_value=52, value=1)
        module_name = st.text_input("Module Name", placeholder="e.g., Patient Registration")
        competency = st.selectbox("Related Competency", [
            "None",
            "Patient Registration",
            "Pathway Creation",
            "Episode Management",
            "RTT Clock Management",
            "Milestone Recording"
        ])
    
    with col2:
        due_date = st.date_input("Due Date")
        total_marks = st.number_input("Total Marks", min_value=1, max_value=500, value=100)
        pass_mark = st.number_input("Pass Mark", min_value=1, max_value=500, value=50)
        required = st.checkbox("Required Assignment", value=True)
        allow_late = st.checkbox("Allow Late Submissions", value=False)
    
    description = st.text_area("Description*", placeholder="Brief description of the assignment...", height=100)
    
    instructions = st.text_area(
        "Instructions*",
        placeholder="Detailed instructions for students...\n\nWhat students need to do:\n1. ...\n2. ...",
        height=200
    )
    
    if st.button("📝 Create Assignment", type="primary"):
        if not title or not description or not instructions:
            st.error("Please fill in all required fields")
            return
        
        result = create_assignment(
            title=title,
            description=description,
            instructions=instructions,
            week=week,
            module_name=module_name,
            competency=competency if competency != "None" else "",
            due_date=str(due_date),
            total_marks=total_marks,
            pass_mark=pass_mark,
            required=required,
            allow_late_submission=allow_late
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            st.balloons()
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_view_assignments_teacher():
    """View all assignments (teacher)"""
    
    st.markdown("### 📋 All Assignments")
    
    assignments = get_all_assignments()
    
    if not assignments:
        st.info("No assignments created yet.")
        return
    
    st.write(f"**Total Assignments: {len(assignments)}**")
    
    for assignment in assignments:
        due_date = assignment.get('due_date', '')
        is_overdue = datetime.fromisoformat(due_date).date() < datetime.now().date() if due_date else False
        due_icon = "🔴" if is_overdue else "🟢"
        
        with st.expander(f"{due_icon} {assignment['title']} - Week {assignment.get('week', 0)} - Due: {due_date}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Description:** {assignment['description']}")
                st.write(f"**Week:** {assignment.get('week', 0)}")
                st.write(f"**Module:** {assignment.get('module_name', 'N/A')}")
                if assignment.get('competency'):
                    st.write(f"**Competency:** {assignment['competency']}")
            
            with col2:
                st.write(f"**Due Date:** {due_date}")
                st.write(f"**Total Marks:** {assignment.get('total_marks', 100)}")
                st.write(f"**Pass Mark:** {assignment.get('pass_mark', 50)}")
                st.write(f"**Required:** {'Yes' if assignment.get('required') else 'No'}")
                st.write(f"**Late Allowed:** {'Yes' if assignment.get('allow_late_submission') else 'No'}")
            
            st.markdown("**Instructions:**")
            st.write(assignment.get('instructions', ''))
            
            # Submission count
            submissions = get_submissions(assignment_id=assignment.get('id'))
            st.info(f"📥 **{len(submissions)} submissions received**")


def render_grade_submissions():
    """Grade submissions"""
    
    st.markdown("### 📥 Grade Submissions")
    
    # Get all assignments
    assignments = get_all_assignments()
    
    if not assignments:
        st.info("No assignments created yet.")
        return
    
    # Select assignment
    assignment_options = {f"{a['title']} (Week {a.get('week', 0)})": a for a in assignments}
    selected = st.selectbox("Select Assignment:", ["-- Select Assignment --"] + list(assignment_options.keys()))
    
    if selected == "-- Select Assignment --":
        return
    
    assignment = assignment_options[selected]
    
    # Get submissions
    submissions = get_submissions(assignment_id=assignment.get('id'))
    
    if not submissions:
        st.info("No submissions yet for this assignment.")
        return
    
    st.write(f"**Total Submissions: {len(submissions)}**")
    
    # Display submissions
    for submission in submissions:
        status_icon = "✅" if submission.get('status') == 'graded' else "⏳"
        late_icon = "🔴 LATE" if submission.get('is_late') else ""
        
        with st.expander(f"{status_icon} {submission['student_name']} - {submission.get('submitted_date', '')[:10]} {late_icon}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Student:** {submission['student_name']}")
                st.write(f"**Email:** {submission['student_email']}")
                st.write(f"**Submitted:** {submission.get('submitted_date', '')[:19]}")
                st.write(f"**Late:** {'Yes' if submission.get('is_late') else 'No'}")
            
            with col2:
                if submission.get('status') == 'graded':
                    st.write(f"**Marks:** {submission.get('marks_awarded')}/{assignment.get('total_marks')}")
                    st.write(f"**Graded By:** {submission.get('graded_by')}")
                    st.write(f"**Graded Date:** {submission.get('graded_date', '')[:10]}")
                else:
                    st.write("**Status:** Not yet graded")
            
            st.markdown("**Submission:**")
            st.write(submission.get('submission_text', ''))
            
            if submission.get('file_url'):
                st.markdown(f"**File:** [Download]({submission['file_url']})")
            
            # Grading section
            if submission.get('status') != 'graded':
                st.markdown("---")
                st.markdown("**Grade This Submission:**")
                
                marks = st.number_input(
                    f"Marks (out of {assignment.get('total_marks')})",
                    min_value=0,
                    max_value=assignment.get('total_marks', 100),
                    value=0,
                    key=f"marks_{submission.get('id')}"
                )
                
                feedback = st.text_area(
                    "Feedback",
                    placeholder="Provide feedback to the student...",
                    key=f"feedback_{submission.get('id')}"
                )
                
                if st.button(f"✅ Submit Grade", key=f"grade_{submission.get('id')}"):
                    result = grade_submission(
                        submission_id=submission.get('id'),
                        marks_awarded=marks,
                        feedback=feedback,
                        graded_by=st.session_state.get('user_email', 'admin')
                    )
                    
                    if result.get('success'):
                        st.success("✅ Submission graded!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.get('error')}")
            else:
                st.markdown("---")
                st.markdown("**Feedback Given:**")
                st.write(submission.get('feedback', 'No feedback'))


def render_assignment_stats():
    """Assignment statistics"""
    
    st.markdown("### 📊 Assignment Statistics")
    
    assignments = get_all_assignments()
    all_submissions = get_submissions()
    
    if not assignments:
        st.info("No assignments created yet.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assignments", len(assignments))
    
    with col2:
        st.metric("Total Submissions", len(all_submissions))
    
    with col3:
        graded = len([s for s in all_submissions if s.get('status') == 'graded'])
        st.metric("Graded Submissions", graded)
    
    # Per assignment stats
    st.markdown("---")
    st.markdown("### Submissions per Assignment")
    
    for assignment in assignments:
        submissions = get_submissions(assignment_id=assignment.get('id'))
        graded_count = len([s for s in submissions if s.get('status') == 'graded'])
        st.write(f"**{assignment['title']}:** {len(submissions)} submissions ({graded_count} graded)")


def render_student_assignments():
    """Student view for assignments"""
    
    st.info("**Student View:** View assignments and submit your work")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "📋 Available Assignments",
        "📥 My Submissions",
        "📊 My Grades"
    ])
    
    with tab1:
        render_available_assignments()
    
    with tab2:
        render_my_submissions()
    
    with tab3:
        render_my_grades()


def render_available_assignments():
    """View available assignments (student)"""
    
    st.markdown("### 📋 Available Assignments")
    
    assignments = get_all_assignments()
    student_email = st.session_state.get('user_email', 'student@example.com')
    
    if not assignments:
        st.info("No assignments available yet.")
        return
    
    for assignment in assignments:
        due_date = assignment.get('due_date', '')
        is_overdue = datetime.fromisoformat(due_date).date() < datetime.now().date() if due_date else False
        
        # Check if already submitted
        submissions = get_submissions(assignment_id=assignment.get('id'), student_email=student_email)
        already_submitted = len(submissions) > 0
        
        status_icon = "✅" if already_submitted else ("🔴" if is_overdue else "📝")
        
        with st.expander(f"{status_icon} {assignment['title']} - Due: {due_date}"):
            st.write(f"**Description:** {assignment['description']}")
            st.write(f"**Week:** {assignment.get('week', 0)}")
            st.write(f"**Due Date:** {due_date}")
            st.write(f"**Total Marks:** {assignment.get('total_marks', 100)}")
            st.write(f"**Pass Mark:** {assignment.get('pass_mark', 50)}")
            
            st.markdown("**Instructions:**")
            st.write(assignment.get('instructions', ''))
            
            if already_submitted:
                st.success("✅ You have already submitted this assignment")
            elif is_overdue and not assignment.get('allow_late_submission'):
                st.error("🔴 Assignment overdue - late submissions not allowed")
            else:
                # Submission form
                st.markdown("---")
                st.markdown("### 📝 Submit Assignment")
                
                submission_text = st.text_area(
                    "Your Submission",
                    placeholder="Type your answer here...",
                    height=200,
                    key=f"sub_text_{assignment.get('id')}"
                )
                
                file_url = st.text_input(
                    "File URL (optional)",
                    placeholder="https://drive.google.com/file/d/...",
                    key=f"file_url_{assignment.get('id')}"
                )
                
                if st.button(f"📤 Submit Assignment", key=f"submit_{assignment.get('id')}", type="primary"):
                    if not submission_text:
                        st.error("Please enter your submission")
                        return
                    
                    result = submit_assignment(
                        assignment_id=assignment.get('id'),
                        student_email=student_email,
                        student_name=st.session_state.get('user_name', student_email),
                        submission_text=submission_text,
                        file_url=file_url,
                        file_name=file_url.split('/')[-1] if file_url else ""
                    )
                    
                    if result.get('success'):
                        st.success(f"✅ {result.get('message')}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error')}")


def render_my_submissions():
    """View my submissions (student)"""
    
    st.markdown("### 📥 My Submissions")
    
    student_email = st.session_state.get('user_email', 'student@example.com')
    submissions = get_submissions(student_email=student_email)
    
    if not submissions:
        st.info("You haven't submitted any assignments yet.")
        return
    
    st.write(f"**Total Submissions: {len(submissions)}**")
    
    for submission in submissions:
        # Get assignment details
        assignments = get_all_assignments()
        assignment = next((a for a in assignments if str(a.get('id')) == str(submission.get('assignment_id'))), None)
        
        status_icon = "✅" if submission.get('status') == 'graded' else "⏳"
        
        with st.expander(f"{status_icon} {assignment['title'] if assignment else 'Assignment'} - {submission.get('submitted_date', '')[:10]}"):
            st.write(f"**Submitted:** {submission.get('submitted_date', '')[:19]}")
            st.write(f"**Status:** {submission.get('status').title()}")
            
            if submission.get('is_late'):
                st.warning("⚠️ Late submission")
            
            st.markdown("**Your Submission:**")
            st.write(submission.get('submission_text', ''))
            
            if submission.get('file_url'):
                st.markdown(f"**File:** [View]({submission['file_url']})")
            
            if submission.get('status') == 'graded':
                st.markdown("---")
                st.success(f"**Grade:** {submission.get('marks_awarded')}/{assignment.get('total_marks') if assignment else 100}")
                st.markdown("**Feedback:**")
                st.write(submission.get('feedback', 'No feedback provided'))


def render_my_grades():
    """View my grades (student)"""
    
    st.markdown("### 📊 My Grades")
    
    student_email = st.session_state.get('user_email', 'student@example.com')
    submissions = get_submissions(student_email=student_email)
    
    graded = [s for s in submissions if s.get('status') == 'graded']
    
    if not graded:
        st.info("No graded assignments yet.")
        return
    
    # Calculate average
    total_marks = sum([s.get('marks_awarded', 0) for s in graded])
    assignments = get_all_assignments()
    max_marks = sum([next((a.get('total_marks', 100) for a in assignments if str(a.get('id')) == str(s.get('assignment_id'))), 100) for s in graded])
    average = (total_marks / max_marks * 100) if max_marks > 0 else 0
    
    st.metric("Average Score", f"{average:.1f}%")
    
    st.markdown("---")
    st.markdown("### Grade Summary")
    
    for submission in graded:
        assignment = next((a for a in assignments if str(a.get('id')) == str(submission.get('assignment_id'))), None)
        
        if assignment:
            marks = submission.get('marks_awarded', 0)
            total = assignment.get('total_marks', 100)
            percentage = (marks / total * 100) if total > 0 else 0
            
            passed = marks >= assignment.get('pass_mark', 50)
            icon = "✅" if passed else "❌"
            
            st.write(f"{icon} **{assignment['title']}:** {marks}/{total} ({percentage:.0f}%)")
