"""
Adzuna API Job Scraper
Adzuna aggregates jobs from multiple sources including NHS Jobs
FREE API with 1000 calls/month
"""

import requests
from datetime import datetime, timedelta
from supabase_database import supabase, SUPABASE_AVAILABLE

# Adzuna API credentials - stored in Streamlit secrets for security
import streamlit as st

try:
    ADZUNA_APP_ID = st.secrets.get("ADZUNA_APP_ID", "cf57c7f2")
    ADZUNA_API_KEY = st.secrets.get("ADZUNA_API_KEY", "4cdfb41b7400cbcee24a3f9c424a4166")
except:
    # Fallback if not in Streamlit context
    ADZUNA_APP_ID = "cf57c7f2"
    ADZUNA_API_KEY = "4cdfb41b7400cbcee24a3f9c424a4166"

def scrape_jobs_adzuna(keywords=None, location='London', max_results=20):
    """
    Get NHS jobs from Adzuna API
    
    Adzuna aggregates jobs from NHS Jobs and other sources
    FREE tier: 1000 API calls per month
    
    Sign up: https://developer.adzuna.com/
    """
    
    if not SUPABASE_AVAILABLE or supabase is None:
        print("❌ Supabase not available")
        return []
    
    # Check if API credentials are configured
    if ADZUNA_APP_ID == "YOUR_APP_ID" or ADZUNA_API_KEY == "YOUR_API_KEY":
        print("⚠️ Adzuna API not configured!")
        print("📝 Sign up at: https://developer.adzuna.com/")
        print("💡 Add your APP_ID and API_KEY to this file")
        return []
    
    discovered_jobs = []
    
    # Build search query - use broader terms first
    if keywords:
        # Try each keyword separately, then combine
        search_queries = [
            'NHS ' + ' '.join(keywords[:2]),  # NHS + first 2 keywords
            'NHS administrator',  # Broad NHS admin search
            ' '.join(keywords),  # All keywords
        ]
    else:
        search_queries = ['NHS administrator', 'NHS pathway', 'NHS validation']
    
    # Try multiple search strategies
    all_jobs = []
    
    for search_query in search_queries:
        # Adzuna API endpoint
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
        
        params = {
            'app_id': ADZUNA_APP_ID,
            'app_key': ADZUNA_API_KEY,
            'results_per_page': max_results,
            'what': search_query,
            'where': location,
            'category': 'healthcare-nursing-jobs',  # Filter for healthcare
            'sort_by': 'date'
        }
    
        try:
            print(f"🔍 Searching Adzuna for: {search_query} in {location}")
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"⚠️ Search '{search_query}' failed: {response.status_code}")
                continue
            
            data = response.json()
            results = data.get('results', [])
            
            print(f"✅ Found {len(results)} jobs for '{search_query}'")
        
        for job in results:
            try:
                title = job.get('title', 'Unknown')
                company = job.get('company', {}).get('display_name', 'NHS Trust')
                location_text = job.get('location', {}).get('display_name', location)
                description = job.get('description', '')
                job_url = job.get('redirect_url', '')
                
                # Extract salary
                salary_min = int(job.get('salary_min', 0)) if job.get('salary_min') else 0
                salary_max = int(job.get('salary_max', 0)) if job.get('salary_max') else 0
                
                # Extract band from title or description
                band = "Not specified"
                for band_num in range(2, 9):
                    if f'band {band_num}' in title.lower() or f'band {band_num}' in description.lower():
                        band = f'Band {band_num}'
                        break
                
                # Generate job reference
                job_id = job.get('id', '')
                job_reference = f"ADZUNA-{job_id}" if job_id else f"ADZUNA-{int(datetime.now().timestamp())}"
                
                # Get created date
                created_date = job.get('created', datetime.now().isoformat())
                
                # Create job data
                job_data = {
                    'title': title,
                    'trust': company,
                    'location': location_text,
                    'band': band,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'closing_date': (datetime.now() + timedelta(days=30)).isoformat(),
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
                        print(f"✅ Added: {title} at {company}")
            
                except Exception as e:
                    print(f"⚠️ Error processing job: {str(e)}")
                    continue
            
            # Break if we found enough jobs
            if len(discovered_jobs) >= max_results:
                break
        
        except Exception as e:
            print(f"⚠️ Search error for '{search_query}': {str(e)}")
            continue
    
    if discovered_jobs:
        print(f"\n🎉 SUCCESS! Added {len(discovered_jobs)} jobs from Adzuna")
    else:
        print(f"\n❌ No jobs found. Tried {len(search_queries)} different searches.")
    
    return discovered_jobs

if __name__ == "__main__":
    print("🚀 Adzuna Job Scraper")
    print("=" * 60)
    print("📝 FREE API - Sign up at: https://developer.adzuna.com/")
    print("=" * 60)
    jobs = scrape_jobs_adzuna(keywords=['RTT', 'Validation', 'NHS'], location='London')
    print(f"\n📊 Total jobs found: {len(jobs)}")
