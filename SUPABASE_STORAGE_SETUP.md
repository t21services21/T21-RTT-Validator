# 📦 SUPABASE STORAGE SETUP FOR FILE UPLOADS

## 🎯 Purpose
Enable teachers to upload learning materials directly (PDF, Word, Excel, PowerPoint, etc.) instead of just linking to external URLs.

---

## ✅ QUICK SETUP (5 MINUTES)

### **Step 1: Open Supabase Dashboard**
1. Go to: https://supabase.com/dashboard
2. Login to your account
3. Select your **T21 Services** project

---

### **Step 2: Create Storage Bucket**
1. In the left sidebar, click **"Storage"**
2. Click **"New Bucket"** button (top right)
3. Enter details:
   - **Name:** `learning_materials`
   - **Public bucket:** ✅ **CHECK THIS BOX** (Important!)
   - Click **"Create Bucket"**

---

### **Step 3: Configure Bucket Policies**
1. Click on the `learning_materials` bucket you just created
2. Click **"Policies"** tab at the top
3. Click **"New Policy"** button

#### **Policy 1: Allow Public Read Access**
- **Policy Name:** `Public Read Access`
- **Allowed Operation:** `SELECT`
- **Target Roles:** `public`
- **Policy Definition:**
  ```sql
  true
  ```
- Click **"Save Policy"**

#### **Policy 2: Allow Authenticated Users to Upload**
- **Policy Name:** `Authenticated Upload`
- **Allowed Operation:** `INSERT`
- **Target Roles:** `authenticated`
- **Policy Definition:**
  ```sql
  (bucket_id = 'learning_materials')
  ```
- Click **"Save Policy"**

---

### **Step 4: Verify Setup**
1. Click **"Files"** tab
2. Try uploading a test file
3. If successful, setup is complete! ✅

---

## 🎯 WHAT THIS ENABLES

### **Before Setup:**
- ❌ Only external URLs (Google Drive, OneDrive, etc.)
- ❌ Teachers must upload elsewhere first
- ❌ Extra steps, less convenient

### **After Setup:**
- ✅ Direct file upload (PDF, Word, Excel, PowerPoint, ZIP, etc.)
- ✅ Files stored in your Supabase cloud
- ✅ Automatic public URLs generated
- ✅ One-click upload for teachers
- ✅ Professional file hosting

---

## 📤 SUPPORTED FILE TYPES

- **📄 Documents:** PDF, Word (.docx, .doc)
- **📊 Spreadsheets:** Excel (.xlsx, .xls)
- **📊 Presentations:** PowerPoint (.pptx, .ppt)
- **📝 Text Files:** .txt
- **📦 Archives:** .zip

---

## 🔒 SECURITY

### **Public Bucket = Safe?**
✅ **YES!** Here's why:
- Files are only accessible if you know the URL
- URLs contain random strings (hard to guess)
- Only metadata is public (not sensitive)
- Learning materials are meant to be shared with students

### **Who Can Upload?**
- ✅ Only authenticated users (logged in)
- ✅ Teachers with proper access
- ❌ Anonymous users cannot upload

### **Who Can Download?**
- ✅ Anyone with the URL
- ✅ Perfect for students to access materials
- ✅ No login required to download

---

## 📊 FILE STORAGE LIMITS

### **Supabase Free Tier:**
- **Storage:** 1 GB free
- **Bandwidth:** 2 GB/month free
- **Files:** Unlimited number of files

### **Supabase Pro Tier ($25/month):**
- **Storage:** 100 GB
- **Bandwidth:** 200 GB/month
- **Everything else unlimited**

### **For T21 Services:**
- Start with free tier
- Most PDF/Word files are 1-5 MB
- 1 GB = ~200-1000 documents
- Upgrade when needed

---

## 🚀 TESTING AFTER SETUP

### **Step 1: Push Code to GitHub**
```bash
git add .
git commit -m "Add direct file upload for learning materials"
git push origin main
```

### **Step 2: Wait for Deployment** (30-60 seconds)

### **Step 3: Test Upload**
1. Navigate to: **🎓 Learning Portal**
2. Go to **Materials** tab
3. Select **"📤 Upload File Directly"**
4. Click **"Upload File"** button
5. Select a PDF or Word document
6. Fill in title, category, etc.
7. Click **"📤 Upload Material"**
8. Should say: **"✅ File uploaded to cloud storage!"**

### **Step 4: Verify in Supabase**
1. Go to Supabase dashboard
2. Click **"Storage"** → **"learning_materials"**
3. Click **"Files"** tab
4. You should see your uploaded file! ✅

---

## 🎯 HOW IT WORKS

### **Teacher Uploads File:**
```
1. Teacher clicks "Upload File Directly"
2. Selects PDF/Word/Excel file
3. File uploaded to: learning_materials/user@email.com/filename.pdf
4. System generates public URL
5. URL saved to database
6. Students can download anytime
```

### **Student Downloads File:**
```
1. Student sees material in Learning Portal
2. Clicks "Download" button
3. File downloads from Supabase Storage
4. No login required
5. Fast & reliable
```

---

## ⚠️ TROUBLESHOOTING

### **Error: "Storage not configured"**
✅ Create the `learning_materials` bucket in Supabase Storage

### **Error: "Access denied"**
✅ Make sure bucket is **PUBLIC**
✅ Check policies are created correctly

### **Upload button doesn't appear**
✅ Push code to GitHub first
✅ Wait for Streamlit Cloud to redeploy

### **File uploads but students can't download**
✅ Make sure bucket is PUBLIC
✅ Check "Public Read Access" policy exists

---

## 🎉 BENEFITS

### **✅ For Teachers:**
- Upload files in seconds
- No need for Google Drive, OneDrive, etc.
- All materials in one place
- Professional cloud storage

### **✅ For Students:**
- Easy one-click downloads
- Fast access to materials
- No external links that break
- Always available

### **✅ For T21 Services:**
- Professional platform
- Complete control over files
- No dependency on external services
- Scalable cloud storage

---

## 📝 NEXT STEPS

1. ✅ Create `learning_materials` bucket
2. ✅ Make it public
3. ✅ Add policies
4. ✅ Push code to GitHub
5. ✅ Test file upload
6. ✅ Share with teachers!

---

## 💡 ALTERNATIVE: Keep Using URLs

**Don't want to setup storage?**

Teachers can still use the **"🔗 Link to External URL"** option to link to:
- Google Drive
- OneDrive
- Dropbox
- Any other cloud storage

Both options work! Choose what's best for you. ✅

---

**T21 Services - Complete Learning Management System**
**October 15, 2025**
