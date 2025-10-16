"""
APPROVAL UI - Request & Approval Interface

FEATURES:
- Submit upgrade requests (Tier 0 → 1, 2, 3)
- Submit module access requests
- View your request status
- Admin approval dashboard
- Bulk approve
"""

import streamlit as st
from approval_system import (
    submit_tier_upgrade_request,
    submit_module_access_request,
    submit_staff_account_request,
    get_pending_requests,
    get_user_requests,
    get_request_by_id,
    approve_request,
    reject_request,
    get_approval_statistics
)


def render_user_request_page():
    """Student/User page to submit and track requests"""
    
    st.header("📝 My Requests")
    
    if 'user_email' not in st.session_state:
        st.warning("Please login to submit requests")
        return
    
    user_email = st.session_state.user_email
    user_name = st.session_state.get('user_name', 'User')
    
    # Tabs
    tab1, tab2 = st.tabs(["📤 Submit Request", "📊 My Requests"])
    
    with tab1:
        render_submit_request(user_email, user_name)
    
    with tab2:
        render_my_requests(user_email)


def render_submit_request(user_email: str, user_name: str):
    """Form to submit new request"""
    
    st.subheader("📤 Submit New Request")
    
    request_type = st.selectbox(
        "What would you like to request?",
        ["Tier Upgrade", "Module Access", "Staff Account", "Other"],
        key="request_type_select"
    )
    
    if request_type == "Tier Upgrade":
        render_tier_upgrade_form(user_email, user_name)
    
    elif request_type == "Module Access":
        render_module_access_form(user_email, user_name)
    
    elif request_type == "Staff Account":
        render_staff_account_form(user_email, user_name)
    
    else:
        st.info("Other request types coming soon. Please contact admin@t21services.co.uk")


def render_tier_upgrade_form(user_email: str, user_name: str):
    """Tier upgrade request form"""
    
    st.markdown("### 🎯 Tier Upgrade Request")
    
    st.info("""
    **Tier Pricing:**
    - 💰 **Tier 0 (Trial):** FREE - Limited access
    - 📚 **Tier 1 (Practice):** £499/6 months - Full access
    - 🎓 **Tier 2 (Certified):** £1,299/12 months - Certification included
    - 💼 **Tier 3 (Premium):** £1,799/12 months - Career support included
    """)
    
    with st.form("tier_upgrade_form"):
        current_tier = st.selectbox(
            "Your Current Tier",
            ["Tier 0 (Trial)", "Tier 1 (Practice)", "Tier 2 (Certified)"],
            key="current_tier"
        )
        
        requested_tier = st.selectbox(
            "Requested Tier",
            ["Tier 1 (Practice)", "Tier 2 (Certified)", "Tier 3 (Premium)"],
            key="requested_tier"
        )
        
        reason = st.text_area(
            "Why do you want to upgrade? (Optional)",
            placeholder="E.g., Need certification for job application",
            height=100,
            key="upgrade_reason"
        )
        
        payment_info = st.text_input(
            "Payment Reference (if already paid)",
            placeholder="E.g., PayPal transaction ID",
            key="payment_ref"
        )
        
        submit = st.form_submit_button("📤 Submit Request", type="primary")
        
        if submit:
            # Submit request
            request = submit_tier_upgrade_request(
                requester_email=user_email,
                requester_name=user_name,
                current_tier=current_tier,
                requested_tier=requested_tier,
                reason=f"{reason}\n\nPayment Reference: {payment_info}" if payment_info else reason
            )
            
            st.success("✅ Your upgrade request has been submitted!")
            st.info(f"Request ID: {request.id}")
            st.info("You will be notified via email when your request is reviewed.")
            st.balloons()


