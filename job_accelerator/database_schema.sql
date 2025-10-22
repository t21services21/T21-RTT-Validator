-- T21 JOB ACCELERATOR - DATABASE SCHEMA
-- PostgreSQL Schema (Supabase Compatible)
-- Designed for scale, speed, and analytics

-- ============================================
-- STUDENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Basic Info
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    
    -- Address
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    postcode VARCHAR(10),
    
    -- T21 Integration
    t21_user_id UUID REFERENCES users(id),
    tquk_certification_number VARCHAR(100),
    tquk_course_code VARCHAR(50) DEFAULT 'PDLC-01-039',
    certification_date DATE,
    certification_level VARCHAR(50), -- Foundation, Practitioner, Expert
    
    -- Job Preferences
    target_roles JSONB, -- ['RTT Validator', 'Hospital Administrator', 'Medical Secretary']
    target_locations JSONB, -- ['London', 'Manchester', 'Remote']
    min_salary INTEGER,
    max_salary INTEGER,
    employment_type VARCHAR(50), -- Full-time, Part-time, Contract
    willing_to_relocate BOOLEAN DEFAULT FALSE,
    
    -- Skills & Experience
    skills JSONB, -- ['RTT Validation', 'PAS Systems', 'MS Office']
    experience_years INTEGER DEFAULT 0,
    previous_roles TEXT,
    qualifications JSONB,
    
    -- Documents
    cv_path VARCHAR(500),
    cover_letter_template TEXT,
    
    -- LinkedIn Integration
    linkedin_profile_url VARCHAR(255),
    linkedin_connected BOOLEAN DEFAULT FALSE,
    linkedin_token TEXT,
    
    -- Status
    status VARCHAR(50) DEFAULT 'active', -- active, placed, paused, inactive
    placement_status VARCHAR(50), -- searching, interviewing, offered, placed
    
    -- Settings
    daily_application_limit INTEGER DEFAULT 10,
    auto_apply_enabled BOOLEAN DEFAULT TRUE,
    approval_required BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_application_at TIMESTAMP,
    
    -- Analytics
    total_applications INTEGER DEFAULT 0,
    total_responses INTEGER DEFAULT 0,
    total_interviews INTEGER DEFAULT 0,
    total_offers INTEGER DEFAULT 0
);

-- Indexes for performance
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_t21_user ON students(t21_user_id);
CREATE INDEX idx_students_placement ON students(placement_status);

-- ============================================
-- JOBS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Job Basics
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    url VARCHAR(500) UNIQUE NOT NULL,
    job_board VARCHAR(50) NOT NULL, -- nhs_jobs, indeed, reed, linkedin, cv_library
    external_id VARCHAR(255), -- Job ID on external site
    
    -- Job Details
    description TEXT,
    requirements TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    salary_text VARCHAR(100),
    
    -- Location
    location VARCHAR(255),
    city VARCHAR(100),
    region VARCHAR(100),
    postcode VARCHAR(10),
    remote_option BOOLEAN DEFAULT FALSE,
    
    -- Job Type
    employment_type VARCHAR(50), -- Full-time, Part-time, Contract, Temporary
    contract_duration VARCHAR(100),
    specialty VARCHAR(100), -- RTT, Outpatients, Emergency, etc.
    
    -- Application Details
    application_method VARCHAR(50), -- form, email, external, easy_apply
    application_url VARCHAR(500),
    application_email VARCHAR(255),
    application_instructions TEXT,
    
    -- Requirements
    required_skills JSONB,
    preferred_skills JSONB,
    certifications_required JSONB,
    experience_required INTEGER,
    
    -- Dates
    posted_date DATE,
    closing_date DATE,
    start_date DATE,
    
    -- Status
    status VARCHAR(50) DEFAULT 'active', -- active, closed, expired, filled
    
    -- AI Scoring
    relevance_score FLOAT, -- 0-100, how relevant for RTT graduates
    match_keywords JSONB, -- Keywords that matched
    
    -- Metadata
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    first_seen_at TIMESTAMP DEFAULT NOW(),
    last_checked_at TIMESTAMP,
    
    -- Analytics
    total_views INTEGER DEFAULT 0,
    total_applications INTEGER DEFAULT 0,
    estimated_applicants INTEGER
);

