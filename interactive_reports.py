"""
T21 INTERACTIVE REPORTING SYSTEM
Replace Excel with built-in dashboards and reports

Features:
- Real-time interactive dashboards
- Downloadable reports (PDF, CSV)
- Visual analytics
- Automated insights
- No Excel needed!
"""

import streamlit as st
from datetime import datetime, timedelta
import json

def generate_student_progress_report(progress_data):
    """Generate comprehensive student progress report"""
    
    report = {
        'student_name': progress_data.get('name', 'Student'),
        'report_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'summary': {
            'total_points': progress_data.get('total_points', 0),
            'quizzes_completed': progress_data.get('quizzes_completed', 0),
            'accuracy': progress_data.get('accuracy', 0),
            'current_streak': progress_data.get('current_streak', 0),
            'best_streak': progress_data.get('best_streak', 0),
            'badges_earned': len(progress_data.get('badges', [])),
            'time_spent_hours': round(progress_data.get('time_spent', 0) / 3600, 2)
        },
        'badges': progress_data.get('badges', []),
        'strengths': identify_strengths(progress_data),
        'areas_for_improvement': identify_weaknesses(progress_data),
        'recommendations': generate_recommendations(progress_data)
    }
    
    return report


def identify_strengths(progress_data):
    """Identify student's strong areas"""
    strengths = []
    
    accuracy = progress_data.get('accuracy', 0)
    if accuracy >= 90:
        strengths.append("Excellent overall accuracy (90%+)")
    elif accuracy >= 80:
        strengths.append("Good accuracy (80%+)")
    
    streak = progress_data.get('best_streak', 0)
    if streak >= 10:
        strengths.append(f"Strong consistency ({streak} correct in a row)")
    
    if progress_data.get('quizzes_completed', 0) >= 20:
        strengths.append("Dedicated learner (20+ quizzes completed)")
    
    return strengths if strengths else ["Keep practicing to build strengths!"]


def identify_weaknesses(progress_data):
    """Identify areas needing improvement"""
    weaknesses = []
    
    accuracy = progress_data.get('accuracy', 0)
    if accuracy < 60:
        weaknesses.append("Focus on understanding RTT codes basics")
    
    if progress_data.get('quizzes_completed', 0) < 10:
        weaknesses.append("Complete more practice quizzes")
    
    return weaknesses if weaknesses else ["No major weaknesses identified!"]


def generate_recommendations(progress_data):
    """Generate personalized learning recommendations"""
    recommendations = []
    
    accuracy = progress_data.get('accuracy', 0)
    
    if accuracy < 70:
        recommendations.append("📚 Review RTT Training Library scenarios")
        recommendations.append("🎯 Focus on Easy difficulty quizzes first")
        recommendations.append("⏰ Take time to read explanations carefully")
    elif accuracy < 85:
        recommendations.append("📈 Try Medium difficulty quizzes")
        recommendations.append("🎬 Watch video explanations")
        recommendations.append("🔄 Revisit questions you got wrong")
    else:
        recommendations.append("🏆 Challenge yourself with Expert level quizzes")
        recommendations.append("⚡ Try Timed Challenge Mode")
        recommendations.append("🎓 Ready for Certification Exam!")
    
    if progress_data.get('quizzes_completed', 0) < 20:
        recommendations.append("💪 Aim to complete at least 20 quizzes")
    
    return recommendations


def generate_validation_report(validation_history):
    """Generate validation performance report"""
    
    if not validation_history:
        return {
            'total_validations': 0,
            'accuracy_rate': 0,
            'common_errors': [],
            'trending': 'No data'
        }
    
    total = len(validation_history)
    correct = sum(1 for v in validation_history if v.get('correct', False))
    
    return {
        'total_validations': total,
        'correct_validations': correct,
        'accuracy_rate': round((correct / total) * 100, 1) if total > 0 else 0,
        'most_validated_codes': get_most_used_codes(validation_history),
        'error_patterns': identify_error_patterns(validation_history),
        'performance_trend': calculate_trend(validation_history)
    }


