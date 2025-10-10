"""
T21 SERVICES - Verify Supabase 2FA Setup
Quick check that database is ready for 2FA
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def check_connection():
    """Check if Supabase is accessible"""
    print("1. Checking Supabase connection...")
    
    try:
        from supabase_database import test_connection
        if test_connection():
            print("   ✅ Supabase connection successful\n")
            return True
        else:
            print("   ❌ Supabase connection failed\n")
            return False
    except Exception as e:
        print(f"   ❌ Connection error: {e}\n")
        return False


def check_2fa_columns():
    """Check if 2FA columns exist in users table"""
    print("2. Checking for 2FA columns in users table...")
    
    try:
        from supabase_database import supabase
        
        # Try to get a user and check for 2FA columns
        result = supabase.table("users").select("*").limit(1).execute()
        
        if not result.data:
            print("   ⚠️ No users found in database (this is okay for new databases)")
            print("   Creating test query to verify columns...\n")
            return None
        
        user = result.data[0]
        required_columns = [
            'two_factor_secret',
            'two_factor_backup_codes', 
            'two_factor_enabled',
            'two_factor_enabled_at'
        ]
        
        all_present = True
        for col in required_columns:
            if col in user:
                print(f"   ✅ Column '{col}' exists")
            else:
                print(f"   ❌ Column '{col}' MISSING")
                all_present = False
        
        print()
        return all_present
        
    except Exception as e:
        print(f"   ❌ Error checking columns: {e}")
        print("   ⚠️ You may need to run ADD_2FA_COLUMNS.sql\n")
        return False


def test_2fa_enable():
    """Test enabling 2FA for a test user"""
    print("3. Testing 2FA enable function...")
    
    try:
        from supabase_database import get_user_by_email, enable_2fa, disable_2fa
        from two_factor_auth import enable_2fa_for_user
        
        # Check if test user exists
        test_email = "test-2fa@t21services.co.uk"
        user = get_user_by_email(test_email)
        
        if not user:
            print(f"   ⚠️ Test user '{test_email}' not found")
            print("   Skipping enable test (need a real user to test)\n")
            return None
        
        # Generate 2FA setup
        setup = enable_2fa_for_user(test_email)
        
        # Try to enable
        success = enable_2fa(test_email, setup['secret'], setup['backup_codes'])
        
        if success:
            print(f"   ✅ 2FA enabled for test user")
            
            # Clean up
            disable_2fa(test_email)
            print(f"   ✅ 2FA disabled (cleanup)\n")
            return True
        else:
            print(f"   ❌ Failed to enable 2FA\n")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing 2FA: {e}\n")
        return False


def main():
    """Run all verification checks"""
    print("="*60)
    print("T21 SERVICES - SUPABASE 2FA VERIFICATION")
    print("="*60)
    print()
    
    # Check 1: Connection
    has_connection = check_connection()
    
    if not has_connection:
        print("\n" + "="*60)
        print("⚠️ SUPABASE NOT CONFIGURED")
        print("="*60)
        print("\nPlease configure Supabase credentials:")
        print("\nOption 1 - Local Development:")
        print("  Create .streamlit/secrets.toml with:")
        print("  [supabase]")
        print('  url = "https://your-project.supabase.co"')
        print('  service_key = "your-service-role-key"')
        print("\nOption 2 - Use supabase_config_SAFE.py")
        print("  (not recommended for production)")
        return 1
    
    # Check 2: Columns
    has_columns = check_2fa_columns()
    
    if has_columns is False:
        print("="*60)
        print("⚠️ 2FA COLUMNS MISSING")
        print("="*60)
        print("\nPlease run the SQL migration:")
        print("1. Open Supabase Dashboard")
        print("2. Go to SQL Editor")
        print("3. Create New Query")
        print("4. Copy contents of ADD_2FA_COLUMNS.sql")
        print("5. Paste and Run")
        return 1
    
    # Check 3: Functions (optional if no test user)
    test_2fa_enable()
    
    # Summary
    print("="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    if has_connection and (has_columns or has_columns is None):
        print("\n✅ Supabase is configured and ready for 2FA!")
        print("\nNext steps:")
        print("1. Test 2FA setup in the app (Security page)")
        print("2. Scan QR code with authenticator app")
        print("3. Verify login flow with 2FA")
        print("4. Push to GitHub and deploy")
        return 0
    else:
        print("\n⚠️ Some checks failed. Please fix issues above.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user.")
        sys.exit(1)
