"""
APPOINTMENT-PATHWAY LINKING SYSTEM
Link appointments from booking system to RTT pathways

Features:
- Link appointments to pathways
- Track first appointment
- Show appointments in pathway timeline
- Update pathway milestones automatically
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
from pathway_management_system import (
    get_pathway_by_id,
    record_milestone,
    get_all_pathways
)
from supabase_client import get_supabase_client


def link_appointment_to_pathway(
    appointment_id: str,
    pathway_id: str,
    appointment_date: str,
    appointment_type: str = "First Appointment",
    consultant: str = "",
    clinic: str = "",
    outcome: str = ""
) -> Dict:
    """Link an appointment to a pathway"""
    
    try:
        # Check if using Supabase
        supabase = get_supabase_client()
        
        if supabase:
            return _link_appointment_supabase(
                supabase, appointment_id, pathway_id, appointment_date,
                appointment_type, consultant, clinic, outcome
            )
        else:
            return _link_appointment_local(
                appointment_id, pathway_id, appointment_date,
                appointment_type, consultant, clinic, outcome
            )
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _link_appointment_supabase(
    supabase, appointment_id: str, pathway_id: str,
    appointment_date: str, appointment_type: str,
    consultant: str, clinic: str, outcome: str
) -> Dict:
    """Link appointment via Supabase"""
    
    try:
        # Create appointment-pathway link
        link_data = {
            'appointment_id': appointment_id,
            'pathway_id': pathway_id,
            'appointment_date': appointment_date,
            'appointment_type': appointment_type,
            'consultant': consultant,
            'clinic': clinic,
            'outcome': outcome,
            'linked_date': datetime.now().isoformat(),
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        result = supabase.table('appointment_pathway_links').insert(link_data).execute()
        
        # If first appointment, update pathway milestone
        if appointment_type == "First Appointment":
            record_milestone(
                pathway_id=pathway_id,
                milestone_type='first_appointment',
                milestone_date=appointment_date,
                appointment_attended=True,
                consultant=consultant,
                clinic=clinic
            )
        
        return {
            'success': True,
            'message': 'Appointment linked to pathway successfully',
            'link_id': result.data[0].get('id') if result.data else None
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _link_appointment_local(
    appointment_id: str, pathway_id: str,
    appointment_date: str, appointment_type: str,
    consultant: str, clinic: str, outcome: str
) -> Dict:
    """Link appointment via local storage"""
    
    try:
        import json
        import os
        
        # Load existing links
        links_file = 'data/appointment_pathway_links.json'
        os.makedirs('data', exist_ok=True)
        
        if os.path.exists(links_file):
            with open(links_file, 'r') as f:
                links = json.load(f)
        else:
            links = []
        
        # Create new link
        link_data = {
            'id': f"APL-{len(links) + 1:05d}",
            'appointment_id': appointment_id,
            'pathway_id': pathway_id,
            'appointment_date': appointment_date,
            'appointment_type': appointment_type,
            'consultant': consultant,
            'clinic': clinic,
            'outcome': outcome,
            'linked_date': datetime.now().isoformat(),
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        links.append(link_data)
        
        # Save
        with open(links_file, 'w') as f:
            json.dump(links, f, indent=2)
        
        # If first appointment, update pathway milestone
        if appointment_type == "First Appointment":
            record_milestone(
                pathway_id=pathway_id,
                milestone_type='first_appointment',
                milestone_date=appointment_date,
                appointment_attended=True,
                consultant=consultant,
                clinic=clinic
            )
        
        return {
            'success': True,
            'message': 'Appointment linked to pathway successfully',
            'link_id': link_data['id']
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_pathway_appointments(pathway_id: str) -> List[Dict]:
    """Get all appointments linked to a pathway"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('appointment_pathway_links')\
                .select('*')\
                .eq('pathway_id', pathway_id)\
                .execute()
            return result.data if result.data else []
        else:
            import json
            import os
            
            links_file = 'data/appointment_pathway_links.json'
            if os.path.exists(links_file):
                with open(links_file, 'r') as f:
                    links = json.load(f)
                return [link for link in links if link['pathway_id'] == pathway_id]
            return []
    
    except Exception as e:
        st.error(f"Error getting pathway appointments: {e}")
        return []


