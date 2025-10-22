"""
Add test NHS jobs to database for testing the automation
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase_database import supabase, SUPABASE_AVAILABLE

def add_test_jobs():
    """Add test NHS jobs to database"""
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return
    
    # Test jobs matching student criteria (London, Band 3-4)
    test_jobs = [
        {
            'title': 'RTT Validation Officer',
            'trust': 'Royal London Hospital',
            'location': 'London',
            'band': 'Band 3',
            'salary_min': 24000,
            'salary_max': 28000,
            'requires_sponsorship': False,
            'sponsorship_available': True,
            'closing_date': (datetime.now() + timedelta(days=14)).isoformat(),
            'nhs_jobs_url': 'https://www.jobs.nhs.uk/example-1',
            'job_reference': 'TEST-RTT-001',
            'description': 'We are looking for an enthusiastic RTT Validation Officer to join our team. You will be responsible for validating patient pathways and ensuring compliance with 18-week RTT standards.',
            'discovered_at': datetime.now().isoformat()
        },
        {
            'title': 'Patient Pathway Coordinator',
            'trust': "Guy's and St Thomas' NHS Foundation Trust",
            'location': 'London',
            'band': 'Band 4',
            'salary_min': 28000,
            'salary_max': 32000,
            'requires_sponsorship': False,
            'sponsorship_available': True,
            'closing_date': (datetime.now() + timedelta(days=10)).isoformat(),
            'nhs_jobs_url': 'https://www.jobs.nhs.uk/example-2',
            'job_reference': 'TEST-PATH-002',
            'description': 'Join our team as a Patient Pathway Coordinator. You will manage patient pathways from referral to treatment, ensuring timely care delivery.',
            'discovered_at': datetime.now().isoformat()
        },
        {
            'title': 'NHS Administrator - RTT',
            'trust': 'King\'s College Hospital NHS Foundation Trust',
            'location': 'London',
            'band': 'Band 3',
            'salary_min': 24000,
            'salary_max': 27000,
            'requires_sponsorship': False,
            'sponsorship_available': True,
            'closing_date': (datetime.now() + timedelta(days=7)).isoformat(),
            'nhs_jobs_url': 'https://www.jobs.nhs.uk/example-3',
            'job_reference': 'TEST-ADMIN-003',
            'description': 'We need an NHS Administrator with knowledge of RTT pathways. You will support the booking team and validate patient pathway data.',
            'discovered_at': datetime.now().isoformat()
        },
        {
            'title': 'Outpatient Booking Administrator',
            'trust': 'St Thomas\' Hospital',
            'location': 'London',
            'band': 'Band 3',
            'salary_min': 23500,
            'salary_max': 26500,
            'requires_sponsorship': False,
            'sponsorship_available': True,
            'closing_date': (datetime.now() + timedelta(days=12)).isoformat(),
            'nhs_jobs_url': 'https://www.jobs.nhs.uk/example-4',
            'job_reference': 'TEST-BOOK-004',
            'description': 'Join our busy outpatient booking team. Experience with NHS systems and understanding of RTT principles is essential.',
            'discovered_at': datetime.now().isoformat()
        },
        {
            'title': 'Referral Management Coordinator',
            'trust': 'University College London Hospitals',
            'location': 'London',
            'band': 'Band 4',
            'salary_min': 28500,
            'salary_max': 31500,
            'requires_sponsorship': False,
            'sponsorship_available': True,
            'closing_date': (datetime.now() + timedelta(days=9)).isoformat(),
            'nhs_jobs_url': 'https://www.jobs.nhs.uk/example-5',
            'job_reference': 'TEST-REF-005',
            'description': 'Coordinate referral management processes across the trust. Knowledge of RTT pathways and patient tracking systems required.',
            'discovered_at': datetime.now().isoformat()
        }
    ]
    
    print("=" * 60)
    print("ADDING TEST NHS JOBS TO DATABASE")
    print("=" * 60)
    
    added_count = 0
    
    for job in test_jobs:
        try:
            # Check if job already exists
            existing = supabase.table('discovered_jobs').select('id').eq('job_reference', job['job_reference']).execute()
            
            if existing.data:
                print(f"⏭️  Skip: {job['title']} (already exists)")
            else:
                # Add job
                result = supabase.table('discovered_jobs').insert(job).execute()
                if result.data:
                    added_count += 1
                    print(f"✅ Added: {job['title']} at {job['trust']}")
        
        except Exception as e:
            print(f"❌ Error adding {job['title']}: {str(e)}")
    
    print("=" * 60)
    print(f"✅ Complete! Added {added_count} test jobs")
    print("=" * 60)
    print()
    print("Now go back to Manual Runner and click 'RUN AI GENERATOR'")
    print("This will create applications for these jobs!")

if __name__ == "__main__":
    add_test_jobs()
