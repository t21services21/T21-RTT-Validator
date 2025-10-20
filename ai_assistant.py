"""
AI ASSISTANT CHATBOT
Interactive AI helper for students and visitors
Answers questions about RTT, platform features, and provides guidance
"""

import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# Initialize OpenAI client
def get_openai_client():
    """Get OpenAI client from secrets"""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if api_key:
            return OpenAI(api_key=api_key)
    except:
        pass
    return None

# Import complete accurate platform knowledge
try:
    from COMPLETE_PLATFORM_KNOWLEDGE import COMPLETE_PLATFORM_KNOWLEDGE
    import json
    PLATFORM_INFO = json.dumps(COMPLETE_PLATFORM_KNOWLEDGE, indent=2)
except:
    # Fallback if import fails
    PLATFORM_INFO = """
T21 HEALTHCARE PLATFORM - COMPLETE RTT TRAINING & VALIDATION SYSTEM

**WHAT WE OFFER:**

1. **LEARNING PORTAL**
   - Structured 8-week RTT training course
   - Learning materials (PDFs, documents)
   - Video library (lectures, tutorials)
   - Assignments and practice exercises
   - Progress tracking

2. **PATIENT ADMINISTRATION HUB (PAS)**
   - Complete NHS PAS system simulation
   - Patient registration and management
   - Referral processing
   - Appointment scheduling
   - Real NHS workflow practice

3. **RTT PATHWAY MANAGEMENT**
   - Create and manage RTT pathways
   - Episode recording (Outpatient, Diagnostic, Treatment)
   - Clock start/stop management
   - Breach monitoring
   - Real-time pathway tracking

4. **CLINIC LETTER INTERPRETER (AI-POWERED)**
   - Upload clinic letters
   - AI analyzes and extracts key information
   - Identifies RTT status and actions needed
   - Validates against NHS standards
   - Educational mode with explanations

5. **CERTIFICATION SYSTEM**
   - 1000+ RTT questions covering all scenarios
   - 100-question personalized exams
   - Multiple difficulty levels
   - Three certification tiers:
     * Foundation (70-79%)
     * Practitioner (80-89%)
     * Expert (90-100%)
   - Anti-cheating features
   - Downloadable certificates

6. **INTERVIEW PREPARATION**
   - Practice interview questions
   - STAR method guidance
   - NHS-specific scenarios
   - Role-play simulations
   - Tips and best practices

7. **PROGRESS TRACKING**
   - Personal dashboard
   - Course completion tracking
   - Quiz scores and history
   - Certificate achievements
   - Learning analytics

8. **ADMINISTRATION (Teachers/Admins)**
   - Student management
   - Grade tracking
   - Content upload (materials, videos)
   - Progress monitoring
   - Analytics dashboard

**PRICING:**
- Individual: £49/month or £497 one-time (6 months access)
- Small Teams: £2,500/year (5-20 users)
- Enterprise: Custom pricing for NHS Trusts

**WHO IS THIS FOR:**
- Medical secretaries wanting to become RTT validators
- Healthcare administrators
- NHS staff needing RTT training
- Career changers entering NHS
- Training providers and universities

**KEY BENEFITS:**
- Complete RTT training in 8 weeks
- Self-paced learning
- Real NHS system practice
- AI-powered feedback
- Industry-recognized certification
- Job-ready skills

**RTT BASICS:**
RTT (Referral to Treatment) is the NHS standard for tracking patient pathways from referral to treatment. 
Key codes include:
- 10: First Outpatient Appointment
- 20/21: Clock continues
- 30: Treatment - Clock Stop
- 31-34: Various clock stops
- 91-96: Removals from pathway

**CONTACT:**
- Email: admin@t21services.co.uk
- Platform: t21-healthcare-platform.streamlit.app
"""


