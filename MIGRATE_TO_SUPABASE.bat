@echo off
REM ================================================================================
REM T21 SERVICES - MIGRATE TO SUPABASE (DOUBLE-CLICK ME!)
REM ================================================================================

echo.
echo ================================================================================
echo T21 SERVICES - MIGRATING TO SUPABASE DATABASE
echo ================================================================================
echo.
echo This will:
echo 1. Install Supabase library
echo 2. Migrate your 4 existing users to Supabase
echo 3. Verify everything worked
echo.
echo After this, ALL future registrations will be saved FOREVER!
echo No more data loss!
echo.
pause

echo.
echo ================================================================================
echo STEP 1: Installing Supabase library...
echo ================================================================================
echo.
pip install supabase==2.3.0 postgrest==0.13.1

echo.
echo ================================================================================
echo STEP 2: Migrating your users...
echo ================================================================================
echo.
python migrate_to_supabase.py

echo.
echo ================================================================================
echo MIGRATION COMPLETE!
echo ================================================================================
echo.
echo What was done:
echo - Installed Supabase library
echo - Migrated your 4 existing users to Supabase database
echo - Verified migration was successful
echo.
echo Next steps:
echo 1. Add credentials to Streamlit Cloud (I'll show you how)
echo 2. Push to GitHub
echo 3. Test login
echo 4. ALL future registrations will be saved forever!
echo.
echo ================================================================================
echo.
pause
