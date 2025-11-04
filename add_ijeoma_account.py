"""
EMERGENCY FIX - ADD IJEOMA'S ACCOUNT
Run this to create her account in the local database
"""

from student_auth import register_student
from datetime import datetime, timedelta

def add_ijeoma():
    """Add Ijeoma's account"""
    
    email = "ijeoma234@gmail.com"
    password = "aHDzC1AwR"  # The password she's using
    full_name = "Ijeoma"
    
    print("=" * 50)
    print("ADDING IJEOMA'S ACCOUNT")
    print("=" * 50)
    print()
    print(f"Email: {email}")
    print(f"Name: {full_name}")
    print()
    
    # Register with professional license (6 months, unlimited access)
    try:
        success, message, license_obj = register_student(
            email=email,
            password=password,
            full_name=full_name,
            role="professional"  # Professional: 6 months, unlimited features
        )
        
        if success:
            print("✅ SUCCESS!")
            print(f"   {message}")
            print()
            print("Account Details:")
            print(f"   Email: {email}")
            print(f"   License: Full Access")
            print(f"   Expiry: {license_obj.expiry_date.strftime('%d/%m/%Y')}")
            print()
            print("Tell Ijeoma:")
            print("   1. Go to login page")
            print("   2. Enter email: ijeoma234@gmail.com")
            print("   3. Enter password: aHDzC1AwR")
            print("   4. Click 'Login to Training'")
            print()
        else:
            print(f"❌ ERROR: {message}")
            print()
            print("This might mean:")
            print("   - Account already exists")
            print("   - Database connection issue")
            print()
            print("Try resetting her password instead!")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        print()
        print("There was an error creating the account.")
    
    print("=" * 50)

if __name__ == "__main__":
    add_ijeoma()
