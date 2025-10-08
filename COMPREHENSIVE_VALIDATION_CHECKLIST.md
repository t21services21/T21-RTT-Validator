# Comprehensive RTT Validation Checklist

## T21 Services UK - Complete Validation & Verification Guide

---

## ✅ **What The System Now Validates**

Your RTT validation system now checks **EVERYTHING** mentioned in clinic letters against what's actually in PAS.

---

## 📋 **CODE 10 - REFERRAL LETTERS (10 Sections)**

### **Section 1: Referral Logged in System**
- [ ] Referral logged in PAS system (Y/N)
- [ ] Referral actually recorded in system

### **Section 2: Patient Demographics**
- [ ] Patient exists in PAS (Y/N)
- [ ] Patient name matches letter vs PAS
- [ ] NHS number matches letter vs PAS
- [ ] DOB matches letter vs PAS
- [ ] Address correct in PAS (Y/N)

### **Section 3: Referral Details**
- [ ] Referral source (GP/Consultant) recorded correctly (Y/N)
- [ ] Referring GP name matches letter (Y/N)
- [ ] GP practice address recorded (Y/N)
- [ ] Specialty correctly assigned (Y/N)
- [ ] Referral date matches letter date (Y/N)

### **Section 4: Pathway Creation**
- [ ] RTT pathway created in system (Y/N)
- [ ] Pathway number assigned (Y/N)
- [ ] District number assigned (Y/N)
- [ ] Clock start date = referral date (Y/N)
- [ ] Clock status = Active (Y/N)

### **Section 5: Partial Booking List (PBL)**
- [ ] Patient added to Partial Booking List (Y/N)
- [ ] PBL entry date recorded (Y/N)
- [ ] Patient awaiting first appointment

### **Section 6: First Appointment**
- [ ] First appointment booked (Y/N)
- [ ] Appointment date recorded (Y/N)
- [ ] Appointment within target timeframe (Y/N)

### **Section 7: Investigations/Diagnostics**
For each diagnostic test mentioned:
- [ ] ECG ordered in system (Y/N)
- [ ] Angiogram ordered (Y/N)
- [ ] MRI ordered (Y/N)
- [ ] CT Scan ordered (Y/N)
- [ ] Ultrasound ordered (Y/N)
- [ ] Echocardiogram ordered (Y/N)
- [ ] X-Ray ordered (Y/N)
- [ ] Blood Tests ordered (Y/N)
- [ ] Biopsy ordered (Y/N)
- [ ] Booking date recorded for each test

### **Section 8: Priority/Urgency**
- [ ] Urgent/2WW flag set in system (Y/N)
- [ ] Priority booking expedited (Y/N)

### **Section 9: Duplicate Check**
- [ ] No duplicate pathway for same specialty (Y/N)
- [ ] Search performed (same patient, same specialty, last 6 months)

### **Section 10: Acknowledgment**
- [ ] Acknowledgment letter sent to GP (Y/N)
- [ ] Acknowledgment date recorded (Y/N)

---

## 📋 **CODE 20 - CLINIC OUTCOME / DECISION TO TREAT**

### **Waiting List Checks:**
- [ ] Patient added to surgical waiting list (Y/N)
- [ ] Waiting list type recorded (Y/N)
- [ ] WL entry date = letter date (Y/N)
- [ ] Procedure/operation recorded on WL (Y/N)
- [ ] Specialty correct on WL entry (Y/N)

### **TCI Date Checks:**
- [ ] TCI (To Come In) date set in system (Y/N)
- [ ] TCI date within 18 weeks of clock start (Y/N)

### **Diagnostics Checks:**
For each test mentioned:
- [ ] ECG ordered in system (Y/N)
- [ ] Angiogram ordered (Y/N)
- [ ] MRI ordered (Y/N)
- [ ] CT Scan ordered (Y/N)
- [ ] Ultrasound ordered (Y/N)
- [ ] X-Ray ordered (Y/N)
- [ ] Blood Tests ordered (Y/N)
- [ ] Echocardiogram ordered (Y/N)
- [ ] Booking date recorded (Y/N)

---

## 📋 **CODE 30 - FIRST DEFINITIVE TREATMENT**

### **Treatment Record Checks:**
- [ ] Treatment date recorded in PAS (Y/N)
- [ ] Procedure/treatment type documented (Y/N)
- [ ] Clock stop date = treatment date (Y/N)
- [ ] Pathway status = Closed (Y/N)
- [ ] RTT code 30 recorded (Y/N)

### **Post-Treatment:**
- [ ] Post-treatment follow-up booked (Y/N)
- [ ] Follow-up appointment date recorded (Y/N)

---

## 📋 **CODE 33 - DNA (DID NOT ATTEND)**

- [ ] DNA recorded in PAS (Y/N)
- [ ] DNA date = appointment date (Y/N)
- [ ] RTT code 33 applied (Y/N)
- [ ] Rebooking arranged (Y/N)
- [ ] Rebook date within 2 weeks (Y/N)
- [ ] DNA letter sent to patient (Y/N)
- [ ] GP informed of DNA (Y/N)

---

## 📋 **CODE 34 - DISCHARGE / NO TREATMENT**

