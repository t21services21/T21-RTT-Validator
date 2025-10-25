@echo off
echo ========================================
echo PUSHING ALL TQUK FIXES TO GITHUB
echo ========================================
echo.
echo This will deploy:
echo - Level 3 Adult Care module
echo - Fix for automatic Learning Portal
echo - Fix for duplicate key errors
echo - All 27 unit files
echo.
echo ========================================
echo.

cd /d "%~dp0"

echo Adding all files...
"C:\Program Files\Git\bin\git.exe" add .

echo.
echo Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Add Level 3 Adult Care + Fix automatic Learning Portal + Fix duplicate keys - Students only see assigned modules - All TQUK qualifications ready"

echo.
echo Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ========================================
echo DONE! 
echo ========================================
echo.
echo Wait 5 minutes for Streamlit to deploy.
echo Then go assign Level 3 to Ijeoma!
echo.
pause
