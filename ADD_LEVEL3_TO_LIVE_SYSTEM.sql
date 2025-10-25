-- ADD LEVEL 3 ACCESS TO IJEOMA (AND ANY STUDENT)
-- Run this in Supabase SQL Editor
-- This will make Level 3 work even before deployment!

-- 1. Add Level 3 module access for Ijeoma
INSERT INTO module_access (user_email, module_name, granted_by, granted_at)
VALUES 
    ('ijeoma234@gmail.com', '📚 Level 3 Adult Care', 'admin@t21services.co.uk', NOW()),
    ('ijeoma234@gmail.com', '📚 TQUK Document Library', 'admin@t21services.co.uk', NOW()),
    ('ijeoma234@gmail.com', 'ℹ️ Help & Information', 'admin@t21services.co.uk', NOW())
ON CONFLICT (user_email, module_name) DO NOTHING;

-- 2. Enroll in Level 3 course
INSERT INTO tquk_enrollments (learner_email, course_code, course_name, qualification_code, enrollment_date, status, assigned_by)
VALUES 
    ('ijeoma234@gmail.com', 'level3_adult_care', 'Level 3 Diploma in Adult Care', '610/0103/6', NOW(), 'active', 'admin@t21services.co.uk')
ON CONFLICT (learner_email, course_code) DO NOTHING;

-- 3. Verify it worked
SELECT 
    'Module Access' as type,
    module_name,
    granted_at
FROM module_access 
WHERE user_email = 'ijeoma234@gmail.com'

UNION ALL

SELECT 
    'Course Enrollment' as type,
    course_name,
    enrollment_date
FROM tquk_enrollments 
WHERE learner_email = 'ijeoma234@gmail.com';


-- ============================================
-- FOR OTHER STUDENTS: Replace email and run again
-- ============================================

-- Example for another student:
-- INSERT INTO module_access (user_email, module_name, granted_by, granted_at)
-- VALUES 
--     ('student@example.com', '📚 Level 3 Adult Care', 'admin@t21services.co.uk', NOW()),
--     ('student@example.com', '📚 TQUK Document Library', 'admin@t21services.co.uk', NOW()),
--     ('student@example.com', 'ℹ️ Help & Information', 'admin@t21services.co.uk', NOW())
-- ON CONFLICT (user_email, module_name) DO NOTHING;
