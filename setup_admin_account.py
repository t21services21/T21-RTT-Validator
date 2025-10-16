"""
SETUP ADMIN ACCOUNT FOR TESTING
Creates admin account and sends welcome email

User: lawunmilatinwo@outlook.com
"""

import sys
import bcrypt
from datetime import datetime, timedelta

def setup_admin_account():
    """Setup admin account with full access"""
    
    print("=" * 60)
    print("SETTING UP ADMIN ACCOUNT FOR TESTING")
    print("=" * 60)
    
    # Admin details
    admin_email = "lawunmilatinwo@outlook.com"
    admin_name = "Lawunmi Latinwo"
    admin_password = "Admin2025!"  # Strong password
    
    print(f"\n📧 Email: {admin_email}")
    print(f"👤 Name: {admin_name}")
    print(f"🔑 Password: {admin_password}")
    
    # Try Supabase first
    try:
        from supabase_database import supabase
        print("\n✓ Using Supabase database")
        
        # Check if user exists
        existing = supabase.table('users').select('*').eq('email', admin_email).execute()
        
        # Hash password
        hashed_pw = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        if existing.data:
            print(f"\n⚠️  User already exists - UPDATING...")
            
            # Update existing user
            result = supabase.table('users').update({
                'password_hash': hashed_pw,
                'full_name': admin_name,
                'role': 'admin',
                'user_type': 'admin',
                'status': 'active',
                'trial_end_date': (datetime.now() + timedelta(days=3650)).isoformat(),  # 10 years
                'updated_at': datetime.now().isoformat()
            }).eq('email', admin_email).execute()
            
            print("✅ Admin account UPDATED")
        
        else:
            print(f"\n📝 Creating new admin account...")
            
            # Create new user
            result = supabase.table('users').insert({
                'email': admin_email,
                'password_hash': hashed_pw,
                'full_name': admin_name,
                'role': 'admin',
                'user_type': 'admin',
                'status': 'active',
                'trial_end_date': (datetime.now() + timedelta(days=3650)).isoformat(),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }).execute()
            
            print("✅ Admin account CREATED")
    
    except ImportError:
        print("\n⚠️  Supabase not available, using local storage")
        
        try:
            from user_license_system import UserLicense, save_user_license
            
            # Create license
            license = UserLicense(
                email=admin_email,
                role='admin',
                expiry_date=(datetime.now() + timedelta(days=3650)).strftime('%Y-%m-%d')
            )
            
            # Hash password
            hashed_pw = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            license.password_hash = hashed_pw
            license.full_name = admin_name
            
            # Save
            save_user_license(license)
            
            print("✅ Admin account created locally")
        
        except Exception as e:
            print(f"❌ Error creating local account: {e}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Send welcome email
    print("\n📧 Sending welcome email...")
    try:
        from email_service import send_email
        
        email_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #0066cc;">
                <h1 style="color: #0066cc;">🎉 Admin Account Created!</h1>
                
                <p>Hi {admin_name},</p>
                
                <p>Your admin account for the <strong>T21 RTT Platform</strong> has been created!</p>
                
                <div style="background: #f0f8ff; padding: 20px; margin: 20px 0; border-left: 4px solid #0066cc;">
                    <h3 style="margin-top: 0;">🔑 Login Credentials:</h3>
                    <p><strong>Email:</strong> {admin_email}<br>
                    <strong>Password:</strong> {admin_password}<br>
                    <strong>Role:</strong> Administrator (Full Access)</p>
                </div>
                
                <h3>✅ You Have Full Access To:</h3>
                <ul>
                    <li>All 55+ modules</li>
                    <li>Admin Panel</li>
                    <li>User Management</li>
                    <li>Module Access Control</li>
                    <li>Approval Dashboard</li>
                    <li>All clinical workflows</li>
                    <li>All training content</li>
                    <li>Everything!</li>
                </ul>
                
                <h3>🎯 Your Mission:</h3>
                <p><strong>Test EVERYTHING!</strong></p>
                <ol>
                    <li>Login to the platform</li>
                    <li>Test all 55+ modules</li>
                    <li>Check Information Governance</li>
                    <li>Test Partial Booking List</li>
                    <li>Try certification exam</li>
                    <li>Report any bugs</li>
                </ol>
                
                <div style="background: #fff3cd; padding: 15px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <h3 style="margin-top: 0;">📋 Testing Guide</h3>
                    <p>Check your email for the comprehensive <strong>STAFF_TESTING_GUIDE.md</strong></p>
                    <p>This guide includes:</p>
                    <ul>
                        <li>What to test (priority order)</li>
                        <li>How to test each feature</li>
                        <li>Bug reporting template</li>
                        <li>Testing checklist</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background: #0066cc; color: white; padding: 15px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; 
                              font-weight: bold;">
                        🚀 LOGIN NOW
                    </a>
                </div>
                
                <p><strong>Need Help?</strong><br>
                Contact: admin@t21services.co.uk</p>
                
                <p>Best regards,<br>
                <strong>T21 Services Team</strong></p>
                
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    © 2025 T21 Services. All rights reserved.
                </p>
            </div>
        </body>
        </html>
        """
        
        send_email(
            to_email=admin_email,
            subject="🎉 Admin Account Created - T21 Platform Testing",
            html_content=email_content
        )
        
        print("✅ Welcome email sent!")
    
    except Exception as e:
        print(f"⚠️  Email not sent: {e}")
        print("   (User can still login, just didn't get email)")
    
    # Create notification
    print("\n🔔 Creating in-app notification...")
    try:
        from notification_system import create_notification, NotificationType, NotificationPriority
        
        create_notification(
            user_email=admin_email,
            title="👤 Admin Account Ready!",
            message="Your admin account is ready. You have full access to all 55+ modules for testing. Happy testing!",
            notification_type=NotificationType.SUCCESS,
            priority=NotificationPriority.HIGH,
            send_email=False,  # Already sent email above
            action_url="/",
            action_label="Start Testing"
        )
        
        print("✅ Notification created")
    
    except Exception as e:
        print(f"⚠️  Notification not created: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ADMIN ACCOUNT SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n📧 Email: {admin_email}")
    print(f"🔑 Password: {admin_password}")
    print(f"👤 Role: Administrator")
    print(f"✅ Status: Active")
    print(f"📅 Expiry: Never")
    print("\n🎯 User can now:")
    print("  1. Login to the platform")
    print("  2. Access ALL modules")
    print("  3. Use Admin Panel")
    print("  4. Test everything")
    print("\n✉️  Welcome email sent to: " + admin_email)
    print("📋 User should also check spam folder")
    print("\n" + "=" * 60)
    
    return True


if __name__ == "__main__":
    success = setup_admin_account()
    
    if success:
        print("\n🎉 SUCCESS!")
        sys.exit(0)
    else:
        print("\n❌ FAILED - Check errors above")
        sys.exit(1)
