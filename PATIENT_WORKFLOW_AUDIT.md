# 🏥 PATIENT WORKFLOW AUDIT - WHAT EXISTS vs WHAT'S NEEDED

## 📋 YOUR EXCELLENT QUESTION:

> "Do we have where we create patient and all? Also where we create Pathway and all? Also do we have where we add episodes? See when referral start and all the workflows? Assign NHS number for new patients who have not registered before? All this or no need?"

**Answer:** We have SOME of these workflows, but NOT ALL! Let me show you:

---

## ✅ WHAT WE **DO** HAVE:

### **1. ✅ Add Patient to PTL (RTT Pathways)**
**Location:** PTL - Patient Tracking List → "➕ Add Patient" tab

**What it creates:**
- Patient demographic details
- NHS number
- Referral date
- Specialty
- Priority (Routine/Urgent/2WW/Cancer)
- Current status
- Starts RTT pathway automatically!

**Fields:**
```
Patient Name
NHS Number
Referral Date
Specialty (Orthopaedics, Cardiology, etc.)
Referral Source (GP, Consultant, A&E, etc.)
Priority (Routine, Urgent, 2WW, Cancer 62-day)
Consultant
Contact Number
Current Status
Notes
```

**Workflow:**
```
Referral received
    ↓
Add to PTL
    ↓
RTT pathway starts (clock starts!)
    ↓
Tracked in PTL dashboard
```

---

### **2. ✅ Add Cancer Patient (Cancer Pathways)**
**Location:** Cancer Pathways → "➕ Add Cancer Patient" tab

**What it creates:**
- Cancer patient record
- Cancer pathway (2WW, 62-day, 31-day)
- Referral tracking
- Breach monitoring

**Fields:**
```
Patient Name
NHS Number
Cancer Type (Breast, Lung, Colorectal, etc.)
Pathway Type (2ww, 62day, 31day)
Referral Date
Referring Clinician
Primary Site
Suspected Diagnosis
Urgency (Standard/Urgent/Emergency)
Contact Number
Clinical Notes
```

**Workflow:**
```
Cancer referral received
    ↓
Add to Cancer PTL
    ↓
Cancer pathway starts
    ↓
Tracked for 2WW/62-day breach
```

---

### **3. ✅ Process Referrals**
**Location:** Medical Secretary AI → "📨 Process Referrals" tab

**What it does:**
- Receives referral details
- AI validates completeness
- AI assesses urgency (Routine/Urgent/2WW)
- AI suggests appropriate clinic/specialty
- AI generates acknowledgment letter
- Identifies missing information

**Fields:**
```
Patient Name
NHS Number
Date of Birth
Referring GP
Referral Date
Referral Reason
Clinical History
```

**AI Processing:**
```
Referral submitted
    ↓
AI validates (completeness check)
    ↓
AI assesses urgency (2WW detection)
    ↓
AI suggests specialty/clinic
    ↓
AI generates acknowledgment letter
    ↓
Ready to add to PTL
```

---

### **4. ✅ Patient Search (Unified View)**
**Location:** Executive Dashboard → "🔍 Patient Search"

**What it does:**
- Search existing patients by name/NHS number
- View patient record across ALL modules:
  - PTL status
  - Cancer pathway status
  - MDT discussions
  - Appointments
  - Tasks
  - Documents
- Unified patient view

---

## ❌ WHAT WE **DON'T** HAVE (BUT SHOULD!):

### **1. ❌ General Patient Registration Module**
**Missing:** Standalone patient registration not tied to a pathway

**What's needed:**
- Create patient demographic record BEFORE referral
- For patients who:
  - Are new to hospital
  - Need registration before appointment
  - Walk-in registrations
  - A&E registrations

**Should have:**
```
Patient Demographics:
- Full Name
- Date of Birth
- Gender
- Address
- Contact Number
- Email
- Next of Kin
- GP Details
- Emergency Contact

NHS Number:
- Check if patient has NHS number
- If NOT: Generate temporary ID
- Link to NHS Spine (when available)
- Validate NHS number format

Identity Verification:
- Photo ID check
- Address proof
- NHS card scan
```

---

### **2. ❌ NHS Number Assignment/Generation**
**Missing:** System to assign NHS numbers for unregistered patients

