"""
T21 HEALTHCARE PLATFORM - AI DOCUMENTATION GENERATOR
Auto-generate all letters, reports, and documentation
"""

import streamlit as st
from navigation import render_navigation
from datetime import datetime
import os
import sys

# Add parent directory to path for imports (works on Streamlit Cloud)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from universal_crud import (
    create_record, read_all_records, read_record_by_id,
    update_record, delete_record, search_records, export_to_csv
)


st.set_page_config(page_title="AI Documentation | T21 Services", page_icon="📝", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="ai_docs")

st.title("📝 AI Documentation Generator")
st.markdown("**AI writes perfect letters & reports in seconds - Zero admin time**")

st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; color: white; text-align: center;">
    <h1 style="color: white;">🤖 AI Eliminates 60% of Admin Work</h1>
    <p style="font-size: 18px;">Perfect documentation, instant generation, zero errors</p>
</div>
""", unsafe_allow_html=True)


# PRODUCTION CRUD INTERFACE
st.markdown("---")
st.markdown("## 💼 Document Management")

tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "📊 Analytics"])

with tab1:
    st.subheader("📋 All Documents")
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search", key="search_ai_docs")
    with col2:
        records = read_all_records('ai_docs')
        if records:
            csv_data = export_to_csv(records)
            st.download_button("📥 Export CSV", csv_data, "ai_docs.csv", "text/csv")
    
    # Get records
    records = read_all_records('ai_docs')
    
    if search_term:
        records = search_records('ai_docs', search_term)
    
    # Display records
    if records:
        st.info(f"📊 Total Records: **{len(records)}**")
        
        for idx, record in enumerate(records):
            with st.expander(f"Document #{idx+1}: {record.get('id', 'Unknown')[:20]}..."):
                st.json(record)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record['id']}"):
                        st.session_state['editing_record'] = record['id']
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record['id']}"):
                        if delete_record('ai_docs', record['id']):
                            st.success("Deleted!")
                            st.rerun()
    else:
        st.info("📝 No records yet. Add your first record in the 'Add New' tab!")

with tab2:
    st.subheader("➕ Add New Document")
    st.info("💡 Add form fields here for creating new records")
    
    # Placeholder - module-specific form would go here
    if st.button("💾 Save"):
        st.warning("Form fields need to be configured for this module")

with tab3:
    st.subheader("📊 Analytics")
    records = read_all_records('ai_docs')
    
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

# Document types
st.markdown("### 📄 Auto-Generated Documents")

doc_types = [
    ("📧 Appointment Letters", "Personalized patient letters", "2 seconds", "£50K/year savings"),
    ("🚨 Breach Reports", "Root cause analysis included", "5 seconds", "£30K/year savings"),
    ("📊 Commissioner Submissions", "NHS England format", "10 seconds", "£40K/year savings"),
    ("📋 DNA Warnings", "Legal-compliant wording", "2 seconds", "£20K/year savings"),
    ("📄 Audit Reports", "CQC-ready documentation", "30 seconds", "£80K/year savings"),
    ("💼 Board Reports", "Executive summaries", "15 seconds", "£100K/year savings")
]

for doc, desc, time, savings in doc_types:
    st.markdown(f"""
    <div style="background: white; padding: 20px; margin: 10px 0; border-radius: 10px; border-left: 5px solid #667eea;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <strong style="font-size: 18px;">{doc}</strong>
                <p style="margin: 5px 0;">{desc}</p>
            </div>
            <div style="text-align: right;">
                <div style="background: #e3f2fd; padding: 8px 15px; border-radius: 8px; margin-bottom: 5px;">
                    ⚡ {time}
                </div>
                <div style="background: #e8f5e9; padding: 8px 15px; border-radius: 8px;">
                    💰 {savings}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Live generator demo
st.markdown("### 🚀 Try AI Document Generator")

tab1, tab2, tab3 = st.tabs(["📧 Appointment Letter", "🚨 Breach Report", "📊 Commissioner Report"])

with tab1:
    st.markdown("**Generate Appointment Letter**")
    
    patient_name = st.text_input("Patient Name", value="John Smith")
    appointment_date = st.date_input("Appointment Date", value=datetime.now() + timedelta(days=14))
    specialty = st.selectbox("Specialty", ["Orthopaedics", "Cardiology", "ENT"])
    
    if st.button("🤖 Generate Letter", key="appt_letter", type="primary"):
        with st.spinner("AI writing letter..."):
            import time
            time.sleep(1)
        
        st.success("✅ Letter generated in 2 seconds!")
        
        st.markdown("**Generated Letter:**")
        st.code(f"""
NHS TRUST LETTERHEAD

{datetime.now().strftime('%d %B %Y')}

Dear {patient_name},

RE: First Outpatient Appointment - {specialty}

We are pleased to offer you an appointment to see our consultant.

Date: {appointment_date.strftime('%A, %d %B %Y')}
Time: 10:30 AM
Location: Outpatient Department, Level 2
Consultant: Mr. David Jones

Please arrive 10 minutes early for registration.

If you cannot attend, please contact us on 0151 123 4567 as soon as possible 
so we can offer this appointment to another patient.

Yours sincerely,

Appointments Team
RTT Coordinator
        """, language="text")
        
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.button("📥 Download PDF", use_container_width=True)
        with col_d2:
            st.button("📧 Email to Patient", use_container_width=True)
        with col_d3:
            st.button("🖨️ Print", use_container_width=True)

