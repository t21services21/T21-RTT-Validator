-- ============================================
-- OPTIMIZE SLOW QUERIES - PERFORMANCE FIX
-- ============================================
-- This script creates indexes to speed up slow queries
-- Run this in Supabase SQL Editor
-- ============================================

-- First, let's analyze which tables are being queried most
-- and create appropriate indexes

-- ============================================
-- COMMON INDEXES FOR TYPICAL QUERIES
-- ============================================

-- Students table indexes
CREATE INDEX IF NOT EXISTS idx_students_email ON public.students(email);
CREATE INDEX IF NOT EXISTS idx_students_status ON public.students(status);
CREATE INDEX IF NOT EXISTS idx_students_tier ON public.students(tier);
CREATE INDEX IF NOT EXISTS idx_students_created_at ON public.students(created_at);

-- Applications table indexes
CREATE INDEX IF NOT EXISTS idx_applications_student_email ON public.applications(student_email);
CREATE INDEX IF NOT EXISTS idx_applications_status ON public.applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_priority ON public.applications(priority);
CREATE INDEX IF NOT EXISTS idx_applications_submitted_at ON public.applications(submitted_at);
CREATE INDEX IF NOT EXISTS idx_applications_status_priority ON public.applications(status, priority);

-- Interviews table indexes
CREATE INDEX IF NOT EXISTS idx_interviews_student_email ON public.interviews(student_email);
CREATE INDEX IF NOT EXISTS idx_interviews_interview_date ON public.interviews(interview_date);
CREATE INDEX IF NOT EXISTS idx_interviews_status ON public.interviews(status);
CREATE INDEX IF NOT EXISTS idx_interviews_date_time ON public.interviews(interview_date, interview_time);

-- Tasks table indexes
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON public.tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON public.tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON public.tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON public.tasks(created_at);

-- Messages table indexes
CREATE INDEX IF NOT EXISTS idx_trac_inbox_messages_recipient ON public.trac_inbox_messages(recipient_email);
CREATE INDEX IF NOT EXISTS idx_trac_inbox_messages_sender ON public.trac_inbox_messages(sender_email);
CREATE INDEX IF NOT EXISTS idx_trac_inbox_messages_read ON public.trac_inbox_messages(is_read);
CREATE INDEX IF NOT EXISTS idx_trac_inbox_messages_created ON public.trac_inbox_messages(created_at);

-- Direct messages indexes
CREATE INDEX IF NOT EXISTS idx_direct_messages_sender ON public.direct_messages(sender_email);
CREATE INDEX IF NOT EXISTS idx_direct_messages_recipient ON public.direct_messages(recipient_email);
CREATE INDEX IF NOT EXISTS idx_direct_messages_created ON public.direct_messages(created_at);
CREATE INDEX IF NOT EXISTS idx_direct_messages_deleted ON public.direct_messages(is_deleted);

-- Quiz tables indexes
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_student ON public.quiz_attempts(student_email);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_quiz ON public.quiz_attempts(quiz_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_created ON public.quiz_attempts(created_at);

-- Student progress indexes
CREATE INDEX IF NOT EXISTS idx_student_progress_email ON public.student_progress(student_email);
CREATE INDEX IF NOT EXISTS idx_student_progress_course ON public.student_progress(course_id);
CREATE INDEX IF NOT EXISTS idx_student_progress_updated ON public.student_progress(updated_at);

-- Email notifications indexes
CREATE INDEX IF NOT EXISTS idx_email_notifications_recipient ON public.email_notifications(recipient_email);
CREATE INDEX IF NOT EXISTS idx_email_notifications_sent ON public.email_notifications(sent_at);
CREATE INDEX IF NOT EXISTS idx_email_notifications_status ON public.email_notifications(status);

-- Waiting list indexes
CREATE INDEX IF NOT EXISTS idx_waiting_list_patient_id ON public.waiting_list(patient_id);
CREATE INDEX IF NOT EXISTS idx_waiting_list_priority ON public.waiting_list(priority);
CREATE INDEX IF NOT EXISTS idx_waiting_list_added_date ON public.waiting_list(added_date);

-- ============================================
-- COMPOSITE INDEXES FOR COMPLEX QUERIES
-- ============================================

-- For filtering applications by status and sorting by date
CREATE INDEX IF NOT EXISTS idx_applications_status_submitted ON public.applications(status, submitted_at DESC);

-- For student overview queries
CREATE INDEX IF NOT EXISTS idx_students_status_tier ON public.students(status, tier);

-- For interview scheduling queries
CREATE INDEX IF NOT EXISTS idx_interviews_status_date ON public.interviews(status, interview_date);

-- For message queries (sender/recipient combinations)
CREATE INDEX IF NOT EXISTS idx_direct_messages_sender_recipient ON public.direct_messages(sender_email, recipient_email, created_at DESC);

-- ============================================
-- ANALYZE TABLES TO UPDATE STATISTICS
-- ============================================

ANALYZE public.students;
ANALYZE public.applications;
ANALYZE public.interviews;
ANALYZE public.tasks;
ANALYZE public.trac_inbox_messages;
ANALYZE public.direct_messages;
ANALYZE public.quiz_attempts;
ANALYZE public.student_progress;
ANALYZE public.email_notifications;
ANALYZE public.waiting_list;

-- ============================================
-- VERIFY INDEXES CREATED
-- ============================================

SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- ============================================
-- CHECK INDEX USAGE
-- ============================================

SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- ============================================
-- SUCCESS MESSAGE
-- ============================================

SELECT 'Indexes created successfully! Query performance should improve significantly.' as status;

-- ============================================
-- NOTES:
-- ============================================
-- 1. Indexes speed up SELECT queries but slow down INSERT/UPDATE/DELETE slightly
-- 2. Monitor query performance after creating indexes
-- 3. Drop unused indexes if they don't improve performance
-- 4. Run ANALYZE periodically to update statistics
-- 5. Consider VACUUM ANALYZE for maintenance

-- To drop an index if needed:
-- DROP INDEX IF EXISTS index_name;

-- To see table sizes:
-- SELECT 
--     schemaname,
--     tablename,
--     pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
-- FROM pg_tables
-- WHERE schemaname = 'public'
-- ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- ============================================
-- RESULT: Slow queries should be much faster!
-- ============================================
