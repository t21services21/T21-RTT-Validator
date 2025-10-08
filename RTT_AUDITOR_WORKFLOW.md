# RTT Pathway Validation & Auditing Workflow

## T21 Services UK - RTT Auditor Guide

---

## 🎯 **Your Role: RTT Pathway Validator/Auditor**

You validate and audit NHS RTT pathways to ensure:
1. **Correct RTT coding** (codes 10-98)
2. **Actions match records** - what clinic letters say vs what's actually in PAS
3. **Data quality** - accurate patient details, dates, and pathway tracking
4. **Compliance reporting** - flagging gaps in your Excel tracker

---

## 📋 **The Validation Process**

### **Step 1: Read the Clinic Letter**
- GP referral letters
- Consultant outcome letters
- Treatment letters
- Discharge letters

### **Step 2: Interpret & Assign RTT Code**
The system automatically detects letter type and assigns correct code:
- **Code 10** - Referral letters (pathway start)
- **Code 20** - Subsequent activities / decision to treat
- **Code 21** - Inter-provider transfers
- **Code 30** - First definitive treatment
- **Code 31/32** - Active monitoring
- **Code 33** - DNA first care
- **Code 34** - Discharge / no treatment
- **Code 35** - Patient declined

### **Step 3: Cross-Check Against PAS**
Verify what the letter says vs what's recorded in system:

**Letter says:** "Please book patient on surgical waiting list"  
**PAS check:** Is patient actually on waiting list? Y/N

**Letter says:** "Order coronary angiogram"  
**PAS check:** Has investigation been ordered? Y/N

**Letter says:** "Follow-up in 6 weeks"  
**PAS check:** Is follow-up appointment booked? Y/N

### **Step 4: Flag Gaps**
System identifies discrepancies:
- ✅ **GREEN** = All actions completed (PASS)
- ⚠️ **AMBER** = 1-2 actions outstanding (PARTIAL)
- ❌ **RED** = 3+ critical gaps (FAIL)

### **Step 5: Record in Excel Tracker**
System provides Excel-ready output:
```
Validation Date: 08/10/2025
Validator Initials: JDS
RTT Code: 10
Clock Status: Active
Actions Complete (Y/N): N
Flag Color: RED
```

### **Step 6: Generate Comment Line for PAS**
Standardised format: **DATE/INITIALS/CODE – ACTIONS – NEXT – STATUS**

Example:
```
08/10/2025/JDS/CODE10 – REFERRAL RECEIVED & VALIDATED. 
ACTIONS: CHECKED PATIENT ON SYSTEM, DEMOGRAPHICS VERIFIED. 
NEXT: BOOK FIRST OPA, SEND GP ACK. 
STATUS: RTT CLOCK STARTED. PATHWAY ACTIVE.
```

---

## 📊 **Excel Tracker Columns Explained**

Based on your spreadsheet shown:

### **Patient Details:**
- Patient First Name
- Patient Last Name
- Gender
- Date of Birth
- Email
- Patient Address
- Postal Code
- Phone Number

### **RTT Pathway Tracking:**
- **District Number** (e.g., PDN000000121)
- **Pathway Number** (e.g., PPN000000006)
- **NHS Number** (e.g., XXX0000121)
- **Referral Source** - GP Practice Address & Postcode
- **Referring GP Names**
- **NHS Consultant Name**
- **Specialty** (e.g., Cardiology, Gynecology, Orthopedic)
- **NHS Hospital Names** (e.g., Aberdeen Hospital, Birmingham Hospital)

### **Validation Fields (What You Add):**
- **Validation Date** - When you checked
- **Validator Initials** - Your initials (e.g., JDS, AKM)
- **RTT Code Assigned** - The correct code (10-98)
- **Clock Status** - Active / Stopped / Paused / Transferred
- **Actions Complete (Y/N)** - Are all letter actions done?
- **Flag Color** - GREEN / AMBER / RED
- **Comments** - The standardised comment line

---

## 🔍 **What The System Validates**

### **For Code 10 (Referral Letters):**
✅ **Patient exists in PAS**  
✅ **Demographics match** (Name, NHS Number, DOB)  
✅ **No duplicate pathway** (same specialty, within 6 months)  
✅ **Mandatory fields present** (referral date, GP details, specialty)  
✅ **Referral registered** in PAS  
✅ **Pathway number assigned**  
✅ **Clock start date set**  
✅ **First appointment booked** (2 weeks urgent / 6 weeks routine)  
✅ **Acknowledgment sent** to GP  
✅ **Investigations ordered** (if mentioned in referral)  
✅ **Priority flag set** (if urgent/2WW/cancer)  

### **For Code 20 (Clinic Outcomes):**
✅ **Waiting list** - if letter says "list for surgery"  
✅ **Follow-up booked** - if letter says "review in X weeks"  
✅ **Diagnostics ordered** - if letter requests tests  
✅ **GP letter sent** - if letter says "copy to GP"  

