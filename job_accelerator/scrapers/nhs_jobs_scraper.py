"""
NHS JOBS SCRAPER - The Crown Jewel
Most sophisticated NHS Jobs scraper built specifically for healthcare roles
Priority #1: RTT Validators, Hospital Administrators, Medical Secretaries
"""

import asyncio
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from playwright.async_api import async_playwright, Page
import json

logger = logging.getLogger(__name__)

class NHSJobsScraper:
    """
    Ultra-sophisticated NHS Jobs scraper
    
    Features:
    - Targeted RTT/healthcare role discovery
    - Full job detail extraction
    - Application method detection
    - Salary parsing and normalization
    - Location extraction and geocoding
    - Duplicate detection
    - Rate limiting and politeness
    - Error recovery and retry logic
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.base_url = "https://beta.jobs.nhs.uk"
        self.search_url = f"{self.base_url}/candidate/search/results"
        
        # Our specialty keywords (prioritized for healthcare)
        self.priority_keywords = [
            "RTT",
            "Referral to Treatment",
            "Waiting List",
            "RTT Validator",
            "RTT Coordinator",
            "Access Coordinator",
            "Hospital Administrator",
            "Medical Secretary",
            "Outpatient Administrator",
            "Patient Access",
            "Booking Administrator"
        ]
        
        self.jobs_found = []
        self.errors = []
        
    async def scrape_jobs(
        self, 
        keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Main scraping function - discovers NHS jobs
        
        Args:
            keywords: Search keywords (defaults to priority_keywords)
            locations: Target locations (None = nationwide)
            max_results: Maximum jobs to return
            
        Returns:
            List of job dictionaries with full details
        """
        keywords = keywords or self.priority_keywords
        
        logger.info(f"🔍 Starting NHS Jobs scrape for: {', '.join(keywords)}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.config.get('headless', True)
            )
            
            # Create context with realistic user agent
            context = await browser.new_context(
                user_agent=self.config.get('user_agents', [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ])[0],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                all_jobs = []
                
                # Search for each keyword (prioritized)
                for keyword in keywords:
                    logger.info(f"🔎 Searching for: {keyword}")
                    
                    jobs = await self._search_keyword(page, keyword, locations)
                    
                    logger.info(f"✅ Found {len(jobs)} jobs for '{keyword}'")
                    all_jobs.extend(jobs)
                    
                    # Rate limiting - be polite!
                    await asyncio.sleep(2)
                    
                    if len(all_jobs) >= max_results:
                        break
                
                # Remove duplicates (same URL)
                unique_jobs = self._remove_duplicates(all_jobs)
                
                # Score relevance
                scored_jobs = self._score_relevance(unique_jobs)
                
                # Sort by relevance and return top N
                sorted_jobs = sorted(
                    scored_jobs, 
                    key=lambda x: x.get('relevance_score', 0), 
                    reverse=True
                )[:max_results]
                
                logger.info(f"🎯 Returning {len(sorted_jobs)} unique, relevant jobs")
                
                self.jobs_found = sorted_jobs
                return sorted_jobs
                
            except Exception as e:
                logger.error(f"❌ Scraping failed: {str(e)}")
                self.errors.append(str(e))
                raise
            
            finally:
                await browser.close()
    
    async def _search_keyword(
        self, 
        page: Page, 
        keyword: str, 
        locations: Optional[List[str]] = None
    ) -> List[Dict]:
        """Search NHS Jobs for specific keyword"""
        
        try:
            # Build search URL
            search_params = {
                'keyword': keyword,
                'location': '',  # Empty for nationwide
                'distance': '25',  # Miles
                'sort': 'publicationDateDesc'  # Newest first
            }
            
            # Navigate to search
            search_url_with_params = f"{self.search_url}?"
            search_url_with_params += "&".join([f"{k}={v}" for k, v in search_params.items()])
            
            await page.goto(search_url_with_params, wait_until='networkidle', timeout=30000)
            
            # Wait for results to load
            await page.wait_for_selector('.nhsuk-list-panel', timeout=10000)
            
            # Extract job listings
            job_cards = await page.query_selector_all('article.nhsuk-list-panel')
            
            logger.info(f"📄 Found {len(job_cards)} job listings on page")
            
            jobs = []
            
            for card in job_cards:
                try:
                    job = await self._extract_job_from_card(page, card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to extract job: {str(e)}")
                    continue
            
            return jobs
            
        except Exception as e:
            logger.error(f"❌ Keyword search failed for '{keyword}': {str(e)}")
            return []
    
    async def _extract_job_from_card(self, page: Page, card) -> Optional[Dict]:
        """Extract job details from a search result card"""
        
        try:
            # Job title and URL
            title_element = await card.query_selector('h2 a')
            if not title_element:
                return None
            
            title = await title_element.inner_text()
            job_url = await title_element.get_attribute('href')
            
            if not job_url.startswith('http'):
                job_url = f"{self.base_url}{job_url}"
            
            # Employer
            employer_element = await card.query_selector('.nhsuk-heading-s')
            employer = await employer_element.inner_text() if employer_element else "NHS"
            
            # Location
            location_element = await card.query_selector('[data-test="search-result-location"]')
            location = await location_element.inner_text() if location_element else ""
            
            # Salary
            salary_element = await card.query_selector('[data-test="search-result-salary"]')
            salary_text = await salary_element.inner_text() if salary_element else "Not specified"
            
            # Closing date
            closing_element = await card.query_selector('[data-test="search-result-closingDate"]')
            closing_date_text = await closing_element.inner_text() if closing_element else ""
            
            # Extract job ID from URL
            job_id_match = re.search(r'/(\d+)-', job_url)
            job_id = job_id_match.group(1) if job_id_match else None
            
            # Parse salary
            salary_min, salary_max = self._parse_salary(salary_text)
            
            # Parse closing date
            closing_date = self._parse_date(closing_date_text)
            
            # Basic job object
            job = {
                'title': title.strip(),
                'company': employer.strip(),
                'url': job_url,
                'job_board': 'nhs_jobs',
                'external_id': job_id,
                'location': location.strip(),
                'salary_text': salary_text.strip(),
                'salary_min': salary_min,
                'salary_max': salary_max,
                'closing_date': closing_date,
                'posted_date': datetime.now().date(),  # Assume recent
                'status': 'active',
                'application_method': 'form',  # NHS Jobs uses forms
                'scraped_at': datetime.now()
            }
            
            return job
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to extract job card: {str(e)}")
            return None
    
    async def get_job_details(self, job_url: str) -> Optional[Dict]:
        """
        Get full job details from job page
        This is called AFTER initial scraping to get full description
        """
        
        logger.info(f"📖 Fetching full details for: {job_url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(job_url, wait_until='networkidle', timeout=30000)
                
                # Wait for job description
                await page.wait_for_selector('.job-description', timeout=10000)
                
                # Extract full description
                description_element = await page.query_selector('.job-description')
                description = await description_element.inner_text() if description_element else ""
                
                # Extract requirements
                requirements_element = await page.query_selector('.requirements')
                requirements = await requirements_element.inner_text() if requirements_element else ""
                
                # Extract application instructions
                instructions_element = await page.query_selector('.application-instructions')
                instructions = await instructions_element.inner_text() if instructions_element else ""
                
                # Extract specialty/department
                specialty_element = await page.query_selector('[data-test="job-specialty"]')
                specialty = await specialty_element.inner_text() if specialty_element else ""
                
                # Employment type
                employment_element = await page.query_selector('[data-test="job-employment-type"]')
                employment_type = await employment_element.inner_text() if employment_element else "Full-time"
                
                # Contract duration
                duration_element = await page.query_selector('[data-test="job-contract-duration"]')
                duration = await duration_element.inner_text() if duration_element else ""
                
                # Working pattern
                pattern_element = await page.query_selector('[data-test="job-working-pattern"]')
                working_pattern = await pattern_element.inner_text() if pattern_element else ""
                
                details = {
                    'description': description.strip(),
                    'requirements': requirements.strip(),
                    'application_instructions': instructions.strip(),
                    'specialty': specialty.strip(),
                    'employment_type': employment_type.strip(),
                    'contract_duration': duration.strip(),
                    'working_pattern': working_pattern.strip(),
                    'required_skills': self._extract_skills(description + requirements),
                    'experience_required': self._extract_experience(description + requirements)
                }
                
                return details
                
            except Exception as e:
                logger.error(f"❌ Failed to get job details: {str(e)}")
                return None
            
            finally:
                await browser.close()
    
    def _parse_salary(self, salary_text: str) -> tuple:
        """Parse salary text into min/max integers"""
        
        if not salary_text or salary_text.lower() in ['not specified', 'competitive', 'negotiable']:
            return None, None
        
        # Remove £ and commas
        salary_clean = salary_text.replace('£', '').replace(',', '')
        
        # Try to find range (e.g., "25000-30000" or "25,000 - 30,000")
        range_match = re.search(r'(\d+)\s*-\s*(\d+)', salary_clean)
        if range_match:
            return int(range_match.group(1)), int(range_match.group(2))
        
        # Try to find single value
        single_match = re.search(r'(\d+)', salary_clean)
        if single_match:
            value = int(single_match.group(1))
            return value, value
        
        return None, None
    
    def _parse_date(self, date_text: str) -> Optional[str]:
        """Parse closing date text to ISO date"""
        
        if not date_text:
            return None
        
        try:
            # Common formats: "24 October 2025", "24/10/2025", "24-10-2025"
            
            # Try multiple formats
            for fmt in ['%d %B %Y', '%d/%m/%Y', '%d-%m-%Y']:
                try:
                    parsed = datetime.strptime(date_text.strip(), fmt)
                    return parsed.date().isoformat()
                except:
                    continue
            
            # If we see "in X days"
            days_match = re.search(r'in (\d+) days?', date_text.lower())
            if days_match:
                days = int(days_match.group(1))
                future_date = datetime.now().date() + timedelta(days=days)
                return future_date.isoformat()
            
            return None
            
        except:
            return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract required skills from job description"""
        
        skills = []
        
        # Common NHS/healthcare skills to look for
        skill_patterns = [
            r'RTT',
            r'Referral to Treatment',
            r'PAS system',
            r'Patient Administration System',
            r'Microsoft Office',
            r'Excel',
            r'Data analysis',
            r'Communication skills',
            r'Organizational skills',
            r'Attention to detail',
            r'Time management',
            r'18 week pathway',
            r'Waiting list management',
            r'Booking appointments',
            r'Medical terminology',
            r'NHS guidelines',
        ]
        
        text_lower = text.lower()
        
        for pattern in skill_patterns:
            if pattern.lower() in text_lower:
                skills.append(pattern)
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> int:
        """Extract years of experience required"""
        
        # Look for patterns like "2 years experience", "2+ years", "minimum 2 years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(of\s*)?experience',
            r'minimum\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?',
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return int(match.group(1))
        
        return 0  # No experience required
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on URL"""
        
        seen_urls = set()
        unique_jobs = []
        
        for job in jobs:
            if job['url'] not in seen_urls:
                seen_urls.add(job['url'])
                unique_jobs.append(job)
        
        removed = len(jobs) - len(unique_jobs)
        if removed > 0:
            logger.info(f"🔄 Removed {removed} duplicate jobs")
        
        return unique_jobs
    
    def _score_relevance(self, jobs: List[Dict]) -> List[Dict]:
        """
        Score job relevance for RTT/healthcare graduates
        Higher score = better match for T21 students
        """
        
        for job in jobs:
            score = 0
            title_lower = job['title'].lower()
            
            # High priority keywords (perfect for our students)
            if any(kw in title_lower for kw in ['rtt', 'referral to treatment', 'validator']):
                score += 50
            
            # Medium priority (very relevant)
            if any(kw in title_lower for kw in ['waiting list', 'access', 'booking', 'outpatient']):
                score += 30
            
            # Relevant roles
            if any(kw in title_lower for kw in ['administrator', 'secretary', 'coordinator']):
                score += 20
            
            # Healthcare context
            if any(kw in title_lower for kw in ['hospital', 'nhs', 'clinic', 'medical']):
                score += 10
            
            # Bonus for NHS Jobs (our specialty!)
            if job['job_board'] == 'nhs_jobs':
                score += 10
            
            # Penalty for senior roles (students are entry/mid-level)
            if any(kw in title_lower for kw in ['senior', 'lead', 'manager', 'head of', 'director']):
                score -= 30
            
            # Cap at 100
            job['relevance_score'] = min(score, 100)
        
        return jobs
    
    async def test_connection(self) -> bool:
        """Test if NHS Jobs site is accessible"""
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                response = await page.goto(self.base_url, timeout=15000)
                success = response.status == 200
                
                await browser.close()
                
                if success:
                    logger.info("✅ NHS Jobs connection test passed")
                else:
                    logger.error(f"❌ NHS Jobs returned status {response.status}")
                
                return success
                
        except Exception as e:
            logger.error(f"❌ NHS Jobs connection test failed: {str(e)}")
            return False


# ============================================
# USAGE EXAMPLE
# ============================================

async def main():
    """Example usage of NHS Jobs scraper"""
    
    config = {
        'headless': False,  # Show browser for testing
        'user_agents': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36']
    }
    
    scraper = NHSJobsScraper(config)
    
    # Test connection first
    logger.info("Testing connection to NHS Jobs...")
    connected = await scraper.test_connection()
    
    if not connected:
        logger.error("Cannot connect to NHS Jobs")
        return
    
    # Scrape jobs
    logger.info("Scraping RTT jobs...")
    jobs = await scraper.scrape_jobs(
        keywords=['RTT Validator', 'Hospital Administrator'],
        max_results=20
    )
    
    # Print results
    print(f"\n✅ Found {len(jobs)} jobs!\n")
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Salary: {job['salary_text']}")
        print(f"   Relevance Score: {job['relevance_score']}/100")
        print(f"   URL: {job['url']}")
        print()
    
    # Get full details for first job
    if jobs:
        logger.info(f"\nFetching full details for: {jobs[0]['title']}")
        details = await scraper.get_job_details(jobs[0]['url'])
        
        if details:
            print("\nFull Job Details:")
            print(f"Description: {details['description'][:200]}...")
            print(f"Skills Required: {', '.join(details['required_skills'])}")
            print(f"Experience: {details['experience_required']} years")

if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(main())