def render_ai_assistant():
    """Render the AI assistant chatbot"""
    
    st.subheader("🤖 AI Assistant")
    
    # Check OpenAI availability
    client = get_openai_client()
    
    if not client:
        st.error("⚠️ AI Assistant not available. OpenAI API key not configured.")
        st.info("Contact admin to enable AI features.")
        return
    
    # Initialize chat history
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = [
            {
                "role": "assistant",
                "content": "👋 Hi! I'm your T21 AI Assistant. I can help you with:\n\n"
                          "📚 Platform features and navigation\n"
                          "📖 RTT concepts and codes\n"
                          "❓ Course questions\n"
                          "💡 Study tips and guidance\n\n"
                          "What would you like to know?"
            }
        ]
    
    # Display chat history
    for message in st.session_state.ai_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about T21 or RTT..."):
        # Add user message
        st.session_state.ai_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare messages for API
                    messages = [
                        {
                            "role": "system",
                            "content": f"""You are a helpful AI assistant for the T21 Healthcare Platform, 
                            an RTT (Referral to Treatment) training and validation system.
                            
                            You help students learn about RTT, navigate the platform, and understand NHS workflows.
                            
                            Be friendly, professional, and educational. If asked about features not mentioned in the 
                            platform info, politely say you're not sure but encourage them to explore the platform.
                            
                            PLATFORM INFORMATION:
                            {PLATFORM_INFO}
                            
                            Keep responses concise but helpful. Use emojis occasionally to be engaging.
                            If asked about RTT codes, provide clear explanations with examples."""
                        }
                    ]
                    
                    # Add conversation history (last 10 messages)
                    messages.extend(st.session_state.ai_messages[-10:])
                    
                    # Get AI response
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        max_tokens=500,
                        temperature=0.7
                    )
                    
                    assistant_message = response.choices[0].message.content
                    
                    # Display and save response
                    st.markdown(assistant_message)
                    st.session_state.ai_messages.append({"role": "assistant", "content": assistant_message})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.ai_messages.append({"role": "assistant", "content": error_msg})
    
    # Quick action buttons
    st.markdown("---")
    st.markdown("**Quick Questions:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 What modules are available?", key="quick_modules"):
            st.session_state.ai_messages.append({
                "role": "user",
                "content": "What modules are available?"
            })
            st.rerun()
    
    with col2:
        if st.button("🎓 How do I get certified?", key="quick_cert"):
            st.session_state.ai_messages.append({
                "role": "user",
                "content": "How do I get certified?"
            })
            st.rerun()
    
    with col3:
        if st.button("❓ What is RTT?", key="quick_rtt"):
            st.session_state.ai_messages.append({
                "role": "user",
                "content": "What is RTT?"
            })
            st.rerun()
    
    # Clear chat button
    st.markdown("---")
    if st.button("🔄 Clear Chat", key="clear_chat"):
        st.session_state.ai_messages = [
            {
                "role": "assistant",
                "content": "👋 Chat cleared! How can I help you?"
            }
        ]
        st.rerun()


def render_quick_help():
    """Render quick help sidebar widget"""
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 💬 Need Help?")
        
        if st.button("🤖 Ask AI Assistant", key="sidebar_ai", use_container_width=True):
            st.session_state.show_ai_assistant = True
        
        with st.expander("📚 Quick Links"):
            st.markdown("""
            - [📖 Course Overview](#)
            - [🎥 Tutorial Videos](#)
            - [📋 RTT Codes Reference](#)
            - [❓ FAQ](#)
            - [📧 Contact Support](mailto:admin@t21services.co.uk)
            """)


# Example integration in main app
def example_integration():
    """Show how to integrate in main app"""
    
    # Add to navigation
    st.sidebar.markdown("---")
    if st.sidebar.button("🤖 AI Assistant", key="nav_ai"):
        st.switch_page("pages/ai_assistant.py")
    
    # Or add as expandable section
    with st.sidebar.expander("💬 Ask AI"):
        st.info("Click here to chat with our AI assistant about the platform!")
        if st.button("Open AI Chat"):
            st.session_state.show_ai_assistant = True


if __name__ == "__main__":
    st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
    render_ai_assistant()
