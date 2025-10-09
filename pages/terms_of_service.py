"""
T21 HEALTHCARE INTELLIGENCE PLATFORM
Terms of Service Page

By T21 Services Limited
Company No: 13091053
"""

import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Terms of Service | T21 Services Limited",
    page_icon="📄",
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
    <h1 style='color: white; margin: 0;'>📄 Terms of Service</h1>
    <p style='color: white; margin: 10px 0 0 0;'>T21 Services Limited - Healthcare Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

st.markdown("**Effective Date:** October 9, 2025")
st.markdown("**Company:** T21 Services Limited (Company No: 13091053)")
st.markdown("**Address:** 64 Upper Parliament Street, Liverpool, L8 7LF, England")

st.markdown("---")

# Terms of Service Content
st.markdown("""
## 1. Agreement to Terms

By accessing or using the T21 Healthcare Intelligence Platform ("Platform"), you agree to be bound by these Terms of Service ("Terms").

**IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THE PLATFORM.**

**Platform Provider:**
- **Company Name:** T21 Services Limited
- **Company Number:** 13091053
- **Registered Address:** 64 Upper Parliament Street, Liverpool, L8 7LF, England
- **Website:** www.t21services.co.uk
- **Contact:** info@t21services.co.uk

---

## 2. Definitions

- **"Platform"** = T21 Healthcare Intelligence Platform (software and services)
- **"User"** / **"You"** = Individual or organization using the Platform
- **"We"** / **"Us"** / **"T21"** = T21 Services Limited
- **"NHS Organization"** = NHS Trusts, hospitals, healthcare providers
- **"Student"** = Individual learner using training features
- **"Content"** = All materials, data, and information on the Platform

---

## 3. Eligibility

### 3.1 Age Requirement
You must be at least 18 years old to use the Platform. Users under 18 require parental/guardian consent.

### 3.2 Professional Use
This Platform is designed for healthcare professionals, students, and NHS organizations in the UK.

### 3.3 Accuracy
You agree to provide accurate, current, and complete information during registration.

---

## 4. User Accounts

### 4.1 Account Types

**Taster (1 Month):**
- £99 for 1 month
- Limited platform access
- AI tutor (10 questions/day)
- Sample scenarios and demo tools

**Tier 1 - Platform Practice (6 Months):**
- £499 for 6 months
- Full platform access
- Unlimited AI tutor
- Complete hands-on clinical tools
- RTT Clinical Validator, Pathway Validator, Appointment System

**Tier 2 - TQUK Certification (12 Months):**
- £1,299 for 12 months
- 8-week intensive certification program
- Official TQUK certification (Ofqual-regulated)
- Live Zoom tutor sessions (4 sessions)
- Alumni network access (lifetime)
- 10 months continued platform access after certification

**Tier 3 - Premium Job Placement (12 Months):**
- £1,799 for 12 months
- Everything in Tier 2 PLUS:
- Our staff applies to NHS jobs on your behalf
- 3-5 NHS interview invitations guaranteed (no time limit)
- 5 × 1-on-1 mock interview coaching sessions
- Unlimited application reviews
- Weekly accountability check-ins
- Support until employed

**NHS Organization Licenses:**
- Custom pricing based on trust size
- Bulk user management
- Contact sales@t21services.co.uk

### 4.2 Account Security
You are responsible for:
- Keeping your password confidential
- All activity under your account
- Notifying us of unauthorized access
- Logging out after each session

### 4.3 Account Termination
We may suspend or terminate your account if:
- You violate these Terms
- You provide false information
- Payment fails
- Suspicious or fraudulent activity detected

---

## 5. Subscription & Payment

### 5.1 Fees
All fees are in GBP (£) and exclude VAT (if applicable).

### 5.2 Payment Options

**Pay in Full (BEST DEAL - Save Money!):**
- **Tier 1:** £449 (save £50!)
- **Tier 2:** £1,199 (save £100!)
- **Tier 3:** £1,699 (save £100!)
- One-time payment, immediate access
- No recurring charges

**Installment Plans (Convenience Fee Applied):**

**Tier 1 (£499 regular):**
- 2 payments: £259 (month 1) + £259 (month 4) = £518 (+£19)
- 3 payments: £175 × 3 (every 2 months) = £525 (+£26)

**Tier 2 (£1,299 regular - 8 week program):**
- 2 payments: £700 (month 1) + £650 (month 5) = £1,350 (+£51)
- 3 payments: £475 × 3 (months 1, 4, 7) = £1,425 (+£126)

**Tier 3 (£1,799 regular - 8 week program + job placement):**
- 2 payments: £925 (month 1) + £925 (month 5) = £1,850 (+£51)
- 3 payments: £625 × 3 (months 1, 4, 7) = £1,875 (+£76)

**⚠️ NO MONTHLY PAYMENT OPTIONS**
- Prevents gaming the system
- First payment covers 50%+ of cost

**Payment Methods:**
- Credit/debit card (Visa, Mastercard, Amex)
- PayPal
- Bank transfer (UK only, full payment only)
- All prices in GBP (£)

### 5.3 Refunds
- **Taster (£99):** 48-hour money-back guarantee if not satisfied
- **Tier 1 (£499):** 7-day money-back guarantee
- **Tier 2 (£1,299):** No refunds after TQUK certification issued
- **Tier 3 (£1,799):** No refunds (unlimited job placement service provided)
- **NHS Organizations:** As per contract terms

### 5.4 Tier 3 Job Placement Service Terms
**Our Guarantee:**
- We guarantee 3-5 NHS interview invitations
- No time limit - we continue applying until target achieved
- Service is non-refundable (we provide unlimited support, not money back)

**Your Obligations:**
- Must complete TQUK certification program
- Must attend all 5 mock interview sessions
- Must respond to our communications within 48 hours
- Must be actively seeking employment
- Must accept interviews when offered

**Service Termination:**
We may terminate job placement service if you:
- Stop responding for 30+ consecutive days
- Decline 3+ interview invitations without valid reason
- Fail to attend scheduled mock interview sessions
- Are not actively participating in job search

### 5.5 Installment Plan Terms - LEGALLY BINDING CONTRACT

**⚠️ CRITICAL: Installment plans are LEGALLY BINDING CONTRACTS**

By choosing an installment plan, you agree to pay ALL scheduled payments, even if you:
- Complete the program early
- No longer wish to continue
- Change your mind
- Experience financial hardship
- Leave the country

**Legal Obligations:**
- All payments are legally enforceable
- We may pursue collections or legal action for non-payment
- You remain liable for full balance regardless of program completion
- Certificate/credentials withheld until final payment received

**Payment Structure:**
- **First payment: 50%+ of total cost** (covers our operational costs)
- **Subsequent payments:** Scheduled 3-4 months apart
- **Auto-debit required:** Valid credit/debit card kept on file
- **Automatic charges:** Payments processed automatically on due date

**Failed Payment Consequences:**
- **1st missed payment:** 
  - 7-day grace period
  - £25 late fee applied
  - Warning email sent
- **2nd missed payment:** 
  - Account immediately suspended
  - Platform access blocked
  - £50 late fee applied
- **3rd missed payment or 30+ days overdue:** 
  - Sent to collections agency
  - Legal action initiated
  - Certificate permanently withheld
  - Credit rating impact
  - Additional fees may apply

**Certificate/Credential Release:**
- **Tier 2 & 3:** TQUK certificate held until FINAL payment received
- Even if you complete program in 8 weeks, certificate withheld until payment plan complete
- **No exceptions or early releases** (prevents payment avoidance)
- Job placement services paused if payments missed (Tier 3)

**Example - Tier 2, 2 Payments:**
- Enroll Oct 1: Pay £700 (immediate program start)
- Complete program: Week 8 (mid-November)
- Pass exam: Week 8 (mid-November)
- **Certificate withheld**
- Mar 1: Pay £650 (final payment)
- Mar 2: **Certificate issued**

**Early Payoff (Recommended):**
- Pay remaining balance anytime
- Receive 5% discount on remaining balance
- Immediate certificate release (if program complete)
- Contact support@t21services.co.uk

### 5.6 Auto-Renewal
- **Taster (£99):** Does NOT auto-renew
- **Tier 1-3:** Do NOT auto-renew (fixed-term programs)
- You must manually renew or upgrade at end of period
- No surprise charges

### 5.7 Price Changes
We may change prices with 30 days' notice. Price changes do not affect active subscriptions or installment plans.

---

## 6. License & Permitted Use

### 6.1 License Grant
We grant you a limited, non-exclusive, non-transferable, revocable license to access and use the Platform for its intended purpose.

### 6.2 Permitted Use
You may use the Platform to:
- Complete training scenarios
- Access NHS administration tools
- Generate reports and analytics
- Collaborate with colleagues (if applicable)

### 6.3 Prohibited Use
You may NOT:
- Share your account credentials
- Access the Platform using automated tools (bots, scrapers)
- Reverse engineer or decompile the Platform
- Copy, modify, or distribute Platform content
- Use the Platform for illegal purposes
- Attempt to bypass security measures
- Upload malicious code or viruses
- Impersonate another user
- Resell or sublicense Platform access
- Use the Platform outside the UK without permission

---

## 7. Intellectual Property

### 7.1 Our Ownership
We own all rights to:
- Platform software and code
- Training scenarios and content
- AI models and algorithms
- Trademarks and branding
- Documentation and materials

### 7.2 Your Content
You retain ownership of data you upload, but grant us a license to:
- Store and process your data
- Display it within the Platform
- Use anonymized data for improvement

### 7.3 Trademarks
"T21 Services," the T21 logo, and other marks are our trademarks. Unauthorized use is prohibited.

---

## 8. Training & Certification

### 8.1 Educational Purpose
Training scenarios are for educational purposes only and supplement (but do not replace) formal NHS training and on-the-job experience.

### 8.2 TQUK Certification (Tier 2 & 3 Only)
**Official Qualification:**
- TQUK (Training Qualifications UK) certification
- Ofqual-regulated qualification
- NHS-recognized credential
- Nationally recognized in the UK
- Awarded upon successful completion of 8-week program

**Program Requirements:**
- Attend all training sessions
- Complete all assessments
- Pass final TQUK examination
- Demonstrate competency in RTT administration

**Certification Details:**
- Official TQUK certificate issued
- Digital credential provided
- Verifiable by employers
- Valid indefinitely (does not expire)

### 8.3 Job Placement Support (Tier 3 Only)
**What We Provide:**
- Professional NHS job application writing and submission
- 3-5 guaranteed interview invitations (no time limit)
- Mock interview preparation sessions
- Application strategy and guidance
- LinkedIn profile optimization
- Support until employed

**What We Do NOT Guarantee:**
- Job offers (hiring decisions are made by NHS employers)
- Specific job titles or salaries
- Employment within a specific timeframe
- Interviews at specific NHS trusts

**Your Responsibility:**
- Interview performance and success
- Meeting NHS employer requirements
- Accepting suitable job offers

### 8.4 Limitations
We do not guarantee:
- Employment outcomes
- Specific salary levels
- Job placement timelines (though average is 2-4 months)
- Acceptance by any specific NHS trust

---

## 9. Operational Tools (NHS Organizations)

### 9.1 Accuracy
While our AI tools are highly accurate, you are responsible for:
- Verifying all AI-generated recommendations
- Final decision-making
- Compliance with NHS protocols
- Patient safety

### 9.2 Not Medical Advice
The Platform provides administrative tools, NOT medical advice or clinical decision support.

### 9.3 Integration
If integrating with existing NHS systems, you ensure:
- Data security compliance
- Proper authorization
- Information governance approval

---

## 10. Data Protection & Privacy

### 10.1 Privacy Policy
Our Privacy Policy (available separately) explains how we handle your data.

### 10.2 GDPR Compliance
We comply with UK GDPR and Data Protection Act 2018.

### 10.3 Your Responsibilities
You agree to:
- Comply with data protection laws
- Not upload patient-identifiable data without authorization
- Obtain necessary consents
- Report data breaches to us immediately

---

## 11. Service Availability

### 11.1 Uptime
We strive for 99.5% uptime but do not guarantee uninterrupted service.

### 11.2 Maintenance
We may perform scheduled maintenance with advance notice.

### 11.3 Force Majeure
We are not liable for service interruptions due to events beyond our control (natural disasters, cyberattacks, etc.).

---

## 12. Limitation of Liability

### 12.1 No Warranties
THE PLATFORM IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND.

### 12.2 Liability Cap
Our total liability is limited to:
- **Students:** Amount paid in the last 12 months
- **NHS Organizations:** As per contract terms

### 12.3 Exclusions
We are NOT liable for:
- Indirect, consequential, or incidental damages
- Loss of profits, data, or goodwill
- Third-party actions
- User negligence

### 12.4 NHS-Specific
We are NOT liable for:
- Clinical decisions made using Platform data
- Patient harm resulting from misuse
- Non-compliance with NHS protocols

---

## 13. Indemnification

You agree to indemnify and hold us harmless from claims arising from:
- Your use of the Platform
- Your violation of these Terms
- Your violation of any laws
- Your infringement of third-party rights

---

## 14. User Content & Conduct

### 14.1 Acceptable Conduct
You agree to:
- Use the Platform professionally and ethically
- Respect other users
- Comply with NHS values (if applicable)
- Report bugs or security issues

### 14.2 Prohibited Content
Do NOT upload:
- Patient-identifiable information (without authorization)
- Offensive, defamatory, or discriminatory content
- Copyrighted material without permission
- Malware or harmful code

### 14.3 Monitoring
We reserve the right to monitor and remove content violating these Terms.

---

## 15. Third-Party Services

### 15.1 Integrations
The Platform may integrate with third-party services (payment processors, analytics, etc.).

### 15.2 No Endorsement
We do not endorse third-party services and are not responsible for their actions.

### 15.3 Third-Party Terms
You must comply with third-party terms of service.

---

## 16. Termination

### 16.1 By You
You may cancel your subscription anytime via your account settings.

### 16.2 By Us
We may terminate your account immediately if you:
- Breach these Terms
- Engage in fraudulent activity
- Pose a security risk

### 16.3 Effect of Termination
Upon termination:
- Your access is immediately revoked
- Your data is retained per our Privacy Policy
- Outstanding fees remain due

---

## 17. Changes to Terms

### 17.1 Updates
We may update these Terms periodically. Changes effective upon posting.

### 17.2 Notification
Significant changes will be communicated via email or Platform notification.

### 17.3 Continued Use
Continued use after changes constitutes acceptance.

---

## 18. Dispute Resolution

### 18.1 Governing Law
These Terms are governed by the laws of England and Wales.

### 18.2 Jurisdiction
Courts of England and Wales have exclusive jurisdiction.

### 18.3 Informal Resolution
We encourage resolving disputes informally by contacting us first.

### 18.4 Arbitration (Optional)
Parties may agree to binding arbitration.

---

## 19. General Provisions

### 19.1 Entire Agreement
These Terms constitute the entire agreement between you and us.

### 19.2 Severability
If any provision is unenforceable, the remaining provisions remain in effect.

### 19.3 No Waiver
Failure to enforce any provision does not waive our right to enforce it later.

### 19.4 Assignment
You may not assign these Terms. We may assign them to a successor.

### 19.5 Force Majeure
We are not liable for failures due to circumstances beyond our control.

---

## 20. Contact Information

For questions about these Terms:

**General Inquiries:**
- **Email:** info@t21services.co.uk
- **Phone:** [Your Phone Number]

**Legal Department:**
- **Email:** legal@t21services.co.uk
- **Mail:** T21 Services Limited, Legal Department, 64 Upper Parliament Street, Liverpool, L8 7LF, England

**Sales (NHS Organizations):**
- **Email:** sales@t21services.co.uk

**Support:**
- **Email:** support@t21services.co.uk

---

## Acknowledgment

BY CLICKING "I AGREE" OR BY ACCESSING THE PLATFORM, YOU ACKNOWLEDGE THAT YOU HAVE READ, UNDERSTOOD, AND AGREE TO BE BOUND BY THESE TERMS OF SERVICE.

---

**T21 Services Limited**  
Company No: 13091053  
Registered in England and Wales  
www.t21services.co.uk

© 2020-2025 T21 Services Limited. All rights reserved.
""")

st.markdown("---")

# Agreement checkbox
st.markdown("### Agreement")
if st.checkbox("I have read and agree to the Terms of Service"):
    st.success("✅ Thank you for reviewing our Terms of Service")

# Back button
if st.button("← Back to Home"):
    st.switch_page("landing_page.py")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>T21 Services Limited</strong> | Company No: 13091053 | Liverpool, England</p>
    <p>📧 legal@t21services.co.uk | 🌐 www.t21services.co.uk</p>
</div>
""", unsafe_allow_html=True)
