"""
CREATE STAFF TEST ACCOUNTS
Quick script to create multiple staff accounts for testing

Usage:
    python create_staff_accounts.py
"""

import os
import sys
from datetime import datetime, timedelta

# Check if Supabase is enabled
SUPABASE_ENABLED = os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY")

def create_staff_via_supabase():
    """Create staff accounts using Supabase"""
    try:
        from supabase_database import supabase
        import bcrypt
        
        # Staff accounts to create
        staff_members = [
            {
                "email": "staff1@t21services.co.uk",
                "password": "TestStaff123!",
                "full_name": "Test Staff 1",
                "role": "staff"
            },
            {
                "email": "staff2@t21services.co.uk",
                "password": "TestStaff123!",
                "full_name": "Test Staff 2",
                "role": "staff"
            },
            {
                "email": "teacher1@t21services.co.uk",
                "password": "TestTeacher123!",
                "full_name": "Test Teacher 1",
                "role": "teacher"
            },
            {
                "email": "tester@t21services.co.uk",
                "password": "Tester123!",
                "full_name": "QA Tester",
                "role": "staff"
            }
        ]
        
        print("=" * 60)
        print("CREATING STAFF ACCOUNTS VIA SUPABASE")
        print("=" * 60)
        
        for staff in staff_members:
            print(f"\n📧 Creating: {staff['email']}")
            
            try:
                # Check if user already exists
                existing = supabase.table('users').select('*').eq('email', staff['email']).execute()
                
                if existing.data:
                    print(f"   ⚠️  Account already exists - UPDATING")
                    
                    # Update existing account
                    hashed_pw = bcrypt.hashpw(staff['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    result = supabase.table('users').update({
                        'password_hash': hashed_pw,
                        'full_name': staff['full_name'],
                        'role': staff['role'],
                        'user_type': staff['role'],
                        'status': 'active',
                        'trial_end_date': (datetime.now() + timedelta(days=365)).isoformat(),
                        'updated_at': datetime.now().isoformat()
                    }).eq('email', staff['email']).execute()
                    
                    print(f"   ✅ Updated successfully")
                else:
                    # Create new account
                    hashed_pw = bcrypt.hashpw(staff['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    result = supabase.table('users').insert({
                        'email': staff['email'],
                        'password_hash': hashed_pw,
                        'full_name': staff['full_name'],
                        'role': staff['role'],
                        'user_type': staff['role'],
                        'status': 'active',
                        'trial_end_date': (datetime.now() + timedelta(days=365)).isoformat(),
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    }).execute()
                    
                    print(f"   ✅ Created successfully")
                
                print(f"   👤 Role: {staff['role']}")
                print(f"   🔑 Password: {staff['password']}")
                
                # SEND WELCOME EMAIL
                try:
                    from email_service import send_email
                    
                    email_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #0066cc;">
                            <h1 style="color: #0066cc;">🎉 Account Created!</h1>
                            <p>Hi {staff['full_name']},</p>
                            <p>Your {staff['role']} account for the T21 RTT Platform has been created!</p>
                            
                            <div style="background: #f0f8ff; padding: 20px; margin: 20px 0; border-left: 4px solid #0066cc;">
                                <h3 style="margin-top: 0;">🔑 Login Credentials:</h3>
                                <p><strong>Email:</strong> {staff['email']}<br>
                                <strong>Password:</strong> {staff['password']}<br>
                                <strong>Role:</strong> {staff['role'].title()}</p>
                            </div>
                            
                            <h3>✅ You Have Access To:</h3>
                            <ul>
                                <li>All 55+ modules</li>
                                <li>Clinical workflows (PTL, Cancer, MDT, Booking)</li>
                                <li>Information Governance</li>
                                <li>Partial Booking List</li>
                                <li>All training content</li>
                                {'<li><strong>Admin Panel</strong></li>' if staff['role'] == 'admin' else ''}
                            </ul>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="https://t21-healthcare-platform.streamlit.app" 
                                   style="background: #0066cc; color: white; padding: 15px 30px; 
                                          text-decoration: none; border-radius: 5px; display: inline-block; 
                                          font-weight: bold;">
                                    🚀 LOGIN NOW
                                </a>
                            </div>
                            
                            <p>Best regards,<br><strong>T21 Services Team</strong></p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    send_email(
                        to_email=staff['email'],
                        subject=f"🎉 Account Created - T21 Platform ({staff['role'].title()})",
                        html_content=email_content
                    )
                    
                    print(f"   ✅ Welcome email sent to {staff['email']}")
                
                except Exception as email_error:
                    print(f"   ⚠️  Email not sent: {email_error}")
                
                # CREATE NOTIFICATION
                try:
                    from notification_system import create_notification, NotificationType, NotificationPriority
                    
                    create_notification(
                        user_email=staff['email'],
                        title=f"👤 {staff['role'].title()} Account Ready!",
                        message=f"Your account is ready. You have access to all modules for testing. Happy testing!",
                        notification_type=NotificationType.SUCCESS,
                        priority=NotificationPriority.HIGH,
                        send_email=False,  # Already sent above
                        action_url="/",
                        action_label="Start Testing"
                    )
                    
                    print(f"   ✅ Notification created")
                
                except Exception as notif_error:
                    print(f"   ⚠️  Notification not created: {notif_error}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print("\n" + "=" * 60)
        print("STAFF ACCOUNTS READY FOR TESTING!")
        print("=" * 60)
        print("\n📋 LOGIN CREDENTIALS:")
        print("-" * 60)
        for staff in staff_members:
            print(f"Email:    {staff['email']}")
            print(f"Password: {staff['password']}")
            print(f"Role:     {staff['role']}")
            print("-" * 60)
        
        print("\n✅ All staff can now login and test ALL features!")
        print("🔓 Staff and teachers have access to ALL modules")
        
    except ImportError:
        print("❌ Error: Supabase not configured")
        print("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
        return False
    except Exception as e:
        print(f"❌ Error creating accounts: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def create_staff_via_local():
    """Create staff accounts using local file system"""
    try:
        from user_license_system import UserLicense, save_user_license
        import bcrypt
        
        print("=" * 60)
        print("CREATING STAFF ACCOUNTS LOCALLY")
        print("=" * 60)
        
        staff_members = [
            {
                "email": "staff1@t21services.co.uk",
                "password": "TestStaff123!",
                "full_name": "Test Staff 1",
                "role": "staff"
            },
            {
                "email": "staff2@t21services.co.uk",
                "password": "TestStaff123!",
                "full_name": "Test Staff 2",
                "role": "staff"
            },
            {
                "email": "teacher1@t21services.co.uk",
                "password": "TestTeacher123!",
                "full_name": "Test Teacher 1",
                "role": "teacher"
            },
            {
                "email": "tester@t21services.co.uk",
                "password": "Tester123!",
                "full_name": "QA Tester",
                "role": "staff"
            }
        ]
        
        for staff in staff_members:
            print(f"\n📧 Creating: {staff['email']}")
            
            try:
                # Create user license
                license = UserLicense(
                    email=staff['email'],
                    role=staff['role'],
                    expiry_date=(datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
                )
                
                # Hash password
                hashed_pw = bcrypt.hashpw(staff['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                license.password_hash = hashed_pw
                license.full_name = staff['full_name']
                
                # Save license
                save_user_license(license)
                
                print(f"   ✅ Created successfully")
                print(f"   👤 Role: {staff['role']}")
                print(f"   🔑 Password: {staff['password']}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        print("\n" + "=" * 60)
        print("STAFF ACCOUNTS READY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    print("\n🚀 T21 STAFF ACCOUNT CREATOR")
    print("Creating test accounts for staff to test all features...\n")
    
    if SUPABASE_ENABLED:
        success = create_staff_via_supabase()
    else:
        success = create_staff_via_local()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! STAFF ACCOUNTS CREATED")
        print("=" * 60)
        print("\n📝 WHAT STAFF SHOULD TEST:")
        print("-" * 60)
        print("1. ✅ Login with their credentials")
        print("2. ✅ Access ALL 55+ modules")
        print("3. ✅ Test Training Library (522 scenarios)")
        print("4. ✅ Take Certification Exam (1000+ questions)")
        print("5. ✅ Complete Information Governance training")
        print("6. ✅ Test Partial Booking List (PBL)")
        print("7. ✅ Create patients, appointments, etc.")
        print("8. ✅ Test all clinical letters with DOB")
        print("9. ✅ Test Admin Panel features")
        print("10. ✅ Report any bugs or issues")
        print("=" * 60)
        print("\n🎉 Staff are ready to start testing NOW!")
    else:
        print("\n❌ Failed to create accounts. Check errors above.")
        sys.exit(1)
