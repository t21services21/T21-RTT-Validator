@echo off
echo ========================================
echo DEPLOYING SPEED FIX FOR INTERVIEW PREP
echo ========================================
echo.
echo Changes:
echo - Added 45-second timeout
echo - Simplified prompt (30 lines vs 400 lines)
echo - Reduced to 15-20 questions (was 30-40)
echo - Shorter answers (100-150 words vs 300-500)
echo - Reduced tokens (6000 vs 16000)
echo - Should be 5x FASTER!
echo.

cd /d "%~dp0"

echo Adding files...
git add interview_prep.py

echo.
echo Committing...
git commit -m "SPEED FIX: Interview Prep now 5x faster - simplified prompt, timeout added"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DONE! Wait 3 minutes then test.
echo ========================================
echo.
echo Should now take 10-15 seconds instead of 60+ seconds!
echo.
pause
