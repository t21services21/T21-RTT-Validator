"""
COMPREHENSIVE LEARNING SYSTEM
Use ALL existing platform data to create structured learning path

LEARNING BEFORE TESTING!
Students must LEARN first, then practice, then test.

Content Sources:
1. Training Library (38 scenarios)
2. Interactive quizzes
3. RTT code definitions
4. AI Tutor
5. Video library
6. Materials uploaded by teachers
7. Certification questions (for practice)
8. Information Governance module
"""

import streamlit as st
from training_library import get_all_scenarios
from datetime import datetime
import json

# ============================================
# LEARNING MODULES STRUCTURE
# ============================================

LEARNING_MODULES = {
    "module_1": {
        "title": "RTT Fundamentals",
        "duration": "Week 1-2",
        "order": 1,
        "lessons": [
            {
                "lesson_id": "1.1",
                "title": "What is RTT?",
                "type": "theory",
                "content": """
# What is RTT (Referral to Treatment)?

## Introduction
RTT stands for **Referral to Treatment** - it's the NHS system for tracking how long patients wait from their GP referral to receiving treatment.

## The 18-Week Target
- 92% of patients must receive treatment within **18 weeks** (126 days)
- This is a legal NHS requirement
- Trusts can be fined for breaches

## Why RTT Matters
1. **Patient Care**: Faster treatment = better outcomes
2. **Performance**: NHS monitors Trust performance
3. **Funding**: Affects Trust funding and ratings
4. **Legal**: Patients have right to treatment within 18 weeks

## Key Terms
- **Pathway**: Patient's journey from referral to treatment
- **Clock Start**: When 18-week countdown begins (usually GP referral)
- **Clock Stop**: When countdown ends (usually first treatment)
- **Breach**: When treatment takes longer than 18 weeks

## Your Role as RTT Administrator
- Track patient pathways
- Ensure patients get treatment on time
- Use correct RTT codes
- Prevent breaches
- Report to NHS
                """,
                "duration": "30 mins",
                "quiz_questions": [
                    {
                        "question": "What does RTT stand for?",
                        "options": [
                            "Referral to Treatment",
                            "Ready to Treat",
                            "Return to Therapy",
                            "Rapid Treatment Track"
                        ],
                        "correct": 0,
                        "explanation": "RTT stands for Referral to Treatment - the NHS system for tracking patient waiting times."
                    },
                    {
                        "question": "What is the 18-week RTT target?",
                        "options": [
                            "All patients must be treated in 18 weeks",
                            "92% of patients treated within 18 weeks",
                            "50% of patients treated within 18 weeks",
                            "18 weeks from diagnosis to treatment"
                        ],
                        "correct": 1,
                        "explanation": "The target is 92% of patients must receive first definitive treatment within 18 weeks of referral."
                    },
                    {
                        "question": "How many days is 18 weeks?",
                        "options": ["90 days", "100 days", "126 days", "180 days"],
                        "correct": 2,
                        "explanation": "18 weeks = 126 days. This is the maximum wait time for 92% of patients."
                    }
                ]
            },
            {
                "lesson_id": "1.2",
                "title": "RTT Codes Overview",
                "type": "theory",
                "content": """
# RTT Codes Overview

## What are RTT Codes?
RTT codes are numbers (10-98) used to track patient pathway events in the NHS Patient Administration System (PAS).

## Three Types of Codes

### 1. CLOCK START CODES
These **START** the 18-week countdown:
- **Code 10**: GP Referral (most common)
- **Code 11**: After Watchful Wait
- **Code 12**: Consultant Referral (new condition)

### 2. CLOCK CONTINUE CODES
Clock keeps **TICKING**:
- **Code 20**: Subsequent appointments, diagnostics
- **Code 21**: Tertiary referral

### 3. CLOCK STOP CODES
These **STOP** the countdown:
- **Code 30**: First Definitive Treatment ✅ (TARGET!)
- **Code 31**: Patient Declined Treatment
- **Code 32**: Clinician Watchful Wait
- **Code 33**: Patient DNA (Did Not Attend) 1st appointment
- **Code 34**: Decision Not to Treat
- **Code 35**: Patient Declines Treatment
- **Code 36**: Patient Deceased

## The Pathway Flow

```
GP Referral
   ↓
Code 10 (CLOCK STARTS) ⏰
   ↓
Outpatient Appointment
   ↓
Code 20 (CLOCK CONTINUES) ⏰
   ↓
Diagnostic Tests
   ↓
Code 20 (CLOCK CONTINUES) ⏰
   ↓
Treatment Given
   ↓
Code 30 (CLOCK STOPS) ⏱️ DONE!
```

## Why Codes Matter
- Track patient journey
- Calculate waiting times
- Report to NHS
- Identify breaches
- Audit compliance
                """,
                "duration": "45 mins",
                "practice_scenarios": ["scenario_1", "scenario_2", "scenario_3"]
            },
            {
                "lesson_id": "1.3",
                "title": "Understanding the Clock",
                "type": "theory",
                "content": """
# Understanding the RTT Clock

## When Does the Clock Start? ⏰

The clock STARTS when:
1. **GP sends referral** (Code 10)
2. **Patient ready after watchful wait** (Code 11)
3. **Consultant refers for NEW condition** (Code 12)

### IMPORTANT: Clock starts on the DATE the GP wrote the referral, NOT when the hospital receives it!

Example:
- GP writes referral: 01/03/2024
- Hospital receives it: 05/03/2024
- **Clock starts: 01/03/2024** ✅

## When Does the Clock Stop? ⏱️

The clock STOPS when:
1. **First definitive treatment given** (Code 30) - This is the goal!
2. **Patient declines treatment** (Code 31 or 35)
3. **Clinician decides to monitor** (Code 32)
4. **Patient DNA 1st appointment** (Code 33)
5. **Decision not to treat** (Code 34)
6. **Patient deceased** (Code 36)

## When Does the Clock Continue? ⏰

The clock KEEPS TICKING during:
- Diagnostic tests (Code 20)
- Follow-up appointments (Code 20)
- Adding to waiting list (Code 20)
- Referral to specialist center (Code 21)

## Calculating Wait Time

**Example Pathway:**
- Referral: 01/03/2024 (Code 10)
- Outpatient: 15/03/2024 (Code 20)
- CT Scan: 22/03/2024 (Code 20)
- Surgery: 15/05/2024 (Code 30)

**Wait Time**: 01/03/2024 to 15/05/2024 = **75 days** ✅ (within 126 days)

## What is a Breach? ⚠️

A breach occurs when:
- Patient doesn't receive treatment within 126 days (18 weeks)
- Example: Referral 01/01/2024, Treatment 10/06/2024 = 161 days ❌ BREACH

**Consequences:**
- Trust fined (£10,000+ per breach)
- Poor performance ratings
- Patient dissatisfaction
                """,
                "duration": "45 mins"
            }
        ]
    },
    
    "module_2": {
        "title": "RTT Codes Deep Dive",
        "duration": "Week 3-4",
        "order": 2,
        "lessons": [
            {
                "lesson_id": "2.1",
                "title": "Code 10: The Referral",
                "type": "detailed",
                "content": """
# Code 10: First Activity After Referral in RTT

## What is Code 10?
The most common RTT code! Used when a GP refers a patient to hospital.

## When to Use Code 10
- GP referral letter received
- Dentist referral received
- First outpatient appointment for new pathway
- Starting a new patient journey

## Key Rules
1. Clock starts on **GP letter date**, not hospital receipt date
2. Only use for **NEW** referrals
3. Starts the 18-week countdown
4. One Code 10 per pathway

## Real Example
**Scenario:**
GP Dr. Smith writes referral on 15/03/2024 for patient with knee pain. Hospital receives letter on 20/03/2024.

**Correct Action:**
- RTT Code: 10
- Clock Start Date: 15/03/2024 (GP letter date)
- Comment: "RTT - 10 - 15/03/24 - Referral from GP Dr Smith - Knee pain"

## Common Mistakes ❌
1. Using hospital receipt date instead of GP letter date
2. Using Code 10 for follow-up appointments (should be Code 20)
3. Using Code 10 when patient already on pathway

## Practice Makes Perfect
You'll now practice Code 10 with real scenarios!
                """,
                "practice_scenarios": ["scenario_1", "scenario_2", "scenario_4", "scenario_7"],
                "quiz_questions": [
                    {
                        "question": "When does the RTT clock start for Code 10?",
                        "options": [
                            "Date hospital receives referral",
                            "Date GP writes referral letter",
                            "Date patient first attends",
                            "Date referral is entered in PAS"
                        ],
                        "correct": 1,
                        "explanation": "Clock ALWAYS starts on the date the GP wrote the referral letter, NOT when hospital receives it. This is a common mistake!"
                    },
                    {
                        "question": "A patient attends follow-up appointment. Which code?",
                        "options": ["Code 10", "Code 20", "Code 30", "Code 90"],
                        "correct": 1,
                        "explanation": "Code 10 is ONLY for NEW referrals. Follow-up appointments use Code 20."
                    }
                ]
            },
            {
                "lesson_id": "2.2",
                "title": "Code 20: Continuing the Journey",
                "type": "detailed",
                "content": """
# Code 20: Subsequent Consultant/Diagnostic Tests

## What is Code 20?
The MOST USED RTT code! Used for everything between referral and treatment.

## When to Use Code 20
- Follow-up outpatient appointments
- Diagnostic tests (X-ray, MRI, CT, blood tests)
- Adding patient to waiting list
- Pre-operative assessment
- Consultant review
- Any activity AFTER Code 10 and BEFORE Code 30

## Clock Effect
⏰ **CONTINUES** - Clock keeps ticking!

## Real Examples

**Example 1: Diagnostic Test**
- Patient referred (Code 10)
- MRI scan ordered (Code 20)
- Clock continues

**Example 2: Follow-up**
- Patient seen in clinic (Code 20)
- Review results (Code 20)
- Clock continues

**Example 3: Waiting List**
- Patient added to surgical waiting list (Code 20)
- Clock continues

## Key Rule
Use Code 20 for EVERYTHING between referral (Code 10) and treatment (Code 30).

## Common Mistakes ❌
1. Forgetting to use Code 20 for diagnostics
2. Thinking waiting list = clock stops (NO! Clock continues)
3. Using Code 30 for pre-op assessment (should be Code 20)

## Commenting Examples
- RTT - 20 - 15/04/24 - Outpatient appointment attended
- RTT - 20 - 22/04/24 - MRI scan performed
- RTT - 20 - 30/04/24 - Added to surgical waiting list
                """,
                "practice_scenarios": ["scenario_5", "scenario_6", "scenario_8"],
                "quiz_questions": [
                    {
                        "question": "Patient has MRI scan. Which code?",
                        "options": ["Code 10", "Code 20", "Code 30", "Code 92"],
                        "correct": 1,
                        "explanation": "Diagnostic tests = Code 20. Clock continues while awaiting results."
                    }
                ]
            },
            {
                "lesson_id": "2.3",
                "title": "Code 30: First Treatment (The Goal!)",
                "type": "detailed",
                "content": """
# Code 30: Start First Definitive Treatment

## What is Code 30?
🎯 **THE TARGET CODE!** This is what we aim for within 18 weeks!

## What is "Definitive Treatment"?
Treatment intended to **manage the patient's disease, condition or injury**.

## Examples of Code 30
✅ Surgery performed
✅ Injection given (therapeutic)
✅ Cryotherapy
✅ Chemotherapy starts
✅ Radiotherapy starts
✅ Physiotherapy starts (if definitive treatment)

## NOT Code 30 (Common Mistakes)
❌ Diagnostic injection (Code 20)
❌ Pre-operative assessment (Code 20)
❌ Follow-up after treatment (Code 90)
❌ Watchful waiting (Code 31 or 32)

## Clock Effect
⏰ **STOPS** - 18-week target achieved!

## Real Example
**Pathway:**
- 01/03/24: GP Referral (Code 10) ⏰ START
- 15/03/24: Outpatient (Code 20) ⏰ continues
- 22/03/24: MRI Scan (Code 20) ⏰ continues
- 10/05/24: Surgery (Code 30) ⏱️ STOP

**Wait Time**: 70 days ✅ (within 126 days)

## Why It Matters
- THIS is the 18-week target
- Must achieve within 126 days
- Prevents breach
- Patient gets treatment!

## Commenting Example
- RTT - 30 - 10/05/24 - Definitive treatment - Knee arthroscopy performed
                """,
                "practice_scenarios": ["scenario_9", "scenario_10", "scenario_11"],
                "quiz_questions": [
                    {
                        "question": "Patient has pre-operative assessment. Which code?",
                        "options": ["Code 10", "Code 20", "Code 30", "Code 90"],
                        "correct": 1,
                        "explanation": "Pre-op assessment is NOT treatment! It's preparation. Use Code 20. Clock continues."
                    }
                ]
            },
            {
                "lesson_id": "2.4",
                "title": "DNA & Decline Codes (31-36)",
                "type": "detailed",
                "content": """
# DNA & Patient Decline Codes

## Code 31: Patient Declined Treatment (Watchful Wait)
**When**: Patient wants to WAIT and see how condition develops

**Examples:**
- Patient thinking about surgery
- Patient wants to try physiotherapy first
- Patient not ready for treatment

**Clock Effect**: ⏱️ STOPS (PAUSE)
**Can Restart**: YES - with Code 11

## Code 32: Clinician Watchful Wait (Active Monitoring)
**When**: CLINICIAN decides to monitor, no immediate treatment needed

**Examples:**
- Watch and wait approach
- Active surveillance
- Monitor condition over time

**Clock Effect**: ⏱️ STOPS (PAUSE)
**Can Restart**: YES - with Code 11

## Code 33: Patient DNA First Activity
**When**: Patient doesn't attend FIRST appointment

**IMPORTANT**: Only for FIRST appointment!

**Clock Effect**: ⏱️ STOPS
**Note**: If DNA at follow-up = Code 20, clock continues!

## Code 34: Decision Not to Treat
**When**: Clinical decision - NO treatment needed

**Examples:**
- Nothing wrong found
- Problem resolved naturally
- Discharge to GP

**Clock Effect**: ⏱️ STOPS (FINAL)

## Code 35: Patient Declines Treatment
**When**: Patient REFUSES treatment offered

**Examples:**
- Patient says no to surgery
- Patient refuses intervention
- Patient's choice

**Clock Effect**: ⏱️ STOPS

## Code 36: Patient Deceased
**When**: Patient has died

**Clock Effect**: ⏱️ STOPS (FINAL)

## Key Differences
**Code 31 vs 32**: WHO decided to wait (patient vs clinician)
**Code 31/32 vs 33**: Can restart (11) vs Cannot
**Code 33**: FIRST appointment DNA only
**Code 34 vs 35**: Clinical decision vs Patient decision
                """,
                "practice_scenarios": ["scenario_12", "scenario_13", "scenario_14"]
            }
        ]
    },
    
    "module_3": {
        "title": "Advanced RTT & Practical NHS Training",
        "duration": "Week 5-6",
        "order": 3,
        "lessons": [
            {
                "lesson_id": "3.1",
                "title": "Multiple Pathways & Complex Cases",
                "type": "advanced",
                "content": """
# Multiple Pathways & Complex Cases

## Can One Patient Have Multiple RTT Pathways?
✅ **YES!** Absolutely!

## Key Rule
**One pathway per CONDITION**

## Example
**Patient: Mr. Jones**

**Pathway 1 - Orthopaedics (Knee)**
- 01/03/24: GP referral for knee pain (Code 10)
- Clock running...
- Waiting for surgery

**Pathway 2 - Ophthalmology (Cataract)**
- 15/03/24: GP referral for cataracts (Code 10)
- Clock running...
- Different condition = Different pathway

**Result**: TWO separate pathways, TWO separate clocks!

## Important Points
1. Each pathway tracked independently
2. Each has own RTT codes
3. Each has own 18-week target
4. Treatment for one doesn't affect the other

## Complex Scenario
**Patient has:**
- Knee replacement pathway (Ortho)
- Cataract surgery pathway (Opthal)
- Diabetes monitoring (NOT RTT - Code 91)

**How many RTT pathways?** TWO (knee and cataract)
**Diabetes?** Not RTT because active monitoring

## When Pathways Interact
**Scenario**: Patient needs knee surgery but has heart condition

**Solution**:
- Knee pathway continues (Code 20)
- May need cardiology clearance
- Still same knee pathway
- Heart is EXISTING condition
                """,
                "practice_scenarios": ["scenario_20", "scenario_21"]
            },
            {
                "lesson_id": "3.2",
                "title": "PRACTICAL: Patient Registration & Pathways",
                "type": "hands-on",
                "content": """
# 🏥 HANDS-ON PRACTICAL: Patient Administration

## Welcome to Real NHS Practice!
Now you'll learn by DOING! This is hands-on NHS administration training.

## What You'll Practice
✅ Register new patients
✅ Create RTT pathways
✅ Manage patient episodes
✅ Update patient records
✅ Search patient database
✅ Handle waiting lists

## Where to Practice
Go to: **Patient Administration Hub** (in sidebar)

## Step-by-Step Practice

### Task 1: Register Your First Patient
1. Click "Patient Administration Hub"
2. Go to "Patient Registration" tab
3. Fill in patient details:
   - NHS Number (e.g., 123 456 7890)
   - Name, DOB, Address
   - GP details
4. Click "Register Patient"
5. ✅ Patient created!

### Task 2: Create RTT Pathway
1. Go to "Pathway Management" tab
2. Select your patient
3. Create new pathway:
   - Specialty: Orthopaedics
   - Referral Date: Today
   - Referral Source: GP
4. Click "Create Pathway"
5. ✅ Pathway created with Code 10!

### Task 3: Add Episode (Code 20)
1. Go to "Episode Management" tab
2. Select your patient's pathway
3. Add new episode:
   - Type: Outpatient Appointment
   - Date: Today
   - RTT Code: 20
   - Comment: "RTT - 20 - [date] - Outpatient attended"
4. Click "Add Episode"
5. ✅ Clock continues!

### Task 4: Add to Waiting List
1. Go to "Waiting List Management" tab
2. Add patient to list:
   - Procedure: Knee surgery
   - Priority: Routine
   - Target date: Calculate 18 weeks from referral
3. Click "Add to Waiting List"
4. ✅ Patient tracked!

## Practice Goals
✅ Register 3 different patients
✅ Create 3 pathways (different specialties)
✅ Add 5 episodes (different codes)
✅ Manage waiting list

## Real NHS Skills
This is EXACTLY what NHS RTT Administrators do daily!
                """,
                "practical_module": "Patient Administration Hub",
                "duration": "2 hours hands-on"
            },
            {
                "lesson_id": "3.3",
                "title": "PRACTICAL: PTL & Breach Management",
                "type": "hands-on",
                "content": """
# 🏥 HANDS-ON PRACTICAL: Patient Tracking List (PTL)

## Real NHS Breach Prevention!
Learn to manage PTL just like NHS RTT Coordinators!

## What is PTL?
The Patient Tracking List shows ALL patients waiting for treatment.
Your job: Make sure NONE breach the 18-week target!

## Where to Practice
Go to: **Clinical Workflows → PTL** (in sidebar)

## Step-by-Step Practice

### Task 1: Add Patients to PTL
1. Click "Clinical Workflows"
2. Go to "PTL" tab
3. Click "Add Patient" tab
4. Add 5 patients with different wait times:
   - Patient 1: Referred 2 weeks ago
   - Patient 2: Referred 10 weeks ago (getting close!)
   - Patient 3: Referred 16 weeks ago (HIGH RISK!)
   - Patient 4: Referred 17 weeks ago (CRITICAL!)
   - Patient 5: Referred 1 week ago
5. Save each patient

### Task 2: Monitor Breach Risk
1. Go to "PTL Dashboard" tab
2. Look at the color coding:
   - 🟢 GREEN: Safe (0-12 weeks)
   - 🟡 YELLOW: Monitor (13-16 weeks)
   - 🟠 ORANGE: High risk (17 weeks)
   - 🔴 RED: Critical (18+ weeks)
3. Identify patients at risk
4. Filter by "High Risk"
5. See who needs urgent action!

### Task 3: Prevent Breaches
For patients at 16+ weeks:
1. Click on high-risk patient
2. Review pathway
3. Actions:
   - Book appointment ASAP
   - Escalate to manager
   - Contact patient
   - Document action taken
4. Update status
5. Move to "Active" or "Booked"

### Task 4: Use AI Breach Predictor
1. Go to "AI Insights" tab
2. See AI predictions:
   - "Patient X will breach in 2 weeks"
   - "High DNA risk for Patient Y"
   - "Capacity issue in Orthopaedics"
3. Take preventive action!
4. Check AI recommendations

### Task 5: Generate Reports
1. Go to "Export & Reports" tab
2. Generate PTL report:
   - All patients
   - Breach risk summary
   - By specialty
3. Download CSV
4. Review in Excel

## Practice Goals
✅ Add 10 patients to PTL
✅ Identify high-risk patients
✅ Book 3 urgent appointments
✅ Prevent 2 breaches
✅ Generate weekly report

## Real NHS Impact
This saves the NHS millions! You're learning critical skills!
                """,
                "practical_module": "Clinical Workflows - PTL",
                "duration": "2 hours hands-on"
            },
            {
                "lesson_id": "3.4",
                "title": "PRACTICAL: Appointments & Booking",
                "type": "hands-on",
                "content": """
# 🏥 HANDS-ON PRACTICAL: NHS Appointment Booking

## Real Appointment System!
Learn to book appointments just like NHS booking clerks!

## Where to Practice
Go to: **Clinical Workflows → Booking** (in sidebar)

## Step-by-Step Practice

### Task 1: Book Outpatient Appointment
1. Click "Clinical Workflows"
2. Go to "Booking" tab
3. Search for patient (use one you created)
4. Select appointment type: Outpatient
5. Choose:
   - Clinic: Orthopaedics
   - Date: Within 2 weeks
   - Time: 10:00 AM
   - Duration: 30 mins
6. Click "Book Appointment"
7. ✅ Appointment confirmed!

### Task 2: Book Diagnostic Test
1. Select patient
2. Book MRI scan:
   - Department: Radiology
   - Test: MRI Knee
   - Priority: Routine
   - Date: Next available
3. Send confirmation to patient
4. Add to pathway (Code 20)

### Task 3: Book Surgery (Code 30!)
1. Select patient on waiting list
2. Book theatre slot:
   - Procedure: Knee arthroscopy
   - Surgeon: Select from list
   - Date: Within 18 weeks!
   - Theatre: Main Theatre 2
3. Pre-op assessment date
4. Confirm with patient
5. Add to pathway (Code 30 - when done!)

### Task 4: Handle DNA (Did Not Attend)
1. Patient doesn't attend appointment
2. Mark as DNA in system
3. Check: Is this FIRST appointment?
   - YES = Code 33 (clock stops)
   - NO = Code 20 (clock continues)
4. Rebook appointment
5. Contact patient
6. Document reason

### Task 5: Manage Cancellations
1. Patient calls to cancel
2. Cancel appointment in system
3. Rebook immediately:
   - Offer next available
   - Prioritize if near breach
4. Update pathway notes
5. Free slot for another patient

## Practice Goals
✅ Book 5 outpatient appointments
✅ Book 2 diagnostic tests
✅ Book 1 surgical procedure
✅ Handle 2 DNAs correctly
✅ Manage 3 cancellations

## Real NHS Skills
Booking is CRITICAL for meeting RTT targets!
                """,
                "practical_module": "Clinical Workflows - Booking",
                "duration": "2 hours hands-on"
            },
            {
                "lesson_id": "3.5",
                "title": "PRACTICAL: Cancer Pathways (2WW)",
                "type": "hands-on",
                "content": """
# 🏥 HANDS-ON PRACTICAL: Urgent Cancer Pathways

## 2-Week Wait (2WW) Practice
Urgent cancer referrals - patient MUST be seen within 14 days!

## Where to Practice
Go to: **Clinical Workflows → Cancer** (in sidebar)

## Critical Rules
⚠️ 2WW = Patient seen within 14 days
⚠️ 62-day = Treatment within 62 days
⚠️ These are URGENT - highest priority!

## Step-by-Step Practice

### Task 1: Receive 2WW Referral
1. Click "Clinical Workflows"
2. Go to "Cancer" tab
3. Add urgent referral:
   - Referral type: 2-Week Wait
   - Suspected cancer: Breast
   - Referral date: Today
   - RTT Code: 10 (but flagged URGENT!)
4. System alerts: "BOOK WITHIN 14 DAYS!"

### Task 2: Book Urgent Appointment
1. Check 2WW calendar
2. Find slot within 14 days
3. Book:
   - Clinic: Breast Surgery
   - Date: Within 14 days
   - Consultant: Specialist
4. Send urgent confirmation
5. Flag in system: "2WW"

### Task 3: Track 62-Day Pathway
1. Patient seen (2WW target met ✅)
2. Needs biopsy (urgent)
3. Book diagnostic within 7 days
4. Result: Confirm cancer
5. Book treatment within 62 days total
6. Monitor countdown: 62 days from referral

### Task 4: Prioritize Over Routine
1. 2WW patient needs slot
2. Clinic full with routine patients
3. Action: BUMP routine patient
4. Rebook routine patient later
5. Give slot to 2WW
6. 2WW = PRIORITY ALWAYS!

## Practice Goals
✅ Handle 3 2WW referrals
✅ Book all within 14 days
✅ Track 62-day pathway
✅ Prioritize correctly
✅ Meet cancer targets

## Real NHS Impact
2WW saves lives! This is critical healthcare!
                """,
                "practical_module": "Clinical Workflows - Cancer",
                "duration": "1.5 hours hands-on"
            },
            {
                "lesson_id": "3.6",
                "title": "PRACTICAL: MDT Coordination",
                "type": "hands-on",
                "content": """
# 🏥 HANDS-ON PRACTICAL: Multi-Disciplinary Team (MDT)

## Real MDT Meeting Coordination
Learn to coordinate MDT meetings for complex cases!

## What is MDT?
Team of specialists discuss complex patients together:
- Surgeon
- Oncologist
- Radiologist
- Pathologist
- Nurse specialist

## Where to Practice
Go to: **Clinical Workflows → MDT** (in sidebar)

## Step-by-Step Practice

### Task 1: Schedule MDT Meeting
1. Click "Clinical Workflows"
2. Go to "MDT" tab
3. Create new meeting:
   - Date: Next week
   - Time: 2:00 PM
   - Duration: 2 hours
   - Attendees: Select team
4. Send invitations
5. Book meeting room

### Task 2: Add Patients to MDT List
1. Select MDT meeting
2. Add complex patients:
   - Patient 1: Cancer diagnosis
   - Patient 2: Complex surgery
   - Patient 3: Treatment decision
3. Attach patient records
4. Add imaging (X-rays, CT, MRI)
5. Prepare case summaries

### Task 3: Document MDT Decisions
1. MDT discusses each patient
2. Record decisions:
   - Treatment plan agreed
   - Surgery recommended
   - Further tests needed
3. Actions assigned:
   - Surgeon to operate
   - Oncologist for chemo
   - Nurse for follow-up
4. Save decisions
5. Update patient pathways

### Task 4: Action MDT Outcomes
1. Patient approved for surgery
2. Book theatre (Code 30)
3. Pre-op assessment
4. Anesthetist review
5. Update pathway
6. Inform patient
7. Schedule surgery within target

## Practice Goals
✅ Schedule 2 MDT meetings
✅ Add 5 patients for discussion
✅ Document 5 decisions
✅ Action 3 outcomes
✅ Coordinate team

## Real NHS Value
MDT ensures best patient outcomes!
                """,
                "practical_module": "Clinical Workflows - MDT",
                "duration": "1.5 hours hands-on"
            }
        ]
    },
    
    "module_4": {
        "title": "Clinic Letter Interpretation & Validation",
        "duration": "Week 7-8",
        "order": 4,
        "lessons": [
            {
                "lesson_id": "4.1",
                "title": "Understanding Clinical Letters",
                "type": "theory",
                "content": """
# 📝 Understanding NHS Clinical Letters

## What are Clinical Letters?
Letters sent between healthcare professionals about patient care.

## Types of Clinical Letters
✅ Referral letters (GP to Consultant)
✅ Clinic letters (after appointments)
✅ Discharge summaries
✅ Investigation results
✅ Treatment plans

## Why Validation Matters
**Problem:** NHS backlogs caused by validation errors!

**Common Errors:**
- Letter says patient treated → NOT in system
- Letter says discharge → Pathway still active
- Letter says appointment booked → NOT booked
- Letter says test done → NO results

**Your Role:** VERIFY everything in the letter against PAS system!

## Validation vs Just Reading
❌ **Reading:** Accept what letter says
✅ **Validation:** CHECK if it's actually true in the system!

## Medical Terminology Basics
- OPD = Outpatient Department
- DNA = Did Not Attend
- MRI = Magnetic Resonance Imaging
- CT = Computerized Tomography
- Mx = Management/Treatment
- Hx = History
- Rx = Treatment/Prescription
                """,
                "duration": "1 hour"
            },
            {
                "lesson_id": "4.2",
                "title": "Letter Validation Process",
                "type": "detailed",
                "content": """
# 📋 How to Validate Clinical Letters

## Step-by-Step Validation Workflow

### Step 1: Read the Letter
- Patient details (NHS number, name, DOB)
- Appointment date
- What happened (seen, treated, discharged, DNA)
- Next steps (follow-up, tests, treatment)

### Step 2: Check PAS System
✅ Is patient registered?
✅ Does pathway exist?
✅ Is appointment recorded?
✅ Are test results in system?
✅ Is treatment recorded?

### Step 3: Identify Discrepancies
🚨 Letter says X → System shows Y

Examples:
- Letter: "Patient treated"
  System: No treatment recorded → FLAG ERROR
  
- Letter: "Patient discharged"
  System: Pathway still active → FLAG ERROR
  
- Letter: "MRI booked for 15/05"
  System: No MRI booking → FLAG ERROR

### Step 4: Generate Correct RTT Code
Based on VERIFIED reality, not letter claims!

- Letter says treated, System confirms: Code 30 ✅
- Letter says treated, System shows nothing: INVESTIGATE 🚨
- Letter says discharge, System shows active: INVESTIGATE 🚨

### Step 5: Add Comment
RTT - [CODE] - [DATE] - [VERIFIED ACTION]

Example:
- "RTT - 30 - 15/05/24 - Definitive treatment verified - Surgery performed"
- "RTT - INVESTIGATE - 15/05/24 - Letter states treatment but no system record"
                """,
                "duration": "1.5 hours"
            },
            {
                "lesson_id": "4.3",
                "title": "PRACTICAL: Clinic Letter Interpreter",
                "type": "hands-on",
                "content": """
# 🏥 HANDS-ON: Validate Real Clinic Letters

## Welcome to Real NHS Validation!
This is what NHS validators do every single day!

## Where to Practice
Go to: **Clinic Letter Interpreter** (in sidebar)

## Step-by-Step Practice

### Task 1: Read Your First Letter
1. Click "Clinic Letter Interpreter"
2. Letter appears - read it carefully
3. Note key information:
   - Patient name
   - Appointment date
   - What happened
   - What letter claims

### Task 2: Check Against PAS
1. Look at "PAS System Check" section
2. See what's ACTUALLY recorded:
   - Was appointment attended?
   - Was treatment given?
   - Are tests recorded?
   - Is pathway status correct?

### Task 3: Identify Discrepancies
1. Compare letter vs PAS
2. Do they match?
   - YES = Validate normally
   - NO = FLAG DISCREPANCY!

Example:
```
Letter says: "Patient treated with injection"
PAS shows: No treatment recorded

ACTION: FLAG for investigation!
```

### Task 4: Choose Correct RTT Code
1. Based on VERIFIED information
2. Not based on letter alone!
3. Select from:
   - Code 10 (Referral)
   - Code 20 (Appointment/Test)
   - Code 30 (Treatment)
   - Code 33 (DNA)
   - Code 34 (Discharge)
   - INVESTIGATE (If mismatch)

### Task 5: Generate Comment
1. Use standard format
2. Reflect VERIFIED reality
3. Flag any issues
4. Submit validation

### Task 6: Get Instant Feedback
1. See if you're correct ✅ or wrong ❌
2. Read explanation
3. Learn from mistakes
4. Try next letter

## Practice Goals
✅ Validate 20 clinic letters
✅ Identify 5 discrepancies
✅ Use correct RTT codes
✅ Generate proper comments
✅ Achieve 90%+ accuracy

## Real NHS Impact
Proper validation prevents:
- NHS backlogs
- Patient delays
- Financial penalties
- Data errors
- Breach investigations

## Teaching Mode Features
✅ See multiple scenarios
✅ Learn why each code fits
✅ Understand validation logic
✅ Build decision-making skills

## AI Validation
✅ Use AI Auto-Validator
✅ Get AI suggestions
✅ Compare your answer vs AI
✅ Learn from AI reasoning
                """,
                "practical_module": "Clinic Letter Interpreter",
                "duration": "3 hours hands-on"
            },
            {
                "lesson_id": "4.4",
                "title": "PRACTICAL: AI Auto-Validator",
                "type": "hands-on",
                "content": """
# 🤖 HANDS-ON: Use AI Auto-Validator

## AI-Powered Validation
Let AI help you validate faster and more accurately!

## Where to Practice
Go to: **AI Auto-Validator** (in sidebar)

## Step-by-Step Practice

### Task 1: Upload/Paste Letter
1. Click "AI Auto-Validator"
2. Paste clinic letter
3. Click "Analyze"
4. AI reads and interprets

### Task 2: See AI Analysis
AI shows you:
✅ Patient details extracted
✅ Key events identified
✅ RTT code recommendation
✅ Comment line generated
✅ Confidence score

### Task 3: Review AI Suggestions
1. Read AI reasoning
2. Check if you agree
3. Learn AI logic
4. Understand why

### Task 4: Compare Your Answer
1. You validate letter
2. AI validates letter
3. Compare results
4. Discuss differences
5. Learn best practice

### Task 5: Batch Validation
1. Process multiple letters
2. AI validates 10 letters/minute
3. Review AI results
4. Approve or override
5. 30X faster than manual!

## Practice Goals
✅ Use AI on 30 letters
✅ Compare AI vs manual
✅ Learn AI reasoning
✅ Achieve validation speed
✅ Maintain accuracy

## Real NHS Value
- Manual validation: 2-3 minutes per letter
- AI validation: 5 seconds per letter
- **30X FASTER!**

Backlog of 10,000 letters:
- Manual: 500 hours (12 weeks)
- AI: 14 hours (2 days!)
                """,
                "practical_module": "AI Auto-Validator",
                "duration": "2 hours hands-on"
            }
        ]
    },
    
    "module_5": {
        "title": "Medical Secretary & Communication Skills",
        "duration": "Week 9-10",
        "order": 5,
        "lessons": [
            {
                "lesson_id": "5.1",
                "title": "Medical Secretary Role",
                "type": "theory",
                "content": """
# 📧 NHS Medical Secretary Role

## What Do Medical Secretaries Do?
Support consultants and clinical teams with administrative duties.

## Key Responsibilities
✅ Type clinic letters
✅ Manage consultant diaries
✅ Book appointments
✅ Handle correspondence
✅ Coordinate clinics
✅ Patient communication
✅ File management
✅ Meeting coordination

## Skills Required
- Fast typing (50+ WPM)
- Medical terminology
- Professional communication
- Organization
- Confidentiality
- Multi-tasking
- IT skills

## Career Path
Medical Secretary → Senior Secretary → PA → Office Manager

## Salary Range
- Junior: £22,000-£25,000
- Experienced: £26,000-£30,000
- Senior: £30,000-£35,000
                """,
                "duration": "1 hour"
            },
            {
                "lesson_id": "5.2",
                "title": "PRACTICAL: Medical Secretary AI",
                "type": "hands-on",
                "content": """
# 🏥 HANDS-ON: Medical Secretary Tasks

## Where to Practice
Go to: **Medical Secretary AI** (in sidebar)

## Step-by-Step Practice

### Task 1: Generate Clinic Letter
1. Click "Medical Secretary AI"
2. Select letter type: Clinic Letter
3. Fill in details:
   - Patient name
   - Date of appointment
   - Consultant name
   - Clinical findings
   - Plan
4. Click "Generate Letter"
5. AI creates professional letter
6. Review and edit
7. Save/Export

### Task 2: Create Referral Letter
1. Select: Referral Letter
2. Enter patient details
3. Reason for referral
4. Urgency (routine/2WW)
5. Generate
6. Professional referral created!

### Task 3: Discharge Summary
1. Select: Discharge Summary
2. Admission details
3. Treatment given
4. Follow-up plan
5. GP instructions
6. Generate complete summary

### Task 4: Manage Consultant Diary
1. View diary
2. Book appointments
3. Block time for clinics
4. Schedule meetings
5. Holiday planning

## Practice Goals
✅ Generate 10 clinic letters
✅ Create 5 referral letters
✅ Write 3 discharge summaries
✅ Manage diary for 1 week

## Real NHS Skills
This is exactly what medical secretaries do daily!
                """,
                "practical_module": "Medical Secretary AI",
                "duration": "3 hours hands-on"
            }
        ]
    },
    
    "module_6": {
        "title": "Data Quality & Timeline Auditing",
        "duration": "Week 11-12",
        "order": 6,
        "lessons": [
            {
                "lesson_id": "6.1",
                "title": "PRACTICAL: Timeline Auditor",
                "type": "hands-on",
                "content": """
# 📅 HANDS-ON: Audit RTT Timelines

## Where to Practice
Go to: **Timeline Auditor** (in sidebar)

## What You'll Do
Check if RTT events are in correct chronological order and properly coded.

## Step-by-Step Practice

### Task 1: Review Timeline
1. See complete patient pathway
2. Check sequence of events
3. Verify dates are logical
4. Check code progression

### Task 2: Identify Errors
Common errors:
- Code 30 before Code 10 (impossible!)
- Code 20 after Code 30 (should be Code 90)
- DNA coded as Code 20 (should be Code 33 if first)
- Dates out of sequence

### Task 3: Correct Timeline
1. Identify wrong codes
2. Suggest corrections
3. Re-sequence events
4. Generate audit report

## Practice Goals
✅ Audit 15 timelines
✅ Find 20 errors
✅ Correct all mistakes
✅ Generate audit reports
                """,
                "practical_module": "Timeline Auditor",
                "duration": "2 hours hands-on"
            },
            {
                "lesson_id": "6.2",
                "title": "PRACTICAL: Data Quality System",
                "type": "hands-on",
                "content": """
# 📊 HANDS-ON: Data Quality Management

## Where to Practice
Go to: **Data Quality System** (in sidebar)

## Step-by-Step Practice

### Task 1: Run Data Validation
1. Select validation checks:
   - Missing NHS numbers
   - Invalid dates
   - Duplicate pathways
   - Orphaned episodes
   - Data inconsistencies
2. Run validation
3. See errors found

### Task 2: Review Errors
1. See list of data errors
2. Prioritize by severity
3. Assign to team members
4. Track corrections

### Task 3: Correct Data
1. Fix NHS numbers
2. Correct dates
3. Merge duplicates
4. Link orphaned records
5. Validate corrections

### Task 4: Generate Reports
1. Data quality scorecard
2. Error trends
3. Improvement metrics
4. Submit to managers

## Practice Goals
✅ Validate 100 patient records
✅ Find 30 errors
✅ Correct all errors
✅ Improve data quality score to 95%+
                """,
                "practical_module": "Data Quality System",
                "duration": "2 hours hands-on"
            }
        ]
    },
    
    "module_7": {
        "title": "NHS Reporting & Analytics",
        "duration": "Week 13-14",
        "order": 7,
        "lessons": [
            {
                "lesson_id": "7.1",
                "title": "PRACTICAL: Interactive Reports",
                "type": "hands-on",
                "content": """
# 📊 HANDS-ON: Build NHS Reports

## Where to Practice
Go to: **Interactive Reports** (in sidebar)

## Step-by-Step Practice

### Task 1: Monthly RTT Report
1. Generate RTT performance report
2. See 18-week achievement %
3. Breach analysis
4. By specialty breakdown
5. Export to Excel

### Task 2: Cancer Waiting Times
1. 2WW performance
2. 62-day achievement
3. Diagnostic waiting times
4. Treatment performance

### Task 3: Dashboard Creation
1. Build live dashboard
2. Key metrics
3. Visual charts
4. Traffic light indicators
5. Share with team

## Practice Goals
✅ Generate 5 different reports
✅ Build 3 dashboards
✅ Export 10 datasets
✅ Present findings
                """,
                "practical_module": "Interactive Reports",
                "duration": "2 hours hands-on"
            }
        ]
    },
    
    "module_8": {
        "title": "Information Governance & Certification",
        "duration": "Week 15-16",
        "order": 8,
        "lessons": [
            {
                "lesson_id": "8.1",
                "title": "Information Governance (Mandatory)",
                "type": "mandatory",
                "content": """
# 🔒 MANDATORY: NHS Information Governance Training

## Why This is Mandatory
ALL NHS staff MUST complete IG training annually. No exceptions!

## What You'll Learn
✅ GDPR & Data Protection Act 2018
✅ NHS Caldicott Principles
✅ Patient Confidentiality
✅ Cyber Security
✅ Data Breach Reporting

## Where to Complete
Go to: **Information Governance** module (in sidebar)

## Must Score 100%
This is NHS requirement - you MUST score 100% to pass.
Unlimited retakes allowed until you pass.

## Time Required
2 hours to complete

## After Passing
✅ Certificate issued immediately
✅ Valid for 12 months
✅ Recorded in your profile
✅ Required for job applications
                """,
                "practical_module": "Information Governance",
                "duration": "2 hours",
                "mandatory": True
            },
            {
                "lesson_id": "8.2",
                "title": "Career Preparation",
                "type": "career",
                "content": """
# 💼 Prepare for NHS Careers

## CV Building
Go to: **CV Builder** module
- Create professional CV
- ATS-optimized
- NHS-specific format
- Export to PDF/Word

## Interview Preparation
Go to: **Job Interview Prep** module
- Practice interview questions
- STAR technique
- Competency questions
- Mock interviews

## Final Certification
Go to: **Certification Exam** module
- 100 questions
- 90 minutes
- 80% pass rate
- TQUK-endorsed certificate
                """,
                "duration": "4 hours"
            }
        ]
    }
}

