"""
SOC TRAINING DATABASE SYSTEM
Complete backend for student progress, courses, labs, certifications

Features:
- Student progress tracking
- Course completion
- Lab results
- Certification records
- Leaderboards
- Analytics
"""

import sqlite3
import json
from datetime import datetime
import hashlib

class SOCTrainingDatabase:
    def __init__(self, db_path="soc_training.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize all database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Students table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            enrolled_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_points INTEGER DEFAULT 0,
            rank INTEGER,
            level TEXT DEFAULT 'Beginner',
            active BOOLEAN DEFAULT 1
        )
        """)
        
        # Courses table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            course_code TEXT UNIQUE,
            level TEXT,
            duration_weeks INTEGER,
            price REAL,
            description TEXT,
            active BOOLEAN DEFAULT 1
        )
        """)
        
        # Course modules table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_modules (
            module_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            module_name TEXT,
            module_order INTEGER,
            video_url TEXT,
            duration_minutes INTEGER,
            content TEXT,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        """)
        
        # Student enrollments
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completion_date TIMESTAMP,
            progress_percentage REAL DEFAULT 0,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        """)
        
        # Module progress
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS module_progress (
            progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            module_id INTEGER,
            completed BOOLEAN DEFAULT 0,
            completion_date TIMESTAMP,
            time_spent_minutes INTEGER DEFAULT 0,
            quiz_score REAL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (module_id) REFERENCES course_modules(module_id)
        )
        """)
        
        # Labs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS labs (
            lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_name TEXT NOT NULL,
            category TEXT,
            difficulty TEXT,
            points INTEGER,
            time_limit_minutes INTEGER,
            description TEXT,
            objectives TEXT,
            flag TEXT,
            hints TEXT,
            active BOOLEAN DEFAULT 1
        )
        """)
        
        # Lab attempts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            lab_id INTEGER,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            completed BOOLEAN DEFAULT 0,
            score REAL,
            hints_used INTEGER DEFAULT 0,
            time_taken_minutes INTEGER,
            flag_submitted TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (lab_id) REFERENCES labs(lab_id)
        )
        """)
        
        # Certifications table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS certifications (
            cert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cert_name TEXT NOT NULL,
            cert_code TEXT UNIQUE,
            level TEXT,
            requirements TEXT,
            exam_questions INTEGER,
            passing_score REAL,
            active BOOLEAN DEFAULT 1
        )
        """)
        
        # Certification exams
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cert_exams (
            exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            cert_id INTEGER,
            exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            score REAL,
            passed BOOLEAN,
            time_taken_minutes INTEGER,
            verification_code TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (cert_id) REFERENCES certifications(cert_id)
        )
        """)
        
        # Achievements table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            achievement_name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            points INTEGER,
            requirement TEXT
        )
        """)
        
        # Student achievements
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            achievement_id INTEGER,
            earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id)
        )
        """)
        
        # CTF competitions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ctf_competitions (
            competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_name TEXT NOT NULL,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            prize TEXT,
            description TEXT,
            active BOOLEAN DEFAULT 1
        )
        """)
        
        # CTF submissions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ctf_submissions (
            submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            competition_id INTEGER,
            flags_captured INTEGER DEFAULT 0,
            total_points INTEGER DEFAULT 0,
            submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (competition_id) REFERENCES ctf_competitions(competition_id)
        )
        """)
        
        # Study groups
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            description TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            member_count INTEGER DEFAULT 0,
            active BOOLEAN DEFAULT 1
        )
        """)
        
        # Group memberships
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_memberships (
            membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            group_id INTEGER,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            role TEXT DEFAULT 'member',
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (group_id) REFERENCES study_groups(group_id)
        )
        """)
        
        conn.commit()
        conn.close()
    
    # ============================================
    # STUDENT METHODS
    # ============================================
    
    def add_student(self, email, name):
        """Add new student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO students (email, name)
            VALUES (?, ?)
            """, (email, name))
            conn.commit()
            student_id = cursor.lastrowid
            return student_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_student(self, email):
        """Get student by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM students WHERE email = ?
        """, (email,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def update_student_points(self, student_id, points):
        """Update student total points"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE students 
        SET total_points = total_points + ?
        WHERE student_id = ?
        """, (points, student_id))
        conn.commit()
        conn.close()
    
    # ============================================
    # COURSE METHODS
    # ============================================
    
    def add_course(self, course_name, course_code, level, duration_weeks, price, description):
        """Add new course"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO courses (course_name, course_code, level, duration_weeks, price, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (course_name, course_code, level, duration_weeks, price, description))
        conn.commit()
        course_id = cursor.lastrowid
        conn.close()
        return course_id
    
    def enroll_student(self, student_id, course_id):
        """Enroll student in course"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO enrollments (student_id, course_id)
        VALUES (?, ?)
        """, (student_id, course_id))
        conn.commit()
        conn.close()
    
    def update_course_progress(self, student_id, course_id, progress_percentage):
        """Update course progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE enrollments 
        SET progress_percentage = ?
        WHERE student_id = ? AND course_id = ?
        """, (progress_percentage, student_id, course_id))
        conn.commit()
        conn.close()
    
    # ============================================
    # LAB METHODS
    # ============================================
    
    def add_lab(self, lab_name, category, difficulty, points, time_limit, description, objectives, flag, hints):
        """Add new lab"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO labs (lab_name, category, difficulty, points, time_limit_minutes, description, objectives, flag, hints)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (lab_name, category, difficulty, points, time_limit, description, objectives, flag, hints))
        conn.commit()
        lab_id = cursor.lastrowid
        conn.close()
        return lab_id
    
    def start_lab(self, student_id, lab_id):
        """Start lab attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO lab_attempts (student_id, lab_id)
        VALUES (?, ?)
        """, (student_id, lab_id))
        conn.commit()
        attempt_id = cursor.lastrowid
        conn.close()
        return attempt_id
    
    def submit_lab_flag(self, attempt_id, flag_submitted, correct_flag):
        """Submit lab flag"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        completed = (flag_submitted == correct_flag)
        score = 100 if completed else 0
        
        cursor.execute("""
        UPDATE lab_attempts 
        SET end_time = CURRENT_TIMESTAMP,
            completed = ?,
            score = ?,
            flag_submitted = ?
        WHERE attempt_id = ?
        """, (completed, score, flag_submitted, attempt_id))
        conn.commit()
        conn.close()
        return completed
    
    # ============================================
    # CERTIFICATION METHODS
    # ============================================
    
    def add_certification(self, cert_name, cert_code, level, requirements, exam_questions, passing_score):
        """Add new certification"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO certifications (cert_name, cert_code, level, requirements, exam_questions, passing_score)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (cert_name, cert_code, level, requirements, exam_questions, passing_score))
        conn.commit()
        cert_id = cursor.lastrowid
        conn.close()
        return cert_id
    
    def record_exam(self, student_id, cert_id, score, time_taken):
        """Record certification exam"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get passing score
        cursor.execute("SELECT passing_score FROM certifications WHERE cert_id = ?", (cert_id,))
        passing_score = cursor.fetchone()[0]
        
        passed = (score >= passing_score)
        verification_code = hashlib.sha256(f"{student_id}{cert_id}{datetime.now()}".encode()).hexdigest()[:12]
        
        cursor.execute("""
        INSERT INTO cert_exams (student_id, cert_id, score, passed, time_taken_minutes, verification_code)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, cert_id, score, passed, time_taken, verification_code))
        conn.commit()
        conn.close()
        return passed, verification_code
    
    # ============================================
    # LEADERBOARD METHODS
    # ============================================
    
    def get_leaderboard(self, limit=10):
        """Get top students"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT name, email, total_points, rank
        FROM students
        WHERE active = 1
        ORDER BY total_points DESC
        LIMIT ?
        """, (limit,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def update_rankings(self):
        """Update all student rankings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE students
        SET rank = (
            SELECT COUNT(*) + 1
            FROM students s2
            WHERE s2.total_points > students.total_points
        )
        """)
        conn.commit()
        conn.close()
    
    # ============================================
    # ANALYTICS METHODS
    # ============================================
    
    def get_student_stats(self, student_id):
        """Get comprehensive student statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Basic info
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        stats['student'] = cursor.fetchone()
        
        # Course progress
        cursor.execute("""
        SELECT COUNT(*) as enrolled, 
               AVG(progress_percentage) as avg_progress,
               SUM(CASE WHEN progress_percentage = 100 THEN 1 ELSE 0 END) as completed
        FROM enrollments
        WHERE student_id = ?
        """, (student_id,))
        stats['courses'] = cursor.fetchone()
        
        # Lab stats
        cursor.execute("""
        SELECT COUNT(*) as attempts,
               SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed,
               AVG(score) as avg_score
        FROM lab_attempts
        WHERE student_id = ?
        """, (student_id,))
        stats['labs'] = cursor.fetchone()
        
        # Certifications
        cursor.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) as passed
        FROM cert_exams
        WHERE student_id = ?
        """, (student_id,))
        stats['certifications'] = cursor.fetchone()
        
        conn.close()
        return stats

# Initialize database on import
db = SOCTrainingDatabase()
