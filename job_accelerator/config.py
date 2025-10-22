"""
T21 JOB ACCELERATOR - Configuration
Central configuration for the entire job application system
"""

import os
from datetime import timedelta

# ============================================
# ENVIRONMENT & DEPLOYMENT
# ============================================

ENV = os.getenv('ENVIRONMENT', 'development')  # development, staging, production
DEBUG = ENV == 'development'

# ============================================
# DATABASE (Supabase)
# ============================================

DATABASE_CONFIG = {
    'url': os.getenv('SUPABASE_URL', 'your-project-url.supabase.co'),
    'key': os.getenv('SUPABASE_KEY', 'your-anon-key'),
    'service_key': os.getenv('SUPABASE_SERVICE_KEY', 'your-service-key')
}

# ============================================
# AI SERVICES (OpenAI)
# ============================================

OPENAI_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY', ''),
    'model': 'gpt-4-turbo-preview',  # Best model for quality
    'backup_model': 'gpt-3.5-turbo',  # Fallback if GPT-4 fails
    'temperature': 0.7,
    'max_tokens': 2000
}

# ============================================
# EMAIL (SendGrid)
# ============================================

EMAIL_CONFIG = {
    'api_key': os.getenv('SENDGRID_API_KEY', ''),
    'from_email': 'jobaccelerator@t21services.co.uk',
    'from_name': 'T21 Job Accelerator',
    'reply_to': 'support@t21services.co.uk'
}

# ============================================
# JOB BOARDS CONFIGURATION
# ============================================

JOB_BOARDS = {
    'nhs_jobs': {
        'name': 'NHS Jobs',
        'enabled': True,
        'priority': 100,  # Highest priority (our specialty!)
        'base_url': 'https://beta.jobs.nhs.uk',
        'search_url': 'https://beta.jobs.nhs.uk/candidate/search/results',
        'requires_login': False,
        'rate_limit': {
            'requests_per_minute': 20,
            'delay_ms': 3000
        },
        'scrape_config': {
            'frequency_minutes': 30,  # Check every 30 minutes
            'max_results': 100,
            'keywords': ['RTT', 'Validator', 'Waiting List', 'Hospital Administrator', 'Medical Secretary', 'Outpatients', 'Access Coordinator']
        }
    },
    
    'indeed': {
        'name': 'Indeed UK',
        'enabled': True,
        'priority': 90,
        'base_url': 'https://uk.indeed.com',
        'search_url': 'https://uk.indeed.com/jobs',
        'requires_login': False,
        'rate_limit': {
            'requests_per_minute': 15,
            'delay_ms': 4000
        },
        'scrape_config': {
            'frequency_minutes': 60,
            'max_results': 200,
            'keywords': ['NHS RTT', 'Hospital Administrator', 'Medical Secretary', 'Healthcare Admin']
        }
    },
    
    'reed': {
        'name': 'Reed',
        'enabled': True,
        'priority': 80,
        'base_url': 'https://www.reed.co.uk',
        'search_url': 'https://www.reed.co.uk/jobs',
        'requires_login': False,
        'rate_limit': {
            'requests_per_minute': 15,
            'delay_ms': 4000
        },
        'scrape_config': {
            'frequency_minutes': 60,
            'max_results': 150,
            'keywords': ['NHS', 'Hospital', 'Healthcare Administration']
        }
    },
    
    'linkedin': {
        'name': 'LinkedIn',
        'enabled': True,
        'priority': 70,
        'base_url': 'https://www.linkedin.com',
        'search_url': 'https://www.linkedin.com/jobs/search',
        'requires_login': True,  # LinkedIn Easy Apply requires login
        'rate_limit': {
            'requests_per_minute': 10,
            'delay_ms': 6000
        },
        'scrape_config': {
            'frequency_minutes': 120,
            'max_results': 100,
            'keywords': ['RTT Validator', 'NHS Administrator', 'Healthcare']
        }
    },
    
    'cv_library': {
        'name': 'CV Library',
        'enabled': True,
        'priority': 60,
        'base_url': 'https://www.cv-library.co.uk',
        'search_url': 'https://www.cv-library.co.uk/search-jobs',
        'requires_login': False,
        'rate_limit': {
            'requests_per_minute': 15,
            'delay_ms': 4000
        },
        'scrape_config': {
            'frequency_minutes': 90,
            'max_results': 100,
            'keywords': ['NHS', 'Hospital', 'Healthcare']
        }
    }
}

# ============================================
# AUTOMATION SETTINGS
# ============================================

