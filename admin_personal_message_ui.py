"""
T21 SERVICES - ADMIN PERSONAL MESSAGE UI
Send personalized messages to individual users

Features:
- Select any user from dropdown
- Write custom subject and message
- Preview before sending
- Track sent messages
"""

import streamlit as st
from student_auth import list_all_students
from email_service import send_personal_message


def render_personal_message_ui():
    """Render the personal message interface for admins"""
    
    st.header("💬 Send Personal Message")
    st.markdown("**Send a personalized email to any user**")
    
    st.info("💡 **Use this to:** Contact individual users for support, follow-up, or personalized offers.")
    
    # Get all students
    try:
        all_students = list_all_students()
        
        if not all_students:
            st.warning("No users found in database.")
            return
        
        # Select recipient
        st.subheader("👤 Select Recipient")
        
        user_options = [f"{s['full_name']} ({s['email']}) - {s['role'].title()}" for s in all_students]
        selected_user_display = st.selectbox(
            "Choose user to message:",
            user_options,
            key="personal_msg_user"
        )
        
        # Extract email from selection
        selected_email = selected_user_display.split("(")[1].split(")")[0]
        
        # Find selected student details
        selected_student = next((s for s in all_students if s['email'] == selected_email), None)
        
        if selected_student:
            # Display user info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Name", selected_student['full_name'])
            
            with col2:
                st.metric("Role", selected_student['role'].title())
            
            with col3:
                st.metric("Status", selected_student['status'])
            
            st.markdown("---")
            
            # Compose message
            st.subheader("✍️ Compose Message")
            
            # Initialize session state for templates
            if 'template_subject' not in st.session_state:
                st.session_state.template_subject = ""
            if 'template_message' not in st.session_state:
                st.session_state.template_message = ""
            
            # Subject
            subject = st.text_input(
                "Subject:",
                value=st.session_state.template_subject,
                placeholder="e.g., Welcome to T21 Services!",
                help="Keep it clear and engaging"
            )
            
            # Message body
            message = st.text_area(
                "Message:",
                value=st.session_state.template_message,
                placeholder=f"""Hello {selected_student['full_name']},

I wanted to reach out personally to...

Best regards,
T21 Services Team""",
                height=300,
                help="Write your personalized message. HTML supported."
            )
            
            # From name
            from_admin = st.text_input(
                "From (Your Name):",
                value="T21 Admin",
                help="Your name as it appears in the email"
            )
            
            st.markdown("---")
            
            # Preview
            st.subheader("👀 Message Preview")
            
            if subject and message:
                with st.expander("Preview Email", expanded=True):
                    st.markdown(f"**To:** {selected_student['full_name']} ({selected_email})")
                    st.markdown(f"**From:** {from_admin}")
                    st.markdown(f"**Subject:** {subject}")
                    st.markdown("---")
                    st.markdown(message)
            else:
                st.info("Enter subject and message to see preview")
            
            st.markdown("---")
            
            # Send button
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if st.button("📧 Send Message", type="primary"):
                    if not subject:
                        st.error("❌ Please enter email subject")
                    elif not message:
                        st.error("❌ Please enter email message")
                    else:
                        # Send email
                        with st.spinner(f"Sending message to {selected_student['full_name']}..."):
                            success = send_personal_message(
                                user_email=selected_email,
                                user_name=selected_student['full_name'],
                                subject=subject,
                                message=message,
                                from_admin=from_admin
                            )
                            
                            if success:
                                st.success(f"✅ Message sent successfully to {selected_student['full_name']}!")
                                st.balloons()
                                
                                # Clear form
                                st.session_state.template_subject = ""
                                st.session_state.template_message = ""
                            else:
                                st.error("❌ Failed to send message. Please check SendGrid configuration.")
            
            with col2:
                if st.button("🧪 Send Test to Yourself"):
                    if not subject or not message:
                        st.warning("Please enter subject and message first")
                    else:
                        admin_email = st.session_state.user_email
                        st.info(f"Test email would be sent to: {admin_email}")
            
            st.markdown("---")
            
            # Quick message templates
            st.subheader("📋 Quick Templates")
            
            template_choice = st.selectbox(
                "Load a template:",
                [
                    "-- Select Template --",
                    "👋 Welcome & Introduction",
                    "⏰ Trial Ending Reminder",
                    "🎁 Exclusive Upgrade Offer",
                    "💡 Feature Announcement",
                    "🤝 Thank You Message",
                    "❓ Check-in / Support"
                ]
            )
            
            if template_choice == "👋 Welcome & Introduction":
                st.session_state.template_subject = f"Welcome to T21 Services, {selected_student['full_name']}!"
                st.session_state.template_message = f"""Hello {selected_student['full_name']},

I wanted to personally welcome you to the T21 RTT Training Platform!

I noticed you recently joined, and I wanted to make sure you have everything you need to succeed.

If you have any questions or need any assistance, please don't hesitate to reach out. I'm here to help!

Looking forward to supporting your learning journey.

Best regards,
{from_admin}"""
                st.success("Template loaded! Scroll up to edit and send.")
                st.rerun()
            
            elif template_choice == "⏰ Trial Ending Reminder":
                st.session_state.template_subject = f"{selected_student['full_name']}, Your Trial is Ending Soon!"
                st.session_state.template_message = f"""Hi {selected_student['full_name']},

I noticed your trial is ending soon, and I wanted to reach out personally.

I hope you've enjoyed exploring our platform! I'd love to help you continue your learning journey.

We have some exclusive upgrade offers available. Would you like to discuss which plan works best for you?

Feel free to reply to this email with any questions!

Best regards,
{from_admin}"""
                st.success("Template loaded! Scroll up to edit and send.")
                st.rerun()
            
            elif template_choice == "🎁 Exclusive Upgrade Offer":
                st.session_state.template_subject = f"Exclusive Offer for You, {selected_student['full_name']}!"
                st.session_state.template_message = f"""Hi {selected_student['full_name']},

I have an exclusive offer just for you!

For a limited time, I can offer you 20% OFF any upgrade plan:
- Basic: £239 (was £299)
- Professional: £479 (was £599)
- Premium: £799 (was £999)

This offer is valid for the next 48 hours.

Would you like to take advantage of this special offer?

Best regards,
{from_admin}"""
                st.success("Template loaded! Scroll up to edit and send.")
                st.rerun()
            
            elif template_choice == "💡 Feature Announcement":
                st.session_state.template_subject = "Exciting New Feature Just for You!"
                st.session_state.template_message = f"""Hi {selected_student['full_name']},

I'm excited to share that we've just launched a new feature that I think you'll love!

[Describe the new feature here]

This feature is now available in your account. Login to try it out!

I'd love to hear your feedback!

Best regards,
{from_admin}"""
                st.success("Template loaded! Scroll up to edit and send.")
                st.rerun()
            
            elif template_choice == "🤝 Thank You Message":
                st.session_state.template_subject = f"Thank You, {selected_student['full_name']}!"
                st.session_state.template_message = f"""Hi {selected_student['full_name']},

I just wanted to say thank you for being part of the T21 Services community!

Your progress and dedication to learning have been inspiring.

If there's anything I can do to support your journey, please let me know.

Keep up the great work!

Best regards,
{from_admin}"""
                st.success("Template loaded! Scroll up to edit and send.")
                st.rerun()
            
            elif template_choice == "❓ Check-in / Support":
                st.session_state.template_subject = f"How Are You Doing, {selected_student['full_name']}?"
                st.session_state.template_message = f"""Hi {selected_student['full_name']},

I wanted to check in and see how your learning experience has been so far.

Are there any challenges you're facing? Any features you'd like to see?

Your feedback is incredibly valuable to us, and I'm here to help in any way I can.

Looking forward to hearing from you!

Best regards,
{from_admin}"""
                st.success("Template loaded! Scroll up to edit and send.")
                st.rerun()
    
    except Exception as e:
        st.error(f"Error loading users: {e}")
