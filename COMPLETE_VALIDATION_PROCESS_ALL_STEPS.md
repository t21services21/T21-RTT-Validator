# 🔍 COMPLETE RTT VALIDATION PROCESS - Every Single Step

**Date:** October 14, 2025  
**Purpose:** Document EVERY validation step from start to finish  
**Critical:** Code 11 RESTARTS clock previously stopped by 31/32/91

---

## 🎯 CRITICAL CORRECTION: CODE 11

### Code 11 - Clock RESTART (Not just start!)
- **Code 11** = FIRST ACTIVITY AFTER WATCHFUL WAIT ENDS
- **Restarts clock** that was previously stopped by:
  - Code 31 (Patient watchful wait)
  - Code 32 (Clinician watchful wait)
  - Code 91 (Activity during watchful wait)
- **NOT a new clock** - it's a continuation!

**Example:**
```
Step 1: Code 10 (Clock starts) - Referral received
Step 2: Code 20 (Clock ticking) - First appointment
Step 3: Code 31 (Clock STOPS) - Patient chooses watchful wait
        [Clock paused - patient monitoring condition]
Step 4: Code 11 (Clock RESTARTS) - Patient ready for treatment
Step 5: Code 20 (Clock ticking) - Further appointments
Step 6: Code 30 (Clock STOPS) - Treatment given

Total waiting time = (Step 3 date - Step 1 date) + (Step 6 date - Step 4 date)
Excludes the watchful wait period!
```

---

## 📋 COMPLETE VALIDATION PROCESS - ALL STEPS

### PHASE 1: PRE-VALIDATION SETUP

#### Step 1.1: Data Import
**What:** Load patient data from PAS/CSV
**Check:**
1. File exists and readable
2. File format valid (CSV/Excel/XML)
3. File not corrupted
4. File encoding correct (UTF-8)
5. File size reasonable (<500MB)

**Actions:**
- Parse file
- Count total records
- Identify columns
- Map to standard fields

**Output:** Raw data loaded into validation engine

---

#### Step 1.2: Column Mapping
**What:** Map PAS columns to RTT fields
**Check:**
1. NHS Number column exists
2. Patient Name column exists
3. Date of Birth column exists
4. Referral Date column exists
5. Clock Start Date column exists
6. Clock Stop Date column exists
7. RTT Code column exists
8. Specialty column exists
9. Consultant column exists
10. All mandatory columns present

**Actions:**
- Auto-detect column names
- Map to standard fields
- Flag missing columns
- Suggest corrections

**Output:** Column mapping complete

---

#### Step 1.3: Data Type Validation
**What:** Check data types correct
**Check:**
1. Dates are dates (not text)
2. Numbers are numbers
3. Codes are text/numbers
4. No mixed data types
5. No special characters in wrong fields

**Actions:**
- Convert data types
- Standardize formats
- Flag conversion errors

**Output:** Data types standardized

---

### PHASE 2: PATIENT-LEVEL VALIDATION

#### Step 2.1: NHS Number Validation
**What:** Validate NHS number for EACH patient
**Check:**
1. NHS Number exists (not blank)
2. NHS Number is 10 digits
3. NHS Number check digit valid (Modulus 11 algorithm)
4. NHS Number not duplicate in file
5. NHS Number format correct (no spaces/dashes)
6. NHS Number realistic (not 0000000000)
7. NHS Number not test number (9999999999)

**Auto-Fix:**
- Add leading zeros if 9 digits
- Remove spaces/dashes
- Flag invalid check digits

**Output:** Valid NHS numbers or error list

---

#### Step 2.2: Patient Demographics Validation
**What:** Validate patient details
**Check:**
1. Patient name not blank
2. Patient name format valid (First Last)
3. Date of birth exists
4. Date of birth format valid (DD/MM/YYYY)
5. Date of birth not in future
6. Date of birth realistic (not >120 years ago)
7. Age calculated correctly
8. Age consistent with specialty (e.g., not paediatrics if 50 years old)
9. Gender valid (1=Male, 2=Female, 9=Unknown)
10. Gender consistent with specialty (e.g., not gynae if male)
11. Postcode valid UK format
12. Postcode exists in UK database
13. GP Practice code valid (6 characters)
14. GP Practice exists in national database
15. Commissioner code valid

**Auto-Fix:**
- Format names (capitalize)
- Convert date formats
- Standardize gender codes
- Format postcodes (add space)

