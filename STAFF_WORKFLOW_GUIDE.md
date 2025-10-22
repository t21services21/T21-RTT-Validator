# 📋 STAFF WORKFLOW GUIDE - COMPLETE PROCESS

## **HOW TO GET STARTED WITH JOB AUTOMATION**

---

## **🎯 THREE OPTIONS FOR MANAGING APPLICATIONS**

### **OPTION 1: REVIEW MODE** ⭐ **RECOMMENDED FOR FIRST FEW STUDENTS**
✅ Staff reviews EVERY application before submission  
✅ Check all information is correct  
✅ Click "Approve" to submit  
✅ Edit supporting information if needed  

**When to use:** 
- New students
- First applications
- Students with complex situations
- Quality control

---

### **OPTION 2: AUTO-SUBMIT MODE** 🚀 **RECOMMENDED FOR SCALE**
✅ Applications submit automatically  
✅ NO staff approval needed  
✅ Student receives email notifications  
✅ Staff monitors dashboard  

**When to use:**
- Trusted students with good data
- High volume (10,000+ applications)
- Students with signed contracts

---

### **OPTION 3: HYBRID MODE** ⚙️ **BEST OF BOTH WORLDS**
✅ Auto-submit for some students  
✅ Review mode for others  
✅ Flexibility per student  

**When to use:**
- Mix of new and experienced students
- Different trust levels
- Custom requirements

---

## **📊 GETTING LEARNER DATA INTO SYSTEM**

You have **THREE OPTIONS** for importing student data:

---

### **METHOD 1: BULK EXCEL IMPORT** 📥 **FASTEST FOR MANY STUDENTS**

#### **Step 1: Export Template**
```python
from job_automation.student_data_import import StudentDataImporter

importer = StudentDataImporter()
importer.export_template_excel('student_import_template.xlsx')
```

This creates an Excel file with these columns:
- First Name
- Last Name
- Email
- Phone
- Address Line 1
- City
- Postcode
- NHS Number (optional)
- Date of Birth
- Qualifications (can be JSON or simple text)
- Employment History
- Immigration Status
- Requires Sponsorship (Yes/No)
- Preferred Locations (comma-separated)
- Preferred Bands (comma-separated)
- TQUK Completion Date

#### **Step 2: Fill Excel with Learner Data**

**Example Row:**
```
First Name: John
Last Name: Smith
Email: john.smith@email.com
Phone: 07700900000
Address Line 1: 123 High Street
City: London
Postcode: SW1A 1AA
NHS Number: AB123456C
Date of Birth: 1995-05-15
Qualifications: BSc Health - 2:1 - 2020, GCSE English - C - 2015
Employment History: Admin Assistant at Hospital - 2023-2024
Immigration Status: British citizen with the right to work in the UK
Requires Sponsorship: No
Preferred Locations: London, Manchester
Preferred Bands: Band 3, Band 4
TQUK Completion Date: 2025-04
```

#### **Step 3: Import Excel**
```python
results = importer.import_from_excel('completed_student_data.xlsx')

print(f"✅ Successfully imported: {results['successful']}")
print(f"❌ Failed: {results['failed']}")

# View errors
for error in results['errors']:
    print(f"Row {error['row']}: {error['error']}")
```

**What happens:**
- ✅ Student profiles created in database
- ✅ Automation settings created (PAUSED status)
- ✅ Staff must review before activating
- ✅ Contract must be uploaded

---

### **METHOD 2: MANUAL WEB FORM** 📝 **BEST FOR FEW STUDENTS**

#### **Step 1: Open Staff Dashboard**
```bash
streamlit run job_automation/staff_review_system.py
```

#### **Step 2: Click "Add New Student"**

Fill in web form:
- Personal details
- Address
- Immigration status
- Qualifications
- TQUK completion date
- Employment history
- References
- Job preferences
- Trac account details

#### **Step 3: Submit**

Student profile created with status: **PENDING REVIEW**

---

### **METHOD 3: STAFF FILLS FIRST APPLICATION** ✍️ **LEARN BY DOING**

#### **Step 1: Create Basic Student Profile**
Minimum info needed:
- Name
- Email
- Phone
- Immigration status
- TQUK completion date

#### **Step 2: Staff Manually Fills First Application**
- Use Trac system manually
- Fill all sections
- Take notes of what was entered

#### **Step 3: Import That Data**
Use notes to complete student profile in system

#### **Step 4: Future Applications = Automated!**
System uses the data from first application

---

## **🔧 STUDENT SETUP WORKFLOW (COMPLETE)**

### **PHASE 1: INITIAL REGISTRATION**

```
1. Import student data (Excel, manual, or first app)
   ↓
2. Student profile created with status: PENDING REVIEW
   ↓
3. Automation settings created with status: PAUSED
```

---

### **PHASE 2: TRAC ACCOUNT SETUP**

**Two Options:**