AUTOMATION_CONFIG = {
    # Application Limits
    'max_applications_per_student_per_day': 50,
    'max_applications_per_job_board_per_day': 20,
    'min_delay_between_applications_seconds': 60,
    
    # Timing
    'application_hours': {
        'start': 8,  # 8 AM
        'end': 18    # 6 PM (don't apply late at night - looks automated!)
    },
    'application_days': [0, 1, 2, 3, 4],  # Monday to Friday only
    
    # Quality Controls
    'min_match_score_to_auto_apply': 60,  # Only auto-apply if 60%+ match
    'require_approval_threshold': 40,  # Require staff approval if <40% match
    
    # Follow-ups
    'follow_up_after_days': 7,
    'max_follow_ups_per_application': 2,
    
    # Success Prediction
    'min_predicted_success_rate': 10,  # Only apply if >10% predicted interview chance
}

# ============================================
# AI PROMPTS (For CV/Cover Letter Generation)
# ============================================

AI_PROMPTS = {
    'cv_tailor': """
You are an expert CV writer specializing in NHS and healthcare roles.

Given the following:
- Job Title: {job_title}
- Company: {company}
- Job Description: {job_description}
- Student Profile: {student_profile}
- TQUK Certification: {tquk_certification}

Create a tailored CV that:
1. Emphasizes TQUK Approved Centre #36257481088 certification
2. Highlights relevant skills for THIS specific job
3. Uses NHS terminology and keywords from job description
4. Demonstrates understanding of RTT pathways (if relevant)
5. Shows professionalism and attention to detail
6. Is ATS-friendly (uses keywords from job description)

Format as professional CV text (not markdown).
Keep it concise (1-2 pages equivalent).
""",

    'cover_letter': """
You are an expert in writing compelling NHS job application cover letters.

Given the following:
- Job Title: {job_title}
- Company: {company}
- Job Description: {job_description}
- Student Name: {student_name}
- Student Profile: {student_profile}
- TQUK Certification: {tquk_certification}

Write a professional cover letter (250-300 words) that:
1. Shows genuine enthusiasm for the role and NHS
2. Highlights TQUK training and certification
3. Addresses specific requirements from job description
4. Demonstrates understanding of the role
5. Shows personality while remaining professional
6. Ends with clear call to action

Use professional UK business letter format.
Do NOT use overly formal or robotic language.
Make it personal and authentic.
""",

    'job_match_score': """
Analyze how well this student matches this job.

Student Profile:
{student_profile}

Job Requirements:
{job_description}

Provide a match score (0-100) and brief explanation.
Consider:
- TQUK certification relevance
- Skills match
- Experience requirements
- Location preferences
- Employment type match

Return JSON: {{"score": <0-100>, "reasoning": "<brief explanation>", "missing_requirements": ["requirement1", "requirement2"]}}
""",

    'interview_prediction': """
Based on historical data and this application, predict likelihood of getting an interview.

Student Profile: {student_profile}
Job: {job_title} at {company}
Job Board: {job_board}
Match Score: {match_score}
Historical Success Rate for similar applications: {historical_success_rate}%

Provide prediction (0-100%) and confidence level.
Return JSON: {{"interview_probability": <0-100>, "confidence": "<low|medium|high>", "key_factors": ["factor1", "factor2"]}}
"""
}

# ============================================
# TQUK INTEGRATION
# ============================================

TQUK_CONFIG = {
    'centre_number': '36257481088',
    'course_code': 'PDLC-01-039',
    'course_name': 'Proficient Professional Development Learning Course in Understanding RTT and Hospital Administration',
    'verification_url': 'https://t21-healthcare-platform.streamlit.app',
    
    'certification_levels': {
        'foundation': {
            'name': 'RTT Foundation Certificate',
            'min_score': 70,
            'description': 'Demonstrates foundational understanding of RTT pathways'
        },
        'practitioner': {
            'name': 'RTT Practitioner Certificate',
            'min_score': 80,
            'description': 'Demonstrates practical competence in RTT validation'
        },
        'expert': {
            'name': 'RTT Expert Certificate',
            'min_score': 90,
            'description': 'Demonstrates expert-level RTT knowledge and skills'
        }
    }
}

# ============================================
# SCRAPING CONFIGURATION
# ============================================

SCRAPING_CONFIG = {
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ],
    
    'headless': ENV == 'production',  # Show browser in development for debugging
    'timeout': 30000,  # 30 seconds
    'retry_attempts': 3,
    'retry_delay_seconds': 5,
    
    # Anti-detection
    'use_stealth': True,
    'randomize_user_agent': True,
    'respect_robots_txt': True,
}

# ============================================
# LOGGING
# ============================================

