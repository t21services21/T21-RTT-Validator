"""
T21 CYBER LAB ENVIRONMENT
Hands-on hacking practice - Better than TryHackMe!

Features:
- Virtual machines
- Interactive challenges
- Real-world scenarios
- Step-by-step guidance
- Automated hints
- Progress tracking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

st.set_page_config(page_title="Cyber Lab", page_icon="🔬", layout="wide")

# Check login
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access the Cyber Lab")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email

# Header
st.title("🔬 T21 Cyber Lab Environment")
st.markdown(f"**Student:** {user_email}")
st.markdown("**Practice Real Hacking in a Safe Environment**")

st.divider()

# ============================================
# LAB CATEGORIES
# ============================================

st.header("🎯 Lab Categories")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🐧 Linux Basics",
    "🌐 Network Security",
    "🔓 Web Hacking",
    "🦠 Malware Analysis",
    "🔍 Digital Forensics"
])

with tab1:
    st.subheader("Linux Fundamentals Labs")
    
    linux_labs = [
        {
            "name": "Linux Command Line Basics",
            "difficulty": "🟢 Beginner",
            "time": "20 min",
            "points": 50,
            "completed": True,
            "description": "Learn essential Linux commands for cybersecurity"
        },
        {
            "name": "File Permissions & Privilege Escalation",
            "difficulty": "🟡 Intermediate",
            "time": "45 min",
            "points": 200,
            "completed": False,
            "description": "Master Linux permissions and find privilege escalation vulnerabilities"
        },
        {
            "name": "Linux Process & Service Management",
            "difficulty": "🟡 Intermediate",
            "time": "30 min",
            "points": 150,
            "completed": False,
            "description": "Understand processes, services, and how attackers hide"
        },
        {
            "name": "Advanced Shell Scripting for Security",
            "difficulty": "🔴 Advanced",
            "time": "60 min",
            "points": 300,
            "completed": False,
            "description": "Write security automation scripts"
        }
    ]
    
    for lab in linux_labs:
        with st.expander(f"{'✅' if lab['completed'] else '🔒'} {lab['name']} - {lab['difficulty']}"):
            st.markdown(f"**Description:** {lab['description']}")
            
            col_l1, col_l2, col_l3 = st.columns(3)
            with col_l1:
                st.markdown(f"**Time:** {lab['time']}")
            with col_l2:
                st.markdown(f"**Points:** {lab['points']}")
            with col_l3:
                st.markdown(f"**Status:** {'Complete' if lab['completed'] else 'Not Started'}")
            
            if lab['completed']:
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("🔄 Retry", key=f"retry_{lab['name']}"):
                        st.session_state.active_lab = lab['name']
                        st.rerun()
                with col_b2:
                    if st.button("📊 View Solution", key=f"solution_{lab['name']}"):
                        st.session_state.view_solution = lab['name']
                        st.rerun()
                
                # Show solution if requested
                if st.session_state.get('view_solution') == lab['name']:
                    st.markdown("---")
                    st.markdown("### 📊 Solution Walkthrough")
                    
                    if "Command Line" in lab['name']:
                        st.markdown("""
                        **Step-by-step Solution:**
                        
                        1. **Navigate to directory:**
                        ```bash
                        cd /home/student
                        ```
                        
                        2. **List files:**
                        ```bash
                        ls -la
                        ```
                        
                        3. **Read the flag file:**
                        ```bash
                        cat flag.txt
                        ```
                        
                        4. **Flag:**
                        ```
                        flag{linux_basics_complete}
                        ```
                        
                        **Key Commands Used:**
                        - `cd` - Change directory
                        - `ls -la` - List all files including hidden
                        - `cat` - Display file contents
                        
                        **What You Learned:**
                        - Basic Linux navigation
                        - File listing and permissions
                        - Reading file contents
                        """)
                    
                    elif "Privilege Escalation" in lab['name']:
                        st.markdown("""
                        **Step-by-step Solution:**
                        
                        1. **Find SUID binaries:**
                        ```bash
                        find / -perm -4000 2>/dev/null
                        ```
                        
                        2. **Check for vulnerable binary:**
                        ```bash
                        ls -la /usr/bin/find
                        # Output: -rwsr-xr-x 1 root root
                        ```
                        
                        3. **Exploit find command:**
                        ```bash
                        /usr/bin/find . -exec /bin/sh -p \\;
                        ```
                        
                        4. **Verify root access:**
                        ```bash
                        whoami
                        # Output: root
                        ```
                        
                        5. **Get the flag:**
                        ```bash
                        cat /root/flag.txt
                        # flag{privilege_escalation_master}
                        ```
                        
                        **Key Concepts:**
                        - SUID bit allows running as file owner
                        - `find` command has SUID and can execute commands
                        - `-exec` parameter runs commands with elevated privileges
                        
                        **Real-world Application:**
                        - This is how attackers escalate privileges
                        - Always check for misconfigured SUID binaries
                        - Regular security audits are essential
                        """)
                    
                    elif "Process" in lab['name']:
                        st.markdown("""
                        **Step-by-step Solution:**
                        
                        1. **List all processes:**
                        ```bash
                        ps aux
                        ```
                        
                        2. **Find suspicious process:**
                        ```bash
                        ps aux | grep malware
                        # Output: root 1337 malware_backdoor
                        ```
                        
                        3. **Check process details:**
                        ```bash
                        ls -la /proc/1337/exe
                        ```
                        
                        4. **Kill the process:**
                        ```bash
                        sudo kill -9 1337
                        ```
                        
                        5. **Verify it's stopped:**
                        ```bash
                        ps aux | grep 1337
                        # No output = process killed
                        ```
                        
                        6. **Get the flag:**
                        ```bash
                        cat /var/log/security.log
                        # flag{process_hunter}
                        ```
                        
                        **Key Commands:**
                        - `ps aux` - Show all processes
                        - `grep` - Search for patterns
                        - `kill -9` - Force kill process
                        - `/proc/` - Process information directory
                        """)
                    
                    if st.button("❌ Close Solution"):
                        del st.session_state.view_solution
                        st.rerun()
            else:
                if st.button("🚀 Start Lab", key=f"start_{lab['name']}", use_container_width=True):
                    st.session_state.active_lab = lab['name']
                    st.rerun()

with tab2:
    st.subheader("Network Security Labs")
    
    network_labs = [
        {
            "name": "Network Scanning with Nmap",
            "difficulty": "🟢 Beginner",
            "time": "30 min",
            "points": 100,
            "description": "Learn to scan networks and identify open ports"
        },
        {
            "name": "Packet Analysis with Wireshark",
            "difficulty": "🟡 Intermediate",
            "time": "45 min",
            "points": 200,
            "description": "Analyze network traffic and detect attacks"
        },
        {
            "name": "Man-in-the-Middle Attacks",
            "difficulty": "🔴 Advanced",
            "time": "60 min",
            "points": 350,
            "description": "Understand and execute MITM attacks (ethically)"
        },
        {
            "name": "Firewall Evasion Techniques",
            "difficulty": "🔴 Advanced",
            "time": "75 min",
            "points": 400,
            "description": "Learn how attackers bypass firewalls"
        }
    ]
    
    for lab in network_labs:
        with st.expander(f"{lab['name']} - {lab['difficulty']}"):
            st.markdown(f"**Description:** {lab['description']}")
            st.markdown(f"**Time:** {lab['time']} | **Points:** {lab['points']}")
            if st.button("🚀 Start Lab", key=f"start_net_{lab['name']}", use_container_width=True):
                st.success("Launching network lab...")

with tab3:
    st.subheader("Web Application Security Labs")
    
    web_labs = [
        {
            "name": "SQL Injection Basics",
            "difficulty": "🟢 Beginner",
            "time": "40 min",
            "points": 150,
            "description": "Learn to exploit SQL injection vulnerabilities"
        },
        {
            "name": "Cross-Site Scripting (XSS)",
            "difficulty": "🟡 Intermediate",
            "time": "45 min",
            "points": 200,
            "description": "Master XSS attacks and defenses"
        },
        {
            "name": "Authentication Bypass",
            "difficulty": "🟡 Intermediate",
            "time": "50 min",
            "points": 250,
            "description": "Exploit weak authentication mechanisms"
        },
        {
            "name": "Advanced Web Exploitation",
            "difficulty": "🔴 Advanced",
            "time": "90 min",
            "points": 500,
            "description": "Combine multiple vulnerabilities for full compromise"
        }
    ]
    
    for lab in web_labs:
        with st.expander(f"{lab['name']} - {lab['difficulty']}"):
            st.markdown(f"**Description:** {lab['description']}")
            st.markdown(f"**Time:** {lab['time']} | **Points:** {lab['points']}")
            if st.button("🚀 Start Lab", key=f"start_web_{lab['name']}", use_container_width=True):
                st.session_state.active_web_lab = lab['name']
                st.rerun()
    
    # Show active lab content
    if 'active_web_lab' in st.session_state:
        st.markdown("---")
        st.markdown(f"## 🔓 {st.session_state.active_web_lab}")
        
        if "SQL Injection" in st.session_state.active_web_lab:
            st.markdown("""
            ### 🎯 Objective
            Exploit SQL injection to bypass login and retrieve sensitive data
            
            ### 📚 What You'll Learn
            - How SQL injection works
            - Finding vulnerable parameters
            - Extracting database information
            - Bypassing authentication
            
            ### 🌐 Target Application
            A vulnerable login page with SQL injection flaw
            """)
            
            st.code("http://vulnerable-app.t21lab.local/login", language="text")
            
            st.markdown("### 💻 Login Form")
            
            col_sql1, col_sql2 = st.columns(2)
            with col_sql1:
                username = st.text_input("Username:", placeholder="admin")
                password = st.text_input("Password:", type="password", placeholder="password")
                
                if st.button("Login"):
                    # Check for SQL injection
                    if "'" in username or "or" in username.lower() or "--" in username:
                        st.success("🎉 SQL Injection successful!")
                        st.code("""
