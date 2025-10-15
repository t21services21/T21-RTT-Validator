"""
TASK MANAGEMENT SYSTEM
Track MDT actions, appointments, and clinical tasks

Features:
- Create tasks from MDT decisions
- Assign tasks to users
- Track task completion
- Reminders for overdue tasks
- Task priority management
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
from session_manager import get_current_user_email
from config import SUPABASE_ENABLED

if SUPABASE_ENABLED:
    from supabase_database import (
        supabase_create_task,
        supabase_get_tasks_for_user,
        supabase_update_task,
        supabase_delete_task
    )

TASKS_DB = "tasks.json"


def load_tasks():
    """Load tasks database"""
    user_email = get_current_user_email()
    if SUPABASE_ENABLED:
        try:
            from supabase_database import get_tasks_for_user
            return {'tasks': get_tasks_for_user(user_email)}
        except:
            pass
    
    if os.path.exists(TASKS_DB):
        with open(TASKS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'tasks': []}


def save_tasks(data):
    """Save tasks database - deprecated with Supabase"""
    if not SUPABASE_ENABLED:
        with open(TASKS_DB, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def create_task(
    title: str,
    description: str,
    task_type: str,  # 'MDT_ACTION', 'APPOINTMENT', 'CLINICAL', 'ADMIN'
    priority: str,  # 'LOW', 'MEDIUM', 'HIGH', 'URGENT'
    due_date: str,
    assigned_to: str = None,
    patient_nhs: str = None,
    related_id: str = None,  # meeting_id, appointment_id, etc.
    related_module: str = None  # 'MDT', 'Cancer', 'PTL', etc.
) -> str:
    """Create a new task"""
    
    user_email = get_current_user_email()
    task_id = f"TASK_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    task_data = {
        'task_id': task_id,
        'title': title,
        'description': description,
        'task_type': task_type,
        'priority': priority,
        'due_date': due_date,
        'assigned_to': assigned_to or user_email,
        'created_by': user_email,
        'patient_nhs': patient_nhs,
        'related_id': related_id,
        'related_module': related_module,
        'status': 'PENDING',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'completed_at': None,
        'notes': []
    }
    
    if SUPABASE_ENABLED:
        try:
            success, result = supabase_create_task(user_email, task_data)
            if success:
                return task_id
            else:
                print(f"❌ Error creating task: {result}")
                import streamlit as st
                st.error(f"❌ Failed to create task: {result}")
                return None
        except Exception as e:
            print(f"❌ Exception creating task: {e}")
            return None
    else:
        # Fallback to local storage
        tasks = load_tasks()
        tasks['tasks'].append(task_data)
        save_tasks(tasks)
        return task_id


def create_tasks_from_mdt_actions(
    meeting_id: str,
    patient_nhs: str,
    patient_name: str,
    actions: List[str],
    due_date: str = None
) -> List[str]:
    """Create multiple tasks from MDT action list"""
    
    if not due_date:
        # Default to 2 weeks from now
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    
    task_ids = []
    
    for action in actions:
        if action.strip():
            task_id = create_task(
                title=f"MDT Action: {action[:50]}",
                description=f"Patient: {patient_name} (NHS: {patient_nhs})\nAction: {action}",
                task_type='MDT_ACTION',
                priority='HIGH',
                due_date=due_date,
                patient_nhs=patient_nhs,
                related_id=meeting_id,
                related_module='MDT'
            )
            if task_id:
                task_ids.append(task_id)
    
    return task_ids


def get_all_tasks(include_completed: bool = False) -> List[Dict]:
    """Get all tasks for current user"""
    tasks_data = load_tasks()
    tasks = tasks_data.get('tasks', [])
    
    if not include_completed:
        tasks = [t for t in tasks if t.get('status') != 'COMPLETED']
    
    return tasks


def get_tasks_by_status(status: str) -> List[Dict]:
    """Get tasks by status"""
    all_tasks = get_all_tasks(include_completed=True)
    return [t for t in all_tasks if t.get('status', '').upper() == status.upper()]


def get_overdue_tasks() -> List[Dict]:
    """Get overdue tasks"""
    all_tasks = get_all_tasks(include_completed=False)
    today = datetime.now().date()
    
    overdue = []
    for task in all_tasks:
        try:
            due_date = datetime.fromisoformat(task.get('due_date', '')).date()
            if due_date < today:
                overdue.append(task)
        except:
            continue
    
    return overdue


def get_tasks_due_soon(days: int = 7) -> List[Dict]:
    """Get tasks due within specified days"""
    all_tasks = get_all_tasks(include_completed=False)
    today = datetime.now().date()
    target_date = today + timedelta(days=days)
    
    due_soon = []
    for task in all_tasks:
        try:
            due_date = datetime.fromisoformat(task.get('due_date', '')).date()
            if today <= due_date <= target_date:
                due_soon.append(task)
        except:
            continue
    
    return due_soon


def update_task_status(task_id: str, status: str, notes: str = "") -> bool:
    """Update task status"""
    user_email = get_current_user_email()
    
    updates = {
        'status': status,
        'updated_at': datetime.now().isoformat()
    }
    
    if status == 'COMPLETED':
        updates['completed_at'] = datetime.now().isoformat()
    
    if notes:
        task = get_task_by_id(task_id)
        if task:
            task_notes = task.get('notes', [])
            task_notes.append({
                'date': datetime.now().isoformat(),
                'user': user_email,
                'note': notes
            })
            updates['notes'] = task_notes
    
    if SUPABASE_ENABLED:
        try:
            success, _ = supabase_update_task(user_email, task_id, updates)
            return success
        except:
            return False
    else:
        tasks = load_tasks()
        for task in tasks['tasks']:
            if task['task_id'] == task_id:
                task.update(updates)
                save_tasks(tasks)
                return True
        return False


def get_task_by_id(task_id: str) -> Optional[Dict]:
    """Get specific task by ID"""
    all_tasks = get_all_tasks(include_completed=True)
    return next((t for t in all_tasks if t['task_id'] == task_id), None)


def delete_task(task_id: str) -> bool:
    """Delete a task"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            return supabase_delete_task(user_email, task_id)
        except:
            return False
    else:
        tasks = load_tasks()
        tasks['tasks'] = [t for t in tasks['tasks'] if t['task_id'] != task_id]
        save_tasks(tasks)
        return True


