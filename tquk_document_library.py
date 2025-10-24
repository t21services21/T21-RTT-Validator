"""
TQUK DOCUMENT LIBRARY
Complete document management for Admin, Tutors, and Assessors
"""

import streamlit as st
import os
from pathlib import Path

# Document categories and files
DOCUMENTS = {
    "admin": {
        "TQUK Submission Documents": {
            "description": "Documents to submit to TQUK for CDA approval",
            "files": [
                {
                    "name": "CDA Submission Package",
                    "file": "TQUK_CDA_SUBMISSION_PACKAGE.md",
                    "description": "Complete submission with mapping matrix",
                    "required": True
                },
                {
                    "name": "Email Template to TQUK",
                    "file": "EMAIL_TO_TQUK_CDA_APPROVAL.md",
                    "description": "Copy-paste email for TQUK submission",
                    "required": True
                },
                {
                    "name": "Assessment Pack Templates",
                    "file": "LEVEL3_ASSESSMENT_PACK_TEMPLATES.md",
                    "description": "All assessment forms and templates",
                    "required": True
                }
            ]
        },
        "Quality Assurance Documents": {
            "description": "Quality assurance and compliance documentation",
            "files": [
                {
                    "name": "Content Quality Assurance Report",
                    "file": "TQUK_CONTENT_QUALITY_ASSURANCE.md",
                    "description": "Complete quality verification report",
                    "required": False
                },
                {
                    "name": "Compliance Verification",
                    "file": "TQUK_COMPLIANCE_VERIFIED.md",
                    "description": "TQUK compliance checklist",
                    "required": False
                },
                {
                    "name": "Certification Process Guide",
                    "file": "TQUK_CERTIFICATION_PROCESS.md",
                    "description": "How TQUK certificates are issued",
                    "required": False
                }
            ]
        },
        "System Documentation": {
            "description": "Complete system guides and documentation",
            "files": [
                {
                    "name": "Complete System Guide",
                    "file": "DEPLOY_COMPLETE_TQUK_SYSTEM.md",
                    "description": "Full system deployment guide",
                    "required": False
                },
                {
                    "name": "All Qualifications Summary",
                    "file": "TQUK_ALL_QUALIFICATIONS_SUMMARY.md",
                    "description": "Overview of all TQUK qualifications",
                    "required": False
                }
            ]
        }
    },
    "tutor": {
        "Delivery Resources": {
            "description": "Complete teaching and delivery resources",
            "files": [
                {
                    "name": "Complete Tutor Delivery Pack",
                    "file": "COMPLETE_TUTOR_DELIVERY_PACK.md",
                    "description": "18-week lesson plans, activities, PowerPoints",
                    "required": True
                },
                {
                    "name": "Tutor Guide - All 27 Units",
                    "file": "TUTOR_GUIDE_ALL_27_UNITS.md",
                    "description": "Unit-by-unit teaching notes and tips",
                    "required": True
                },
                {
                    "name": "User-Friendly Module Guide",
                    "file": "ALL_TQUK_MODULES_USER_FRIENDLY_COMPLETE.md",
                    "description": "Easy guide for all TQUK modules",
                    "required": False
                }
            ]
        },
        "Student Resources": {
            "description": "Resources to share with students",
            "files": [
                {
                    "name": "Complete Student Workbook",
                    "file": "COMPLETE_STUDENT_WORKBOOK.md",
                    "description": "Comprehensive student workbook",
                    "required": True
                },
                {
                    "name": "All Units Summary",
                    "file": "ALL_UNITS_COMPLETE_SUMMARY.md",
                    "description": "Summary of all 27 units",
                    "required": False
                }
            ]
        },
        "Assessment Templates": {
            "description": "Assessment and marking resources",
            "files": [
                {
                    "name": "Assessment Pack Templates",
                    "file": "LEVEL3_ASSESSMENT_PACK_TEMPLATES.md",
                    "description": "All assessment forms",
                    "required": True
                },
                {
                    "name": "Assessment Templates",
                    "file": "ASSESSMENT_TEMPLATES.md",
                    "description": "Additional assessment templates",
                    "required": False
                }
            ]
        }
    },
    "assessor": {
        "Assessment Tools": {
            "description": "Tools for conducting assessments",
            "files": [
                {
                    "name": "Assessment Pack Templates",
                    "file": "LEVEL3_ASSESSMENT_PACK_TEMPLATES.md",
                    "description": "Observation, witness statements, professional discussions",
                    "required": True
                },
                {
                    "name": "Assessment Templates",
                    "file": "ASSESSMENT_TEMPLATES.md",
                    "description": "Additional assessment forms",
                    "required": False
                }
            ]
        },
        "Marking Schemes": {
            "description": "Marking and grading guidance",
            "files": [
                {
                    "name": "Assessment Marking Schemes",
                    "file": "ASSESSMENT_MARKING_SCHEMES.md",
                    "description": "Detailed marking criteria",
                    "required": True
                }
            ]
        },
        "Unit Materials": {
            "description": "All unit learning materials for reference",
            "files": [
                {
                    "name": "All Units Summary",
                    "file": "ALL_UNITS_COMPLETE_SUMMARY.md",
                    "description": "Quick reference for all units",
                    "required": False
                }
            ]
        }
    }
}


def get_file_path(filename):
    """Get the full path to a document file"""
    base_path = Path(__file__).parent
    return base_path / filename


def file_exists(filename):
    """Check if a file exists"""
    return get_file_path(filename).exists()


def read_file_content(filename):
    """Read the content of a file"""
    try:
        file_path = get_file_path(filename)
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None


