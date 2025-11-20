@echo off
echo ========================================
echo  Installing Personal Finance Tracker
echo ========================================

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

:: 2. Create Virtual Environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: 3. Activate and Install
echo Installing dependencies...
call venv\Scripts\activate
pip install -r backend\requirements.txt

echo.
echo ========================================
echo  Installation Complete!
echo  You can now delete the 'frontend' folder.
echo  Use 'run.bat' to start the app.
echo ========================================
pause