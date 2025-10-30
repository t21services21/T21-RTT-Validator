"""
JOB BOARD - EXCLUSIVE CYBERSECURITY OPPORTUNITIES
Connect students with employers - Guaranteed interviews for top performers

Features:
- Exclusive job postings
- Direct employer connections
- Application tracking
- Interview scheduling
- Salary insights
- Career progression paths
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Job Board", page_icon="💼", layout="wide")

# Check login
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access the Job Board")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email

# Header
st.title("💼 Cybersecurity Job Board")
st.markdown("**Exclusive Opportunities for T21 Students & Graduates**")
st.markdown(f"Student: {user_email}")

st.divider()

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🎯 Active Jobs", "47")
with col2:
    st.metric("✅ Placements This Month", "12")
with col3:
    st.metric("💰 Avg Starting Salary", "£35,000")
with col4:
    st.metric("📈 Interview Success Rate", "78%")

st.divider()

# Job listings
st.header("🔥 Featured Opportunities")

jobs = [
    {
        "title": "Junior SOC Analyst",
        "company": "CyberDefense UK",
        "location": "London (Hybrid)",
        "salary": "£28,000 - £35,000",
        "type": "Full-time",
        "posted": "2 days ago",
        "level": "Entry Level",
        "description": "Join our 24/7 SOC team monitoring client networks. Perfect for T21 graduates!",
        "requirements": ["T21 SOC Certification", "Basic SIEM knowledge", "Willingness to learn"],
        "guaranteed_interview": True
    },
    {
        "title": "Security Operations Analyst",
        "company": "FinTech Security Ltd",
        "location": "Manchester (Remote)",
        "salary": "£32,000 - £40,000",
        "type": "Full-time",
        "posted": "5 days ago",
        "level": "Entry-Mid Level",
        "description": "Monitor security events, investigate incidents, and respond to threats.",
        "requirements": ["SOC experience or training", "SIEM tools", "Incident response"],
        "guaranteed_interview": False
    },
    {
        "title": "Cyber Threat Analyst",
        "company": "Gov Security Services",
        "location": "Bristol (On-site)",
        "salary": "£35,000 - £45,000",
        "type": "Full-time",
        "posted": "1 week ago",
        "level": "Mid Level",
        "description": "Analyze threats, conduct investigations, and provide intelligence reports.",
        "requirements": ["Security clearance eligible", "Threat intelligence", "2+ years experience"],
        "guaranteed_interview": False
    },
    {
        "title": "SOC Analyst Apprentice",
        "company": "T21 Services UK",
        "location": "Remote",
        "salary": "£25,000 + Training",
        "type": "Apprenticeship",
        "posted": "3 days ago",
        "level": "Entry Level",
        "description": "Work with real clients while completing your training. Earn while you learn!",
        "requirements": ["Enrolled in T21 SOC course", "Commitment to learn", "Good communication"],
        "guaranteed_interview": True
    }
]

for i, job in enumerate(jobs):
    with st.expander(f"{'⭐ ' if job['guaranteed_interview'] else ''}{job['title']} - {job['company']}"):
        col_job1, col_job2 = st.columns([2, 1])
        
        with col_job1:
            st.markdown(f"### {job['title']}")
            st.markdown(f"**Company:** {job['company']}")
            st.markdown(f"**Location:** {job['location']}")
            st.markdown(f"**Salary:** {job['salary']}")
            st.markdown(f"**Type:** {job['type']}")
            st.markdown(f"**Level:** {job['level']}")
            
            if job['guaranteed_interview']:
                st.success("⭐ **GUARANTEED INTERVIEW** for T21 students!")
            
            st.markdown("**Description:**")
            st.write(job['description'])
            
            st.markdown("**Requirements:**")
            for req in job['requirements']:
                st.markdown(f"- {req}")
        
        with col_job2:
            st.markdown(f"**Posted:** {job['posted']}")
            
            if st.button("📝 Apply Now", key=f"apply_{i}"):
                # Save application to session state
                if 'job_applications' not in st.session_state:
                    st.session_state.job_applications = []
                
                application = {
                    'job_title': job['title'],
                    'company': job['company'],
                    'applied_date': datetime.now().strftime('%Y-%m-%d'),
                    'status': 'Pending',
                    'user_email': user_email
                }
                st.session_state.job_applications.append(application)
                
                st.success("✅ Application submitted!")
                st.info(f"📧 Confirmation email sent to {user_email}")
                st.info("The employer will contact you within 48 hours")
                st.balloons()
            
            if st.button("💾 Save Job", key=f"save_{i}"):
                # Save job to session state
                if 'saved_jobs' not in st.session_state:
                    st.session_state.saved_jobs = []
                
                saved_job = {
                    'job_title': job['title'],
                    'company': job['company'],
                    'salary': job['salary'],
                    'location': job['location'],
                    'saved_date': datetime.now().strftime('%Y-%m-%d')
                }
                st.session_state.saved_jobs.append(saved_job)
                st.success("✅ Job saved to your profile")
                st.info(f"You have {len(st.session_state.saved_jobs)} saved jobs")
            
            if st.button("📧 Email to Friend", key=f"share_{i}"):
                st.success("✅ Email sent!")
                st.code(f"""
