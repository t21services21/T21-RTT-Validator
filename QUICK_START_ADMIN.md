# 🚀 QUICK START - ADMIN SETUP

## 🔐 **YOUR ADMIN LOGIN DETAILS:**

### **Default Admin Account:**
```
Email:    admin@t21services.co.uk
Password: Admin123!
Role:     Super Administrator
```

⚠️ **IMPORTANT:** Change password after first login!

---

## 📋 **STEP-BY-STEP SETUP:**

### **STEP 1: CREATE YOUR ADMIN ACCOUNT**

Run this command **ONCE**:

```powershell
python setup_admin.py
```

**What this does:**
- Creates your Super Admin account
- Sets up the database
- Shows your login details
- Ready to use immediately!

**Output:**
```
============================================================
T21 ADMIN ACCOUNT SETUP
============================================================

✅ SUPER ADMIN ACCOUNT CREATED!

============================================================
YOUR LOGIN DETAILS:
============================================================
Email:    admin@t21services.co.uk
Password: Admin123!

Role: Super Administrator (Full Access)
Created: 08/10/2025 10:00:00
Expires: Never
```

---

### **STEP 2: START THE APP**

```powershell
py -3.12 -m streamlit run app.py
```

---

### **STEP 3: LOGIN**

1. App opens in browser
2. You'll see Login/Register page
3. Click "Login" tab
4. Enter:
   - Email: `admin@t21services.co.uk`
   - Password: `Admin123!`
5. Click "Login"

**You're in!** ✅

---

### **STEP 4: ACCESS ADMIN PANEL**

1. Look at sidebar
2. You'll see: `👤 Student Profile`
3. Shows: `✅ Super Administrator`
4. Scroll down sidebar menu
5. Click: `🔧 Admin Panel`

**You now have full control!** 🎯

---

## 📅 **HOW TO SET CUSTOM EXPIRY DATES:**

### **METHOD 1: Using Admin Panel (Web Interface)**

1. Go to `🔧 Admin Panel`
2. Click `👥 User Management` tab
3. Select user from dropdown
4. Click `➕ Extend License` button
5. You'll see **TWO OPTIONS**:

**Option 1: Extend by Days**
```
Days to extend: [30]
[Confirm Extension]
```
- Simple: Just add days to current expiry
- Example: Add 30 days

**Option 2: Set Custom Expiry Date/Time**
```
Expiry Date: [📅 31/12/2025]
Expiry Time: [🕐 23:59]
[Set Custom Expiry]
```
- Precise: Set exact date and time
- Example: 31/12/2025 at 23:59

**Example:**

Student needs access until end of year:
- Expiry Date: `31/12/2025`
- Expiry Time: `23:59`
- Click "Set Custom Expiry"
- ✅ Done!

---

### **METHOD 2: Using Python Script**

If you prefer command line:

```powershell
python set_custom_expiry.py
```

**Interactive prompts:**
```
Available users:
1. student@email.com
   Role: student_professional
   Current Expiry: 15/01/2026 12:00:00

Enter user email: student@email.com

Enter new expiry date/time:
Format: DD/MM/YYYY HH:MM
Example: 31/12/2025 23:59

New expiry (DD/MM/YYYY HH:MM): 31/12/2025 23:59

✅ EXPIRY DATE UPDATED!
User: student@email.com
New Expiry: 31/12/2025 23:59:00
Days Remaining: 84
```

---

## 👥 **HOW TO CREATE A STUDENT:**

### **Option 1: Student Self-Registers (Automatic Trial)**

Student goes to your platform:
1. Clicks "Register" tab
2. Enters email, password, name
3. Clicks "Register & Start Free Trial"
4. Gets **7 days trial** automatically!
5. You see them in Admin Panel

### **Option 2: You Create Them (Admin Panel)**

1. Go to `🔧 Admin Panel`
2. `👥 User Management` tab
3. Scroll to `➕ Create New User`
4. Fill in:
   - Email: `student@email.com`
   - Password: `Student123!`
   - Full Name: `John Smith`
   - Role: `student_professional` (or any other)
5. Click "Create User"

**Custom expiry during creation:**
- User is created with role's default duration
- Then use "Extend License" to set custom expiry

---

## ⚙️ **COMMON ADMIN TASKS:**

### **✅ Upgrade a Student:**

Student pays you £999 for Professional plan:

1. Admin Panel → User Management
2. Select: `student@email.com`
3. Click: `⬆️ Change Role`
4. Select: `student_professional`
5. Click: "Confirm Role Change"
6. ✅ Upgraded! (Gets 6 months access)

