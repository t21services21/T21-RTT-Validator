"""
DIAGNOSTIC SCRIPT - CHECK IJEOMA'S ACCESS
Run this to see exactly what's wrong
"""

from supabase_database import supabase, get_user_modules
from tquk_course_assignment import get_learner_enrollments

# Ijeoma's email
IJEOMA_EMAIL = "ijeoma234@gmail.com"

print("=" * 60)
print("DIAGNOSTIC REPORT FOR IJEOMA")
print("=" * 60)
print()

# Check 1: User exists
print("CHECK 1: Does user exist in database?")
try:
    result = supabase.table('users').select('*').eq('email', IJEOMA_EMAIL).execute()
    if result.data:
        user = result.data[0]
        print(f"✅ YES - User found")
        print(f"   Name: {user.get('full_name')}")
        print(f"   Role: {user.get('role')}")
        print(f"   Status: {user.get('status')}")
        print(f"   User Type: {user.get('user_type')}")
    else:
        print(f"❌ NO - User not found!")
except Exception as e:
    print(f"❌ ERROR: {e}")
print()

# Check 2: Module access
print("CHECK 2: What modules does she have access to?")
try:
    modules = get_user_modules(IJEOMA_EMAIL)
    if modules:
        print(f"✅ Has {len(modules)} modules:")
        for module in modules:
            print(f"   - {module}")
        
        # Check specifically for Level 3
        if "📚 Level 3 Adult Care" in modules:
            print()
            print("✅ HAS Level 3 Adult Care module!")
        else:
            print()
            print("❌ MISSING Level 3 Adult Care module!")
    else:
        print(f"❌ NO modules assigned!")
except Exception as e:
    print(f"❌ ERROR: {e}")
print()

# Check 3: TQUK enrollment
print("CHECK 3: Is she enrolled in Level 3 course?")
try:
    enrollments = get_learner_enrollments(IJEOMA_EMAIL)
    if enrollments:
        print(f"✅ Has {len(enrollments)} course enrollments:")
        for enrollment in enrollments:
            print(f"   - {enrollment.get('course_name')} (ID: {enrollment.get('course_id')})")
            print(f"     Status: {enrollment.get('status')}")
            print(f"     Progress: {enrollment.get('progress')}%")
        
        # Check specifically for Level 3
        level3_enrolled = any(e.get('course_id') == 'level3_adult_care' for e in enrollments)
        print()
        if level3_enrolled:
            print("✅ ENROLLED in Level 3 Adult Care!")
        else:
            print("❌ NOT ENROLLED in Level 3 Adult Care!")
    else:
        print(f"❌ NO course enrollments!")
except Exception as e:
    print(f"❌ ERROR: {e}")
print()

# Check 4: Module access table
print("CHECK 4: Raw module_access table check")
try:
    result = supabase.table('module_access').select('*').eq('user_email', IJEOMA_EMAIL).execute()
    if result.data:
        print(f"✅ Found {len(result.data)} module access records:")
        for record in result.data:
            print(f"   - {record.get('module_name')}")
            print(f"     Granted by: {record.get('granted_by')}")
            print(f"     Granted at: {record.get('granted_at')}")
            print(f"     Status: {record.get('status', 'active')}")
    else:
        print(f"❌ NO module access records!")
except Exception as e:
    print(f"❌ ERROR: {e}")
print()

# Check 5: TQUK enrollments table
print("CHECK 5: Raw tquk_enrollments table check")
try:
    result = supabase.table('tquk_enrollments').select('*').eq('learner_email', IJEOMA_EMAIL).execute()
    if result.data:
        print(f"✅ Found {len(result.data)} enrollment records:")
        for record in result.data:
            print(f"   - Course: {record.get('course_name')}")
            print(f"     Course ID: {record.get('course_id')}")
            print(f"     Status: {record.get('status')}")
            print(f"     Assigned by: {record.get('assigned_by')}")
            print(f"     Assigned date: {record.get('assigned_date')}")
    else:
        print(f"❌ NO enrollment records!")
except Exception as e:
    print(f"❌ ERROR: {e}")
print()

# DIAGNOSIS
print("=" * 60)
print("DIAGNOSIS:")
print("=" * 60)

try:
    modules = get_user_modules(IJEOMA_EMAIL)
    enrollments = get_learner_enrollments(IJEOMA_EMAIL)
    
    has_module = modules and "📚 Level 3 Adult Care" in modules
    has_enrollment = enrollments and any(e.get('course_id') == 'level3_adult_care' for e in enrollments)
    
    if has_module and has_enrollment:
        print("✅ EVERYTHING LOOKS GOOD!")
        print("   She has both module access AND course enrollment.")
        print("   Problem might be:")
        print("   1. Browser cache - ask her to clear cache")
        print("   2. Mobile display issue - ask her to use computer")
        print("   3. Tab not visible - ask her to scroll tabs")
    elif has_module and not has_enrollment:
        print("⚠️ PARTIAL SETUP!")
        print("   She has module access but NOT enrolled in course.")
        print("   FIX: Go to TQUK Course Assignment and enroll her")
    elif not has_module and has_enrollment:
        print("⚠️ PARTIAL SETUP!")
        print("   She is enrolled but doesn't have module access.")
        print("   FIX: Go to simple_course_assignment and assign Level 3")
    else:
        print("❌ NOTHING SET UP!")
        print("   She has neither module access nor course enrollment.")
        print("   FIX:")
        print("   1. Go to TQUK Course Assignment")
        print("   2. Select Ijeoma")
        print("   3. Tick 'Level 3 Diploma in Adult Care'")
        print("   4. Click 'Assign Selected'")
except Exception as e:
    print(f"❌ ERROR during diagnosis: {e}")

print()
print("=" * 60)
print("END OF DIAGNOSTIC REPORT")
print("=" * 60)
