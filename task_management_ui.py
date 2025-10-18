"""
TASK MANAGEMENT UI
User interface for task tracking and management
"""

import streamlit as st
from datetime import datetime, timedelta
from task_management_system import (
    create_task,
    get_all_tasks,
    get_tasks_by_status,
    get_overdue_tasks,
    get_tasks_due_soon,
    update_task_status,
    get_task_stats,
    delete_task,
    get_task_by_id
)


def render_task_management():
    """Main task management interface"""
    
    st.header("✅ Task Management")
    st.markdown("**Track MDT Actions, Appointments & Clinical Tasks**")
    
    # Get task statistics
    stats = get_task_stats()
    
    # Summary Dashboard
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Tasks", stats['total'])
    with col2:
        st.metric("⏳ Pending", stats['pending'])
    with col3:
        st.metric("🔄 In Progress", stats['in_progress'])
    with col4:
        st.metric("⚠️ Overdue", stats['overdue'], delta=None if stats['overdue'] == 0 else "Action Required")
    with col5:
        st.metric("✅ Completed", stats['completed'])
    
    # Priority breakdown
    st.markdown("---")
    st.markdown("### 📊 Tasks by Priority")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 URGENT", stats['by_priority']['URGENT'])
    with col2:
        st.metric("🟠 HIGH", stats['by_priority']['HIGH'])
    with col3:
        st.metric("🟡 MEDIUM", stats['by_priority']['MEDIUM'])
    with col4:
        st.metric("🟢 LOW", stats['by_priority']['LOW'])
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 All Tasks",
        "⚠️ Overdue",
        "📅 Due Soon",
        "➕ Create Task",
        "📊 Analytics"
    ])
    
    with tab1:
        render_all_tasks()
    
    with tab2:
        render_overdue_tasks()
    
    with tab3:
        render_due_soon_tasks()
    
    with tab4:
        render_create_task()
    
    with tab5:
        render_task_analytics(stats)


def render_all_tasks():
    """Display all tasks with filtering"""
    st.markdown("### 📋 All Tasks")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "PENDING", "IN_PROGRESS", "COMPLETED"], key="status_filter_all")
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "URGENT", "HIGH", "MEDIUM", "LOW"], key="priority_filter_all")
    with col3:
        type_filter = st.selectbox("Type", ["All", "MDT_ACTION", "APPOINTMENT", "CLINICAL", "ADMIN"], key="type_filter_all")
    
    # Get tasks
    if status_filter == "All":
        tasks = get_all_tasks(include_completed=True)
    else:
        tasks = get_tasks_by_status(status_filter)
    
    # Apply filters
    if priority_filter != "All":
        tasks = [t for t in tasks if t.get('priority') == priority_filter]
    if type_filter != "All":
        tasks = [t for t in tasks if t.get('task_type') == type_filter]
    
    # Sort by due date
    tasks.sort(key=lambda x: (x.get('due_date', ''), x.get('priority', 'LOW')))
    
    if tasks:
        st.markdown(f"**{len(tasks)} task(s) found**")
        render_task_list(tasks)
    else:
        st.info("📭 No tasks found with selected filters")


def render_overdue_tasks():
    """Display overdue tasks"""
    st.markdown("### ⚠️ Overdue Tasks")
    
    overdue = get_overdue_tasks()
    
    if overdue:
        st.error(f"**{len(overdue)} overdue task(s) requiring immediate attention!**")
        render_task_list(overdue, show_overdue_warning=True)
    else:
        st.success("✅ No overdue tasks! Great work!")


def render_due_soon_tasks():
    """Display tasks due soon"""
    st.markdown("### 📅 Tasks Due Soon")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        days = st.selectbox("Due within", [3, 7, 14, 30], index=1)
    
    due_soon = get_tasks_due_soon(days=days)
    
    if due_soon:
        st.warning(f"**{len(due_soon)} task(s) due within {days} days**")
        render_task_list(due_soon)
    else:
        st.success(f"✅ No tasks due within {days} days!")


