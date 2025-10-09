-- T21 SERVICES - SUPABASE DATABASE SETUP
-- Copy and paste this into Supabase SQL Editor and click RUN

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table (Main user accounts)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'trial',
    user_type TEXT NOT NULL DEFAULT 'student',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    expiry_date TIMESTAMP WITH TIME ZONE,
    suspended_reason TEXT,
    suspended_by TEXT,
    suspended_at TIMESTAMP WITH TIME ZONE,
    terminated_at TIMESTAMP WITH TIME ZONE,
    created_by TEXT DEFAULT 'system'
);

-- User Usage Table (Track activity)
CREATE TABLE IF NOT EXISTS user_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    total_logins INTEGER DEFAULT 0,
    logins_today INTEGER DEFAULT 0,
    last_login_date DATE,
    ai_questions_today INTEGER DEFAULT 0,
    quizzes_today INTEGER DEFAULT 0,
    validations_today INTEGER DEFAULT 0,
    last_reset_date DATE DEFAULT CURRENT_DATE
);

-- User Tracking Table (Geolocation & Security)
CREATE TABLE IF NOT EXISTS user_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email TEXT NOT NULL,
    login_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    success BOOLEAN NOT NULL,
    ip_address TEXT,
    city TEXT,
    region TEXT,
    country TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    device TEXT,
    browser TEXT,
    os TEXT
);

-- Module Access Table (Per-user module permissions)
CREATE TABLE IF NOT EXISTS module_access (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email TEXT NOT NULL,
    module_name TEXT NOT NULL,
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    granted_by TEXT,
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_email, module_name)
);

-- Audit Log Table (Track admin actions)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    action TEXT NOT NULL,
    performed_by TEXT NOT NULL,
    target_user TEXT,
    details JSONB,
    ip_address TEXT
);

-- User Notes Table (Admin notes about users)
CREATE TABLE IF NOT EXISTS user_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email TEXT NOT NULL,
    note TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_type ON users(user_type);
CREATE INDEX IF NOT EXISTS idx_users_expiry ON users(expiry_date);
CREATE INDEX IF NOT EXISTS idx_tracking_email ON user_tracking(user_email);
CREATE INDEX IF NOT EXISTS idx_tracking_time ON user_tracking(login_time);
CREATE INDEX IF NOT EXISTS idx_module_access_email ON module_access(user_email);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_target ON audit_log(target_user);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to auto-update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert your existing 4 users (with hashed passwords from your JSON files)
-- You'll update these after migration script runs

SELECT 'Database setup complete! Tables created successfully!' as status;
