"""
ANNOUNCEMENTS SYSTEM
Post news and updates for students

Features:
- Post announcements
- Categorize (General, Important, Deadline, etc.)
- Pin important announcements
- Student view of all announcements
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List
from supabase_client import get_supabase_client
import json
import os


def create_announcement(
    title: str,
    message: str,
    category: str = "General",
    pinned: bool = False,
    visible_to_all: bool = True
) -> Dict:
    """Create a new announcement"""
    
    try:
        supabase = get_supabase_client()
        
        announcement_data = {
            'title': title,
            'message': message,
            'category': category,
            'pinned': pinned,
            'visible_to_all': visible_to_all,
            'posted_by': st.session_state.get('user_email', 'admin@example.com'),
            'posted_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        if supabase:
            result = supabase.table('announcements').insert(announcement_data).execute()
            return {
                'success': True,
                'message': 'Announcement posted successfully',
                'announcement_id': result.data[0].get('id') if result.data else None
            }
        else:
            # Local storage
            announcements_file = 'data/announcements.json'
            os.makedirs('data', exist_ok=True)
            
            if os.path.exists(announcements_file):
                with open(announcements_file, 'r') as f:
                    announcements = json.load(f)
            else:
                announcements = []
            
            announcement_data['id'] = f"ANN-{len(announcements) + 1:05d}"
            announcements.append(announcement_data)
            
            with open(announcements_file, 'w') as f:
                json.dump(announcements, f, indent=2)
            
            return {
                'success': True,
                'message': 'Announcement posted successfully',
                'announcement_id': announcement_data['id']
            }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_all_announcements(category: str = None) -> List[Dict]:
    """Get all active announcements"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            query = supabase.table('announcements').select('*').eq('status', 'active')
            
            if category:
                query = query.eq('category', category)
            
            result = query.order('pinned', desc=True).order('posted_date', desc=True).execute()
            return result.data if result.data else []
        else:
            announcements_file = 'data/announcements.json'
            if os.path.exists(announcements_file):
                with open(announcements_file, 'r') as f:
                    announcements = json.load(f)
                
                # Filter
                if category:
                    announcements = [a for a in announcements if a.get('category') == category]
                
                announcements = [a for a in announcements if a.get('status') == 'active']
                
                # Sort: pinned first, then by date
                announcements.sort(key=lambda x: (not x.get('pinned', False), x.get('posted_date', '')), reverse=True)
                return announcements
            return []
    
    except Exception as e:
        st.error(f"Error getting announcements: {e}")
        return []


def delete_announcement(announcement_id: str) -> Dict:
    """Delete an announcement"""
    
    try:
        supabase = get_supabase_client()
        
        if supabase:
            result = supabase.table('announcements').update({
                'status': 'deleted'
            }).eq('id', announcement_id).execute()
            return {'success': True, 'message': 'Announcement deleted'}
        else:
            announcements_file = 'data/announcements.json'
            if os.path.exists(announcements_file):
                with open(announcements_file, 'r') as f:
                    announcements = json.load(f)
                
                for announcement in announcements:
                    if announcement.get('id') == announcement_id:
                        announcement['status'] = 'deleted'
                
                with open(announcements_file, 'w') as f:
                    json.dump(announcements, f, indent=2)
            
            return {'success': True, 'message': 'Announcement deleted'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_announcements_manager():
    """UI for managing announcements (Teacher view)"""
    
    st.subheader("📢 Announcements Manager")
    
    st.info("Post news, updates, and important information for students")
    
    # Tabs
    tab1, tab2 = st.tabs([
        "➕ Post Announcement",
        "📋 All Announcements"
    ])
    
    with tab1:
        render_post_announcement()
    
    with tab2:
        render_all_announcements_manager()


def render_post_announcement():
    """Post new announcement"""
    
    st.markdown("### ➕ Post New Announcement")
    
    title = st.text_input("Title*", placeholder="e.g., Week 2 Assignment Due Friday")
    
    category = st.selectbox("Category*", [
        "General",
        "Important",
        "Deadline",
        "Schedule Change",
        "Resources Available",
        "Other"
    ])
    
    message = st.text_area(
        "Message*",
        placeholder="Type your announcement message here...",
        height=150
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        pinned = st.checkbox("📌 Pin to Top", help="Pinned announcements appear first")
    
    with col2:
        visible_to_all = st.checkbox("Visible to All Students", value=True)
    
    if st.button("📢 Post Announcement", type="primary"):
        if not title or not message:
            st.error("Please fill in all required fields")
            return
        
        result = create_announcement(
            title=title,
            message=message,
            category=category,
            pinned=pinned,
            visible_to_all=visible_to_all
        )
        
        if result.get('success'):
            st.success(f"✅ {result.get('message')}")
            st.balloons()
            st.rerun()
        else:
            st.error(f"❌ Error: {result.get('error')}")


def render_all_announcements_manager():
    """View all announcements (Manager view)"""
    
    st.markdown("### 📋 All Announcements")
    
    announcements = get_all_announcements()
    
    if not announcements:
        st.info("No announcements posted yet.")
        return
    
    st.write(f"**Total Announcements: {len(announcements)}**")
    
    for announcement in announcements:
        pinned_icon = "📌" if announcement.get('pinned') else ""
        category = announcement.get('category', 'General')
        
        # Category color
        if category == "Important":
            color = "🔴"
        elif category == "Deadline":
            color = "🟠"
        elif category == "Resources Available":
            color = "🟢"
        else:
            color = "🔵"
        
        with st.expander(f"{pinned_icon} {color} {announcement['title']} ({category})"):
            st.write(f"**Posted:** {announcement.get('posted_date', '')[:10]}")
            st.write(f"**Category:** {category}")
            st.markdown("---")
            st.write(announcement['message'])
            st.markdown("---")
            
            if st.button(f"🗑️ Delete", key=f"delete_ann_{announcement.get('id')}"):
                result = delete_announcement(announcement.get('id'))
                if result.get('success'):
                    st.success("Announcement deleted")
                    st.rerun()


def render_student_announcements():
    """Student view of announcements"""
    
    st.subheader("📢 Announcements")
    
    # Category filter
    category_filter = st.selectbox(
        "Filter:",
        ["All", "General", "Important", "Deadline", "Schedule Change", "Resources Available", "Other"]
    )
    
    category = None if category_filter == "All" else category_filter
    
    announcements = get_all_announcements(category=category)
    
    if not announcements:
        st.info("No announcements available.")
        return
    
    # Display announcements
    for announcement in announcements:
        pinned_icon = "📌 " if announcement.get('pinned') else ""
        category = announcement.get('category', 'General')
        
        # Category styling
        if category == "Important":
            st.error(f"{pinned_icon}**{announcement['title']}**")
        elif category == "Deadline":
            st.warning(f"{pinned_icon}**{announcement['title']}**")
        else:
            st.info(f"{pinned_icon}**{announcement['title']}**")
        
        st.write(f"*Posted: {announcement.get('posted_date', '')[:10]} | Category: {category}*")
        st.write(announcement['message'])
        st.markdown("---")
