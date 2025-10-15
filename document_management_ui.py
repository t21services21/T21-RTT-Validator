"""
DOCUMENT MANAGEMENT UI
Upload, view, and manage clinical documents
"""

import streamlit as st
from datetime import datetime
from document_management_system import (
    upload_document,
    get_documents_by_patient,
    search_documents,
    delete_document,
    download_document,
    get_document_stats,
    DOCUMENT_TYPES,
    validate_file_type,
    get_file_icon,
    load_documents
)


def render_document_management():
    """Main document management interface"""
    
    st.header("📁 Document Management")
    st.markdown("**Store & Retrieve Clinical Documents**")
    
    st.success("""
    📁 **Document Features:**
    - Upload clinic letters, test results, scans
    - Link to patient NHS number
    - Search by patient or document type
    - View/download documents
    - Secure storage in Supabase
    """)
    
    # Get statistics
    stats = get_document_stats()
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Documents", stats['total_documents'])
    with col2:
        st.metric("Recent Uploads (7 days)", stats['recent_uploads'])
    with col3:
        st.metric("Total Storage", f"{stats['total_size_mb']} MB")
    with col4:
        st.metric("Document Types", len(stats['by_type']))
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Upload Document",
        "📋 All Documents",
        "🔍 Search Documents",
        "📊 Statistics"
    ])
    
    with tab1:
        render_upload_document()
    
    with tab2:
        render_all_documents()
    
    with tab3:
        render_search_documents()
    
    with tab4:
        render_document_statistics(stats)


