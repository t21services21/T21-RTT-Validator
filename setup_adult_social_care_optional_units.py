"""
Setup script for Adult Social Care Optional Units
Registers all optional units in the database for Level 2 Certificate in Preparing to Work in Adult Social Care
"""

from supabase_client import get_supabase_client

COURSE_ID = "level2_adult_social_care"

# Optional units data
OPTIONAL_UNITS_DATA = [
    {
        "course_id": COURSE_ID,
        "unit_number": 6,
        "unit_name": "The role of the health and social care worker",
        "credits": 2,
        "learning_outcomes": 3,
        "category": "Core Skills",
        "description": "Understand the working relationship in health and social care, work in ways that are agreed with the employer, and work in partnership with others"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 7,
        "unit_name": "Understand how to handle information in social care settings",
        "credits": 1,
        "learning_outcomes": 2,
        "category": "Core Skills",
        "description": "Understand the need for secure handling of information and know how to access support for handling information"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 8,
        "unit_name": "Understand person centred approaches in adult social care settings",
        "credits": 3,
        "learning_outcomes": 5,
        "category": "Person-Centred Care",
        "description": "Understand person centred approaches, working in a person centred way, consent, active participation, and supporting individual rights"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 9,
        "unit_name": "Understand the context of supporting individuals with learning disabilities",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "Specialist Care",
        "description": "Understand models of disability, legislation and policies, and the meaning of learning disability"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 10,
        "unit_name": "Understand physical disability",
        "credits": 3,
        "learning_outcomes": 5,
        "category": "Specialist Care",
        "description": "Understand the importance of differentiating between conditions and the impact of living with physical disability"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 11,
        "unit_name": "Understand mental health problems",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "Specialist Care",
        "description": "Understand the main forms of mental ill health, factors that may influence mental health, and the impact on individuals and others"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 12,
        "unit_name": "Understand dementia",
        "credits": 2,
        "learning_outcomes": 4,
        "category": "Specialist Care",
        "description": "Understand what dementia is, types of dementia, and factors that may reduce the risk of dementia"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 13,
        "unit_name": "Understand the administration of medication to individuals with dementia",
        "credits": 2,
        "learning_outcomes": 4,
        "category": "Specialist Care",
        "description": "Understand legislation, policies and procedures, types of medication, and common adverse reactions"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 14,
        "unit_name": "Understand the nutritional needs that are unique to individuals with dementia",
        "credits": 2,
        "learning_outcomes": 4,
        "category": "Specialist Care",
        "description": "Understand factors affecting nutritional needs, importance of good nutrition, and support for eating and drinking"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 15,
        "unit_name": "Understand health and safety in social care settings",
        "credits": 3,
        "learning_outcomes": 6,
        "category": "Health & Safety",
        "description": "Understand legislation, responsibilities, risk assessment, hazardous substances, infection control, and moving and handling"
    }
]

def setup_optional_units():
    """Register all optional units in database"""
    supabase = get_supabase_client()
    if not supabase:
        print("ERROR: Could not connect to database")
        return False
    
    print(f"Setting up {len(OPTIONAL_UNITS_DATA)} optional units for Adult Social Care...")
    
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
    print("=" * 80)
    print("ADULT SOCIAL CARE OPTIONAL UNITS SETUP")
    print("=" * 80)
    print()
    
    success = setup_optional_units()
    
    print()
    print("=" * 80)
    if success:
        print("✅ ALL OPTIONAL UNITS REGISTERED SUCCESSFULLY!")
        print()
        print("Students can now:")
        print("1. View all optional units in the Optional Units tab")
        print("2. Select units to reach minimum 19 credits")
        print("3. Study selected units in Learning Materials tab")
        print("4. Submit evidence for selected units")
    else:
        print("⚠️ SOME UNITS FAILED TO REGISTER")
        print("Check error messages above and try again")
    print("=" * 80)
