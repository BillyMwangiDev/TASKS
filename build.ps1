# TASKY - PowerShell Build Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    TASKY - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Building TASKY executable..." -ForegroundColor Yellow
Write-Host "This will create a standalone .exe file" -ForegroundColor Yellow
Write-Host ""

# Run the build script
python build.py

Write-Host ""
Write-Host "Build process completed!" -ForegroundColor Green
Write-Host "Check the output above for any errors." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
