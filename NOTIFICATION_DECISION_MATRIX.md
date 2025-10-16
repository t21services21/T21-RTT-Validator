# 📊 NOTIFICATION DECISION MATRIX - WHEN TO USE WHAT

**The Complete Guide to Notifications, Pop-Ups, and Emails**

---

## 🎯 **THE GOLDEN RULES**

### **Rule 1: Urgency Levels**
- 🔴 **CRITICAL (4):** Pop-up + Email + In-app
- 🟠 **HIGH (3):** Email + In-app + Pop-up (optional)
- 🟡 **MEDIUM (2):** Email + In-app
- 🟢 **LOW (1):** In-app only

### **Rule 2: User Impact**
- **Requires immediate action** → Pop-up
- **Important but can wait** → Email + In-app
- **FYI only** → In-app only

### **Rule 3: Event Type**
- **User-initiated** (they did something) → In-app + Email confirmation
- **System-initiated** (something happened) → Email + In-app
- **Urgent alert** (needs immediate action) → Pop-up + Email + In-app

---

## 📋 **COMPLETE NOTIFICATION TABLE**

| Event | Urgency | Pop-Up | Email | In-App | Why |
|-------|---------|--------|-------|--------|-----|
| **RTT BREACH ALERT (<14 days)** | 🔴 CRITICAL | ✅ YES (RED) | ✅ YES | ✅ YES | Immediate action needed! |
| **RTT BREACH ALERT (14-28 days)** | 🟠 HIGH | ❌ NO | ✅ YES | ✅ YES | Important but not immediate |
| **2WW Cancer Referral** | 🔴 CRITICAL | ✅ YES (RED) | ✅ YES | ✅ YES | 14-day deadline critical |
| **Patient Added to PBL** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Patient expects email |
| **Patient Added to PTL** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Patient expects email |
| **Appointment Booked** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Confirmation needed |
| **Appointment Cancelled** | 🟠 HIGH | ❌ NO | ✅ YES | ✅ YES | Patient needs to know ASAP |
| **MDT Meeting Scheduled** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Attendees need to plan |
| **Referral Received** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Patient acknowledgment |
| **Clinical Letter Generated** | 🟢 LOW | ❌ NO | ❌ NO | ✅ YES | FYI for staff |
| **Tier Upgrade Requested** | 🟠 HIGH | ✅ YES (for admin) | ✅ YES | ✅ YES | Admin needs to act |
| **Tier Upgrade APPROVED** | 🟠 HIGH | ✅ YES (GREEN) | ✅ YES | ✅ YES | Student should celebrate! |
| **Tier Upgrade REJECTED** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Disappointing but not urgent |
| **New Message Received** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | User checks messages regularly |
| **New Message (URGENT)** | 🟠 HIGH | ✅ YES (ORANGE) | ✅ YES | ✅ YES | Marked as urgent by sender |
| **Staff Account Created** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Welcome email important |
| **Password Reset Request** | 🟠 HIGH | ❌ NO | ✅ YES | ✅ YES | Security - email essential |
| **Login from New Device** | 🟠 HIGH | ❌ NO | ✅ YES | ✅ YES | Security alert |
| **Module Access Granted** | 🟡 MEDIUM | ✅ YES (GREEN) | ✅ YES | ✅ YES | User should know immediately |
| **Payment Received** | 🟠 HIGH | ✅ YES (GREEN) | ✅ YES | ✅ YES | Confirmation important |
| **Certificate Issued** | 🟠 HIGH | ✅ YES (GREEN) | ✅ YES | ✅ YES | Achievement! |
| **Course Completed** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Progress update |
| **Assignment Due Soon** | 🟠 HIGH | ✅ YES (ORANGE) | ✅ YES | ✅ YES | Reminder needed |
| **System Maintenance** | 🟠 HIGH | ✅ YES (ORANGE) | ✅ YES | ✅ YES | Users need to know |
| **Welcome New User** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | Onboarding email |
| **Trial Expiring (1 day)** | 🔴 CRITICAL | ✅ YES (RED) | ✅ YES | ✅ YES | Last chance! |
| **Trial Expiring (7 days)** | 🟠 HIGH | ❌ NO | ✅ YES | ✅ YES | Warning needed |
| **Data Breach Alert** | 🔴 CRITICAL | ✅ YES (RED) | ✅ YES | ✅ YES | Security critical |
| **Support Ticket Reply** | 🟡 MEDIUM | ❌ NO | ✅ YES | ✅ YES | User expects response |

