"""
T21 SERVICES - TRIAL EXPIRY AUTOMATION UI
Admin interface to manage automated trial expiry emails

Features:
- View trial users and their status
- Manually trigger expiry check
- View email history
- Reset email history for testing
"""

import streamlit as st
import pandas as pd
from trial_expiry_automation import (
    check_and_send_expiry_warnings,
    get_trial_users_status,
    reset_email_history_for_user
)


def render_trial_automation_ui():
    """Render the trial expiry automation admin interface"""
    
    st.header("⏰ Trial Expiry Automation")
    st.markdown("**Automated email warnings for expiring trials**")
    
    st.info("💡 **How it works:** The system checks trial users and sends automated emails at 24hr, 1hr, and after expiry.")
    
    # Manual trigger
    st.subheader("🔄 Manual Check & Send")
    st.markdown("Manually trigger the expiry check system")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🚀 Run Expiry Check Now", type="primary"):
            with st.spinner("Checking trial users and sending emails..."):
                stats = check_and_send_expiry_warnings()
                
                st.success("✅ Expiry check complete!")
                
                st.markdown("**Results:**")
                st.markdown(f"- 👥 Checked: {stats['checked']} users")
                st.markdown(f"- 📧 24hr warnings: {stats['24hr_warnings']}")
                st.markdown(f"- ⚠️ 1hr warnings: {stats['1hr_warnings']}")
                st.markdown(f"- ❌ Expired notices: {stats['expired_notices']}")
                
                if stats['errors'] > 0:
                    st.error(f"⚠️ Errors: {stats['errors']}")
                
                st.balloons()
    
    with col2:
        st.markdown("**When to use:**")
        st.markdown("- After deploying email features")
        st.markdown("- To catch up on missed warnings")
        st.markdown("- For testing purposes")
        st.caption("⚠️ The system prevents duplicate emails automatically")
    
    st.markdown("---")
    
    # Trial Users Status
    st.subheader("👥 Trial Users Status")
    
    trial_users = get_trial_users_status()
    
    if not trial_users:
        st.info("No trial users found")
    else:
        st.markdown(f"**Total trial users:** {len(trial_users)}")
        
        # Create DataFrame
        df_data = []
        for user in trial_users:
            hours = user['hours_remaining']
            
            if hours <= 0:
                status_emoji = "❌"
                status_text = "EXPIRED"
            elif hours <= 1:
                status_emoji = "🔴"
                status_text = f"{int(hours * 60)}min left"
            elif hours <= 6:
                status_emoji = "🟠"
                status_text = f"{int(hours)}h left"
            elif hours <= 24:
                status_emoji = "🟡"
                status_text = f"{int(hours)}h left"
            else:
                status_emoji = "🟢"
                status_text = f"{hours:.1f}h left"
            
            df_data.append({
                "Status": f"{status_emoji} {status_text}",
                "Name": user['full_name'],
                "Email": user['email'],
                "24hr ✉️": "✅" if user['24hr_sent'] else "❌",
                "1hr ✉️": "✅" if user['1hr_sent'] else "❌",
                "Expired ✉️": "✅" if user['expired_sent'] else "❌"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.caption("Legend: ✅ = Email sent | ❌ = Not sent yet")
        
        # Statistics
        st.markdown("---")
        st.subheader("📊 Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active_count = sum(1 for u in trial_users if u['hours_remaining'] > 0)
            st.metric("Active Trials", active_count)
        
        with col2:
            expiring_soon = sum(1 for u in trial_users if 0 < u['hours_remaining'] <= 6)
            st.metric("Expiring < 6hr", expiring_soon)
        
        with col3:
            expired_count = sum(1 for u in trial_users if u['hours_remaining'] <= 0)
            st.metric("Expired", expired_count)
        
        with col4:
            warnings_sent = sum(1 for u in trial_users if u['24hr_sent'] or u['1hr_sent'])
            st.metric("Warnings Sent", warnings_sent)
        
        st.markdown("---")
        
        # Reset Email History (for testing)
        st.subheader("🔧 Testing Tools")
        
        with st.expander("⚠️ Reset Email History (Testing Only)"):
            st.warning("**Warning:** This will allow emails to be resent to users. Use only for testing!")
            
            reset_email = st.selectbox(
                "Select user to reset:",
                options=["-- Select User --"] + [u['email'] for u in trial_users]
            )
            
            if reset_email != "-- Select User --":
                if st.button("🔄 Reset Email History for User"):
                    if reset_email_history_for_user(reset_email):
                        st.success(f"✅ Reset email history for {reset_email}")
                        st.info("This user will now receive emails again on next check")
                        st.rerun()
                    else:
                        st.error("User not found in email history")
    
    st.markdown("---")
    
    # Email Templates Info
    st.subheader("📧 Email Templates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**24-Hour Warning**")
        st.caption("Sent when < 24 hours remain")
        st.caption("Subject: Trial expires in 24 hours")
        st.caption("Encourages upgrade")
    
    with col2:
        st.markdown("**1-Hour Warning**")
        st.caption("Sent when < 1 hour remains")
        st.caption("Subject: URGENT - Trial expires soon")
        st.caption("Final reminder to upgrade")
    
    with col3:
        st.markdown("**Expired Notice**")
        st.caption("Sent after trial expires")
        st.caption("Subject: Your trial has ended")
        st.caption("Shows upgrade options")
    
    st.markdown("---")
    
    # Automation Schedule
    st.subheader("⚙️ Automation Schedule")
    
    st.info("""
    **Current Setup:**
    - 🔵 **Manual trigger only** - Click "Run Expiry Check Now" to send emails
    - 📧 **Smart duplicate prevention** - Won't resend emails to same user
    - ✅ **Instant processing** - Takes 2-3 seconds per user
    
    **To automate fully:**
    1. Set up a scheduled task (e.g., run every 6 hours)
    2. Or integrate with a background job scheduler
    3. Or use GitHub Actions for automated checks
    
    For now, you can manually run the check whenever needed!
    """)
