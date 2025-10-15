-- =====================================================
-- T21 COMPLETE NHS TRAINING SYSTEM - DATABASE SETUP
-- =====================================================
-- Run this in Supabase SQL Editor to set up ALL tables
-- Version: 3.0 - Complete System
-- Date: October 15, 2025
-- =====================================================

-- =====================================================
-- PART 1: APPOINTMENT-PATHWAY LINKS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.appointment_pathway_links (
    id BIGSERIAL PRIMARY KEY,
    appointment_id TEXT NOT NULL,
    pathway_id TEXT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_type TEXT,
    consultant TEXT,
    clinic TEXT,
    outcome TEXT,
    linked_date TIMESTAMPTZ DEFAULT NOW(),
    user_email TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_appt_pathway_pathway ON public.appointment_pathway_links(pathway_id);
CREATE INDEX IF NOT EXISTS idx_appt_pathway_appt ON public.appointment_pathway_links(appointment_id);

-- =====================================================
-- PART 2: WAITING LIST
-- =====================================================

CREATE TABLE IF NOT EXISTS public.waiting_list (
    id BIGSERIAL PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    specialty TEXT,
    procedure TEXT,
    priority TEXT DEFAULT 'Routine',
    position INTEGER,
    added_date DATE DEFAULT CURRENT_DATE,
    expected_wait_weeks INTEGER,
    expected_date DATE,
    status TEXT DEFAULT 'waiting',
    removed_date DATE,
    removal_reason TEXT,
    priority_changed_date DATE,
    notes TEXT,
    user_email TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_waiting_list_pathway ON public.waiting_list(pathway_id);
CREATE INDEX IF NOT EXISTS idx_waiting_list_status ON public.waiting_list(status);
CREATE INDEX IF NOT EXISTS idx_waiting_list_specialty ON public.waiting_list(specialty);

-- =====================================================
-- PART 3: DNA RECORDS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.dna_records (
    id BIGSERIAL PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    appointment_id TEXT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_type TEXT,
    clinic TEXT,
    consultant TEXT,
    recorded_date DATE DEFAULT CURRENT_DATE,
    notes TEXT,
    user_email TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dna_pathway ON public.dna_records(pathway_id);
CREATE INDEX IF NOT EXISTS idx_dna_patient ON public.dna_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_dna_date ON public.dna_records(recorded_date);

-- =====================================================
-- PART 4: CANCELLATION RECORDS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.cancellation_records (
    id BIGSERIAL PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    appointment_id TEXT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_type TEXT,
    cancelled_by TEXT,  -- 'Patient' or 'Hospital'
    reason TEXT,
    rebook_required BOOLEAN DEFAULT TRUE,
    clinic TEXT,
    consultant TEXT,
    cancelled_date DATE DEFAULT CURRENT_DATE,
    notes TEXT,
    user_email TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cancellation_pathway ON public.cancellation_records(pathway_id);
CREATE INDEX IF NOT EXISTS idx_cancellation_patient ON public.cancellation_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_cancellation_cancelled_by ON public.cancellation_records(cancelled_by);

-- =====================================================
-- PART 5: UPDATE EXISTING PATHWAYS TABLE
-- Add all NHS workflow fields if not already present
-- =====================================================

-- Clock pause/resume fields
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS clock_paused BOOLEAN DEFAULT FALSE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS pause_reason TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS pause_start_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS pause_end_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS total_pause_days INTEGER DEFAULT 0;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS pause_history JSONB DEFAULT '[]'::jsonb;

-- Milestone tracking fields
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS first_appointment_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS first_appointment_attended BOOLEAN;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS decision_to_treat_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS treatment_start_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS admission_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS surgery_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS discharge_date DATE;

-- Days to milestones (calculated)
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS days_to_first_appointment INTEGER;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS days_to_decision_to_treat INTEGER;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS days_to_treatment INTEGER;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS days_to_discharge INTEGER;

-- RTT status management
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS rtt_status TEXT DEFAULT 'active';
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS waiting_list_status TEXT DEFAULT 'not_listed';
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS treatment_received BOOLEAN DEFAULT FALSE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS treatment_outcome TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS discharge_reason TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS discharge_destination TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS follow_up_required BOOLEAN DEFAULT FALSE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS follow_up_date DATE;

-- Waiting list tracking
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS waiting_list_entry_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS waiting_list_position INTEGER;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS expected_wait_weeks INTEGER;

-- DNA and cancellation tracking
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS dna_count INTEGER DEFAULT 0;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS last_dna_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS cancellation_count INTEGER DEFAULT 0;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS last_cancellation_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS last_cancellation_reason TEXT;

-- =====================================================
-- PART 6: UPDATE EXISTING EPISODES TABLE
-- Add episode codes and deletion tracking
-- =====================================================

ALTER TABLE public.episodes ADD COLUMN IF NOT EXISTS episode_code TEXT;
ALTER TABLE public.episodes ADD COLUMN IF NOT EXISTS deleted BOOLEAN DEFAULT FALSE;
ALTER TABLE public.episodes ADD COLUMN IF NOT EXISTS deleted_date TIMESTAMPTZ;
ALTER TABLE public.episodes ADD COLUMN IF NOT EXISTS deletion_reason TEXT;

-- =====================================================
-- PART 7: ENABLE ROW LEVEL SECURITY (Optional)
-- Uncomment if you want user isolation
-- =====================================================

-- ALTER TABLE public.appointment_pathway_links ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE public.waiting_list ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE public.dna_records ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE public.cancellation_records ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "Users can see own appointment links" ON public.appointment_pathway_links
--     FOR ALL USING (auth.email() = user_email);

-- CREATE POLICY "Users can see own waiting list" ON public.waiting_list
--     FOR ALL USING (auth.email() = user_email);

-- CREATE POLICY "Users can see own DNA records" ON public.dna_records
--     FOR ALL USING (auth.email() = user_email);

-- CREATE POLICY "Users can see own cancellations" ON public.cancellation_records
--     FOR ALL USING (auth.email() = user_email);

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check all tables exist
SELECT 'appointment_pathway_links' as table_name, COUNT(*) as row_count FROM public.appointment_pathway_links
UNION ALL
SELECT 'waiting_list', COUNT(*) FROM public.waiting_list
UNION ALL
SELECT 'dna_records', COUNT(*) FROM public.dna_records
UNION ALL
SELECT 'cancellation_records', COUNT(*) FROM public.cancellation_records;

-- Check pathways table columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'pathways' 
  AND column_name IN ('clock_paused', 'first_appointment_date', 'rtt_status', 'dna_count')
ORDER BY column_name;

-- Check episodes table columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'episodes' 
  AND column_name IN ('episode_code', 'deleted')
ORDER BY column_name;

-- =====================================================
-- SUCCESS MESSAGE
-- =====================================================

SELECT '✅ DATABASE SETUP COMPLETE!' as status,
       'All tables created and columns added successfully' as message,
       NOW() as completed_at;

-- =====================================================
-- NOTES
-- =====================================================
-- 
-- This script is idempotent - safe to run multiple times
-- It uses IF NOT EXISTS and ADD COLUMN IF NOT EXISTS
-- 
-- Tables created:
-- 1. appointment_pathway_links - Link appointments to pathways
-- 2. waiting_list - Patient waiting list management
-- 3. dna_records - Did Not Attend tracking
-- 4. cancellation_records - Appointment cancellations
--
-- Tables updated:
-- 1. pathways - Added ~30 new NHS workflow columns
-- 2. episodes - Added episode codes and deletion tracking
--
-- =====================================================
