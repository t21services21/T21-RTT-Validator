@echo off
echo ========================================
echo DEPLOYING TQUK QUALIFICATION MODULES
echo ========================================
echo.

cd /d "C:\Users\User\CascadeProjects\T21-RTT-Validator"

echo Step 1: Adding all new files...
git add tquk_course_assignment.py
git add tquk_level3_adult_care_module.py
git add tquk_it_user_skills_module.py
git add tquk_customer_service_module.py
git add tquk_business_admin_module.py
git add CREATE_TQUK_TABLES.sql
git add TQUK_MODULES_COMPLETE_GUIDE.md
git add app.py
git add auth_persistence.py

echo.
echo Step 2: Committing changes...
git commit -m "ADD: Complete TQUK qualification modules - 4 standalone courses with assignment system, progress tracking, and materials viewer"

echo.
echo Step 3: Pushing to GitHub...
git push

echo.
echo ========================================
echo DEPLOYMENT INITIATED!
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. CREATE DATABASE TABLES:
echo    - Go to: https://supabase.com
echo    - Open SQL Editor
echo    - Copy contents of CREATE_TQUK_TABLES.sql
echo    - Run the SQL
echo.
echo 2. WAIT FOR STREAMLIT DEPLOYMENT:
echo    - Go to: https://share.streamlit.io/
echo    - Check deployment status
echo    - Wait 2-3 minutes
echo.
echo 3. TEST THE MODULES:
echo    - Refresh your browser
echo    - Log in as teacher
echo    - Go to Teaching ^& Assessment
echo    - Click TQUK Course Assignment tab
echo    - Assign a course to a student
echo    - Log in as that student
echo    - See the module in sidebar!
echo.
echo 4. YOU'LL SEE 4 NEW MODULES:
echo    - 📚 Level 3 Adult Care
echo    - 💻 IT User Skills
echo    - 🤝 Customer Service
echo    - 📊 Business Administration
echo.
echo ========================================
echo READY TO GENERATE £74,230 PROFIT/YEAR!
echo ========================================
echo.
pause
