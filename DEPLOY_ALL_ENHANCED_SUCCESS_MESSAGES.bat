@echo off
echo ========================================
echo DEPLOYING ENHANCED SUCCESS MESSAGES
echo ALL MODULES - SYSTEM-WIDE
echo ========================================
echo.
echo SUCCESS MESSAGE ENHANCEMENTS:
echo.
echo 1. BALLOONS + CLEAR TEXT - Visual + written confirmation
echo 2. BIG BOLD TITLES - "SUCCESSFULLY COMPLETED!"
echo 3. DETAILED INFORMATION - IDs, dates, status
echo 4. MULTIPLE CONFIRMATIONS - Checkmarks throughout
echo 5. NEXT STEPS GUIDANCE - What to do next
echo 6. STAYS VISIBLE - Doesn't disappear quickly
echo.
echo MODULES UPDATED:
echo.
echo  [X] Pathway Management - Create, pause, resume, milestones, status
echo  [X] Patient Registration - New patient registration
echo  [X] Episode Management - Consultant, treatment, diagnostic episodes
echo  [X] Advanced Booking - Appointments and clinic templates
echo  [X] Task Management - Task creation
echo  [X] Success Messages Utility - Reusable functions for all modules
echo.
echo ALSO INCLUDES:
echo  [X] All T21 enhanced formats (full details in all commenting styles)
echo  [X] Pathway date fix
echo  [X] Interview Prep fix
echo.

cd /d "%~dp0"

echo Adding files...
git add pathway_management_ui.py
git add pathway_management_system.py
git add patient_registration_ui.py
git add episode_management_ui.py
git add advanced_booking_ui.py
git add task_management_ui.py
git add success_messages.py
git add clinic_letter_interpreter_EDUCATIONAL.py
git add interview_prep.py

echo.
echo Committing...
git commit -m "System-wide: Enhanced success messages across all modules - clear, detailed, reassuring"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo SUCCESS MESSAGES ENHANCED IN:
echo.
echo 1. Pathway Management
echo    - Create pathway
echo    - Pause/resume clock
echo    - Record milestones
echo    - Update status
echo.
echo 2. Patient Registration
echo    - Register new patient
echo.
echo 3. Episode Management
echo    - Create consultant episode
echo    - Create treatment episode
echo    - Create diagnostic episode
echo    - Update episode
echo    - Move episode
echo.
echo 4. Advanced Booking
echo    - Book appointment
echo    - Create clinic template
echo.
echo 5. Task Management
echo    - Create task
echo.
echo FEATURES IN EVERY SUCCESS MESSAGE:
echo  * Balloons animation
echo  * Bold title with "SUCCESSFULLY"
echo  * All relevant details (IDs, dates, etc.)
echo  * Multiple confirmations
echo  * Next steps guidance
echo  * Message stays visible
echo.
echo Wait 3 minutes for Streamlit to redeploy.
echo Then try creating pathways, patients, episodes, etc.
echo You'll see the new enhanced success messages!
echo.
pause
