# 🔐 ACCESS CONTROL - UPDATE NEEDED

**Date:** 9th October 2025, 21:12  
**Priority:** HIGH - Do Tomorrow Morning

---

## 📋 CURRENT SITUATION

**File:** `access_control.py` already exists

**Problem:** Uses OLD tier structure that doesn't match new pricing

---

## 🎯 NEW TIER STRUCTURE (Approved Today)

### **TIER 1: Video Library (£99/6 months)**

**What they can access:**
- ✅ Training video library
- ✅ Text-based courses
- ✅ Basic AI Tutor (5 questions/day)
- ✅ Community forum
- ❌ NO RTT Clinical Validator
- ❌ NO live tutors
- ❌ NO certification

**Pages they should see:**
- Dashboard
- Training Library (limited)
- Community
- My Account
- **HIDE:** RTT Clinical Validator, Pathway Validator, Appointment System, PAS Demo, 2FA Setup

---

### **TIER 2: Full Platform (£499/6 months)**

**What they can access:**
- ✅ Everything in Tier 1 PLUS:
- ✅ RTT Clinical Validator ⭐
- ✅ Pathway Validator ⭐
- ✅ Appointment System ⭐
- ✅ Unlimited AI Tutor
- ✅ AI Interview Prep
- ✅ AI CV Builder
- ✅ 2FA Setup
- ❌ NO certification program

**Pages they should see:**
- Everything Tier 1 can see PLUS:
- RTT Clinical Validator ✅
- Pathway Validator ✅
- Appointment System ✅
- **HIDE:** Certification Dashboard, Alumni Network

---

### **TIER 3: TQUK Certification (£1,299)**

**What they can access:**
- ✅ Everything in Tier 2 PLUS:
- ✅ 8-week certification program
- ✅ TQUK certification
- ✅ Alumni network
- ✅ Live Zoom sessions
- ✅ Job resources

**Pages they should see:**
- Everything Tier 2 can see PLUS:
- Certification Dashboard ✅
- Alumni Network ✅
- Live Sessions ✅
- **HIDE:** Job Coaching Portal

---

### **TIER 4: + Job Coaching (£1,799)**

**What they can access:**
- ✅ Everything in Tier 3 PLUS:
- ✅ Job coaching dashboard
- ✅ Mock interview scheduler
- ✅ Application reviews

**Pages they should see:**
- Everything!
- Job Coaching Portal ✅
- Mock Interview Scheduler ✅

---

### **STAFF/ADMIN**

**What they can access:**
- ✅ Everything ALL tiers have PLUS:
- ✅ Admin Panel
- ✅ User Management
- ✅ Analytics Dashboard
- ✅ PAS Integration Demo
- ✅ All system management

---

## 🔧 HOW TO IMPLEMENT

### **Update `access_control.py`:**

Replace the ROLES dictionary with:

