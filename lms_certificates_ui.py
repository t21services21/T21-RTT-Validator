"""
T21 LMS - CERTIFICATE UI
Display and manage certificates for students

Features:
- Certificate gallery
- View certificates
- Download certificates
- Share on LinkedIn
- Verify certificates
"""

import streamlit as st
from lms_certificates import (
    get_user_certificates, get_certificate,
    generate_certificate_html, get_linkedin_share_url,
    verify_certificate
)
from datetime import datetime


def render_certificates_gallery(user_email):
    """Render the user's certificate gallery"""
    
    st.subheader("🏆 My Certificates")
    
    certificates = get_user_certificates(user_email)
    
    if not certificates:
        st.info("📚 Complete courses to earn certificates!")
        st.markdown("""
        **How to earn certificates:**
        1. Enroll in a course
        2. Complete all lessons
        3. Pass all quizzes
        4. Receive your certificate!
        
        Certificates are automatically generated when you complete a course.
        """)
        return
    
    st.markdown(f"**You've earned {len(certificates)} certificate{'s' if len(certificates) != 1 else ''}!** 🎉")
    
    st.markdown("---")
    
    # Display certificates
    for cert in certificates:
        render_certificate_card(cert)


def render_certificate_card(cert):
    """Render a certificate card"""
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 🏆 {cert['course_title']}")
            
            completion_date = datetime.fromisoformat(cert['completion_date'])
            date_str = completion_date.strftime('%B %d, %Y')
            
            st.caption(f"✅ Completed on {date_str}")
            st.caption(f"🆔 Certificate ID: `{cert['certificate_id']}`")
        
        with col2:
            if st.button("👁️ View", key=f"view_{cert['certificate_id']}"):
                st.session_state.viewing_certificate = cert['certificate_id']
                st.rerun()
        
        st.markdown("---")


def render_certificate_viewer(cert_id):
    """Render full certificate view"""
    
    cert = get_certificate(cert_id)
    
    if not cert:
        st.error("Certificate not found")
        return
    
    # Back button
    if st.button("⬅️ Back to Certificates"):
        if 'viewing_certificate' in st.session_state:
            del st.session_state.viewing_certificate
        st.rerun()
    
    st.markdown("---")
    
    # Certificate display
    cert_html = generate_certificate_html(cert_id)
    st.markdown(cert_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download PDF", use_container_width=True):
            st.info("💡 PDF download feature coming soon! For now, you can print this page as PDF.")
    
    with col2:
        linkedin_url = get_linkedin_share_url(cert_id)
        if linkedin_url:
            st.link_button(
                "🔗 Share on LinkedIn",
                linkedin_url,
                use_container_width=True
            )
    
    with col3:
        if st.button("📧 Email Certificate", use_container_width=True):
            st.info("💡 Email feature coming soon!")
    
    st.markdown("---")
    
    # Verification info
    st.markdown("### ✅ Certificate Verification")
    st.info(f"""
    This certificate can be verified at:
    
    **https://t21-rtt-validator.streamlit.app/verify/{cert_id}**
    
    Certificate ID: `{cert_id}`
    """)


def render_certificate_verification_page(cert_id):
    """Public certificate verification page"""
    
    st.title("🔍 Certificate Verification")
    
    if verify_certificate(cert_id):
        cert = get_certificate(cert_id)
        
        st.success("✅ **CERTIFICATE VERIFIED**")
        
        st.markdown("---")
        
        # Display certificate
        cert_html = generate_certificate_html(cert_id)
        st.markdown(cert_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Verification details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Certificate Holder:**")
            st.info(cert['user_name'])
        
        with col2:
            st.markdown("**Course:**")
            st.info(cert['course_title'])
        
        completion_date = datetime.fromisoformat(cert['completion_date'])
        issued_date = datetime.fromisoformat(cert['issued_date'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Completed:**")
            st.info(completion_date.strftime('%B %d, %Y'))
        
        with col2:
            st.markdown("**Issued:**")
            st.info(issued_date.strftime('%B %d, %Y'))
        
        st.markdown("---")
        
        st.success("""
        ✅ This certificate is **AUTHENTIC** and was issued by T21 Services UK.
        
        T21 Services is a registered training provider for NHS and healthcare professionals.
        """)
    
    else:
        st.error("❌ **CERTIFICATE NOT FOUND**")
        
        st.warning("""
        This certificate ID could not be verified in our system.
        
        Possible reasons:
        - Invalid certificate ID
        - Certificate may have been revoked
        - Typing error in the certificate ID
        
        Please check the certificate ID and try again.
        """)
        
        st.markdown("---")
        
        st.info("""
        **Need help?**
        
        Contact us at: admin@t21services.co.uk
        """)


def render_mini_certificate_preview(cert):
    """Render a mini certificate preview"""
    
    completion_date = datetime.fromisoformat(cert['completion_date'])
    date_str = completion_date.strftime('%B %d, %Y')
    
    st.markdown(f"""
    <div style="
        border: 3px solid #0066cc;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        text-align: center;
    ">
        <h3 style="color: #0066cc; margin: 0;">🏆 Certificate of Achievement</h3>
        <p style="font-size: 20px; margin: 10px 0;"><strong>{cert['user_name']}</strong></p>
        <p style="font-size: 16px; font-style: italic;">{cert['course_title']}</p>
        <p style="font-size: 14px; color: #666;">Completed: {date_str}</p>
        <p style="font-size: 12px; color: #999; font-family: monospace;">ID: {cert['certificate_id']}</p>
    </div>
    """, unsafe_allow_html=True)
