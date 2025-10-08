"""
T21 CERTIFICATION EXAM SYSTEM
Official RTT Certification with Downloadable Certificate

Features:
- 50-question final exam
- 80% pass mark required
- Timed exam (90 minutes)
- Official T21 certificate (PDF)
- Unique verification code
- Employer verification portal
"""

from datetime import datetime
import random
import hashlib

# CERTIFICATION EXAM QUESTIONS (50 questions)
CERTIFICATION_QUESTIONS = [
    {
        "id": "cert_1",
        "question": "What is the RTT standard target?",
        "options": ["16 weeks", "18 weeks", "20 weeks", "26 weeks"],
        "correct": "18 weeks",
        "points": 2
    },
    {
        "id": "cert_2",
        "question": "Code 10 is used for:",
        "options": ["GP Referral", "Treatment", "Discharge", "DNA"],
        "correct": "GP Referral",
        "points": 2
    },
    {
        "id": "cert_3",
        "question": "Code 30 represents:",
        "options": ["Referral", "Decision to Treat", "First Definitive Treatment", "Discharge"],
        "correct": "First Definitive Treatment",
        "points": 2
    },
    {
        "id": "cert_4",
        "question": "Patient DNA = Code:",
        "options": ["31", "33", "35", "39"],
        "correct": "33",
        "points": 2
    },
    {
        "id": "cert_5",
        "question": "Active Monitoring code:",
        "options": ["30", "31", "32", "35"],
        "correct": "32",
        "points": 2
    },
    # Add 45 more questions here...
    {
        "id": "cert_6",
        "question": "2WW referral must be seen within:",
        "options": ["7 days", "14 days", "21 days", "28 days"],
        "correct": "14 days",
        "points": 2
    },
    {
        "id": "cert_7",
        "question": "Cancer treatment 62-day target starts from:",
        "options": ["GP referral", "First appointment", "Diagnosis", "MDT decision"],
        "correct": "GP referral",
        "points": 2
    },
    {
        "id": "cert_8",
        "question": "Patient declines treatment = Code:",
        "options": ["31", "34", "35", "36"],
        "correct": "35",
        "points": 2
    },
    {
        "id": "cert_9",
        "question": "Discharge without treatment = Code:",
        "options": ["30", "31", "33", "34"],
        "correct": "34",
        "points": 2
    },
    {
        "id": "cert_10",
        "question": "Tertiary referral = Code:",
        "options": ["20", "21", "30", "36"],
        "correct": "21",
        "points": 2
    }
]


def generate_exam(randomize=True):
    """Generate certification exam (50 questions)"""
    
    # For full certification, you'd have all 50 questions
    # This is a sample with 10 - expand to 50 for production
    
    exam_questions = CERTIFICATION_QUESTIONS.copy()
    
    if randomize:
        random.shuffle(exam_questions)
    
    return {
        'exam_id': generate_exam_id(),
        'questions': exam_questions,
        'total_questions': len(exam_questions),
        'pass_mark': 80,  # 80% required
        'time_limit_minutes': 90,
        'started_at': datetime.now()
    }


