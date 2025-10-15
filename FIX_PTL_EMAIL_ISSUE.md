# 🔍 PTL EMAIL MISMATCH - DIAGNOSIS

**Issue:** Logged in as `admin@t21services.co.uk` but seeing 0 patients, even though 2 patients exist in Supabase under that email.

---

## 🎯 POSSIBLE CAUSES:

### **1. Email Case Sensitivity**
```
Database has: admin@t21services.co.uk
Session has: Admin@t21services.co.uk (capital A)
Match: NO ❌
```

### **2. Whitespace**
```
Database has: admin@t21services.co.uk
Session has: admin@t21services.co.uk  (trailing space)
Match: NO ❌
```

### **3. Session Not Set**
```
st.session_state.user_email = NOT SET
get_current_user_email() returns: demo@t21services.co.uk (default)
Match: NO ❌
```

---

## ✅ SOLUTION - CHECK DEBUG INFO:

**Refresh PTL page and click "🔍 DEBUG INFO"**

It will show:
1. `user_email` in session
2. `session_email` in session  
3. `get_current_user_email()` result
4. All patients with their emails

**Then we'll know the exact issue!**

---

## 🔧 QUICK FIX OPTIONS:

### **Option A: If email not set in session**
```python
# Add to staff_login.py after 2FA success
st.session_state.user_email = email.strip().lower()
st.session_state.session_email = email.strip().lower()
```

### **Option B: If case sensitivity issue**
```python
# Change query to case-insensitive
result = supabase.table('ptl_patients').select('*').ilike('user_email', user_email).execute()
```

### **Option C: If patients saved under different email**
```sql
-- Update all patients to correct email
UPDATE ptl_patients 
SET user_email = 'admin@t21services.co.uk' 
WHERE user_email LIKE '%admin%';
```

---

## 🚀 NEXT STEP:

**SHOW ME THE DEBUG INFO OUTPUT!**

Click the "🔍 DEBUG INFO" expander on PTL Dashboard and tell me what it says!
