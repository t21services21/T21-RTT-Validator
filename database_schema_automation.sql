-- ============================================================================
-- T21 NHS JOB APPLICATION AUTOMATION - COMPLETE DATABASE SCHEMA
-- ============================================================================

-- Student automation settings with contract approval
CREATE TABLE IF NOT EXISTS student_automation_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    
    -- Trac credentials (encrypted)
    trac_email TEXT NOT NULL,
    trac_password_encrypted TEXT NOT NULL,
    encryption_key_id TEXT NOT NULL,
    
    -- Contract approval (already signed)
    contract_signed BOOLEAN DEFAULT true,
    contract_signed_date TIMESTAMPTZ,
    contract_document_url TEXT,
    
    -- Auto-submit settings (no per-app approval needed!)
    auto_submit_enabled BOOLEAN DEFAULT true,
    max_applications_per_day INTEGER DEFAULT 50,
    
    -- Job search filters - COMPLETE
    requires_sponsorship BOOLEAN DEFAULT false,
    
    -- Keywords filter
    search_keywords TEXT[] DEFAULT ARRAY['RTT', 'Patient Pathway', 'Administrator', 'Coordinator', 'Validator'],
    exclude_keywords TEXT[] DEFAULT ARRAY['Senior', 'Manager', 'Lead', 'Consultant'],
    
    -- Location filters
    preferred_locations TEXT[] DEFAULT ARRAY['London', 'Manchester', 'Birmingham'],
    search_radius_miles INTEGER DEFAULT 20,
    
    -- Band filters
    preferred_bands TEXT[] DEFAULT ARRAY['Band 3', 'Band 4', 'Band 5'],
    
    -- Working pattern filters
    working_patterns TEXT[] DEFAULT ARRAY['Full time', 'Part time'],
    include_hybrid BOOLEAN DEFAULT true,
    include_remote BOOLEAN DEFAULT true,
    
    -- Contract type filters
    contract_types TEXT[] DEFAULT ARRAY['Permanent', 'Fixed term'],
    
    -- Timing filters
    max_days_until_closing INTEGER DEFAULT 14,
    min_days_until_closing INTEGER DEFAULT 2,
    
    -- Notification settings
    notification_email TEXT,
    notification_phone TEXT,
    send_daily_summary BOOLEAN DEFAULT true,
    send_interview_alerts BOOLEAN DEFAULT true,
    
    -- Status
    status TEXT DEFAULT 'active', -- active, paused, suspended
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Discovered jobs from NHS Jobs scraper
CREATE TABLE IF NOT EXISTS discovered_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Job identification
    job_reference TEXT UNIQUE NOT NULL,
    nhs_jobs_id TEXT,
    
    -- Basic info
    title TEXT NOT NULL,
    trust TEXT NOT NULL,
    location TEXT,
    city TEXT,
    postcode TEXT,
    
    -- Job details
    band TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    working_pattern TEXT, -- Full time, Part time, Flexible
    contract_type TEXT, -- Permanent, Fixed term, Bank
    is_hybrid BOOLEAN DEFAULT false,
    is_remote BOOLEAN DEFAULT false,
    
    -- Sponsorship (CRITICAL!)
    has_sponsorship BOOLEAN DEFAULT false,
    sponsorship_text TEXT,
    
    -- Dates
    posted_date DATE,
    closing_date DATE NOT NULL,
    start_date DATE,
    
    -- Job content
    job_description TEXT,
    main_duties TEXT,
    person_specification JSONB,
    essential_criteria JSONB,
    desirable_criteria JSONB,
    
    -- URLs
    nhs_jobs_url TEXT,
    trac_apply_url TEXT,
    
    -- Metadata
    discovered_at TIMESTAMPTZ DEFAULT NOW(),
    last_checked TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Application queue and tracking
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- References
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    job_id UUID REFERENCES discovered_jobs(id) ON DELETE CASCADE,
    
    -- Status workflow
    status TEXT DEFAULT 'queued',
    -- Statuses: queued -> processing -> ready -> auto_submitting -> submitted -> failed
    
    -- Priority
    priority TEXT DEFAULT 'normal', -- urgent, high, normal, low
    
    -- AI-generated content
    ai_supporting_information TEXT,
    ai_generation_time NUMERIC, -- seconds
    ai_word_count INTEGER,
    
    -- Application data
    application_data JSONB,
    preview_pdf_url TEXT,
    
    -- Scheduling
    queued_at TIMESTAMPTZ DEFAULT NOW(),
    scheduled_submit_time TIMESTAMPTZ,
    processing_started_at TIMESTAMPTZ,
    
    -- Submission
    submitted_at TIMESTAMPTZ,
    confirmation_number TEXT,
    trac_application_id TEXT,
    trac_application_url TEXT,
    
    -- Error handling
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    error_message TEXT,
    last_error_at TIMESTAMPTZ,
    
    -- Tracking
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Prevent duplicate applications
    UNIQUE(student_id, job_id)
);

