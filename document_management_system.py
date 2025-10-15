"""
DOCUMENT MANAGEMENT SYSTEM
Store, retrieve, and manage clinical documents

Features:
- Upload documents (PDFs, images, etc.)
- Link to patient NHS number
- Categorize by type (letter, scan, test result, etc.)
- View/download documents
- Search documents
- Document history per patient
- Secure storage with Supabase
"""

from datetime import datetime
from typing import Dict, List, Optional
import json
import os
import base64
from session_manager import get_current_user_email
from config import SUPABASE_ENABLED

if SUPABASE_ENABLED:
    from supabase_database import (
        supabase_upload_document,
        supabase_get_documents_for_patient,
        supabase_get_all_documents,
        supabase_delete_document,
        supabase_download_document
    )

# Document types
DOCUMENT_TYPES = [
    "Clinic Letter",
    "GP Letter",
    "MDT Letter",
    "Blood Test Result",
    "Radiology Report",
    "CT Scan",
    "MRI Scan",
    "X-Ray",
    "Ultrasound",
    "Pathology Report",
    "Biopsy Result",
    "ECG",
    "Echocardiogram",
    "Consent Form",
    "Discharge Summary",
    "Referral Letter",
    "Prescription",
    "Treatment Plan",
    "Operation Notes",
    "Nursing Notes",
    "Other"
]

DOCUMENTS_DB = "documents.json"


def load_documents():
    """Load documents database"""
    user_email = get_current_user_email()
    if SUPABASE_ENABLED:
        try:
            from supabase_database import get_all_documents_for_user
            return {'documents': get_all_documents_for_user(user_email)}
        except:
            pass
    
    if os.path.exists(DOCUMENTS_DB):
        with open(DOCUMENTS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'documents': []}


