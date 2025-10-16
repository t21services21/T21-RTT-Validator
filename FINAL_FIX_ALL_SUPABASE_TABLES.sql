-- ============================================
-- T21 SERVICES - FINAL COMPLETE SUPABASE TABLE FIX
-- This script fixes ALL table name and column discrepancies
-- ============================================

-- First, let's handle existing tables with wrong names/structures
-- We'll rename cancer_patients to cancer_pathways_backup (if it exists)
-- Then create the correct cancer_pathways table

-- Handle the cancer_patients table that was created with wrong structure
ALTER TABLE IF EXISTS cancer_patients RENAME TO cancer_patients_backup;

-- ============================================
-- USERS TABLE (must be first as other tables reference it)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT NOT NULL,
  role TEXT DEFAULT 'trial',
  user_type TEXT DEFAULT 'student',
  status TEXT DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP,
  expiry_date TIMESTAMP
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT USING (auth.jwt() ->> 'email' = email);

CREATE POLICY "Admins can manage all users" ON users
  FOR ALL USING (email = 'admin@t21services.co.uk');


-- ============================================
-- USER TRACKING TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS user_tracking (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_email TEXT NOT NULL,
  login_time TIMESTAMP DEFAULT NOW(),
  success BOOLEAN NOT NULL,
  ip_address TEXT,
  city TEXT,
  country TEXT,
  device TEXT,
  browser TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_tracking_email ON user_tracking(user_email);
CREATE INDEX IF NOT EXISTS idx_user_tracking_success ON user_tracking(success);

-- Enable Row Level Security
ALTER TABLE user_tracking ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own tracking" ON user_tracking
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Admins can view all tracking" ON user_tracking
  FOR SELECT USING (EXISTS (SELECT 1 FROM users WHERE email = auth.jwt() ->> 'email' AND role = 'admin'));


-- ============================================
-- MODULE ACCESS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS module_access (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_email TEXT NOT NULL,
  module_name TEXT NOT NULL,
  granted_at TIMESTAMP DEFAULT NOW(),
  granted_by TEXT NOT NULL
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_module_access_email ON module_access(user_email);
CREATE INDEX IF NOT EXISTS idx_module_access_module ON module_access(module_name);

-- Enable Row Level Security
ALTER TABLE module_access ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own access" ON module_access
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Admins can manage access" ON module_access
  FOR ALL USING (EXISTS (SELECT 1 FROM users WHERE email = auth.jwt() ->> 'email' AND role = 'admin'));


-- ============================================
-- LEARNING MATERIALS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS learning_materials (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  category TEXT NOT NULL,
  file_url TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_type TEXT NOT NULL,
  file_size INTEGER DEFAULT 0,
  competency TEXT,
  week INTEGER DEFAULT 0,
  required BOOLEAN DEFAULT true,
  visible_to_all BOOLEAN DEFAULT true,
  uploaded_by TEXT NOT NULL,
  uploaded_date DATE NOT NULL,
  download_count INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active',
  deleted_date DATE
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_learning_materials_category ON learning_materials(category);
CREATE INDEX IF NOT EXISTS idx_learning_materials_week ON learning_materials(week);
CREATE INDEX IF NOT EXISTS idx_learning_materials_competency ON learning_materials(competency);
CREATE INDEX IF NOT EXISTS idx_learning_materials_status ON learning_materials(status);

-- Enable Row Level Security
ALTER TABLE learning_materials ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view learning materials" ON learning_materials
  FOR SELECT USING (status = 'active' AND (visible_to_all = true OR auth.jwt() ->> 'email' = uploaded_by));

CREATE POLICY "Teachers can insert learning materials" ON learning_materials
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = uploaded_by);

CREATE POLICY "Teachers can update learning materials" ON learning_materials
  FOR UPDATE USING (auth.jwt() ->> 'email' = uploaded_by);

CREATE POLICY "Teachers can delete learning materials" ON learning_materials
  FOR DELETE USING (auth.jwt() ->> 'email' = uploaded_by);


-- ============================================
-- MATERIAL DOWNLOADS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS material_downloads (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  material_id UUID REFERENCES learning_materials(id),
  student_email TEXT NOT NULL,
  download_date TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_material_downloads_material_id ON material_downloads(material_id);
CREATE INDEX IF NOT EXISTS idx_material_downloads_student_email ON material_downloads(student_email);

-- Enable Row Level Security
ALTER TABLE material_downloads ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own downloads" ON material_downloads
  FOR SELECT USING (auth.jwt() ->> 'email' = student_email);

CREATE POLICY "Users can insert own downloads" ON material_downloads
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = student_email);


-- ============================================
-- ASSIGNMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS assignments (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  instructions TEXT NOT NULL,
  week INTEGER NOT NULL,
  module_name TEXT NOT NULL,
  competency TEXT,
  due_date DATE NOT NULL,
  total_marks INTEGER DEFAULT 100,
  pass_mark INTEGER DEFAULT 50,
  required BOOLEAN DEFAULT true,
  allow_late_submission BOOLEAN DEFAULT false,
  created_by TEXT NOT NULL,
  created_date DATE NOT NULL,
  status TEXT DEFAULT 'active'
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_assignments_week ON assignments(week);
CREATE INDEX IF NOT EXISTS idx_assignments_module ON assignments(module_name);
CREATE INDEX IF NOT EXISTS idx_assignments_competency ON assignments(competency);
CREATE INDEX IF NOT EXISTS idx_assignments_status ON assignments(status);

-- Enable Row Level Security
ALTER TABLE assignments ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view assignments" ON assignments
  FOR SELECT USING (status = 'active');

CREATE POLICY "Teachers can manage assignments" ON assignments
  FOR ALL USING (auth.jwt() ->> 'email' = created_by);


-- ============================================
-- ASSIGNMENT SUBMISSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS assignment_submissions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  assignment_id UUID REFERENCES assignments(id),
  student_email TEXT NOT NULL,
  student_name TEXT NOT NULL,
  submission_text TEXT,
  file_url TEXT,
  file_name TEXT,
  submitted_date TIMESTAMP DEFAULT NOW(),
  is_late BOOLEAN DEFAULT false,
  marks_awarded INTEGER,
  feedback TEXT,
  graded_by TEXT,
  graded_date TIMESTAMP,
  status TEXT DEFAULT 'submitted'
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_assignment_submissions_assignment ON assignment_submissions(assignment_id);
CREATE INDEX IF NOT EXISTS idx_assignment_submissions_student ON assignment_submissions(student_email);
CREATE INDEX IF NOT EXISTS idx_assignment_submissions_status ON assignment_submissions(status);

-- Enable Row Level Security
ALTER TABLE assignment_submissions ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own submissions" ON assignment_submissions
  FOR SELECT USING (auth.jwt() ->> 'email' = student_email OR auth.jwt() ->> 'email' = graded_by);

CREATE POLICY "Students can insert submissions" ON assignment_submissions
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = student_email);

CREATE POLICY "Teachers can grade submissions" ON assignment_submissions
  FOR UPDATE USING (auth.jwt() ->> 'email' = graded_by);


-- ============================================
-- VIDEO LIBRARY TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS video_library (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  vimeo_url TEXT NOT NULL,
  vimeo_id TEXT NOT NULL,
  category TEXT NOT NULL,
  week INTEGER DEFAULT 0,
  duration_minutes INTEGER DEFAULT 0,
  competency TEXT,
  required BOOLEAN DEFAULT true,
  visible_to_all BOOLEAN DEFAULT true,
  uploaded_by TEXT NOT NULL,
  uploaded_date DATE NOT NULL,
  view_count INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active',
  deleted_date DATE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_video_library_category ON video_library(category);
CREATE INDEX IF NOT EXISTS idx_video_library_week ON video_library(week);
CREATE INDEX IF NOT EXISTS idx_video_library_competency ON video_library(competency);
CREATE INDEX IF NOT EXISTS idx_video_library_status ON video_library(status);

-- Enable Row Level Security
ALTER TABLE video_library ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view videos" ON video_library
  FOR SELECT USING (status = 'active' AND (visible_to_all = true OR auth.jwt() ->> 'email' = uploaded_by));

CREATE POLICY "Teachers can manage videos" ON video_library
  FOR ALL USING (auth.jwt() ->> 'email' = uploaded_by);


-- ============================================
-- VIDEO VIEWS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS video_views (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  video_id UUID REFERENCES video_library(id),
  student_email TEXT NOT NULL,
  view_date TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_video_views_video_id ON video_views(video_id);
CREATE INDEX IF NOT EXISTS idx_video_views_student_email ON video_views(student_email);

-- Enable Row Level Security
ALTER TABLE video_views ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own video views" ON video_views
  FOR SELECT USING (auth.jwt() ->> 'email' = student_email);

CREATE POLICY "Users can insert own video views" ON video_views
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = student_email);


-- ============================================
-- ANNOUNCEMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS announcements (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  category TEXT DEFAULT 'General',
  pinned BOOLEAN DEFAULT false,
  visible_to_all BOOLEAN DEFAULT true,
  posted_by TEXT NOT NULL,
  posted_date TIMESTAMP DEFAULT NOW(),
  status TEXT DEFAULT 'active'
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_announcements_category ON announcements(category);
CREATE INDEX IF NOT EXISTS idx_announcements_pinned ON announcements(pinned);
CREATE INDEX IF NOT EXISTS idx_announcements_status ON announcements(status);

-- Enable Row Level Security
ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view announcements" ON announcements
  FOR SELECT USING (status = 'active');

CREATE POLICY "Teachers can manage announcements" ON announcements
  FOR ALL USING (auth.jwt() ->> 'email' = posted_by);


-- ============================================
-- PTL PATIENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS ptl_patients (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  patient_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  nhs_number TEXT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  dob DATE,
  address TEXT,
  phone TEXT,
  email TEXT,
  referral_date DATE,
  first_appointment_date DATE,
  consultation_date DATE,
  clock_start_date TEXT,
  clock_status TEXT DEFAULT 'ACTIVE',
  milestones JSONB,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_ptl_patients_user_email ON ptl_patients(user_email);
CREATE INDEX IF NOT EXISTS idx_ptl_patients_clock_status ON ptl_patients(clock_status);
CREATE INDEX IF NOT EXISTS idx_ptl_patients_referral_date ON ptl_patients(referral_date);

-- Enable Row Level Security
ALTER TABLE ptl_patients ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own PTL patients" ON ptl_patients
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own PTL patients" ON ptl_patients
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own PTL patients" ON ptl_patients
  FOR UPDATE USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own PTL patients" ON ptl_patients
  FOR DELETE USING (auth.jwt() ->> 'email' = user_email);


-- ============================================
-- CANCER PATHWAYS TABLE (CORRECTED to match your code)
-- ============================================
CREATE TABLE IF NOT EXISTS cancer_pathways (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  pathway_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  nhs_number TEXT,
  patient_name TEXT NOT NULL,
  dob DATE,
  cancer_type TEXT NOT NULL,
  diagnosis_date DATE,  -- This was missing!
  referral_date DATE,
  first_appointment_date DATE,
  treatment_start_date DATE,
  mdt_discussion_date DATE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_cancer_pathways_user_email ON cancer_pathways(user_email);
CREATE INDEX IF NOT EXISTS idx_cancer_pathways_cancer_type ON cancer_pathways(cancer_type);
CREATE INDEX IF NOT EXISTS idx_cancer_pathways_diagnosis_date ON cancer_pathways(diagnosis_date);

-- Enable Row Level Security
ALTER TABLE cancer_pathways ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own cancer patients" ON cancer_pathways
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own cancer patients" ON cancer_pathways
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own cancer patients" ON cancer_pathways
  FOR UPDATE USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own cancer patients" ON cancer_pathways
  FOR DELETE USING (auth.jwt() ->> 'email' = user_email);


-- ============================================
-- MDT MEETINGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS mdt_meetings (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  meeting_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  specialty TEXT NOT NULL,
  date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  location TEXT,
  agenda TEXT,
  attendees JSONB,
  notes TEXT,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_mdt_meetings_user_email ON mdt_meetings(user_email);
CREATE INDEX IF NOT EXISTS idx_mdt_meetings_specialty ON mdt_meetings(specialty);
CREATE INDEX IF NOT EXISTS idx_mdt_meetings_date ON mdt_meetings(date);

-- Enable Row Level Security
ALTER TABLE mdt_meetings ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own MDT meetings" ON mdt_meetings
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own MDT meetings" ON mdt_meetings
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own MDT meetings" ON mdt_meetings
  FOR UPDATE USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own MDT meetings" ON mdt_meetings
  FOR DELETE USING (auth.jwt() ->> 'email' = user_email);


-- ============================================
-- CLINICS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS clinics (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  clinic_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  specialty TEXT NOT NULL,
  name TEXT NOT NULL,
  location TEXT NOT NULL,
  default_duration INTEGER NOT NULL,
  default_capacity INTEGER NOT NULL,
  notes TEXT,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_clinics_user_email ON clinics(user_email);
CREATE INDEX IF NOT EXISTS idx_clinics_specialty ON clinics(specialty);

-- Enable Row Level Security
ALTER TABLE clinics ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own clinics" ON clinics
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own clinics" ON clinics
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own clinics" ON clinics
  FOR UPDATE USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own clinics" ON clinics
  FOR DELETE USING (auth.jwt() ->> 'email' = user_email);


-- ============================================
-- APPOINTMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS appointments (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  appointment_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  clinic_id TEXT NOT NULL,
  patient_name TEXT NOT NULL,
  nhs_number TEXT,
  date DATE NOT NULL,
  time TIME NOT NULL,
  duration INTEGER NOT NULL,
  status TEXT DEFAULT 'booked',
  notes TEXT,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_appointments_user_email ON appointments(user_email);
CREATE INDEX IF NOT EXISTS idx_appointments_clinic_id ON appointments(clinic_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date);
CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);

-- Enable Row Level Security
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own appointments" ON appointments
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own appointments" ON appointments
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own appointments" ON appointments
  FOR UPDATE USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own appointments" ON appointments
  FOR DELETE USING (auth.jwt() ->> 'email' = user_email);


-- ============================================
-- DIARY EVENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS diary_events (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  event_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  consultant TEXT NOT NULL,
  date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  event_type TEXT NOT NULL,
  location TEXT,
  description TEXT,
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_diary_events_user_email ON diary_events(user_email);
CREATE INDEX IF NOT EXISTS idx_diary_events_consultant ON diary_events(consultant);
CREATE INDEX IF NOT EXISTS idx_diary_events_date ON diary_events(date);

-- Enable Row Level Security
ALTER TABLE diary_events ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only see their own events
CREATE POLICY "Users can view own diary events" ON diary_events
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own diary events" ON diary_events
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own diary events" ON diary_events
  FOR UPDATE USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own diary events" ON diary_events
  FOR DELETE USING (auth.jwt() ->> 'email' = user_email);


-- ============================================
-- CORRESPONDENCE TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS correspondence (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  letter_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  letter_type TEXT NOT NULL,
  patient_name TEXT NOT NULL,
  nhs_number TEXT,
  gp_name TEXT,
  gp_address TEXT,
  clinic_date DATE,
  consultant_name TEXT,
  diagnosis TEXT,
  treatment_plan TEXT,
  content TEXT NOT NULL,
  status TEXT DEFAULT 'draft',
  created_date TIMESTAMP DEFAULT NOW(),
  updated_date TIMESTAMP DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_correspondence_user_email ON correspondence(user_email);
CREATE INDEX IF NOT EXISTS idx_correspondence_letter_type ON correspondence(letter_type);
CREATE INDEX IF NOT EXISTS idx_correspondence_patient ON correspondence(patient_name);

-- Enable Row Level Security
ALTER TABLE correspondence ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only see their own correspondence
CREATE POLICY "Users can view own correspondence" ON correspondence
  FOR SELECT USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can insert own correspondence" ON correspondence
  FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can update own correspondence" ON correspondence
  FOR UPDATE USING (auth.jwt() ->> 'email' = user_email);

CREATE POLICY "Users can delete own correspondence" ON correspondence
  FOR DELETE USING (auth.jwt() ->> 'email' = user_email);


-- ============================================
-- VERIFY ALL TABLES CREATED
-- ============================================
SELECT 
  'learning_materials' as table_name, 
  COUNT(*) as row_count 
FROM learning_materials
UNION ALL
SELECT 
  'material_downloads' as table_name, 
  COUNT(*) as row_count 
FROM material_downloads
UNION ALL
SELECT 
  'assignments' as table_name, 
  COUNT(*) as row_count 
FROM assignments
UNION ALL
SELECT 
  'assignment_submissions' as table_name, 
  COUNT(*) as row_count 
FROM assignment_submissions
UNION ALL
SELECT 
  'video_library' as table_name, 
  COUNT(*) as row_count 
FROM video_library
UNION ALL
SELECT 
  'video_views' as table_name, 
  COUNT(*) as row_count 
FROM video_views
UNION ALL
SELECT 
  'announcements' as table_name, 
  COUNT(*) as row_count 
FROM announcements
UNION ALL
SELECT 
  'ptl_patients' as table_name, 
  COUNT(*) as row_count 
FROM ptl_patients
UNION ALL
SELECT 
  'cancer_pathways' as table_name, 
  COUNT(*) as row_count 
FROM cancer_pathways
UNION ALL
SELECT 
  'mdt_meetings' as table_name, 
  COUNT(*) as row_count 
FROM mdt_meetings
UNION ALL
SELECT 
  'clinics' as table_name, 
  COUNT(*) as row_count 
FROM clinics
UNION ALL
SELECT 
  'appointments' as table_name, 
  COUNT(*) as row_count 
FROM appointments
UNION ALL
SELECT 
  'diary_events' as table_name, 
  COUNT(*) as row_count 
FROM diary_events
UNION ALL
SELECT 
  'correspondence' as table_name, 
  COUNT(*) as row_count 
FROM correspondence
UNION ALL
SELECT 
  'users' as table_name, 
  COUNT(*) as row_count 
FROM users
UNION ALL
SELECT 
  'user_tracking' as table_name, 
  COUNT(*) as row_count 
FROM user_tracking
UNION ALL
SELECT 
  'module_access' as table_name, 
  COUNT(*) as row_count 
FROM module_access;

-- ============================================
-- SUCCESS MESSAGE
-- ============================================
SELECT 'SUCCESS! All T21 Services tables fixed and created!' as message;
