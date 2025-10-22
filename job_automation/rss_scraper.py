"""
NHS Jobs RSS Feed Scraper
NHS Jobs provides RSS feeds for job searches - this is the OFFICIAL way to get jobs!
"""

import feedparser
import requests
from datetime import datetime, timedelta
from supabase_database import supabase, SUPABASE_AVAILABLE

def scrape_nhs_jobs_rss(keywords=None, location='London'):
    """
    Scrape NHS Jobs using their official RSS feed
    
    Args:
        keywords: List of job keywords
        location: Location to search
    
    Returns:
        List of discovered jobs
    """
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return []
    
    discovered_jobs = []
    
    # NHS Jobs RSS feed URL
    search_keywords = '+'.join(keywords) if keywords else 'RTT+Validation+Administrator'
    
    # Try multiple RSS feed formats
    rss_urls = [
        f"https://www.jobs.nhs.uk/feed/jobs?keyword={search_keywords}&location={location}",
        f"https://www.jobs.nhs.uk/xi/vacancy_feed?keyword={search_keywords}&location={location}",
        f"https://www.jobs.nhs.uk/xi/vacancy_feed?action=search&keyword={search_keywords}&location={location}&format=rss"
    ]
    
    for rss_url in rss_urls:
        try:
            print(f"🔍 Trying RSS feed: {rss_url}")
            
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            if feed.entries and len(feed.entries) > 0:
                print(f"✅ Found {len(feed.entries)} jobs in RSS feed!")
                
                for entry in feed.entries[:20]:  # Limit to 20 jobs
                    try:
                        # Extract job details from RSS entry
                        title = entry.get('title', 'Unknown')
                        job_url = entry.get('link', '')
                        description = entry.get('summary', '')
                        published = entry.get('published', '')
                        
                        # Extract trust/employer from description or title
                        trust = "NHS Trust"
                        if 'NHS' in description:
                            # Try to extract trust name
                            import re
                            trust_match = re.search(r'([A-Z][a-z]+ (?:NHS )?(?:Foundation )?Trust)', description)
                            if trust_match:
                                trust = trust_match.group(1)
                        
                        # Extract location
                        location_text = location
                        if 'location' in description.lower():
                            loc_match = re.search(r'Location[:\s]+([A-Za-z\s,]+)', description, re.IGNORECASE)
                            if loc_match:
                                location_text = loc_match.group(1).strip()
                        
                        # Extract salary
                        salary_min = 0
                        salary_max = 0
                        salary_match = re.findall(r'£([\d,]+)', description)
                        if len(salary_match) >= 2:
                            salary_min = int(salary_match[0].replace(',', ''))
                            salary_max = int(salary_match[1].replace(',', ''))
                        elif len(salary_match) == 1:
                            salary_min = salary_max = int(salary_match[0].replace(',', ''))
                        
                        # Extract band
                        band = "Not specified"
                        for band_num in range(2, 9):
                            if f'band {band_num}' in title.lower() or f'band {band_num}' in description.lower():
                                band = f'Band {band_num}'
                                break
                        
                        # Generate job reference from URL
                        job_reference = job_url.split('/')[-1] if job_url else f'RSS-{int(datetime.now().timestamp())}'
                        
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
                                print(f"✅ Added: {title}")
                    
                    except Exception as e:
                        print(f"⚠️ Error processing RSS entry: {str(e)}")
                        continue
                
                if discovered_jobs:
                    print(f"\n🎉 SUCCESS! Added {len(discovered_jobs)} jobs from RSS feed")
                    return discovered_jobs
        
        except Exception as e:
            print(f"⚠️ RSS feed failed: {str(e)}")
            continue
    
    # If RSS doesn't work, try direct API call
    print("\n🔄 RSS feeds didn't work, trying direct API...")
    
    try:
        api_url = "https://www.jobs.nhs.uk/api/vacancy/search"
        
        payload = {
            "keyword": ' '.join(keywords) if keywords else 'RTT Validation',
            "location": location,
            "distance": 20,
            "pageSize": 20
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print(f"✅ API returned {len(results)} jobs")
            
            for job in results[:20]:
                try:
                    job_data = {
                        'title': job.get('title', 'Unknown'),
                        'trust': job.get('employer', {}).get('name', 'NHS Trust'),
                        'location': job.get('location', {}).get('name', location),
                        'band': job.get('band', 'Not specified'),
                        'salary_min': job.get('salaryMin', 0),
                        'salary_max': job.get('salaryMax', 0),
                        'closing_date': job.get('closingDate', (datetime.now() + timedelta(days=14)).isoformat()),
                        'nhs_jobs_url': job.get('url', ''),
                        'job_reference': job.get('id', f'API-{int(datetime.now().timestamp())}'),
                        'discovered_at': datetime.now().isoformat()
                    }
                    
                    existing = supabase.table('discovered_jobs').select('id').eq('job_reference', job_data['job_reference']).execute()
                    
                    if not existing.data:
                        result = supabase.table('discovered_jobs').insert(job_data).execute()
                        if result.data:
                            discovered_jobs.append(result.data[0])
                            print(f"✅ Added: {job_data['title']}")
                
                except Exception as e:
                    print(f"⚠️ Error processing API job: {str(e)}")
                    continue
            
            if discovered_jobs:
                print(f"\n🎉 SUCCESS! Added {len(discovered_jobs)} jobs from API")
                return discovered_jobs
    
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
    
    print("\n❌ All methods failed to find jobs")
    return []

if __name__ == "__main__":
    print("🚀 NHS Jobs RSS/API Scraper")
    print("=" * 60)
    jobs = scrape_nhs_jobs_rss(keywords=['RTT', 'Validation', 'Administrator'], location='London')
    print(f"\n📊 Total jobs found: {len(jobs)}")
