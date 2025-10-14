# 🏥 REAL NHS VALIDATION PROCESS - How It Actually Works

**Date:** October 14, 2025  
**Source:** Real NHS Data Quality Officer workflow  
**Purpose:** Document the ACTUAL validation process used in NHS

---

## 🎯 THE REAL VALIDATION PROCESS

### What Validation REALLY Means:

**NOT just checking data fields!**

**It's about:**
1. Reading clinic letters
2. Reading consultation notes
3. Reading appointment outcomes
4. Reading diagnostic test results
5. Translating all of this into correct RTT codes
6. Ensuring PAS matches reality

---

## 📋 STEP-BY-STEP REAL VALIDATION

### STEP 1: DATA COMPARISON
**What:** Compare PAS data vs Excel spreadsheet (job assignment)

**Check:**
1. ✅ PATHWAY NUMBER - Same in PAS and Excel?
2. ✅ NHS NUMBER - Same in PAS and Excel?
3. ✅ DATE OF BIRTH - Same in PAS and Excel?
4. ✅ NAME - Same in PAS and Excel?
5. ✅ ADDRESS - Same in PAS and Excel?
6. ✅ REFERRAL DATE - Same in PAS and Excel?
7. ✅ SPECIALTY - Same in PAS and Excel?
8. ✅ CONSULTANT - Same in PAS and Excel?
9. ✅ ALL DATA ACCURATE - PAS = Excel?

**If mismatch:** Flag for correction

---

### STEP 2: READ CLINIC LETTERS
**What:** Read EVERY clinic letter to understand what happened

**Example 1: Referral Received, No Appointment Yet**

**Letter says:**
```
"Dear Mr. Smith,

We have received your referral from Dr. Jones (GP) for knee pain.
Your referral has been accepted by our Orthopaedic department.

Unfortunately, we do not have any appointment slots available at this time.
You have been placed on our Partial Booking List (PBL).

We will contact you as soon as an appointment becomes available.

Yours sincerely,
Orthopaedic Department"
```

**Validation:**
- ✅ Referral received = TRUE
- ✅ Referral accepted = TRUE
- ✅ Appointment offered = NO
- ✅ Patient on PBL = YES
- ✅ **RTT CODE = 10** (First activity - referral registered)
- ✅ **EPISODE = 1** (First episode)
- ✅ Clock started = YES
- ✅ Clock ticking = YES

**Record in PAS:**
- Episode 1: Code 10, Date = referral date
- Status: On PBL, waiting for first appointment

---

**Example 2: Referral Received, Appointment Offered**

**Letter says:**
```
"Dear Mr. Smith,

We have received your referral from Dr. Jones (GP) for knee pain.
Your referral has been accepted by our Orthopaedic department.

We are pleased to offer you an appointment:
Date: 15th October 2025
Time: 10:00 AM
Location: Outpatient Clinic, Room 3

Please confirm your attendance.

Yours sincerely,
Orthopaedic Department"
```

**Validation:**
- ✅ Referral received = TRUE
- ✅ Referral accepted = TRUE
- ✅ Appointment offered = YES
- ✅ Appointment date = 15/10/2025
- ✅ **RTT CODE = 10** (First activity - referral registered)
- ✅ **EPISODE = 1** (First episode)
- ✅ Clock started = YES
- ✅ Patient status = Appointment booked

**Record in PAS:**
- Episode 1: Code 10, Date = referral date
- Status: Appointment booked for 15/10/2025

**NOTE:** Patient still on Code 10 until appointment happens!

---

### STEP 3: READ APPOINTMENT OUTCOME
**What:** Read consultation notes to see what happened at appointment

**Example 3: Patient Attended First Appointment**

**Consultation notes say:**
```
"Patient: Mr. Smith
Date: 15/10/2025
Appointment Type: New (N)

History: 6-month history of right knee pain, worse on stairs.
Examination: Tenderness over medial joint line, positive McMurray test.
Diagnosis: Suspected medial meniscus tear
Plan: Request MRI scan to confirm diagnosis
       Review in clinic after MRI results available

Outcome: Patient attended
Next steps: MRI requested, await results

Dr. Williams, Consultant Orthopaedic Surgeon"
```

