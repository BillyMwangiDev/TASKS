@echo off
echo ========================================
echo    TASKY - Installation Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

echo Installing PyQt6...
python -m pip install PyQt6>=6.9.1

echo Installing win10toast...
python -m pip install win10toast>=0.0.3

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To run TASKY, use: python main.py
echo Or double-click: run.bat
echo.
echo Press any key to test the installation...
pause >nul

echo Testing installation...
python test_app.py

echo.
echo If no errors appeared above, TASKY is ready to use!
echo.
pause
