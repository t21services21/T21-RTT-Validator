# 🔧 SUPABASE TABLE SETUP INSTRUCTIONS

## ⚠️ IMPORTANT: Medical Secretary AI needs these tables!

Your Medical Secretary AI is currently trying to use Supabase tables that don't exist yet. Follow these steps to create them:

---

## 📋 **STEP-BY-STEP INSTRUCTIONS:**

### **Step 1: Open Supabase Dashboard**
1. Go to: https://supabase.com/dashboard
2. Login to your account
3. Select your **T21 Services** project

---

### **Step 2: Open SQL Editor**
1. In the left sidebar, click **"SQL Editor"**
2. Click **"New Query"** button (top right)

---

### **Step 3: Copy & Paste SQL**
1. Open the file: `CREATE_SUPABASE_TABLES.sql` (in this folder)
2. **Copy ALL the SQL code** (Ctrl+A, Ctrl+C)
3. **Paste** into the Supabase SQL Editor (Ctrl+V)

---

### **Step 4: Run the SQL**
1. Click the **"RUN"** button (or press Ctrl+Enter)
2. Wait for execution to complete (5-10 seconds)
3. You should see: **"SUCCESS! All Medical Secretary tables created!"**

---

### **Step 5: Verify Tables Created**

**Check Tables Exist:**
1. In left sidebar, click **"Table Editor"**
2. You should now see:
   - ✅ `diary_events` table
   - ✅ `correspondence` table

**Check Columns:**

**diary_events table should have:**
- id
- event_id
- user_email
- consultant
- date
- start_time
- end_time
- event_type
- location
- description
- created_date
- updated_date

**correspondence table should have:**
- id
- letter_id
- user_email
- letter_type
- patient_name
- nhs_number
- gp_name
- gp_address
- clinic_date
- consultant_name
- diagnosis
- treatment_plan
- content
- status
- created_date
- updated_date

---

### **Step 6: Test the Feature**
1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Add Supabase fallback for Medical Secretary"
   git push origin main
   ```

2. **Wait 30-60 seconds** for Streamlit Cloud to redeploy

3. **Go to Medical Secretary AI** in your app

4. **Try adding a diary event** - should now work! ✅

---

## ✅ **BENEFITS OF SUPABASE STORAGE:**

### **✅ Persistent Storage**
- Data survives logout/login
- Never loses information
- Professional database

### **✅ Multi-User Support**
- Each user sees only their own data
- Row Level Security enabled
- Secure and private

### **✅ Real-Time Access**
- Access from anywhere
- Always up-to-date
- Cloud-based

### **✅ Scalable**
- Handles thousands of users
- Fast queries with indexes
- Production-ready

---

## 🔒 **SECURITY FEATURES:**

**Row Level Security (RLS) is enabled:**
- Users can **only** see their own diary events
- Users can **only** see their own correspondence
- No one can see other users' data
- Automatic email filtering

---

## 🚨 **TROUBLESHOOTING:**

### **Error: "relation already exists"**
✅ **This is fine!** Tables already created, just continue.

### **Error: "permission denied"**
❌ Check you're logged in as the project owner
❌ Check you selected the correct project

### **Tables not showing in Table Editor**
1. Refresh the page
2. Clear browser cache
3. Check SQL ran successfully

---

## 📊 **WHAT EACH TABLE DOES:**

### **📅 diary_events**
**Purpose:** Store consultant diary events
**Used by:** Medical Secretary AI - Intelligent Diary Management
**Features:**
- Track consultant appointments
- Manage clinic schedules
- Detect time conflicts
- AI-powered scheduling

### **📧 correspondence**
**Purpose:** Store drafted medical letters
**Used by:** Medical Secretary AI - Correspondence Management
**Features:**
- Draft clinic letters
- Store patient correspondence
- Track letter status
- Professional NHS formatting

---

## 🎯 **NEXT STEPS AFTER SETUP:**

1. ✅ Tables created in Supabase
2. ✅ Push code to GitHub
3. ✅ Wait for Streamlit redeploy
4. ✅ Test Medical Secretary AI
5. ✅ Add diary events (they'll persist!)
6. ✅ Draft letters (they'll be saved!)

---

## 💡 **IMPORTANT NOTES:**

**Current Behavior:**
- ❌ Local JSON files (temporary, lost on logout)

**After Supabase Setup:**
- ✅ Persistent database (permanent storage)
- ✅ Multi-user support (each user's own data)
- ✅ Secure (Row Level Security)
- ✅ Professional (cloud database)

---

## 🚀 **READY TO CREATE TABLES?**

1. Open: `CREATE_SUPABASE_TABLES.sql`
2. Go to Supabase SQL Editor
3. Paste the SQL
4. Click RUN
5. Done! ✅

---

**Questions? Check the SQL file for complete table definitions!**

**T21 Services - Professional Database Setup**
**October 15, 2025**
