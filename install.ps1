# TASKY - PowerShell Installation Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    TASKY - Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host ""

# Install PyQt6
Write-Host "Installing PyQt6..." -ForegroundColor Blue
python -m pip install "PyQt6>=6.9.1"

# Install win10toast
Write-Host "Installing win10toast..." -ForegroundColor Blue
python -m pip install "win10toast>=0.0.3"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Installation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "To run TASKY, use: python main.py" -ForegroundColor Green
Write-Host "Or double-click: run.bat" -ForegroundColor Green
Write-Host ""

# Test installation
Write-Host "Testing installation..." -ForegroundColor Yellow
python test_app.py

Write-Host ""
Write-Host "If no errors appeared above, TASKY is ready to use!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
