"""
UPDATE USER ROLE
Change user role between admin, staff, teacher, student, trial

Usage:
    python update_user_role.py email@example.com new_role
    
Example:
    python update_user_role.py lawunmilatinwo@outlook.com staff
"""

import sys
from datetime import datetime

def update_user_role(email: str, new_role: str):
    """Update user's role"""
    
    valid_roles = ['admin', 'staff', 'teacher', 'student', 'trial']
    
    if new_role not in valid_roles:
        print(f"❌ Invalid role: {new_role}")
        print(f"Valid roles: {', '.join(valid_roles)}")
        return False
    
    print("=" * 60)
    print(f"UPDATING USER ROLE")
    print("=" * 60)
    print(f"\n📧 Email: {email}")
    print(f"🔄 New Role: {new_role}")
    
    try:
        from supabase_database import supabase
        
        # Check if user exists
        existing = supabase.table('users').select('*').eq('email', email).execute()
        
        if not existing.data:
            print(f"\n❌ User not found: {email}")
            return False
        
        current_role = existing.data[0].get('role', 'unknown')
        print(f"📋 Current Role: {current_role}")
        
        # Update role
        result = supabase.table('users').update({
            'role': new_role,
            'user_type': new_role,
            'updated_at': datetime.now().isoformat()
        }).eq('email', email).execute()
        
        print(f"\n✅ Role updated successfully!")
        print(f"   From: {current_role}")
        print(f"   To:   {new_role}")
        
        # Show what access they now have
        print(f"\n🔐 Access Level for '{new_role}' role:")
        
        if new_role == 'admin':
            print("  ✅ ALL 55+ modules")
            print("  ✅ Admin Panel (full access)")
            print("  ✅ User Management")
            print("  ✅ Module Access Control")
            print("  ✅ Approvals")
            print("  ✅ Everything!")
        
        elif new_role in ['staff', 'teacher']:
            print("  ✅ ALL 55+ modules")
            print("  ✅ Patient Administration")
            print("  ✅ Clinical Workflows")
            print("  ✅ Information Governance")
            print("  ✅ Partial Booking List")
            print("  ✅ Training & Certification")
            print("  ❌ NO Admin Panel access")
        
        elif new_role == 'student':
            print("  ✅ Limited modules (based on tier)")
            print("  ✅ Training content")
            print("  ❌ NO Admin Panel")
            print("  ❌ Limited clinical tools")
        
        else:  # trial
            print("  ✅ Very limited access (trial)")
            print("  ❌ Most modules locked")
        
        # Send notification
        try:
            from notification_system import create_notification, NotificationType, NotificationPriority
            
            message = f"Your role has been updated to '{new_role}'. "
            if new_role == 'admin':
                message += "You now have full access to all modules including the Admin Panel."
            elif new_role in ['staff', 'teacher']:
                message += "You have access to all modules except the Admin Panel."
            
            create_notification(
                user_email=email,
                title=f"🔐 Role Updated to {new_role.title()}",
                message=message,
                notification_type=NotificationType.INFO,
                priority=NotificationPriority.MEDIUM,
                send_email=True,
                action_url="/"
            )
            
            print(f"\n✅ Notification sent to user")
        
        except Exception as e:
            print(f"\n⚠️  Notification not sent: {e}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_user_role.py email@example.com new_role")
        print("\nValid roles:")
        print("  - admin   : Full access including Admin Panel")
        print("  - staff   : All modules EXCEPT Admin Panel")
        print("  - teacher : All modules EXCEPT Admin Panel")
        print("  - student : Limited access based on tier")
        print("  - trial   : Very limited trial access")
        print("\nExample:")
        print("  python update_user_role.py lawunmilatinwo@outlook.com staff")
        sys.exit(1)
    
    email = sys.argv[1]
    new_role = sys.argv[2].lower()
    
    success = update_user_role(email, new_role)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ SUCCESS - Role updated!")
        print("=" * 60)
        print(f"\nUser {email} now has '{new_role}' role")
        print("They can login and see their updated access level")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ FAILED - Check errors above")
        print("=" * 60)
        sys.exit(1)
