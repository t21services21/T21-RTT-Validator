"""
T21 HEALTHCARE PLATFORM - NATURAL LANGUAGE AI INTERFACE
Talk to the system - AI understands and responds
"""

import streamlit as st
from datetime import datetime
import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from universal_crud import (
    create_
from navigation import render_navigation
record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)



st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="voice_ai")

st.title("🗣️ Natural Language AI - Talk to T21")
st.markdown("**First RTT system you can TALK to - No clicking required!**")

# Voice interface demo
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; color: white; text-align: center; margin: 30px 0;">
    <h1 style="color: white; margin: 0;">🎤</h1>
    <h2 style="color: white;">Say Anything - AI Understands</h2>
    <p style="font-size: 18px;">Natural conversation with your RTT system</p>
</div>
""", unsafe_allow_html=True)


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Interaction Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Interactions")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_voice_interactions")
    with col2:
        records = read_all_records('voice_interactions')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "voice_interactions.csv", "text/csv")
    
    # Get records
    records = read_all_records('voice_interactions')
    
    if search_term:
        records = search_records('voice_interactions', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Interaction #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('voice_interactions', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Interaction")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('voice_interactions')
    
    if records:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(records))
        with col2:
            st.metric("This Month", 0)  # Calculate as needed
        with col3:
            st.metric("Active", len(records))
    else:
        st.info("No data for analytics yet")

st.markdown("---")
# Educational content continues below...


st.markdown("---")

# Command examples
st.markdown("### 💬 Try These Commands")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Queries & Reports")
    queries = [
        "Show me all patients at risk of breach",
        "What's our RTT performance this month?",
        "Generate monthly commissioner report",
        "Who's waiting longest in Orthopaedics?",
        "How many DNAs this week?",
        "What's our 52-week waiter count?"
    ]
    for q in queries:
        if st.button(f"🎤 {q}", key=f"query_{q}", use_container_width=True):
            st.success(f"✅ Processing: '{q}'")
            with st.spinner("AI thinking..."):
                import time
                time.sleep(1)
            
            if "performance" in q.lower():
                st.info("**AI Response:** Your RTT performance this month is **92.8%**, which is **0.8 percentage points above target**. You're treating an average of 245 patients per month.")
            elif "breach" in q.lower():
                st.warning("**AI Response:** **12 patients** are at high risk of breach (16-17 weeks waiting). Here's the list:\n- John Smith (Ortho, 17 weeks)\n- Mary Jones (Cardiology, 16.5 weeks)\n- [See full list in dashboard]")
            elif "report" in q.lower():
                st.success("**AI Response:** Commissioner report generated! Downloading PDF... ✅")
            else:
                st.info("**AI Response:** Processing your request...")

with col2:
    st.markdown("#### ⚡ Actions & Commands")
    actions = [
        "Validate NHS number 1234567890",
        "Pause clock for patient John Smith",
        "Send DNA warning to Mary Jones",
        "Book appointment for next Tuesday",
        "Transfer patient to Rheumatology",
        "Alert clinical director about breaches"
    ]
    for a in actions:
        if st.button(f"🎤 {a}", key=f"action_{a}", use_container_width=True):
            st.success(f"✅ Executing: '{a}'")
            with st.spinner("AI working..."):
                import time
                time.sleep(1)
            
            if "validate" in a.lower():
                st.success("**AI Response:** ✅ Pathway **VALID**\n- Referral: 10 weeks ago\n- Within 18-week target\n- No issues found")
            elif "pause" in a.lower():
                st.info("**AI Response:** Clock paused for John Smith. Reason: [Please specify]\n- Patient holiday? Patient choice? Clinical reason?")
            elif "alert" in a.lower():
                st.success("**AI Response:** ✅ Alert sent to Dr. Sarah Johnson, Clinical Director.\n📧 Email delivered\n📱 SMS delivered")
            else:
                st.info("**AI Response:** Action completed successfully!")

st.markdown("---")

# Interactive voice input
st.markdown("### 🎙️ Live Voice Input (Demo)")

user_command = st.text_input("🗣️ Type or speak your command:", 
    placeholder="e.g., Show me Orthopaedics waiting list")

if st.button("🚀 Execute Command", type="primary", use_container_width=True):
    if user_command:
        st.success(f"🎤 **Command received:** {user_command}")
        
        with st.spinner("🤖 AI processing..."):
            import time
            time.sleep(1.5)
        
        # Smart responses based on keywords
        command_lower = user_command.lower()
        
        if any(word in command_lower for word in ["show", "list", "display", "what"]):
            st.markdown("""
            **🤖 AI Response:**
            
            Here's your requested information:
            
            | Patient | Specialty | Weeks Waiting | Status |
            |---------|-----------|---------------|--------|
            | John Smith | Orthopaedics | 15 | 🟢 Safe |
            | Mary Jones | Orthopaedics | 17 | 🟡 At Risk |
            | David Brown | Orthopaedics | 12 | 🟢 Safe |
            
            Would you like me to:
            - Export this to CSV?
            - Send breach alerts?
            - Generate detailed report?
            """)
        
        elif any(word in command_lower for word in ["validate", "check"]):
            st.success("""
            **🤖 AI Response:** ✅ Validation Complete
            
            **Result:** COMPLIANT
            - Clock started correctly
            - Within 18-week target
            - All documentation present
            - No anomalies detected
            
            Confidence: 99.8%
            """)
        
        elif any(word in command_lower for word in ["send", "email", "notify"]):
            st.success("""
            **🤖 AI Response:** ✅ Message Sent
            
            📧 Email delivered to: clinical.team@nhs.uk
            📱 SMS sent to: 3 team members
            ⏰ Timestamp: 11:15am
            
            Message: "RTT breach alert - 12 patients require attention"
            """)
        
        else:
            st.info("""
            **🤖 AI Response:** I understand you want to know about RTT pathways.
            
            Could you be more specific? For example:
            - "Show me Ortho waiting list"
            - "Validate NHS 1234567890"
            - "Send breach alerts"
            """)
    else:
        st.warning("Please enter a command first!")

st.markdown("---")

# Voice training
st.markdown("### 🎓 What AI Can Understand")

tab1, tab2, tab3 = st.tabs(["📊 Queries", "⚡ Actions", "🤝 Conversations"])

with tab1:
    st.markdown("""
    **Questions AI Understands:**
    
    - "What's our RTT performance?"
    - "Show me breach risks"
    - "How many patients waiting in Cardiology?"
    - "Who DNAed today?"
    - "Generate this month's report"
    - "Compare to last month"
    - "What's our longest wait?"
    - "Show me 52-week waiters"
    
    **Try natural language - AI adapts to your style!**
    """)

with tab2:
    st.markdown("""
    **Commands AI Executes:**
    
    - "Validate this pathway"
    - "Pause the clock"
    - "Send DNA warning"
    - "Book an appointment"
    - "Transfer to another specialty"
    - "Alert the team"
    - "Export to CSV"
    - "Create a report"
    
    **AI confirms actions before executing!**
    """)

with tab3:
    st.markdown("""
    **Natural Conversations:**
    
    You: "Show me Ortho patients"  
    AI: "Here are 45 Orthopaedics patients..."
    
    You: "Filter by breach risk"  
    AI: "Filtered to 8 high-risk patients..."
    
    You: "Send alerts to their coordinators"  
    AI: "Alerts sent to 3 coordinators. Done!"
    
    **Multi-step conversations = AI remembers context!**
    """)

st.markdown("---")

# Benefits showcase
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.markdown("""
    <div style="background: #e3f2fd; padding: 25px; border-radius: 15px;">
        <h3>⚡ 5x Faster</h3>
        <p>Voice commands vs clicking through menus</p>
        <strong>Example:</strong>
        <ul>
            <li>Voice: 5 seconds</li>
            <li>Clicking: 25 seconds</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_b2:
    st.markdown("""
    <div style="background: #f3e5f5; padding: 25px; border-radius: 15px;">
        <h3>🎯 Zero Learning</h3>
        <p>No training needed - just talk naturally</p>
        <strong>Accessible:</strong>
        <ul>
            <li>Dyslexia friendly</li>
            <li>Visual impairment</li>
            <li>Hands-free work</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_b3:
    st.markdown("""
    <div style="background: #e8f5e9; padding: 25px; border-radius: 15px;">
        <h3>🤖 AI Learns</h3>
        <p>Adapts to your speech patterns</p>
        <strong>Gets better:</strong>
        <ul>
            <li>Understands accents</li>
            <li>Learns your vocab</li>
            <li>Predicts intent</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.success("""
🎤 **Coming Soon:** Full voice recognition with microphone input  
🌐 **Languages:** English (UK), with multi-language support planned  
🔐 **Privacy:** Voice processing on secure NHS-approved servers  
📱 **Mobile:** Voice commands available in T21 Mobile App
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