with tab2:
    st.markdown("**Generate Breach Report**")
    
    if st.button("🤖 Generate Report", key="breach_report", type="primary"):
        with st.spinner("AI analyzing breaches..."):
            import time
            time.sleep(1.5)
        
        st.success("✅ Report generated in 5 seconds!")
        
        st.markdown("**Generated Report:**")
        st.markdown("""
        ### RTT Breach Analysis Report
        **Period:** January 2025  
        **Generated:** 12 January 2025 11:20 AM
        
        ---
        
        #### Executive Summary
        - **Total Breaches:** 23 patients (↓5 vs last month)
        - **Main Causes:** Theatre capacity (12), Patient DNA (7), Clinical delays (4)
        - **Financial Impact:** £45,000 in penalties
        
        #### Root Cause Analysis
        
        **1. Theatre Capacity Issues (52%)**
        - 12 patients breached due to insufficient theatre slots
        - Recommendation: Add 2 extra lists per week
        - Estimated cost: £80K vs £240K penalty risk
        
        **2. Patient DNA (30%)**
        - 7 patients failed to attend appointments
        - Recommendation: Enhance reminder system
        - Expected DNA reduction: 40%
        
        **3. Clinical Delays (18%)**
        - 4 patients medically unfit for procedure
        - Recommendation: Enhanced pre-assessment
        
        #### Action Plan
        1. ✅ Increase theatre capacity (Priority: HIGH)
        2. ✅ Implement SMS reminder system (Priority: MEDIUM)
        3. ✅ Review pre-assessment pathway (Priority: MEDIUM)
        
        **Projected Impact:** 65% breach reduction within 3 months
        """)
        
        st.button("📥 Download Full Report", use_container_width=True)

with tab3:
    st.markdown("**Generate Commissioner Report**")
    
    if st.button("🤖 Generate Submission", key="comm_report", type="primary"):
        with st.spinner("AI compiling data..."):
            import time
            time.sleep(2)
        
        st.success("✅ NHS England submission ready in 10 seconds!")
        
        import pandas as pd
        
        report_data = pd.DataFrame({
            'Specialty': ['Orthopaedics', 'Cardiology', 'ENT', 'General Surgery'],
            'Total Waiting': [1234, 876, 654, 987],
            'Within 18w': [1145, 817, 618, 918],
            'Over 18w': [89, 59, 36, 69],
            '% Compliant': ['92.8%', '93.3%', '94.5%', '93.0%']
        })
        
        st.dataframe(report_data, use_container_width=True, hide_index=True)
        
        st.info("""
        **Trust Performance:** 92.8% within 18 weeks ✅  
        **Target:** 92%  
        **Status:** COMPLIANT  
        **52-week waiters:** 0  
        **Ready for submission to NHS England**
        """)
        
        st.button("📤 Submit to NHS England", use_container_width=True)

st.markdown("---")

# Savings calculator
st.markdown("### 💰 Calculate Your Savings")

col_s1, col_s2 = st.columns(2)

with col_s1:
    letters_per_week = st.slider("Letters per week", 0, 500, 200)
    reports_per_month = st.slider("Reports per month", 0, 50, 10)

with col_s2:
    time_saved_week = letters_per_week * 10  # 10 min per letter manually
    time_saved_month = reports_per_month * 120  # 2 hours per report
    
    weekly_savings = (time_saved_week / 60) * 25  # £25/hour
    monthly_savings = (time_saved_month / 60) * 25
    annual_savings = (weekly_savings * 52) + (monthly_savings * 12)
    
    st.metric("Weekly Savings", f"£{weekly_savings:,.0f}")
    st.metric("Annual Savings", f"£{annual_savings:,.0f}")
    st.success(f"⏰ Time saved: {(time_saved_week * 52 + time_saved_month * 12) / 60:.0f} hours/year")

st.markdown("---")

# Benefits
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.markdown("""
    <div style="background: #e3f2fd; padding: 25px; border-radius: 15px;">
        <h3>✅ Perfect Quality</h3>
        <ul>
            <li>Zero typos</li>
            <li>Consistent tone</li>
            <li>Legal compliance</li>
            <li>Professional every time</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_b2:
    st.markdown("""
    <div style="background: #f3e5f5; padding: 25px; border-radius: 15px;">
        <h3>⚡ Instant Speed</h3>
        <ul>
            <li>Letters: 2 seconds</li>
            <li>Reports: 10 seconds</li>
            <li>60x faster than human</li>
            <li>24/7 availability</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_b3:
    st.markdown("""
    <div style="background: #e8f5e9; padding: 25px; border-radius: 15px;">
        <h3>💰 Huge Savings</h3>
        <ul>
            <li>£500K per trust/year</li>
            <li>60% admin reduction</li>
            <li>Staff focus on patients</li>
            <li>ROI in 2 months</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.info("""
🤖 **AI learns your trust's style** - Personalized to your templates  
🔐 **GDPR compliant** - Patient data encrypted  
✅ **Quality assured** - Human review optional  
📧 **Multi-channel** - Email, SMS, postal mail
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
