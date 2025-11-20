@echo off
SETLOCAL

echo ==========================================
echo      Personal Finance Tracker - Test Mode
echo ==========================================

:: 1. Install Python Backend Dependencies
echo.
echo [1/5] Checking Backend Dependencies...
cd backend
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error installing Python dependencies.
    pause
    exit /b %ERRORLEVEL%
)
cd ..

:: 2. Install Node Frontend Dependencies
echo.
echo [2/5] Checking Frontend Dependencies...
cd frontend
if not exist node_modules (
    echo Installing node_modules...
    call npm install
)
cd ..

:: 3. Build React Frontend
echo.
echo [3/5] Building React Frontend...
cd frontend
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo Error building React app.
    pause
    exit /b %ERRORLEVEL%
)
cd ..

:: 4. Deploy Frontend to Backend Static Folder
echo.
echo [4/5] Copying Frontend to Backend...
:: Remove old static folder if it exists
if exist "backend\app\static" (
    rmdir /s /q "backend\app\static"
)

:: Create directory structure
mkdir "backend\app\static"

:: Copy build files
xcopy /E /I /Y "frontend\build\*" "backend\app\static\"

:: 5. Run the App (Python Mode)
echo.
echo [5/5] Starting Application...
echo Press Ctrl+C in this terminal to stop the server if the window closes.
echo.

cd backend
python run_app.py

pause