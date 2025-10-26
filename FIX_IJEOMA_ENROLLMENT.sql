-- ============================================
-- FIX IJEOMA'S ENROLLMENT - COMPLETE ACCESS
-- ============================================

-- She has module access but not course enrollment!
-- This adds the course enrollment so she can see the content

-- Step 1: Check what columns exist in tquk_enrollments
-- Run this first to see the table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'tquk_enrollments';

-- Step 2: Based on the columns that exist, insert enrollment
-- Try this version (most common structure):
INSERT INTO tquk_enrollments (learner_email, course_id, course_name, status, assigned_by)
VALUES 
    ('ijeoma234@gmail.com', 'level3_adult_care', 'Level 3 Diploma in Adult Care', 'active', 'admin@t21services.co.uk')
ON CONFLICT (learner_email, course_id) DO NOTHING;

-- Step 3: Verify she's enrolled
SELECT 
    learner_email,
    course_id,
    course_name,
    status,
    assigned_by
FROM tquk_enrollments 
WHERE learner_email = 'ijeoma234@gmail.com';

-- ============================================
-- IF STEP 2 FAILS WITH COLUMN ERROR:
-- ============================================
-- Look at the results from Step 1 and tell me what columns exist
-- I'll give you the correct SQL based on your table structure
-- ============================================
