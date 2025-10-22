"""
NHS JOBS SCRAPER ENGINE
Scrapes NHS Jobs website for matching positions based on student preferences
Stores discovered jobs in Supabase database
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from supabase_database import supabase, SUPABASE_AVAILABLE

def scrape_nhs_jobs(locations=None, bands=None, requires_sponsorship=False, keywords=None):
    """
    Scrape NHS Jobs website for matching positions
    
    Args:
        locations: List of preferred locations (e.g., ['London', 'Manchester'])
        bands: List of NHS bands (e.g., ['Band 3', 'Band 4'])
        requires_sponsorship: Boolean - filter for visa sponsorship
        keywords: List of job title keywords (e.g., ['RTT', 'Validation', 'Administrator'])
    
    Returns:
        List of discovered job dictionaries
    """
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return []
    
    discovered_jobs = []
    
    # NHS Jobs search URL - we'll scrape the actual website
    base_url = "https://www.jobs.nhs.uk/xi/search_vacancy"
    
    # Build search parameters
    search_keywords = keywords if keywords else ['RTT', 'Validation', 'Administrator', 'Pathway']
    location = locations[0] if locations else 'London'
    
    params = {
        'action': 'search',
        'keyword': ' '.join(search_keywords),
        'location': location,
        'distanceFromLocation': '20'
    }
    
    try:
        print(f"🔍 Searching NHS Jobs for: {params['keyword']}")
        print(f"📍 Locations: {', '.join(locations) if locations else 'All'}")
        print(f"🏥 Bands: {', '.join(bands) if bands else 'All'}")
        
        # Make request to NHS Jobs website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Referer': 'https://www.jobs.nhs.uk/'
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch NHS Jobs: {response.status_code}")
            print(f"URL: {response.url}")
            return []
        
        print(f"✅ Got response from NHS Jobs")
        
        # Parse HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple possible selectors for job listings
        job_listings = (
            soup.find_all('article', class_='vacancy') or
            soup.find_all('div', class_='vacancy-result') or
            soup.find_all('li', class_='search-result') or
            soup.find_all('div', {'data-test': 'vacancy-item'})
        )
        
        print(f"📊 Found {len(job_listings)} potential jobs")
        
        for listing in job_listings:
            try:
                # Extract job details from HTML - try multiple selectors
                title_elem = (
                    listing.find('h2', class_='vacancy__header') or
                    listing.find('h3') or
                    listing.find('a', class_='vacancy__link')
                )
                title = title_elem.get_text(strip=True) if title_elem else 'Unknown'
                
                # Get trust/employer
                trust_elem = (
                    listing.find('span', class_='vacancy__employer') or
                    listing.find('p', class_='employer')
                )
                trust = trust_elem.get_text(strip=True) if trust_elem else 'Unknown'
                
                # Get location
                location_elem = (
                    listing.find('span', class_='vacancy__location') or
                    listing.find('p', class_='location')
                )
                location_text = location_elem.get_text(strip=True) if location_elem else 'Unknown'
                
                # Get salary
                salary_elem = listing.find('span', class_='vacancy__salary')
                salary_text = salary_elem.get_text(strip=True) if salary_elem else ''
                salary_min, salary_max = parse_salary(salary_text)
                
                # Extract band
                band = extract_band(title, salary_text)
                
                # Get job URL
                link_elem = listing.find('a', href=True)
                job_url = 'https://www.jobs.nhs.uk' + link_elem['href'] if link_elem and link_elem['href'].startswith('/') else (link_elem['href'] if link_elem else '')
                
                # Get job reference from URL or generate one
                job_reference = job_url.split('/')[-1] if job_url else f'NHS-{datetime.now().timestamp()}'
                
                # Get closing date
                closing_elem = listing.find('span', class_='vacancy__closing')
                closing_text = closing_elem.get_text(strip=True) if closing_elem else ''
                closing_date = parse_closing_date(closing_text)
                
                # Check if requires sponsorship (look in job description)
                sponsorship_available = check_sponsorship(job_url) if requires_sponsorship else True
                
                # Filter by criteria
                if not matches_criteria(title, location_text, band, locations, bands, requires_sponsorship, sponsorship_available):
                    continue
                
                # Create job dictionary
                job_data = {
                    'title': title,
                    'trust': trust,
                    'location': location_text,
                    'band': band,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'requires_sponsorship': requires_sponsorship,
                    'sponsorship_available': sponsorship_available,
                    'closing_date': closing_date,
                    'nhs_jobs_url': job_url,
                    'job_reference': job_reference,
                    'discovered_at': datetime.now().isoformat()
                }
                
                # Check if job already exists in database
                existing = supabase.table('discovered_jobs').select('id').eq('job_reference', job_reference).execute()
                
                if not existing.data:
                    # Insert into database
                    result = supabase.table('discovered_jobs').insert(job_data).execute()
                    if result.data:
                        discovered_jobs.append(result.data[0])
                        print(f"✅ Added: {title} at {trust}")
                else:
                    print(f"⏭️ Skip: {title} (already in database)")
            
            except Exception as e:
                print(f"⚠️ Error parsing job listing: {str(e)}")
                continue
        
        print(f"✅ Scraping complete! Found {len(discovered_jobs)} new jobs")
        return discovered_jobs
    
    except Exception as e:
        print(f"❌ Scraping error: {str(e)}")
        return []

def parse_salary(salary_text):
    """Extract min and max salary from text"""
    try:
        # Look for patterns like "£24,000 - £28,000"
        numbers = re.findall(r'£?([\d,]+)', salary_text)
        if len(numbers) >= 2:
            salary_min = int(numbers[0].replace(',', ''))
            salary_max = int(numbers[1].replace(',', ''))
            return salary_min, salary_max
        elif len(numbers) == 1:
            salary = int(numbers[0].replace(',', ''))
            return salary, salary
    except:
        pass
    
    return 0, 0

def extract_band(title, salary_text):
    """Extract NHS band from title or salary"""
    text = f"{title} {salary_text}".lower()
    
    for band_num in range(2, 9):
        if f'band {band_num}' in text or f'band{band_num}' in text:
            return f'Band {band_num}'
    
    return 'Not specified'

def parse_closing_date(closing_text):
    """Parse closing date from text"""
    try:
        # Look for date patterns
        if 'today' in closing_text.lower():
            return datetime.now().isoformat()
        elif 'tomorrow' in closing_text.lower():
            return (datetime.now() + timedelta(days=1)).isoformat()
        else:
            # Try to extract date
            date_match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', closing_text)
            if date_match:
                day = int(date_match.group(1))
                month_name = date_match.group(2)
                year = int(date_match.group(3))
                
                months = {
                    'january': 1, 'february': 2, 'march': 3, 'april': 4,
                    'may': 5, 'june': 6, 'july': 7, 'august': 8,
                    'september': 9, 'october': 10, 'november': 11, 'december': 12
                }
                
                month = months.get(month_name.lower(), 1)
                return datetime(year, month, day).isoformat()
    except:
        pass
    
    # Default to 14 days from now
    return (datetime.now() + timedelta(days=14)).isoformat()

def check_sponsorship(job_url):
    """Check if job offers visa sponsorship"""
    try:
        response = requests.get(job_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        content = soup.get_text().lower()
        
        # Look for sponsorship keywords
        sponsorship_keywords = ['visa sponsorship', 'tier 2 sponsorship', 'skilled worker visa', 
                               'certificate of sponsorship', 'sponsor license']
        
        for keyword in sponsorship_keywords:
            if keyword in content:
                return True
        
        return False
    except:
        return False

def matches_criteria(title, location, band, target_locations, target_bands, requires_sponsorship, sponsorship_available):
    """Check if job matches student criteria"""
    
    # Check location
    if target_locations:
        location_match = any(loc.lower() in location.lower() for loc in target_locations)
        if not location_match:
            return False
    
    # Check band
    if target_bands:
        band_match = any(b.lower() in band.lower() for b in target_bands)
        if not band_match:
            return False
    
    # Check sponsorship
    if requires_sponsorship and not sponsorship_available:
        return False
    
    return True

def scrape_jobs_for_all_students():
    """Scrape jobs for all active students"""
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return
    
    try:
        # Get all active students
        students = supabase.table('student_automation_settings').select('*, users(email)').eq('status', 'active').execute()
        
        if not students.data:
            print("ℹ️ No active students found")
            return
        
        print(f"🔍 Scraping jobs for {len(students.data)} students")
        
        total_jobs = 0
        
        for student in students.data:
            print(f"\n👤 Processing: {student.get('users', {}).get('email', 'Unknown')}")
            
            # Extract preferences
            locations = student.get('preferred_locations', [])
            bands = student.get('preferred_bands', [])
            requires_sponsorship = student.get('requires_sponsorship', False)
            
            # Scrape jobs
            jobs = scrape_nhs_jobs(
                locations=locations,
                bands=bands,
                requires_sponsorship=requires_sponsorship
            )
            
            total_jobs += len(jobs)
        
        print(f"\n✅ COMPLETE: Found {total_jobs} new jobs across all students")
    
    except Exception as e:
        print(f"❌ Error scraping for all students: {str(e)}")

if __name__ == "__main__":
    print("🚀 NHS Jobs Scraper Engine")
    print("=" * 50)
    scrape_jobs_for_all_students()