def get_task_stats() -> Dict:
    """Get task statistics"""
    all_tasks = get_all_tasks(include_completed=True)
    
    stats = {
        'total': len(all_tasks),
        'pending': len([t for t in all_tasks if t.get('status') == 'PENDING']),
        'in_progress': len([t for t in all_tasks if t.get('status') == 'IN_PROGRESS']),
        'completed': len([t for t in all_tasks if t.get('status') == 'COMPLETED']),
        'overdue': len(get_overdue_tasks()),
        'due_this_week': len(get_tasks_due_soon(7)),
        'by_priority': {
            'URGENT': len([t for t in all_tasks if t.get('priority') == 'URGENT' and t.get('status') != 'COMPLETED']),
            'HIGH': len([t for t in all_tasks if t.get('priority') == 'HIGH' and t.get('status') != 'COMPLETED']),
            'MEDIUM': len([t for t in all_tasks if t.get('priority') == 'MEDIUM' and t.get('status') != 'COMPLETED']),
            'LOW': len([t for t in all_tasks if t.get('priority') == 'LOW' and t.get('status') != 'COMPLETED'])
        },
        'by_type': {}
    }
    
    # Count by type
    for task in all_tasks:
        if task.get('status') != 'COMPLETED':
            task_type = task.get('task_type', 'UNKNOWN')
            stats['by_type'][task_type] = stats['by_type'].get(task_type, 0) + 1
    
    return stats
