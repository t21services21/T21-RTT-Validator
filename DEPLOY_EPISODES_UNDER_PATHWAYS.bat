@echo off
echo ========================================
echo DEPLOYING: EPISODES UNDER PATHWAYS
echo PAS-Style Integration
echo ========================================
echo.
echo FEATURE ADDED:
echo.
echo Episodes now display DIRECTLY under pathways!
echo Just like your PAS system shows.
echo.
echo WHERE EPISODES NOW APPEAR:
echo.
echo 1. "All Pathways" Tab
echo    - View any pathway
echo    - Episodes table shown below pathway details
echo    - Shows: Type, Dates, Specialty, Consultant, Status
echo.
echo 2. "Manage Pathway" Tab
echo    - Select a pathway to manage
echo    - Episodes table shown below current status
echo    - All episode details visible
echo.
echo EPISODE DETAILS SHOWN:
echo  * Episode ID
echo  * Episode Type (Consultant/Treatment/Diagnostic)
echo  * Start Date / End Date
echo  * Specialty
echo  * Consultant Name
echo  * Status
echo  * Treatment Type (if applicable)
echo  * Test Type (if applicable)
echo  * Results (if available)
echo  * Clinical Notes
echo.
echo ALSO INCLUDES ALL PREVIOUS FIXES:
echo  [X] Enhanced success messages (all modules)
echo  [X] All T21 detailed formats
echo  [X] Pathway date fix
echo  [X] Interview Prep fix
echo.

cd /d "%~dp0"

echo Adding files...
git add pathway_management_ui.py

echo.
echo Committing...
git commit -m "Added: Episodes table under pathways (PAS-style integration)"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo NOW WHEN YOU VIEW A PATHWAY:
echo.
echo 1. Go to Pathway Management
echo 2. Click "All Pathways" tab
echo 3. Select a patient
echo 4. View pathway - EPISODES appear below!
echo.
echo OR
echo.
echo 1. Go to "Manage Pathway" tab
echo 2. Select a pathway
echo 3. EPISODES table shows below status
echo 4. See all episode details
echo.
echo Just like your PAS system!
echo.
echo Wait 3 minutes for Streamlit to redeploy.
echo Then test it!
echo.
pause
