# 📚 T21 RTT Example Scenarios

Use these example scenarios to practice with the T21 RTT Pathway Intelligence system.

---

## Scenario 1: Standard Compliant Pathway ✅

**Specialty:** ENT  
**Referral Source:** GP  
**Referral Received Date:** 02/01/2025  
**First Appointment Date:** 10/01/2025  
**Diagnostics Date:** 25/01/2025  
**Decision To Treat Date:** 01/02/2025  
**Planned Admission Date:** 12/02/2025  
**First Treatment Date:** 20/02/2025  
**Delays/Pauses:** None  
**Current RTT Event:** 30  

**Expected Result:**
- Clock Status: Stopped
- Weeks Elapsed: 7
- Breach Flag: None
- Action: Stop (treatment completed)

---

## Scenario 2: Pathway with Patient-Initiated Delay ⏸️

**Specialty:** Orthopaedics  
**Referral Source:** GP  
**Referral Received Date:** 01/01/2025  
**First Appointment Date:** 15/01/2025  
**Diagnostics Date:** 20/01/2025  
**Decision To Treat Date:** 05/02/2025  
**Planned Admission Date:** 01/03/2025  
**First Treatment Date:** 15/03/2025  
**Delays/Pauses:** Patient requested 4-week delay for holiday  
**Current RTT Event:** 30  

**Expected Result:**
- Clock Status: Stopped
- Weeks Elapsed: 6 (10 calendar weeks minus 4 pause weeks)
- Breach Flag: None
- Action: Stop (with documented pause)

---

## Scenario 3: Active Monitoring Pathway 🔍

**Specialty:** Dermatology  
**Referral Source:** GP  
**Referral Received Date:** 05/01/2025  
**First Appointment Date:** 15/01/2025  
**Diagnostics Date:** 16/01/2025  
**Decision To Treat Date:** N/A  
**Planned Admission Date:** N/A  
**First Treatment Date:** N/A  
**Active Monitoring:** 32_clinician  
**AM Start Date:** 18/01/2025  
**Delays/Pauses:** Conservative management - review in 12 weeks  
**Current RTT Event:** 32  

**Expected Result:**
- Clock Status: Paused
- Breach Flag: None (clock paused during AM)
- Action: Pause
- Code: 32 (clinician-initiated active monitoring)

---

## Scenario 4: Breached Pathway (26 weeks) 🚨

**Specialty:** Urology  
**Referral Source:** GP  
**Referral Received Date:** 01/08/2024  
**First Appointment Date:** 15/08/2024  
**Diagnostics Date:** 01/09/2024  
**Decision To Treat Date:** 15/09/2024  
**Planned Admission Date:** TBC  
**First Treatment Date:** N/A  
**Delays/Pauses:** None  
**Current RTT Event:** 20  

**Expected Result:**
- Clock Status: Active
- Weeks Elapsed: 27+
- Breach Flag: 26-week breach
- Action: Escalate (serious wait breach)

---

## Scenario 5: Critical Breach (52 weeks) ⚠️

**Specialty:** General Surgery  
**Referral Source:** GP  
**Referral Received Date:** 01/01/2024  
**First Appointment Date:** 15/01/2024  
**Diagnostics Date:** 01/02/2024  
**Decision To Treat Date:** 15/02/2024  
**Planned Admission Date:** TBC  
**First Treatment Date:** N/A  
**Delays/Pauses:** Multiple cancellations by trust  
**Current RTT Event:** 20  

**Expected Result:**
- Clock Status: Breached
- Weeks Elapsed: 52+
- Breach Flag: 52-week breach (critical)
- Action: Escalate immediately
- Note: Provider cancellations do NOT pause clock

---

## Clinic Letter Examples

### Example 1: Decision to Treat (Surgical Listing)

```
ENT Review: Patient assessed for deviated septum.
Plan: Proceed to septoplasty – patient consented.
Please book on surgical waiting list (ENT – Septoplasty).
Follow-up in 6 weeks pre-op clinic to confirm fitness.
Copy to GP.
```

