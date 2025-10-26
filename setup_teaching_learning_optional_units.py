"""
Setup script for Teaching and Learning Optional Units
Registers all optional units in the database for Level 3 Certificate in Supporting Teaching and Learning in Schools
"""

from supabase_client import get_supabase_client

COURSE_ID = "level3_teaching_learning"

# Optional units data
OPTIONAL_UNITS_DATA = [
    {
        "course_id": COURSE_ID,
        "unit_number": 4,
        "unit_name": "Support children and young people's health and safety",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "Health & Safety",
        "description": "Understand health and safety legislation, maintain safe environments, and respond to accidents and emergencies"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 5,
        "unit_name": "Understand child and young person development",
        "credits": 4,
        "learning_outcomes": 5,
        "category": "Child Development",
        "description": "Understand expected patterns of development, factors affecting development, and how to monitor development"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 6,
        "unit_name": "Support assessment for learning",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "Teaching Support",
        "description": "Understand assessment for learning, support assessment activities, and provide feedback to learners"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 7,
        "unit_name": "Support literacy and numeracy activities",
        "credits": 4,
        "learning_outcomes": 5,
        "category": "Teaching Support",
        "description": "Support literacy development, numeracy development, and use of ICT to support learning"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 8,
        "unit_name": "Support children and young people's positive behaviour",
        "credits": 3,
        "learning_outcomes": 4,
        "category": "Behaviour Management",
        "description": "Understand policies and procedures, support positive behaviour, and respond to challenging behaviour"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 9,
        "unit_name": "Safeguarding and protection of children and young people",
        "credits": 3,
        "learning_outcomes": 5,
        "category": "Safeguarding",
        "description": "Understand safeguarding legislation, recognize signs of abuse, and respond to concerns appropriately"
    },
    {
        "course_id": COURSE_ID,
        "unit_number": 10,
        "unit_name": "Support children and young people with disabilities and special educational needs",
        "credits": 4,
        "learning_outcomes": 5,
        "category": "SEND Support",
        "description": "Understand types of disabilities and SEN, support inclusive practice, and work with families and professionals"
    }
]

def setup_optional_units():
    """Register all optional units in database"""
    supabase = get_supabase_client()
    if not supabase:
        print("ERROR: Could not connect to database")
        return False
    
    print(f"Setting up {len(OPTIONAL_UNITS_DATA)} optional units for Teaching and Learning...")
    
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
    print("TEACHING AND LEARNING OPTIONAL UNITS SETUP")
    print("=" * 80)
    print()
    
    success = setup_optional_units()
    
    print()
    print("=" * 80)
    if success:
        print("ALL OPTIONAL UNITS REGISTERED SUCCESSFULLY!")
        print()
        print("Students can now:")
        print("1. View all optional units in the Optional Units tab")
        print("2. Select units to reach minimum 30 credits")
        print("3. Study selected units in Learning Materials tab")
        print("4. Submit evidence for selected units")
    else:
        print("SOME UNITS FAILED TO REGISTER")
        print("Check error messages above and try again")
    print("=" * 80)
