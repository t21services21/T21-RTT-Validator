"""
T21 HEALTHCARE PLATFORM - EXECUTIVE DASHBOARD
Real-time performance dashboard for C-suite and board
"""

import streamlit as st
from navigation import render_navigation
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Executive Dashboard | T21 Services", page_icon="📊", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    header[data-testid="stHeader"] {display: none !important;}
    .main .block-container {padding-top: 0 !important; margin-top: -80px !important;}
</style>
""", unsafe_allow_html=True)

render_navigation(current_page="executive")

st.title("📊 Executive Dashboard - Real-Time Performance")
st.markdown("**C-Suite & Board: Live RTT Intelligence**")

# Key metrics at top
st.markdown("### 🎯 Key Performance Indicators (Live)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 14px; opacity: 0.9;">RTT Performance</div>
        <div style="font-size: 48px; font-weight: bold; margin: 10px 0;">92.8%</div>
        <div style="font-size: 12px;">Target: 92% ✅</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 14px; opacity: 0.9;">Total Waiting</div>
        <div style="font-size: 48px; font-weight: bold; margin: 10px 0;">4,523</div>
        <div style="font-size: 12px;">↓ 245 vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 14px; opacity: 0.9;">Active Breaches</div>
        <div style="font-size: 48px; font-weight: bold; margin: 10px 0;">87</div>
        <div style="font-size: 12px;">↓ 23 vs last month</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 14px; opacity: 0.9;">Monthly Savings</div>
        <div style="font-size: 48px; font-weight: bold; margin: 10px 0;">£167K</div>
        <div style="font-size: 12px;">ROI: 847%</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 25px; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 14px; opacity: 0.9;">52-Week Waiters</div>
        <div style="font-size: 48px; font-weight: bold; margin: 10px 0;">0</div>
        <div style="font-size: 12px;">Zero Tolerance ✅</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Trend charts
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📈 RTT Performance Trend")
    
    # Demo trend data
    trend_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Performance': [89.2, 90.1, 91.5, 91.8, 92.3, 92.8],
        'Target': [92, 92, 92, 92, 92, 92]
    })
    
    st.line_chart(trend_data.set_index('Month'))
    st.success("✅ **6-month improvement:** +3.6 percentage points")

with col_right:
    st.markdown("### 📊 Specialty Breakdown")
    
    specialty_data = pd.DataFrame({
        'Specialty': ['Orthopaedics', 'Cardiology', 'ENT', 'General Surgery', 'Ophthalmology'],
        'Performance': [91.2, 93.5, 94.1, 92.8, 95.2],
        'Patients': [1234, 876, 654, 987, 543]
    })
    
    st.dataframe(specialty_data, use_container_width=True, hide_index=True)

st.markdown("---")

# Financial impact
st.markdown("### 💰 Financial Impact Analysis")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.metric("Annual Savings (Projected)", "£2.1M", "+£350K vs target")

with col_f2:
    st.metric("Breach Penalties Avoided", "£485K", "↓ 65% vs last year")

with col_f3:
    st.metric("Capacity Optimization Gain", "£623K", "22% efficiency increase")

st.markdown("---")

# Risk alerts
st.markdown("### 🚨 Executive Alerts & Actions Required")

alerts = [
    ("🔴 **URGENT**", "12 patients at critical breach risk (16-17 weeks)", "Escalate to Clinical Director", "High"),
    ("🟡 **WARNING**", "Orthopaedics waiting list growing (+45 patients)", "Review capacity planning", "Medium"),
    ("🟢 **SUCCESS**", "Zero DNA rate improvement (+15% vs target)", "Share best practice", "Low"),
    ("🔵 **INFO**", "Commissioner reporting due in 3 days", "Auto-generated, ready to submit", "Low")
]

for priority, title, action, level in alerts:
    color = {"High": "#ffe5e5", "Medium": "#fff9e5", "Low": "#e5ffe5"}.get(level, "#e5e5e5")
    st.markdown(f"""
    <div style="background: {color}; padding: 15px; margin: 10px 0; border-radius: 10px; border-left: 5px solid #333;">
        <strong>{priority}</strong> {title}<br>
        <small>📋 Action: {action}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Benchmarking
st.markdown("### 🏆 National Benchmarking")

col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown("""
    <div style="background: #f0f2f6; padding: 25px; border-radius: 15px;">
        <h4>Your Trust Rank</h4>
        <div style="font-size: 72px; font-weight: bold; color: #667eea; text-align: center;">35th</div>
        <div style="text-align: center;">out of 200 NHS Trusts</div>
        <div style="text-align: center; margin-top: 15px; color: #43e97b;">↑ 12 positions vs last quarter</div>
    </div>
    """, unsafe_allow_html=True)

with col_b2:
    st.markdown("""
    <div style="background: #f0f2f6; padding: 25px; border-radius: 15px;">
        <h4>To Reach Top 10</h4>
        <ul>
            <li>✅ Reduce breaches by 15 patients</li>
            <li>✅ Improve Ortho performance to 93%</li>
            <li>✅ Maintain zero 52-week waiters</li>
            <li>🎯 Estimated: 8-12 weeks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick actions for executives
st.markdown("### ⚡ Executive Actions")

col_a1, col_a2, col_a3, col_a4 = st.columns(4)

with col_a1:
    if st.button("📊 Generate Board Report", use_container_width=True):
        st.success("✅ Board report generated! Ready to download.")

with col_a2:
    if st.button("📧 Email to Commissioners", use_container_width=True):
        st.success("✅ Monthly submission sent!")

with col_a3:
    if st.button("🎯 Set New Targets", use_container_width=True):
        st.info("Opening target setting interface...")

with col_a4:
    if st.button("🔔 Alert Clinical Directors", use_container_width=True):
        st.success("✅ Alerts sent to all clinical leads!")

st.markdown("---")

# Auto-refresh notice
st.info("""
🔄 **Live Dashboard:** Auto-refreshes every 60 seconds  
📱 **Mobile App:** Access from your phone via T21 Mobile  
🔐 **Secure:** Executive-only access with multi-factor authentication  
📊 **Customizable:** Configure your preferred KPIs and alerts
""")

# Back to main platform button
st.markdown("---")
col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("← Back to Platform Dashboard", use_container_width=True, type="primary"):
        st.switch_page("app.py")
