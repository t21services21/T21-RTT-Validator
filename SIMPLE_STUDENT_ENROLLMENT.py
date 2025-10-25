"""
SIMPLE STUDENT ENROLLMENT SYSTEM
One function to enroll any student in Level 3 (or any course)
Works even if module isn't deployed yet!

Usage:
    python SIMPLE_STUDENT_ENROLLMENT.py
    
Then follow the prompts!
"""

from supabase_database import supabase, grant_module_access
from datetime import datetime

def enroll_student_in_level3(student_email, admin_email="admin@t21services.co.uk"):
    """
    Enroll a student in Level 3 Adult Care
    Works regardless of deployment status!
    """
    
    print("=" * 60)
    print(f"ENROLLING: {student_email}")
    print("COURSE: Level 3 Diploma in Adult Care")
    print("=" * 60)
    print()
    
    success_count = 0
    error_count = 0
    
    # Step 1: Enroll in TQUK course (database)
    print("[1/4] Enrolling in TQUK course database...")
    try:
        enrollment_data = {
            "learner_email": student_email,
            "course_code": "level3_adult_care",
            "course_name": "Level 3 Diploma in Adult Care",
            "qualification_code": "610/0103/6",
            "enrollment_date": datetime.now().isoformat(),
            "status": "active",
            "assigned_by": admin_email,
            "progress": 0
        }
        
        # Check if already enrolled
        existing = supabase.table('tquk_enrollments').select('*').eq('learner_email', student_email).eq('course_code', 'level3_adult_care').execute()
        
        if existing.data:
            print("   ℹ️  Already enrolled in course (that's okay!)")
        else:
            result = supabase.table('tquk_enrollments').insert(enrollment_data).execute()
            print("   ✅ Enrolled in TQUK course!")
            success_count += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        error_count += 1
    
    print()
    
    # Step 2: Grant Level 3 module access (if it exists)
    print("[2/4] Granting Level 3 Adult Care module access...")
    try:
        result = grant_module_access(student_email, "📚 Level 3 Adult Care", admin_email)
        if result.get('success'):
            print("   ✅ Level 3 module access granted!")
            success_count += 1
        else:
            print(f"   ⚠️  Module not available yet (will work after deployment)")
    except Exception as e:
        print(f"   ⚠️  Module not available yet: {e}")
    
    print()
    
    # Step 3: Grant TQUK Document Library access
    print("[3/4] Granting TQUK Document Library access...")
    try:
        result = grant_module_access(student_email, "📚 TQUK Document Library", admin_email)
        if result.get('success'):
            print("   ✅ Document library access granted!")
            success_count += 1
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    print()
    
    # Step 4: Grant basic access modules
    print("[4/4] Granting basic access modules...")
    basic_modules = [
        "ℹ️ Help & Information",
        "⚙️ My Account",
        "📧 Contact & Support"
    ]
    
    for module in basic_modules:
        try:
            result = grant_module_access(student_email, module, admin_email)
            if result.get('success'):
                print(f"   ✅ {module}")
                success_count += 1
        except Exception as e:
            print(f"   ⚠️  {module}: {e}")
    
    print()
    print("=" * 60)
    print(f"ENROLLMENT COMPLETE!")
    print(f"✅ Success: {success_count} items")
    if error_count > 0:
        print(f"⚠️  Warnings: {error_count} items")
    print("=" * 60)
    print()
    
    return success_count > 0


def enroll_multiple_students():
    """Enroll multiple students at once"""
    
    print("=" * 60)
    print("BULK STUDENT ENROLLMENT - LEVEL 3 ADULT CARE")
    print("=" * 60)
    print()
    
    # Get admin email
    admin_email = input("Your email (admin): ").strip()
    if not admin_email:
        admin_email = "admin@t21services.co.uk"
    
    print()
    print("Enter student emails (one per line)")
    print("Press Enter twice when done:")
    print()
    
    students = []
    while True:
        email = input("Student email: ").strip()
        if not email:
            break
        students.append(email)
    
    if not students:
        print("No students entered!")
        return
    
    print()
    print(f"Enrolling {len(students)} students...")
    print()
    
    success = 0
    for i, student_email in enumerate(students, 1):
        print(f"\n[{i}/{len(students)}]")
        if enroll_student_in_level3(student_email, admin_email):
            success += 1
        print()
    
    print("=" * 60)
    print(f"BULK ENROLLMENT COMPLETE!")
    print(f"Successfully enrolled: {success}/{len(students)} students")
    print("=" * 60)
    print()
    print("Tell students to:")
    print("1. Refresh their page (Ctrl+Shift+R)")
    print("2. Look for 'Level 3 Adult Care' in sidebar")
    print("3. If not there yet, wait for deployment (5-10 minutes)")
    print("=" * 60)


def main():
    """Main menu"""
    
    print()
    print("=" * 60)
    print("     SIMPLE STUDENT ENROLLMENT SYSTEM")
    print("=" * 60)
    print()
    print("Choose an option:")
    print()
    print("1. Enroll ONE student in Level 3")
    print("2. Enroll MULTIPLE students in Level 3")
    print("3. Exit")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print()
        student_email = input("Student email: ").strip()
        admin_email = input("Your email (admin): ").strip()
        
        if not admin_email:
            admin_email = "admin@t21services.co.uk"
        
        print()
        enroll_student_in_level3(student_email, admin_email)
        
        print()
        print("Tell the student to:")
        print("1. Refresh their page (Ctrl+Shift+R)")
        print("2. Look for 'Level 3 Adult Care' in sidebar")
        print("3. Click on it to access course materials")
        print()
        
    elif choice == "2":
        enroll_multiple_students()
        
    elif choice == "3":
        print("Goodbye!")
        return
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
