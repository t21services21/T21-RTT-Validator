@echo off
cls
echo.
echo ========================================
echo    DEPLOYING LEVEL 3 TO STREAMLIT
echo ========================================
echo.
echo This will push all changes to GitHub
echo and make Level 3 available in 5 minutes!
echo.
echo ========================================
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Adding files...
git add .

echo.
echo [2/3] Committing...
git commit -m "Deploy Level 3 Adult Care module - Make it available in dropdown"

echo.
echo [3/3] Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo          DEPLOYMENT STARTED!
echo ========================================
echo.
echo Wait 5 minutes, then:
echo 1. Refresh your browser
echo 2. Go to Manage Access
echo 3. Level 3 will be in the dropdown!
echo 4. Select it and grant to Ijeoma
echo 5. Done!
echo.
echo ========================================
pause
