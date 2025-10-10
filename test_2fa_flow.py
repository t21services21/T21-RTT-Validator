"""
T21 SERVICES - 2FA FLOW TEST SCRIPT
Quick verification of 2FA implementation
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_2fa_imports():
    """Test that all 2FA modules can be imported"""
    print("Testing 2FA imports...")
    
    try:
        import pyotp
        print("✅ pyotp imported")
    except ImportError as e:
        print(f"❌ pyotp import failed: {e}")
        return False
    
    try:
        import qrcode
        print("✅ qrcode imported")
    except ImportError as e:
        print(f"❌ qrcode import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        from two_factor_auth import (
            generate_2fa_secret,
            verify_2fa_code,
            generate_backup_codes,
            enable_2fa_for_user,
            get_current_code
        )
        print("✅ two_factor_auth module imported")
    except ImportError as e:
        print(f"❌ two_factor_auth import failed: {e}")
        return False
    
    return True


def test_2fa_generation():
    """Test 2FA secret and code generation"""
    print("\nTesting 2FA generation...")
    
    from two_factor_auth import generate_2fa_secret, get_current_code, verify_2fa_code
    
    # Generate secret
    test_email = "test@t21services.co.uk"
    secret = generate_2fa_secret(test_email)
    print(f"✅ Generated secret: {secret[:10]}...")
    
    # Generate current code
    current_code = get_current_code(secret)
    print(f"✅ Current TOTP code: {current_code}")
    
    # Verify the code
    if verify_2fa_code(secret, current_code):
        print("✅ Code verification successful")
    else:
        print("❌ Code verification failed")
        return False
    
    # Test invalid code
    if not verify_2fa_code(secret, "000000"):
        print("✅ Invalid code correctly rejected")
    else:
        print("❌ Invalid code was accepted")
        return False
    
    return True


def test_backup_codes():
    """Test backup code generation"""
    print("\nTesting backup codes...")
    
    from two_factor_auth import generate_backup_codes
    
    codes = generate_backup_codes(10)
    
    if len(codes) == 10:
        print(f"✅ Generated 10 backup codes")
    else:
        print(f"❌ Expected 10 codes, got {len(codes)}")
        return False
    
    # Check format
    for code in codes:
        if len(code) == 9 and code[4] == '-':
            continue
        else:
            print(f"❌ Invalid backup code format: {code}")
            return False
    
    print(f"✅ All backup codes have correct format (XXXX-XXXX)")
    print(f"   Sample codes: {codes[0]}, {codes[1]}")
    
    return True


def test_qr_generation():
    """Test QR code generation"""
    print("\nTesting QR code generation...")
    
    from two_factor_auth import enable_2fa_for_user
    
    test_email = "test@t21services.co.uk"
    setup = enable_2fa_for_user(test_email)
    
    required_keys = ['secret', 'qr_uri', 'qr_base64', 'backup_codes']
    
    for key in required_keys:
        if key in setup:
            print(f"✅ Setup contains '{key}'")
        else:
            print(f"❌ Setup missing '{key}'")
            return False
    
    # Check QR is base64
    if len(setup['qr_base64']) > 100:
        print(f"✅ QR code generated (base64 length: {len(setup['qr_base64'])})")
    else:
        print(f"❌ QR code seems too short")
        return False
    
    return True


def test_supabase_functions():
    """Test Supabase 2FA functions (without actually connecting)"""
    print("\nTesting Supabase functions...")
    
    try:
        from supabase_database import enable_2fa, disable_2fa, use_backup_code
        print("✅ Supabase 2FA functions imported")
        return True
    except ImportError as e:
        print(f"❌ Supabase functions import failed: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("T21 SERVICES - 2FA IMPLEMENTATION TEST")
    print("="*60)
    
    tests = [
        ("Imports", test_2fa_imports),
        ("2FA Generation", test_2fa_generation),
        ("Backup Codes", test_backup_codes),
        ("QR Generation", test_qr_generation),
        ("Supabase Functions", test_supabase_functions),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n⚠️ {test_name} test failed")
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name} test crashed: {e}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 All tests passed! 2FA implementation is ready.")
        print("\nNext steps:")
        print("1. Run ADD_2FA_COLUMNS.sql in Supabase")
        print("2. Add Supabase credentials to .streamlit/secrets.toml")
        print("3. Test end-to-end in the app")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please fix issues before deployment.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
