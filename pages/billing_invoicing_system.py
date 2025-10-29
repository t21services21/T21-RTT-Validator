"""
BILLING & INVOICING SYSTEM
Automated billing, payments, and financial management

Features:
- Automated invoicing
- Payment processing
- Subscription management
- Revenue tracking
- Financial reports
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Billing System", page_icon="💰", layout="wide")

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
st.title("💰 Billing & Invoicing System")
st.markdown(f"**User:** {user_email}")
st.markdown("**Automated Financial Management**")

st.divider()

# ============================================
# FINANCIAL DASHBOARD
# ============================================

st.header("📊 Financial Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Monthly Revenue", "£127,500", "+£23,500")

with col2:
    st.metric("📈 Annual Revenue", "£1,245,000", "+18%")

with col3:
    st.metric("💳 Outstanding", "£45,000", "-£12,000")

with col4:
    st.metric("✅ Paid This Month", "£82,500", "+15%")

# Revenue chart
st.subheader("Revenue Trend (Last 12 Months)")

months = ['Nov 24', 'Dec 24', 'Jan 25', 'Feb 25', 'Mar 25', 'Apr 25', 'May 25', 'Jun 25', 'Jul 25', 'Aug 25', 'Sep 25', 'Oct 25']
revenue = [85000, 92000, 88000, 95000, 102000, 98000, 105000, 112000, 108000, 115000, 122000, 127500]

fig_revenue = px.line(x=months, y=revenue, labels={'x': 'Month', 'y': 'Revenue (£)'})
fig_revenue.update_layout(height=300)
st.plotly_chart(fig_revenue, use_container_width=True)

st.divider()

# ============================================
# INVOICES
# ============================================

st.header("📄 Invoices")

tab1, tab2, tab3, tab4 = st.tabs(["📋 All Invoices", "⏳ Pending", "✅ Paid", "➕ Create Invoice"])

with tab1:
    # Filter options
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        status_filter = st.selectbox("Status", ["All", "Paid", "Pending", "Overdue", "Draft"])
    
    with col_f2:
        client_filter = st.selectbox("Client", ["All Clients", "NHS Trust London", "FinTech Solutions", "Global Manufacturing"])
    
    with col_f3:
        date_filter = st.selectbox("Period", ["All Time", "This Month", "Last Month", "This Quarter", "This Year"])
    
    # Sample invoices
    invoices = [
        {
            "invoice_no": "INV-2025-101",
            "client": "NHS Trust London",
            "amount": "£15,000",
            "status": "✅ Paid",
            "date": "Oct 1, 2025",
            "due": "Oct 31, 2025",
            "paid_date": "Oct 28, 2025"
        },
        {
            "invoice_no": "INV-2025-102",
            "client": "FinTech Solutions",
            "amount": "£12,500",
            "status": "⏳ Pending",
            "date": "Oct 15, 2025",
            "due": "Nov 15, 2025",
            "paid_date": "-"
        },
        {
            "invoice_no": "INV-2025-103",
            "client": "Global Manufacturing",
            "amount": "£25,000",
            "status": "🔴 Overdue",
            "date": "Sep 15, 2025",
            "due": "Oct 15, 2025",
            "paid_date": "-"
        },
        {
            "invoice_no": "INV-2025-104",
            "client": "Tech Startup XYZ",
            "amount": "£8,000",
            "status": "✅ Paid",
            "date": "Oct 10, 2025",
            "due": "Nov 10, 2025",
            "paid_date": "Oct 25, 2025"
        }
    ]
    
    for invoice in invoices:
        with st.expander(f"{invoice['status']} {invoice['invoice_no']} - {invoice['client']} - {invoice['amount']}"):
            col_i1, col_i2 = st.columns(2)
            
            with col_i1:
                st.markdown(f"**Invoice:** {invoice['invoice_no']}")
                st.markdown(f"**Client:** {invoice['client']}")
                st.markdown(f"**Amount:** {invoice['amount']}")
                st.markdown(f"**Status:** {invoice['status']}")
            
            with col_i2:
                st.markdown(f"**Issue Date:** {invoice['date']}")
                st.markdown(f"**Due Date:** {invoice['due']}")
                st.markdown(f"**Paid Date:** {invoice['paid_date']}")
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            
            with col_b1:
                if st.button("👁️ View", key=f"view_{invoice['invoice_no']}"):
                    st.info("Loading invoice...")
            
            with col_b2:
                if st.button("📥 Download PDF", key=f"pdf_{invoice['invoice_no']}"):
                    st.success("Downloading PDF...")
            
            with col_b3:
                if st.button("📧 Send Email", key=f"email_{invoice['invoice_no']}"):
                    st.success("Email sent!")
            
            with col_b4:
                if invoice['status'] == "⏳ Pending":
                    if st.button("✅ Mark Paid", key=f"paid_{invoice['invoice_no']}"):
                        st.success("Marked as paid!")

with tab2:
    st.subheader("Pending Invoices")
    
    pending = [inv for inv in invoices if inv['status'] == "⏳ Pending"]
    
    if pending:
        total_pending = sum([float(inv['amount'].replace('£', '').replace(',', '')) for inv in pending])
        st.info(f"💰 Total Pending: £{total_pending:,.2f}")
        
        for inv in pending:
            col_p1, col_p2, col_p3, col_p4 = st.columns([2, 2, 1, 1])
            with col_p1:
                st.markdown(f"**{inv['invoice_no']}**")
            with col_p2:
                st.markdown(inv['client'])
            with col_p3:
                st.markdown(inv['amount'])
            with col_p4:
                if st.button("Send Reminder", key=f"remind_{inv['invoice_no']}"):
                    st.success("Reminder sent!")
    else:
        st.success("✅ No pending invoices!")

with tab3:
    st.subheader("Paid Invoices")
    
    paid = [inv for inv in invoices if inv['status'] == "✅ Paid"]
    
    if paid:
        total_paid = sum([float(inv['amount'].replace('£', '').replace(',', '')) for inv in paid])
        st.success(f"✅ Total Paid This Month: £{total_paid:,.2f}")
        
        for inv in paid:
            st.markdown(f"✅ **{inv['invoice_no']}** - {inv['client']} - {inv['amount']} (Paid: {inv['paid_date']})")

with tab4:
    st.subheader("➕ Create New Invoice")
    
    col_new1, col_new2 = st.columns(2)
    
    with col_new1:
        inv_client = st.selectbox("Select Client*", ["NHS Trust London", "FinTech Solutions", "Global Manufacturing", "Tech Startup XYZ"])
        inv_service = st.selectbox("Service*", ["24/7 SOC Monitoring", "Managed SIEM", "Incident Response", "Consulting", "Training"])
        inv_amount = st.number_input("Amount (£)*", min_value=0, value=15000, step=1000)
    
    with col_new2:
        inv_date = st.date_input("Invoice Date*")
        inv_due = st.date_input("Due Date*")
        inv_notes = st.text_area("Notes")
    
    if st.button("➕ Create Invoice", use_container_width=True):
        if inv_client and inv_service and inv_amount:
            st.success(f"✅ Invoice created: INV-2025-{random.randint(105, 999)}")
            st.balloons()
        else:
            st.error("Please fill in all required fields (*)")

st.divider()

# ============================================
# SUBSCRIPTIONS
# ============================================

st.header("🔄 Subscription Management")

subscriptions = [
    {
        "client": "NHS Trust London",
        "plan": "Enterprise SOC",
        "amount": "£15,000/month",
        "status": "🟢 Active",
        "next_billing": "Nov 1, 2025",
        "auto_renew": True
    },
    {
        "client": "FinTech Solutions",
        "plan": "Professional SOC",
        "amount": "£12,500/month",
        "status": "🟢 Active",
        "next_billing": "Nov 15, 2025",
        "auto_renew": True
    },
    {
        "client": "Global Manufacturing",
        "plan": "Enterprise SOC",
        "amount": "£25,000/month",
        "status": "🟡 Payment Issue",
        "next_billing": "Overdue",
        "auto_renew": True
    }
]

for sub in subscriptions:
    with st.expander(f"{sub['status']} {sub['client']} - {sub['plan']} - {sub['amount']}"):
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown(f"**Client:** {sub['client']}")
            st.markdown(f"**Plan:** {sub['plan']}")
            st.markdown(f"**Amount:** {sub['amount']}")
        
        with col_s2:
            st.markdown(f"**Status:** {sub['status']}")
            st.markdown(f"**Next Billing:** {sub['next_billing']}")
            st.markdown(f"**Auto-Renew:** {'✅ Yes' if sub['auto_renew'] else '❌ No'}")
        
        col_sb1, col_sb2, col_sb3 = st.columns(3)
        
        with col_sb1:
            if st.button("📝 Edit Plan", key=f"edit_{sub['client']}"):
                st.info("Editing plan...")
        
        with col_sb2:
            if st.button("⏸️ Pause", key=f"pause_{sub['client']}"):
                st.warning("Subscription paused")
        
        with col_sb3:
            if st.button("❌ Cancel", key=f"cancel_{sub['client']}"):
                st.error("Subscription cancelled")

st.divider()

# ============================================
# PAYMENT PROCESSING
# ============================================

st.header("💳 Payment Processing")

col_pay1, col_pay2 = st.columns(2)

with col_pay1:
    st.subheader("Recent Payments")
    
    payments = [
        {"date": "Oct 28, 2025", "client": "NHS Trust London", "amount": "£15,000", "method": "Bank Transfer"},
        {"date": "Oct 25, 2025", "client": "Tech Startup XYZ", "amount": "£8,000", "method": "Credit Card"},
        {"date": "Oct 22, 2025", "client": "Retail Corp", "amount": "£10,500", "method": "PayPal"},
    ]
    
    for payment in payments:
        st.success(f"✅ {payment['date']} - {payment['client']} - {payment['amount']} ({payment['method']})")

with col_pay2:
    st.subheader("Payment Methods")
    
    methods = {
        "Bank Transfer": 45,
        "Credit Card": 35,
        "PayPal": 15,
        "Other": 5
    }
    
    fig_methods = px.pie(values=list(methods.values()), names=list(methods.keys()), hole=0.4)
    fig_methods.update_layout(height=300)
    st.plotly_chart(fig_methods, use_container_width=True)

st.divider()

# ============================================
# FINANCIAL REPORTS
# ============================================

st.header("📊 Financial Reports")

report_tabs = st.tabs(["📈 Revenue Report", "💰 Profit & Loss", "📉 Cash Flow", "📊 Client Revenue"])

with report_tabs[0]:
    st.subheader("Revenue Report")
    
    col_r1, col_r2, col_r3 = st.columns(3)
    
    with col_r1:
        st.metric("This Month", "£127,500", "+18%")
    with col_r2:
        st.metric("This Quarter", "£357,500", "+22%")
    with col_r3:
        st.metric("This Year", "£1,245,000", "+18%")
    
    # Revenue breakdown
    st.subheader("Revenue by Service")
    
    services = {
        "24/7 SOC Monitoring": 750000,
        "Managed SIEM": 285000,
        "Incident Response": 125000,
        "Consulting": 55000,
        "Training": 30000
    }
    
    fig_services = px.bar(x=list(services.keys()), y=list(services.values()), 
                          labels={'x': 'Service', 'y': 'Revenue (£)'})
    fig_services.update_layout(height=400)
    st.plotly_chart(fig_services, use_container_width=True)

with report_tabs[1]:
    st.subheader("Profit & Loss Statement")
    
    pl_data = {
        "Category": ["Revenue", "Cost of Sales", "Gross Profit", "Operating Expenses", "Net Profit"],
        "Amount": [1245000, 498000, 747000, 373500, 373500],
        "Percentage": [100, 40, 60, 30, 30]
    }
    
    df_pl = pd.DataFrame(pl_data)
    
    st.dataframe(df_pl, use_container_width=True, hide_index=True)
    
    st.success(f"💰 Net Profit Margin: 30%")

with report_tabs[2]:
    st.subheader("Cash Flow Statement")
    
    st.info("Cash flow analysis coming soon!")

with report_tabs[3]:
    st.subheader("Revenue by Client")
    
    client_revenue = {
        "NHS Trust London": 180000,
        "FinTech Solutions": 150000,
        "Global Manufacturing": 300000,
        "Tech Startup XYZ": 96000,
        "Retail Corp": 126000,
        "Others": 393000
    }
    
    fig_clients = px.pie(values=list(client_revenue.values()), names=list(client_revenue.keys()))
    fig_clients.update_layout(height=400)
    st.plotly_chart(fig_clients, use_container_width=True)

st.divider()

# ============================================
# AUTOMATED REMINDERS
# ============================================

st.header("📧 Automated Payment Reminders")

col_rem1, col_rem2 = st.columns(2)

with col_rem1:
    st.subheader("Reminder Settings")
    
    reminder_7days = st.checkbox("Send reminder 7 days before due date", value=True)
    reminder_3days = st.checkbox("Send reminder 3 days before due date", value=True)
    reminder_due = st.checkbox("Send reminder on due date", value=True)
    reminder_overdue = st.checkbox("Send reminder for overdue invoices (daily)", value=True)
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved!")

with col_rem2:
    st.subheader("Recent Reminders Sent")
    
    reminders = [
        {"date": "Oct 29, 2025", "client": "FinTech Solutions", "type": "7-day reminder"},
        {"date": "Oct 28, 2025", "client": "Global Manufacturing", "type": "Overdue notice"},
        {"date": "Oct 27, 2025", "client": "Tech Startup XYZ", "type": "3-day reminder"},
    ]
    
    for reminder in reminders:
        st.info(f"📧 {reminder['date']} - {reminder['client']} ({reminder['type']})")

st.divider()

# ============================================
# EXPORT OPTIONS
# ============================================

st.header("📥 Export Options")

col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    if st.button("📊 Export to Excel", use_container_width=True):
        st.success("Exporting to Excel...")

with col_exp2:
    if st.button("📄 Export to PDF", use_container_width=True):
        st.success("Exporting to PDF...")

with col_exp3:
    if st.button("💾 Export to CSV", use_container_width=True):
        st.success("Exporting to CSV...")

# Footer
st.markdown("---")
st.caption("💰 T21 Billing & Invoicing System - Automated Financial Management")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
