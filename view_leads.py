"""
LEADS DASHBOARD - View Captured Emails from Chatbot
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Leads Dashboard", page_icon="📧", layout="wide")

st.title("📧 Leads Dashboard - Captured Emails")

st.info("These are the emails captured by the AI chatbot on your homepage!")

# Connect to database
try:
    conn = sqlite3.connect("chatbot_conversations.db")
    
    # Get leads
    leads_df = pd.read_sql_query("""
    SELECT 
        id,
        email,
        phone,
        timestamp,
        conversation_count,
        quality
    FROM leads
    ORDER BY timestamp DESC
    """, conn)
    
    if len(leads_df) > 0:
        # Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Leads", len(leads_df))
        with col2:
            today_leads = len(leads_df[leads_df['timestamp'] >= datetime.now().strftime('%Y-%m-%d')])
            st.metric("Today", today_leads)
        with col3:
            hot_leads = len(leads_df[leads_df['quality'] == 'HOT'])
            st.metric("🔥 HOT Leads", hot_leads, help="Gave phone + 5+ messages")
        with col4:
            with_phone = len(leads_df[leads_df['phone'] != 'Not provided'])
            st.metric("📞 With Phone", with_phone)
        
        st.markdown("---")
        
        # Leads table
        st.markdown("### 📋 All Leads")
        
        # Format timestamp
        leads_df['timestamp'] = pd.to_datetime(leads_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Color code by quality
        def highlight_quality(row):
            if row['quality'] == 'HOT':
                return ['background-color: #ffcccc'] * len(row)
            elif row['quality'] == 'WARM':
                return ['background-color: #fff4cc'] * len(row)
            else:
                return [''] * len(row)
        
        # Display
        st.dataframe(
            leads_df.style.apply(highlight_quality, axis=1),
            use_container_width=True,
            column_config={
                "id": "ID",
                "email": st.column_config.TextColumn("Email", width="medium"),
                "phone": st.column_config.TextColumn("Phone", width="medium"),
                "timestamp": "Captured At",
                "conversation_count": "Messages",
                "quality": st.column_config.TextColumn("Quality", width="small")
            },
            hide_index=True
        )
        
        st.caption("🔴 Red = HOT Lead (gave phone + 5+ messages) | 🟡 Yellow = WARM (gave phone) | ⚪ White = COLD (email only)")
        
        # Export button
        st.markdown("---")
        csv = leads_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # Actions
        st.markdown("### 🚀 Next Steps - PRIORITY ORDER")
        st.markdown("""
        **🔥 HOT LEADS (Red) - CALL WITHIN 4 HOURS!**
        - Gave phone number + 5+ messages = READY TO BUY!
        - Conversion rate: 40-60%!
        - Call script: "Hi, you asked about our RTT training. I'm calling to help!"
        
        **🟡 WARM LEADS (Yellow) - CALL WITHIN 24 HOURS**
        - Gave phone number = Interested
        - Conversion rate: 20-30%
        - Call script: "You requested our course guide. Any questions?"
        
        **⚪ COLD LEADS (White) - EMAIL ONLY**
        - Email only = Less engaged
        - Conversion rate: 5-10%
        - Action: Send email with guide + £100 discount code
        
        **Email Template:**
        ```
        Subject: Your T21 Course Guide + Special Offer Inside!
        
        Hi there!
        
        Thanks for your interest in T21 Healthcare Training!
        
        Here's what you asked about:
        - Complete Course Guide: [Link]
        - Pricing: £99-£1,799 (4 tiers)
        - 20+ Career Paths: £25k-£55k salaries
        - TQUK-Endorsed Certification
        
        SPECIAL OFFER FOR YOU:
        £100 OFF any tier if you enroll within 48 hours!
        Use code: CHAT100
        
        Ready to start? Click here: [Link]
        
        Questions? Reply to this email!
        
        Best,
        T21 Team
        ```
        """)
    else:
        st.info("No leads captured yet. Keep the chatbot running and they'll appear here!")
        st.markdown("""
        **How it works:**
        1. Visitor chats with AI on homepage
        2. After 3 messages, AI asks for email
        3. Visitor provides email
        4. **Email appears here!**
        5. You follow up and convert!
        """)
    
    conn.close()
    
except Exception as e:
    st.error(f"Database error: {e}")
    st.info("Make sure the chatbot has been used at least once to create the database!")