-- Indexes
CREATE INDEX idx_jobs_board ON jobs(job_board);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_location ON jobs(city, region);
CREATE INDEX idx_jobs_posted ON jobs(posted_date DESC);
CREATE INDEX idx_jobs_relevance ON jobs(relevance_score DESC);
CREATE INDEX idx_jobs_closing ON jobs(closing_date);

-- ============================================
-- APPLICATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Relations
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    
    -- Application Details
    application_method VARCHAR(50), -- form, email, easy_apply
    cv_used TEXT, -- Tailored CV content
    cover_letter TEXT, -- Generated cover letter
    
    -- Documents
    cv_file_path VARCHAR(500),
    cover_letter_file_path VARCHAR(500),
    additional_documents JSONB,
    
    -- Status Tracking
    status VARCHAR(50) DEFAULT 'pending', -- pending, submitted, viewed, responded, interviewing, offered, rejected, withdrawn
    substatus VARCHAR(100), -- More detailed status
    
    -- Timeline
    created_at TIMESTAMP DEFAULT NOW(),
    submitted_at TIMESTAMP,
    viewed_at TIMESTAMP,
    responded_at TIMESTAMP,
    interview_scheduled_at TIMESTAMP,
    interview_date TIMESTAMP,
    outcome_date TIMESTAMP,
    
    -- Response Details
    response_type VARCHAR(50), -- interview, rejection, request_info, offer
    response_text TEXT,
    rejection_reason TEXT,
    
    -- Interview Details
    interview_location VARCHAR(255),
    interview_type VARCHAR(50), -- phone, video, in-person
    interview_notes TEXT,
    
    -- Offer Details
    offer_salary INTEGER,
    offer_start_date DATE,
    offer_accepted BOOLEAN,
    
    -- AI Matching
    match_score FLOAT, -- 0-100, how well student matches job
    predicted_success_rate FLOAT, -- AI prediction of interview likelihood
    
    -- Automation Details
    automated BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMP,
    
    -- Follow-up
    follow_up_sent BOOLEAN DEFAULT FALSE,
    follow_up_date TIMESTAMP,
    
    -- Metadata
    updated_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    
    -- Reference number (from application confirmation)
    reference_number VARCHAR(100),
    
    UNIQUE(student_id, job_id) -- Prevent duplicate applications
);

-- Indexes
CREATE INDEX idx_applications_student ON applications(student_id);
CREATE INDEX idx_applications_job ON applications(job_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_submitted ON applications(submitted_at DESC);
CREATE INDEX idx_applications_interview ON applications(interview_date);
CREATE INDEX idx_applications_automated ON applications(automated, status);

-- ============================================
-- FOLLOW_UPS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS follow_ups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    
    -- Follow-up Details
    follow_up_type VARCHAR(50), -- reminder, inquiry, thank_you
    scheduled_for TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,
    
    -- Content
    subject VARCHAR(255),
    message TEXT,
    
    -- Response
    response_received BOOLEAN DEFAULT FALSE,
    response_at TIMESTAMP,
    response_text TEXT,
    
    -- Status
    status VARCHAR(50) DEFAULT 'scheduled', -- scheduled, sent, responded, cancelled
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_followups_application ON follow_ups(application_id);
CREATE INDEX idx_followups_scheduled ON follow_ups(scheduled_for);
CREATE INDEX idx_followups_status ON follow_ups(status);

-- ============================================
-- ANALYTICS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event Details
    event_type VARCHAR(100) NOT NULL, -- job_scraped, application_submitted, response_received, etc.
    event_category VARCHAR(50), -- scraping, application, response, system
    
    -- Relations
    student_id UUID REFERENCES students(id),
    job_id UUID REFERENCES jobs(id),
    application_id UUID REFERENCES applications(id),
    
    -- Event Data
    event_data JSONB,
    
    -- Metrics
    metric_name VARCHAR(100),
    metric_value FLOAT,
    
    -- Timestamp
    occurred_at TIMESTAMP DEFAULT NOW(),
    
    -- Context
    job_board VARCHAR(50),
    location VARCHAR(100),
    user_agent VARCHAR(255)
);

