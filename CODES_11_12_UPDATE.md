# ✅ Codes 11 & 12 Added - Update Summary

## 🎯 What Was Added

I've successfully added **Code 11** and **Code 12** to your T21 RTT Pathway Intelligence system.

---

## 📋 Code Definitions

### **Code 11** - First Activity After Active Monitoring/Watchful Wait Ends
- **Clock Impact:** Restarts RTT clock (after pause)
- **Used When:** Patient returns from Active Monitoring (31/32) and treatment resumes
- **Validation Rule:** Must have prior code 31 or 32 in the timeline
- **Example:** Patient reviewed after 6-month watchful wait, now proceeding to treatment

### **Code 12** - First Activity Following Consultant/AHP Referral for NEW Condition
- **Clock Impact:** Starts NEW RTT clock
- **Used When:** Consultant-to-consultant referral for different condition
- **Validation Rule:** Creates new separate pathway
- **Example:** ENT consultant refers to Dermatology for unrelated skin issue

---

## 📁 Files Updated

### 1. **app.py** (Web UI)
✅ Added codes 11 & 12 to all dropdown menus:
- Pathway Validator
- Timeline Auditor  
- Comment Line Generator

✅ Updated RTT Rules Reference table with full descriptions

### 2. **README.md** (Documentation)
✅ Added codes 11 & 12 to RTT Code Reference table
✅ Updated with clock impact details

### 3. **rtt_validator.py** (Validation Logic)
✅ Updated `validate_timeline()` function:
- Accepts code 10, 11, or 12 as pathway start
- Validates code 11 requires prior code 31/32 (AM start)
- Provides specific error messages when code 11 used incorrectly

### 4. **TOOL_SUMMARY.md**
✅ Updated Code Repetition Rules section with codes 11, 12, 21, 92, 98

### 5. **RTT_CODES_REFERENCE.md** (NEW FILE)
✅ Created comprehensive reference guide with:
- Full description of ALL RTT codes (10-98)
- Clock impact for each code
- Usage examples
- Valid/invalid sequence patterns
- T21 comment line formats
- Complete RTT terminology glossary

### 6. **CODES_11_12_UPDATE.md** (This File)
✅ Summary of changes

---

## 🧪 Validation Rules Implemented

### Code 11 Validation:
```
❌ ERROR: Code 11 without prior 31/32
Timeline: 10 → 20 → 11 → 30
Issue: Code 11 requires Active Monitoring to have started first

✅ VALID: Code 11 after Active Monitoring
Timeline: 10 → 20 → 32 → 91 → 11 → 20 → 30
Explanation: AM started (32), patient monitored (91), then returned to treatment (11)
```

### Code 12 Validation:
```
✅ VALID: Code 12 for new condition
Timeline: 12 → 20 → 30
Explanation: New pathway for new clinical condition (separate from any existing pathway)

✅ VALID: Code 12 alongside code 10
Patient can have MULTIPLE pathways:
- Pathway A: 10 → 20 → 30 (ENT - Septoplasty)
- Pathway B: 12 → 20 → 30 (Dermatology - New skin issue)
```

---

## 📊 Updated Code List

| Code | Description | Clock Impact |
|------|-------------|--------------|
| **10** | First activity in pathway | Start |
| **11** | First activity after AM/Watchful Wait ends | Restart |
| **12** | First activity - Consultant/AHP referral NEW condition | Start (new pathway) |
| **20** | Subsequent activity | Continue |
| **21** | Tertiary referral / Transfer | Transfer responsibility |
| **30** | First definitive treatment | Stop |
| **31** | Active monitoring (patient-initiated) | Pause |
| **32** | Active monitoring (clinician-initiated) | Pause |
| **33** | DNA first care activity | Special |
| **34** | Decision not to treat | Stop |
| **35** | Patient declined treatment | Stop |
| **36** | Patient died | Stop |
| **90** | FDT occurred previously | Non-RTT |
| **91** | Activity during active monitoring | During AM |
| **92** | Diagnostics only | Non-RTT |
| **98** | Not applicable to RTT | Non-RTT |

---

## 🎯 How To Use New Codes

### **Using Code 11:**
1. Patient must first be placed on Active Monitoring (code 31 or 32)
2. During AM, use code 91 for review appointments
3. When treatment resumes, use code 11 to restart the clock
4. Continue with code 20 for subsequent activities

**Example Timeline:**
```
01/01/2025 - Referral received - Code 10
15/01/2025 - Clinic review - Code 20
20/01/2025 - Start watchful wait (6 months) - Code 32
15/03/2025 - Review during AM - Code 91
20/07/2025 - AM ends, treatment needed - Code 11
25/07/2025 - Pre-op assessment - Code 20
05/08/2025 - Surgery - Code 30
```

### **Using Code 12:**
1. Use when consultant refers to ANOTHER specialty for DIFFERENT condition
2. This creates a NEW, SEPARATE RTT pathway
3. Original pathway continues independently

**Example:**
```
Patient A - ENT Pathway:
01/01/2025 - GP referral - Code 10
15/01/2025 - ENT review - Code 20
20/02/2025 - Septoplasty - Code 30

Patient A - Dermatology Pathway (SEPARATE):
15/01/2025 - ENT consultant notices skin lesion, refers Derm - Code 12
25/01/2025 - Derm review - Code 20
10/02/2025 - Skin biopsy - Code 30
```

---

## ✅ Testing

### Test Code 11 in Timeline Auditor:

1. Open app (or use CLI)
2. Select "Timeline Auditor"
3. Enter events:
   - `01/01/2025 - Referral - 10`
   - `15/01/2025 - Review - 20`
   - `20/01/2025 - AM Start - 32`
   - `15/03/2025 - AM Review - 91`
   - `20/07/2025 - AM End - 11`
   - `05/08/2025 - Surgery - 30`
4. Result: ✅ Pass

### Test Code 11 Error Detection:

1. Enter events:
   - `01/01/2025 - Referral - 10`
   - `15/01/2025 - Review - 20`
   - `20/01/2025 - ??? - 11` (NO prior 31/32)
2. Result: ❌ Error - "Code 11 used without prior Active Monitoring (31/32)"

---

## 📖 Additional Resources

- **RTT_CODES_REFERENCE.md** - Complete code guide with examples
- **README.md** - Updated with codes 11 & 12
- **TOOL_SUMMARY.md** - Feature overview with new codes

---

## 🚀 Ready To Use

All tools now support codes 11 and 12:
- ✅ Pathway Validator
- ✅ Clinic Letter Interpreter
- ✅ Timeline Auditor
- ✅ Patient Registration Validator
- ✅ Appointment & Booking Checker
- ✅ Comment Line Generator

**The system is fully updated and ready for use!** 🎉

---

*T21 Services UK | NHS RTT Training & Validation System v1.2*  
*Updated: 08/10/2025 with Codes 11 & 12*
