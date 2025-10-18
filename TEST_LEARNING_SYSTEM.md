# 🧪 TEST THE LEARNING SYSTEM

## Quick Test Guide

### **Step 1: Test Core Infrastructure**

Run this in Python console or terminal:

```bash
cd C:\Users\User\CascadeProjects\T21-RTT-Validator
python learning_system_core.py
```

**Expected Output:**
```
T21 Learning System initialized successfully!
Database: t21_learning_system.db
Added test example: ID 1
Example Library Stats:
{
  "letter_interpreter": {
    "categories": {
      "referral": {
        "count": 1,
        "avg_quality": 1.0,
        "total_usage": 0
      }
    },
    "total_examples": 1
  }
}
```

✅ If you see this → Core system working!

---

### **Step 2: Test Anonymization**

```bash
python data_anonymizer.py
```

**Expected Output:**
```
ORIGINAL LETTER:
Dear Dr Smith,
Re: John Doe, DOB 15/03/1975, NHS Number: 123 456 7890
...

ANONYMIZED LETTER:
Dear Dr Smith,
Re: [NAME], DOB [DATE], NHS Number: XXX XXX XXXX
...

VALIDATION:
Is Safe: True
Risk Level: LOW
Warnings: []
```

✅ If patient data is removed → Anonymization working!

---

### **Step 3: Test RAG System**

```bash
python letter_interpreter_rag.py
```

**Expected Output:**
```
T21 Letter Interpreter RAG System

Added test examples

Retrieved 2 contextual examples:

Example 1:
  Input: GP referral for chest pain investigation...
  Output: 18/10/2025 T21 - REF REC'D 01/10/2025 FOR CHEST PAIN...
  Specialty: Cardiology

Learning Statistics:
{
  "example_library": {
    "total_examples": 2,
    "categories": {
      "referral": {
        "count": 1
      },
      "discharge": {
        "count": 1
      }
    }
  }
}

Improvement Suggestions:
[MEDIUM] Need more examples for treatment letters
  Action: Save validated treatment letters to improve AI accuracy
```

✅ If examples are retrieved → RAG working!

---

### **Step 4: Test In Streamlit App**

1. **Start the app:**
```bash
streamlit run app.py
```

2. **Navigate to:** Pages → Clinic Letter Interpreter

3. **Upload a test letter** (or paste text)

4. **Click:** "🎓 Interpret & Teach Me"

5. **Scroll to bottom** after interpretation

6. **Look for:** "🧠 Help The System Learn!" section

7. **Click:** "✅ Perfect - Save as Example"

8. **Check:** "📊 Learning System Stats" expander

**Expected:**
- ✅ Balloons animation
- ✅ "Thank you! Example saved to learning library"
- ✅ Stats show: "Total validated examples: 1"

---

### **Step 5: Test Learning Improvement**

1. **Upload ANOTHER similar letter** (same type/specialty)

2. **The system should:**
   - Retrieve your saved example
   - Use it as context for AI
   - Give better interpretation

3. **Check the prompt enhancement** (in code):
   - AI now sees: "Learn from these validated examples..."
   - Your example is shown as context

---

## 🎯 What To Test For

### **Feedback Collection:**
- ✅ "Perfect" button saves example
- ✅ "Wrong" button shows correction form
- ✅ Correction form accepts input
- ✅ Stats update after saving

### **Anonymization:**
- ✅ NHS numbers removed
- ✅ Patient names removed
- ✅ Postcodes removed
- ✅ Clinical info preserved

### **RAG Retrieval:**
- ✅ Similar examples retrieved
- ✅ Specialty filtering works
- ✅ Category filtering works
- ✅ Usage count increments

### **Learning Over Time:**
- ✅ More examples = better accuracy
- ✅ Examples specific to your trust
- ✅ Specialty expertise develops

---

## 📊 Check Database Directly

**View the database:**
```bash
# Install DB Browser for SQLite (free tool)
# Open: t21_learning_system.db

# Or use command line:
sqlite3 t21_learning_system.db

# Run queries:
SELECT COUNT(*) FROM example_library;
SELECT * FROM example_library LIMIT 5;
SELECT module, COUNT(*) FROM feedback GROUP BY module;
```

**Expected Tables:**
- example_library
- feedback
- patterns
- analytics
- insights

---

## 🐛 Common Issues & Fixes

### **Issue: "Learning system not available" warning**
**Fix:** 
```bash
# Check files exist:
ls learning_system_core.py
ls data_anonymizer.py
ls letter_interpreter_rag.py

# Restart Streamlit
```

### **Issue: Database error**
**Fix:**
```bash
# Delete and recreate
rm t21_learning_system.db
python learning_system_core.py
```

### **Issue: Import errors**
**Fix:**
```bash
# Install required packages
pip install openai PyPDF2 python-docx
```

### **Issue: Feedback buttons don't work**
**Fix:**
- Ensure you clicked "Interpret" first
- Check browser console for errors
- Try refreshing page

---

## ✅ Success Checklist

- [ ] Core system initializes
- [ ] Database created
- [ ] Test examples added
- [ ] Anonymization removes patient data
- [ ] RAG retrieves similar examples
- [ ] Feedback UI appears in app
- [ ] "Perfect" button saves example
- [ ] Stats show saved examples
- [ ] Correction form works
- [ ] Database tables populated

---

## 📈 Track Improvements

### **Week 1:**
- Examples saved: _______
- Accuracy improvement: _______
- Feedback participation: _______

### **Month 1:**
- Examples saved: _______
- Accuracy improvement: _______
- Time saved per letter: _______

### **Month 3:**
- Examples saved: _______
- Accuracy improvement: _______
- Coverage gaps filled: _______

---

## 🎉 Ready For Production?

Before rolling out to all validators:

1. ✅ Test with 10-20 real letters
2. ✅ Verify anonymization is working
3. ✅ Confirm examples are useful
4. ✅ Check database performance
5. ✅ Brief validators on feedback process
6. ✅ Set up monitoring/analytics

---

**The learning system is LIVE and ready to make your platform smarter!**

Every validation you do now teaches the AI. 
Every correction you make improves future accuracy.
Every example you save helps the next validator.

**Welcome to AI that learns from YOUR expertise!** 🚀
