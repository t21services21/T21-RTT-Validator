-- T21 SERVICES - PTL PATIENTS TABLE
-- Permanent storage for student practice data

CREATE TABLE IF NOT EXISTS ptl_patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    patient_name VARCHAR(255) NOT NULL,
    nhs_number VARCHAR(20) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    referral_date DATE NOT NULL,
    referral_source VARCHAR(255),
    clock_start_date DATE NOT NULL,
    pathway_type VARCHAR(50) DEFAULT 'routine',
    priority VARCHAR(50) DEFAULT 'Routine',
    current_status VARCHAR(255) DEFAULT 'Awaiting First Appointment',
    consultant VARCHAR(255),
    contact_number VARCHAR(50),
    rtt_code VARCHAR(10) DEFAULT '10',
    clock_status VARCHAR(50) DEFAULT 'ACTIVE',
    notes TEXT,
    added_date TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW(),
    appointments JSONB DEFAULT '[]',
    events JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast user queries
CREATE INDEX IF NOT EXISTS idx_ptl_user_email ON ptl_patients(user_email);
CREATE INDEX IF NOT EXISTS idx_ptl_patient_id ON ptl_patients(patient_id);
CREATE INDEX IF NOT EXISTS idx_ptl_specialty ON ptl_patients(specialty);
CREATE INDEX IF NOT EXISTS idx_ptl_clock_status ON ptl_patients(clock_status);

-- Row Level Security (RLS) - Users can only see their own data
ALTER TABLE ptl_patients ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own PTL data"
    ON ptl_patients FOR SELECT
    USING (auth.email() = user_email);

CREATE POLICY "Users can insert own PTL data"
    ON ptl_patients FOR INSERT
    WITH CHECK (auth.email() = user_email);

CREATE POLICY "Users can update own PTL data"
    ON ptl_patients FOR UPDATE
    USING (auth.email() = user_email);

CREATE POLICY "Users can delete own PTL data"
    ON ptl_patients FOR DELETE
    USING (auth.email() = user_email);

-- Admin can see all data
CREATE POLICY "Admins can view all PTL data"
    ON ptl_patients FOR SELECT
    USING (auth.email() IN (
        SELECT email FROM users WHERE user_type = 'admin'
    ));