**Option A: Student Already Has Trac Account**
```
1. Student provides Trac email + password
   ↓
2. Staff verifies credentials work
   ↓
3. System encrypts and stores credentials
   ↓
4. Ready for automation!
```

**Option B: Staff Creates New Trac Account for Student**
```
1. Staff creates Trac account manually
   ↓
2. Staff enters Trac email + password in system
   ↓
3. System encrypts and stores
   ↓
4. Ready for automation!
```

**Code to Add Trac Credentials:**
```python
from job_automation.student_data_import import TracAccountSetup

trac_setup = TracAccountSetup()

# Verify credentials work BEFORE storing
is_valid = await trac_setup.verify_trac_credentials(
    'student@email.com',
    'their_password'
)

if is_valid:
    # Store encrypted credentials
    trac_setup.add_trac_credentials(
        student_id='uuid-here',
        trac_email='student@email.com',
        trac_password='their_password'  # Will be encrypted
    )
    print("✅ Credentials stored securely")
else:
    print("❌ Invalid credentials - check with student")
```

---

### **PHASE 3: CONTRACT & ACTIVATION**

```
1. Student signs contract (physical or digital)
   ↓
2. Staff uploads contract PDF in system
   ↓
3. Staff marks contract as signed
   ↓
4. Staff chooses automation mode:
   - Review Mode (staff approves each app)
   - Auto-Submit Mode (fully automated)
   - Paused (no automation)
   ↓
5. Staff clicks "Activate Automation"
   ↓
6. System status changes to: ACTIVE
```

---

### **PHASE 4: AUTOMATION BEGINS**

**If Review Mode:**
```
Job discovered → Application generated → 
STAFF REVIEWS → Staff clicks "Approve" → 
Application submitted → Student notified
```

**If Auto-Submit Mode:**
```
Job discovered → Application generated → 
Application submitted automatically → 
Student notified → Staff sees in dashboard
```

---

## **👨‍💼 STAFF DAILY WORKFLOW**

### **Morning Routine (5-10 minutes)**

1. **Open Staff Dashboard**
```bash
streamlit run job_automation/staff_review_system.py
```

2. **Check System Health**
- ✅ Scraper running?
- ✅ Queue processor running?
- ✅ Interview detector running?
- ⚠️ Any errors?

3. **Review Mode Students: Approve Applications**
- Go to "Pending Review" tab
- See list of applications waiting
- For each application:
  - ✅ Preview supporting information
  - ✅ Check job details (trust, band, location)
  - ✅ Verify sponsorship if needed
  - ✅ Click "Approve & Submit" OR "Reject"

4. **Auto-Submit Students: Monitor**
- Go to "Submission History" tab
- See what was submitted automatically
- Check for any errors

---

### **Weekly Tasks (30 minutes)**

1. **Review Student Performance**
- Check success rates
- Identify top performing students
- Adjust settings for struggling students

2. **Update Job Preferences**
- Add new locations if needed
- Adjust bands
- Update sponsorship requirements

3. **System Maintenance**
- Review error logs
- Clear old data
- Export reports for management

---

### **Monthly Tasks (1 hour)**

1. **Success Rate Analysis**
- Which trusts are hiring most?
- Which job titles get most interviews?
- Adjust automation strategy

2. **Student Reviews**
- Check contract renewals
- Update Trac passwords if changed
- Remove inactive students

3. **Platform Updates**
- Install system updates
- Review new features
- Train staff on improvements

---

## **🎛️ STAFF DASHBOARD FEATURES**

### **Tab 1: Pending Review** 📝
**What you see:**
- All applications waiting for approval
- Student name, job title, trust
- AI-generated supporting information preview
- Priority level (urgent, high, normal, low)
- Sponsorship availability

**Actions:**
- ✅ Approve & Submit Now
- 📝 Edit & Approve
- ⏰ Schedule for Later
- ❌ Reject

**Filters:**
- By student
- By priority
- By sponsorship requirement

---

### **Tab 2: Student Settings** ⚙️
**What you see:**
- List of all students
- Current automation status
- Application stats

**For each student:**
- 🔴 Paused (no automation)
- 🟡 Review Mode (staff approval required)
- 🟢 Auto-Submit (fully automated)

**Configure:**
- Max applications per day
- Sponsorship requirement
- Preferred locations
- Preferred bands
- Working patterns
- Contract status

**Actions:**
- ▶️ Start Automation
- ⏸️ Pause Automation
- 💾 Save Settings
- 📄 Upload Contract

---

### **Tab 3: Submission History** 📊
**What you see:**
- All submitted applications (last 100)
- Student name, job title, trust
- Submission date/time
- Confirmation number
- Status

**Actions:**
- 📥 Export to CSV
- 🔍 Filter by student
- 📧 Resend confirmation email

---

### **Tab 4: Global Settings** 🔧
**System-wide configuration:**

**Automation:**
- Enable/disable global auto-submit
- Job scraper interval (hours)
- Max concurrent applications
- Rate limit per hour

**Defaults for New Students:**
- Default automation mode
- Default max apps/day
- Require signed contract

