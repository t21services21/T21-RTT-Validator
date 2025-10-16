"""
TRUST CUSTOMIZATION UI
Upload Trust-specific policies and train AI on your workflows

🚀 COMPETITIVE ADVANTAGE: Trust-specific AI training (like Sigma, but integrated into full platform)
"""

import streamlit as st
from datetime import datetime
from trust_customization_system import (
    get_trust_from_email,
    upload_trust_document,
    get_trust_documents,
    get_trust_config,
    delete_trust_document,
    update_trust_settings,
    get_trust_statistics,
    get_all_trusts
)


def render_trust_customization():
    """Main Trust customization interface"""
    
    st.header("🏥 Trust-Specific AI Customization")
    
    st.success("""
    **🚀 COMPETITIVE ADVANTAGE:**
    Train our AI on YOUR Trust's specific policies, SOPs, and workflows!
    
    Unlike generic AI chatbots, your AI will understand:
    ✅ Your local RTT validation procedures
    ✅ Your Trust-specific policies
    ✅ Your escalation workflows
    ✅ Your documentation standards
    """)
    
    # Get user's Trust
    user_email = st.session_state.get('user_email', 'demo@trust.nhs.uk')
    trust_id = get_trust_from_email(user_email)
    trust_config = get_trust_config(trust_id)
    
    # Trust info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Your Trust", trust_config.get('trust_name', trust_id))
    with col2:
        st.metric("Documents Uploaded", len(trust_config.get('documents', [])))
    with col3:
        status = trust_config.get('ai_training_status', 'not_configured')
        status_emoji = {
            'trained': '✅',
            'pending': '⏳',
            'not_configured': '⚠️',
            'error': '❌'
        }.get(status, '❓')
        st.metric("AI Training Status", f"{status_emoji} {status.replace('_', ' ').title()}")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Upload Documents",
        "📚 Your Documents",
        "⚙️ Settings",
        "📊 Statistics"
    ])
    
    with tab1:
        render_upload_documents(trust_id)
    
    with tab2:
        render_trust_documents(trust_id)
    
    with tab3:
        render_trust_settings(trust_id, trust_config)
    
    with tab4:
        render_trust_statistics(trust_id)


def render_upload_documents(trust_id: str):
    """Upload Trust-specific documents"""
    
    st.subheader("📤 Upload Trust Documents")
    
    st.info("""
    **What to upload:**
    - RTT validation policies
    - Local SOPs and procedures
    - Escalation workflows
    - Trust-specific guidance
    - Meeting notes from RTT meetings
    - Email communications about RTT processes
    """)
    
    with st.form("upload_document_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            document_name = st.text_input("Document Name*", placeholder="RTT Validation Policy 2025")
            
            document_type = st.selectbox("Document Type*", [
                "policy",
                "sop",
                "workflow",
                "procedure",
                "guidance",
                "meeting_notes",
                "email_guidance"
            ], format_func=lambda x: {
                'policy': '📋 Policy',
                'sop': '📝 Standard Operating Procedure',
                'workflow': '🔄 Workflow',
                'procedure': '📖 Procedure',
                'guidance': '💡 Guidance',
                'meeting_notes': '📝 Meeting Notes',
                'email_guidance': '📧 Email Guidance'
            }[x])
        
        with col2:
            category = st.selectbox("Category*", [
                "RTT Validation",
                "Clock Rules",
                "Booking Procedures",
                "Data Quality",
                "Patient Communication",
                "Escalation",
                "Reporting",
                "Other"
            ])
            
            uploaded_file = st.file_uploader(
                "Upload File (Optional)",
                type=['txt', 'pdf', 'doc', 'docx'],
                help="Upload a document file, or paste text below"
            )
        
        content = st.text_area(
            "Document Content*",
            height=300,
            placeholder="""Paste your Trust's policy/procedure here, or upload a file above.

Example:
"RTT Clock Start Rules at [Trust Name]:
1. All GP referrals start clock on receipt date
2. Consultant-to-consultant referrals start clock when accepted
3. Clock pauses require approval from RTT Lead
..."
            """,
            help="The AI will learn from this content"
        )
        
        submit = st.form_submit_button("📤 Upload Document", type="primary")
        
        if submit:
            if not document_name or not content:
                st.error("❌ Please provide document name and content")
            else:
                with st.spinner("📤 Uploading document..."):
                    result = upload_trust_document(
                        trust_id=trust_id,
                        document_name=document_name,
                        document_type=document_type,
                        content=content,
                        category=category
                    )
                    
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                        st.balloons()
                        st.info("💡 **Your AI will now reference this document when answering questions!**")
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('error', 'Upload failed')}")


