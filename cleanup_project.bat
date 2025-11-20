@echo off
echo ==========================================
echo      Fixing Folder Structure
echo ==========================================

if exist "frontend\srcsrc" (
    echo Removing accidental 'srcsrc' folder...
    rmdir /s /q "frontend\srcsrc"
    echo Done.
) else (
    echo 'srcsrc' folder not found. Good.
)

echo.
echo You can now run test_app.bat
pause