---

## **📋 COMMON SCENARIOS & SOLUTIONS**

### **Scenario 1: New Student Registration**

**Question:** "We have 10 new students who just completed TQUK training. How do we get them started?"

**Answer:**
1. Export Excel template
2. Fill in student details from their records
3. Import Excel (all 10 students at once)
4. For each student:
   - Get/create Trac account
   - Verify Trac credentials
   - Upload signed contract
   - Set to Review Mode initially
   - Activate automation
5. Review first few applications to ensure quality
6. Switch to Auto-Submit mode once confident

**Time:** 30 minutes for all 10 students

---

### **Scenario 2: Student Requires Sponsorship**

**Question:** "Student needs sponsorship. How do we filter for those jobs?"

**Answer:**
1. Go to Student Settings tab
2. Select student
3. Check ✅ "Requires Sponsorship"
4. Save settings
5. System will ONLY show jobs with sponsorship available

---

### **Scenario 3: Check Application Before Submitting**

**Question:** "I want to check every application before it goes out."

**Answer:**
1. Set student to 🟡 Review Mode
2. Applications will appear in "Pending Review" tab
3. You'll see preview of supporting information
4. Click "Approve" when satisfied
5. Application submits immediately

---

### **Scenario 4: Fully Automate Trusted Student**

**Question:** "Student has good data, I trust the system. Can it run without me?"

**Answer:**
1. Set student to 🟢 Auto-Submit Mode
2. System will submit automatically
3. You'll see submissions in "Submission History"
4. Student gets email for each submission
5. You just monitor dashboard

---

### **Scenario 5: Interview Detected!**

**Question:** "Student got interview invitation. What happens?"

**Answer:**
**AUTOMATIC - NO STAFF INPUT NEEDED!**

1. System checks Trac inbox every 30 minutes
2. AI detects interview invitation
3. Extracts date, time, location
4. Creates interview record in database
5. Sends email to student: "Interview scheduled!"
6. Appears in staff dashboard interview calendar
7. Sends reminder 24 hours before interview

**You do nothing!** ✅

---

### **Scenario 6: Student Changes Trac Password**

**Question:** "Student changed their Trac password. How do we update?"

**Answer:**
1. Go to Student Settings
2. Select student
3. Scroll to "Trac Account" section
4. Click "Update Credentials"
5. Enter new password
6. System re-encrypts and stores
7. Automation resumes

---

## **⚠️ IMPORTANT NOTES**

### **Security:**
- ✅ All Trac passwords are encrypted (Fernet encryption)
- ✅ Encryption keys stored separately
- ✅ No plain-text passwords anywhere
- ✅ Staff cannot see passwords after entry

### **Contract Requirements:**
- ✅ Student must sign contract before automation
- ✅ Contract grants permission for job applications
- ✅ Student can revoke anytime
- ✅ All tracked in audit log

### **Quality Control:**
- ✅ Review Mode for first few applications
- ✅ Switch to Auto-Submit once confident
- ✅ Monitor success rates weekly
- ✅ Adjust settings based on performance

### **Data Sources:**
- Student application data from T21 training records
- TQUK completion dates from course completion
- Qualifications from student enrollment forms
- References can include T21 tutors

---

## **🚀 RECOMMENDED ROLLOUT PLAN**

### **Week 1: Pilot (5 Students)**
- Import 5 students manually
- Set all to Review Mode
- Approve every application personally
- Learn the system
- Identify any issues

### **Week 2: Expand (20 Students)**
- Import 20 students via Excel
- Keep in Review Mode
- Start identifying patterns
- Switch high-performers to Auto-Submit

### **Week 3: Scale (50+ Students)**
- Bulk Excel import
- Most students on Auto-Submit
- Review Mode only for new/complex cases
- Monitor dashboard daily

### **Week 4: Full Automation (All Students)**
- All students imported
- 90% on Auto-Submit mode
- 10% on Review Mode (complex cases)
- Weekly monitoring only

---

## **📊 SUCCESS METRICS TO TRACK**

Dashboard automatically tracks:
- ✅ Applications per student per day
- ✅ Interview invitation rate
- ✅ Success rate (applications → interviews → offers)
- ✅ Average time to interview invitation
- ✅ Top performing trusts
- ✅ Top hiring job titles

**Use these to:**
- Identify what works
- Adjust student preferences
- Focus on high-success trusts
- Optimize job search keywords

---

## **✅ SUMMARY: STAFF FLEXIBILITY**

**You have COMPLETE control:**

1. **Choose per student:** Review vs Auto-Submit
2. **Review any time:** Check applications before they go
3. **Edit content:** Modify AI-generated text
4. **Pause/Resume:** Control when automation runs
5. **Monitor everything:** Full dashboard visibility
6. **NO SURPRISES:** Email notifications for all actions

**The system adapts to YOUR workflow, not the other way around!** ✨

---

**Questions? Check the system dashboard or documentation!** 📚
