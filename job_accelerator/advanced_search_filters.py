"""
ADVANCED SEARCH FILTERS
Comprehensive filtering system for job searches
Handles sponsorship, location, keywords, bands, work type, etc.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class WorkType(Enum):
    """Work location type"""
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    ANY = "any"

class NHSBand(Enum):
    """NHS Pay Bands"""
    BAND_2 = "Band 2"
    BAND_3 = "Band 3"
    BAND_4 = "Band 4"
    BAND_5 = "Band 5"
    BAND_6 = "Band 6"
    BAND_7 = "Band 7"
    BAND_8A = "Band 8A"
    BAND_8B = "Band 8B"
    ANY = "Any Band"

@dataclass
class JobSearchFilters:
    """
    Comprehensive job search filters
    
    CRITICAL FEATURES:
    1. Sponsorship filtering (for international students)
    2. Location-based search (city, postcode, radius)
    3. Multiple keywords (different ways to describe same role)
    4. NHS Band filtering (pay grade)
    5. Work type (remote, hybrid, onsite)
    6. Salary range
    7. Contract type
    """
    
    # Sponsorship (CRITICAL for visa holders!)
    requires_sponsorship: bool = False  # Student needs visa sponsorship
    sponsorship_keywords: List[str] = None  # Keywords indicating sponsorship
    
    # Location
    cities: List[str] = None  # Target cities
    postcode: str = None  # Search from postcode
    radius_miles: int = 25  # Search radius in miles
    regions: List[str] = None  # UK regions (e.g., London, North West)
    
    # Keywords (MULTIPLE variations for same role)
    primary_keywords: List[str] = None  # Main job titles
    alternative_keywords: List[str] = None  # Alternative terms
    exclude_keywords: List[str] = None  # Words to avoid
    
    # NHS Specific
    nhs_bands: List[str] = None  # Target NHS bands
    nhs_trusts: List[str] = None  # Specific NHS trusts only
    
    # Work Type
    work_types: List[WorkType] = None  # Remote, hybrid, onsite
    
    # Employment Details
    min_salary: int = None
    max_salary: int = None
    contract_types: List[str] = None  # Full-time, Part-time, Contract, etc.
    min_hours_per_week: int = None
    
    # Experience Level
    entry_level_only: bool = False
    exclude_senior_roles: bool = True  # Exclude "Senior", "Lead", "Manager"
    
    # Job Boards
    preferred_boards: List[str] = None  # Prioritize certain boards
    
    def __post_init__(self):
        """Initialize default values"""
        if self.sponsorship_keywords is None:
            self.sponsorship_keywords = [
                "certificate of sponsorship",
                "cos",
                "visa sponsorship",
                "right to work",
                "work visa",
                "tier 2",
                "skilled worker visa",
                "sponsorship available",
                "we can sponsor"
            ]
        
        if self.primary_keywords is None:
            self.primary_keywords = ["RTT Validator", "Hospital Administrator"]
        
        if self.alternative_keywords is None:
            self.alternative_keywords = [
                "RTT Coordinator",
                "Waiting List Coordinator",
                "Access Coordinator",
                "Patient Access Coordinator",
                "Outpatient Administrator",
                "Medical Secretary",
                "Booking Administrator"
            ]
        
        if self.exclude_keywords is None:
            self.exclude_keywords = [
                "Senior",
                "Lead",
                "Manager",
                "Head of",
                "Director",
                "Consultant"
            ]
        
        if self.work_types is None:
            self.work_types = [WorkType.ANY]
        
        if self.contract_types is None:
            self.contract_types = ["Full-time", "Part-time"]


class SponsorshipFilter:
    """
    Filter jobs by sponsorship availability
    
    CRITICAL: Many international students need visa sponsorship
    Jobs must explicitly state "Certificate of Sponsorship" available
    """
    
    @staticmethod
    def job_offers_sponsorship(job_description: str) -> bool:
        """
        Check if job offers visa sponsorship
        
        Keywords to look for:
        - "Certificate of Sponsorship"
        - "COS"
        - "Visa sponsorship available"
        - "We can sponsor"
        - "Right to work in UK" (sometimes indicates no sponsorship!)
        """
        description_lower = job_description.lower()
        
        # Positive indicators (offers sponsorship)
        positive_keywords = [
            "certificate of sponsorship",
            "cos available",
            "visa sponsorship available",
            "we can sponsor",
            "sponsorship provided",
            "tier 2 sponsor",
            "skilled worker sponsor"
        ]
        
        # Negative indicators (requires existing right to work)
        negative_keywords = [
            "must have right to work",
            "right to work in uk required",
            "uk work permit required",
            "no sponsorship",
            "sponsorship not available"
        ]
        
        # Check positive keywords
        has_positive = any(keyword in description_lower for keyword in positive_keywords)
        
        # Check negative keywords
        has_negative = any(keyword in description_lower for keyword in negative_keywords)
        
        if has_negative:
            return False  # Explicitly doesn't offer sponsorship
        
        if has_positive:
            return True  # Explicitly offers sponsorship
        
        # If neither, return None (unknown)
        return None  # We don't know - might need manual check
    
    @staticmethod
    def filter_jobs_by_sponsorship(jobs: List[Dict], requires_sponsorship: bool) -> List[Dict]:
        """
        Filter jobs based on sponsorship requirements
        
        If student requires_sponsorship=True:
        - Only return jobs that offer sponsorship
        - Or jobs where sponsorship status is unknown (let student decide)
        
        If student requires_sponsorship=False:
        - Return all jobs (student has right to work)
        """
        if not requires_sponsorship:
            return jobs  # Student doesn't need sponsorship, return all jobs
        
        filtered_jobs = []
        
        for job in jobs:
            description = job.get('description', '') + ' ' + job.get('requirements', '')
            sponsorship_status = SponsorshipFilter.job_offers_sponsorship(description)
            
            if sponsorship_status is True:
                # Definitely offers sponsorship
                job['sponsorship_confirmed'] = True
                filtered_jobs.append(job)
            elif sponsorship_status is None:
                # Unknown - include but flag for review
                job['sponsorship_unknown'] = True
                filtered_jobs.append(job)
            # If sponsorship_status is False, don't include job
        
        return filtered_jobs


class LocationFilter:
    """
    Filter jobs by location
    
    Features:
    - City-based search
    - Postcode + radius search
    - Region-based search
    - Remote/hybrid filtering
    """
    
    @staticmethod
    def filter_by_city(jobs: List[Dict], target_cities: List[str]) -> List[Dict]:
        """Filter jobs by city"""
        if not target_cities:
            return jobs
        
        target_cities_lower = [city.lower() for city in target_cities]
        
        filtered = []
        for job in jobs:
            job_location = job.get('location', '').lower()
            job_city = job.get('city', '').lower()
            
            # Check if any target city is in the job location
            if any(city in job_location or city in job_city for city in target_cities_lower):
                filtered.append(job)
        
        return filtered
    
    @staticmethod
    def filter_by_radius(jobs: List[Dict], postcode: str, radius_miles: int) -> List[Dict]:
        """
        Filter jobs by distance from postcode
        
        TODO: Implement geocoding and distance calculation
        For now, placeholder
        """
        # This would require geocoding API (Google Maps, Postcodes.io, etc.)
        # For MVP, we'll use city-based filtering
        return jobs
    
    @staticmethod
    def filter_by_work_type(jobs: List[Dict], work_types: List[WorkType]) -> List[Dict]:
        """Filter by work type (remote, hybrid, onsite)"""
        if WorkType.ANY in work_types:
            return jobs
        
        filtered = []
        for job in jobs:
            description = (job.get('description', '') + ' ' + 
                          job.get('title', '') + ' ' + 
                          job.get('working_pattern', '')).lower()
            
            # Check for remote
            if WorkType.REMOTE in work_types:
                if any(keyword in description for keyword in ['remote', 'work from home', 'wfh']):
                    filtered.append(job)
                    continue
            
            # Check for hybrid
            if WorkType.HYBRID in work_types:
                if 'hybrid' in description:
                    filtered.append(job)
                    continue
            
            # Check for onsite
            if WorkType.ONSITE in work_types:
                if any(keyword in description for keyword in ['on-site', 'onsite', 'office-based', 'in-office']):
                    filtered.append(job)
                    continue
                # If no mention of remote/hybrid, assume onsite
                if 'remote' not in description and 'hybrid' not in description:
                    filtered.append(job)
        
        return filtered


class NHSBandFilter:
    """
    Filter jobs by NHS Band (pay grade)
    
    NHS Bands:
    - Band 2: £22,383 - £22,383 (Support roles)
    - Band 3: £24,071 - £25,674 (Admin, some clinical support)
    - Band 4: £26,530 - £29,114 (Senior admin, some clinical)
    - Band 5: £29,970 - £36,483 (Newly qualified professionals)
    - Band 6: £33,706 - £41,659 (Experienced professionals)
    - Band 7: £43,742 - £50,056 (Senior professionals, team leaders)
    - Band 8A: £53,755 - £60,504 (Advanced practitioners, managers)
    
    RTT Validators typically: Band 3-5
    Hospital Administrators: Band 3-6
    """
    
    @staticmethod
    def extract_band_from_job(job: Dict) -> Optional[str]:
        """Extract NHS Band from job title or description"""
        text = (job.get('title', '') + ' ' + 
                job.get('description', '') + ' ' + 
                job.get('salary_text', '')).lower()
        
        # Look for "Band X" pattern
        import re
        band_pattern = r'band\s*(\d+[a-z]?)'
        match = re.search(band_pattern, text)
        
        if match:
            return f"Band {match.group(1).upper()}"
        
        return None
    
    @staticmethod
    def filter_by_bands(jobs: List[Dict], target_bands: List[str]) -> List[Dict]:
        """Filter jobs by NHS Band"""
        if not target_bands or 'Any Band' in target_bands:
            return jobs
        
        filtered = []
        for job in jobs:
            job_band = NHSBandFilter.extract_band_from_job(job)
            
            if job_band in target_bands:
                filtered.append(job)
            elif job_band is None:
                # Band not specified - include it (might be suitable)
                filtered.append(job)
        
        return filtered


class KeywordFilter:
    """
    Filter jobs by keywords with variations
    
    CRITICAL: Use MULTIPLE keyword variations for same role
    Example:
    - "RTT Validator" OR "RTT Coordinator" OR "Waiting List Coordinator"
    - Different trusts use different job titles for same role!
    """
    
    @staticmethod
    def filter_by_keywords(
        jobs: List[Dict],
        primary_keywords: List[str],
        alternative_keywords: List[str] = None,
        exclude_keywords: List[str] = None
    ) -> List[Dict]:
        """
        Filter jobs by keywords with scoring
        
        Returns jobs that match primary OR alternative keywords
        Excludes jobs with exclude_keywords
        """
        if not primary_keywords:
            return jobs
        
        alternative_keywords = alternative_keywords or []
        exclude_keywords = exclude_keywords or []
        
        filtered = []
        
        for job in jobs:
            text = (job.get('title', '') + ' ' + 
                   job.get('description', '')).lower()
            
            # Check exclude keywords first
            if any(keyword.lower() in text for keyword in exclude_keywords):
                continue  # Skip this job
            
            # Check primary keywords
            primary_match = any(keyword.lower() in text for keyword in primary_keywords)
            
            # Check alternative keywords
            alternative_match = any(keyword.lower() in text for keyword in alternative_keywords)
            
            if primary_match or alternative_match:
                # Add relevance score
                job['keyword_match'] = 'primary' if primary_match else 'alternative'
                filtered.append(job)
        
        return filtered


class AdvancedSearchEngine:
    """
    Main search engine that applies all filters
    """
    
    def __init__(self, filters: JobSearchFilters):
        self.filters = filters
    
    def search(self, all_jobs: List[Dict]) -> List[Dict]:
        """
        Apply all filters to job list
        
        Returns filtered and scored jobs
        """
        jobs = all_jobs.copy()
        
        # 1. Sponsorship filter (CRITICAL!)
        if self.filters.requires_sponsorship:
            jobs = SponsorshipFilter.filter_jobs_by_sponsorship(
                jobs, 
                self.filters.requires_sponsorship
            )
        
        # 2. Location filters
        if self.filters.cities:
            jobs = LocationFilter.filter_by_city(jobs, self.filters.cities)
        
        if self.filters.work_types:
            jobs = LocationFilter.filter_by_work_type(jobs, self.filters.work_types)
        
        # 3. NHS Band filter
        if self.filters.nhs_bands:
            jobs = NHSBandFilter.filter_by_bands(jobs, self.filters.nhs_bands)
        
        # 4. Keyword filter
        jobs = KeywordFilter.filter_by_keywords(
            jobs,
            self.filters.primary_keywords,
            self.filters.alternative_keywords,
            self.filters.exclude_keywords
        )
        
        # 5. Salary filter
        if self.filters.min_salary or self.filters.max_salary:
            jobs = self._filter_by_salary(jobs)
        
        # 6. Entry level filter
        if self.filters.entry_level_only or self.filters.exclude_senior_roles:
            jobs = self._filter_by_experience_level(jobs)
        
        return jobs
    
    def _filter_by_salary(self, jobs: List[Dict]) -> List[Dict]:
        """Filter by salary range"""
        filtered = []
        
        for job in jobs:
            salary_min = job.get('salary_min')
            salary_max = job.get('salary_max')
            
            # If salary not specified, include job
            if salary_min is None and salary_max is None:
                filtered.append(job)
                continue
            
            # Check if salary overlaps with target range
            if self.filters.min_salary and salary_max and salary_max < self.filters.min_salary:
                continue  # Too low
            
            if self.filters.max_salary and salary_min and salary_min > self.filters.max_salary:
                continue  # Too high
            
            filtered.append(job)
        
        return filtered
    
    def _filter_by_experience_level(self, jobs: List[Dict]) -> List[Dict]:
        """Filter by experience level"""
        if not self.filters.exclude_senior_roles:
            return jobs
        
        filtered = []
        
        senior_keywords = ['senior', 'lead', 'manager', 'head of', 'director', 'principal']
        
        for job in jobs:
            title_lower = job.get('title', '').lower()
            
            # Exclude if title contains senior keyword
            if not any(keyword in title_lower for keyword in senior_keywords):
                filtered.append(job)
        
        return filtered


# ============================================
# USAGE EXAMPLES
# ============================================

def create_student_search_filters(student: Dict) -> JobSearchFilters:
    """
    Create search filters based on student preferences
    """
    return JobSearchFilters(
        requires_sponsorship=student.get('requires_sponsorship', False),
        cities=student.get('target_locations', ['London', 'Manchester']),
        radius_miles=student.get('search_radius', 25),
        primary_keywords=student.get('target_roles', ['RTT Validator']),
        alternative_keywords=[
            'RTT Coordinator',
            'Waiting List Coordinator',
            'Access Coordinator'
        ],
        nhs_bands=student.get('target_bands', ['Band 3', 'Band 4', 'Band 5']),
        work_types=[WorkType.ANY],  # Accept any work type
        min_salary=student.get('min_salary', 25000),
        exclude_senior_roles=True,
        entry_level_only=student.get('experience_years', 0) < 2
    )


if __name__ == "__main__":
    # Example usage
    
    # Sample student requiring sponsorship
    student = {
        'requires_sponsorship': True,
        'target_locations': ['London', 'Birmingham'],
        'target_roles': ['RTT Validator', 'Hospital Administrator'],
        'min_salary': 26000,
        'target_bands': ['Band 4', 'Band 5']
    }
    
    # Create filters
    filters = create_student_search_filters(student)
    
    # Sample jobs
    sample_jobs = [
        {
            'title': 'RTT Validator - Band 4',
            'description': 'We offer Certificate of Sponsorship for international candidates...',
            'location': 'London',
            'salary_min': 26530,
            'salary_max': 29114
        },
        {
            'title': 'Senior RTT Manager - Band 7',
            'description': 'Must have right to work in UK...',
            'location': 'London',
            'salary_min': 43742
        },
        {
            'title': 'Waiting List Coordinator - Band 4',
            'description': 'Visa sponsorship available...',
            'location': 'Birmingham',
            'salary_min': 26530
        }
    ]
    
    # Apply filters
    engine = AdvancedSearchEngine(filters)
    filtered_jobs = engine.search(sample_jobs)
    
    print(f"Found {len(filtered_jobs)} suitable jobs out of {len(sample_jobs)}")
    for job in filtered_jobs:
        print(f"- {job['title']} in {job['location']}")
