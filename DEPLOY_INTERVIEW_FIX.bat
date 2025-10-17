@echo off
echo ========================================
echo DEPLOYING INTERVIEW PREP FIX
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Adding changed files...
git add interview_prep.py
git add INTERVIEW_PREP_ROOT_CAUSE_FIXED.md
git add INTERVIEW_PREP_FALLBACK_FIXED.md

echo.
echo Step 2: Committing changes...
git commit -m "FIX: Interview Prep - Force JSON mode + Smart fallback"

echo.
echo Step 3: Pushing to GitHub (this will auto-deploy to Streamlit)...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your fix is now deploying to Streamlit Cloud.
echo Wait 2-3 minutes, then refresh your browser.
echo.
pause
