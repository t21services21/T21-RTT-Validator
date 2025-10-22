"""
NHS Job Automation System
Complete automation for NHS job applications
"""

from .nhs_jobs_scraper import scrape_jobs_for_all_students, scrape_nhs_jobs
from .ai_application_generator import generate_applications_for_all_students, create_applications_for_student
from .run_automation_cycle import run_full_automation_cycle, quick_test

__all__ = [
    'scrape_jobs_for_all_students',
    'scrape_nhs_jobs',
    'generate_applications_for_all_students',
    'create_applications_for_student',
    'run_full_automation_cycle',
    'quick_test'
]

__version__ = '1.0.0'