### **For Code 30 (Treatment):**
✅ **Treatment date recorded**  
✅ **Procedure documented**  
✅ **Clock stop date set**  
✅ **Pathway closed**  
✅ **Post-op follow-up booked**  

---

## 🚩 **Common Gaps Found**

| Gap | What It Means | Excel Flag |
|-----|---------------|------------|
| Patient NOT on waiting list | Letter says "list for surgery" but PAS shows no WL entry | RED |
| Follow-up NOT booked | Letter says "review in 6 weeks" but no appointment in diary | AMBER |
| Investigations NOT ordered | Referral requests angiogram but not ordered in system | RED |
| Duplicate pathway | Patient already has active pathway for same specialty | RED |
| Demographics mismatch | NHS number on letter doesn't match PAS record | RED |
| GP letter NOT sent | Letter says "copy to GP" but no correspondence sent | AMBER |
| Wrong clock status | Clock should be paused (AM) but showing active | RED |

---

## 💬 **Comment Line Examples**

### **Referral (Code 10):**
```
08/10/2025/JDS/CODE10 – REFERRAL RECEIVED & VALIDATED. 
ACTIONS: CHECKED PATIENT ON SYSTEM, DEMOGRAPHICS VERIFIED. 
NEXT: BOOK FIRST OPA, SEND GP ACK. 
STATUS: RTT CLOCK STARTED. PATHWAY ACTIVE.
```

### **Decision to Treat (Code 20):**
```
08/10/2025/AKM/CODE20 – PATHWAY CONTINUES. 
ACTIONS: CLINIC OUTCOME RECORDED, WL ENTRY CREATED. 
NEXT: TCI DATE REQUIRED, CONFIRM FITNESS FOR SURGERY. 
STATUS: RTT CLOCK ACTIVE. AWAITING TREATMENT.
```

### **Treatment (Code 30):**
```
08/10/2025/VLD/CODE30 – FDT COMPLETED. 
ACTIONS: TREATMENT PERFORMED (SEPTOPLASTY), CLOCK STOPPED. 
NEXT: POST-OP FU 6W, GP LETTER. 
STATUS: RTT CLOCK STOPPED. PATHWAY CLOSED.
```

### **DNA (Code 33):**
```
08/10/2025/JDS/CODE33 – DNA FIRST CARE ACTIVITY. 
ACTIONS: DNA RECORDED, GP INFORMED. 
NEXT: REBOOK WITHIN 2WW, SEND DNA LETTER. 
STATUS: CLOCK CONTINUES (TRUST POLICY).
```

---

## 📝 **How To Use The System**

### **1. Open Clinic Letter Interpreter Tool**
- Paste clinic letter text
- Enter your validator initials

### **2. Check PAS Summary**
Mark what's ACTUALLY in the system:
- Follow-up booked? Y/N
- Diagnostics ordered? Y/N
- Waiting list? Y/N
- GP letter sent? Y/N

### **3. Click "Interpret Letter"**
System provides:
- ✅ Correct RTT code
- 📊 Validation summary
- 📋 Checklist of required vs completed actions
- 🚩 Gaps found
- 📊 Excel-ready output
- 💬 Comment line for PAS

### **4. Copy to Excel Tracker**
Use the "Excel Tracker Report" section:
- Validation Date
- Validator Initials
- RTT Code
- Clock Status
- Actions Complete Y/N
- Flag Color (GREEN/AMBER/RED)

### **5. Paste Comment to PAS**
Copy the standardised comment line and paste into PAS notes field

---

## 🎯 **Quality Assurance Metrics**

Track your audit findings:
- **Total pathways audited**
- **Pass rate** (GREEN flags)
- **Partial compliance** (AMBER flags)
- **Failure rate** (RED flags)
- **Common gap types**
- **Specialty-specific issues**

---

## 📚 **RTT Rules Reference**

### **Clock Start:**
- Code 10 - Referral received
- Code 11 - Return from Active Monitoring
- Code 12 - New condition referral

### **Clock Continues:**
- Code 20 - Subsequent activity
- Code 21 - Inter-provider transfer

### **Clock Pause:**
- Code 31 - Active Monitoring (patient-initiated)
- Code 32 - Active Monitoring (clinician-initiated)

### **Clock Stop:**
- Code 30 - First Definitive Treatment
- Code 34 - Discharge / no treatment
- Code 35 - Patient declined
- Code 36 - Patient died

### **Special:**
- Code 33 - DNA first care

### **Non-RTT:**
- Code 90 - Post-treatment follow-up
- Code 91 - Activity during AM
- Code 92 - Diagnostics only
- Code 98 - Not applicable to RTT

---

*T21 Services UK | RTT Pathway Intelligence v1.2*  
*RTT Auditor Workflow Guide*
