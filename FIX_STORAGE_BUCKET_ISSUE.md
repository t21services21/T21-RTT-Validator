# 🔧 **FIX: Storage Bucket Not Configured**

## **❌ THE PROBLEM:**

You're seeing this error:
```
⚠️ Cloud storage not configured yet. Using temporary URL.

To enable file uploads:
1. Go to your Supabase dashboard
2. Click "Storage" in left sidebar
3. Create a bucket called "learning_materials"
4. Make it public
5. Enable file uploads
```

## **🔍 WHY THIS HAPPENED:**

The SQL scripts created **database tables** but NOT **storage buckets**.

**Storage buckets CANNOT be created with SQL** - you must create them manually in the Supabase Dashboard!

---

## **✅ SOLUTION: CREATE STORAGE BUCKETS**

### **STEP 1: Go to Supabase Dashboard**

1. Open browser
2. Go to: https://supabase.com/dashboard/
3. Login to your account
4. Select project: **T21-RTT-Validator**

---

### **STEP 2: Create Storage Bucket**

1. In left sidebar, click **"Storage"**
2. Click **"New bucket"** button (top right)

**Bucket Configuration:**

```
Bucket Name: learning_materials
Public bucket: ✅ YES (toggle ON)
File size limit: 200 MB
Allowed MIME types: Leave as default (all allowed)
```

3. Click **"Create bucket"**

---

### **STEP 3: Verify Bucket Created**

You should now see:
```
📁 learning_materials (public)
Created just now
0 objects
```

---

### **STEP 4: Set Up Policies (Optional - for security)**

1. Click on **"learning_materials"** bucket
2. Go to **"Policies"** tab
3. Click **"New Policy"**

**Create 4 policies:**

**Policy 1: Public Read**
```
Name: Public Access
Operation: SELECT
Policy: (bucket_id = 'learning_materials')
```

**Policy 2: Teachers Can Upload**
```
Name: Teachers can upload
Operation: INSERT
Policy: (bucket_id = 'learning_materials' AND auth.role() = 'authenticated')
```

**Policy 3: Users Can Update Own Files**
```
Name: Update own files
Operation: UPDATE
Policy: (bucket_id = 'learning_materials' AND owner = auth.uid())
```

**Policy 4: Users Can Delete Own Files**
```
Name: Delete own files
Operation: DELETE
Policy: (bucket_id = 'learning_materials' AND owner = auth.uid())
```

---

### **STEP 5: Test Upload**

1. Go back to your T21 platform
2. Navigate to: **Learning Portal → Learning Materials**
3. Click **"Upload Material"**
4. Choose **"Upload File Directly"**
5. Select a PDF file
6. Fill in Title, Category, etc.
7. Click **"Upload"**

**Expected Result:**
```
✅ File uploaded to cloud storage!
✅ Material uploaded successfully!
🎈 (balloons)
```

---

## **📊 QUICK FIX CHECKLIST:**

- [ ] Login to Supabase Dashboard
- [ ] Go to Storage section
- [ ] Create "learning_materials" bucket
- [ ] Set to PUBLIC
- [ ] Set file size limit to 200MB
- [ ] Click Create
- [ ] Test upload in platform
- [ ] Should work now! ✅

---

## **🔍 IF STILL NOT WORKING:**

### **Check 1: Bucket Exists**
In Supabase Storage, you should see:
```
📁 learning_materials (public)
```

### **Check 2: Bucket is Public**
Next to bucket name, it should say **(public)**

### **Check 3: File Size**
Make sure file is under 200MB

### **Check 4: Connection**
Run this SQL in Supabase SQL Editor:
```sql
SELECT * FROM storage.buckets WHERE name = 'learning_materials';
```

Should return 1 row.

---

## **🎯 EXPECTED FOLDER STRUCTURE:**

After uploads, your bucket will look like:
```
learning_materials/
├── admin@t21services.co.uk/
│   ├── RTT_CODES-ALL-PAGE (3).pdf
│   ├── Week1_Lecture.pdf
│   └── Assignment1.docx
├── teacher1@example.com/
│   └── slides.pptx
└── teacher2@example.com/
    └── notes.pdf
```

Each teacher's files are organized in their own folder.

---

## **💡 WHY MANUAL CREATION?**

**Supabase Storage Buckets:**
- ❌ Cannot be created via SQL
- ✅ Must use Dashboard UI
- ✅ Or use Supabase REST API (advanced)

**Database Tables:**
- ✅ Can be created via SQL (we did this)
- ✅ Already exist

**You only need to create the STORAGE BUCKET manually!**

---

## **📋 ADDITIONAL BUCKETS (Optional):**

While you're there, create these too for future features:

**Bucket 2: documents**
```
Name: documents
Public: YES
Size limit: 50 MB
Use: General document storage
```

**Bucket 3: profile_pictures**
```
Name: profile_pictures
Public: YES
Size limit: 5 MB
Use: User profile avatars
```

---

## **🚀 AFTER CREATION:**

1. ✅ Uploads will work instantly
2. ✅ Files stored in cloud
3. ✅ Public URLs generated
4. ✅ Fast downloads
5. ✅ No "temporary URL" warning

---

## **📊 WHAT HAPPENS AFTER FIX:**

### **Before (Now):**
```
❌ Cloud storage not configured
⚠️ Use external URL option
📎 Temporary URLs only
```

### **After (Fixed):**
```
✅ File uploaded to cloud storage!
✅ Material uploaded successfully!
🎈 Balloons!
📎 Permanent public URL
🔗 Direct download links
```

---

## **⏱️ TIME TO FIX:**

**2 minutes total:**
- 1 minute to login and navigate
- 30 seconds to create bucket
- 30 seconds to configure settings

**Then it works forever!**

---

## **🎯 SUMMARY:**

**Problem:** Storage bucket doesn't exist  
**Solution:** Create it manually in Supabase Dashboard  
**Location:** Storage → New Bucket → "learning_materials"  
**Settings:** Public, 200MB limit  
**Time:** 2 minutes  
**Result:** ✅ Uploads work forever!

---

## **🔗 HELPFUL LINKS:**

- Supabase Dashboard: https://supabase.com/dashboard/
- Storage Docs: https://supabase.com/docs/guides/storage
- Your Project: https://supabase.com/dashboard/project/YOUR_PROJECT_ID

---

**Do this now and uploads will work immediately!** ✅
