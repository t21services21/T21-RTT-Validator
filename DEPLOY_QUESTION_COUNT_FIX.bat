@echo off
echo ========================================
echo DEPLOYING QUESTION COUNT FIX
echo ========================================
echo.
echo ISSUE: Only getting 4 questions instead of 15-20
echo.
echo FIX:
echo - Made prompt VERY clear: "Generate EXACTLY 15-20 questions"
echo - Added "CRITICAL: You MUST generate at least 15 questions"
echo - Increased tokens to 8000 (was 6000)
echo.

cd /d "%~dp0"

echo Adding files...
git add interview_prep.py

echo.
echo Committing...
git commit -m "FIX: Interview Prep now generates 15-20 questions (was only 4)"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DONE! Wait 3 minutes then test.
echo ========================================
echo.
echo You should now get 15-20 questions instead of 4!
echo.
pause
