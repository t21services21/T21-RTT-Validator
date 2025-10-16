# 🚀 QUICK START - STAFF TESTING SETUP

**Time Required:** 5-10 minutes  
**Goal:** Create staff accounts and start testing

---

## ⚡ **FASTEST METHOD: RUN THE SCRIPT**

### **Option 1: Using Python Script (Automated)**

1. **Open Terminal/Command Prompt:**
   ```bash
   cd c:\Users\User\CascadeProjects\T21-RTT-Validator
   ```

2. **Run the Script:**
   ```bash
   python create_staff_accounts.py
   ```

3. **Script Will Create 4 Test Accounts:**
   - `staff1@t21services.co.uk` (Password: TestStaff123!)
   - `staff2@t21services.co.uk` (Password: TestStaff123!)
   - `teacher1@t21services.co.uk` (Password: TestTeacher123!)
   - `tester@t21services.co.uk` (Password: Tester123!)

4. **Share Credentials with Your Team:**
   - Send them their email and password
   - Share the platform URL
   - Give them the STAFF_TESTING_GUIDE.md

5. **Done!** ✅

---

## 🖱️ **ALTERNATIVE: MANUAL CREATION VIA ADMIN PANEL**

### **If Script Doesn't Work, Use Admin Panel:**

1. **Login as Admin:**
   - Go to your platform
   - Login with admin credentials

2. **Navigate to Admin Panel:**
   - Click: **⚙️ Administration**
   - Click: **🔧 Admin Panel** tab
   - Click: **👥 User Management** sub-tab

3. **Create New User:**
   - Look for "Create New User" or "Add User" button
   - Fill in:
     ```
     Email: staff1@t21services.co.uk
     Password: TestStaff123!
     Full Name: Test Staff 1
     Role: staff
     Status: Active
     Expiry: 365 days from now
     ```

4. **Grant Full Access:**
   - Go to **🔐 Module Access Control** tab
   - Find the user you just created
   - Check ALL modules (give them full access)

5. **Repeat for Each Staff Member:**
   - Create as many accounts as needed

---

## 📋 **WHAT TO DO AFTER CREATING ACCOUNTS**

### **1. Send Welcome Email to Each Staff Member:**

```
Subject: Test Account Created - T21 RTT Platform

Hi [Staff Name],

Your test account for the T21 RTT Platform is ready!

LOGIN CREDENTIALS:
Email: [their email]
Password: [their password]
URL: [your platform URL]

WHAT TO DO:
1. Login with your credentials
2. Download the testing guide: STAFF_TESTING_GUIDE.md
3. Test PRIORITY 1 features first (see guide)
4. Report any bugs using the bug template
5. Complete testing checklist

YOUR ROLE:
You have FULL ACCESS to all 55+ modules as staff/teacher.

FOCUS AREAS:
- Information Governance (NEW!)
- Partial Booking List (NEW!)
- 1000+ Question Exam (NEW!)
- Admin Panel (verify it works)
- All clinical features

Please start testing ASAP and report findings daily.

Thank you!
```

---

### **2. Share Testing Guide:**

Send them `STAFF_TESTING_GUIDE.md` which includes:
- What to test
- How to test
- Bug reporting template
- Testing checklist

---

### **3. Set Up Daily Standups:**

**Daily at [Time]:**
- What did you test yesterday?
- What bugs did you find?
- What will you test today?
- Any blockers?

---

## ✅ **VERIFICATION CHECKLIST**

Before staff start testing, verify:

- [ ] Staff accounts created successfully
- [ ] Passwords work (test login yourself)
- [ ] Staff have "staff" or "teacher" role
- [ ] Staff can access ALL modules
- [ ] Testing guide shared with team
- [ ] Bug reporting process explained
- [ ] Platform URL shared
- [ ] Contact method established (email/Slack)

---

## 🎯 **EXPECTED OUTCOMES**

### **Day 1 (Today):**
- [ ] All staff accounts created
- [ ] All staff can login
- [ ] Testing guide distributed
- [ ] Staff start testing PRIORITY 1 features

### **Day 2-3:**
- [ ] PRIORITY 1 features tested (IG, PBL, Exam)
- [ ] Bugs reported and documented
- [ ] Critical bugs fixed

### **Day 4-7:**
- [ ] All features tested
- [ ] Regression testing complete
- [ ] All bugs categorized (High/Medium/Low)
- [ ] Platform ready for production

---

## 🐛 **BUG TRACKING**

### **How to Track Bugs:**

**Option 1: Simple Spreadsheet**
```
Bug ID | Feature | Description | Priority | Status | Assigned To
001    | IG      | Module 1... | High     | Open   | Developer
002    | PBL     | Email not.. | Medium   | Fixed  | Developer
```

**Option 2: GitHub Issues**
- Create issue for each bug
- Label by priority (High/Medium/Low)
- Assign to developer
- Close when fixed

**Option 3: Dedicated Bug Tracker**
- Jira, Trello, or similar
- Create tickets for bugs
- Track progress

---

## 💡 **TESTING TIPS**

### **For You (Admin):**
1. Monitor staff progress daily
2. Prioritize critical bugs
3. Fix and redeploy quickly
4. Communicate fixes to team
5. Celebrate wins!

### **For Staff:**
1. Test systematically (don't skip around)
2. Document everything
3. Test edge cases
4. Think like an NHS user
5. Be thorough but efficient

---

## 📞 **SUPPORT**

### **If Staff Have Issues:**

**Can't Login:**
- Verify email/password
- Check role is "staff" or "teacher"
- Reset password if needed

**Can't Access Module:**
- Check module access permissions
- Grant access via Module Access Control tab

**Found Critical Bug:**
- Report immediately
- Mark as High Priority
- Test workaround if available

---

## 🎉 **YOU'RE READY!**

1. ✅ Run `python create_staff_accounts.py`
2. ✅ Share credentials with team
3. ✅ Give them STAFF_TESTING_GUIDE.md
4. ✅ Set up daily standups
5. ✅ Start testing!

---

**Expected Timeline:**
- **Today:** Create accounts (5-10 mins)
- **Tomorrow:** Staff start testing
- **This Week:** Complete all testing
- **Next Week:** Production ready!

---

**Good luck! Your platform is about to get thoroughly tested and be production-perfect!** 🚀
