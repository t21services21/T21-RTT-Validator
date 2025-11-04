# 🚀 DEPLOYMENT INSTRUCTIONS FOR TQUK CDA DOCUMENTS

## ✅ WHAT'S BEEN UPDATED:

The file `pages/tquk_cda_documents.py` has been updated to include:

1. ✅ All 7 mandatory unit assessment plans for Level 3 Diploma in Adult Care
2. ✅ CDA Submission Summary document
3. ✅ Email Response to TQUK template
4. ✅ PDF and Word download buttons for all documents

---

## 📂 FILES THAT NEED TO BE DEPLOYED:

### **1. Updated Python File:**
- `pages/tquk_cda_documents.py` (ALREADY UPDATED)

### **2. New Document Files (Need to be copied to root):**
Copy these files from `TQUK_CDA_Complete_Submission/` to the root directory:

```
TQUK_CDA_Complete_Submission/
├── Unit_1_Assessment_Plan_Duty_of_Care.md
├── Unit_2_Assessment_Plan_Equality_Diversity_Inclusion.md
├── Unit_3_Assessment_Plan_Person_Centred_Practice.md
├── Unit_4_Assessment_Plan_Safeguarding.md
├── Unit_5_Assessment_Plan_Communication.md
├── Unit_6_Assessment_Plan_Health_Safety.md
├── Unit_7_Assessment_Plan_CPD.md
├── CDA_SUBMISSION_SUMMARY.md
└── EMAIL_RESPONSE_TO_TQUK.md
```

---

## 🔧 DEPLOYMENT STEPS:

### **Option 1: If Using Streamlit Cloud**

1. **Upload files to GitHub:**
   - Copy all files from `TQUK_CDA_Complete_Submission/` folder
   - Add them to your GitHub repository root
   - Commit and push changes
   - Streamlit Cloud will auto-deploy

2. **Or use Streamlit Cloud file upload:**
   - Go to your Streamlit Cloud dashboard
   - Upload the files manually

### **Option 2: If Using Local Deployment**

1. **Copy files to root:**
   ```powershell
   Copy-Item -Path "C:\Users\User\CascadeProjects\T21-RTT-Validator\TQUK_CDA_Complete_Submission\*" -Destination "C:\Users\User\CascadeProjects\T21-RTT-Validator\" -Force
   ```

2. **Restart Streamlit:**
   ```powershell
   # Stop current Streamlit (Ctrl+C)
   # Then restart:
   streamlit run app.py
   ```

### **Option 3: Manual File Copy**

1. Open File Explorer
2. Navigate to: `C:\Users\User\CascadeProjects\T21-RTT-Validator\TQUK_CDA_Complete_Submission\`
3. Select all `.md` files
4. Copy them
5. Paste into: `C:\Users\User\CascadeProjects\T21-RTT-Validator\`
6. Restart Streamlit

---

## 🌐 ACCESS THE PAGE:

Once deployed, access the documents at:

**URL:** `https://your-streamlit-app.streamlit.app/tquk_cda_documents`

Or navigate from the main app menu.

---

## 📥 WHAT USERS CAN DO:

1. ✅ View all 7 unit assessment plans
2. ✅ Download each unit as PDF
3. ✅ Download each unit as Word document
4. ✅ Download complete submission summary
5. ✅ Download email template for TQUK

---

## ✅ VERIFICATION:

After deployment, verify:
- [ ] Page loads without errors
- [ ] All 7 units show download buttons
- [ ] PDF downloads work
- [ ] Word downloads work
- [ ] Summary document downloads
- [ ] Email template downloads

---

## 🎯 NEXT STEPS FOR USER:

1. Access the TQUK CDA Documents page
2. Download all documents
3. Upload to Google Drive
4. Send email to TQUK with Google Drive link

---

**Prepared by:** T21 Services UK  
**Date:** November 2025  
**Platform:** T21 Healthcare Intelligence Platform
