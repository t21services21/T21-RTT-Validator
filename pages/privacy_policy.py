"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Privacy Policy Page

By T21 Services Limited
Company No: 13091053
"""

import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Privacy Policy | T21 Services Limited",
    page_icon="🔒",
    layout="wide"
)

# Custom sidebar
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from sidebar_manager import render_sidebar
    render_sidebar()
except:
    pass

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin-bottom: 30px;'>
    <h1 style='color: white; margin: 0;'>🔒 Privacy Policy</h1>
    <p style='color: white; margin: 10px 0 0 0;'>T21 Services Limited - Healthcare Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

st.markdown("**Last Updated:** October 9, 2025")
st.markdown("**Company:** T21 Services Limited (Company No: 13091053)")
st.markdown("**Address:** 64 Upper Parliament Street, Liverpool, L8 7LF, England")

st.markdown("---")

# Privacy Policy Content
st.markdown("""
## 1. Introduction

Welcome to T21 Services Limited ("we," "our," or "us"). We are committed to protecting your personal data and respecting your privacy.

This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our T21 Healthcare Intelligence Platform.

**Contact Information:**
- **Company Name:** T21 Services Limited
- **Company Number:** 13091053
- **Registered Address:** 64 Upper Parliament Street, Liverpool, L8 7LF, England
- **Email:** privacy@t21services.co.uk
- **Website:** www.t21services.co.uk

---

## 2. Information We Collect

### 2.1 Personal Information
When you register or use our platform, we collect:
- **Account Information:** Name, email address, password (encrypted)
- **Professional Information:** Job title, organization, role
- **Contact Details:** Phone number, mailing address (if provided)
- **Payment Information:** Processed securely through third-party payment processors

### 2.2 Usage Information
We automatically collect:
- **Login Data:** IP address, login times, device information
- **Geolocation:** Approximate location based on IP address (for security)
- **Platform Usage:** Pages visited, features used, time spent
- **Training Progress:** Scenarios completed, scores, certifications

### 2.3 Technical Information
- Browser type and version
- Operating system
- Device identifiers
- Cookies and similar technologies

---

## 3. How We Use Your Information

We use your information for:

### 3.1 Service Delivery
- Providing access to the platform
- Processing your training scenarios
- Generating AI-powered insights
- Managing your account and license

### 3.2 Communication
- Sending account notifications
- Providing customer support
- Sending educational content
- Marketing communications (with your consent)

### 3.3 Security & Fraud Prevention
- Monitoring suspicious login activity
- Detecting unusual location patterns
- Preventing unauthorized access
- Protecting against cyber threats

### 3.4 Improvement & Analytics
- Analyzing platform usage
- Improving AI algorithms
- Developing new features
- Conducting research (anonymized data)

### 3.5 Legal Compliance
- Complying with UK and EU laws
- Responding to legal requests
- Enforcing our terms of service
- Protecting rights and safety

---

## 4. Legal Basis for Processing (GDPR)

We process your data under:

- **Contract Performance:** To provide our services to you
- **Legitimate Interests:** Platform improvement, security, marketing
- **Consent:** Where you have given explicit consent
- **Legal Obligation:** Compliance with UK/EU law

---

## 5. Data Sharing & Disclosure

### 5.1 We DO NOT Sell Your Data
We never sell, rent, or trade your personal information.

### 5.2 We Share Data With:

**Service Providers:**
- Cloud hosting (secure servers)
- Payment processors (encrypted transactions)
- Email services (for notifications)
- Analytics tools (anonymized data)

**Legal Requirements:**
- Law enforcement (when legally required)
- Regulators (NHS, ICO, etc.)
- Courts (in legal proceedings)

**Business Transfers:**
- In case of merger, acquisition, or sale

### 5.3 NHS Organizations
If you use our platform through an NHS organization:
- Your employer may access your training records
- Aggregated performance data may be shared
- Individual medical records are NEVER shared

---

## 6. Data Security

We implement robust security measures:

### 6.1 Technical Safeguards
- 256-bit SSL/TLS encryption
- Encrypted password storage (SHA-256 hashing)
- Regular security audits
- Firewall protection
- Intrusion detection systems

