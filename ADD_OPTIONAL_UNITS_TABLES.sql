-- ADD OPTIONAL UNITS SELECTION AND EVIDENCE TRACKING

-- Optional Units Available
CREATE TABLE IF NOT EXISTS tquk_optional_units (
    id BIGSERIAL PRIMARY KEY,
    course_id TEXT NOT NULL,
    unit_number INTEGER NOT NULL,
    unit_name TEXT NOT NULL,
    credits INTEGER NOT NULL,
    category TEXT, -- e.g., 'dementia_care', 'mental_health', 'end_of_life'
    description TEXT,
    learning_outcomes INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Student's Selected Optional Units
CREATE TABLE IF NOT EXISTS tquk_student_optional_units (
    id BIGSERIAL PRIMARY KEY,
    learner_email TEXT NOT NULL,
    course_id TEXT NOT NULL,
    unit_number INTEGER NOT NULL,
    unit_name TEXT NOT NULL,
    credits INTEGER NOT NULL,
    selected_date TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'selected', -- selected, in_progress, completed
    completion_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert Optional Units for Level 3 Adult Care
INSERT INTO tquk_optional_units (course_id, unit_number, unit_name, credits, category, learning_outcomes) VALUES
('level3_adult_care', 8, 'Dementia Care', 5, 'dementia_care', 6),
('level3_adult_care', 9, 'Mental Health Awareness', 4, 'mental_health', 5),
('level3_adult_care', 10, 'End of Life Care', 5, 'end_of_life', 6),
('level3_adult_care', 11, 'Medication Management', 4, 'medication', 5),
('level3_adult_care', 12, 'Moving and Handling', 3, 'moving_handling', 4),
('level3_adult_care', 13, 'Infection Prevention and Control', 3, 'infection_control', 4),
('level3_adult_care', 14, 'Nutrition and Hydration', 3, 'nutrition', 4),
('level3_adult_care', 15, 'Personal Care', 4, 'personal_care', 5),
('level3_adult_care', 16, 'Supporting Independence', 4, 'independence', 5),
('level3_adult_care', 17, 'Working in Partnership', 3, 'partnership', 4),
('level3_adult_care', 18, 'Dignity and Privacy', 3, 'dignity', 4),
('level3_adult_care', 19, 'Safeguarding Vulnerable Adults', 4, 'safeguarding', 5);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_optional_units_course ON tquk_optional_units(course_id);
CREATE INDEX IF NOT EXISTS idx_student_optional_units ON tquk_student_optional_units(learner_email, course_id);
CREATE INDEX IF NOT EXISTS idx_evidence_status ON tquk_evidence(learner_email, status);

-- Enable RLS
ALTER TABLE tquk_optional_units ENABLE ROW LEVEL SECURITY;
ALTER TABLE tquk_student_optional_units ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Everyone can view optional units" ON tquk_optional_units
    FOR SELECT USING (true);

CREATE POLICY "Students can view own selections" ON tquk_student_optional_units
    FOR SELECT USING (auth.jwt() ->> 'email' = learner_email);

CREATE POLICY "Students can insert own selections" ON tquk_student_optional_units
    FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = learner_email);

CREATE POLICY "Teachers can view all selections" ON tquk_student_optional_units
    FOR ALL USING (auth.jwt() ->> 'role' IN ('teacher', 'admin', 'super_admin'));

-- Add function to calculate total credits
CREATE OR REPLACE FUNCTION calculate_student_credits(student_email TEXT, course TEXT)
RETURNS INTEGER AS $$
DECLARE
    total_credits INTEGER;
BEGIN
    -- Mandatory credits (fixed for Level 3 Adult Care)
    total_credits := 24;
    
    -- Add optional unit credits
    SELECT COALESCE(SUM(credits), 0) INTO total_credits
    FROM tquk_student_optional_units
    WHERE learner_email = student_email AND course_id = course;
    
    RETURN total_credits + 24; -- 24 mandatory + optional
END;
$$ LANGUAGE plpgsql;