**Validation:**
- ✅ Patient attended = YES
- ✅ Appointment type = N (New)
- ✅ Consultation happened = YES
- ✅ Outcome = Further investigation needed (MRI)
- ✅ **RTT CODE = 20** (Subsequent activity)
- ✅ **EPISODE = 2** (Second episode)
- ✅ Clock still ticking = YES (diagnostic test doesn't stop clock!)
- ✅ Next step = MRI scan

**Record in PAS:**
- Episode 1: Code 10, Date = referral date
- Episode 2: Code 20, Date = 15/10/2025 (first appointment attended)
- Status: Awaiting MRI scan

---

### STEP 4: READ DIAGNOSTIC TEST RESULTS
**What:** Check diagnostic test was done and results available

**Example 4: MRI Scan Completed**

**Radiology report says:**
```
"Patient: Mr. Smith
Date: 25/10/2025
Test: MRI Right Knee

Findings: Complex tear of medial meniscus with displaced fragment.
          No other significant abnormality.

Conclusion: Medial meniscus tear requiring surgical intervention.

Dr. Brown, Consultant Radiologist"
```

**Validation:**
- ✅ MRI completed = YES
- ✅ MRI date = 25/10/2025
- ✅ Results available = YES
- ✅ Diagnosis confirmed = Meniscus tear
- ✅ **RTT CODE = 20** (Subsequent activity - diagnostic test)
- ✅ **EPISODE = 3** (Third episode)
- ✅ Clock still ticking = YES (diagnostic doesn't stop clock!)
- ✅ Next step = Review results with consultant

**Record in PAS:**
- Episode 1: Code 10, Date = referral date
- Episode 2: Code 20, Date = 15/10/2025 (first appointment)
- Episode 3: Code 20, Date = 25/10/2025 (MRI scan)
- Status: MRI completed, awaiting review

---

### STEP 5: READ FOLLOW-UP CONSULTATION
**What:** Read notes from follow-up appointment

**Example 5: Results Discussed, Treatment Planned**

**Consultation notes say:**
```
"Patient: Mr. Smith
Date: 05/11/2025
Appointment Type: Follow-up (F)

MRI Results: Confirmed medial meniscus tear with displaced fragment.

Discussion: Discussed surgical options with patient.
            Explained arthroscopic meniscectomy procedure.
            Patient wishes to proceed with surgery.

Plan: Add patient to waiting list for arthroscopic meniscectomy.
      Target date: Within 6 weeks.
      Pre-operative assessment to be arranged.

Outcome: Patient consented to surgery
Next steps: Add to surgical waiting list

Dr. Williams, Consultant Orthopaedic Surgeon"
```

**Validation:**
- ✅ Follow-up attended = YES
- ✅ Results discussed = YES
- ✅ Treatment decided = Surgery
- ✅ Patient consented = YES
- ✅ **RTT CODE = 20** (Subsequent activity)
- ✅ **EPISODE = 4** (Fourth episode)
- ✅ Clock still ticking = YES (treatment not yet given!)
- ✅ Next step = Surgery

**Record in PAS:**
- Episode 1: Code 10, Date = referral date
- Episode 2: Code 20, Date = 15/10/2025 (first appointment)
- Episode 3: Code 20, Date = 25/10/2025 (MRI scan)
- Episode 4: Code 20, Date = 05/11/2025 (follow-up, surgery planned)
- Status: On surgical waiting list (WL)
- TCI DATE: Target within 6 weeks

---

### STEP 6: READ PRE-OPERATIVE ASSESSMENT
**What:** Check pre-op assessment completed

**Example 6: Pre-Op Assessment Done**

**Pre-op notes say:**
```
"Patient: Mr. Smith
Date: 15/11/2025

Pre-operative Assessment:
- Blood pressure: 130/80 (acceptable)
- ECG: Normal sinus rhythm
- Blood tests: All within normal limits
- MRSA screening: Negative
- Fitness for anaesthesia: ASA Grade 1 (healthy)

Outcome: Fit for surgery under general anaesthetic
Consent: Signed and dated

Nurse Practitioner: J. Taylor"
```

**Validation:**
- ✅ Pre-op assessment done = YES
- ✅ Fit for surgery = YES
- ✅ Consent signed = YES
- ✅ **RTT CODE = 20** (Subsequent activity)
- ✅ **EPISODE = 5** (Fifth episode)
- ✅ Clock still ticking = YES (treatment not yet given!)
- ✅ Ready for surgery = YES

**Record in PAS:**
- Episode 1: Code 10, Date = referral date
- Episode 2: Code 20, Date = 15/10/2025 (first appointment)
- Episode 3: Code 20, Date = 25/10/2025 (MRI scan)
- Episode 4: Code 20, Date = 05/11/2025 (follow-up)
- Episode 5: Code 20, Date = 15/11/2025 (pre-op assessment)
- Status: Ready for surgery, awaiting date

---

### STEP 7: READ OPERATION NOTES
**What:** Check surgery was performed (FIRST DEFINITIVE TREATMENT!)

**Example 7: Surgery Performed**

**Operation notes say:**
```
"Patient: Mr. Smith
Date: 25/11/2025
Procedure: Arthroscopic meniscectomy, right knee

Operation: Under general anaesthetic, arthroscopy performed.
           Medial meniscus tear identified and debrided.
           Displaced fragment removed.
           Joint irrigated and closed.

Outcome: Procedure successful, no complications.
         Patient recovered well from anaesthetic.
         Discharged same day with physiotherapy referral.

Post-op plan: Physiotherapy for 6 weeks
              Review in clinic in 8 weeks

Mr. Williams, Consultant Orthopaedic Surgeon"
```

**Validation:**
- ✅ Surgery performed = YES
- ✅ Surgery date = 25/11/2025
- ✅ This is FIRST DEFINITIVE TREATMENT = YES
- ✅ **RTT CODE = 30** (First definitive treatment - CLOCK STOPS!)
- ✅ **EPISODE = 6** (Sixth episode - FINAL)
- ✅ Clock stopped = YES
- ✅ RTT pathway complete = YES

**Record in PAS:**
- Episode 1: Code 10, Date = referral date (e.g., 01/09/2025)
- Episode 2: Code 20, Date = 15/10/2025 (first appointment)
- Episode 3: Code 20, Date = 25/10/2025 (MRI scan)
- Episode 4: Code 20, Date = 05/11/2025 (follow-up)
- Episode 5: Code 20, Date = 15/11/2025 (pre-op assessment)
- Episode 6: Code 30, Date = 25/11/2025 (SURGERY - CLOCK STOPS!)

**Waiting Time Calculation:**
- Clock start: 01/09/2025
- Clock stop: 25/11/2025
- Total waiting time: 85 days = 12.1 weeks
- Within 18 weeks: YES ✅
- Breach: NO ✅

---

## 🔍 WHAT VALIDATOR MUST DO

### For EACH Patient:

**1. Read ALL Documents:**
- Referral letter
- Acceptance letter
- Appointment letters
- Consultation notes
- Diagnostic test requests
- Diagnostic test results
- Follow-up notes
- Pre-op assessment
- Operation notes
- Discharge summary

**2. Extract Key Information:**
- What happened?
- When did it happen?
- What was the outcome?
- What's the next step?

**3. Translate to RTT Codes:**
- Referral received = Code 10
- Appointment attended = Code 20
- Diagnostic test = Code 20
- Follow-up = Code 20
- Pre-op = Code 20
- Surgery/Treatment = Code 30

**4. Create Episodes:**
- Each event = New episode
- Each episode = RTT code + date
- Episodes in chronological order

**5. Verify in PAS:**
- Check PAS has correct codes
- Check PAS has correct dates
- Check episodes match reality
- Check waiting time calculated correctly

**6. Check Against Excel:**
- Verify all data matches
- Verify codes correct
- Verify dates correct
- Verify no missing episodes

---

## 🤖 WHAT AI MUST DO

### AI Must Read and Understand:

**1. Clinic Letters (NLP):**
- Extract: "referral received and accepted"
- Translate to: Code 10
- Extract: "appointment offered"
- Extract: appointment date

**2. Consultation Notes (NLP):**
- Extract: "patient attended"
- Translate to: Code 20
- Extract: consultation outcome
- Extract: next steps

**3. Diagnostic Reports (NLP):**
- Extract: test type (MRI/CT/X-ray)
- Extract: test date
- Translate to: Code 20
- Extract: results
- Extract: diagnosis

**4. Operation Notes (NLP):**
- Extract: "surgery performed"
- Extract: procedure name
- Extract: surgery date
- Translate to: Code 30 (CLOCK STOPS!)

**5. Outcome Letters (NLP):**
- Extract: "patient declined treatment"
- Translate to: Code 35
- Extract: "patient DNA"
- Translate to: Code 33
- Extract: "watchful wait"
- Translate to: Code 31/32

### AI Must Then:

**6. Create Episode Timeline:**
```
Episode 1: Code 10, 01/09/2025 (referral)
Episode 2: Code 20, 15/10/2025 (first appointment)
Episode 3: Code 20, 25/10/2025 (MRI)
Episode 4: Code 20, 05/11/2025 (follow-up)
Episode 5: Code 20, 15/11/2025 (pre-op)
Episode 6: Code 30, 25/11/2025 (surgery)
```

**7. Validate Against PAS:**
- Does PAS have all 6 episodes?
- Are codes correct?
- Are dates correct?
- Is waiting time correct?

**8. Auto-Fix Errors:**
- Missing episode → Add it
- Wrong code → Correct it
- Wrong date → Fix it
- Missing Code 30 → Add it

**9. Generate Report:**
- List all errors found
- Show what was fixed
- Flag items needing review

---

## ✅ REAL VALIDATION CHECKLIST

For EACH patient, validator must:

1. ✅ Read referral letter
2. ✅ Confirm Code 10 recorded
3. ✅ Read appointment letters
4. ✅ Read consultation notes
5. ✅ Confirm Code 20 for each appointment
6. ✅ Read diagnostic test requests
7. ✅ Confirm diagnostic tests done
8. ✅ Confirm Code 20 for each test
9. ✅ Read follow-up notes
10. ✅ Confirm Code 20 for each follow-up
11. ✅ Read operation notes (if surgery)
12. ✅ Confirm Code 30 recorded
13. ✅ Check all episodes in PAS
14. ✅ Check all dates correct
15. ✅ Check waiting time calculated correctly
16. ✅ Check breach status correct
17. ✅ Compare PAS vs Excel
18. ✅ Flag any discrepancies

**This is REAL validation!** Not just checking data fields!

---

## 💡 WHY THIS IS HARD

**Manual validation takes 40 hours/month because:**
- Must read 100s of letters per patient
- Must understand medical terminology
- Must translate outcomes to codes
- Must check every episode
- Must verify every date
- Must calculate waiting times
- Must check against PAS
- Must check against Excel
- Must fix errors manually

**AI can do this in 30 seconds because:**
- NLP reads all letters instantly
- AI understands medical terminology
- AI translates outcomes to codes automatically
- AI checks all episodes simultaneously
- AI verifies all dates instantly
- AI calculates waiting times automatically
- AI compares PAS vs Excel instantly
- AI auto-fixes errors

---

## 🎯 SUMMARY

**Real Validation Process:**
1. Read clinic letters
2. Read consultation notes
3. Read diagnostic results
4. Read operation notes
5. Extract what happened
6. Translate to RTT codes
7. Create episodes
8. Verify in PAS
9. Check against Excel
10. Fix errors

**Each patient has multiple episodes**
**Each episode = RTT code + date**
**Validator must read ALL documents to code correctly**

**This is what TRUE AI validation must do!** 🚀

---

**T21 Services Limited | Company No: 13091053**  
**Real NHS Validation Process - How It Actually Works**
