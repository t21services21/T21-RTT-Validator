# 🤖 AI VALIDATION - Reading Letters AND Comment Lines

**Date:** October 14, 2025  
**Purpose:** How AI validates when letters are NOT available  
**Method:** Read NHS comment lines to extract episodes and codes

---

## 🎯 THE REAL SITUATION

### Sometimes We Don't Have Letters!

**Problem:**
- Clinic letters not scanned
- Letters not available in system
- Letters missing or lost
- Only have PAS comment lines

**Solution:**
- Read comment lines instead
- Extract what happened from comments
- Translate comments to RTT codes
- Validate episodes from comments

---

## 📋 NHS COMMENT LINE FORMATS

### **Format 1: Clock Continues**
```
[DATE] T21 - [ACTION/STATUS]
```

### **Format 2: Clock Stops**
```
CS ([STOP_DATE])([CODE]) [INITIALS] REASON FOR CLOCK STOP
```

---

## 🔍 AI MUST READ COMMENT LINES

### Example 1: Referral Received (Code 10)

**Comment Line:**
```
01/07/2022 T21 - AWAITING 1ST OPA
```

**AI Extracts:**
- Date: 01/07/2022
- Action: Awaiting first outpatient appointment
- RTT Code: 10 (referral received)
- Clock Status: Started
- Episode: 1

**AI Records:**
```
Episode 1: Code 10, Date 01/07/2022 (Referral received)
Status: On PBL, awaiting first appointment
Clock: STARTED
```

---

### Example 2: First Appointment Booked (Still Code 10)

**Comment Line:**
```
03/07/2022 T21 - 1ST OPA 10/12/2022
```

**AI Extracts:**
- Date: 03/07/2022 (comment date)
- Action: First appointment booked
- Appointment Date: 10/12/2022
- RTT Code: Still 10 (nothing happened yet)
- Clock Status: Still ticking
- Episode: Still 1

**AI Records:**
```
Episode 1: Code 10, Date 01/07/2022 (Referral received)
Status: First appointment booked for 10/12/2022
Clock: TICKING
```

**Note:** Code stays 10 until patient ATTENDS!

---

### Example 3: MRI Scan Needed (Code 20)

**Comment Line:**
```
01/07/2022 T21 - AWAITING DSG [MRI SCAN]
```

**AI Extracts:**
- Date: 01/07/2022
- Action: Awaiting diagnostic (MRI scan)
- RTT Code: 20 (subsequent activity)
- Clock Status: Ticking
- Episode: 2

**AI Records:**
```
Episode 1: Code 10, Date 01/07/2022 (Referral)
Episode 2: Code 20, Date 01/07/2022 (MRI scan requested)
Status: Awaiting MRI booking
Clock: TICKING
```

---

### Example 4: MRI Scan Booked (Still Code 20)

**Comment Line:**
```
01/10/2017 T21 - DSG [MRI SCAN] 04/11/2017
```

**AI Extracts:**
- Date: 01/10/2017 (comment date)
- Action: Diagnostic booked
- Test: MRI SCAN
- Test Date: 04/11/2017
- RTT Code: 20 (subsequent activity)
- Clock Status: Ticking
- Episode: Still 2

**AI Records:**
```
Episode 1: Code 10, Date 01/07/2022 (Referral)
Episode 2: Code 20, Date 01/10/2017 (MRI scan booked for 04/11/2017)
Status: MRI booked
Clock: TICKING
```

---

### Example 5: MRI Scan Done (Code 20)

**Comment Line:**
```
01/07/2022 T21 - DXG [MRI SCAN] 05/11/2017
```