-- Indexes for analytics queries
CREATE INDEX idx_analytics_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_occurred ON analytics_events(occurred_at DESC);
CREATE INDEX idx_analytics_student ON analytics_events(student_id);
CREATE INDEX idx_analytics_board ON analytics_events(job_board);

-- ============================================
-- JOB_BOARD_CONFIG TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS job_board_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    board_name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    
    -- Configuration
    enabled BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 50, -- Higher priority boards checked first
    
    -- Scraping Settings
    scrape_frequency_minutes INTEGER DEFAULT 60,
    max_results_per_scrape INTEGER DEFAULT 100,
    
    -- Rate Limiting
    requests_per_minute INTEGER DEFAULT 10,
    delay_between_requests_ms INTEGER DEFAULT 1000,
    
    -- Authentication
    requires_login BOOLEAN DEFAULT FALSE,
    login_url VARCHAR(500),
    
    -- Endpoints
    base_url VARCHAR(500),
    search_url VARCHAR(500),
    job_url_template VARCHAR(500),
    
    -- Selectors (for scraping)
    selectors JSONB,
    
    -- Application Settings
    application_methods JSONB, -- ['form', 'email', 'external']
    supports_easy_apply BOOLEAN DEFAULT FALSE,
    
    -- Status
    last_scraped_at TIMESTAMP,
    last_error TEXT,
    error_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert default job board configurations
INSERT INTO job_board_config (board_name, display_name, enabled, priority, base_url) VALUES
('nhs_jobs', 'NHS Jobs', TRUE, 100, 'https://www.jobs.nhs.uk'),
('indeed', 'Indeed UK', TRUE, 90, 'https://uk.indeed.com'),
('reed', 'Reed', TRUE, 80, 'https://www.reed.co.uk'),
('linkedin', 'LinkedIn', TRUE, 70, 'https://www.linkedin.com'),
('cv_library', 'CV Library', TRUE, 60, 'https://www.cv-library.co.uk')
ON CONFLICT (board_name) DO NOTHING;

-- ============================================
-- SYSTEM_LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS system_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    log_level VARCHAR(20), -- debug, info, warning, error, critical
    component VARCHAR(100), -- scraper, applier, ai_generator, etc.
    
    message TEXT NOT NULL,
    details JSONB,
    
    error_type VARCHAR(100),
    stack_trace TEXT,
    
    occurred_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_logs_level ON system_logs(log_level);
CREATE INDEX idx_logs_component ON system_logs(component);
CREATE INDEX idx_logs_occurred ON system_logs(occurred_at DESC);

-- ============================================
-- VIEWS FOR ANALYTICS
-- ============================================

-- Student Success Dashboard
CREATE OR REPLACE VIEW v_student_success AS
SELECT 
    s.id,
    s.first_name,
    s.last_name,
    s.email,
    s.placement_status,
    s.total_applications,
    s.total_responses,
    s.total_interviews,
    s.total_offers,
    CASE WHEN s.total_applications > 0 
        THEN ROUND((s.total_responses::FLOAT / s.total_applications * 100)::NUMERIC, 2)
        ELSE 0 END AS response_rate,
    CASE WHEN s.total_applications > 0 
        THEN ROUND((s.total_interviews::FLOAT / s.total_applications * 100)::NUMERIC, 2)
        ELSE 0 END AS interview_rate,
    COUNT(DISTINCT a.job_board) AS boards_applied_to,
    MAX(a.submitted_at) AS last_application_date,
    DATE_PART('day', NOW() - s.created_at) AS days_since_registration
FROM students s
LEFT JOIN applications a ON s.id = a.student_id AND a.status = 'submitted'
GROUP BY s.id;

