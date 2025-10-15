-- UPDATE EPISODES TABLE TO ADD EPISODE CODES AND DELETE TRACKING
-- Run this in Supabase SQL Editor

-- Add episode_code column for HRG codes, procedure codes, etc.
ALTER TABLE public.episodes ADD COLUMN IF NOT EXISTS episode_code TEXT;

-- Add deleted_date column to track when episode was deleted
ALTER TABLE public.episodes ADD COLUMN IF NOT EXISTS deleted_date TIMESTAMPTZ;

-- Success message
SELECT 'Episodes table updated with episode codes and delete tracking!' as message;