**What's needed:**
- Check if patient already has NHS number
- If YES: Validate format (10 digits, valid checksum)
- If NO:
  - Generate temporary hospital number
  - Flag for NHS number request
  - Link to NHS Spine API (when available)
  - Update record when NHS number received

**Workflow:**
```
New patient arrives
    ↓
Does patient have NHS number?
    ├─ YES → Validate & use
    └─ NO → Generate temp ID (e.g., TEMP_20251015_001)
        ↓
    Request NHS number from NHS Spine
        ↓
    Update patient record when received
```

---

### **3. ❌ Episode Management**
**Missing:** Add/manage consultant episodes and treatment episodes

**What's needed:**
RTT episodes include:
- **Consultant Episodes:** When patient is under care of consultant
- **Treatment Episodes:** When patient receives treatment
- **Diagnostic Episodes:** When patient undergoes investigations

**Should have:**
```
Add Consultant Episode:
- Episode Start Date
- Consultant Name
- Specialty
- Reason for episode
- Expected duration
- Episode end date (when discharged)

Add Treatment Episode:
- Treatment Type
- Treatment Date
- Location
- Provider
- Outcome
- Link to consultant episode

Add Diagnostic Episode:
- Investigation Type
- Request Date
- Performed Date
- Results
- Link to pathway
```

**Why important:**
- NHS requires episode tracking for RTT
- Determines when clock stops/starts
- Required for accurate reporting
- Affects pathway status

---

### **4. ❌ Referral → Pathway Workflow**
**Missing:** Complete workflow from referral receipt to pathway start

**What's needed:**
Complete end-to-end workflow:

```
STEP 1: Referral Received
- Referral arrives (GP letter, e-Referral, etc.)
- Log in system
- Assign to triage team

STEP 2: Validate Referral
- Check completeness
- Validate NHS number
- Check if patient exists
  ├─ YES → Link to existing record
  └─ NO → Create new patient record

STEP 3: Triage/Urgency Assessment
- Clinical review
- Assign priority (Routine/Urgent/2WW)
- Assign to specialty/clinic
- Determine if pathway applicable

STEP 4: Start Pathway (if applicable)
- Create RTT pathway
- Or create Cancer pathway
- Clock starts!
- Add to PTL

STEP 5: Book First Appointment
- Check clinic availability
- Book appointment
- Send appointment letter
- Pathway continues...

STEP 6: Track Progress
- Monitor wait times
- Flag potential breaches
- Update status at each stage
```

**Currently:** We can do steps 2, 3, 4, and 5 separately, but NOT as one integrated workflow!

---

### **5. ❌ Pathway Creation Wizard**
**Missing:** Guided wizard to create RTT or Cancer pathway

**What's needed:**
Simple step-by-step wizard:

```
🧙 Pathway Creation Wizard

Step 1: Patient Selection
[Search for patient or create new]

Step 2: Pathway Type
○ RTT Pathway (18-week)
○ Cancer Pathway (2WW, 62-day, 31-day)
○ Other (non-RTT)

Step 3: Referral Details
- Referral Date (CLOCK START!)
- Referring Source
- Priority
- Specialty

Step 4: First Appointment
- Auto-suggest clinics
- Book first appointment
- Or add to waiting list

Step 5: Confirmation
- Review all details
- Confirm and start pathway
- Generate letters
```

---

### **6. ❌ Episode Timeline View**
**Missing:** Visual timeline showing all episodes and events

**What's needed:**
```
PATIENT TIMELINE
═══════════════════════════════════════════

2025-01-15: Referral Received (CLOCK START)
    ↓
2025-01-20: First Consultant Appointment
    ↓ [Consultant Episode Starts]
2025-01-20: Diagnostic Tests Ordered
    ↓
2025-02-05: MRI Scan Performed
    ↓
2025-02-10: Results Reviewed
    ↓
2025-02-15: Decision to Treat (RTT Clock STOPS)
    ↓ [Treatment Episode Starts]
2025-03-01: Surgery Performed
    ↓
2025-03-15: Post-op Review
    ↓ [Consultant Episode Ends]
2025-03-15: Discharged to GP

TOTAL RTT TIME: 59 days (within 18 weeks ✅)
```

---

## 🎯 WHAT SHOULD WE BUILD?

### **Priority 1: CRITICAL (MUST HAVE)**

