"""
LEARNING MATERIALS MANAGEMENT SYSTEM
Upload and manage learning resources for students

Features:
- Upload documents (PDF, Word, Excel, PowerPoint)
- Organize by category/topic
- Attach to specific competencies
- Student access to materials
- Download tracking
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
from supabase_client import get_supabase_client
import json
import os


def upload_learning_material(
    title: str,
    description: str,
    category: str,
    file_url: str,
    file_name: str,
    file_type: str,
    file_size: int,
    competency: str = "",
    week: int = 0,
    required: bool = True,
    visible_to_all: bool = True
) -> Dict:
    """Upload a learning material"""
    
    try:
        supabase = get_supabase_client()
        
        material_data = {
            'title': title,
            'description': description,
            'category': category,
            'file_url': file_url,
            'file_name': file_name,
            'file_type': file_type,
            'file_size': file_size,
            'competency': competency,
            'week': week,
            'required': required,
            'visible_to_all': visible_to_all,
            'uploaded_by': st.session_state.get('user_email', 'admin@example.com'),
            'uploaded_date': datetime.now().date().isoformat(),
            'download_count': 0,
            'status': 'active'
        }
        
        if supabase:
            result = supabase.table('learning_materials').insert(material_data).execute()
            return {
                'success': True,
                'message': 'Material uploaded successfully',
                'material_id': result.data[0].get('id') if result.data else None
            }
        else:
            # Local storage
            materials_file = 'data/learning_materials.json'
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(materials_file):
                with open(materials_file, 'r') as f:
                    materials = json.load(f)
            else:
                materials = []
            
            material_data['id'] = f"MAT-{len(materials) + 1:05d}"
            materials.append(material_data)
            
            with open(materials_file, 'w') as f:
                json.dump(materials, f, indent=2)
            
            return {
                'success': True,
                'message': 'Material uploaded successfully',
                'material_id': material_data['id']
            }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_all_materials(category: str = None, competency: str = None, week: int = None) -> List[Dict]:
    """Get all learning materials with filters"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('learning_materials').select('*').eq('status', 'active')
            
            if category:
                query = query.eq('category', category)
            if competency:
                query = query.eq('competency', competency)
            if week is not None:
                query = query.eq('week', week)
            
            result = query.order('uploaded_date', desc=True).execute()
            return result.data if result.data else []
        else:
            materials_file = 'data/learning_materials.json'
            if os.path.exists(materials_file):
                with open(materials_file, 'r') as f:
                    materials = json.load(f)
                
                # Filter
                if category:
                    materials = [m for m in materials if m.get('category') == category]
                if competency:
                    materials = [m for m in materials if m.get('competency') == competency]
                if week is not None:
                    materials = [m for m in materials if m.get('week') == week]
                
                materials = [m for m in materials if m.get('status') == 'active']
                return sorted(materials, key=lambda x: x.get('uploaded_date', ''), reverse=True)
            return []
    
    except Exception as e:
        st.error(f"Error getting materials: {e}")
        return []


