# COMPLETE DATABASE SCHEMA MAPPING - ALL MODULES

## SQL TABLE SCHEMAS (from SUPABASE_CREATE_ALL_TABLES.sql):

### 1. PTL_PATIENTS TABLE:
```
- id (SERIAL PRIMARY KEY)
- patient_id (TEXT UNIQUE NOT NULL)
- user_email (TEXT NOT NULL)
- patient_name, nhs_number, specialty
- referral_date (DATE)
- referral_source, clock_start_date (DATE)
- pathway_type, priority, current_status
- consultant, contact_number, rtt_code, clock_status
- notes, added_date (TIMESTAMP)
- last_updated (TIMESTAMP)
- appointments (JSONB)
- events (JSONB)
- created_at (TIMESTAMP DEFAULT NOW())
```
✅ FIXED - Using correct fields

---

### 2. MDT_MEETINGS TABLE:
```
- id (SERIAL PRIMARY KEY)
- meeting_id (TEXT UNIQUE NOT NULL)
- user_email (TEXT NOT NULL)
- meeting_date (DATE NOT NULL)
- meeting_time (TIME)
- specialty, location
- chair_person (TEXT) ← NOT 'chair'!
- attendees (JSONB)
- patients_discussed (JSONB) ← NOT 'patients'!
- decisions (JSONB) ← NOT 'outcomes'!
- action_points (JSONB)
- notes (TEXT)
- status (TEXT DEFAULT 'scheduled')
- created_at (TIMESTAMP DEFAULT NOW())
- updated_at (TIMESTAMP DEFAULT NOW()) ← NOT 'last_updated'!
```
✅ FIXED - Using correct fields

---

### 3. CANCER_PATHWAYS TABLE:
```
- id (SERIAL PRIMARY KEY)
- pathway_id (TEXT UNIQUE NOT NULL) ← NOT 'patient_id'!
- user_email (TEXT NOT NULL)
- patient_name, nhs_number, cancer_type
- referral_date (DATE)
- pathway_type
- clock_start_date (DATE) ← NOT 'pathway_start_date'!
- target_date (DATE)
- current_status (TEXT)
- milestones (JSONB)
- treatments (JSONB) ← NOT 'appointments', 'diagnostics', 'events'!
- notes (TEXT)
- created_at (TIMESTAMP DEFAULT NOW())
- updated_at (TIMESTAMP DEFAULT NOW())
```
✅ FIXED - Using correct fields

---

### 4. APPOINTMENTS TABLE:
```
- id (SERIAL PRIMARY KEY)
- appointment_id (TEXT UNIQUE NOT NULL)
- user_email (TEXT NOT NULL)
- patient_id, patient_name, nhs_number
- appointment_date (DATE NOT NULL)
- appointment_time (TIME)
- specialty, clinic_location, appointment_type
- consultant, status (TEXT DEFAULT 'booked')
- notes (TEXT)
- created_at (TIMESTAMP DEFAULT NOW())
- updated_at (TIMESTAMP DEFAULT NOW())
```
⚠️ NEEDS CHECKING

---

### 5. VALIDATION_HISTORY TABLE:
```
- id (SERIAL PRIMARY KEY)
- validation_id (TEXT UNIQUE NOT NULL)
- user_email (TEXT NOT NULL)
- validation_type (TEXT)
- patient_data (JSONB)
- result (JSONB)
- is_valid (BOOLEAN)
- confidence_score (INTEGER)
- issues (JSONB)
- created_at (TIMESTAMP DEFAULT NOW())
```
⚠️ NEEDS CHECKING

---

### 6. TRAINING_PROGRESS TABLE:
```
- id (SERIAL PRIMARY KEY)
- user_email (TEXT NOT NULL)
- scenario_id (TEXT NOT NULL)
- scenario_name (TEXT)
- completed (BOOLEAN DEFAULT false)
- score (INTEGER)
- time_taken (INTEGER)
- attempts (INTEGER DEFAULT 1)
- completed_at (TIMESTAMP)
- created_at (TIMESTAMP DEFAULT NOW())
- UNIQUE(user_email, scenario_id)
```
⚠️ NEEDS CHECKING

---

## CRITICAL FIELD NAME MISMATCHES FOUND:

### CANCER MODULE:
- ❌ `patient_id` → ✅ `pathway_id`
- ❌ `pathway_start_date` → ✅ `clock_start_date`
- ❌ Extra fields removed ✅

### MDT MODULE:
- ❌ `chair` → ✅ `chair_person`
- ❌ `patients` → ✅ `patients_discussed`
- ❌ `outcomes` → ✅ `decisions`
- ❌ `last_updated` → ✅ `updated_at`
- ❌ Extra fields removed ✅

### PTL MODULE:
- ✅ Already correct!

---

## ALL FIXES COMPLETED:
1. ✅ PTL System - Already correct
2. ✅ Cancer Pathway System - FIXED
3. ✅ MDT Coordination System - FIXED
4. ⏳ Appointments - Need to check
5. ⏳ Validation History - Need to check
6. ⏳ Training Progress - Need to check

---

**RESTART APP TO LOAD ALL FIXES!**