LOGGING_CONFIG = {
    'level': 'DEBUG' if DEBUG else 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/job_accelerator.log',
    'max_bytes': 10485760,  # 10MB
    'backup_count': 5
}

# ============================================
# ANALYTICS
# ============================================

ANALYTICS_CONFIG = {
    'track_events': True,
    'retention_days': 365,
    
    'key_metrics': [
        'applications_submitted',
        'response_rate',
        'interview_rate',
        'placement_rate',
        'time_to_placement',
        'board_performance',
        'student_satisfaction'
    ]
}

# ============================================
# FEATURE FLAGS
# ============================================

FEATURES = {
    'ai_cv_tailoring': True,
    'ai_cover_letters': True,
    'ai_job_matching': True,
    'ai_interview_prediction': True,
    'auto_follow_ups': True,
    'linkedin_integration': False,  # Phase 2
    'employer_relationship_management': False,  # Phase 2
    'success_guarantee_tracking': True,
}

# ============================================
# BUSINESS SETTINGS
# ============================================

BUSINESS_CONFIG = {
    'success_guarantee_days': 90,  # Job within 90 days or refund
    'target_response_rate': 15,  # % (industry average is 3-5%)
    'target_interview_rate': 25,  # % (industry average is 5-10%)
    'target_placement_rate': 50,  # % within 90 days
    
    'pricing': {
        'included_in_training': True,
        'standalone_monthly': 59,
        'success_fee': 500,
        
        # For reselling to other providers
        'saas_monthly': 500,
        'white_label_annual': 5000,
    }
}

# ============================================
# NOTIFICATIONS
# ============================================

NOTIFICATION_CONFIG = {
    'email_templates': {
        'application_submitted': {
            'subject': '✅ Application Submitted: {job_title}',
            'enabled': True
        },
        'response_received': {
            'subject': '🎉 Response Received: {job_title}',
            'enabled': True
        },
        'interview_scheduled': {
            'subject': '📅 Interview Scheduled: {job_title}',
            'enabled': True
        },
        'daily_summary': {
            'subject': '📊 Daily Application Summary',
            'enabled': True,
            'send_time': '18:00'
        }
    },
    
    'sms_enabled': False,  # Phase 2
    'whatsapp_enabled': False,  # Phase 2
}

# ============================================
# SECURITY
# ============================================

SECURITY_CONFIG = {
    'encrypt_student_data': True,
    'gdpr_compliant': True,
    'data_retention_days': 365,
    'require_2fa_for_staff': True,
    'session_timeout_minutes': 60,
    'max_login_attempts': 5,
}

# ============================================
# SYSTEM HEALTH
# ============================================

HEALTH_CHECK_CONFIG = {
    'check_interval_minutes': 5,
    'alert_on_failure': True,
    'alert_email': 'admin@t21services.co.uk',
    
    'checks': [
        'database_connection',
        'openai_api',
        'sendgrid_api',
        'disk_space',
        'memory_usage',
        'scraper_status'
    ]
}

# ============================================
# DEVELOPMENT HELPERS
# ============================================

if DEBUG:
    # More verbose logging in development
    LOGGING_CONFIG['level'] = 'DEBUG'
    
    # Slower rate limits for development
    for board in JOB_BOARDS.values():
        board['rate_limit']['delay_ms'] *= 2
    
    # Lower application limits for testing
    AUTOMATION_CONFIG['max_applications_per_student_per_day'] = 10

# ============================================
# VALIDATION
# ============================================

def validate_config():
    """Validate that all required configuration is present"""
    errors = []
    
    if not OPENAI_CONFIG['api_key']:
        errors.append("OPENAI_API_KEY not set")
    
    if not EMAIL_CONFIG['api_key']:
        errors.append("SENDGRID_API_KEY not set")
    
    if not DATABASE_CONFIG['url'] or 'your-project-url' in DATABASE_CONFIG['url']:
        errors.append("SUPABASE_URL not configured")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True

# ============================================
# EXPORT
# ============================================

__all__ = [
    'ENV',
    'DEBUG',
    'DATABASE_CONFIG',
    'OPENAI_CONFIG',
    'EMAIL_CONFIG',
    'JOB_BOARDS',
    'AUTOMATION_CONFIG',
    'AI_PROMPTS',
    'TQUK_CONFIG',
    'SCRAPING_CONFIG',
    'LOGGING_CONFIG',
    'ANALYTICS_CONFIG',
    'FEATURES',
    'BUSINESS_CONFIG',
    'NOTIFICATION_CONFIG',
    'SECURITY_CONFIG',
    'HEALTH_CHECK_CONFIG',
    'validate_config'
]
