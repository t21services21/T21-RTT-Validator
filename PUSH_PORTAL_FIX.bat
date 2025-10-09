@echo off
REM ================================================================================
REM T21 SERVICES - PUSH PORTAL FIX TO GITHUB
REM ================================================================================

echo.
echo ================================================================================
echo PUSHING PORTAL LOGIN FIXES TO GITHUB
echo ================================================================================
echo.
echo This will push the fixed portal pages to GitHub:
echo - pages/staff_login.py (Fixed for Supabase)
echo - pages/nhs_login.py (Fixed for Supabase)
echo.
pause

echo.
echo Adding files...
git add pages/staff_login.py
git add pages/nhs_login.py

echo.
echo Committing changes...
git commit -m "Fix portal logins for Supabase compatibility"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ================================================================================
echo DONE! PORTAL FIXES PUSHED TO GITHUB!
echo ================================================================================
echo.
echo Streamlit Cloud will auto-deploy in 30-60 seconds.
echo Then your separate portals will work perfectly!
echo.
echo ================================================================================
echo.
pause