---

## 🚨 **POP-UP NOTIFICATION RULES**

### **✅ USE POP-UP WHEN:**

1. **Immediate Action Required**
   - RTT breach <14 days
   - 2WW cancer referral
   - Trial expiring in 1 day
   - Payment failed
   - Data breach

2. **Good News (Celebrate!)**
   - Tier upgrade approved
   - Certificate issued
   - Payment received
   - Module access granted

3. **Admin Alerts**
   - New tier upgrade request
   - New staff account request
   - System error

4. **Urgent Messages**
   - Message marked "urgent" by sender
   - Teacher needs immediate response
   - Admin announcement

5. **Security Alerts**
   - Unusual login activity
   - Password changed
   - 2FA code required

### **❌ DON'T USE POP-UP WHEN:**

1. **Routine Updates**
   - Course progress
   - Regular messages
   - General notifications

2. **FYI Information**
   - Clinical letter generated
   - Report available
   - System updates

3. **Low Priority**
   - Newsletter
   - Tips and tricks
   - Feature announcements

---

## 📧 **EMAIL NOTIFICATION RULES**

### **✅ ALWAYS SEND EMAIL FOR:**

1. **Patient Communications**
   - Appointment confirmations
   - Appointment cancellations
   - Referral acknowledgments
   - PBL acknowledgments
   - Any clinical communication

2. **Account & Security**
   - Welcome emails
   - Password resets
   - Login alerts
   - Account changes
   - Payment receipts

3. **Approvals & Requests**
   - Request submitted
   - Request approved
   - Request rejected
   - Any status change

4. **Messages**
   - New message received
   - Reply received
   - Message from admin

5. **Important Updates**
   - Certificate issued
   - Course completed
   - Trial expiring
   - Payment due

### **❌ DON'T SEND EMAIL FOR:**

1. **Very Low Priority**
   - Login success (unless suspicious)
   - Page viewed
   - Button clicked
   - Session started

2. **Too Frequent**
   - Every notification (would overwhelm inbox)
   - Real-time chat messages (unless first message)

3. **User Preference Off**
   - User disabled email notifications
   - Respect their choice!

---

## 🔔 **IN-APP NOTIFICATION RULES**

### **✅ ALWAYS SHOW IN-APP FOR:**

**EVERYTHING!** 

Every event gets an in-app notification. Why?
- Shows in notification center
- Keeps history
- Doesn't overwhelm email
- Users can review anytime
- Badge shows unread count

### **Priority Levels:**

**🔴 URGENT (4):**
- RTT breach <14 days
- 2WW cancer referral
- Critical security alerts
- Payment failed
- Data breach

**🟠 HIGH (3):**
- RTT breach 14-28 days
- Tier upgrade requests
- Tier upgrade approved
- Appointment cancelled
- Urgent messages

**🟡 MEDIUM (2):**
- Patient added to PTL/PBL
- Appointment booked
- Referral received
- MDT meeting scheduled
- Regular messages
- Module access requests

**🟢 LOW (1):**
- Course progress
- Tips and tricks
- Clinical letter generated
- Reports available
- General updates

---

## 🎨 **POP-UP COLOR CODING**

### **🔴 RED (CRITICAL - Requires Immediate Action):**
```
Examples:
- 🚨 RTT BREACH ALERT! Patient Smith - 10 days to breach
- 🚨 2WW CANCER REFERRAL! Must book within 14 days
- 🚨 TRIAL EXPIRES TOMORROW! Upgrade now
- 🚨 DATA BREACH DETECTED! Action required
```

### **🟠 ORANGE (WARNING - Important):**
```
Examples:
- ⚠️ Assignment Due Tomorrow! Submit by 5pm
- ⚠️ RTT Breach Risk - 21 days remaining
- ⚠️ System Maintenance in 1 hour
- ⚠️ Payment Due Soon
```

### **🟢 GREEN (SUCCESS - Good News!):**
```
Examples:
- ✅ Tier Upgrade Approved! You now have Tier 2
- ✅ Certificate Issued! Congratulations
- ✅ Payment Received - Thank you
- ✅ Module Access Granted
```

### **🔵 BLUE (INFO - FYI):**
```
Examples:
- ℹ️ New Feature Available
- ℹ️ Course Updated
- ℹ️ Report Ready to Download
```

---

## 🎯 **DECISION FLOWCHART**

