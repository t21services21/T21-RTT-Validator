# 🔒 GITGUARDIAN SECURITY ALERT - COMPLETE FIX GUIDE

**Date:** October 17, 2025  
**Status:** ⚠️ PASSWORD EXPOSED IN GIT HISTORY  
**Alert From:** GitGuardian

---

## **✅ GOOD NEWS:**

Your `.gitignore` **IS ALREADY GOOD!** It includes:

```gitignore
# You already have:
*.env
.env
.env.local
.streamlit/secrets.toml
secrets.toml
config.ini
```

---

## **❌ THE PROBLEM:**

**GitGuardian found a password in your Git HISTORY, not current files!**

### **What Happened:**

1. **Before:** You committed `security_email_notifications.py` with a REAL password
2. **Later:** You changed it to placeholder `"your-app-password-here"`
3. **Now:** Current file is safe, BUT Git history still has the real password
4. **GitGuardian:** Scans entire history → Found the real password in old commit

**Even though `.gitignore` protects future commits, it doesn't remove history!**

---

## **🔥 IMMEDIATE ACTIONS (DO NOW!):**

### **1. Change/Revoke the Password ✅**

- [ ] Go to your email provider (Gmail/Outlook)
- [ ] **Revoke the app password** immediately
- [ ] Generate a NEW app password
- [ ] Store it in Streamlit secrets (never in code)

---

### **2. Fix the Code (Already Done!) ✅**

I've updated `security_email_notifications.py` to use Streamlit secrets:

**Before (UNSAFE):**
```python
SENDER_PASSWORD = "your-app-password-here"  # NEVER DO THIS!
```

**After (SAFE):**
```python
import streamlit as st
SENDER_PASSWORD = st.secrets.get("SENDER_PASSWORD", "")

if not SENDER_PASSWORD:
    return False  # Don't send if not configured
```

---

### **3. Click "Fix This Secret Leak" Button**

In the GitGuardian email, click the blue button:
```
┌─────────────────────────────────┐
│   Fix This Secret Leak          │
└─────────────────────────────────┘
```

This will:
- Mark the alert as acknowledged
- Guide you through GitHub's secret removal process

---

### **4. Remove from Git History (CRITICAL!)**

The password is still in your Git commit history. You MUST remove it:

#### **Method 1: GitHub Secret Scanner (EASIEST)**

1. Go to: https://github.com/t21services2/T21-RTT-Validator
2. Click "Settings" → "Security" → "Secret scanning alerts"
3. Find the alert
4. Follow GitHub's guided removal process

#### **Method 2: Manual Removal**

If you have Git installed locally:

```bash
cd C:\Users\User\CascadeProjects\T21-RTT-Validator

# Remove the file from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch security_email_notifications.py" \
  --prune-empty --tag-name-filter cat -- --all

# OR use BFG Repo-Cleaner (faster):
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --replace-text passwords.txt

# Force push to overwrite history
git push origin --force --all
git push origin --force --tags
```

⚠️ **WARNING:** Force push will rewrite history. Anyone who cloned before needs to re-clone!

#### **Method 3: Delete & Re-Create Repo (NUCLEAR OPTION)**

If the above fails:

1. Download all your current files locally (safe copy)
2. Delete the GitHub repository
3. Create a new repository
4. Push current files (password-free versions)
5. Update collaborators

---

## **🛡️ CONFIGURE STREAMLIT SECRETS:**

### **Local Development:**

Create `.streamlit/secrets.toml` (this is already in `.gitignore`):

```toml
# .streamlit/secrets.toml
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "security@t21services.co.uk"
SENDER_PASSWORD = "your-NEW-app-password-here"

# Other secrets
SENDGRID_API_KEY = "your-sendgrid-key"
OPENAI_API_KEY = "your-openai-key"
```

### **Streamlit Cloud:**

1. Go to: https://share.streamlit.io/
2. Click your app → "Settings" → "Secrets"
3. Add the same secrets:

```toml
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "security@t21services.co.uk"
SENDER_PASSWORD = "your-NEW-app-password-here"
```

---

## **✅ VERIFY IT'S FIXED:**

### **Check 1: Current File is Safe**
```bash
# Search current files for passwords
findstr /s /i "password.*=.*@" *.py
```

Should return nothing sensitive.

### **Check 2: Git History is Clean**