```python
ROLES = {
    "tier1": {
        "name": "Video Library Access",
        "duration_days": 180,  # 6 months
        "price": 99,
        "features": {
            "training_library": "limited",  # Videos only
            "ai_tutor": "limited",  # 5 questions/day
            "community_forum": True,
            "rtt_clinical_validator": False,  # NO HANDS-ON
            "pathway_validator": False,
            "appointment_system": False,
            "live_tutors": False,
            "certification": False,
            "alumni_network": False
        },
        "limits": {
            "ai_questions_per_day": 5,
            "video_access": "all"
        }
    },
    
    "tier2": {
        "name": "Full Platform Access",
        "duration_days": 180,  # 6 months
        "price": 499,
        "features": {
            "training_library": True,  # Full access
            "ai_tutor": True,  # Unlimited
            "community_forum": True,
            "rtt_clinical_validator": True,  # HANDS-ON! ⭐
            "pathway_validator": True,  # ⭐
            "appointment_system": True,  # ⭐
            "ai_interview_prep": True,
            "ai_cv_builder": True,
            "two_fa_setup": True,
            "live_tutors": "monthly",  # Monthly Q&A
            "certification": False,
            "alumni_network": False
        },
        "limits": {
            "ai_questions_per_day": "unlimited"
        }
    },
    
    "tier3": {
        "name": "TQUK Certification Program",
        "duration_days": 56,  # 8 weeks program
        "price": 1299,
        "features": {
            # Everything Tier 2 has PLUS:
            "training_library": True,
            "ai_tutor": True,
            "rtt_clinical_validator": True,
            "pathway_validator": True,
            "appointment_system": True,
            "ai_interview_prep": True,
            "ai_cv_builder": True,
            "two_fa_setup": True,
            "live_tutors": "weekly",  # Weekly sessions
            "certification": True,  # TQUK CERT! ⭐⭐⭐
            "alumni_network": True,  # ⭐
            "job_resources": True,
            "certification_dashboard": True
        },
        "limits": {
            "ai_questions_per_day": "unlimited",
            "certification_attempts": 1
        },
        "post_program_access": {
            # After 8 weeks, they get Tier 2 for 3 months
            "tier": "tier2",
            "duration_days": 90
        }
    },
    
    "tier4": {
        "name": "Certification + Job Coaching",
        "duration_days": 56 + 90,  # 8 weeks + 3 months coaching
        "price": 1799,
        "features": {
            # Everything Tier 3 has PLUS:
            "training_library": True,
            "ai_tutor": True,
            "rtt_clinical_validator": True,
            "pathway_validator": True,
            "appointment_system": True,
            "ai_interview_prep": True,
            "ai_cv_builder": True,
            "two_fa_setup": True,
            "live_tutors": "weekly",
            "certification": True,
            "alumni_network": True,
            "job_resources": True,
            "job_coaching": True,  # PREMIUM! ⭐
            "mock_interviews": 5,  # 5 sessions
            "application_reviews": "unlimited",
            "weekly_checkins": True
        },
        "limits": {
            "ai_questions_per_day": "unlimited",
            "certification_attempts": 1,
            "mock_interviews": 5
        }
    },
    
    "staff": {
        "name": "Staff Member",
        "duration_days": 9999,
        "price": 0,
        "features": {
            "all_features": True,
            "admin_panel": False  # Basic staff, not admin
        }
    },
    
    "admin": {
        "name": "Administrator",
        "duration_days": 9999,
        "price": 0,
        "features": {
            "all_features": True,
            "admin_panel": True,
            "user_management": True,
            "analytics": True,
            "pas_integration_demo": True
        }
    }
}
```

---

## 📋 PAGE VISIBILITY MATRIX

```
┌─────────────────────────────────────────────────────────────────┐
│ PAGE                  │ Tier1│ Tier2│ Tier3│ Tier4│ Staff│ Admin│
├───────────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Training Library      │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │
│ AI Tutor              │ Limit│ Full │ Full │ Full │ Full │ Full │
│ Community             │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │
│ RTT Clinical Validator│ ✗    │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │
│ Pathway Validator     │ ✗    │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │
│ Appointment System    │ ✗    │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │
│ 2FA Setup             │ ✗    │ ✓    │ ✓    │ ✓    │ ✓    │ ✓    │
│ Certification Program │ ✗    │ ✗    │ ✓    │ ✓    │ ✓    │ ✓    │
│ Alumni Network        │ ✗    │ ✗    │ ✓    │ ✓    │ ✓    │ ✓    │
│ Job Coaching          │ ✗    │ ✗    │ ✗    │ ✓    │ ✓    │ ✓    │
│ PAS Integration Demo  │ ✗    │ ✗    │ ✗    │ ✗    │ ✗    │ ✓    │
│ Admin Panel           │ ✗    │ ✗    │ ✗    │ ✗    │ ✗    │ ✓    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 IMPLEMENTATION CHECKLIST

### **Tomorrow Morning:**

- [ ] Update `access_control.py` with new ROLES dictionary
- [ ] Test tier checking function
- [ ] Add tier check to each protected page
- [ ] Update upgrade paths
- [ ] Test all 4 tier access levels
- [ ] Ensure admin has full access
- [ ] Test upgrade prompts for locked features

---

## 💡 UPGRADE PROMPTS

**When Tier 1 clicks RTT Clinical Validator:**
```
🔒 This feature requires Full Platform Access

Upgrade to Tier 2 (£499) to access:
✅ RTT Clinical Validator (hands-on)
✅ Pathway Validator
✅ Appointment System
✅ Unlimited AI Tutor

[Upgrade Now] button
```

**When Tier 2 clicks Certification Dashboard:**
```
🎓 This feature requires Certification Program

Upgrade to Tier 3 (£1,299) to get:
✅ Official TQUK Certification
✅ 8-week structured program
✅ Alumni network access
✅ Weekly live tutors

[Upgrade Now] button
```

---

**STATUS:** Ready to implement tomorrow!

**TIME ESTIMATE:** 1-2 hours

**PRIORITY:** Do first thing after pushing files!

---

*Created: 9th October 2025, 21:12*