```
EVENT HAPPENS
    ↓
Is it CRITICAL? (Safety/Security/Deadline <14 days)
    ↓ YES → Pop-up (RED) + Email + In-app
    ↓ NO
    ↓
Is it HIGH priority? (User needs to know soon)
    ↓ YES → Email + In-app + Pop-up (if good news)
    ↓ NO
    ↓
Is it MEDIUM priority? (User should know)
    ↓ YES → Email + In-app
    ↓ NO
    ↓
Is it LOW priority? (FYI)
    ↓ YES → In-app only
    ↓
DONE
```

---

## 📊 **BY USER ROLE**

### **Students:**
- **Pop-ups:** Tier approved, certificate issued, urgent messages, trial expiring
- **Email:** All confirmations, approvals, messages
- **In-app:** Everything

### **Teachers:**
- **Pop-ups:** Urgent student messages, admin requests, system alerts
- **Email:** Student messages, admin communications
- **In-app:** Everything

### **Admin:**
- **Pop-ups:** New requests, urgent alerts, system errors
- **Email:** All requests, important updates
- **In-app:** Everything

### **NHS Coordinators:**
- **Pop-ups:** RTT breaches, 2WW referrals, critical alerts
- **Email:** All clinical events, breach warnings
- **In-app:** Everything

---

## 🔧 **IMPLEMENTATION CODE**

### **How to Use in Your Code:**

```python
from notification_system import create_notification, NotificationType, NotificationPriority

# EXAMPLE 1: RTT Breach (CRITICAL)
create_notification(
    user_email="coordinator@nhs.uk",
    title="🚨 RTT BREACH ALERT!",
    message=f"Patient {name} - {days} days to breach",
    notification_type=NotificationType.URGENT,
    priority=NotificationPriority.URGENT,  # This triggers pop-up!
    send_email=True,
    action_url="/ptl"
)

# EXAMPLE 2: Appointment Booked (MEDIUM)
create_notification(
    user_email="patient@example.com",
    title="✅ Appointment Confirmed",
    message=f"Your appointment is on {date}",
    notification_type=NotificationType.SUCCESS,
    priority=NotificationPriority.MEDIUM,  # No pop-up
    send_email=True,
    action_url="/appointments"
)

# EXAMPLE 3: Tier Approved (HIGH - Good news!)
create_notification(
    user_email="student@example.com",
    title="🎉 Tier Upgrade Approved!",
    message="You now have access to Tier 2",
    notification_type=NotificationType.SUCCESS,
    priority=NotificationPriority.HIGH,  # Triggers green pop-up!
    send_email=True,
    action_url="/my-account"
)

# EXAMPLE 4: Clinical Letter Generated (LOW)
create_notification(
    user_email="staff@nhs.uk",
    title="📝 Clinical Letter Generated",
    message=f"Letter for {patient} is ready",
    notification_type=NotificationType.INFO,
    priority=NotificationPriority.LOW,  # No pop-up, no email
    send_email=False,
    action_url="/letters"
)
```

---

## ✅ **QUICK REFERENCE CARD**

### **When in Doubt:**

**Use Pop-Up if:**
- ✅ Deadline <14 days
- ✅ Security issue
- ✅ Good news to celebrate
- ✅ Requires immediate action

**Use Email if:**
- ✅ Patient communication
- ✅ Confirmation needed
- ✅ Account/payment related
- ✅ User expects it

**Use In-App:**
- ✅ ALWAYS (for everything!)

---

## 🎯 **YOUR PLATFORM AUTO-DECIDES!**

The notification system I built **automatically** decides based on priority:

```python
# In notification_ui.py
def check_and_show_new_notifications():
    for notif in unread_notifs:
        if notif.priority >= 3:  # High or Urgent
            show_popup_notification(notif)  # AUTO POP-UP!
```

**You don't have to decide each time - the system does it!**

---

## 💡 **BEST PRACTICES**

1. **Don't Overwhelm Users**
   - Max 3 pop-ups per session
   - Group similar notifications
   - Use badges for counts

2. **Respect User Preferences**
   - Let users disable emails
   - Let users set quiet hours
   - But keep critical alerts

3. **Be Clear & Actionable**
   - Pop-up should have clear action
   - Email should have next steps
   - In-app should link to details

4. **Test Everything**
   - Test with different priorities
   - Test email delivery
   - Test pop-up timing

---

**The system I built handles all of this automatically based on priority levels!** 🎉

---

*Notification Decision Matrix v1.0*  
*Created: 16 October 2025*  
*Status: Production Ready*
