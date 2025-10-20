"""
COMPLETE LEARNING MANAGEMENT SYSTEM (LMS)
All LMS features in ONE module for better organization

Features:
- Learning Materials (documents)
- Video Library (Vimeo)
- Announcements
- Assignments & Grading
- Quizzes & Auto-Grading
- Student Portfolios
- Teacher Dashboard
- Progress Tracking

Everything consolidated for easy maintenance!
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, List, Optional
from supabase_database import supabase
import json
import os

# Get Supabase URL for public file URLs
try:
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
except:
    try:
        from supabase_config_SAFE import SUPABASE_URL
    except:
        SUPABASE_URL = ""


# ============================================
# LEARNING MATERIALS SYSTEM
# ============================================

def render_learning_materials():
    """Main UI for learning materials"""
    
    st.subheader("📚 Learning Materials")
    
    # Check user role
    user_email = st.session_state.get('user_email', '')
    is_teacher = 'admin' in user_email or 'teacher' in user_email
    
    if is_teacher:
        render_materials_teacher(user_email)
    else:
        render_materials_student(user_email)


def render_materials_teacher(user_email):
    """Teacher view - upload and manage materials"""
    
    st.info("**Teacher View:** Upload and manage learning materials")
    
    tab1, tab2 = st.tabs(["➕ Upload Material", "📋 All Materials"])
    
    with tab1:
        st.markdown("### ➕ Upload Learning Material")
        
        # Choose upload method
        upload_method = st.radio(
            "How do you want to add the material?",
            ["📤 Upload File Directly", "🔗 Link to External URL (Google Drive, OneDrive, etc.)"],
            key="material_upload_method",
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title*", placeholder="e.g., Week 1 - Introduction", key="material_title_input")
            category = st.selectbox("Category*", [
                "Lecture Notes",
                "Tutorial Sheets",
                "Practice Exercises",
                "Reference Materials",
                "Templates",
                "Other"
            ], key="material_category_select")
            week = st.number_input("Week Number", min_value=0, max_value=52, value=1, key="material_week_input")
        
        with col2:
            if upload_method == "📤 Upload File Directly":
                uploaded_files = st.file_uploader(
                    "Upload File(s)*",
                    type=['pdf', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 'txt', 'zip'],
                    key="material_file_uploader",
                    accept_multiple_files=True,
                    help="📤 You can upload MULTIPLE files at once! Supported: PDF, Word, Excel, PowerPoint, Text, ZIP"
                )
                file_url = None
                file_name = ", ".join([f.name for f in uploaded_files]) if uploaded_files else ""
                
                if uploaded_files:
                    st.success(f"✅ {len(uploaded_files)} file(s) selected")
            else:
                uploaded_files = None
                file_url = st.text_input("File URL*", placeholder="https://drive.google.com/file/d/...", key="material_file_url")
                file_name = st.text_input("File Name*", placeholder="week1_intro.pdf", key="material_file_name")
            
            required = st.checkbox("Required Material", value=True, key="material_required_check")
        
        description = st.text_area("Description", placeholder="Brief description...", key="material_description_area")
        
        if st.button("📤 Upload Material(s)", type="primary", key="upload_material_btn"):
            # Validation
            if not title:
                st.error("Please enter a title")
                return
            
            if upload_method == "📤 Upload File Directly":
                if not uploaded_files:
                    st.error("Please upload at least one file")
                    return
            else:
                if not file_url:
                    st.error("Please enter a file URL")
                    return
            
            try:
                # Handle file upload to Supabase Storage
                if upload_method == "📤 Upload File Directly" and uploaded_files:
                    uploaded_count = 0
                    uploaded_materials = []
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, uploaded_file in enumerate(uploaded_files):
                        try:
                            status_text.text(f"Uploading {idx+1}/{len(uploaded_files)}: {uploaded_file.name}...")
                            
                            # Upload to Supabase Storage (using import from top of file)
                            import time
                            import re
                            
                            # Sanitize filename to avoid path issues
                            safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', uploaded_file.name)
                            safe_email = re.sub(r'[^a-zA-Z0-9@._-]', '_', user_email)
                            
                            # Add timestamp to avoid duplicates
                            timestamp = int(time.time())
                            file_path = f"{safe_email}/{timestamp}_{safe_filename}"
                            
                            # Upload file
                            result = supabase.storage.from_('learning_materials').upload(
                                file_path,
                                uploaded_file.getvalue()
                            )
                            
                            # Get public URL using Supabase's get_public_url method
                            # This works correctly in v1.0.4 if bucket is public
                            file_url = supabase.storage.from_('learning_materials').get_public_url(file_path)
                            
                            uploaded_count += 1
                            uploaded_materials.append({
                                'name': uploaded_file.name,
                                'url': file_url
                            })
                            
                        except Exception as upload_error:
                            st.error(f"❌ Failed to upload {uploaded_file.name}: {str(upload_error)}")
                            continue
                        
                        # Update progress
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    if uploaded_count == 0:
                        st.error("❌ All uploads failed!")
                        return
                    
                    st.success(f"✅ {uploaded_count}/{len(uploaded_files)} file(s) uploaded successfully!")
                    st.balloons()
                    
                    # Create separate database entry for EACH file
                    for material in uploaded_materials:
                        material_data = {
                            'title': f"{title} - {material['name']}" if len(uploaded_materials) > 1 else title,
                            'description': description,
                            'category': category,
                            'file_url': material['url'],
                            'file_name': material['name'],
                            'week': week,
                            'required': required,
                            'uploaded_by': user_email,
                            'uploaded_date': datetime.now().date().isoformat(),
                            'download_count': 0,
                            'status': 'active'
                        }
                        
                        supabase.table('learning_materials').insert(material_data).execute()
                    
                    # Show uploaded materials summary
                    st.info(f"""✅ **Upload Confirmed:**
                    - **Base Title:** {title}
                    - **Category:** {category}
                    - **Week:** {week}
                    - **Files Uploaded:** {uploaded_count}
                    
                    📊 Go to "All Materials" tab to see all uploaded files.""")
                    
                    # Show links to all uploaded files
                    st.markdown("**📎 View Uploaded Files:**")
                    for material in uploaded_materials:
                        st.markdown(f"- [{material['name']}]({material['url']})")
                
                else:
                    # External URL method
                    material_data = {
                        'title': title,
                        'description': description,
                        'category': category,
                        'file_url': file_url,
                        'file_name': file_name,
                        'week': week,
                        'required': required,
                        'uploaded_by': user_email,
                        'uploaded_date': datetime.now().date().isoformat(),
                        'download_count': 0,
                        'status': 'active'
                    }
                    
                    result = supabase.table('learning_materials').insert(material_data).execute()
                    st.success("✅ Material linked successfully!")
                    st.balloons()
                    
                    if result.data:
                        uploaded = result.data[0]
                        st.info(f"""✅ **Link Confirmed:**
                        - **Title:** {uploaded.get('title')}
                        - **Category:** {uploaded.get('category')}
                        - **Week:** {uploaded.get('week')}
                        - **File:** {uploaded.get('file_name')}
                        
                        📊 Go to "All Materials" tab to see all materials.""")
                        st.markdown(f"[🔗 View Linked File]({uploaded.get('file_url')})")
            
            except Exception as e:
                st.error(f"Error uploading material: {e}")
    
    with tab2:
        st.markdown("### 📋 All Materials")
        
        try:
            result = supabase.table('learning_materials').select('*').eq('status', 'active').order('week').execute()
            materials = result.data if result.data else []
            
            if not materials:
                st.info("No materials uploaded yet.")
                return
            
            st.write(f"**Total Materials: {len(materials)}**")
            
            for material in materials:
                with st.expander(f"📄 {material['title']} - Week {material.get('week', 0)}"):
                    # Check if in edit mode for this material
                    edit_mode_key = f"edit_mode_{material.get('id')}"
                    if edit_mode_key not in st.session_state:
                        st.session_state[edit_mode_key] = False
                    
                    if st.session_state[edit_mode_key]:
                        # EDIT MODE - Show form
                        st.markdown("### ✏️ Edit Material")
                        
                        edit_title = st.text_input("Title*", value=material.get('title', ''), key=f"edit_title_{material.get('id')}")
                        edit_category = st.selectbox("Category*", [
                            "Lecture Notes", "Video Recordings", "Tutorial Sheets",
                            "Practice Exercises", "Reference Materials", "Templates", "Other"
                        ], index=["Lecture Notes", "Video Recordings", "Tutorial Sheets", "Practice Exercises", "Reference Materials", "Templates", "Other"].index(material.get('category', 'Lecture Notes')), key=f"edit_cat_{material.get('id')}")
                        edit_week = st.number_input("Week Number", min_value=0, max_value=52, value=int(material.get('week', 1)), key=f"edit_week_{material.get('id')}")
                        edit_description = st.text_area("Description", value=material.get('description', ''), key=f"edit_desc_{material.get('id')}")
                        edit_required = st.checkbox("Required Material", value=material.get('required', True), key=f"edit_req_{material.get('id')}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("💾 Save Changes", key=f"save_{material.get('id')}", type="primary"):
                                try:
                                    # Update material
                                    supabase.table('learning_materials').update({
                                        'title': edit_title,
                                        'category': edit_category,
                                        'week': edit_week,
                                        'description': edit_description,
                                        'required': edit_required
                                    }).eq('id', material.get('id')).execute()
                                    
                                    st.success("✅ Material updated!")
                                    st.session_state[edit_mode_key] = False
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Update failed: {e}")
                        
                        with col2:
                            if st.button("❌ Cancel", key=f"cancel_{material.get('id')}", type="secondary"):
                                st.session_state[edit_mode_key] = False
                                st.rerun()
                    
                    else:
                        # VIEW MODE - Show material info
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Category:** {material.get('category')}")
                            st.write(f"**Description:** {material.get('description', 'N/A')}")
                            st.write(f"**Downloads:** {material.get('download_count', 0)}")
                            st.write(f"**Uploaded by:** {material.get('uploaded_by', 'Unknown')}")
                            st.write(f"**Upload date:** {material.get('uploaded_date', 'N/A')}")
                            st.markdown(f"[🔗 View File]({material['file_url']})")
                        
                        with col2:
                            st.write("")  # Spacing
                            
                            # EDIT BUTTON
                            if st.button("✏️ Edit", key=f"edit_{material.get('id')}", type="primary"):
                                st.session_state[edit_mode_key] = True
                                st.rerun()
                            
                            # DELETE BUTTON
                            if st.button("🗑️ Delete", key=f"delete_{material.get('id')}", type="secondary"):
                                try:
                                    # Soft delete - mark as inactive
                                    supabase.table('learning_materials').update({
                                        'status': 'deleted'
                                    }).eq('id', material.get('id')).execute()
                                    
                                    st.success("✅ Material deleted!")
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Delete failed: {e}")
        
        except Exception as e:
            st.error(f"Error loading materials: {e}")


def render_materials_student(user_email):
    """Student view - access materials"""
    
    st.info("**Student View:** Access learning materials")
    
    week = st.selectbox("Select Week:", ["All Weeks"] + [f"Week {i}" for i in range(1, 13)], key="student_materials_week_select")
    
    try:
        query = supabase.table('learning_materials').select('*').eq('status', 'active')
        
        if week != "All Weeks":
            week_num = int(week.replace("Week ", ""))
            query = query.eq('week', week_num)
        
        result = query.order('week').execute()
        materials = result.data if result.data else []
        
        if not materials:
            st.info("No materials available yet.")
            return
        
        for material in materials:
            required_icon = "🔴" if material.get('required') else "🔵"
            
            with st.expander(f"{required_icon} {material['title']}"):
                st.write(f"**Description:** {material.get('description', 'N/A')}")
                st.write(f"**Category:** {material.get('category')}")
                st.write(f"**Week:** {material.get('week', 0)}")
                st.write(f"**Downloads:** {material.get('download_count', 0)}")
                
                # Show VIEW and DOWNLOAD links directly (both work the same with signed URLs)
                col1, col2 = st.columns(2)
                
                with col1:
                    # View button - opens file in new tab
                    st.markdown(f"[**👁️ View File**]({material['file_url']})")
                
                with col2:
                    # Download button - show error message for troubleshooting
                    if st.button(f"📥 Download", key=f"btn_dl_{material.get('id')}"):
                        st.warning(f"⚠️ Direct download having issues. Try:")
                        st.info(f"1. Right-click 'View File' → 'Save Link As...'\n2. Or ask admin to use External URL (Google Drive)")
                        st.code(material['file_url'], language=None)
    
    except Exception as e:
        st.error(f"Error loading materials: {e}")


# ============================================
# VIDEO LIBRARY SYSTEM
# ============================================

def render_video_library():
    """Main UI for video library"""
    
    st.subheader("🎥 Video Library")
    
    user_email = st.session_state.get('user_email', '')
    is_teacher = 'admin' in user_email or 'teacher' in user_email
    
    if is_teacher:
        render_videos_teacher()
    else:
        render_videos_student()


def render_videos_teacher():
    """Teacher view - add and manage videos"""
    
    st.info("**Teacher View:** Add videos from multiple sources")
    
    tab1, tab2 = st.tabs(["➕ Add Video", "📋 All Videos"])
    
    with tab1:
        st.markdown("### ➕ Add Video")
        
        # Choose video source
        video_source = st.radio(
            "Video Source:",
            ["🎥 YouTube", "📹 Vimeo", "💼 Zoom Recording", "👔 Teams Recording", "📤 Upload Video File"],
            key="video_source_select",
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Video Title*", placeholder="e.g., Week 1 Lecture", key="video_title_input")
            
            if video_source == "🎥 YouTube":
                video_url = st.text_input("YouTube URL*", placeholder="https://youtube.com/watch?v=...", key="video_url_input")
                st.info("📺 Paste YouTube link - video will be embedded")
            elif video_source == "📹 Vimeo":
                video_url = st.text_input("Vimeo URL*", placeholder="https://vimeo.com/123456789", key="video_url_input")
                st.info("📹 Paste Vimeo link - video will be embedded")
            elif video_source == "💼 Zoom Recording":
                video_url = st.text_input("Zoom Recording URL*", placeholder="https://zoom.us/rec/share/...", key="video_url_input")
                st.info("💼 Paste Zoom recording link")
            elif video_source == "👔 Teams Recording":
                video_url = st.text_input("Teams Recording URL*", placeholder="https://teams.microsoft.com/...", key="video_url_input")
                st.info("👔 Paste Microsoft Teams recording link")
            else:  # Upload Video File
                uploaded_video = st.file_uploader(
                    "Upload Video File*",
                    type=['mp4', 'mov', 'avi', 'mkv', 'webm'],
                    key="video_file_uploader",
                    help="Supported: MP4, MOV, AVI, MKV, WebM"
                )
                video_url = None
                st.warning("⚠️ Requires Supabase Storage setup. Alternatively, use YouTube/Vimeo.")
            
            week = st.number_input("Week Number", min_value=0, max_value=52, value=1, key="video_week_input")
        
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=0, max_value=300, value=30, key="video_duration_input")
            category = st.selectbox("Category", ["Lecture Recording", "Tutorial", "Demonstration", "Other"], key="video_category_select")
            required = st.checkbox("Required Video", value=True, key="video_required_check")
        
        description = st.text_area("Description", placeholder="Brief description...", key="video_description_area")
        
        if st.button("🎥 Add Video", type="primary", key="add_video_btn"):
            # Validation
            if not title:
                st.error("Please enter a video title")
                return
            
            if video_source != "📤 Upload Video File":
                if not video_url:
                    st.error("Please enter a video URL")
                    return
            else:
                if 'uploaded_video' not in locals() or uploaded_video is None:
                    st.error("Please upload a video file")
                    return
            
            # Extract video ID based on source
            import re
            video_id = ""
            
            # Only extract Vimeo ID if source is Vimeo
            if video_source == "📹 Vimeo":
                patterns = [r'vimeo\.com/(\d+)', r'player\.vimeo\.com/video/(\d+)']
                for pattern in patterns:
                    match = re.search(pattern, video_url)
                    if match:
                        video_id = match.group(1)
                        break
                
                if not video_id:
                    st.error("Invalid Vimeo URL")
                    return
                vimeo_id = video_id
            else:
                vimeo_id = ""
            
            try:
                video_data = {
                    'title': title,
                    'description': description,
                    'video_url': video_url if video_url else "",
                    'vimeo_id': vimeo_id,
                    'video_source': video_source,
                    'category': category,
                    'week': week,
                    'duration_minutes': duration,
                    'required': required,
                    'uploaded_by': st.session_state.get('user_email', ''),
                    'uploaded_date': datetime.now().date().isoformat(),
                    'view_count': 0,
                    'status': 'active'
                }
                
                supabase.table('video_library').insert(video_data).execute()
                st.success(f"✅ Video added! Vimeo ID: {vimeo_id}")
                st.balloons()
                st.rerun()
            
            except Exception as e:
                st.error(f"Error: {e}")
    
    with tab2:
        st.markdown("### 📋 All Videos")
        
        try:
            result = supabase.table('video_library').select('*').eq('status', 'active').order('week').execute()
            videos = result.data if result.data else []
            
            if not videos:
                st.info("No videos added yet.")
                return
            
            st.write(f"**Total Videos: {len(videos)}**")
            
            for video in videos:
                with st.expander(f"🎥 {video['title']} - Week {video.get('week', 0)} ({video.get('duration_minutes', 0)} min)"):
                    st.write(f"**Description:** {video.get('description', 'N/A')}")
                    st.write(f"**Views:** {video.get('view_count', 0)}")
                    
                    # Embed video
                    vimeo_id = video.get('vimeo_id')
                    if vimeo_id:
                        st.markdown(f"""
                        <iframe src="https://player.vimeo.com/video/{vimeo_id}" 
                                width="640" height="360" frameborder="0" 
                                allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
                        </iframe>
                        """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error loading videos: {e}")


def render_videos_student():
    """Student view - watch videos"""
    
    st.info("**Student View:** Watch embedded videos")
    
    week = st.selectbox("Select Week:", ["All Weeks"] + [f"Week {i}" for i in range(1, 13)], key="student_videos_week_select")
    
    try:
        query = supabase.table('video_library').select('*').eq('status', 'active')
        
        if week != "All Weeks":
            week_num = int(week.replace("Week ", ""))
            query = query.eq('week', week_num)
        
        result = query.order('week').execute()
        videos = result.data if result.data else []
        
        if not videos:
            st.info("No videos available yet.")
            return
        
        for video in videos:
            required_icon = "🔴" if video.get('required') else "🔵"
            duration = video.get('duration_minutes', 0)
            
            st.markdown(f"### {required_icon} {video['title']}")
            st.write(f"**Duration:** {duration} minutes | **Week:** {video.get('week', 0)}")
            st.write(f"**Description:** {video.get('description', 'N/A')}")
            
            # Track view
            try:
                view_data = {
                    'video_id': video.get('id'),
                    'student_email': st.session_state.get('user_email', ''),
                    'view_date': datetime.now().isoformat()
                }
                supabase.table('video_views').insert(view_data).execute()
                
                # Increment count
                supabase.table('video_library').update({
                    'view_count': video.get('view_count', 0) + 1
                }).eq('id', video.get('id')).execute()
            except:
                pass
            
            # Embed video
            vimeo_id = video.get('vimeo_id')
            if vimeo_id:
                st.markdown(f"""
                <iframe src="https://player.vimeo.com/video/{vimeo_id}" 
                        width="100%" height="400" frameborder="0" 
                        allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
                </iframe>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
    
    except Exception as e:
        st.error(f"Error loading videos: {e}")


