# 🔍 DOCUMENT LIBRARY TROUBLESHOOTING

**Issue:** Can't see "📚 TQUK Document Library" in sidebar after deploy

---

## 🎯 **POSSIBLE CAUSES:**

### **1. SIDEBAR IS SCROLLABLE** ⭐ Most Likely!

**The Problem:**
- You have 19+ menu items
- Sidebar might not show all at once
- Need to scroll down in the sidebar!

**Solution:**
- Look at your LEFT SIDEBAR
- **SCROLL DOWN** in the sidebar
- Document Library is item #4 in the list
- Should be between "Teaching & Assessment" and "Clinical Workflows"

---

### **2. CACHE ISSUE**

**The Problem:**
- Browser cached old version
- Not showing new menu items

**Solution:**
```
Press Ctrl + Shift + R (Windows)
or
Cmd + Shift + R (Mac)
```

Or:
1. Clear browser cache
2. Close all tabs
3. Reopen platform

---

### **3. DEPLOYMENT NOT COMPLETE**

**The Problem:**
- Streamlit Cloud still deploying
- Takes 5-10 minutes

**Solution:**
- Wait 10 minutes after push
- Check Streamlit Cloud dashboard
- Look for "Running" status

---

### **4. WRONG ACCOUNT**

**The Problem:**
- Logged in as student
- Document library only for admin

**Solution:**
- Check what role you're logged in as
- Should be: admin, super_admin, or tester
- Logout and login with admin account

---

## 🔍 **DEBUG STEPS:**

### **Step 1: Check Your Role**
1. Login to platform
2. Look at top right - see your email
3. Go to "⚙️ Administration" or "My Account"
4. Check your role

**Should be one of:**
- super_admin
- admin
- tester
- staff

### **Step 2: Count Sidebar Items**
1. Look at sidebar
2. Count how many items you see
3. **Should see 19 items for admin**
4. If you see less, scroll down!

### **Step 3: Search for It**
1. Look in sidebar
2. Search for emoji: 📚
3. Should see TWO items with 📚:
   - "📚 TQUK Document Library" ← This one!
   - "📚 Level 3 Adult Care"

### **Step 4: Check Position**
**Document Library should be at position #4:**
1. 🏥 Patient Administration Hub
2. 🎓 Learning Portal
3. 👨‍🏫 Teaching & Assessment
4. **📚 TQUK Document Library** ← HERE!
5. 🏥 Clinical Workflows
6. ...

---

## 🚀 **IMMEDIATE SOLUTIONS:**

### **Solution A: Scroll Down in Sidebar**
- Most likely issue!
- Sidebar has scroll
- Document Library is item #4
- Scroll to see it

### **Solution B: Hard Refresh**
```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

### **Solution C: Clear Cache**
1. Browser settings
2. Clear cache and cookies
3. Reload platform

### **Solution D: Check Deployment**
1. Go to Streamlit Cloud
2. Check app status
3. Should say "Running"
4. If "Building" - wait 5 minutes

---

## 🎯 **ALTERNATIVE: USE FILES DIRECTLY**

**While troubleshooting, you can still get the documents:**

1. **Open File Explorer**
2. **Go to:** `C:\Users\User\CascadeProjects\T21-RTT-Validator\`
3. **Find files:**
   - TQUK_CDA_SUBMISSION_PACKAGE.md
   - LEVEL3_UNIT1_DUTY_OF_CARE_COMPLETE.md
   - LEVEL3_UNIT2_EQUALITY_DIVERSITY_COMPLETE.md
   - LEVEL3_UNIT3_PERSON_CENTRED_CARE_COMPLETE.md
   - LEVEL3_ASSESSMENT_PACK_TEMPLATES.md
4. **Open in Word**
5. **Add header** (T21 Services branding)
6. **Save as PDF**
7. **Send to TQUK**

---

## 📋 **CHECKLIST:**

- [ ] Scrolled down in sidebar
- [ ] Hard refreshed browser (Ctrl+Shift+R)
- [ ] Cleared cache
- [ ] Waited 10 minutes after deploy
- [ ] Checked logged in as admin
- [ ] Counted sidebar items (should be 19)
- [ ] Looked for 📚 emoji
- [ ] Checked Streamlit Cloud status

---

## 🔧 **IF STILL NOT SHOWING:**

**Let's add a direct link. I'll create a page file:**

The document library can also be accessed as a page:
`pages/tquk_documents.py`

This will make it appear in the sidebar automatically!

---

## 💡 **MOST LIKELY ISSUE:**

**The sidebar is scrollable and you need to scroll down to see item #4!**

**Look for this in your sidebar:**
```
👨‍🏫 Teaching & Assessment
📚 TQUK Document Library  ← Scroll to here!
🏥 Clinical Workflows
```

---

**TRY SCROLLING DOWN IN THE SIDEBAR FIRST!** 📜⬇️