### 6.2 Organizational Safeguards
- Staff training on data protection
- Access controls (role-based)
- Confidentiality agreements
- Incident response procedures

### 6.3 Monitoring
- Real-time security alerts
- Suspicious login detection
- Multiple location tracking
- Failed login monitoring

---

## 7. Data Retention

We retain your data for:

- **Active Accounts:** Duration of your subscription + 6 months
- **Inactive Accounts:** Up to 2 years, then deleted
- **Training Records:** Up to 7 years (NHS regulatory requirements)
- **Financial Records:** 7 years (UK tax law)
- **Marketing Data:** Until you unsubscribe + 3 months

You can request deletion at any time (subject to legal obligations).

---

## 8. Your Rights (GDPR & UK Data Protection)

You have the right to:

### 8.1 Access
Request a copy of your personal data

### 8.2 Rectification
Correct inaccurate or incomplete data

### 8.3 Erasure ("Right to be Forgotten")
Request deletion of your data

### 8.4 Restriction
Limit how we process your data

### 8.5 Portability
Receive your data in a portable format

### 8.6 Object
Object to processing based on legitimate interests

### 8.7 Withdraw Consent
Withdraw consent for marketing communications

### 8.8 Complain
Lodge a complaint with the ICO (UK regulator)

**To exercise your rights, email:** privacy@t21services.co.uk

---

## 9. Cookies & Tracking

We use cookies for:
- Authentication (keep you logged in)
- Preferences (remember your settings)
- Analytics (understand platform usage)
- Security (detect suspicious activity)

You can control cookies in your browser settings.

---

## 10. Third-Party Links

Our platform may contain links to third-party websites. We are not responsible for their privacy practices. Please review their policies.

---

## 11. Children's Privacy

Our platform is NOT intended for users under 18 without parental consent. We do not knowingly collect data from children under 18.

If you are under 18, please obtain parental consent before registering.

---

## 12. International Data Transfers

Your data is primarily stored in the UK. If transferred internationally, we ensure:
- Adequate safeguards (Standard Contractual Clauses)
- GDPR compliance
- Secure encryption during transfer

---

## 13. NHS-Specific Data

If you are an NHS professional using our platform:

### 13.1 NHS Data
- We do NOT access patient data
- We do NOT integrate with patient records
- We only process training/admin data

### 13.2 Caldicott Principles
We adhere to NHS Caldicott Principles:
- Justify the purpose
- Only use when necessary
- Use minimum necessary data
- Access on need-to-know basis
- Everyone has responsibilities
- Understand and comply with the law
- Duty to share information

---

## 14. Changes to This Policy

We may update this policy periodically. Changes will be posted on this page with an updated "Last Updated" date.

Significant changes will be communicated via email.

---

## 15. Contact Us

For privacy questions or to exercise your rights:

**Privacy Team:**
- **Email:** privacy@t21services.co.uk
- **Mail:** T21 Services Limited, Privacy Team, 64 Upper Parliament Street, Liverpool, L8 7LF, England
- **Phone:** [Your Phone Number]

**Data Protection Officer (if applicable):**
- **Email:** dpo@t21services.co.uk

**Regulator (UK):**
- **Information Commissioner's Office (ICO)**
- Website: ico.org.uk
- Helpline: 0303 123 1113

---

## 16. Regulatory Compliance

We comply with:
- 🇬🇧 **UK Data Protection Act 2018**
- 🇪🇺 **General Data Protection Regulation (GDPR)**
- 🏥 **NHS Data Security and Protection Toolkit**
- 💳 **Payment Card Industry Data Security Standard (PCI DSS)**
- 📧 **Privacy and Electronic Communications Regulations (PECR)**

---

## Your Consent

By using our platform, you consent to this Privacy Policy.

If you do not agree, please do not use our services.

---

**T21 Services Limited**  
Company No: 13091053  
Registered in England and Wales  
www.t21services.co.uk

© 2020-2025 T21 Services Limited. All rights reserved.
""")

st.markdown("---")

# Back button
if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>T21 Services Limited</strong> | Company No: 13091053 | Liverpool, England</p>
    <p>📧 privacy@t21services.co.uk | 🌐 www.t21services.co.uk</p>
</div>
""", unsafe_allow_html=True)
