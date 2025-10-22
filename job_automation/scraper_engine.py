"""
NHS Jobs Scraper Engine with Advanced Filters
Continuously discovers jobs matching student criteria
"""

import asyncio
from playwright.async_api import async_playwright, Page
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from supabase import create_client
import os
import re

logger = logging.getLogger(__name__)

class JobScraperEngine:
    """
    24/7 job discovery engine with comprehensive filtering
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        self.nhs_jobs_url = 'https://beta.jobs.nhs.uk'
        self.scrape_interval_hours = 6
        
    async def scrape_continuously(self):
        """
        Main loop - runs forever
        """
        logger.info("🚀 Starting NHS Jobs scraper engine...")
        
        while True:
            try:
                # Get all active student searches
                active_students = await self.get_active_students()
                
                logger.info(f"📊 Found {len(active_students)} active students")
                
                for student in active_students:
                    try:
                        await self.scrape_for_student(student)
                    except Exception as e:
                        logger.error(f"❌ Error scraping for student {student['student_id']}: {e}")
                        continue
                
                logger.info(f"✅ Scrape cycle complete. Sleeping for {self.scrape_interval_hours} hours...")
                await asyncio.sleep(self.scrape_interval_hours * 3600)
                
            except Exception as e:
                logger.error(f"❌ Scraper engine error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def get_active_students(self) -> List[Dict]:
        """
        Get all students with active automation settings
        """
        response = self.supabase.table('student_automation_settings')\
            .select('*')\
            .eq('status', 'active')\
            .eq('auto_submit_enabled', True)\
            .execute()
        
        return response.data
    
    async def scrape_for_student(self, student_settings: Dict):
        """
        Scrape jobs for individual student based on their preferences
        """
        logger.info(f"🔍 Scraping jobs for student: {student_settings['student_id']}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Build search with ALL filters
                jobs = await self.search_jobs_with_filters(page, student_settings)
                
                logger.info(f"📦 Found {len(jobs)} jobs for student")
                
                # Store jobs and queue applications
                await self.process_discovered_jobs(jobs, student_settings)
                
            finally:
                await browser.close()
    
    async def search_jobs_with_filters(self, page: Page, settings: Dict) -> List[Dict]:
        """
        Search NHS Jobs with COMPLETE filter set
        """
        jobs = []
        
        # Navigate to NHS Jobs search
        await page.goto(f'{self.nhs_jobs_url}/candidate/search')
        await page.wait_for_load_state('networkidle')
        
        # Build search query from keywords
        keywords = ' OR '.join(settings.get('search_keywords', ['RTT', 'Administrator']))
        await page.fill('input[name="keyword"]', keywords)
        
        # LOCATION FILTER
        for location in settings.get('preferred_locations', []):
            await page.fill('input[name="location"]', location)
            
            # RADIUS FILTER
            radius = settings.get('search_radius_miles', 20)
            await page.select_option('select[name="distance"]', str(radius))
            
            # BAND FILTER
            for band in settings.get('preferred_bands', []):
                band_checkbox = page.locator(f'input[type="checkbox"][value*="{band}"]')
                if await band_checkbox.count() > 0:
                    await band_checkbox.first.check()
            
            # WORKING PATTERN FILTER
            working_patterns = settings.get('working_patterns', ['Full time', 'Part time'])
            for pattern in working_patterns:
                pattern_checkbox = page.locator(f'input[type="checkbox"][value*="{pattern}"]')
                if await pattern_checkbox.count() > 0:
                    await pattern_checkbox.first.check()
            
            # HYBRID/REMOTE FILTER
            if settings.get('include_hybrid', True):
                hybrid_checkbox = page.locator('input[value*="Hybrid"]')
                if await hybrid_checkbox.count() > 0:
                    await hybrid_checkbox.check()
            
            if settings.get('include_remote', True):
                remote_checkbox = page.locator('input[value*="Remote"]')
                if await remote_checkbox.count() > 0:
                    await remote_checkbox.check()
            
            # CONTRACT TYPE FILTER
            contract_types = settings.get('contract_types', ['Permanent', 'Fixed term'])
            for contract_type in contract_types:
                contract_checkbox = page.locator(f'input[value*="{contract_type}"]')
                if await contract_checkbox.count() > 0:
                    await contract_checkbox.first.check()
            
            # Click search
            await page.click('button:has-text("Search")')
            await page.wait_for_load_state('networkidle')
            
            # Scrape results (all pages)
            page_jobs = await self.scrape_search_results(page, settings)
            jobs.extend(page_jobs)
        
        # Remove duplicates
        unique_jobs = {job['job_reference']: job for job in jobs}.values()
        
        return list(unique_jobs)
    
    async def scrape_search_results(self, page: Page, settings: Dict) -> List[Dict]:
        """
        Scrape all jobs from search results (with pagination)
        """
        all_jobs = []
        page_num = 1
        
        while True:
            logger.info(f"📄 Scraping page {page_num}...")
            
            # Wait for job cards
            await page.wait_for_selector('.job-card, .vacancy-card', timeout=10000)
            
            # Get all job cards on page
            job_cards = await page.locator('.job-card, .vacancy-card').all()
            
            for card in job_cards:
                try:
                    # Extract basic info from card
                    job_link = await card.locator('a').first.get_attribute('href')
                    
                    # Click to view full details
                    await card.click()
                    await page.wait_for_load_state('networkidle')
                    
                    # Extract full job details
                    job = await self.extract_job_details(page, settings)
                    
                    if job:
                        all_jobs.append(job)
                    
                    # Go back to results
                    await page.go_back()
                    await page.wait_for_load_state('networkidle')
                    
                except Exception as e:
                    logger.error(f"❌ Error extracting job: {e}")
                    continue
            
            # Check for next page
            next_button = page.locator('a:has-text("Next"), button:has-text("Next")')
            if await next_button.count() > 0 and await next_button.is_visible():
                await next_button.click()
                await page.wait_for_load_state('networkidle')
                page_num += 1
            else:
                break
        
        return all_jobs
    
    async def extract_job_details(self, page: Page, settings: Dict) -> Optional[Dict]:
        """
        Extract complete job details from job page
        """
        try:
            # Get job reference
            job_ref = await page.locator('.job-reference, [data-job-reference]').first.inner_text()
            job_ref = job_ref.strip()
            
            # Get title
            title = await page.locator('h1').first.inner_text()
            
            # Get trust
            trust = await page.locator('.employer-name, .trust-name').first.inner_text()
            
            # Get location
            location = await page.locator('.location, [data-location]').first.inner_text()
            city = self.extract_city(location)
            
            # Get closing date
            closing_text = await page.locator('text=/Closing.*?date/i').first.inner_text()
            closing_date = self.parse_closing_date(closing_text)
            
            # Check closing date filter
            days_until_closing = (closing_date - datetime.now().date()).days
            if days_until_closing < settings.get('min_days_until_closing', 2):
                logger.info(f"⏭️ Skipping {title} - closes too soon")
                return None
            if days_until_closing > settings.get('max_days_until_closing', 14):
                logger.info(f"⏭️ Skipping {title} - closes too far away")
                return None
            
            # Get full description
            description_html = await page.locator('.job-description, .vacancy-description').first.inner_html()
            description_text = await page.locator('.job-description, .vacancy-description').first.inner_text()
            
            # Check exclude keywords
            exclude_keywords = settings.get('exclude_keywords', [])
            if any(keyword.lower() in title.lower() or keyword.lower() in description_text.lower() 
                   for keyword in exclude_keywords):
                logger.info(f"⏭️ Skipping {title} - matches exclude keywords")
                return None
            
            # CRITICAL: Detect sponsorship
            has_sponsorship = self.detect_sponsorship(description_html, description_text)
            
            # Filter by sponsorship if required
            if settings.get('requires_sponsorship', False) and not has_sponsorship:
                logger.info(f"⏭️ Skipping {title} - no sponsorship")
                return None
            
            # Extract other details
            band = self.extract_band(description_text)
            salary_min, salary_max = self.extract_salary(description_text)
            working_pattern = self.extract_working_pattern(description_text)
            contract_type = self.extract_contract_type(description_text)
            is_hybrid = 'hybrid' in description_text.lower()
            is_remote = 'remote' in description_text.lower()
            
            # Get apply URL
            apply_button = page.locator('a:has-text("Apply"), button:has-text("Apply")')
            apply_url = None
            if await apply_button.count() > 0:
                apply_url = await apply_button.first.get_attribute('href')
            
            # Extract structured data
            essential_criteria = await self.extract_criteria(page, 'essential')
            desirable_criteria = await self.extract_criteria(page, 'desirable')
            main_duties = await self.extract_main_duties(page)
            
            job_data = {
                'job_reference': job_ref,
                'title': title,
                'trust': trust,
                'location': location,
                'city': city,
                'band': band,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'working_pattern': working_pattern,
                'contract_type': contract_type,
                'is_hybrid': is_hybrid,
                'is_remote': is_remote,
                'has_sponsorship': has_sponsorship,
                'sponsorship_text': self.extract_sponsorship_text(description_html) if has_sponsorship else None,
                'closing_date': closing_date.isoformat(),
                'job_description': description_text,
                'essential_criteria': essential_criteria,
                'desirable_criteria': desirable_criteria,
                'main_duties': main_duties,
                'nhs_jobs_url': page.url,
                'trac_apply_url': apply_url,
                'discovered_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Extracted: {title} at {trust} {'(Sponsorship ✓)' if has_sponsorship else ''}")
            
            return job_data
            
        except Exception as e:
            logger.error(f"❌ Error extracting job details: {e}")
            return None
    
    def detect_sponsorship(self, html: str, text: str) -> bool:
        """
        AI-powered sponsorship detection
        """
        combined = (html + ' ' + text).lower()
        
        sponsorship_keywords = [
            'certificate of sponsorship',
            'skilled worker sponsorship',
            'visa sponsorship',
            'can sponsor',
            'will sponsor',
            'sponsorship available',
            'we welcome applications from job seekers who require',
            'applicants requiring sponsorship',
            'work visa sponsorship'
        ]
        
        for keyword in sponsorship_keywords:
            if keyword in combined:
                return True
        
        return False
    
    def extract_sponsorship_text(self, html: str) -> str:
        """
        Extract sponsorship section text
        """
        # Look for Certificate of Sponsorship section
        match = re.search(r'Certificate of Sponsorship.*?</p>', html, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(0)
        return ''
    
    def extract_city(self, location: str) -> str:
        """Extract city from location string"""
        # Usually first part before comma
        return location.split(',')[0].strip()
    
    def parse_closing_date(self, text: str) -> datetime.date:
        """Parse closing date from text"""
        # Extract date in format like "28 October 2025"
        match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', text)
        if match:
            day, month, year = match.groups()
            return datetime.strptime(f"{day} {month} {year}", "%d %B %Y").date()
        return datetime.now().date() + timedelta(days=14)  # Default
    
    def extract_band(self, text: str) -> Optional[str]:
        """Extract NHS band"""
        match = re.search(r'Band\s+(\d[a-z]?)', text, re.IGNORECASE)
        return f"Band {match.group(1)}" if match else None
    
    def extract_salary(self, text: str):
        """Extract salary range"""
        match = re.search(r'£([\d,]+).*?£([\d,]+)', text)
        if match:
            min_sal = float(match.group(1).replace(',', ''))
            max_sal = float(match.group(2).replace(',', ''))
            return min_sal, max_sal
        return None, None
    
    def extract_working_pattern(self, text: str) -> Optional[str]:
        """Extract working pattern"""
        patterns = ['Full time', 'Part time', 'Flexible', 'Hybrid', 'Remote']
        for pattern in patterns:
            if pattern.lower() in text.lower():
                return pattern
        return None
    
    def extract_contract_type(self, text: str) -> Optional[str]:
        """Extract contract type"""
        types = ['Permanent', 'Fixed term', 'Temporary', 'Bank']
        for contract_type in types:
            if contract_type.lower() in text.lower():
                return contract_type
        return None
    
    async def extract_criteria(self, page: Page, criteria_type: str) -> Dict:
        """Extract essential or desirable criteria"""
        try:
            section = page.locator(f'text=/{criteria_type} criteria/i')
            if await section.count() > 0:
                criteria_text = await section.locator('..').inner_text()
                return {'raw': criteria_text}
        except:
            pass
        return {}
    
    async def extract_main_duties(self, page: Page) -> str:
        """Extract main duties section"""
        try:
            section = page.locator('text=/main duties/i, text=/job description/i')
            if await section.count() > 0:
                return await section.locator('..').inner_text()
        except:
            pass
        return ''
    
    async def process_discovered_jobs(self, jobs: List[Dict], student_settings: Dict):
        """
        Store jobs and create application queue entries
        """
        for job in jobs:
            try:
                # Store job (upsert)
                job_result = self.supabase.table('discovered_jobs')\
                    .upsert(job, on_conflict='job_reference')\
                    .execute()
                
                job_id = job_result.data[0]['id']
                
                # Create application queue entry (if not exists)
                priority = self.calculate_priority(job, student_settings)
                
                application = {
                    'student_id': student_settings['student_id'],
                    'job_id': job_id,
                    'status': 'queued',
                    'priority': priority,
                    'scheduled_submit_time': self.calculate_submit_time(job, priority)
                }
                
                # Insert (will skip if already exists due to UNIQUE constraint)
                self.supabase.table('applications')\
                    .insert(application)\
                    .execute()
                
                logger.info(f"✅ Queued application: {job['title']} (Priority: {priority})")
                
            except Exception as e:
                # Likely duplicate - skip
                logger.debug(f"Skipping duplicate job: {job['job_reference']}")
                continue
    
    def calculate_priority(self, job: Dict, settings: Dict) -> str:
        """Calculate application priority"""
        closing_date = datetime.fromisoformat(job['closing_date']).date()
        days_until_closing = (closing_date - datetime.now().date()).days
        
        # Urgent: Closes within 2 days
        if days_until_closing <= 2:
            return 'urgent'
        
        # High: Sponsorship match + closes soon
        if settings.get('requires_sponsorship') and job.get('has_sponsorship') and days_until_closing <= 7:
            return 'high'
        
        # Normal: Standard
        if days_until_closing <= 10:
            return 'normal'
        
        return 'low'
    
    def calculate_submit_time(self, job: Dict, priority: str) -> str:
        """Calculate when to submit application"""
        closing_date = datetime.fromisoformat(job['closing_date']).date()
        
        if priority == 'urgent':
            # Submit within 6 hours
            submit_time = datetime.now() + timedelta(hours=6)
        elif priority == 'high':
            # Submit within 24 hours
            submit_time = datetime.now() + timedelta(hours=24)
        else:
            # Submit 3-5 days before closing
            days_before = 4  # Middle ground
            submit_time = datetime.combine(closing_date, datetime.min.time()) - timedelta(days=days_before)
        
        return submit_time.isoformat()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scraper = JobScraperEngine()
    asyncio.run(scraper.scrape_continuously())
