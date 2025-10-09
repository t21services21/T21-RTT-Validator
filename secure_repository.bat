@echo off
REM ================================================================================
REM T21 SERVICES - AUTOMATIC SECURITY CLEANUP
REM ================================================================================
REM This script removes sensitive files from GitHub
REM Run this in your project folder!
REM ================================================================================

echo.
echo ================================================================================
echo T21 SERVICES - SECURING YOUR REPOSITORY
echo ================================================================================
echo.
echo This will remove sensitive files from GitHub (but keep them on your computer)
echo.
pause

echo.
echo Step 1: Removing sensitive test files...
git rm --cached reset_staff_password.py 2>nul
git rm --cached test_login.py 2>nul
git rm --cached test_password.py 2>nul
git rm --cached verify_login_works.py 2>nul
git rm --cached diagnose_login.py 2>nul
git rm --cached create_admin_simple.py 2>nul
git rm --cached check_all_users.py 2>nul
git rm --cached test_admin_functions.py 2>nul

echo.
echo Step 2: Removing database files...
git rm --cached users_database.json 2>nul
git rm --cached users_advanced.json 2>nul
git rm --cached validation_history.json 2>nul
git rm --cached user_tracking.json 2>nul
git rm --cached audit_log.json 2>nul

echo.
echo Step 3: Adding .gitignore to protect future commits...
git add .gitignore

echo.
echo Step 4: Committing changes...
git commit -m "Security: Remove sensitive files and add .gitignore protection"

echo.
echo Step 5: Pushing to GitHub...
git push origin main

echo.
echo ================================================================================
echo SECURITY CLEANUP COMPLETE!
echo ================================================================================
echo.
echo What was done:
echo - Sensitive test files removed from GitHub
echo - Database files removed from GitHub
echo - .gitignore added to prevent future leaks
echo.
echo Files are STILL on your computer (only removed from GitHub)
echo.
echo Next steps:
echo 1. Check GitHub to verify files are gone
echo 2. Create .streamlit/secrets.toml for local testing
echo 3. Add secrets to Streamlit Cloud for production
echo.
echo ================================================================================
echo.
pause
