# T21 SERVICES COMMENTING STYLES
## Official NHS Comment Format Guide

---

## 📋 **TWO MAIN FORMATS:**

### **1️⃣ CLOCK CONTINUES:**
```
[DATE] T21 - [ACTION/STATUS]
```

### **2️⃣ CLOCK STOPS:**
```
CS ([STOP_DATE])([CODE]) [INITIALS] REASON FOR CLOCK STOP
```

---

## ✅ **CLOCK CONTINUES COMMENTS:**

### **Referrals & Appointments:**

| Type | Format | Example |
|------|--------|---------|
| Awaiting 1st OPA | `[DATE] T21 - AWAITING 1ST OPA` | `01/07/2022 T21 - AWAITING 1ST OPA` |
| 1st OPA Booked | `[DATE] T21 - 1ST OPA [DATE]` | `03/07/2022 T21 - 1ST OPA 10/12/2022` |
| Awaiting F/U Appt | `[DATE] T21 - AWAITING F/U APPT` | `01/07/2022 T21 - AWAITING F/U APPT` |
| F/U Appt Booked | `[DATE] T21 - F/U APPT [DATE]` | `01/07/2022 T21 - F/U APPT 05/11/2017` |

---

### **Diagnostics/Tests:**

| Type | Format | Example |
|------|--------|---------|
| Awaiting Diagnostic | `[DATE] T21 - AWAITING DSG [TEST NAME]` | `01/07/2022 T21 - AWAITING DSG [MRI SCAN]` |
| Diagnostic Booked | `[DATE] T21 - DSG [TEST NAME] [DATE]` | `01/10/2017 T21 - DSG [MRI SCAN] 04/11/2017` |
| Diagnostic Done | `[DATE] T21 - DXG [TEST NAME] [DATE]` | `01/07/2022 T21 - DXG [WB RT RX(T)] 05/11/2017` |
| Awaiting Results | `[DATE] T21 - AWAITING RESULTS [TEST]` | `01/07/2022 T21 - AWAITING RESULTS [RCS]` |

---

### **Surgery/Waiting List:**

| Type | Format | Example |
|------|--------|---------|
| Awaiting WL Entry | `[DATE] T21 - AWAITING WAITING LIST ENTRY` | `01/07/2022 T21 - AWAITING WAITING LIST ENTRY` |
| Awaiting TCI Date | `[DATE] T21 - AWAITING 1CL` | `01/07/2022 T21 - AWAITING 1CL` |
| TCI Date Set | `[DATE] T21 - 1CL [SURGERY DATE]` | `01/07/2022 T21 - 1CL 25/12/2022` |

---

### **Other Scenarios:**

| Type | Format | Example |
|------|--------|---------|
| Awaiting Clinic Letter | `[DATE] T21 - NO CLINIC LTR` | `01/10/2022 T21 - NO CLINIC LTR` |
| DNA Recorded | `[DATE] T21 - DNA RECORDED. REBOOK REQUIRED` | `01/07/2022 T21 - DNA RECORDED. REBOOK REQUIRED` |
| Returned from AM | `[DATE] T21 - RETURNED FROM AM. CLOCK RESTARTED` | `01/07/2022 T21 - RETURNED FROM AM. CLOCK RESTARTED` |

---

## 🛑 **CLOCK STOP COMMENTS:**

### **Format:**
```
CS ([STOP_DATE])([RTT_CODE]) [VALIDATOR_INITIALS] REASON FOR CLOCK STOP
```

### **Examples:**

| RTT Code | Reason | Example |
|----------|--------|---------|
| **30** | First Definitive Treatment | `CS (23/04/2025)(30) JDS PATIENT RCVD MEDICATION/TREATMENT` |
| **30** | Treatment with F/U | `CS (23/04/2025)(30) JDS PATIENT RCVD MEDICATION/TREATMENT. F/U APPT BOOKED` |
| **34** | Discharge | `CS (15/09/2025)(34) MOD PATIENT DISCHARGED - NO TREATMENT REQUIRED` |
| **35** | Patient Declined | `CS (20/08/2025)(35) AKM PATIENT DECLINED TREATMENT` |
| **36** | Further TX Not Appropriate | `CS (10/07/2025)(36) IE FURTHER TREATMENT NOT APPROPRIATE` |

---

## 📊 **COMPLETE EXAMPLES:**

### **Example 1: Referral Received**

**Letter:** GP referral received 01/07/2022

**Comment:**
```
01/07/2022 T21 - AWAITING 1ST OPA
```

---

### **Example 2: MRI Scan to be Booked**