def get_most_used_codes(validation_history):
    """Get most frequently validated RTT codes"""
    code_count = {}
    
    for validation in validation_history:
        code = validation.get('code', 'Unknown')
        code_count[code] = code_count.get(code, 0) + 1
    
    # Sort by count
    sorted_codes = sorted(code_count.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_codes[:5]  # Top 5


def identify_error_patterns(validation_history):
    """Identify common error patterns"""
    errors = []
    
    for validation in validation_history:
        if not validation.get('correct', False):
            error_type = validation.get('error_type', 'Unknown error')
            errors.append(error_type)
    
    # Count frequency
    error_count = {}
    for error in errors:
        error_count[error] = error_count.get(error, 0) + 1
    
    # Get top 3 errors
    sorted_errors = sorted(error_count.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_errors[:3]


def calculate_trend(validation_history):
    """Calculate if performance is improving, declining, or stable"""
    
    if len(validation_history) < 10:
        return "Not enough data"
    
    # Split into first half and second half
    mid = len(validation_history) // 2
    first_half = validation_history[:mid]
    second_half = validation_history[mid:]
    
    first_accuracy = sum(1 for v in first_half if v.get('correct', False)) / len(first_half) * 100
    second_accuracy = sum(1 for v in second_half if v.get('correct', False)) / len(second_half) * 100
    
    if second_accuracy > first_accuracy + 5:
        return "📈 Improving"
    elif second_accuracy < first_accuracy - 5:
        return "📉 Declining"
    else:
        return "➡️ Stable"


def generate_csv_export(data, report_type):
    """Generate CSV export of data"""
    
    if report_type == 'student_progress':
        csv_content = "Metric,Value\n"
        csv_content += f"Total Points,{data['summary']['total_points']}\n"
        csv_content += f"Quizzes Completed,{data['summary']['quizzes_completed']}\n"
        csv_content += f"Accuracy,{data['summary']['accuracy']}%\n"
        csv_content += f"Best Streak,{data['summary']['best_streak']}\n"
        csv_content += f"Time Spent (hours),{data['summary']['time_spent_hours']}\n"
        
        return csv_content
    
    elif report_type == 'validation_history':
        csv_content = "Date,Code,Correct,Notes\n"
        for entry in data:
            date = entry.get('date', 'N/A')
            code = entry.get('code', 'N/A')
            correct = 'Yes' if entry.get('correct', False) else 'No'
            notes = entry.get('notes', '')
            csv_content += f"{date},{code},{correct},{notes}\n"
        
        return csv_content
    
    return ""


def format_report_for_print(report_data):
    """Format report for printing/PDF export"""
    
    report_text = f"""
====================================
T21 SERVICES - STUDENT PROGRESS REPORT
====================================

Student: {report_data['student_name']}
Report Date: {report_data['report_date']}

SUMMARY
-------
Total Points: {report_data['summary']['total_points']}
Quizzes Completed: {report_data['summary']['quizzes_completed']}
Accuracy: {report_data['summary']['accuracy']}%
Current Streak: {report_data['summary']['current_streak']}
Best Streak: {report_data['summary']['best_streak']}
Badges Earned: {report_data['summary']['badges_earned']}
Time Spent: {report_data['summary']['time_spent_hours']} hours

STRENGTHS
---------
"""
    
    for strength in report_data['strengths']:
        report_text += f"✓ {strength}\n"
    
    report_text += "\nAREAS FOR IMPROVEMENT\n"
    report_text += "---------------------\n"
    
    for weakness in report_data['areas_for_improvement']:
        report_text += f"→ {weakness}\n"
    
    report_text += "\nRECOMMENDATIONS\n"
    report_text += "---------------\n"
    
    for rec in report_data['recommendations']:
        report_text += f"{rec}\n"
    
    report_text += "\n====================================\n"
    report_text += "Generated by T21 Interactive Learning System\n"
    report_text += "====================================\n"
    
    return report_text


def render_interactive_reports():
    """Render interactive reports UI"""
    
    st.subheader("📊 Interactive Reports")
    
    st.info("""
    **🚧 Interactive Reports - Coming Soon!**
    
    This feature will include:
    - 📈 Student progress reports
    - 📊 Validation performance analytics
    - 📉 Trend analysis
    - 📄 Downloadable reports (PDF, CSV)
    - 📧 Automated email reports
    
    Currently in development. Check back soon!
    """)
    
    st.markdown("---")
    st.success("For now, please use the **Executive Dashboard** tab for real-time analytics.")
