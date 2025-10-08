# Letter Parsing - Past vs Future Actions

## T21 RTT Validation - Understanding Letter Context

---

## 🎯 **Key Principle:**

Every clinic letter contains **TWO types of information**:

1. **PAST ACTIONS** - What has already been done
2. **FUTURE ACTIONS** - What needs to be done next

The system **MUST** distinguish between these to validate correctly.

---

## 📖 **Why This Matters:**

### **Example: Discharge Letter**

```
"I am pleased to inform you that the results from both the 
Coronary Angiography and the Echocardiogram were performed 
appropriately and have returned as normal.

Based on these findings, I do not believe that any medical 
intervention is needed at this point."
```

**WRONG Interpretation:**
- ❌ "echocardiogram" found → order echocardiogram
- ❌ "angiography" found → order angiography

**CORRECT Interpretation:**
- ✅ "results from...Echocardiogram were performed" → PAST action (already done)
- ✅ "have returned as normal" → PAST action (results available)
- ✅ "no intervention is needed" → Code 34 (discharge)
- ✅ No future actions to validate

---

## 🔍 **How The System Detects Past vs Future:**

### **PAST TENSE INDICATORS:**
- "was performed"
- "were performed"
- "has been done"
- "have been completed"
- "results from"
- "findings from"
- "showed", "demonstrated", "revealed"
- "underwent", "received"
- "have returned"
- "came back"

### **FUTURE/REQUEST INDICATORS:**
- "please arrange"
- "please book"
- "please order"
- "I recommend"
- "would recommend"
- "needs to"
- "should"
- "must"
- "to be ordered"
- "to be booked"
- "kindly arrange"

---

## 📝 **Letter Examples:**

### **Example 1: Referral Letter (Code 10)**

```
Dear Consultant,

I am writing to refer Mr. John Doe for assessment.

Clinical Details:
Patient complaining of chest pain after exercise.

Please arrange:
- Coronary angiogram
- ECG stress test
```

**System Parsing:**
- ✅ "I am writing to refer" → Code 10 (Referral)
- ✅ "Please arrange: Coronary angiogram" → FUTURE action
  - CHECK: Angiogram ordered? (Y/N)
  - FLAG if not ordered
- ✅ "Please arrange: ECG stress test" → FUTURE action
  - CHECK: ECG ordered? (Y/N)
  - FLAG if not ordered

**Validation:**
- Actions Required: 15+
- Gaps: "Angiogram NOT ORDERED", "ECG NOT ORDERED"

---

### **Example 2: Results Letter (Code 34 - Discharge)**

```
Dear Mr. Doe,

Re: Results from Your Recent Investigations

The Coronary Angiography was performed appropriately and 
has returned as normal. The ECG stress test also showed 
no abnormalities.

Based on these findings, no medical intervention is needed.
```

**System Parsing:**
- ✅ "results from" → Results letter
- ✅ "Coronary Angiography was performed" → PAST action (already done)
  - VERIFY: Results recorded in clinical notes
  - NO gap flagged (not an order)
- ✅ "ECG stress test also showed" → PAST action (already done)
  - VERIFY: Results recorded in clinical notes
  - NO gap flagged (not an order)
- ✅ "no medical intervention is needed" → Code 34 (Discharge)

**Validation:**
- Actions Required: 6
- Gaps: "GP letter" only
- NO diagnostic order gaps

---

### **Example 3: Clinic Outcome (Code 20)**

```
Dear Mr. Smith,

Thank you for attending clinic today.

I have reviewed your X-rays which were performed last week.
They show early signs of arthritis.

Plan:
- Please arrange MRI scan of the knee
- List patient for orthopaedic review
```

**System Parsing:**
- ✅ "X-rays which were performed last week" → PAST action
  - VERIFY: X-ray results recorded
  - NO order gap
- ✅ "Please arrange MRI scan" → FUTURE action
  - CHECK: MRI ordered? (Y/N)
  - FLAG if not ordered
- ✅ "List patient for orthopaedic review" → Code 20 (Decision to treat)

**Validation:**
- Actions Required: 10+
- Gaps: "MRI NOT ORDERED", "Patient NOT on waiting list"

---

## ⚙️ **How It Works Technically:**

### **Context Window Analysis:**

For each diagnostic keyword found (e.g., "angiogram"):

1. **Extract Context:** Get 100 characters before and after the keyword
   
2. **Check Indicators:**
   ```
   "...results from both the Coronary Angiography and the 
    Echocardiogram were performed appropriately and..."
   ```
   - Found: "results from" → PAST
   - Found: "were performed" → PAST
   - Conclusion: This is a PAST action

3. **Determine Action Type:**
   - **If PAST:** Verify results recorded (documentation check)
   - **If FUTURE:** Check if ordered in system (order check)
   - **If UNCLEAR:** Default to requiring validation

---

## 🎯 **Validation Logic:**

### **For PAST Actions (Already Done):**
```
Action: "VERIFY: Echocardiogram results from letter recorded in clinical notes (Y/N)"
Gap: None (documentation check, not an order)
```

### **For FUTURE Actions (To Be Done):**
```
Action: "CHECK: Echocardiogram ordered in system (Y/N)"
Gap: "FLAG: Letter requests Echocardiogram - NOT ORDERED IN SYSTEM"
```

---

## 📊 **Real-World Scenarios:**

### **Scenario 1: Mixed Letter**

```
"Patient underwent MRI scan last month which showed a lesion.
I recommend CT-guided biopsy to confirm diagnosis."
```

**Parsing:**
- "underwent MRI scan" → PAST
  - No order gap
- "I recommend CT-guided biopsy" → FUTURE
  - CHECK: Biopsy ordered?
  - FLAG if not ordered

---

### **Scenario 2: Post-Treatment**

```
"Surgery was performed on 15/03/2025. Patient recovering well.
Please arrange follow-up X-ray in 6 weeks."
```

**Parsing:**
- "Surgery was performed" → PAST → Code 30 (Treatment)
- "Please arrange follow-up X-ray" → FUTURE
  - CHECK: X-ray ordered?
  - FLAG if not ordered

---

## ✅ **Benefits:**

### **Before (Without Past/Future Detection):**
- ❌ False positives: "order tests that are already done"
- ❌ Unnecessary gaps flagged
- ❌ Incorrect validation counts
- ❌ Confusing reports

### **After (With Past/Future Detection):**
- ✅ Accurate detection: Only flag FUTURE actions
- ✅ Correct gap identification
- ✅ Proper validation counts
- ✅ Clear, actionable reports

---

## 🎓 **Training Example:**

**Letter:** 
```
"Blood tests were taken yesterday. Results show elevated cholesterol.
Please arrange lipid clinic referral."
```

**Questions to Ask:**
1. What has been done?
   - Blood tests taken
   
2. What needs to be done?
   - Lipid clinic referral

**System Validation:**
- ✅ Blood tests → PAST → Verify results recorded
- ✅ Lipid clinic referral → FUTURE → Check if referral made
- ✅ Only gap: "Referral NOT made" (not "blood tests not ordered")

---

*T21 Services UK | RTT Pathway Intelligence v1.2*  
*Intelligent Letter Parsing with Past/Future Action Detection*
