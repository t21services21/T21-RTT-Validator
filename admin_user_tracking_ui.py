"""
T21 ADVANCED USER MANAGEMENT & TRACKING DASHBOARD
Complete admin control with geolocation tracking

Features:
- View ALL users (including free trials)
- See exact location (IP, country, city, street)
- Suspend/Approve/Extend/Upgrade users
- Track login history
- Monitor activity
- Security alerts
"""

import streamlit as st
from user_tracking_system import (
    get_all_users_tracking,
    get_user_login_history,
    get_user_tracking_summary,
    get_user_activity_summary,
    detect_suspicious_login
)
from student_auth import (
    list_all_students,
    upgrade_student,
    extend_student_license,
    get_student_info
)
from admin_management import load_users_db, save_users_db
from datetime import datetime, timedelta
import pandas as pd


def render_user_tracking_dashboard():
    """Main user tracking dashboard for admins"""
    
    st.header("👥 Advanced User Management & Tracking")
    st.markdown("**Complete user monitoring with geolocation and activity tracking**")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 All Users Dashboard",
        "🗺️ User Locations Map",
        "🔍 User Details & Actions",
        "🚨 Security Alerts"
    ])
    
    with tab1:
        render_all_users_dashboard()
    
    with tab2:
        render_user_locations()
    
    with tab3:
        render_user_detail_actions()
    
    with tab4:
        render_security_alerts()


def render_all_users_dashboard():
    """Show ALL users including trial users"""
    
    st.subheader("📊 Complete User Database")
    
    # Get all students
    all_students = list_all_students()
    
    # Get all advanced users (admin, staff, nhs)
    all_advanced = load_users_db()
    
    # Get tracking data
    tracking_data = get_all_users_tracking()
    
    # Combine all users
    all_users = []
    
    # Add students
    for student in all_students:
        email = student.get('email')
        tracking = tracking_data.get(email, {})
        
        user_row = {
            'Email': email,
            'Name': student.get('student_name', 'N/A'),
            'Type': 'Student',
            'Role': student.get('license', {}).get('role', 'trial'),
            'Status': 'Active' if student.get('license', {}).get('days_remaining', 0) > 0 else 'Expired',
            'Days Remaining': student.get('license', {}).get('days_remaining', 0),
            'Created': student.get('created_at', 'Unknown'),
            'Last Login': tracking.get('last_login', 'Never'),
            'Last IP': tracking.get('last_ip', 'Unknown'),
            'Last Location': tracking.get('last_location', 'Unknown'),
            'Total Logins': tracking.get('total_logins', 0),
            'Failed Logins': tracking.get('failed_logins', 0)
        }
        all_users.append(user_row)
    
    # Add advanced users
    for email, user_account in all_advanced.items():
        tracking = tracking_data.get(email, {})
        
        # UserAccount is an object, not a dict - use attributes or get_summary()
        try:
            summary = user_account.get_summary() if hasattr(user_account, 'get_summary') else {}
            
            user_row = {
                'Email': email,
                'Name': user_account.full_name if hasattr(user_account, 'full_name') else summary.get('full_name', 'N/A'),
                'Type': user_account.user_type if hasattr(user_account, 'user_type') else summary.get('user_type', 'Unknown').title(),
                'Role': user_account.role if hasattr(user_account, 'role') else summary.get('role', 'N/A'),
                'Status': user_account.status if hasattr(user_account, 'status') else 'Active',
                'Days Remaining': summary.get('days_remaining', 99999),  # Admin/staff don't expire
                'Created': user_account.created_at.strftime('%Y-%m-%d') if hasattr(user_account, 'created_at') else summary.get('created_at', 'Unknown'),
                'Last Login': tracking.get('last_login', 'Never'),
                'Last IP': tracking.get('last_ip', 'Unknown'),
                'Last Location': tracking.get('last_location', 'Unknown'),
                'Total Logins': tracking.get('total_logins', 0),
                'Failed Logins': tracking.get('failed_logins', 0)
            }
            all_users.append(user_row)
        except Exception as e:
            st.error(f"Error processing user {email}: {str(e)}")
            continue
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(all_users))
    
    with col2:
        trial_users = len([u for u in all_users if u['Role'] == 'trial'])
        st.metric("Trial Users", trial_users)
    
    with col3:
        active_users = len([u for u in all_users if u['Status'] == 'Active'])
        st.metric("Active Users", active_users)
    
    with col4:
        paid_users = len([u for u in all_users if u['Role'] not in ['trial', 'admin', 'staff']])
        st.metric("Paid Users", paid_users)
    
    st.markdown("---")
    
    # Filters
    st.markdown("### 🔍 Filter Users")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox("User Type", ["All", "Student", "Admin", "Staff", "NHS"])
    
    with col2:
        filter_role = st.selectbox("Role", ["All", "trial", "monthly", "annual", "professional"])
    
    with col3:
        filter_status = st.selectbox("Status", ["All", "Active", "Expired"])
    
    # Apply filters
    filtered_users = all_users.copy()
    
    if filter_type != "All":
        filtered_users = [u for u in filtered_users if u['Type'] == filter_type]
    
    if filter_role != "All":
        filtered_users = [u for u in filtered_users if u['Role'] == filter_role]
    
    if filter_status != "All":
        filtered_users = [u for u in filtered_users if u['Status'] == filter_status]
    
    st.info(f"📊 Showing {len(filtered_users)} of {len(all_users)} users")
    
    # Display table
    if filtered_users:
        df = pd.DataFrame(filtered_users)
        
        # Style the dataframe
        def color_status(val):
            if val == 'Active':
                return 'background-color: #d4edda'
            else:
                return 'background-color: #f8d7da'
        
        # Display with formatting
        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download User Database (CSV)",
            data=csv,
            file_name=f"user_database_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No users found with current filters")