**Output:** Valid demographics or error list

---

#### Step 2.3: Duplicate Patient Check
**What:** Check for duplicate patients
**Check:**
1. Same NHS Number appears once only
2. Same Name + DOB appears once only
3. Same Name + Postcode appears once only
4. No duplicate pathways for same condition

**Actions:**
- Flag duplicates
- Suggest merge
- Identify which record to keep

**Output:** Duplicate report

---

### PHASE 3: PATHWAY-LEVEL VALIDATION

#### Step 3.1: Pathway Number Validation
**What:** Validate pathway identifier
**Check:**
1. PATHWAY NUMBER exists
2. PATHWAY NUMBER unique per patient per condition
3. PATHWAY NUMBER format valid
4. PATHWAY NUMBER not duplicate
5. One active pathway per condition
6. Previous pathways closed correctly

**Auto-Fix:**
- Generate missing pathway numbers
- Format pathway numbers

**Output:** Valid pathway numbers

---

#### Step 3.2: Referral Validation
**What:** Validate referral details
**Check:**
1. Referral date exists
2. Referral date format valid
3. Referral date not in future
4. Referral date not before patient DOB
5. Referral date realistic (within last 2 years)
6. Referral source valid (GP/Consultant/A&E/Dentist/Optician/Other)
7. Referral source code valid
8. Referral priority valid (Routine/Urgent/2WW)
9. Referral reason documented
10. Referral letter received (if GP referral)

**Auto-Fix:**
- Convert date formats
- Standardize referral source codes
- Format priority codes

**Output:** Valid referral data

---

#### Step 3.3: Specialty & Consultant Validation
**What:** Validate clinical codes
**Check:**
1. Specialty code exists
2. Specialty code valid (3 digits, e.g., 100)
3. Specialty code in national list
4. Treatment Function code valid
5. Consultant code exists
6. Consultant code valid format
7. Consultant exists in trust database
8. Consultant works in this specialty
9. Location code valid
10. Location exists in trust

**Auto-Fix:**
- Format specialty codes (remove decimals)
- Lookup consultant from name

**Output:** Valid clinical codes

---

### PHASE 4: CLOCK START VALIDATION

#### Step 4.1: Clock Start Date Validation
**What:** Validate RTT clock start date
**Check:**
1. Clock start date exists
2. Clock start date format valid (DD/MM/YYYY)
3. Clock start date not blank
4. Clock start date not in future
5. Clock start date not before referral date
6. Clock start date not before patient DOB
7. Clock start date realistic (within last 2 years)
8. Clock start date not on invalid date (e.g., 32/01/2025)
9. Clock start date not before 01/01/2007 (RTT started)
10. Clock start time valid (if recorded)

**2WW Specific Checks:**
11. Clock start within 24 hours of referral (2WW)
12. Clock start date = referral date (usually for 2WW)

**Urgent Specific Checks:**
13. Clock start within 2 weeks of referral (Urgent)

**Auto-Fix:**
- Convert date formats
- Set clock start = referral date if missing
- Flag future dates

**Output:** Valid clock start dates

---

#### Step 4.2: Clock Start Code Validation
**What:** Validate RTT code at clock start
**Check:**
1. Clock start code exists
2. Clock start code is 10, 11, or 12 ONLY
3. Code 10 used for NEW referral
4. Code 11 used for RESTART after watchful wait (31/32/91)
5. Code 12 used for NEW CONDITION (consultant referral)
6. Clock start code is FIRST code in pathway
7. No code 20 before clock start code
8. No code 30-36 before clock start code
9. No code 90-92 before clock start code

**Code 11 Specific Checks (CRITICAL!):**
10. If code 11, previous code must be 31, 32, or 91
11. If code 11, previous clock stop date exists
12. If code 11, time between stop and restart documented
13. If code 11, reason for restart documented
14. If code 11, this is a RESTART not a new clock
15. If code 11, waiting time calculation includes both periods

**Auto-Fix:**
- Add missing code 10 if first activity
- Change code 20 to code 10 if first
- Flag code 11 without previous 31/32/91

**Output:** Valid clock start codes

---

#### Step 4.3: Clock Start Sequence Validation
**What:** Validate code sequence from start
**Check:**
1. First code in pathway is 10, 11, or 12
2. If code 11, check previous pathway exists
3. If code 11, check previous pathway stopped with 31/32/91
4. If code 12, check referral is from consultant
5. No duplicate clock starts
6. Clock start not after first appointment
7. Clock start not after treatment

