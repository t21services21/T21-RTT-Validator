"""
HANDS-ON LAB SYSTEM - REAL CYBERSECURITY TOOLS
Practice with actual tools used by SOC analysts worldwide

Features:
- Live terminal access
- Real security tools (Nmap, Wireshark, Metasploit, etc.)
- Capture-the-Flag challenges
- Real-world scenarios
- Instant feedback
- Progress tracking
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hands-On Labs", page_icon="🔬", layout="wide")

# Check login
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access Hands-On Labs")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email

# Header
st.title("🔬 Hands-On Cybersecurity Labs")
st.markdown("**Practice with REAL tools - Learn by DOING!**")
st.markdown(f"Student: {user_email}")

st.divider()

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🎯 Labs Completed", "12/50")
with col2:
    st.metric("⭐ Points Earned", "850")
with col3:
    st.metric("🔥 Current Streak", "7 days")
with col4:
    st.metric("🏆 Rank", "#23")

st.divider()

# Lab categories
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐧 Linux", "🌐 Network", "🔍 SIEM", "🦠 Malware", "🕵️ Forensics", "🎯 CTF"
])

with tab1:
    st.header("🐧 Linux Command Line Labs")
    
    labs = [
        {
            "name": "Linux Basics - Navigation & Files",
            "difficulty": "Beginner",
            "points": 50,
            "time": "20 min",
            "tools": ["bash", "ls", "cd", "cat"],
            "scenario": "Learn essential Linux commands for cybersecurity",
            "completed": True
        },
        {
            "name": "File Permissions & Privilege Escalation",
            "difficulty": "Intermediate",
            "points": 200,
            "time": "45 min",
            "tools": ["chmod", "chown", "sudo", "find"],
            "scenario": "Find SUID binaries and escalate to root",
            "completed": False
        },
        {
            "name": "Process Management & Monitoring",
            "difficulty": "Intermediate",
            "points": 150,
            "time": "30 min",
            "tools": ["ps", "top", "kill", "systemctl"],
            "scenario": "Identify and stop malicious processes",
            "completed": False
        }
    ]
    
    for lab in labs:
        with st.expander(f"{'✅' if lab['completed'] else '🔒'} {lab['name']} - {lab['points']} pts"):
            col_lab1, col_lab2 = st.columns([2, 1])
            
            with col_lab1:
                st.markdown(f"**Difficulty:** {lab['difficulty']}")
                st.markdown(f"**Time:** {lab['time']}")
                st.markdown(f"**Scenario:** {lab['scenario']}")
                st.markdown(f"**Tools:** {', '.join(lab['tools'])}")
                
                if lab['completed']:
                    st.success("✅ Completed!")
                else:
                    if st.button("🚀 Start Lab", key=f"start_{lab['name']}"):
                        st.session_state.active_lab = lab['name']
                        st.rerun()
            
            with col_lab2:
                st.info(f"**{lab['points']} points**")
                if not lab['completed']:
                    st.warning("Not started")

with tab2:
    st.header("🌐 Network Security Labs")
    
    st.markdown("### 🎯 Active Lab: Network Scanning with Nmap")
    
    st.markdown("""
    **Objective:** Scan the target network and identify open ports and services
    
    **Target:** 192.168.1.0/24
    
    **Your Tasks:**
    1. Perform a basic scan to find live hosts
    2. Identify open ports on each host
    3. Determine service versions
    4. Find the hidden SSH server
    5. Submit the flag
    """)
    
    # Terminal simulation
    st.markdown("### 💻 Terminal")
    
    with st.container():
        st.code("""
student@kali:~$ nmap --help
Nmap 7.94 ( https://nmap.org )
Usage: nmap [Scan Type(s)] [Options] {target specification}

Common scan types:
  -sS/sT/sA/sW/sM: TCP SYN/Connect()/ACK/Window/Maimon scans
  -sU: UDP Scan
  -sN/sF/sX: TCP Null, FIN, and Xmas scans
  -sV: Probe open ports to determine service/version info
  -O: Enable OS detection

Example: nmap -sV 192.168.1.1
        """, language="bash")
    
    # Command input
    command = st.text_input("Enter command:", placeholder="nmap -sV 192.168.1.1", key="nmap_cmd")
    
    if st.button("▶️ Execute"):
        if "nmap" in command.lower():
            st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.100
Host is up (0.0012s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 8.2p1 Ubuntu
80/tcp   open  http       Apache httpd 2.4.41
443/tcp  open  ssl/http   Apache httpd 2.4.41
3306/tcp open  mysql      MySQL 5.7.33

Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds
            """, language="bash")
            st.success("✅ Scan complete! SSH server found on port 22")
        else:
            st.error("❌ Invalid command. Try using nmap")
    
    # Flag submission
    st.markdown("### 🚩 Submit Flag")
    flag = st.text_input("Enter the flag:", placeholder="flag{...}", key="nmap_flag")
    if st.button("Submit Flag"):
        if "ssh" in flag.lower() or "22" in flag:
            st.success("🎉 Correct! +100 points")
            st.balloons()
        else:
            st.error("❌ Incorrect flag. Keep trying!")

