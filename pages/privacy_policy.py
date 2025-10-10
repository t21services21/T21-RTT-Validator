"""
T21 SERVICES - PRIVACY POLICY PAGE
"""

import streamlit as st

st.set_page_config(page_title="Privacy Policy | T21 Services", page_icon="🔒", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.title("🔒 Privacy Policy")
st.markdown("---")

st.write("""
## T21 Services Limited - Privacy Policy

**Last Updated:** October 10, 2025  
**Company Number:** 13091053  
**Registered Address:** Liverpool, England, UK

---

### 1. Introduction

T21 Services Limited is committed to protecting your privacy and personal data in accordance with UK GDPR and Data Protection Act 2018.

### 2. Data We Collect

- Name and contact information
- Email address and phone number
- Training records and progress
- Payment information
- Usage data and analytics

### 3. How We Use Your Data

- To provide training services
- To communicate with you
- To improve our services
- To comply with legal obligations

### 4. Your Rights Under UK GDPR

You have the right to:
- Access your personal data
- Rectify inaccurate data
- Request deletion of your data
- Object to processing
- Data portability
- Withdraw consent

### 5. Data Security

We implement robust security measures including:
- Encryption of data in transit and at rest
- Access controls and authentication
- Regular security audits
- Secure UK-based hosting

### 6. Data Retention

- Active accounts: Duration of service + 7 years
- Training records: 7 years (NHS compliance)
- Financial records: 7 years (HMRC requirement)

### 7. Contact Us

**Data Protection Officer:**  
Email: dpo@t21services.co.uk  
Phone: +44 (0) 151 123 4567

**For Privacy Concerns:**  
Email: privacy@t21services.co.uk

**Supervisory Authority:**  
Information Commissioner's Office (ICO)  
Website: www.ico.org.uk  
Helpline: 0303 123 1113

---

**Company Details:**  
T21 Services Limited  
Company Number: 13091053  
Registered in England and Wales

---

*This privacy policy is compliant with UK GDPR, Data Protection Act 2018, and NHS data protection requirements.*
""")

st.markdown("---")

if st.button("← Back to Home"):
    st.switch_page("app.py")
