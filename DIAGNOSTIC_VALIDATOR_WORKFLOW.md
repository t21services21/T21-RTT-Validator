# 🔬 DIAGNOSTIC TEST - Validator Workflow Explained

**Date:** October 18, 2025 at 4:24pm  
**Purpose:** Clarify what validators must CHECK for diagnostic tests

---

## **🎯 THE QUESTION:**

**Letter says:** "Patient needs MRI Brain for suspected MS"

**But validator must CHECK:**
1. ❓ Is the test booked yet?
2. ❓ Has the test been done yet?
3. ❓ Are results available yet?

**Comment based on what you FIND, not what letter says!**

---

## **🔍 THE 4 DIAGNOSTIC STATES:**

### **State 1: Test NOT Booked Yet**

**What validator finds:**
- Letter says: "MRI Brain needed"
- System shows: No test ordered yet
- Status: **NOT BOOKED**

**Comment:**
```
18/10/2025 T21 - AWAITING DSG [MRI BRAIN] FOR SUSPECTED MS
```

**Means:** Test not booked yet, awaiting diagnostic

---

### **State 2: Test BOOKED But Not Done**

**What validator finds:**
- Letter says: "MRI Brain needed"
- System shows: MRI booked for 25/10/2025
- Today: 18/10/2025 (test date in future)
- Status: **BOOKED BUT NOT DONE YET**

**Comment:**
```
18/10/2025 T21 - DSG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS
```

**Means:** Test is booked for 25/10/2025, but hasn't happened yet

---

### **State 3: Test DONE But Awaiting Results**

**What validator finds:**
- System shows: MRI done on 25/10/2025
- Today: 30/10/2025 (test date has passed)
- Results: Not received yet
- Status: **DONE, AWAITING RESULTS**

**Comment:**
```
30/10/2025 T21 - DXG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS - AWAITING RESULTS
```

**Means:** Test was done on 25/10/2025, now waiting for results

---

### **State 4: Test DONE And Results Received**

**What validator finds:**
- System shows: MRI done on 25/10/2025
- Results: No abnormality detected
- Status: **DONE, RESULTS IN**

**Comment:**
```
05/11/2025 T21 - DXG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS - RESULTS: NO ABNORMALITY DETECTED
```

**Means:** Test was done, results show no abnormality

---

## **📊 VALIDATOR DECISION TREE:**

```
Letter mentions diagnostic test
         |
         ↓
    CHECK SYSTEM
         |
         ↓
Is test booked? ────NO───→ AWAITING DSG [TEST] FOR [CONDITION]
         |
        YES
         ↓
Has test date passed?
         |
    ┌────┴────┐
   NO        YES
    |          |
    ↓          ↓
DSG [TEST]   Are results
[DATE] FOR   available?
[CONDITION]      |
            ┌────┴────┐
           NO        YES
            |          |
            ↓          ↓
         DXG [TEST]  DXG [TEST]
         [DATE] FOR  [DATE] FOR
         [CONDITION] [CONDITION]
         AWAITING    RESULTS:
         RESULTS     [OUTCOME]
```

---

## **💡 REAL EXAMPLE:**

### **Scenario: MRI Brain for Suspected MS**

**Letter received:** 15/10/2025  
**Letter says:** "Patient requires MRI Brain to investigate suspected Multiple Sclerosis"

---

### **Validation 1: 18/10/2025**

**Validator checks system:**
- Test booked? YES
- Test date: 25/10/2025
- Today: 18/10/2025
- Test done? NO (future date)

**Comment:**
```
18/10/2025 T21 - DSG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS
```

**State:** Test BOOKED but not done yet

---

### **Validation 2: 30/10/2025** (New letter or follow-up)

**Validator checks system:**
- Test booked? YES
- Test date: 25/10/2025
- Today: 30/10/2025
- Test done? YES (date has passed)
- Results? NO (not received yet)

**Comment:**
```
30/10/2025 T21 - DXG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS - AWAITING RESULTS
```

**State:** Test DONE, awaiting results

---

### **Validation 3: 05/11/2025** (Results letter received)

**Validator checks system:**
- Test done: YES (25/10/2025)
- Results: YES (No abnormality detected)

**Comment:**
```
05/11/2025 T21 - DXG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS - RESULTS: NO ABNORMALITY DETECTED
```

**State:** Test DONE, results received

---

## **🔑 KEY ABBREVIATIONS:**

| Abbreviation | Meaning | When to Use |
|--------------|---------|-------------|
| **AWAITING DSG** | Awaiting Diagnostic | Test NOT booked yet |
| **DSG [test] [date]** | Diagnostic Scheduled | Test BOOKED but not done |
| **DXG [test] [date]** | Diagnostic Complete | Test DONE |
| **AWAITING RESULTS** | Waiting for results | Test done, results not in |
| **RESULTS: [outcome]** | Results statement | Results received |

---

## **⚠️ COMMON MISTAKES:**

### **Mistake 1: Not Checking Date**

**Wrong:**
```
Letter says: MRI booked 25/10/2025
Comment: 18/10/2025 T21 - DXG [MRI] 25/10/2025 - AWAITING RESULTS
```

**Problem:** Used "DXG" (diagnostic complete) but test is in future!

**Correct:**
```
18/10/2025 T21 - DSG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS
```

---

### **Mistake 2: Not Checking Results Status**

**Wrong:**
```
Test done 25/10/2025, but no results yet
Comment: 30/10/2025 T21 - DXG [MRI] 25/10/2025 - RESULTS: PENDING
```

**Problem:** Used "RESULTS:" field when results not available!

**Correct:**
```
30/10/2025 T21 - DXG [MRI BRAIN] 25/10/2025 FOR SUSPECTED MS - AWAITING RESULTS
```

---

## **✅ VALIDATOR CHECKLIST:**

When letter mentions diagnostic test:

1. [ ] **CHECK:** Is test booked in system?
   - NO → Use "AWAITING DSG"
   - YES → Continue to step 2

2. [ ] **CHECK:** What's the test date?
   - Future date → Use "DSG [test] [date]"
   - Past date → Continue to step 3

3. [ ] **CHECK:** Are results available?
   - NO → Use "DXG [test] [date] - AWAITING RESULTS"
   - YES → Use "DXG [test] [date] - RESULTS: [outcome]"

4. [ ] **INCLUDE:** Full details
   - Test name
   - Test date
   - Condition/diagnosis
   - Results (if available)

---

## **🎓 WHAT LETTER INTERPRETER NOW TEACHES:**

### **Step 5: NHS Comment Format - DIAGNOSTIC Section**

Shows:
- ⚠️ Warning: "Validator must CHECK: Is test booked? Has test date passed? Are results available?"
- **4 clear scenarios:**
  1. Test NOT booked yet
  2. Test BOOKED but not done
  3. Test DONE - awaiting results
  4. Test DONE - results received

### **Step 6: Next Actions**

Shows:
- CHECK diagnostic system
- CHECK test date vs today's date
- CHECK results status
- Comment based on what you FIND

---

## **🚀 DEPLOYMENT:**

```
Double-click: DEPLOY_ALL_3_FIXES.bat
```

Includes:
1. ✅ Pathway date fix
2. ✅ Letter Interpreter with T21 formats
3. ✅ Enhanced detailed formats
4. ✅ **Diagnostic validator workflow** (NEW!)
5. ✅ Interview Prep fix

---

**Validators will now understand they must CHECK the system and comment based on reality, not assumptions!** ✅

---

*T21 Services Limited | Validator Training*  
*Last Updated: October 18, 2025 at 4:24pm*
