# 📝 VALIDATION COMMENTING PROCESS - The REAL Workflow

**Date:** October 14, 2025  
**Purpose:** Document what comments are REALLY for  
**Key:** Comments are what YOU WRITE after validation, not what you read!

---

## 🎯 THE REAL PROCESS

### VALIDATION WORKFLOW:

**STEP 1: Read Source Documents**
- Read clinic letters (if available)
- Read consultation notes
- Read diagnostic reports
- Read appointment outcomes
- Read operation notes

**STEP 2: Check PAS Data**
- Compare letter vs PAS
- Check if episodes recorded
- Check if codes correct
- Check if dates accurate

**STEP 3: Validate & Update PAS**
- Add missing episodes
- Correct wrong codes
- Fix incorrect dates
- Update waiting times

**STEP 4: WRITE VALIDATION COMMENT**
- Document what you found
- Document what you did
- Document what's missing
- Document next steps

---

## 📋 WHEN TO USE EACH COMMENT STYLE

### **Scenario 1: Clinic Letter Available**

**What You Have:**
- Clinic letter dated 24/05/2025
- Letter says: "Patient treated with antibiotics on 23/04/2025"
- PAS shows: Treatment recorded correctly

**Your Validation Comment:**
```
CS (23/04/2025)(30) JDS AS PER CL DATED 24/05/2025 PATIENT RCVD MEDICATION/TREATMENT
```

**Meaning:**
- "I validated this pathway"
- "I read the clinic letter dated 24/05/2025"
- "Letter confirms treatment on 23/04/2025"
- "I recorded Code 30 in PAS"
- "Clock stopped correctly"

---

### **Scenario 2: NO Clinic Letter Available**

**What You Have:**
- PAS shows appointment on 15/10/2025
- PAS shows "Attended"
- NO clinic letter scanned
- NO notes available

**Your Validation Comment:**
```
15/10/2025 JDS NO CLINIC LETTER AVAILABLE. PATIENT ATTENDED APPOINTMENT AS PER PAS. CODE 20 RECORDED
```

**Meaning:**
- "I validated this pathway"
- "NO clinic letter available"
- "I checked PAS - shows attended"
- "I recorded Code 20 based on PAS data"
- "Clock continues"

---

### **Scenario 3: Not Enough Information**

**What You Have:**
- PAS shows appointment on 15/10/2025
- NO outcome recorded
- NO clinic letter
- NO notes
- Can't determine what happened

**Your Validation Comment:**
```
15/10/2025 JDS INSUFFICIENT INFORMATION. NO CLINIC LETTER. NO OUTCOME RECORDED IN PAS. UNABLE TO VALIDATE. QUERY SENT TO ADMIN TEAM
```

**Meaning:**
- "I tried to validate"
- "Not enough information available"
- "Can't determine RTT code"
- "Sent query to admin team"
- "Awaiting response"

---

### **Scenario 4: Letter Says One Thing, PAS Shows Another**

**What You Have:**
- Clinic letter says: "Surgery on 25/11/2025"
- PAS shows: No treatment recorded

**Your Validation Comment:**
```
08/10/2025 JDS AS PER CL DATED 30/11/2025 SURGERY PERFORMED 25/11/2025. PAS UPDATED. CODE 30 ADDED. CLOCK STOPPED
```

**Meaning:**
- "I found discrepancy"
- "Letter says surgery done"
- "PAS was missing this"
- "I UPDATED PAS"
- "Added Code 30"
- "Clock now stopped correctly"

---

### **Scenario 5: MRI Scan Requested But Not Booked**

**What You Have:**
- Clinic letter says: "Patient to undergo MRI scan"
- PAS shows: NO MRI ordered

**Your Validation Comment:**
```
08/10/2025 JDS AS PER CL DATED 05/10/2025 MRI SCAN REQUESTED. NOT BOOKED IN PAS. QUERY SENT TO BOOKING TEAM. CODE 20 RECORDED
```

