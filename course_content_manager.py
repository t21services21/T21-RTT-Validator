"""
COURSE CONTENT MANAGEMENT SYSTEM
Manage all training content, videos, quizzes, materials

Features:
- Course content storage
- Video management
- Quiz generation
- Progress tracking
- Content delivery
"""

import json
from datetime import datetime
from soc_training_database import db

class CourseContentManager:
    
    def __init__(self):
        self.initialize_default_courses()
    
    def initialize_default_courses(self):
        """Initialize default SOC training courses"""
        
        # Check if courses already exist
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            return  # Already initialized
        
        # Level 1: Foundation
        foundation_id = db.add_course(
            course_name="SOC Analyst Foundation",
            course_code="SOC-101",
            level="Foundation",
            duration_weeks=8,
            price=2000.00,
            description="Complete foundation in SOC operations and cybersecurity fundamentals"
        )
        
        # Level 2: Professional
        professional_id = db.add_course(
            course_name="SOC Analyst Professional",
            course_code="SOC-201",
            level="Professional",
            duration_weeks=12,
            price=3500.00,
            description="Advanced threat detection, malware analysis, and incident response"
        )
        
        # Level 3: Expert
        expert_id = db.add_course(
            course_name="SOC Analyst Expert",
            course_code="SOC-301",
            level="Expert",
            duration_weeks=16,
            price=5000.00,
            description="APT hunting, red team operations, and SOC leadership"
        )
        
        # Add modules for Foundation course
        self.add_foundation_modules(foundation_id)
        self.add_professional_modules(professional_id)
        self.add_expert_modules(expert_id)
        
        # Initialize certifications
        self.initialize_certifications()
        
        # Initialize labs
        self.initialize_labs()
        
        # Initialize achievements
        self.initialize_achievements()
    
    def add_foundation_modules(self, course_id):
        """Add Foundation course modules"""
        
        modules = [
            {
                "name": "Introduction to Cybersecurity",
                "order": 1,
                "duration": 240,  # 4 hours
                "content": """
                # Introduction to Cybersecurity
                
                ## Learning Objectives
                - Understand the CIA Triad
                - Learn about threat landscape
                - Identify common attack vectors
                - Understand security principles
                
                ## Topics Covered
                1. Confidentiality, Integrity, Availability
                2. Threat actors and motivations
                3. Attack vectors and vulnerabilities
                4. Defense in depth
                5. Risk management basics
                
                ## Practical Exercises
                - Identify security threats in scenarios
                - Analyze real-world breaches
                - Risk assessment exercise
                """
            },
            {
                "name": "Network Security Basics",
                "order": 2,
                "duration": 360,  # 6 hours
                "content": """
                # Network Security Fundamentals
                
                ## Learning Objectives
                - Master TCP/IP fundamentals
                - Understand network protocols
                - Learn firewall concepts
                - Implement network segmentation
                
                ## Topics Covered
                1. TCP/IP protocol suite
                2. Common protocols (HTTP, DNS, FTP, SSH)
                3. Firewalls and IDS/IPS
                4. Network segmentation
                5. VPNs and encryption
                
                ## Hands-On Labs
                - Wireshark packet analysis
                - Firewall rule configuration
                - Network traffic monitoring
                """
            },
            {
                "name": "SOC Fundamentals",
                "order": 3,
                "duration": 480,  # 8 hours
                "content": """
                # Security Operations Center Fundamentals
                
                ## Learning Objectives
                - Understand SOC structure
                - Learn SOC analyst roles
                - Master alert triage
                - Understand escalation procedures
                
                ## Topics Covered
                1. What is a SOC?
                2. SOC tiers (1, 2, 3)
                3. SOC workflows
                4. Alert triage and prioritization
                5. Incident escalation
                
                ## Practical Training
                - SOC simulator exercises
                - Alert triage practice
                - Escalation scenarios
                """
            },
            {
                "name": "SIEM Tools & Log Analysis",
                "order": 4,
                "duration": 600,  # 10 hours
                "content": """
                # SIEM Tools and Log Analysis
                
                ## Learning Objectives
                - Master SIEM concepts
                - Learn Splunk basics
                - Understand log analysis
                - Create effective searches
                
                ## Topics Covered
                1. What is SIEM?
                2. Popular SIEM platforms
                3. Log sources and collection
                4. Search queries and filters
                5. Dashboard creation
                
                ## Hands-On Practice
                - Splunk fundamentals
                - Creating searches and alerts
                - Building dashboards
                - Log correlation
                """
            },
            {
                "name": "Incident Detection & Response",
                "order": 5,
                "duration": 480,  # 8 hours
                "content": """
                # Incident Detection and Response
                
                ## Learning Objectives
                - Identify indicators of compromise
                - Understand incident response lifecycle
                - Learn containment strategies
                - Master evidence collection
                
                ## Topics Covered
                1. Indicators of Compromise (IoCs)
                2. Incident response phases
                3. Containment strategies
                4. Evidence preservation
                5. Documentation requirements
                
                ## Real-World Scenarios
                - Incident detection exercises
                - Response playbook execution
                - Evidence gathering
                """
            }
        ]
        
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        for module in modules:
            cursor.execute("""
            INSERT INTO course_modules (course_id, module_name, module_order, duration_minutes, content)
            VALUES (?, ?, ?, ?, ?)
            """, (course_id, module['name'], module['order'], module['duration'], module['content']))
        
        conn.commit()
        conn.close()
    
    def add_professional_modules(self, course_id):
        """Add Professional course modules"""
        
        modules = [
            {"name": "Advanced Threat Detection", "order": 1, "duration": 600},
            {"name": "Threat Intelligence", "order": 2, "duration": 480},
            {"name": "Malware Analysis Fundamentals", "order": 3, "duration": 720},
            {"name": "Static Malware Analysis", "order": 4, "duration": 600},
            {"name": "Dynamic Malware Analysis", "order": 5, "duration": 720},
            {"name": "Digital Forensics Basics", "order": 6, "duration": 600},
            {"name": "Incident Forensics", "order": 7, "duration": 720},
            {"name": "Security Automation", "order": 8, "duration": 480},
            {"name": "SOAR Platforms", "order": 9, "duration": 600}
        ]
        
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        for module in modules:
            cursor.execute("""
            INSERT INTO course_modules (course_id, module_name, module_order, duration_minutes, content)
            VALUES (?, ?, ?, ?, ?)
            """, (course_id, module['name'], module['order'], module['duration'], "Content coming soon"))
        
        conn.commit()
        conn.close()
    
    def add_expert_modules(self, course_id):
        """Add Expert course modules"""
        
        modules = [
            {"name": "Advanced Persistent Threats", "order": 1, "duration": 720},
            {"name": "Threat Hunting Methodologies", "order": 2, "duration": 720},
            {"name": "Red Team Operations", "order": 3, "duration": 840},
            {"name": "Blue Team Defense", "order": 4, "duration": 720},
            {"name": "Purple Team Collaboration", "order": 5, "duration": 600},
            {"name": "Cloud Security (AWS)", "order": 6, "duration": 720},
            {"name": "Cloud Security (Azure)", "order": 7, "duration": 720},
            {"name": "Container Security", "order": 8, "duration": 600},
            {"name": "Zero Trust Architecture", "order": 9, "duration": 480},
            {"name": "SOC Management", "order": 10, "duration": 600},
            {"name": "Strategic Security Leadership", "order": 11, "duration": 480}
        ]
        
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        for module in modules:
            cursor.execute("""
            INSERT INTO course_modules (course_id, module_name, module_order, duration_minutes, content)
            VALUES (?, ?, ?, ?, ?)
            """, (course_id, module['name'], module['order'], module['duration'], "Content coming soon"))
        
        conn.commit()
        conn.close()
    
    def initialize_certifications(self):
        """Initialize certification exams"""
        
        # Foundation Certification
        db.add_certification(
            cert_name="T21 Certified SOC Analyst Foundation",
            cert_code="TCSAF",
            level="Foundation",
            requirements="Complete SOC-101 course",
            exam_questions=100,
            passing_score=70.0
        )
        
        # Professional Certification
        db.add_certification(
            cert_name="T21 Certified SOC Analyst Professional",
            cert_code="TCSAP",
            level="Professional",
            requirements="Complete SOC-201 course and hold TCSAF",
            exam_questions=150,
            passing_score=75.0
        )
        
        # Expert Certification
        db.add_certification(
            cert_name="T21 Certified SOC Analyst Expert",
            cert_code="TCSAE",
            level="Expert",
            requirements="Complete SOC-301 course and hold TCSAP",
            exam_questions=200,
            passing_score=80.0
        )
    
    def initialize_labs(self):
        """Initialize hands-on labs"""
        
        labs = [
            # Linux Labs
            {
                "name": "Linux Command Line Basics",
                "category": "Linux",
                "difficulty": "Beginner",
                "points": 50,
                "time_limit": 20,
                "description": "Learn essential Linux commands",
                "objectives": "Master basic Linux commands for cybersecurity",
                "flag": "flag{linux_master_2025}",
                "hints": json.dumps(["Try 'ls -la'", "Check hidden files", "Look in /home directory"])
            },
            {
                "name": "File Permissions & Privilege Escalation",
                "category": "Linux",
                "difficulty": "Intermediate",
                "points": 200,
                "time_limit": 45,
                "description": "Find and exploit SUID binaries",
                "objectives": "Escalate privileges to root",
                "flag": "flag{root_access_achieved}",
                "hints": json.dumps(["Find SUID binaries", "Check /usr/bin", "Use find command"])
            },
            # Network Labs
            {
                "name": "Network Scanning with Nmap",
                "category": "Network",
                "difficulty": "Beginner",
                "points": 100,
                "time_limit": 30,
                "description": "Scan target network",
                "objectives": "Identify open ports and services",
                "flag": "flag{nmap_scan_complete}",
                "hints": json.dumps(["Use nmap -sV", "Scan all ports", "Check for SSH"])
            },
            {
                "name": "Packet Analysis with Wireshark",
                "category": "Network",
                "difficulty": "Intermediate",
                "points": 200,
                "time_limit": 45,
                "description": "Analyze network traffic",
                "objectives": "Find hidden data in packets",
                "flag": "flag{packet_analysis_expert}",
                "hints": json.dumps(["Filter HTTP traffic", "Look for POST requests", "Check packet data"])
            },
            # Web Hacking Labs
            {
                "name": "SQL Injection Basics",
                "category": "Web",
                "difficulty": "Beginner",
                "points": 150,
                "time_limit": 40,
                "description": "Exploit SQL injection vulnerability",
                "objectives": "Extract database information",
                "flag": "flag{sql_injection_success}",
                "hints": json.dumps(["Try ' OR '1'='1", "Use UNION SELECT", "Enumerate tables"])
            },
            {
                "name": "Cross-Site Scripting (XSS)",
                "category": "Web",
                "difficulty": "Intermediate",
                "points": 200,
                "time_limit": 45,
                "description": "Find and exploit XSS vulnerability",
                "objectives": "Execute JavaScript in victim browser",
                "flag": "flag{xss_vulnerability_found}",
                "hints": json.dumps(["Try <script>alert(1)</script>", "Check input fields", "Bypass filters"])
            }
        ]
        
        for lab in labs:
            db.add_lab(
                lab_name=lab['name'],
                category=lab['category'],
                difficulty=lab['difficulty'],
                points=lab['points'],
                time_limit=lab['time_limit'],
                description=lab['description'],
                objectives=lab['objectives'],
                flag=lab['flag'],
                hints=lab['hints']
            )
    
    def initialize_achievements(self):
        """Initialize achievement badges"""
        
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        achievements = [
            ("First Steps", "Complete your first module", "👣", 10, "complete_first_module"),
            ("Lab Rat", "Complete 10 hands-on labs", "🔬", 50, "complete_10_labs"),
            ("Speed Learner", "Complete 5 modules in one week", "⚡", 100, "5_modules_one_week"),
            ("CTF Champion", "Win a CTF competition", "🏆", 500, "win_ctf"),
            ("Certified Pro", "Earn Professional certification", "🎖️", 200, "earn_professional_cert"),
            ("Master Hacker", "Complete all advanced labs", "💻", 1000, "complete_all_advanced_labs"),
            ("Perfect Score", "Score 100% on any exam", "💯", 150, "perfect_exam_score"),
            ("Early Bird", "Log in before 6 AM", "🌅", 25, "login_before_6am"),
            ("Night Owl", "Complete lab after midnight", "🦉", 25, "lab_after_midnight"),
            ("Streak Master", "7-day learning streak", "🔥", 100, "7_day_streak")
        ]
        
        for ach in achievements:
            cursor.execute("""
            INSERT INTO achievements (achievement_name, description, icon, points, requirement)
            VALUES (?, ?, ?, ?, ?)
            """, ach)
        
        conn.commit()
        conn.close()
    
    def get_course_content(self, course_id):
        """Get all modules for a course"""
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM course_modules
        WHERE course_id = ?
        ORDER BY module_order
        """, (course_id,))
        
        modules = cursor.fetchall()
        conn.close()
        return modules
    
    def get_student_progress(self, student_id, course_id):
        """Get student progress in a course"""
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT cm.module_id, cm.module_name, cm.duration_minutes,
               COALESCE(mp.completed, 0) as completed,
               COALESCE(mp.time_spent_minutes, 0) as time_spent
        FROM course_modules cm
        LEFT JOIN module_progress mp ON cm.module_id = mp.module_id 
            AND mp.student_id = ?
        WHERE cm.course_id = ?
        ORDER BY cm.module_order
        """, (student_id, course_id))
        
        progress = cursor.fetchall()
        conn.close()
        return progress

# Initialize content manager
content_manager = CourseContentManager()
