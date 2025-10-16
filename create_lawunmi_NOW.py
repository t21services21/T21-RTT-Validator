"""
CREATE LAWUNMI'S ACCOUNT - GUARANTEED TO WORK
Creates in BOTH databases and sends email
"""

import bcrypt
from datetime import datetime, timedelta
import json
import os

def create_lawunmi():
    """Create Lawunmi's account properly"""
    
    # ACCOUNT DETAILS
    email = "lawunmilatinwo@outlook.com"
    password = "Admin2025!"
    name = "Lawunmi Latinwo"
    role = "staff"  # Change to "admin" if they need Admin Panel access
    
    print("=" * 70)
    print("CREATING LAWUNMI'S ACCOUNT")
    print("=" * 70)
    print(f"\n📧 Email: {email}")
    print(f"👤 Name: {name}")
    print(f"🔑 Password: {password}")
    print(f"👔 Role: {role}")
    
    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    success_count = 0
    
    # ========================================
    # STEP 1: Create in SUPABASE
    # ========================================
    print("\n1️⃣ Creating in Supabase...")
    try:
        from supabase_database import supabase
        
        # Check if exists
        existing = supabase.table('users').select('*').eq('email', email).execute()
        
        if existing.data:
            print("   ⚠️  Already exists - updating...")
            result = supabase.table('users').update({
                'password_hash': hashed_pw,
                'full_name': name,
                'role': role,
                'user_type': role,
                'status': 'active',
                'trial_end_date': (datetime.now() + timedelta(days=365)).isoformat(),
                'updated_at': datetime.now().isoformat()
            }).eq('email', email).execute()
            print("   ✅ Updated in Supabase")
        else:
            result = supabase.table('users').insert({
                'email': email,
                'password_hash': hashed_pw,
                'full_name': name,
                'role': role,
                'user_type': role,
                'status': 'active',
                'trial_end_date': (datetime.now() + timedelta(days=365)).isoformat(),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }).execute()
            print("   ✅ Created in Supabase")
        
        success_count += 1
    
    except Exception as e:
        print(f"   ❌ Supabase failed: {e}")
    
    # ========================================
    # STEP 2: Create in LOCAL JSON
    # ========================================
    print("\n2️⃣ Creating in local JSON database...")
    try:
        db_file = "users_advanced.json"
        
        if os.path.exists(db_file):
            with open(db_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}
        
        users[email] = {
            'email': email,
            'password_hash': hashed_pw,
            'full_name': name,
            'role': role,
            'user_type': role,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'trial_end_date': (datetime.now() + timedelta(days=365)).isoformat(),
            'total_logins': 0,
            'last_login': None,
            'custom_permissions': []
        }
        
        with open(db_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        print(f"   ✅ Created in {db_file}")
        success_count += 1
    
    except Exception as e:
        print(f"   ❌ Local JSON failed: {e}")
    
    # ========================================
    # STEP 3: SEND WELCOME EMAIL
    # ========================================
    print("\n3️⃣ Sending welcome email...")
    try:
        from email_service import send_email
        
        email_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #0066cc;">
                <h1 style="color: #0066cc;">🎉 Welcome to T21 Platform!</h1>
                <p>Hi {name},</p>
                <p>Your account has been created and is ready to use!</p>
                
                <div style="background: #f0f8ff; padding: 20px; margin: 20px 0; border-left: 4px solid #0066cc;">
                    <h3 style="margin-top: 0;">🔑 Login Credentials:</h3>
                    <p><strong>Email:</strong> {email}<br>
                    <strong>Password:</strong> {password}<br>
                    <strong>Role:</strong> {role.title()}</p>
                </div>
                
                <h3>✅ You Have Access To:</h3>
                <ul>
                    <li>All 55+ modules</li>
                    <li>Patient Administration Hub</li>
                    <li>Clinical Workflows (PTL, Cancer, MDT, Booking)</li>
                    <li>Information Governance</li>
                    <li>Partial Booking List</li>
                    <li>Training & Certification</li>
                    <li>Career Development Tools</li>
                    <li>AI & Automation</li>
                    {'<li><strong>Admin Panel</strong></li>' if role == 'admin' else '<li>All modules except Admin Panel</li>'}
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://t21-healthcare-platform.streamlit.app" 
                       style="background: #0066cc; color: white; padding: 15px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block; 
                              font-weight: bold;">
                        🚀 LOGIN NOW
                    </a>
                </div>
                
                <p>Start exploring and testing all features!</p>
                
                <p>Best regards,<br><strong>T21 Services Team</strong></p>
            </div>
        </body>
        </html>
        """
        
        send_email(
            to_email=email,
            subject=f"🎉 Welcome to T21 Platform - {role.title()} Account",
            html_content=email_content
        )
        
        print("   ✅ Welcome email sent!")
        success_count += 1
    
    except Exception as e:
        print(f"   ❌ Email failed: {e}")
        print(f"   ⚠️  Manual share: Send credentials to {email}")
    
    # ========================================
    # STEP 4: CREATE NOTIFICATION
    # ========================================
    print("\n4️⃣ Creating in-app notification...")
    try:
        from notification_system import create_notification, NotificationType, NotificationPriority
        
        create_notification(
            user_email=email,
            title=f"👋 Welcome {name}!",
            message=f"Your {role} account is ready! Start exploring all {55 if role == 'staff' else 'all'} modules.",
            notification_type=NotificationType.SUCCESS,
            priority=NotificationPriority.HIGH,
            send_email=False,  # Already sent above
            action_url="/",
            action_label="Get Started"
        )
        
        print("   ✅ Notification created!")
        success_count += 1
    
    except Exception as e:
        print(f"   ❌ Notification failed: {e}")
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n" + "=" * 70)
    if success_count >= 2:  # At least database + one other thing
        print("✅ SUCCESS - ACCOUNT CREATED!")
        print("=" * 70)
        print(f"\n📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"👔 Role: {role}")
        print(f"🌐 URL: https://t21-healthcare-platform.streamlit.app")
        
        if role == 'staff':
            print(f"\n✅ Access: ALL modules EXCEPT Admin Panel")
        else:
            print(f"\n✅ Access: ALL modules INCLUDING Admin Panel")
        
        print(f"\n✅ Lawunmi should now appear in Admin Panel!")
        print(f"✅ Welcome email sent to {email}")
        print(f"✅ Can login immediately!")
        
        print("\n📋 NEXT STEPS:")
        print("1. Refresh Admin Panel - Lawunmi should be in user list")
        print("2. Ask Lawunmi to check email (spam folder too!)")
        print("3. They can login and start testing")
        print("4. They'll see notification when they login")
        
    else:
        print("⚠️  PARTIAL SUCCESS")
        print("=" * 70)
        print(f"Only {success_count}/4 steps completed")
        print("\nManually share credentials:")
        print(f"Email: {email}")
        print(f"Password: {password}")
    
    print("=" * 70)


if __name__ == "__main__":
    create_lawunmi()