**Auto-Fix:**
- Reorder codes chronologically
- Flag invalid sequences

**Output:** Valid code sequence

---

### PHASE 5: ACTIVITY VALIDATION (Code 20)

#### Step 5.1: Appointment Validation
**What:** Validate ALL appointments
**Check:**
1. All appointments have dates
2. Appointment dates format valid
3. Appointment dates chronological
4. No appointments before referral
5. No appointments before clock start
6. No appointments after discharge
7. No appointments in future (unless booked)
8. First appointment within target:
   - 2WW: 14 days from referral
   - Urgent: 2 weeks from referral
   - Routine: 18 weeks from referral
9. Appointment type valid (N=New, F=Follow-up)
10. First appointment marked as N (New)
11. Subsequent appointments marked as F (Follow-up)
12. Appointment specialty matches pathway
13. Appointment consultant valid
14. Appointment location valid
15. Appointment outcome recorded
16. Appointment attendance status recorded

**OPA/OPD Specific Checks:**
17. OP REG DATE recorded (outpatient registration)
18. OP REG DATE = appointment date
19. OP DISCHARGED DATE recorded (if discharged)
20. OP DISCHARGED DATE after last appointment

**PBL Specific Checks:**
21. If waiting for first appointment, on PBL (Partial Booking List)
22. PBL entry has expected appointment date
23. PBL priority correct

**Auto-Fix:**
- Add missing appointment dates
- Set first appointment as N
- Set subsequent as F
- Add OP REG DATE

**Output:** Valid appointment data

---

#### Step 5.2: Appointment Outcome Validation
**What:** Validate appointment outcomes
**Check:**
1. Appointment outcome exists
2. Appointment outcome valid code
3. Outcome = Attended/DNA/Cancelled
4. If DNA, reason documented
5. If DNA and FIRST appointment, code 33 used
6. If DNA and NOT first, code 20 used
7. If Patient Cancellation, documented
8. If Hospital Cancellation, reason documented
9. If rescheduled, new appointment linked
10. If discharged, OP DISCHARGED DATE set

**DNA Specific Checks:**
11. DNA policy followed (2 DNAs = discharge?)
12. DNA letter sent to patient
13. DNA letter sent to GP
14. If 2nd DNA, decision to discharge or re-offer
15. If DNA first appointment, clock stops (code 33)

**Auto-Fix:**
- Add DNA code 33 if first appointment
- Link rescheduled appointments
- Set OP DISCHARGED DATE if discharged

**Output:** Valid outcomes

---

#### Step 5.3: Appointment RTT Code Validation
**What:** Validate RTT codes for appointments
**Check:**
1. All appointments coded as 20
2. Code 20 = SUBSEQUENT ACTIVITY
3. Code 20 used for ALL appointments after first activity
4. Code 20 does NOT stop clock
5. Code 20 can repeat multiple times
6. No code 30-36 for appointments (unless treatment)
7. No code 90-92 for active pathway appointments

**Auto-Fix:**
- Add missing code 20 for appointments
- Change incorrect codes to 20

**Output:** Valid appointment codes

---

#### Step 5.4: Diagnostic Test Validation
**What:** Validate ALL diagnostic tests/investigations
**Check:**
1. All diagnostic tests have dates
2. Test dates chronological
3. Test dates not before referral
4. Test dates not in future (unless booked)
5. Test type valid:
   - Imaging (X-ray/CT/MRI/Ultrasound)
   - Blood tests (Phlebotomy)
   - Cardiology assessment
   - Endoscopy
   - Urodynamic assessment
   - Neurophysiology
   - Nuclear Medicine
   - Sleep Studies
   - Audiology
6. Test requested by valid clinician
7. Test location valid
8. Test completed (or booked)
9. Test results available
10. Test results reviewed by clinician

**CRITICAL - Diagnostic Tests and Clock:**
11. ALL diagnostic tests coded as 20
12. Diagnostic tests do NOT stop clock
13. Diagnostic tests do NOT pause clock
14. Clock keeps ticking during diagnostics
15. Only treatment (code 30) stops clock

**WL Specific Checks (if waiting for test):**
16. If waiting for diagnostic, on WL (Waiting List)
17. TCI DATE set (To Come In date)
18. TCI DATE within 18 weeks
19. WL ACTIVE status = Yes
20. WL priority correct

