"""
VIDEO LIBRARY SYSTEM
Manage and display video content (Vimeo integration)

Features:
- Add Vimeo video links
- Organize by week/topic
- Embed videos in student portal
- Track video views
- Required vs optional videos
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List
from supabase_client import get_supabase_client
import json
import os
import re


def extract_vimeo_id(vimeo_url: str) -> str:
    """Extract Vimeo video ID from URL"""
    # Matches various Vimeo URL formats
    patterns = [
        r'vimeo\.com/(\d+)',
        r'player\.vimeo\.com/video/(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, vimeo_url)
        if match:
            return match.group(1)
    
    return ""


def add_video(
    title: str,
    description: str,
    vimeo_url: str,
    category: str,
    week: int = 0,
    duration_minutes: int = 0,
    competency: str = "",
    required: bool = True,
    visible_to_all: bool = True
) -> Dict:
    """Add a video to the library"""
    
    try:
        vimeo_id = extract_vimeo_id(vimeo_url)
        
        if not vimeo_id:
            return {'success': False, 'error': 'Invalid Vimeo URL'}
        
        supabase = get_supabase_client()
        
        video_data = {
            'title': title,
            'description': description,
            'vimeo_url': vimeo_url,
            'vimeo_id': vimeo_id,
            'category': category,
            'week': week,
            'duration_minutes': duration_minutes,
            'competency': competency,
            'required': required,
            'visible_to_all': visible_to_all,
            'uploaded_by': st.session_state.get('user_email', 'admin@example.com'),
            'uploaded_date': datetime.now().date().isoformat(),
            'view_count': 0,
            'status': 'active'
        }
        
        if supabase:
            result = supabase.table('video_library').insert(video_data).execute()
            return {
                'success': True,
                'message': 'Video added successfully',
                'video_id': result.data[0].get('id') if result.data else None
            }
        else:
            # Local storage
            videos_file = 'data/video_library.json'
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(videos_file):
                with open(videos_file, 'r') as f:
                    videos = json.load(f)
            else:
                videos = []
            
            video_data['id'] = f"VID-{len(videos) + 1:05d}"
            videos.append(video_data)
            
            with open(videos_file, 'w') as f:
                json.dump(videos, f, indent=2)
            
            return {
                'success': True,
                'message': 'Video added successfully',
                'video_id': video_data['id']
            }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_all_videos(category: str = None, week: int = None, competency: str = None) -> List[Dict]:
    """Get all videos with filters"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('video_library').select('*').eq('status', 'active')
            
            if category:
                query = query.eq('category', category)
            if week is not None:
                query = query.eq('week', week)
            if competency:
                query = query.eq('competency', competency)
            
            result = query.order('week').order('uploaded_date', desc=True).execute()
            return result.data if result.data else []
        else:
            videos_file = 'data/video_library.json'
            if os.path.exists(videos_file):
                with open(videos_file, 'r') as f:
                    videos = json.load(f)
                
                # Filter
                if category:
                    videos = [v for v in videos if v.get('category') == category]
                if week is not None:
                    videos = [v for v in videos if v.get('week') == week]
                if competency:
                    videos = [v for v in videos if v.get('competency') == competency]
                
                videos = [v for v in videos if v.get('status') == 'active']
                return sorted(videos, key=lambda x: (x.get('week', 0), x.get('uploaded_date', '')))
            return []
    
    except Exception as e:
        st.error(f"Error getting videos: {e}")
        return []


