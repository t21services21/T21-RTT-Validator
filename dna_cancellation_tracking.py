"""
DNA & CANCELLATION TRACKING SYSTEM
Track Did Not Attend (DNA) and appointment cancellations

Features:
- Record DNA events
- Record cancellations (patient/hospital)
- Track DNA count per pathway
- Impact on RTT clock
- Generate DNA reports
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List
from supabase_client import get_supabase_client
from pathway_management_system import get_pathway_by_id, get_all_pathways


def record_dna(
    pathway_id: str,
    patient_id: str,
    patient_name: str,
    appointment_id: str,
    appointment_date: str,
    appointment_type: str,
    clinic: str = "",
    consultant: str = "",
    notes: str = ""
) -> Dict:
    """Record a DNA (Did Not Attend) event"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            return _record_dna_supabase(
                supabase, pathway_id, patient_id, patient_name,
                appointment_id, appointment_date, appointment_type,
                clinic, consultant, notes
            )
        else:
            return _record_dna_local(
                pathway_id, patient_id, patient_name,
                appointment_id, appointment_date, appointment_type,
                clinic, consultant, notes
            )
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _record_dna_supabase(
    supabase, pathway_id: str, patient_id: str, patient_name: str,
    appointment_id: str, appointment_date: str, appointment_type: str,
    clinic: str, consultant: str, notes: str
) -> Dict:
    """Record DNA via Supabase"""
    
    try:
        # Create DNA record
        dna_data = {
            'pathway_id': pathway_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'appointment_id': appointment_id,
            'appointment_date': appointment_date,
            'appointment_type': appointment_type,
            'clinic': clinic,
            'consultant': consultant,
            'recorded_date': datetime.now().date().isoformat(),
            'notes': notes,
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        result = supabase.table('dna_records').insert(dna_data).execute()
        
        # Update pathway DNA count
        pathway = get_pathway_by_id(pathway_id)
        current_dna_count = pathway.get('dna_count', 0) if pathway else 0
        
        supabase.table('pathways').update({
            'dna_count': current_dna_count + 1,
            'last_dna_date': appointment_date
        }).eq('pathway_id', pathway_id).execute()
        
        return {
            'success': True,
            'message': f'DNA recorded for appointment {appointment_id}',
            'dna_count': current_dna_count + 1
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _record_dna_local(
    pathway_id: str, patient_id: str, patient_name: str,
    appointment_id: str, appointment_date: str, appointment_type: str,
    clinic: str, consultant: str, notes: str
) -> Dict:
    """Record DNA via local storage"""
    
    try:
        import json
        import os
        
        # Load existing DNA records
        dna_file = 'data/dna_records.json'
        os.makedirs('data', exist_ok=True)
        
        if os.path.exists(dna_file):
            with open(dna_file, 'r') as f:
                dna_records = json.load(f)
        else:
            dna_records = []
        
        # Create DNA record
        dna_data = {
            'id': f"DNA-{len(dna_records) + 1:05d}",
            'pathway_id': pathway_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'appointment_id': appointment_id,
            'appointment_date': appointment_date,
            'appointment_type': appointment_type,
            'clinic': clinic,
            'consultant': consultant,
            'recorded_date': datetime.now().date().isoformat(),
            'notes': notes,
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        dna_records.append(dna_data)
        
        # Save
        with open(dna_file, 'w') as f:
            json.dump(dna_records, f, indent=2)
        
        # Count DNAs for this pathway
        pathway_dna_count = len([r for r in dna_records if r['pathway_id'] == pathway_id])
        
        return {
            'success': True,
            'message': f'DNA recorded for appointment {appointment_id}',
            'dna_count': pathway_dna_count
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def record_cancellation(
    pathway_id: str,
    patient_id: str,
    patient_name: str,
    appointment_id: str,
    appointment_date: str,
    appointment_type: str,
    cancelled_by: str,  # "Patient" or "Hospital"
    reason: str,
    rebook_required: bool = True,
    clinic: str = "",
    consultant: str = "",
    notes: str = ""
) -> Dict:
    """Record an appointment cancellation"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            return _record_cancellation_supabase(
                supabase, pathway_id, patient_id, patient_name,
                appointment_id, appointment_date, appointment_type,
                cancelled_by, reason, rebook_required, clinic, consultant, notes
            )
        else:
            return _record_cancellation_local(
                pathway_id, patient_id, patient_name,
                appointment_id, appointment_date, appointment_type,
                cancelled_by, reason, rebook_required, clinic, consultant, notes
            )
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _record_cancellation_supabase(
    supabase, pathway_id: str, patient_id: str, patient_name: str,
    appointment_id: str, appointment_date: str, appointment_type: str,
    cancelled_by: str, reason: str, rebook_required: bool,
    clinic: str, consultant: str, notes: str
) -> Dict:
    """Record cancellation via Supabase"""
    
    try:
        # Create cancellation record
        cancel_data = {
            'pathway_id': pathway_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'appointment_id': appointment_id,
            'appointment_date': appointment_date,
            'appointment_type': appointment_type,
            'cancelled_by': cancelled_by,
            'reason': reason,
            'rebook_required': rebook_required,
            'clinic': clinic,
            'consultant': consultant,
            'cancelled_date': datetime.now().date().isoformat(),
            'notes': notes,
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        result = supabase.table('cancellation_records').insert(cancel_data).execute()
        
        # Update pathway cancellation count
        pathway = get_pathway_by_id(pathway_id)
        current_cancel_count = pathway.get('cancellation_count', 0) if pathway else 0
        
        supabase.table('pathways').update({
            'cancellation_count': current_cancel_count + 1,
            'last_cancellation_date': appointment_date,
            'last_cancellation_reason': reason
        }).eq('pathway_id', pathway_id).execute()
        
        return {
            'success': True,
            'message': f'Cancellation recorded for appointment {appointment_id}',
            'cancellation_count': current_cancel_count + 1
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _record_cancellation_local(
    pathway_id: str, patient_id: str, patient_name: str,
    appointment_id: str, appointment_date: str, appointment_type: str,
    cancelled_by: str, reason: str, rebook_required: bool,
    clinic: str, consultant: str, notes: str
) -> Dict:
    """Record cancellation via local storage"""
    
    try:
        import json
        import os
        
        # Load existing cancellation records
        cancel_file = 'data/cancellation_records.json'
        os.makedirs('data', exist_ok=True)
        
        if os.path.exists(cancel_file):
            with open(cancel_file, 'r') as f:
                cancel_records = json.load(f)
        else:
            cancel_records = []
        
        # Create cancellation record
        cancel_data = {
            'id': f"CAN-{len(cancel_records) + 1:05d}",
            'pathway_id': pathway_id,
            'patient_id': patient_id,
            'patient_name': patient_name,
            'appointment_id': appointment_id,
            'appointment_date': appointment_date,
            'appointment_type': appointment_type,
            'cancelled_by': cancelled_by,
            'reason': reason,
            'rebook_required': rebook_required,
            'clinic': clinic,
            'consultant': consultant,
            'cancelled_date': datetime.now().date().isoformat(),
            'notes': notes,
            'user_email': st.session_state.get('user_email', 'guest@example.com')
        }
        
        cancel_records.append(cancel_data)
        
        # Save
        with open(cancel_file, 'w') as f:
            json.dump(cancel_records, f, indent=2)
        
        # Count cancellations for this pathway
        pathway_cancel_count = len([r for r in cancel_records if r['pathway_id'] == pathway_id])
        
        return {
            'success': True,
            'message': f'Cancellation recorded for appointment {appointment_id}',
            'cancellation_count': pathway_cancel_count
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_dna_records(pathway_id: str = None) -> List[Dict]:
    """Get DNA records"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('dna_records').select('*')
            if pathway_id:
                query = query.eq('pathway_id', pathway_id)
            result = query.order('recorded_date', desc=True).execute()
            return result.data if result.data else []
        else:
            import json
            import os
            
            dna_file = 'data/dna_records.json'
            if os.path.exists(dna_file):
                with open(dna_file, 'r') as f:
                    dna_records = json.load(f)
                
                if pathway_id:
                    dna_records = [r for r in dna_records if r['pathway_id'] == pathway_id]
                
                return sorted(dna_records, key=lambda x: x['recorded_date'], reverse=True)
            return []
    
    except Exception as e:
        st.error(f"Error getting DNA records: {e}")
        return []


def get_cancellation_records(pathway_id: str = None) -> List[Dict]:
    """Get cancellation records"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('cancellation_records').select('*')
            if pathway_id:
                query = query.eq('pathway_id', pathway_id)
            result = query.order('cancelled_date', desc=True).execute()
            return result.data if result.data else []
        else:
            import json
            import os
            
            cancel_file = 'data/cancellation_records.json'
            if os.path.exists(cancel_file):
                with open(cancel_file, 'r') as f:
                    cancel_records = json.load(f)
                
                if pathway_id:
                    cancel_records = [r for r in cancel_records if r['pathway_id'] == pathway_id]
                
                return sorted(cancel_records, key=lambda x: x['cancelled_date'], reverse=True)
            return []
    
    except Exception as e:
        st.error(f"Error getting cancellation records: {e}")
        return []


def render_dna_cancellation_ui():
    """UI for DNA and cancellation tracking"""
    
    st.subheader("📊 DNA & Cancellation Tracking")
    
    st.info("""
    **Track appointment non-attendance and cancellations:**
    - Record DNA (Did Not Attend) events
    - Record cancellations (patient/hospital)
    - Track counts per pathway
    - View DNA/cancellation history
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "❌ Record DNA",
        "🗓️ Record Cancellation",
        "📋 View Records",
        "📊 Statistics"
    ])
    
    with tab1:
        render_record_dna()
    
    with tab2:
        render_record_cancellation()
    
    with tab3:
        render_view_records()
    
    with tab4:
        render_dna_cancellation_stats()


def render_record_dna():
    """Record DNA event"""
    
    st.markdown("### ❌ Record DNA (Did Not Attend)")
    
    # Get pathways
    pathways = get_all_pathways()
    
    if not pathways:
        st.warning("No pathways found.")
        return
    
    # Select pathway
    pathway_options = {f"{p['pathway_id']} - {p['patient_name']} ({p['specialty']})": p for p in pathways}
    selected = st.selectbox("Select Pathway:", ["-- Select Pathway --"] + list(pathway_options.keys()), key="dna_pathway")
    
    if selected == "-- Select Pathway --":
        return
    
    pathway = pathway_options[selected]
    
    col1, col2 = st.columns(2)
    
    with col1:
        appointment_id = st.text_input("Appointment ID", placeholder="e.g., APT-12345")
        appointment_date = st.date_input("Appointment Date")
        appointment_type = st.selectbox("Appointment Type", ["First Appointment", "Follow-up", "Treatment", "Pre-op", "Other"])
    
    with col2:
        clinic = st.text_input("Clinic", placeholder="e.g., Orthopaedics")
        consultant = st.text_input("Consultant", placeholder="e.g., Dr Smith")
        notes = st.text_area("Notes", placeholder="Additional information...")
    
    if st.button("❌ Record DNA", type="primary"):
        if not appointment_id:
            st.error("Please enter appointment ID")
            return
        
        result = record_dna(
            pathway_id=pathway['pathway_id'],
            patient_id=pathway['patient_id'],
            patient_name=pathway['patient_name'],
            appointment_id=appointment_id,
            appointment_date=str(appointment_date),
            appointment_type=appointment_type,
            clinic=clinic,
            consultant=consultant,
            notes=notes
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            st.warning(f"⚠️ Total DNAs for this pathway: {result.get('dna_count')}")
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_record_cancellation():
    """Record cancellation"""
    
    st.markdown("### 🗓️ Record Cancellation")
    
    # Get pathways
    pathways = get_all_pathways()
    
    if not pathways:
        st.warning("No pathways found.")
        return
    
    # Select pathway
    pathway_options = {f"{p['pathway_id']} - {p['patient_name']} ({p['specialty']})": p for p in pathways}
    selected = st.selectbox("Select Pathway:", ["-- Select Pathway --"] + list(pathway_options.keys()), key="cancel_pathway")
    
    if selected == "-- Select Pathway --":
        return
    
    pathway = pathway_options[selected]
    
    col1, col2 = st.columns(2)
    
    with col1:
        appointment_id = st.text_input("Appointment ID", placeholder="e.g., APT-12345", key="cancel_appt_id")
        appointment_date = st.date_input("Appointment Date", key="cancel_appt_date")
        appointment_type = st.selectbox("Appointment Type", ["First Appointment", "Follow-up", "Treatment", "Pre-op", "Other"], key="cancel_appt_type")
        cancelled_by = st.selectbox("Cancelled By", ["Patient", "Hospital"], key="cancelled_by")
    
    with col2:
        reason = st.text_area("Cancellation Reason", placeholder="Reason for cancellation...", key="cancel_reason")
        rebook_required = st.checkbox("Rebook Required", value=True, key="rebook_req")
        clinic = st.text_input("Clinic", placeholder="e.g., Orthopaedics", key="cancel_clinic")
        consultant = st.text_input("Consultant", placeholder="e.g., Dr Smith", key="cancel_consultant")
    
    notes = st.text_area("Additional Notes", placeholder="Additional information...", key="cancel_notes")
    
    if st.button("🗓️ Record Cancellation", type="primary"):
        if not appointment_id or not reason:
            st.error("Please enter appointment ID and reason")
            return
        
        result = record_cancellation(
            pathway_id=pathway['pathway_id'],
            patient_id=pathway['patient_id'],
            patient_name=pathway['patient_name'],
            appointment_id=appointment_id,
            appointment_date=str(appointment_date),
            appointment_type=appointment_type,
            cancelled_by=cancelled_by,
            reason=reason,
            rebook_required=rebook_required,
            clinic=clinic,
            consultant=consultant,
            notes=notes
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            if rebook_required:
                st.warning("⚠️ Rebook required!")
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_view_records():
    """View DNA and cancellation records"""
    
    st.markdown("### 📋 DNA & Cancellation Records")
    
    record_type = st.radio("View:", ["DNA Records", "Cancellation Records"], horizontal=True)
    
    if record_type == "DNA Records":
        dna_records = get_dna_records()
        
        if not dna_records:
            st.info("No DNA records found.")
            return
        
        st.write(f"**Total DNA Events: {len(dna_records)}**")
        
        for record in dna_records:
            with st.expander(f"❌ {record['appointment_id']} - {record['patient_name']} ({record['appointment_date']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Patient:** {record['patient_name']}")
                    st.write(f"**Pathway ID:** {record['pathway_id']}")
                    st.write(f"**Appointment ID:** {record['appointment_id']}")
                    st.write(f"**Appointment Date:** {record['appointment_date']}")
                
                with col2:
                    st.write(f"**Type:** {record['appointment_type']}")
                    st.write(f"**Clinic:** {record.get('clinic', 'N/A')}")
                    st.write(f"**Consultant:** {record.get('consultant', 'N/A')}")
                    st.write(f"**Recorded:** {record['recorded_date']}")
                
                if record.get('notes'):
                    st.info(f"**Notes:** {record['notes']}")
    
    else:  # Cancellation Records
        cancel_records = get_cancellation_records()
        
        if not cancel_records:
            st.info("No cancellation records found.")
            return
        
        st.write(f"**Total Cancellations: {len(cancel_records)}**")
        
        for record in cancel_records:
            cancelled_by_icon = "👤" if record['cancelled_by'] == "Patient" else "🏥"
            
            with st.expander(f"{cancelled_by_icon} {record['appointment_id']} - {record['patient_name']} ({record['appointment_date']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Patient:** {record['patient_name']}")
                    st.write(f"**Pathway ID:** {record['pathway_id']}")
                    st.write(f"**Appointment ID:** {record['appointment_id']}")
                    st.write(f"**Appointment Date:** {record['appointment_date']}")
                    st.write(f"**Type:** {record['appointment_type']}")
                
                with col2:
                    st.write(f"**Cancelled By:** {record['cancelled_by']}")
                    st.write(f"**Reason:** {record['reason']}")
                    st.write(f"**Rebook Required:** {'Yes' if record.get('rebook_required') else 'No'}")
                    st.write(f"**Clinic:** {record.get('clinic', 'N/A')}")
                    st.write(f"**Cancelled Date:** {record['cancelled_date']}")
                
                if record.get('notes'):
                    st.info(f"**Notes:** {record['notes']}")


def render_dna_cancellation_stats():
    """Show DNA and cancellation statistics"""
    
    st.markdown("### 📊 DNA & Cancellation Statistics")
    
    dna_records = get_dna_records()
    cancel_records = get_cancellation_records()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total DNAs", len(dna_records))
    
    with col2:
        st.metric("Total Cancellations", len(cancel_records))
    
    with col3:
        patient_cancels = len([r for r in cancel_records if r['cancelled_by'] == "Patient"])
        st.metric("Patient Cancellations", patient_cancels)
    
    # Pathways with most DNAs
    if dna_records:
        st.markdown("---")
        st.markdown("### Top Pathways by DNA Count")
        
        pathway_dna_counts = {}
        for record in dna_records:
            pathway_id = record['pathway_id']
            pathway_dna_counts[pathway_id] = pathway_dna_counts.get(pathway_id, 0) + 1
        
        sorted_pathways = sorted(pathway_dna_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for pathway_id, count in sorted_pathways:
            st.write(f"**{pathway_id}:** {count} DNAs")
