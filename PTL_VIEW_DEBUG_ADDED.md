# 🔧 PTL VIEW DEBUG INFO ADDED!

**Date:** October 15, 2025, 8:48 AM  
**Status:** DEBUG INFO ADDED TO DIAGNOSE ISSUE ✅

---

## 🎯 THE ISSUE:

**User reports:**
- Patient adds successfully ✅
- Success message shows ✅
- But patient not appearing in "Full Patient List" ❌

---

## 🔧 WHAT I ADDED:

### **Debug Expander in Patient List:**

When no patients show, you'll now see:

```
ℹ️ No patients on PTL. Add patients using the 'Add Patient' tab.

🔧 Debug Info (click to expand)
├─ Total patients in database: 0
├─ User email: demo@t21services.co.uk
└─ Sample patient data: {...}
```

---

## 🎯 HOW TO USE DEBUG INFO:

### **Step 1: Add a Patient**
1. Go to PTL → Add Patient
2. Fill in form
3. Click "Add to PTL"
4. See success message ✅

### **Step 2: Check Full Patient List**
1. Go to "Full Patient List" tab
2. If no patients show, click "🔧 Debug Info"

### **Step 3: Read Debug Info**

**Scenario A: Total patients = 0**
```
Total patients in database: 0
User email: student@example.com
```
**Diagnosis:** Patient not being saved at all
**Solution:** Check console logs for save errors

**Scenario B: Total patients > 0 but not showing**
```
Total patients in database: 1
User email: student@example.com
Sample patient data: {
    "patient_id": "PTL_123",
    "patient_name": "John Smith",
    "user_email": "different@example.com"  ← DIFFERENT EMAIL!
}
```
**Diagnosis:** Patient saved under different user email
**Solution:** User email mismatch issue

**Scenario C: Total patients > 0 and correct email**
```
Total patients in database: 1
User email: student@example.com
Sample patient data: {
    "patient_id": "PTL_123",
    "patient_name": "John Smith",
    "user_email": "student@example.com"  ← SAME EMAIL!
}
```
**Diagnosis:** Search/filter issue
**Solution:** Check search_patients() function

---

## 🎯 POSSIBLE CAUSES:

### **1. Supabase Table Missing**
- Patients saving to session/file only
- Not persisting to Supabase
- Lost on page refresh

**Check:** Console logs for "Supabase save failed"

### **2. User Email Mismatch**
- Patient saved with one email
- Loading with different email
- Data isolation working TOO well!

**Check:** Debug info shows different emails

### **3. Search Function Issue**
- Patients exist in database
- But search_patients() not finding them
- Filter or query problem

**Check:** Debug shows patients exist

### **4. Session Storage Not Loading**
- Patients in session storage
- But load_ptl() not checking session
- Already fixed in ptl_system.py!

---

## 🚀 NEXT STEPS:

### **After Adding Patient:**

1. **Go to Full Patient List**
2. **If no patients show, click "🔧 Debug Info"**
3. **Check the output:**
   - Total patients = 0? → Save is failing
   - Total patients > 0? → Load/filter issue
   - Different email? → User email problem

4. **Check Console Logs:**
   - Look for "✅ Patient saved to Supabase"
   - Or "⚠️ Supabase save failed"
   - Or "✅ Patient saved to session storage"

5. **Report Back:**
   - What does debug info show?
   - What do console logs say?
   - Then we can fix the exact issue!

---

## 💡 LIKELY ISSUE:

### **My Guess:**

**Supabase table `ptl_patients` doesn't exist yet!**

**What's happening:**
1. Patient saves to session storage ✅
2. Page refreshes (st.rerun())
3. Session cleared
4. load_ptl() tries Supabase
5. Supabase returns empty (table doesn't exist)
6. No patients show

**Solution:**
- Create `ptl_patients` table in Supabase
- Or patients will only persist in session (temporary)

---

## 🎯 TO CREATE SUPABASE TABLE:

### **SQL to Run in Supabase:**

```sql
CREATE TABLE ptl_patients (
    id SERIAL PRIMARY KEY,
    patient_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    patient_name TEXT,
    nhs_number TEXT,
    specialty TEXT,
    referral_date TEXT,
    referral_source TEXT,
    clock_start_date TEXT,
    pathway_type TEXT,
    priority TEXT,
    current_status TEXT,
    consultant TEXT,
    contact_number TEXT,
    rtt_code TEXT,
    clock_status TEXT,
    notes TEXT,
    added_date TEXT,
    last_updated TEXT,
    appointments JSONB DEFAULT '[]'::jsonb,
    events JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_ptl_user_email ON ptl_patients(user_email);
CREATE INDEX idx_ptl_patient_id ON ptl_patients(patient_id);
```

---

## 🚀 TEST WITH DEBUG:

```bash
streamlit run app.py
```

**Then:**
1. Add a patient
2. Go to Full Patient List
3. Click "🔧 Debug Info"
4. **Tell me what it says!**

---

**T21 Services Limited | Company No: 13091053**  
**Debug Info Added - Let's Find The Issue!** ✅

---

**DEBUG INFO WILL SHOW US THE PROBLEM!** ✅🔧🔍
