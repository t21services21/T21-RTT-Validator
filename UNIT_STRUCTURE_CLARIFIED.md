# UNIT STRUCTURE CLARIFIED - MANDATORY + OPTIONAL

Date: October 24, 2025 5:36 PM
Issue: Enrollment shows "Units: 7" but doesn't explain optional units
Status: FIXED

---

## THE ISSUE:

### What You Saw:
Enrollment screen showed:
- Units: 7

### What Was Missing:
- No mention of 3 mandatory units
- No mention of 4 optional units
- No explanation that learners choose 4 from 20+ options

---

## LEVEL 3 DIPLOMA STRUCTURE:

### ACTUAL QUALIFICATION:

**Mandatory Units (3 units = 37 credits):**
1. Unit 1: Duty of Care in Health and Social Care
2. Unit 2: Equality, Diversity and Inclusion
3. Unit 3: Person-Centred Care and Support

**Optional Units (4 units = 21 credits):**
- Choose 4 units from 20+ available options
- Examples:
  - Communication in Health and Social Care
  - Health and Safety
  - Safeguarding
  - Dementia Care
  - End of Life Care
  - Mental Health
  - Learning Disabilities
  - And many more...

**Total: 7 units = 58 credits**

---

## WHAT I FIXED:

### File: tquk_course_assignment.py

**Added to qualification definition:**
```python
"level3_adult_care": {
    "name": "Level 3 Diploma in Adult Care",
    "code": "610/0103/6",
    "duration": "12-18 weeks",
    "price": "£1,500",
    "credits": 58,
    "units": 7,
    "mandatory_units": 3,
    "optional_units": 4,
    "unit_structure": "3 Mandatory + 4 Optional (from 20+ choices)"
}
```

**Updated display:**
- Before: "Units: 7"
- After: "Units: 3 Mandatory + 4 Optional (from 20+ choices)"

---

## WHAT IT WILL SHOW NOW:

### Enrollment Screen:

```
Level 3 Diploma in Adult Care

- Code: 610/0103/6
- Duration: 12-18 weeks
- Price: £1,500
- Credits: 58
- Units: 3 Mandatory + 4 Optional (from 20+ choices)
```

**Much clearer!**

---

## DEPLOY NOW:

### Using GitHub Desktop:

1. See 1 changed file:
   - tquk_course_assignment.py (unit structure clarified)

2. Commit message:
   "Clarify Level 3 unit structure - 3 mandatory + 4 optional"

3. Click Commit
4. Click Push
5. Wait 5 minutes

---

## AFTER DEPLOYMENT:

### What Learners Will See:

When enrolled, they'll see:
- 3 Mandatory Units (must complete all)
- Optional Units tab (choose 4 from 20+ options)
- Clear explanation of structure
- Progress tracking for both types

---

## OPTIONAL UNITS IN THE SYSTEM:

The platform already has the optional units selector!

**Location:**
Level 3 Adult Care module → Optional Units tab

**Features:**
- 20+ optional units to choose from
- Credit calculator
- Unit descriptions
- Learning outcomes
- Assessment criteria

**Learners can:**
1. Browse all optional units
2. Select 4 units (21 credits minimum)
3. See unit details
4. Track progress
5. Submit evidence

---

## SUMMARY:

**Issue:** Enrollment showed "Units: 7" without explanation
**Fix:** Now shows "3 Mandatory + 4 Optional (from 20+ choices)"
**Impact:** Clearer for teachers and learners
**Deploy:** Push to GitHub
**Result:** Better understanding of qualification structure

---

## QUALIFICATION STRUCTURE:

**Total Credits:** 58
**Total Units:** 7

**Breakdown:**
- 3 Mandatory Units = 37 credits (fixed)
- 4 Optional Units = 21 credits (choose from 20+)

**Learner Journey:**
1. Complete 3 mandatory units (everyone does these)
2. Choose 4 optional units (personalized learning)
3. Complete all 7 units
4. Submit evidence
5. Internal verification
6. External verification (TQUK)
7. Certificate issued

---

PUSH NOW TO CLARIFY UNIT STRUCTURE!
ENROLLMENT WILL SHOW MANDATORY + OPTIONAL!
