-- ============================================================================
-- FIX JOB AUTOMATION FOREIGN KEY CONSTRAINTS
-- Change all references from "students" table to "users" table
-- ============================================================================

-- Drop all existing foreign key constraints
ALTER TABLE student_automation_settings DROP CONSTRAINT IF EXISTS student_automation_settings_student_id_fkey;
ALTER TABLE applications DROP CONSTRAINT IF EXISTS applications_student_id_fkey;
ALTER TABLE interviews DROP CONSTRAINT IF EXISTS interviews_student_id_fkey;
ALTER TABLE trac_inbox_messages DROP CONSTRAINT IF EXISTS trac_inbox_messages_student_id_fkey;
ALTER TABLE email_notifications DROP CONSTRAINT IF EXISTS email_notifications_student_id_fkey;
ALTER TABLE student_application_stats DROP CONSTRAINT IF EXISTS student_application_stats_student_id_fkey;

-- Add new foreign key constraints referencing "users" table instead
ALTER TABLE student_automation_settings 
ADD CONSTRAINT student_automation_settings_student_id_fkey 
FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE applications 
ADD CONSTRAINT applications_student_id_fkey 
FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE interviews 
ADD CONSTRAINT interviews_student_id_fkey 
FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE trac_inbox_messages 
ADD CONSTRAINT trac_inbox_messages_student_id_fkey 
FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE email_notifications 
ADD CONSTRAINT email_notifications_student_id_fkey 
FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE student_application_stats 
ADD CONSTRAINT student_application_stats_student_id_fkey 
FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE;

-- Update views to use users table
DROP VIEW IF EXISTS admin_student_overview;

CREATE OR REPLACE VIEW admin_student_overview AS
SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.email,
    sas.auto_submit_enabled,
    sas.status AS automation_status,
    sas.requires_sponsorship,
    stats.total_applications,
    stats.applications_submitted,
    stats.interviews_invited,
    stats.offers_received,
    stats.overall_success_rate,
    stats.last_application_date,
    sas.created_at AS automation_started
FROM users u
LEFT JOIN student_automation_settings sas ON u.id = sas.student_id
LEFT JOIN student_application_stats stats ON u.id = stats.student_id
WHERE u.role LIKE '%student%' OR u.user_type = 'student'
ORDER BY stats.last_application_date DESC NULLS LAST;

DROP VIEW IF EXISTS admin_application_queue;

CREATE OR REPLACE VIEW admin_application_queue AS
SELECT 
    a.id,
    u.first_name || ' ' || u.last_name AS student_name,
    dj.title AS job_title,
    dj.trust,
    dj.location,
    dj.closing_date,
    a.status,
    a.priority,
    a.scheduled_submit_time,
    a.attempts,
    a.created_at
FROM applications a
JOIN users u ON a.student_id = u.id
JOIN discovered_jobs dj ON a.job_id = dj.id
ORDER BY a.scheduled_submit_time ASC NULLS LAST;

DROP VIEW IF EXISTS admin_interview_calendar;

CREATE OR REPLACE VIEW admin_interview_calendar AS
SELECT 
    i.id,
    u.first_name || ' ' || u.last_name AS student_name,
    u.email AS student_email,
    dj.title AS job_title,
    dj.trust,
    i.interview_date,
    i.interview_location,
    i.interview_format,
    i.status,
    i.outcome
FROM interviews i
JOIN users u ON i.student_id = u.id
LEFT JOIN discovered_jobs dj ON i.job_id = dj.id
WHERE i.status IN ('scheduled', 'confirmed')
ORDER BY i.interview_date ASC;

-- Success message
SELECT 'Foreign key constraints updated successfully! Now references users table instead of students table.' AS status;
