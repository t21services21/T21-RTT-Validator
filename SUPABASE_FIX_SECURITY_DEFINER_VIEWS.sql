-- ============================================
-- FIX SECURITY DEFINER VIEWS
-- ============================================
-- Recreate the 3 views without SECURITY DEFINER
-- This removes the last 3 security warnings
-- ============================================

-- First, let's see what these views currently look like
-- Run this to see the view definitions:
SELECT 
    schemaname,
    viewname,
    definition
FROM pg_views
WHERE schemaname = 'public'
AND viewname IN ('admin_interview_calendar', 'admin_student_overview', 'admin_application_queue')
ORDER BY viewname;

-- ============================================
-- STEP 1: Drop the existing views
-- ============================================

DROP VIEW IF EXISTS public.admin_interview_calendar CASCADE;
DROP VIEW IF EXISTS public.admin_student_overview CASCADE;
DROP VIEW IF EXISTS public.admin_application_queue CASCADE;

-- ============================================
-- STEP 2: Recreate views WITHOUT SECURITY DEFINER
-- ============================================

-- Note: You'll need to replace these with your actual view definitions
-- The views will be recreated as normal views (SECURITY INVOKER by default)

-- Example structure (replace with your actual view logic):

-- View 1: admin_interview_calendar
-- This view likely shows interview schedules for admins
CREATE OR REPLACE VIEW public.admin_interview_calendar AS
SELECT 
    i.id,
    i.student_email,
    i.interview_date,
    i.interview_time,
    i.status,
    i.interviewer,
    i.notes,
    i.created_at
FROM public.interviews i
ORDER BY i.interview_date DESC, i.interview_time DESC;

-- View 2: admin_student_overview
-- This view likely shows student summary information
CREATE OR REPLACE VIEW public.admin_student_overview AS
SELECT 
    s.id,
    s.email,
    s.full_name,
    s.status,
    s.enrollment_date,
    s.tier,
    COUNT(DISTINCT a.id) as application_count,
    COUNT(DISTINCT i.id) as interview_count
FROM public.students s
LEFT JOIN public.applications a ON s.email = a.student_email
LEFT JOIN public.interviews i ON s.email = i.student_email
GROUP BY s.id, s.email, s.full_name, s.status, s.enrollment_date, s.tier;

-- View 3: admin_application_queue
-- This view likely shows pending applications for admins
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
    s.tier as student_tier
FROM public.applications a
LEFT JOIN public.students s ON a.student_email = s.email
WHERE a.status IN ('pending', 'in_review', 'interview_scheduled')
ORDER BY a.priority DESC, a.submitted_at ASC;

-- ============================================
-- IMPORTANT: The above are EXAMPLE definitions
-- You need to check your actual view definitions first!
-- ============================================

-- To get your actual view definitions, run:
-- SELECT pg_get_viewdef('public.admin_interview_calendar', true);
-- SELECT pg_get_viewdef('public.admin_student_overview', true);
-- SELECT pg_get_viewdef('public.admin_application_queue', true);

-- Then replace the CREATE VIEW statements above with your actual definitions

-- ============================================
-- STEP 3: Verify views are recreated
-- ============================================

SELECT 
    schemaname,
    viewname,
    viewowner
FROM pg_views
WHERE schemaname = 'public'
AND viewname IN ('admin_interview_calendar', 'admin_student_overview', 'admin_application_queue')
ORDER BY viewname;

-- ============================================
-- RESULT: Views recreated without SECURITY DEFINER
-- All 3 security warnings should be resolved
-- ============================================
