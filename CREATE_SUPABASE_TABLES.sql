-- ============================================
-- T21 SERVICES - SUPABASE TABLE CREATION
-- Medical Secretary AI & Other Missing Tables
-- ============================================

-- TABLE 1: DIARY EVENTS
-- For Medical Secretary diary management
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
-- TABLE 2: CORRESPONDENCE
-- For Medical Secretary letter management
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
-- VERIFY TABLES CREATED
-- ============================================
SELECT 'diary_events' as table_name, COUNT(*) as row_count FROM diary_events
UNION ALL
SELECT 'correspondence' as table_name, COUNT(*) as row_count FROM correspondence;

-- ============================================
-- SUCCESS MESSAGE
-- ============================================
SELECT 'SUCCESS! All Medical Secretary tables created!' as message;