-- Interview tracking with Trac integration
CREATE TABLE IF NOT EXISTS interviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- References
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    job_id UUID REFERENCES discovered_jobs(id),
    application_id UUID REFERENCES applications(id),
    
    -- Interview details
    interview_date TIMESTAMPTZ,
    interview_time TIME,
    interview_location TEXT,
    interview_address TEXT,
    interview_format TEXT, -- in-person, video, phone, teams, zoom
    interview_panel TEXT[],
    
    -- Trac data
    trac_message_id TEXT,
    trac_detected_at TIMESTAMPTZ,
    invitation_email_html TEXT,
    
    -- Status
    status TEXT DEFAULT 'scheduled', -- scheduled, confirmed, completed, cancelled, rescheduled, no_show
    
    -- Outcome
    outcome TEXT, -- offered, rejected, second_interview, assessment_centre, waiting
    outcome_date DATE,
    offer_details JSONB,
    
    -- Preparation
    preparation_materials_sent BOOLEAN DEFAULT false,
    reminder_sent BOOLEAN DEFAULT false,
    
    -- Notes
    student_notes TEXT,
    admin_notes TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trac inbox monitoring (auto-detect interviews)
CREATE TABLE IF NOT EXISTS trac_inbox_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Student reference
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    trac_email TEXT NOT NULL,
    
    -- Message details
    message_id TEXT NOT NULL,
    subject TEXT,
    from_sender TEXT,
    received_date TIMESTAMPTZ,
    message_html TEXT,
    message_plain TEXT,
    
    -- Classification
    message_type TEXT, -- interview_invitation, rejection, offer, query, other
    confidence_score NUMERIC,
    
    -- Processing
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMPTZ,
    linked_interview_id UUID REFERENCES interviews(id),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(student_id, message_id)
);

-- Email notifications log
CREATE TABLE IF NOT EXISTS email_notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Recipient
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    email_address TEXT NOT NULL,
    
    -- Notification details
    notification_type TEXT NOT NULL,
    -- Types: application_submitted, interview_detected, interview_reminder, 
    --        offer_received, weekly_summary, daily_digest
    
    subject TEXT NOT NULL,
    html_content TEXT,
    
    -- Related data
    related_application_id UUID REFERENCES applications(id),
    related_interview_id UUID REFERENCES interviews(id),
    
    -- Tracking
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    delivered_at TIMESTAMPTZ,
    opened_at TIMESTAMPTZ,
    clicked_at TIMESTAMPTZ,
    bounced BOOLEAN DEFAULT false,
    
    -- SendGrid tracking
    sendgrid_message_id TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Student statistics (auto-calculated)