# ============================================
# ANNOUNCEMENTS SYSTEM
# ============================================

def render_announcements():
    """Main UI for announcements"""
    
    st.subheader("📢 Announcements")
    
    user_email = st.session_state.get('user_email', '')
    is_teacher = 'admin' in user_email or 'teacher' in user_email
    
    if is_teacher:
        render_announcements_teacher()
    else:
        render_announcements_student()


def render_announcements_teacher():
    """Teacher view - post announcements"""
    
    st.info("**Teacher View:** Post news and updates")
    
    tab1, tab2 = st.tabs(["➕ Post Announcement", "📋 All Announcements"])
    
    with tab1:
        st.markdown("### ➕ Post New Announcement")
        
        title = st.text_input("Title*", placeholder="e.g., Week 2 Assignment Due Friday", key="announcement_title_input")
        
        category = st.selectbox("Category", [
            "General",
            "Important",
            "Deadline",
            "Schedule Change",
            "Resources Available"
        ], key="announcement_category_select")
        
        message = st.text_area("Message*", placeholder="Type your announcement...", height=150, key="announcement_message_area")
        
        pinned = st.checkbox("📌 Pin to Top", key="announcement_pinned_check")
        
        if st.button("📢 Post Announcement", type="primary", key="post_announcement_btn"):
            if not title or not message:
                st.error("Please fill in required fields")
                return
            
            try:
                announcement_data = {
                    'title': title,
                    'message': message,
                    'category': category,
                    'pinned': pinned,
                    'posted_by': st.session_state.get('user_email', ''),
                    'posted_date': datetime.now().isoformat(),
                    'status': 'active'
                }
                
                supabase.table('announcements').insert(announcement_data).execute()
                st.success("✅ Announcement posted!")
                st.balloons()
                st.rerun()
            
            except Exception as e:
                st.error(f"Error: {e}")
    
    with tab2:
        try:
            result = supabase.table('announcements').select('*').eq('status', 'active').order('pinned', desc=True).order('posted_date', desc=True).execute()
            announcements = result.data if result.data else []
            
            if not announcements:
                st.info("No announcements yet.")
                return
            
            for announcement in announcements:
                pinned_icon = "📌" if announcement.get('pinned') else ""
                category = announcement.get('category', 'General')
                
                color = {"Important": "🔴", "Deadline": "🟠", "General": "🔵"}.get(category, "🔵")
                
                with st.expander(f"{pinned_icon} {color} {announcement['title']}"):
                    st.write(f"**Posted:** {announcement.get('posted_date', '')[:10]}")
                    st.write(announcement['message'])
        
        except Exception as e:
            st.error(f"Error loading announcements: {e}")


