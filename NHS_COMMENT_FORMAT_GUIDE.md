# NHS STANDARD COMMENT FORMAT GUIDE

## T21 RTT Validator - Comment Line Standards

---

## 📋 **Comment Structure:**

### **Format for Clock Stopped:**
```
CS [CLOCK_STOP_DATE] ([RTT_CODE]) [INITIALS] AS PER CL DATED [LETTER_DATE] [ACTION]. F/U STATUS
```

### **Format for Clock Continues:**
```
[VALIDATION_DATE] [INITIALS] [SUMMARY OF LETTER]. [STATUS]
```

---

## 🔑 **Key Abbreviations:**

| Abbreviation | Meaning |
|--------------|---------|
| **CS** | Clock Stop |
| **CL** | Clinic Letter |
| **F/U** | Follow-up |
| **APPT** | Appointment |
| **AM** | Active Monitoring |
| **DNA** | Did Not Attend |
| **OPA** | Outpatient Appointment |

---

## ✅ **Examples by RTT Code:**

### **Code 30 - First Definitive Treatment (Clock Stops)**
### **Code 20 - Decision to Treat (Clock Continues)**

**Letter Says:**
> "Patient to undergo MRI scan. Then list for surgery."

**Validation Date:** 08/10/2025

**PAS Check:** MRI ordered = YES, MRI date = 15/10/2025

**Comment:**
```
08/10/2025 AKM PATIENT TO UNDERGO MRI SCAN. MRI SCAN BOOKED FOR 15/10/2025
```

---

**If MRI NOT Booked:**
```
08/10/2025 AKM PATIENT TO UNDERGO MRI SCAN. AWAITING MRI SCAN BOOKING
```

---

**If MRI Already Done (awaiting results):**
```
08/10/2025 AKM PATIENT UNDERWENT MRI SCAN. AWAITING RESULTS
```

---

**If Letter About Waiting List:**

**PAS Check:** On waiting list = YES

**Comment:**
```
08/10/2025 AKM DECISION TO TREAT MADE. PATIENT ADDED TO WAITING LIST
```

**If NOT on Waiting List:**
```
08/10/2025 AKM DECISION TO TREAT MADE. AWAITING WAITING LIST ENTRY
```

---

### **Code 10 - Referral (Clock Starts)**

**Letter Says:**
> "I am writing to refer this patient for cardiology assessment."

**Validation Date:** 08/10/2025

**Comment:**
```
08/10/2025 IE REFERRAL RECEIVED. RTT CLOCK STARTED. OPA BOOKING REQUIRED
```

---

### **Code 33 - DNA (Did Not Attend)**

**Appointment Date:** 15/09/2025

**Comment:**
```
DNA (33) CO AS PER APPOINTMENT DATED 15/09/2025 DNA RECORDED. REBOOK WITHIN 2 WEEKS
```

---

### **Code 31/32 - Active Monitoring (Clock Pauses)**

**Letter Says:**
> "Watchful waiting approach. Review in 3 months."

**Letter Dated:** 10/08/2025

**Code:** 32 (Clinician-initiated)

**PAS Check:** Follow-up booked = YES, Date = 10/11/2025

**Comment:**
```
AM (CODE 32) YO AS PER CL DATED 10/08/2025 ACTIVE MONITORING CLINICIAN INITIATED. CLOCK PAUSED. F/U APPT BOOKED FOR 10/11/2025
```

---

## 🔄 **Logic Flow:**

### **1. Determine Clock Status:**
- **Codes 30-36** = Clock STOPS → Use `CS [DATE] ([CODE])` format
- **All other codes** = Clock CONTINUES → Standard format

### **2. Extract Letter Date:**
- System scans letter for date patterns
- Looks for: "Date:", "Dated:", or any DD/MM/YYYY format
- Falls back to validation date if not found

### **3. Identify Actions from Letter:**
- Treatment completed → "MEDICATION PRESCRIBED/TREATMENT COMPLETED"
- Discharge → "DISCHARGED NO TREATMENT REQUIRED"
- Waiting list → "PATIENT ADDED TO WAITING LIST"
- Referral → "REFERRAL RECEIVED. RTT CLOCK STARTED"

### **4. Check PAS vs Letter:**
- If letter says "follow-up in 6 weeks"
  - PAS shows booked → "F/U APPT BOOKED FOR [DATE]"
  - PAS shows not booked → "F/U APPT REQUIRED BOOKING"

### **5. Generate Final Comment:**
```
Combine: Clock Status + Date + Code + Initials + Letter Reference + Actions + F/U Status
```

---

## 📊 **Real-World Examples:**

### **Example 1: Treatment Letter with Booked Follow-up**