def render_upload_document():
    """Upload document form"""
    st.markdown("### 📤 Upload Document")
    
    with st.form("upload_document"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_nhs = st.text_input("Patient NHS Number*", placeholder="123 456 7890")
            patient_name = st.text_input("Patient Name*", placeholder="John Smith")
            document_type = st.selectbox("Document Type*", DOCUMENT_TYPES)
            document_date = st.date_input("Document Date*", value=datetime.now())
        
        with col2:
            uploaded_file = st.file_uploader(
                "Choose file*",
                type=['pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'csv', 'dcm', 'dicom', 'tiff', 'tif'],
                help="Allowed: PDF, Images, Office documents, DICOM"
            )
            
            description = st.text_area("Description (optional)", height=80,
                                      placeholder="E.g., Blood test results showing improved liver function...")
        
        if st.form_submit_button("📤 Upload Document", type="primary"):
            if uploaded_file and patient_nhs and patient_name and document_type:
                # Read file
                file_data = uploaded_file.read()
                filename = uploaded_file.name
                
                # Validate file type
                is_valid, message = validate_file_type(filename)
                
                if not is_valid:
                    st.error(f"❌ {message}")
                else:
                    # Upload
                    with st.spinner("Uploading document..."):
                        document_id = upload_document(
                            file_data=file_data,
                            filename=filename,
                            patient_nhs=patient_nhs,
                            patient_name=patient_name,
                            document_type=document_type,
                            document_date=str(document_date),
                            description=description
                        )
                    
                    if document_id:
                        st.success(f"✅ Document uploaded successfully! ID: {document_id}")
                        st.balloons()
                    else:
                        st.error("❌ Failed to upload document. Check console for details.")
            else:
                st.error("❌ Please fill all required fields and select a file")


def render_all_documents():
    """View all documents"""
    st.markdown("### 📋 All Documents")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        type_filter = st.selectbox("Filter by Type", ["All"] + DOCUMENT_TYPES, key="type_filter_all")
    with col2:
        sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Patient Name", "Document Type"])
    with col3:
        limit = st.selectbox("Show", [10, 25, 50, 100, "All"])
    
    # Get all documents
    documents_data = load_documents()
    all_docs = documents_data.get('documents', [])
    
    # Apply type filter
    if type_filter != "All":
        all_docs = [d for d in all_docs if d.get('document_type') == type_filter]
    
    # Sort
    if sort_by == "Date (Newest)":
        all_docs.sort(key=lambda x: x.get('document_date', ''), reverse=True)
    elif sort_by == "Date (Oldest)":
        all_docs.sort(key=lambda x: x.get('document_date', ''))
    elif sort_by == "Patient Name":
        all_docs.sort(key=lambda x: x.get('patient_name', ''))
    elif sort_by == "Document Type":
        all_docs.sort(key=lambda x: x.get('document_type', ''))
    
    # Limit
    if limit != "All":
        all_docs = all_docs[:int(limit)]
    
    if all_docs:
        st.markdown(f"**{len(all_docs)} document(s) found**")
        render_document_list(all_docs)
    else:
        st.info("📭 No documents found")


def render_search_documents():
    """Search documents interface"""
    st.markdown("### 🔍 Search Documents")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search", placeholder="Patient name, NHS number, or description...", key="doc_search")
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if search_query or search_button:
        if len(search_query) >= 2:
            results = search_documents(search_query)
            
            if results:
                st.markdown(f"### Found {len(results)} document(s)")
                render_document_list(results)
            else:
                st.warning(f"⚠️ No documents found matching '{search_query}'")
        else:
            st.info("💡 Enter at least 2 characters to search")


def render_document_list(documents: list):
    """Render list of documents"""
    
    for doc in documents:
        file_ext = doc.get('file_extension', 'unknown')
        file_icon = get_file_icon(file_ext)
        doc_type = doc.get('document_type', 'Unknown')
        
        with st.expander(f"{file_icon} {doc['patient_name']} - {doc_type} ({doc.get('document_date', 'N/A')})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Document ID:** {doc.get('document_id', 'N/A')}")
                st.markdown(f"**Patient:** {doc.get('patient_name', 'Unknown')}")
                st.markdown(f"**NHS Number:** {doc.get('patient_nhs', 'N/A')}")
                st.markdown(f"**Document Type:** {doc_type}")
                st.markdown(f"**Document Date:** {doc.get('document_date', 'N/A')}")
            
            with col2:
                st.markdown(f"**Filename:** {doc.get('filename', 'Unknown')}")
                file_size_kb = doc.get('file_size', 0) / 1024
                st.markdown(f"**File Size:** {file_size_kb:.1f} KB")
                st.markdown(f"**Uploaded By:** {doc.get('uploaded_by', 'Unknown')}")
                st.markdown(f"**Uploaded At:** {doc.get('uploaded_at', 'N/A')[:16]}")
            
            if doc.get('description'):
                st.markdown(f"**Description:**")
                st.info(doc.get('description'))
            
            # Actions
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("💾 Download", key=f"download_{doc['document_id']}", use_container_width=True):
                    file_data = download_document(doc['document_id'])
                    if file_data:
                        st.download_button(
                            "📥 Click to Save",
                            data=file_data,
                            file_name=doc.get('filename', 'document'),
                            mime="application/octet-stream",
                            key=f"save_{doc['document_id']}",
                            use_container_width=True
                        )
                    else:
                        st.error("❌ Failed to download document")
            
            with col_b:
                if st.button("👁️ View Patient", key=f"view_patient_{doc['document_id']}", use_container_width=True):
                    st.session_state['viewing_patient_nhs'] = doc.get('patient_nhs')
                    st.info(f"Switch to '🔍 Patient Search' to view {doc.get('patient_name')}'s complete record")
            
            with col_c:
                if st.button("🗑️ Delete", key=f"delete_{doc['document_id']}", use_container_width=True):
                    if delete_document(doc['document_id']):
                        st.success("✅ Document deleted!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete document")


def render_document_statistics(stats: dict):
    """Display document statistics"""
    st.markdown("### 📊 Document Statistics")
    
    # Storage usage
    st.markdown("#### 💾 Storage Usage")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", stats['total_documents'])
    with col2:
        st.metric("Total Size", f"{stats['total_size_mb']} MB")
    with col3:
        avg_size = (stats['total_size_mb'] / stats['total_documents']) if stats['total_documents'] > 0 else 0
        st.metric("Average Size", f"{avg_size:.2f} MB")
    
    # By document type
    st.markdown("---")
    st.markdown("#### 📑 Documents by Type")
    
    if stats['by_type']:
        # Sort by count
        sorted_types = sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)
        
        col1, col2 = st.columns(2)
        mid_point = len(sorted_types) // 2
        
        with col1:
            for doc_type, count in sorted_types[:mid_point]:
                st.markdown(f"**{doc_type}:** {count}")
        
        with col2:
            for doc_type, count in sorted_types[mid_point:]:
                st.markdown(f"**{doc_type}:** {count}")
    else:
        st.info("No documents uploaded yet")
    
    # Recent activity
    st.markdown("---")
    st.markdown("#### 📅 Recent Activity")
    st.metric("Uploads in Last 7 Days", stats['recent_uploads'])


def render_patient_documents_view(patient_nhs: str, patient_name: str):
    """Render documents for a specific patient (used in patient search)"""
    
    st.markdown(f"### 📁 Documents for {patient_name}")
    
    docs = get_documents_by_patient(patient_nhs)
    
    if docs:
        st.markdown(f"**{len(docs)} document(s) on file**")
        
        # Quick summary
        doc_types = set([d.get('document_type') for d in docs])
        st.markdown(f"**Types:** {', '.join(doc_types)}")
        
        # Display documents
        for doc in docs:
            file_icon = get_file_icon(doc.get('file_extension', ''))
            
            with st.expander(f"{file_icon} {doc.get('document_type', 'Unknown')} - {doc.get('document_date', 'N/A')}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Type:** {doc.get('document_type')}")
                    st.markdown(f"**Date:** {doc.get('document_date')}")
                    st.markdown(f"**Filename:** {doc.get('filename')}")
                    if doc.get('description'):
                        st.markdown(f"**Description:** {doc.get('description')}")
                
                with col2:
                    if st.button("💾 Download", key=f"pat_download_{doc['document_id']}", use_container_width=True):
                        file_data = download_document(doc['document_id'])
                        if file_data:
                            st.download_button(
                                "📥 Save",
                                data=file_data,
                                file_name=doc.get('filename', 'document'),
                                mime="application/octet-stream",
                                key=f"pat_save_{doc['document_id']}"
                            )
    else:
        st.info("📭 No documents on file for this patient")
        
        # Quick upload option
        if st.button("📤 Upload Document for This Patient"):
            st.session_state['upload_for_patient'] = patient_nhs
            st.info("Go to 'Upload Document' tab to upload")
