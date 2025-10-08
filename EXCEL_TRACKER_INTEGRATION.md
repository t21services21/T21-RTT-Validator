# Excel Tracker Integration Guide

## T21 RTT Validation - Excel Tracker Fields

---

## 📊 **Excel Tracker Columns (Exact Match)**

Your validation system now outputs data in the **exact format** of your Excel tracker:

### **Column W: Validator Name**
- Your initials (2-3 letters)
- Example: `JDS`, `AKM`, `MOD`

### **Column X: Clock Status**
- **Dropdown Options:**
  - `Previously Stopped` - Another validator stopped the clock before
  - `Unclear` - Status needs clarification
  - `No` - Clock not stopped
  - `Yes` - You are stopping the clock now

### **Column Y: Outcome**
Dropdown with exact options from your tracker:
- **(Blank)**
- **Awaiting OPD Appt**
- **Awaiting results**
- **Awaiting TC date**
- **CL Required**
- **Discharged**
- **Further Information Required**
- **OPD Appt (Booked)**

### **Column Z: Validation Date**
- Format: `DD/MM/YYYY`
- Example: `16/09/2025`

### **Column AA: Validation Comments**
- **Format:** `DATE SUMMARY ACTIONS DONE/OUTSTANDING OUTCOME`
- **Examples from your tracker:**
  - `CS 02/04/2023 30 MO AS SEEN ON C`
  - `16/09/2025 IE As seen on PA no ref`
  - `16/09/2025 CO As per CL Dated 02/`
  - `16/09/25 AA AS SEEN ON PAS D4/06`

---

## 🎯 **How The System Generates Comments**

### **Comment Structure:**
```
[DATE] [LETTER_TYPE] [ACTIONS_VERIFIED] [OUTSTANDING] [OUTCOME]
```

### **Examples:**

**Referral Letter (Code 10):**
```
08/10/2025 REFERRAL RECEIVED. 4 ACTIONS VERIFIED IN PAS. 20 OUTSTANDING. 
REQUIRED: PBL, OPA, DIAGNOSTICS. Awaiting OPD Appt.
```

**Clinic Outcome (Code 20):**
```
08/10/2025 CLINIC OUTCOME LETTER REVIEWED. 2 ACTIONS VERIFIED IN PAS. 
3 OUTSTANDING. REQUIRED: WL, GP LTR. Awaiting TC date.
```

**Treatment Completed (Code 30):**
```
08/10/2025 FDT COMPLETED. ALL COMPLETE. Discharged.
```

**DNA (Code 33):**
```
08/10/2025 DNA RECORDED. 1 OUTSTANDING. REQUIRED: OPA. Awaiting OPD Appt.
```

---

## 📝 **Abbreviations Used in Comments**

| Abbreviation | Full Meaning |
|--------------|--------------|
| **WL** | Waiting List |
| **PBL** | Partial Booking List |
| **OPA** | Outpatient Appointment |
| **GP LTR** | GP Letter |
| **FDT** | First Definitive Treatment |
| **AM** | Active Monitoring |
| **CL** | Clinic Letter |
| **TC** | To Come In (surgery date) |

---

## 🔄 **Your Complete Workflow**

### **Step 1: Open Clinic Letter Interpreter**
- Paste letter text
- Enter your initials (e.g., "JDS")

### **Step 2: Select Excel Tracker Fields**
- **Clock Status:** Select from dropdown
  - `Yes` if you're stopping the clock (codes 30-36)
  - `Previously Stopped` if already stopped
  - `No` if clock continues
- **Outcome:** Select next action
  - `Awaiting OPD Appt` if waiting for first appointment
  - `Awaiting TC date` if on waiting list
  - `CL Required` if more info needed
  - etc.

### **Step 3: Check PAS**
- Mark what's actually in the system (Y/N)
- Follow-up booked?
- Diagnostics ordered?
- Waiting list?
- GP letter sent?

### **Step 4: Click "Interpret Letter"**
System generates:
- ✅ RTT Code
- 📊 Validation summary
- 📋 Checklist
- 🚩 Gaps found
- **📊 Excel Tracker Report** (Ready to copy/paste)

### **Step 5: Copy to Excel**
The system outputs:
```
Validator Name: JDS
Clock Status: Yes
Outcome: Awaiting OPD Appt
Validation Date: 08/10/2025
Validation Comments: 08/10/2025 REFERRAL RECEIVED. 4 ACTIONS VERIFIED IN PAS. 20 OUTSTANDING. REQUIRED: PBL, OPA, DIAGNOSTICS. Awaiting OPD Appt.
```

### **Step 6: Paste into Excel Tracker**
- Copy each field
- Paste into corresponding column (W, X, Y, Z, AA)
- Done!

---

## 🎯 **Clock Status Selection Guide**

### **When to Select "Yes":**
Clock stop codes (you are stopping it now):
- Code 30 - First Definitive Treatment
- Code 31 - Active Monitoring (patient-initiated) - PAUSES clock
- Code 32 - Active Monitoring (clinician-initiated) - PAUSES clock
- Code 33 - DNA first care - Special handling
- Code 34 - Discharge / no treatment
- Code 35 - Patient declined
- Code 36 - Patient died

### **When to Select "Previously Stopped":**
- You're checking a letter where another validator already stopped the clock
- Verifying that the clock was correctly stopped

### **When to Select "No":**
- Clock continues (codes 10, 11, 12, 20, 21)
- Pathway still active

### **When to Select "Unclear":**
- Not sure if clock should be stopped
- Needs further investigation

### **When to Select "Hospital to Review":**
- Complex case needing clinical review
- Escalation required

---

## 📊 **Outcome Selection Guide**

| Select This | When Letter Says... |
|-------------|---------------------|
| **Awaiting OPD Appt** | "Book first outpatient appointment" (not yet booked) |
| **OPD Appt (Booked)** | First appointment has been booked and recorded in system |
| **Awaiting results** | "Awaiting blood test results", "Pending MRI" |
| **Awaiting TC date** | "List for surgery", "Await theatre slot" |
| **CL Required** | "Further clinic letter needed" |
| **Discharged** | "Discharge to GP", "No further treatment" |
| **Further Information Required** | "Need more info", "Contact patient" |

---

## 🚀 **Quick Start Example**

**Scenario:** GP Referral Letter for Cardiology requesting angiogram

**Your Actions:**
1. Paste letter into system
2. Enter initials: `JDS`
3. Select Clock Status: `No` (referral starts clock, doesn't stop it)
4. Select Outcome: `Awaiting OPD Appt` (need first appointment)
5. Check PAS:
   - Follow-up booked? `N`
   - Diagnostics ordered? `N`
   - etc.
6. Click "Interpret Letter"

**System Outputs:**
```
Validator Name: JDS
Clock Status: No
Outcome: Awaiting OPD Appt
Validation Date: 08/10/2025
Validation Comments: 08/10/2025 REFERRAL RECEIVED. 0 ACTIONS VERIFIED IN PAS. 
25 OUTSTANDING. REQUIRED: PBL, OPA, DIAGNOSTICS. Awaiting OPD Appt.
```

**You Copy/Paste to Excel:**
- Column W: `JDS`
- Column X: `No`
- Column Y: `Awaiting OPD Appt`
- Column Z: `08/10/2025`
- Column AA: `08/10/2025 REFERRAL RECEIVED. 0 ACTIONS VERIFIED IN PAS. 25 OUTSTANDING. REQUIRED: PBL, OPA, DIAGNOSTICS. Awaiting OPD Appt.`

✅ Done!

---

*T21 Services UK | RTT Pathway Intelligence v1.2*  
*Excel Tracker Integration Complete*