**Auto-Fix:**
- Code all diagnostics as 20
- Change code 30 to 20 if diagnostic
- Set TCI DATE if missing
- Update WL ACTIVE status

**Output:** Valid diagnostic data

---

#### Step 5.5: Transfer Validation (Code 21)
**What:** Validate transfers to other providers
**Check:**
1. Transfer coded as 21
2. Transfer date valid
3. Transfer reason documented
4. Transfer destination valid (other trust/hospital)
5. Transfer accepted by receiving provider
6. IPTMDS sent (Inter Provider Transfer Data Set)
7. Clock continues at receiving trust
8. Clock does NOT restart
9. Same pathway number continues
10. Receiving trust takes responsibility

**Auto-Fix:**
- Code transfers as 21
- Flag missing IPTMDS

**Output:** Valid transfer data

---

### PHASE 6: WAITING LIST VALIDATION

#### Step 6.1: Waiting List Type Validation
**What:** Validate correct waiting list used
**Check:**
1. Patient on correct waiting list type:
   - PBL = Partial Booking List (waiting for FIRST appointment)
   - WL = Waiting List (waiting for treatment/diagnostic)
   - PL = Planned List (planned procedures)
2. PBL used ONLY for first OPA
3. WL used for treatment/diagnostic waiting
4. PL used for planned/elective procedures
5. Only on ONE waiting list at a time
6. Waiting list specialty matches pathway
7. Waiting list consultant matches pathway

**Auto-Fix:**
- Move patient to correct list
- Remove from multiple lists

**Output:** Correct waiting list assignment

---

#### Step 6.2: TCI DATE Validation
**What:** Validate To Come In date
**Check:**
1. TCI DATE exists (if on WL/PL)
2. TCI DATE format valid
3. TCI DATE not in past (unless completed)
4. TCI DATE not too far in future (>18 weeks)
5. TCI DATE within 18 weeks of clock start
6. TCI DATE realistic and achievable
7. TCI DATE considers:
   - Clinic capacity
   - Theatre capacity
   - Diagnostic capacity
   - Patient availability
8. Patient informed of TCI DATE
9. Patient consent obtained
10. Patient confirmed attendance

**Auto-Fix:**
- Set TCI DATE if missing
- Flag TCI DATE >18 weeks

**Output:** Valid TCI dates

---

#### Step 6.3: WL ACTIVE Status Validation
**What:** Validate waiting list active status
**Check:**
1. WL ACTIVE = Yes (if actively waiting)
2. WL ACTIVE = No (if removed/treated)
3. WL ACTIVE status matches patient status
4. If WL ACTIVE = Yes, TCI DATE exists
5. If WL ACTIVE = No, removal reason documented
6. If treated, WL ACTIVE = No
7. If discharged, WL ACTIVE = No

**Auto-Fix:**
- Update WL ACTIVE status
- Set to No if treated

**Output:** Correct WL status

---

#### Step 6.4: Pre-Treatment Checks
**What:** Validate pre-treatment requirements
**Check (if surgery):**
1. Pre-operative assessment completed
2. Fitness for surgery confirmed
3. Anaesthetic assessment done
4. Consent form signed
5. Blood tests done (if required)
6. Imaging done (if required)
7. MRSA screening done
8. Pregnancy test done (if applicable)
9. Fasting instructions given
10. Patient prepared

**Auto-Fix:**
- Flag missing pre-op checks

**Output:** Pre-treatment readiness

---

### PHASE 7: CLOCK STOP VALIDATION

#### Step 7.1: Clock Stop Date Validation
**What:** Validate RTT clock stop date
**Check:**
1. Clock stop date exists (if pathway complete)
2. Clock stop date format valid
3. Clock stop date not before clock start
4. Clock stop date not before referral
5. Clock stop date not in future
6. Clock stop date realistic
7. Clock stop date after all appointments
8. Clock stop date = treatment date (if code 30)
9. Clock stop time valid (if recorded)

**Auto-Fix:**
- Set clock stop date if missing
- Flag invalid dates

**Output:** Valid clock stop dates

---

#### Step 7.2: Clock Stop Code Validation
**What:** Validate RTT code at clock stop
**Check:**
1. Clock stop code exists
2. Clock stop code is 30-36 ONLY
3. Code 30 = First definitive TREATMENT
4. Code 31 = Watchful wait by PATIENT
5. Code 32 = Watchful wait by CLINICIAN
6. Code 33 = DNA first activity
7. Code 34 = Decision NOT to treat
8. Code 35 = Patient DECLINED treatment
9. Code 36 = Patient DECEASED
10. Clock stop code is LAST code in pathway
11. No code 20 after clock stop
12. No code 10-12 after clock stop