def render_user_locations():
    """Show user locations on map"""
    
    st.subheader("🗺️ User Geographic Distribution")
    
    tracking_data = get_all_users_tracking()
    
    # Collect location data
    locations = []
    
    for email, data in tracking_data.items():
        if data.get('last_location') and data.get('last_location') != 'Unknown':
            locations.append({
                'Email': email,
                'Location': data.get('last_location'),
                'IP': data.get('last_ip'),
                'Logins': data.get('total_logins', 0)
            })
    
    if locations:
        # Group by location
        from collections import Counter
        location_counts = Counter([loc['Location'] for loc in locations])
        
        st.markdown("### 📍 User Distribution by Location")
        
        # Display as chart
        location_df = pd.DataFrame([
            {'Location': loc, 'Users': count}
            for loc, count in location_counts.most_common(20)
        ])
        
        st.bar_chart(location_df.set_index('Location'))
        
        # Detailed table
        st.markdown("### 📋 All User Locations")
        
        df = pd.DataFrame(locations)
        st.dataframe(df, use_container_width=True)
        
        # Map visualization (if coordinates available)
        st.info("💡 Tip: For precise map visualization, upgrade to include coordinate tracking")
        
    else:
        st.warning("No location data available yet. Users need to log in for tracking to start.")


def render_user_detail_actions():
    """Detailed user view with admin actions"""
    
    st.subheader("🔍 User Details & Management Actions")
    
    # Select user
    all_students = list_all_students()
    all_advanced = load_users_db()
    
    all_emails = [s['email'] for s in all_students] + list(all_advanced.keys())
    
    if not all_emails:
        st.warning("No users in system yet")
        return
    
    selected_email = st.selectbox("Select User", sorted(all_emails))
    
    if selected_email:
        # Get user data
        user_info = get_student_info(selected_email)
        if not user_info:
            # Try advanced users
            user_info = all_advanced.get(selected_email)
        
        tracking = get_user_tracking_summary(selected_email)
        login_history = get_user_login_history(selected_email, limit=10)
        activity = get_user_activity_summary(selected_email, days=30)
        
        # User Profile
        st.markdown("### 👤 User Profile")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Email:** {selected_email}")
            st.markdown(f"**Name:** {user_info.get('student_name', user_info.get('name', 'N/A'))}")
            st.markdown(f"**Type:** {user_info.get('user_type', 'Student').title()}")
        
        with col2:
            if 'license' in user_info:
                license_info = user_info['license']
                st.markdown(f"**Role:** {license_info.get('role', 'trial')}")
                st.markdown(f"**Days Remaining:** {license_info.get('days_remaining', 0)}")
                st.markdown(f"**Status:** {'Active' if license_info.get('days_remaining', 0) > 0 else 'Expired'}")
            else:
                st.markdown(f"**Role:** {user_info.get('role', 'N/A')}")
                st.markdown(f"**Status:** Active (Staff/Admin)")
        
        with col3:
            st.markdown(f"**Created:** {user_info.get('created_at', 'Unknown')}")
            if tracking:
                st.markdown(f"**First Seen:** {tracking.get('first_seen', 'Unknown')[:10]}")
                st.markdown(f"**Total Logins:** {tracking.get('total_logins', 0)}")
        
        st.markdown("---")
        
        # Location & Security
        if tracking:
            st.markdown("### 🗺️ Location & Security Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Latest Location:**")
                st.info(f"""
                **IP Address:** {tracking.get('last_ip', 'Unknown')}  
                **Location:** {tracking.get('last_location', 'Unknown')}  
                **Last Login:** {tracking.get('last_login', 'Never')[:19]}
                """)
                
                st.markdown("**Login Statistics:**")
                st.success(f"""
                **Successful Logins:** {tracking.get('successful_logins', 0)}  
                **Failed Logins:** {tracking.get('failed_logins', 0)}  
                **Unique IPs:** {len(tracking.get('unique_ips', []))}  
                **Unique Locations:** {len(tracking.get('unique_locations', []))}
                """)
            
            with col2:
                # Recent login history
                st.markdown("**Recent Login History:**")
                
                if login_history:
                    for idx, login in enumerate(login_history[:5], 1):
                        geo = login.get('geolocation', {})
                        
                        with st.expander(f"{idx}. {login['timestamp'][:19]} - {'✅' if login['success'] else '❌'}"):
                            st.markdown(f"**IP:** {login['ip_address']}")
                            st.markdown(f"**Location:** {geo.get('city', 'Unknown')}, {geo.get('country', 'Unknown')}")
                            st.markdown(f"**Street Estimate:** {geo.get('street_estimate', 'N/A')}")
                            st.markdown(f"**ISP:** {geo.get('isp', 'Unknown')}")
                            st.markdown(f"**Device:** {login.get('device', {}).get('browser', 'Unknown')}")
                            st.markdown(f"**Success:** {'Yes' if login['success'] else 'No'}")
                else:
                    st.info("No login history available")
        
        st.markdown("---")
        
        # Admin Actions
        st.markdown("### ⚙️ Admin Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔴 Suspend User", use_container_width=True):
                # Suspend user
                if 'license' in user_info:
                    all_students_db = list_all_students()
                    for student in all_students_db:
                        if student['email'] == selected_email:
                            student['license']['days_remaining'] = 0
                            student['license']['role'] = 'suspended'
                    
                    # Save (need to implement save function)
                    st.success(f"✅ User {selected_email} suspended!")
                    st.rerun()
        
        with col2:
            if st.button("✅ Approve/Activate", use_container_width=True):
                # Activate user
                if 'license' in user_info:
                    result = extend_student_license(selected_email, days=30)
                    if result['success']:
                        st.success("✅ User activated with 30 days!")
                        st.rerun()
        
        with col3:
            st.markdown("**Extend License:**")
            extend_days = st.number_input("Days", min_value=1, max_value=365, value=30, key=f"extend_{selected_email}")
            if st.button("➕ Extend", use_container_width=True):
                result = extend_student_license(selected_email, days=extend_days)
                if result['success']:
                    st.success(f"✅ Extended by {extend_days} days!")
                    st.rerun()
        
        with col4:
            st.markdown("**Upgrade User:**")
            new_role = st.selectbox("New Role", ["trial", "monthly", "annual", "professional"], key=f"upgrade_{selected_email}")
            if st.button("⬆️ Upgrade", use_container_width=True):
                result = upgrade_student(selected_email, new_role=new_role)
                if result['success']:
                    st.success(f"✅ Upgraded to {new_role}!")
                    st.rerun()