def track_download(material_id: str, student_email: str) -> Dict:
    """Track when a student downloads a material"""
    
    try:
        supabase = get_supabase_client()
        
        download_data = {
            'material_id': material_id,
            'student_email': student_email,
            'download_date': datetime.now().isoformat()
        }
        
        if supabase:
            # Record download
            supabase.table('material_downloads').insert(download_data).execute()
            
            # Increment download count
            supabase.rpc('increment_download_count', {'material_id': material_id}).execute()
            
            return {'success': True}
        else:
            # Local tracking
            downloads_file = 'data/material_downloads.json'
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(downloads_file):
                with open(downloads_file, 'r') as f:
                    downloads = json.load(f)
            else:
                downloads = []
            
            downloads.append(download_data)
            
            with open(downloads_file, 'w') as f:
                json.dump(downloads, f, indent=2)
            
            return {'success': True}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def delete_material(material_id: str) -> Dict:
    """Soft delete a material"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('learning_materials').update({
                'status': 'deleted',
                'deleted_date': datetime.now().date().isoformat()
            }).eq('id', material_id).execute()
            return {'success': True, 'message': 'Material deleted'}
        else:
            materials_file = 'data/learning_materials.json'
            if os.path.exists(materials_file):
                with open(materials_file, 'r') as f:
                    materials = json.load(f)
                
                for material in materials:
                    if material.get('id') == material_id:
                        material['status'] = 'deleted'
                        material['deleted_date'] = datetime.now().date().isoformat()
                
                with open(materials_file, 'w') as f:
                    json.dump(materials, f, indent=2)
            
            return {'success': True, 'message': 'Material deleted'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_learning_materials_manager():
    """UI for managing learning materials (Teacher view)"""
    
    st.subheader("📚 Learning Materials Manager")
    
    st.info("""
    **Upload and manage learning resources:**
    - Documents (PDF, Word, Excel, PowerPoint)
    - Organize by category and competency
    - Track student downloads
    - Required vs optional materials
    """)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "➕ Upload Material",
        "📋 All Materials",
        "📊 Download Statistics"
    ])
    
    with tab1:
        render_upload_material()
    
    with tab2:
        render_all_materials()
    
    with tab3:
        render_download_stats()


def render_upload_material():
    """Upload new learning material"""
    
    st.markdown("### ➕ Upload Learning Material")
    
    st.warning("**Note:** File upload requires Supabase Storage to be configured. For now, you can paste a file URL (e.g., Google Drive, Dropbox, OneDrive link).")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Title*", placeholder="e.g., Week 1 - Introduction to NHS Pathways")
        category = st.selectbox("Category*", [
            "Lecture Notes",
            "Tutorial Sheets",
            "Practice Exercises",
            "Reference Materials",
            "Templates",
            "Handouts",
            "Other"
        ])
        competency = st.selectbox("Related Competency", [
            "None",
            "Patient Registration",
            "Pathway Creation",
            "Episode Management",
            "RTT Clock Management",
            "Milestone Recording"
        ])
    
    with col2:
        week = st.number_input("Week Number", min_value=0, max_value=52, value=1)
        required = st.checkbox("Required Material", value=True)
        visible_to_all = st.checkbox("Visible to All Students", value=True)
    
    description = st.text_area("Description*", placeholder="Brief description of what this material covers...")
    
    file_url = st.text_input("File URL*", placeholder="https://drive.google.com/file/d/...")
    
    col1, col2 = st.columns(2)
    with col1:
        file_name = st.text_input("File Name*", placeholder="week1_introduction.pdf")
    with col2:
        file_type = st.selectbox("File Type*", ["PDF", "Word", "Excel", "PowerPoint", "Other"])
    
    if st.button("📤 Upload Material", type="primary"):
        if not title or not description or not file_url or not file_name:
            st.error("Please fill in all required fields")
            return
        
        result = upload_learning_material(
            title=title,
            description=description,
            category=category,
            file_url=file_url,
            file_name=file_name,
            file_type=file_type,
            file_size=0,  # Unknown for URL-based uploads
            competency=competency if competency != "None" else "",
            week=week,
            required=required,
            visible_to_all=visible_to_all
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            st.balloons()
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_all_materials():
    """View all learning materials"""
    
    st.markdown("### 📋 All Learning Materials")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("Filter by Category:", ["All"] + [
            "Lecture Notes", "Tutorial Sheets", "Practice Exercises",
            "Reference Materials", "Templates", "Handouts", "Other"
        ])
    
    with col2:
        week_filter = st.selectbox("Filter by Week:", ["All"] + [f"Week {i}" for i in range(1, 13)])
    
    with col3:
        competency_filter = st.selectbox("Filter by Competency:", ["All", "Patient Registration",
            "Pathway Creation", "Episode Management", "RTT Clock Management", "Milestone Recording"])
    
    # Apply filters
    category = None if category_filter == "All" else category_filter
    week = None if week_filter == "All" else int(week_filter.replace("Week ", ""))
    competency = None if competency_filter == "All" else competency_filter
    
    materials = get_all_materials(category=category, competency=competency, week=week)
    
    if not materials:
        st.info("No materials found matching filters.")
        return
    
    st.write(f"**Total Materials: {len(materials)}**")
    
    # Display materials
    for material in materials:
        required_badge = "🔴 Required" if material.get('required') else "🔵 Optional"
        
        with st.expander(f"📄 {material['title']} - Week {material.get('week', 0)} ({required_badge})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Title:** {material['title']}")
                st.write(f"**Description:** {material['description']}")
                st.write(f"**Category:** {material['category']}")
                if material.get('competency'):
                    st.write(f"**Competency:** {material['competency']}")
            
            with col2:
                st.write(f"**Week:** {material.get('week', 0)}")
                st.write(f"**Type:** {material.get('file_type')}")
                st.write(f"**Uploaded:** {material.get('uploaded_date')}")
                st.write(f"**Downloads:** {material.get('download_count', 0)}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"🔗 View File", key=f"view_{material.get('id')}"):
                    st.markdown(f"[Open File]({material['file_url']})")
            
            with col2:
                st.download_button(
                    "📥 Download Link",
                    data=material['file_url'],
                    file_name="link.txt",
                    key=f"download_{material.get('id')}"
                )
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"delete_{material.get('id')}"):
                    result = delete_material(material.get('id'))
                    if result.get('success'):
                        st.success("Material deleted")
                        st.rerun()


def render_download_stats():
    """Show download statistics"""
    
    st.markdown("### 📊 Download Statistics")
    
    materials = get_all_materials()
    
    if not materials:
        st.info("No materials uploaded yet.")
        return
    
    # Sort by download count
    sorted_materials = sorted(materials, key=lambda x: x.get('download_count', 0), reverse=True)
    
    st.markdown("#### Most Downloaded Materials")
    
    for i, material in enumerate(sorted_materials[:10], 1):
        downloads = material.get('download_count', 0)
        st.write(f"{i}. **{material['title']}** - {downloads} downloads")
    
    # Category breakdown
    st.markdown("---")
    st.markdown("#### Downloads by Category")
    
    category_downloads = {}
    for material in materials:
        category = material.get('category', 'Other')
        downloads = material.get('download_count', 0)
        category_downloads[category] = category_downloads.get(category, 0) + downloads
    
    for category, downloads in category_downloads.items():
        st.write(f"**{category}:** {downloads} downloads")


def render_student_materials_view():
    """Student view of learning materials"""
    
    st.subheader("📚 Learning Materials")
    
    st.info("Access course materials, lecture notes, and resources")
    
    # Week selector
    week = st.selectbox("Select Week:", ["All Weeks"] + [f"Week {i}" for i in range(1, 13)])
    
    week_num = None if week == "All Weeks" else int(week.replace("Week ", ""))
    
    materials = get_all_materials(week=week_num)
    
    if not materials:
        st.info("No materials available for this week.")
        return
    
    # Group by category
    categories = {}
    for material in materials:
        category = material.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(material)
    
    # Display by category
    for category, items in categories.items():
        st.markdown(f"### 📁 {category}")
        
        for material in items:
            required_icon = "🔴" if material.get('required') else "🔵"
            
            with st.expander(f"{required_icon} {material['title']}"):
                st.write(f"**Description:** {material['description']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {material.get('file_type')}")
                    st.write(f"**Week:** {material.get('week', 0)}")
                
                with col2:
                    if material.get('competency'):
                        st.write(f"**Competency:** {material['competency']}")
                    st.write(f"**Downloads:** {material.get('download_count', 0)}")
                
                if st.button(f"📥 Download / View", key=f"student_download_{material.get('id')}"):
                    # Track download
                    student_email = st.session_state.get('user_email', 'student@example.com')
                    track_download(material.get('id'), student_email)
                    
                    st.markdown(f"[**🔗 Open File**]({material['file_url']})")
                    st.success("Download tracked! Click link above to access material.")
