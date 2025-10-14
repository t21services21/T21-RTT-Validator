# 🔧 SETUP ENVIRONMENT VARIABLES

**Quick guide to set up API keys for new AI features**

---

## 🎯 WHAT YOU NEED:

### **REQUIRED (for AI features to work):**
- ✅ OpenAI API Key

### **OPTIONAL (for SMS/Email features):**
- ⚠️ Twilio Account (for SMS reminders)
- ⚠️ Email SMTP (for email reminders)

---

## 📝 STEP-BY-STEP SETUP:

### **STEP 1: Create .env File**

1. Copy the example file:
   ```bash
   # On Windows
   copy .env.example .env
   
   # Or just create new file called .env
   ```

2. Open `.env` in any text editor

---

### **STEP 2: Get OpenAI API Key (REQUIRED)**

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)
5. Paste into `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Cost:** ~£50-100/month for typical trust  
**What it enables:**
- Audio transcription (200x faster)
- Handwriting OCR
- NLP letter reading
- AI comment generation

---

### **STEP 3: Get Twilio Account (OPTIONAL)**

**Only needed if you want SMS reminders**

1. Go to: https://www.twilio.com/try-twilio
2. Sign up for free trial (£15 credit)
3. Get your credentials from console:
   - Account SID
   - Auth Token
   - Phone Number
4. Paste into `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=+44XXXXXXXXXX
   ```

**Cost:** ~£0.04 per SMS  
**What it enables:**
- Automated patient reminders
- Appointment confirmations
- DNA reduction (30%)

---

### **STEP 4: Setup Email (OPTIONAL)**

**Only needed if you want email reminders**

**Option A: Gmail**
1. Enable 2-factor authentication
2. Generate app password: https://myaccount.google.com/apppasswords
3. Paste into `.env`:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your.email@gmail.com
   SMTP_PASSWORD=your_app_password_here
   ```

**Option B: Other Email Provider**
- Use your email provider's SMTP settings
- Usually found in their help docs

**Cost:** Usually free  
**What it enables:**
- Email reminders
- Automated notifications
- Letter delivery tracking

---

## ✅ VERIFY SETUP:

### **Test if environment variables are loaded:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Check OpenAI
if os.getenv('OPENAI_API_KEY'):
    print("✅ OpenAI API key loaded")
else:
    print("❌ OpenAI API key missing")

# Check Twilio (optional)
if os.getenv('TWILIO_ACCOUNT_SID'):
    print("✅ Twilio credentials loaded")
else:
    print("⚠️ Twilio not configured (optional)")

# Check Email (optional)
if os.getenv('SMTP_USERNAME'):
    print("✅ Email configured")
else:
    print("⚠️ Email not configured (optional)")
```

---

## 🛡️ SECURITY:

### **IMPORTANT:**
- ✅ `.env` file is in `.gitignore` (won't be committed to Git)
- ✅ Never share your API keys
- ✅ Never commit `.env` to GitHub
- ✅ Use `.env.example` for documentation only

### **If you accidentally commit .env:**
1. Immediately revoke the API keys
2. Generate new keys
3. Update `.env` with new keys
4. Remove from Git history

---

## 💰 COST BREAKDOWN:

### **Monthly Costs (Typical Trust):**

**OpenAI API:**
- Audio transcription: £30/month
- OCR processing: £20/month
- Text generation: £30/month
- **Subtotal: £80/month**

**Twilio SMS:**
- 2,500 SMS × £0.04 = £100/month
- **Subtotal: £100/month**

**Email:**
- Usually free
- **Subtotal: £0/month**

**TOTAL: ~£180/month**

**Savings: £16,700/month (£200k/year)**

**ROI: 93x return!**

---

## 🚀 WHAT WORKS WITHOUT API KEYS:

### **Your existing 55 modules work 100% without any API keys!**

**What needs API keys:**
- ❌ Audio transcription (needs OpenAI)
- ❌ Handwriting OCR (needs OpenAI)
- ❌ SMS reminders (needs Twilio)
- ❌ Email reminders (needs SMTP)

**What works without API keys:**
- ✅ All 55 existing modules
- ✅ RTT validation
- ✅ Training platform
- ✅ Admin panel
- ✅ Everything else!

**Strategy:**
1. Start without API keys (everything works)
2. Add OpenAI key when ready (enables AI features)
3. Add Twilio later (enables SMS)
4. Add Email later (enables email)

---

## 📞 NEED HELP?

**Having trouble with API keys?**

**Email:** info@t21services.co.uk  
**We can help you:**
- Set up API accounts
- Configure environment variables
- Test API connections
- Troubleshoot issues

---

## ✅ CHECKLIST:

- [ ] Created `.env` file
- [ ] Added OpenAI API key (required)
- [ ] Added Twilio credentials (optional)
- [ ] Added Email SMTP (optional)
- [ ] Tested environment variables load
- [ ] Verified `.env` is in `.gitignore`
- [ ] Never committed `.env` to Git

---

**Once setup, your AI features will work automatically!** 🚀

**T21 Services Limited | Company No: 13091053**
