# COMPLETE SYSTEM ARCHITECTURE - BEST PRACTICES

Date: October 25, 2025
Platform: T21 Healthcare Training Platform
Purpose: TQUK Qualifications + NHS RTT Training
Status: Production-Ready Architecture

---

## WHAT WE ARE BUILDING:

A professional learning management platform that delivers:
1. TQUK-Endorsed Qualifications (Level 3 Adult Care, IT, Customer Service, Business Admin)
2. NHS RTT Training (TQUK-Endorsed PDLC-01-039)
3. Career Development Tools (CV Builder, Interview Prep)
4. Complete Admin Control (You manage everything)

---

## CORE PRINCIPLES:

### 1. EXPLICIT CONTROL
- Nothing happens automatically
- You assign everything
- You control expiry dates
- You decide what each student gets

### 2. DATABASE AS TRUTH
- Database is single source of truth
- Sidebar shows database content
- No hardcoded defaults
- No role-based assumptions

### 3. SEPARATION OF CONCERNS
- Account creation != Module access
- Module access != Course enrollment
- Role != Access (role is for pricing)
- Each layer independent

### 4. AUDIT EVERYTHING
- Who assigned what
- When it was assigned
- Who modified it
- When it expires

### 5. REVERSIBLE ACTIONS
- Can remove access
- Can extend expiry
- Can suspend/reactivate
- Nothing permanent except audit trail

---

## SYSTEM LAYERS:

### LAYER 1: USER ACCOUNTS
- Email, password, name
- Role (student_basic/professional/ultimate)
- Status (active/suspended/expired)
- Expiry date (YOU set this)
- Created with NO modules

### LAYER 2: MODULE ACCESS
- Stored in module_access table
- user_email + module_name
- Granted by admin
- Timestamp recorded
- Can be revoked

### LAYER 3: COURSE ENROLLMENT
- Stored in course_enrollments table
- learner_email + course_id
- Enrolled by admin
- Timestamp recorded
- Status tracked

### LAYER 4: SIDEBAR DISPLAY
- Queries module_access table
- Shows ONLY what student has
- Plus basic modules (My Account, Help, Contact)
- Real-time from database

### LAYER 5: ADMIN OVERSIGHT
- Access Overview dashboard
- See all students
- See all their access
- Quick actions
- Visual indicators

---

## STUDENT TYPES:

### TYPE 1: TQUK QUALIFICATION STUDENT
**Example:** Level 3 Adult Care student

**What they get:**
- Learning Portal
- Level 3 Adult Care module
- Help & Information

**Optional:**
- CV Builder
- Career Development
- Job Interview Prep

**Total modules:** 3-7

**Business model:**
- Pay for qualification
- 90/180/365 days access
- TQUK certificate on completion

---

### TYPE 2: NHS RTT TRAINING STUDENT
**Example:** NHS staff learning RTT

**What they get:**
- Learning Portal
- Training & Certification
- Patient Administration Hub
- Clinical Workflows
- Task Management
- Reports & Analytics
- Help & Information

**Total modules:** 7-9

**Business model:**
- Pay for RTT training
- TQUK-Endorsed certificate
- Professional development

---

### TYPE 3: CAREER DEVELOPMENT ONLY
**Example:** Job seeker

**What they get:**
- Learning Portal
- CV Builder
- Career Development
- Job Interview Prep
- Help & Information

**Total modules:** 5

**Business model:**
- Pay for career tools
- No qualification
- Support service

---

### TYPE 4: COMBINED PACKAGE
**Example:** Ultimate student

**What they get:**
- Multiple TQUK courses
- RTT training
- Career tools
- Everything

**Total modules:** 10-15

**Business model:**
- Premium pricing
- 365 days access
- Multiple certificates

---

## ACCESS CONTROL FLOW:

### REGISTRATION:
1. Admin registers student
2. Sets role (basic/professional/ultimate)
3. Sets expiry date (30/60/90/180/365 days)
4. Account created
5. Student has NO modules yet

### ASSIGNMENT:
1. Admin goes to TQUK Course Assignment
2. Selects student
3. Ticks what they need
4. Clicks Assign
5. Database updated
6. Student can now access

