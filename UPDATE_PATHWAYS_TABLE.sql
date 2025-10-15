-- UPDATE PATHWAYS TABLE TO ADD NHS WORKFLOW FIELDS
-- Run this in Supabase SQL Editor

-- Add new columns for complete NHS workflow
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS referral_method TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS referral_received_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS clock_start_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS earliest_reasonable_offer_date DATE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS presenting_complaint TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS suspected_diagnosis TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS gp_name TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS gp_practice TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS patient_informed BOOLEAN DEFAULT TRUE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS interpreter_required BOOLEAN DEFAULT FALSE;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS language_needed TEXT;
ALTER TABLE public.pathways ADD COLUMN IF NOT EXISTS additional_needs TEXT;

-- Success message
SELECT 'Pathways table updated with NHS workflow fields!' as message;
