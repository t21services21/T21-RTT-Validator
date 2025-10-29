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
            try:
                # Use OpenAI API
                client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
                
                # System prompt for cybersecurity tutor
                system_prompt = """You are an expert cybersecurity tutor for SOC analyst training.

Your role:
- Explain concepts clearly and simply
- Provide hints for labs WITHOUT giving direct answers
- Encourage critical thinking
- Relate concepts to real-world scenarios
- Be encouraging and supportive
- Guide students to discover answers themselves

Topics you cover:
- Network security
- SIEM and log analysis
- Incident response
- Threat hunting
- Malware analysis
- SOC operations
- Security tools (Splunk, Wireshark, etc.)
- Career guidance

Keep responses concise (2-3 paragraphs max) unless asked for detail."""

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.tutor_messages
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                ai_response = response.choices[0].message.content
                
            except Exception as e:
                # Fallback response if API fails
                ai_response = f"""I'm having trouble connecting right now, but here's what I can tell you:

**About your question:** "{prompt}"

This is a great question! Here are some key points:

1. **Start with the basics** - Make sure you understand the fundamentals
2. **Practice hands-on** - Theory is important, but labs solidify learning
3. **Use resources** - Check the module content, videos, and documentation
4. **Ask specific questions** - The more specific, the better I can help!

Try rephrasing your question or check the course materials. I'll be back online soon!

💡 **Tip:** Break complex problems into smaller parts."""

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