**Expected Code:** 20 (Continue)  
**Required Actions:**
- Add to surgical waiting list
- Book pre-op appointment (6 weeks)
- Send GP letter

---

### Example 2: Active Monitoring

```
We have agreed to manage Ms A. Khan conservatively for 6 months.
Please arrange review at 26 weeks.
No diagnostic tests required at this stage.
```

**Expected Code:** 32 (Clinician-initiated AM)  
**Required Actions:**
- Record AM start (code 32)
- Book 26-week review
- Clock pauses

---

### Example 3: Discharge (No Treatment Required)

```
Patient seen in clinic. Symptoms have resolved.
No intervention required at this time.
Discharge back to GP care.
```

**Expected Code:** 34 (Decision not to treat)  
**Required Actions:**
- Record discharge (code 34)
- Send GP letter
- Clock stops

---

## Timeline Auditor Examples

### Example 1: Correct Timeline ✅

```
01/02/2025 – Referral received – Code 10 – GP to ENT
10/02/2025 – New OP – Code 20
22/02/2025 – Diagnostics – Code 92
01/03/2025 – DTT – Code 20
20/03/2025 – Septoplasty – Code 30
```

**Expected Result:** Pass (correct sequencing)

---

### Example 2: Duplicate Code 10 ❌

```
01/02/2025 – Referral received – Code 10
06/02/2025 – New OP – Code 10
18/02/2025 – Diagnostics – Code 20
```

**Expected Result:** Fail  
**Issue:** Duplicate code 10 (should be unique)  
**Fix:** Change 06/02/2025 to code 20

---

### Example 3: Code 91 Without AM Start ❌

```
01/02/2025 – Referral received – Code 10
10/02/2025 – OP review – Code 91
```

**Expected Result:** Fail  
**Issue:** Code 91 used without prior code 31 or 32  
**Fix:** Change to code 20 OR add code 31/32 first

---

### Example 4: Code 20 After Treatment ❌

```
01/02/2025 – Referral received – Code 10
10/02/2025 – New OP – Code 20
20/02/2025 – Surgery (FDT) – Code 30
05/03/2025 – Post-op review – Code 20
```

**Expected Result:** Warning  
**Issue:** Code 20 used after code 30 (treatment)  
**Fix:** Change 05/03/2025 to code 90 (FDT occurred previously)

---

## Practice Exercises

### Exercise 1: Identify the Breach
**Given:**
- Referral: 01/09/2024
- First Appt: 15/09/2024
- Treatment: 15/02/2025
- Patient delay: 2 weeks

**Question:** What is the breach status?

<details>
<summary>Answer</summary>

Total weeks: 24  
Adjusted: 24 - 2 = 22 weeks  
**Breach Flag:** 18-week breach (over 18 but under 26)

</details>

---

### Exercise 2: Choose the Correct Code
**Scenario:** Patient attends 3rd review during active monitoring period.

**Question:** What code should be used?

<details>
<summary>Answer</summary>

**Code 91** (Activity during active monitoring)  
Note: This assumes code 31 or 32 was recorded when AM started.

</details>

---

### Exercise 3: Spot the Timeline Error
**Timeline:**
```
01/01/2025 – Referral – Code 10
15/01/2025 – OP – Code 20
20/01/2025 – Surgery – Code 30
25/01/2025 – Surgery – Code 30
```

**Question:** What's wrong?

<details>
<summary>Answer</summary>

**Duplicate code 30** - Code 30 should only appear ONCE per pathway.  
Second surgery (if genuine) should be recorded as part of the same treatment episode or a new pathway must be started.

</details>

---

## Tips for Using the App

1. **Start with simple scenarios** (Example 1) to understand the flow
2. **Experiment with dates** to see breach thresholds in action
3. **Test pause logic** by adding patient-initiated delays
4. **Use the Timeline Auditor** to understand code sequencing rules
5. **Read the "About RTT Rules"** section for quick reference

---

*Practice makes perfect! Work through these scenarios to build RTT validation expertise.*

**T21 Services UK | NHS RTT Training Environment**
