@echo off
echo ========================================
echo PUSHING LEVEL 3 MATERIALS TO GITHUB
echo ========================================
echo.

cd /d "C:\Users\User\CascadeProjects\T21-RTT-Validator"

echo Adding files...
git add app.py
git add TQUK_QUALIFICATIONS_MASTER_LIST.md
git add TQUK_ALL_QUALIFICATIONS_SUMMARY.md
git add HOW_TO_SEE_LEVEL3_IN_STREAMLIT.md

echo.
echo Committing...
git commit -m "ADD: Level 3 Diploma and IT User Skills to Learning Portal - visible now"

echo.
echo Pushing to GitHub...
git push

echo.
echo ========================================
echo DONE! STREAMLIT WILL AUTO-DEPLOY IN 2-3 MINUTES
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Wait 2-3 minutes
echo 2. Go to: https://share.streamlit.io/
echo 3. Check deployment status
echo 4. Refresh your browser
echo 5. Go to Learning Portal
echo 6. See your new tabs!
echo.
pause
