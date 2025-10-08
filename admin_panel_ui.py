"""
T21 ADMIN PANEL UI
Streamlit interface for managing all users, permissions, and platform

To integrate into app.py:
- Add new menu item: "🔧 Admin Panel"
- Import this file
- Call render_admin_panel()
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from admin_management import (
    get_all_users, get_user_details, create_user, suspend_user, unsuspend_user,
    terminate_user, delete_user, extend_license, change_role,
    grant_custom_permission, revoke_custom_permission,
    get_revenue_stats, get_audit_log, get_platform_stats
)
from advanced_access_control import USER_TYPES, ACCOUNT_STATUS


def render_admin_panel(admin_email):
    """
    Render complete admin panel
    
    Args:
        admin_email: Email of logged-in admin
    """
    
    st.title("🔧 Admin Control Panel")
    st.markdown("**Complete platform management system**")
    
    # Check if user is admin - try advanced DB first, then old DB
    admin_user = get_user_details(admin_email)
    
    # If not in advanced DB, check old database
    if not admin_user:
        import json
        import os
        if os.path.exists("users_database.json"):
            with open("users_database.json", 'r') as f:
                old_users = json.load(f)
            if admin_email in old_users:
                user_data = old_users[admin_email]
                if user_data.get("license", {}).get("role") == "admin":
                    admin_user = {
                        "user_type": "admin",
                        "role": "admin",
                        "email": admin_email
                    }
    
    # Check permissions
    if not admin_user:
        st.error("⛔ Access Denied - Admin privileges required")
        return
    
    # Check if user_type exists and is admin/super_admin
    user_type = admin_user.get("user_type", "")
    user_role = admin_user.get("role", "")
    
    if user_type not in ["admin", "super_admin"] and user_role != "admin":
        st.error("⛔ Access Denied - Admin privileges required")
        return
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard",
        "👥 User Management",
        "🔑 Permissions",
        "💰 Revenue & Analytics",
        "📜 Audit Log",
        "⚙️ System Settings"
    ])
    
    # ========================================
    # TAB 1: DASHBOARD
    # ========================================
    with tab1:
        render_dashboard()
    
    # ========================================
    # TAB 2: USER MANAGEMENT
    # ========================================
    with tab2:
        render_user_management(admin_email, admin_user)
    
    # ========================================
    # TAB 3: PERMISSIONS
    # ========================================
    with tab3:
        render_permissions_management(admin_email)
    
    # ========================================
    # TAB 4: REVENUE & ANALYTICS
    # ========================================
    with tab4:
        render_revenue_analytics()
    
    # ========================================
    # TAB 5: AUDIT LOG
    # ========================================
    with tab5:
        render_audit_log()
    
    # ========================================
    # TAB 6: SYSTEM SETTINGS
    # ========================================
    with tab6:
        render_system_settings(admin_user)


# ========================================
# DASHBOARD
# ========================================

def render_dashboard():
    """Render dashboard overview"""
    st.subheader("📊 Platform Overview")
    
    stats = get_platform_stats()
    revenue = get_revenue_stats()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", stats["total_users"])
        st.caption(f"Active: {stats['active_users']}")
    
    with col2:
        st.metric("Students", stats["students"])
        st.caption(f"Staff: {stats['staff']}")
    
    with col3:
        st.metric("Total Revenue", f"£{revenue['total_revenue']:,}")
        st.caption(f"Active: {revenue['active_students']}")
    
    with col4:
        st.metric("Total Logins", stats["total_logins"])
        st.caption("All time")
    
    st.markdown("---")
    
    # Status breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Account Status")
        status_data = {
            "Active": stats["active_users"],
            "Expired": stats["expired_users"],
            "Suspended": stats["suspended_users"],
            "Terminated": stats["terminated_users"]
        }
        st.bar_chart(status_data)
    
    with col2:
        st.subheader("User Types")
        type_data = {
            "Students": stats["students"],
            "Staff": stats["staff"],
            "Admins": stats["admins"]
        }
        st.bar_chart(type_data)
    
    # Recent activity
    st.markdown("---")
    st.subheader("📜 Recent Activity")
    recent_logs = get_audit_log(limit=10)
    
    if recent_logs:
        for log in recent_logs:
            timestamp = datetime.fromisoformat(log["timestamp"]).strftime("%d/%m/%Y %H:%M")
            st.markdown(f"**{timestamp}** - {log['action']} - {log['performed_by']} → {log['target_user']}")
            if log.get("details"):
                st.caption(log["details"])
    else:
        st.info("No activity yet")


# ========================================
# USER MANAGEMENT
# ========================================

def render_user_management(admin_email, admin_user):
    """Render user management interface"""
    st.subheader("👥 User Management")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        user_type_filter = st.selectbox(
            "User Type",
            ["All", "student", "staff", "admin", "super_admin"],
            key="filter_user_type"
        )
    
    with col2:
        status_filter = st.selectbox(
            "Status",
            ["All", "active", "suspended", "expired", "terminated"],
            key="filter_status"
        )
    
    with col3:
        st.write("")  # Spacer
    
    # Build filter
    filter_by = {}
    if user_type_filter != "All":
        filter_by["type"] = user_type_filter
    if status_filter != "All":
        filter_by["status"] = status_filter
    
    # Get users
    users = get_all_users(filter_by=filter_by if filter_by else None)
    
    st.markdown(f"**Total users found:** {len(users)}")
    
    # Display users in table
    if users:
        df = pd.DataFrame(users)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
        
        # User actions
        st.subheader("User Actions")
        
        selected_email = st.selectbox(
            "Select User",
            [u["email"] for u in users],
            key="user_mgmt_user_select"
        )
        
        if selected_email:
            user_details = get_user_details(selected_email)
            
            if user_details:
                # Display user details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### User Details")
                    st.markdown(f"**Name:** {user_details['full_name']}")
                    st.markdown(f"**Email:** {user_details['email']}")
                    st.markdown(f"**Role:** {user_details['role_name']}")
                    st.markdown(f"**Type:** {user_details['user_type']}")
                    st.markdown(f"**Status:** {user_details['status_text']}")
                    st.markdown(f"**Created:** {user_details['created_at']}")
                    st.markdown(f"**Expires:** {user_details['expiry_date']}")
                    st.markdown(f"**Days Remaining:** {user_details['days_remaining']}")
                
                with col2:
                    st.markdown("### Usage Statistics")
                    st.markdown(f"**Total Logins:** {user_details['total_logins']}")
                    st.markdown(f"**Last Login:** {user_details['last_login']}")
                    
                    if user_details.get("usage"):
                        usage = user_details["usage"]
                        st.markdown(f"**Today:**")
                        st.markdown(f"- Logins: {usage.get('logins_today', 0)}")
                        st.markdown(f"- AI Questions: {usage.get('ai_questions_today', 0)}")
                        st.markdown(f"- Quizzes: {usage.get('quizzes_today', 0)}")
                        st.markdown(f"- Validations: {usage.get('validations_today', 0)}")
                
                st.markdown("---")
                
                # Action buttons
                st.markdown("### Actions")
                
                action_col1, action_col2, action_col3, action_col4, action_col5 = st.columns(5)
                
                with action_col1:
                    if st.button("⏸️ Suspend", key=f"suspend_{selected_email}"):
                        st.session_state.action = "suspend"
                        st.session_state.target_email = selected_email
                
                with action_col2:
                    if st.button("✅ Unsuspend", key=f"unsuspend_{selected_email}"):
                        success, msg = unsuspend_user(selected_email, admin_email)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                
                with action_col3:
                    if st.button("⚠️ Terminate", key=f"terminate_{selected_email}"):
                        st.session_state.action = "terminate"
                        st.session_state.target_email = selected_email
                
                with action_col4:
                    if st.button("⬆️ Change Role", key=f"change_role_{selected_email}"):
                        st.session_state.action = "change_role"
                        st.session_state.target_email = selected_email
                
                with action_col5:
                    if st.button("➕ Extend License", key=f"extend_{selected_email}"):
                        st.session_state.action = "extend"
                        st.session_state.target_email = selected_email
                
                # Handle actions
                if st.session_state.get("action") == "suspend" and st.session_state.get("target_email") == selected_email:
                    st.markdown("### Suspend User")
                    reason = st.text_area("Reason for suspension:")
                    if st.button("Confirm Suspension"):
                        if reason:
                            success, msg = suspend_user(selected_email, reason, admin_email)
                            if success:
                                st.success(msg)
                                st.session_state.action = None
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.warning("Please enter a reason")
                
                if st.session_state.get("action") == "terminate" and st.session_state.get("target_email") == selected_email:
                    st.error("### ⚠️ TERMINATE USER (PERMANENT)")
                    st.warning("This action is PERMANENT and cannot be undone!")
                    reason = st.text_area("Reason for termination:")
                    confirm = st.checkbox("I understand this is permanent")
                    if st.button("CONFIRM TERMINATION", type="primary"):
                        if confirm and reason:
                            success, msg = terminate_user(selected_email, reason, admin_email)
                            if success:
                                st.success(msg)
                                st.session_state.action = None
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.warning("Please confirm and enter reason")
                
                if st.session_state.get("action") == "change_role" and st.session_state.get("target_email") == selected_email:
                    st.markdown("### Change User Role")
                    new_role = st.selectbox(
                        "New Role",
                        list(USER_TYPES.keys()),
                        key="change_role_select"
                    )
                    if st.button("Confirm Role Change"):
                        success, msg = change_role(selected_email, new_role, admin_email)
                        if success:
                            st.success(msg)
                            st.session_state.action = None
                            st.rerun()
                        else:
                            st.error(msg)
                
                if st.session_state.get("action") == "extend" and st.session_state.get("target_email") == selected_email:
                    st.markdown("### Extend License")
                    
                    # Option 1: Extend by days
                    st.markdown("**Option 1: Extend by Days**")
                    days = st.number_input("Days to extend", min_value=1, max_value=365, value=30)
                    if st.button("Confirm Extension"):
                        success, msg = extend_license(selected_email, days, admin_email)
                        if success:
                            st.success(msg)
                            st.session_state.action = None
                            st.rerun()
                        else:
                            st.error(msg)
                    
                    st.markdown("---")
                    
                    # Option 2: Set custom expiry date/time
                    st.markdown("**Option 2: Set Custom Expiry Date/Time**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        expiry_date = st.date_input("Expiry Date")
                    
                    with col2:
                        expiry_time = st.time_input("Expiry Time")
                    
                    if st.button("Set Custom Expiry"):
                        from datetime import datetime
                        
                        # Combine date and time
                        new_expiry = datetime.combine(expiry_date, expiry_time)
                        
                        # Update user
                        from admin_management import load_users_db, save_users_db
                        users = load_users_db()
                        
                        if selected_email in users:
                            user = users[selected_email]
                            old_expiry = user.expiry_date
                            user.expiry_date = new_expiry
                            user.add_note(f"Custom expiry set to {new_expiry.strftime('%d/%m/%Y %H:%M:%S')} by {admin_email}")
                            
                            save_users_db(users)
                            
                            st.success(f"✅ Custom expiry set!")
                            st.info(f"**Old:** {old_expiry.strftime('%d/%m/%Y %H:%M')}")
                            st.info(f"**New:** {new_expiry.strftime('%d/%m/%Y %H:%M')}")
                            
                            days_remaining = (new_expiry - datetime.now()).days
                            
                            if days_remaining < 0:
                                st.warning(f"⚠️ This date is in the PAST! Account is now EXPIRED.")
                            else:
                                st.success(f"User has {days_remaining} days remaining")
                            
                            st.session_state.action = None
                        else:
                            st.error("User not found")
    
    else:
        st.info("No users found with selected filters")
    
    # Create new user
    st.markdown("---")
    st.subheader("➕ Create New User")
    
    with st.expander("Create User Form"):
        new_email = st.text_input("Email", key="create_user_email")
        new_password = st.text_input("Password", type="password", key="create_user_password")
        new_name = st.text_input("Full Name", key="create_user_name")
        new_role = st.selectbox("Role", list(USER_TYPES.keys()), key="create_user_role")
        
        st.markdown("**Custom Expiry Date/Time (Optional)**")
        st.caption("Leave blank to use default duration for selected role")
        
        col1, col2 = st.columns(2)
        with col1:
            custom_expiry_date = st.date_input("Expiry Date", value=None, key="create_user_expiry_date")
        with col2:
            custom_expiry_time = st.time_input("Expiry Time", value=None, key="create_user_expiry_time")
        
        if st.button("Create User"):
            if new_email and new_password and new_name:
                # Check if custom expiry is set
                custom_expiry = None
                if custom_expiry_date and custom_expiry_time:
                    from datetime import datetime
                    custom_expiry = datetime.combine(custom_expiry_date, custom_expiry_time)
                
                success, msg = create_user(new_email, new_password, new_name, new_role, admin_email, custom_expiry)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please fill all required fields (Email, Password, Name)")


# ========================================
# PERMISSIONS MANAGEMENT
# ========================================

def render_permissions_management(admin_email):
    """Render permissions management"""
    st.subheader("🔑 Custom Permissions Management")
    
    st.info("Grant or revoke specific feature permissions for individual users")
    
    # Select user
    users = get_all_users()
    selected_email = st.selectbox(
        "Select User",
        [u["email"] for u in users],
        key="permissions_user_select"
    )
    
    if selected_email:
        user_details = get_user_details(selected_email)
        
        st.markdown(f"**User:** {user_details['full_name']}")
        st.markdown(f"**Current Role:** {user_details['role_name']}")
        
        # Show custom permissions
        if user_details.get("custom_permissions"):
            st.markdown("### Current Custom Permissions")
            for feature, granted in user_details["custom_permissions"].items():
                status = "✅ Granted" if granted else "❌ Revoked"
                st.markdown(f"- **{feature}**: {status}")
        
        st.markdown("---")
        
        # Grant permission
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Grant Permission")
            feature_to_grant = st.text_input("Feature Name", key="grant_feature")
            if st.button("Grant"):
                if feature_to_grant:
                    success, msg = grant_custom_permission(selected_email, feature_to_grant, admin_email)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        
        with col2:
            st.markdown("### Revoke Permission")
            feature_to_revoke = st.text_input("Feature Name", key="revoke_feature")
            if st.button("Revoke"):
                if feature_to_revoke:
                    success, msg = revoke_custom_permission(selected_email, feature_to_revoke, admin_email)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)


# ========================================
# REVENUE & ANALYTICS
# ========================================

def render_revenue_analytics():
    """Render revenue and analytics"""
    st.subheader("💰 Revenue & Analytics")
    
    revenue = get_revenue_stats()
    
    # Total revenue
    st.metric("Total Revenue", f"£{revenue['total_revenue']:,}")
    st.metric("Active Paying Students", revenue['active_students'])
    
    st.markdown("---")
    
    # Revenue by role
    st.markdown("### Revenue Breakdown by Plan")
    
    if revenue['revenue_by_role']:
        for role_name, data in revenue['revenue_by_role'].items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{role_name}**")
            with col2:
                st.markdown(f"{data['count']} students")
            with col3:
                st.markdown(f"£{data['revenue']:,}")
    else:
        st.info("No revenue data yet")


# ========================================
# AUDIT LOG
# ========================================

def render_audit_log():
    """Render audit log"""
    st.subheader("📜 System Audit Log")
    
    limit = st.slider("Number of entries", 10, 500, 100)
    logs = get_audit_log(limit=limit)
    
    if logs:
        for log in logs:
            timestamp = datetime.fromisoformat(log["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
            
            with st.expander(f"{timestamp} - {log['action']} - {log['performed_by']}"):
                st.markdown(f"**Action:** {log['action']}")
                st.markdown(f"**Performed By:** {log['performed_by']}")
                st.markdown(f"**Target User:** {log['target_user']}")
                st.markdown(f"**Details:** {log.get('details', 'N/A')}")
    else:
        st.info("No audit logs found")


# ========================================
# SYSTEM SETTINGS
# ========================================

def render_system_settings(admin_user):
    """Render system settings"""
    st.subheader("⚙️ System Settings")
    
    if admin_user["user_type"] != "super_admin":
        st.warning("⚠️ Some settings require Super Admin access")
    
    st.markdown("### Platform Configuration")
    st.info("System settings coming soon...")
    
    # Show role definitions
    st.markdown("---")
    st.markdown("### Available Roles")
    
    for role_key, role_data in USER_TYPES.items():
        with st.expander(f"{role_data['name']} ({role_key})"):
            st.markdown(f"**Type:** {role_data['type']}")
            st.markdown(f"**Duration:** {role_data['duration_days']} days")
            st.markdown(f"**Price:** £{role_data['price']}")
            st.markdown("**Features:**")
            for feature, access in role_data['features'].items():
                st.markdown(f"- {feature}: {access}")
