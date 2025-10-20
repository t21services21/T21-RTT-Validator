"""
FLOATING CHATBOT - Professional Style
Appears as bubble in bottom right corner like big company websites
"""

import streamlit as st
from openai import OpenAI
from COMPLETE_PLATFORM_KNOWLEDGE import COMPLETE_PLATFORM_KNOWLEDGE
import json
from datetime import datetime
import sqlite3
import os

# Initialize conversation database for learning
def init_conversation_db():
    """Initialize SQLite database to store and learn from conversations"""
    db_path = "chatbot_conversations.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create conversations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user_question TEXT,
        ai_response TEXT,
        topic TEXT,
        helpful INTEGER DEFAULT 1
    )
    """)
    
    # Create common questions cache
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS common_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT UNIQUE,
        answer TEXT,
        times_asked INTEGER DEFAULT 1,
        last_asked TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def save_conversation(question, answer, topic="general"):
    """Save conversation for learning"""
    try:
        conn = sqlite3.connect("chatbot_conversations.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO conversations (timestamp, user_question, ai_response, topic)
        VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), question, answer, topic))
        conn.commit()
        conn.close()
    except:
        pass

def get_similar_questions(question):
    """Get similar previously asked questions and answers (simple RAG)"""
    try:
        conn = sqlite3.connect("chatbot_conversations.db")
        cursor = conn.cursor()
        
        # Simple keyword matching (can be enhanced with embeddings)
        keywords = question.lower().split()[:3]  # First 3 words
        
        results = []
        for keyword in keywords:
            cursor.execute("""
            SELECT user_question, ai_response 
            FROM conversations 
            WHERE user_question LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT 3
            """, (f"%{keyword}%",))
            results.extend(cursor.fetchall())
        
        conn.close()
        return results[:3]  # Return top 3
    except:
        return []

def render_floating_chatbot():
    """Render SMART floating chatbot - like Intercom/Drift/big companies"""
    
    # Initialize DB
    init_conversation_db()
    
    # Initialize smart behavior states
    if "chatbot_appeared" not in st.session_state:
        st.session_state.chatbot_appeared = False
    if "chatbot_minimized_by_user" not in st.session_state:
        st.session_state.chatbot_minimized_by_user = False
    if "page_visit_time" not in st.session_state:
        st.session_state.page_visit_time = datetime.now()
    if "proactive_message_shown" not in st.session_state:
        st.session_state.proactive_message_shown = False
    
    # CSS for floating bubble with ADVANCED animations
    st.markdown("""
    <style>
        /* Floating chat bubble - PROFESSIONAL */
        .floating-chat-bubble {
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            z-index: 9999;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .floating-chat-bubble:hover {
            transform: scale(1.1) translateY(-2px);
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
        }
        
        /* Unread badge */
        .unread-badge {
            position: absolute;
            top: -4px;
            right: -4px;
            background: #ff4444;
            color: white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid white;
            animation: bounce 0.5s ease-in-out infinite alternate;
        }
        
        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-4px); }
        }
        
        /* Pulse animation - ATTENTION GRABBING */
        @keyframes pulse {
            0% { 
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 8px 40px rgba(102, 126, 234, 0.8);
                transform: scale(1.05);
            }
            100% { 
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
                transform: scale(1);
            }
        }
        
        .pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        /* Ripple effect on click */
        @keyframes ripple {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            100% {
                transform: scale(1.5);
                opacity: 0;
            }
        }
        
        /* Welcome tooltip - PROACTIVE MESSAGE */
        .welcome-tooltip {
            position: fixed;
            bottom: 100px;
            right: 24px;
            background: white;
            padding: 16px 20px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            max-width: 280px;
            z-index: 9998;
            animation: slideIn 0.4s ease-out;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .welcome-tooltip::after {
            content: '';
            position: absolute;
            bottom: -8px;
            right: 32px;
            width: 16px;
            height: 16px;
            background: white;
            transform: rotate(45deg);
        }
        
        .tooltip-close {
            position: absolute;
            top: 8px;
            right: 8px;
            cursor: pointer;
            color: #999;
            font-size: 18px;
            font-weight: bold;
        }
        
        /* Typing indicator */
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            animation: typing 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .floating-chat-bubble {
                bottom: 16px;
                right: 16px;
                width: 56px;
                height: 56px;
            }
            
            .welcome-tooltip {
                right: 16px;
                bottom: 84px;
                max-width: calc(100vw - 32px);
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chat state
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False
    
    if "floating_chat_messages" not in st.session_state:
        st.session_state.floating_chat_messages = [
            {
                "role": "assistant",
                "content": "👋 **Hi! I'm T21's AI Assistant!**\n\n"
                          "Ask me about:\n"
                          "💰 Pricing (4 tiers: £99-£1,799)\n"
                          "🎓 20+ Career Paths (£25k-£55k)\n"
                          "📚 TQUK-Endorsed Training\n"
                          "🏥 NHS Trust Solutions\n\n"
                          "**What can I help with?**"
            }
        ]
    
    # SMART BEHAVIOR: Show proactive message after 8 seconds
    time_on_page = (datetime.now() - st.session_state.page_visit_time).total_seconds()
    show_proactive = time_on_page > 8 and not st.session_state.proactive_message_shown and not st.session_state.chatbot_minimized_by_user
    
    # Show welcome tooltip (proactive message)
    if show_proactive and not st.session_state.chat_open:
        st.markdown("""
        <div class="welcome-tooltip">
            <span class="tooltip-close" onclick="this.parentElement.style.display='none'">×</span>
            <div style="font-weight: bold; color: #667eea; margin-bottom: 8px;">👋 Need help?</div>
            <div style="font-size: 14px; color: #555;">Ask me about pricing, careers, or training!</div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.proactive_message_shown = True
    
    # Add fixed position container for button
    st.markdown("""
    <style>
        .fixed-chat-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999999;
        }
        
        /* Override Streamlit button styling for chat button */
        div[data-testid="stButton"] > button[kind="primary"] {
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            z-index: 999999 !important;
            border-radius: 50px !important;
            padding: 12px 24px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
            animation: pulse 2s infinite !important;
        }
        
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
        }
        
        @keyframes pulse {
            0%, 100% { box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5); }
            50% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.9); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Toggle button - Make it visible!
    st.markdown("---")
    if not st.session_state.chat_open:
        if st.button("💬 Chat with Our AI Assistant", key="chat_toggle", type="primary", use_container_width=True):
            st.session_state.chat_open = True
    else:
        if st.button("✖️ Close Chat", key="chat_close", type="secondary", use_container_width=True):
            st.session_state.chat_open = False
    
    # Show chat window if open
    if st.session_state.chat_open:
        st.markdown("### 💬 T21 AI Assistant")
        st.info("🚀 Get instant answers! I learn from every conversation.")
        
        # Display messages
        for msg in st.session_state.floating_chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Chat input using regular text input (won't create blue bar!)
        st.markdown("---")
        st.markdown("**💬 Type your message:**")
        
        col_input, col_send = st.columns([5, 1])
        with col_input:
            user_input = st.text_input("Message", key="chat_text_input", placeholder="Ask me anything...", label_visibility="collapsed")
        with col_send:
            send_btn = st.button("Send", key="send_btn", type="primary", use_container_width=True)
        
        prompt = None
        if send_btn and user_input:
            prompt = user_input
            # Add user message
            st.session_state.floating_chat_messages.append({"role": "user", "content": prompt})
        elif send_btn and not user_input:
            st.warning("Please type a message first!")
        
        if prompt:
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get similar previous questions (RAG)
            similar_qa = get_similar_questions(prompt)
            context_from_history = ""
            if similar_qa:
                context_from_history = "\n\nPREVIOUS SIMILAR QUESTIONS:\n"
                for q, a in similar_qa:
                    context_from_history += f"Q: {q}\nA: {a[:200]}...\n\n"
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("✨ Thinking..."):
                    try:
                        client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
                        
                        system_prompt = f"""You are an enthusiastic sales AI for T21 Healthcare Platform.

COMPLETE PLATFORM INFO:
{json.dumps(COMPLETE_PLATFORM_KNOWLEDGE, indent=2)}

{context_from_history}

INSTRUCTIONS:
1. Use COMPLETE_PLATFORM_KNOWLEDGE for accurate answers
2. If similar questions were asked before, use that context too
3. Highlight value: "£5,000+ for £1,299" (Tier 2)
4. Create urgency: "30 spots/month", "Price increase April 2026"
5. Add bonuses: "£300 FREE bonuses!"
6. Social proof: "Sarah: £24k → £34k (8 weeks)"
7. ROI: "92% get jobs within 3 months"
8. Show 20+ career paths
9. End with CTA
10. Keep under 200 words

PRICING:
- Taster: £99/1 month
- Tier 1: £499/6 months
- Tier 2: £1,299/12 months (TQUK cert) ⭐ MOST POPULAR
- Tier 3: £1,799/12 months (cert + coach)

Guide them to click LOGIN/REGISTER!"""
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                *st.session_state.floating_chat_messages[-6:]
                            ],
                            max_tokens=400,
                            temperature=0.7
                        )
                        
                        answer = response.choices[0].message.content
                        st.markdown(answer)
                        st.session_state.floating_chat_messages.append({"role": "assistant", "content": answer})
                        
                        # Save conversation for learning
                        save_conversation(prompt, answer, topic="general")
                        
                    except Exception as e:
                        error = "AI temporarily unavailable. Email: admin@t21services.co.uk"
                        st.error(error)
                        st.session_state.floating_chat_messages.append({"role": "assistant", "content": error})
        
        # Quick actions
        st.markdown("**Quick Questions:**")
        qa1, qa2, qa3 = st.columns(3)
        
        with qa1:
            if st.button("💰 Price", key="float_q1", use_container_width=True):
                st.session_state.quick_question = "How much does it cost?"
        
        with qa2:
            if st.button("🎓 Jobs", key="float_q2", use_container_width=True):
                st.session_state.quick_question = "What career paths are available?"
        
        with qa3:
            if st.button("⏱️ Time", key="float_q3", use_container_width=True):
                st.session_state.quick_question = "How long does training take?"
        
        # Handle quick question (generate AI response)
        if "quick_question" in st.session_state and st.session_state.quick_question:
            prompt = st.session_state.quick_question
            st.session_state.quick_question = None  # Clear flag
            
            # Add user message
            st.session_state.floating_chat_messages.append({"role": "user", "content": prompt})
            
            # Get similar previous questions (RAG)
            similar_qa = get_similar_questions(prompt)
            context_from_history = ""
            if similar_qa:
                context_from_history = "\n\nPREVIOUS SIMILAR QUESTIONS:\n"
                for q, a in similar_qa:
                    context_from_history += f"Q: {q}\nA: {a[:200]}...\n\n"
            
            # Generate AI response
            try:
                from openai import OpenAI
                from COMPLETE_PLATFORM_KNOWLEDGE import COMPLETE_PLATFORM_KNOWLEDGE
                import json
                
                client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
                
                system_prompt = f"""You are an enthusiastic sales AI for T21 Healthcare Platform.

COMPLETE PLATFORM INFO:
{json.dumps(COMPLETE_PLATFORM_KNOWLEDGE, indent=2)}

{context_from_history}

INSTRUCTIONS:
1. Use COMPLETE_PLATFORM_KNOWLEDGE for accurate answers
2. If similar questions were asked before, use that context too
3. Highlight value: "£5,000+ for £1,299" (Tier 2)
4. Create urgency: "30 spots/month", "Price increase April 2026"
5. Add bonuses: "£300 FREE bonuses!"
6. Social proof: "Sarah: £24k → £34k (8 weeks)"
7. ROI: "92% get jobs within 3 months"
8. Show 20+ career paths
9. End with CTA
10. Keep under 200 words

PRICING:
- Taster: £99/1 month
- Tier 1: £499/6 months
- Tier 2: £1,299/12 months (TQUK cert) ⭐ MOST POPULAR
- Tier 3: £1,799/12 months (cert + coach)

Guide them to click LOGIN/REGISTER!"""
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.floating_chat_messages[-6:]
                    ],
                    max_tokens=400,
                    temperature=0.7
                )
                
                answer = response.choices[0].message.content
                st.session_state.floating_chat_messages.append({"role": "assistant", "content": answer})
                
                # Save conversation for learning
                save_conversation(prompt, answer, topic="quick_question")
                
            except Exception as e:
                error = "AI temporarily unavailable. Email: admin@t21services.co.uk"
                st.session_state.floating_chat_messages.append({"role": "assistant", "content": error})
        
        # LEAD CAPTURE: Progressive approach (email first, then phone)
        message_count = len([m for m in st.session_state.floating_chat_messages if m["role"] == "user"])
        
        # Step 1: Email capture (after 3 messages)
        if message_count >= 3 and "email_captured" not in st.session_state:
            st.markdown("---")
            st.info("💌 **Want our complete course guide?** Enter your email below!")
            email_input = st.text_input("📧 Email Address", key="lead_email", placeholder="your@email.com")
            if st.button("📥 Get Free Guide", key="capture_email"):
                if email_input and "@" in email_input:
                    st.session_state.email_captured = email_input
                    st.success("✅ Perfect! One more thing...")
                else:
                    st.error("Please enter a valid email")
        
        # Step 2: Phone capture (after email captured)
        elif "email_captured" in st.session_state and "phone_captured" not in st.session_state:
            st.markdown("---")
            st.success(f"✅ Email saved: {st.session_state.email_captured}")
            st.info("📞 **Want faster help?** Our team can call you to answer questions!")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                phone_input = st.text_input("📱 Phone Number (Optional)", key="lead_phone", placeholder="07XXX XXXXXX or +44...")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                skip_phone = st.button("Skip", key="skip_phone")
            
            if st.button("📞 Yes, Call Me!", key="capture_phone"):
                st.session_state.phone_captured = phone_input if phone_input else "Not provided"
                # Save complete lead to database
                try:
                    conn = sqlite3.connect("chatbot_conversations.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        phone TEXT,
                        timestamp TEXT,
                        conversation_count INTEGER,
                        quality TEXT
                    )
                    """)
                    
                    # Determine lead quality
                    quality = "HOT" if phone_input and message_count >= 5 else "WARM" if phone_input else "COLD"
                    
                    cursor.execute("""
                    INSERT INTO leads (email, phone, timestamp, conversation_count, quality)
                    VALUES (?, ?, ?, ?, ?)
                    """, (st.session_state.email_captured, st.session_state.phone_captured, 
                          datetime.now().isoformat(), message_count, quality))
                    conn.commit()
                    conn.close()
                    
                    if phone_input:
                        st.success("🎉 Amazing! We'll call you within 24 hours!")
                    else:
                        st.success("✅ Great! Check your email for the complete guide!")
                    
                    st.info("Ready to enroll now? Click **LOGIN/REGISTER** above!")
                except:
                    pass
            
            if skip_phone:
                st.session_state.phone_captured = "Not provided"
                # Save to database
                try:
                    conn = sqlite3.connect("chatbot_conversations.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        phone TEXT,
                        timestamp TEXT,
                        conversation_count INTEGER,
                        quality TEXT
                    )
                    """)
                    cursor.execute("""
                    INSERT INTO leads (email, phone, timestamp, conversation_count, quality)
                    VALUES (?, ?, ?, ?, ?)
                    """, (st.session_state.email_captured, "Not provided", 
                          datetime.now().isoformat(), message_count, "COLD"))
                    conn.commit()
                    conn.close()
                except:
                    pass
                st.success("✅ No problem! Check your email for the guide!")
                st.info("Ready to enroll? Click **LOGIN/REGISTER** above!")
        
        # Feedback
        st.markdown("---")
        st.markdown("**Was this helpful?** 👍 or 👎")
        fb1, fb2 = st.columns(2)
        with fb1:
            if st.button("👍 Yes", key="helpful_yes"):
                st.success("Thanks! 🎉 Ready to enroll? Click LOGIN/REGISTER above!")
        with fb2:
            if st.button("👎 No", key="helpful_no"):
                st.info("We'll improve! Any specific question? Ask me!")

# End of render_floating_chatbot function
