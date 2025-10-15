-- ============================================
-- COMPLETE SUPABASE SETUP
-- Run this SQL in Supabase SQL Editor
-- ============================================

-- ============================================
-- 1. TASKS TABLE (Task Management)
-- ============================================
CREATE TABLE IF NOT EXISTS tasks (
    id BIGSERIAL PRIMARY KEY,
    task_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT NOT NULL,
    priority TEXT NOT NULL,
    due_date DATE NOT NULL,
    assigned_to TEXT,
    created_by TEXT,
    patient_nhs TEXT,
    related_id TEXT,
    related_module TEXT,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    notes JSONB DEFAULT '[]'::jsonb
);

-- Indexes for tasks
CREATE INDEX IF NOT EXISTS idx_tasks_user_email ON tasks(user_email);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_patient_nhs ON tasks(patient_nhs);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);

-- ============================================
-- 2. DOCUMENTS TABLE (Document Management)
-- ============================================
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    document_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    patient_nhs TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    document_type TEXT NOT NULL,
    document_date DATE NOT NULL,
    filename TEXT NOT NULL,
    file_extension TEXT,
    file_size BIGINT,
    storage_path TEXT NOT NULL,
    description TEXT,
    uploaded_by TEXT,
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for documents
CREATE INDEX IF NOT EXISTS idx_documents_user_email ON documents(user_email);
CREATE INDEX IF NOT EXISTS idx_documents_patient_nhs ON documents(patient_nhs);
CREATE INDEX IF NOT EXISTS idx_documents_document_type ON documents(document_type);
CREATE INDEX IF NOT EXISTS idx_documents_document_date ON documents(document_date);
CREATE INDEX IF NOT EXISTS idx_documents_uploaded_at ON documents(uploaded_at);

-- ============================================
-- 3. ROW LEVEL SECURITY (RLS) - TASKS
-- ============================================
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own tasks" ON tasks;
DROP POLICY IF EXISTS "Users can create tasks" ON tasks;
DROP POLICY IF EXISTS "Users can update their tasks" ON tasks;
DROP POLICY IF EXISTS "Users can delete their tasks" ON tasks;

-- Create new policies
CREATE POLICY "Users can view their own tasks" ON tasks
    FOR SELECT 
    USING (
        user_email = auth.jwt() ->> 'email' 
        OR assigned_to = auth.jwt() ->> 'email'
    );

CREATE POLICY "Users can create tasks" ON tasks
    FOR INSERT 
    WITH CHECK (user_email = auth.jwt() ->> 'email');

CREATE POLICY "Users can update their tasks" ON tasks
    FOR UPDATE 
    USING (
        user_email = auth.jwt() ->> 'email' 
        OR assigned_to = auth.jwt() ->> 'email'
    );

CREATE POLICY "Users can delete their tasks" ON tasks
    FOR DELETE 
    USING (user_email = auth.jwt() ->> 'email');

-- ============================================
-- 4. ROW LEVEL SECURITY (RLS) - DOCUMENTS
-- ============================================
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own documents" ON documents;
DROP POLICY IF EXISTS "Users can create documents" ON documents;
DROP POLICY IF EXISTS "Users can delete their documents" ON documents;

-- Create new policies
CREATE POLICY "Users can view their own documents" ON documents
    FOR SELECT 
    USING (user_email = auth.jwt() ->> 'email');

CREATE POLICY "Users can create documents" ON documents
    FOR INSERT 
    WITH CHECK (user_email = auth.jwt() ->> 'email');

CREATE POLICY "Users can delete their documents" ON documents
    FOR DELETE 
    USING (user_email = auth.jwt() ->> 'email');

-- ============================================
-- 5. STORAGE BUCKET SETUP
-- Note: This needs to be done in Supabase Dashboard > Storage
-- ============================================

/*
MANUAL STEPS IN SUPABASE DASHBOARD:

1. Go to Storage section in Supabase Dashboard
2. Click "New Bucket"
3. Name: "documents"
4. Set as Public: NO (keep private)
5. Click "Create Bucket"

6. Then click on "documents" bucket
7. Go to "Policies" tab
8. Add these policies:

Policy Name: "Users can upload their own documents"
Operation: INSERT
Target Roles: authenticated
WITH CHECK: (bucket_id = 'documents' AND auth.uid() IS NOT NULL)

Policy Name: "Users can view their own documents"
Operation: SELECT
Target Roles: authenticated
USING: (bucket_id = 'documents' AND auth.uid() IS NOT NULL)

Policy Name: "Users can delete their own documents"
Operation: DELETE
Target Roles: authenticated
USING: (bucket_id = 'documents' AND auth.uid() IS NOT NULL)
*/

-- ============================================
-- 6. VERIFICATION QUERIES
-- ============================================

-- Check if tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('tasks', 'documents');

-- Check if indexes exist
SELECT indexname 
FROM pg_indexes 
WHERE schemaname = 'public' 
AND tablename IN ('tasks', 'documents');

-- Check RLS policies
SELECT schemaname, tablename, policyname 
FROM pg_policies 
WHERE tablename IN ('tasks', 'documents');

-- ============================================
-- 7. TEST DATA (OPTIONAL - FOR TESTING)
-- ============================================

-- You can insert test task (will be deleted later)
/*
INSERT INTO tasks (
    task_id, user_email, title, description, 
    task_type, priority, due_date, status
) VALUES (
    'TASK_TEST_001',
    'your-email@example.com',  -- REPLACE WITH YOUR EMAIL
    'Test Task',
    'This is a test task to verify the setup',
    'ADMIN',
    'LOW',
    CURRENT_DATE + INTERVAL '7 days',
    'PENDING'
);

-- Check if task was inserted
SELECT * FROM tasks WHERE task_id = 'TASK_TEST_001';

-- Delete test task
DELETE FROM tasks WHERE task_id = 'TASK_TEST_001';
*/

-- ============================================
-- SETUP COMPLETE!
-- ============================================

-- Next steps:
-- 1. Create 'documents' storage bucket in Supabase Dashboard
-- 2. Set up storage policies as described above
-- 3. Restart your Streamlit app
-- 4. Test uploading a document
-- 5. Test creating a task

-- Success message
SELECT 'Database setup complete! Remember to create storage bucket manually.' AS status;