**Code 30 Specific Checks:**
13. If code 30, treatment actually given
14. If code 30, treatment date = clock stop date
15. If code 30, treatment type documented
16. If code 30, procedure code recorded (OPCS-4)
17. If code 30, treatment location valid
18. If code 30, treating consultant valid

**Code 31/32 Specific Checks:**
19. If code 31, patient chose to wait
20. If code 31, patient informed of risks
21. If code 31, review date set
22. If code 32, clinician decided to monitor
23. If code 32, monitoring plan documented
24. If code 32, review date set

**Code 33 Specific Checks:**
25. If code 33, was FIRST appointment
26. If code 33, DNA documented
27. If code 33, DNA letter sent
28. If code 33, decision made (discharge/re-offer)

**Auto-Fix:**
- Add missing clock stop code
- Change code 20 after treatment to 90
- Flag invalid clock stop codes

**Output:** Valid clock stop codes

---

#### Step 7.3: Clock Stop Sequence Validation
**What:** Validate code sequence to stop
**Check:**
1. Code sequence valid (10→20→30 or 10→20→31, etc.)
2. Clock stop code is LAST in sequence
3. No activity after clock stop (except code 90/91)
4. If code 31/32, can restart with code 11
5. If code 30, pathway complete
6. If code 33-36, pathway complete

**Auto-Fix:**
- Reorder codes chronologically
- Flag invalid sequences

**Output:** Valid code sequence

---

### PHASE 8: WAITING TIME CALCULATION

#### Step 8.1: Basic Waiting Time Calculation
**What:** Calculate total waiting time
**Formula:**
```
Waiting Time (days) = Clock Stop Date - Clock Start Date
Waiting Time (weeks) = Waiting Time (days) / 7
```

**Check:**
1. Calculation correct
2. Days calculated correctly
3. Weeks calculated correctly
4. No negative waiting times
5. Waiting time realistic (<2 years)

**Auto-Fix:**
- Recalculate if wrong
- Flag negative times

**Output:** Basic waiting time

---

#### Step 8.2: Pause Period Exclusion
**What:** Exclude pause periods from waiting time
**Exclude:**
1. Patient delays (patient cancelled/rescheduled)
2. Clinical exceptions (patient unfit)
3. Active monitoring periods (code 31/32)
4. Time between code 31/32 and code 11

**Formula:**
```
Adjusted Waiting Time = Total Time - Patient Delays - Clinical Exceptions - Active Monitoring
```

**Check:**
1. All pauses identified
2. Pause start dates valid
3. Pause end dates valid
4. Pause reasons documented
5. Pauses excluded from calculation

**Auto-Fix:**
- Identify pause periods
- Recalculate excluding pauses

**Output:** Adjusted waiting time

---

#### Step 8.3: Code 11 Restart Calculation (CRITICAL!)
**What:** Calculate waiting time for restarted clocks
**Scenario:**
```
Code 10 (01/01/2025) - Clock starts
Code 20 (15/01/2025) - Appointment
Code 31 (30/01/2025) - Patient watchful wait (Clock STOPS)
[Patient monitoring for 3 months]
Code 11 (30/04/2025) - Restart after watchful wait (Clock RESTARTS)
Code 20 (15/05/2025) - Appointment
Code 30 (30/05/2025) - Treatment (Clock STOPS)
```

**Calculation:**
```
Period 1: 30/01/2025 - 01/01/2025 = 29 days
Period 2: 30/05/2025 - 30/04/2025 = 30 days
Total Waiting Time = 29 + 30 = 59 days = 8.4 weeks
Watchful wait period (3 months) EXCLUDED
```

**Check:**
1. If code 11 exists, identify previous stop (31/32/91)
2. Calculate time before stop
3. Calculate time after restart
4. Add both periods
5. Exclude watchful wait period
6. Total waiting time correct

**Auto-Fix:**
- Recalculate with both periods
- Flag if watchful wait not excluded

**Output:** Correct waiting time for restarts

---

