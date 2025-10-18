@echo off
echo ========================================
echo DEPLOYING: PBL BOOKING INTEGRATION
echo Critical NHS Workflow Missing Feature
echo ========================================
echo.
echo CRITICAL GAP FIXED:
echo.
echo ❌ BEFORE: Booking fails → Shows alternatives → Dead end
echo ✅ AFTER:  Booking fails → Add to PBL button → Complete workflow
echo.
echo NHS WORKFLOW NOW COMPLETE:
echo.
echo 1. User tries to book appointment
echo 2. No slots available (booking fails)
echo 3. System shows: "Add to Partial Booking List" button
echo 4. User clicks button
echo 5. PBL form appears with patient details pre-filled
echo 6. User completes: DOB, Email, Referral Date, etc.
echo 7. Click "Add to Partial Booking List"
echo 8. Patient added to PBL
echo 9. Acknowledgment email sent automatically
echo 10. Patient monitored for RTT breach risk
echo 11. When slot available → Book and remove from PBL
echo.
echo WHAT WAS ADDED:
echo.
echo  advanced_booking_ui.py:
echo   1. "Add to Partial Booking List" button when booking fails
echo   2. Complete PBL form (DOB, Email, Referral info)
echo   3. Integration with partial_booking_list_system.py
echo   4. Acknowledgment email checkbox
echo   5. Success confirmation with next steps
echo.
echo MATCHES NHS STANDARD PRACTICE:
echo  - Referral accepted but no appointment available
echo  - Add to PBL (not left hanging!)
echo  - Send acknowledgment within 10 working days
echo  - Monitor RTT clock (18-week target)
echo  - Book when slot becomes available
echo  - Auto-remove from PBL when booked
echo.

cd /d "%~dp0"

echo Adding files...
git add advanced_booking_ui.py

echo.
echo Committing...
git commit -m "CRITICAL: Add to PBL when booking fails - NHS workflow complete"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Wait 3 minutes for Streamlit to redeploy.
echo.
echo TESTING:
echo  1. Go to Advanced Booking System
echo  2. Try to book appointment (use fake clinic ID)
echo  3. Booking will fail (no slots)
echo  4. Should see "Add to Partial Booking List" button
echo  5. Click button
echo  6. PBL form appears
echo  7. Fill in details and submit
echo  8. Patient added to PBL!
echo  9. Go to "Partial Booking List" tab to verify
echo.
echo This closes a critical gap in the NHS workflow!
echo.
pause
