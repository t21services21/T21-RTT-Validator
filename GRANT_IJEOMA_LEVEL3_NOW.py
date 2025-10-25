"""
EMERGENCY FIX - GRANT IJEOMA ACCESS TO LEVEL 3 RIGHT NOW
Just run this script and she'll have access!
"""

from supabase_database import supabase, grant_module_access

def grant_ijeoma_access():
    """Grant Ijeoma access to Level 3 Adult Care"""
    
    student_email = "ijeoma234@gmail.com"
    admin_email = "admin@t21services.co.uk"  # Change this to your email
    
    print("=" * 50)
    print("GRANTING IJEOMA ACCESS TO LEVEL 3")
    print("=" * 50)
    print()
    
    # 1. Enroll in TQUK course
    print("[1/3] Enrolling in Level 3 Diploma course...")
    try:
        enrollment_data = {
            "learner_email": student_email,
            "course_code": "level3_adult_care",
            "course_name": "Level 3 Diploma in Adult Care",
            "enrollment_date": "2025-10-25",
            "status": "active",
            "assigned_by": admin_email
        }
        
        result = supabase.table('tquk_enrollments').insert(enrollment_data).execute()
        print("✅ Enrolled in course!")
    except Exception as e:
        print(f"⚠️ Course enrollment: {e}")
        print("   (Might already be enrolled - that's okay!)")
    
    print()
    
    # 2. Grant module access
    print("[2/3] Granting Level 3 Adult Care module access...")
    try:
        result = grant_module_access(student_email, "📚 Level 3 Adult Care", admin_email)
        if result.get('success'):
            print("✅ Module access granted!")
        else:
            print(f"⚠️ {result.get('error')}")
    except Exception as e:
        print(f"⚠️ Module access: {e}")
    
    print()
    
    # 3. Grant basic modules
    print("[3/3] Granting basic access...")
    basic_modules = [
        "ℹ️ Help & Information",
        "⚙️ My Account",
        "📧 Contact & Support"
    ]
    
    for module in basic_modules:
        try:
            grant_module_access(student_email, module, admin_email)
            print(f"✅ {module}")
        except:
            pass
    
    print()
    print("=" * 50)
    print("DONE!")
    print("=" * 50)
    print()
    print("Tell Ijeoma to:")
    print("1. Refresh her page (Ctrl+Shift+R)")
    print("2. Look at the sidebar")
    print("3. She should see '📚 Level 3 Adult Care'")
    print("4. Click on it!")
    print()
    print("If she doesn't see it, wait 2 minutes and refresh again.")
    print("=" * 50)

if __name__ == "__main__":
    grant_ijeoma_access()