def render_trust_documents(trust_id: str):
    """Display Trust's uploaded documents"""
    
    st.subheader("📚 Your Trust's Documents")
    
    documents = get_trust_documents(trust_id)
    
    if not documents:
        st.info("📭 No documents uploaded yet. Upload your first document to customize your AI!")
        return
    
    st.success(f"✅ **{len(documents)} documents** are training your AI")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.selectbox("Filter by Type", ["All"] + ["policy", "sop", "workflow", "procedure", "guidance"])
    with col2:
        category_filter = st.selectbox("Filter by Category", ["All", "RTT Validation", "Clock Rules", "Booking Procedures"])
    
    # Display documents
    for i, doc in enumerate(documents):
        if doc.get('status') != 'active':
            continue
        
        # Apply filters
        if type_filter != "All" and doc.get('document_type') != type_filter:
            continue
        if category_filter != "All" and doc.get('category') != category_filter:
            continue
        
        with st.expander(f"📄 {doc['document_name']}", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**Type:** {doc['document_type'].replace('_', ' ').title()}")
                st.write(f"**Category:** {doc.get('category', 'N/A')}")
            
            with col2:
                st.write(f"**Uploaded:** {doc.get('upload_date', 'N/A')[:10]}")
                st.write(f"**Word Count:** {doc.get('word_count', 0):,}")
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{doc['document_id']}"):
                    result = delete_trust_document(trust_id, doc['document_id'])
                    if result['success']:
                        st.success("✅ Document deleted")
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('error')}")
            
            # Show content preview
            st.markdown("**Content Preview:**")
            preview = doc['content'][:500]
            st.text_area("", value=preview, height=150, disabled=True, key=f"preview_{i}")


def render_trust_settings(trust_id: str, trust_config: dict):
    """Configure Trust settings"""
    
    st.subheader("⚙️ Trust Settings")
    
    with st.form("trust_settings_form"):
        trust_name = st.text_input(
            "Trust Name",
            value=trust_config.get('trust_name', trust_id),
            help="Display name for your Trust"
        )
        
        ai_model = st.selectbox(
            "AI Model Preference",
            ["default", "fast", "detailed", "technical"],
            help="Choose AI response style"
        )
        
        response_style = st.selectbox(
            "Response Style",
            ["professional", "concise", "detailed", "conversational"],
            help="How should the AI respond?"
        )
        
        custom_instructions = st.text_area(
            "Custom Instructions for AI",
            placeholder="""Additional instructions for AI responses:
- Always reference Trust RTT policy version 3.2
- Escalate complex queries to RTT Lead
- Include relevant policy section numbers in responses
""",
            height=150
        )
        
        submit = st.form_submit_button("💾 Save Settings", type="primary")
        
        if submit:
            result = update_trust_settings(
                trust_id=trust_id,
                trust_name=trust_name,
                ai_model_preference=ai_model,
                response_style=response_style,
                custom_instructions=custom_instructions
            )
            
            if result['success']:
                st.success("✅ Settings updated successfully!")
                st.rerun()
            else:
                st.error(f"❌ {result.get('error')}")


def render_trust_statistics(trust_id: str):
    """Show Trust customization statistics"""
    
    st.subheader("📊 Trust AI Statistics")
    
    stats = get_trust_statistics(trust_id)
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", stats['total_documents'])
    with col2:
        st.metric("Total Words", f"{stats['total_words']:,}")
    with col3:
        ai_knowledge = min(100, (stats['total_words'] / 1000) * 100)
        st.metric("AI Knowledge Level", f"{ai_knowledge:.0f}%")
    
    st.markdown("---")
    
    # Documents by type
    if stats['by_type']:
        st.markdown("### 📋 Documents by Type")
        col1, col2 = st.columns(2)
        
        with col1:
            for doc_type, count in stats['by_type'].items():
                st.write(f"**{doc_type.title()}:** {count}")
        
        with col2:
            if stats['by_category']:
                st.markdown("**By Category:**")
                for category, count in stats['by_category'].items():
                    st.write(f"• {category}: {count}")
    
    # Recent uploads
    if stats['recent_uploads']:
        st.markdown("---")
        st.markdown("### 🕒 Recent Uploads")
        for upload in stats['recent_uploads']:
            st.write(f"• {upload['name']} ({upload['type']}) - {upload['date'][:10]}")
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💡 Recommendations")
    
    if stats['total_documents'] < 3:
        st.warning("⚠️ Upload more documents to improve AI accuracy. Aim for at least 5-10 key documents.")
    elif stats['total_words'] < 5000:
        st.info("💡 Add more detailed content to enhance AI understanding. Current: {stats['total_words']:,} words, Target: 10,000+ words")
    else:
        st.success("✅ Great job! Your AI has substantial Trust-specific knowledge.")


# For integration into sidebar
def render_trust_admin_widget():
    """Quick widget for sidebar"""
    user_email = st.session_state.get('user_email', '')
    trust_id = get_trust_from_email(user_email)
    stats = get_trust_statistics(trust_id)
    
    with st.expander("🏥 Trust AI Status"):
        st.metric("Documents", stats['total_documents'])
        st.metric("Words", f"{stats['total_words']:,}")
        if st.button("⚙️ Customize AI"):
            st.session_state.active_module = "Trust AI Customization"
            st.rerun()
