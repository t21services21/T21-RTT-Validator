-- T21 SERVICES - ADD TWO-FACTOR AUTHENTICATION COLUMNS
-- Run this SQL script in your Supabase SQL Editor to add 2FA support
-- Navigate to: Supabase Dashboard → SQL Editor → New Query → Paste and Run

-- Add 2FA columns to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS two_factor_secret TEXT,
ADD COLUMN IF NOT EXISTS two_factor_backup_codes TEXT,
ADD COLUMN IF NOT EXISTS two_factor_enabled BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS two_factor_enabled_at TIMESTAMP WITH TIME ZONE;

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_two_factor_enabled ON users(two_factor_enabled);

-- Add comment for documentation
COMMENT ON COLUMN users.two_factor_secret IS 'Base32 encoded TOTP secret for 2FA';
COMMENT ON COLUMN users.two_factor_backup_codes IS 'JSON array of backup codes';
COMMENT ON COLUMN users.two_factor_enabled IS 'Whether 2FA is enabled for this user';
COMMENT ON COLUMN users.two_factor_enabled_at IS 'Timestamp when 2FA was enabled';

-- SUCCESS!
-- You can now use Two-Factor Authentication in T21 Services Platform
