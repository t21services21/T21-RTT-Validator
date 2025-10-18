@echo off
echo ========================================
echo DEPLOYING: PATHWAY/EPISODE FIXES
echo 1. Add Episode Button Now Works
echo 2. Episode "Date" (not "Start Date")
echo ========================================
echo.
echo ISSUES FIXED:
echo.
echo ISSUE 1: Add Episode Button Not Working
echo  ❌ BEFORE: Button did nothing when clicked
echo  ✅ AFTER:  Saves pathway info, shows success message
echo            User can go to Episode Management with pathway pre-selected
echo.
echo ISSUE 2: Episode "Start Date" Confusing
echo  ❌ BEFORE: "Start Date: 2025-09-16" (confusing with pathway start)
echo  ✅ AFTER:  "Date: 2025-09-16" (clear and simple)
echo.
echo HOW IT WORKS NOW:
echo.
echo 1. User views pathway (e.g., RTT_20251018154557)
echo 2. Clicks "➕ Add New Episode to This Pathway"
echo 3. System saves pathway info to session state
echo 4. Shows success message with instructions
echo 5. User goes to Episode Management (from top menu)
echo 6. Pathway is automatically pre-selected!
echo 7. User fills in episode details and saves
echo 8. Episode is linked to correct pathway
echo.
echo CHANGES MADE:
echo  - pathway_management_ui.py:
echo    * Add Episode button stores pathway in session state
echo    * Changed "Start Date" to "Date" for episodes
echo    * Shows helpful success messages
echo.
echo  - patient_selector_component.py:
echo    * render_pathway_selector checks session state
echo    * Pre-selects pathway if saved from Pathway Management
echo    * Shows notification that pathway was pre-selected
echo.

cd /d "%~dp0"

echo Adding files...
git add pathway_management_ui.py
git add patient_selector_component.py

echo.
echo Committing...
git commit -m "Fixed: Add Episode button works + Episode Date label clarity"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Wait 3 minutes for Streamlit to redeploy.
echo.
echo TESTING:
echo  1. Go to Pathway Management → View All Pathways
echo  2. Open a pathway
echo  3. Click "➕ Add New Episode to This Pathway"
echo  4. Should see success message
echo  5. Go to Episode Management (from top dropdown)
echo  6. Pathway should be pre-selected!
echo  7. Episode display should show "Date:" not "Start Date:"
echo.
pause
