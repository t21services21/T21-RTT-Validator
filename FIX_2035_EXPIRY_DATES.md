# FIX 2035 EXPIRY DATES

Date: October 25, 2025 11:48 AM
Issue: All users have expiry date 2035-01-01 (10 years!)
Status: FIXED - Updated code + created fix script

---

## ❌ **THE PROBLEM:**

**All users show:**
- Expires: 2035-01-01
- Days Remaining: 9999

**Why this happened:**
- Old code set 3650 days (10 years) for all users
- This was the default before you asked for control

---

## ✅ **WHAT I FIXED:**

### **1. Updated create_user Function**

**File:** `supabase_database.py`

**Changed:**
```python
# OLD (10 years for staff/admin)
"staff": 3650,
"admin": 3650,
"super_admin": 3650

# NEW (1 year for staff/admin, proper days for students)
"student_basic": 90,
"student_professional": 180,
"student_ultimate": 365,
"staff": 365,
"admin": 365,
"teacher": 365
```

**Also added:**
- `expiry_date` parameter to function
- You can now pass custom expiry when creating users
- Falls back to role-based defaults if not provided

---

### **2. Created Fix Script**

**File:** `fix_expiry_dates.py`

**What it does:**
- Finds all users with 2035+ expiry
- Calculates proper expiry based on role
- Updates their expiry dates
- Shows progress

**Proper expiry by role:**
- trial → 2 days
- student_basic → 90 days
- student_professional → 180 days
- student_ultimate → 365 days
- staff/admin/teacher → 365 days

---

## 🚀 **HOW TO FIX EXISTING USERS:**

### **Option 1: Run Fix Script (Recommended)**

1. **Open terminal** in project folder
2. **Run:**
   ```
   python fix_expiry_dates.py
   ```
3. **Type:** `yes` to confirm
4. **Script will:**
   - Find all users with 2035 expiry
   - Update to proper expiry based on role
   - Show progress
5. **Done!** All users fixed

---

### **Option 2: Manual Fix (One by One)**

1. **Go to:** Teaching & Assessment → All Students
2. **For each student:**
   - Click "Edit"
   - Change expiry date
   - Choose preset (90/180/365 days)
   - Save
3. **Repeat** for all students

---

## 📋 **WHAT WILL HAPPEN:**

### **After Running Fix Script:**

**Ijeoma (student_ultimate):**
- Created: 2025-10-25
- OLD expiry: 2035-01-01 (10 years)
- NEW expiry: 2026-10-25 (365 days from creation)

**Boluwaji (Module Tester):**
- Created: 2025-10-10
- OLD expiry: 2035-01-01 (10 years)
- NEW expiry: 2026-10-10 (365 days from creation)

**All future students:**
- student_basic → 90 days
- student_professional → 180 days
- student_ultimate → 365 days
- **OR custom date if you set it!**

---

## ✅ **AFTER DEPLOYMENT:**

### **New Students:**
When you register new students:
```
Account Type: [student_basic ▼]
⏰ Access expires in: 90 days (Basic)

☐ 🔧 Customize expiry date
[Pick any date you want]
```

**You control it!**
- Keep default (90/180/365 days)
- OR tick "Customize" and pick any date

---

### **Edit Existing Students:**
```
⏰ Access Expiry Date: [2025-12-25 📅]

Or choose preset:
- 90 days (Basic)
- 180 days (Professional)
- 365 days (Ultimate)
- Custom (use date above)
```

**You can change anytime!**

---

## 🎯 **SUMMARY:**

**Problem:** All users have 2035 expiry (10 years)  
**Cause:** Old code set 3650 days default  
**Fix 1:** Updated code to proper defaults  
**Fix 2:** Created script to fix existing users  
**Result:** Proper expiry dates for everyone  

**New defaults:**
- student_basic: 90 days
- student_professional: 180 days
- student_ultimate: 365 days
- staff/admin/teacher: 365 days

**Your control:**
- Set custom expiry when registering
- Change expiry anytime
- Extend or reduce as needed

---

## 🚀 **DEPLOY NOW:**

### **Step 1: Push to GitHub**
1. GitHub Desktop
2. Commit: "Fix expiry dates - remove 10-year default"
3. Push
4. Wait 5 minutes

### **Step 2: Run Fix Script**
1. Open terminal
2. Run: `python fix_expiry_dates.py`
3. Type: `yes`
4. Done! All existing users fixed

### **Step 3: Verify**
1. Refresh platform
2. Check user details
3. Should show proper expiry dates

---

NO MORE 2035 EXPIRY!
PROPER DEFAULTS NOW!
YOU CONTROL EVERYTHING!
RUN FIX SCRIPT TO UPDATE EXISTING USERS!
