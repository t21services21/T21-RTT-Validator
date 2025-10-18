@echo off
echo ========================================
echo DEPLOYING: INTERVIEW PREP - ALL FIXES
echo 1. 40-50+ Questions Fix
echo 2. Professional UX (Hide GPT-4)
echo ========================================
echo.
echo FIXES INCLUDED:
echo.
echo FIX 1: Question Count
echo  - Generate 15-20 categories
echo  - 3-4 questions per category
echo  - Total: 45-80 questions (matches promise!)
echo.
echo FIX 2: Professional UX
echo  - Remove all "GPT-4" references
echo  - Remove technical debug messages
echo  - Clean professional status messages
echo  - Reduce timeout to 30 seconds
echo.
echo CURRENT ISSUES (Your Screenshot):
echo  ❌ Only 21 questions (should be 40-50+)
echo  ❌ Shows "Using GPT-4 AI..." messages
echo  ❌ Shows "Connecting to GPT-4..."
echo  ❌ Shows debug output
echo.
echo AFTER DEPLOYMENT:
echo  ✅ 45-60 questions (15-20 categories)
echo  ✅ "Analyzing your job description..."
echo  ✅ No GPT-4 mentions
echo  ✅ No debug output
echo  ✅ Professional clean interface
echo.

cd /d "%~dp0"

echo Adding files...
git add interview_prep.py

echo.
echo Committing...
git commit -m "Interview Prep: 40-50+ questions + Professional UX (hide GPT-4)"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo ⏰ IMPORTANT: Wait 3-5 minutes for Streamlit to redeploy!
echo.
echo Then test again:
echo  1. Upload a job description
echo  2. Click Generate
echo  3. Should see ~45-60 questions (not 21)
echo  4. Should NOT see "GPT-4" messages
echo  5. Should see clean professional messages
echo.
echo Your current output (21 questions + GPT-4 messages) 
echo will be replaced with new output (45-60 questions, clean UX)!
echo.
pause
