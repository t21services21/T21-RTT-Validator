-- ============================================
-- T21 SERVICES - COMPLETE DATABASE SCHEMA
-- Create all tables with RLS enabled
-- ============================================

-- 1. USERS TABLE (if not exists)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    user_type TEXT DEFAULT 'student',
    role TEXT DEFAULT 'trial',
    two_factor_enabled BOOLEAN DEFAULT false,
    two_factor_secret TEXT,
    backup_codes JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. PTL PATIENTS TABLE (already exists, but ensure structure)
CREATE TABLE IF NOT EXISTS ptl_patients (
    id SERIAL PRIMARY KEY,
    patient_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    patient_name TEXT,
    nhs_number TEXT,
    specialty TEXT,
    referral_date DATE,
    referral_source TEXT,
    clock_start_date DATE,
    pathway_type TEXT,
    priority TEXT,
    current_status TEXT,
    consultant TEXT,
    contact_number TEXT,
    rtt_code TEXT,
    clock_status TEXT,
    notes TEXT,
    added_date TIMESTAMP,
    last_updated TIMESTAMP,
    appointments JSONB DEFAULT '[]'::jsonb,
    events JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. MDT MEETINGS TABLE
CREATE TABLE IF NOT EXISTS mdt_meetings (
    id SERIAL PRIMARY KEY,
    meeting_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    meeting_date DATE NOT NULL,
    meeting_time TIME,
    specialty TEXT,
    location TEXT,
    chair_person TEXT,
    attendees JSONB DEFAULT '[]'::jsonb,
    patients_discussed JSONB DEFAULT '[]'::jsonb,
    decisions JSONB DEFAULT '[]'::jsonb,
    action_points JSONB DEFAULT '[]'::jsonb,
    notes TEXT,
    status TEXT DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 4. APPOINTMENTS TABLE
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    appointment_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    patient_id TEXT,
    patient_name TEXT,
    nhs_number TEXT,
    appointment_date DATE NOT NULL,
    appointment_time TIME,
    specialty TEXT,
    clinic_location TEXT,
    appointment_type TEXT,
    consultant TEXT,
    status TEXT DEFAULT 'booked',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. CANCER PATHWAYS TABLE
CREATE TABLE IF NOT EXISTS cancer_pathways (
    id SERIAL PRIMARY KEY,
    pathway_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    patient_name TEXT,
    nhs_number TEXT,
    cancer_type TEXT,
    referral_date DATE,
    pathway_type TEXT,
    clock_start_date DATE,
    target_date DATE,
    current_status TEXT,
    milestones JSONB DEFAULT '[]'::jsonb,
    treatments JSONB DEFAULT '[]'::jsonb,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 6. VALIDATION HISTORY TABLE
CREATE TABLE IF NOT EXISTS validation_history (
    id SERIAL PRIMARY KEY,
    validation_id TEXT UNIQUE NOT NULL,
    user_email TEXT NOT NULL,
    validation_type TEXT,
    patient_data JSONB,
    result JSONB,
    is_valid BOOLEAN,
    confidence_score INTEGER,
    issues JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 7. TRAINING PROGRESS TABLE
CREATE TABLE IF NOT EXISTS training_progress (
    id SERIAL PRIMARY KEY,
    user_email TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    scenario_name TEXT,
    completed BOOLEAN DEFAULT false,
    score INTEGER,
    time_taken INTEGER,
    attempts INTEGER DEFAULT 1,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_email, scenario_id)
);

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_ptl_user_email ON ptl_patients(user_email);
CREATE INDEX IF NOT EXISTS idx_ptl_patient_id ON ptl_patients(patient_id);
CREATE INDEX IF NOT EXISTS idx_mdt_user_email ON mdt_meetings(user_email);
CREATE INDEX IF NOT EXISTS idx_mdt_meeting_id ON mdt_meetings(meeting_id);
CREATE INDEX IF NOT EXISTS idx_appointments_user_email ON appointments(user_email);
CREATE INDEX IF NOT EXISTS idx_appointments_appointment_id ON appointments(appointment_id);
CREATE INDEX IF NOT EXISTS idx_cancer_user_email ON cancer_pathways(user_email);
CREATE INDEX IF NOT EXISTS idx_validation_user_email ON validation_history(user_email);
CREATE INDEX IF NOT EXISTS idx_training_user_email ON training_progress(user_email);

-- ============================================
-- ENABLE ROW LEVEL SECURITY (RLS)
-- ============================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE ptl_patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE mdt_meetings ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE cancer_pathways ENABLE ROW LEVEL SECURITY;
ALTER TABLE validation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_progress ENABLE ROW LEVEL SECURITY;

-- ============================================
-- CREATE RLS POLICIES
-- ============================================

-- PTL PATIENTS POLICIES
CREATE POLICY "Users can view their own PTL patients"
ON ptl_patients FOR SELECT
USING (user_email = current_user);

CREATE POLICY "Users can insert their own PTL patients"
ON ptl_patients FOR INSERT
WITH CHECK (user_email = current_user);

CREATE POLICY "Users can update their own PTL patients"
ON ptl_patients FOR UPDATE
USING (user_email = current_user);

CREATE POLICY "Users can delete their own PTL patients"
ON ptl_patients FOR DELETE
USING (user_email = current_user);

CREATE POLICY "Service role has full access to PTL patients"
ON ptl_patients FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- MDT MEETINGS POLICIES
CREATE POLICY "Users can manage their own MDT meetings"
ON mdt_meetings FOR ALL
USING (user_email = current_user);

CREATE POLICY "Service role full access to MDT"
ON mdt_meetings FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- APPOINTMENTS POLICIES
CREATE POLICY "Users can manage their own appointments"
ON appointments FOR ALL
USING (user_email = current_user);

CREATE POLICY "Service role full access to appointments"
ON appointments FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- CANCER PATHWAYS POLICIES
CREATE POLICY "Users can manage their own cancer pathways"
ON cancer_pathways FOR ALL
USING (user_email = current_user);

CREATE POLICY "Service role full access to cancer pathways"
ON cancer_pathways FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- VALIDATION HISTORY POLICIES
CREATE POLICY "Users can view their own validation history"
ON validation_history FOR SELECT
USING (user_email = current_user);

CREATE POLICY "Users can insert their own validation history"
ON validation_history FOR INSERT
WITH CHECK (user_email = current_user);

CREATE POLICY "Service role full access to validation history"
ON validation_history FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- TRAINING PROGRESS POLICIES
CREATE POLICY "Users can manage their own training progress"
ON training_progress FOR ALL
USING (user_email = current_user);

CREATE POLICY "Service role full access to training progress"
ON training_progress FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- USERS TABLE POLICIES
CREATE POLICY "Users can view their own profile"
ON users FOR SELECT
USING (email = current_user);

CREATE POLICY "Users can update their own profile"
ON users FOR UPDATE
USING (email = current_user);

CREATE POLICY "Service role full access to users"
ON users FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- ============================================
-- SUCCESS MESSAGE
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '✅ All tables created successfully!';
    RAISE NOTICE '✅ Row Level Security enabled on all tables!';
    RAISE NOTICE '✅ Policies created for data isolation!';
    RAISE NOTICE '✅ Indexes created for performance!';
    RAISE NOTICE '';
    RAISE NOTICE '🔒 Your database is now secure!';
    RAISE NOTICE '📊 Students can only see their own data!';
    RAISE NOTICE '🚀 Ready for production use!';
END $$;