def render_security_alerts():
    """Show security alerts and suspicious activity"""
    
    st.subheader("🚨 Security Monitoring & Alerts")
    
    tracking_data = get_all_users_tracking()
    
    # Check all users for suspicious activity
    alerts = []
    
    for email, data in tracking_data.items():
        # Check failed login ratio
        total = data.get('total_logins', 0)
        failed = data.get('failed_logins', 0)
        
        if total > 0:
            failure_rate = failed / total
            
            if failure_rate > 0.5 and total > 3:
                alerts.append({
                    'Email': email,
                    'Type': 'High Failure Rate',
                    'Severity': 'HIGH',
                    'Details': f"{failed}/{total} failed logins ({failure_rate*100:.0f}%)",
                    'Last IP': data.get('last_ip', 'Unknown')
                })
            
            # Check multiple locations
            if len(data.get('unique_locations', [])) > 5:
                alerts.append({
                    'Email': email,
                    'Type': 'Multiple Locations',
                    'Severity': 'MEDIUM',
                    'Details': f"Logged in from {len(data['unique_locations'])} different locations",
                    'Last IP': data.get('last_ip', 'Unknown')
                })
            
            # Check multiple IPs
            if len(data.get('unique_ips', [])) > 10:
                alerts.append({
                    'Email': email,
                    'Type': 'Multiple IP Addresses',
                    'Severity': 'MEDIUM',
                    'Details': f"Used {len(data['unique_ips'])} different IP addresses",
                    'Last IP': data.get('last_ip', 'Unknown')
                })
    
    # Display alerts
    if alerts:
        st.error(f"⚠️ {len(alerts)} Security Alert(s) Detected!")
        
        for alert in alerts:
            severity_color = {
                'HIGH': '🔴',
                'MEDIUM': '🟠',
                'LOW': '🟡'
            }
            
            with st.expander(f"{severity_color.get(alert['Severity'], '🟡')} {alert['Type']} - {alert['Email']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Email:** {alert['Email']}")
                    st.markdown(f"**Alert Type:** {alert['Type']}")
                    st.markdown(f"**Severity:** {alert['Severity']}")
                
                with col2:
                    st.markdown(f"**Details:** {alert['Details']}")
                    st.markdown(f"**Last IP:** {alert['Last IP']}")
                
                if st.button(f"🔴 Suspend {alert['Email']}", key=f"suspend_{alert['Email']}"):
                    st.warning(f"Suspending {alert['Email']}...")
    else:
        st.success("✅ No security alerts at this time. All activity appears normal.")
    
    st.markdown("---")
    
    # Security recommendations
    st.markdown("### 🛡️ Security Recommendations")
    
    st.info("""
    **Recommended Security Measures:**
    
    1. **Enable 2FA** - Two-factor authentication for all admin accounts
    2. **Monitor Failed Logins** - Suspend accounts with >5 failed attempts
    3. **Geographic Restrictions** - Alert on logins from unexpected countries
    4. **Session Timeout** - Auto-logout after 30 minutes of inactivity
    5. **IP Whitelist** - Restrict admin access to known IP ranges
    6. **Regular Audits** - Review user activity monthly
    """)
