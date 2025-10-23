@echo off
echo ========================================
echo FIXING UNICODE ERROR AND PUSHING TO GITHUB
echo ========================================
echo.

cd /d "C:\Users\User\CascadeProjects\T21-RTT-Validator"

echo Adding all files...
git add .

echo.
echo Committing...
git commit -m "FIX: UnicodeEncodeError in auth_persistence.py + ADD Level 3 Diploma to Learning Portal"

echo.
echo Pushing to GitHub...
git push

echo.
echo ========================================
echo DONE! 
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Wait 2-3 minutes for Streamlit Cloud to deploy
echo 2. Refresh your browser at: t21-healthcare-platform.streamlit.app
echo 3. Go to Learning Portal
echo 4. See your new Level 3 Diploma and IT User Skills tabs!
echo.
echo OR run locally:
echo 1. Close this window
echo 2. Run: streamlit run app.py
echo 3. Go to Learning Portal
echo.
pause