def generate_exam_id():
    """Generate unique exam ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = random.randint(1000, 9999)
    return f"T21-EXAM-{timestamp}-{random_suffix}"


def grade_exam(exam_data, answers):
    """Grade certification exam"""
    
    total_questions = len(exam_data['questions'])
    correct_count = 0
    
    results = []
    
    for idx, question in enumerate(exam_data['questions']):
        user_answer = answers.get(question['id'], '')
        correct = user_answer == question['correct']
        
        if correct:
            correct_count += 1
        
        results.append({
            'question_id': question['id'],
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': question['correct'],
            'correct': correct
        })
    
    score_percentage = (correct_count / total_questions) * 100
    passed = score_percentage >= exam_data['pass_mark']
    
    return {
        'exam_id': exam_data['exam_id'],
        'total_questions': total_questions,
        'correct_answers': correct_count,
        'score_percentage': round(score_percentage, 1),
        'pass_mark': exam_data['pass_mark'],
        'passed': passed,
        'results': results,
        'completed_at': datetime.now()
    }


def generate_certificate(student_name, exam_result):
    """Generate certification certificate data"""
    
    if not exam_result['passed']:
        return None
    
    verification_code = generate_verification_code(student_name, exam_result['exam_id'])
    
    certificate = {
        'student_name': student_name,
        'certification_title': 'RTT Pathway Management Professional',
        'issuing_organization': 'T21 Services UK',
        'exam_id': exam_result['exam_id'],
        'score': exam_result['score_percentage'],
        'date_issued': datetime.now().strftime('%d/%m/%Y'),
        'verification_code': verification_code,
        'valid_until': calculate_expiry_date(),
        'certificate_number': generate_certificate_number()
    }
    
    return certificate


def generate_verification_code(student_name, exam_id):
    """Generate unique verification code"""
    
    data_string = f"{student_name}{exam_id}{datetime.now().strftime('%Y%m%d')}"
    hash_object = hashlib.sha256(data_string.encode())
    hash_hex = hash_object.hexdigest()
    
    # Take first 12 characters and format
    code = hash_hex[:12].upper()
    formatted_code = f"{code[:4]}-{code[4:8]}-{code[8:12]}"
    
    return formatted_code


def calculate_expiry_date():
    """Calculate certificate expiry (2 years from issue)"""
    from datetime import timedelta
    expiry = datetime.now() + timedelta(days=730)  # 2 years
    return expiry.strftime('%d/%m/%Y')


def generate_certificate_number():
    """Generate unique certificate number"""
    timestamp = datetime.now().strftime('%Y%m')
    random_num = random.randint(10000, 99999)
    return f"T21-CERT-{timestamp}-{random_num}"


def verify_certificate(verification_code):
    """Verify if certificate is valid (for employer portal)"""
    
    # In production, this would check against a database
    # For now, just validate format
    
    if len(verification_code) == 14 and verification_code.count('-') == 2:
        return {
            'valid': True,
            'message': 'Certificate is valid',
            'details': 'Check with T21 Services for full verification'
        }
    
    return {
        'valid': False,
        'message': 'Invalid verification code format'
    }


def format_certificate_html(certificate_data):
    """Format certificate as printable HTML"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4 landscape;
            margin: 0;
        }}
        body {{
            font-family: 'Georgia', serif;
            margin: 0;
            padding: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .certificate {{
            background: white;
            padding: 60px;
            border: 20px solid #FFD700;
            box-shadow: 0 0 40px rgba(0,0,0,0.3);
            text-align: center;
        }}
        .title {{
            font-size: 48px;
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 3px;
        }}
        .subtitle {{
            font-size: 24px;
            color: #7f8c8d;
            margin-bottom: 40px;
        }}
        .student {{
            font-size: 42px;
            color: #005EB8;
            margin: 40px 0;
            font-weight: bold;
            border-bottom: 3px solid #005EB8;
            padding-bottom: 20px;
        }}
        .description {{
            font-size: 20px;
            color: #34495e;
            margin: 30px 0;
            line-height: 1.8;
        }}
        .score {{
            font-size: 32px;
            color: #27ae60;
            margin: 30px 0;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .signature {{
            border-top: 2px solid #000;
            padding-top: 10px;
            font-size: 16px;
        }}
        .verification {{
            font-size: 14px;
            color: #7f8c8d;
        }}
        .seal {{
            width: 120px;
            height: 120px;
            border: 5px solid #FFD700;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #005EB8;
            color: white;
            font-weight: bold;
            font-size: 18px;
            margin: 0 auto 20px;
        }}
    </style>
</head>
<body>
    <div class="certificate">
        <div class="seal">T21<br/>CERTIFIED</div>
        
        <div class="title">Certificate of Achievement</div>
        <div class="subtitle">RTT Pathway Management Professional</div>
        
        <div class="description">This is to certify that</div>
        
        <div class="student">{certificate_data['student_name']}</div>
        
        <div class="description">
            has successfully completed the comprehensive RTT Pathway Management
            certification exam and has demonstrated exceptional understanding of
            NHS RTT standards, pathway validation, and clinical administration.
        </div>
        
        <div class="score">Final Score: {certificate_data['score']}%</div>
        
        <div class="footer">
            <div class="signature">
                <strong>T21 Services UK</strong><br/>
                Accredited Training Provider<br/>
                Date: {certificate_data['date_issued']}
            </div>
            
            <div class="verification">
                <strong>Certificate Number:</strong> {certificate_data['certificate_number']}<br/>
                <strong>Verification Code:</strong> {certificate_data['verification_code']}<br/>
                <strong>Valid Until:</strong> {certificate_data['valid_until']}<br/>
                <small>Verify at: www.t21services.uk/verify</small>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def get_exam_statistics(all_exam_results):
    """Get statistics on exam performance"""
    
    if not all_exam_results:
        return {}
    
    total_exams = len(all_exam_results)
    passed_exams = sum(1 for r in all_exam_results if r['passed'])
    
    average_score = sum(r['score_percentage'] for r in all_exam_results) / total_exams
    
    return {
        'total_exams_taken': total_exams,
        'passed': passed_exams,
        'failed': total_exams - passed_exams,
        'pass_rate': round((passed_exams / total_exams) * 100, 1),
        'average_score': round(average_score, 1)
    }
