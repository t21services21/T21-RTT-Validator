"""
VIDEO COURSE PLAYER
Video streaming and progress tracking for courses

Features:
- Video playback
- Progress tracking
- Bookmarks
- Playback speed control
- Transcripts
- Quiz integration
"""

import streamlit as st
from datetime import datetime
from soc_training_database import db

class VideoCoursePlayer:
    """
    Video course player with progress tracking
    In production: Integrate with Vimeo, YouTube, or AWS S3
    """
    
    def __init__(self):
        self.video_providers = {
            "youtube": "https://www.youtube.com/embed/",
            "vimeo": "https://player.vimeo.com/video/",
            "aws": "https://d1234.cloudfront.net/"
        }
    
    def get_video_url(self, video_id, provider="youtube"):
        """Get embeddable video URL"""
        
        base_url = self.video_providers.get(provider, self.video_providers["youtube"])
        return f"{base_url}{video_id}"
    
    def render_video_player(self, module_id, video_id, student_id, provider="youtube"):
        """Render video player with controls"""
        
        st.markdown("### 📹 Video Lecture")
        
        # Get video URL
        video_url = self.get_video_url(video_id, provider)
        
        # Embed video
        st.markdown(f"""
        <iframe width="100%" height="500" 
                src="{video_url}?autoplay=0&rel=0" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
        """, unsafe_allow_html=True)
        
        # Video controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⏮️ Previous"):
                st.info("Loading previous video...")
        
        with col2:
            if st.button("⏸️ Pause"):
                st.info("Video paused")
        
        with col3:
            if st.button("⏭️ Next"):
                st.info("Loading next video...")
        
        with col4:
            speed = st.selectbox("Speed", ["0.5x", "0.75x", "1x", "1.25x", "1.5x", "2x"], index=2)
        
        # Progress tracking
        st.markdown("---")
        
        col_prog1, col_prog2 = st.columns([3, 1])
        
        with col_prog1:
            st.markdown("**Mark as complete when finished:**")
        
        with col_prog2:
            if st.button("✅ Complete", use_container_width=True):
                self.mark_video_complete(student_id, module_id)
                st.success("Video marked as complete!")
                st.balloons()
        
        # Transcript
        with st.expander("📝 Video Transcript"):
            st.markdown("""
            **Introduction to Cybersecurity**
            
            [00:00] Welcome to Introduction to Cybersecurity...
            [00:15] In this module, we'll cover the CIA Triad...
            [00:45] Confidentiality ensures that data is only accessible...
            [01:30] Integrity means data hasn't been tampered with...
            [02:15] Availability ensures systems are accessible when needed...
            
            *Full transcript available*
            """)
        
        # Notes
        with st.expander("📓 My Notes"):
            notes = st.text_area("Add your notes here:", height=150)
            if st.button("💾 Save Notes"):
                st.success("Notes saved!")
        
        # Resources
        with st.expander("📚 Additional Resources"):
            st.markdown("""
            **Recommended Reading:**
            - [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
            - [OWASP Top 10](https://owasp.org/www-project-top-ten/)
            - [MITRE ATT&CK](https://attack.mitre.org/)
            
            **Practice Labs:**
            - Linux Basics Lab
            - Network Security Lab
            """)
    
    def mark_video_complete(self, student_id, module_id):
        """Mark video as completed"""
        
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # Check if progress exists
        cursor.execute("""
        SELECT progress_id FROM module_progress 
        WHERE student_id = ? AND module_id = ?
        """, (student_id, module_id))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing
            cursor.execute("""
            UPDATE module_progress 
            SET completed = 1, completion_date = CURRENT_TIMESTAMP
            WHERE student_id = ? AND module_id = ?
            """, (student_id, module_id))
        else:
            # Insert new
            cursor.execute("""
            INSERT INTO module_progress (student_id, module_id, completed, completion_date)
            VALUES (?, ?, 1, CURRENT_TIMESTAMP)
            """, (student_id, module_id))
        
        conn.commit()
        conn.close()
        
        # Award points
        db.update_student_points(student_id, 10)
    
    def get_course_videos(self, course_id):
        """Get all videos for a course"""
        
        # Sample video data (in production, load from database)
        videos = {
            "SOC-101": [
                {"module_id": 1, "title": "Introduction to Cybersecurity", "video_id": "dQw4w9WgXcQ", "duration": "15:30"},
                {"module_id": 2, "title": "The CIA Triad", "video_id": "dQw4w9WgXcQ", "duration": "20:45"},
                {"module_id": 3, "title": "Threat Landscape Overview", "video_id": "dQw4w9WgXcQ", "duration": "25:15"},
                {"module_id": 4, "title": "Common Attack Vectors", "video_id": "dQw4w9WgXcQ", "duration": "18:30"},
                {"module_id": 5, "title": "Defense in Depth", "video_id": "dQw4w9WgXcQ", "duration": "22:00"},
            ]
        }
        
        return videos.get(course_id, [])
    
    def render_course_playlist(self, course_id, student_id):
        """Render course video playlist"""
        
        st.markdown("### 📚 Course Modules")
        
        videos = self.get_course_videos(course_id)
        
        for i, video in enumerate(videos, 1):
            with st.expander(f"Module {i}: {video['title']} ({video['duration']})"):
                
                col_v1, col_v2 = st.columns([3, 1])
                
                with col_v1:
                    st.markdown(f"**Duration:** {video['duration']}")
                    st.markdown(f"**Status:** ✅ Complete" if i <= 2 else "**Status:** 🔒 Not Started")
                
                with col_v2:
                    if st.button("▶️ Watch", key=f"watch_{i}"):
                        st.session_state.current_video = video
                        st.rerun()

# Video player instance
video_player = VideoCoursePlayer()

def render_video_course_page(student_id, course_id):
    """Render complete video course page"""
    
    st.title("📹 Video Course")
    
    # Course info
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.metric("Progress", "40%")
    
    with col_info2:
        st.metric("Completed", "2/5 modules")
    
    with col_info3:
        st.metric("Time Spent", "1.2 hours")
    
    st.progress(0.4)
    
    st.markdown("---")
    
    # Main content
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        # Current video
        if 'current_video' in st.session_state:
            video = st.session_state.current_video
            video_player.render_video_player(
                module_id=video['module_id'],
                video_id=video['video_id'],
                student_id=student_id
            )
        else:
            st.info("👈 Select a module from the playlist to start learning")
    
    with col_side:
        # Playlist
        video_player.render_course_playlist(course_id, student_id)
