"""
T21 ADMIN - AI TRAINING & KNOWLEDGE BASE MANAGER
Upload materials and train AI on your RTT content

Features:
- Upload training materials (PDF, DOCX, TXT)
- Text extraction
- Knowledge base management
- AI training preparation
- Search and test AI knowledge
"""

import streamlit as st
from ai_knowledge_base import (
    add_training_material,
    get_all_materials,
    get_material_by_id,
    get_materials_by_category,
    delete_material,
    get_knowledge_base_stats,
    search_knowledge_base,
    export_knowledge_for_ai,
    save_knowledge_export,
    prepare_fine_tuning_data
)
from document_processor import (
    extract_from_uploaded_file,
    get_supported_formats,
    check_format_support
)
import json
from datetime import datetime


def render_ai_training_admin():
    """Main AI training admin interface"""
    
    st.header("🤖 AI Training & Knowledge Base")
    st.markdown("**Upload your training materials to make AI expert on YOUR content!**")
    
    st.success("""
    ✅ **Upload your RTT materials** - PDFs, documents, videos transcripts  
    ✅ **AI learns from YOUR content** - Becomes expert on your training  
    ✅ **Always references your materials** - No missing information  
    ✅ **Continuous updates** - Add new materials anytime  
    ✅ **Fine-tune AI model** - Train on your specific content  
    """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Upload Materials",
        "📚 Knowledge Base",
        "🔍 Search & Test",
        "⚙️ AI Training",
        "📊 Statistics"
    ])
    
    with tab1:
        render_upload_materials()
    
    with tab2:
        render_knowledge_base()
    
    with tab3:
        render_search_test()
    
    with tab4:
        render_ai_training()
    
    with tab5:
        render_statistics()


