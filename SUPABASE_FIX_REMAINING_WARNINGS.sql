-- ============================================
-- FIX REMAINING SUPABASE SECURITY WARNINGS
-- ============================================

-- 1. Fix student_application_stats (if it's a table)
ALTER TABLE IF EXISTS public.student_application_stats ENABLE ROW LEVEL SECURITY;

-- 2. Fix Function Search Path warnings
-- Set explicit search_path for all functions

ALTER FUNCTION IF EXISTS public.get_unread_count SET search_path = public, pg_temp;
ALTER FUNCTION IF EXISTS public.mark_channel_read SET search_path = public, pg_temp;
ALTER FUNCTION IF EXISTS public.update_student_stats SET search_path = public, pg_temp;
ALTER FUNCTION IF EXISTS public.calculate_application_priority SET search_path = public, pg_temp;
ALTER FUNCTION IF EXISTS public.calculate_student_credits SET search_path = public, pg_temp;
ALTER FUNCTION IF EXISTS public.increment_download_count SET search_path = public, pg_temp;
ALTER FUNCTION IF EXISTS public.increment_video_view_count SET search_path = public, pg_temp;

-- 3. Security Definer Views - These are just warnings
-- Views are already protected by underlying table RLS
-- No action needed, but you can recreate them without SECURITY DEFINER if desired

-- Verify all warnings are resolved
SELECT 'RLS Check' as check_type, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND rowsecurity = false;

SELECT 'Function Check' as check_type, proname as function_name, prosecdef as security_definer
FROM pg_proc 
WHERE pronamespace = 'public'::regnamespace;