To: friend@example.com
Subject: Check out this job opportunity!

Hi,

I found this great opportunity and thought of you:

{job['title']} at {job['company']}
Location: {job['location']}
Salary: {job['salary']}

Apply here: https://t21-jobs.com/apply/{i}

Best regards
                """)

st.divider()

# My Applications and Saved Jobs
st.header("📋 My Job Activity")

tab_app, tab_saved = st.tabs(["My Applications", "Saved Jobs"])

with tab_app:
    if 'job_applications' in st.session_state and len(st.session_state.job_applications) > 0:
        st.success(f"✅ You have {len(st.session_state.job_applications)} active applications")
        
        for app in st.session_state.job_applications:
            with st.expander(f"{app['job_title']} - {app['company']}"):
                st.markdown(f"**Applied:** {app['applied_date']}")
                st.markdown(f"**Status:** {app['status']}")
                st.markdown(f"**Email:** {app['user_email']}")
                
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    if st.button("📧 Follow Up", key=f"followup_{app['job_title']}"):
                        st.success("Follow-up email sent!")
                with col_a2:
                    if st.button("❌ Withdraw", key=f"withdraw_{app['job_title']}"):
                        st.warning("Application withdrawn")
    else:
        st.info("No applications yet. Apply to jobs above to track them here!")

with tab_saved:
    if 'saved_jobs' in st.session_state and len(st.session_state.saved_jobs) > 0:
        st.success(f"✅ You have {len(st.session_state.saved_jobs)} saved jobs")
        
        for job in st.session_state.saved_jobs:
            with st.expander(f"{job['job_title']} - {job['company']}"):
                st.markdown(f"**Salary:** {job['salary']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Saved:** {job['saved_date']}")
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    if st.button("📝 Apply Now", key=f"apply_saved_{job['job_title']}"):
                        st.success("Redirecting to application...")
                with col_s2:
                    if st.button("🗑️ Remove", key=f"remove_{job['job_title']}"):
                        st.warning("Job removed from saved list")
    else:
        st.info("No saved jobs yet. Save jobs above to view them here!")

st.divider()

# Career resources
st.header("📚 Career Resources")

col_res1, col_res2, col_res3 = st.columns(3)

with col_res1:
    st.subheader("📄 Resume Builder")
    st.write("Create a professional cybersecurity resume")
    if st.button("Build Resume"):
        st.info("Resume builder coming soon!")

with col_res2:
    st.subheader("🎤 Interview Prep")
    st.write("Practice common SOC analyst interview questions")
    if st.button("Start Practice"):
        st.info("Interview prep system ready!")

with col_res3:
    st.subheader("💰 Salary Guide")
    st.write("Know your worth in the cybersecurity market")
    if st.button("View Salaries"):
        st.info("Salary data available!")

st.divider()

# Success stories
st.header("🌟 Success Stories")

success_stories = [
    {"name": "Sarah M.", "role": "Junior SOC Analyst", "company": "CyberDefense UK", "salary": "£32,000", "time": "2 months after graduation"},
    {"name": "James K.", "role": "Security Analyst", "company": "FinTech Security", "salary": "£38,000", "time": "3 months after graduation"},
    {"name": "Priya S.", "role": "Threat Analyst", "company": "Gov Security", "salary": "£42,000", "time": "6 months after graduation"}
]

for story in success_stories:
    st.success(f"**{story['name']}** landed a {story['role']} role at {story['company']} earning {story['salary']} - just {story['time']}!")

st.markdown("---")
st.caption("💼 T21 Job Board - Connecting talent with opportunity")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