-- Job Board Performance
CREATE OR REPLACE VIEW v_board_performance AS
SELECT 
    j.job_board,
    COUNT(DISTINCT j.id) AS total_jobs,
    COUNT(DISTINCT a.id) AS total_applications,
    COUNT(DISTINCT CASE WHEN a.status IN ('responded', 'interviewing', 'offered') THEN a.id END) AS total_responses,
    COUNT(DISTINCT CASE WHEN a.status = 'interviewing' OR a.interview_date IS NOT NULL THEN a.id END) AS total_interviews,
    CASE WHEN COUNT(DISTINCT a.id) > 0 
        THEN ROUND((COUNT(DISTINCT CASE WHEN a.status IN ('responded', 'interviewing', 'offered') THEN a.id END)::FLOAT / COUNT(DISTINCT a.id) * 100)::NUMERIC, 2)
        ELSE 0 END AS response_rate,
    AVG(j.relevance_score) AS avg_relevance_score
FROM jobs j
LEFT JOIN applications a ON j.id = a.job_id
WHERE j.status = 'active'
GROUP BY j.job_board;

-- Daily Application Stats
CREATE OR REPLACE VIEW v_daily_stats AS
SELECT 
    DATE(submitted_at) AS application_date,
    COUNT(*) AS applications_submitted,
    COUNT(DISTINCT student_id) AS unique_students,
    COUNT(DISTINCT job_id) AS unique_jobs,
    AVG(match_score) AS avg_match_score
FROM applications
WHERE submitted_at IS NOT NULL
GROUP BY DATE(submitted_at)
ORDER BY application_date DESC;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Update student statistics
CREATE OR REPLACE FUNCTION update_student_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE students SET
        total_applications = (SELECT COUNT(*) FROM applications WHERE student_id = NEW.student_id AND status = 'submitted'),
        total_responses = (SELECT COUNT(*) FROM applications WHERE student_id = NEW.student_id AND status IN ('responded', 'interviewing', 'offered')),
        total_interviews = (SELECT COUNT(*) FROM applications WHERE student_id = NEW.student_id AND status = 'interviewing'),
        total_offers = (SELECT COUNT(*) FROM applications WHERE student_id = NEW.student_id AND status = 'offered'),
        updated_at = NOW()
    WHERE id = NEW.student_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update student stats when application status changes
CREATE TRIGGER trigger_update_student_stats
AFTER INSERT OR UPDATE ON applications
FOR EACH ROW
EXECUTE FUNCTION update_student_stats();

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================

-- Enable RLS on all tables
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE follow_ups ENABLE ROW LEVEL SECURITY;

-- Students can only see their own data
CREATE POLICY students_select_own ON students
    FOR SELECT USING (t21_user_id = auth.uid());

CREATE POLICY students_update_own ON students
    FOR UPDATE USING (t21_user_id = auth.uid());

-- Students can see all jobs
CREATE POLICY jobs_select_all ON jobs
    FOR SELECT TO authenticated USING (true);

-- Students can see their own applications
CREATE POLICY applications_select_own ON applications
    FOR SELECT USING (
        student_id IN (SELECT id FROM students WHERE t21_user_id = auth.uid())
    );

-- Admins can see everything
CREATE POLICY admin_all_access ON students
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role IN ('super_admin', 'admin')
        )
    );

-- ============================================
-- SEED DATA (for testing)
-- ============================================

-- This will be populated by the application
-- Sample student, jobs, and applications for development

COMMENT ON TABLE students IS 'T21 graduates using the job accelerator service';
COMMENT ON TABLE jobs IS 'Jobs scraped from multiple job boards';
COMMENT ON TABLE applications IS 'Applications submitted by students to jobs';
COMMENT ON TABLE follow_ups IS 'Scheduled follow-up communications';
COMMENT ON TABLE analytics_events IS 'System-wide events for analytics and reporting';
COMMENT ON TABLE job_board_config IS 'Configuration for each job board integration';
COMMENT ON TABLE system_logs IS 'Application logs for debugging and monitoring';