**Letter:** Patient to undergo MRI scan

**PAS:** MRI ordered = NO

**Comment:**
```
08/10/2025 T21 - AWAITING DSG [MRI SCAN]
```

---

### **Example 3: MRI Scan Booked**

**Letter:** Patient to undergo MRI scan

**PAS:** MRI ordered = YES, Date = 15/10/2025

**Comment:**
```
08/10/2025 T21 - DSG [MRI SCAN] 15/10/2025
```

---

### **Example 4: MRI Done, Awaiting Results**

**Letter:** MRI was performed on 10/10/2025. Awaiting results.

**Comment:**
```
08/10/2025 T21 - AWAITING RESULTS [MRI SCAN]
```

---

### **Example 5: MRI Results Received**

**Letter:** MRI performed 10/10/2025 showed normal findings.

**Comment:**
```
08/10/2025 T21 - DXG [MRI SCAN] 10/10/2025
```

---

### **Example 6: Waiting for Surgery Date**

**Letter:** Patient listed for knee arthroscopy

**PAS:** On waiting list = YES, TCI date = Not set

**Comment:**
```
08/10/2025 T21 - AWAITING 1CL
```

---

### **Example 7: Surgery Date Confirmed**

**Letter:** Surgery scheduled for 25/12/2025

**PAS:** On waiting list = YES, TCI date = 25/12/2025

**Comment:**
```
08/10/2025 T21 - 1CL 25/12/2025
```

---

### **Example 8: Treatment Completed (Clock Stop)**

**Letter Dated:** 24/05/2025  
**Letter Says:** Patient treated with antibiotics on 23/04/2025. Follow-up in 6 weeks.

**PAS:** Follow-up booked = YES

**Comment:**
```
CS (23/04/2025)(30) JDS PATIENT RCVD MEDICATION/TREATMENT. F/U APPT BOOKED
```

---

### **Example 9: Discharge (Clock Stop)**

**Letter Dated:** 15/09/2025  
**Letter Says:** Results normal. Discharged to GP care.

**Comment:**
```
CS (15/09/2025)(34) MOD PATIENT DISCHARGED - NO TREATMENT REQUIRED
```

---

## 🔑 **KEY ABBREVIATIONS:**

| Abbreviation | Meaning |
|--------------|---------|
| **T21** | T21 Services identifier |
| **CS** | Clock Stop |
| **OPA** | Outpatient Appointment |
| **F/U** | Follow-up |
| **DSG** | Diagnostic (to be done) |
| **DXG** | Diagnostic (done) |
| **WL** | Waiting List |
| **1CL** | First Clinic/TCI Date |
| **AM** | Active Monitoring |
| **DNA** | Did Not Attend |
| **IPT** | Inter-Provider Transfer |
| **TX** | Treatment |

---

## 📝 **QUICK DECISION TREE:**

### **Step 1: Does the clock STOP?**
- **YES** (Codes 30, 34, 35, 36) → Use `CS ([DATE])([CODE]) [INITIALS] REASON`
- **NO** (Codes 10, 20, 11, 12, 21, etc.) → Use `[DATE] T21 - [ACTION]`

### **Step 2: For Clock CONTINUES, what's the main action?**
- **Referral received** → `AWAITING 1ST OPA`
- **Diagnostic to be booked** → `AWAITING DSG [TEST]`
- **Diagnostic booked** → `DSG [TEST] [DATE]`
- **Diagnostic done** → `DXG [TEST] [DATE]` or `AWAITING RESULTS [TEST]`
- **Surgery to be listed** → `AWAITING WAITING LIST ENTRY`
- **On WL, no date** → `AWAITING 1CL`
- **Surgery date set** → `1CL [DATE]`
- **Follow-up needed** → `AWAITING F/U APPT`
- **Follow-up booked** → `F/U APPT [DATE]`

### **Step 3: For Clock STOPS, which code?**
- **30** → Treatment completed
- **34** → Discharge/no treatment
- **35** → Patient declined
- **36** → Further treatment not appropriate

---

## ✅ **VALIDATION WORKFLOW:**

1. **Read Letter** → Determine RTT code
2. **Check PAS** → See what's been done
3. **Choose Format:**
   - Clock stops? → `CS ([DATE])([CODE]) [INIT] REASON`
   - Clock continues? → `[DATE] T21 - [ACTION]`
4. **Generate Comment** → Copy to PAS
5. **Copy to Excel** → Validation Comments column

---

*T21 Services UK | Official NHS Commenting Standards*  
*Updated: 08/10/2025*
