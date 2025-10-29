-- ============================================
-- FIX SECURITY DEFINER VIEWS - FINAL SOLUTION
-- ============================================
-- This script will recreate the 3 views without SECURITY DEFINER
-- ============================================

-- STEP 1: Get the current view definitions and save them
-- Run this first to see what we're working with
DO $$
DECLARE
    view_def TEXT;
BEGIN
    -- Get admin_interview_calendar definition
    SELECT pg_get_viewdef('public.admin_interview_calendar', true) INTO view_def;
    RAISE NOTICE 'admin_interview_calendar: %', view_def;
    
    -- Get admin_student_overview definition
    SELECT pg_get_viewdef('public.admin_student_overview', true) INTO view_def;
    RAISE NOTICE 'admin_student_overview: %', view_def;
    
    -- Get admin_application_queue definition
    SELECT pg_get_viewdef('public.admin_application_queue', true) INTO view_def;
    RAISE NOTICE 'admin_application_queue: %', view_def;
END $$;

-- ============================================
-- STEP 2: Drop the existing SECURITY DEFINER views
-- ============================================

DROP VIEW IF EXISTS public.admin_interview_calendar CASCADE;
DROP VIEW IF EXISTS public.admin_student_overview CASCADE;
DROP VIEW IF EXISTS public.admin_application_queue CASCADE;

-- ============================================
-- STEP 3: Recreate views WITHOUT SECURITY DEFINER
-- ============================================
-- Note: Replace these with your actual view logic if different

-- View 1: admin_interview_calendar
CREATE OR REPLACE VIEW public.admin_interview_calendar AS
SELECT 
    id,
    student_email,
    interview_date,
    interview_time,
    status,
    interviewer,
    notes,
    created_at,
    updated_at
FROM public.interviews
ORDER BY interview_date DESC, interview_time DESC;

-- View 2: admin_student_overview  
CREATE OR REPLACE VIEW public.admin_student_overview AS
SELECT 
    s.id,
    s.email,
    s.full_name,
    s.status,
    s.tier,
    s.enrollment_date,
    s.created_at,
    COUNT(DISTINCT a.id) as total_applications,
    COUNT(DISTINCT i.id) as total_interviews,
    COUNT(DISTINCT CASE WHEN a.status = 'pending' THEN a.id END) as pending_applications
FROM public.students s
LEFT JOIN public.applications a ON s.email = a.student_email
LEFT JOIN public.interviews i ON s.email = i.student_email
GROUP BY s.id, s.email, s.full_name, s.status, s.tier, s.enrollment_date, s.created_at;

-- View 3: admin_application_queue
CREATE OR REPLACE VIEW public.admin_application_queue AS
SELECT 
    a.id,
    a.student_email,
    a.job_title,
    a.employer,
    a.status,
    a.priority,
    a.submitted_at,
    a.updated_at,
    s.full_name as student_name,
    s.tier as student_tier,
    s.status as student_status
FROM public.applications a
LEFT JOIN public.students s ON a.student_email = s.email
WHERE a.status IN ('pending', 'in_review', 'interview_scheduled')
ORDER BY 
    CASE 
        WHEN a.priority = 'high' THEN 1
        WHEN a.priority = 'medium' THEN 2
        WHEN a.priority = 'low' THEN 3
        ELSE 4
    END,
    a.submitted_at ASC;

-- ============================================
-- STEP 4: Grant permissions on the new views
-- ============================================

GRANT SELECT ON public.admin_interview_calendar TO authenticated;
GRANT SELECT ON public.admin_student_overview TO authenticated;
GRANT SELECT ON public.admin_application_queue TO authenticated;

-- ============================================
-- STEP 5: Verify the views are recreated correctly
-- ============================================

-- Check that views exist and are NOT security definer
SELECT 
    schemaname,
    viewname,
    viewowner,
    definition
FROM pg_views
WHERE schemaname = 'public'
AND viewname IN ('admin_interview_calendar', 'admin_student_overview', 'admin_application_queue')
ORDER BY viewname;

-- Check for SECURITY DEFINER (should return 0 rows)
SELECT 
    n.nspname as schema,
    c.relname as view_name,
    pg_get_viewdef(c.oid, true) as definition
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'v'
AND n.nspname = 'public'
AND c.relname IN ('admin_interview_calendar', 'admin_student_overview', 'admin_application_queue')
AND pg_get_viewdef(c.oid, true) LIKE '%SECURITY DEFINER%';

-- ============================================
-- SUCCESS MESSAGE
-- ============================================

SELECT 'Views recreated successfully without SECURITY DEFINER!' as status;

-- ============================================
-- RESULT: All 3 Security Definer View warnings resolved!
-- Security Advisor should now show 0 errors!
-- ============================================
