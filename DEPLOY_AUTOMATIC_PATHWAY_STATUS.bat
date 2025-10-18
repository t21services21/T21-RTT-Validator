@echo off
echo ========================================
echo DEPLOYING: AUTOMATIC PATHWAY STATUS
echo NHS Workflow - Episode-Driven
echo ========================================
echo.
echo CRITICAL NHS FEATURE IMPLEMENTED:
echo.
echo Last Episode RTT Code → Determines Pathway Status
echo.
echo HOW IT WORKS:
echo.
echo 1. User creates episode with RTT code
echo    Example: Episode with Code 91 (Patient DNA 2+ times)
echo.
echo 2. System checks the code automatically
echo    Code 91 = Clock Stop Code
echo.
echo 3. System updates pathway status
echo    Pathway Status → CLOSED
echo    Clock Status → STOPPED
echo.
echo RTT CLOCK STOP CODES (Pathway CLOSED):
echo  - 30: Treatment - Clock Stop
echo  - 31: Patient declined treatment
echo  - 32: Patient DNA - Clock Stop
echo  - 34: Discharged
echo  - 91: Patient DNA 2+ times
echo  - 92: No longer requires treatment
echo  - 93: Moved out of area
echo  - 94: Patient died
echo  - 95: Patient requested removal
echo  - 96: Other admin removal
echo.
echo RTT CLOCK CONTINUE CODES (Pathway ACTIVE):
echo  - 10: First Outpatient - New referral
echo  - 11: Active Monitoring - Clock RESTART
echo  - 12: Consultant-to-Consultant - NEW condition
echo  - 20: Clock continues - Awaiting treatment
echo  - 21: Clock continues - Further outpatient
echo.
echo SPECIAL CASE - CODE 11:
echo  If pathway was closed (Code 91, 31, etc.)
echo  Then Code 11 RESTARTS the clock
echo  Creates NEW active pathway period
echo.
echo MATCHES YOUR PAS SYSTEM EXACTLY!
echo.

cd /d "%~dp0"

echo Adding files...
git add pathway_status_automation.py
git add episode_management_system.py
git add pathway_management_system.py
git add pathway_management_ui.py

echo.
echo Committing...
git commit -m "NHS Workflow: Automatic pathway status from episode RTT codes"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo WHAT HAPPENS NOW:
echo.
echo 1. Create an episode with RTT code
echo 2. Code is checked automatically
echo 3. Pathway status updates automatically
echo 4. Success message shows new status
echo.
echo EXAMPLE:
echo  Create Episode with Code 91
echo  → Pathway status changes to CLOSED
echo  → Clock status changes to STOPPED
echo  → Success message: "Pathway status: CLOSED"
echo.
echo Just like NHS PAS systems!
echo.
echo Wait 3 minutes for Streamlit to redeploy.
echo Then test by creating episodes with different codes!
echo.
pause
