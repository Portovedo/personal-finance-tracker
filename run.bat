@echo off
title Personal Finance Tracker
echo Starting Finance Tracker...
echo.

:: Activate the environment
call venv\Scripts\activate

:: Run the python app launcher directly
python backend/run_app.py

pause