"""
Setup script to register Level 2 Business Admin optional units in database
Run this once to populate the tquk_optional_units table
"""

from supabase_client import get_supabase_client

COURSE_ID = "level2_business_admin"

OPTIONAL_UNITS_DATA = [
    {
        "course_id": COURSE_ID,
        "unit_number": 6,
        "unit_name": "Principles of business administrative tasks",
        "credits": 3,
        "learning_outcomes": 5,
        "category": "core_admin",
        "description": "Essential administrative tasks for business operations"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 7,
        "unit_name": "Understand how to prepare text",
        "credits": 2,
        "learning_outcomes": 4,
        "category": "documentation",
        "description": "Text preparation and formatting skills"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 8,
        "unit_name": "Administrative support for meetings",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "core_admin",
        "description": "Organize and support business meetings"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 9,
        "unit_name": "Store, retrieve and archive information",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "information_management",
        "description": "Information management and archiving"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 10,
        "unit_name": "Customer service environment",
        "credits": 2,
        "learning_outcomes": 3,
        "category": "customer_service",
        "description": "Understanding customer service principles"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 11,
        "unit_name": "Use of research in business",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "business_skills",
        "description": "Research methods for business decisions"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 12,
        "unit_name": "Customer relationships",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "customer_service",
        "description": "Building and maintaining customer relationships"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 13,
        "unit_name": "Marketing theory",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "marketing",
        "description": "Fundamental marketing concepts and theory"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 14,
        "unit_name": "Exploring social media",
        "credits": 2,
        "learning_outcomes": 3,
        "category": "digital",
        "description": "Social media platforms and business use"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 15,
        "unit_name": "Safe use of online platforms",
        "credits": 2,
        "learning_outcomes": 3,
        "category": "digital",
        "description": "Online safety and security practices"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 16,
        "unit_name": "Equality and diversity",
        "credits": 2,
        "learning_outcomes": 3,
        "category": "professional_development",
        "description": "Understanding equality and diversity in workplace"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 17,
        "unit_name": "Digital marketing",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "marketing",
        "description": "Digital marketing strategies and tools"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 18,
        "unit_name": "Team leading",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "leadership",
        "description": "Leadership and team management skills"
    }
]

def setup_optional_units():
    """Register all optional units in database"""
    supabase = get_supabase_client()
    if not supabase:
        print("ERROR: Could not connect to database")
        return False
    
    print(f"Setting up {len(OPTIONAL_UNITS_DATA)} optional units for Business Admin...")
    
    # First, delete existing units for this course (in case of re-run)
    try:
        supabase.table('tquk_optional_units').delete().eq('course_id', COURSE_ID).execute()
        print("SUCCESS: Cleared existing units")
    except Exception as e:
        print(f"WARNING: Error clearing existing units: {e}")
    
    # Insert all units
    success_count = 0
    for unit in OPTIONAL_UNITS_DATA:
        try:
            supabase.table('tquk_optional_units').insert(unit).execute()
            print(f"SUCCESS: Added Unit {unit['unit_number']}: {unit['unit_name']}")
            success_count += 1
        except Exception as e:
            print(f"ERROR: Failed to add Unit {unit['unit_number']}: {e}")
    
    print(f"\nSetup complete! {success_count}/{len(OPTIONAL_UNITS_DATA)} units registered")
    return success_count == len(OPTIONAL_UNITS_DATA)

if __name__ == "__main__":
    setup_optional_units()