def get_appointment_pathway(appointment_id: str) -> Optional[Dict]:
    """Get pathway linked to an appointment"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('appointment_pathway_links')\
                .select('*')\
                .eq('appointment_id', appointment_id)\
                .execute()
            return result.data[0] if result.data else None
        else:
            import json
            import os
            
            links_file = 'data/appointment_pathway_links.json'
            if os.path.exists(links_file):
                with open(links_file, 'r') as f:
                    links = json.load(f)
                for link in links:
                    if link['appointment_id'] == appointment_id:
                        return link
            return None
    
    except Exception as e:
        st.error(f"Error getting appointment pathway: {e}")
        return None


def unlink_appointment(appointment_id: str) -> Dict:
    """Remove appointment-pathway link"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('appointment_pathway_links')\
                .delete()\
                .eq('appointment_id', appointment_id)\
                .execute()
            return {'success': True, 'message': 'Appointment unlinked'}
        else:
            import json
            import os
            
            links_file = 'data/appointment_pathway_links.json'
            if os.path.exists(links_file):
                with open(links_file, 'r') as f:
                    links = json.load(f)
                
                links = [link for link in links if link['appointment_id'] != appointment_id]
                
                with open(links_file, 'w') as f:
                    json.dump(links, f, indent=2)
            
            return {'success': True, 'message': 'Appointment unlinked'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_appointment_linking_ui():
    """UI for linking appointments to pathways"""
    
    st.subheader("🔗 Link Appointment to Pathway")
    
    st.info("""
    **Link appointments to RTT pathways to:**
    - Track first appointment milestone
    - Show appointments in pathway timeline
    - Automatically update pathway progress
    """)
    
    # Get all pathways
    pathways = get_all_pathways()
    
    if not pathways:
        st.warning("No pathways found. Create a pathway first.")
        return
    
    # Select pathway
    pathway_options = {f"{p['pathway_id']} - {p['patient_name']} ({p['specialty']})": p['pathway_id'] for p in pathways}
    selected_pathway = st.selectbox("Select Pathway:", ["-- Select Pathway --"] + list(pathway_options.keys()))
    
    if selected_pathway == "-- Select Pathway --":
        return
    
    pathway_id = pathway_options[selected_pathway]
    
    # Appointment details
    col1, col2 = st.columns(2)
    
    with col1:
        appointment_id = st.text_input("Appointment ID", placeholder="e.g., APT-12345")
        appointment_date = st.date_input("Appointment Date")
        appointment_type = st.selectbox(
            "Appointment Type",
            ["First Appointment", "Follow-up", "Treatment", "Pre-op", "Post-op", "Other"]
        )
    
    with col2:
        consultant = st.text_input("Consultant", placeholder="e.g., Dr Smith")
        clinic = st.text_input("Clinic", placeholder="e.g., Orthopaedics")
        outcome = st.text_area("Outcome/Notes", placeholder="Appointment outcome...")
    
    if st.button("🔗 Link Appointment to Pathway", type="primary"):
        if not appointment_id:
            st.error("Please enter appointment ID")
            return
        
        result = link_appointment_to_pathway(
            appointment_id=appointment_id,
            pathway_id=pathway_id,
            appointment_date=str(appointment_date),
            appointment_type=appointment_type,
            consultant=consultant,
            clinic=clinic,
            outcome=outcome
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            if appointment_type == "First Appointment":
                st.info("📅 First appointment milestone recorded automatically!")
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")
    
    # Show linked appointments
    st.markdown("---")
    st.markdown("### 📋 Linked Appointments")
    
    linked_appointments = get_pathway_appointments(pathway_id)
    
    if linked_appointments:
        for appt in linked_appointments:
            with st.expander(f"📅 {appt['appointment_id']} - {appt['appointment_date']} ({appt['appointment_type']})"):
                st.write(f"**Type:** {appt['appointment_type']}")
                st.write(f"**Date:** {appt['appointment_date']}")
                st.write(f"**Consultant:** {appt.get('consultant', 'N/A')}")
                st.write(f"**Clinic:** {appt.get('clinic', 'N/A')}")
                st.write(f"**Outcome:** {appt.get('outcome', 'N/A')}")
                st.write(f"**Linked:** {appt.get('linked_date', 'N/A')}")
                
                if st.button(f"🗑️ Unlink {appt['appointment_id']}", key=f"unlink_{appt['appointment_id']}"):
                    unlink_result = unlink_appointment(appt['appointment_id'])
                    if unlink_result.get('success'):
                        st.success("✅ Appointment unlinked")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {unlink_result.get('error')}")
    else:
        st.info("No appointments linked to this pathway yet.")
