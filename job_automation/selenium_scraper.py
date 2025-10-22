"""
NHS Jobs Scraper using Selenium (Real Browser)
This uses a real Chrome browser to scrape NHS Jobs, making it harder to block
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
from supabase_database import supabase, SUPABASE_AVAILABLE

def scrape_nhs_jobs_selenium(keywords=None, location='London', max_jobs=20):
    """
    Scrape NHS Jobs using Selenium (real browser)
    
    Args:
        keywords: List of job keywords
        location: Location to search
        max_jobs: Maximum number of jobs to scrape
    
    Returns:
        List of discovered jobs
    """
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return []
    
    discovered_jobs = []
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run without opening browser window
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    
    try:
        print("🌐 Starting Chrome browser...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Build search URL
        search_keywords = ' '.join(keywords) if keywords else 'RTT Validation Administrator'
        search_url = f"https://www.jobs.nhs.uk/xi/search_vacancy/?action=search&keyword={search_keywords}&location={location}"
        
        print(f"🔍 Visiting: {search_url}")
        driver.get(search_url)
        
        # Wait for page to load
        time.sleep(3)
        
        print("⏳ Waiting for job listings to load...")
        
        # Try to find job listings with multiple possible selectors
        job_elements = []
        selectors = [
            "//article[contains(@class, 'vacancy')]",
            "//div[contains(@class, 'vacancy-result')]",
            "//li[contains(@class, 'search-result')]",
            "//div[@data-test='vacancy-item']"
        ]
        
        for selector in selectors:
            try:
                job_elements = driver.find_elements(By.XPATH, selector)
                if job_elements:
                    print(f"✅ Found {len(job_elements)} jobs using selector: {selector}")
                    break
            except:
                continue
        
        if not job_elements:
            print("❌ No job listings found on page")
            print(f"Page title: {driver.title}")
            print(f"Page URL: {driver.current_url}")
            return []
        
        print(f"📊 Processing {min(len(job_elements), max_jobs)} jobs...")
        
        for i, job_elem in enumerate(job_elements[:max_jobs]):
            try:
                # Extract job title
                try:
                    title = job_elem.find_element(By.XPATH, ".//h2 | .//h3 | .//a[contains(@class, 'vacancy')]").text.strip()
                except:
                    title = "Unknown Position"
                
                # Extract employer/trust
                try:
                    trust = job_elem.find_element(By.XPATH, ".//*[contains(@class, 'employer') or contains(@class, 'organisation')]").text.strip()
                except:
                    trust = "NHS Trust"
                
                # Extract location
                try:
                    location_text = job_elem.find_element(By.XPATH, ".//*[contains(@class, 'location')]").text.strip()
                except:
                    location_text = location
                
                # Extract salary
                try:
                    salary_text = job_elem.find_element(By.XPATH, ".//*[contains(@class, 'salary')]").text.strip()
                except:
                    salary_text = ""
                
                # Extract job URL
                try:
                    link = job_elem.find_element(By.XPATH, ".//a[@href]")
                    job_url = link.get_attribute('href')
                    if not job_url.startswith('http'):
                        job_url = 'https://www.jobs.nhs.uk' + job_url
                except:
                    job_url = ""
                
                # Generate job reference
                job_reference = f"NHS-SELENIUM-{int(datetime.now().timestamp())}-{i}"
                
                # Parse salary
                salary_min = 0
                salary_max = 0
                if salary_text:
                    import re
                    numbers = re.findall(r'[\d,]+', salary_text)
                    if len(numbers) >= 2:
                        salary_min = int(numbers[0].replace(',', ''))
                        salary_max = int(numbers[1].replace(',', ''))
                    elif len(numbers) == 1:
                        salary_min = salary_max = int(numbers[0].replace(',', ''))
                
                # Extract band
                band = "Not specified"
                for band_num in range(2, 9):
                    if f'band {band_num}' in title.lower() or f'band {band_num}' in salary_text.lower():
                        band = f'Band {band_num}'
                        break
                
                # Create job data
                job_data = {
                    'title': title,
                    'trust': trust,
                    'location': location_text,
                    'band': band,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'closing_date': (datetime.now() + timedelta(days=14)).isoformat(),
                    'nhs_jobs_url': job_url,
                    'job_reference': job_reference,
                    'discovered_at': datetime.now().isoformat()
                }
                
                # Check if already exists
                existing = supabase.table('discovered_jobs').select('id').eq('job_reference', job_reference).execute()
                
                if not existing.data:
                    result = supabase.table('discovered_jobs').insert(job_data).execute()
                    if result.data:
                        discovered_jobs.append(result.data[0])
                        print(f"✅ {i+1}. Added: {title} at {trust}")
                
            except Exception as e:
                print(f"⚠️ Error processing job {i+1}: {str(e)}")
                continue
        
        print(f"\n✅ Scraping complete! Added {len(discovered_jobs)} new jobs")
        return discovered_jobs
    
    except Exception as e:
        print(f"❌ Selenium error: {str(e)}")
        return []
    
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")

if __name__ == "__main__":
    print("🚀 NHS Jobs Selenium Scraper")
    print("=" * 60)
    jobs = scrape_nhs_jobs_selenium(keywords=['RTT', 'Validation', 'Administrator'], location='London', max_jobs=10)
    print(f"\n📊 Total jobs scraped: {len(jobs)}")