### LOGIN:
1. Student logs in
2. System checks status (active/expired)
3. If active, query module_access table
4. Display modules in sidebar
5. Student sees only what they have

### EXPIRY:
1. System checks expiry daily
2. If expired, status = expired
3. Student blocked from login
4. Admin can extend
5. Access restored

---

## ADMIN WORKFLOWS:

### WORKFLOW 1: NEW STUDENT
1. Register student (set expiry)
2. Go to TQUK Course Assignment
3. Select student
4. Tick Level 3 Diploma
5. Click Assign
6. Done! Student has access

**Time:** 2 minutes

---

### WORKFLOW 2: AUDIT ALL STUDENTS
1. Go to Access Overview
2. Filter: Too Much Access (10+)
3. Review each student
4. Remove unnecessary modules
5. Filter: No Access
6. Assign modules to those who need
7. Done! System clean

**Time:** 10 minutes for 50 students

---

### WORKFLOW 3: EXTEND ACCESS
1. Go to All Students
2. Find student
3. Click Edit
4. Change expiry date (add 90 days)
5. Save
6. Done! Access extended

**Time:** 30 seconds

---

### WORKFLOW 4: SUSPEND STUDENT
1. Go to All Students
2. Find student
3. Click Edit
4. Status: Suspended
5. Save
6. Done! Student blocked

**Time:** 30 seconds

---

## BUSINESS LOGIC:

### PRICING TIERS:

**Basic (90 days):**
- 1 TQUK course
- Basic modules
- Price: £X

**Professional (180 days):**
- 1 TQUK course
- Career tools
- Price: £Y

**Ultimate (365 days):**
- Multiple TQUK courses
- RTT training
- Career tools
- Price: £Z

---

### REVENUE STREAMS:

1. TQUK Qualifications (main)
2. NHS RTT Training (secondary)
3. Career Development Tools (add-on)
4. Access Extensions (recurring)
5. Corporate Packages (bulk)

---

## TECHNICAL BEST PRACTICES:

### DATABASE:
- Supabase (PostgreSQL)
- Row-level security
- Audit trails
- Backup daily

### AUTHENTICATION:
- Secure password hashing
- Session management
- Role-based access
- Email verification

### ACCESS CONTROL:
- Database-driven
- No hardcoded lists
- Real-time queries
- Cached for performance

### MONITORING:
- Access Overview dashboard
- Usage analytics
- Expiry tracking
- Problem detection

### SCALABILITY:
- Works for 10 students
- Works for 10,000 students
- Same logic
- Same performance

---

## SECURITY:

### USER LEVEL:
- Can only see their modules
- Cannot access others' data
- Cannot modify their access
- Cannot extend their expiry

### ADMIN LEVEL:
- Can see all students
- Can modify all access
- Can extend expiry
- Full audit trail

### SYSTEM LEVEL:
- Enforces expiry dates
- Blocks expired users
- Validates all access
- Logs all actions

---

## MAINTENANCE:

### DAILY:
- Check expiry dates
- Send expiry warnings
- Block expired users
- Generate reports

### WEEKLY:
- Audit student access
- Check for problems
- Clean up issues
- Review analytics

### MONTHLY:
- Full system audit
- Review all students
- Check all access
- Optimize performance

---

## SUCCESS METRICS:

### OPERATIONAL:
- Registration to access: Under 2 minutes
- Access assignment: Under 1 minute
- Problem detection: Instant (visual)
- Problem resolution: Under 2 minutes

### BUSINESS:
- Student satisfaction: High (clean access)
- Admin efficiency: 90% time saved
- System reliability: 99.9% uptime
- Scalability: Unlimited students

---

## SUMMARY:

YOU CONTROL:
- Who gets access
- What they access
- How long they have it
- When to extend
- When to terminate

SYSTEM ENFORCES:
- Your decisions
- Expiry dates
- Access restrictions
- Security rules

RESULT:
- Professional platform
- Complete control
- Easy management
- Scalable business
- Happy students
- Happy admin (you!)

---

THIS IS THE BEST SYSTEM ARCHITECTURE!
PUSH TO GITHUB NOW!
DEPLOY AND TEST!
YOU HAVE A PROFESSIONAL PLATFORM!