def track_video_view(video_id: str, student_email: str) -> Dict:
    """Track when a student views a video"""
    
    try:
        supabase = get_supabase_client()
        
        view_data = {
            'video_id': video_id,
            'student_email': student_email,
            'view_date': datetime.now().isoformat()
        }
        
        if supabase:
            # Record view
            supabase.table('video_views').insert(view_data).execute()
            
            # Increment view count
            supabase.rpc('increment_video_view_count', {'video_id': video_id}).execute()
            
            return {'success': True}
        else:
            # Local tracking
            views_file = 'data/video_views.json'
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(views_file):
                with open(views_file, 'r') as f:
                    views = json.load(f)
            else:
                views = []
            
            views.append(view_data)
            
            with open(views_file, 'w') as f:
                json.dump(views, f, indent=2)
            
            return {'success': True}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def delete_video(video_id: str) -> Dict:
    """Soft delete a video"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('video_library').update({
                'status': 'deleted',
                'deleted_date': datetime.now().date().isoformat()
            }).eq('id', video_id).execute()
            return {'success': True, 'message': 'Video deleted'}
        else:
            videos_file = 'data/video_library.json'
            if os.path.exists(videos_file):
                with open(videos_file, 'r') as f:
                    videos = json.load(f)
                
                for video in videos:
                    if video.get('id') == video_id:
                        video['status'] = 'deleted'
                        video['deleted_date'] = datetime.now().date().isoformat()
                
                with open(videos_file, 'w') as f:
                    json.dump(videos, f, indent=2)
            
            return {'success': True, 'message': 'Video deleted'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_video_library_manager():
    """UI for managing video library (Teacher view)"""
    
    st.subheader("🎥 Video Library Manager")
    
    st.info("""
    **Manage video content:**
    - Add Vimeo videos (recorded classes, tutorials)
    - Organize by week and topic
    - Track student views
    - Required vs optional videos
    """)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "➕ Add Video",
        "📋 All Videos",
        "📊 View Statistics"
    ])
    
    with tab1:
        render_add_video()
    
    with tab2:
        render_all_videos_manager()
    
    with tab3:
        render_video_stats()


def render_add_video():
    """Add new video"""
    
    st.markdown("### ➕ Add Video to Library")
    
    st.success("**Vimeo Integration:** Paste your Vimeo video URL below. Videos will be embedded for students.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Video Title*", placeholder="e.g., Week 1 - Introduction Lecture")
        category = st.selectbox("Category*", [
            "Lecture Recording",
            "Tutorial",
            "Demonstration",
            "Guest Speaker",
            "Q&A Session",
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
        duration_minutes = st.number_input("Duration (minutes)", min_value=0, max_value=300, value=30)
        required = st.checkbox("Required Video", value=True)
        visible_to_all = st.checkbox("Visible to All Students", value=True)
    
    description = st.text_area("Description*", placeholder="Brief description of what this video covers...")
    
    vimeo_url = st.text_input(
        "Vimeo URL*",
        placeholder="https://vimeo.com/123456789 or https://player.vimeo.com/video/123456789",
        help="Paste the full Vimeo video URL. You can get this from your Vimeo account."
    )
    
    # Preview Vimeo ID extraction
    if vimeo_url:
        vimeo_id = extract_vimeo_id(vimeo_url)
        if vimeo_id:
            st.success(f"✅ Valid Vimeo URL detected! Video ID: {vimeo_id}")
        else:
            st.warning("⚠️ Invalid Vimeo URL format. Please check the URL.")
    
    if st.button("🎥 Add Video", type="primary"):
        if not title or not description or not vimeo_url:
            st.error("Please fill in all required fields")
            return
        
        result = add_video(
            title=title,
            description=description,
            vimeo_url=vimeo_url,
            category=category,
            week=week,
            duration_minutes=duration_minutes,
            competency=competency if competency != "None" else "",
            required=required,
            visible_to_all=visible_to_all
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            st.balloons()
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_all_videos_manager():
    """View all videos (Manager view)"""
    
    st.markdown("### 📋 All Videos")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.selectbox("Filter by Category:", ["All"] + [
            "Lecture Recording", "Tutorial", "Demonstration",
            "Guest Speaker", "Q&A Session", "Other"
        ])
    
    with col2:
        week_filter = st.selectbox("Filter by Week:", ["All"] + [f"Week {i}" for i in range(1, 13)])
    
    # Apply filters
    category = None if category_filter == "All" else category_filter
    week = None if week_filter == "All" else int(week_filter.replace("Week ", ""))
    
    videos = get_all_videos(category=category, week=week)
    
    if not videos:
        st.info("No videos found matching filters.")
        return
    
    st.write(f"**Total Videos: {len(videos)}**")
    
    # Display videos
    for video in videos:
        required_badge = "🔴 Required" if video.get('required') else "🔵 Optional"
        duration = video.get('duration_minutes', 0)
        
        with st.expander(f"🎥 {video['title']} - Week {video.get('week', 0)} ({required_badge}) - {duration} min"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Title:** {video['title']}")
                st.write(f"**Description:** {video['description']}")
                st.write(f"**Category:** {video['category']}")
                if video.get('competency'):
                    st.write(f"**Competency:** {video['competency']}")
            
            with col2:
                st.write(f"**Week:** {video.get('week', 0)}")
                st.write(f"**Duration:** {duration} minutes")
                st.write(f"**Uploaded:** {video.get('uploaded_date')}")
                st.write(f"**Views:** {video.get('view_count', 0)}")
            
            # Embed video preview
            vimeo_id = video.get('vimeo_id')
            if vimeo_id:
                st.markdown(f"""
                <iframe src="https://player.vimeo.com/video/{vimeo_id}?h=0&title=0&byline=0&portrait=0" 
                        width="640" height="360" frameborder="0" 
                        allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
                </iframe>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🔗 Open in Vimeo", key=f"open_{video.get('id')}"):
                    st.markdown(f"[Open Video]({video['vimeo_url']})")
            
            with col2:
                if st.button(f"🗑️ Delete", key=f"delete_{video.get('id')}"):
                    result = delete_video(video.get('id'))
                    if result.get('success'):
                        st.success("Video deleted")
                        st.rerun()


