-- ============================================
-- SUPABASE STORAGE BUCKETS SETUP
-- Run this in your Supabase SQL Editor
-- ============================================

-- IMPORTANT: Storage buckets CANNOT be created via SQL!
-- You MUST create them in the Supabase Dashboard.

-- However, we can create the policies for them here.
-- First, create the buckets manually:

/*
MANUAL STEPS - DO THIS FIRST:
================================

1. Go to https://supabase.com/dashboard/
2. Select your project: T21-RTT-Validator
3. Click "Storage" in left sidebar
4. Click "New bucket"
5. Create these buckets:

BUCKET 1: learning_materials
- Name: learning_materials
- Public bucket: YES ✅
- File size limit: 200 MB
- Allowed MIME types: 
  - application/pdf
  - application/msword
  - application/vnd.openxmlformats-officedocument.wordprocessingml.document
  - application/vnd.ms-excel
  - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  - application/vnd.ms-powerpoint
  - application/vnd.openxmlformats-officedocument.presentationml.presentation
  - text/plain
  - application/zip

BUCKET 2: documents (for other documents)
- Name: documents
- Public bucket: YES ✅
- File size limit: 50 MB
- Allowed MIME types: Same as above

BUCKET 3: profile_pictures (optional, for future)
- Name: profile_pictures
- Public bucket: YES ✅
- File size limit: 5 MB
- Allowed MIME types: image/jpeg, image/png, image/webp

================================
*/

-- After creating buckets manually, run these policies:

-- ============================================
-- STORAGE POLICIES FOR learning_materials BUCKET
-- ============================================

-- Policy 1: Anyone can view files (public bucket)
CREATE POLICY "Public Access" ON storage.objects
  FOR SELECT
  USING (bucket_id = 'learning_materials');

-- Policy 2: Teachers/Staff can upload
CREATE POLICY "Teachers can upload" ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'learning_materials' 
    AND (auth.jwt() ->> 'email') IN (
      SELECT email FROM user_licenses 
      WHERE role IN ('teacher', 'staff', 'super_admin', 'admin')
    )
  );

-- Policy 3: Teachers can update their own files
CREATE POLICY "Teachers can update own files" ON storage.objects
  FOR UPDATE
  USING (
    bucket_id = 'learning_materials' 
    AND (auth.jwt() ->> 'email') = owner
  );

-- Policy 4: Teachers can delete their own files
CREATE POLICY "Teachers can delete own files" ON storage.objects
  FOR DELETE
  USING (
    bucket_id = 'learning_materials' 
    AND (auth.jwt() ->> 'email') = owner
  );


-- ============================================
-- STORAGE POLICIES FOR documents BUCKET
-- ============================================

-- Policy 1: Anyone can view files (public bucket)
CREATE POLICY "Public Access" ON storage.objects
  FOR SELECT
  USING (bucket_id = 'documents');

-- Policy 2: Authenticated users can upload
CREATE POLICY "Authenticated users can upload" ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'documents' 
    AND auth.role() = 'authenticated'
  );

-- Policy 3: Users can update their own files
CREATE POLICY "Users can update own files" ON storage.objects
  FOR UPDATE
  USING (
    bucket_id = 'documents' 
    AND (auth.jwt() ->> 'email') = owner
  );

-- Policy 4: Users can delete their own files
CREATE POLICY "Users can delete own files" ON storage.objects
  FOR DELETE
  USING (
    bucket_id = 'documents' 
    AND (auth.jwt() ->> 'email') = owner
  );


-- ============================================
-- VERIFY SETUP
-- ============================================

-- Check if buckets exist (run this AFTER creating buckets manually)
SELECT 
  id,
  name,
  public,
  file_size_limit,
  created_at
FROM storage.buckets
WHERE name IN ('learning_materials', 'documents', 'profile_pictures');

-- Check policies
SELECT 
  policyname,
  tablename,
  roles,
  cmd,
  qual
FROM pg_policies
WHERE schemaname = 'storage'
  AND tablename = 'objects';


-- ============================================
-- TROUBLESHOOTING
-- ============================================

/*
If uploads still fail:

1. CHECK BUCKET EXISTS:
   - Go to Supabase Dashboard → Storage
   - Confirm "learning_materials" bucket exists
   - Confirm it's set to PUBLIC

2. CHECK POLICIES:
   - Go to Storage → learning_materials → Policies
   - Should see 4 policies (SELECT, INSERT, UPDATE, DELETE)
   - Run the verify query above

3. CHECK AUTHENTICATION:
   - Make sure user is logged in
   - Check st.session_state.user_email exists
   - Check user has appropriate role

4. CHECK FILE SIZE:
   - Max 200MB per file
   - Check uploaded_file size

5. CHECK SUPABASE CONNECTION:
   - Test supabase connection in code
   - Check SUPABASE_URL and SUPABASE_KEY in secrets

6. COMMON ERROR FIXES:
   - "Bucket not found" → Create bucket in dashboard
   - "Permission denied" → Check policies, check user role
   - "File too large" → Increase bucket file size limit
   - "Invalid file type" → Add MIME type to allowed list
*/


-- ============================================
-- NOTES
-- ============================================

/*
WHY MANUAL BUCKET CREATION?
- Supabase doesn't support CREATE BUCKET in SQL
- Must use dashboard or REST API
- Policies can be created via SQL

BUCKET SETTINGS:
- learning_materials: For PDFs, docs, slides (200MB)
- documents: For general documents (50MB)
- profile_pictures: For user avatars (5MB)

SECURITY:
- All buckets set to PUBLIC for easy access
- Policies control WHO can upload/delete
- Students can view all, teachers can upload
- Users can only delete their own files

FILE ORGANIZATION:
- learning_materials/
  ├── teacher1@email.com/
  │   ├── document1.pdf
  │   └── document2.docx
  └── teacher2@email.com/
      └── slides.pptx
*/