CREATE TABLE IF NOT EXISTS student_application_stats (
    student_id UUID PRIMARY KEY REFERENCES students(id) ON DELETE CASCADE,
    
    -- Application counts
    total_applications INTEGER DEFAULT 0,
    applications_queued INTEGER DEFAULT 0,
    applications_processing INTEGER DEFAULT 0,
    applications_submitted INTEGER DEFAULT 0,
    applications_failed INTEGER DEFAULT 0,
    
    -- Interview counts
    interviews_invited INTEGER DEFAULT 0,
    interviews_scheduled INTEGER DEFAULT 0,
    interviews_completed INTEGER DEFAULT 0,
    
    -- Outcomes
    offers_received INTEGER DEFAULT 0,
    rejections_received INTEGER DEFAULT 0,
    
    -- Success metrics
    application_to_interview_rate NUMERIC,
    interview_to_offer_rate NUMERIC,
    overall_success_rate NUMERIC,
    
    -- Timing
    average_response_time_days NUMERIC,
    last_application_date DATE,
    last_interview_date DATE,
    
    -- Activity
    applications_this_week INTEGER DEFAULT 0,
    applications_this_month INTEGER DEFAULT 0,
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Admin activity log
CREATE TABLE IF NOT EXISTS admin_activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Admin user
    admin_user_id UUID,
    admin_email TEXT,
    
    -- Action
    action_type TEXT NOT NULL,
    -- Types: student_registered, settings_updated, application_reviewed, 
    --        interview_updated, system_paused, bulk_action
    
    action_details JSONB,
    
    -- Related entities
    affected_student_id UUID,
    affected_application_id UUID,
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- System configuration
CREATE TABLE IF NOT EXISTS system_config (
    key TEXT PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_by TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default system config
INSERT INTO system_config (key, value, description) VALUES
    ('scraper_interval_hours', '6', 'How often to run job scraper'),
    ('max_concurrent_applications', '10', 'Max applications to process in parallel'),
    ('rate_limit_per_hour', '50', 'Max applications to submit per hour'),
    ('ai_model', '"gpt-4"', 'OpenAI model for supporting information'),
    ('enable_auto_submit', 'true', 'Global auto-submit toggle'),
    ('enable_interview_detection', 'true', 'Auto-detect interviews from Trac')
ON CONFLICT (key) DO NOTHING;

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_applications_student_status ON applications(student_id, status);
CREATE INDEX IF NOT EXISTS idx_applications_scheduled_time ON applications(scheduled_submit_time) WHERE status = 'ready';
CREATE INDEX IF NOT EXISTS idx_discovered_jobs_closing_date ON discovered_jobs(closing_date) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_discovered_jobs_sponsorship ON discovered_jobs(has_sponsorship) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_interviews_student_date ON interviews(student_id, interview_date);
CREATE INDEX IF NOT EXISTS idx_interviews_status ON interviews(status);
CREATE INDEX IF NOT EXISTS idx_trac_messages_unprocessed ON trac_inbox_messages(student_id, processed) WHERE processed = false;

-- ============================================================================
-- TRIGGERS FOR AUTO-UPDATES
-- ============================================================================

-- Update student stats when application status changes
CREATE OR REPLACE FUNCTION update_student_stats()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO student_application_stats (student_id)
    VALUES (NEW.student_id)
    ON CONFLICT (student_id) DO UPDATE SET
        total_applications = (
            SELECT COUNT(*) FROM applications WHERE student_id = NEW.student_id
        ),
        applications_queued = (
            SELECT COUNT(*) FROM applications WHERE student_id = NEW.student_id AND status = 'queued'
        ),
        applications_submitted = (
            SELECT COUNT(*) FROM applications WHERE student_id = NEW.student_id AND status = 'submitted'
        ),
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_student_stats
AFTER INSERT OR UPDATE ON applications
FOR EACH ROW
EXECUTE FUNCTION update_student_stats();

-- ============================================================================
-- VIEWS FOR ADMIN DASHBOARD
-- ============================================================================

-- Admin overview: All students and their performance
CREATE OR REPLACE VIEW admin_student_overview AS
SELECT 
    s.id,
    s.first_name,
    s.last_name,
    s.email,
    sas.auto_submit_enabled,
    sas.status AS automation_status,
    sas.requires_sponsorship,
    stats.total_applications,
    stats.applications_submitted,
    stats.interviews_invited,
    stats.offers_received,
    stats.overall_success_rate,
    stats.last_application_date,
    sas.created_at AS automation_started
FROM students s
LEFT JOIN student_automation_settings sas ON s.id = sas.student_id
LEFT JOIN student_application_stats stats ON s.id = stats.student_id
ORDER BY stats.last_application_date DESC NULLS LAST;

-- Admin job queue overview
CREATE OR REPLACE VIEW admin_application_queue AS
SELECT 
    a.id,
    s.first_name || ' ' || s.last_name AS student_name,
    dj.title AS job_title,
    dj.trust,
    dj.location,
    dj.closing_date,
    a.status,
    a.priority,
    a.scheduled_submit_time,
    a.attempts,
    a.created_at
FROM applications a
JOIN students s ON a.student_id = s.id
JOIN discovered_jobs dj ON a.job_id = dj.id
ORDER BY a.scheduled_submit_time ASC NULLS LAST;

-- Admin interview calendar
CREATE OR REPLACE VIEW admin_interview_calendar AS
SELECT 
    i.id,
    s.first_name || ' ' || s.last_name AS student_name,
    s.email AS student_email,
    dj.title AS job_title,
    dj.trust,
    i.interview_date,
    i.interview_location,
    i.interview_format,
    i.status,
    i.outcome
FROM interviews i
JOIN students s ON i.student_id = s.id
LEFT JOIN discovered_jobs dj ON i.job_id = dj.id
WHERE i.status IN ('scheduled', 'confirmed')
ORDER BY i.interview_date ASC;

-- ============================================================================
-- FUNCTIONS FOR BUSINESS LOGIC
-- ============================================================================

-- Calculate priority based on closing date and student preferences
CREATE OR REPLACE FUNCTION calculate_application_priority(
    p_closing_date DATE,
    p_has_sponsorship BOOLEAN,
    p_student_requires_sponsorship BOOLEAN
)
RETURNS TEXT AS $$
DECLARE
    days_until_closing INTEGER;
BEGIN
    days_until_closing := p_closing_date - CURRENT_DATE;
    
    -- Urgent: Closes within 2 days
    IF days_until_closing <= 2 THEN
        RETURN 'urgent';
    END IF;
    
    -- High: Sponsorship match + closes within 7 days
    IF p_student_requires_sponsorship AND p_has_sponsorship AND days_until_closing <= 7 THEN
        RETURN 'high';
    END IF;
    
    -- Normal: Standard processing
    IF days_until_closing <= 14 THEN
        RETURN 'normal';
    END IF;
    
    -- Low: Long time until closing
    RETURN 'low';
END;
$$ LANGUAGE plpgsql;

COMMENT ON TABLE student_automation_settings IS 'Student job automation settings with contract-based approval';
COMMENT ON TABLE discovered_jobs IS 'Jobs scraped from NHS Jobs with sponsorship detection';
COMMENT ON TABLE applications IS 'Application queue with auto-submit (no per-app approval)';
COMMENT ON TABLE interviews IS 'Interview tracking with Trac auto-detection';
COMMENT ON TABLE trac_inbox_messages IS 'Trac inbox messages for interview detection';
