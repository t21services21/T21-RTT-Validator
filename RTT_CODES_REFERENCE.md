# RTT National Status Codes - Complete Reference

## T21 Services UK - NHS RTT Pathway Intelligence

---

## 🔵 **Clock Start Codes**

### **Code 10** - First Activity in Pathway
- **Clock Impact:** Starts RTT clock
- **Used When:** Initial referral to consultant-led service is received and first activity occurs
- **Examples:** 
  - First outpatient appointment after GP referral
  - First contact with consultant-led service
- **Rules:** Can only appear ONCE at the beginning of a pathway
- **Comment Line:** `RTT START 10/DD/MM/YYYY - FIRST ACTIVITY. CLOCK STARTED.`

### **Code 11** - First Activity After Active Monitoring/Watchful Wait Ends
- **Clock Impact:** Restarts RTT clock (after AM pause)
- **Used When:** 
  - Patient returns from Active Monitoring (31/32)
  - Watchful Wait period ends and treatment pathway resumes
  - Clinical decision made to proceed with treatment after monitoring
- **Examples:**
  - Patient reviewed after 6-month active monitoring, now needs treatment
  - Return to active pathway after "watch and wait" for skin lesion
- **Rules:** Must follow a previous code 31 or 32 (AM start)
- **Comment Line:** `RTT RESTART 11/DD/MM/YYYY - AM ENDED. CLOCK RESTARTED. CONTINUE RTT.`

### **Code 12** - First Activity Following Consultant/AHP Referral for NEW Condition
- **Clock Impact:** Starts NEW RTT clock
- **Used When:**
  - Consultant refers to another consultant for a DIFFERENT condition
  - Allied Health Professional (AHP) makes referral for new issue
  - New pathway for separate clinical condition
- **Examples:**
  - ENT consultant refers to Dermatology for unrelated skin condition
  - Physiotherapist refers to Orthopaedics for new joint problem
- **Rules:** Creates entirely new pathway; original pathway continues separately
- **Comment Line:** `NEW RTT 12/DD/MM/YYYY - NEW CONDITION REFERRAL. NEW CLOCK STARTED.`

---

## 🟢 **Clock Continue Codes**

### **Code 20** - Subsequent Activity in RTT Period
- **Clock Impact:** Clock continues (active)
- **Used When:** Any follow-up activity while pathway is active
- **Examples:**
  - Follow-up appointments
  - Pre-operative assessments
  - Consultant reviews
  - Decision to treat made
- **Rules:** Can repeat multiple times; must occur BEFORE code 30
- **Comment Line:** `RTT CONTINUE 20/DD/MM/YYYY - SUBSEQUENT ACTIVITY. PATHWAY ACTIVE.`

### **Code 21** - Transfer to Another Health Care Provider
- **Clock Impact:** Transfers responsibility (clock continues at receiving provider)
- **Used When:** Inter-Provider Transfer (IPT)
- **Examples:**
  - Patient transferred to specialist center
  - Move to another NHS trust for treatment
- **Rules:** 
  - Sending provider stops their clock
  - Receiving provider starts new clock on acceptance
  - Use IPT MDS (Minimum Data Set) for transfer
- **Comment Line:** `IPT 21/DD/MM/YYYY - TRANSFERRED TO [PROVIDER]. CLOCK TRANSFERRED.`

---

## 🔴 **Clock Stop Codes**

### **Code 30** - Start of First Definitive Treatment (FDT)
- **Clock Impact:** STOPS RTT clock
- **Used When:** Treatment begins
- **Examples:**
  - Surgery performed
  - Active medication started (not diagnostic)
  - Therapeutic procedure commenced
- **Rules:** Can only appear ONCE; ends the RTT pathway
- **Comment Line:** `FDT 30/DD/MM/YYYY - TREATMENT STARTED ([PROCEDURE]). RTT CLOSED.`

### **Code 31** - Active Monitoring Initiated by PATIENT
- **Clock Impact:** PAUSES RTT clock
- **Used When:** Patient requests delay/deferral
- **Examples:**
  - Patient asks to postpone treatment for personal reasons
  - Patient-requested watchful waiting
- **Rules:** Clock pauses; restarts with code 11 when patient ready
- **Comment Line:** `AM PATIENT 31/DD/MM/YYYY - CLOCK PAUSED. PATIENT INITIATED.`

### **Code 32** - Active Monitoring Initiated by HOSPITAL
- **Clock Impact:** PAUSES RTT clock
- **Used When:** Clinician decides on watchful waiting/conservative management
- **Examples:**
  - Clinical decision for 6-month observation period
  - Watch-and-wait for slow-growing condition
- **Rules:** Clock pauses; restarts with code 11 when review indicates treatment needed
- **Comment Line:** `AM CLINICAL 32/DD/MM/YYYY - CLOCK PAUSED. WATCHFUL WAIT INITIATED.`

### **Code 33** - DNA (Did Not Attend) First Care Activity
- **Clock Impact:** Special handling (trust policy dependent)
- **Used When:** Patient does not attend first appointment
- **Examples:**
  - Patient DNA'd initial outpatient appointment
  - No show for first consultant review
- **Rules:** 
  - Should not repeat (per Local_Policy_Allow_Multiple_33: false)
  - Rebook within trust policy (typically 2 weeks)
  - Clock may continue or be reset depending on trust rules
- **Comment Line:** `DNA 33/DD/MM/YYYY - FIRST CARE DNA. REBOOK 2W. GP INFORMED.`

