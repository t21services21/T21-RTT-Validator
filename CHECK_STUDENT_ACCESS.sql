-- ============================================
-- CHECK STUDENT ACCESS - DIAGNOSTIC TOOL
-- Run this to see what access the student has
-- ============================================

-- Replace 'ijeoma234@gmail.com' with the student's email

-- Check 1: What modules does the student have access to?
SELECT 
    'MODULE ACCESS' as check_type,
    module_name,
    granted_by,
    granted_at
FROM module_access 
WHERE user_email = 'ijeoma234@gmail.com'
ORDER BY granted_at DESC;

-- Check 2: Is the student enrolled in any TQUK courses?
SELECT 
    'COURSE ENROLLMENT' as check_type,
    course_id,
    course_name,
    status,
    assigned_by
FROM tquk_enrollments 
WHERE learner_email = 'ijeoma234@gmail.com';

-- Check 3: What is the student's user type?
SELECT 
    'USER INFO' as check_type,
    email,
    user_type,
    full_name
FROM users 
WHERE email = 'ijeoma234@gmail.com';

-- ============================================
-- WHAT TO LOOK FOR:
-- ============================================
-- 
-- MODULE ACCESS should show:
-- - 📚 Level 3 Adult Care
-- - 📚 TQUK Document Library
-- - ℹ️ Help & Information
-- - ⚙️ My Account
--
-- COURSE ENROLLMENT should show:
-- - level3_adult_care | Level 3 Diploma in Adult Care
--
-- USER INFO should show:
-- - user_type: student
--
-- If any of these are missing, that's the problem!
-- ============================================
