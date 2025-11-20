@echo off
echo ==========================================
echo      Switching to Vite (Clean Install)
echo ==========================================

cd frontend

echo [1/3] Cleaning old node_modules and lockfiles...
if exist "node_modules" (
    rmdir /s /q "node_modules"
)
if exist "package-lock.json" (
    del "package-lock.json"
)

echo.
echo [2/3] Installing Vite Dependencies...
call npm install

echo.
echo [3/3] Verifying Vite...
if exist "node_modules\.bin\vite.cmd" (
    echo SUCCESS: Vite found!
) else (
    echo ERROR: Vite installation failed.
)

cd ..
echo.
echo Done. Please ensure you DELETED 'frontend/public/index.html' before running test_app.bat.
pause