**Set custom expiry after upgrade:**
7. Click: `➕ Extend License`
8. Option 2: Set Custom Expiry
9. Date: `08/04/2026` (6 months from now)
10. Time: `23:59`
11. ✅ Done!

---

### **⏸️ Suspend a User:**

User violates terms:

1. Admin Panel → User Management
2. Select: `baduser@email.com`
3. Click: `⏸️ Suspend`
4. Enter reason: `Violation of terms - account sharing`
5. Click: "Confirm Suspension"
6. ✅ User immediately blocked!

User **cannot login** until unsuspended.

---

### **➕ Extend License (Compensation):**

Student had technical issue, you give 1 week free:

1. Admin Panel → User Management
2. Select: `student@email.com`
3. Click: `➕ Extend License`
4. Option 1: Days to extend: `7`
5. Click: "Confirm Extension"
6. ✅ 7 days added to their expiry!

---

### **🎁 Give Special Access:**

Basic student needs certification exam (special case):

1. Admin Panel → `🔑 Permissions` tab
2. Select user: `student@email.com`
3. Grant Permission section
4. Feature Name: `certification_exam`
5. Click "Grant"
6. ✅ Student can now access certification!

---

### **⚠️ Terminate Account (Permanent):**

**ONLY Super Admin can do this!**

Serious violation (fraud, abuse):

1. Admin Panel → User Management
2. Select: `frauduser@email.com`
3. Click: `⚠️ Terminate`
4. Enter reason: `Fraudulent payment detected`
5. Check: "I understand this is permanent"
6. Click: "CONFIRM TERMINATION"
7. ⚠️ Account PERMANENTLY disabled!

**Cannot be undone!**

---

## 📊 **VIEW ANALYTICS:**

### **Dashboard:**

Admin Panel → `📊 Dashboard` tab

Shows:
- Total users
- Active/expired/suspended counts
- Total revenue
- User type breakdown
- Recent activity

### **Revenue:**

Admin Panel → `💰 Revenue & Analytics` tab

Shows:
- Total revenue: `£89,900`
- Active paying students: `90`
- Revenue breakdown:
  - Basic: 40 students = £23,960
  - Professional: 30 students = £29,970
  - Ultimate: 20 students = £29,980

### **Audit Log:**

Admin Panel → `📜 Audit Log` tab

Shows all actions:
```
08/10/2025 10:30 - CREATE_USER - admin@t21 → student@email.com
08/10/2025 11:45 - SUSPEND_USER - admin@t21 → baduser@email.com
08/10/2025 14:20 - EXTEND_LICENSE - admin@t21 → student@email.com (+30 days)
08/10/2025 16:55 - GRANT_PERMISSION - admin@t21 → student@email.com (certification_exam)
```

**Complete accountability!**

---

## 🎯 **EXPIRY DATE EXAMPLES:**

### **Example 1: Student Pays for 3 Months**

**Today:** 08/10/2025

**Want them to have access until:** 08/01/2026

**Method:**
1. Select student
2. Extend License → Option 2
3. Date: `08/01/2026`
4. Time: `23:59`
5. ✅ Set!

**They can access until:** 08/01/2026 at 23:59

---

### **Example 2: End of Year Access**

**Want:** All students to expire on same date (31/12/2025)

**For each student:**
1. Select student
2. Extend License → Option 2
3. Date: `31/12/2025`
4. Time: `23:59`
5. ✅ Done!

**All expire:** 31/12/2025 at 23:59

---

### **Example 3: Lifetime Access**

**Want:** Student to have very long access (10 years)

**Method:**
1. Select student
2. Extend License → Option 2
3. Date: `08/10/2035` (10 years from now)
4. Time: `23:59`
5. ✅ Set!

**They have:** 3,652 days (10 years)

---

## 📝 **SUMMARY:**

**YOUR ADMIN LOGIN:**
```
Email:    admin@t21services.co.uk
Password: Admin123!
```

**TO GET STARTED:**
1. `python setup_admin.py` (run once)
2. `py -3.12 -m streamlit run app.py`
3. Login with admin credentials
4. Go to Admin Panel
5. Start managing users!

**TO SET CUSTOM EXPIRY:**
- **Web UI:** Admin Panel → User Management → Extend License → Option 2
- **Script:** `python set_custom_expiry.py`

**BOTH METHODS LET YOU:**
✅ Set exact date (DD/MM/YYYY)
✅ Set exact time (HH:MM)
✅ See days remaining
✅ Get warnings if date is past

---

## 🎉 **YOU'RE READY!**

Run setup and start managing your platform! 🚀
