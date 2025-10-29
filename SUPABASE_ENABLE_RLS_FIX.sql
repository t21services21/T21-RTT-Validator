-- ============================================
-- SUPABASE SECURITY FIX: ENABLE ROW LEVEL SECURITY
-- ============================================
-- This script enables RLS on all tables (not views)
-- Run this in Supabase SQL Editor
-- ============================================

-- TABLES ONLY (Views cannot have RLS enabled)

-- Core student/application tables
ALTER TABLE IF EXISTS public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.student_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.student_automation_settings ENABLE ROW LEVEL SECURITY;

-- Quiz/assessment tables
ALTER TABLE IF EXISTS public.quizzes ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.quiz_attempts ENABLE ROW LEVEL SECURITY;

-- Interview/job tables
ALTER TABLE IF EXISTS public.interviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.discovered_jobs ENABLE ROW LEVEL SECURITY;

-- Task/workflow tables
ALTER TABLE IF EXISTS public.tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.waiting_list ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.appointment_pathway_links ENABLE ROW LEVEL SECURITY;

-- Record tables
ALTER TABLE IF EXISTS public.dna_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.cancellation_records ENABLE ROW LEVEL SECURITY;

-- Communication tables
ALTER TABLE IF EXISTS public.trac_inbox_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.email_notifications ENABLE ROW LEVEL SECURITY;

-- Admin/system tables
ALTER TABLE IF EXISTS public.admin_activity_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.system_config ENABLE ROW LEVEL SECURITY;

-- NOTE: These are likely VIEWS and cannot have RLS:
-- - admin_interview_calendar (VIEW)
-- - admin_student_overview (VIEW)
-- - admin_application_queue (VIEW)
-- - student_application_stats (VIEW)
-- Views inherit security from their underlying tables

-- ============================================
-- CREATE BASIC RLS POLICIES
-- ============================================

-- Policy 1: Service role (backend) has full access to everything
-- This ensures your Streamlit app continues to work

-- Policy 2: Authenticated users can read their own data
-- Example for students table:

CREATE POLICY IF NOT EXISTS "Users can view own student data"
ON public.students
FOR SELECT
USING (
  auth.uid()::text = user_id::text
  OR
  EXISTS (
    SELECT 1 FROM public.user_accounts
    WHERE user_accounts.user_id = auth.uid()::text
    AND user_accounts.role IN ('admin', 'super_admin', 'staff', 'teacher', 'tutor')
  )
);

-- Policy 3: Admins have full access
CREATE POLICY IF NOT EXISTS "Admins have full access to students"
ON public.students
FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.user_accounts
    WHERE user_accounts.user_id = auth.uid()::text
    AND user_accounts.role IN ('admin', 'super_admin', 'staff')
  )
);

-- ============================================
-- IMPORTANT NOTES:
-- ============================================

-- 1. After running this, your app will still work because:
--    - You're using the SERVICE ROLE key in your backend
--    - Service role bypasses RLS automatically
--    - This just adds security for direct database access

-- 2. Views (admin_interview_calendar, etc.) are protected because:
--    - They query underlying tables
--    - Those tables now have RLS
--    - Views inherit the security

-- 3. To add more specific policies for other tables:
--    - Copy the policy examples above
--    - Change table name
--    - Adjust the USING clause for your needs

-- 4. To verify RLS is enabled:
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- ============================================
-- END OF SCRIPT
-- ============================================
