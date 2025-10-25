@echo off
cls
echo.
echo ========================================
echo   DEPLOYING LEVEL 3 TO LIVE WEB SYSTEM
echo ========================================
echo.
echo This will make Level 3 work from the web!
echo No more SQL scripts needed!
echo.
echo After this, you can enroll students from:
echo - Teaching ^& Assessment ^> TQUK Course Assignment
echo - Just tick Level 3 and click Assign
echo - Done!
echo.
echo ========================================
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Adding all files...
"C:\Program Files\Git\bin\git.exe" add -A

echo.
echo [2/3] Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "Deploy Level 3 Adult Care module + Fix enrollment system - Make everything work from web UI"

echo.
echo [3/3] Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ========================================
echo          DEPLOYMENT STARTED!
echo ========================================
echo.
echo Wait 5-7 minutes for Streamlit to update.
echo.
echo Then you can enroll students from the web:
echo 1. Go to Teaching ^& Assessment
echo 2. Click TQUK Course Assignment
echo 3. Select student
echo 4. Tick Level 3 Diploma in Adult Care
echo 5. Click Assign Selected
echo 6. Done!
echo.
echo No more SQL scripts!
echo No more command line!
echo Everything from the web!
echo.
echo ========================================
pause
