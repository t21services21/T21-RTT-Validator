# 📧 EMAIL INTEGRATION GUIDE - ALL MODULES

**Status:** ✅ Email system ready for integration  
**File:** `nhs_email_notifications.py`  
**Coverage:** All NHS clinical events

---

## 🎯 **WHAT'S BEEN CREATED**

### **New File: `nhs_email_notifications.py`**

**9 Comprehensive Email Functions:**
1. ✅ `send_patient_added_to_ptl_email()` - PTL notifications
2. ✅ `send_pbl_acknowledgment_email()` - PBL notifications (already integrated!)
3. ✅ `send_appointment_booked_email()` - Appointment confirmations
4. ✅ `send_appointment_cancelled_email()` - Cancellation notifications
5. ✅ `send_mdt_meeting_scheduled_email()` - MDT meeting invites
6. ✅ `send_referral_received_email()` - Referral acknowledgments
7. ✅ `send_rtt_breach_alert_email()` - Breach risk alerts
8. ✅ `send_2ww_referral_received_email()` - Urgent cancer referrals
9. ✅ `send_letter_generated_notification()` - Clinical letter notifications

---

## 🔧 **HOW TO INTEGRATE (STEP-BY-STEP)**

### **INTEGRATION 1: PTL (Patient Tracking List)**

**File to Modify:** `ptl_system.py` or `ptl_ui.py`

**Where:** When patient is added to PTL

**Add This Code:**
```python
from nhs_email_notifications import send_patient_added_to_ptl_email

# EXISTING CODE: After patient is added to PTL
def add_patient_to_ptl(patient_data):
    # ... existing code to save patient ...
    
    # NEW: Send email notification
    send_patient_added_to_ptl_email(patient_data)
    
    return {"success": True, "message": "Patient added and email sent"}
```

---

### **INTEGRATION 2: PBL (Partial Booking List)**

**Status:** ✅ **ALREADY INTEGRATED!**

PBL already sends acknowledgment emails via `partial_booking_list_system.py`.

No action needed - working automatically!

---

### **INTEGRATION 3: Advanced Booking System**

**File to Modify:** `advanced_booking_system.py` or `advanced_booking_ui.py`

**Where:** When appointment is booked

**Add This Code:**
```python
from nhs_email_notifications import send_appointment_booked_email, send_appointment_cancelled_email

# EXISTING CODE: After appointment is booked
def book_appointment(appointment_data):
    # ... existing code to save appointment ...
    
    # NEW: Send confirmation email
    send_appointment_booked_email(appointment_data)
    
    return {"success": True, "appointment_id": "APT123"}

# EXISTING CODE: When appointment is cancelled
def cancel_appointment(appointment_data):
    # ... existing code to cancel appointment ...
    
    # NEW: Send cancellation email
    send_appointment_cancelled_email(appointment_data)
    
    return {"success": True}
```

---

### **INTEGRATION 4: MDT Coordination**

**File to Modify:** `mdt_coordination_system.py` or `mdt_coordination_ui.py`

**Where:** When MDT meeting is created

**Add This Code:**
```python
from nhs_email_notifications import send_mdt_meeting_scheduled_email

# EXISTING CODE: After MDT meeting is created
def create_mdt_meeting(meeting_data, attendees):
    # ... existing code to save meeting ...
    
    # NEW: Send invites to all attendees
    send_mdt_meeting_scheduled_email(meeting_data, attendees)
    
    return {"success": True, "meeting_id": "MDT123"}
```

---

### **INTEGRATION 5: Referral Management**

**File to Modify:** Where referrals are received

**Add This Code:**
```python
from nhs_email_notifications import send_referral_received_email

# EXISTING CODE: When referral is received
def process_referral(referral_data):
    # ... existing code to save referral ...
    
    # NEW: Send acknowledgment to patient
    send_referral_received_email(referral_data)
    
    return {"success": True}
```

---

### **INTEGRATION 6: RTT Breach Monitoring**

**File to Modify:** `ptl_system.py` or breach monitoring module

**Where:** Daily/weekly breach checks

**Add This Code:**
```python
from nhs_email_notifications import send_rtt_breach_alert_email

# EXISTING CODE: Check all patients for breach risk
def check_breach_risks():
    patients = load_all_ptl_patients()
    
    for patient in patients:
        days_until_breach = calculate_days_until_breach(patient)
        
        # NEW: Send alert if < 28 days to breach
        if days_until_breach < 28:
            send_rtt_breach_alert_email(patient, days_until_breach)
```

---

### **INTEGRATION 7: Cancer Pathways (2WW)**

**File to Modify:** `cancer_pathway_system.py` or `cancer_pathway_ui.py`

**Add This Code:**
```python
from nhs_email_notifications import send_2ww_referral_received_email

# EXISTING CODE: When 2WW referral received
def add_2ww_referral(patient_data):
    # ... existing code ...
    
    # NEW: Send urgent notification
    send_2ww_referral_received_email(patient_data)
    
    return {"success": True}
```

---

### **INTEGRATION 8: Clinical Letters**

**File to Modify:** `clinical_letters_ui.py`

**Add This Code:**
```python
from nhs_email_notifications import send_letter_generated_notification

# EXISTING CODE: After letter is generated
def generate_letter(letter_type, patient_name):
    # ... existing code to generate letter ...
    
    # NEW: Notify relevant staff
    send_letter_generated_notification(
        letter_type=letter_type,
        patient_name=patient_name,
        recipient_email="consultant@trust.nhs.uk"
    )
```

---

## ⚙️ **CONFIGURATION REQUIRED**