def render_upload_materials():
    """Upload training materials"""
    
    st.subheader("📤 Upload Training Materials")
    st.markdown("**Upload your RTT training materials for AI to learn from**")
    
    # Check supported formats
    format_support = check_format_support()
    supported_formats = get_supported_formats()
    
    st.success(f"""
    ✅ **ALL DOCUMENT TYPES SUPPORTED!**
    
    Upload ANY of these formats:
    - 📄 **PDF Documents** {'✅' if format_support['pdf'] else '⚠️ (install PyPDF2)'}
    - 📝 **Word Documents** (.docx, .doc) {'✅' if format_support['word'] else '⚠️ (install python-docx)'}
    - 📊 **Excel Spreadsheets** (.xlsx, .xls) {'✅' if format_support['excel'] else '⚠️ (install openpyxl)'}
    - 📽️ **PowerPoint** (.pptx, .ppt) {'✅' if format_support['powerpoint'] else '⚠️ (install python-pptx)'}
    - 🖼️ **Images with OCR** (.png, .jpg, .jpeg) {'✅' if format_support['image_ocr'] else '⚠️ (install pytesseract)'}
    - 📋 **Text Files** (.txt, .csv, .json) ✅
    - 🌐 **HTML/Markdown** (.html, .md) {'✅' if format_support['html'] else '⚠️ (install beautifulsoup4)'}
    
    **What to Upload:**
    - RTT rules and guidelines
    - Training manuals
    - Case studies
    - NHS documentation
    - Policy documents
    - Best practice guides
    - Video transcripts
    - Course materials
    - Spreadsheets with data
    - Presentation slides
    - Scanned documents (with OCR)
    """)
    
    with st.form("upload_material"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Material Title*", placeholder="e.g., RTT Validation Guide 2025")
            
            material_type = st.selectbox("Material Type*", [
                "PDF Document",
                "Word Document",
                "Training Manual",
                "Video Transcript",
                "Case Study",
                "Policy Document",
                "Guidelines",
                "Presentation",
                "Other"
            ])
            
            category = st.selectbox("Category*", [
                "RTT Rules & Guidelines",
                "Validation Procedures",
                "Pathway Coordination",
                "Case Studies",
                "Best Practices",
                "NHS Policies",
                "Training Scenarios",
                "Clinical Letters",
                "Coding & Classification",
                "Breach Management",
                "Patient Management",
                "Administrative Procedures",
                "Other"
            ])
        
        with col2:
            description = st.text_area("Description", height=100,
                placeholder="Brief description of this material...")
            
            tags_input = st.text_input("Tags (comma-separated)",
                placeholder="rtt, validation, pathway, nhs")
            
            file_name = st.text_input("Original File Name (optional)",
                placeholder="e.g., rtt_guide_2025.pdf")
        
        st.markdown("---")
        st.markdown("### 📝 Material Content")
        
        input_method = st.radio("Input Method:", ["Paste Text", "Upload File"])
        
        content = ""
        
        if input_method == "Paste Text":
            content = st.text_area(
                "Paste Content*",
                height=400,
                placeholder="Paste the complete text content here...\n\nYou can paste:\n- Copied text from PDFs\n- Word document content\n- Training materials\n- Any text content"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload File - ANY FORMAT!",
                type=['txt', 'pdf', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 
                      'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff',
                      'csv', 'json', 'html', 'htm', 'md', 'markdown'],
                help="Upload ANY document type - we'll extract the text automatically!"
            )
            
            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # Use document processor to extract text
                with st.spinner("🔄 Extracting text from document..."):
                    extraction_result = extract_from_uploaded_file(uploaded_file)
                    
                    if extraction_result['success']:
                        content = extraction_result['text']
                        metadata = extraction_result.get('metadata', {})
                        
                        st.success(f"""
                        ✅ **Text Extracted Successfully!**
                        - Characters: {metadata.get('character_count', len(content)):,}
                        - Words: {metadata.get('word_count', len(content.split())):,}
                        - File Type: {extraction_result['file_type']}
                        """)
                        
                        # Show preview
                        with st.expander("👁️ Preview Extracted Text"):
                            st.text_area("Preview (first 1000 characters):", 
                                       content[:1000] + "..." if len(content) > 1000 else content,
                                       height=200)
                    else:
                        st.error(f"❌ Could not extract text: {extraction_result.get('error')}")
                        if 'instructions' in extraction_result:
                            st.info(f"💡 {extraction_result['instructions']}")
                        st.warning("Please try pasting the text manually instead.")
        
        submit = st.form_submit_button("🚀 Upload & Add to Knowledge Base", type="primary")
        
        if submit:
            if not title or not content:
                st.error("❌ Please provide title and content!")
            else:
                with st.spinner("🤖 Processing and adding to knowledge base..."):
                    # Parse tags
                    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
                    
                    # Add material
                    material_id = add_training_material(
                        title=title,
                        content=content,
                        material_type=material_type,
                        category=category,
                        description=description,
                        tags=tags,
                        file_name=file_name or uploaded_file.name if input_method == "Upload File" else ""
                    )
                    
                    st.success(f"✅ Material added successfully! ID: {material_id}")
                    st.balloons()
                    
                    st.info("""
                    🎉 **Material Added to Knowledge Base!**
                    
                    - AI can now reference this material
                    - Content has been chunked for processing
                    - Available for search and retrieval
                    - Included in AI training data
                    
                    Go to "Search & Test" tab to test AI knowledge!
                    """)


def render_knowledge_base():
    """View and manage knowledge base"""
    
    st.subheader("📚 Knowledge Base")
    st.markdown("**All training materials in the knowledge base**")
    
    materials = get_all_materials()
    
    if not materials:
        st.info("📚 No materials uploaded yet. Upload your first material in the 'Upload Materials' tab!")
        return
    
    st.success(f"📚 **{len(materials)} materials in knowledge base**")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        categories = list(set(m['category'] for m in materials))
        selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    with col2:
        material_types = list(set(m['material_type'] for m in materials))
        selected_type = st.selectbox("Filter by Type", ["All"] + material_types)
    
    # Filter materials
    filtered_materials = materials
    if selected_category != "All":
        filtered_materials = [m for m in filtered_materials if m['category'] == selected_category]
    if selected_type != "All":
        filtered_materials = [m for m in filtered_materials if m['material_type'] == selected_type]
    
    st.markdown(f"**Showing {len(filtered_materials)} materials**")
    st.markdown("---")
    
    # Display materials
    for material in filtered_materials:
        with st.expander(f"📄 {material['title']} ({material['category']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**ID:** `{material['material_id']}`")
                st.markdown(f"**Type:** {material['material_type']}")
                st.markdown(f"**Category:** {material['category']}")
                if material['description']:
                    st.markdown(f"**Description:** {material['description']}")
                if material['tags']:
                    st.markdown(f"**Tags:** {', '.join(material['tags'])}")
                st.markdown(f"**Uploaded:** {material['upload_date'][:10]}")
                st.markdown(f"**Size:** {material['word_count']:,} words ({material['character_count']:,} characters)")
            
            with col2:
                if st.button("🗑️ Delete", key=f"del_{material['material_id']}"):
                    if st.session_state.get(f"confirm_delete_{material['material_id']}"):
                        delete_material(material['material_id'])
                        st.success("✅ Deleted!")
                        st.rerun()
                    else:
                        st.session_state[f"confirm_delete_{material['material_id']}"] = True
                        st.warning("Click again to confirm")


def render_search_test():
    """Search knowledge base and test AI"""
    
    st.subheader("🔍 Search & Test AI Knowledge")
    st.markdown("**Test if AI can find information from your materials**")
    
    st.info("""
    💡 **How to Test:**
    1. Enter a question about your training materials
    2. AI searches the knowledge base
    3. See what AI finds and would tell students
    4. Verify AI has learned your content correctly
    """)
    
    query = st.text_input("Ask AI about your training materials:",
        placeholder="e.g., What are the RTT validation rules for urgent referrals?")
    
    category_filter = st.selectbox("Search in Category:", 
        ["All Categories"] + [
            "RTT Rules & Guidelines",
            "Validation Procedures",
            "Pathway Coordination",
            "Case Studies",
            "Best Practices"
        ])
    
    if st.button("🔍 Search Knowledge Base", type="primary"):
        if query:
            with st.spinner("🤖 Searching knowledge base..."):
                category = None if category_filter == "All Categories" else category_filter
                results = search_knowledge_base(query, category=category, limit=5)
                
                if results:
                    st.success(f"✅ Found {len(results)} relevant sections!")
                    
                    st.markdown("### 📚 AI Found This Information:")
                    
                    for idx, result in enumerate(results, 1):
                        with st.expander(f"Result {idx}: {result['material_title']} (Chunk {result['chunk_number']})"):
                            st.markdown(f"**From Material:** {result['material_title']}")
                            st.markdown(f"**Chunk ID:** `{result['chunk_id']}`")
                            st.markdown("---")
                            st.markdown(result['content'])
                    
                    st.markdown("---")
                    st.success("""
                    ✅ **AI Can Access This Information!**
                    
                    When students ask questions, AI will:
                    - Search your knowledge base
                    - Find relevant sections
                    - Provide accurate answers based on YOUR materials
                    - Never miss important information
                    """)
                else:
                    st.warning("❌ No relevant information found. Try different keywords or upload more materials.")
        else:
            st.warning("Please enter a search query!")


def render_ai_training():
    """AI training preparation"""
    
    st.subheader("⚙️ AI Training Preparation")
    st.markdown("**Prepare your materials for AI fine-tuning**")
    
    stats = get_knowledge_base_stats()
    
    st.info(f"""
    📊 **Current Knowledge Base:**
    - {stats['total_materials']} materials uploaded
    - {stats['total_chunks']} chunks processed
    - {stats['total_words']:,} total words
    
    This is enough for AI training!
    """)
    
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Export Full Knowledge")
        st.markdown("Export all materials in one text file for AI context")
        
        if st.button("📥 Export Knowledge Base", type="primary"):
            with st.spinner("Preparing export..."):
                filename = save_knowledge_export()
                st.success(f"✅ Exported to: {filename}")
                st.info("""
                **This file contains:**
                - All your training materials
                - Organized by category
                - Ready for AI to read
                
                Use this file to provide context to AI!
                """)
    
    with col2:
        st.markdown("#### 🎓 Prepare Fine-Tuning Data")
        st.markdown("Create dataset for OpenAI fine-tuning")
        
        if st.button("📥 Generate Fine-Tune Data"):
            with st.spinner("Preparing fine-tuning data..."):
                fine_tune_data = prepare_fine_tuning_data()
                
                # Save to JSONL file
                filename = f"fine_tune_data_{datetime.now().strftime('%Y%m%d')}.jsonl"
                with open(filename, 'w', encoding='utf-8') as f:
                    for example in fine_tune_data:
                        f.write(json.dumps(example) + '\n')
                
                st.success(f"✅ Created: {filename}")
                st.info(f"""
                **Fine-tuning dataset ready!**
                - {len(fine_tune_data)} training examples
                - JSONL format for OpenAI
                - Upload to OpenAI for fine-tuning
                
                Next steps:
                1. Upload to OpenAI platform
                2. Start fine-tuning job
                3. Get custom model ID
                4. Use in your application
                """)
    
    st.markdown("---")
    st.markdown("### 🎯 How AI Uses Your Materials")
    
    st.markdown("""
    **Immediate Use (Already Working):**
    - ✅ AI searches knowledge base when students ask questions
    - ✅ Retrieves relevant sections from your materials
    - ✅ Provides answers based on your content
    - ✅ No training needed - works instantly!
    
    **Fine-Tuning (Advanced):**
    - 🎓 Train custom OpenAI model on your materials
    - 🎓 Model becomes expert on your specific content
    - 🎓 Even better responses
    - 🎓 Faster inference
    
    **Both methods ensure AI never misses your content!**
    """)


def render_statistics():
    """Show knowledge base statistics"""
    
    st.subheader("📊 Knowledge Base Statistics")
    
    stats = get_knowledge_base_stats()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Materials", stats['total_materials'])
    
    with col2:
        st.metric("Total Chunks", stats['total_chunks'])
    
    with col3:
        st.metric("Total Words", f"{stats['total_words']:,}")
    
    with col4:
        avg_words = stats['total_words'] // max(stats['total_materials'], 1)
        st.metric("Avg Words/Material", f"{avg_words:,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📁 Materials by Category")
        for category, count in stats['categories'].items():
            st.markdown(f"**{category}:** {count} materials")
    
    with col2:
        st.markdown("### 📄 Materials by Type")
        for material_type, count in stats['material_types'].items():
            st.markdown(f"**{material_type}:** {count} materials")
    
    st.markdown("---")
    st.markdown("### 📅 Recent Uploads")
    
    if stats['recent_uploads']:
        for material in stats['recent_uploads']:
            st.markdown(f"- **{material['title']}** ({material['category']}) - {material['upload_date'][:10]}")
    else:
        st.info("No materials uploaded yet")
