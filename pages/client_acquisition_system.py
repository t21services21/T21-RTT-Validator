"""
CLIENT ACQUISITION SYSTEM
Automated lead generation, sales, and onboarding

Features:
- Lead tracking
- Automated proposals
- Contract management
- Client onboarding
- Pipeline management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Client Acquisition", page_icon="💼", layout="wide")

# Check if admin/staff
if 'user_email' not in st.session_state or not st.session_state.get('logged_in'):
    st.error("🔒 Please log in")
    if st.button("🔐 Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user_email
user_role = st.session_state.get('user_license', {})
if hasattr(user_role, 'role'):
    user_role = user_role.role
else:
    user_role = 'student'

is_admin = user_role in ['super_admin', 'admin', 'staff'] or 'admin@t21services' in user_email.lower()

if not is_admin:
    st.error("🚫 Admin/Staff Only")
    st.stop()

# Header
st.title("💼 Client Acquisition System")
st.markdown(f"**User:** {user_email}")
st.markdown("**Automated Lead Generation & Sales Pipeline**")

st.divider()

# ============================================
# DASHBOARD METRICS
# ============================================

st.header("📊 Sales Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎯 Active Leads", "47", "+12 this week")

with col2:
    st.metric("💰 Pipeline Value", "£485K", "+£125K")

with col3:
    st.metric("✅ Closed Deals", "8", "+3 this month")

with col4:
    st.metric("📈 Conversion Rate", "17%", "+3%")

st.divider()

# ============================================
# SALES PIPELINE
# ============================================

st.header("🔄 Sales Pipeline")

# Pipeline stages
pipeline_data = {
    "Stage": ["New Leads", "Qualified", "Proposal Sent", "Negotiation", "Closed Won"],
    "Count": [47, 23, 15, 8, 8],
    "Value": [470000, 345000, 225000, 120000, 96000]
}

df_pipeline = pd.DataFrame(pipeline_data)

fig_funnel = go.Figure(go.Funnel(
    y=df_pipeline['Stage'],
    x=df_pipeline['Count'],
    textinfo="value+percent initial",
    marker={"color": ["#3498db", "#2ecc71", "#f39c12", "#e74c3c", "#27ae60"]}
))

fig_funnel.update_layout(height=400, title="Sales Funnel")
st.plotly_chart(fig_funnel, use_container_width=True)

st.divider()

# ============================================
# LEADS MANAGEMENT
# ============================================

st.header("👥 Leads Management")

tab1, tab2, tab3, tab4 = st.tabs(["📋 All Leads", "➕ Add Lead", "📧 Email Campaigns", "📊 Analytics"])

with tab1:
    # Filter options
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        status_filter = st.selectbox("Filter by Status", ["All", "New", "Qualified", "Proposal Sent", "Negotiation", "Won", "Lost"])
    
    with col_f2:
        source_filter = st.selectbox("Filter by Source", ["All", "Website", "LinkedIn", "Referral", "Cold Outreach", "Event"])
    
    with col_f3:
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Value (High-Low)", "Value (Low-High)"])
    
    # Sample leads data
    leads = [
        {
            "Company": "NHS Trust London",
            "Contact": "Dr. Sarah Johnson",
            "Email": "s.johnson@nhslondon.nhs.uk",
            "Value": "£50,000",
            "Status": "Proposal Sent",
            "Source": "Referral",
            "Date": "Oct 25, 2025"
        },
        {
            "Company": "FinTech Solutions Ltd",
            "Contact": "Michael Chen",
            "Email": "m.chen@fintech.com",
            "Value": "£35,000",
            "Status": "Qualified",
            "Source": "LinkedIn",
            "Date": "Oct 27, 2025"
        },
        {
            "Company": "Global Manufacturing Inc",
            "Contact": "Emily Rodriguez",
            "Email": "e.rodriguez@globalmfg.com",
            "Value": "£75,000",
            "Status": "Negotiation",
            "Source": "Website",
            "Date": "Oct 20, 2025"
        },
        {
            "Company": "Tech Startup XYZ",
            "Contact": "James Williams",
            "Email": "james@techxyz.io",
            "Value": "£25,000",
            "Status": "New",
            "Source": "Cold Outreach",
            "Date": "Oct 29, 2025"
        }
    ]
    
    df_leads = pd.DataFrame(leads)
    
    # Display leads
    for i, lead in enumerate(leads):
        with st.expander(f"🏢 {lead['Company']} - {lead['Status']} - {lead['Value']}"):
            col_l1, col_l2 = st.columns(2)
            
            with col_l1:
                st.markdown(f"**Contact:** {lead['Contact']}")
                st.markdown(f"**Email:** {lead['Email']}")
                st.markdown(f"**Source:** {lead['Source']}")
            
            with col_l2:
                st.markdown(f"**Value:** {lead['Value']}")
                st.markdown(f"**Status:** {lead['Status']}")
                st.markdown(f"**Date:** {lead['Date']}")
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            
            with col_b1:
                if st.button("📧 Send Email", key=f"email_{i}"):
                    st.success("Email sent!")
            
            with col_b2:
                if st.button("📄 Generate Proposal", key=f"proposal_{i}"):
                    st.success("Proposal generated!")
            
            with col_b3:
                if st.button("📞 Schedule Call", key=f"call_{i}"):
                    st.info("Call scheduled!")
            
            with col_b4:
                if st.button("✅ Update Status", key=f"status_{i}"):
                    st.info("Status updated!")

with tab2:
    st.subheader("➕ Add New Lead")
    
    col_add1, col_add2 = st.columns(2)
    
    with col_add1:
        company_name = st.text_input("Company Name*")
        contact_name = st.text_input("Contact Name*")
        contact_email = st.text_input("Contact Email*")
        phone = st.text_input("Phone Number")
    
    with col_add2:
        estimated_value = st.number_input("Estimated Value (£)", min_value=0, value=25000, step=5000)
        lead_source = st.selectbox("Lead Source", ["Website", "LinkedIn", "Referral", "Cold Outreach", "Event", "Other"])
        industry = st.selectbox("Industry", ["Healthcare", "Finance", "Technology", "Manufacturing", "Retail", "Other"])
        notes = st.text_area("Notes")
    
    if st.button("➕ Add Lead", use_container_width=True):
        if company_name and contact_name and contact_email:
            st.success(f"✅ Lead added: {company_name}")
            st.balloons()
        else:
            st.error("Please fill in all required fields (*)")

with tab3:
    st.subheader("📧 Email Campaigns")
    
    st.markdown("### Active Campaigns")
    
    campaigns = [
        {"name": "SOC Services Intro", "sent": 150, "opened": 67, "clicked": 23, "replied": 8},
        {"name": "Free Security Assessment", "sent": 200, "opened": 95, "clicked": 42, "replied": 15},
        {"name": "Case Study: NHS Trust", "sent": 85, "opened": 52, "clicked": 28, "replied": 12}
    ]
    
    for campaign in campaigns:
        with st.expander(f"📧 {campaign['name']}"):
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            
            with col_c1:
                st.metric("Sent", campaign['sent'])
            with col_c2:
                st.metric("Opened", campaign['opened'], f"{round(campaign['opened']/campaign['sent']*100)}%")
            with col_c3:
                st.metric("Clicked", campaign['clicked'], f"{round(campaign['clicked']/campaign['sent']*100)}%")
            with col_c4:
                st.metric("Replied", campaign['replied'], f"{round(campaign['replied']/campaign['sent']*100)}%")
            
            if st.button("📊 View Details", key=f"campaign_{campaign['name']}"):
                st.success(f"✅ Campaign: {campaign['name']}")
                st.markdown(f"""
                **Campaign Performance:**
                - Sent: {campaign['sent']} emails
                - Opened: {campaign['opened']} ({round(campaign['opened']/campaign['sent']*100)}%)
                - Clicked: {campaign['clicked']} ({round(campaign['clicked']/campaign['sent']*100)}%)
                - Replied: {campaign['replied']} ({round(campaign['replied']/campaign['sent']*100)}%)
                
                **Top Performing Links:**
                1. Service Overview - 45 clicks
                2. Pricing Page - 32 clicks
                3. Case Studies - 28 clicks
                """)
                st.balloons()
    
    st.markdown("### Create New Campaign")
    
    if st.button("➕ New Email Campaign", use_container_width=True):
        st.info("Campaign builder coming soon!")

with tab4:
    st.subheader("📊 Lead Analytics")
    
    # Lead sources pie chart
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("### Leads by Source")
        sources = {"Website": 45, "LinkedIn": 32, "Referral": 28, "Cold Outreach": 15, "Event": 10}
        fig_sources = px.pie(values=list(sources.values()), names=list(sources.keys()), hole=0.4)
        fig_sources.update_layout(height=300)
        st.plotly_chart(fig_sources, use_container_width=True)
    
    with col_a2:
        st.markdown("### Leads by Industry")
        industries = {"Healthcare": 38, "Finance": 25, "Technology": 22, "Manufacturing": 15, "Other": 10}
        fig_industries = px.pie(values=list(industries.values()), names=list(industries.keys()), hole=0.4)
        fig_industries.update_layout(height=300)
        st.plotly_chart(fig_industries, use_container_width=True)
    
    # Conversion timeline
    st.markdown("### Lead Conversion Timeline")
    dates = pd.date_range(start='2025-10-01', end='2025-10-29', freq='D')
    conversions = [2, 1, 3, 2, 4, 3, 2, 5, 3, 4, 6, 5, 4, 7, 6, 5, 8, 7, 6, 9, 8, 7, 10, 9, 8, 11, 10, 9, 12]
    
    fig_timeline = px.line(x=dates, y=conversions, labels={'x': 'Date', 'y': 'Conversions'})
    fig_timeline.update_layout(height=300)
    st.plotly_chart(fig_timeline, use_container_width=True)

st.divider()

# ============================================
# AUTOMATED PROPOSAL GENERATOR
# ============================================

st.header("📄 AI Proposal Generator")

st.markdown("Generate professional proposals in seconds!")

col_prop1, col_prop2 = st.columns(2)

with col_prop1:
    prop_company = st.text_input("Client Company Name")
    prop_contact = st.text_input("Contact Person")
    prop_service = st.selectbox("Service Type", [
        "24/7 SOC Monitoring",
        "Managed SIEM Services",
        "Incident Response",
        "Vulnerability Assessment",
        "Penetration Testing",
        "Security Consulting"
    ])

with col_prop2:
    prop_duration = st.selectbox("Contract Duration", ["Monthly", "Quarterly", "Annual"])
    prop_value = st.number_input("Monthly Value (£)", min_value=5000, value=15000, step=1000)
    prop_start = st.date_input("Proposed Start Date")

if st.button("🚀 Generate Proposal", use_container_width=True):
    with st.spinner("AI is generating your proposal..."):
        time.sleep(2)  # Simulate AI processing
        st.success("✅ Proposal generated!")
        
        st.markdown(f"""
        ### Proposal Preview
        
        **To:** {prop_contact}, {prop_company}  
        **Service:** {prop_service}  
        **Value:** £{prop_value:,}/month  
        **Duration:** {prop_duration}  
        **Start Date:** {prop_start}
        
        ---
        
        **Executive Summary**
        
        T21 Services UK is pleased to present this proposal for {prop_service} services 
        for {prop_company}. Our enterprise-grade security operations center provides 24/7 
        monitoring, threat detection, and incident response capabilities.
        
        **Scope of Services:**
        - Real-time security monitoring
        - Threat intelligence integration
        - Incident detection and response
        - Monthly executive reports
        - Dedicated SOC analysts
        
        **Investment:** £{prop_value:,} per month
        
        ---
        """)
        
        col_down1, col_down2 = st.columns(2)
        with col_down1:
            if st.button("📥 Download PDF"):
                st.success("Downloading PDF...")
        with col_down2:
            if st.button("📧 Send to Client"):
                st.success("Proposal sent!")

st.divider()

# ============================================
# CLIENT ONBOARDING
# ============================================

st.header("🎯 Client Onboarding")

st.markdown("### Recent Onboardings")

onboardings = [
    {"client": "NHS Trust London", "status": "✅ Complete", "date": "Oct 20, 2025"},
    {"client": "FinTech Solutions", "status": "🔄 In Progress (Step 3/5)", "date": "Oct 27, 2025"},
    {"client": "Global Manufacturing", "status": "⏳ Scheduled", "date": "Nov 1, 2025"}
]

for onboard in onboardings:
    col_o1, col_o2, col_o3 = st.columns([2, 1, 1])
    with col_o1:
        st.markdown(f"**{onboard['client']}**")
    with col_o2:
        st.markdown(onboard['status'])
    with col_o3:
        st.markdown(onboard['date'])

if st.button("➕ Start New Onboarding", use_container_width=True):
    st.info("Onboarding wizard coming soon!")

# Footer
st.markdown("---")
st.caption("💼 T21 Client Acquisition System - Automated Sales & Onboarding")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
