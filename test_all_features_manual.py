"""
COMPREHENSIVE FEATURE TEST - MANUAL VERIFICATION GUIDE
Since Streamlit requires browser interaction, this guides you through testing
"""

import webbrowser
import time

LIVE_URL = "https://t21-rtt-validator-gv99yb9rjapzfshj8nermb.streamlit.app/"

print("="*70)
print("COMPREHENSIVE FEATURE TESTING GUIDE")
print("="*70)
print()

# Open live site
print("Opening live site in browser...")
webbrowser.open(LIVE_URL)
time.sleep(2)

print()
print("="*70)
print("TEST EACH FEATURE - CHECK THE BOXES")
print("="*70)
print()

tests = [
    ("LANDING PAGE", [
        "Logo displays at top",
        "Sidebar shows with logo",
        "Student Login button visible",
        "Staff Login button visible", 
        "NHS Login button visible",
        "Contact Us button works",
        "Terms of Service link works",
        "Privacy Policy link works",
        "NO error messages visible"
    ]),
    
    ("STUDENT LOGIN", [
        "Login page loads",
        "Logo shows at top",
        "Can enter email",
        "Can enter password",
        "Login button works",
        "Redirects to dashboard after login",
        "NO errors during login"
    ]),
    
    ("DASHBOARD (AFTER LOGIN)", [
        "Dashboard loads successfully",
        "Welcome message displays",
        "User name shows correctly",
        "Sidebar navigation visible",
        "All menu items clickable",
        "NO AttributeError",
        "NO red error boxes"
    ]),
    
    ("RTT CLINICAL VALIDATOR", [
        "Page loads from sidebar",
        "Can enter patient data",
        "Validation button works",
        "Results display correctly",
        "NO errors during validation"
    ]),
    
    ("ACCOUNT PAGE", [
        "Account/Profile page loads",
        "User information displays",
        "Shows 4 pricing tiers (Taster, Tier 1, 2, 3)",
        "Pricing shows: £99, £499, £1,299, £1,799",
        "License details visible",
        "NO AttributeError",
        "NO 'user_license.usage' error"
    ]),
    
    ("ADMIN PANEL (IF ADMIN LOGIN)", [
        "Admin panel accessible",
        "Dashboard tab loads",
        "User Management tab loads",
        "User list displays",
        "Can filter users",
        "Statistics show correctly",
        "NO comparison error ('>not supported')",
        "NO datetime errors"
    ]),
    
    ("USER TRACKING (IF ADMIN)", [
        "User tracking page loads",
        "User statistics display",
        "User table shows data",
        "Can download CSV",
        "NO errors"
    ]),
    
    ("AI TUTOR", [
        "AI Tutor page loads",
        "Can ask questions",
        "Receives responses",
        "NO errors"
    ]),
    
    ("DOCUMENT UPLOAD", [
        "File uploader visible",
        "Can select PDF file",
        "Can select Word file",
        "Upload works",
        "NO errors"
    ]),
    
    ("NAVIGATION", [
        "All sidebar links work",
        "All buttons clickable",
        "Page transitions smooth",
        "Back buttons work",
        "NO broken links",
        "NO page crashes"
    ])
]

for category, checks in tests:
    print(f"\n{'='*70}")
    print(f"TESTING: {category}")
    print('='*70)
    for i, check in enumerate(checks, 1):
        print(f"  [ ] {i}. {check}")
    print()
    input("Press ENTER when you've tested this section...")

print()
print("="*70)
print("TESTING COMPLETE!")
print("="*70)
print()

# Collect results
print("REPORT ANY ERRORS FOUND:")
print()
errors = input("Type any errors you found (or 'NONE' if all good): ")

if errors.upper() == "NONE":
    print()
    print("="*70)
    print("SUCCESS! ALL FEATURES WORKING!")
    print("="*70)
    print()
    print("Platform is ready for NHS demo!")
else:
    print()
    print("="*70)
    print("ERRORS TO FIX:")
    print("="*70)
    print(errors)
    print()
    print("Copy these errors and report them for fixing!")
