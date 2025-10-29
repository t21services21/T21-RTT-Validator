"""
TQUK CDA SUBMISSION DOCUMENTS
Download page for all CDA submission materials
"""

import streamlit as st
import os
from datetime import datetime
from io import BytesIO
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import markdown2
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

st.set_page_config(page_title="TQUK CDA Documents", page_icon="📋", layout="wide")

# Conversion functions
def markdown_to_word(markdown_text, title):
    """Convert markdown to Word document"""
    doc = Document()
    
    # Add title
    title_para = doc.add_heading(title, 0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add metadata
    doc.add_paragraph(f"Centre: T21 Services UK (#36257481088)")
    doc.add_paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}")
    doc.add_paragraph("")
    
    # Process markdown content
    lines = markdown_text.split('\n')
    for line in lines:
        if line.startswith('# '):
            doc.add_heading(line[2:], 1)
        elif line.startswith('## '):
            doc.add_heading(line[3:], 2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], 3)
        elif line.startswith('#### '):
            doc.add_heading(line[5:], 4)
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            doc.add_paragraph(line.strip()[2:], style='List Bullet')
        elif line.strip().startswith('✓ ') or line.strip().startswith('✅ '):
            doc.add_paragraph(line.strip(), style='List Bullet')
        elif line.strip():
            doc.add_paragraph(line)
    
    # Save to BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def markdown_to_pdf(markdown_text, title):
    """Convert markdown to PDF document"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=RGBColor(0, 0, 139),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=RGBColor(0, 0, 139),
        spaceAfter=12,
        spaceBefore=12
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=RGBColor(0, 0, 139),
        spaceAfter=10,
        spaceBefore=10
    )
    
    # Add title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 12))
    
    # Add metadata
    elements.append(Paragraph(f"<b>Centre:</b> T21 Services UK (#36257481088)", styles['Normal']))
    elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Process markdown content
    lines = markdown_text.split('\n')
    for line in lines:
        if line.startswith('# '):
            elements.append(Paragraph(line[2:], heading1_style))
        elif line.startswith('## '):
            elements.append(Paragraph(line[3:], heading2_style))
        elif line.startswith('### '):
            elements.append(Paragraph(line[4:], styles['Heading3']))
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            elements.append(Paragraph(f"• {line.strip()[2:]}", styles['Normal']))
        elif line.strip().startswith('✓ ') or line.strip().startswith('✅ '):
            elements.append(Paragraph(line.strip(), styles['Normal']))
        elif line.strip() == '---':
            elements.append(Spacer(1, 12))
        elif line.strip():
            # Clean up markdown formatting
            clean_line = line.replace('**', '').replace('`', '')
            elements.append(Paragraph(clean_line, styles['Normal']))
            elements.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Header
st.title("📋 TQUK CDA Submission Documents")
st.markdown("**Centre:** T21 Services UK (#36257481088)")
st.markdown(f"**Generated:** {datetime.now().strftime('%B %d, %Y')}")

st.divider()

# Introduction
st.info("""
**Complete CDA Package for 10 TQUK Qualifications**

