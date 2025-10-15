-- T21 PATIENT REGISTRATION & EPISODE MANAGEMENT
-- Supabase Database Schema

-- ============================================
-- TABLE 1: PATIENTS
-- ============================================

CREATE TABLE IF NOT EXISTS public.patients (
    id BIGSERIAL PRIMARY KEY,
    patient_id TEXT NOT NULL UNIQUE,
    nhs_number TEXT,
    nhs_status TEXT DEFAULT 'pending', -- 'verified', 'pending', 'invalid'
    
    -- Demographics
    title TEXT,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    full_name TEXT,
    date_of_birth DATE,
    gender TEXT,
    
    -- Address
    address_line1 TEXT,
    address_line2 TEXT,
    city TEXT,
    postcode TEXT,
    
    -- Contact
    phone_home TEXT,
    phone_mobile TEXT,
    email TEXT,
    
    -- GP Information
    gp_name TEXT,
    gp_practice TEXT,
    gp_address TEXT,
    
    -- Next of Kin
    next_of_kin_name TEXT,
    next_of_kin_relationship TEXT,
    next_of_kin_phone TEXT,
    
    -- Emergency Contact
    emergency_contact_name TEXT,
    emergency_contact_phone TEXT,
    
    -- Additional Info
    ethnicity TEXT,
    language TEXT DEFAULT 'English',
    interpreter_required BOOLEAN DEFAULT FALSE,
    religion TEXT,
    marital_status TEXT,
    occupation TEXT,
    
    -- Notes
    notes TEXT,
    
    -- Status
    status TEXT DEFAULT 'active',
    registration_date TIMESTAMPTZ DEFAULT NOW(),
    registered_by TEXT,
    
    -- Multi-tenant
    user_email TEXT NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_patients_user_email ON public.patients(user_email);
CREATE INDEX IF NOT EXISTS idx_patients_nhs_number ON public.patients(nhs_number);
CREATE INDEX IF NOT EXISTS idx_patients_patient_id ON public.patients(patient_id);
CREATE INDEX IF NOT EXISTS idx_patients_full_name ON public.patients(full_name);

-- Row Level Security
ALTER TABLE public.patients ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own patients
CREATE POLICY patients_user_isolation ON public.patients
    FOR ALL
    USING (user_email = auth.jwt() ->> 'email');


-- ============================================
-- TABLE 2: EPISODES
-- ============================================

CREATE TABLE IF NOT EXISTS public.episodes (
    id BIGSERIAL PRIMARY KEY,
    episode_id TEXT NOT NULL UNIQUE,
    episode_type TEXT NOT NULL, -- 'consultant', 'treatment', 'diagnostic'
    
    -- Patient Reference
    patient_id TEXT NOT NULL,
    patient_name TEXT,
    
    -- Common Fields
    status TEXT DEFAULT 'active',
    created_date TIMESTAMPTZ DEFAULT NOW(),
    created_by TEXT,
    notes TEXT,
    
    -- Consultant Episode Fields
    consultant_name TEXT,
    specialty TEXT,
    start_date DATE,
    end_date DATE,
    reason TEXT,
    expected_duration_weeks INTEGER,
    priority TEXT,
    referral_source TEXT,
    discharge_reason TEXT,
    closed_date TIMESTAMPTZ,
    
    -- Treatment Episode Fields
    treatment_type TEXT,
    treatment_date DATE,
    location TEXT,
    provider TEXT,
    outcome TEXT,
    complications TEXT,
    consultant_episode_id TEXT,
    
    -- Diagnostic Episode Fields
    investigation_type TEXT,
    request_date DATE,
    requested_by TEXT,
    performed_date DATE,
    results TEXT,
    urgency TEXT,
    
    -- Linking
    pathway_id TEXT,
    
    -- Multi-tenant
    user_email TEXT NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_episodes_user_email ON public.episodes(user_email);
CREATE INDEX IF NOT EXISTS idx_episodes_patient_id ON public.episodes(patient_id);
CREATE INDEX IF NOT EXISTS idx_episodes_episode_id ON public.episodes(episode_id);
CREATE INDEX IF NOT EXISTS idx_episodes_type ON public.episodes(episode_type);
CREATE INDEX IF NOT EXISTS idx_episodes_pathway_id ON public.episodes(pathway_id);

-- Row Level Security
ALTER TABLE public.episodes ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own episodes
CREATE POLICY episodes_user_isolation ON public.episodes
    FOR ALL
    USING (user_email = auth.jwt() ->> 'email');


-- ============================================
-- DONE!
-- ============================================

-- Run this SQL in Supabase SQL Editor:
-- 1. Go to your Supabase project
-- 2. Click "SQL Editor" in left sidebar
-- 3. Click "New Query"
-- 4. Copy and paste this entire file
-- 5. Click "Run" or press Ctrl+Enter
-- 6. Tables will be created!