# ============================================
# LEARNING PROGRESS TRACKING
# ============================================

def get_student_progress(user_email):
    """Get student's learning progress"""
    try:
        # Try to load from file (simple JSON storage)
        import os
        progress_file = f"student_progress_{user_email.replace('@', '_').replace('.', '_')}.json"
        
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                return json.load(f)
        else:
            # Initialize new progress
            return {
                "user_email": user_email,
                "started_date": datetime.now().isoformat(),
                "current_module": "module_1",
                "current_lesson": "1.1",
                "completed_lessons": [],
                "quiz_scores": {},
                "practice_attempts": {},
                "total_study_time": 0,
                "certificates_earned": []
            }
    except:
        return {
            "user_email": user_email,
            "started_date": datetime.now().isoformat(),
            "current_module": "module_1",
            "current_lesson": "1.1",
            "completed_lessons": [],
            "quiz_scores": {},
            "practice_attempts": {},
            "total_study_time": 0,
            "certificates_earned": []
        }


def save_student_progress(user_email, progress_data):
    """Save student progress"""
    try:
        progress_file = f"student_progress_{user_email.replace('@', '_').replace('.', '_')}.json"
        with open(progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)
        return True
    except:
        return False


def mark_lesson_complete(user_email, lesson_id, quiz_score=None):
    """Mark lesson as complete"""
    progress = get_student_progress(user_email)
    
    if lesson_id not in progress["completed_lessons"]:
        progress["completed_lessons"].append(lesson_id)
    
    if quiz_score is not None:
        progress["quiz_scores"][lesson_id] = quiz_score
    
    save_student_progress(user_email, progress)
    return progress