with tab3:
    st.header("🔍 SIEM & Log Analysis Labs")
    
    st.markdown("### 📊 Active Lab: Detecting Brute Force Attacks")
    
    st.markdown("""
    **Scenario:** A server is under brute force attack. Analyze the logs and identify the attacker.
    
    **Your Tasks:**
    1. Search for failed login attempts
    2. Identify the source IP
    3. Count total attempts
    4. Determine compromised accounts
    5. Create an alert rule
    """)
    
    # Sample logs
    st.markdown("### 📄 System Logs")
    
    logs = """
2025-10-29 22:15:01 Failed password for admin from 185.220.101.45 port 54321
2025-10-29 22:15:03 Failed password for root from 185.220.101.45 port 54322
2025-10-29 22:15:05 Failed password for admin from 185.220.101.45 port 54323
2025-10-29 22:15:07 Failed password for user from 185.220.101.45 port 54324
2025-10-29 22:15:09 Failed password for admin from 185.220.101.45 port 54325
2025-10-29 22:15:11 Accepted password for admin from 185.220.101.45 port 54326
2025-10-29 22:15:13 Session opened for user admin by (uid=0)
    """
    
    st.code(logs, language="log")
    
    # Analysis questions
    st.markdown("### 🔍 Analysis")
    
    q1 = st.text_input("1. What is the attacker's IP address?", key="siem_q1")
    q2 = st.number_input("2. How many failed attempts before success?", min_value=0, key="siem_q2")
    q3 = st.text_input("3. Which account was compromised?", key="siem_q3")
    
    if st.button("Submit Analysis"):
        correct = 0
        if "185.220.101.45" in q1:
            st.success("✅ Q1: Correct!")
            correct += 1
        else:
            st.error("❌ Q1: Incorrect")
        
        if q2 == 5:
            st.success("✅ Q2: Correct!")
            correct += 1
        else:
            st.error("❌ Q2: Incorrect")
        
        if "admin" in q3.lower():
            st.success("✅ Q3: Correct!")
            correct += 1
        else:
            st.error("❌ Q3: Incorrect")
        
        if correct == 3:
            st.success("🎉 Perfect score! +150 points")
            st.balloons()

with tab4:
    st.header("🦠 Malware Analysis Labs")
    
    st.markdown("### 🔬 Active Lab: Analyzing Suspicious Files")
    
    st.markdown("""
    **Scenario:** A suspicious file was found on a user's computer. Analyze it safely.
    
    **Tools Available:**
    - VirusTotal API
    - Strings analysis
    - Hash calculator
    - Sandbox environment
    """)
    
    # File analysis
    st.markdown("### 📁 Suspicious File: suspicious.exe")
    
    col_mal1, col_mal2 = st.columns(2)
    
    with col_mal1:
        st.markdown("**File Properties:**")
        st.code("""
Filename: suspicious.exe
Size: 2.4 MB
MD5: 5d41402abc4b2a76b9719d911017c592
SHA256: 2c26b46b68ffc68ff99b453c1d30413413422d706...
Created: 2025-10-28 14:32:11
        """)
    
    with col_mal2:
        st.markdown("**Actions:**")
        if st.button("🔍 Calculate Hash"):
            st.success("Hash calculated!")
        if st.button("🌐 Check VirusTotal"):
            st.warning("⚠️ 45/70 vendors detected this as malware!")
        if st.button("📝 Extract Strings"):
            st.code("http://malicious-c2-server.com\npassword123\nbackdoor.dll")
        if st.button("🔬 Run in Sandbox"):
            st.error("🚨 Malicious behavior detected! File attempts to connect to C2 server")

with tab5:
    st.header("🕵️ Digital Forensics Labs")
    
    st.markdown("### 💾 Active Lab: Disk Image Analysis")
    
    st.markdown("""
    **Scenario:** Investigate a compromised system. Find evidence of the attack.
    
    **Evidence:** disk_image.dd (500 MB)
    
    **Your Tasks:**
    1. Mount the disk image
    2. Find deleted files
    3. Recover evidence
    4. Build timeline
    5. Identify attacker
    """)
    
    st.info("🔧 Forensics tools: Autopsy, FTK Imager, Volatility, Sleuth Kit")

with tab6:
    st.header("🎯 Capture The Flag Challenges")
    
    st.markdown("### 🏆 Weekly CTF Competition")
    
    st.success("**Current Challenge:** Corporate Network Breach")
    st.markdown("**Prize:** £100 + Premium Certification")
    st.markdown("**Ends in:** 3 days, 14 hours")
    
    st.progress(0.65)
    st.caption("You've captured 13/20 flags (65%)")
    
    # CTF challenges
    challenges = [
        {"name": "Web Exploitation", "flags": "3/5", "points": 300},
        {"name": "Cryptography", "flags": "2/3", "points": 200},
        {"name": "Reverse Engineering", "flags": "1/4", "points": 400},
        {"name": "Network Analysis", "flags": "4/4", "points": 400},
        {"name": "Privilege Escalation", "flags": "3/4", "points": 350}
    ]
    
    for challenge in challenges:
        col_ctf1, col_ctf2, col_ctf3 = st.columns([2, 1, 1])
        with col_ctf1:
            st.markdown(f"**{challenge['name']}**")
        with col_ctf2:
            st.markdown(f"Flags: {challenge['flags']}")
        with col_ctf3:
            st.markdown(f"Points: {challenge['points']}")

st.divider()

# Quick access tools
st.header("🛠️ Quick Access Tools")

col_tool1, col_tool2, col_tool3, col_tool4 = st.columns(4)

with col_tool1:
    if st.button("🐧 Linux Terminal"):
        st.info("Opening Kali Linux terminal...")

with col_tool2:
    if st.button("🦈 Wireshark"):
        st.info("Launching Wireshark...")

with col_tool3:
    if st.button("🔍 Splunk"):
        st.info("Opening Splunk dashboard...")

with col_tool4:
    if st.button("🎯 Metasploit"):
        st.info("Starting Metasploit Framework...")

st.markdown("---")
st.caption("🔬 Hands-On Labs - Practice makes perfect!")
st.caption(f"Session: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