#### Step 8.4: Breach Status Calculation
**What:** Determine if pathway breached 18-week target
**Check:**
1. Waiting time > 18 weeks = BREACH
2. Waiting time ≤ 18 weeks = NOT BREACH
3. Breach status field correct
4. If breach, breach date calculated
5. If breach, breach reason documented
6. If breach, escalation done

**Auto-Fix:**
- Set breach status correctly
- Calculate breach date
- Flag for escalation

**Output:** Correct breach status

---

### PHASE 9: POST-TREATMENT VALIDATION

#### Step 9.1: Post-Treatment Activity Validation
**What:** Validate activity after treatment
**Check:**
1. Activity after code 30 coded as 90
2. Code 90 = After first definitive treatment
3. Follow-up appointments coded as 90
4. Emergency admissions coded as 90
5. No code 20 after code 30

**Auto-Fix:**
- Change code 20 to 90 after treatment

**Output:** Valid post-treatment codes

---

#### Step 9.2: Active Monitoring Validation
**What:** Validate activity during watchful wait
**Check:**
1. Activity during code 31/32 coded as 91
2. Code 91 = During active monitoring
3. Review appointments coded as 91
4. No code 20 during watchful wait

**Auto-Fix:**
- Change code 20 to 91 during monitoring

**Output:** Valid monitoring codes

---

#### Step 9.3: Discharge Validation
**What:** Validate discharge process
**Check:**
1. Discharge date exists
2. Discharge date after treatment
3. Discharge summary sent to GP
4. Discharge letter sent to patient
5. OP DISCHARGED DATE set
6. Follow-up plan documented
7. Pathway closed correctly

**Auto-Fix:**
- Set OP DISCHARGED DATE
- Flag missing discharge summary

**Output:** Valid discharge data

---

### PHASE 10: FINAL COMPLIANCE CHECKS

#### Step 10.1: Complete Pathway Validation
**What:** Validate entire pathway end-to-end
**Check:**
1. Complete code sequence valid
2. All dates chronological
3. All mandatory fields populated
4. No orphaned records
5. No missing data
6. Pathway outcome recorded
7. All activities accounted for
8. Timeline makes sense
9. No gaps in care
10. Audit trail complete

**Output:** Pathway compliance report

---

#### Step 10.2: National Submission Validation
**What:** Validate ready for NHS England submission
**Check:**
1. All RTT codes valid
2. All dates valid
3. Waiting time calculated correctly
4. Breach status correct
5. Data format matches national specification
6. All mandatory fields present
7. No validation errors
8. Ready for upload to NHS Digital

**Output:** Submission-ready data

---

#### Step 10.3: Trust Performance Validation
**What:** Calculate trust performance metrics
**Calculate:**
1. Total patients on PTL
2. Total patients waiting <18 weeks
3. Total patients waiting >18 weeks (breaches)
4. % patients within 18 weeks
5. Average waiting time
6. Median waiting time
7. 92nd percentile waiting time
8. Performance by specialty
9. Performance by consultant
10. Trend analysis

**Output:** Trust performance report

---

## 📊 VALIDATION SUMMARY

### Total Validation Steps: 10 PHASES
1. Pre-Validation Setup (3 steps)
2. Patient-Level Validation (3 steps)
3. Pathway-Level Validation (3 steps)
4. Clock Start Validation (3 steps)
5. Activity Validation (5 steps)
6. Waiting List Validation (4 steps)
7. Clock Stop Validation (3 steps)
8. Waiting Time Calculation (4 steps)
9. Post-Treatment Validation (3 steps)
10. Final Compliance Checks (3 steps)

**Total Sub-Steps: 34 detailed validation steps**
**Total Individual Checks: 200+ validation rules**

### Critical Code 11 Logic:
- Code 11 RESTARTS clock (not starts new clock)
- Previous code must be 31/32/91
- Waiting time = Period 1 + Period 2
- Watchful wait period EXCLUDED

---

## ✅ VERIFICATION CHECKLIST

**Can you verify I understand:**
- ✅ Code 11 restarts clock (not new clock)
- ✅ Code 11 follows 31/32/91
- ✅ Waiting time includes both periods
- ✅ Watchful wait excluded from calculation
- ✅ All 10 validation phases
- ✅ All 34 sub-steps
- ✅ 200+ individual checks
- ✅ Auto-fix logic
- ✅ NHS submission requirements
- ✅ Trust performance metrics

**This is the COMPLETE validation process!** 🚀

---

**T21 Services Limited | Company No: 13091053**  
**Complete RTT Validation Process - All Steps Documented**