# ============================================
# RENDER FUNCTIONS
# ============================================

def render_learning_dashboard():
    """Main learning dashboard"""
    st.header("🎓 Your Learning Journey")
    
    user_email = st.session_state.get('user_email', 'demo@example.com')
    progress = get_student_progress(user_email)
    
    # Progress overview
    total_lessons = sum(len(module["lessons"]) for module in LEARNING_MODULES.values())
    completed = len(progress["completed_lessons"])
    progress_pct = (completed / total_lessons * 100) if total_lessons > 0 else 0
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Lessons Completed", f"{completed}/{total_lessons}")
    with col2:
        st.metric("📈 Progress", f"{progress_pct:.0f}%")
    with col3:
        st.metric("🏆 Certificates", len(progress["certificates_earned"]))
    with col4:
        avg_score = sum(progress["quiz_scores"].values()) / len(progress["quiz_scores"]) if progress["quiz_scores"] else 0
        st.metric("⭐ Avg Quiz Score", f"{avg_score:.0f}%")
    
    # Progress bar
    st.progress(progress_pct / 100)
    
    # Modules
    st.markdown("---")
    st.subheader("📋 Learning Modules")
    
    for module_id, module in sorted(LEARNING_MODULES.items(), key=lambda x: x[1]["order"]):
        with st.expander(f"📚 {module['title']} - {module['duration']}", expanded=(module_id == progress["current_module"])):
            
            # Module lessons
            for lesson in module["lessons"]:
                lesson_complete = lesson["lesson_id"] in progress["completed_lessons"]
                icon = "✅" if lesson_complete else "📝"
                
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"{icon} **{lesson['lesson_id']}: {lesson['title']}**")
                    st.caption(f"⏱️ {lesson.get('duration', '30 mins')} • {lesson['type'].title()}")
                with col_b:
                    if st.button(f"Start →", key=f"btn_{lesson['lesson_id']}"):
                        st.session_state['current_lesson'] = lesson
                        st.session_state['learning_view'] = 'lesson'
                        st.rerun()