**Letter:**
```
Date: 24/05/2025
Dear Patient,
You were treated with antibiotics for infection on 23/04/2025.
Please attend follow-up on 05/07/2025 to review progress.
```

**PAS:**
- Follow-up booked: Y
- Follow-up date: 05/07/2025

**Comment:**
```
CS 23/04/2025 (30) JDS AS PER CL DATED 24/05/2025 MEDICATION PRESCRIBED/TREATMENT COMPLETED. F/U APPT BOOKED FOR 05/07/2025
```

---

### **Example 2: Treatment Letter WITHOUT Follow-up Booked**

**Letter:**
```
Date: 24/05/2025
Dear Patient,
Treatment completed on 23/04/2025. Follow-up required in 6 weeks.
```

**PAS:**
- Follow-up booked: N

**Comment:**
```
CS 23/04/2025 (30) JDS AS PER CL DATED 24/05/2025 MEDICATION PRESCRIBED/TREATMENT COMPLETED. F/U APPT REQUIRED BOOKING
```

---

### **Example 3: Discharge with No Follow-up**

**Letter:**
```
Date: 16/09/2025
Results normal. No further treatment required. Discharged to GP care.
```

**Comment:**
```
CS 16/09/2025 (34) IE AS PER CL DATED 16/09/2025 DISCHARGED NO TREATMENT REQUIRED
```

---

### **Example 4: Decision to Treat - Patient on WL**

**Letter:**
```
Date: 16/09/2025
Decision made to list patient for knee arthroscopy.
Patient added to surgical waiting list today.
```

**PAS:**
- Waiting list: Y

**Validation Date:** 08/10/2025

**Comment:**
```
08/10/2025 CO DECISION TO TREAT MADE. PATIENT ADDED TO WAITING LIST
```

---

### **Example 5: Decision to Treat - NOT on WL Yet**

**Letter:**
```
Date: 16/09/2025
Decision made to list patient for surgery.
```

**PAS:**
- Waiting list: N

**Validation Date:** 08/10/2025

**Comment:**
```
08/10/2025 CO DECISION TO TREAT MADE. AWAITING WAITING LIST ENTRY
```

---

## ✅ **Validation Workflow:**

1. **Read Letter** → Extract:
   - Letter date
   - What happened (treatment/discharge/decision)
   - What's needed next (follow-up/WL/diagnostics)

2. **Check PAS** → Verify:
   - Has letter action been completed?
   - Follow-up booked? (Y/N)
   - Waiting list entry? (Y/N)
   - Diagnostics ordered? (Y/N)

3. **Update PAS** → Correct any mismatches:
   - If letter says "treatment on 23/04" but PAS blank → UPDATE PAS
   - If letter says "F/U in 6 weeks" but not booked → BOOK IT or FLAG

4. **Generate Comment** → Reflects FINAL state:
   - After you've updated PAS
   - Comment shows what IS NOW in system
   - Not what WAS missing

---

## 🎯 **Key Principle:**

**Comment = What you've VERIFIED and UPDATED in PAS**

**NOT** what was originally missing!

After validation:
- Letter says: Treatment on 23/04
- PAS was empty
- You UPDATE PAS: Treatment recorded, code 30 added, F/U booked
- Comment reflects COMPLETED state: `CS 23/04/2025 (30) JDS...`

---

## 📝 **Quick Reference:**

| RTT Code | Clock Action | Comment Format |
|----------|--------------|----------------|
| 10 | START | `[VALIDATION_DATE] [INITIALS] REFERRAL RECEIVED...` |
| 20 | CONTINUE | `[VALIDATION_DATE] [INITIALS] [LETTER SUMMARY]...` |
| 30 | **STOP** | `CS [STOP_DATE] (30) [INITIALS] AS PER CL DATED [LETTER_DATE]...` |
| 31/32 | **PAUSE** | `AM (CODE XX) [INITIALS] AS PER CL DATED [LETTER_DATE]...` |
| 33 | CONTINUE/STOP | `DNA (33) [INITIALS] AS PER APPOINTMENT DATED [DATE]...` |
| 34 | **STOP** | `CS [STOP_DATE] (34) [INITIALS] AS PER CL DATED [LETTER_DATE]...` |
| 35 | **STOP** | `CS [STOP_DATE] (35) [INITIALS] AS PER CL DATED [LETTER_DATE]...` |

### **Key Difference:**
- **Clock STOPPED (30-36):** Use full format with `CS [DATE] ([CODE]) [INITIALS] AS PER CL DATED...`
- **Clock CONTINUES (10, 20, etc.):** Use simple format `[VALIDATION_DATE] [INITIALS] [SUMMARY]`

---

*T21 Services UK | NHS Standard Comment Format*  
*Validation Comments Reflecting Verified PAS Data*
