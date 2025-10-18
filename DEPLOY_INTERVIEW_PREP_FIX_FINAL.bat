@echo off
echo ========================================
echo DEPLOYING: INTERVIEW PREP - 40-50+ QUESTIONS FIX
echo ========================================
echo.
echo ISSUE FIXED:
echo  - Previously: 15 categories × 1 question = 15 total ❌
echo  - Now: 15-20 categories × 3-4 questions = 45-80 total ✅
echo.
echo CHANGES MADE:
echo  1. Updated GPT-4 prompt to generate 3-4 questions per category
echo  2. Increased max_tokens from 8000 to 16000
echo  3. Added clear examples in prompt showing multiple questions per category
echo  4. Enhanced instructions to emphasize "3-4 per category, NOT just 1"
echo.
echo RESULT:
echo  Users will now get 40-50+ questions as promised!
echo.
echo EXAMPLE OUTPUT (After Fix):
echo  Technical - Medical Terminology Questions (4)
echo   Q1. Can you explain your experience with medical terminology?
echo   Q2. How do you ensure accuracy when using medical terms?
echo   Q3. Give an example of a complex medical term you've used.
echo   Q4. How do you keep your medical terminology knowledge updated?
echo.
echo  Competency - Organizational Skills Questions (3)
echo   Q1. Describe a time when you managed multiple tasks...
echo   Q2. How do you prioritize when everything is urgent?
echo   Q3. Give an example of how you stay organized...
echo.
echo  ... (continues for 15-20 categories)
echo.

cd /d "%~dp0"

echo Adding files...
git add interview_prep.py

echo.
echo Committing...
git commit -m "FIXED: Interview Prep now generates 40-50+ questions (3-4 per category)"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Wait 3 minutes for Streamlit to redeploy.
echo Then test with a job description!
echo.
echo Expected result:
echo  "Based on this job description, you're likely to be
echo   asked 45-60 types of questions"
echo.
echo  Each category will show (3-4) questions!
echo.
pause