def render_lesson_view():
    """Render individual lesson"""
    lesson = st.session_state.get('current_lesson')
    
    if not lesson:
        st.warning("No lesson selected")
        return
    
    # Lesson header
    st.markdown(f"# {lesson['lesson_id']}: {lesson['title']}")
    st.caption(f"⏱️ Estimated time: {lesson.get('duration', '30 mins')}")
    
    # Lesson content
    st.markdown(lesson['content'])
    
    st.markdown("---")
    
    # Practice scenarios
    if 'practice_scenarios' in lesson:
        st.subheader("🎯 Practice with Real Scenarios")
        st.info(f"Apply what you learned with {len(lesson['practice_scenarios'])} real RTT scenarios")
        
        for scenario_id in lesson['practice_scenarios']:
            if st.button(f"📖 Practice: {scenario_id}", key=f"practice_{scenario_id}"):
                # Show scenario from training library
                st.session_state['practice_scenario'] = scenario_id
                st.rerun()
    
    # Quiz questions
    if 'quiz_questions' in lesson:
        st.subheader("✅ Quick Knowledge Check")
        
        score = 0
        total = len(lesson['quiz_questions'])
        
        for idx, q in enumerate(lesson['quiz_questions']):
            st.markdown(f"**Question {idx + 1}:** {q['question']}")
            answer = st.radio("Select your answer:", q['options'], key=f"q_{lesson['lesson_id']}_{idx}")
            
            if st.button(f"Check Answer", key=f"check_{lesson['lesson_id']}_{idx}"):
                selected_idx = q['options'].index(answer)
                if selected_idx == q['correct']:
                    st.success(f"✅ Correct! {q['explanation']}")
                    score += 1
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
        
        st.markdown("---")
        
        if st.button("✅ Complete Lesson", type="primary"):
            quiz_score = (score / total * 100) if total > 0 else 100
            user_email = st.session_state.get('user_email', 'demo@example.com')
            mark_lesson_complete(user_email, lesson['lesson_id'], quiz_score)
            st.success(f"🎉 Lesson complete! Score: {quiz_score:.0f}%")
            st.balloons()
            st.session_state['learning_view'] = 'dashboard'
            st.rerun()
    
    # Navigation
    if st.button("← Back to Dashboard"):
        st.session_state['learning_view'] = 'dashboard'
        st.rerun()


def render_comprehensive_learning():
    """Main render function"""
    
    # Initialize session state
    if 'learning_view' not in st.session_state:
        st.session_state['learning_view'] = 'dashboard'
    
    # Route to appropriate view
    if st.session_state['learning_view'] == 'dashboard':
        render_learning_dashboard()
    elif st.session_state['learning_view'] == 'lesson':
        render_lesson_view()