If you have Git installed:
```bash
# Search all commits for passwords
git log --all --full-history -p | findstr /i "password"
```

Should show no real passwords.

### **Check 3: .gitignore is Active**
```bash
# Verify secrets are ignored
git check-ignore .streamlit/secrets.toml
```

Should return the path (means it's ignored).

---

## **📋 ADDITIONAL SECURITY IMPROVEMENTS:**

### **Add to `.gitignore`:**

Add these additional patterns (for extra safety):

```gitignore
# Additional security patterns
**/secrets.toml
**/*password*.py
**/*secret*.py
*.key
*.pem
*.p12
*.pfx
*.crt
credentials.json
service-account*.json
```

### **Files Already Using Secrets Correctly:**

✅ **SAFE:**
- `email_service.py` - Uses `st.secrets.get("SENDGRID_API_KEY")`
- `security_email_notifications.py` - NOW FIXED to use secrets

### **Other Files to Check:**

Review these files for any hardcoded credentials:

- `nhs_email_notifications.py`
- `admin_bulk_email.py`
- Any other `*email*.py` files

---

## **🎯 PREVENTION CHECKLIST:**

### **For Every New Feature:**

- [ ] Never hardcode passwords/API keys/tokens
- [ ] Always use `st.secrets.get("KEY_NAME")`
- [ ] Add secret name to `.streamlit/secrets.toml` locally
- [ ] Add to Streamlit Cloud secrets dashboard
- [ ] Test that it works without hardcoded values

### **Before Every Commit:**

- [ ] Search code for patterns: `password.*=.*"`, `api_key.*=.*"`
- [ ] Check no `.env` files are staged
- [ ] Verify `.gitignore` is working: `git status --ignored`

### **Use Pre-Commit Hooks:**

Create `.git/hooks/pre-commit`:

```bash
#!/bin/sh
# Prevent commits with passwords

if git diff --cached | grep -i "password.*=.*['\"].*@"; then
    echo "❌ BLOCKED: Potential password found in commit!"
    echo "Use Streamlit secrets instead of hardcoding passwords."
    exit 1
fi

exit 0
```

---

## **📞 IF YOU'RE UNSURE:**

### **Questions to Ask Yourself:**

1. **"Did I change the exposed password?"**
   - If NO → Do it NOW!
   - If YES → Good, continue to next step

2. **"Is the password still in Git history?"**
   - If UNSURE → Assume YES and clean history
   - If YES → Follow Method 1 or 2 above

3. **"Are secrets now in Streamlit secrets?"**
   - If NO → Add them now
   - If YES → Good, test that app still works

---

## **✅ COMPLETION CHECKLIST:**

- [ ] 1. ✅ Changed/revoked the exposed password
- [ ] 2. ✅ Updated code to use Streamlit secrets (DONE)
- [ ] 3. ⚠️ Clicked "Fix This Secret Leak" in GitGuardian email
- [ ] 4. ⚠️ Removed password from Git history
- [ ] 5. ✅ Created `.streamlit/secrets.toml` (if not exists)
- [ ] 6. ✅ Added secrets to Streamlit Cloud dashboard
- [ ] 7. ⚠️ Verified Git history is clean
- [ ] 8. ✅ Tested app still works with secrets
- [ ] 9. ⚠️ Notified any collaborators about force push

---

## **🚨 CRITICAL REMINDER:**

**Anyone who has cloned your repo can still see the password in their local Git history until you:**

1. Clean the history
2. Force push
3. They delete their local copy and re-clone

**This is why immediate password revocation is critical!**

---

## **📊 SUMMARY:**

| Item | Status | Action |
|------|--------|--------|
| `.gitignore` | ✅ GOOD | Already protecting secrets |
| Current code | ✅ FIXED | Now uses Streamlit secrets |
| Git history | ⚠️ TODO | Remove password from history |
| Password | ⚠️ TODO | Revoke and replace |
| Secrets config | ⚠️ TODO | Add to `.streamlit/secrets.toml` |

---

**Priority:** 🔥 HIGH - Do steps 1, 3, and 4 immediately!

**Impact:** 🚨 CRITICAL - Exposed passwords can be used for unauthorized access

**Difficulty:** ⭐⭐ MEDIUM - Requires Git history cleanup

---

*T21 Services Limited | Security Best Practices*  
*Last Updated: October 17, 2025*
