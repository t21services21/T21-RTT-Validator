@echo off
cls
echo.
echo ========================================
echo   ENABLE WEB-BASED STUDENT ENROLLMENT
echo ========================================
echo.
echo This will fix the enrollment system so:
echo - Teachers can enroll students from web
echo - No more SQL scripts needed
echo - Works just like RTT enrollment
echo - Simple and user-friendly
echo.
echo ========================================
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Adding fixed files...
"C:\Program Files\Git\bin\git.exe" add tquk_course_assignment.py simple_course_assignment.py

echo.
echo [2/3] Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix TQUK enrollment system - Teachers can now enroll students from web UI without SQL"

echo.
echo [3/3] Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ========================================
echo          DEPLOYMENT STARTED!
echo ========================================
echo.
echo Wait 5-7 minutes for Streamlit to update.
echo.
echo Then teachers can enroll students:
echo.
echo 1. Go to Teaching ^& Assessment
echo 2. Click "TQUK Course Assignment"
echo 3. Select student from dropdown
echo 4. Tick "Level 3 Diploma in Adult Care"
echo 5. Click "Assign Selected"
echo 6. Done!
echo.
echo Student gets:
echo - Enrolled in course (database)
echo - Module access granted
echo - Welcome email sent
echo - Can access course immediately
echo.
echo No SQL needed!
echo No command line!
echo Everything from web!
echo.
echo ========================================
pause