### **Step 1: Set Up Email Credentials**

In `st.secrets` (Streamlit secrets) or `.env` file:

```toml
# SendGrid Configuration
SENDGRID_API_KEY = "your_sendgrid_api_key_here"
FROM_EMAIL = "noreply@t21services.co.uk"

# NHS Contact Emails
RTT_COORDINATOR_EMAIL = "rtt.coordinator@trust.nhs.uk"
CANCER_COORDINATOR_EMAIL = "cancer.coordinator@trust.nhs.uk"
MDT_COORDINATOR_EMAIL = "mdt.coordinator@trust.nhs.uk"
```

### **Step 2: Update Email Addresses**

In `nhs_email_notifications.py`, replace placeholder emails:

```python
# FIND these lines and update:
coordinator_email = "rtt.coordinator@trust.nhs.uk"  # YOUR RTT COORDINATOR
cancer_coordinator = "cancer.coordinator@trust.nhs.uk"  # YOUR CANCER COORDINATOR
```

---

## 📧 **EMAIL TEMPLATES INCLUDED**

### **All emails are NHS-compliant with:**
- ✅ Professional NHS branding
- ✅ Clear patient information
- ✅ Action items and next steps
- ✅ Contact information
- ✅ Mobile-responsive design
- ✅ Accessible formatting

### **Email Types:**
1. **Patient Notifications** - Friendly, clear language
2. **Staff Alerts** - Clinical details, action required
3. **Coordinator Notifications** - Full clinical context
4. **Urgent Alerts** - Red/amber/green color coding

---

## ✅ **TESTING EMAILS**

### **Test Email Delivery:**

```python
from nhs_email_notifications import send_patient_added_to_ptl_email

# Test data
test_patient = {
    'name': 'Test Patient',
    'nhs_number': '123 456 7890',
    'email': 'your.email@example.com',  # YOUR EMAIL FOR TESTING
    'specialty': 'Cardiology',
    'priority': 'Routine',
    'referral_date': '2025-10-16'
}

# Send test email
send_patient_added_to_ptl_email(test_patient)
```

### **Check:**
- [ ] Email arrives within 1 minute
- [ ] Formatting looks correct
- [ ] All information displays properly
- [ ] Links work (if any)
- [ ] Mobile display is good

---

## 🚀 **QUICK START IMPLEMENTATION**

### **Priority 1 (Implement First):**
1. ✅ **PBL** - Already done!
2. ✅ **Appointments** - High patient impact
3. ✅ **RTT Breach Alerts** - Critical for compliance

### **Priority 2 (Next Week):**
4. ✅ **PTL notifications**
5. ✅ **MDT meeting invites**
6. ✅ **Referral acknowledgments**

### **Priority 3 (When Needed):**
7. ✅ **Cancer pathway alerts**
8. ✅ **Clinical letter notifications**

---

## 📊 **EMAIL TRACKING & ANALYTICS**

### **Future Enhancements (Optional):**

**Track Email Performance:**
- Delivery rates
- Open rates
- Click rates
- Bounce rates

**Add to each email function:**
```python
from email_analytics import log_email_sent

def send_appointment_booked_email(data):
    result = send_email(...)
    
    # Log for analytics
    log_email_sent(
        email_type="appointment_booked",
        recipient=data['patient_email'],
        status="sent" if result else "failed"
    )
    
    return result
```

---

## 🐛 **TROUBLESHOOTING**

### **Email Not Sending:**
1. Check SendGrid API key is set
2. Verify FROM_EMAIL in secrets
3. Check recipient email is valid
4. Look for errors in console
5. Test SendGrid credentials separately

### **Wrong Content:**
1. Verify patient_data dictionary has all fields
2. Check email template formatting
3. Test with dummy data first

### **Spam Folder:**
1. Set up SPF/DKIM records
2. Use verified sender domain
3. Avoid spam trigger words
4. SendGrid provides domain verification

---

## 📋 **INTEGRATION CHECKLIST**

### **For Each Module:**
- [ ] Identify trigger event (e.g., "patient added")
- [ ] Import relevant email function
- [ ] Call function with correct data
- [ ] Test with dummy data
- [ ] Test with real email
- [ ] Verify email received
- [ ] Check formatting
- [ ] Deploy to production

---

## 💡 **BEST PRACTICES**

### **Do's:**
✅ Send emails for ALL significant events  
✅ Include all relevant information  
✅ Use clear, simple language  
✅ Provide contact information  
✅ Test thoroughly before production  
✅ Log all emails sent  

### **Don'ts:**
❌ Send too many emails (overwhelming)  
❌ Include sensitive clinical details in subject lines  
❌ Use technical jargon with patients  
❌ Forget to handle email failures gracefully  
❌ Send emails without patient consent  

---

## 🎯 **EXPECTED OUTCOMES**

### **After Full Integration:**
- ✅ **100% of clinical events** trigger appropriate emails
- ✅ **Patients** receive timely updates
- ✅ **Staff** get critical alerts
- ✅ **Coordinators** stay informed
- ✅ **Audit trail** complete
- ✅ **Communication gaps** eliminated

### **Benefits:**
- 📧 Better patient communication
- ⏰ Reduced DNA rates
- 🔔 Proactive breach prevention
- 📊 Complete audit trail
- ✅ NHS compliance
- 💚 Improved patient experience

---

## 🎉 **YOU'RE READY!**

**The email system is ready to integrate across ALL your modules!**

**Start with PBL (already done) → Appointments → RTT Alerts**

---

*Email Integration Guide v1.0*  
*Created: 16 October 2025*  
*Status: Ready for deployment*