**AI Extracts:**
- Date: 01/07/2022 (comment date)
- Action: Diagnostic done (DXG)
- Test: MRI SCAN
- Test Date: 05/11/2017
- RTT Code: 20 (diagnostic completed)
- Clock Status: Ticking (diagnostics don't stop clock!)
- Episode: 3

**AI Records:**
```
Episode 1: Code 10, Date 01/07/2022 (Referral)
Episode 2: Code 20, Date 01/10/2017 (MRI scan booked)
Episode 3: Code 20, Date 05/11/2017 (MRI scan completed)
Status: MRI done, awaiting results review
Clock: TICKING
```

---

### Example 6: Surgery Date Set (Code 20)

**Comment Line:**
```
01/07/2022 T21 - 1CL 25/12/2022
```

**AI Extracts:**
- Date: 01/07/2022 (comment date)
- Action: First clinic/TCI date set
- Surgery Date: 25/12/2022
- RTT Code: 20 (subsequent activity)
- Clock Status: Ticking
- Episode: 4

**AI Records:**
```
Episode 1: Code 10, Date 01/07/2022 (Referral)
Episode 2: Code 20, Date 01/10/2017 (MRI booked)
Episode 3: Code 20, Date 05/11/2017 (MRI done)
Episode 4: Code 20, Date 01/07/2022 (Surgery date set: 25/12/2022)
Status: On surgical waiting list, TCI date 25/12/2022
Clock: TICKING
```

---

### Example 7: Treatment Given - CLOCK STOPS! (Code 30)

**Comment Line:**
```
CS (23/04/2025)(30) JDS PATIENT RCVD MEDICATION/TREATMENT
```

**AI Extracts:**
- CS = Clock Stop
- Stop Date: 23/04/2025
- RTT Code: 30 (first definitive treatment)
- Initials: JDS
- Reason: Patient received medication/treatment
- Clock Status: STOPPED
- Episode: 5 (FINAL)

**AI Records:**
```
Episode 1: Code 10, Date 01/07/2022 (Referral)
Episode 2: Code 20, Date 01/10/2017 (MRI booked)
Episode 3: Code 20, Date 05/11/2017 (MRI done)
Episode 4: Code 20, Date 01/07/2022 (Surgery date set)
Episode 5: Code 30, Date 23/04/2025 (Treatment given - CLOCK STOPS!)
Status: Pathway complete
Clock: STOPPED
Waiting Time: 23/04/2025 - 01/07/2022 = Calculate days
```

---

### Example 8: Patient Declined Treatment (Code 35)

**Comment Line:**
```
CS (20/08/2025)(35) AKM PATIENT DECLINED TREATMENT
```

**AI Extracts:**
- CS = Clock Stop
- Stop Date: 20/08/2025
- RTT Code: 35 (patient declined)
- Initials: AKM
- Reason: Patient declined treatment
- Clock Status: STOPPED
- Episode: Final

**AI Records:**
```
Episode X: Code 35, Date 20/08/2025 (Patient declined - CLOCK STOPS!)
Status: Pathway closed - patient choice
Clock: STOPPED
```

---

### Example 9: Discharge No Treatment (Code 34)

**Comment Line:**
```
CS (15/09/2025)(34) MOD PATIENT DISCHARGED - NO TREATMENT REQUIRED
```

**AI Extracts:**
- CS = Clock Stop
- Stop Date: 15/09/2025
- RTT Code: 34 (decision not to treat)
- Initials: MOD
- Reason: Patient discharged, no treatment required
- Clock Status: STOPPED
- Episode: Final

**AI Records:**
```
Episode X: Code 34, Date 15/09/2025 (Discharged - CLOCK STOPS!)
Status: Pathway closed - no treatment needed
Clock: STOPPED
```

---

### Example 10: DNA Recorded (Code 33)

**Comment Line:**
```
01/07/2022 T21 - DNA RECORDED. REBOOK REQUIRED
```

**AI Extracts:**
- Date: 01/07/2022
- Action: DNA (Did Not Attend)
- RTT Code: 33 (if first appointment) or 20 (if not first)
- Clock Status: Depends on if first appointment
- Next Action: Rebook required

**AI Records:**
```
Episode X: Code 33, Date 01/07/2022 (DNA first appointment)
Status: DNA recorded, awaiting rebook decision
Clock: STOPPED (if Code 33) or TICKING (if Code 20)
```

---

### Example 11: Returned from Active Monitoring (Code 11)

**Comment Line:**
```
01/07/2022 T21 - RETURNED FROM AM. CLOCK RESTARTED
```

**AI Extracts:**
- Date: 01/07/2022
- Action: Returned from Active Monitoring
- RTT Code: 11 (clock restart after watchful wait)
- Clock Status: RESTARTED
- Previous Code: Must have been 31/32/91

**AI Records:**
```
Episode X-1: Code 31/32, Date [PREVIOUS] (Watchful wait - CLOCK STOPPED)
Episode X: Code 11, Date 01/07/2022 (Clock RESTARTED)
Status: Active treatment pathway resumed
Clock: RESTARTED
Waiting Time: Period 1 + Period 2 (exclude watchful wait)
```

---

## 🤖 AI VALIDATION PROCESS WITH COMMENTS

### Step 1: Read ALL Comment Lines
```
01/07/2022 T21 - AWAITING 1ST OPA
03/07/2022 T21 - 1ST OPA 10/12/2022
10/12/2022 T21 - AWAITING DSG [MRI SCAN]
15/12/2022 T21 - DSG [MRI SCAN] 20/12/2022
20/12/2022 T21 - DXG [MRI SCAN] 20/12/2022
05/01/2023 T21 - AWAITING 1CL
10/01/2023 T21 - 1CL 15/02/2023
CS (15/02/2023)(30) JDS PATIENT RCVD TREATMENT
```

### Step 2: Extract Episodes
```
Episode 1: Code 10, 01/07/2022 (Referral - AWAITING 1ST OPA)
Episode 2: Code 20, 10/12/2022 (First appointment attended)
Episode 3: Code 20, 15/12/2022 (MRI scan booked)
Episode 4: Code 20, 20/12/2022 (MRI scan done)
Episode 5: Code 20, 05/01/2023 (Added to waiting list)
Episode 6: Code 20, 10/01/2023 (Surgery date set)
Episode 7: Code 30, 15/02/2023 (Treatment given - CLOCK STOPS!)
```

### Step 3: Validate Code Sequence
```
✅ Code 10 first (referral)
✅ Code 20 for all activities
✅ Code 30 last (treatment)
✅ No code 20 after code 30
✅ All dates chronological
✅ Sequence valid
```

### Step 4: Calculate Waiting Time
```
Clock Start: 01/07/2022
Clock Stop: 15/02/2023
Waiting Time: 229 days = 32.7 weeks
Breach: YES (>18 weeks)
```

### Step 5: Validate Against PAS
```
Check PAS has all 7 episodes
Check codes match comments
Check dates match comments
Check waiting time correct
```

---

## 📊 COMMENT LINE ABBREVIATIONS AI MUST UNDERSTAND

| Abbreviation | Meaning | RTT Code |
|--------------|---------|----------|
| **AWAITING 1ST OPA** | Awaiting first outpatient appointment | 10 |
| **1ST OPA [DATE]** | First appointment booked | 10 |
| **AWAITING DSG [TEST]** | Awaiting diagnostic test | 20 |
| **DSG [TEST] [DATE]** | Diagnostic booked | 20 |
| **DXG [TEST] [DATE]** | Diagnostic done | 20 |
| **AWAITING RESULTS** | Awaiting test results | 20 |
| **AWAITING 1CL** | Awaiting TCI date (surgery) | 20 |
| **1CL [DATE]** | TCI date set | 20 |
| **AWAITING F/U APPT** | Awaiting follow-up | 20 |
| **F/U APPT [DATE]** | Follow-up booked | 20 |
| **DNA RECORDED** | Did not attend | 33 or 20 |
| **RETURNED FROM AM** | Returned from active monitoring | 11 |
| **CS ([DATE])(30)** | Clock stop - treatment | 30 |
| **CS ([DATE])(34)** | Clock stop - discharge | 34 |
| **CS ([DATE])(35)** | Clock stop - declined | 35 |
| **CS ([DATE])(36)** | Clock stop - deceased | 36 |

---

## ✅ AI VALIDATION LOGIC

### When Letter Available:
1. Read letter
2. Extract what happened
3. Translate to RTT code
4. Create episode
5. Validate in PAS

### When Letter NOT Available:
1. Read comment lines
2. Extract what happened from comments
3. Translate comments to RTT codes
4. Create episodes from comments
5. Validate in PAS

### Both Methods Result In:
- Complete episode timeline
- Correct RTT codes
- Accurate waiting time
- Valid pathway

---

## 🎯 SUMMARY

**AI Must Be Able To:**
1. ✅ Read clinic letters (NLP)
2. ✅ Read comment lines (NLP)
3. ✅ Extract episodes from both
4. ✅ Translate to RTT codes
5. ✅ Validate code sequences
6. ✅ Calculate waiting times
7. ✅ Auto-fix errors
8. ✅ Generate reports

**Comment Lines Are:**
- Shorthand for what happened
- Used when letters not available
- Standardized format (T21 style)
- Contain all key information
- Can be read by AI

**AI Validation Works With:**
- Clinic letters ✅
- Comment lines ✅
- Consultation notes ✅
- Diagnostic reports ✅
- Operation notes ✅
- Any text describing patient journey ✅

**This is TRUE AI validation!** 🚀

---

**T21 Services Limited | Company No: 13091053**  
**AI Validation - Reading Letters AND Comment Lines**