def render_module_access_form(user_email: str, user_name: str):
    """Module access request form"""
    
    st.markdown("### 🔐 Module Access Request")
    
    with st.form("module_access_form"):
        module_name = st.selectbox(
            "Which module do you need access to?",
            [
                "Information Governance",
                "Partial Booking List",
                "Advanced Booking System",
                "Cancer Pathways",
                "MDT Coordination",
                "PTL Management",
                "Executive Dashboard",
                "Other"
            ],
            key="module_name"
        )
        
        if module_name == "Other":
            module_name = st.text_input("Specify module name", key="other_module")
        
        reason = st.text_area(
            "Why do you need access to this module?*",
            placeholder="E.g., Required for my role as RTT Coordinator",
            height=120,
            key="module_reason"
        )
        
        submit = st.form_submit_button("📤 Submit Request", type="primary")
        
        if submit and reason:
            request = submit_module_access_request(
                requester_email=user_email,
                requester_name=user_name,
                module_name=module_name,
                reason=reason
            )
            
            st.success("✅ Your module access request has been submitted!")
            st.info(f"Request ID: {request.id}")


def render_staff_account_form(user_email: str, user_name: str):
    """Staff account request form"""
    
    st.markdown("### 👤 Staff Account Request")
    
    with st.form("staff_account_form"):
        role = st.selectbox(
            "Requested Role",
            ["Teacher", "Staff", "Admin"],
            key="staff_role"
        )
        
        organization = st.text_input(
            "Organization/Institution",
            placeholder="E.g., NHS Trust, Training Provider",
            key="organization"
        )
        
        job_title = st.text_input(
            "Job Title",
            placeholder="E.g., RTT Coordinator",
            key="job_title"
        )
        
        reason = st.text_area(
            "Why do you need a staff account?*",
            placeholder="E.g., I will be teaching RTT courses to students",
            height=120,
            key="staff_reason"
        )
        
        submit = st.form_submit_button("📤 Submit Request", type="primary")
        
        if submit and reason:
            request = submit_staff_account_request(
                requester_email=user_email,
                requester_name=user_name,
                requested_role=role,
                reason=reason,
                additional_info={
                    'organization': organization,
                    'job_title': job_title
                }
            )
            
            st.success("✅ Your staff account request has been submitted!")
            st.info(f"Request ID: {request.id}")