def save_documents(data):
    """Save documents database - deprecated with Supabase"""
    if not SUPABASE_ENABLED:
        with open(DOCUMENTS_DB, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def upload_document(
    file_data: bytes,
    filename: str,
    patient_nhs: str,
    patient_name: str,
    document_type: str,
    document_date: str,
    description: str = "",
    uploaded_by: str = None
) -> str:
    """Upload a document"""
    
    user_email = get_current_user_email()
    document_id = f"DOC_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Get file extension
    file_extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
    
    document_data = {
        'document_id': document_id,
        'patient_nhs': patient_nhs,
        'patient_name': patient_name,
        'document_type': document_type,
        'document_date': document_date,
        'filename': filename,
        'file_extension': file_extension,
        'file_size': len(file_data),
        'description': description,
        'uploaded_by': uploaded_by or user_email,
        'uploaded_at': datetime.now().isoformat(),
        'user_email': user_email
    }
    
    if SUPABASE_ENABLED:
        try:
            # Upload file to Supabase Storage
            success, result = supabase_upload_document(user_email, document_id, file_data, filename, document_data)
            if success:
                return document_id
            else:
                print(f"❌ Error uploading document: {result}")
                import streamlit as st
                st.error(f"❌ Failed to upload document: {result}")
                return None
        except Exception as e:
            print(f"❌ Exception uploading document: {e}")
            import streamlit as st
            st.error(f"❌ Exception: {e}")
            return None
    else:
        # Fallback: Store as base64 in JSON (not recommended for production)
        document_data['file_data_base64'] = base64.b64encode(file_data).decode('utf-8')
        documents = load_documents()
        documents['documents'].append(document_data)
        save_documents(documents)
        return document_id


def get_documents_by_patient(patient_nhs: str) -> List[Dict]:
    """Get all documents for a patient"""
    from unified_patient_system import normalize_nhs_number
    
    patient_nhs_normalized = normalize_nhs_number(patient_nhs)
    
    if SUPABASE_ENABLED:
        try:
            user_email = get_current_user_email()
            docs = supabase_get_documents_for_patient(user_email, patient_nhs)
            return docs
        except:
            pass
    
    # Fallback
    documents = load_documents()
    all_docs = documents.get('documents', [])
    
    patient_docs = []
    for doc in all_docs:
        if normalize_nhs_number(doc.get('patient_nhs', '')) == patient_nhs_normalized:
            patient_docs.append(doc)
    
    # Sort by date, newest first
    patient_docs.sort(key=lambda x: x.get('document_date', ''), reverse=True)
    
    return patient_docs


def get_documents_by_type(document_type: str) -> List[Dict]:
    """Get all documents of a specific type"""
    documents = load_documents()
    all_docs = documents.get('documents', [])
    
    return [doc for doc in all_docs if doc.get('document_type') == document_type]


def search_documents(query: str) -> List[Dict]:
    """Search documents by patient name, NHS number, or description"""
    query_lower = query.lower().strip()
    
    if not query_lower:
        return []
    
    documents = load_documents()
    all_docs = documents.get('documents', [])
    
    results = []
    for doc in all_docs:
        # Search in patient name, NHS, description, filename
        if (query_lower in doc.get('patient_name', '').lower() or
            query_lower in doc.get('patient_nhs', '').lower() or
            query_lower in doc.get('description', '').lower() or
            query_lower in doc.get('filename', '').lower()):
            results.append(doc)
    
    return results


def delete_document(document_id: str) -> bool:
    """Delete a document"""
    user_email = get_current_user_email()
    
    if SUPABASE_ENABLED:
        try:
            return supabase_delete_document(user_email, document_id)
        except:
            return False
    else:
        documents = load_documents()
        documents['documents'] = [d for d in documents['documents'] if d['document_id'] != document_id]
        save_documents(documents)
        return True


def download_document(document_id: str) -> Optional[bytes]:
    """Download document file data"""
    
    if SUPABASE_ENABLED:
        try:
            user_email = get_current_user_email()
            return supabase_download_document(user_email, document_id)
        except:
            return None
    else:
        # Fallback: Get from JSON base64
        documents = load_documents()
        all_docs = documents.get('documents', [])
        
        for doc in all_docs:
            if doc['document_id'] == document_id:
                if 'file_data_base64' in doc:
                    return base64.b64decode(doc['file_data_base64'])
        
        return None


def get_document_stats() -> Dict:
    """Get document statistics"""
    documents = load_documents()
    all_docs = documents.get('documents', [])
    
    stats = {
        'total_documents': len(all_docs),
        'by_type': {},
        'recent_uploads': 0,
        'total_size_mb': 0
    }
    
    # Count by type
    for doc in all_docs:
        doc_type = doc.get('document_type', 'Unknown')
        stats['by_type'][doc_type] = stats['by_type'].get(doc_type, 0) + 1
        
        # Total size
        stats['total_size_mb'] += doc.get('file_size', 0) / (1024 * 1024)
    
    # Recent uploads (last 7 days)
    from datetime import timedelta
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    stats['recent_uploads'] = len([d for d in all_docs if d.get('uploaded_at', '') >= week_ago])
    
    stats['total_size_mb'] = round(stats['total_size_mb'], 2)
    
    return stats


def get_patient_document_summary(patient_nhs: str) -> Dict:
    """Get summary of documents for a patient"""
    docs = get_documents_by_patient(patient_nhs)
    
    summary = {
        'total_documents': len(docs),
        'by_type': {},
        'latest_upload': None,
        'has_clinic_letters': False,
        'has_test_results': False,
        'has_scans': False
    }
    
    test_result_types = ['Blood Test Result', 'Pathology Report', 'Biopsy Result']
    scan_types = ['CT Scan', 'MRI Scan', 'X-Ray', 'Ultrasound', 'Radiology Report']
    
    for doc in docs:
        doc_type = doc.get('document_type', 'Unknown')
        summary['by_type'][doc_type] = summary['by_type'].get(doc_type, 0) + 1
        
        if 'Letter' in doc_type:
            summary['has_clinic_letters'] = True
        if doc_type in test_result_types:
            summary['has_test_results'] = True
        if doc_type in scan_types:
            summary['has_scans'] = True
    
    if docs:
        summary['latest_upload'] = docs[0].get('uploaded_at')
    
    return summary


def validate_file_type(filename: str) -> tuple[bool, str]:
    """Validate if file type is allowed"""
    
    allowed_extensions = [
        'pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp',
        'doc', 'docx', 'txt', 'rtf',
        'xls', 'xlsx', 'csv',
        'dcm', 'dicom',  # Medical imaging
        'tiff', 'tif'
    ]
    
    extension = filename.split('.')[-1].lower() if '.' in filename else ''
    
    if extension in allowed_extensions:
        return True, extension
    else:
        return False, f"File type .{extension} not allowed. Allowed: {', '.join(allowed_extensions)}"


def get_file_icon(file_extension: str) -> str:
    """Get emoji icon for file type"""
    
    icons = {
        'pdf': '📄',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️', 'bmp': '🖼️',
        'doc': '📝', 'docx': '📝', 'txt': '📝', 'rtf': '📝',
        'xls': '📊', 'xlsx': '📊', 'csv': '📊',
        'dcm': '🏥', 'dicom': '🏥',
        'tiff': '🖼️', 'tif': '🖼️'
    }
    
    return icons.get(file_extension.lower(), '📎')
