@echo off
echo ========================================
echo DEPLOYING PDF DOWNLOAD FEATURE
echo ========================================
echo.

cd /d "C:\Users\User\CascadeProjects\T21-RTT-Validator"

echo Adding files...
git add requirements.txt
git add tquk_pdf_converter.py
git add tquk_level3_adult_care_module.py
git add tquk_it_user_skills_module.py
git add tquk_customer_service_module.py
git add tquk_business_admin_module.py

echo.
echo Committing...
git commit -m "ADD: Professional PDF download for TQUK learning materials - students can now download units as formatted PDF documents"

echo.
echo Pushing...
git push

echo.
echo ========================================
echo PDF FEATURE DEPLOYED!
echo ========================================
echo.
echo WHAT'S NEW:
echo.
echo 1. Students can download materials as PDF
echo 2. Professional formatting with TQUK branding
echo 3. Proper headers, footers, and styling
echo 4. Works on all devices
echo.
echo WAIT 2-3 MINUTES FOR DEPLOYMENT
echo Then refresh browser and test!
echo.
pause