def render_my_requests(user_email: str):
    """Show user's request history"""
    
    st.subheader("📊 Your Requests")
    
    requests = get_user_requests(user_email)
    
    if not requests:
        st.info("📭 You haven't submitted any requests yet")
        return
    
    # Summary
    pending = len([r for r in requests if r.status == 'pending'])
    approved = len([r for r in requests if r.status == 'approved'])
    rejected = len([r for r in requests if r.status == 'rejected'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏳ Pending", pending)
    with col2:
        st.metric("✅ Approved", approved)
    with col3:
        st.metric("❌ Rejected", rejected)
    
    st.markdown("---")
    
    # Display requests
    for request in requests:
        render_request_card(request, is_admin=False)


def render_request_card(request, is_admin: bool = False):
    """Render single request card"""
    
    # Status icons and colors
    status_config = {
        'pending': {'icon': '⏳', 'color': '#ffc107', 'label': 'Pending Review'},
        'approved': {'icon': '✅', 'color': '#28a745', 'label': 'Approved'},
        'rejected': {'icon': '❌', 'color': '#dc3545', 'label': 'Rejected'}
    }
    
    config = status_config.get(request.status, status_config['pending'])
    
    with st.expander(f"{config['icon']} {request.request_type.replace('_', ' ').title()} - {config['label']}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Request Type:** {request.request_type.replace('_', ' ').title()}")
            st.markdown(f"**Requester:** {request.requester_name} ({request.requester_email})")
            if request.current_tier:
                st.markdown(f"**Current Tier:** {request.current_tier}")
            if request.requested_tier:
                st.markdown(f"**Requested Tier:** {request.requested_tier}")
            if request.requested_item:
                st.markdown(f"**Requested Item:** {request.requested_item}")
        
        with col2:
            st.markdown(f"**Status:** {config['label']}")
            st.markdown(f"**Priority:** {request.priority.title()}")
            st.markdown(f"**Submitted:** {request.submitted_at[:10]}")
            if request.reviewed_at:
                st.markdown(f"**Reviewed:** {request.reviewed_at[:10]}")
        
        st.markdown("---")
        st.markdown(f"**Reason:**")
        st.markdown(request.reason)
        
        if request.reviewer_comment:
            st.markdown(f"**Admin Comment:**")
            st.info(request.reviewer_comment)
        
        # Admin actions
        if is_admin and request.status == 'pending':
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Approve", key=f"approve_{request.id}", type="primary"):
                    st.session_state[f'approving_{request.id}'] = True
                    st.rerun()
            
            with col2:
                if st.button("❌ Reject", key=f"reject_{request.id}"):
                    st.session_state[f'rejecting_{request.id}'] = True
                    st.rerun()
            
            # Approval form
            if st.session_state.get(f'approving_{request.id}', False):
                with st.form(key=f"approve_form_{request.id}"):
                    comment = st.text_area("Comment (optional)", key=f"approve_comment_{request.id}")
                    submit = st.form_submit_button("✅ Confirm Approval")
                    
                    if submit:
                        admin_email = st.session_state.user_email
                        admin_name = st.session_state.get('user_name', 'Admin')
                        approve_request(request.id, admin_email, admin_name, comment)
                        st.success("✅ Request approved!")
                        del st.session_state[f'approving_{request.id}']
                        st.rerun()
            
            # Rejection form
            if st.session_state.get(f'rejecting_{request.id}', False):
                with st.form(key=f"reject_form_{request.id}"):
                    reason = st.text_area("Rejection reason*", key=f"reject_reason_{request.id}")
                    submit = st.form_submit_button("❌ Confirm Rejection")
                    
                    if submit and reason:
                        admin_email = st.session_state.user_email
                        admin_name = st.session_state.get('user_name', 'Admin')
                        reject_request(request.id, admin_email, admin_name, reason)
                        st.success("Request rejected")
                        del st.session_state[f'rejecting_{request.id}']
                        st.rerun()


def render_admin_approval_dashboard():
    """Admin dashboard for managing approval requests"""
    
    st.header("🔧 Approval Dashboard")
    
    # Statistics
    stats = get_approval_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⏳ Pending", stats['pending'])
    with col2:
        st.metric("✅ Approved", stats['approved'])
    with col3:
        st.metric("❌ Rejected", stats['rejected'])
    with col4:
        st.metric("📊 Approval Rate", f"{stats['approval_rate']:.1f}%")
    
    st.info(f"⏱️ Average approval time: {stats['avg_approval_time_hours']} hours")
    
    st.markdown("---")
    
    # Tabs for different request types
    tab1, tab2, tab3, tab4 = st.tabs([
        "⏳ All Pending",
        "🎯 Tier Upgrades",
        "🔐 Module Access",
        "👤 Staff Accounts"
    ])
    
    with tab1:
        st.subheader("⏳ All Pending Requests")
        pending = get_pending_requests()
        if pending:
            for request in pending:
                render_request_card(request, is_admin=True)
        else:
            st.success("✅ No pending requests!")
    
    with tab2:
        st.subheader("🎯 Tier Upgrade Requests")
        tier_requests = get_pending_requests(request_type='tier_upgrade')
        if tier_requests:
            for request in tier_requests:
                render_request_card(request, is_admin=True)
        else:
            st.info("No pending tier upgrade requests")
    
    with tab3:
        st.subheader("🔐 Module Access Requests")
        module_requests = get_pending_requests(request_type='module_access')
        if module_requests:
            for request in module_requests:
                render_request_card(request, is_admin=True)
        else:
            st.info("No pending module access requests")
    
    with tab4:
        st.subheader("👤 Staff Account Requests")
        staff_requests = get_pending_requests(request_type='staff_account')
        if staff_requests:
            for request in staff_requests:
                render_request_card(request, is_admin=True)
        else:
            st.info("No pending staff account requests")


# Export
__all__ = [
    'render_user_request_page',
    'render_admin_approval_dashboard'
]
