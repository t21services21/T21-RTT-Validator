@echo off
echo ========================================
echo PUSHING TQUK FIXES TO GITHUB
echo ========================================
echo.

cd /d "C:\Users\User\CascadeProjects\T21-RTT-Validator"

echo Adding files...
git add .

echo.
echo Committing...
git commit -m "FIX: Admin access to TQUK modules + enhanced materials viewer"

echo.
echo Pushing...
git push

echo.
echo ========================================
echo DONE! WAIT 2-3 MINUTES FOR DEPLOYMENT
echo ========================================
echo.
echo Then:
echo 1. Go to https://share.streamlit.io/
echo 2. Find your app
echo 3. Click "Reboot app" if needed
echo 4. Refresh browser
echo.
pause