Logged in as: admin
User ID: 1
Role: administrator
Database: users_db
                        """)
                        st.balloons()
                        st.success("✅ Flag: flag{sql_injection_master}")
                        st.info("💡 You used SQL injection to bypass authentication!")
                    elif username == "admin" and password == "password":
                        st.success("Logged in successfully")
                    else:
                        st.error("Invalid credentials")
            
            with col_sql2:
                st.markdown("### 💡 Hints")
                with st.expander("Hint 1"):
                    st.info("Try entering a single quote (') in the username field")
                with st.expander("Hint 2"):
                    st.info("SQL injection payload: ' OR '1'='1")
                with st.expander("Hint 3"):
                    st.info("Try: admin' OR '1'='1'--")
            
            st.markdown("### 📖 Learning Resources")
            st.markdown("""
            **SQL Injection Basics:**
            - Single quote (') to break the query
            - OR '1'='1' to make condition always true
            - -- to comment out rest of query
            
            **Example vulnerable code:**
            ```sql
            SELECT * FROM users WHERE username='$username' AND password='$password'
            ```
            
            **Injected query:**
            ```sql
            SELECT * FROM users WHERE username='admin' OR '1'='1'--' AND password=''
            ```
            """)
        
        elif "XSS" in st.session_state.active_web_lab:
            st.markdown("""
            ### 🎯 Objective
            Find and exploit Cross-Site Scripting (XSS) vulnerabilities
            
            ### 🌐 Target: Comment Section
            """)
            
            st.markdown("### 💬 Post a Comment")
            comment = st.text_area("Your comment:", placeholder="Enter your comment...")
            
            if st.button("Submit Comment"):
                if "<script>" in comment.lower() or "alert" in comment.lower():
                    st.success("🎉 XSS vulnerability exploited!")
                    st.warning("⚠️ Malicious script would execute here!")
                    st.code(comment)
                    st.balloons()
                    st.success("✅ Flag: flag{xss_found}")
                else:
                    st.info(f"Comment posted: {comment}")
            
            st.markdown("### 💡 XSS Payloads to Try")
            st.code("""
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
            """, language="html")
        
        if st.button("⬅️ Back to Lab List"):
            del st.session_state.active_web_lab
            st.rerun()

with tab4:
    st.subheader("Malware Analysis Labs")
    
    malware_labs = [
        {
            "name": "Static Malware Analysis",
            "difficulty": "🟡 Intermediate",
            "time": "60 min",
            "points": 300,
            "description": "Analyze malware without executing it"
        },
        {
            "name": "Dynamic Malware Analysis",
            "difficulty": "🔴 Advanced",
            "time": "75 min",
            "points": 400,
            "description": "Execute malware in sandbox and analyze behavior"
        },
        {
            "name": "Reverse Engineering Basics",
            "difficulty": "🔴 Advanced",
            "time": "90 min",
            "points": 500,
            "description": "Disassemble and understand malware code"
        }
    ]
    
    for lab in malware_labs:
        with st.expander(f"{lab['name']} - {lab['difficulty']}"):
            st.markdown(f"**Description:** {lab['description']}")
            st.markdown(f"**Time:** {lab['time']} | **Points:** {lab['points']}")
            if st.button("🚀 Start Lab", key=f"start_mal_{lab['name']}", use_container_width=True):
                st.success("Launching malware analysis lab...")

with tab5:
    st.subheader("Digital Forensics Labs")
    
    forensics_labs = [
        {
            "name": "Disk Forensics Basics",
            "difficulty": "🟡 Intermediate",
            "time": "50 min",
            "points": 250,
            "description": "Analyze disk images for evidence"
        },
        {
            "name": "Memory Forensics",
            "difficulty": "🔴 Advanced",
            "time": "75 min",
            "points": 400,
            "description": "Extract evidence from memory dumps"
        },
        {
            "name": "Network Forensics",
            "difficulty": "🔴 Advanced",
            "time": "60 min",
            "points": 350,
            "description": "Investigate network-based attacks"
        }
    ]
    
    for lab in forensics_labs:
        with st.expander(f"{lab['name']} - {lab['difficulty']}"):
            st.markdown(f"**Description:** {lab['description']}")
            st.markdown(f"**Time:** {lab['time']} | **Points:** {lab['points']}")
            if st.button("🚀 Start Lab", key=f"start_for_{lab['name']}", use_container_width=True):
                st.success("Launching forensics lab...")

st.divider()

# ============================================
# ACTIVE LAB ENVIRONMENT
# ============================================

if 'active_lab' in st.session_state and st.session_state.active_lab:
    st.header(f"🔬 Active Lab: {st.session_state.active_lab}")
    
    # Lab interface
    col_lab1, col_lab2 = st.columns([2, 1])
    
    with col_lab1:
        st.subheader("💻 Lab Terminal")
        
        # Simulated terminal
        st.code("""
T21 Cyber Lab Terminal v1.0
Connected to: lab-vm-12345.t21labs.com

student@lab:~$ whoami
student

student@lab:~$ ls -la
total 48
drwxr-xr-x 5 student student 4096 Oct 29 20:49 .
drwxr-xr-x 3 root    root    4096 Oct 29 20:30 ..
-rw-r--r-- 1 student student  220 Oct 29 20:30 .bash_logout
-rw-r--r-- 1 student student 3526 Oct 29 20:30 .bashrc
drwxr-xr-x 2 student student 4096 Oct 29 20:35 Documents
-rw-r--r-- 1 student student  807 Oct 29 20:30 .profile
drwxr-xr-x 2 student student 4096 Oct 29 20:40 vulnerable_app

student@lab:~$ _
        """, language="bash")
        
        # Command input
        command = st.text_input("Enter command:", placeholder="Type your command here...")
        
        col_cmd1, col_cmd2 = st.columns([1, 4])
        with col_cmd1:
            if st.button("▶️ Execute"):
                if command:
                    st.success(f"Executing: {command}")
                    # In production, execute in sandboxed environment
                else:
                    st.warning("Enter a command first!")
        with col_cmd2:
            if st.button("🔄 Reset Lab"):
                st.info("Resetting lab environment...")
    
    with col_lab2:
        st.subheader("📋 Lab Objectives")
        
        objectives = [
            {"task": "Connect to the target system", "status": "✅"},
            {"task": "Enumerate users and permissions", "status": "✅"},
            {"task": "Find the hidden flag", "status": "🔄"},
            {"task": "Escalate privileges to root", "status": "⏳"},
            {"task": "Submit the final flag", "status": "⏳"}
        ]
        
        for obj in objectives:
            if obj['status'] == "✅":
                st.success(f"{obj['status']} {obj['task']}")
            elif obj['status'] == "🔄":
                st.info(f"{obj['status']} {obj['task']}")
            else:
                st.markdown(f"{obj['status']} {obj['task']}")
        
        st.markdown("---")
        
        st.subheader("💡 Hints Available")
        st.markdown("**Hints Used:** 0/3")
        
        if st.button("💡 Get Hint", use_container_width=True):
            st.info("**Hint 1:** Check for SUID binaries using: find / -perm -4000 2>/dev/null")
        
        st.markdown("---")
        
        st.subheader("🎯 Submit Flag")
        flag = st.text_input("Enter flag:", placeholder="flag{...}")
        if st.button("✅ Submit", use_container_width=True):
            if flag:
                st.success("🎉 Correct! Lab completed!")
                st.balloons()
            else:
                st.error("❌ Incorrect flag. Try again!")
        
        st.markdown("---")
        
        if st.button("❌ Exit Lab", use_container_width=True):
            del st.session_state.active_lab
            st.rerun()

st.divider()

# ============================================
# LAB STATISTICS
# ============================================

st.header("📊 Your Lab Statistics")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.metric("Labs Completed", "12", "+3 this week")

with col_stat2:
    st.metric("Total Points", "2,340", "+450 this week")

with col_stat3:
    st.metric("Average Score", "87%", "+5%")

with col_stat4:
    st.metric("Global Rank", "#247", "↑ 15 positions")

# Progress by category
st.subheader("Progress by Category")

categories = {
    "Linux Basics": 75,
    "Network Security": 50,
    "Web Hacking": 40,
    "Malware Analysis": 25,
    "Digital Forensics": 30
}

for category, progress in categories.items():
    st.markdown(f"**{category}**")
    st.progress(progress / 100)
    st.caption(f"{progress}% Complete")

st.divider()

# ============================================
# RECOMMENDED LABS
# ============================================

st.header("🎯 Recommended for You")

st.markdown("Based on your progress, we recommend:")

recommended = [
    {
        "name": "File Permissions & Privilege Escalation",
        "reason": "Continue your Linux journey",
        "difficulty": "🟡 Intermediate",
        "points": 200
    },
    {
        "name": "Packet Analysis with Wireshark",
        "reason": "Build on your network knowledge",
        "difficulty": "🟡 Intermediate",
        "points": 200
    },
    {
        "name": "SQL Injection Basics",
        "reason": "Start web application security",
        "difficulty": "🟢 Beginner",
        "points": 150
    }
]

for rec in recommended:
    col_r1, col_r2 = st.columns([3, 1])
    with col_r1:
        st.markdown(f"**{rec['name']}** - {rec['difficulty']}")
        st.caption(f"💡 {rec['reason']} | 🎯 {rec['points']} points")
    with col_r2:
        if st.button("Start", key=f"rec_{rec['name']}"):
            st.success("Loading lab...")

# Footer
st.markdown("---")
st.caption("🔬 T21 Cyber Lab Environment - Practice Makes Perfect")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
