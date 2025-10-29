"""
TQUK CDA SUBMISSION DOCUMENTS
Download page for all CDA submission materials
"""

import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="TQUK CDA Documents", page_icon="📋", layout="wide")

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
        
        st.download_button(
            label="📥 Download Master Mapping Document",
            data=content_1,
            file_name="TQUK_CDA_Master_Mapping_Document.md",
            mime="text/markdown",
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
        
        st.download_button(
            label="📥 Download Assessment Strategy",
            data=content_2,
            file_name="TQUK_CDA_Assessment_Strategy.md",
            mime="text/markdown",
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
        
        st.download_button(
            label="📥 Download Form Completion Guide",
            data=content_3,
            file_name="TQUK_CDA_Form_Completion_Guide.md",
            mime="text/markdown",
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
        
        st.download_button(
            label="📥 Download Complete Package Summary",
            data=content_4,
            file_name="TQUK_CDA_Complete_Package_Summary.md",
            mime="text/markdown",
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