**Meaning:**
- "I validated this"
- "Letter says MRI needed"
- "PAS shows not booked"
- "I sent query to booking team"
- "Recorded Code 20 (activity)"
- "Clock continues"

---

### **Scenario 6: Patient DNA First Appointment**

**What You Have:**
- Appointment date: 15/09/2025
- PAS shows: DNA
- This was first appointment

**Your Validation Comment:**
```
15/09/2025 JDS PATIENT DNA FIRST APPOINTMENT. CODE 33 RECORDED. CLOCK STOPPED. QUERY SENT RE REBOOK OR DISCHARGE
```

**Meaning:**
- "Patient didn't attend first appointment"
- "Recorded Code 33"
- "Clock stopped"
- "Sent query about next steps"

---

### **Scenario 7: Follow-up Mentioned But Not Booked**

**What You Have:**
- Clinic letter says: "Follow-up in 6 weeks"
- PAS shows: NO follow-up booked

**Your Validation Comment:**
```
08/10/2025 JDS AS PER CL DATED 24/05/2025 F/U REQUIRED IN 6 WEEKS. NOT BOOKED IN PAS. QUERY SENT TO BOOKING TEAM
```

**Meaning:**
- "Letter says follow-up needed"
- "Not booked yet"
- "I sent query to booking team"
- "Awaiting booking"

---

### **Scenario 8: Watchful Wait - Clock Paused**

**What You Have:**
- Clinic letter says: "Active monitoring. Review in 3 months"
- PAS shows: No code recorded

**Your Validation Comment:**
```
AM (CODE 32) JDS AS PER CL DATED 10/08/2025 ACTIVE MONITORING CLINICIAN INITIATED. CLOCK PAUSED. REVIEW DATE 10/11/2025
```

**Meaning:**
- "Clinician decided watchful wait"
- "Recorded Code 32"
- "Clock paused"
- "Review date set"

---

## 📊 VALIDATION COMMENT STRUCTURE

### **Purpose of Comments:**
1. ✅ Document what you validated
2. ✅ Document source of information (letter/PAS)
3. ✅ Document what you found
4. ✅ Document what you did (updated PAS/sent query)
5. ✅ Document RTT code assigned
6. ✅ Document clock status
7. ✅ Document next steps

### **Comments Are:**
- Your validation record
- Audit trail
- Evidence of work done
- Communication to others
- Documentation of issues found

### **Comments Are NOT:**
- What you read from letters
- What was already in PAS
- Pre-existing notes

---

## 🤖 WHAT AI MUST DO

### AI Validation Process:

**STEP 1: Read All Sources**
- Read clinic letters
- Read PAS data
- Read appointment outcomes
- Read diagnostic results

**STEP 2: Compare & Validate**
- Letter vs PAS
- Identify discrepancies
- Identify missing data
- Identify errors

**STEP 3: Update PAS**
- Add missing episodes
- Correct wrong codes
- Fix dates
- Update status

**STEP 4: GENERATE VALIDATION COMMENT**

**If Letter Available:**
```
CS (23/04/2025)(30) AI AS PER CL DATED 24/05/2025 PATIENT RCVD MEDICATION/TREATMENT. F/U APPT BOOKED
```

**If NO Letter:**
```
15/10/2025 AI NO CLINIC LETTER AVAILABLE. PATIENT ATTENDED AS PER PAS. CODE 20 RECORDED
```

**If Insufficient Info:**
```
15/10/2025 AI INSUFFICIENT INFORMATION. NO CLINIC LETTER. NO OUTCOME IN PAS. FLAGGED FOR MANUAL REVIEW
```

**If Discrepancy Found:**
```
08/10/2025 AI AS PER CL DATED 30/11/2025 SURGERY PERFORMED 25/11/2025. PAS UPDATED. CODE 30 ADDED. CLOCK STOPPED
```

---

## 📋 COMMENT TEMPLATES BY SCENARIO

### **Template 1: Standard Validation (Letter Available)**
```
[VALIDATION_DATE] [INITIALS] AS PER CL DATED [LETTER_DATE] [WHAT LETTER SAYS]. [WHAT YOU DID]. [RTT CODE]. [CLOCK STATUS]
```

