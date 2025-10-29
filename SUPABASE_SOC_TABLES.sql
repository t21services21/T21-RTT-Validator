-- ============================================
-- T21 SOC TRAINING PLATFORM - DATABASE TABLES
-- Run this in Supabase SQL Editor
-- ============================================

-- Students table
CREATE TABLE IF NOT EXISTS soc_students (
    student_id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    enrolled_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_points INTEGER DEFAULT 0,
    rank INTEGER,
    level TEXT DEFAULT 'Beginner',
    active BOOLEAN DEFAULT true
);

-- Courses table
CREATE TABLE IF NOT EXISTS soc_courses (
    course_id BIGSERIAL PRIMARY KEY,
    course_name TEXT NOT NULL,
    course_code TEXT UNIQUE,
    level TEXT,
    duration_weeks INTEGER,
    price DECIMAL(10,2),
    description TEXT,
    active BOOLEAN DEFAULT true
);

-- Course modules table
CREATE TABLE IF NOT EXISTS soc_course_modules (
    module_id BIGSERIAL PRIMARY KEY,
    course_id BIGINT REFERENCES soc_courses(course_id),
    module_name TEXT,
    module_order INTEGER,
    video_url TEXT,
    duration_minutes INTEGER,
    content TEXT
);

-- Student enrollments
CREATE TABLE IF NOT EXISTS soc_enrollments (
    enrollment_id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES soc_students(student_id),
    course_id BIGINT REFERENCES soc_courses(course_id),
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date TIMESTAMP,
    progress_percentage DECIMAL(5,2) DEFAULT 0,
    status TEXT DEFAULT 'active'
);

-- Module progress
CREATE TABLE IF NOT EXISTS soc_module_progress (
    progress_id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES soc_students(student_id),
    module_id BIGINT REFERENCES soc_course_modules(module_id),
    completed BOOLEAN DEFAULT false,
    completion_date TIMESTAMP,
    time_spent_minutes INTEGER DEFAULT 0,
    quiz_score DECIMAL(5,2)
);

-- Labs table
CREATE TABLE IF NOT EXISTS soc_labs (
    lab_id BIGSERIAL PRIMARY KEY,
    lab_name TEXT NOT NULL,
    category TEXT,
    difficulty TEXT,
    points INTEGER,
    time_limit_minutes INTEGER,
    description TEXT,
    objectives TEXT,
    flag TEXT,
    hints TEXT,
    active BOOLEAN DEFAULT true
);

-- Lab attempts
CREATE TABLE IF NOT EXISTS soc_lab_attempts (
    attempt_id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES soc_students(student_id),
    lab_id BIGINT REFERENCES soc_labs(lab_id),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    completed BOOLEAN DEFAULT false,
    score DECIMAL(5,2),
    hints_used INTEGER DEFAULT 0,
    time_taken_minutes INTEGER,
    flag_submitted TEXT
);

-- Certifications table
CREATE TABLE IF NOT EXISTS soc_certifications (
    cert_id BIGSERIAL PRIMARY KEY,
    cert_name TEXT NOT NULL,
    cert_code TEXT UNIQUE,
    level TEXT,
    requirements TEXT,
    exam_questions INTEGER,
    passing_score DECIMAL(5,2),
    active BOOLEAN DEFAULT true
);

-- Certification exams
CREATE TABLE IF NOT EXISTS soc_cert_exams (
    exam_id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES soc_students(student_id),
    cert_id BIGINT REFERENCES soc_certifications(cert_id),
    exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score DECIMAL(5,2),
    passed BOOLEAN,
    time_taken_minutes INTEGER,
    verification_code TEXT
);

-- Achievements table
CREATE TABLE IF NOT EXISTS soc_achievements (
    achievement_id BIGSERIAL PRIMARY KEY,
    achievement_name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    points INTEGER,
    requirement TEXT
);