def render_document_library(user_role):
    """Render document library based on user role"""
    
    st.title("📚 Document Library")
    
    # Role-based greeting
    if user_role == "admin":
        st.success("👨‍💼 **Admin Document Library** - TQUK submissions, compliance, and system documentation")
    elif user_role == "tutor":
        st.success("👨‍🏫 **Tutor Resource Center** - Delivery packs, teaching guides, and student resources")
    elif user_role == "assessor":
        st.success("✅ **Assessor Tools** - Assessment templates, marking schemes, and unit materials")
    
    st.markdown("---")
    
    # Get documents for this role
    role_docs = DOCUMENTS.get(user_role, {})
    
    if not role_docs:
        st.warning(f"No documents available for role: {user_role}")
        return
    
    # Display documents by category
    for category, category_data in role_docs.items():
        with st.expander(f"📂 {category}", expanded=True):
            st.info(f"**{category_data['description']}**")
            
            for doc in category_data['files']:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    # Document name and description
                    required_badge = "🔴 **REQUIRED**" if doc['required'] else "⚪ Optional"
                    st.markdown(f"**{doc['name']}** {required_badge}")
                    st.caption(doc['description'])
                
                with col2:
                    # Check if file exists
                    if file_exists(doc['file']):
                        st.success("✅ Available")
                    else:
                        st.error("❌ Missing")
                
                with col3:
                    # Download buttons
                    if file_exists(doc['file']):
                        # View button
                        if st.button("👁️ View", key=f"view_{doc['file']}"):
                            st.session_state[f'viewing_{doc["file"]}'] = True
                        
                        # Download button
                        content = read_file_content(doc['file'])
                        if content:
                            st.download_button(
                                label="📥 Download",
                                data=content,
                                file_name=doc['file'],
                                mime="text/markdown",
                                key=f"download_{doc['file']}"
                            )
                
                # Show content if viewing
                if st.session_state.get(f'viewing_{doc["file"]}', False):
                    content = read_file_content(doc['file'])
                    if content:
                        with st.container():
                            st.markdown("---")
                            st.markdown(f"### 📄 {doc['name']}")
                            st.markdown(content)
                            st.markdown("---")
                            if st.button("❌ Close", key=f"close_{doc['file']}"):
                                st.session_state[f'viewing_{doc["file"]}'] = False
                                st.rerun()
                
                st.markdown("---")


def render_admin_document_library():
    """Admin-specific document library"""
    render_document_library("admin")
    
    st.markdown("---")
    
    # Quick actions for admin
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📧 Submit to TQUK**
        
        1. Download CDA Submission Package
        2. Download Email Template
        3. Download Unit Materials
        4. Download Assessment Templates
        5. Send to support@tquk.org
        """)
    
    with col2:
        st.info("""
        **👨‍🏫 Share with Tutors**
        
        1. Download Tutor Delivery Pack
        2. Download Tutor Guide
        3. Share via email or platform
        4. Provide access to unit materials
        """)
    
    with col3:
        st.info("""
        **✅ Share with Assessors**
        
        1. Download Assessment Templates
        2. Download Marking Schemes
        3. Provide unit materials
        4. Set up assessment schedule
        """)


def render_tutor_document_library():
    """Tutor-specific document library"""
    render_document_library("tutor")
    
    st.markdown("---")
    
    # Quick start guide for tutors
    st.subheader("🎯 Quick Start Guide")
    
    st.success("""
    **📚 Essential Documents to Download:**
    
    1. ✅ **Complete Tutor Delivery Pack** - Your main teaching resource
    2. ✅ **Tutor Guide - All 27 Units** - Unit-by-unit teaching notes
    3. ✅ **Assessment Pack Templates** - For assessing students
    4. ✅ **Complete Student Workbook** - To share with students
    
    **🎓 How to Use:**
    
    - **Week 1-8:** Follow the 18-week delivery plan
    - **Each Unit:** Use the tutor guide for key points
    - **Assessments:** Use templates to assess student work
    - **Student Support:** Share workbook and unit materials
    """)


def render_assessor_document_library():
    """Assessor-specific document library"""
    render_document_library("assessor")
    
    st.markdown("---")
    
    # Assessment guidance
    st.subheader("✅ Assessment Guidance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📋 Assessment Methods:**
        
        1. **Observations** - Direct workplace observation
        2. **Witness Statements** - From qualified colleagues
        3. **Professional Discussions** - 30-45 minutes
        4. **Reflective Accounts** - 500-1000 words
        5. **Work Products** - Care plans, records
        """)
    
    with col2:
        st.info("""
        **🎯 Assessment Criteria:**
        
        - ✅ Maps to learning outcomes
        - ✅ Sufficient evidence
        - ✅ Authentic (learner's own work)
        - ✅ Current (recent)
        - ✅ Valid (meets criteria)
        - ✅ Reliable (consistent)
        """)


# Main render function
def render_tquk_documents():
    """Main function to render document library based on user role"""
    
    # Determine user role
    user_role = st.session_state.get('user_role', 'student')
    
    # Only show for admin, tutor, or assessor
    if user_role not in ['admin', 'tutor', 'assessor', 'staff']:
        st.warning("⚠️ Document library is only available for Admin, Tutors, and Assessors.")
        return
    
    # Map staff to admin
    if user_role == 'staff':
        user_role = 'admin'
    
    # Render appropriate library
    if user_role == 'admin':
        render_admin_document_library()
    elif user_role == 'tutor':
        render_tutor_document_library()
    elif user_role == 'assessor':
        render_assessor_document_library()
