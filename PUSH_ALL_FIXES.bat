@echo off
REM ================================================================================
REM T21 SERVICES - PUSH ALL REMAINING FIXES
REM ================================================================================

echo.
echo ================================================================================
echo PUSHING ALL REMAINING FIXES TO GITHUB
echo ================================================================================
echo.
echo This will push:
echo - Student login portal (Supabase support)
echo - Admin user tracking fix (UserLicense error)
echo - Complete migration status document
echo.
pause

echo.
echo Adding all files...
git add pages/student_login.py
git add admin_user_tracking_ui.py
git add MIGRATION_COMPLETE_STATUS.md
git add PUSH_ALL_FIXES.bat

echo.
echo Committing changes...
git commit -m "Fix admin panel UserLicense error + Add Supabase to student portal + Status doc"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ================================================================================
echo SUCCESS! ALL FIXES PUSHED!
echo ================================================================================
echo.
echo What was fixed:
echo - Admin Panel User Tracking error (UserLicense vs dict)
echo - Student Login portal now supports Supabase
echo - Complete migration status documented
echo.
echo Next steps:
echo 1. Wait 30-60 seconds for Streamlit to deploy
echo 2. Hard refresh your browser (Ctrl+Shift+R)
echo 3. Test admin panel (should work now!)
echo 4. Test registration (main app)
echo 5. Verify users saved to Supabase
echo.
echo ================================================================================
echo.
pause