### **Template 2: No Clinic Letter**
```
[VALIDATION_DATE] [INITIALS] NO CLINIC LETTER AVAILABLE. [WHAT PAS SHOWS]. [WHAT YOU DID]. [RTT CODE]. [CLOCK STATUS]
```

### **Template 3: Insufficient Information**
```
[VALIDATION_DATE] [INITIALS] INSUFFICIENT INFORMATION. [WHAT'S MISSING]. UNABLE TO VALIDATE. [QUERY SENT TO WHOM]
```

### **Template 4: Discrepancy Found**
```
[VALIDATION_DATE] [INITIALS] AS PER CL DATED [LETTER_DATE] [WHAT LETTER SAYS]. [WHAT PAS SHOWED]. PAS UPDATED. [WHAT YOU ADDED]. [RTT CODE]. [CLOCK STATUS]
```

### **Template 5: Clock Stop**
```
CS ([STOP_DATE])([CODE]) [INITIALS] AS PER CL DATED [LETTER_DATE] [REASON FOR STOP]. [F/U STATUS]
```

### **Template 6: Active Monitoring**
```
AM (CODE [31/32]) [INITIALS] AS PER CL DATED [LETTER_DATE] ACTIVE MONITORING [PATIENT/CLINICIAN] INITIATED. CLOCK PAUSED. REVIEW DATE [DATE]
```

---

## ✅ VALIDATION EXCEL SHEET COLUMNS

### Typical Validation Spreadsheet:

| Column | Purpose |
|--------|---------|
| **Pathway Number** | Unique pathway ID |
| **NHS Number** | Patient identifier |
| **Patient Name** | Patient name |
| **Referral Date** | Clock start date |
| **Specialty** | Clinical specialty |
| **Clinic Letter Date** | Date of letter (if available) |
| **Clinic Letter Available?** | Yes/No |
| **What Letter Says** | Summary of letter |
| **What PAS Shows** | Current PAS data |
| **Discrepancy?** | Yes/No |
| **RTT Code** | Code assigned |
| **Episode Date** | Date of episode |
| **Clock Status** | Started/Ticking/Stopped/Paused |
| **Waiting Time** | Days/weeks |
| **Breach?** | Yes/No |
| **Action Taken** | What you did |
| **Query Sent?** | Yes/No |
| **Validation Comment** | Your comment |
| **Validator Initials** | Who validated |
| **Validation Date** | When validated |

---

## 🎯 KEY PRINCIPLES

### **Comments Document:**
1. ✅ What you READ (letter/PAS)
2. ✅ What you FOUND (discrepancies/issues)
3. ✅ What you DID (updated PAS/sent query)
4. ✅ What CODE you assigned
5. ✅ What CLOCK STATUS is
6. ✅ What NEXT STEPS are

### **Comments Are Written:**
- AFTER validation
- To document your work
- To create audit trail
- To communicate issues
- To track progress

### **Comments Are NOT:**
- Pre-existing in PAS
- What you read from letters
- What was already there

---

## 💡 SUMMARY

**REAL Validation Process:**
1. Read clinic letter (if available)
2. Check PAS data
3. Compare letter vs PAS
4. Identify discrepancies
5. Update PAS
6. WRITE validation comment
7. Record in Excel

**Comment Styles Used When:**
- ✅ Letter available → Standard format
- ✅ NO letter → "NO CLINIC LETTER AVAILABLE"
- ✅ Insufficient info → "INSUFFICIENT INFORMATION"
- ✅ Discrepancy → "PAS UPDATED"
- ✅ Clock stops → "CS (DATE)(CODE)"

**AI Must:**
1. Read all sources
2. Validate data
3. Update PAS
4. GENERATE appropriate comment
5. Record in validation sheet

**This is the REAL workflow!** 🚀

---

**T21 Services Limited | Company No: 13091053**  
**Validation Commenting Process - What Comments Really Are**
