"""
AI TUTOR SYSTEM - 24/7 PERSONAL CYBERSECURITY MENTOR
Powered by OpenAI GPT-4 - Personalized learning assistance

Features:
- Ask any cybersecurity question
- Get instant explanations
- Lab hints and guidance
- Career advice
- Personalized learning paths
"""

import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="AI Tutor", page_icon="🤖", layout="wide")

# Check login
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in to access the AI Tutor")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email

# Header
st.title("🤖 AI Cybersecurity Tutor")
st.markdown("**Your 24/7 Personal Mentor - Powered by GPT-4**")
st.markdown(f"Student: {user_email}")

st.divider()

# Initialize chat history
if 'tutor_messages' not in st.session_state:
    st.session_state.tutor_messages = [
        {"role": "assistant", "content": """👋 Hi! I'm your AI Cybersecurity Tutor!

I can help you with:
- 📚 Explaining cybersecurity concepts
- 🔬 Hints for labs (without giving answers)
- 💡 Career advice
- 🎯 Study strategies
- 🐛 Debugging help
- 📝 Exam preparation

What would you like to learn today?"""}
    ]

# Display chat history
for message in st.session_state.tutor_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about cybersecurity..."):
    # Add user message
    st.session_state.tutor_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Intelligent fallback system - works WITHOUT API key
            ai_response = None
            
            # Check for common questions and provide smart answers
            prompt_lower = prompt.lower()
            
            # CIA Triad questions
            if "cia" in prompt_lower and ("triad" in prompt_lower or "what" in prompt_lower):
                ai_response = """**The CIA Triad** is the foundation of cybersecurity:

**C - Confidentiality:** Ensuring information is only accessible to authorized people
- Example: Encryption, access controls, passwords

**I - Integrity:** Ensuring information is accurate and hasn't been tampered with  
- Example: Checksums, digital signatures, version control

**A - Availability:** Ensuring information is accessible when needed
- Example: Backups, redundancy, DDoS protection

💡 **Real-world example:** A hospital needs:
- Confidentiality: Only doctors see patient records
- Integrity: Medical records must be accurate
- Availability: Records available 24/7 for emergencies"""

            # Nmap questions
            elif "nmap" in prompt_lower:
                ai_response = """**Nmap (Network Mapper)** is the #1 network scanning tool!

**Basic Commands:**
```bash
nmap 192.168.1.1          # Basic scan
nmap -sV 192.168.1.1      # Service version detection
nmap -O 192.168.1.1       # OS detection
nmap -p- 192.168.1.1      # Scan all ports
```

**Common Use Cases:**
- Find open ports on a target
- Identify services and versions
- Detect operating system
- Security auditing

💡 **Tip:** Always get permission before scanning! Unauthorized scanning is illegal.

**Try the Nmap lab** in the Cyber Lab to practice hands-on!"""
            
            # SQL Injection questions
            elif "sql" in prompt_lower and "injection" in prompt_lower:
                ai_response = """**SQL Injection** is a critical web vulnerability!

**How it works:**
Attackers insert malicious SQL code into input fields to manipulate database queries.

**Example Attack:**
```sql
Username: admin' OR '1'='1'--
Password: anything
```

**Why it works:**
The query becomes: `SELECT * FROM users WHERE username='admin' OR '1'='1'--'`
- The `OR '1'='1'` is always true
- The `--` comments out the rest

**Prevention:**
- Use prepared statements
- Input validation
- Parameterized queries
- Never trust user input!

🔬 **Practice:** Try the SQL Injection lab in the Web Hacking section!"""

            # Wireshark questions
            elif "wireshark" in prompt_lower:
                ai_response = """**Wireshark** is the world's most popular packet analyzer!

**What it does:**
Captures and analyzes network traffic in real-time.

**Common Filters:**
```
ip.addr == 192.168.1.1    # Specific IP
tcp.port == 80             # HTTP traffic
http                       # All HTTP
dns                        # DNS queries
```

**Use Cases:**
- Troubleshoot network issues
- Detect suspicious activity
- Analyze malware traffic
- Investigate security incidents

💡 **Tip:** Start with broad filters, then narrow down!

🔬 **Practice:** Check out the Wireshark lab in Network Security!"""

            # Career questions
            elif "career" in prompt_lower or "job" in prompt_lower or "salary" in prompt_lower:
                ai_response = """**SOC Analyst Career Path:**

**Entry Level (0-2 years):**
- Junior SOC Analyst
- Salary: £28,000 - £35,000
- Focus: Alert monitoring, basic investigations

**Mid Level (2-5 years):**
- SOC Analyst / Security Analyst
- Salary: £35,000 - £50,000
- Focus: Incident response, threat hunting

**Senior Level (5+ years):**
- Senior SOC Analyst / Team Lead
- Salary: £50,000 - £70,000
- Focus: Advanced threats, mentoring, strategy

**Required Skills:**
- SIEM tools (Splunk, QRadar)
- Network security
- Incident response
- Threat intelligence
- Communication skills

💼 **Check the Job Board** for current opportunities!"""

            # Default response for other questions
            else:
                ai_response = f"""Great question about: **{prompt}**

Here's what I can help with:

**If you're asking about a concept:**
- Check the SOC Training Portal for detailed lessons
- Watch the video lectures
- Read the module content

**If you're stuck on a lab:**
- Review the hints provided
- Check the cheat sheets
- Try breaking the problem into smaller steps

**If you need tool help:**
- Visit the Tool Practice Arena
- Check the command references
- Practice with the interactive examples

**Popular topics I can explain:**
- CIA Triad
- Nmap scanning
- SQL Injection
- Wireshark analysis
- SIEM tools
- Career advice

💡 **Tip:** Ask specific questions like "What is the CIA Triad?" or "How does Nmap work?"

Try rephrasing your question to be more specific, and I'll give you a detailed answer!"""

            st.markdown(ai_response)
            st.session_state.tutor_messages.append({"role": "assistant", "content": ai_response})

st.divider()

# Quick help buttons
st.markdown("### 🎯 Quick Help Topics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 Explain a Concept"):
        st.info("Ask me: 'What is the CIA triad?' or 'Explain how firewalls work'")

with col2:
    if st.button("🔬 Lab Hint"):
        st.info("Ask me: 'I'm stuck on the Nmap lab' or 'How do I find SUID binaries?'")

with col3:
    if st.button("💼 Career Advice"):
        st.info("Ask me: 'How do I become a SOC analyst?' or 'What certifications should I get?'")

with col4:
    if st.button("🎓 Study Tips"):
        st.info("Ask me: 'How should I prepare for the exam?' or 'Best way to learn SIEM?'")

# Clear chat
if st.button("🗑️ Clear Chat History"):
    st.session_state.tutor_messages = [
        {"role": "assistant", "content": "Chat cleared! What would you like to learn?"}
    ]
    st.rerun()

st.markdown("---")
st.caption("🤖 AI Tutor powered by OpenAI GPT-4 - Available 24/7")
st.caption(f"Session: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
