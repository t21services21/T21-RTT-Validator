"""
Trac Auto-Submitter
Automatically fills and submits NHS job applications via Trac
NO per-application approval - uses contract-based permission
"""

import asyncio
from playwright.async_api import async_playwright, Page
from datetime import datetime
import logging
from supabase import create_client
import os
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class TracAutoSubmitter:
    """
    Automatically submits NHS job applications through Trac system
    Contract-based approval - no confirmation needed per application
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        self.trac_url = 'https://www.trac.jobs'
    
    async def submit_application(self, application_id: str) -> dict:
        """
        Submit a single application
        
        Args:
            application_id: UUID of application in database
        
        Returns:
            dict with confirmation_number, trac_url, success
        """
        logger.info(f"📝 Starting auto-submission for application: {application_id}")
        
        # Get application data
        app = self.supabase.table('applications')\
            .select('*, student:student_id(*), job:job_id(*)')\
            .eq('id', application_id)\
            .single()\
            .execute()
        
        if not app.data:
            raise Exception(f"Application {application_id} not found")
        
        application = app.data
        student = application['student']
        job = application['job']
        
        # Get student automation settings (with Trac credentials)
        settings = self.supabase.table('student_automation_settings')\
            .select('*')\
            .eq('student_id', student['id'])\
            .single()\
            .execute()
        
        if not settings.data:
            raise Exception(f"No automation settings for student {student['id']}")
        
        creds = settings.data
        
        # Check contract approval
        if not creds.get('contract_signed'):
            raise Exception("No signed contract - cannot auto-submit")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Login to Trac
                await self.login_to_trac(page, creds)
                
                # Navigate to job application
                await page.goto(job['trac_apply_url'])
                await page.wait_for_load_state('networkidle')
                
                # Fill all form sections
                await self.fill_application_form(page, application, student)
                
                # Submit
                confirmation = await self.submit_form(page)
                
                logger.info(f"✅ Application submitted successfully!")
                
                return {
                    'success': True,
                    'confirmation_number': confirmation['reference'],
                    'trac_url': confirmation['url'],
                    'submitted_at': datetime.now().isoformat()
                }
                
            except Exception as e:
                logger.error(f"❌ Submission failed: {e}")
                raise
            finally:
                await browser.close()
    
    async def login_to_trac(self, page: Page, creds: dict):
        """Login to Trac"""
        password = self.decrypt_password(creds['trac_password_encrypted'])
        
        await page.goto(f'{self.trac_url}/Candidate/LogOn')
        await page.fill('input[name="Email"]', creds['trac_email'])
        await page.fill('input[name="Password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')
        
        # Handle OTP if present
        if 'otp' in page.url.lower():
            logger.warning("⚠️ OTP required - implement OTP automation")
            # TODO: Implement automatic OTP handling via email
            await page.wait_for_timeout(60000)
    
    async def fill_application_form(self, page: Page, application: dict, student: dict):
        """
        Fill complete Trac application form
        Handles all sections adaptively
        """
        app_data = application['application_data']
        
        logger.info("📝 Filling application form sections...")
        
        # 1. Personal Details
        await self.fill_personal_details(page, student, app_data)
        
        # 2. Pre-screening questions
        await self.fill_prescreening(page, app_data)
        
        # 3. Education & Qualifications
        await self.fill_qualifications(page, student)
        
        # 4. Training Courses
        await self.fill_training_courses(page, student)
        
        # 5. Employment History
        await self.fill_employment_history(page, student)
        
        # 6. Supporting Information (AI-GENERATED!)
        await self.fill_supporting_information(page, application['ai_supporting_information'])
        
        # 7. References
        await self.fill_references(page, student)
        
        # 8. Equal Opportunities
        await self.fill_equal_opportunities(page, student)
        
        # 9. Declaration
        await self.fill_declaration(page)
        
        logger.info("✅ All form sections filled")
    
    async def fill_personal_details(self, page: Page, student: dict, app_data: dict):
        """Fill personal details section"""
        logger.info("Filling personal details...")
        
        await self.click_section(page, "Personal details")
        
        # Title
        await page.select_option('select[name*="title"]', student.get('title', 'Mr'))
        
        # Names
        await page.fill('input[name*="forename"]', student.get('first_name', ''))
        await page.fill('input[name*="surname"]', student.get('last_name', ''))
        
        # Address
        await page.fill('input[name*="address"]', student.get('address_line1', ''))
        await page.fill('input[name*="city"]', student.get('city', ''))
        await page.fill('input[name*="postcode"]', student.get('postcode', ''))
        
        # Contact
        await page.fill('input[name*="mobile"]', student.get('phone', ''))
        await page.fill('input[name*="email"]', student.get('email', ''))
        
        # Working patterns
        for pattern in app_data.get('working_patterns', ['Full time']):
            checkbox = page.locator(f'input[type="checkbox"][value*="{pattern}"]')
            if await checkbox.count() > 0:
                await checkbox.check()
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_prescreening(self, page: Page, app_data: dict):
        """Fill pre-screening questions"""
        logger.info("Filling pre-screening...")
        
        await self.click_section(page, "Pre-screening")
        
        # Immigration status - CRITICAL!
        immigration_status = app_data.get('immigration_status', 'British citizen with the right to work in the UK')
        
        immigration_select = page.locator('select[name*="immigration"]')
        if await immigration_select.count() > 0:
            await immigration_select.select_option(label=immigration_status)
        
        # Current employee
        await self.select_radio(page, 'current.*employee.*trust', 'No')
        await self.select_radio(page, 'current.*employee.*nhs', 'No')
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_qualifications(self, page: Page, student: dict):
        """Fill qualifications"""
        logger.info("Filling qualifications...")
        
        await self.click_section(page, "Education")
        
        qualifications = student.get('qualifications', [])
        
        for i, qual in enumerate(qualifications[:11]):  # Max 11
            # Click "Add qualification"
            if i > 0:
                add_btn = page.locator('button:has-text("Add"), a:has-text("Add")')
                if await add_btn.count() > 0:
                    await add_btn.click()
                    await page.wait_for_timeout(1000)
            
            # Fill fields
            await page.fill(f'input[name*="subject"][{i}]', qual.get('subject', ''))
            await page.fill(f'input[name*="institution"][{i}]', qual.get('place_of_study', ''))
            await page.fill(f'input[name*="grade"][{i}]', qual.get('grade', ''))
            await page.fill(f'input[name*="year"][{i}]', str(qual.get('year', '')))
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_training_courses(self, page: Page, student: dict):
        """Fill training courses - TQUK COURSE!"""
        logger.info("Filling training courses...")
        
        await self.click_section(page, "Training")
        
        # Add TQUK course
        await page.fill('input[name*="course_title"]', 
            'Proficient Professional Development Learning Course in Understanding RTT and Hospital Administration')
        
        await page.fill('input[name*="provider"]',
            'T21 Services (TQUK Approved Centre #36257481088)')
        
        await page.fill('input[name*="duration"]', '12 weeks')
        
        await page.fill('input[name*="year"]', student.get('tquk_completion_year', '2025'))
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_employment_history(self, page: Page, student: dict):
        """Fill employment history"""
        logger.info("Filling employment history...")
        
        await self.click_section(page, "Employment")
        
        employment = student.get('employment_history', [])
        
        for i, job in enumerate(employment[:10]):  # Max 10
            if i > 0:
                add_btn = page.locator('button:has-text("Add employer")')
                if await add_btn.count() > 0:
                    await add_btn.click()
                    await page.wait_for_timeout(1000)
            
            await page.fill(f'input[name*="employer_name"][{i}]', job.get('employer', ''))
            await page.fill(f'input[name*="job_title"][{i}]', job.get('job_title', ''))
            await page.fill(f'input[name*="start_date"][{i}]', job.get('start_date', ''))
            await page.fill(f'input[name*="end_date"][{i}]', job.get('end_date', ''))
            await page.fill(f'textarea[name*="duties"][{i}]', job.get('duties', ''))
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_supporting_information(self, page: Page, supporting_info: str):
        """Fill AI-generated supporting information"""
        logger.info("Filling supporting information (AI-generated)...")
        
        await self.click_section(page, "Supporting information")
        
        # Find text area
        textarea = page.locator('textarea[name*="supporting"], textarea[name*="statement"]')
        
        if await textarea.count() > 0:
            await textarea.fill(supporting_info)
            logger.info(f"✅ Filled {len(supporting_info.split())} words of AI-generated content")
        
        # AI usage declaration
        ai_declaration = page.locator('textarea[name*="ai"], textarea[name*="artificial"]')
        if await ai_declaration.count() > 0:
            await ai_declaration.fill(
                "Yes, I used AI to assist with drafting the supporting information section to ensure clarity and professionalism in presenting my qualifications and experience."
            )
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_references(self, page: Page, student: dict):
        """Fill references"""
        logger.info("Filling references...")
        
        await self.click_section(page, "References")
        
        references = student.get('references', [])
        
        for i, ref in enumerate(references[:3]):  # Min 2, max 3
            if i > 0:
                add_btn = page.locator('button:has-text("Add reference")')
                if await add_btn.count() > 0:
                    await add_btn.click()
                    await page.wait_for_timeout(1000)
            
            await page.fill(f'input[name*="ref_name"][{i}]', ref.get('name', ''))
            await page.fill(f'input[name*="ref_organisation"][{i}]', ref.get('organisation', ''))
            await page.fill(f'input[name*="ref_email"][{i}]', ref.get('email', ''))
            await page.fill(f'input[name*="ref_phone"][{i}]', ref.get('phone', ''))
            await page.fill(f'input[name*="ref_position"][{i}]', ref.get('position', ''))
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_equal_opportunities(self, page: Page, student: dict):
        """Fill equal opportunities (not used in selection)"""
        logger.info("Filling equal opportunities...")
        
        await self.click_section(page, "Equal opportunities")
        
        # Optional fields - can skip or fill
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def fill_declaration(self, page: Page):
        """Fill declaration - MUST check agreement"""
        logger.info("Filling declaration...")
        
        await self.click_section(page, "Declaration")
        
        # Find and check declaration checkbox
        declaration_checkbox = page.locator('input[type="checkbox"][name*="declaration"]')
        if await declaration_checkbox.count() > 0:
            await declaration_checkbox.check()
        
        await page.click('button:has-text("Save")')
        await page.wait_for_load_state('networkidle')
    
    async def submit_form(self, page: Page) -> dict:
        """
        Final submission
        """
        logger.info("🚀 Submitting application...")
        
        # Click final submit button
        submit_btn = page.locator('button:has-text("Submit application"), input[value*="Submit"]')
        
        if await submit_btn.count() > 0:
            await submit_btn.click()
            await page.wait_for_load_state('networkidle')
            
            # Wait for confirmation page
            await page.wait_for_timeout(3000)
            
            # Extract confirmation number
            confirmation_text = await page.locator('.confirmation, .success, .reference').inner_text()
            
            # Parse reference number
            import re
            ref_match = re.search(r'[A-Z0-9]{8,}', confirmation_text)
            reference = ref_match.group(0) if ref_match else 'SUBMITTED'
            
            return {
                'reference': reference,
                'url': page.url,
                'confirmation_html': await page.content()
            }
        else:
            raise Exception("Submit button not found")
    
    async def click_section(self, page: Page, section_name: str):
        """Click section to open it"""
        section = page.locator(f'text=/{section_name}/i')
        if await section.count() > 0:
            await section.click()
            await page.wait_for_timeout(500)
    
    async def select_radio(self, page: Page, pattern: str, value: str):
        """Select radio button by pattern"""
        radio = page.locator(f'input[type="radio"][name*="{pattern}"][value*="{value}"]')
        if await radio.count() > 0:
            await radio.check()
    
    def decrypt_password(self, encrypted: str) -> str:
        """Decrypt Trac password"""
        key = os.getenv('ENCRYPTION_KEY')
        cipher = Fernet(key.encode())
        return cipher.decrypt(encrypted.encode()).decode()


if __name__ == '__main__':
    import asyncio
    
    submitter = TracAutoSubmitter()
    result = asyncio.run(submitter.submit_application('test-application-id'))
    print(f"Submitted: {result['confirmation_number']}")
