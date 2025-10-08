@echo off
echo ========================================
echo T21 RTT Pathway Intelligence
echo Starting Application...
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Installing/checking requirements...
python -m pip install -r requirements.txt

echo.
echo Starting Streamlit app...
echo Your browser will open automatically to http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

streamlit run app.py

pause
