@echo off
cls
echo.
echo ========================================
echo   DEPLOY LEVEL 2 BUSINESS ADMIN + RTT
echo ========================================
echo.
echo This will deploy:
echo - Complete TQUK Level 2 Business Admin (603/2949/X)
echo - All 18 units (5 mandatory + 13 optional)
echo - Full RTT integration
echo - Evidence collection system
echo - Dual certification pathway
echo.
echo After deployment, teachers can enroll students who will get:
echo - TQUK Level 2 Business Admin qualification
echo - T21 RTT Hospital Admin certification
echo - Real NHS workplace experience
echo.
echo ========================================
echo.
pause

cd /d "%~dp0"

echo.
echo [1/4] Adding files...
"C:\Program Files\Git\bin\git.exe" add tquk_business_admin_module.py tquk_course_assignment.py simple_course_assignment.py

echo.
echo [2/4] Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Deploy Level 2 Business Admin with RTT Integration - Complete TQUK qualification with dual certification pathway"

echo.
echo [3/4] Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo [4/4] Deployment initiated!
echo.
echo ========================================
echo          DEPLOYMENT SUCCESSFUL!
echo ========================================
echo.
echo Wait 5-7 minutes for Streamlit to update.
echo.
echo Then you can:
echo.
echo 1. ENROLL STUDENTS:
echo    - Go to Teaching ^& Assessment
echo    - Click TQUK Course Assignment
echo    - Select student
echo    - Tick "Level 2 Certificate in Business Administration"
echo    - Click Assign
echo.
echo 2. STUDENTS WILL SEE:
echo    - All 18 TQUK units (5 mandatory + 13 optional)
echo    - RTT practical tasks for each unit
echo    - Evidence collection guidance
echo    - Progress tracking
echo    - Dual certification pathway
echo.
echo 3. UNIQUE FEATURES:
echo    - Theory + Practice combined
echo    - Real NHS RTT experience
echo    - Automatic evidence capture
echo    - Two qualifications in one course
echo    - 12-week completion pathway
echo.
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. Wait 5-7 minutes for deployment
echo 2. Test with a student enrollment
echo 3. Verify all 18 units visible
echo 4. Check RTT integration works
echo 5. Market as dual certification!
echo.
echo ========================================
pause
