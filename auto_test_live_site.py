"""
AUTOMATED LIVE SITE TESTER
Run this to automatically test your live site
"""

import requests
import time

LIVE_URL = "https://t21-rtt-validator-gv99yb9rjapzfshj8nermb.streamlit.app/"

print("="*70)
print("AUTOMATED LIVE SITE TESTING")
print("="*70)
print()

# Test 1: Site is reachable
print("[TEST 1] Checking if site is online...")
try:
    response = requests.get(LIVE_URL, timeout=10)
    if response.status_code == 200:
        print("[PASS] Site is online and responding")
    else:
        print(f"[FAIL] Site returned status code: {response.status_code}")
except Exception as e:
    print(f"[FAIL] Cannot reach site: {str(e)}")

print()

# Test 2: Check for common errors in HTML
print("[TEST 2] Checking for errors in page content...")
try:
    response = requests.get(LIVE_URL, timeout=10)
    html = response.text.lower()
    
    errors_found = []
    
    if "attributeerror" in html:
        errors_found.append("AttributeError detected")
    if "traceback" in html:
        errors_found.append("Python traceback detected")
    if "error:" in html:
        errors_found.append("Generic error detected")
    if "exception" in html:
        errors_found.append("Exception detected")
    
    if errors_found:
        print("[FAIL] Errors found on page:")
        for error in errors_found:
            print(f"  - {error}")
    else:
        print("[PASS] No obvious errors detected in HTML")
except Exception as e:
    print(f"[WARN] Could not check content: {str(e)}")

print()

# Test 3: Check if key elements exist
print("[TEST 3] Checking for key page elements...")
try:
    response = requests.get(LIVE_URL, timeout=10)
    html = response.text.lower()
    
    checks = {
        "Logo": "logo.png" in html or "t21 services" in html,
        "Login buttons": "login" in html,
        "Navigation": "sidebar" in html or "navigation" in html,
    }
    
    for element, found in checks.items():
        status = "[PASS]" if found else "[WARN]"
        print(f"{status} {element}: {'Found' if found else 'Not detected'}")
except Exception as e:
    print(f"[WARN] Could not check elements: {str(e)}")

print()
print("="*70)
print("AUTOMATED TESTING COMPLETE")
print("="*70)
print()
print("NEXT STEPS:")
print("1. If all tests PASS - manually verify features work")
print("2. If any FAIL - copy error messages and report them")
print("3. Open live site in browser for visual verification")
print()
