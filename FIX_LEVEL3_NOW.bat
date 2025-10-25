@echo off
cls
echo.
echo ========================================
echo   FIXING LEVEL 3 ENROLLMENT SYSTEM
echo ========================================
echo.
echo This will make Level 3 work like RTT!
echo.
echo Changes:
echo - Level 3 enrollment won't fail
echo - Works even if module not deployed
echo - Students get enrolled immediately
echo - Same smooth experience as RTT
echo.
echo ========================================
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Adding files...
git add simple_course_assignment.py

echo.
echo [2/3] Committing...
git commit -m "Fix Level 3 enrollment - make it work like RTT training (smooth and simple)"

echo.
echo [3/3] Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo          FIX DEPLOYED!
echo ========================================
echo.
echo Wait 5 minutes for Streamlit to update.
echo.
echo Then Level 3 enrollment will work just like RTT:
echo 1. Select student
echo 2. Tick Level 3
echo 3. Click Assign
echo 4. Done!
echo.
echo No more errors!
echo No more complications!
echo Just like RTT - smooth and simple!
echo.
echo ========================================
pause