This page provides access to all Centre-Devised Assessment (CDA) submission documents 
for TQUK approval of our AI-powered digital learning platform.
""")

# Document list
st.header("📄 Available Documents")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ Master Mapping Document")
    st.markdown("""
    **Size:** 6,500+ words  
    **Content:**
    - Complete mapping of all 10 qualifications
    - Learning outcomes coverage
    - Assessment criteria alignment
    - Platform overview
    - Evidence requirements
    """)
    
    # Check if file exists
    file_path_1 = "TQUK_CDA_MASTER_MAPPING_DOCUMENT.md"
    if os.path.exists(file_path_1):
        with open(file_path_1, 'r', encoding='utf-8') as f:
            content_1 = f.read()
        
        # PDF Download
        pdf_buffer_1 = markdown_to_pdf(content_1, "TQUK CDA Master Mapping Document")
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_buffer_1,
            file_name="TQUK_CDA_Master_Mapping_Document.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        # Word Download
        word_buffer_1 = markdown_to_word(content_1, "TQUK CDA Master Mapping Document")
        st.download_button(
            label="📝 Download as Word",
            data=word_buffer_1,
            file_name="TQUK_CDA_Master_Mapping_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    else:
        st.error("File not found")

with col2:
    st.subheader("2️⃣ Assessment Strategy")
    st.markdown("""
    **Size:** 4,500+ words  
    **Content:**
    - Assessment principles (VRASAC)
    - Assessment methods detailed
    - Quality assurance processes
    - Staff roles and responsibilities
    - Continuous improvement
    """)
    
    file_path_2 = "TQUK_CDA_ASSESSMENT_STRATEGY.md"
    if os.path.exists(file_path_2):
        with open(file_path_2, 'r', encoding='utf-8') as f:
            content_2 = f.read()
        
        # PDF Download
        pdf_buffer_2 = markdown_to_pdf(content_2, "TQUK CDA Assessment Strategy")
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_buffer_2,
            file_name="TQUK_CDA_Assessment_Strategy.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        # Word Download
        word_buffer_2 = markdown_to_word(content_2, "TQUK CDA Assessment Strategy")
        st.download_button(
            label="📝 Download as Word",
            data=word_buffer_2,
            file_name="TQUK_CDA_Assessment_Strategy.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    else:
        st.error("File not found")

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("3️⃣ Form Completion Guide")
    st.markdown("""
    **Size:** 3,000+ words  
    **Content:**
    - Step-by-step form filling instructions
    - Exact text to copy/paste
    - Email template
    - Submission checklist
    - Timeline expectations
    """)
    
    file_path_3 = "TQUK_CDA_FORM_COMPLETION_GUIDE.md"
    if os.path.exists(file_path_3):
        with open(file_path_3, 'r', encoding='utf-8') as f:
            content_3 = f.read()
        
        # PDF Download
        pdf_buffer_3 = markdown_to_pdf(content_3, "TQUK CDA Form Completion Guide")
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_buffer_3,
            file_name="TQUK_CDA_Form_Completion_Guide.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        # Word Download
        word_buffer_3 = markdown_to_word(content_3, "TQUK CDA Form Completion Guide")
        st.download_button(
            label="📝 Download as Word",
            data=word_buffer_3,
            file_name="TQUK_CDA_Form_Completion_Guide.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    else:
        st.error("File not found")

with col4:
    st.subheader("4️⃣ Complete Package Summary")
    st.markdown("""
    **Size:** 2,500+ words  
    **Content:**
    - Overview of everything
    - Your action steps
    - Timeline
    - Success metrics
    - Revenue potential
    """)
    
    file_path_4 = "TQUK_CDA_SUBMISSION_COMPLETE_PACKAGE.md"
    if os.path.exists(file_path_4):
        with open(file_path_4, 'r', encoding='utf-8') as f:
            content_4 = f.read()
        
        # PDF Download
        pdf_buffer_4 = markdown_to_pdf(content_4, "TQUK CDA Complete Package Summary")
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_buffer_4,
            file_name="TQUK_CDA_Complete_Package_Summary.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        # Word Download
        word_buffer_4 = markdown_to_word(content_4, "TQUK CDA Complete Package Summary")
        st.download_button(
            label="📝 Download as Word",
            data=word_buffer_4,
            file_name="TQUK_CDA_Complete_Package_Summary.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    else:
        st.error("File not found")

st.divider()

# Qualifications covered
st.header("📚 Qualifications Covered (10 Total)")

col5, col6, col7 = st.columns(3)

with col5:
    st.subheader("🔤 Functional Skills (4)")
    st.markdown("""
    1. English Level 1 (610/2626/6)
    2. English Level 2 (610/2625/6)
    3. Maths Level 1 (610/2623/2)
    4. Maths Level 2 (610/2624/4)
    """)

with col6:
    st.subheader("📊 Level 2 Certificates (4)")
    st.markdown("""
    5. Customer Service (603/3895/7)
    6. IT User Skills (603/5640/9)
    7. Adult Social Care (601/4040/9)
    8. Business Admin (603/2949/X)
    """)

with col7:
    st.subheader("🎓 Level 3 Qualifications (2)")
    st.markdown("""
    9. Teaching & Learning (601/2731/4)
    10. Adult Care (610/0103/6)
    """)

st.divider()

# Next steps
st.header("🚀 Next Steps")

st.success("""
**After Downloading:**

1. **Convert to PDF** - Open each .md file in Word or use an online converter
2. **Create Google Drive Folder** - Organize all documents
3. **Take Platform Screenshots** - Capture key features
4. **Fill CDA Form** - Use the Form Completion Guide
5. **Submit to TQUK** - Email with Google Drive link

**Expected Timeline:**
- Submission: Today
- TQUK Review: 5-15 working days
- Approval: December 2025
""")

# Additional resources
st.header("📖 Additional Resources")

with st.expander("📋 Qualifications List"):
    file_path_5 = "TQUK_ALL_QUALIFICATIONS_COMPLETE_LIST.md"
    if os.path.exists(file_path_5):
        with open(file_path_5, 'r', encoding='utf-8') as f:
            content_5 = f.read()
        
        st.download_button(
            label="📥 Download Complete Qualifications List",
            data=content_5,
            file_name="TQUK_All_Qualifications_List.md",
            mime="text/markdown"
        )
    else:
        st.warning("Qualifications list not found")

with st.expander("📝 Submission Guide"):
    file_path_6 = "TQUK_CDA_FORM_SUBMISSION_GUIDE.md"
    if os.path.exists(file_path_6):
        with open(file_path_6, 'r', encoding='utf-8') as f:
            content_6 = f.read()
        
        st.download_button(
            label="📥 Download Original Submission Guide",
            data=content_6,
            file_name="TQUK_CDA_Form_Submission_Guide.md",
            mime="text/markdown"
        )

st.divider()

# Contact info
st.info("""
**Questions?**

Contact TQUK:
- Email: support@tquk.org / quality@tquk.org
- Phone: 03333 58 3344

Centre Contact:
- Amb. Tosin Michael Owonifari
- Email: t.owonifari@t21services.co.uk
""")

# Footer
st.markdown("---")
st.caption("T21 Services UK | Centre #36257481088 | TQUK Approved Centre")
st.caption(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