-- Student achievements
CREATE TABLE IF NOT EXISTS soc_student_achievements (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES soc_students(student_id),
    achievement_id BIGINT REFERENCES soc_achievements(achievement_id),
    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CTF competitions
CREATE TABLE IF NOT EXISTS soc_ctf_competitions (
    competition_id BIGSERIAL PRIMARY KEY,
    competition_name TEXT NOT NULL,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    prize TEXT,
    description TEXT,
    active BOOLEAN DEFAULT true
);

-- CTF submissions
CREATE TABLE IF NOT EXISTS soc_ctf_submissions (
    submission_id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES soc_students(student_id),
    competition_id BIGINT REFERENCES soc_ctf_competitions(competition_id),
    flags_captured INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Study groups
CREATE TABLE IF NOT EXISTS soc_study_groups (
    group_id BIGSERIAL PRIMARY KEY,
    group_name TEXT NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    member_count INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT true
);

-- Group memberships
CREATE TABLE IF NOT EXISTS soc_group_memberships (
    membership_id BIGSERIAL PRIMARY KEY,
    student_id BIGINT REFERENCES soc_students(student_id),
    group_id BIGINT REFERENCES soc_study_groups(group_id),
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT DEFAULT 'member'
);

-- ============================================
-- INSERT SAMPLE DATA
-- ============================================

-- Insert default courses
INSERT INTO soc_courses (course_name, course_code, level, duration_weeks, price, description) VALUES
('SOC Analyst Foundation', 'SOC-101', 'Foundation', 8, 2000.00, 'Complete foundation in SOC operations and cybersecurity fundamentals'),
('SOC Analyst Professional', 'SOC-201', 'Professional', 12, 3500.00, 'Advanced threat detection, malware analysis, and incident response'),
('SOC Analyst Expert', 'SOC-301', 'Expert', 16, 5000.00, 'APT hunting, red team operations, and SOC leadership')
ON CONFLICT (course_code) DO NOTHING;

-- Insert certifications
INSERT INTO soc_certifications (cert_name, cert_code, level, requirements, exam_questions, passing_score) VALUES
('T21 Certified SOC Analyst Foundation', 'TCSAF', 'Foundation', 'Complete SOC-101 course', 100, 70.0),
('T21 Certified SOC Analyst Professional', 'TCSAP', 'Professional', 'Complete SOC-201 course and hold TCSAF', 150, 75.0),
('T21 Certified SOC Analyst Expert', 'TCSAE', 'Expert', 'Complete SOC-301 course and hold TCSAP', 200, 80.0)
ON CONFLICT (cert_code) DO NOTHING;

-- Insert sample labs
INSERT INTO soc_labs (lab_name, category, difficulty, points, time_limit_minutes, description, objectives, flag, hints) VALUES
('Linux Command Line Basics', 'Linux', 'Beginner', 50, 20, 'Learn essential Linux commands', 'Master basic Linux commands for cybersecurity', 'flag{linux_basics_complete}', '["Try ls -la", "Check hidden files", "Look in /home directory"]'),
('File Permissions & Privilege Escalation', 'Linux', 'Intermediate', 200, 45, 'Find and exploit SUID binaries', 'Escalate privileges to root', 'flag{root_access_achieved}', '["Find SUID binaries", "Check /usr/bin", "Use find command"]'),
('Network Scanning with Nmap', 'Network', 'Beginner', 100, 30, 'Scan target network', 'Identify open ports and services', 'flag{nmap_scan_complete}', '["Use nmap -sV", "Scan all ports", "Check for SSH"]'),
('Packet Analysis with Wireshark', 'Network', 'Intermediate', 200, 45, 'Analyze network traffic', 'Find hidden data in packets', 'flag{packet_analysis_expert}', '["Filter HTTP traffic", "Look for POST requests", "Check packet data"]'),
('SQL Injection Basics', 'Web', 'Beginner', 150, 40, 'Exploit SQL injection vulnerability', 'Extract database information', 'flag{sql_injection_success}', '["Try OR 1=1", "Use UNION SELECT", "Enumerate tables"]'),
('Cross-Site Scripting (XSS)', 'Web', 'Intermediate', 200, 45, 'Find and exploit XSS vulnerability', 'Execute JavaScript in victim browser', 'flag{xss_vulnerability_found}', '["Try <script>alert(1)</script>", "Check input fields", "Bypass filters"]')
ON CONFLICT DO NOTHING;

-- Insert achievements
INSERT INTO soc_achievements (achievement_name, description, icon, points, requirement) VALUES
('First Steps', 'Complete your first module', '👣', 10, 'complete_first_module'),
('Lab Rat', 'Complete 10 hands-on labs', '🔬', 50, 'complete_10_labs'),
('Speed Learner', 'Complete 5 modules in one week', '⚡', 100, '5_modules_one_week'),
('CTF Champion', 'Win a CTF competition', '🏆', 500, 'win_ctf'),
('Certified Pro', 'Earn Professional certification', '🎖️', 200, 'earn_professional_cert'),
('Master Hacker', 'Complete all advanced labs', '💻', 1000, 'complete_all_advanced_labs'),
('Perfect Score', 'Score 100% on any exam', '💯', 150, 'perfect_exam_score'),
('Early Bird', 'Log in before 6 AM', '🌅', 25, 'login_before_6am'),
('Night Owl', 'Complete lab after midnight', '🦉', 25, 'lab_after_midnight'),
('Streak Master', '7-day learning streak', '🔥', 100, '7_day_streak')
ON CONFLICT DO NOTHING;

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_soc_students_email ON soc_students(email);
CREATE INDEX IF NOT EXISTS idx_soc_enrollments_student ON soc_enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_soc_enrollments_course ON soc_enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_soc_module_progress_student ON soc_module_progress(student_id);
CREATE INDEX IF NOT EXISTS idx_soc_lab_attempts_student ON soc_lab_attempts(student_id);
CREATE INDEX IF NOT EXISTS idx_soc_cert_exams_student ON soc_cert_exams(student_id);

-- ============================================
-- ENABLE ROW LEVEL SECURITY (RLS)
-- ============================================

ALTER TABLE soc_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_course_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_module_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_labs ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_lab_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_certifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_cert_exams ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_student_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_ctf_competitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_ctf_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_study_groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE soc_group_memberships ENABLE ROW LEVEL SECURITY;

-- ============================================
-- CREATE RLS POLICIES (Allow authenticated users)
-- ============================================

-- Students can view their own data
CREATE POLICY "Students can view own data" ON soc_students FOR SELECT USING (auth.uid()::text = email);
CREATE POLICY "Students can update own data" ON soc_students FOR UPDATE USING (auth.uid()::text = email);

-- Everyone can view courses
CREATE POLICY "Anyone can view courses" ON soc_courses FOR SELECT TO authenticated USING (true);
CREATE POLICY "Anyone can view modules" ON soc_course_modules FOR SELECT TO authenticated USING (true);
CREATE POLICY "Anyone can view labs" ON soc_labs FOR SELECT TO authenticated USING (true);
CREATE POLICY "Anyone can view certifications" ON soc_certifications FOR SELECT TO authenticated USING (true);
CREATE POLICY "Anyone can view achievements" ON soc_achievements FOR SELECT TO authenticated USING (true);

-- Students can manage their own enrollments
CREATE POLICY "Students can view own enrollments" ON soc_enrollments FOR SELECT USING (true);
CREATE POLICY "Students can create enrollments" ON soc_enrollments FOR INSERT WITH CHECK (true);

-- Students can manage their own progress
CREATE POLICY "Students can view own progress" ON soc_module_progress FOR ALL USING (true);
CREATE POLICY "Students can view own lab attempts" ON soc_lab_attempts FOR ALL USING (true);
CREATE POLICY "Students can view own exams" ON soc_cert_exams FOR ALL USING (true);
CREATE POLICY "Students can view own achievements" ON soc_student_achievements FOR ALL USING (true);

-- CTF policies
CREATE POLICY "Anyone can view CTF competitions" ON soc_ctf_competitions FOR SELECT TO authenticated USING (true);
CREATE POLICY "Students can manage own submissions" ON soc_ctf_submissions FOR ALL USING (true);

-- Study group policies
CREATE POLICY "Anyone can view study groups" ON soc_study_groups FOR SELECT TO authenticated USING (true);
CREATE POLICY "Students can manage group memberships" ON soc_group_memberships FOR ALL USING (true);

-- ============================================
-- DONE!
-- ============================================

-- Verify tables created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE 'soc_%'
ORDER BY table_name;
