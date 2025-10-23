-- TQUK COURSE ENROLLMENT AND PROGRESS TRACKING TABLES

-- Course Enrollments
CREATE TABLE IF NOT EXISTS tquk_enrollments (
    id BIGSERIAL PRIMARY KEY,
    learner_email TEXT NOT NULL,
    course_id TEXT NOT NULL,
    course_name TEXT NOT NULL,
    assigned_by TEXT NOT NULL,
    assigned_date TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'enrolled', -- enrolled, in_progress, completed
    progress INTEGER DEFAULT 0, -- 0-100
    units_completed INTEGER DEFAULT 0,
    total_units INTEGER NOT NULL,
    completion_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Unit Progress Tracking
CREATE TABLE IF NOT EXISTS tquk_unit_progress (
    id BIGSERIAL PRIMARY KEY,
    learner_email TEXT NOT NULL,
    course_id TEXT NOT NULL,
    unit_number INTEGER NOT NULL,
    unit_name TEXT NOT NULL,
    status TEXT DEFAULT 'not_started', -- not_started, in_progress, completed
    progress INTEGER DEFAULT 0, -- 0-100
    activities_completed INTEGER DEFAULT 0,
    total_activities INTEGER NOT NULL,
    evidence_submitted BOOLEAN DEFAULT FALSE,
    assessment_status TEXT DEFAULT 'pending', -- pending, submitted, passed, failed
    assessor_feedback TEXT,
    completion_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Evidence Submissions
CREATE TABLE IF NOT EXISTS tquk_evidence (
    id BIGSERIAL PRIMARY KEY,
    learner_email TEXT NOT NULL,
    course_id TEXT NOT NULL,
    unit_number INTEGER NOT NULL,
    evidence_type TEXT NOT NULL, -- observation, witness_statement, reflective_account, product_evidence
    file_url TEXT,
    description TEXT,
    submission_date TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'pending', -- pending, approved, rejected
    assessor_email TEXT,
    assessor_feedback TEXT,
    assessment_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Learning Materials Access Log
CREATE TABLE IF NOT EXISTS tquk_materials_access (
    id BIGSERIAL PRIMARY KEY,
    learner_email TEXT NOT NULL,
    course_id TEXT NOT NULL,
    unit_number INTEGER,
    material_type TEXT, -- handbook, unit_content, assessment_template
    access_date TIMESTAMP DEFAULT NOW(),
    time_spent_seconds INTEGER DEFAULT 0
);

-- Certificates
CREATE TABLE IF NOT EXISTS tquk_certificates (
    id BIGSERIAL PRIMARY KEY,
    learner_email TEXT NOT NULL,
    course_id TEXT NOT NULL,
    course_name TEXT NOT NULL,
    issue_date TIMESTAMP DEFAULT NOW(),
    certificate_number TEXT UNIQUE NOT NULL,
    issued_by TEXT NOT NULL,
    pdf_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_enrollments_learner ON tquk_enrollments(learner_email);
CREATE INDEX IF NOT EXISTS idx_enrollments_course ON tquk_enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_unit_progress_learner ON tquk_unit_progress(learner_email, course_id);
CREATE INDEX IF NOT EXISTS idx_evidence_learner ON tquk_evidence(learner_email, course_id);
CREATE INDEX IF NOT EXISTS idx_certificates_learner ON tquk_certificates(learner_email);

-- Enable Row Level Security (RLS)
ALTER TABLE tquk_enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE tquk_unit_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE tquk_evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE tquk_materials_access ENABLE ROW LEVEL SECURITY;
ALTER TABLE tquk_certificates ENABLE ROW LEVEL SECURITY;

-- RLS Policies (learners can only see their own data, teachers can see all)
CREATE POLICY "Learners can view own enrollments" ON tquk_enrollments
    FOR SELECT USING (auth.jwt() ->> 'email' = learner_email);

CREATE POLICY "Teachers can view all enrollments" ON tquk_enrollments
    FOR SELECT USING (auth.jwt() ->> 'role' IN ('teacher', 'admin', 'super_admin'));

CREATE POLICY "Teachers can insert enrollments" ON tquk_enrollments
    FOR INSERT WITH CHECK (auth.jwt() ->> 'role' IN ('teacher', 'admin', 'super_admin'));

CREATE POLICY "Teachers can update enrollments" ON tquk_enrollments
    FOR UPDATE USING (auth.jwt() ->> 'role' IN ('teacher', 'admin', 'super_admin'));

-- Similar policies for other tables
CREATE POLICY "Learners can view own progress" ON tquk_unit_progress
    FOR SELECT USING (auth.jwt() ->> 'email' = learner_email);

CREATE POLICY "Teachers can view all progress" ON tquk_unit_progress
    FOR ALL USING (auth.jwt() ->> 'role' IN ('teacher', 'admin', 'super_admin'));

CREATE POLICY "Learners can submit evidence" ON tquk_evidence
    FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = learner_email);

CREATE POLICY "Learners can view own evidence" ON tquk_evidence
    FOR SELECT USING (auth.jwt() ->> 'email' = learner_email);

CREATE POLICY "Teachers can view all evidence" ON tquk_evidence
    FOR ALL USING (auth.jwt() ->> 'role' IN ('teacher', 'admin', 'super_admin'));
