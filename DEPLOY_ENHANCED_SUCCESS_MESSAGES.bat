@echo off
echo ========================================
echo DEPLOYING ENHANCED SUCCESS MESSAGES
echo ========================================
echo.
echo IMPROVEMENTS:
echo.
echo 1. SUCCESS MESSAGES - Clear, detailed, reassuring
echo 2. BALLOONS + TEXT - Visual + written confirmation
echo 3. STAYS VISIBLE - Doesn't disappear quickly
echo 4. NEXT STEPS - Guides users on what to do next
echo.
echo MODULES UPDATED:
echo - Pathway Management (all actions)
echo - Success messages utility module created
echo.
echo ALSO INCLUDES:
echo - All T21 enhanced formats (full details)
echo - Pathway date fix
echo - Interview Prep fix
echo.

cd /d "%~dp0"

echo Adding files...
git add pathway_management_ui.py
git add pathway_management_system.py
git add clinic_letter_interpreter_EDUCATIONAL.py
git add interview_prep.py
git add success_messages.py

echo.
echo Committing...
git commit -m "Enhanced success messages: Clear, detailed, reassuring confirmations with balloons"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Changes deployed:
echo [X] Pathway date fix
echo [X] Enhanced success messages (Pathway Management)
echo [X] Success messages utility module
echo [X] All T21 formats with full details
echo [X] Interview Prep 15-20 questions fix
echo.
echo Wait 3 minutes for Streamlit to redeploy.
echo Then create a pathway to see the new success messages!
echo.
pause
