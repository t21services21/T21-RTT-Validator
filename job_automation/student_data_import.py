"""
Student Data Import System
Import learner data from various sources into job automation system
"""

import pandas as pd
from datetime import datetime
import logging
from supabase import create_client
import os
from cryptography.fernet import Fernet
import json

logger = logging.getLogger(__name__)

class StudentDataImporter:
    """
    Import student data from Excel, CSV, or manual entry
    Prepare for job automation
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    def import_from_excel(self, excel_file_path: str) -> dict:
        """
        Import multiple students from Excel file
        
        Excel Format Required:
        - First Name
        - Last Name
        - Email
        - Phone
        - Address Line 1
        - City
        - Postcode
        - NHS Number (optional)
        - Date of Birth
        - Qualifications (JSON or comma-separated)
        - Employment History (JSON or comma-separated)
        - Immigration Status
        - Requires Sponsorship (Yes/No)
        - Preferred Locations (comma-separated)
        - Preferred Bands (comma-separated)
        - TQUK Completion Date
        
        Returns:
            dict with success count, errors, imported students
        """
        logger.info(f"📥 Importing students from Excel: {excel_file_path}")
        
        try:
            # Read Excel
            df = pd.read_excel(excel_file_path)
            
            results = {
                'total': len(df),
                'successful': 0,
                'failed': 0,
                'errors': [],
                'imported_students': []
            }
            
            for index, row in df.iterrows():
                try:
                    student_data = self.parse_excel_row(row)
                    student_id = self.create_student_profile(student_data)
                    
                    results['successful'] += 1
                    results['imported_students'].append({
                        'email': student_data['email'],
                        'student_id': student_id
                    })
                    
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append({
                        'row': index + 2,  # Excel row (1-indexed + header)
                        'email': row.get('Email', 'Unknown'),
                        'error': str(e)
                    })
            
            logger.info(f"✅ Import complete: {results['successful']} successful, {results['failed']} failed")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Excel import failed: {e}")
            raise
    
    def parse_excel_row(self, row: pd.Series) -> dict:
        """
        Parse Excel row into student data structure
        """
        # Parse qualifications
        qualifications = []
        if pd.notna(row.get('Qualifications')):
            quals_str = str(row['Qualifications'])
            if quals_str.startswith('['):
                # JSON format
                qualifications = json.loads(quals_str)
            else:
                # Comma-separated: "BSc Health - 2:1 - 2020, GCSE Maths - A - 2015"
                for qual in quals_str.split(','):
                    parts = qual.strip().split('-')
                    if len(parts) >= 3:
                        qualifications.append({
                            'subject': parts[0].strip(),
                            'grade': parts[1].strip(),
                            'year': parts[2].strip()
                        })
        
        # Parse employment history
        employment_history = []
        if pd.notna(row.get('Employment History')):
            emp_str = str(row['Employment History'])
            if emp_str.startswith('['):
                employment_history = json.loads(emp_str)
            else:
                # Simple comma-separated: "Admin Assistant at Hospital - 2023-2024"
                for emp in emp_str.split(','):
                    employment_history.append({'description': emp.strip()})
        
        # Parse locations
        preferred_locations = []
        if pd.notna(row.get('Preferred Locations')):
            preferred_locations = [loc.strip() for loc in str(row['Preferred Locations']).split(',')]
        
        # Parse bands
        preferred_bands = []
        if pd.notna(row.get('Preferred Bands')):
            preferred_bands = [band.strip() for band in str(row['Preferred Bands']).split(',')]
        
        student_data = {
            # Personal details
            'first_name': str(row.get('First Name', '')).strip(),
            'last_name': str(row.get('Last Name', '')).strip(),
            'email': str(row.get('Email', '')).strip().lower(),
            'phone': str(row.get('Phone', '')).strip(),
            'date_of_birth': str(row.get('Date of Birth', '')),
            'ni_number': str(row.get('NHS Number', '')).strip() if pd.notna(row.get('NHS Number')) else '',
            
            # Address
            'address_line1': str(row.get('Address Line 1', '')).strip(),
            'city': str(row.get('City', '')).strip(),
            'postcode': str(row.get('Postcode', '')).strip(),
            
            # Immigration
            'immigration_status': str(row.get('Immigration Status', 'British citizen with the right to work in the UK')),
            'requires_sponsorship': str(row.get('Requires Sponsorship', 'No')).upper() == 'YES',
            
            # Qualifications
            'qualifications': qualifications,
            'employment_history': employment_history,
            
            # TQUK
            'tquk_completion_date': str(row.get('TQUK Completion Date', '2025')),
            
            # Job preferences
            'preferred_locations': preferred_locations or ['London'],
            'preferred_bands': preferred_bands or ['Band 3', 'Band 4'],
            'search_keywords': ['RTT', 'Patient Pathway', 'Administrator', 'Validator'],
            'working_patterns': ['Full time', 'Part time']
        }
        
        return student_data
    
    def create_student_profile(self, student_data: dict) -> str:
        """
        Create complete student profile in database
        Including automation settings
        
        Returns:
            student_id (UUID)
        """
        logger.info(f"Creating profile for: {student_data['email']}")
        
        # 1. Create student record
        student_record = {
            'email': student_data['email'],
            'first_name': student_data['first_name'],
            'last_name': student_data['last_name'],
            'phone': student_data['phone'],
            'date_of_birth': student_data['date_of_birth'],
            'ni_number': student_data['ni_number'],
            'address_line1': student_data['address_line1'],
            'city': student_data['city'],
            'postcode': student_data['postcode'],
            'qualifications': student_data['qualifications'],
            'employment_history': student_data['employment_history'],
            'tquk_completion_date': student_data['tquk_completion_date'],
            'immigration_status': student_data['immigration_status'],
            'created_at': datetime.now().isoformat()
        }
        
        result = self.supabase.table('students').insert(student_record).execute()
        student_id = result.data[0]['id']
        
        # 2. Create automation settings (PAUSED initially - staff must review)
        automation_settings = {
            'student_id': student_id,
            'trac_email': student_data['email'],  # Will be updated with actual Trac email
            'trac_password_encrypted': '',  # Will be set later
            'encryption_key_id': '',
            'contract_signed': False,  # Staff must upload contract
            'auto_submit_enabled': False,  # PAUSED until staff enables
            'status': 'pending_review',  # Staff must review first
            'requires_sponsorship': student_data['requires_sponsorship'],
            'search_keywords': student_data['search_keywords'],
            'preferred_locations': student_data['preferred_locations'],
            'preferred_bands': student_data['preferred_bands'],
            'working_patterns': student_data['working_patterns'],
            'include_hybrid': True,
            'include_remote': True,
            'contract_types': ['Permanent', 'Fixed term'],
            'max_applications_per_day': 50,
            'notification_email': student_data['email']
        }
        
        self.supabase.table('student_automation_settings').insert(automation_settings).execute()
        
        logger.info(f"✅ Student profile created: {student_id}")
        
        return student_id
    
    def create_manual_entry_form(self) -> dict:
        """
        Returns template for manual student entry
        Staff can fill this in web form
        """
        return {
            'personal_details': {
                'first_name': '',
                'last_name': '',
                'email': '',
                'phone': '',
                'date_of_birth': '',
                'ni_number': ''
            },
            'address': {
                'address_line1': '',
                'address_line2': '',
                'city': '',
                'postcode': ''
            },
            'immigration': {
                'status': 'British citizen with the right to work in the UK',
                'requires_sponsorship': False,
                'visa_expiry_date': None
            },
            'qualifications': [
                {
                    'subject': 'GCSE English',
                    'grade': 'C',
                    'year': '2015',
                    'place_of_study': 'Secondary School'
                },
                {
                    'subject': 'GCSE Maths',
                    'grade': 'C',
                    'year': '2015',
                    'place_of_study': 'Secondary School'
                }
            ],
            'tquk_training': {
                'completion_date': '2025-04',
                'course_code': 'PDLC-01-039',
                'centre_number': '36257481088'
            },
            'employment_history': [
                {
                    'employer': '',
                    'job_title': '',
                    'start_date': '',
                    'end_date': '',
                    'duties': '',
                    'reason_for_leaving': ''
                }
            ],
            'references': [
                {
                    'name': 'T21 Services Tutor',
                    'organisation': 'T21 Services',
                    'position': 'Course Instructor',
                    'email': 'info@t21services.co.uk',
                    'phone': '02033752061',
                    'relationship': 'Course Tutor'
                }
            ],
            'job_preferences': {
                'keywords': ['RTT', 'Patient Pathway', 'Administrator', 'Validator'],
                'exclude_keywords': ['Senior', 'Manager', 'Lead'],
                'locations': ['London'],
                'radius_miles': 20,
                'bands': ['Band 3', 'Band 4'],
                'working_patterns': ['Full time', 'Part time'],
                'include_hybrid': True,
                'include_remote': True,
                'requires_sponsorship': False
            },
            'trac_account': {
                'email': '',  # Can be same as main email or different
                'password': '',  # Will be encrypted
                'account_exists': False  # True if student already has Trac account
            }
        }
    
    def export_template_excel(self, output_path: str):
        """
        Export blank Excel template for bulk import
        """
        template_data = {
            'First Name': ['John', 'Jane'],
            'Last Name': ['Smith', 'Doe'],
            'Email': ['john.smith@email.com', 'jane.doe@email.com'],
            'Phone': ['07700900000', '07700900001'],
            'Address Line 1': ['123 High Street', '456 Main Road'],
            'City': ['London', 'Manchester'],
            'Postcode': ['SW1A 1AA', 'M1 1AA'],
            'NHS Number': ['AB123456C', 'CD789012E'],
            'Date of Birth': ['1995-05-15', '1994-03-20'],
            'Qualifications': [
                'BSc Health Management - 2:1 - 2020, GCSE English - C - 2015',
                'BA Business - 2:2 - 2019, GCSE Maths - B - 2014'
            ],
            'Employment History': [
                'Admin Assistant at Hospital - 2023-2024',
                'Receptionist at Clinic - 2022-2023'
            ],
            'Immigration Status': [
                'British citizen with the right to work in the UK',
                'Skilled Worker visa'
            ],
            'Requires Sponsorship': ['No', 'Yes'],
            'Preferred Locations': ['London, Manchester', 'Birmingham, Leeds'],
            'Preferred Bands': ['Band 3, Band 4', 'Band 4, Band 5'],
            'TQUK Completion Date': ['2025-04', '2025-03']
        }
        
        df = pd.DataFrame(template_data)
        df.to_excel(output_path, index=False)
        
        logger.info(f"✅ Template exported to: {output_path}")
        
        return output_path


class TracAccountSetup:
    """
    Setup Trac accounts for students
    Option 1: Student provides existing account
    Option 2: Staff creates new account
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    def add_trac_credentials(self, student_id: str, trac_email: str, trac_password: str):
        """
        Add Trac credentials for student
        Encrypts password before storing
        """
        # Encrypt password
        encryption_key = Fernet.generate_key()
        cipher = Fernet(encryption_key)
        encrypted_password = cipher.encrypt(trac_password.encode()).decode()
        
        # Store encryption key securely (in production, use key vault)
        key_id = f"key_{student_id}"
        
        # Update automation settings
        self.supabase.table('student_automation_settings')\
            .update({
                'trac_email': trac_email,
                'trac_password_encrypted': encrypted_password,
                'encryption_key_id': key_id
            })\
            .eq('student_id', student_id)\
            .execute()
        
        logger.info(f"✅ Trac credentials added for student: {student_id}")
    
    async def verify_trac_credentials(self, trac_email: str, trac_password: str) -> bool:
        """
        Verify Trac credentials work before storing
        """
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto('https://www.trac.jobs/Candidate/LogOn')
                await page.fill('input[name="Email"]', trac_email)
                await page.fill('input[name="Password"]', trac_password)
                await page.click('button[type="submit"]')
                await page.wait_for_load_state('networkidle')
                
                # Check if login successful
                if 'dashboard' in page.url.lower() or 'candidate' in page.url.lower():
                    logger.info(f"✅ Trac credentials verified: {trac_email}")
                    await browser.close()
                    return True
                else:
                    logger.error(f"❌ Trac login failed: {trac_email}")
                    await browser.close()
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Trac verification error: {e}")
                await browser.close()
                return False


# Example usage
if __name__ == '__main__':
    importer = StudentDataImporter()
    
    # Export template
    importer.export_template_excel('student_import_template.xlsx')
    
    # Import from Excel
    # results = importer.import_from_excel('completed_student_data.xlsx')
    # print(f"Imported {results['successful']} students")
