-- ============================================
-- FIX EVERYTHING - COMPLETE SOLUTION
-- Run this in Supabase SQL Editor
-- ============================================

-- Step 1: Check if tquk_enrollments table exists and what columns it has
-- If this fails, we need to create the table first

-- Step 2: Grant Level 3 Access to Ijeoma (and works for any student)
-- This WILL work because module_access table exists

INSERT INTO module_access (user_email, module_name, granted_by, granted_at)
VALUES 
    ('ijeoma234@gmail.com', '📚 Level 3 Adult Care', 'admin@t21services.co.uk', NOW()),
    ('ijeoma234@gmail.com', '📚 TQUK Document Library', 'admin@t21services.co.uk', NOW()),
    ('ijeoma234@gmail.com', 'ℹ️ Help & Information', 'admin@t21services.co.uk', NOW()),
    ('ijeoma234@gmail.com', '⚙️ My Account', 'admin@t21services.co.uk', NOW()),
    ('ijeoma234@gmail.com', '📧 Contact & Support', 'admin@t21services.co.uk', NOW())
ON CONFLICT (user_email, module_name) DO NOTHING;

-- Step 3: Create tquk_enrollments table if it doesn't exist
CREATE TABLE IF NOT EXISTS tquk_enrollments (
    id BIGSERIAL PRIMARY KEY,
    learner_email TEXT NOT NULL,
    course_id TEXT NOT NULL,
    course_name TEXT NOT NULL,
    qualification_code TEXT,
    enrollment_date TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'active',
    assigned_by TEXT,
    progress INTEGER DEFAULT 0,
    completed_date TIMESTAMP,
    certificate_issued BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(learner_email, course_id)
);

-- Step 4: Now enroll Ijeoma in Level 3 course
INSERT INTO tquk_enrollments (learner_email, course_id, course_name, qualification_code, enrollment_date, status, assigned_by)
VALUES 
    ('ijeoma234@gmail.com', 'level3_adult_care', 'Level 3 Diploma in Adult Care', '610/0103/6', NOW(), 'active', 'admin@t21services.co.uk')
ON CONFLICT (learner_email, course_id) DO NOTHING;

-- Step 5: Verify everything worked
SELECT 
    'Module Access' as type,
    module_name as name,
    granted_at as date
FROM module_access 
WHERE user_email = 'ijeoma234@gmail.com'

UNION ALL

SELECT 
    'Course Enrollment' as type,
    course_name as name,
    enrollment_date as date
FROM tquk_enrollments 
WHERE learner_email = 'ijeoma234@gmail.com';

-- ============================================
-- SUCCESS MESSAGE
-- ============================================
-- If you see results above, Ijeoma now has:
-- 1. ✅ Module access to Level 3 Adult Care
-- 2. ✅ Enrolled in Level 3 course
-- 3. ✅ Access to TQUK Document Library
-- 4. ✅ Basic access modules
--
-- Tell her to refresh her page (Ctrl+Shift+R)
-- She'll see "📚 Level 3 Adult Care" in her sidebar!
-- ============================================


-- ============================================
-- FOR OTHER STUDENTS: Copy this template
-- ============================================
/*
-- Replace 'student@example.com' with the actual student email

INSERT INTO module_access (user_email, module_name, granted_by, granted_at)
VALUES 
    ('student@example.com', '📚 Level 3 Adult Care', 'admin@t21services.co.uk', NOW()),
    ('student@example.com', '📚 TQUK Document Library', 'admin@t21services.co.uk', NOW()),
    ('student@example.com', 'ℹ️ Help & Information', 'admin@t21services.co.uk', NOW())
ON CONFLICT (user_email, module_name) DO NOTHING;

INSERT INTO tquk_enrollments (learner_email, course_id, course_name, qualification_code, enrollment_date, status, assigned_by)
VALUES 
    ('student@example.com', 'level3_adult_care', 'Level 3 Diploma in Adult Care', '610/0103/6', NOW(), 'active', 'admin@t21services.co.uk')
ON CONFLICT (learner_email, course_id) DO NOTHING;
*/
