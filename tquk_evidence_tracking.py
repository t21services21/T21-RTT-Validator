"""
TQUK EVIDENCE TRACKING SYSTEM
View and manage submitted evidence with assessor feedback
"""

import streamlit as st
from datetime import datetime

# Import Supabase client
try:
    from supabase_client import get_supabase_client
except ImportError:
    def get_supabase_client():
        try:
            from supabase_database import supabase
            return supabase
        except:
            return None


def get_student_evidence(learner_email, course_id):
    """Get all evidence submitted by a student"""
    supabase = get_supabase_client()
    if not supabase:
        return []
    
    try:
        response = supabase.table('tquk_evidence').select('*').eq('learner_email', learner_email).eq('course_id', course_id).order('submission_date', desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error loading evidence: {str(e)}")
        return []


def submit_evidence(learner_email, course_id, unit_number, evidence_type, description, file_url=None):
    """Submit new evidence"""
    supabase = get_supabase_client()
    if not supabase:
        return False
    
    try:
        data = {
            'learner_email': learner_email,
            'course_id': course_id,
            'unit_number': unit_number,
            'evidence_type': evidence_type,
            'description': description,
            'file_url': file_url,
            'submission_date': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        response = supabase.table('tquk_evidence').insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error submitting evidence: {str(e)}")
        return False


def render_evidence_tracking(learner_email, course_id):
    """Render evidence tracking interface"""
    
    st.subheader("📋 My Submitted Evidence")
    
    evidence_list = get_student_evidence(learner_email, course_id)
    
    if not evidence_list:
        st.info("📝 No evidence submitted yet. Go to the Assessments tab to submit your first piece of evidence!")
        return
    
    # Summary metrics
    total = len(evidence_list)
    pending = len([e for e in evidence_list if e['status'] == 'pending'])
    approved = len([e for e in evidence_list if e['status'] == 'approved'])
    rejected = len([e for e in evidence_list if e['status'] == 'rejected'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Submissions", total)
    with col2:
        st.metric("Pending Review", pending, delta=f"{pending} waiting")
    with col3:
        st.metric("Approved", approved, delta=f"{approved} ✅")
    with col4:
        st.metric("Needs Revision", rejected, delta=f"{rejected} ⚠️")
    
    st.markdown("---")
    
    # Filter options
    filter_status = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "Approved", "Rejected"],
        key="evidence_filter"
    )
    
    # Filter evidence
    if filter_status != "All":
        evidence_list = [e for e in evidence_list if e['status'].lower() == filter_status.lower()]
    
    # Display evidence
    for evidence in evidence_list:
        status_color = {
            'pending': '🟡',
            'approved': '🟢',
            'rejected': '🔴'
        }.get(evidence['status'], '⚪')
        
        with st.expander(f"{status_color} Unit {evidence['unit_number']} - {evidence['evidence_type'].replace('_', ' ').title()} ({evidence['status'].title()})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Evidence Type:** {evidence['evidence_type'].replace('_', ' ').title()}")
                st.write(f"**Description:**")
                st.write(evidence['description'])
                
                if evidence.get('file_url'):
                    st.write(f"**File:** [{evidence['file_url']}]({evidence['file_url']})")
            
            with col2:
                st.write(f"**Submitted:** {evidence['submission_date'][:10]}")
                st.write(f"**Status:** {evidence['status'].title()}")
                
                if evidence.get('assessor_email'):
                    st.write(f"**Assessor:** {evidence['assessor_email']}")
                
                if evidence.get('assessment_date'):
                    st.write(f"**Assessed:** {evidence['assessment_date'][:10]}")
            
            # Show feedback if available
            if evidence.get('assessor_feedback'):
                if evidence['status'] == 'approved':
                    st.success(f"✅ **Assessor Feedback:**\n\n{evidence['assessor_feedback']}")
                elif evidence['status'] == 'rejected':
                    st.error(f"⚠️ **Assessor Feedback:**\n\n{evidence['assessor_feedback']}")
                else:
                    st.info(f"💬 **Assessor Feedback:**\n\n{evidence['assessor_feedback']}")
            else:
                if evidence['status'] == 'pending':
                    st.info("⏳ Waiting for assessor review...")


def render_evidence_submission_form(learner_email, course_id, unit_number):
    """Render evidence submission form"""
    
    st.subheader(f"📝 Submit Evidence for Unit {unit_number}")
    
    # Evidence type
    evidence_type = st.selectbox(
        "Evidence Type",
        [
            "observation",
            "witness_statement",
            "reflective_account",
            "product_evidence",
            "professional_discussion",
            "case_study"
        ],
        format_func=lambda x: x.replace('_', ' ').title(),
        key=f"evidence_type_{unit_number}"
    )
    
    # Description
    description = st.text_area(
        "Describe what this evidence demonstrates...",
        height=150,
        placeholder="Explain how this evidence meets the learning outcomes for this unit...",
        key=f"evidence_desc_{unit_number}"
    )
    
    # File upload
    st.write("**Upload Evidence (PDF, Word, Image)**")
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png'],
        help="Limit 200MB per file • PDF, DOCX, DOC, JPG, JPEG, PNG",
        key=f"evidence_file_{unit_number}"
    )
    
    # Submit button
    if st.button("📤 Submit Evidence", key=f"submit_evidence_{unit_number}", type="primary"):
        if not description:
            st.error("❌ Please provide a description of your evidence.")
        else:
            # TODO: Upload file to storage and get URL
            file_url = None
            if uploaded_file:
                # For now, just use filename
                file_url = uploaded_file.name
            
            if submit_evidence(learner_email, course_id, unit_number, evidence_type, description, file_url):
                st.success("✅ Evidence submitted successfully!")
                st.balloons()
                st.info("Your assessor will review your evidence and provide feedback soon.")
            else:
                st.error("❌ Failed to submit evidence. Please try again.")
