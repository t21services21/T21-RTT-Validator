-- T21 PATHWAYS TABLE
-- Add this to Supabase to enable pathway management

-- ============================================
-- TABLE: PATHWAYS
-- ============================================

CREATE TABLE IF NOT EXISTS public.pathways (
    id BIGSERIAL PRIMARY KEY,
    pathway_id TEXT NOT NULL UNIQUE,
    pathway_type TEXT NOT NULL,
    pathway_name TEXT,
    
    -- Patient Reference
    patient_id TEXT NOT NULL,
    patient_name TEXT,
    
    -- Timeline
    start_date DATE NOT NULL,
    end_date DATE,
    breach_date DATE,
    
    -- Status
    status TEXT DEFAULT 'active',
    clock_status TEXT DEFAULT 'running',
    
    -- Progress
    days_elapsed INTEGER DEFAULT 0,
    days_remaining INTEGER,
    risk_level TEXT,
    
    -- Clinical Details
    specialty TEXT,
    consultant TEXT,
    referral_source TEXT,
    priority TEXT,
    reason TEXT,
    notes TEXT,
    
    -- Closure
    outcome TEXT,
    closing_notes TEXT,
    closed_date TIMESTAMPTZ,
    
    -- Audit
    created_date TIMESTAMPTZ DEFAULT NOW(),
    created_by TEXT,
    
    -- Multi-tenant
    user_email TEXT NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_pathways_user_email ON public.pathways(user_email);
CREATE INDEX IF NOT EXISTS idx_pathways_patient_id ON public.pathways(patient_id);
CREATE INDEX IF NOT EXISTS idx_pathways_pathway_id ON public.pathways(pathway_id);
CREATE INDEX IF NOT EXISTS idx_pathways_type ON public.pathways(pathway_type);
CREATE INDEX IF NOT EXISTS idx_pathways_status ON public.pathways(status);
CREATE INDEX IF NOT EXISTS idx_pathways_risk_level ON public.pathways(risk_level);

-- Row Level Security
ALTER TABLE public.pathways ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own pathways
CREATE POLICY pathways_user_isolation ON public.pathways
    FOR ALL
    USING (user_email = auth.jwt() ->> 'email');
