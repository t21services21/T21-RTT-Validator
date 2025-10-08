"""
T21 SERVICES - ADMIN BULK EMAIL SYSTEM
Send bulk emails to users with filtering options

Features:
- Send to all users
- Filter by role (trial, basic, professional, etc.)
- Filter by status (active, expired)
- Custom subject and message
- Email preview
- Track sent emails
"""

import streamlit as st
from student_auth import list_all_students
from email_service import send_bulk_email


def render_bulk_email_ui():
    """Render the bulk email interface for admins"""
    
    st.header("📧 Bulk Email System")
    st.markdown("**Send emails to multiple users at once**")
    
    st.info("💡 **Tip:** Use this to announce new features, send upgrade offers, or communicate important information.")
    
    # Get all students
    try:
        all_students = list_all_students()
        
        if not all_students:
            st.warning("No users found in database.")
            return
        
        # Filtering Options
        st.subheader("🎯 Select Recipients")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Filter by role
            role_filter = st.multiselect(
                "Filter by Role:",
                options=["trial", "basic", "professional", "ultimate", "admin", "staff", "nhs_trust"],
                default=["trial"],
                help="Select which user roles to email"
            )
        
        with col2:
            # Filter by status
            status_filter = st.multiselect(
                "Filter by Status:",
                options=["Active", "Expired"],
                default=["Active"],
                help="Select active or expired users"
            )
        
        # Apply filters
        filtered_students = []
        for student in all_students:
            # Check role
            if student['role'] not in role_filter:
                continue
            
            # Check status
            if student['status'] not in status_filter:
                continue
            
            filtered_students.append(student)
        
        # Show recipient count
        st.success(f"✅ **{len(filtered_students)} recipients** selected")
        
        if filtered_students:
            with st.expander("👥 View Recipients"):
                for i, student in enumerate(filtered_students[:50], 1):
                    st.markdown(f"{i}. **{student['full_name']}** ({student['email']}) - {student['role'].title()} - {student['status']}")
                
                if len(filtered_students) > 50:
                    st.info(f"... and {len(filtered_students) - 50} more")
        
        st.markdown("---")
        
        # Email Composition
        st.subheader("✍️ Compose Email")
        
        # Subject
        subject = st.text_input(
            "Email Subject:",
            placeholder="e.g., New Feature Alert: AI Tutor Now Available!",
            help="Keep it clear and engaging"
        )
        
        # Message body
        message = st.text_area(
            "Email Message (HTML supported):",
            placeholder="""Hello,

We're excited to announce...

Best regards,
T21 Services Team""",
            height=300,
            help="Write your message here. You can use HTML tags for formatting."
        )
        
        st.markdown("---")
        
        # Preview
        st.subheader("👀 Email Preview")
        
        if subject and message:
            with st.expander("Preview Email", expanded=True):
                st.markdown(f"**Subject:** {subject}")
                st.markdown("---")
                st.markdown(message)
        else:
            st.info("Enter subject and message to see preview")
        
        st.markdown("---")
        
        # Send Button
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("📨 Send Bulk Email", type="primary"):
                if not subject:
                    st.error("❌ Please enter email subject")
                elif not message:
                    st.error("❌ Please enter email message")
                elif not filtered_students:
                    st.error("❌ No recipients selected")
                else:
                    # Send emails
                    with st.spinner(f"Sending emails to {len(filtered_students)} recipients..."):
                        recipient_emails = [s['email'] for s in filtered_students]
                        success_count, failed_emails = send_bulk_email(recipient_emails, subject, message)
                        
                        if success_count > 0:
                            st.success(f"✅ Successfully sent {success_count} emails!")
                            st.balloons()
                        
                        if failed_emails:
                            st.warning(f"⚠️ Failed to send to {len(failed_emails)} recipients:")
                            for email in failed_emails:
                                st.caption(f"- {email}")
        
        with col2:
            if st.button("📄 Save as Draft"):
                st.info("Draft saving feature coming soon!")
        
        with col3:
            if st.button("🧪 Send Test"):
                admin_email = "admin@t21services.co.uk"
                st.info(f"Test email would be sent to: {admin_email}")
        
        st.markdown("---")
        
        # Quick Templates
        st.subheader("📋 Quick Templates")
        
        template_choice = st.selectbox(
            "Load a template:",
            [
                "-- Select Template --",
                "🎉 New Feature Announcement",
                "💰 Upgrade Offer",
                "⏰ Trial Expiring Soon",
                "📚 New Training Content"
            ]
        )
        
        if template_choice == "🎉 New Feature Announcement":
            st.session_state.template_subject = "🎉 Exciting New Feature: [Feature Name]"
            st.session_state.template_message = """Hello!

We're thrilled to announce a brand new feature on the T21 RTT Training Platform:

**[Feature Name]**

This feature will help you...

Login now to try it out: https://t21-rtt-validator.streamlit.app

Best regards,
T21 Services Team"""
            st.success("Template loaded! Scroll up to edit.")
        
        elif template_choice == "💰 Upgrade Offer":
            st.session_state.template_subject = "💰 Special Offer: Upgrade and Save!"
            st.session_state.template_message = """Hello!

For a limited time, we're offering an exclusive discount on all upgrade plans:

**20% OFF** when you upgrade this week!

- Basic: £239 (was £299)
- Professional: £479 (was £599)
- Premium: £799 (was £999)

Don't miss out on this opportunity!

Upgrade now: https://t21-rtt-validator.streamlit.app

Best regards,
T21 Services Team"""
            st.success("Template loaded! Scroll up to edit.")
        
        elif template_choice == "⏰ Trial Expiring Soon":
            st.session_state.template_subject = "⏰ Your Trial Expires Soon - Don't Lose Access!"
            st.session_state.template_message = """Hello!

Your 48-hour trial is ending soon!

Don't lose access to:
✅ RTT Pathway Validator
✅ AI RTT Tutor
✅ 40+ Training Scenarios
✅ Interactive Quizzes
✅ Certification Exam

Upgrade now to continue your learning journey!

Best regards,
T21 Services Team"""
            st.success("Template loaded! Scroll up to edit.")
        
        elif template_choice == "📚 New Training Content":
            st.session_state.template_subject = "📚 New Training Content Added!"
            st.session_state.template_message = """Hello!

We've just added new training content to the platform:

- 5 new RTT scenarios
- Updated quiz questions
- New AI Tutor capabilities

Login now to explore: https://t21-rtt-validator.streamlit.app

Best regards,
T21 Services Team"""
            st.success("Template loaded! Scroll up to edit.")
    
    except Exception as e:
        st.error(f"Error loading users: {e}")