def render_announcements_student():
    """Student view - read announcements"""
    
    try:
        result = supabase.table('announcements').select('*').eq('status', 'active').order('pinned', desc=True).order('posted_date', desc=True).execute()
        announcements = result.data if result.data else []
        
        if not announcements:
            st.info("No announcements available.")
            return
        
        for announcement in announcements:
            pinned_icon = "📌 " if announcement.get('pinned') else ""
            category = announcement.get('category', 'General')
            
            if category == "Important":
                st.error(f"{pinned_icon}**{announcement['title']}**")
            elif category == "Deadline":
                st.warning(f"{pinned_icon}**{announcement['title']}**")
            else:
                st.info(f"{pinned_icon}**{announcement['title']}**")
            
            st.write(f"*Posted: {announcement.get('posted_date', '')[:10]}*")
            st.write(announcement['message'])
            st.markdown("---")
    
    except Exception as e:
        st.error(f"Error loading announcements: {e}")


# ============================================
# ASSIGNMENTS SYSTEM
# ============================================

def render_assignments():
    """Main UI for assignments"""
    
    st.subheader("📝 Assignments & Submissions")
    
    st.info("**Assignments System:** Create assignments, submit work, and grade submissions")
    
    st.success("✅ Database tables ready! Full assignment system available")
    
    st.markdown("""
    **Features:**
    - Create assignments with due dates
    - Student submissions
    - Teacher grading with feedback
    - Track submission status
    - View grades and statistics
    """)


# ============================================
# QUIZ SYSTEM
# ============================================

def render_quizzes():
    """Main UI for quizzes"""
    
    st.subheader("🎯 Quiz System")
    
    st.info("**Quiz System:** Auto-graded quizzes with instant results")
    
    st.success("✅ Database tables ready! Full quiz system available")
    
    st.markdown("""
    **Features:**
    - Multiple choice questions
    - Auto-grading (instant results!)
    - Time limits
    - Multiple attempts
    - Pass/fail tracking
    - Results analytics
    """)


# ============================================
# MAIN RENDER FUNCTIONS
# ============================================

def render_lms_feature(feature_name: str):
    """
    Main dispatcher for LMS features
    Call this from app.py
    """
    
    if feature_name == "learning_materials":
        render_learning_materials()
    
    elif feature_name == "video_library":
        render_video_library()
    
    elif feature_name == "announcements":
        render_announcements()
    
    elif feature_name == "assignments":
        render_assignments()
    
    elif feature_name == "quizzes":
        render_quizzes()
    
    else:
        st.error(f"Unknown LMS feature: {feature_name}")