- [ ] Discharge recorded in PAS (Y/N)
- [ ] Discharge date = letter date (Y/N)
- [ ] Clock stop date set (Y/N)
- [ ] Pathway status = Closed (Y/N)
- [ ] RTT code 34 recorded (Y/N)
- [ ] Discharge letter sent to GP (Y/N)

---

## 📋 **CODE 31/32 - ACTIVE MONITORING**

- [ ] Active Monitoring pathway created (Y/N)
- [ ] AM start date recorded (Y/N)
- [ ] RTT code 31 or 32 recorded (Y/N)
- [ ] Clock status = Paused (Y/N)
- [ ] Review date set for AM monitoring (Y/N)

---

## 📋 **STANDARD CHECKS (All Letter Types)**

### **Follow-Up Appointments:**
- [ ] Follow-up appointment booked (Y/N)
- [ ] Follow-up date recorded (Y/N)
- [ ] Follow-up within timeframe stated in letter

### **GP Correspondence:**
- [ ] GP letter sent (Y/N)
- [ ] GP letter date recorded (Y/N)
- [ ] Letter recorded in correspondence log

---

## 🚩 **Excel Reporting Fields**

Your validation produces these fields for Excel:

| Field | Example Value |
|-------|--------------|
| **Validation Date** | 08/10/2025 |
| **Validator Initials** | JDS |
| **RTT Code Assigned** | 10 |
| **Clock Status** | Active |
| **Actions Complete (Y/N)** | N |
| **Flag Color** | RED |
| **Compliance Rate** | 45% |
| **Total Actions Required** | 35 |
| **Actions Completed** | 15 |
| **Actions Outstanding** | 20 |
| **Comments** | Full comment line with initials |

---

## 💡 **Example Validation Flow**

### **Scenario: GP Referral Letter for Cardiology**

**Letter says:**
- "I am writing to refer Mr. John Doe"
- "NHS Number: 9876543210"
- "Please arrange coronary angiogram"
- "Suspected coronary artery disease"

**System Checks:**

1. ✅ **Code 10 Detected** - Referral letter
2. 📋 **35 Validation Checks Created:**
   - Check referral logged
   - Verify patient demographics (name, NHS number, DOB)
   - Check pathway created
   - Check PBL entry
   - Check angiogram ordered
   - Check urgent flag set
   - Check first appointment booked
   - ...and 28 more

3. 🔍 **You Check PAS:**
   - Referral logged? **N**
   - Patient exists? **Y**
   - NHS number matches? **Y**
   - Pathway created? **N**
   - Angiogram ordered? **N**
   - First appointment booked? **N**

4. 🚩 **System Flags:**
   - ❌ RED Flag (20+ gaps found)
   - 📊 Compliance: 15%
   - 🔴 **GAPS:**
     - Referral not logged in system
     - Pathway not created
     - Angiogram not ordered
     - PBL entry missing
     - First appointment not booked
     - Urgent flag not set

5. 📊 **Excel Output:**
   ```
   Date: 08/10/2025
   Validator: JDS
   Code: 10
   Clock: Should be Active
   Complete: N
   Flag: RED
   Comments: 08/10/2025/JDS/CODE10 – REFERRAL RECEIVED...
   ```

6. ✅ **PAS Actions Generated:**
   - ACTION: Log referral with all fields
   - ACTION: Create RTT pathway
   - ACTION: Assign pathway number
   - ACTION: Order coronary angiogram
   - ACTION: Add to PBL
   - ACTION: Set urgent flag
   - ACTION: Book first appointment within 2 weeks

---

## 📊 **Your Workflow**

```
┌─────────────────────────────────────┐
│   1. RECEIVE CLINIC LETTER          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   2. PASTE INTO SYSTEM              │
│   - Enter your initials             │
│   - Paste letter text               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   3. SYSTEM ASSIGNS RTT CODE        │
│   - Detects letter type             │
│   - Creates validation checklist    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   4. CHECK PAS SYSTEM               │
│   - Go through each check (Y/N)     │
│   - Verify what's actually in PAS   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   5. SYSTEM GENERATES REPORT        │
│   - Flag color (GREEN/AMBER/RED)    │
│   - List of gaps found              │
│   - PAS actions required            │
│   - Excel-ready output              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   6. RECORD IN EXCEL TRACKER        │
│   - Copy validation details         │
│   - Paste into spreadsheet          │
│   - Flag pathway as RED/AMBER/GREEN │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   7. PASTE COMMENT TO PAS           │
│   - Copy standardised comment line  │
│   - Paste into PAS notes field      │
└─────────────────────────────────────┘
```

---

## 🎯 **What "Validate" Really Means**

**NOT just:** "What RTT code should this be?"

**BUT:** "Is what the letter says ACTUALLY done in the system?"

### **Examples:**

❌ **Wrong Approach:**
- Letter says "book ECG" → System says "Code 20"
- ✅ Done

✅ **Correct Approach:**
- Letter says "book ECG" → System says "Code 20"
- CHECK: Is ECG actually booked in system? **NO**
- FLAG: ECG requested but NOT booked
- EXCEL: Mark as RED flag
- PAS ACTION: Order ECG
- COMMENT: "ECG NOT ORDERED - ACTION REQUIRED"

---

*T21 Services UK | RTT Pathway Intelligence v1.2*  
*Comprehensive Validation & Verification System*
