"""
ANALYTICS & REPORTING SYSTEM
Complete analytics for training, operations, and business

Features:
- Student analytics
- Course performance
- Revenue tracking
- SOC operations metrics
- Business intelligence
"""

import sqlite3
from datetime import datetime, timedelta
import pandas as pd
from soc_training_database import db

class AnalyticsEngine:
    """
    Complete analytics and reporting system
    """
    
    def __init__(self):
        self.db_path = db.db_path
    
    # ============================================
    # TRAINING ANALYTICS
    # ============================================
    
    def get_training_overview(self):
        """Get overall training metrics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total students
        cursor.execute("SELECT COUNT(*) FROM students WHERE active = 1")
        total_students = cursor.fetchone()[0]
        
        # Active enrollments
        cursor.execute("SELECT COUNT(*) FROM enrollments WHERE status = 'active'")
        active_enrollments = cursor.fetchone()[0]
        
        # Completed courses
        cursor.execute("SELECT COUNT(*) FROM enrollments WHERE progress_percentage = 100")
        completed_courses = cursor.fetchone()[0]
        
        # Average progress
        cursor.execute("SELECT AVG(progress_percentage) FROM enrollments WHERE status = 'active'")
        avg_progress = cursor.fetchone()[0] or 0
        
        # Certifications earned
        cursor.execute("SELECT COUNT(*) FROM cert_exams WHERE passed = 1")
        certifications_earned = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_students": total_students,
            "active_enrollments": active_enrollments,
            "completed_courses": completed_courses,
            "avg_progress": round(avg_progress, 1),
            "certifications_earned": certifications_earned
        }
    
    def get_course_performance(self, course_id):
        """Get performance metrics for a course"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enrollment count
        cursor.execute("SELECT COUNT(*) FROM enrollments WHERE course_id = ?", (course_id,))
        enrollment_count = cursor.fetchone()[0]
        
        # Completion rate
        cursor.execute("""
        SELECT 
            COUNT(CASE WHEN progress_percentage = 100 THEN 1 END) * 100.0 / COUNT(*) as completion_rate
        FROM enrollments 
        WHERE course_id = ?
        """, (course_id,))
        completion_rate = cursor.fetchone()[0] or 0
        
        # Average score
        cursor.execute("""
        SELECT AVG(mp.quiz_score)
        FROM module_progress mp
        JOIN course_modules cm ON mp.module_id = cm.module_id
        WHERE cm.course_id = ?
        """, (course_id,))
        avg_score = cursor.fetchone()[0] or 0
        
        # Time to complete
        cursor.execute("""
        SELECT AVG(JULIANDAY(completion_date) - JULIANDAY(enrollment_date))
        FROM enrollments
        WHERE course_id = ? AND completion_date IS NOT NULL
        """, (course_id,))
        avg_days_to_complete = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "enrollment_count": enrollment_count,
            "completion_rate": round(completion_rate, 1),
            "avg_score": round(avg_score, 1),
            "avg_days_to_complete": round(avg_days_to_complete, 1)
        }
    
    def get_student_performance(self, student_id):
        """Get comprehensive student performance"""
        
        stats = db.get_student_stats(student_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Learning streak
        cursor.execute("""
        SELECT COUNT(DISTINCT DATE(completion_date))
        FROM module_progress
        WHERE student_id = ? 
        AND completion_date >= DATE('now', '-7 days')
        """, (student_id,))
        learning_streak = cursor.fetchone()[0]
        
        # Total time spent
        cursor.execute("""
        SELECT SUM(time_spent_minutes)
        FROM module_progress
        WHERE student_id = ?
        """, (student_id,))
        total_time_minutes = cursor.fetchone()[0] or 0
        
        # Achievements earned
        cursor.execute("""
        SELECT COUNT(*)
        FROM student_achievements
        WHERE student_id = ?
        """, (student_id,))
        achievements_earned = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            **stats,
            "learning_streak": learning_streak,
            "total_time_hours": round(total_time_minutes / 60, 1),
            "achievements_earned": achievements_earned
        }
    
    # ============================================
    # LAB ANALYTICS
    # ============================================
    
    def get_lab_statistics(self):
        """Get overall lab statistics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total attempts
        cursor.execute("SELECT COUNT(*) FROM lab_attempts")
        total_attempts = cursor.fetchone()[0]
        
        # Completion rate
        cursor.execute("""
        SELECT COUNT(CASE WHEN completed = 1 THEN 1 END) * 100.0 / COUNT(*)
        FROM lab_attempts
        """)
        completion_rate = cursor.fetchone()[0] or 0
        
        # Average score
        cursor.execute("SELECT AVG(score) FROM lab_attempts WHERE completed = 1")
        avg_score = cursor.fetchone()[0] or 0
        
        # Most popular labs
        cursor.execute("""
        SELECT l.lab_name, COUNT(*) as attempts
        FROM lab_attempts la
        JOIN labs l ON la.lab_id = l.lab_id
        GROUP BY l.lab_id
        ORDER BY attempts DESC
        LIMIT 5
        """)
        popular_labs = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_attempts": total_attempts,
            "completion_rate": round(completion_rate, 1),
            "avg_score": round(avg_score, 1),
            "popular_labs": popular_labs
        }
    
    # ============================================
    # FINANCIAL ANALYTICS
    # ============================================
    
    def get_revenue_metrics(self):
        """Get revenue and financial metrics"""
        
        # Simulated data (in production, query actual payment records)
        
        today = datetime.now()
        
        return {
            "monthly_revenue": 127500,
            "annual_revenue": 1245000,
            "outstanding": 45000,
            "paid_this_month": 82500,
            "revenue_by_service": {
                "Training": 630000,
                "SOC Monitoring": 750000,
                "Consulting": 125000
            },
            "revenue_trend": self.get_revenue_trend(),
            "client_count": 12,
            "avg_client_value": 103750
        }
    
    def get_revenue_trend(self):
        """Get 12-month revenue trend"""
        
        # Simulated data
        months = []
        revenue = []
        
        for i in range(12, 0, -1):
            date = datetime.now() - timedelta(days=30*i)
            months.append(date.strftime('%b %y'))
            revenue.append(85000 + (i * 3500))  # Growing trend
        
        return {"months": months, "revenue": revenue}
    
    # ============================================
    # SOC OPERATIONS ANALYTICS
    # ============================================
    
    def get_soc_metrics(self):
        """Get SOC operations metrics"""
        
        # Simulated data (in production, query actual SOC data)
        
        return {
            "active_alerts": 23,
            "alerts_today": 47,
            "threats_blocked": 156,
            "avg_response_time_minutes": 4.2,
            "incidents_resolved": 34,
            "sla_compliance": 94.0,
            "client_satisfaction": 4.8,
            "uptime": 99.97
        }
    
    def get_threat_analytics(self):
        """Get threat intelligence analytics"""
        
        return {
            "threats_by_type": {
                "Brute Force": 45,
                "Malware": 23,
                "Phishing": 18,
                "DDoS": 12,
                "SQL Injection": 8
            },
            "threats_by_severity": {
                "Critical": 3,
                "High": 12,
                "Medium": 47,
                "Low": 94
            },
            "threats_by_source": {
                "Russia": 45,
                "China": 32,
                "North Korea": 18,
                "Iran": 12,
                "Other": 8
            }
        }
    
    # ============================================
    # BUSINESS INTELLIGENCE
    # ============================================
    
    def get_business_overview(self):
        """Get complete business overview"""
        
        training = self.get_training_overview()
        revenue = self.get_revenue_metrics()
        soc = self.get_soc_metrics()
        
        return {
            "training": training,
            "revenue": revenue,
            "soc": soc,
            "growth_rate": 18.5,
            "market_share": 0.5,
            "employee_count": 25
        }
    
    def generate_executive_report(self, period="monthly"):
        """Generate executive summary report"""
        
        overview = self.get_business_overview()
        
        report = {
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_revenue": overview['revenue']['monthly_revenue'],
                "total_students": overview['training']['total_students'],
                "active_clients": overview['revenue']['client_count'],
                "growth_rate": overview['growth_rate']
            },
            "training": overview['training'],
            "revenue": overview['revenue'],
            "operations": overview['soc'],
            "recommendations": self.generate_recommendations(overview)
        }
        
        return report
    
    def generate_recommendations(self, overview):
        """Generate AI-powered recommendations"""
        
        recommendations = []
        
        # Training recommendations
        if overview['training']['avg_progress'] < 50:
            recommendations.append({
                "category": "Training",
                "priority": "High",
                "recommendation": "Average course progress is low. Consider adding more engagement features or reducing module length."
            })
        
        # Revenue recommendations
        if overview['revenue']['outstanding'] > 40000:
            recommendations.append({
                "category": "Finance",
                "priority": "High",
                "recommendation": "Outstanding payments exceed £40K. Implement automated payment reminders."
            })
        
        # Operations recommendations
        if overview['soc']['sla_compliance'] < 95:
            recommendations.append({
                "category": "Operations",
                "priority": "Medium",
                "recommendation": "SLA compliance below target. Review response times and staffing levels."
            })
        
        return recommendations
    
    # ============================================
    # EXPORT FUNCTIONS
    # ============================================
    
    def export_to_dataframe(self, data, data_type):
        """Export data to pandas DataFrame"""
        
        if data_type == "students":
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM students", conn)
            conn.close()
            return df
        
        elif data_type == "enrollments":
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM enrollments", conn)
            conn.close()
            return df
        
        elif data_type == "lab_attempts":
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM lab_attempts", conn)
            conn.close()
            return df
        
        return pd.DataFrame()
    
    def export_to_csv(self, data_type, filename):
        """Export data to CSV file"""
        
        df = self.export_to_dataframe(None, data_type)
        df.to_csv(filename, index=False)
        return filename
    
    def export_to_excel(self, report_data, filename):
        """Export report to Excel"""
        
        # In production: Use pandas ExcelWriter
        return filename

# Analytics engine instance
analytics_engine = AnalyticsEngine()

# Quick access functions
def get_training_overview():
    return analytics_engine.get_training_overview()

def get_revenue_metrics():
    return analytics_engine.get_revenue_metrics()

def get_soc_metrics():
    return analytics_engine.get_soc_metrics()

def generate_executive_report(period="monthly"):
    return analytics_engine.generate_executive_report(period)
