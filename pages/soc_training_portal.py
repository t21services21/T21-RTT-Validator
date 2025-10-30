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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📚 My Courses",
    "🔬 Labs",
    "🎖️ Certifications",
    "🏆 Leaderboard",
    "📊 My Progress"
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
                    st.session_state.current_module = module['name']
                    st.rerun()
            elif module['status'] == "✅ Complete":
                if st.button("Review", key=f"review_{module['name']}"):
                    st.session_state.current_module = module['name']
                    st.rerun()
            else:
                st.button("Locked", key=f"locked_{module['name']}", disabled=True)
    
    # Show module content if selected
    if 'current_module' in st.session_state:
        st.markdown("---")
        st.markdown(f"## 📚 {st.session_state.current_module}")
        
        # Module content (text to read)
        module_content = {
            "Introduction to Cybersecurity": """
            ## 📖 Module Content
            
            ### What is Cybersecurity?
            
            Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. 
            These cyberattacks are usually aimed at accessing, changing, or destroying sensitive information, 
            extorting money from users, or interrupting normal business processes.
            
            ### The CIA Triad
            
            The foundation of cybersecurity is built on three core principles:
            
            **1. Confidentiality**
            - Ensures that information is only accessible to authorized individuals
            - Examples: Encryption, access controls, authentication
            - Real-world: Password protection, data encryption
            
            **2. Integrity**
            - Ensures that information is accurate and hasn't been tampered with
            - Examples: Checksums, digital signatures, version control
            - Real-world: File integrity monitoring, blockchain
            
            **3. Availability**
            - Ensures that information and resources are accessible when needed
            - Examples: Redundancy, backups, DDoS protection
            - Real-world: Load balancing, disaster recovery
            
            ### Common Threats
            
            **Malware:** Malicious software designed to harm or exploit systems
            - Viruses, worms, trojans, ransomware, spyware
            
            **Phishing:** Social engineering attacks to steal credentials
            - Email phishing, spear phishing, whaling
            
            **DDoS Attacks:** Overwhelming systems with traffic
            - Volumetric, protocol, application layer attacks
            
            **Insider Threats:** Threats from within the organization
            - Malicious insiders, negligent employees
            
            ### Defense in Depth
            
            Multiple layers of security controls:
            1. Physical security
            2. Network security
            3. Endpoint security
            4. Application security
            5. Data security
            6. User education
            
            ### Key Takeaways
            
            ✅ Cybersecurity protects against digital threats
            ✅ CIA Triad is the foundation (Confidentiality, Integrity, Availability)
            ✅ Multiple threat types require multiple defenses
            ✅ Defense in depth provides layered protection
            """,
            
            "Network Security Basics": """
            ## 📖 Module Content
            
            ### Network Fundamentals
            
            **TCP/IP Model:**
            - Application Layer (HTTP, FTP, SSH)
            - Transport Layer (TCP, UDP)
            - Internet Layer (IP, ICMP)
            - Network Access Layer (Ethernet, Wi-Fi)
            
            ### Common Ports
            
            | Port | Protocol | Use |
            |------|----------|-----|
            | 21   | FTP      | File Transfer |
            | 22   | SSH      | Secure Shell |
            | 23   | Telnet   | Remote Access (Insecure) |
            | 25   | SMTP     | Email |
            | 53   | DNS      | Domain Name System |
            | 80   | HTTP     | Web Traffic |
            | 443  | HTTPS    | Secure Web Traffic |
            | 3389 | RDP      | Remote Desktop |
            
            ### Firewalls
            
            **Types:**
            - Packet filtering
            - Stateful inspection
            - Application layer
            - Next-generation (NGFW)
            
            **Rules:**
            - Allow/Deny traffic based on:
              - Source IP
              - Destination IP
              - Port numbers
              - Protocols
            
            ### IDS vs IPS
            
            **IDS (Intrusion Detection System):**
            - Monitors network traffic
            - Alerts on suspicious activity
            - Passive monitoring
            
            **IPS (Intrusion Prevention System):**
            - Monitors AND blocks threats
            - Active prevention
            - Can stop attacks in real-time
            
            ### VPNs
            
            **Purpose:**
            - Secure remote access
            - Encrypt traffic
            - Hide IP addresses
            
            **Types:**
            - Site-to-site VPN
            - Remote access VPN
            - SSL/TLS VPN
            
            ### Network Segmentation
            
            **Why segment?**
            - Limit attack spread
            - Improve performance
            - Easier management
            - Compliance requirements
            
            **Methods:**
            - VLANs
            - Subnets
            - DMZ (Demilitarized Zone)
            - Zero Trust Architecture
            
            ### Key Takeaways
            
            ✅ Understand TCP/IP and common ports
            ✅ Firewalls filter traffic based on rules
            ✅ IDS detects, IPS prevents
            ✅ VPNs provide secure remote access
            ✅ Network segmentation limits attack spread
            """,
            
            "SOC Fundamentals": """
            ## 📖 Module Content
            
            ### What is a SOC?
            
            A Security Operations Center (SOC) is a centralized unit that deals with security 
            issues on an organizational and technical level.
            
            **Purpose:**
            - Monitor security events 24/7
            - Detect and respond to threats
            - Investigate incidents
            - Maintain security posture
            
            ### SOC Team Structure
            
            **Tier 1 Analyst (Alert Triage):**
            - Monitor alerts
            - Initial investigation
            - Escalate to Tier 2
            - 80% of SOC work
            
            **Tier 2 Analyst (Incident Response):**
            - Deep investigation
            - Threat hunting
            - Incident response
            - Create playbooks
            
            **Tier 3 Analyst (Threat Hunter):**
            - Advanced threat hunting
            - Malware analysis
            - Threat intelligence
            - Security research
            
            **SOC Manager:**
            - Team leadership
            - Metrics and reporting
            - Process improvement
            - Stakeholder communication
            
            ### SOC Workflow
            
            **1. Detection**
            - SIEM alerts
            - IDS/IPS alerts
            - EDR alerts
            - User reports
            
            **2. Triage**
            - Is it a real threat?
            - What's the severity?
            - Who's affected?
            - What's the impact?
            
            **3. Investigation**
            - Gather evidence
            - Analyze logs
            - Check threat intelligence
            - Determine root cause
            
            **4. Response**
            - Contain the threat
            - Eradicate malware
            - Recover systems
            - Document everything
            
            **5. Reporting**
            - Incident report
            - Lessons learned
            - Metrics and KPIs
            - Executive summary
            
            ### Key Tools
            
            - **SIEM:** Splunk, QRadar, Sentinel
            - **EDR:** CrowdStrike, Carbon Black
            - **Threat Intel:** MISP, ThreatConnect
            - **Ticketing:** ServiceNow, Jira
            - **Analysis:** Wireshark, Volatility
            
            ### Metrics & KPIs
            
            - Mean Time to Detect (MTTD)
            - Mean Time to Respond (MTTR)
            - Number of incidents
            - False positive rate
            - SLA compliance
            
            ### Key Takeaways
            
            ✅ SOC provides 24/7 security monitoring
            ✅ Three tiers of analysts (Triage, Response, Hunter)
            ✅ Standard workflow: Detect → Triage → Investigate → Respond → Report
            ✅ Multiple tools work together
            ✅ Metrics measure effectiveness
            """,
            
            "SIEM Tools & Log Analysis": """
            ## 📖 Module Content
            
            ### What is SIEM?
            
            Security Information and Event Management (SIEM) is a solution that helps organizations 
            detect, analyze, and respond to security threats before they harm business operations.
            
            **Key Functions:**
            - Log collection and aggregation
            - Real-time event correlation
            - Alert generation
            - Compliance reporting
            - Forensic analysis
            
            ### Popular SIEM Platforms
            
            **Splunk**
            - Industry leader
            - Powerful search (SPL)
            - Extensive integrations
            - Expensive but feature-rich
            
            **IBM QRadar**
            - Strong correlation engine
            - AI-powered analytics
            - Good for enterprises
            - Complex but powerful
            
            **Microsoft Sentinel**
            - Cloud-native
            - Azure integration
            - AI and ML built-in
            - Cost-effective
            
            **Elastic (ELK Stack)**
            - Open source option
            - Highly customizable
            - Good for log analysis
            - Requires more setup
            
            ### Log Sources
            
            **Network Devices:**
            - Firewalls
            - Routers and switches
            - IDS/IPS
            - VPN concentrators
            
            **Servers:**
            - Windows Event Logs
            - Linux Syslog
            - Application logs
            - Database logs
            
            **Security Tools:**
            - Antivirus/EDR
            - Web proxies
            - Email gateways
            - DLP systems
            
            **Cloud Services:**
            - AWS CloudTrail
            - Azure Activity Logs
            - Office 365 logs
            - SaaS application logs
            
            ### Log Analysis Techniques
            
            **1. Search and Filter**
            ```
            index=security sourcetype=firewall action=blocked
            | stats count by src_ip
            | sort -count
            ```
            
            **2. Correlation**
            - Connect related events
            - Identify patterns
            - Detect multi-stage attacks
            
            **3. Baseline and Anomaly Detection**
            - Establish normal behavior
            - Alert on deviations
            - Machine learning helps
            
            **4. Threat Intelligence Integration**
            - Check IPs against threat feeds
            - Identify known malicious domains
            - Correlate with IOCs
            
            ### Common Use Cases
            
            **Failed Login Attempts:**
            - Detect brute force attacks
            - Identify compromised accounts
            - Geographic anomalies
            
            **Malware Detection:**
            - Suspicious file downloads
            - Command and control traffic
            - Unusual process execution
            
            **Data Exfiltration:**
            - Large data transfers
            - Unusual destinations
            - After-hours activity
            
            **Insider Threats:**
            - Privilege escalation
            - Access to sensitive data
            - Policy violations
            
            ### Creating Effective Searches
            
            **Best Practices:**
            - Start broad, then narrow
            - Use time ranges wisely
            - Leverage field extractions
            - Save useful searches
            - Create dashboards
            
            **Example Search:**
            ```
            index=windows EventCode=4625
            | stats count by Account_Name, src_ip
            | where count > 5
            ```
            
            ### Dashboards and Alerts
            
            **Dashboard Components:**
            - Real-time metrics
            - Trend charts
            - Top talkers
            - Geographic maps
            - Alert status
            
            **Alert Configuration:**
            - Define trigger conditions
            - Set severity levels
            - Configure notifications
            - Avoid alert fatigue
            
            ### Key Takeaways
            
            ✅ SIEM aggregates and analyzes security logs
            ✅ Multiple log sources provide visibility
            ✅ Correlation detects complex attacks
            ✅ Effective searches require practice
            ✅ Dashboards and alerts enable proactive monitoring
            """,
            
            "Incident Detection & Response": """
            ## 📖 Module Content
            
            ### Incident Response Lifecycle
            
            The NIST Incident Response framework consists of four main phases:
            
            **1. Preparation**
            - Develop IR plan
            - Train IR team
            - Deploy tools
            - Create playbooks
            - Establish communication channels
            
            **2. Detection & Analysis**
            - Monitor alerts
            - Identify incidents
            - Determine scope
            - Assess severity
            - Document findings
            
            **3. Containment, Eradication & Recovery**
            - Contain the threat
            - Remove malware
            - Patch vulnerabilities
            - Restore systems
            - Verify recovery
            
            **4. Post-Incident Activity**
            - Lessons learned
            - Update procedures
            - Improve defenses
            - Report to stakeholders
            
            ### Indicators of Compromise (IOCs)
            
            **Network IOCs:**
            - Suspicious IP addresses
            - Malicious domains
            - Unusual ports
            - C2 traffic patterns
            
            **Host IOCs:**
            - Malicious file hashes
            - Registry modifications
            - Suspicious processes
            - Unauthorized accounts
            
            **Behavioral IOCs:**
            - Unusual login times
            - Lateral movement
            - Data staging
            - Privilege escalation
            
            ### Incident Classification
            
            **Severity Levels:**
            
            **Critical:**
            - Active data breach
            - Ransomware outbreak
            - Critical system compromise
            - Response: Immediate, all hands
            
            **High:**
            - Malware infection
            - Unauthorized access
            - DDoS attack
            - Response: Within 1 hour
            
            **Medium:**
            - Policy violations
            - Suspicious activity
            - Failed attacks
            - Response: Within 4 hours
            
            **Low:**
            - False positives
            - Minor violations
            - Informational alerts
            - Response: Next business day
            
            ### Containment Strategies
            
            **Short-term Containment:**
            - Isolate affected systems
            - Block malicious IPs
            - Disable compromised accounts
            - Preserve evidence
            
            **Long-term Containment:**
            - Apply patches
            - Rebuild systems
            - Implement additional controls
            - Monitor for reinfection
            
            ### Evidence Collection
            
            **What to Collect:**
            - System logs
            - Network traffic captures
            - Memory dumps
            - Disk images
            - Screenshots
            - Timeline of events
            
            **Chain of Custody:**
            - Document who handled evidence
            - When it was collected
            - Where it's stored
            - Any modifications made
            
            ### Incident Response Tools
            
            **Analysis Tools:**
            - Wireshark (network analysis)
            - Volatility (memory forensics)
            - Autopsy (disk forensics)
            - Sysinternals (Windows analysis)
            
            **Response Tools:**
            - EDR platforms
            - SOAR platforms
            - Forensic toolkits
            - Backup/recovery tools
            
            ### Communication During Incidents
            
            **Internal Communication:**
            - IR team coordination
            - Management updates
            - IT team collaboration
            - Regular status meetings
            
            **External Communication:**
            - Law enforcement (if needed)
            - Customers (if affected)
            - Regulators (if required)
            - Media (if necessary)
            
            ### Common Incident Types
            
            **Malware Infections:**
            - Identify patient zero
            - Determine spread
            - Remove malware
            - Prevent reinfection
            
            **Phishing Attacks:**
            - Identify victims
            - Reset credentials
            - Block sender
            - User education
            
            **Data Breaches:**
            - Determine what was accessed
            - Identify how breach occurred
            - Notify affected parties
            - Regulatory reporting
            
            **Insider Threats:**
            - Investigate activity
            - Preserve evidence
            - Coordinate with HR/Legal
            - Implement controls
            
            ### Post-Incident Review
            
            **Questions to Answer:**
            - What happened?
            - How did it happen?
            - What was the impact?
            - What worked well?
            - What needs improvement?
            - How can we prevent recurrence?
            
            **Deliverables:**
            - Incident report
            - Timeline of events
            - Lessons learned document
            - Updated procedures
            - Recommendations
            
            ### Key Takeaways
            
            ✅ Follow the incident response lifecycle
            ✅ Identify and document IOCs
            ✅ Classify incidents by severity
            ✅ Contain quickly, investigate thoroughly
            ✅ Learn from every incident
            ✅ Communication is critical
            ✅ Preparation prevents panic
            """
        }
        
        # Show text content
        content = module_content.get(st.session_state.current_module, "Content coming soon...")
        st.markdown(content)
        
        st.markdown("---")
        
        # Video section
        st.markdown("### 📹 Video Lecture")
        
        # Map modules to real training videos
        video_map = {
            "Introduction to Cybersecurity": "https://www.youtube.com/watch?v=inWWhr5tnEA",
            "Network Security Basics": "https://www.youtube.com/watch?v=qiQR5rTSshw",
            "SOC Fundamentals": "https://www.youtube.com/watch?v=Q7Cn_yJwXWE",
            "SIEM Tools & Log Analysis": "https://www.youtube.com/watch?v=ULGILG-ZhO0",
            "Incident Detection & Response": "https://www.youtube.com/watch?v=M7hfYp7Gs7Y"
        }
        
        video_url = video_map.get(st.session_state.current_module, "https://www.youtube.com/watch?v=inWWhr5tnEA")
        
        st.info("📺 Watch the video lecture to reinforce what you just read!")
        st.warning("🔊 **No sound?** Click the video and press the unmute button (🔇), or click the link below to watch on YouTube directly.")
        
        # Show video
        st.video(video_url)
        
        # Provide direct YouTube link
        col_yt1, col_yt2 = st.columns([3, 1])
        with col_yt1:
            st.markdown(f"**Can't hear audio?** [🎥 Watch on YouTube]({video_url})")
        with col_yt2:
            if st.button("🔗 Open in YouTube"):
                st.markdown(f"[Click here to open]({video_url})")
                st.info("Video will open in a new tab")
        
        col_vid1, col_vid2 = st.columns(2)
        with col_vid1:
            if st.button("✅ Mark Video Complete"):
                st.success("Video marked as complete!")
                st.balloons()
        with col_vid2:
            if st.button("⏭️ Next Video"):
                st.success("✅ Moving to next video!")
                st.info("📹 Next video in the series will load here")
        
        # Quiz section
        st.markdown("### 📝 Module Quiz")
        with st.expander("Take Quiz"):
            st.markdown("**Question 1:** What does CIA stand for in cybersecurity?")
            answer = st.radio("Select answer:", 
                ["Confidentiality, Integrity, Availability", 
                 "Central Intelligence Agency",
                 "Cyber Information Analysis",
                 "Computer Internet Access"])
            if st.button("Submit Answer"):
                # Save quiz result
                if 'quiz_results' not in st.session_state:
                    st.session_state.quiz_results = {}
                
                module_name = st.session_state.current_module
                is_correct = (answer == "Confidentiality, Integrity, Availability")
                
                st.session_state.quiz_results[module_name] = {
                    'answer': answer,
                    'correct': is_correct,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                
                if is_correct:
                    st.success("✅ Correct!")
                    st.balloons()
                    st.info("Quiz result saved to your profile!")
                else:
                    st.error("❌ Incorrect. Try again!")
                    st.info("Hint: Think about the three pillars of information security")
        
        # Lab section
        st.markdown("### 🔬 Hands-On Lab")
        with st.expander("Start Lab"):
            st.info("Lab environment: Linux Command Line Basics")
            st.code("ssh student@lab.t21services.co.uk", language="bash")
            flag_input = st.text_input("Submit Flag:", placeholder="flag{...}")
            if st.button("Submit Flag"):
                # Save lab completion
                if 'lab_completions' not in st.session_state:
                    st.session_state.lab_completions = {}
                
                module_name = st.session_state.current_module
                
                if "linux" in flag_input.lower():
                    st.session_state.lab_completions[module_name] = {
                        'flag': flag_input,
                        'completed': True,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'points': 50
                    }
                    
                    st.success("🎉 Correct flag! Lab completed!")
                    st.success("✅ +50 points earned!")
                    st.info("Lab completion saved to your profile!")
                    st.balloons()
                else:
                    st.error("❌ Incorrect flag")
                    st.info("Hint: The flag contains 'linux'")
        
        # Resources
        st.markdown("### 📚 Additional Resources")
        st.markdown("""
        - [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
        - [OWASP Top 10](https://owasp.org/www-project-top-ten/)
        - [MITRE ATT&CK](https://attack.mitre.org/)
        """)
        
        if st.button("⬅️ Back to Course List"):
            del st.session_state.current_module
            st.rerun()
    
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
                    st.success("🎬 Course started!")
                    st.info(f"📹 {course['videos']} videos available - Start watching now!")
            elif course['progress'] == 100:
                if st.button("Review Course", key=f"review_course_{i}"):
                    st.success("📚 Course materials ready!")
                    st.info("Review all videos and download your certificate")
            else:
                if st.button("Continue Learning", key=f"continue_course_{i}"):
                    st.success("▶️ Continuing where you left off!")
                    st.info(f"Progress: {course['progress']}% - Keep going!")
            
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
            st.success("✅ Challenge environment ready!")
            st.info("🎯 Objective: Analyze the logs and identify the attacker's IP address")
            st.code("ssh student@challenge-server.t21.lab", language="bash")
    with col_ch2:
        if st.button("💡 Get Hint", use_container_width=True):
            st.info("💡 Hint: Look for failed login attempts from the same IP")
            st.caption("Check /var/log/auth.log for suspicious patterns")

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

with tab5:
    st.subheader("📊 My Learning Progress")
    
    # Quiz Results
    st.markdown("### 📝 Quiz Results")
    if 'quiz_results' in st.session_state and len(st.session_state.quiz_results) > 0:
        correct_count = sum(1 for r in st.session_state.quiz_results.values() if r['correct'])
        total_count = len(st.session_state.quiz_results)
        
        st.success(f"✅ {correct_count}/{total_count} quizzes passed ({round(correct_count/total_count*100)}%)")
        
        for module, result in st.session_state.quiz_results.items():
            status = "✅" if result['correct'] else "❌"
            st.markdown(f"{status} **{module}** - {result['date']}")
    else:
        st.info("No quiz results yet. Complete quizzes to track your progress!")
    
    st.divider()
    
    # Lab Completions
    st.markdown("### 🔬 Lab Completions")
    if 'lab_completions' in st.session_state and len(st.session_state.lab_completions) > 0:
        total_points = sum(lab['points'] for lab in st.session_state.lab_completions.values())
        
        st.success(f"✅ {len(st.session_state.lab_completions)} labs completed")
        st.success(f"⭐ {total_points} points earned")
        
        for module, lab in st.session_state.lab_completions.items():
            st.markdown(f"✅ **{module}** - {lab['points']} points - {lab['date']}")
    else:
        st.info("No labs completed yet. Complete labs to earn points!")
    
    st.divider()
    
    # Overall Progress
    st.markdown("### 📈 Overall Statistics")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        quiz_count = len(st.session_state.get('quiz_results', {}))
        st.metric("Quizzes Taken", quiz_count)
    
    with col_stat2:
        lab_count = len(st.session_state.get('lab_completions', {}))
        st.metric("Labs Completed", lab_count)
    
    with col_stat3:
        total_points = sum(lab['points'] for lab in st.session_state.get('lab_completions', {}).values())
        st.metric("Total Points", total_points)

# Footer
st.markdown("---")
st.caption("🎓 T21 SOC Analyst Training Portal - Your Path to Cybersecurity Excellence")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
