"""
FIX EXPIRY DATES FOR ALL USERS

This script fixes the expiry dates for all users who have the old 10-year (2035) expiry.
Sets proper expiry based on their role:
- student_basic: 90 days from creation
- student_professional: 180 days from creation
- student_ultimate: 365 days from creation
- staff/admin/teacher: 365 days from creation
"""

from supabase_database import supabase
from datetime import datetime, timedelta

def fix_all_expiry_dates():
    """Fix expiry dates for all users"""
    
    print("🔧 Fixing expiry dates for all users...")
    
    try:
        # Get all users
        result = supabase.table('users').select('*').execute()
        users = result.data if result.data else []
        
        print(f"📊 Found {len(users)} users")
        
        fixed_count = 0
        skipped_count = 0
        
        for user in users:
            email = user.get('email')
            role = user.get('role', 'student_basic')
            created_at = user.get('created_at')
            current_expiry = user.get('expiry_date')
            
            # Parse created date
            try:
                if created_at:
                    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                else:
                    created_date = datetime.now()
            except:
                created_date = datetime.now()
            
            # Calculate proper expiry based on role
            expiry_days = {
                "trial": 2,
                "student_basic": 90,
                "student_professional": 180,
                "student_ultimate": 365,
                "staff": 365,
                "admin": 365,
                "super_admin": 365,
                "teacher": 365
            }
            
            days = expiry_days.get(role, 90)
            new_expiry = created_date + timedelta(days=days)
            
            # Check if needs updating (if expiry is in 2035 or beyond)
            try:
                if current_expiry:
                    current_expiry_date = datetime.fromisoformat(current_expiry.replace('Z', '+00:00'))
                    if current_expiry_date.year >= 2035:
                        # Update to proper expiry
                        supabase.table('users').update({
                            'expiry_date': new_expiry.isoformat()
                        }).eq('email', email).execute()
                        
                        print(f"✅ Fixed {email}: {role} → {days} days (expires {new_expiry.date()})")
                        fixed_count += 1
                    else:
                        print(f"⏭️  Skipped {email}: Already has proper expiry ({current_expiry_date.date()})")
                        skipped_count += 1
                else:
                    # No expiry date, set one
                    supabase.table('users').update({
                        'expiry_date': new_expiry.isoformat()
                    }).eq('email', email).execute()
                    
                    print(f"✅ Set expiry for {email}: {days} days")
                    fixed_count += 1
            
            except Exception as e:
                print(f"❌ Error processing {email}: {e}")
        
        print("\n" + "="*50)
        print(f"✅ Fixed: {fixed_count} users")
        print(f"⏭️  Skipped: {skipped_count} users (already correct)")
        print("="*50)
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("="*50)
    print("EXPIRY DATE FIX SCRIPT")
    print("="*50)
    print()
    
    confirm = input("This will update expiry dates for all users with 2035+ expiry. Continue? (yes/no): ")
    
    if confirm.lower() == 'yes':
        fix_all_expiry_dates()
    else:
        print("❌ Cancelled")
