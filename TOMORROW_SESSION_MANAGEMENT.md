# 🔒 SESSION MANAGEMENT - TODO TOMORROW

**Date:** 9th October 2025, 22:33  
**Priority:** HIGH - Implement before launch  
**Time Required:** 1-2 hours

---

## 🎯 REQUIREMENT

**User Request:**
"Make sure users can only login on one device at once"

**Why This Matters:**
- Prevents account sharing
- Increases security
- Ensures proper licensing (each user = one login)
- Prevents revenue loss from shared accounts

---

## 📊 CURRENT STATE

**What We Have:**
- ✅ Session timeout (15 minutes inactivity)
- ✅ Session state in Streamlit
- ✅ Password hashing
- ✅ 2FA support

**What's Missing:**
- ❌ Database-backed session tracking
- ❌ Single device enforcement
- ❌ Session invalidation on new login

---

## 🔧 IMPLEMENTATION PLAN

### **Step 1: Database Schema Update (15 min)**

Add to Supabase `users` table:
```sql
-- Add session tracking columns
ALTER TABLE users ADD COLUMN active_session_id TEXT;
ALTER TABLE users ADD COLUMN session_device TEXT;
ALTER TABLE users ADD COLUMN session_ip TEXT;
ALTER TABLE users ADD COLUMN last_session_start TIMESTAMP;

-- Create index for faster session lookups
CREATE INDEX idx_users_session ON users(active_session_id);
```

### **Step 2: Update Login Functions (30 min)**

**File:** `supabase_database.py`

Add new function:
```python
import uuid
import hashlib

def create_user_session(email, device_info=None, ip_address=None):
    """Create new session and invalidate old ones"""
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Update user with new session
    supabase.table('users').update({
        'active_session_id': session_id,
        'session_device': device_info or 'Unknown',
        'session_ip': ip_address or 'Unknown',
        'last_session_start': 'now()',
        'last_login': 'now()'
    }).eq('email', email).execute()
    
    return session_id

def validate_user_session(email, session_id):
    """Check if session is still valid"""
    user = supabase.table('users').select('active_session_id').eq('email', email).execute()
    
    if not user.data:
        return False
    
    # Check if session matches
    return user.data[0].get('active_session_id') == session_id

def invalidate_user_session(email):
    """Clear user session on logout"""
    supabase.table('users').update({
        'active_session_id': None
    }).eq('email', email).execute()
```

### **Step 3: Update Login Pages (20 min)**

**Files:** `pages/student_login.py`, `pages/staff_login.py`, `pages/nhs_login.py`

After successful login:
```python
# Generate session
import platform
device_info = f"{platform.system()} {platform.release()}"
session_id = create_user_session(email, device_info)

# Store in session state
st.session_state.session_id = session_id
st.session_state.logged_in = True
st.session_state.user_email = email
```

### **Step 4: Add Session Validation (20 min)**

**File:** `app.py`

Add after session state initialization:
```python
# Validate session on each page load
if st.session_state.logged_in:
    email = st.session_state.get('user_email')
    session_id = st.session_state.get('session_id')
    
    # Check if session is still valid
    if not validate_user_session(email, session_id):
        # Session invalid - someone else logged in
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.session_id = None
        st.error("⚠️ Your session has been ended because a login was detected from another device.")
        st.stop()
```

### **Step 5: Update Logout (10 min)**

**File:** `sidebar_manager.py`

In logout button:
```python
if st.button("🚪 Logout", key="btn_logout", ...):
    # Invalidate session in database
    email = st.session_state.get('user_email')
    if email:
        invalidate_user_session(email)
    
    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
```

---

## 🧪 TESTING CHECKLIST

**Test Scenarios:**
- [ ] Login on Device 1
- [ ] Try login on Device 2 (should kick Device 1)
- [ ] Verify Device 1 shows "session ended" message
- [ ] Logout on Device 2
- [ ] Login again on Device 1 (should work)
- [ ] Close browser without logout
- [ ] Login again (should work - session replaced)
- [ ] Test with 2FA enabled
- [ ] Test with all 3 portals (Student, Staff, NHS)

---

## ⚠️ EDGE CASES TO HANDLE

### **Case 1: Session Expires**
- Current: 15-minute timeout
- New: Also clear `active_session_id` in database
- Solution: Add cleanup to timeout check

### **Case 2: Browser Crash**
- User closes browser without logout
- Session still active in database
- Solution: Allow new login to replace old session (already handled)

### **Case 3: Network Issues**
- Session validation fails due to network
- Solution: Retry 3 times before kicking user out

### **Case 4: Multiple Tabs Same Browser**
- User opens multiple tabs
- Same session ID
- Solution: Allow (same device, same user)

---

## 📋 IMPLEMENTATION ORDER

**Tomorrow Morning:**
1. ✅ Run SQL to add columns (5 min)
2. ✅ Add session functions to `supabase_database.py` (20 min)
3. ✅ Update login pages (20 min)
4. ✅ Add session validation to `app.py` (15 min)
5. ✅ Update logout function (10 min)
6. ✅ Test thoroughly (30 min)
7. ✅ Push to production (5 min)

**Total Time: ~1.5 hours**

---

## 💰 BUSINESS VALUE

**Why This Matters:**

**Without Session Management:**
- 1 account shared between 5 students
- You earn: £1,299 (1 × Tier 2)
- You serve: 5 students
- Loss: £5,196 (4 × £1,299)

**With Session Management:**
- Each student needs own account
- You earn: £6,495 (5 × £1,299)
- Prevents revenue loss: **+£5,196 per shared account!**

**If 20% of users share accounts:**
- 100 users = 20 shared accounts
- Lost revenue: £103,920/year
- **This feature pays for itself immediately!**

---

## 🎯 PRIORITY LEVEL

**CRITICAL - Do Before Launch**

**Why:**
- Prevents account sharing
- Protects revenue
- Industry standard security
- Expected by enterprise customers

**When:**
- Tomorrow morning (fresh mind)
- Before marketing launch
- After logo/branding (already done tonight)

---

## 📝 NOTES

**User asked at:** 22:33 (after 14.5 hours of work)  
**Recommendation:** Sleep now, implement tomorrow  
**Reason:** Complex security feature needs fresh brain  
**Status:** Documented, ready to implement tomorrow

---

**Tomorrow morning: Read this doc, implement in 1.5 hours, launch!** 🚀
