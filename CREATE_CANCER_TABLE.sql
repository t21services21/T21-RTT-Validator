-- T21 SERVICES - CANCER PATIENTS TABLE
CREATE TABLE IF NOT EXISTS cancer_patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    patient_name VARCHAR(255) NOT NULL,
    nhs_number VARCHAR(20) NOT NULL,
    cancer_type VARCHAR(100) NOT NULL,
    pathway_type VARCHAR(50) NOT NULL,
    referral_date DATE NOT NULL,
    pathway_start_date DATE NOT NULL,
    referring_clinician VARCHAR(255),
    primary_site VARCHAR(255),
    suspected_diagnosis TEXT,
    urgency VARCHAR(50),
    contact_number VARCHAR(50),
    current_status VARCHAR(255),
    pathway_status VARCHAR(50),
    notes TEXT,
    added_date TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW(),
    milestones JSONB DEFAULT '[]',
    appointments JSONB DEFAULT '[]',
    diagnostics JSONB DEFAULT '[]',
    mdt_dates JSONB DEFAULT '[]',
    events JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_cancer_user_email ON cancer_patients(user_email);
CREATE INDEX IF NOT EXISTS idx_cancer_patient_id ON cancer_patients(patient_id);

-- Row Level Security
ALTER TABLE cancer_patients ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own cancer patients" ON cancer_patients FOR SELECT USING (auth.email() = user_email);
CREATE POLICY "Users can insert their own cancer patients" ON cancer_patients FOR INSERT WITH CHECK (auth.email() = user_email);
CREATE POLICY "Users can update their own cancer patients" ON cancer_patients FOR UPDATE USING (auth.email() = user_email);
CREATE POLICY "Users can delete their own cancer patients" ON cancer_patients FOR DELETE USING (auth.email() = user_email);
