"""
TQUK DOCUMENT LIBRARY
Complete document management for Admin, Tutors, and Assessors
"""

import streamlit as st
import os
from pathlib import Path
from datetime import datetime

# Company branding information
COMPANY_INFO = {
    "name": "T21 SERVICES LIMITED",
    "company_number": "13091053",
    "centre_number": "36257481088",
    "address_line1": "64 Upper Parliament Street",
    "address_line2": "Liverpool",
    "postcode": "L8 7LF",
    "country": "United Kingdom",
    "email": "t.owonifari@t21services.co.uk",
    "phone": "07447459420",
    "website": "www.t21services.co.uk",
    "centre_manager": "H.E. Ambassador Tosin Michael Owonifari",
    "qualification": "Level 3 Diploma in Adult Care (RQF)",
    "qualification_code": "610/0103/6"
}


def get_document_header():
    """Generate professional document header with company branding"""
    header = f"""
{'='*80}

                            {COMPANY_INFO['name']}
                    Company Number: {COMPANY_INFO['company_number']}
                    TQUK Approved Centre #{COMPANY_INFO['centre_number']}
                {COMPANY_INFO['qualification']} - {COMPANY_INFO['qualification_code']}

{'='*80}

REGISTERED OFFICE:
{COMPANY_INFO['name']}
{COMPANY_INFO['address_line1']}
{COMPANY_INFO['address_line2']}
{COMPANY_INFO['postcode']}
{COMPANY_INFO['country']}

CONTACT DETAILS:
📧 Email: {COMPANY_INFO['email']}
📞 Phone: {COMPANY_INFO['phone']}
🌐 Website: {COMPANY_INFO['website']}

CENTRE INFORMATION:
Centre Number: {COMPANY_INFO['centre_number']}
Centre Manager: {COMPANY_INFO['centre_manager']}
Awarding Organization: TQUK (Training Qualifications UK)
Qualification: {COMPANY_INFO['qualification']}
Qualification Code: {COMPANY_INFO['qualification_code']}

{'='*80}

"""
    return header


def get_document_footer():
    """Generate professional document footer"""
    footer = f"""

{'='*80}

{COMPANY_INFO['name']} | TQUK Centre #{COMPANY_INFO['centre_number']}
📧 {COMPANY_INFO['email']} | 📞 {COMPANY_INFO['phone']}
{COMPANY_INFO['qualification']} - {COMPANY_INFO['qualification_code']}

© {datetime.now().year} {COMPANY_INFO['name']}. All Rights Reserved.
Company Number: {COMPANY_INFO['company_number']}
This document is the property of {COMPANY_INFO['name']} and may not be 
reproduced without permission.

{'='*80}
"""
    return footer


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


def read_file_content(filename, add_branding=False):
    """Read the content of a file, optionally with company branding"""
    try:
        file_path = get_file_path(filename)
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add company branding if requested
            if add_branding:
                content = get_document_header() + content + get_document_footer()
            
            return content
        return None
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None


def get_branded_content(filename):
    """Get file content with full company branding for official use"""
    content = read_file_content(filename, add_branding=False)
    if content:
        # Add header and footer
        branded_content = get_document_header() + "\n" + content + "\n" + get_document_footer()
        return branded_content
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
                        
                        # Download WITH BRANDING button (for official use)
                        branded_content = get_branded_content(doc['file'])
                        if branded_content:
                            # Create filename with branding indicator
                            base_name = doc['file'].replace('.md', '')
                            branded_filename = f"{base_name}_OFFICIAL.txt"
                            
                            st.download_button(
                                label="📥 Official",
                                data=branded_content,
                                file_name=branded_filename,
                                mime="text/plain",
                                key=f"download_branded_{doc['file']}",
                                help="Download with T21 Services branding for official use"
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
    
    # Important instructions at the top
    st.info("""
    ### 📥 **How to Download for TQUK Submission:**
    
    1. Click "📥 Official" button to download with T21 Services branding
    2. Files download as .txt format with full company details
    3. **To convert to PDF:**
       - **Option 1:** Open in Word → Save As PDF
       - **Option 2:** Use online converter: https://www.markdowntopdf.com/
       - **Option 3:** Copy content to Google Docs → Download as PDF
    
    ✅ All downloads include your registered office address and company details!
    """)
    
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
