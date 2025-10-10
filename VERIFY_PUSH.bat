@echo off
echo ========================================
echo CHECKING GIT STATUS
echo ========================================
echo.

cd /d "%~dp0"

echo Current directory:
cd
echo.

echo Checking if git is initialized:
if exist .git (
    echo [OK] Git repository found
) else (
    echo [ERROR] No git repository!
    pause
    exit
)

echo.
echo ========================================
echo INSTRUCTIONS:
echo ========================================
echo.
echo 1. Open GitHub Desktop
echo 2. Make sure you're in "T21-RTT-Validator" repo
echo 3. Check if you see files in "Changes" tab
echo 4. If YES - commit and push
echo 5. If NO - close and reopen GitHub Desktop
echo.
echo After pushing, check GitHub.com to verify
echo the files are there!
echo.
pause