def render_task_list(tasks: list, show_overdue_warning: bool = False):
    """Render list of tasks"""
    
    for task in tasks:
        # Priority icon
        priority = task.get('priority', 'MEDIUM')
        if priority == 'URGENT':
            priority_icon = "🔴"
        elif priority == 'HIGH':
            priority_icon = "🟠"
        elif priority == 'MEDIUM':
            priority_icon = "🟡"
        else:
            priority_icon = "🟢"
        
        # Status icon
        status = task.get('status', 'PENDING')
        if status == 'COMPLETED':
            status_icon = "✅"
        elif status == 'IN_PROGRESS':
            status_icon = "🔄"
        else:
            status_icon = "⏳"
        
        # Check if overdue
        is_overdue = False
        try:
            due_date = datetime.fromisoformat(task.get('due_date', '')).date()
            is_overdue = due_date < datetime.now().date() and status != 'COMPLETED'
        except:
            pass
        
        overdue_marker = "⚠️ OVERDUE! " if is_overdue and show_overdue_warning else ""
        
        with st.expander(f"{priority_icon} {status_icon} {overdue_marker}{task.get('title', 'Untitled Task')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Task ID:** {task.get('task_id', 'N/A')}")
                st.markdown(f"**Type:** {task.get('task_type', 'N/A')}")
                st.markdown(f"**Priority:** {priority_icon} {priority}")
                st.markdown(f"**Status:** {status_icon} {status}")
                st.markdown(f"**Due Date:** {task.get('due_date', 'N/A')}")
            
            with col2:
                st.markdown(f"**Assigned To:** {task.get('assigned_to', 'N/A')}")
                st.markdown(f"**Created By:** {task.get('created_by', 'N/A')}")
                if task.get('patient_nhs'):
                    st.markdown(f"**Patient NHS:** {task.get('patient_nhs')}")
                if task.get('related_module'):
                    st.markdown(f"**Related Module:** {task.get('related_module')}")
                st.markdown(f"**Created:** {task.get('created_at', 'N/A')[:10]}")
            
            st.markdown(f"**Description:**")
            st.info(task.get('description', 'No description'))
            
            # Notes
            if task.get('notes'):
                st.markdown("**Notes:**")
                for note in task.get('notes', []):
                    st.caption(f"🗒️ {note.get('date', 'N/A')[:10]} - {note.get('user', 'Unknown')}: {note.get('note', '')}")
            
            # Actions
            col_a, col_b, col_c, col_d = st.columns(4)
            
            if status != 'COMPLETED':
                with col_a:
                    if st.button("🔄 In Progress", key=f"progress_{task['task_id']}", use_container_width=True):
                        if update_task_status(task['task_id'], 'IN_PROGRESS'):
                            st.success("✅ Status updated!")
                            st.rerun()
                
                with col_b:
                    if st.button("✅ Complete", key=f"complete_{task['task_id']}", use_container_width=True):
                        st.session_state[f"completing_{task['task_id']}"] = True
                
                with col_c:
                    if st.button("📝 Add Note", key=f"note_{task['task_id']}", use_container_width=True):
                        st.session_state[f"adding_note_{task['task_id']}"] = True
            
            with col_d:
                if st.button("🗑️ Delete", key=f"delete_{task['task_id']}", use_container_width=True):
                    if delete_task(task['task_id']):
                        st.success("✅ Task deleted!")
                        st.rerun()
            
            # Complete task form
            if st.session_state.get(f"completing_{task['task_id']}"):
                with st.form(f"complete_form_{task['task_id']}"):
                    completion_notes = st.text_area("Completion Notes", placeholder="Task completed successfully...")
                    
                    col_x, col_y = st.columns(2)
                    with col_x:
                        if st.form_submit_button("✅ Confirm Complete", type="primary", use_container_width=True):
                            if update_task_status(task['task_id'], 'COMPLETED', completion_notes):
                                st.success("✅ Task completed!")
                                del st.session_state[f"completing_{task['task_id']}"]
                                st.rerun()
                    with col_y:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            del st.session_state[f"completing_{task['task_id']}"]
                            st.rerun()
            
            # Add note form
            if st.session_state.get(f"adding_note_{task['task_id']}"):
                with st.form(f"note_form_{task['task_id']}"):
                    new_note = st.text_area("Add Note", placeholder="Progress update...")
                    
                    col_x, col_y = st.columns(2)
                    with col_x:
                        if st.form_submit_button("💾 Save Note", type="primary", use_container_width=True):
                            if update_task_status(task['task_id'], status, new_note):
                                st.success("✅ Note added!")
                                del st.session_state[f"adding_note_{task['task_id']}"]
                                st.rerun()
                    with col_y:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            del st.session_state[f"adding_note_{task['task_id']}"]
                            st.rerun()


