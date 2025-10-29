"""
T21 SOC ANALYST TRAINING PORTAL
Complete cybersecurity training platform - Better than TryHackMe!

Features:
- Video courses
- Interactive lessons
- Hands-on labs
- Progress tracking
- Certifications
- AI tutor
- Leaderboards
- Achievements
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="SOC Training Portal", page_icon="🎓", layout="wide")

# Check if user is logged in
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access the SOC Training Portal")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email

# Header
st.title("🎓 T21 SOC Analyst Training Portal")
st.markdown(f"**Student:** {user_email}")
st.markdown("**Your Path to Becoming a World-Class SOC Analyst**")

st.divider()

# ============================================
# STUDENT DASHBOARD
# ============================================

st.header("📊 Your Learning Dashboard")

# Simulate student progress (in production, load from database)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 Overall Progress",
        value="35%",
        delta="+5% this week"
    )

with col2:
    st.metric(
        label="⏱️ Hours Learned",
        value="47.5",
        delta="+12.5 this week"
    )

with col3:
    st.metric(
        label="🏆 Challenges Completed",
        value="23/100",
        delta="+5 this week"
    )

with col4:
    st.metric(
        label="🎖️ Certifications",
        value="1/3",
        delta="Foundation earned!"
    )

st.divider()

# ============================================
# LEARNING PATHS
# ============================================

st.header("🛤️ Learning Paths")

tab1, tab2, tab3, tab4 = st.tabs([
    "📚 SOC Analyst Track",
    "🔍 Threat Hunter Track",
    "🚨 Incident Responder Track",
    "🎯 Penetration Tester Track"
])

with tab1:
    st.subheader("SOC Analyst Career Path")
    
    # Progress bar
    progress = 35
    st.progress(progress / 100)
    st.caption(f"{progress}% Complete")
    
    st.markdown("### Level 1: Foundation (8 Weeks)")
    
    modules = [
        {"name": "Introduction to Cybersecurity", "status": "✅ Complete", "time": "4 hours"},
        {"name": "Network Security Basics", "status": "✅ Complete", "time": "6 hours"},
        {"name": "SOC Fundamentals", "status": "🔄 In Progress", "time": "8 hours"},
        {"name": "SIEM Tools & Log Analysis", "status": "🔒 Locked", "time": "10 hours"},
        {"name": "Incident Detection & Response", "status": "🔒 Locked", "time": "8 hours"},
    ]
    
    for module in modules:
        col_mod1, col_mod2, col_mod3 = st.columns([3, 1, 1])
        with col_mod1:
            st.markdown(f"**{module['name']}**")
        with col_mod2:
            st.markdown(module['status'])
        with col_mod3:
            if module['status'] == "🔄 In Progress":
                if st.button("Continue", key=f"continue_{module['name']}"):
                    st.info("Loading module...")
            elif module['status'] == "✅ Complete":
                if st.button("Review", key=f"review_{module['name']}"):
                    st.info("Loading review...")
            else:
                st.button("Locked", key=f"locked_{module['name']}", disabled=True)
    
    st.markdown("### Level 2: Professional (12 Weeks)")
    st.info("🔒 Unlock by completing Level 1")
    
    st.markdown("### Level 3: Expert (16 Weeks)")
    st.info("🔒 Unlock by completing Level 2")

with tab2:
    st.subheader("Threat Hunter Career Path")
    st.info("🔒 Unlock after completing SOC Analyst Level 1")
    
    st.markdown("""
    **What You'll Learn:**
    - Proactive threat hunting
    - Hypothesis-driven investigations
    - Advanced threat detection
    - Hunt methodologies
    - Tools and techniques
    """)

with tab3:
    st.subheader("Incident Responder Career Path")
    st.info("🔒 Unlock after completing SOC Analyst Level 1")
    
    st.markdown("""
    **What You'll Learn:**
    - Incident response lifecycle
    - Forensic investigation
    - Evidence collection
    - Containment strategies
    - Recovery procedures
    """)

with tab4:
    st.subheader("Penetration Tester Career Path")
    st.info("🔒 Unlock after completing SOC Analyst Level 2")
    
    st.markdown("""
    **What You'll Learn:**
    - Ethical hacking
    - Vulnerability assessment
    - Exploitation techniques
    - Report writing
    - Client communication
    """)

st.divider()

# ============================================
# HANDS-ON LABS
# ============================================

st.header("🔬 Hands-On Labs")

col_lab1, col_lab2 = st.columns(2)

with col_lab1:
    st.subheader("🖥️ Active Labs")
    
    labs = [
        {"name": "Linux Fundamentals", "difficulty": "🟢 Beginner", "time": "30 min", "points": "100"},
        {"name": "Network Analysis with Wireshark", "difficulty": "🟡 Intermediate", "time": "45 min", "points": "200"},
        {"name": "SIEM Log Analysis", "difficulty": "🟡 Intermediate", "time": "60 min", "points": "250"},
        {"name": "Malware Analysis Basics", "difficulty": "🔴 Advanced", "time": "90 min", "points": "500"},
    ]
    
    for lab in labs:
        with st.expander(f"{lab['name']} - {lab['difficulty']}"):
            col_l1, col_l2, col_l3 = st.columns(3)
            with col_l1:
                st.markdown(f"**Time:** {lab['time']}")
            with col_l2:
                st.markdown(f"**Points:** {lab['points']}")
            with col_l3:
                if st.button("Start Lab", key=f"start_{lab['name']}"):
                    st.success("🚀 Launching lab environment...")
                    st.info("Lab will open in new window")

with col_lab2:
    st.subheader("🏆 Completed Labs")
    
    completed = [
        {"name": "Introduction to Linux", "score": "95%", "date": "Oct 25, 2025"},
        {"name": "Basic Network Security", "score": "88%", "date": "Oct 22, 2025"},
    ]
    
    if completed:
        for lab in completed:
            st.success(f"✅ {lab['name']} - Score: {lab['score']} ({lab['date']})")
    else:
        st.info("Complete your first lab to see it here!")

st.divider()

# ============================================
# VIDEO COURSES
# ============================================

st.header("📹 Video Courses")

courses = [
    {
        "title": "Introduction to Cybersecurity",
        "instructor": "Dr. Sarah Johnson",
        "duration": "4 hours",
        "videos": 12,
        "progress": 100,
        "thumbnail": "🛡️"
    },
    {
        "title": "Network Security Fundamentals",
        "instructor": "Prof. Michael Chen",
        "duration": "6 hours",
        "videos": 18,
        "progress": 100,
        "thumbnail": "🌐"
    },
    {
        "title": "SOC Operations & Workflows",
        "instructor": "Emily Rodriguez",
        "duration": "8 hours",
        "videos": 24,
        "progress": 45,
        "thumbnail": "🔍"
    },
    {
        "title": "SIEM Tools Mastery",
        "instructor": "James Williams",
        "duration": "10 hours",
        "videos": 30,
        "progress": 0,
        "thumbnail": "📊"
    },
]

col_c1, col_c2 = st.columns(2)

for i, course in enumerate(courses):
    with col_c1 if i % 2 == 0 else col_c2:
        with st.container():
            st.markdown(f"### {course['thumbnail']} {course['title']}")
            st.caption(f"By {course['instructor']}")
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown(f"**Duration:** {course['duration']}")
            with col_info2:
                st.markdown(f"**Videos:** {course['videos']}")
            
            st.progress(course['progress'] / 100)
            st.caption(f"{course['progress']}% Complete")
            
            if course['progress'] == 0:
                if st.button("Start Course", key=f"start_course_{i}"):
                    st.success("🎬 Starting course...")
            elif course['progress'] == 100:
                if st.button("Review Course", key=f"review_course_{i}"):
                    st.info("📚 Loading course...")
            else:
                if st.button("Continue Learning", key=f"continue_course_{i}"):
                    st.success("▶️ Resuming course...")
            
            st.markdown("---")

st.divider()

# ============================================
# CHALLENGES & CTF
# ============================================

st.header("🎯 Challenges & CTF")

challenge_tabs = st.tabs(["🔥 Daily Challenge", "🏆 Weekly CTF", "📈 Leaderboard"])

with challenge_tabs[0]:
    st.subheader("Today's Challenge")
    
    st.markdown("""
    ### 🔍 Suspicious Login Detection
    
    **Difficulty:** 🟡 Intermediate  
    **Points:** 300  
    **Time Limit:** 45 minutes
    
    **Scenario:**
    You're a SOC analyst monitoring login attempts. You've received an alert about 
    suspicious login activity. Analyze the logs and identify the attack pattern.
    
    **Objectives:**
    1. Identify the attack type
    2. Find the attacker's IP address
    3. Determine compromised accounts
    4. Recommend mitigation steps
    """)
    
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        if st.button("🚀 Start Challenge", use_container_width=True):
            st.success("Loading challenge environment...")
    with col_ch2:
        if st.button("💡 Get Hint", use_container_width=True):
            st.info("Hint: Look for failed login attempts from the same IP")

with challenge_tabs[1]:
    st.subheader("This Week's CTF Competition")
    
    st.markdown("""
    ### 🏆 Corporate Network Breach
    
    **Duration:** 7 days (Ends Nov 5, 2025)  
    **Prize:** £500 + Premium Certification  
    **Participants:** 247 students
    
    **Description:**
    A corporate network has been breached. Your team must investigate the incident,
    identify the attack vector, and secure the environment.
    
    **Flags to Capture:** 10  
    **Your Progress:** 3/10 flags captured
    """)
    
    st.progress(3 / 10)
    
    if st.button("🎮 Join CTF", use_container_width=True):
        st.success("Joining CTF competition...")

with challenge_tabs[2]:
    st.subheader("Global Leaderboard")
    
    leaderboard = [
        {"rank": 1, "name": "Alex_Hacker", "points": 15420, "country": "🇬🇧 UK"},
        {"rank": 2, "name": "CyberNinja", "points": 14890, "country": "🇺🇸 USA"},
        {"rank": 3, "name": "SecMaster", "points": 14230, "country": "🇩🇪 Germany"},
        {"rank": 4, "name": "ThreatHunter", "points": 13750, "country": "🇨🇦 Canada"},
        {"rank": 5, "name": "You", "points": 2340, "country": "🇬🇧 UK", "highlight": True},
    ]
    
    for entry in leaderboard:
        if entry.get("highlight"):
            st.success(f"**#{entry['rank']} {entry['name']}** - {entry['points']} points - {entry['country']}")
        else:
            st.markdown(f"#{entry['rank']} {entry['name']} - {entry['points']} points - {entry['country']}")

st.divider()

# ============================================
# AI TUTOR
# ============================================

st.header("🤖 AI Tutor - Ask Anything!")

st.markdown("Get instant help with any cybersecurity question!")

question = st.text_area(
    "Ask your question:",
    placeholder="e.g., What is a SIEM and how does it work?",
    height=100
)

if st.button("🚀 Get Answer", use_container_width=True):
    if question:
        with st.spinner("AI Tutor is thinking..."):
            # In production, integrate with OpenAI API
            st.success("**AI Tutor Response:**")
            st.markdown("""
            A SIEM (Security Information and Event Management) is a comprehensive security solution that:
            
            1. **Collects** security data from multiple sources (firewalls, servers, endpoints)
            2. **Aggregates** and normalizes the data
            3. **Analyzes** events in real-time
            4. **Correlates** events to detect threats
            5. **Alerts** security teams about incidents
            6. **Stores** logs for compliance and investigation
            
            Popular SIEM tools include Splunk, IBM QRadar, and Microsoft Sentinel.
            
            **Want to learn more?** Check out the "SIEM Tools Mastery" course above!
            """)
    else:
        st.warning("Please enter a question!")

st.divider()

# ============================================
# CERTIFICATIONS
# ============================================

st.header("🎖️ Certifications")

cert_col1, cert_col2, cert_col3 = st.columns(3)

with cert_col1:
    st.markdown("### 🥉 Foundation")
    st.markdown("**Status:** ✅ Earned")
    st.markdown("**Date:** Oct 20, 2025")
    st.markdown("**Score:** 87%")
    if st.button("📄 View Certificate", key="cert1"):
        st.success("Downloading certificate...")

with cert_col2:
    st.markdown("### 🥈 Professional")
    st.markdown("**Status:** 🔒 Locked")
    st.markdown("**Requirements:**")
    st.markdown("- Complete Level 2")
    st.markdown("- Pass exam (70%+)")
    st.info("Complete 15 more modules to unlock")

with cert_col3:
    st.markdown("### 🥇 Expert")
    st.markdown("**Status:** 🔒 Locked")
    st.markdown("**Requirements:**")
    st.markdown("- Complete Level 3")
    st.markdown("- Pass exam (80%+)")
    st.info("Complete 35 more modules to unlock")

st.divider()

# ============================================
# ACHIEVEMENTS
# ============================================

st.header("🏅 Achievements")

achievements = [
    {"name": "First Steps", "desc": "Complete your first module", "icon": "👣", "earned": True},
    {"name": "Lab Rat", "desc": "Complete 10 hands-on labs", "icon": "🔬", "earned": True},
    {"name": "Speed Learner", "desc": "Complete 5 modules in one week", "icon": "⚡", "earned": True},
    {"name": "CTF Champion", "desc": "Win a CTF competition", "icon": "🏆", "earned": False},
    {"name": "Certified Pro", "desc": "Earn Professional certification", "icon": "🎖️", "earned": False},
    {"name": "Master Hacker", "desc": "Complete all advanced labs", "icon": "💻", "earned": False},
]

col_ach1, col_ach2, col_ach3 = st.columns(3)

for i, ach in enumerate(achievements):
    with [col_ach1, col_ach2, col_ach3][i % 3]:
        if ach['earned']:
            st.success(f"{ach['icon']} **{ach['name']}**")
            st.caption(ach['desc'])
        else:
            st.info(f"🔒 **{ach['name']}**")
            st.caption(ach['desc'])

st.divider()

# ============================================
# STUDY GROUPS
# ============================================

st.header("👥 Study Groups")

st.markdown("Join study groups to learn with peers!")

groups = [
    {"name": "SOC Beginners", "members": 45, "active": "Online now"},
    {"name": "SIEM Masters", "members": 23, "active": "3 online"},
    {"name": "CTF Warriors", "members": 67, "active": "12 online"},
]

for group in groups:
    col_g1, col_g2, col_g3 = st.columns([2, 1, 1])
    with col_g1:
        st.markdown(f"**{group['name']}**")
    with col_g2:
        st.markdown(f"👥 {group['members']} members")
    with col_g3:
        if st.button("Join", key=f"join_{group['name']}"):
            st.success(f"Joined {group['name']}!")

# Footer
st.markdown("---")
st.caption("🎓 T21 SOC Analyst Training Portal - Your Path to Cybersecurity Excellence")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