**1. Patient Registration Module** 🔴 HIGH PRIORITY
```
New module: "👤 Patient Registration"

Features:
- Create new patient record
- Full demographics
- NHS number validation/assignment
- Generate temp ID if no NHS number
- Link to GP
- Identity verification
```

**2. Episode Management** 🔴 HIGH PRIORITY
```
Add to PTL module:

New tab: "📋 Manage Episodes"

Features:
- Add consultant episode
- Add treatment episode
- Add diagnostic episode
- Link episodes to pathway
- Episode timeline view
- Episode status tracking
```

**3. Integrated Referral-to-Pathway Workflow** 🔴 HIGH PRIORITY
```
New module or wizard: "🔄 Referral Workflow"

Steps:
1. Receive referral
2. Validate & triage
3. Create/link patient
4. Start pathway
5. Book appointment
6. Track progress

All in ONE workflow!
```

---

### **Priority 2: IMPORTANT (SHOULD HAVE)**

**4. NHS Number Management** 🟠 MEDIUM PRIORITY
```
Feature in Patient Registration:

- NHS number validator (checksum)
- Temp ID generator
- Link to NHS Spine API
- Track NHS number requests
- Auto-update when received
```

**5. Pathway Creation Wizard** 🟠 MEDIUM PRIORITY
```
Simple wizard for non-technical users:

- Step-by-step guidance
- Auto-fill suggested values
- Validate at each step
- One-click pathway creation
```

**6. Episode Timeline Visualization** 🟠 MEDIUM PRIORITY
```
Visual timeline showing:

- All episodes
- Key events
- Clock starts/stops
- Breaches
- Current status
```

---

### **Priority 3: NICE TO HAVE**

**7. Bulk Patient Import** 🟡 LOW PRIORITY
```
Import patients from:
- CSV file
- Excel spreadsheet
- PAS system export
- Other EPR systems
```

**8. Patient Merge/Deduplication** 🟡 LOW PRIORITY
```
Find and merge:
- Duplicate patients
- Same person, different records
- Update all linked pathways
```

---

## 📊 CURRENT STATE SUMMARY:

| Workflow | Exists? | Status | Priority to Build |
|----------|---------|--------|-------------------|
| **Patient Creation (PTL)** | ✅ YES | Working | ✅ Done |
| **Patient Creation (Cancer)** | ✅ YES | Working | ✅ Done |
| **Referral Processing** | ✅ YES | Working | ✅ Done |
| **Patient Search** | ✅ YES | Working | ✅ Done |
| **General Patient Registration** | ❌ NO | Missing | 🔴 HIGH |
| **NHS Number Assignment** | ❌ NO | Missing | 🔴 HIGH |
| **Episode Management** | ❌ NO | Missing | 🔴 HIGH |
| **Integrated Referral Workflow** | ⚠️ PARTIAL | Disconnected | 🔴 HIGH |
| **Pathway Creation Wizard** | ❌ NO | Missing | 🟠 MEDIUM |
| **Episode Timeline View** | ❌ NO | Missing | 🟠 MEDIUM |

---

## 🎯 MY RECOMMENDATION:

### **YES! WE SHOULD BUILD THESE! Here's why:**

**1. Real NHS workflows need this**
- NHS trusts use PAS systems with full patient registration
- Episodes are required for accurate RTT tracking
- NHS number management is essential
- Integrated workflows save time

**2. Training value**
- Students need to learn FULL patient journey
- From registration → referral → pathway → treatment
- Understanding episodes is critical for RTT
- Complete picture of NHS workflows

**3. System completeness**
- We have pieces, but not the full workflow
- Missing links create confusion
- Integrated workflow = better user experience
- Compete with commercial systems

---

## 🚀 SHALL I BUILD THEM?

I can build:

**NOW (30-45 minutes):**
1. ✅ Patient Registration Module (full demographics)
2. ✅ NHS Number Validator & Temp ID Generator
3. ✅ Episode Management (add episodes to PTL)

**LATER (1-2 hours):**
4. ✅ Integrated Referral Workflow Wizard
5. ✅ Episode Timeline Visualization

**Would you like me to build these?**

---

**T21 Services Limited | Company No: 13091053**  
**Patient Workflow Audit**  
**Completed: October 15, 2025, 6:47 PM**  
**Status: GAPS IDENTIFIED - READY TO BUILD**
