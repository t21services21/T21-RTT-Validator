"""
WAITING LIST MANAGEMENT SYSTEM
Manage patient waiting lists for NHS services

Features:
- Add patients to waiting list
- Track position in queue
- Calculate expected wait time
- Priority ordering
- Remove from waiting list
- Waiting list statistics
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from supabase_client import get_supabase_client
from pathway_management_system import get_pathway_by_id, get_all_pathways


def add_to_waiting_list(
    pathway_id: str,
    patient_id: str,
    patient_name: str,
    specialty: str,
    procedure: str,
    priority: str = "Routine",
    expected_wait_weeks: int = 12,
    notes: str = ""
) -> Dict:
    """Add patient to waiting list"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            return _add_to_waiting_list_supabase(
                supabase, pathway_id, patient_id, patient_name,
                specialty, procedure, priority, expected_wait_weeks, notes
            )
        else:
            return _add_to_waiting_list_local(
                pathway_id, patient_id, patient_name,
                specialty, procedure, priority, expected_wait_weeks, notes
            )
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _add_to_waiting_list_supabase(
    supabase, pathway_id: str, patient_id: str, patient_name: str,
    specialty: str, procedure: str, priority: str,
    expected_wait_weeks: int, notes: str
) -> Dict:
    """Add to waiting list via Supabase"""
    
    try:
        # Get current position (last position + 1)
        result = supabase.table('waiting_list').select('position').order('position', desc=True).limit(1).execute()
        next_position = (result.data[0]['position'] + 1) if result.data else 1
        
        # Calculate expected date
        expected_date = (datetime.now() + timedelta(weeks=expected_wait_weeks)).date()
        
        # Create waiting list entry
        entry_data = {
            'pathway_id': pathway_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'specialty': specialty,
            'procedure': procedure,
            'priority': priority,
            'position': next_position,
            'added_date': datetime.now().date().isoformat(),
            'expected_wait_weeks': expected_wait_weeks,
            'expected_date': expected_date.isoformat(),
            'status': 'waiting',
            'notes': notes,
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        result = supabase.table('waiting_list').insert(entry_data).execute()
        
        # Update pathway
        supabase.table('pathways').update({
            'waiting_list_status': 'waiting',
            'waiting_list_entry_date': datetime.now().date().isoformat(),
            'waiting_list_position': next_position,
            'expected_wait_weeks': expected_wait_weeks
        }).eq('pathway_id', pathway_id).execute()
        
        return {
            'success': True,
            'message': f'Added to waiting list at position {next_position}',
            'position': next_position,
            'expected_date': expected_date.isoformat()
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _add_to_waiting_list_local(
    pathway_id: str, patient_id: str, patient_name: str,
    specialty: str, procedure: str, priority: str,
    expected_wait_weeks: int, notes: str
) -> Dict:
    """Add to waiting list via local storage"""
    
    try:
        import json
        import os
        
        # Load existing waiting list
        wl_file = 'data/waiting_list.json'
        os.makedirs('data', exist_ok=True)
        
        if os.path.exists(wl_file):
            with open(wl_file, 'r') as f:
                waiting_list = json.load(f)
        else:
            waiting_list = []
        
        # Get next position
        next_position = max([entry['position'] for entry in waiting_list], default=0) + 1
        
        # Calculate expected date
        expected_date = (datetime.now() + timedelta(weeks=expected_wait_weeks)).date()
        
        # Create entry
        entry_data = {
            'id': f"WL-{len(waiting_list) + 1:05d}",
            'pathway_id': pathway_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'specialty': specialty,
            'procedure': procedure,
            'priority': priority,
            'position': next_position,
            'added_date': datetime.now().date().isoformat(),
            'expected_wait_weeks': expected_wait_weeks,
            'expected_date': expected_date.isoformat(),
            'status': 'waiting',
            'notes': notes,
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        waiting_list.append(entry_data)
        
        # Save
        with open(wl_file, 'w') as f:
            json.dump(waiting_list, f, indent=2)
        
        return {
            'success': True,
            'message': f'Added to waiting list at position {next_position}',
            'position': next_position,
            'expected_date': expected_date.isoformat()
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_waiting_list(specialty: str = None, status: str = "waiting") -> List[Dict]:
    """Get waiting list entries"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('waiting_list').select('*')
            
            if specialty:
                query = query.eq('specialty', specialty)
            if status:
                query = query.eq('status', status)
            
            result = query.order('position').execute()
            return result.data if result.data else []
        else:
            import json
            import os
            
            wl_file = 'data/waiting_list.json'
            if os.path.exists(wl_file):
                with open(wl_file, 'r') as f:
                    waiting_list = json.load(f)
                
                # Filter
                if specialty:
                    waiting_list = [e for e in waiting_list if e['specialty'] == specialty]
                if status:
                    waiting_list = [e for e in waiting_list if e['status'] == status]
                
                # Sort by position
                waiting_list.sort(key=lambda x: x['position'])
                return waiting_list
            return []
    
    except Exception as e:
        st.error(f"Error getting waiting list: {e}")
        return []


def remove_from_waiting_list(pathway_id: str, reason: str = "") -> Dict:
    """Remove patient from waiting list"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('waiting_list').update({
                'status': 'removed',
                'removed_date': datetime.now().date().isoformat(),
                'removal_reason': reason
            }).eq('pathway_id', pathway_id).execute()
            
            # Update pathway
            supabase.table('pathways').update({
                'waiting_list_status': 'removed'
            }).eq('pathway_id', pathway_id).execute()
            
            return {'success': True, 'message': 'Removed from waiting list'}
        else:
            import json
            import os
            
            wl_file = 'data/waiting_list.json'
            if os.path.exists(wl_file):
                with open(wl_file, 'r') as f:
                    waiting_list = json.load(f)
                
                for entry in waiting_list:
                    if entry['pathway_id'] == pathway_id:
                        entry['status'] = 'removed'
                        entry['removed_date'] = datetime.now().date().isoformat()
                        entry['removal_reason'] = reason
                
                with open(wl_file, 'w') as f:
                    json.dump(waiting_list, f, indent=2)
            
            return {'success': True, 'message': 'Removed from waiting list'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def update_waiting_list_position(pathway_id: str, new_position: int) -> Dict:
    """Update position in waiting list (for priority changes)"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('waiting_list').update({
                'position': new_position,
                'priority_changed_date': datetime.now().date().isoformat()
            }).eq('pathway_id', pathway_id).execute()
            
            return {'success': True, 'message': f'Position updated to {new_position}'}
        else:
            import json
            import os
            
            wl_file = 'data/waiting_list.json'
            if os.path.exists(wl_file):
                with open(wl_file, 'r') as f:
                    waiting_list = json.load(f)
                
                for entry in waiting_list:
                    if entry['pathway_id'] == pathway_id:
                        entry['position'] = new_position
                        entry['priority_changed_date'] = datetime.now().date().isoformat()
                
                with open(wl_file, 'w') as f:
                    json.dump(waiting_list, f, indent=2)
            
            return {'success': True, 'message': f'Position updated to {new_position}'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_waiting_list_stats() -> Dict:
    """Get waiting list statistics"""
    
    waiting_list = get_waiting_list(status="waiting")
    
    if not waiting_list:
        return {
            'total_waiting': 0,
            'by_specialty': {},
            'by_priority': {},
            'avg_wait_weeks': 0
        }
    
    # Calculate stats
    by_specialty = {}
    by_priority = {}
    
    for entry in waiting_list:
        specialty = entry.get('specialty', 'Unknown')
        priority = entry.get('priority', 'Routine')
        
        by_specialty[specialty] = by_specialty.get(specialty, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
    
    avg_wait = sum([e.get('expected_wait_weeks', 0) for e in waiting_list]) / len(waiting_list)
    
    return {
        'total_waiting': len(waiting_list),
        'by_specialty': by_specialty,
        'by_priority': by_priority,
        'avg_wait_weeks': round(avg_wait, 1)
    }


def render_waiting_list_ui():
    """UI for waiting list management"""
    
    st.subheader("📋 Waiting List Management")
    
    st.info("""
    **Waiting List Features:**
    - Add patients to waiting list
    - Track queue position
    - Manage priorities
    - View expected wait times
    """)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "➕ Add to Waiting List",
        "📋 View Waiting List",
        "📊 Statistics"
    ])
    
    with tab1:
        render_add_to_waiting_list()
    
    with tab2:
        render_view_waiting_list()
    
    with tab3:
        render_waiting_list_stats()


def render_add_to_waiting_list():
    """Add patient to waiting list"""
    
    st.markdown("### ➕ Add to Waiting List")
    
    # Get pathways not on waiting list
    pathways = get_all_pathways()
    available_pathways = [p for p in pathways if p.get('waiting_list_status') != 'waiting']
    
    if not available_pathways:
        st.warning("No pathways available. All patients are already on waiting list or no pathways exist.")
        return
    
    # Select pathway
    pathway_options = {f"{p['pathway_id']} - {p['patient_name']} ({p['specialty']})": p for p in available_pathways}
    selected = st.selectbox("Select Pathway:", ["-- Select Pathway --"] + list(pathway_options.keys()))
    
    if selected == "-- Select Pathway --":
        return
    
    pathway = pathway_options[selected]
    
    col1, col2 = st.columns(2)
    
    with col1:
        procedure = st.text_input("Procedure/Treatment", placeholder="e.g., Hip Replacement")
        priority = st.selectbox("Priority", ["Routine", "Urgent", "Expedited", "Emergency"])
    
    with col2:
        expected_wait_weeks = st.number_input("Expected Wait (weeks)", min_value=1, max_value=52, value=12)
        notes = st.text_area("Notes", placeholder="Additional information...")
    
    if st.button("➕ Add to Waiting List", type="primary"):
        if not procedure:
            st.error("Please enter procedure/treatment")
            return
        
        result = add_to_waiting_list(
            pathway_id=pathway['pathway_id'],
            patient_id=pathway['patient_id'],
            patient_name=pathway['patient_name'],
            specialty=pathway.get('specialty', 'Unknown'),
            procedure=procedure,
            priority=priority,
            expected_wait_weeks=expected_wait_weeks,
            notes=notes
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            st.info(f"📅 Expected date: {result.get('expected_date')}")
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_view_waiting_list():
    """View waiting list"""
    
    st.markdown("### 📋 Current Waiting List")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        specialty_filter = st.selectbox("Filter by Specialty:", ["All"] + [
            "Cardiology", "Dermatology", "ENT", "Gastroenterology",
            "General Surgery", "Neurology", "Ophthalmology", "Orthopaedics",
            "Respiratory", "Rheumatology", "Urology", "Oncology"
        ])
    
    with col2:
        status_filter = st.selectbox("Filter by Status:", ["waiting", "removed", "all"])
    
    # Get waiting list
    specialty = None if specialty_filter == "All" else specialty_filter
    status = None if status_filter == "all" else status_filter
    
    waiting_list = get_waiting_list(specialty=specialty, status=status)
    
    if not waiting_list:
        st.info("No patients on waiting list matching filters.")
        return
    
    st.write(f"**Total: {len(waiting_list)} patients**")
    
    # Display list
    for entry in waiting_list:
        priority_icon = "🔴" if entry['priority'] == "Urgent" else "🟢"
        status_icon = "⏳" if entry['status'] == "waiting" else "✅"
        
        with st.expander(f"{status_icon} {priority_icon} Position {entry['position']}: {entry['patient_name']} - {entry['procedure']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Patient:** {entry['patient_name']}")
                st.write(f"**Pathway ID:** {entry['pathway_id']}")
                st.write(f"**Specialty:** {entry['specialty']}")
                st.write(f"**Procedure:** {entry['procedure']}")
            
            with col2:
                st.write(f"**Priority:** {entry['priority']}")
                st.write(f"**Position:** {entry['position']}")
                st.write(f"**Added:** {entry['added_date']}")
                st.write(f"**Expected Wait:** {entry['expected_wait_weeks']} weeks")
                st.write(f"**Expected Date:** {entry.get('expected_date', 'N/A')}")
            
            if entry.get('notes'):
                st.info(f"**Notes:** {entry['notes']}")
            
            if entry['status'] == "waiting":
                if st.button(f"🗑️ Remove from List", key=f"remove_{entry['pathway_id']}"):
                    reason = st.text_input("Removal Reason:", key=f"reason_{entry['pathway_id']}")
                    result = remove_from_waiting_list(entry['pathway_id'], reason)
                    if result.get('success'):
                        st.success("✅ Removed from waiting list")
                        st.rerun()


def render_waiting_list_stats():
    """Show waiting list statistics"""
    
    st.markdown("### 📊 Waiting List Statistics")
    
    stats = get_waiting_list_stats()
    
    # Overall stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Waiting", stats['total_waiting'])
    
    with col2:
        st.metric("Average Wait", f"{stats['avg_wait_weeks']} weeks")
    
    with col3:
        longest_wait = max([e.get('expected_wait_weeks', 0) for e in get_waiting_list(status="waiting")], default=0)
        st.metric("Longest Wait", f"{longest_wait} weeks")
    
    # By specialty
    st.markdown("---")
    st.markdown("### By Specialty")
    
    if stats['by_specialty']:
        for specialty, count in stats['by_specialty'].items():
            st.write(f"**{specialty}:** {count} patients")
    else:
        st.info("No data available")
    
    # By priority
    st.markdown("---")
    st.markdown("### By Priority")
    
    if stats['by_priority']:
        for priority, count in stats['by_priority'].items():
            st.write(f"**{priority}:** {count} patients")
    else:
        st.info("No data available")
