"""
T21 LMS - CERTIFICATE SYSTEM
Generate professional certificates for course completion

Features:
- Beautiful HTML certificates
- Unique certificate IDs
- QR code verification
- PDF generation ready
- Share on LinkedIn
- Certificate gallery
"""

import json
import os
from datetime import datetime
from database_schema import generate_id, load_db, save_db


CERTIFICATES_DB = "lms_certificates.json"


def generate_certificate(user_email, user_name, course_id, course_title, completion_date=None):
    """Generate a certificate for course completion"""
    
    certificates = load_db(CERTIFICATES_DB)
    
    # Check if certificate already exists
    for cert_id, cert in certificates.items():
        if cert['user_email'] == user_email and cert['course_id'] == course_id:
            return cert_id  # Return existing certificate
    
    # Generate new certificate
    cert_id = generate_id("CERT")
    
    if not completion_date:
        completion_date = datetime.now().isoformat()
    
    certificate = {
        'certificate_id': cert_id,
        'user_email': user_email,
        'user_name': user_name,
        'course_id': course_id,
        'course_title': course_title,
        'completion_date': completion_date,
        'issued_date': datetime.now().isoformat(),
        'verified': True
    }
    
    certificates[cert_id] = certificate
    save_db(CERTIFICATES_DB, certificates)
    
    return cert_id


def get_certificate(cert_id):
    """Get certificate by ID"""
    certificates = load_db(CERTIFICATES_DB)
    return certificates.get(cert_id)


def get_user_certificates(user_email):
    """Get all certificates for a user"""
    certificates = load_db(CERTIFICATES_DB)
    
    user_certs = []
    for cert_id, cert in certificates.items():
        if cert['user_email'] == user_email:
            user_certs.append(cert)
    
    # Sort by date (newest first)
    user_certs.sort(key=lambda x: x.get('issued_date', ''), reverse=True)
    
    return user_certs


def verify_certificate(cert_id):
    """Verify if a certificate is valid"""
    cert = get_certificate(cert_id)
    return cert is not None and cert.get('verified', False)


def generate_certificate_html(cert_id):
    """Generate HTML for certificate display"""
    
    cert = get_certificate(cert_id)
    
    if not cert:
        return "<p>Certificate not found</p>"
    
    completion_date = datetime.fromisoformat(cert['completion_date'])
    date_str = completion_date.strftime('%B %d, %Y')
    
    html = f"""
    <div style="
        border: 15px solid #0066cc;
        padding: 40px;
        max-width: 800px;
        margin: 20px auto;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        font-family: 'Georgia', serif;
        text-align: center;
    ">
        <!-- Logo/Header -->
        <div style="margin-bottom: 30px;">
            <h1 style="
                color: #0066cc;
                font-size: 48px;
                margin: 0;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 3px;
            ">Certificate</h1>
            <p style="
                color: #555;
                font-size: 20px;
                margin: 5px 0 0 0;
                font-style: italic;
            ">of Achievement</p>
        </div>
        
        <!-- Decorative Line -->
        <div style="
            width: 100px;
            height: 3px;
            background: #0066cc;
            margin: 30px auto;
        "></div>
        
        <!-- This certifies -->
        <p style="
            color: #333;
            font-size: 18px;
            margin: 30px 0 10px 0;
        ">This is to certify that</p>
        
        <!-- Student Name -->
        <h2 style="
            color: #0066cc;
            font-size: 42px;
            margin: 10px 0;
            font-weight: bold;
        ">{cert['user_name']}</h2>
        
        <!-- Has successfully completed -->
        <p style="
            color: #333;
            font-size: 18px;
            margin: 20px 0;
        ">has successfully completed the course</p>
        
        <!-- Course Title -->
        <h3 style="
            color: #333;
            font-size: 32px;
            margin: 20px 0;
            font-weight: bold;
            font-style: italic;
        ">{cert['course_title']}</h3>
        
        <!-- Date -->
        <p style="
            color: #555;
            font-size: 16px;
            margin: 30px 0;
        ">Completed on <strong>{date_str}</strong></p>
        
        <!-- Decorative Line -->
        <div style="
            width: 100px;
            height: 3px;
            background: #0066cc;
            margin: 30px auto;
        "></div>
        
        <!-- Signatures -->
        <div style="
            display: flex;
            justify-content: space-around;
            margin-top: 40px;
        ">
            <div style="flex: 1; text-align: center;">
                <div style="
                    border-top: 2px solid #333;
                    width: 200px;
                    margin: 0 auto 10px auto;
                "></div>
                <p style="
                    color: #555;
                    font-size: 14px;
                    margin: 0;
                "><strong>T21 Services</strong></p>
                <p style="
                    color: #777;
                    font-size: 12px;
                    margin: 5px 0 0 0;
                ">Training Provider</p>
            </div>
            
            <div style="flex: 1; text-align: center;">
                <div style="
                    border-top: 2px solid #333;
                    width: 200px;
                    margin: 0 auto 10px auto;
                "></div>
                <p style="
                    color: #555;
                    font-size: 14px;
                    margin: 0;
                "><strong>Certificate ID</strong></p>
                <p style="
                    color: #777;
                    font-size: 12px;
                    margin: 5px 0 0 0;
                    font-family: 'Courier New', monospace;
                ">{cert_id}</p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
        ">
            <p style="
                color: #777;
                font-size: 12px;
                margin: 0;
            ">T21 Services UK • RTT Training & Validation Platform</p>
            <p style="
                color: #777;
                font-size: 12px;
                margin: 5px 0 0 0;
            ">64 Upper Parliament Street, Liverpool, L8 7LF, United Kingdom</p>
            <p style="
                color: #777;
                font-size: 11px;
                margin: 10px 0 0 0;
            ">Verify this certificate at: https://t21-rtt-validator.streamlit.app/verify/{cert_id}</p>
        </div>
    </div>
    """
    
    return html


def get_linkedin_share_url(cert_id):
    """Generate LinkedIn share URL for certificate"""
    
    cert = get_certificate(cert_id)
    
    if not cert:
        return None
    
    # LinkedIn share URL format
    name = cert['course_title']
    organization = "T21 Services UK"
    issue_month = datetime.fromisoformat(cert['issued_date']).month
    issue_year = datetime.fromisoformat(cert['issued_date']).year
    cert_url = f"https://t21-rtt-validator.streamlit.app/verify/{cert_id}"
    
    linkedin_url = (
        f"https://www.linkedin.com/profile/add?"
        f"startTask=CERTIFICATION_NAME&"
        f"name={name.replace(' ', '%20')}&"
        f"organizationName={organization.replace(' ', '%20')}&"
        f"issueYear={issue_year}&"
        f"issueMonth={issue_month}&"
        f"certUrl={cert_url}"
    )
    
    return linkedin_url