### **Code 34** - Decision NOT to Treat / No Further Contact Required
- **Clock Impact:** STOPS RTT clock
- **Used When:** Clinical decision made that treatment not needed
- **Examples:**
  - Symptoms resolved
  - No intervention required after assessment
  - Discharge to GP care
- **Rules:** Closes pathway; can only appear once
- **Comment Line:** `DISCHARGE 34/DD/MM/YYYY - NO TREATMENT REQUIRED. RTT CLOSED. GP LETTER SENT.`

### **Code 35** - Patient Declined Offered Treatment
- **Clock Impact:** STOPS RTT clock
- **Used When:** Patient refuses recommended treatment
- **Examples:**
  - Patient declines surgery after consultation
  - Patient refuses offered intervention
- **Rules:** Document patient decision; closes pathway
- **Comment Line:** `DECLINED 35/DD/MM/YYYY - PATIENT REFUSED TREATMENT. RTT CLOSED.`

### **Code 36** - Patient Died Before Treatment
- **Clock Impact:** STOPS RTT clock
- **Used When:** Patient dies while on RTT pathway
- **Rules:** Close pathway immediately
- **Comment Line:** `DECEASED 36/DD/MM/YYYY - PATIENT DIED. RTT CLOSED.`

---

## 🟡 **Non-RTT Codes (Post-Treatment & Other)**

### **Code 90** - First Definitive Treatment Occurred Previously
- **Clock Impact:** Non-RTT (post-treatment activity)
- **Used When:** Any activity AFTER code 30 (treatment completed)
- **Examples:**
  - Post-operative follow-up appointments
  - Wound checks after surgery
  - Recovery monitoring
- **Rules:** Can repeat; all post-treatment activities use this code
- **Comment Line:** `POST-TX 90/DD/MM/YYYY - FDT OCCURRED PREVIOUSLY. NON-RTT FOLLOW-UP.`

### **Code 91** - Care Activity DURING Active Monitoring
- **Clock Impact:** During AM (clock paused)
- **Used When:** Appointments during active monitoring period
- **Examples:**
  - 3-month review during watchful wait
  - Check-up during observation period
- **Rules:** Can repeat; requires prior code 31 or 32
- **Comment Line:** `AM REVIEW 91/DD/MM/YYYY - ACTIVITY DURING AM. CLOCK PAUSED.`

### **Code 92** - Diagnostics Only (Not Yet Referred for Treatment)
- **Clock Impact:** Non-RTT
- **Used When:** Diagnostic tests without consultant-led referral
- **Examples:**
  - GP-requested X-ray (no consultant involvement)
  - Standalone diagnostic imaging
- **Rules:** Not part of RTT pathway; no clock starts
- **Comment Line:** `DIAGNOSTICS 92/DD/MM/YYYY - NON-RTT DIAGNOSTIC ONLY.`

### **Code 98** - Activity NOT Applicable to RTT Periods
- **Clock Impact:** Non-RTT
- **Used When:** Administrative or non-treatment activities
- **Examples:**
  - Admin appointments
  - Non-clinical contacts
- **Rules:** Exclude from RTT reporting
- **Comment Line:** `NON-RTT 98/DD/MM/YYYY - NOT APPLICABLE TO RTT.`

---

## 📊 **Code Sequencing Rules**

### ✅ **Valid Sequences:**
- `10 → 20 → 20 → 30` (Standard pathway)
- `10 → 20 → 32 → 91 → 91 → 11 → 20 → 30` (With active monitoring)
- `10 → 20 → 30 → 90 → 90` (Treatment then follow-ups)
- `12 → 20 → 30` (New condition referral pathway)

### ❌ **Invalid Sequences:**
- `10 → 10` (Duplicate start - ERROR)
- `10 → 30 → 20` (Activity after treatment - should be 90)
- `10 → 91` (AM activity without AM start - ERROR)
- `10 → 20 → 30 → 30` (Duplicate treatment - ERROR)

---

## 🎯 **Key RTT Terminology**

| Term | Definition |
|------|------------|
| **RTT** | Referral to Treatment |
| **PTL** | Patient Tracking List - patients awaiting treatment |
| **DNA** | Did Not Attend |
| **IPT MDS** | Inter Provider Transfer Minimum Data Set |
| **PBL** | Partial Booking List - awaiting first appointment |
| **WL** | Waiting List (for treatment or diagnostics) |
| **TCI** | To Come In date (surgery/diagnostic date) |
| **OPA/OPD** | Outpatient Appointment/Department |
| **AM** | Active Monitoring |
| **FDT** | First Definitive Treatment |
| **AHP** | Allied Health Professional |
| **Nullify** | Make pathway invalid (data quality issue) |

---

## ⏱️ **Breach Thresholds**

- **18 weeks** - Standard NHS RTT target
- **26 weeks** - Serious wait breach (escalate)
- **52 weeks** - Critical breach (immediate action required)

**Calculation:** 
- Start date = Referral received (code 10/11/12)
- Stop date = First treatment (30) or discharge (34/35/36)
- Subtract any patient-initiated pause periods (31)
- Provider-initiated pauses (32) depend on trust policy

---

## 📝 **Clock Pause vs Stop**

### **Pause (31/32):**
- Clock temporarily stops
- Can restart with code 11
- Time paused does NOT count toward 18-week target
- Patient remains on PTL

### **Stop (30/34/35/36):**
- Clock ends permanently for this pathway
- Pathway closed
- Patient removed from PTL
- Post-treatment follow-ups use code 90

---

*T21 Services UK | NHS RTT Training & Validation System v1.2*  
*Complete RTT Code Reference - Updated with Codes 11 & 12*