def render_create_task():
    """Create new task form"""
    st.markdown("### ➕ Create New Task")
    
    with st.form("create_task_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Task Title*", placeholder="e.g., Book surgery for patient")
            task_type = st.selectbox("Task Type*", ["MDT_ACTION", "APPOINTMENT", "CLINICAL", "ADMIN"])
            priority = st.selectbox("Priority*", ["LOW", "MEDIUM", "HIGH", "URGENT"])
            due_date = st.date_input("Due Date*", value=datetime.now() + timedelta(days=7))
        
        with col2:
            assigned_to = st.text_input("Assigned To (email)", placeholder="Leave blank for self")
            patient_nhs = st.text_input("Patient NHS Number (optional)", placeholder="123 456 7890")
            related_module = st.selectbox("Related Module (optional)", ["", "PTL", "Cancer", "MDT", "Appointments"])
            related_id = st.text_input("Related ID (optional)", placeholder="Meeting/Appointment ID")
        
        description = st.text_area("Description*", height=100, placeholder="Detailed task description...")
        
        if st.form_submit_button("➕ Create Task", type="primary"):
            if title and description:
                task_id = create_task(
                    title=title,
                    description=description,
                    task_type=task_type,
                    priority=priority,
                    due_date=str(due_date),
                    assigned_to=assigned_to if assigned_to else None,
                    patient_nhs=patient_nhs if patient_nhs else None,
                    related_id=related_id if related_id else None,
                    related_module=related_module if related_module else None
                )
                
                if task_id:
                    st.balloons()
                    st.success(f"""
                    ✅ **TASK CREATED SUCCESSFULLY!**
                    
                    **Task ID:** {task_id}  
                    **Priority:** {priority}  
                    **Due Date:** {due_date}  
                    **Assigned To:** {assigned_to}  
                    
                    ✔️ Task has been saved and is now active!  
                    📋 Team member will be notified!
                    """)
                    st.info("💡 **Next Steps:** Track task progress in the dashboard or update status as work progresses.")
                else:
                    st.error("❌ Failed to create task")
            else:
                st.error("❌ Please fill in title and description")


def render_task_analytics(stats: dict):
    """Display task analytics"""
    st.markdown("### 📊 Task Analytics")
    
    # Completion rate
    if stats['total'] > 0:
        completion_rate = (stats['completed'] / stats['total'] * 100)
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        if completion_rate >= 80:
            st.success(f"✅ Excellent completion rate!")
        elif completion_rate >= 60:
            st.info(f"ℹ️ Good completion rate")
        else:
            st.warning(f"⚠️ Completion rate needs improvement")
    
    # Tasks by type
    st.markdown("#### Tasks by Type")
    for task_type, count in stats['by_type'].items():
        st.markdown(f"- **{task_type}:** {count}")
    
    # Overdue analysis
    if stats['overdue'] > 0:
        st.markdown("---")
        st.error(f"⚠️ **{stats['overdue']} overdue tasks** requiring immediate attention!")
        st.markdown("**Recommended Actions:**")
        st.markdown("- Review and prioritize overdue tasks")
        st.markdown("- Delegate if necessary")
        st.markdown("- Update due dates if realistic")
        st.markdown("- Complete or cancel if no longer needed")