def render_video_stats():
    """Show video view statistics"""
    
    st.markdown("### 📊 Video View Statistics")
    
    videos = get_all_videos()
    
    if not videos:
        st.info("No videos uploaded yet.")
        return
    
    # Sort by view count
    sorted_videos = sorted(videos, key=lambda x: x.get('view_count', 0), reverse=True)
    
    st.markdown("#### Most Viewed Videos")
    
    for i, video in enumerate(sorted_videos[:10], 1):
        views = video.get('view_count', 0)
        duration = video.get('duration_minutes', 0)
        st.write(f"{i}. **{video['title']}** - {views} views ({duration} min)")
    
    # Category breakdown
    st.markdown("---")
    st.markdown("#### Views by Category")
    
    category_views = {}
    for video in videos:
        category = video.get('category', 'Other')
        views = video.get('view_count', 0)
        category_views[category] = category_views.get(category, 0) + views
    
    for category, views in category_views.items():
        st.write(f"**{category}:** {views} views")


def render_student_video_library():
    """Student view of video library"""
    
    st.subheader("🎥 Video Library")
    
    st.info("Watch recorded lectures, tutorials, and demonstrations")
    
    # Week selector
    week = st.selectbox("Select Week:", ["All Weeks"] + [f"Week {i}" for i in range(1, 13)])
    
    week_num = None if week == "All Weeks" else int(week.replace("Week ", ""))
    
    videos = get_all_videos(week=week_num)
    
    if not videos:
        st.info("No videos available for this week.")
        return
    
    # Display videos
    for video in videos:
        required_icon = "🔴" if video.get('required') else "🔵"
        duration = video.get('duration_minutes', 0)
        
        st.markdown(f"### {required_icon} {video['title']}")
        st.write(f"**Duration:** {duration} minutes | **Week:** {video.get('week', 0)} | **Category:** {video.get('category')}")
        st.write(f"**Description:** {video['description']}")
        
        # Embed video
        vimeo_id = video.get('vimeo_id')
        if vimeo_id:
            # Track view when video section is expanded
            student_email = st.session_state.get('user_email', 'student@example.com')
            track_video_view(video.get('id'), student_email)
            
            st.markdown(f"""
            <iframe src="https://player.vimeo.com/video/{vimeo_id}?h=0&title=0&byline=0&portrait=0" 
                    width="100%" height="400" frameborder="0" 
                    allow="autoplay; fullscreen; picture-in-picture" allowfullscreen>
            </iframe>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
